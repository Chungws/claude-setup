---
description: Create GitHub/GitLab PR/MR after code review
---

# Create Pull Request

Perform commit, push, and PR/MR creation after passing `/review-phase`.

## Prerequisites

- `/review-phase` completed (mandatory)
- Must be on feature branch
- All tests passing

## Steps

1. **Check review results**
   - Verify /review-phase execution completed
   - Stop if not executed and guide user

2. **Check branch**
   - Verify on feature/* branch
   - Stop if on develop/main

3. **Evaluate branch name (optional)**
   - Analyze changes to check branch name appropriateness
   - Suggest change if inappropriate

4. **Create commits**
   - Create commits following project commit guidelines
   - MUST create granular, logical commits (NOT one giant commit)
   - Keep each commit small and focused (10-50 lines recommended)

5. **Push and create PR/MR**
   - Push branch
   - Create PR/MR (use GitHub MCP or GitLab MCP if available)
   - Target: main development branch (usually `develop` or `main`)

6. **Report PR info**
   - Output PR URL and number
   - Guide checks status

## PR Writing Rules

- **Title**: `<type>: <description>`
- **Body**: Summary, changes, test plan, impact
- **Target**: Main development branch (check project conventions)

## Important

- Never proceed without /review-phase execution
- Branch name is default for PR title, so choose carefully

## Next Steps

```
After PR merged → /end-phase
```
