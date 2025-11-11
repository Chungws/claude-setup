---
name: alembic-migrations
description: Database migration management using Alembic. Use when creating/applying migrations after model changes. Critical rule - ALWAYS use --autogenerate, NEVER edit migration files manually (except data migrations). Framework-agnostic, works with any Python project using Alembic.
---

# Alembic Database Migrations

## 🔴 CRITICAL RULE

**ALWAYS use `--autogenerate` for migrations.**

**NEVER manually create or edit migration files** (except data migrations).

## Standard Workflow

### 1. Modify Model

```python
# app/{feature}/models.py
from sqlmodel import Field, SQLModel

class MyModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # ✅ ADD: New field
    description: str | None = Field(default=None)
```

### 2. Auto-Generate Migration

```bash
# ✅ CORRECT: Use --autogenerate
uv run alembic revision --autogenerate -m "add description field to my_model"

# Output example:
# Generating /backend/migrations/versions/abc123_add_description_field.py ...done
```

### 3. Review Generated File

```bash
# Check what was generated
cat migrations/versions/abc123_add_description_field.py
```

**Verify:**
- [ ] Correct table name
- [ ] Correct column type
- [ ] No unexpected changes
- [ ] Both `upgrade()` and `downgrade()` present

### 4. Apply Migration

```bash
# Apply to database
uv run alembic upgrade head

# Verify current version
uv run alembic current
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
# Good practice: test rollback works
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

# 2. Apply other migrations first
uv run alembic upgrade head

# 3. Regenerate your migration
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
    op.add_column('my_table',
        sa.Column('status', sa.String(), nullable=True)
    )

    # ✅ MANUAL: Populate existing rows
    # Comment explaining why manual edit
    op.execute("""
        UPDATE my_table
        SET status = 'pending'
        WHERE status IS NULL
    """)

    # Auto-generated: Make non-nullable
    op.alter_column('my_table', 'status',
        nullable=False)

def downgrade() -> None:
    op.drop_column('my_table', 'status')
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

## Migration Checklist

Before finalizing migration:

- [ ] Used `--autogenerate` (not manual creation)
- [ ] Reviewed generated file
- [ ] Applied migration: `uv run alembic upgrade head`
- [ ] Tested downgrade: `uv run alembic downgrade -1`
- [ ] Tested upgrade again: `uv run alembic upgrade head`
- [ ] Migration file in `migrations/versions/`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating migration file manually | Use `--autogenerate` |
| Editing auto-generated file | Only for data migrations |
| Not testing downgrade | Test `downgrade -1` / `upgrade head` |
| Migration conflict | Delete conflicting file, regenerate |

## Quick Reference

```bash
# Standard workflow
1. Modify model (app/*/models.py)
2. uv run alembic revision --autogenerate -m "description"
3. uv run alembic upgrade head
4. Test: uv run alembic downgrade -1 && uv run alembic upgrade head

# Common commands
uv run alembic current            # Current version
uv run alembic history            # All migrations
uv run alembic upgrade head       # Apply all
uv run alembic downgrade -1       # Rollback one
uv run alembic downgrade base     # Rollback all

# Conflict resolution
rm migrations/versions/conflicting_file.py
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "your changes"
```

---

💬 **Questions about Alembic or migrations? Just ask!**
