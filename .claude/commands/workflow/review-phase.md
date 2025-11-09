---
description: Self code review and document updates before creating PR
---

# Review Phase and Update Documents

Perform self code review and document updates before creating PR.

## Steps

1. **Update main branch (CRITICAL!)**
   - Update main development branch, then return to current branch
   - Check changes against latest main branch

2. **Analyze changes**
   - Check changed files and line count
   - Evaluate PR size (< 300 lines recommended)

3. **Check project policies**
   - Read WORKSPACE/00_PROJECT.md
   - Verify NO FK, PR policies, etc.

4. **Check conventions**
   - Backend: TDD, uv, Alembic, ruff
   - Frontend: RSC, shadcn/ui, Chrome DevTools MCP
   - Code consistency and impact analysis

5. **Update documentation**
   - Update FEATURES checklist (if phase work)
   - Update ROADMAP progress (if phase work)

6. **Report review results**
   - Summary of pass/warning/needs-fix items
   - Determine if PR creation is ready

## Important

- Never skip checklist
- If > 300 lines, recommend splitting PR

## Next Steps

```
After review passes → /create-pr
```
