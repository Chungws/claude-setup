---
description: Create GitHub PR with English format after code review
---

# Create GitHub PR

Perform commit, push, and PR creation after passing `/review-phase`.

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

5. **Push and create PR**
   - Push branch
   - Create PR with GitHub MCP (in English)
   - Target: develop

6. **Report PR info**
   - Output PR URL and number
   - Guide checks status

## PR Writing Rules

- **Language**: English
- **Title**: `<type>: <description>`
- **Body**: Summary, changes, test plan, impact
- **Target**: develop

## Important

- Never proceed without /review-phase execution
- Branch name is default for PR title, so choose carefully

## Next Steps

```
After PR merged → /end-phase
```
