---
name: alembic-migrations
description: Database migration management for this project using Alembic. Use when creating/applying migrations after model changes. Critical rule - ALWAYS use --autogenerate, NEVER edit migration files manually (except data migrations).
---

# Alembic Database Migrations

## 🔴 CRITICAL RULE

**ALWAYS use `--autogenerate` for migrations.**

**NEVER manually create or edit migration files** (except data migrations).

## Standard Workflow

### 1. Modify Model

```python
# app/translation/models.py
from sqlmodel import Field, SQLModel

class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sample_id: int = Field(index=True)
    result_text: str
    # ✅ ADD: New field
    score: float | None = Field(default=None)
```

### 2. Ensure PostgreSQL Running

```bash
# Start database
docker compose up -d

# Verify it's running
docker compose ps
```

### 3. Auto-Generate Migration

```bash
# ✅ CORRECT: Use --autogenerate
uv run alembic revision --autogenerate -m "add score field to translation_result"

# Output example:
# Generating /backend/migrations/versions/abc123_add_score_field.py ...done
```

### 4. Review Generated File

```bash
# Check what was generated
cat migrations/versions/abc123_add_score_field.py
```

**Verify:**
- [ ] Correct table name
- [ ] Correct column type
- [ ] No unexpected changes
- [ ] Both `upgrade()` and `downgrade()` present

### 5. Apply Migration

```bash
# Apply to database
uv run alembic upgrade head

# Verify current version
uv run alembic current
```

### 6. Commit Together

```bash
# Commit model + migration together
git add app/translation/models.py
git add migrations/versions/abc123_add_score_field.py
git commit -m "feat: add score field to TranslationResult"
```

## Common Operations

### Check Current Version

```bash
# See current migration version
uv run alembic current

# Output: abc123 (head)
```

### View History

```bash
# See all migrations
uv run alembic history

# See recent migrations
uv run alembic history | head -20
```

### Downgrade (Rollback)

```bash
# Rollback one migration
uv run alembic downgrade -1

# Rollback to specific version
uv run alembic downgrade abc123

# Rollback all
uv run alembic downgrade base
```

### Test Up/Down Cycle

```bash
# Good practice before committing
uv run alembic downgrade -1
uv run alembic upgrade head
```

## Migration Conflicts

### Problem: Revision Conflict

```bash
# Error: Multiple head revisions present
alembic.util.exc.CommandError: Multiple head revisions
```

### Solution: Delete & Regenerate

```bash
# 1. Delete the conflicting migration file
rm migrations/versions/abc123_your_migration.py

# 2. Pull latest migrations
git pull origin develop

# 3. Regenerate your migration
uv run alembic upgrade head  # Apply others first
uv run alembic revision --autogenerate -m "your changes"
```

## Data Migrations (Exception)

**Only case where manual editing is allowed:**

### When Needed

- Transform existing data
- Populate new non-nullable columns
- Complex data changes

### Process

```bash
# 1. Auto-generate structure first
uv run alembic revision --autogenerate -m "add required field"

# 2. Edit generated file to add data transformation
# migrations/versions/abc123_add_required_field.py
```

Example:

```python
def upgrade() -> None:
    # Auto-generated: Add column (nullable first)
    op.add_column('translation_result',
        sa.Column('status', sa.String(), nullable=True)
    )

    # ✅ MANUAL: Populate existing rows
    # Comment explaining why manual edit
    op.execute("""
        UPDATE translation_result
        SET status = 'pending'
        WHERE status IS NULL
    """)

    # Auto-generated: Make non-nullable
    op.alter_column('translation_result', 'status',
        nullable=False)

def downgrade() -> None:
    op.drop_column('translation_result', 'status')
```

**Important:**
- Add comment explaining manual edit
- Test thoroughly
- Include in code review

## Common Patterns

### Adding Column

```python
# Model change
class MyModel(SQLModel, table=True):
    new_field: str | None = Field(default=None)  # nullable first!

# Generate & apply
uv run alembic revision --autogenerate -m "add new_field to my_model"
uv run alembic upgrade head
```

### Adding Index

```python
# Model change
class MyModel(SQLModel, table=True):
    user_id: int = Field(index=True)  # Add index=True

# Generate & apply
uv run alembic revision --autogenerate -m "add index to user_id"
uv run alembic upgrade head
```

### Renaming Column (Manual)

```python
# Migration file (after autogenerate)
def upgrade() -> None:
    # Alembic sees drop + add, but we want rename
    op.alter_column('my_table', 'old_name',
        new_column_name='new_name')

def downgrade() -> None:
    op.alter_column('my_table', 'new_name',
        new_column_name='old_name')
```

## Pre-Commit Checklist

Before committing migration:

- [ ] Used `--autogenerate` (not manual creation)
- [ ] Reviewed generated file
- [ ] Applied migration: `uv run alembic upgrade head`
- [ ] Tested downgrade: `uv run alembic downgrade -1`
- [ ] Tested upgrade again: `uv run alembic upgrade head`
- [ ] Committed model + migration together
- [ ] Migration file in `migrations/versions/`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating migration file manually | Use `--autogenerate` |
| Editing auto-generated file | Only for data migrations |
| Not testing downgrade | Test `downgrade -1` / `upgrade head` |
| Forgetting to commit migration | `git add migrations/versions/` |
| Migration conflict | Delete, pull, regenerate |
| Not running PostgreSQL | `docker compose up -d` |

## Quick Reference

```bash
# Standard workflow
1. Modify model (app/*/models.py)
2. docker compose up -d
3. uv run alembic revision --autogenerate -m "description"
4. uv run alembic upgrade head
5. git add app/*/models.py migrations/versions/*.py

# Common commands
uv run alembic current            # Current version
uv run alembic history            # All migrations
uv run alembic upgrade head       # Apply all
uv run alembic downgrade -1       # Rollback one
uv run alembic downgrade base     # Rollback all

# Conflict resolution
rm migrations/versions/conflicting_file.py
git pull origin develop
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "your changes"
```

---

💬 **Questions about Alembic or migrations? Just ask!**
