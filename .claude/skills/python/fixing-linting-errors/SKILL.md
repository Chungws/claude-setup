---
name: fixing-linting-errors
description: Systematic workflow for fixing Python linting errors with ruff. Use when encountering ruff linting errors or when running code quality checks. Critical rule - ALWAYS run ruff and pytest from project root.
---

# Fixing Linting Errors

Systematic workflow for resolving Python linting errors using ruff.

## 🔴 CRITICAL RULE

**ALWAYS run ruff and pytest from the project root directory**, never from sub-packages.

```bash
# ✅ CORRECT - from root
cd /path/to/project-root
uv run ruff check
uv run ruff format
uv run pytest -s

# ❌ WRONG - from sub-package
cd backend
uv run ruff check  # May not respect workspace config
```

**Why?**
- Root `pyproject.toml` contains ruff configuration
- Workspace setup requires root execution
- Dev dependencies are centralized in root

## When to Use

- `uv run ruff check` reports errors
- Pre-commit hooks fail
- Preparing code for PR/MR
- After significant code changes

## Basic Workflow

### Step 1: Run Automatic Fixes

```bash
# From project root
uv run ruff check --fix
```

**Fixes automatically:**
- Import sorting
- Unused imports
- Simple formatting issues
- Code simplifications

### Step 2: Format Code

```bash
uv run ruff format
```

**Applies:**
- Line length enforcement
- Consistent indentation
- Quote normalization

### Step 3: Check Remaining Errors

```bash
uv run ruff check
```

### Step 4: Fix Common Errors

#### Exception Chaining (B904)

```python
# ❌ Error
try:
    something()
except Exception as e:
    raise HTTPException(status_code=500, detail="Failed")

# ✅ Fixed - add "from e"
try:
    something()
except Exception as e:
    raise HTTPException(status_code=500, detail="Failed") from e
```

#### Zip Strict Parameter (B905)

```python
# ❌ Error
for a, b in zip(list1, list2):
    pass

# ✅ Fixed - add "strict=True"
for a, b in zip(list1, list2, strict=True):
    pass
```

#### Pytest Exception Match (B017)

```python
# ❌ Error
with pytest.raises(ValueError):
    some_function()

# ✅ Fixed - add "match" parameter
with pytest.raises(ValueError, match="expected error message"):
    some_function()
```

#### Unused Imports (F401)

```python
# ❌ Error (if unused)
from typing import Optional

# ✅ Remove if truly unused
```

### Step 5: Verify All Pass

```bash
# 1. Check linting (should be 0 errors)
uv run ruff check

# 2. Check formatting
uv run ruff format --check

# 3. Run tests
uv run pytest -s
```

## Example Configuration

Typical ruff configuration in root `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
exclude = [
    "alembic/",  # Auto-generated migrations
    "migrations/",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "RUF",    # Ruff-specific rules
]

ignore = [
    "E501",    # line too long (handled by formatter)
    "B008",    # function call in defaults (for FastAPI Depends)
]
```

**NEVER** add `[tool.ruff]` sections to sub-package pyproject.toml files.

## Important Notes

### Ruff Replaces Multiple Tools

Ruff handles all of these:
- **Formatting** (replaces black)
- **Linting** (replaces flake8)
- **Import sorting** (replaces isort)

**DO NOT** use isort or black alongside ruff.

### Exclusions

Add generated code to exclusions:

```toml
[tool.ruff]
exclude = [
    "alembic/",           # Database migrations
    "migrations/",
    "**/generated/",
    "**/__pycache__/",
]
```

## Common Scenarios

**After refactoring:**
1. Run `uvx ruff check --fix` first
2. Review automatic changes
3. Fix remaining errors manually
4. Run tests

**Pre-commit hook fails:**
1. Ensure you're in project root
2. Run workflow (Steps 1-5)
3. Commit again

**First-time setup:**
1. Add ruff config to root `pyproject.toml`
2. Add exclusions for generated code
3. Run full workflow
4. Commit configuration

## Troubleshooting

**"ruff command not found"**
→ Add ruff as dev dependency: `uv add ruff --dev`

**"Configuration file not found"**
→ Run from project root, not sub-package

**Import sorting differs**
→ Remove isort, use only ruff

**Tests pass but ruff fails**
→ Re-run `uv run ruff check` after manual fixes

## Quick Reference

```bash
# Complete workflow from root
1. uv run ruff check --fix      # Auto-fix
2. uv run ruff format            # Format
3. uv run ruff check             # Check remaining
4. [Fix manual errors]           # B904, B905, B017, F401
5. uv run ruff check             # Verify 0 errors
6. uv run ruff format --check    # Verify formatting
7. uv run pytest -s              # Run tests

# Common fixes
- B904: Add "from e" to exception raises
- B905: Add "strict=True" to zip()
- B017: Add "match=" to pytest.raises()
- F401: Remove unused imports
```

## Checklist

- [ ] Navigate to project root
- [ ] Run `uv run ruff check --fix`
- [ ] Run `uv run ruff format`
- [ ] Check remaining errors: `uv run ruff check`
- [ ] Fix B904, B905, B017, F401 errors
- [ ] Verify: `uv run ruff check` (0 errors)
- [ ] Verify: `uv run ruff format --check`
- [ ] Run tests: `uv run pytest -s`
- [ ] Commit changes

---

💬 **Questions about fixing linting errors? Just ask!**
