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

**Typical uv workspace with centralized dev dependencies:**

```
project-root/
├── pyproject.toml          # Root: Dev dependencies ONLY
├── package-a/pyproject.toml  # Production dependencies
├── package-b/pyproject.toml  # Production dependencies
└── shared/pyproject.toml     # Production dependencies
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
cd package-a  # or any sub-package

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
cd project-root

# ✅ CORRECT: Add dev deps to root with --dev flag
uv add pytest --dev
uv add ruff --dev
uv add pytest-asyncio --dev

# ❌ WRONG: Never add dev deps to sub-packages
cd package-a && uv add pytest --dev   # WRONG location!
cd package-b && uv add ruff --dev     # WRONG location!
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

**In a Workspace, run from project root:**

```bash
# ✅ CORRECT: Run from root
cd project-root

# Run tests (uses root dev dependencies)
uv run pytest -s

# Run specific package tests
uv run --directory package-a pytest -s

# Run application server
cd package-a && uv run uvicorn app.main:app --reload

# Run migrations
cd package-a && uv run alembic upgrade head
```

**Why from root?**
- Uses centralized dev dependencies (pytest, ruff, etc.)
- Ensures consistent tool versions
- Follows workspace best practices

### With uv run (Tools from Dev Dependencies)

```bash
# ✅ CORRECT: Use uv run for dev tools (from root)
uv run ruff check                    # Lint all packages
uv run ruff format                   # Format all packages
uv run ruff check --fix              # Auto-fix issues (includes import sorting)

# ❌ WRONG: Don't use isort
uv run isort .                       # isort not needed (ruff does this)
```

**Note:** Ruff handles import sorting with the `I` rule. isort is not needed.

## Syncing Dependencies

### Initial Setup

```bash
# Clone repo, first time setup (from root)
cd project-root
uv sync --all-extras    # Syncs all workspace members + dev dependencies
```

### After Pulling Changes

```bash
# Someone else added dependencies
git pull
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

### Adding Production Dependency

```bash
# 1. Navigate to sub-package
cd package-a

# 2. Add package
uv add httpx

# 3. Return to root and verify
cd ..
uv run pytest -s

# 4. Commit (from root)
git add package-a/pyproject.toml uv.lock
git commit -m "chore: add httpx for API calls"
```

### Adding Development Dependency

```bash
# 1. MUST be at root
cd project-root

# 2. Add with --dev to root
uv add pytest-mock --dev

# 3. Verify tests work
uv run pytest -s

# 4. Commit
git add pyproject.toml uv.lock
git commit -m "chore: add pytest-mock for testing"
```

### Updating Dependencies

```bash
# Update to latest compatible versions (from root)
cd project-root
uv sync --all-extras --upgrade

# Test everything still works
uv run pytest -s

# Commit if successful
git add uv.lock
git commit -m "chore: update dependencies"
```

## Dependency Checklist

Before committing dependency changes:

- [ ] Used `uv add` (NOT pip install)
- [ ] Did NOT edit `pyproject.toml` directly
- [ ] Added dev deps to ROOT only (not sub-packages)
- [ ] Added prod deps to correct sub-package
- [ ] Committed correct `pyproject.toml` and `uv.lock`
- [ ] Ran tests to verify: `uv run pytest -s`
- [ ] Did NOT commit `.venv/` directory

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `pip install httpx` | Use `uv add httpx` |
| Dev deps in sub-package | Dev deps ONLY in root! |
| Adding isort | Don't! Ruff handles import sorting |
| Editing pyproject.toml | Use `uv add/remove` commands |
| Forgetting uv.lock | `git add uv.lock` |
| Committing .venv/ | Add to .gitignore |
| Running pytest from sub-package | Run from root |

## Quick Reference

```bash
# Production dependency → Sub-package
cd package-name && uv add <package>

# Dev dependency → Root ONLY
cd project-root && uv add <package> --dev

# Remove dependency
uv remove <package>

# Sync workspace (from root)
uv sync --all-extras                # install all
uv sync --all-extras --locked       # exact versions
uv sync --all-extras --upgrade      # update all

# Run tests (from root)
uv run pytest -s                    # all tests
uv run --directory package-a pytest # specific package

# Linting (from root)
uv run ruff check                   # check only
uv run ruff check --fix             # auto-fix
uv run ruff format                  # format code

# Commit
git add pyproject.toml uv.lock                # root changes
git add package-a/pyproject.toml uv.lock      # package changes
```

---

💬 **Questions about uv or dependency management? Just ask!**
