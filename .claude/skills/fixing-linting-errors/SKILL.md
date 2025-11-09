---
name: fixing-linting-errors
description: Systematic workflow for fixing Python linting errors with ruff in uv workspace projects. Use when encountering ruff linting errors or when running code quality checks. Critical rule - ALWAYS run ruff and pytest from project root, not from sub-packages. (project)
---

# Fixing Linting Errors

Systematic workflow for resolving Python linting errors using ruff in uv workspace projects.

## Overview

This skill provides a step-by-step process for fixing linting errors detected by ruff, the Python linter and formatter used in this project. Follow this workflow when ruff checks fail or when preparing code for commit.

**Key Principle:** All linting and testing commands MUST be run from the project root directory, never from sub-packages (backend, worker, shared). This ensures consistent behavior across the workspace.

---

## When to Use This Skill

Use this skill when:
- `uvx ruff check` reports linting errors
- Pre-commit hooks fail due to linting issues
- Preparing code for PR review
- After making significant code changes
- Setting up linting configuration for new code

---

## Critical Rules

### 1. Always Run from Root

**ALWAYS** run ruff and pytest from the project root directory:

```bash
# ✅ CORRECT - from root
cd /path/to/project-root
uvx ruff check
uvx ruff format
uv run pytest -s

# ❌ WRONG - from sub-package
cd backend
uvx ruff check  # This may not respect workspace config
```

**Why?**
- Root `pyproject.toml` contains the ruff configuration
- uv workspace requires root execution for consistent behavior
- Dev dependencies (pytest, ruff) are centralized in root

### 2. Ruff Configuration Location

**ONLY** the root `pyproject.toml` should contain ruff configuration:

```toml
# ✅ Root pyproject.toml
[tool.ruff]
line-length = 100
exclude = [
    "backend/alembic/",  # Auto-generated migrations
]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "C4", "SIM", "RUF"]
ignore = ["E501", "B008"]
```

**NEVER** add `[tool.ruff]` sections to sub-package pyproject.toml files.

### 3. Ruff Handles Import Sorting

**DO NOT** use `isort` - ruff's `I` rule handles import sorting:

```bash
# ✅ CORRECT
uvx ruff check --fix  # Fixes imports + other issues

# ❌ WRONG
uvx isort .  # Redundant, conflicts with ruff
```

---

## Workflow: Fixing Linting Errors

Follow these steps in order when encountering linting errors.

### Step 1: Run Automatic Fixes

Start by letting ruff fix what it can automatically:

```bash
# From project root
uvx ruff check --fix
```

**What this fixes:**
- Import sorting (alphabetical, stdlib → third-party → local)
- Unused imports
- Simple formatting issues
- Some code simplifications

**Expected output:**
```
Found 149 errors (126 fixed, 23 remaining).
```

### Step 2: Format Code

Apply consistent code formatting:

```bash
# From project root
uvx ruff format
```

**What this does:**
- Line length enforcement (max 100 chars)
- Consistent indentation
- Quote normalization
- Trailing comma handling

**Expected output:**
```
7 files reformatted
```

### Step 3: Identify Remaining Errors

Check what errors remain:

```bash
# From project root
uvx ruff check
```

**Common remaining error types:**

1. **B904: Exception chaining**
   ```python
   # ❌ Error
   try:
       something()
   except Exception as e:
       raise HTTPException(status_code=500, detail="Failed")

   # ✅ Fixed
   try:
       something()
   except Exception as e:
       raise HTTPException(status_code=500, detail="Failed") from e
   ```

2. **B905: zip() without strict parameter**
   ```python
   # ❌ Error
   for a, b in zip(list1, list2):
       pass

   # ✅ Fixed
   for a, b in zip(list1, list2, strict=True):
       pass
   ```

3. **B017: Blind exception assertion**
   ```python
   # ❌ Error
   with pytest.raises(ValueError):
       some_function()

   # ✅ Fixed
   with pytest.raises(ValueError, match="expected error message"):
       some_function()
   ```

4. **F401: Unused imports**
   ```python
   # ❌ Error (if unused)
   from typing import Optional

   # ✅ Remove if truly unused
   ```

### Step 4: Manual Fixes

Fix remaining errors by category:

#### Exception Chaining (B904)

**Pattern:** Add `from e` to all exception raises inside except blocks

**Search pattern:** Look for `raise` statements inside `except` blocks

**Fix approach:**
```bash
# Find all files with exception handling
uvx ruff check | grep B904
```

