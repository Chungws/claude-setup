---
name: reviewing-python
description: Python code review checklist. Use before creating PR for Python projects. Covers code style, testing, linting, type hints, and common Python patterns.
---

# Python Code Review Checklist

## 🔴 CRITICAL RULE

**Self-review is MANDATORY before creating PR.**

Use `/review-phase` command for automated checks.

## Pre-PR Review Checklist

```
[ ] Git Flow: Using feature/* branch (NOT develop/main)
[ ] Commits: Conventional format (<type>: <subject>)
[ ] PR Size: Under 300 lines
[ ] Target Branch: develop
[ ] Code Style: Imports at top, English comments, Type hints
[ ] Dependencies: Added with `uv add` (NOT pip)
[ ] Linting: uv run ruff check ✅
[ ] Formatting: uv run ruff format --check ✅
[ ] Tests: uv run pytest -s ✅
```

## Code Quality Checks

### 1. Code Style (MUST Follow)

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

### 2. Dependencies

```bash
# ✅ CORRECT
uv add httpx

# ❌ WRONG
pip install httpx
```

### 3. Database Models

Check your project's database patterns documentation (e.g., WORKSPACE/DB_PATTERNS.md) for:
- Foreign key usage policy
- Index requirements
- Migration workflow

### 4. Tests Passing

All tests must pass before PR:
```bash
uv run pytest -s

# Expected output:
# ====== X passed in Y.XXs ======
```

### 5. Linting and Formatting

```bash
uv run ruff check              # Code quality - No errors
uv run ruff format --check     # Formatting - No changes needed

# If you need to fix issues:
uv run ruff check --fix        # Auto-fix linting
uv run ruff format             # Apply formatting
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

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Working on develop directly | Create feature/* branch first |
| pip install | Use uv add |
| Korean comments | Use English only |
| Missing type hints | Add types to all functions |
| Imports in functions | Put all imports at top |
| Not running ruff format | Run `uv run ruff format --check` |
| PR over 300 lines | Split into multiple PRs |

## Quick Reference

```bash
# 1. Check current branch
git branch --show-current
# If develop/main → create feature branch!

# 2. Run quality checks
uv run ruff check && uv run ruff format --check && uv run pytest -s

# 3. Check PR size
git diff develop --shortstat

# 4. Create PR with /create-pr
```

---

💬 **Questions about Python code review? Just ask!**
