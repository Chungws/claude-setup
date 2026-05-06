---
name: gate
description: >
  phase 완료 후 기계적 품질 게이트. ruff, mypy, pytest를 전체 코드베이스 대상으로 실행.
  suppression 감사 포함. PASS해야 review로 넘어감.
  "/ludo:gate" 또는 ludo:go에서 자동 호출.
user-invocable: true
argument-hint: "<phase-number>"
---

# Gate — Mechanical Quality Gate

## 원칙
- 기계적 검증만. 판단이 필요한 리뷰는 `/ludo:review`가 담당.
- **전체 코드베이스** 대상. phase 범위만이 아님.
- PASS해야 review stage로 넘어감 (blocking prerequisite).

## Input
- $ARGUMENTS: phase 번호. 없으면 가장 최근 complete phase.

## 검증 (전체 코드베이스)

### 1. Lint + Format
```bash
ruff check .
ruff format --check .
```

### 2. Type Check
```bash
mypy .
```

### 3. Test + Coverage
```bash
pytest --tb=short --cov --cov-fail-under=100
```

### 4. Suppression 감사

이 phase에서 새로 추가된 suppression 전수 검사:

```bash
git diff {phase-start}..HEAD | grep -E '^\+.*#\s*(noqa|type:\s*ignore)'
```

각 suppression에 대해:
- 이유가 인라인으로 명시되어 있는가? → 없으면 FAIL
- 이유가 합리적인가?
  - OK: 외부 라이브러리 타입 미스매치, 동적 dispatch 등 구조적으로 해결 불가
  - FAIL: 코드를 고치면 해결되는데 suppression으로 회피

### 5. 수용 기준 형식 체크
- PLAN.md에서 해당 phase의 체크박스가 모두 `[x]`인가?

## 출력

```
## Gate: Phase {N}

| 항목 | 결과 | 상세 |
|------|------|------|
| ruff | PASS/FAIL | {에러 수} |
| mypy | PASS/FAIL | {에러 수} |
| pytest | PASS/FAIL | coverage {N}% |
| suppression | PASS/FAIL | 새 {N}개, 부적절 {N}개 |
| 수용 기준 | PASS/FAIL | {미충족 항목} |

GATE_RESULT: PASS / FAIL
FAIL_ITEMS: [실패 항목]
```

## 규칙
- FAIL 하나라도 → 전체 FAIL
- gate는 기계적 판정만 — 코드 수정 안 함, 아키텍처 판단 안 함
- PASS 후 `/ludo:review`로 넘어감
