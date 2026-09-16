<!-- 5~6단계 기록. od-builder와 design-auditor가 이어서 쓴다. -->

# Build Log

od_project: project-2216
od_dir: design/od

## STAGE=tokens
- 실행: 2026-09-16
- 만든 것: design/od/tokens.css · design/od/index.html (토큰 갤러리, artifact entry)
- OD 동기화: write_file tokens.css + create_artifact index.html → project-2216 (entry index.html, manifest 자동 추론)
- tokens.css 변수 표:
  - 색: --color-bg #F6F4FB · --color-surface-1 #FFFFFF · --color-surface-2 #EFEBFD · --color-text #17142B · --color-text-muted #8B87A3 · --color-border #ECE9F6 · --color-accent #6C5CE7 · --color-accent-pressed #5F51CB (12% 어둡게) · --color-accent-soft rgba(108,92,231,.1) · --color-danger #F0506E · --color-overlay rgba(0,0,0,.5) · --color-correct #22C58B (§C quiz.feedback)
  - 간격: --space-1…7 = 4/8/12/16/24/32/48 · --space-screen-padding 16 · --space-section 24 · --space-card-padding 16
  - radius: --radius-sm/md/lg/xl/full = 8/12/16/22/9999
  - 크기: --size-button-sm/md/lg = 36/44/52 · --size-icon-sm/md/lg = 16/20/24 · --size-tap-min 44 · --size-tap-gap 8 · --size-safe-area-top 44 (notch 47) · --size-safe-area-bottom 34 · --size-app-bar 56 · --size-tab-bar 49 · --size-bottom-cta 56 · --size-snackbar 48 · --size-empty-icon 48 · --size-ox-button 120
  - z: --z-base/sticky/app-bar/tab-bar/overlay/sheet/dialog/snackbar = 0/100/200/200/300/400/500/600
  - shadow: --shadow-sm 0 2px 8px rgba(80,70,160,.08) · --shadow-md 0 8px 24px rgba(80,70,160,.12)
  - font: --font-family "IBM Plex Sans KR" · --font-serif "Noto Serif KR" (display·h1)
  - motion: --motion-base 200ms · --motion-sheet 250ms · --motion-crossfade 150ms
  - 타이포 역할: .t-display .t-h1 .t-h2 .t-h3 .t-body .t-body-sm .t-caption .t-label (제목 lh 1.3 / 본문 1.5)
- 스크린샷: 없음 (tokens 단계 — 갤러리만)
- 누락·질문: thumbnail.* 규칙 미사용 → --size-thumbnail 미생성

## STAGE=components
- 실행: 2026-09-16
- 만든 것: design/od/components.css · design/od/icons.svg · design/od/components.html (컴포넌트 갤러리)
- OD 동기화: write_file 3개 → project-2216 (components.css / icons.svg / components.html, sha256 로컬=프로젝트 일치 확인)
- components.css 클래스 표:
  - 프레임: .screen(390×844) · .screen-body(+--has-cta/--has-tab-bar/--has-cta-tab-bar 하단 여백 106/99/155)
  - 버튼: .button × .button-primary/secondary/ghost/danger × .button-sm/md/lg × :active/.is-selected/:disabled(.is-disabled)/.is-loading(스피너 20, 라벨 숨김) · .button-full(radius xl) · .button-row
  - 아이콘 버튼: .icon-button × .icon-button-sm/md/lg × :active/.is-selected/:disabled/.is-loading (탭 영역 44)
  - 카드: .card(:active) · .card-title(2줄) · .card-desc(3줄) · .card-meta · .card-action · .card-row · .list-row(-title/-meta)
  - 폼: .field · .input/.select(:focus/.is-error/:disabled) · .caption(.is-error)
  - 헤더: .app-bar/.nav-header(-title/-actions/-center) · .timer(serif·tabular-nums)
  - 탭바: .tab-bar(env safe-area) · .tab-bar-item(.is-active)
  - 시트: .backdrop · .bottom-sheet(-half/-full) · .sheet-grabber/-header/-header-title/-body/-footer
  - 기타 고정: .dialog(-body/-actions, 폭 390-48) · .bottom-cta(--above-tab-bar) · .snackbar(--above-cta/-label/-action)
  - 상태: .empty-state(-icon 24×2배/-desc/-action) · .skeleton(-line/-line-sm/-card) · .error-state(-icon/-desc/-action) · .offline-banner
  - §C 전용: .choice-list · .choice(-index/-text/-mark, .is-selected/.is-correct/.is-wrong/:disabled) · .ox-row · .ox-button(≥120, .is-correct/.is-wrong) · .progress-bar(-fill) · .score-ring(-10…-100, conic) · .logo(serif) · .exam-image(contain+surface-2)
  - 파생 :root 별칭(숫자만): --font-size-*/--font-weight-*(type.roles 값) · --button-pad-lg 20 · --hairline 1 · --size-grabber/progress/score-ring
  - z-index는 --z-* 만 (app-bar/nav-header 200 · tab-bar 200 · backdrop 300 · bottom-sheet 400 · dialog 500 · snackbar 600 · bottom-cta는 --z-tab-bar 사용)
