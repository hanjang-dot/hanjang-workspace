# 한장 — 스택 기획서

저장소는 `hanjang-dot/hanjang-workspace` 아래 서브모듈 `hanjang-fe`, `hanjang-be`다.

---

## 1. 저장소

```
hanjang-workspace/
  hanjang-fe/          # 서브모듈
  hanjang-be/          # 서브모듈
  docs/
    서비스-기획서.md
    스택-기획서.md
```

`develop`이 기본 브랜치다. `main`은 유지한다.

---

## 2. hanjang-fe

pnpm workspace 모노레포.

```
hanjang-fe/
  apps/
    hanjang-fo/        # Expo 수험생 앱
    hanjang-bo/        # Next.js 운영 웹
  packages/
    tokens/            # FO·BO 디자인 토큰
    api/               # FO·BO 공통 API 정의
  package.json
  pnpm-workspace.yaml
  eslint.config.js
  prettier.config.js
```

`pnpm-workspace.yaml`

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

---

## 3. FE 공통

| 항목 | 선택 |
| --- | --- |
| 언어 | TypeScript |
| 서버 상태 | TanStack Query |
| 클라이언트 상태 | Zustand |
| HTTP | ky |
| 이펙트 | Effect — 타임아웃·재시도·취소 전부 fiber 기반. AbortSignal은 ky 경계에서만 |
| 렌더 계측 | React Profiler |
| 린트·포맷 | ESLint, Prettier, import 순서 |

import 순서: builtin → external → `@hanjang/*` → 상대경로. type import는 맨 아래. Prettier와 `eslint-plugin-import`가 같은 순서를 강제한다.

`packages/tokens`

- 색, 간격, 타이포, 반경
- FO는 Unistyles 테마로 읽는다
- BO는 CSS 변수로 읽는다
- 값은 한곳만 둔다

`packages/api`

- REST 엔드포인트 정의와 생성 타입
- FO·BO는 ky로 같은 엔드포인트에 POST 한다
- 앱이 URL과 스키마를 각자 정의하지 않는다

---

## 4. hanjang-fo

Expo, React Native New Architecture, Expo Router.

추가로 쓰는 것: Expo 기본 모듈, `react-native-unistyles`, `react-native-reanimated`, `react-native-gesture-handler`, `@legendapp/list`, `expo-sqlite`(세션 로컬), `expo-dev-client`, `expo-updates`.

목록은 LegendList만 쓴다. FlatList로 바꾸지 않는다.

화면은 `src/app`, `src/screens`, `src/features/<name>` (api, hooks, types, components). 피처 밖에서 깊은 import를 하지 않는다.

스타일은 Unistyles만. `style={{}}` 금지.

InkSplit의 시험지·펜·채점, SheetKeep의 목록·세션 복원을 이 앱으로 합친다. 저장소 이름은 `hanjang-fo`다.

---

## 5. hanjang-bo

Next.js App Router.

토큰과 API 패키지는 FO와 같다. 목록은 웹 테이블이다. LegendList는 BO에 두지 않는다.

화면: 로그인, 관리자 초대, 시험지 CRUD, 문항·정답 편집, 퀴즈 편집, 발행.

---

## 6. hanjang-be

출처: `https://github.com/cyjoon68/demo-backend` 코드를 가져오되 **데모 백엔드 프로젝트가 아니다.**

가져오는 뼈대

- NestJS 11, REST, Drizzle, Postgres 16
- JWT access/refresh, 카카오, 전화 인증 (수험생 User)
- admin은 아이디·비밀번호 인증 + 초대 링크 (발송 없이 복사). root는 시드. Admin/AdminInvite 테이블
- SQL 마이그레이션, Datadog JSON 로그, e2e

지우는 이름

| demo-backend | 한장 |
| --- | --- |
| `container_name: demo-backend-postgres` | `hanjang-postgres` |
| 볼륨 `postgres-data` | `hanjang-postgres-data` |
| `POSTGRES_DATABASE=chatty_bo` | `hanjang` |
| `DD_SERVICE=demo-backend` | `hanjang-be` |
| package `name: server` | `hanjang-be` |
| SMS 문구 `[Demo]` | `[한장]` |
| README Nest 로고 스타터 | 한장 API |

모듈

- 유지: `auth`, `user`, `phone`, `database`
- 추가: `exam` (시험지), `question`, `session`, `grade`, `quiz`, `mcp`
- `mcp` 모듈: 문항·퀴즈 추가 도구 노출. JWT Bearer + `role = admin` 검사. BO와 같은 서비스 호출
- 필기 초안은 FO 로컬이 우선. 서버 백업은 session 하위

REST가 FO·BO의 계약이다. `packages/api`가 엔드포인트와 타입을 따른다.

로컬:

```bash
pnpm db:up      # docker compose, 컨테이너 hanjang-postgres
pnpm migrate
pnpm start:dev
```

---

## 7. 런타임

```
hanjang-fo (Expo) --ky--> hanjang-be REST
hanjang-bo (Next) --ky--> hanjang-be REST
hanjang-be --> hanjang-postgres
hanjang-fo 로컬 SQLite --> 세션·필기 초안
```

FO 배포: EAS development / preview / production, `newArchEnabled: true`.
BO 배포: 별도 웹 호스트. 1차 완료 조건이 아니다.

---

## 8. 작업 순서

1. `hanjang-be`에 demo-backend 코드를 복사하고 이름을 한장으로 바꾼다. 인증이 뜬다.
2. `hanjang-fe` 워크스페이스, eslint/prettier, `packages/tokens`, `packages/api`.
3. `apps/hanjang-fo` 골격. 목록 → 시험지. 목 데이터로 한 사이클.
4. BE `exam` / `question` / `session` / `grade`. FO를 실 API에 붙인다.
5. `apps/hanjang-bo` 발행 화면. FO 목록이 발행분만 보여 준다.
6. InkSplit·SheetKeep에서 검증한 레이아웃·제스처·채점 run·복원·LegendList를 FO에 옮긴다.

demo-backend 저장소를 서브모듈로 두지 않는다. 한장 코드만 `hanjang-be`에 남는다.
