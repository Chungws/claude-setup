---
name: fastapi-patterns
description: FastAPI architecture patterns for this project. Use when building backend features. Critical rules - 4-layer structure (models → schemas → service → router), business logic in service layer, thin routers, async/await for all DB calls.
---

# FastAPI Architecture Patterns

## 🔴 CRITICAL RULES

1. **4-Layer Structure**: models → schemas → service → router
2. **Business Logic in Service Layer** - Keep routers thin
3. **Async/Await for DB** - All database calls must be async
4. **Dependency Injection** - Use `Depends(get_db)`

## Feature Module Structure

Every feature follows this structure:

```
app/feature/
├── __init__.py
├── models.py      # SQLModel tables
├── schemas.py     # Pydantic schemas (Create/Update/Response)
├── service.py     # Business logic
└── router.py      # API endpoints
```

## 1. Models Layer (models.py)

SQLModel database tables:

```python
# app/translation/models.py
from sqlmodel import Field, SQLModel
from datetime import datetime

class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sample_id: int = Field(index=True)  # NO foreign_key!
    result_text: str
    score: float | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

**Rules:**
- Use SQLModel for tables
- NO foreign keys (index only)
- Type hints required
- Index on frequently queried columns

See `sqlmodel-no-foreign-keys` skill for database modeling rules.

## 2. Schemas Layer (schemas.py)

Pydantic schemas for API:

```python
# app/translation/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

# POST request body
class TranslationResultCreate(BaseModel):
    sample_id: int
    result_text: str
    score: float | None = None

# PUT/PATCH request body
class TranslationResultUpdate(BaseModel):
    result_text: str | None = None
    score: float | None = None

# API response
class TranslationResultResponse(BaseModel):
    id: int
    sample_id: int
    result_text: str
    score: float | None
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLModel compatibility

# Query parameters
class TranslationResultFilter(BaseModel):
    sample_id: int | None = None
    min_score: float | None = None
    limit: int = Field(default=100, le=1000)
```

**Schema Naming Convention:**
- `*Create` - POST request body
- `*Update` - PUT/PATCH request body
- `*Response` - API response
- `*Filter` - Query parameters

## 3. Service Layer (service.py)

Business logic and database operations:

```python
# app/translation/service.py
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import TranslationResult
from .schemas import TranslationResultCreate, TranslationResultUpdate

class TranslationService:
    """Business logic for translations."""

    @staticmethod
    async def create_result(
        db: AsyncSession,
        data: TranslationResultCreate
    ) -> TranslationResult:
        """Create translation result."""
        result = TranslationResult(**data.model_dump())
        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    @staticmethod
    async def get_results(
        db: AsyncSession,
        sample_id: int | None = None,
        limit: int = 100
    ) -> list[TranslationResult]:
        """Get translation results with filters."""
        statement = select(TranslationResult)

        if sample_id:
            statement = statement.where(
                TranslationResult.sample_id == sample_id
            )

        statement = statement.limit(limit)
        results = await db.exec(statement)
        return results.all()

    @staticmethod
    async def update_result(
        db: AsyncSession,
        result_id: int,
        data: TranslationResultUpdate
    ) -> TranslationResult | None:
        """Update translation result."""
        result = await db.get(TranslationResult, result_id)
        if not result:
            return None

        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    @staticmethod
    async def delete_result(
        db: AsyncSession,
        result_id: int
    ) -> bool:
        """Delete translation result."""
        result = await db.get(TranslationResult, result_id)
        if not result:
            return False

        await db.delete(result)
        await db.commit()
        return True
```

**Service Layer Rules:**
- ✅ All business logic here
- ✅ Use `async`/`await` for DB calls
- ✅ Return models or primitives (NOT Response objects)
- ✅ Transaction management with `async with db.begin()`
- ❌ NO HTTP concerns (status codes, HTTPException)

## 4. Router Layer (router.py)

API endpoints (thin layer):

```python
# app/translation/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_db
from .schemas import (
    TranslationResultCreate,
    TranslationResultUpdate,
    TranslationResultResponse,
    TranslationResultFilter
)
from .service import TranslationService

