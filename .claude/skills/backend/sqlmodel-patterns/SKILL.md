---
name: sqlmodel-patterns
description: SQLModel database modeling patterns. Use when defining database models, creating migrations, or handling table relationships. Check project-specific database policies before implementation.
---

# SQLModel Database Modeling Patterns

## Overview

This skill provides SQLModel patterns for database modeling. **IMPORTANT:** Always check project-specific database policies before implementing relationships or constraints.

## 🔴 CRITICAL: Check Project Policies First

**Before implementing database models:**

1. **Check for DB policy documents**
   - Look for ADR (Architecture Decision Records)
   - Review project README or WORKSPACE docs
   - Check for existing model patterns in codebase

2. **Common policy questions:**
   - Are Foreign Keys allowed?
   - Relationship modeling approach?
   - Indexing strategy?
   - Naming conventions?

## Standard Model Patterns

### 1. Basic Model Definition

```python
from sqlmodel import Field, SQLModel
from datetime import datetime

class Product(SQLModel, table=True):
    # Primary key (standard pattern)
    id: int | None = Field(default=None, primary_key=True)

    # Required fields
    name: str
    price: float

    # Optional fields
    description: str | None = None

    # Indexed fields (for query performance)
    category_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

**Key points:**
- Type hints are mandatory
- Primary key pattern: `id: int | None = Field(default=None, primary_key=True)`
- Use `index=True` on frequently queried columns

### 2. Unique Constraints

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Unique business constraints
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
```

### 3. Default Values

```python
from datetime import datetime

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Static default
    status: str = Field(default="pending")

    # Dynamic default (function)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional with None default
    completed_at: datetime | None = None
```

## Handling Relationships

### Option A: Using Foreign Keys (If Allowed)

```python
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Relationship (requires FK)
    posts: list["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    # Foreign key
    user_id: int = Field(foreign_key="user.id", index=True)

    # Relationship
    user: User = Relationship(back_populates="posts")
```

**When to use:**
- Project allows Foreign Keys
- Using single database instance
- Need database-level referential integrity

### Option B: Index-Based References (No FK)

```python
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    # Index-based reference (NO foreign_key parameter)
    user_id: int = Field(index=True)
```

**When to use:**
- Project prohibits Foreign Keys
- Planning microservice separation
- Need flexibility for sharding/scaling

**Handle relationships in service layer:**

```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_user_with_posts(
    db: AsyncSession,
    user_id: int
) -> tuple[User, list[Post]]:
    # Get user
    user = await db.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Get related posts
    statement = select(Post).where(Post.user_id == user_id)
    results = await db.exec(statement)

    return user, results.all()
```

## Data Integrity (Without FK)

### Cascade Delete in Service Layer

```python
from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

async def delete_user_with_posts(
    db: AsyncSession,
    user_id: int
) -> None:
    async with db.begin():
        # Delete children first
        await db.exec(
            delete(Post).where(Post.user_id == user_id)
        )

        # Then delete parent
        await db.exec(
            delete(User).where(User.id == user_id)
        )
```

**Key points:**
- Use transactions (`async with db.begin()`)
- Delete children before parents
- Handle integrity in service layer

## Indexing Strategy

### When to Use Indexes

```python
class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # ✅ Index: frequently queried
    category_id: int = Field(index=True)

    # ✅ Index: filtering/sorting
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # ✅ Index: unique business constraint
    sku: str = Field(unique=True, index=True)

    # ❌ No index: rarely queried
    description: str | None = None
```

**Rules of thumb:**
- Index columns used in WHERE clauses
- Index columns used for sorting (ORDER BY)
- Index foreign key references
- Don't over-index (slows down writes)

## Common Patterns

### Soft Delete

```python
class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Soft delete flag
    deleted_at: datetime | None = None
    is_deleted: bool = Field(default=False, index=True)

# Query only non-deleted
statement = select(Product).where(Product.is_deleted == False)
```

### Timestamps

```python
from datetime import datetime

class BaseModel(SQLModel):
    """Base model with timestamps"""
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # Inherits created_at, updated_at
```

### Enums

```python
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
```

## Model Checklist

Before committing model changes:

- [ ] Type hints on all fields
- [ ] Primary key follows standard pattern
- [ ] Checked project DB policy (FK allowed or not?)
- [ ] Indexes on frequently queried columns
- [ ] Unique constraints on business keys
- [ ] Service layer handles relationships/integrity
- [ ] Migration created (if needed)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing type hints | Add types to all fields |
| No indexes on reference columns | Add `index=True` |
| Using FK when prohibited | Check project policy first |
| Not using FK when allowed | Consider using Relationship() |
| Missing transactions for multi-table ops | Use `async with db.begin()` |

## Quick Reference

```python
# Basic model
class MyModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None

# With index
    category_id: int = Field(index=True)

# With unique constraint
    email: str = Field(unique=True, index=True)

# With default
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Optional field
    notes: str | None = None
```

---

💬 **Questions about SQLModel patterns? Just ask!**
