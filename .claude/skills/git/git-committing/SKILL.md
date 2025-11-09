---
name: committing-changes
description: Git commit guidelines for VLA Arena. Use when creating commits or reviewing commit messages. Covers commit format (<type>: <subject>), types, granular commits, and Co-authored-by attribution.
---

# Committing Changes

## Commit Message Format

**Required format:** `<type>: <subject>`

```bash
# ✅ CORRECT
feat: add LLM Judge evaluation
fix: resolve cache invalidation bug
chore: update dependencies

# ❌ WRONG
feat: Added LLM Judge evaluation feature  # Past tense, capitalized
Fix cache bug  # Missing type
add translation models  # Missing type separator (:)
```

## Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat: add translation evaluation` |
| `fix` | Bug fix | `fix: resolve authentication error` |
| `chore` | Build, config, docs | `chore: update package dependencies` |
| `refactor` | Code refactor (no behavior change) | `refactor: simplify query logic` |
| `test` | Add/update tests | `test: add user service tests` |
| `perf` | Performance improvement | `perf: optimize database queries` |
| `docs` | Documentation only | `docs: update API documentation` |
| `style` | Code formatting (no behavior change) | `style: fix linting issues` |

## Subject Rules

### ✅ DO

- **Imperative mood:** Use command form (`add`, `fix`, `update`)
- **Lowercase start:** Begin with lowercase letter
- **No period:** Don't end with `.`
- **≤ 50 characters:** Keep it concise

```bash
✅ feat: add user authentication
✅ fix: resolve memory leak
✅ chore: update webpack config
```

### ❌ DON'T

```bash
❌ feat: Added user authentication    # Past tense
❌ Fix: resolve memory leak          # Capitalized
❌ chore: update webpack config.     # Period at end
❌ feat: add comprehensive user authentication with JWT tokens and refresh mechanism  # Too long (78 chars)
```

## Granular Commits

**Principle:** One logical change per commit

**Keep commits small and focused!**

### Why Small Commits?

1. **Easier Code Review** - Reviewer can understand each change clearly
2. **Better Bug Tracking** - Find which commit introduced a bug
3. **Safe Rollback** - Revert specific changes without losing other work
4. **Clear History** - Git log tells a story of how the feature was built
5. **Atomic Changes** - Each commit is a complete, working unit

### ✅ Good Practice: Split into Logical Units

**Backend example (models → schemas → service → router → tests):**

```bash
# Commit 1: Models (database layer)
git add backend/app/translation/models.py
git commit -m "feat: add TranslationResult model"

# Commit 2: Schemas (API layer)
git add backend/app/translation/schemas.py
git commit -m "feat: add TranslationResult schemas"

# Commit 3: Service (business logic)
git add backend/app/translation/service.py
git commit -m "feat: implement translation evaluation service"

# Commit 4: Router (API endpoints)
git add backend/app/translation/router.py
git commit -m "feat: add translation evaluation endpoints"

# Commit 5: Tests
git add backend/tests/test_translation.py
git commit -m "test: add translation evaluation tests"

# Result: 5 small, focused commits
# Each commit is reviewable, testable, and revertable
```

**Frontend example (types → service → component → page):**

```bash
# Commit 1: Types
git add frontend/app/translations/_types.ts
git commit -m "feat: add translation types"

# Commit 2: API service
git add frontend/app/translations/service.ts
git commit -m "feat: add translation API service"

# Commit 3: Client component
git add frontend/app/translations/translations-client.tsx
git commit -m "feat: add translations client component"

# Commit 4: Server page
git add frontend/app/translations/page.tsx
git commit -m "feat: add translations page"

# Result: 4 small, focused commits
```

### ❌ Bad Practice: Giant Commits

```bash
# ❌ WRONG: Everything in one commit
git add backend/app/translation/*
git commit -m "feat: add translation feature"

# Problems:
# - Mixes models, schemas, service, router, tests
# - Hard to review (reviewer sees 500+ lines at once)
# - Can't revert just the router if it has bugs
# - Git log is not useful ("what changed?" → "everything")
```

### Commit Size Guidelines

- **Ideal:** 10-50 lines per commit
- **Maximum:** 100-200 lines per commit
- **Too large:** 300+ lines → split into multiple commits