- icons.svg symbol 표 (lucide-static v1.46.0, <symbol id="i-*">): i-home · i-library · i-bookmark · i-history · i-user · i-play · i-highlighter · i-timer · i-check · i-x · i-bar-chart-3 · i-log-out · i-star · i-chevron-left · i-door-open · i-inbox · i-alert-circle · i-loader (18개)
- 스크린샷: 없음 (components 단계 — 갤러리만)
- 누락·질문:
  - thumbnail.* 규칙 미사용 → .thumbnail 미생성
  - empty/error 아이콘: 규칙은 아이콘 48이나 icon.sizes(16/20/24)와 충돌 → 24 스프라이트를 transform scale(2)로 48 표현
  - screens.md 구성 열 첫 토큰이 한국어(선지/진행/점수/이어하기/카카오 등) — od_audit component.manifest가 이를 클래스명으로 기대할 수 있음. screens 단계에서 kebab 매핑 확인 필요 (괄호 안 쉼표 "Logo(한장, serif)"도 "serif)"로 분리됨)
  - bottom-cta의 z-tier는 z.scale에 별도 키 없어 --z-tab-bar(200) 사용

## STAGE=screens
- 파일 표 (화면 × 상태 → screens/<slug>-<state>.html)
  - 한글 파일명 세트 (사용자 지정 basename, 28개):
    - 로그인: default·error / 홈: default·empty·loading·error / 자료실: default·empty·loading·error·offline
    - 저장: default·empty·loading / 복습: default·empty·loading / 마이: default
    - 시험지: default·grading·graded·error·offline / 결과: default
    - 퀴즈-플레이: default·feedback·error / 퀴즈-결과: default
  - 영어 slug 세트 (od_audit 검사용 병행, 75개): login·home·library·saved·review·my·exam·exam-result·quiz-play·quiz-result × default + REQUIRED_STATES(empty·loading·error·long-title·many-items·text-120) + 화면 고유 상태(feedback·grading·graded·offline)
- 에셋: od/assets/exam-passage.svg (시험지 지문, .passage-image <img>로 참조 — 펜 밑줄 포함)
- 스크린샷: design/screenshots/screen-{login,home,library,saved,review,my,exam,exam-result,quiz-play,quiz-result}.png 10개 (390×844)
- OD 동기화: project-2216 write 105개 (screens 103 + assets/exam-passage.svg + index.html), 미러=프로젝트 내용 일치 확인 (raw fetch 비교)
- index.html 갤러리: 영어 slug 링크 행 + 한글 파일명 링크 행 병기
- 누락 컴포넌트: 없음
- 누락·질문:
  - od_audit.py는 slug를 [a-z0-9-]로 제한(L366)하고 brief.md 화면명도 영어(Login·QuizPlay…)라 한글 파일명 세트는 감사에서 완전히 건너뜀 → 영어 slug 세트를 병행 유지해야 screen.missing/states 검사 통과
  - screens.md 구성표 기준 실제 클래스명: exam-image→.passage-image, ox-row/ox-button→.tf-row/.tf-button (components.css에 후자만 존재)
  - Google Fonts <link>: 영어 세트는 포함(렌더링용), 한글 세트는 "link는 tokens/components만" 규칙에 따라 제외
  - 진행바 .progress-bar-fill은 인라인 style 금지로 width 지정 불가 → 100%로 렌더됨 (state별 진행률 표현 한계)
  - 병행 실행 중 다른 에이전트가 영어 slug 세트를 작성하며 한글 파일을 삭제·index.html을 영어 링크로 교체한 이력 있음 → 한글 세트 재생성·갤러리 병기로 복구

## 오디트 #1
- A단계 실패:
- C단계 실패:
- 진단:
- 다음 행동:

## STAGE=screens 완료
- 실행: 2026-09-16
- 파일 수: 109 (루트 5: tokens.css·components.css·icons.svg·index.html·components.html + assets/exam-passage.svg + screens/ 103)
- 프로젝트: project-2216
- 동기화 결과: 성공 — design/od 전체를 write_file로 동기화, resolvedDir과 바이트 단위 cmp 비교 0 mismatch (한글 파일명 세트 28 + 영어 slug 세트 75 포함)

## STAGE=fix #1
- fixed: <결함> → <파일> <전/후>
