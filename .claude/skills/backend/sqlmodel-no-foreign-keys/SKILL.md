---
name: sqlmodel-no-foreign-keys
description: SQLModel database modeling for this project with strict NO Foreign Keys policy (ADR-001). Use when defining database models, creating migrations, handling table relationships, or reviewing database code. Provides patterns for index-based references and service-layer data integrity management.
---

# SQLModel - No Foreign Keys

## Overview

This skill provides SQLModel patterns for this project, which **absolutely prohibits** database-level Foreign Key constraints per ADR-001. Use this skill when working with database models, migrations, or any code that references relationships between tables.

## 🔴 CRITICAL RULE: No Foreign Keys

**Foreign Keys are ABSOLUTELY PROHIBITED in this project.**

### ❌ NEVER Do This

```python
from sqlmodel import Field, SQLModel

class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # ❌ WRONG: foreign_key parameter
    sample_id: int = Field(foreign_key="translationsample.id")
```

### ✅ ALWAYS Do This

```python
from sqlmodel import Field, SQLModel

class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # ✅ CORRECT: index only, NO foreign_key
    sample_id: int = Field(index=True)
```

### Why No Foreign Keys? (Quick Summary)

1. **🔓 Database Independence** - Enables future microservice separation
2. **⚡ Performance** - Bulk operations run faster without FK checks
3. **📈 Horizontal Scaling** - Supports sharding across database instances
4. **🧪 Simpler Testing** - Test data cleanup without constraint violations

**For detailed rationale with examples:** Load `references/adr-001-excerpt.md`

## Model Definition Patterns

### 1. Primary Key (Standard Pattern)

```python
from sqlmodel import Field, SQLModel

class TranslationSample(SQLModel, table=True):
    # Always use this pattern for primary keys
    id: int | None = Field(default=None, primary_key=True)
```

### 2. Reference Columns (Foreign Reference)

```python
class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # ✅ Reference to TranslationSample.id
    # Use index=True for query performance
    sample_id: int = Field(index=True)

    # ✅ Other indexed columns
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

**Key points:**
- Use `index=True` on columns that reference other tables
- Index frequently queried columns (e.g., `created_at`, `user_id`)
- Type hints are mandatory

### 3. Unique Constraints

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # ✅ Unique constraint for business logic
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
```

## Handling Relationships

### ❌ DON'T Use SQLModel Relationship()

```python
from sqlmodel import Relationship

# ❌ WRONG: Relationship requires Foreign Keys
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    posts: list["Post"] = Relationship(back_populates="user")  # ❌ NO!
```

### ✅ DO Handle in Service Layer

```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# ✅ CORRECT: JOIN query in service layer
async def get_sample_with_results(
    db: AsyncSession,
    sample_id: int
) -> tuple[TranslationSample, list[TranslationResult]]:
    # Get sample
    sample = await db.get(TranslationSample, sample_id)
    if not sample:
        raise ValueError(f"Sample {sample_id} not found")

    # Get related results
    statement = select(TranslationResult).where(
        TranslationResult.sample_id == sample_id
    )
    results = await db.exec(statement)

    return sample, results.all()
```

## Data Integrity Management

### Problem: Orphan Records

Without Foreign Keys, deleting a parent record doesn't automatically delete children.

### Solution: Service Layer Transactions

```python
from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

# ✅ CORRECT: Handle cascade delete in service
async def delete_sample_with_results(
    db: AsyncSession,
    sample_id: int
) -> None:
    async with db.begin():
        # Delete children first
        await db.exec(
            delete(TranslationResult).where(
                TranslationResult.sample_id == sample_id
            )
        )

        # Then delete parent
        await db.exec(
            delete(TranslationSample).where(
                TranslationSample.id == sample_id
            )
        )
```

**Key points:**
- Wrap related operations in transactions (`async with db.begin()`)
- Delete children before parents to avoid orphans
- Handle integrity checks in service layer, not database

## Pre-Commit Checklist

Before committing model changes:

- [ ] No `foreign_key` parameter in any Field()
- [ ] No `Relationship()` used
- [ ] `index=True` on reference columns (e.g., `sample_id`, `user_id`)
- [ ] Type hints present on all fields
- [ ] Primary key: `id: int | None = Field(default=None, primary_key=True)`
- [ ] Service layer handles data integrity with transactions

## When You Need More

**Detailed ADR-001 rationale?**
→ Load `references/adr-001-excerpt.md`

**Migration questions?**
→ Use `alembic-migrations` skill (coming soon)

**Complex relationship patterns?**
→ Ask me for service layer examples!

---

💬 **Questions about SQLModel patterns or relationships? Just ask!**
