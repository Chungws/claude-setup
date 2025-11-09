---
name: creating-pull-requests
description: GitHub Pull Request creation for this project. Use when creating PRs. Critical rules - English language, target develop branch, <300 lines per PR, separate commits for logical units.
---

# Creating Pull Requests (PR)

## 🔴 CRITICAL RULES - Project Specific

### Project-Specific Policies

| Policy | Value |
|--------|-------|
| **Target Branch** | `develop` |
| **PR Language** | **English** (title and description) |
| **PR Size Limit** | **<300 lines** (recommended) |

### PR Size

```bash
# Check changes before PR
git diff develop --shortstat

# ✅ GOOD: Under 300 lines
25 files changed, 142 insertions(+), 37 deletions(-)

# ⚠️ WARNING: Over 300 lines - consider splitting
45 files changed, 523 insertions(+), 189 deletions(-)
```

**If over 300 lines:**
- Split into multiple PRs
- Break down Phase into smaller tasks
- Separate code and documentation changes

### Granular Commits

✅ **CORRECT: Logical separation**
```bash
git log --oneline
abc1234 test: add translation result endpoint tests
def5678 feat: add translation result endpoint
ghi9012 feat: add TranslationResult schema
jkl3456 feat: add TranslationResult model
```

❌ **WRONG: Single commit**
```bash
git log --oneline
abc1234 feat: add translation result feature  # All changes in one commit
```

**Pattern:** models → schemas → service → router → tests

### Code + Documentation Separation

✅ **CORRECT: Separate PRs**
- PR #1: Feature implementation (code only)
- PR #2: WORKSPACE documentation update

❌ **WRONG: Mixed in one PR**
- PR #1: Feature implementation + WORKSPACE docs

## PR Creation Workflow

### 1. Pre-PR Checklist

```bash
# Backend changes
cd backend
uvx ruff check
uvx ruff format --check
uv run pytest -s

# Frontend changes
cd frontend
npm run lint
# Manual Chrome DevTools MCP verification if UI changed

# Check diff size
git diff develop --shortstat
```

**All checks must pass.**

### 2. Commit Changes

Follow granular commit pattern:

```bash
# Commit in logical order
git add app/translation/models.py
git commit -m "feat: add TranslationResult model"

git add app/translation/schemas.py
git commit -m "feat: add TranslationResult schema"

git add app/translation/service.py
git commit -m "feat: add translation service"

git add app/translation/router.py
git commit -m "feat: add translation endpoint"

git add tests/test_translation.py
git commit -m "test: add translation tests"
```

See `committing-changes` skill for commit format rules.

### 3. Push Branch

```bash
# Push feature branch
git push -u origin feature/translation-result
```

### 4. Create PR (Using GitHub MCP)

```typescript
// Use mcp__github__create_pull_request tool
{
  "title": "feat: Add translation result storage feature",
  "head": "feature/translation-result",
  "base": "develop",
  "body": "...",  // See template below
  "draft": false
}
```

### 5. PR Description Template

```markdown
## Summary
Add TranslationResult model and API endpoints to store and retrieve translation results.

## Changes
### Backend
- `app/translation/models.py`: Add TranslationResult model
- `app/translation/schemas.py`: Add TranslationResultCreate, TranslationResultResponse schemas
- `app/translation/service.py`: Add create_result, get_results service functions
- `app/translation/router.py`: Add POST /translation-results, GET /translation-results endpoints
- `tests/test_translation.py`: Add translation result CRUD tests

## Test Plan
- [x] Backend tests passing (pytest)
- [x] Lint checks passing (ruff)
- [ ] Manual test: API endpoint verification

## Impact
- Breaking Changes: No
- Database Changes: Migration required (`alembic upgrade head`)
- Dependencies: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## PR Description Structure

### Required Sections

**1. Summary**
- 1-3 sentences
- What was changed and why
- Written in English

**2. Changes**
- Organized by Backend/Frontend
- List main files and changes
- Bullet points

**3. Test Plan**
- Checkboxes for completed tests
- [ ] items for manual tests needed
- Backend: pytest, ruff
- Frontend: npm run lint, Playwright verification

**4. Impact**
- Breaking Changes: Yes/No
- Database changes: Migration needed?
- Dependencies: New packages?

**5. Attribution**
```markdown
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Examples

