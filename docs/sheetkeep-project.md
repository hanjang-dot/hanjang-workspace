> 한장 FO가 다시 구현하는 선행 기획. InkSplit·SheetKeep 저장소 코드를 복사하지 않는다.
> 한장 경험 번호는 [experience-plan.md](./experience-plan.md) HJ-E3, HJ-E4.

# SheetKeep 프로젝트 기획서

슬링 React Native. 오르조처럼 **시험지를 고르고 시간 안에 푸는 앱**이다.  
저장소 `sheetkeep` 미생성. InkSplit과 모노레포 금지.

문제해결 쇼케이스가 아니다. 앱을 켜면 시험지 목록이 있고, 하나를 열어 시험을 보고, 제출한다. 전화 때문에 나갔다 돌아와도 같은 시험이다. 그 경로가 긴 목록·중복 페이지·프로세스 종료에서도 같은 제품으로 남는 것이 문제해결이다.

## 기준

1. **정상 작동이 본체.** 기본 실행에서 시험지 고르기 → 시험 → 제출이 된다. 스트레스 목록을 기본 화면으로 두지 않는다.
2. **회사에 붙는다.** 모의고사 타이머, 수능·공무원 시험지 카드. 주문·상품·종목이면 폐기. README가 라이브러리 소개면 폐기.
3. **문제해결은 그 기능 안에 있다.** 복원 데모 버튼, “중복 페이지 강제” 메뉴 없음.
4. **프론트 코드가 남는다.** 카드 목록은 LegendList. 주어는 시험지 고르기다.

---

## 제품 (기본 실행)

수험생이 시험지를 고르고 제한 시간 안에 푼다.

화면 1 목록
- 시험지 카드: 제목, 연도, 표지
- 기본 데이터: 서로 다른 examId 20개 (수능·모의·공무원 이름)
- 카드를 누르면 그 시험이 시작된다

화면 2 세션
- 남은 시간, 문항, 선지, 제출
- 답을 고르면 남는다
- 제출하면 더 못 고친다

기본 서버
- 페이지마다 다른 시험지
- 표지 보통 크기
- 중복 페이지 없음

성공 기준 (사람이 씀)
- 목록에서 시험지가 보인다
- 하나를 열어 선지를 고를 수 있다
- 제출할 수 있다
- 앱을 종료했다 다시 켜도, 제출 전이면 같은 시험·같은 답·남은 시간이다

하지 않는 일
- 계정, 이용권, 실시간 순위
- 실행 중 “프로세스 죽이기” QA 버튼

---

## 그 안에 포함된 문제해결

| 기능 | 기본에서 하는 일 | 같은 코드가 막아내는 일 | 경험 |
|---|---|---|---|
| 시험 세션 | 시간 안에 풀고 제출 | 앱이 죽어도 같은 설치에서 이어짐 | SK-E1 |
| 복원 | 다시 켜면 그 시험 | 복원 중에 선지를 눌러 빈 시험을 덮지 않음 | SK-E1 |
| 시험지 목록 | 카드를 스크롤하고 고름 | 시험지가 많아도 보이는 카드만 살림 | SK-E2 |
| 목록 페이지 | 다음 시험지가 이어짐 | 같은 시험지 ID만 있는 페이지에서도 다음을 받음 | SK-E2 |
| 표지 | 카드에 표지가 보임 | 화면 밖 표지는 decode하지 않음 | SK-E2 |

200행·중복 3페이지·큰 PNG는 테스트 fixture. 기본 목록이 아니다.

---

## 오르조 대응

| 오르조 | 기본 제품 | 같은 구현의 버팀 |
|---|---|---|
| 시험지 고르기 | 카드 목록 | LegendList recycle |
| 긴 시험 | 타이머 + 제출 | deadlineAt, SQLite |
| 앱 전환 | 다시 열면 이어짐 | restoring variant |
| 표지 | 카드 이미지 | 보이는 행만 decode |

---

## 폴더

```
sheetkeep/
  src/app/App.tsx
  src/screens/sheet-list-screen.tsx
  src/screens/session-screen.tsx
  src/features/session/
  src/features/list/
  src/storage/sqlite.ts
  src/mock/sheet-server.ts          # 기본은 unique 20장
  fixtures/cover-normal.png
  fixtures/cover-large.png          # 테스트만
  contracts/
  __tests__/
  .github/workflows/ci.yml
```

---

## 작업 순서

먼저 고르고 푼다. 그다음 같은 경로를 극단 fixture로 잠근다.

| ID | 작업 | 종류 |
|---|---|---|
| K0 | Expo, Jest, CI | 기본 |
| K1 | 목록 20장, 카드 탭 → 세션 | 정상 작동 |
| K2 | 선지 선택, 타이머, 제출 | 정상 작동 |
| K3 | 종료 후 재실행 시 이어짐 | 정상 작동 + SK-E1 |
| K4 | restoring 중 입력 차단 + variant | SK-E1 |
| K5 | 시험지 카드 LegendList | 정상 작동 목록 |
| K6 | 중복 페이지에서도 다음 시험지 | SK-E2 |
| K7 | 표지 decode 수명 | SK-E2 |
| K8 | 마운트·decode CI | SK-E2 |
| K9 | README: 앱이 하는 일 먼저 | 서류 |

K1~K3가 사람 손으로 안 되면 이후 작업을 완료로 치지 않는다.

---

## 완료 기준

정상 작동
- 목록 → 시험 → 제출 한 사이클
- 제출 전 재실행 시 같은 시험
- 기본 목록이 unique 시험지

문제해결 (같은 빌드)
- CI `session-restore`, `sheet-list`
- 복원 중 입력 0
- 중복 페이지 뒤 다음 시험지
- 표지 decode 상한
- 카드 탭이 스크롤에 안 먹힘

제외: 다중 기기, FlatList 폴백, dadamjang 리스트 복사

## 스택

React Native, JavaScript, TypeScript, Android, iOS  
목록: `@legendapp/list`  
Expo, SQLite, Jest

## 구현 지시 (승인 후)

create-expo-app. K0→K3 먼저. 큰 표지·중복은 테스트 mock만.
