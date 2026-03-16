# Quality Checks

Before committing, always run:
- **Lint**: `ruff check --fix` → `ruff format`
- **Type check**: `mypy .`
- **Tests**: `pytest` (Layer 1+2, with coverage)

Do not commit code with lint errors, type errors, or failing tests.
