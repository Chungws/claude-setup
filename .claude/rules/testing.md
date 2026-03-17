# Testing Strategy

## 3-Layer Test Architecture

**Layer 1: Property/Invariant Tests**
- Test the system's laws — things that must always hold regardless of implementation.
- Use property-based testing (Hypothesis, fast-check, etc.).
- These survive refactoring — they test "what" not "how".
- Examples: "balance is never negative", "output is always sorted", "round-trip encode/decode".

**Layer 2: Behavior Tests (example-based)**
- Test use cases and intent with concrete examples.
- This is the main layer for reaching coverage targets.
- Follow TDD: Red → Green → Refactor.
- Examples: "deposit 1000 → balance 1000", "invalid email → error".

**Layer 3: Integration Tests**
- Verify assembled components work together end-to-end.
- Mark with `@integration` / `@slow` tags for CI/CD separation.
- Run on dedicated pipeline, not on every commit.

## Plan → Test First

Plan mode 완료 후, 구현 전에 수용 기준을 Red 테스트로 먼저 작성한다.
- Plan의 각 단계에서 검증 가능한 행동을 추출 → pytest 테스트로 변환
- 모든 테스트가 Red(실패) 상태인지 확인한 뒤 구현 시작
- 이것이 "사전 명세"의 역할을 한다 — 리뷰 대신 테스트가 수용 기준을 강제
- 이후 Red → Green → Refactor 사이클로 구현 (→ `testing/tdd-principles` 참조)

## Coverage

- Target **100% line coverage** for new code.
- Uncovered line = needs a test or is dead code to remove.
- No "is this important enough to test?" judgment calls — test everything.
- This is critical for agent-assisted development: agents lack institutional knowledge, so tests are the only safety net.

## CI/CD Separation

- **Every commit**: Layer 1 + Layer 2 (fast, < 1 min).
- **Scheduled/pre-merge**: Layer 3 (slow, external dependencies).

For TDD mechanics and test writing patterns → see `testing/tdd-principles` skill.
