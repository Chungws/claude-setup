---
description: Start a new development phase (create feature branch, read conventions)
---

# Start Development Phase

Start a new phase of development.

## Steps

1. **Check branch safety**
   - Check current branch (must be `develop`)
   - If not develop, move and update

2. **Gather basic info**
   - Feature name (e.g., translation-evaluation)
   - Phase number (e.g., phase-1, phase-2)

3. **Create feature branch**
   - Create `feature/{feature-name}-{phase-number}` branch from develop
   - Never work directly on develop!

4. **Check project policies**
   - Read WORKSPACE/00_PROJECT.md (check project conventions and policies)
   - Understand backend/frontend requirements

5. **Check feature document (optional)**
   - Read WORKSPACE/FEATURES/{feature-name}.md
   - Review phase checklist

6. **Establish work plan**
   - Register phase tasks with TodoWrite
   - Report ready to start work

## Next Steps

```
After work complete → /verify-phase
```
