---
name: quality-check-python
description: Run Python quality checks (ruff lint/format, pytest). Use before creating commits or PRs. Auto-invoked by /review-phase for Python projects.
---

# Python Quality Checks

Run all Python quality checks before committing or creating PRs.

## Quality Checks

### 1. Linting Check

```bash
ruff check .
```

### 2. Formatting Check

```bash
ruff format --check
```

### 3. Tests

```bash
pytest
# Or with uv:
uv run pytest
```

## Report Format

```markdown
## Python Quality Check Results

### ✅ Linting
- Command: `ruff check .`
- Status: PASSED
- Errors: 0

### ✅ Formatting
- Command: `ruff format --check`
- Status: PASSED

### ✅ Tests
- Command: `pytest`
- Status: PASSED

**Overall: ✅ ALL CHECKS PASSED - Ready for PR**
```

## If Checks Fail

1. **Linting errors**: Fix with `ruff check . --fix`
2. **Formatting errors**: Fix with `ruff format .`
3. **Test failures**: Fix the failing tests

Re-run checks after fixes.
