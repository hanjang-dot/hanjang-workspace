status: confirmed
confirmed_at: 2026-09-16
preview: design/probes/rules-preview.html

# Design Rules — 한장

## A. 토큰

| 키 | 값 | 출처 |
|---|---|---|
| color.bg | #F6F4FB | 축 1: A 밝은 라이트 |
| color.surface-1 | #FFFFFF | 축 1: A |
| color.surface-2 | #EFEBFD | 축 1: A |
| color.text | #17142B | 축 1: A |
| color.text-muted | #8B87A3 | 축 1: A |
| color.border | #ECE9F6 | 축 1: A |
| color.accent | #6C5CE7 | 축 4: A 바이올렛 |
| color.accent-pressed | accent를 12% 어둡게 | 자동 |
| color.accent-soft | accent 10% 불투명 | 자동 |
| color.danger | #F0506E | 3단계 퀴즈 시안 |
| color.overlay | rgba(0,0,0,.5) | 고정 |
| space.scale | 4 / 8 / 12 / 16 / 24 / 32 / 48 | 기본값 |
| space.screen-padding | 좌우 16 | 축 2: B 중간 |
| space.section | 24 | 축 2: B 중간 |
| space.card-padding | 16 | 축 2: B 중간 |
| radius | sm 8 / md 12 / lg 16 / xl 22 / full 9999 | 축 3: C 큰 라운드 |
| shadow | sm 0 2px 8px rgba(80,70,160,.08) / md 0 8px 24px rgba(80,70,160,.12) | 축 3: C |
| font.family | "IBM Plex Sans KR", -apple-system, Roboto, sans-serif | 축 5: B |
| type.roles | display 28/700 Noto Serif KR · h1 24/700 Noto Serif KR · h2 20/600 · h3 17/600 · body 15/400 · body-sm 14/400 · caption 12/400 · label 13/500 (line-height 1.5, 제목 1.3). 문항 텍스트는 serif | 축 5: B 제목 세리프+본문 고딕 |
| z.scale | base 0 · sticky 100 · app-bar 200 · tab-bar 200 · overlay 300 · sheet 400 · dialog 500 · snackbar 600 | 고정 |
| motion | 200ms ease-out. 시트 250ms. crossfade 150ms | 고정 |
| device.frame | 390×844 기준. 검증 폭 360 / 390 / 430 | 1단계 플랫폼 |
| safe-area | 상단 44(노치 47) · 하단 34. 콘텐츠·고정 바는 안쪽 | 고정 |
| tap.min | 44×44. 인접 탭 영역 간격 최소 8 | 고정 |
| platform | iOS·Android 공통 1벌. 네이티브 Stack·탭바·시트 우선 | 1단계·3단계 네이티브 지시 |

## B. 컴포넌트 규칙

