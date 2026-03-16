---
name: tdd-principles
description: TDD mechanics and test writing patterns. Use when writing tests or implementing features. For strategy (layers, coverage) see testing rule.
---

# TDD Principles

## Red → Green → Refactor

### 1. Red: Write a Failing Test
- Write a test for behavior that doesn't exist yet.
- Run it. It MUST fail. If it passes, the test is wrong.

### 2. Green: Minimal Implementation
- Write the MINIMUM code to make the test pass.
- No extra features. No "while I'm here" improvements.

### 3. Refactor: Clean Up
- Improve code quality while keeping all tests green.
- Extract duplication, rename for clarity, simplify logic.
- Run tests after every change.

## AAA Pattern

Every test follows Arrange → Act → Assert:

```
def test_something():
    # Arrange
    data = create_test_data()

    # Act
    result = do_the_thing(data)

    # Assert
    assert result.status == "success"
```

## Writing Property Tests (Layer 1)

Identify invariants — things that must always hold:

```python
# Hypothesis (Python)
@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)
```

Common property patterns:
- **Round-trip**: encode then decode returns original
- **Idempotency**: applying twice = applying once
- **Invariant preservation**: operation maintains a constraint
- **Commutativity**: order doesn't matter for result

## Writing Behavior Tests (Layer 2)

One concept per test, descriptive names:

```python
def test_deposit_increases_balance():
    account = Account(balance=0)
    account.deposit(1000)
    assert account.balance == 1000

def test_withdraw_below_zero_raises_error():
    account = Account(balance=500)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(1000)
```

## Test Quality Rules

- **One assertion per concept** — a test should verify one behavior.
- **Independent tests** — no test should depend on another test's state.
- **Fast tests** — mock external services when needed (Layer 2), use real services in Layer 3.
- **Descriptive names** — `test_withdraw_below_zero_raises_error` not `test_withdraw_2`.
- **No logic in tests** — no if/else, loops, or try/catch in test code.

## When to Use TDD

**Use TDD when:**
- Building new features (write the contract first)
- Fixing bugs (reproduce with test, then fix)
- Refactoring (safety net before changes)

**Skip TDD when:**
- Prototyping/exploring (write tests after)
- UI layout tweaks
- One-off scripts

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing code before tests | Write test first, see it fail |
| Testing implementation details | Test behavior, not internals |
| Giant test functions | One concept per test |
| Shared mutable state between tests | Fresh setup per test |
| Skipping refactor phase | Always clean up after green |
| Uncovered lines left without justification | Test it or remove dead code |
| Only example tests, no property tests | Write Layer 1 properties for core logic |
