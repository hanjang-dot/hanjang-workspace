> 한장 FO가 다시 구현하는 선행 기획. InkSplit·SheetKeep 저장소 코드를 복사하지 않는다.
> 한장 경험 번호는 [experience-plan.md](./experience-plan.md) HJ-E3.

# SK-E1 시험을 보다가 나갔다 돌아와도 같은 시험이다

이 경험은 시험 세션의 기본 기능이다. 타이머가 돌고 답을 고르고 제출한다. 프로세스 종료 fixture는 그 세션이 리셋되지 않게 잠근다. 복원 데모 버튼이 없다.

프로젝트: SheetKeep  
경험: 1/2  
공고: 슬링 React Native  
레벨: L2  
회사 밀착: 필수. 40~80분 모의고사 중 전화·홈. 주문 재시도 이력이 아님.

프론트 코드로 증명하는 것
- 타이머를 elapsed state가 아니라 `deadlineAt`으로 그림
- 답·필기 초안을 화면 모델로 직렬화해 SQLite에 씀
- 부팅 후 `variant=restoring` 동안 선지 핸들러 no-op
- submitted 화면은 읽기 전용 variant
- CI가 재시작 fixture에서 answers JSON과 variant를 읽음

## 문제 (오르조에서 나는 실패)

시험 중 앱이 내려간다. 다시 열면 45:00과 빈 선지. 또는 복원 전에 ③을 눌러 빈 세션을 덮는다. 수능 앱에서 이건 시간 도둑이다.

## 해결

Session `{ examId, deadlineAt, answers, inkDraft, schemaVersion, status }`. upsert. restoring 게이트. 같은 설치만.

## 병목 fixture

- 프로세스 종료. 메모리 버리고 DB만
- wall clock으로 백그라운드 차감
- restoring 중 탭 fixture
- DB 손상 시 빈 시험으로 덮지 않음

## 기술

1. 답 변경마다 upsert
2. 표시 시간 = deadlineAt - now
3. boot load 완료 전 variant=restoring
4. v1→v2 inkDraft 마이그레이션 테스트 1

## 측정

| 항목 | 통과 |
|---|---|
| 재시작 후 answers | JSON 동등 |
| inkDraft | 동등 |
| 남은 시간 | 오차 ≤ 1초 (fake clock) |
| restoring 중 onChoice | 0 |
| submitted 수정 쿼리 | 0 |
| 잠금 | `testID=session-variant-restoring` |

## 테스트 / CI

CI job `session-restore`: 언로드 후 재load + variant.  
다중 기기 동기화는 완료 기준이 아님.

## 완료

값 복원과 restoring 입력 0과 variant 키가 같이 통과해야 완료.