For each file, add `from e`:
```python
raise HTTPException(...) from e
raise ValueError(...) from e
raise RuntimeError(...) from e
```

#### Zip Strict Parameter (B905)

**Pattern:** Add `strict=True` to all `zip()` calls

**Fix approach:**
```bash
# Find all zip() usage
uvx ruff check | grep B905
```

Add `strict=True`:
```python
zip(list1, list2, strict=True)
zip(items, range(len(items)), strict=False)  # If intentionally different lengths
```

#### Blind Exception Assertions (B017)

**Pattern:** Add `match=` parameter to `pytest.raises()`

**Fix approach:**
```python
# Add expected error message pattern
with pytest.raises(ValueError, match="Invalid input"):
    function_that_should_fail()
```

### Step 5: Verify All Checks Pass

After manual fixes, verify:

```bash
# 1. Run ruff check (should report 0 errors)
uvx ruff check

# 2. Run ruff format check
uvx ruff format --check

# 3. Run all tests (from root)
uv run pytest -s
```

**Expected output:**
```
All checks passed!
203 passed in 3.5s
```

---

## Common Scenarios

### Scenario 1: First-Time Setup

When setting up linting for a new project:

1. Ensure root `pyproject.toml` has ruff config
2. Add exclusions for generated code (alembic, etc.)
3. Run full workflow (Steps 1-5)
4. Commit ruff configuration

### Scenario 2: After Major Refactoring

When significant code changes introduce many errors:

1. Run automatic fixes first (`--fix`)
2. Review changes before committing
3. Fix remaining errors by category
4. Run tests to ensure no breakage

### Scenario 3: Pre-Commit Hook Failure

When pre-commit hooks fail:

1. Run workflow from root (not sub-package!)
2. Check that root pyproject.toml is being used
3. Verify no sub-package has conflicting ruff config
4. Re-run commit

### Scenario 4: Adding New Exclusions

When generated code causes false positives:

1. Add to root `pyproject.toml`:
   ```toml
   [tool.ruff]
   exclude = [
       "backend/alembic/",
       "path/to/generated/",
   ]
   ```

2. Verify exclusion works:
   ```bash
   uvx ruff check
   ```

---

## Project-Specific Patterns

### This Project's Ruff Configuration

```toml
[tool.ruff]
line-length = 100
exclude = [
    "backend/alembic/",  # Auto-generated Alembic migrations
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
    "B008",    # function call in argument defaults (For FastAPI)
]
```

### Common Error Counts by Type

From recent experience (PR #29):
- **Total errors:** 149
- **Auto-fixed:** 126 (85%)
- **Manual fixes needed:** 23 (15%)
  - B904 (exception chaining): ~20 errors
  - B905 (zip strict): ~2 errors
  - B017 (blind assertion): ~1 error

---

## Troubleshooting

### Issue: "ruff command not found"

**Solution:** Run with `uvx` prefix from root:
```bash
uvx ruff check  # NOT just 'ruff check'
```

### Issue: "Configuration file not found"

**Cause:** Running from sub-package instead of root

**Solution:**
```bash
cd /path/to/project-root  # Go to root first
uvx ruff check
```

### Issue: Tests pass but ruff still fails

**Cause:** Forgot to run ruff after manual fixes

**Solution:**
```bash
uvx ruff check --fix  # Re-run after changes
```

### Issue: Import sorting differs from expectation

**Cause:** Using both isort and ruff

**Solution:** Remove isort, use only ruff:
```bash
# Remove isort from dependencies
# Use only: uvx ruff check --fix
```

---

## Checklist

Use this checklist when fixing linting errors:

- [ ] Navigate to project root directory
- [ ] Run `uvx ruff check --fix` (automatic fixes)
- [ ] Run `uvx ruff format` (code formatting)
- [ ] Run `uvx ruff check` (identify remaining errors)
- [ ] Fix B904 errors (add `from e` to exceptions)
- [ ] Fix B905 errors (add `strict=True` to zip)
- [ ] Fix B017 errors (add `match=` to pytest.raises)
- [ ] Run `uvx ruff check` (verify 0 errors)
- [ ] Run `uvx ruff format --check` (verify formatting)
- [ ] Run `uv run pytest -s` (ensure tests pass)
- [ ] Commit changes

---

## References

- **Ruff documentation:** https://docs.astral.sh/ruff/
- **Root config location:** `pyproject.toml` (root only)
- **Related skills:** `reviewing-code`, `backend-tdd-workflow`

---

**Last Updated:** 2025-01-07
**Related PR:** #29 (149 errors fixed)
