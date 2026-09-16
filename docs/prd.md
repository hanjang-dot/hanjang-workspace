# 한장 — PRD

제품 요구사항 문서. 근거는 [서비스 기획서](./service-plan.md), [스택 기획서](./stack-plan.md), [문제해결 경험 기획서](./experience-plan.md). 셋과 충돌하면 이 문서가 아니라 원문을 고친다.

---

## 1. 배경

수험생은 종이 시험지를 태블릿+펜으로 옮기고 싶다. 오르조가 푸는 문제는 같지만, 한장은 그중 **시험지 한 장을 펼쳐 시간 안에 푸는 루프**만 제품으로 가져간다.

## 2. 목표

- 발행된 실제 기출 한 장을 FO에서 처음부터 채점까지 끝낸다.
- 긴 지문, 늦은 채점, 중복 목록, 프로세스 종료에서도 같은 화면·같은 답·같은 시간으로 돌아온다.
- BO가 시험지·문항·정답을 올리고 발행하면 FO 목록에 나타난다.

비목표: AI 코치, 해설 LLM, 오답 소셜, 랭킹, LMS, 한능검·공무원·LEET, 다중 기기 동기화.

## 3. 사용자

| 앱 | 누구 | 목표 |
| --- | --- | --- |
| FO (Expo) | 수험생 | 회차를 고르고 한 장을 시간 안에 푼다 |
| BO (Next.js) | admin | 시험지·문항·선지·정답·퀴즈를 올리고 발행한다. MCP도 같은 admin 계정 |

계정: 카카오·전화 인증. JWT access/refresh.

## 4. 기능 요구사항

### FO

탭 5개: 홈·자료실·저장·복습·마이. 시험지·결과는 탭 밖 스택 화면.

| ID | 탭 | 요구사항 | 수용 기준 |
| --- | --- | --- | --- |
| FR-FO-1 | 홈 | 진행 중 세션 이어하기 카드, 오늘의 퀴즈, 최근 발행 회차. 카드 탭으로만 진입, 자동 이동 없음 | 마운트 후 자동 이동 0 |
| FR-FO-1a | 홈→퀴즈 | 오늘의 퀴즈 4종: OX·빈칸·영단어·한국사. `Quiz { type, prompt, choices, answer, direction }`. 선지 OX 2개, 영단어 6개, 나머지 5개 | 카드 탭 → 세트 시작 |
| FR-FO-1b | 홈→퀴즈 | 세트 10문제, 문항마다 즉시 정오. GradeRun 재사용, 시간 제한 없음. 영단어는 세트 안에서 en→ko / ko→en 번갈아 노출 | abort 후 늦은 성공 적용 0. grading 중 onChoice 0. 세트 내 direction 교대 |
| FR-FO-1c | 홈→퀴즈 | 세트 결과에 정답 수 + 틀린 문항 리스트. 틀린 퀴즈는 로컬에 저장해 복습 탭에서 다시 보기 | 결과 → 틀린 문항 복습 탭 노출 |
| FR-FO-2 | 자료실 | 발행된 시험지를 회차 카드 목록으로 보여 준다. LegendList, 키 `examId` | 200행 초기 마운트가 화면 + recycle 윈도우 이하. 중복 3페이지여도 다음 다른 `examId`가 이어진다. 표지는 보이는 행만 decode |
| FR-FO-3 | 저장 | 회차 북마크 토글·목록. 로컬 저장, 서버 없음 | 재시작 후 북마크 유지 |
| FR-FO-4 | 복습 | 채점 끝난 세션 목록. 정오·내 답 다시보기. 로컬 SQLite의 graded 세션 | 목록 → 결과 재표시, read-only |
| FR-FO-5 | 마이 | 계정 정보 표시, 로그아웃 | 로그아웃 → 로그인 화면 |
| FR-FO-6 | 시험지 | 왼쪽 지문(이미지), 오른쪽 선지 5개. 형제 ScrollView, 문항 폭 `pane-contract.json`. 폰은 지문 위·선지 아래 세로 배치 | 짧은/긴 PNG 간 문항 폭 차이 ≤ 1px. 스트로크 20개 후 첫 선지 y 변화 0. 폰·태블릿 둘 다 동작 |
| FR-FO-7 | 시험지 | 펜 밑줄은 absolute overlay. 선지 위는 choice-wins. 지문 위 수평 팬은 stroke, 빈 곳 세로는 스크롤. Reanimated worklet | 선지 박스 안 탭 10회 = onChoice 10, onStrokeStart 0. 지문 위 수평 팬 시 contentOffset.y 0 |
| FR-FO-8 | 시험지 | 긴 지문 PNG는 보이는 타일만 decode | decodingCount ≤ 보이는 타일 |
| FR-FO-9 | 시험지 | 선지 선택 즉시 채점. `createGradeRun()` + Effect fiber interrupt. 응답 `runId`가 현재가 아니면 drop. variant `idle \| grading \| graded \| aborted \| error` | S1~S5 각 5회 choiceId와 score.runId 일치. abort 후 늦은 성공 적용 0. grading 중 onChoice 0 |
| FR-FO-10 | 시험지 | 세션 `{ examId, deadlineAt, answers, inkDraft, schemaVersion, status }`를 expo-sqlite에 저장. 남은 시간 = deadlineAt − now. 서버 session은 백업 | 재시작 후 answers JSON 동등. 남은 시간 오차 ≤ 1초 (fake clock) |
| FR-FO-11 | 시험지 | `restoring` 동안 onChoice no-op | restoring 중 onChoice 0 |
| FR-FO-12 | 결과 | 이 장의 정오를 보여 준다. 다음 장 자동 이동 없음 | 제출 → 결과 표시 → 종료 |

