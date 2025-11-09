---
name: backend-tdd-workflow
description: Test-Driven Development workflow for backend development. Use when implementing backend features, writing tests, or following TDD practices. Covers Red-Green-Refactor cycle, AAA pattern, and test execution. Framework-agnostic principles applicable to any backend project.
---

# Backend TDD Workflow

## 🔴 CRITICAL RULE

**ALWAYS follow Red → Green → Refactor cycle.**

**Test-First is MANDATORY.**

## TDD Cycle

### 1. 🔴 Red: Write Failing Test

Write a test that **fails** because the feature doesn't exist yet.

```python
# tests/test_translation.py
import pytest
from app.translation.service import TranslationService

@pytest.mark.asyncio
async def test_create_translation_result(db_session):
    # Arrange
    service = TranslationService(db_session)
    data = {
        "sample_id": 1,
        "result_text": "Hello World"
    }

    # Act
    result = await service.create_result(data)

    # Assert
    assert result.id is not None
    assert result.result_text == "Hello World"
```

**Run test - it MUST fail:**
```bash
uv run pytest -s tests/test_translation.py::test_create_translation_result
# Expected: FAILED (feature not implemented yet)
```

### 2. 🟢 Green: Minimal Implementation

Write **minimum code** to make the test pass.

```python
# app/translation/service.py
class TranslationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_result(self, data: dict) -> TranslationResult:
        # Minimal implementation
        result = TranslationResult(**data)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result
```

**Run test again - it MUST pass:**
```bash
uv run pytest -s tests/test_translation.py::test_create_translation_result
# Expected: PASSED
```

### 3. 🔵 Refactor: Improve Code

Improve code quality while keeping tests passing.

```python
# app/translation/service.py (refactored)
class TranslationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_result(self, data: dict) -> TranslationResult:
        # Refactored: Better validation, error handling
        if not data.get("sample_id"):
            raise ValueError("sample_id is required")

        result = TranslationResult(**data)
        self.db.add(result)

        try:
            await self.db.commit()
            await self.db.refresh(result)
        except Exception as e:
            await self.db.rollback()
            raise

        return result
```

**Run tests again - still passing:**
```bash
uv run pytest -s
# All tests PASSED
```

## AAA Pattern

**Every test MUST follow AAA structure:**

```python
def test_example():
    # Arrange: Set up test data
    user_id = 1
    data = {"name": "test"}

    # Act: Execute the action
    result = service.create_user(user_id, data)

    # Assert: Verify the result
    assert result.id == user_id
    assert result.name == "test"
```

## Test Coverage Requirements

### ✅ Service Layer: 100% Coverage

```python
# test_translation_service.py

# Test success case
async def test_create_result_success(db_session):
    """Happy path"""
    pass

# Test edge cases
async def test_create_result_invalid_sample_id(db_session):
    """sample_id doesn't exist"""
    pass

async def test_create_result_missing_data(db_session):
    """Missing required fields"""
    pass

# Test error cases
async def test_create_result_db_error(db_session):
    """Database error handling"""
    pass
```

### ✅ Router: Integration Tests

```python
# test_translation_router.py
from fastapi.testclient import TestClient

def test_create_result_endpoint(client: TestClient):
    # Arrange
    data = {
        "sample_id": 1,
        "result_text": "Hello"
    }

    # Act
    response = client.post("/api/v1/translation/results", json=data)

    # Assert
    assert response.status_code == 201
    assert response.json()["result_text"] == "Hello"
```

## Running Tests

### All Tests

```bash
# Run all tests with output
uv run pytest -s

# Run with coverage report
uv run pytest --cov=app --cov-report=term-missing
```

### Specific Tests

```bash
# Single test file
uv run pytest -s tests/test_translation.py

# Single test function
uv run pytest -s tests/test_translation.py::test_create_result_success

# Tests matching pattern
uv run pytest -s -k "translation"
```

### Async Tests

```python
import pytest

# Mark async tests
@pytest.mark.asyncio
async def test_async_function():
    result = await async_service.do_something()
    assert result is not None
```

## Common Patterns

### Testing Database Operations

```python
@pytest.mark.asyncio
async def test_db_operation(db_session):
    # Arrange
    service = MyService(db_session)

    # Act
    result = await service.create_item({"name": "test"})

    # Assert
    assert result.id is not None

    # Verify it's in database
    db_result = await db_session.get(MyModel, result.id)
    assert db_result.name == "test"
```

### Testing Error Handling

```python
@pytest.mark.asyncio
async def test_error_handling(db_session):
    # Arrange
    service = MyService(db_session)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await service.create_item({"invalid": "data"})

    assert "required field" in str(exc_info.value)
```

### Using Fixtures

```python
# conftest.py
@pytest.fixture
async def db_session():
    """Provides a clean database session for each test"""
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
def sample_data():
    """Provides reusable test data"""
    return {
        "name": "test",
        "value": 123
    }

# test_example.py
async def test_with_fixtures(db_session, sample_data):
    """Use fixtures in tests"""
    result = await service.create(db_session, sample_data)
    assert result.name == sample_data["name"]
```

## Pre-Commit Checklist

Before committing backend code:

- [ ] Wrote tests FIRST (Red phase)
- [ ] Tests failed initially
- [ ] Implemented minimal code (Green phase)
- [ ] Tests now pass
- [ ] Refactored code (Refactor phase)
- [ ] Tests still pass
- [ ] All tests pass: `uv run pytest -s`
- [ ] AAA pattern followed in all tests

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing code before tests | Write test first (Red phase) |
| Skipping failing test verification | Run test, see it fail |
| Over-implementing in Green phase | Write MINIMAL code to pass |
| Not refactoring | Always refactor after Green |
| Forgetting @pytest.mark.asyncio | Add decorator to async tests |
| Not testing error cases | Test both success and failure |

## Quick Reference

```bash
# TDD Cycle
1. Red: Write failing test → uv run pytest -s (FAIL)
2. Green: Minimal implementation → uv run pytest -s (PASS)
3. Refactor: Improve code → uv run pytest -s (PASS)

# Run tests
uv run pytest -s                    # all tests
uv run pytest -s tests/test_file.py # specific file
uv run pytest -s -k "pattern"       # pattern match
uv run pytest --cov=app             # with coverage

# Test structure
def test_name():
    # Arrange
    # Act
    # Assert
```

---

💬 **Questions about TDD or testing? Just ask!**