router = APIRouter(
    prefix="/translations",
    tags=["translations"]
)

@router.post(
    "/",
    response_model=TranslationResultResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_translation_result(
    data: TranslationResultCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new translation result."""
    result = await TranslationService.create_result(db, data)
    return result

@router.get(
    "/",
    response_model=list[TranslationResultResponse]
)
async def get_translation_results(
    filters: TranslationResultFilter = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Get translation results with filters."""
    results = await TranslationService.get_results(
        db,
        sample_id=filters.sample_id,
        limit=filters.limit
    )
    return results

@router.get(
    "/{result_id}",
    response_model=TranslationResultResponse
)
async def get_translation_result(
    result_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get translation result by ID."""
    result = await db.get(TranslationResult, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation result not found"
        )
    return result

@router.put(
    "/{result_id}",
    response_model=TranslationResultResponse
)
async def update_translation_result(
    result_id: int,
    data: TranslationResultUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update translation result."""
    result = await TranslationService.update_result(db, result_id, data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation result not found"
        )
    return result

@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_translation_result(
    result_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete translation result."""
    deleted = await TranslationService.delete_result(db, result_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation result not found"
        )
```

**Router Rules:**
- ✅ Thin layer - only request/response handling
- ✅ Dependency Injection with `Depends()`
- ✅ Use `status.HTTP_*` constants
- ✅ Raise `HTTPException` for errors
- ❌ NO business logic in routers

## Dependency Injection

```python
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_db

# Database dependency
async def get_current_user(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    # Validate token and return user
    pass

# Use in router
@router.get("/protected")
async def protected_route(
    user: User = Depends(get_current_user)
):
    return {"user_id": user.id}
```

## Status Codes

```python
from fastapi import status

# Success
status.HTTP_200_OK              # GET, PUT, PATCH
status.HTTP_201_CREATED         # POST
status.HTTP_204_NO_CONTENT      # DELETE

# Client Errors
status.HTTP_400_BAD_REQUEST     # Invalid input
status.HTTP_401_UNAUTHORIZED    # Authentication required
status.HTTP_403_FORBIDDEN       # No permission
status.HTTP_404_NOT_FOUND       # Resource not found
status.HTTP_409_CONFLICT        # Duplicate/conflict

# Server Errors
status.HTTP_500_INTERNAL_SERVER_ERROR
```

## Error Handling

```python
from fastapi import HTTPException, status

# Not found
if not resource:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found"
    )

# Validation error
if invalid_data:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid data provided"
    )

# Permission denied
if not has_permission:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied"
    )
```

## Async/Await Pattern

```python
# ✅ CORRECT: Async DB calls
async def get_user(db: AsyncSession, user_id: int):
    result = await db.get(User, user_id)  # await!
    return result

# ✅ CORRECT: Async query
async def get_users(db: AsyncSession):
    statement = select(User)
    results = await db.exec(statement)  # await!
    return results.all()

# ❌ WRONG: Missing await
async def get_user_wrong(db: AsyncSession, user_id: int):
    result = db.get(User, user_id)  # NO! Missing await
    return result
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Business logic in router | Move to service layer |
| Sync DB calls in async | Add `await` |
| Missing `Depends(get_db)` | Add dependency injection |
| No type hints | Add type hints to all functions |
| Status code as integer | Use `status.HTTP_*` constants |
| Missing response_model | Add `response_model` to router |

## Quick Reference

```python
# 1. Model (SQLModel table)
class Feature(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

# 2. Schemas (Pydantic)
class FeatureCreate(BaseModel): ...
class FeatureResponse(BaseModel): ...

# 3. Service (Business logic)
class FeatureService:
    @staticmethod
    async def create(db: AsyncSession, data: FeatureCreate):
        ...

# 4. Router (API endpoints)
@router.post("/", response_model=FeatureResponse)
async def create_feature(
    data: FeatureCreate,
    db: AsyncSession = Depends(get_db)
):
    return await FeatureService.create(db, data)
```

---

💬 **Questions about FastAPI patterns? Just ask!**
