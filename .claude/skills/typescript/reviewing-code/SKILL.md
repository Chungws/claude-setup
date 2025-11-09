---
name: reviewing-code
description: Self code review checklist. Use before creating PR. Critical rules - review before PR, check conventions, run all tests (lint, format, tests), verify changes.
---

# Self Code Review Checklist

## 🔴 CRITICAL RULE

**Self-review is MANDATORY before creating PR.**

Use `/review-phase` command for automated checks.

## Pre-PR Review Workflow

### 1. Common Checklist (All Changes)

```
[ ] Git Flow: Using feature/* branch (NOT develop/main)
[ ] Commits: Conventional format (<type>: <subject>)
[ ] PR Size: Under 300 lines
[ ] Target Branch: develop
[ ] PR Language: English
[ ] Code Comments: English only
```

### 2. Backend Changes Checklist

```
[ ] TDD: Test written first (Red-Green-Refactor)
[ ] Foreign Keys: NOT used (index only)
[ ] Dependencies: Added with `uv add` (NOT pip)
[ ] Migrations: Created with `alembic revision --autogenerate`
[ ] Code Style: Imports at top, English comments, Type hints
[ ] Linting: uvx ruff check ✅
[ ] Formatting: uvx ruff format --check ✅
[ ] Tests: uv run pytest -s ✅
```

**Run all checks:**
```bash
cd backend
uvx ruff check              # Code quality
uvx ruff format --check     # Formatting
uv run pytest -s            # Tests
```

### 3. Frontend Changes Checklist

```
[ ] RSC Pattern: page.tsx (Server) vs *-client.tsx (Client)
[ ] Components: shadcn/ui used (NOT raw HTML)
[ ] API Calls: apiClient used (NOT fetch)
[ ] Linting: npm run lint ✅
[ ] UI Verification: Chrome DevTools MCP verified ✅ (MANDATORY for UI changes!)
```

**Run all checks:**
```bash
cd frontend
npm run lint
```

**CRITICAL for UI changes:**
If you changed UI components, you MUST manually verify with Chrome DevTools MCP:
1. Start dev server: `npm run dev`
2. Open page in Playwright: `mcp__chrome-devtools__navigate_page`
3. Verify rendering: `mcp__chrome-devtools__take_snapshot`
4. Check for errors: `mcp__chrome-devtools__list_console_messages`

See `frontend-ui-testing` skill for detailed verification process.

## Review Command

```bash
# Automated review (recommended)
/review-phase

# Manual checks
git diff develop --stat
git diff develop --shortstat  # Check line count
```

## PR Size Guidelines

```bash
# Check changes
git diff develop --shortstat

# ✅ GOOD: Under 300 lines
25 files changed, 142 insertions(+), 37 deletions(-)

# ⚠️ WARNING: Over 300 lines - consider splitting
45 files changed, 523 insertions(+), 189 deletions(-)
```

**If over 300 lines:**
- Split into multiple PRs
- Separate code and documentation changes
- Break down Phase into smaller tasks

## Backend Review Points

### 1. Code Quality

**Foreign Keys:**
```python
# ❌ WRONG
sample_id: int = Field(foreign_key="sample.id")

# ✅ CORRECT
sample_id: int = Field(index=True)
```

**TDD:**
```python
# ✅ Test written first
def test_create_translation():
    response = client.post("/translations", json={...})
    assert response.status_code == 200

# Then implementation
@router.post("/translations")
def create_translation(data: dict):
    ...
```

**Dependencies:**
```bash
# ✅ CORRECT
uv add httpx

# ❌ WRONG
pip install httpx
```

### 1.1. Code Style (MUST Follow)

**Import Location:**
```python
# ✅ CORRECT - All imports at top
from fastapi import APIRouter
from sqlmodel import Session

def my_function():
    ...

# ❌ WRONG - Import in middle
def my_function():
    from fastapi import APIRouter  # NO!
```

**Comments in English Only:**
```python
# ✅ CORRECT
# Calculate the total score
total = sum(scores)

# ❌ WRONG
# 총 점수를 계산합니다  # NO Korean!
```

**Type Hints Required:**
```python
# ✅ CORRECT
def get_user(user_id: int, db: Session) -> User | None:
    return db.get(User, user_id)

# ❌ WRONG - Missing type hints
def get_user(user_id, db):
    return db.get(User, user_id)
```

### 2. Tests Passing

All tests must pass before PR:
```bash
cd backend
uv run pytest -s

# Expected output:
# ====== X passed in Y.XXs ======
```

### 3. Linting and Formatting

```bash
cd backend
uvx ruff check              # Code quality - No errors
uvx ruff format --check     # Formatting - No changes needed

# If you need to fix issues:
uvx ruff check --fix        # Auto-fix linting
uvx ruff format             # Apply formatting
```

## Frontend Review Points

### 1. RSC Pattern

**Server Component (page.tsx):**
```typescript
// ✅ CORRECT: async, no "use client"
export default async function Page() {
  const data = await service.getAll()
  return <Client data={data} />
}

// ❌ WRONG: useState in Server Component
export default function Page() {
  const [data, setData] = useState([])  // NO!
}
```

**Client Component (*-client.tsx):**
```typescript
// ✅ CORRECT: "use client" at top
"use client"
export default function FeatureClient({ data }: Props) {
  const { mutate } = useFeature()
  return <Button onClick={...}>
}
```

### 2. shadcn/ui Usage

```tsx
// ❌ WRONG: Raw HTML
<button className="bg-blue-500">Click</button>

// ✅ CORRECT: shadcn/ui
import { Button } from "@/components/ui/button"
<Button variant="default">Click</Button>
```

### 3. UI Verification (MANDATORY)

**If you changed any UI:**
1. Start dev server: `npm run dev`
2. Use Chrome DevTools MCP to verify:
   - Page loads correctly
   - Components render properly
   - No console errors
   - Layout not broken

See `frontend-ui-testing` skill for detailed instructions.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Working on develop directly | Create feature/* branch first |
| Missing tests | Write test first (TDD) |
| Foreign Key used | Use index only |
| pip install | Use uv add |
| Korean comments | Use English only |
| Missing type hints | Add types to all functions |
| Imports in functions | Put all imports at top |
| Not running ruff format | Run `uvx ruff format --check` |
| Raw HTML elements | Use shadcn/ui |
| UI not verified | Chrome DevTools MCP verification |
| PR over 300 lines | Split into multiple PRs |
| Korean PR description | Write in English |

## Quick Reference

```bash
# 1. Check current branch
git branch --show-current
# If develop/main → create feature branch!

# 2. Run checks
cd backend && uvx ruff check && uvx ruff format --check && uv run pytest -s
cd frontend && npm run lint

# 3. Check PR size
git diff develop --shortstat

# 4. If UI changed: Chrome DevTools MCP verification
# (Manual step - see frontend-ui-testing skill)

# 5. Create PR with /create-pr
```

---

💬 **Questions about code review process? Just ask!**
