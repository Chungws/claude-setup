---
description: Run all code quality checks (lint, format, tests) for phase work
---

# Verify Phase Code

Run all code quality checks for phase work.

## Steps

1. **Analyze changed files**
   - Check if backend changed
   - Check if frontend changed

2. **Backend verification** (if changed)
   - Ruff lint check
   - Import sort check (isort)
   - Run tests (pytest)

3. **Frontend verification** (if changed)
   - ESLint check
   - **If UI changed: Chrome DevTools MCP verification MANDATORY!**

4. **Report results**
   - Summary of pass/fail items
   - Guide items needing fixes

## Important

- All checks must pass
- If UI changed, never skip Playwright verification

## Next Steps

```
After all checks pass → /review-phase
```