| 키 | 값 | 출처 | 사용 여부 |
|---|---|---|---|
| button.sizes | sm 36h / px12 / text14 · md 44h / px16 / text15 · lg 52h / px20 / text16 | 기본값 |  |
| button.radius | radius.lg 16, 풀폭 CTA는 radius.xl 22 | 축 3: C |  |
| button.variants | primary(accent bg, 흰 글자) · secondary(surface-1 bg, text) · ghost(투명, accent 글자) · danger | 기본값 |  |
| button.states | default · pressed(배경 12% 명도 변화, 글자·아이콘 색 유지) · selected(accent-soft bg + accent 1px border) · disabled(opacity .4) · loading(스피너 20, 라벨 숨김, 폭 유지) | 기본값 |  |
| button.row-rule | 같은 줄의 버튼은 같은 size·radius. 두 개면 secondary 왼쪽, primary 오른쪽 | 기본값 |  |
| button.text | 한 줄. 넘치면 문구를 줄인다 | 기본값 |  |
| button.primary-per-screen | 화면당 primary 1개. 하단 고정 바 | 2단계 플로우 |  |
| button.duplicate | 같은 동작을 앱바와 본문에 이중 배치 금지 | 기본값 |  |
| icon.set | lucide 단일. 공식 SVG만, 변형·조합 금지 | 기본값 |  |
| icon.sizes | 16 / 20 / 24 | 기본값 |  |
| icon.stroke | 16→1.5 / 20→1.75 / 24→2 | 기본값 |  |
| icon.gap | 텍스트와 8px, 수직 중앙 | 기본값 |  |
| icon-button.hit | 탭 영역 44×44. 앱바 아이콘 버튼 시각 24 / 탭 44 | 기본값 |  |
| icon-button.name | 아이콘만 있는 버튼 접근성 라벨 필수. 탭바 아이콘은 텍스트 라벨 동반 | 기본값 |  |
| icon.state | 버튼 상태 색을 아이콘도 따른다 | 기본값 |  |
| icon.overflow-menu | 앱바 액션 최대 2개 노출, 점 세 개 뒤에 자주 쓰는 액션 숨기지 않음 | 기본값 |  |
| icon.proximity | 액션 아이콘은 대상 옆. 목록 행 액션은 우측 끝 | 기본값 |  |
| tap.feedback | 모든 탭 가능 요소에 pressed 시각 반응 | 기본값 |  |
| tap.long-press | 롱프레스는 보조 액션에만 | 기본값 |  |
| image.fit-by-purpose | 시험지 지문 이미지 = contain + surface-2 배경. 전체가 보여야 함 | 1단계 PRD |  |
| image.aspect | 컨테이너 비율 고정, 로딩 전 높이 유지 | 기본값 |  |
| thumbnail.spec | | | (미사용) |
| thumbnail.strip | | | (미사용) |
| thumbnail.title | | | (미사용) |
| thumbnail.pressed | | | (미사용) |
| thumbnail.selected | | | (미사용) |
| thumbnail.selected-visible | | | (미사용) |
| image.transition | 다음 이미지 준비 전까지 이전 유지, crossfade 150ms | 기본값 |  |
| image.placeholder | 로딩 = surface-2 스켈레톤, 실패 = surface-2 + 아이콘 24 | 기본값 |  |
| text.role-lock | 같은 역할 = 같은 type.role | 기본값 |  |
| text.truncate | 카드 제목 2줄, 목록 제목 1줄, 설명 3줄 | 기본값 |  |
| text.short-copy | 버튼·짧은 안내 한 줄 | 기본값 |  |
| text.long-copy | 긴 안내 body-sm, 별도 행 | 기본값 |  |
| text.scale | 시스템 글자 확대 120%에서 깨지지 않게 높이 auto | 기본값 |  |
| copy.user-language | 내부 화면 명칭 금지 | 기본값 |  |
| copy.error | 실패 문구 = 이유 + 다시 할 수 있는 조건 | 기본값 |  |
| copy.i18n | 한국어 단일 | 1단계 다국어 아니오 |  |
| layout.left-edge | 모든 섹션 좌측 = space.screen-padding | 기본값 |  |
| layout.section-gap | space.section 24 하나만 | 기본값 |  |
| layout.surface-tiers | bg → surface-1 → surface-2. 3단 이상 금지 | 기본값 |  |
| layout.device-widths | 360 / 390 / 430 동일 레이아웃 | 기본값 |  |
| layout.tablet | 지원. 폰 = 지문 상단/선지 하단 세로, 태블릿 = 지문 좌/선지 우 분할 | 1단계 태블릿 예외 |  |
| layout.thumb-zone | primary CTA 하단 1/3 | 기본값 |  |
| scroll.single | 세로 스크롤 화면당 1개. 가로 스트립 허용 | 기본값 |  |
| scroll.last-item | 하단 여백 = 고정 바 높이 + safe-area + 16 | 기본값 |  |
| fixed.bottom-cta | 높이 56 + safe-area 34, 배경 bg, 상단 border | 기본값 |  |
| fixed.tab-bar | 네이티브 탭바 5개, 아이콘 24 + 라벨 caption | 3단계 네이티브 지시 |  |
| fixed.no-clip | 고정 바가 마지막 항목을 가리지 않음 | 기본값 |  |
| keyboard | 입력 시 본문 올라오고 CTA는 키보드 위 | 기본값 |  |
| sheet.sizes | half / full, 네이티브 formSheet 프레젠테이션 | 3단계 네이티브 지시 |  |
| sheet.structure | 헤더 56 · 본문 스크롤 · 푸터 CTA 56 + safe-area | 기본값 |  |
| sheet.use | 옵션 선택·필터는 시트. 새 작업 흐름은 스택 푸시 | 기본값 |  |
| dialog | 확인·경고만. 네이티브 alert 우선 | 3단계 네이티브 지시 |  |
| dialog.dismiss | 시트는 드래그·오버레이 탭, 다이얼로그는 버튼만 | 기본값 |  |
| app-bar | 네이티브 스택 헤더. 뒤로 · 제목 h3 · 우측 액션 최대 2개 | 3단계 네이티브 지시 |  |
| help.inline | 툴팁 없음. caption 또는 정보 아이콘 → 시트 | 기본값 |  |
| snackbar | 하단 고정 바 위 16, 높이 48, 4초, 액션 1개 | 기본값 |  |
| layer.order | z.scale 준수. 시트 위 시트 금지 | 기본값 |  |
| state.required | 초기 · 빈 · 로딩 · 성공 · 실패 · 비활성 6상태 | 기본값 |  |
| state.empty | 아이콘 48 + 안내 1줄 + primary 버튼 1개, 세로 중앙 | 기본값 |  |
| state.loading | 스켈레톤(surface-2). 풀스크린 스피너 금지 | 기본값 |  |
| state.error | 이유 + 재시도. 네트워크 오류는 스낵바 | 기본값 |  |
| state.offline | 앱바 아래 배너 1줄. 진행 중 세션은 로컬로 계속 | 1단계 오프라인 |  |
| data.range | 제목 짧음/김, 항목 0/1/많음, 글자 확대 120% | 기본값 |  |
| data.ownership | 시트는 현재 선택 대상만 표시 | 기본값 |  |
| change.scope | 요청된 결함만. 기존 조작 유지 | 고정 |  |
| change.relation | 위치 요청은 대상·기준·순서 확인 문장만 | 고정 |  |
| change.propagate | 컴포넌트 수정 시 모든 화면 재확인 | 고정 |  |
| change.no-dup | 새 공통 요소 전 중복 액션 확인 | 고정 |  |

## C. 프로젝트 전용 규칙

| 키 | 값 | 출처 |
|---|---|---|
| quiz.choice-count | OX 2 · 영단어 6 · 빈칸/한국사 5 | 1단계 PRD |
| quiz.direction | 영단어는 en→ko / ko→en 세트 내 번갈아 노출 | 1단계 PRD |
| quiz.feedback | 선지 탭 즉시 정오. 정답 = 초록 #22C58B, 내 오답 = danger | 3단계 퀴즈 시안 |
| quiz.ox-style | O/X 대형 버튼 2개, 높이 ≥120 | 3단계 퀴즈 시안 |
| exam.timer | 시험지 상단 중앙 serif 표시, 남은 시간 = deadline - now | 1단계 PRD |
| exam.ink | 지문 위 펜 밑줄 수평 스트로크. 로컬 우선 저장 | 1단계 PRD |
| nav.native | Expo Router native Stack + 네이티브 탭바. 커스텀 헤더바 최소화 | 3단계 네이티브 지시 |
| session.resume | 이어하기 카드가 홈 최상단. 로컬 세션 우선 | 1단계 PRD |
