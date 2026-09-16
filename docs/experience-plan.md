# 한장 — 문제해결 경험 기획서

슈퍼 이력서 `experience_blueprint` 형식. 한장은 쇼케이스가 아니다. FO에서 시험지 한 장을 풀 수 있고, 그 경로가 극단 데이터에서도 같은 화면으로 남는 것이 경험이다.

병목은 L2+L3를 섞는다. 예방은 성능, 안정, 정합성, 유지보수. 제품 코드를 깨지 않는다. fixture만 긴 지문, 겹친 스트로크, 늦은 채점, 프로세스 종료, 중복 목록, 큰 표지를 넣는다.

InkSplit·SheetKeep 코드를 복사하지 않는다. 같은 문제를 `hanjang-fo`에서 다시 구현한다.

---

## 배치

```
한장 FO
├─ 목록 → 시험지 → 채점                         기본 제품
├─ HJ-E1 시험지 레이아웃·펜·히트·지문 이미지     L2
├─ HJ-E2 채점 run · variant                      L3
├─ HJ-E3 세션 복원 · restoring 잠금              L2
└─ HJ-E4 목록 LegendList · 표지 수명             L3
```

BO 발행은 콘텐츠 공급이다. 이력서 문제해결 경험의 본체는 FO 네 개다.

---

## HJ-E1 시험지 화면의 레이아웃·입력 소유권

오르조: 지문 왼쪽, 문항 오른쪽, 스마트펜.

기본 기능: 지문을 스크롤하고, 밑줄 치고, 선지를 고른다.

같은 화면이 막는 실패

1. 긴 지문·필기가 레이아웃 높이에 들어가면 선지 y가 내려간다.
2. overlay 팬이 지문을 같이 스크롤한다.
3. 밑줄 위 선지 탭이 스트로크가 된다.
4. 긴 시험지 PNG를 통째 decode하면 왼쪽이 죽는다.

해결

- `pane-contract.json`으로 문항 폭 고정
- 지문/문항은 형제 ScrollView
- 필기는 absolute overlay. 선지 위는 choice-wins
- 지문 위 수평 팬 = stroke, 빈 곳 세로 = 스크롤
- 지문 이미지는 보이는 타일만 decode
- 펜 점은 Reanimated worklet, UI 스레드

측정

| 항목 | 통과 |
| --- | --- |
| 짧은 PNG vs 긴 PNG, 문항 width | 차이 ≤ 1px |
| 스트로크 20개 후 첫 선지 y | 0 |
| 선지 박스 안 탭 10회 | onChoice 10, onStrokeStart 0 |
| 지문 위 수평 팬 | contentOffset.y 0 |
| 지문 decode | decodingCount ≤ 보이는 타일 |

CI: `pane-contract`. 계약 숫자 변경 시 measure 실패.

---

## HJ-E2 채점 취소와 늦은 점수

오르조: 고르고 바로 채점, 고쳐서 다시.

기본 기능: 선지를 고르면 정오가 붙는다.

같은 코드가 막는 실패: ② 채점 중 ①로 바꾸고 중지해도 첫 점수가 늦게 와 오답 표시가 ②로 남는다.

해결

- `createGradeRun()` + Effect fiber interrupt (ky 경계에서만 AbortSignal)
- 응답 JSON의 `runId`가 현재가 아니면 drop
- 화면은 `idle | grading | graded | aborted | error` variant 키만
- 정답은 `hanjang-be` REST. 지연·드롭은 테스트 헤더만

측정

| 항목 | 통과 |
| --- | --- |
| S1~S5 각 5회 | choiceId와 score.runId 일치 |
| abort 후 늦은 성공 적용 | 0 |
| grading 중 onChoice | 0 |
| 잠금 | `testID=sheet-variant-*` |

CI: `grade-run`.

---

## HJ-E3 시험 세션 복원

오르조: 40~80분 시험 중 전화·홈.

기본 기능: 타이머가 돌고 답을 고르고 제출한다.

같은 코드가 막는 실패: 재실행 후 45:00과 빈 선지, 또는 복원 전에 선지를 눌러 빈 세션을 덮음.

해결

- Session `{ examId, deadlineAt, answers, inkDraft, schemaVersion, status }`
- FO는 SQLite. 서버 session은 백업
- 남은 시간 = deadlineAt − now
- `restoring` 동안 onChoice no-op
- 목록은 탭 없이 시험으로 가지 않는다. 이어하기는 그 카드를 눌렀을 때만

측정

| 항목 | 통과 |
| --- | --- |
| 재시작 후 answers | JSON 동등 |
| 남은 시간 | 오차 ≤ 1초 (fake clock) |
| restoring 중 onChoice | 0 |
| 목록 마운트 후 자동 이동 | 0 |

CI: `session-restore`.

---

## HJ-E4 시험지 고르기

오르조: 회차가 많은 목록, 표지.

기본 기능: 발행된 시험지 카드를 스크롤하고 고른다. 기본 데이터는 서로 다른 회차.

같은 코드가 막는 실패: 중복 examId 페이지에서 목록이 멈추거나, 표지를 전부 decode해 저가 태블릿에서 죽는다.

해결

- LegendList `recycleItems`, 키 `examId`. FlatList 금지
- seenIds. unique 0이면 fetchNext ≤ 5
- 표지는 보이는 행만 decode
- 카드 탭 slop

측정

| 항목 | 통과 |
| --- | --- |
| 200행 초기 마운트 | 화면 안 + recycle 윈도우 이하 |
| 중복 3페이지 | 다음 다른 examId가 이어짐 |
| decodingCount | ≤ 보이는 행 |
| 목록 주어 | 시험지 고르기. 라이브러리 데모 아님 |

CI: `sheet-list`.

---

## 작업 순서

제품이 한 사이클 된 뒤에 극단 fixture를 잠근다.

1. FO 목록 → 시험지 → 채점 (목 또는 발행 1장)
2. HJ-E1 pane·펜·히트·이미지
3. HJ-E2 GradeRun + BE 정답
4. HJ-E3 SQLite 세션. 자동 이동 없음
5. HJ-E4 LegendList + 표지
6. BO 발행이 FO 목록에 반영

---

## 이력서에 쓰는 문장

한장 FO에서 시험지 한 장을 푼다. 지문이 밀려도 선지가 그대로고, 펜이 스크롤을 먹지 않고, 취소한 채점이 다음 답을 덮지 않고, 나갔다 돌아와도 같은 장이고, 목록은 보이는 카드만 살린다.

---

## 완료

- FO 기본 실행으로 한 장을 채점까지 끝낸다
- HJ-E1~E4 측정과 CI가 같은 빌드에서 통과한다
- InkSplit·SheetKeep 저장소를 한장 경험으로 다시 쓰지 않는다
