# CLAUDE.md

Behavioral guidelines to write better code. Merge with project-specific instructions.

## 1. Think Before Coding

- State assumptions explicitly. If uncertain, ask.
- If multiple approaches exist, present tradeoffs — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop and ask.

## 2. Simplicity First

- No features beyond what was asked.
- No abstractions for single-use code.
- No speculative "flexibility" or "configurability".
- If you write 200 lines and it could be 50, rewrite it.
- Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated issues, mention them — don't fix them silently.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then fix"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

## 5. Code Quality Defaults

- Write tests for new functionality (TDD when appropriate).
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `chore:`.
- One logical change per commit. Keep commits small (10-100 lines ideal).
- Run linters/formatters before committing.
- Type hints in Python, TypeScript strict mode.
