---
description: Create a new feature specification document in WORKSPACE/FEATURES/
---

# Create New Feature Specification

Create a new feature specification document in WORKSPACE/FEATURES/ folder.

## Steps

1. **Gather feature information**
   - Feature name (for filename, kebab-case recommended)
   - Feature display name (human-readable)
   - Goals and background
   - Key requirements

2. **Plan phase breakdown**
   - Break feature into phases
   - Each phase = 1-2 MR units
   - Create checklist for each phase

3. **Analyze tech stack**
   - Backend/Frontend changes
   - DB migration required?
   - New dependencies?

4. **Generate document**
   - File: `WORKSPACE/FEATURES/FEATURE_NAME.md`
   - Structure: Overview, Phase plan, Tech stack, Data models

5. **Update ROADMAP**
   - Add to "Current Focus" section

6. **User approval**
   - Review and modify created spec

## Important

- Read WORKSPACE/00_PROJECT.md first (project policies)
- Keep phases small (target < 300 lines per MR)

## Next Steps

```
Complex feature → /clarify (recommended)
Simple feature → /start-phase
```