### BO

| ID | 요구사항 | 수용 기준 |
| --- | --- | --- |
| FR-BO-1 | admin 로그인 (아이디·비밀번호). Admin 테이블, 수험생 User와 별개 | admin JWT 발급 |
| FR-BO-1a | root admin은 시드로 생성. 모든 admin 동일 권한, 계층 없음 | 시드 후 root 로그인 가능 |
| FR-BO-1b | 관리자 초대: 링크 생성 → 복사해 전달. 메일 발송 없음. 링크에서 아이디·비밀번호 설정하면 admin 생성. `AdminInvite { token, expiresAt, usedAt }` | 만료·사용済 링크는 거부. 모든 admin이 발급 가능 |
| FR-BO-2 | 시험지 목록·생성 (회차, 과목, 연도, 표지, 제한 시간) | CRUD 동작 |
| FR-BO-3 | 문항 편집 (지문 영역, 프롬프트, 선지, 정답) | 저장한 문항이 그대로 읽힌다 |
| FR-BO-4 | 발행 / 숨김 | 발행분만 FO 목록에 노출. 숨김은 사라진다 |
| FR-BO-5 | 퀴즈 편집 (type `ox \| cloze \| word \| history`, 프롬프트, 선지, 정답, direction), 발행 | 발행분만 FO 오늘의 퀴즈에 노출 |

### MCP

| ID | 요구사항 | 수용 기준 |
| --- | --- | --- |
| FR-MCP-1 | hanjang-be가 MCP 엔드포인트를 노출. 문항·퀴즈 추가 도구 (`add_question`, `add_quiz`) | 도구 호출 → BO와 같은 데이터로 저장 |
| FR-MCP-2 | admin JWT Bearer 검사 | 수험생 토큰·토큰 없음 거부 |
| FR-MCP-3 | MCP로 추가한 문항·퀴즈는 BO에서 조회·편집·발행 가능 | 같은 테이블, 같은 목록에 표시 |

## 5. 데이터

User, Admin, AdminInvite, ExamPaper, Question, ExamSession, Answer, Stroke, Quiz, QuizSession. 채점은 서버 정답 + `gradeRunId`. Stroke는 기기 로컬 우선, 서버는 초안 백업만. QuizSession은 deadline 없음. 스키마는 hanjang-be REST API가 계약이고 `packages/api`가 따른다.

## 6. 비기능

- FO: Expo New Architecture, Unistyles만 (`style={{}}` 금지), LegendList만 (FlatList 금지), TanStack Query + Zustand + ky.
- BE: NestJS 11, REST, Drizzle, Postgres 16.
- 정합성 CI 4개: `pane-contract`, `grade-run`, `session-restore`, `sheet-list`. 같은 빌드에서 전부 통과해야 한다.
- 오르조 콘텐츠를 긁지 않는다. 평가원·교육청 공개 기출과 BO 발행분만.

## 7. 출시 기준

- FO에서 발행된 시험지 한 장을 처음부터 채점까지 끝낸다.
- 제출 전 재실행 시 같은 장, 같은 답, 남은 시간.
- BO에서 올린 문항이 FO 목록에 나타난다.
- HJ-E1~E4 측정과 CI가 같은 빌드에서 통과한다.
- TestFlight / 내부 배포 한 빌드.

## 8. 마일스톤

| # | 내용 | 완료 신호 |
| --- | --- | --- |
| M1 | hanjang-be에 demo-backend 뼈대 이식, 한장 이름으로 인증 | 로그인 토큰 발급 |
| M2 | hanjang-fe 워크스페이스, tokens/api 패키지 | lint·빌드 통과 |
| M3 | FO 목록 → 시험지 골격, 목 데이터 한 사이클 | 화면 전환 동작 |
| M4 | BE exam/question/session/grade, FO 실 API 연결 | 발행 1장 풀기 |
| M5 | BO 발행 화면 | 발행분이 FO에 노출 |
| M6 | HJ-E1~E4 극단 fixture 잠금 | CI 4개 통과 |
