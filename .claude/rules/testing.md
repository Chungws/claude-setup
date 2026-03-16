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

## Coverage

- Target **100% line coverage** for new code.
- Uncovered line = needs a test or is dead code to remove.
- No "is this important enough to test?" judgment calls — test everything.
- This is critical for agent-assisted development: agents lack institutional knowledge, so tests are the only safety net.

## CI/CD Separation

- **Every commit**: Layer 1 + Layer 2 (fast, < 1 min).
- **Scheduled/pre-merge**: Layer 3 (slow, external dependencies).

For TDD mechanics and test writing patterns → see `testing/tdd-principles` skill.
