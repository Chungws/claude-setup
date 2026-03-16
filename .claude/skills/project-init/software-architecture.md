# Software Architecture Guide

새 프로젝트를 시작할 때 적용할 수 있는 범용 소프트웨어 아키텍처 가이드.
Claude Code로 프로젝트를 셋업할 때 이 문서를 참고하면 처음부터 깨끗한 구조로 시작할 수 있다.

---

## 핵심 원칙

**의존성은 한 방향으로만 흐른다.** 이 규칙 하나만 지켜도 스파게티를 막을 수 있다.

---

## 레이어드 아키텍처

가장 기본. 아래에서 위로 쌓고, 위에서 아래로만 의존.

```
Types     순수 데이터 정의. 의존 없음.
  ↓
Config    설정, 환경변수. Types만 의존.
  ↓
Repo      데이터 접근 (DB, 외부 API). Types, Config 의존.
  ↓
Service   비즈니스 로직. Repo를 조합해서 유스케이스 수행.
  ↓
Runtime   실행 인프라. 서버, 미들웨어, 라우팅.
  ↓
UI        프레젠테이션. 사용자에게 보여주는 레이어.
```

교차 관심사 (인증, 로깅, 텔레메트리)는 **Providers** 하나를 통해 주입:

```
┌──────────── Business Domain ────────────┐
│                                         │
│  Types → Config → Repo                  │
│                    ↑                    │
│              Providers ← Auth, Logging  │
│                    ↓                    │
│         Service → Runtime → UI          │
└─────────────────────────────────────────┘

Utils (도메인 밖, 범용 유틸리티)
```

### 각 레이어 역할

| 레이어 | 역할 | 예시 | 금지 |
|--------|------|------|------|
| **Types** | 순수 데이터 구조 | dataclass, TypedDict, interface | 로직, import |
| **Config** | 설정 중앙 관리 | 환경변수, DB URL, feature flags | 비즈니스 로직 |
| **Repo** | 외부 시스템 경계 | DB 쿼리, API 클라이언트, 캐시 | 직접 비즈니스 판단 |
| **Service** | 비즈니스 로직 | "주문 생성" = 검증→저장→알림 | UI 의존, 직접 DB 접근 |
| **Runtime** | 실행 인프라 | 라우터, 미들웨어, 서버 부팅 | 비즈니스 로직 |
| **UI** | 프레젠테이션 | 컴포넌트, API 응답 포맷 | 직접 DB/Repo 접근 |
| **Providers** | 교차 관심사 주입 | 인증, 텔레메트리, feature flags | 비즈니스 로직 |
| **Utils** | 도메인 무관 유틸 | 날짜 포맷, retry, 문자열 처리 | 도메인 타입 의존 |

---

## 기반 이론

### Clean Architecture (Robert C. Martin)
- **의존성 규칙**: 바깥 레이어가 안쪽을 의존. 역방향 절대 금지.
- 안쪽 = 비즈니스 규칙 (Types, Service), 바깥 = 인프라 (DB, UI, 프레임워크)
- 비즈니스 로직이 프레임워크를 모른다 → 프레임워크 교체 가능

### Hexagonal Architecture (Ports & Adapters)
- 중심에 도메인, 바깥에 어댑터
- **Port** = 인터페이스 (도메인이 정의), **Adapter** = 구현 (인프라가 제공)
- 위 레이어드 구조에서 **Providers = Port**, **Repo = Adapter** 역할
- DB를 바꿔도 Service 코드는 안 바뀜

### Domain-Driven Design (DDD)
- **Bounded Context**: 하나의 비즈니스 도메인 = 하나의 경계. 도메인 간 명시적 인터페이스.
- 위 레이어링이 각 도메인 안에서 적용됨
- 도메인이 여러 개면 도메인별로 독립된 레이어 구조

### 이 세 가지의 관계

```
Clean Architecture  →  의존성 방향 규칙 (위→아래만)
Hexagonal          →  외부 시스템 추상화 (Providers/Repo)
DDD                →  도메인 경계 분리 (Bounded Context)
```

셋 다 핵심은 같다: **비즈니스 로직을 인프라로부터 격리한다.**

---

## 프로젝트 구조 템플릿

### Python (FastAPI)

