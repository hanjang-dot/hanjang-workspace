> 한장 FO가 다시 구현하는 선행 기획. InkSplit·SheetKeep 저장소 코드를 복사하지 않는다.
> 한장 경험 번호는 [experience-plan.md](./experience-plan.md) HJ-E1.

# IS-E1 시험지 화면이 긴 지문·펜에서도 그대로 풀린다

이 경험은 시험지 화면의 기본 기능이다. 지문 보기, 밑줄, 선지 탭이 기본 실행에서 된다. 긴 PNG·겹친 스트로크는 그 화면을 깨지 못하게 잠그는 테스트다. 병목 데모 화면이 아니다.

프로젝트: InkSplit  
경험: 1/2  
공고: 슬링 React Native  
레벨: L2  
회사 밀착: 필수. 지문 왼쪽 / 문항 오른쪽, 스마트펜 필기, 태블릿 가로. 채팅·호가·장바구니 금지.

프론트 코드로 증명하는 것
- Yoga 트리에서 필기 bbox가 문항 레이아웃에 안 들어감
- 지문 `ScrollView`와 문항 `ScrollView`가 높이를 공유하지 않음
- 지문 위 팬 = stroke, 빈 곳 세로 = 스크롤, 선지 탭 = onChoice (한 PanResponder가 셋 다 먹지 않음)
- 선지 위 overlay `pointerEvents`로 히트 위임
- 왼쪽 지문은 긴 시험지 PNG. 보이는 구간만 decode
- `pane-contract.json` 숫자가 바뀌면 CI measure가 실패

## 문제 (오르조에서 나는 실패)

오르조는 태블릿에서 지문과 문항을 한 화면에 두고 펜으로 밑줄친다. 시안은 짧은 지문이다. 실제 국어 지문은 길고, 시험지는 이미지다.

실패 네 개가 한 화면에서 같이 난다.
1. 필기·이미지를 지문 레이아웃 자식으로 두면 문항 첫 선지 y가 내려간다.
2. overlay를 통째 pan으로 받으면 밑줄 치다가 지문이 움직인다.
3. 밑줄이 선지를 덮으면 ① 탭이 스트로크가 된다.
4. 긴 시험지 PNG를 통째 decode하면 문항 트리가 살아 있어도 왼쪽이 죽는다.

이건 웹 그리드 문제가 아니다. RN 태블릿 시험지 문제다.

## 해결

`pane-contract.json`으로 문항 폭을 고정. 지문 이미지는 overlay/별도 레이어. 입력은 역할로 분리. 이미지 load는 지문 viewport에 보이는 타일만.

## 병목 fixture

- 짧은 지문 PNG vs 세로 4000px 시험지 PNG
- 선지 박스와 겹치는 스트로크
- 문항 폭 wrap 금지
- 동시 decode는 지문 viewport 타일 수 이하

제품 코드에 sleep 넣지 않음.

## 기술

1. 형제 두 ScrollView. 문항 width는 계약 px
2. InkOverlay absolute. 선지 영역 `pointerEvents="none"` 또는 hit 위임
3. RNGH 또는 PanResponder: 수평 우세 팬 → stroke, 수직 우세 → scroll, tap slop 안 → 선지에 위임
4. 지문 이미지는 세로 타일. 화면 밖 타일 unmount 시 decode 취소
5. measure로 문항 pane width, 첫 선지 y를 테스트

## 측정 (프론트 코드가 남는 숫자)

| 항목 | 통과 |
|---|---|
| 짧은 PNG vs 4000px PNG, 문항 width | 차이 ≤ 1px |
| 스트로크 20개 후 첫 선지 y | 차이 0 |
| 선지 박스 안 탭 10회 | onChoice 10, onStrokeStart 0 |
| 지문 위 수평 팬 40pt | contentOffset.y 0, stroke 점 증가 |
| 빈 곳 수직 드래그 | offset.y 증가, 새 stroke 0 |
| 지문 decode 중 | decodingCount ≤ 보이는 타일 |

## 테스트 / CI

- Jest 합성 gesture + Image mock decode 카운터
- CI job `pane-contract`: 계약 JSON 숫자 변경 시 measure 스냅샷 실패
- 실기기 펜 압력은 제외. 실패해도 이력서에 안 씀

## 완료

레이아웃·제스처·히트·지문 이미지 네 측정이 모두 통과해야 IS-E1 완료. 하나라도 빼면 미완료.
