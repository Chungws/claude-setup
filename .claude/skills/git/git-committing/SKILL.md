---
name: git-committing
description: Git commit guidelines for any project. Use when creating commits or reviewing commit messages. Covers conventional commits format, granular commit strategy, and Co-authored-by attribution. Framework and language agnostic.
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

### 2. Review Changes

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

### 3. Write Commit Message

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
# 1. Check branch
git branch --show-current
# Must be on feature branch!

# 2. Review changes
git status
git diff
git diff --stat
# Keep under 100-200 lines per commit!

# 3. Stage specific files
git add path/to/file.py

# 4. Commit with message
git commit -m "feat: add new feature"

# Multi-line commit with attribution
git commit -m "$(cat <<'EOF'
feat: add new feature

Detailed description here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# View recent commits
git log --oneline -n 10

# Interactive staging (split changes)
git add -p file.py
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "added feature" | Use "add feature" (imperative) |
| "feat(backend): add..." | Remove scope, use "feat: add..." |
| Committing to develop | Create feature branch first |
| Giant commit (300+ lines) | Split into 10-50 line commits |
| Missing Co-authored-by | Add Claude attribution |
| Multiple changes in one commit | One logical change per commit |
| Past tense in subject | Use imperative mood |
| Capitalized subject | Start with lowercase |

---

💬 **Questions about commit messages? Just ask!**
