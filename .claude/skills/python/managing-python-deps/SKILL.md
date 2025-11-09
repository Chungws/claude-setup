---
name: managing-python-deps
description: Python dependency management using uv (NOT pip). Use when adding/removing packages, running commands, or managing dependencies. Critical rule - NEVER use pip install or edit pyproject.toml directly.
---

# Managing Python Dependencies with uv

## 🔴 CRITICAL RULES

**Use `uv` for ALL dependency management.**

**NEVER use:**
- ❌ `pip install`
- ❌ `poetry add`
- ❌ Direct `pyproject.toml` editing

**ALWAYS use:**
- ✅ `uv add`
- ✅ `uv remove`
- ✅ `uv sync`

## 📦 Workspace Structure

**Use uv workspace with centralized dev dependencies:**

```
project root/
├── pyproject.toml          # Root: Dev dependencies ONLY
├── backend/pyproject.toml  # Production dependencies only
├── worker/pyproject.toml   # Production dependencies only
└── shared/pyproject.toml   # Production dependencies only
```

**Key Rules:**
1. **Dev dependencies** → ONLY in root `pyproject.toml`
2. **Production dependencies** → In each sub-package
3. **Ruff config** → ONLY in root
4. **NO isort** → Ruff handles import sorting

## Adding Dependencies

### Production Dependencies (Sub-package)

```bash
# Navigate to the sub-package
cd backend  # or worker, or shared

# ✅ CORRECT: Add to sub-package
uv add httpx
uv add sqlmodel
uv add "fastapi>=0.100.0"

# ❌ WRONG
pip install httpx                    # pip forbidden!
poetry add httpx                     # poetry not used
echo "httpx" >> pyproject.toml       # direct edit forbidden!
```

### Development Dependencies (Root ONLY)

**CRITICAL: Dev dependencies must be added at root level**

```bash
# Navigate to project root
cd project root

# ✅ CORRECT: Add dev deps to root with --dev flag
uv add pytest --dev
uv add ruff --dev
uv add pytest-asyncio --dev

# ❌ WRONG: Never add dev deps to sub-packages
cd backend && uv add pytest --dev   # WRONG location!
cd worker && uv add ruff --dev      # WRONG location!
```

**Why?**
- Single source of truth for testing/linting tools
- No version conflicts between packages
- Workspace-level tools available everywhere

### Version Constraints

```bash
# Specific version
uv add "httpx==0.25.0"

# Minimum version
uv add "httpx>=0.25.0"

# Version range
uv add "httpx>=0.25.0,<0.26.0"
```

## Removing Dependencies

```bash
# ✅ CORRECT
uv remove httpx
uv remove pytest --dev

# ❌ WRONG
pip uninstall httpx                  # pip forbidden!
# Editing pyproject.toml directly    # direct edit forbidden!
```

## Running Commands

### With uv run (Project Commands)

**In a Workspace, ALWAYS run from project root:**

```bash
# ✅ CORRECT: Run from root using --directory flag
cd project root  # Navigate to root first

# Run tests (uses root dev dependencies)
uv run --directory backend pytest -s
uv run --directory worker pytest -s

# Or use Makefile (recommended)
make test          # Runs all tests
make lint          # Runs all linters

# Run backend server
cd backend && uv run uvicorn vlaarena_backend.main:app --reload

# Run migrations
cd backend && uv run alembic upgrade head
```

**Why from root?**
- Uses centralized dev dependencies (pytest, ruff, etc.)
- Ensures consistent tool versions
- Follows workspace best practices

### With uvx (One-off Tools)

```bash
# ✅ CORRECT: Use uvx for standalone tools (from root)
uvx ruff check                    # Lint all packages
uvx ruff format                   # Format all packages
uvx ruff check --fix              # Auto-fix issues (includes import sorting)

# ❌ WRONG: Don't use isort
uvx isort .                       # isort not needed (ruff does this)
```

**Difference:**
- `uv run` → Uses project's dependencies
- `uvx` → Runs tool in isolated environment (like `npx`)

**Note:** When using ruff, isort is not needed. Ruff handles import sorting with the `I` rule.

## Syncing Dependencies

### Initial Setup

```bash
# Clone repo, first time setup (from root)
cd project root
uv sync --all-extras    # Syncs all workspace members + dev dependencies
```

### After Pulling Changes

```bash
# Someone else added dependencies
git pull origin develop
uv sync --all-extras    # Re-sync workspace
```

### Locked Dependencies

```bash
# Sync with exact versions from uv.lock
uv sync --all-extras --locked
```

**Note:** `--all-extras` ensures dev dependencies are installed from root.

## Git Workflow

### ✅ ALWAYS Commit

```bash
# After uv add/remove, commit these files:
git add pyproject.toml uv.lock
git commit -m "chore: add httpx dependency"
```

### ❌ NEVER Commit

```bash
# .venv/ should be in .gitignore
.venv/          # ❌ Don't commit!
__pycache__/    # ❌ Don't commit!
*.pyc           # ❌ Don't commit!
```

## Common Workflows

### Adding New Feature Dependency (Production)

```bash
# 1. Navigate to sub-package
cd backend  # or worker, or shared

# 2. Add package
uv add httpx

# 3. Return to root and verify
cd ..
make test

# 4. Commit (from root)
git add backend/pyproject.toml uv.lock
git commit -m "chore: add httpx to backend for API calls"
```

### Adding Test Dependency (Development)

```bash
# 1. MUST be at root
cd project root

# 2. Add with --dev to root
uv add pytest-mock --dev

# 3. Verify tests work
make test

# 4. Commit
git add pyproject.toml uv.lock
git commit -m "chore: add pytest-mock for testing"
```

### Updating All Dependencies

```bash
# Update to latest compatible versions (from root)
cd project root
uv sync --all-extras --upgrade

# Test everything still works
make test

# Commit if successful
git add uv.lock
git commit -m "chore: update dependencies"
```

## Pre-Commit Checklist

Before committing dependency changes:

- [ ] Used `uv add` (NOT pip install)
- [ ] Did NOT edit `pyproject.toml` directly
- [ ] Added dev deps to ROOT only (not sub-packages)
- [ ] Added prod deps to correct sub-package (backend/worker/shared)
- [ ] Committed correct `pyproject.toml` and `uv.lock`
- [ ] Ran `make test` from root to verify
- [ ] Did NOT commit `.venv/` directory

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `pip install httpx` | Use `uv add httpx` |
| `cd backend && uv add pytest --dev` | Dev deps ONLY in root! |
| Adding isort | Don't! Ruff handles import sorting |
| Editing pyproject.toml | Use `uv add/remove` commands |
| Forgetting uv.lock | `git add uv.lock` |
| Committing .venv/ | Add to .gitignore |
| `uv run pytest` from sub-package | Use `make test` from root |

## Quick Reference

```bash
# Production dependency → Sub-package
cd backend && uv add <package>

# Dev dependency → Root ONLY
cd /path/to/root && uv add <package> --dev

# Remove dependency
uv remove <package>

# Sync workspace
uv sync --all-extras                # from root
uv sync --all-extras --locked       # exact versions

# Run tests (from root)
make test                           # all tests
uv run --directory backend pytest   # backend only
uv run --directory worker pytest    # worker only

# Linting (from root)
make lint                           # all linters
uvx ruff check                      # check only
uvx ruff check --fix                # auto-fix

# Commit
git add pyproject.toml uv.lock      # root changes
git add backend/pyproject.toml uv.lock  # backend changes
```

---

💬 **Questions about uv or dependency management? Just ask!**
