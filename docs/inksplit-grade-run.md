> 한장 FO가 다시 구현하는 선행 기획. InkSplit·SheetKeep 저장소 코드를 복사하지 않는다.
> 한장 경험 번호는 [experience-plan.md](./experience-plan.md) HJ-E2.

# IS-E2 채점이 기본으로 되고, 고쳐 다시 보내도 결과가 안 섞인다

이 경험은 채점 버튼의 기본 기능이다. 고르고 채점하면 정오가 붙는다. 중지·늦은 응답 fixture는 그 채점이 이전 답을 덮지 못하게 잠근다. 레이스 데모 앱이 아니다.

프로젝트: InkSplit  
경험: 2/2  
공고: 슬링 React Native  
레벨: L3  
회사 밀착: 필수. 선지 고르고 바로 채점, 틀리면 고쳐서 다시. 채팅 abort를 이식하지 않음.

프론트 코드로 증명하는 것
- 화면 상태의 소유자가 fetch가 아니라 `gradeRunId`
- AbortSignal + generation. 늦은 JSON을 reducer가 버림
- `idle|grading|graded|aborted|error`를 variant 키로만 그림. 인라인 색 없음
- grading 중 선지 잠금이 testID로 보임
- CI가 S1~S5와 variant 키를 같이 봄

## 문제 (오르조에서 나는 실패)

수험생이 ② 채점 중 ①로 바꾸고 중지한다. 첫 자동채점이 늦게 오면 선지는 ①인데 오답 표시는 ②다. 버튼은 opacity만 낮춰 잠금인지 로딩인지 안 보인다. 오르조는 짧은 이터레이션으로 답을 고친다. 이 레이스가 제품 신뢰다.

## 해결

`createGradeRun()`. 응답·에러·flush 전 `payload.runId === current`. 화면은 variant 맵만. fixture가 지연·드롭·역순을 넣음.

## 병목 fixture

- 800ms~3000ms
- 취소 후 200, 취소 후 5xx
- 선택 변경과 이전 버퍼 교차 5종
- variant 키 없이 backgroundColor로 잠그면 테스트 실패

## 기술

1. GradeRun `{ id, signal, generation }`
2. POST body에 runId. 없으면 drop
3. 중지 시 current를 새 idle 세대로 교체
4. `sheetVariant` → 선지 disabled, 중지 버튼, 점수 영역
5. 테스트는 `testID=sheet-variant-grading`을 읽음

## 측정

| 항목 | 통과 |
|---|---|
| S1~S5 각 5회 | choiceId와 score.runId 일치 |
| abort 후 늦은 성공 적용 | 0 |
| 취소된 run 큐 | 길이 ≤ 1 |
| grading 중 onChoice | 0 |
| 잠금 표현 | variant testID. 색 문자열이 아님 |

## 테스트 / CI

CI job `grade-run`: S1~S5 + 각 단계 variant.  
실네트워크 없음.

## 완료

늦은 점수 0회와 variant 키 단언이 둘 다 있어야 완료. 값만 맞고 화면 키가 없으면 미완료.
