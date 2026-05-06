# Quality Checks

Before committing, always run:
- **Lint**: `ruff check --fix` → `ruff format`
- **Type check**: `mypy .`
- **Tests**: `pytest` (Layer 1+2, with coverage)

Do not commit code with lint errors, type errors, or failing tests.

## Suppression Comments

Every `# noqa` or `# type: ignore` must have an English explanation for why the rule is suppressed.

- `# noqa`: append reason inline (e.g. `# noqa: BLE001 — must catch all to post error`)
- `# type: ignore`: put explanation on the line above (mypy doesn't allow text after `[code]`)
