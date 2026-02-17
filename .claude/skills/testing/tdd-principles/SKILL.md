---
name: tdd-principles
description: Test-Driven Development principles. Use when writing tests, implementing features with TDD, or reviewing test coverage. Language and framework agnostic.
---

# TDD Principles

## Red → Green → Refactor

Every feature follows this cycle:

### 1. 🔴 Red: Write a Failing Test
- Write a test for behavior that doesn't exist yet.
- Run it. It MUST fail. If it passes, the test is wrong.

### 2. 🟢 Green: Minimal Implementation
- Write the MINIMUM code to make the test pass.
- No extra features. No "while I'm here" improvements.
- Ugly code is fine — it passes, that's all that matters.

### 3. 🔵 Refactor: Clean Up
- Improve code quality while keeping all tests green.
- Extract duplication, rename for clarity, simplify logic.
- Run tests after every change.

## AAA Pattern

Every test follows Arrange → Act → Assert:

```
def test_something():
    # Arrange: set up preconditions
    data = create_test_data()

    # Act: execute the thing being tested
    result = do_the_thing(data)

    # Assert: verify the outcome
    assert result.status == "success"
```

## What to Test

**Always test:**
- Happy path (expected inputs → expected outputs)
- Edge cases (empty input, boundary values, None/null)
- Error cases (invalid input, missing data, exceptions)
- State changes (database writes, side effects)

**Don't test:**
- Framework internals (ORM, HTTP library)
- Private methods directly (test through public API)
- Trivial getters/setters

## Test Quality Rules

- **One assertion per concept** — a test should verify one behavior.
- **Independent tests** — no test should depend on another test's state.
- **Fast tests** — mock external services (DB, API, filesystem) when needed.
- **Descriptive names** — `test_create_user_with_duplicate_email_raises_error` not `test_create_user_2`.
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
| 100% coverage obsession | Cover critical paths, not every line |