```bash
# Check commit size before committing
git diff --stat

# If too large → split with git add -p (interactive)
git add -p file.py  # Select specific hunks
```

## Before Committing

### 1. Check Current Branch

**CRITICAL:** Never commit directly to `develop` or `main`

```bash
# ALWAYS check first!
git branch --show-current

# If on develop/main → create feature branch
git checkout -b feature/your-feature-name
```

### 2. Run Ruff Check (Backend Only)

**For backend changes, run ruff before committing:**

```bash
cd backend

# 1. Check code quality (linting)
uvx ruff check

# 2. Check formatting
uvx ruff format --check

# Both must pass!
# ✅ All checks passed → OK to commit
# ❌ If errors → fix and run again
```

**What each command does:**
- `ruff check` - Code quality (unused imports, bugs, style issues)
- `ruff format --check` - Code formatting (spacing, line breaks, quotes)

**Auto-fix (during development):**
```bash
# Automatically fix issues
uvx ruff check --fix        # Fix linting issues
uvx ruff format             # Apply formatting
```

**Why ruff?**
- Combines formatting (replaces black) + linting (replaces flake8) + import sorting (replaces isort)
- One tool does everything
- Fast and reliable

**Note:** Frontend uses `npm run lint` (different tool)

### 3. Review Changes

```bash
# See what you're committing
git status
git diff

# Stage specific files
git add path/to/file.py

# Check commit size
git diff --cached --stat
# Keep under 100-200 lines per commit!
```

### 4. Write Commit Message

Use HEREDOC for multi-line messages:

```bash
git commit -m "$(cat <<'EOF'
feat: add LLM Judge evaluation

Implements OpenAI GPT-4 based evaluation for translation quality.
Includes score (1-100) and detailed feedback.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Co-Authored-By Attribution

**Always include** when Claude Code creates commits:

```bash
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Placement:** At the end of commit message body

## Quick Reference

```bash
# Complete workflow (Backend)
cd backend
uvx ruff check                    # ← Linting (MUST pass!)
uvx ruff format --check           # ← Formatting (MUST pass!)
git add file.py
git commit -m "feat: add new feature"

# Auto-fix during development (Backend)
uvx ruff check --fix              # Fix linting issues
uvx ruff format                   # Apply formatting

# Complete workflow (Frontend)
cd frontend
npm run lint                      # ← MUST pass!
git add file.tsx
git commit -m "feat: add new component"

# Multi-line commit with attribution
git commit -m "$(cat <<'EOF'
feat: add new feature

Detailed description here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Check commit size before committing
git diff --stat
# Keep under 100-200 lines!

# View recent commits
git log --oneline -n 10
```

## Backend Code Style Rules (MUST Follow)

When writing backend Python code:

### 1. Import Location
✅ **All imports at the top of file**
❌ **NEVER import in the middle of functions/classes**

```python
# ✅ CORRECT
from fastapi import APIRouter
from sqlmodel import Session

def my_function():
    ...

# ❌ WRONG
def my_function():
    from fastapi import APIRouter  # NO!
    ...
```

### 2. Comments in English Only
✅ **Write all comments in English**
❌ **NEVER use Korean in comments**

```python
# ✅ CORRECT
# Calculate the total score
total = sum(scores)

# ❌ WRONG
# 총 점수를 계산합니다  # NO Korean!
total = sum(scores)
```

### 3. Type Hints Required
✅ **Type hints on all function parameters and return values**

```python
# ✅ CORRECT
def get_user(user_id: int, db: Session) -> User | None:
    return db.get(User, user_id)

# ❌ WRONG - Missing type hints
def get_user(user_id, db):
    return db.get(User, user_id)
```

**Note:** Ruff will catch most of these issues automatically.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "added feature" | Use "add feature" (imperative) |
| "feat(backend): add..." | Remove scope, use "feat: add..." |
| Committing to develop | Create feature branch first |
| Giant commit (300+ lines) | Split into 10-50 line commits |
| Not running ruff | Run `uvx ruff check` + `uvx ruff format --check` |
| Korean comments | Use English only |
| Missing type hints | Add types to all functions |
| Missing Co-authored-by | Add Claude attribution |
| Multiple changes in one commit | One logical change per commit |

---

💬 **Questions about commit messages? Just ask!**
