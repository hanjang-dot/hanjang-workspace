> 한장 FO가 다시 구현하는 선행 기획. 코드를 복사하지 않는다.
> HJ-E3, HJ-E4 — [experience-plan.md](./experience-plan.md)

# SheetKeep

시험지를 고르고 시간 안에 푼다. 끊어도 같은 장으로 돌아온다. 기본 실행이 제품이다.

## 제품

- 목록: 서로 다른 examId 20장, 표지, 연도, 제목
- 세션: 남은 시간, 선지, 제출
- 카드를 눌러야 시험으로 간다
- 중복 강제 메뉴 없음

성공: 목록 → 시험 → 제출. 제출 전 재실행 시 같은 시험·답·시간.

## 오르조

| 오르조 | 구현 |
| --- | --- |
| 시험지 고르기 | LegendList, 키 examId |
| 긴 시험 | deadlineAt, SQLite |
| 앱 전환 | restoring variant |
| 표지 | 보이는 행만 decode |

## HJ-E3 세션 복원

타이머와 답이 재실행 후에도 남는다. 복원 중 선지를 눌러 빈 시험을 덮지 않는다. 목록은 자동으로 시험에 들어가지 않는다.

- Session `{ examId, deadlineAt, answers, inkDraft, status }`
- 남은 시간 = deadlineAt − now
- restoring 동안 onChoice 0

측정: answers JSON 동등, 시간 오차 ≤ 1초, 목록 마운트 후 자동 이동 0.

## HJ-E4 목록

보이는 카드만 살린다. 중복 examId 페이지에서도 다음 시험지가 이어진다. 화면 밖 표지는 decode하지 않는다.

- LegendList `recycleItems`. FlatList 금지
- seenIds, unique 0이면 fetchNext ≤ 5
- 카드 탭 slop

측정: 200행 마운트 ≤ 화면 안 + 윈도우, 표지 decodingCount ≤ 보이는 행.

## 완료

목록 → 제출 한 사이클 + HJ-E3·E4 측정이 같은 빌드에서 통과.