**Backend Feature:**
```markdown
## Summary
Add Human Evaluation feature to allow users to rate translation quality.

## Changes
### Backend
- `app/evaluation/models.py`: Add HumanEvaluation model
- `app/evaluation/schemas.py`: Add evaluation schemas
- `app/evaluation/service.py`: Add evaluation save/retrieve logic
- `app/evaluation/router.py`: Add POST /evaluations endpoint

## Test Plan
- [x] pytest passing
- [x] ruff check passing
- [ ] Manual test: Create and retrieve evaluations

## Impact
- Breaking Changes: No
- Database Changes: Migration required
- Dependencies: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Frontend Feature:**
```markdown
## Summary
Add Translation List page to display saved translation results in a table.

## Changes
### Frontend
- `app/(dashboard)/translations/page.tsx`: Server Component for translation list retrieval
- `app/(dashboard)/translations/translations-client.tsx`: Translation table UI
- `app/(dashboard)/translations/service.ts`: API call functions
- `app/(dashboard)/translations/_types.ts`: Translation type definitions

## Test Plan
- [x] npm run lint passing
- [x] Chrome DevTools MCP verification complete (table rendering, button clicks)

## Impact
- Breaking Changes: No
- Database Changes: None
- Dependencies: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Bug Fix:**
```markdown
## Summary
Fix 500 error when handling null values in Translation API.

## Changes
### Backend
- `app/translation/service.py`: Add null value validation

## Test Plan
- [x] pytest passing (null case tests added)
- [x] ruff check passing
- [ ] Manual test: API call with null input

## Impact
- Breaking Changes: No
- Database Changes: None
- Dependencies: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Using GitHub MCP Tools

### Available Tools

```typescript
// Create PR
mcp__github__create_pull_request({
  title: "feat: Add feature title",
  head: "feature/branch-name",
  base: "develop",
  body: "...",
  draft: false
})

// Get PR details
mcp__github__pull_request_read({
  method: "get",
  owner: "owner-name",
  repo: "repo-name",
  pullNumber: 123
})

// Update PR
mcp__github__update_pull_request({
  owner: "owner-name",
  repo: "repo-name",
  pullNumber: 123,
  title: "Updated title",
  body: "Updated description"
})

// List PRs
mcp__github__list_pull_requests({
  owner: "owner-name",
  repo: "repo-name",
  state: "open"
})
```

### Example: Create PR via MCP

```typescript
// Full PR creation example
mcp__github__create_pull_request({
  owner: "owner-name",
  repo: "repo-name",
  title: "feat: Add translation result storage",
  head: "feature/translation-result",
  base: "develop",
  body: `
## Summary
Add TranslationResult model and API endpoints to store and retrieve translation results.

## Changes
### Backend
- \`app/translation/models.py\`: Add TranslationResult model
- \`app/translation/schemas.py\`: Add schemas
- \`app/translation/service.py\`: Add service functions
- \`app/translation/router.py\`: Add API endpoints

## Test Plan
- [x] Backend tests passing
- [x] Lint checks passing

## Impact
- Breaking Changes: No
- Database Changes: Migration required
- Dependencies: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
  `,
  draft: false
})
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Target branch is other than `develop` | Use `develop` |
| Korean PR title/description | Use English |
| PR over 300 lines | Split into multiple PRs |
| All changes in one commit | Granular commits (models → schemas → service → router → tests) |
| Code + docs in one PR | Separate PRs |
| Missing attribution | Add Claude Code attribution |
| Tests not passing | Run `pytest`, `npm run lint` before PR |
| Using isort separately | Not needed - ruff handles everything |

## Quick Reference

```bash
# Pre-PR checklist (Backend)
uvx ruff check
uvx ruff format --check
uv run pytest -s

# Pre-PR checklist (Frontend)
npm run lint

# Check diff size
git diff develop --shortstat

# Push branch
git push -u origin feature/your-feature

# Create PR using GitHub MCP
# See "Using GitHub MCP Tools" section above
```

**PR Settings:**
- Target: `develop`
- Language: English
- Size: <300 lines

---

💬 **Questions about creating PRs? Just ask!**
