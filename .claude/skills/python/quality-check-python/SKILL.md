---
name: quality-check-python
description: Run Python quality checks (ruff lint/format, pytest). Use before creating commits or PRs. Auto-invoked by /review-phase for Python projects.
---

# Python Quality Checks

Run all Python quality checks before committing or creating PRs.

## Prerequisites

Ruff and pytest should be added as dev dependencies in root `pyproject.toml`:

```bash
cd project-root
uv add ruff --dev
uv add pytest --dev
```

## Quality Checks

Run from project root:

### 1. Linting

```bash
uv run ruff check
```

### 2. Formatting

```bash
uv run ruff format --check
```

### 3. Tests

```bash
uv run pytest -s
```

## If Checks Fail

Use the `fixing-linting-errors` skill for detailed troubleshooting and fixes.
