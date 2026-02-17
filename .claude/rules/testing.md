# Testing

- Follow TDD: Red (failing test) → Green (minimal code) → Refactor.
- Every test: Arrange → Act → Assert. One concept per test.
- Always test: happy path, edge cases (empty/null/boundary), error cases.
- Don't test: framework internals, private methods, trivial getters.
- Test names must describe behavior: `test_create_user_with_duplicate_email_raises_error`.
- No logic in tests (no if/else, loops, try/catch).
- Skip TDD for prototyping, UI tweaks, one-off scripts — write tests after.

For detailed patterns → see `testing/tdd-principles` skill.
