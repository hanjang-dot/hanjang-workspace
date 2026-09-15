> 한장 FO가 다시 구현하는 선행 기획. 코드를 복사하지 않는다.
> HJ-E1, HJ-E2 — [experience-plan.md](./experience-plan.md)

# InkSplit

태블릿 가로 시험지. 지문을 읽고, 밑줄 치고, 선지를 고르고, 채점한다. 기본 실행이 제품이다.

## 제품

- 왼쪽 지문, 오른쪽 선지 5개
- 펜 밑줄, 채점, 중지 후 다시 채점
- 기본 지문은 1페이지, 채점 200~400ms
- Delay/Drop 버튼 없음

성공: 선택 → 채점 → 정오. 중지 후 새 결과만 보인다.

## 오르조

| 오르조 | 구현 |
| --- | --- |
| 지문 왼쪽 문항 오른쪽 | 형제 ScrollView, pane-contract |
| 스마트펜 | overlay, pan vs scroll vs tap |
| 바로 채점 | GradeRun, 늦은 JSON drop |

## HJ-E1 레이아웃·펜·히트·이미지

긴 지문·필기가 선지를 밀지 않는다. 펜이 스크롤을 먹지 않는다. 밑줄 위 선지가 눌린다. 긴 PNG는 보이는 타일만 decode.

- 문항 폭 `pane-contract.json` 420px
- 필기 absolute. 선지 choice-wins
- 수평 팬 = stroke, 세로 = 스크롤
- Reanimated worklet, UI 스레드

측정: 폭 차이 ≤ 1px, 선지 y 0, 선지 탭 시 stroke 0, decode ≤ 보이는 타일.

## HJ-E2 채점 run

고르고 채점하면 정오가 붙는다. 중지한 점수가 다음 답을 덮지 않는다.

- `gradeRunId` + AbortSignal
- variant `idle | grading | graded | aborted | error`
- S1~S5: 늦은 성공 적용 0, grading 중 onChoice 0

## 완료

기본 한 사이클 + HJ-E1·E2 측정이 같은 빌드에서 통과.
