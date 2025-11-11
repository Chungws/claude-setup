---
description: Complete current phase and prepare for next phase
---

# End Phase

Complete the current phase and prepare for the next phase.

## Prerequisites

- PR/MR merged
- Checks passed

## Steps

1. **Verify PR/MR merged**
   - Check if PR/MR has been merged
   - Verify all checks passed
   - Stop if not merged yet

2. **Update develop branch**
   - Switch to develop branch
   - Pull latest changes

3. **Clean up local branches**
   - Delete completed feature branch
   - Remote branch may be deleted automatically depending on settings

4. **Check next phase**
   - Check FEATURES document for next phase
   - If exists: Guide to start next phase
   - If not: Feature complete notification

5. **Report completion**
   - Summarize phase completion
   - Suggest next actions

## Next Steps

```
Next phase exists → /start-phase
Start new feature → /new-feature
```