```
my-project/
├── src/
│   └── my_app/
│       ├── types.py              # 순수 데이터 타입 (의존 없음)
│       ├── config.py             # 설정 중앙 관리 (types만 의존)
│       ├── repos/                # 데이터 접근
│       │   ├── user_repo.py
│       │   └── order_repo.py
│       ├── services/             # 비즈니스 로직
│       │   ├── user_service.py
│       │   └── order_service.py
│       ├── providers/            # 교차 관심사
│       │   ├── auth.py
│       │   └── telemetry.py
│       ├── api/                  # Runtime + UI (FastAPI 라우터)
│       │   ├── app.py
│       │   ├── routes/
│       │   └── middleware/
│       └── utils/                # 도메인 무관 유틸
├── tests/
├── pyproject.toml
└── CLAUDE.md
```

### TypeScript (Next.js / Express)

```
my-project/
├── src/
│   ├── types/                    # 순수 타입 정의
│   │   ├── user.ts
│   │   └── order.ts
│   ├── config/                   # 설정
│   │   └── index.ts
│   ├── repos/                    # 데이터 접근
│   │   ├── user-repo.ts
│   │   └── order-repo.ts
│   ├── services/                 # 비즈니스 로직
│   │   ├── user-service.ts
│   │   └── order-service.ts
│   ├── providers/                # 교차 관심사
│   │   ├── auth.ts
│   │   └── telemetry.ts
│   ├── app/                      # Runtime + UI
│   │   ├── routes/
│   │   └── middleware/
│   └── utils/                    # 도메인 무관 유틸
├── tests/
├── package.json
├── tsconfig.json
└── CLAUDE.md
```

---

## 의존성 규칙 (CI로 강제)

```python
# scripts/check_deps.py
ALLOWED_DEPS = {
    "types":      [],                                    # 아무것도 의존 안 함
    "config":     ["types"],
    "utils":      [],                                    # 도메인 타입도 의존 안 함
    "repos":      ["types", "config", "utils"],
    "providers":  ["types", "config", "utils"],
    "services":   ["types", "config", "repos", "providers", "utils"],
    "api":        ["types", "config", "services", "providers", "utils"],
}
# 각 모듈의 import를 파싱 → 허용 외 의존 발견 시 에러
# 에러 메시지에 수정 방향 포함 (AI 에이전트가 읽고 스스로 수정할 수 있도록)
```

```yaml
# CI에 추가
structure:
  stage: quality
  script:
    - python scripts/check_deps.py
```

---

## CLAUDE.md 템플릿

```markdown
# CLAUDE.md

## Project
{프로젝트 한 줄 설명}

## Architecture
- `src/types/` — 순수 데이터 타입. 의존 없음.
- `src/config/` — 설정 중앙 관리. types만 의존.
- `src/repos/` — 데이터 접근 (DB, 외부 API). types, config 의존.
- `src/services/` — 비즈니스 로직. repos 조합. UI/API 의존 금지.
- `src/providers/` — 교차 관심사 (인증, 로깅). services에 주입.
- `src/api/` — 라우터, 미들웨어. 진입점.
- `src/utils/` — 도메인 무관 유틸. 도메인 타입 의존 금지.

## Dependency Rules
- 의존 방향: types → config → repos/providers → services → api
- 역방향 import 절대 금지
- repos, providers는 서로 독립 (서로 import 금지)
- utils는 도메인 타입을 모른다

## Naming
- 타입명은 의미론적으로: `str` 대신 `UserId`, `OrderId`
- 파일은 작게, 경로는 의미있게: `utils/helpers.py` 금지 → `utils/retry.py`

## Lint & Test
- `ruff check && ruff format --check` (Python)
- `pytest tests/`
- `python scripts/check_deps.py`
```

---

## 언제 어디까지 적용할지

| 프로젝트 규모 | 적용 수준 |
|--------------|----------|
| 스크립트/프로토타입 | types.py + config.py 분리만 |
| 소규모 (~10 파일) | + repos/services 분리 |
| 중규모 (~30 파일) | + providers, CI 의존성 체크 |
| 대규모 (30+ 파일) | + 도메인별 Bounded Context 분리, 린터 강제 |

초기부터 types와 config를 분리하는 건 어떤 규모에서든 해야 한다. 나머지는 프로젝트가 커지면서 점진적으로.

---

## References

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — Robert C. Martin. 의존성 규칙의 원전.
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) — Alistair Cockburn. Ports & Adapters 패턴.
- [Harness engineering](https://openai.com/index/harness-engineering/) — OpenAI. 이 아키텍처를 AI 에이전트가 코드를 생성하는 환경에서 린터로 기계적 강제한 사례.
- [AI is forcing us to write good code](https://bits.logic.inc/p/ai-is-forcing-us-to-write-good-code) — AI 시대에 아키텍처 규율이 선택이 아니라 필수가 된 이유.
