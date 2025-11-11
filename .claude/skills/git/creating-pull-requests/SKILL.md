---
name: creating-pull-requests
description: Pull Request creation for GitHub/GitLab. Use when creating PRs/MRs. Critical rules - granular commits, PR size limits, clear description structure. Platform and language agnostic.
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
abc1234 test: add user profile endpoint tests
def5678 feat: add user profile endpoint
ghi9012 feat: add UserProfile schema
jkl3456 feat: add UserProfile model
```

❌ **WRONG: Single commit**
```bash
git log --oneline
abc1234 feat: add user profile feature  # All changes in one commit
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
# Python project checks
uv run ruff check
uv run ruff format --check
uv run pytest -s

# TypeScript/JavaScript project checks
npm run lint

# Manual UI verification if UI changed

# Check diff size
git diff develop --shortstat
```

**All checks must pass.**

### 2. Commit Changes

Follow granular commit pattern:

```bash
# Commit in logical order
git add app/user/models.py
git commit -m "feat: add UserProfile model"

git add app/user/schemas.py
git commit -m "feat: add UserProfile schema"

git add app/user/service.py
git commit -m "feat: add user profile service"

git add app/user/router.py
git commit -m "feat: add user profile endpoint"

git add tests/test_user_profile.py
git commit -m "test: add user profile tests"
```

See `committing-changes` skill for commit format rules.

### 3. Push Branch

```bash
# Push feature branch
git push -u origin feature/user-profile
```

### 4. Create PR (Using GitHub MCP)

```typescript
// Use mcp__github__create_pull_request tool
{
  "title": "feat: Add user profile feature",
  "head": "feature/user-profile",
  "base": "develop",
  "body": "...",  // See template below
  "draft": false
}
```

### 5. PR Description Template

```markdown
## Summary
Add UserProfile model and API endpoints to manage user profile information.

## Changes
### Backend
- `app/user/models.py`: Add UserProfile model
- `app/user/schemas.py`: Add UserProfileCreate, UserProfileResponse schemas
- `app/user/service.py`: Add create_profile, get_profile service functions
- `app/user/router.py`: Add POST /users/profile, GET /users/profile endpoints
- `tests/test_user_profile.py`: Add user profile CRUD tests

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
Add Product Catalog feature to allow users to browse and search products.

## Changes
### Backend
- `app/product/models.py`: Add Product model
- `app/product/schemas.py`: Add product schemas
- `app/product/service.py`: Add product CRUD operations
- `app/product/router.py`: Add GET /products, POST /products endpoints

## Test Plan
- [x] pytest passing
- [x] ruff check passing
- [ ] Manual test: Create and retrieve products

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
Add Dashboard page to display user statistics and recent activity.

## Changes
### Frontend
- `app/(dashboard)/home/page.tsx`: Server Component for dashboard data retrieval
- `app/(dashboard)/home/dashboard-client.tsx`: Dashboard UI with charts
- `app/(dashboard)/home/service.ts`: API call functions
- `app/(dashboard)/home/_types.ts`: Dashboard type definitions

## Test Plan
- [x] npm run lint passing
- [x] Manual UI verification complete (charts rendering, data display)

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
Fix 500 error when handling null values in User API.

## Changes
### Backend
- `app/user/service.py`: Add null value validation

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
  title: "feat: Add user profile management",
  head: "feature/user-profile",
  base: "develop",
  body: `
## Summary
Add UserProfile model and API endpoints to manage user profile information.

## Changes
### Backend
- \`app/user/models.py\`: Add UserProfile model
- \`app/user/schemas.py\`: Add schemas
- \`app/user/service.py\`: Add service functions
- \`app/user/router.py\`: Add API endpoints

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
# Pre-PR checklist (Python)
uv run ruff check
uv run ruff format --check
uv run pytest -s

# Pre-PR checklist (TypeScript/JavaScript)
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
