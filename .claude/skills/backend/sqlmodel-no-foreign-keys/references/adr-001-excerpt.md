# ADR-001: No Foreign Keys - Detailed Rationale

**Status:** Decided
**Date:** 2025-09-25

## Decision

Database-level `FOREIGN KEY` constraints are **NOT USED** in this project.

Table relationships are managed at the application code level. For example, `TranslationResult` has a `sample_id` field referencing `TranslationSample.id`, but without a Foreign Key constraint.

## Why? (4 Key Reasons)

### 1. Database Independence & Flexibility

Foreign Key constraints tightly couple database schemas, creating obstacles when:
- **Splitting into microservices:** Moving tables to separate databases requires removing FKs first
- **Migrating databases:** Different databases have different FK implementations
- **Schema evolution:** Changing relationships requires complex constraint management

**Example scenario:** If we later split translation evaluation into a separate service, we can move `TranslationResult` to another database without FK migration complexity.

### 2. Development Environment Simplicity

Foreign Keys complicate common development tasks:
- **Test data management:** Creating test fixtures requires careful insertion order
- **Data cleanup:** Deleting test data requires reverse dependency order
- **Partial backups:** Restoring subset of data triggers constraint violations

**Without FKs:** Tests can freely create/delete data in any order within transactions.

### 3. Performance Optimization

Foreign Key checks add overhead to bulk operations:
- **Bulk inserts:** FK validation on each row slows down batch imports
- **Updates/Deletes:** Cascade checks scan related tables
- **Index management:** FKs create implicit indexes that may conflict with optimization

**Real impact:** Inserting 10,000 translation results is faster without FK constraint checks.

### 4. Horizontal Scaling (Sharding)

Future system growth may require sharding:
- **Cross-shard FKs impossible:** Parent and child records may live on different database instances
- **Distributed transactions complex:** Maintaining FK integrity across shards requires 2-phase commits
- **Flexibility preserved:** No FK constraints means sharding-ready from day one

**Forward-thinking:** Even if we don't shard now, avoiding FKs keeps that option open.

## Consequences

### Positive

✅ Schema changes are simpler and faster
✅ Testing requires less setup boilerplate
✅ Microservice extraction is straightforward
✅ Bulk operations perform better
✅ Horizontal scaling remains feasible

### Negative & Mitigation

❌ **Risk:** Orphan records (children without parents) can occur

✅ **Mitigation:** Enforce data integrity in service layer with transactions

#### Example: Cascade Delete Pattern

```python
from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

async def delete_sample_with_results(
    db: AsyncSession,
    sample_id: int
) -> None:
    """
    Delete a TranslationSample and all its TranslationResults.

    Service layer ensures referential integrity via transaction.
    """
    async with db.begin():
        # Step 1: Delete children first
        await db.exec(
            delete(TranslationResult).where(
                TranslationResult.sample_id == sample_id
            )
        )

        # Step 2: Then delete parent
        await db.exec(
            delete(TranslationSample).where(
                TranslationSample.id == sample_id
            )
        )

        # If any step fails, entire transaction rolls back
        # = Data integrity maintained!
```

#### Example: Referential Integrity Check

```python
async def create_translation_result(
    db: AsyncSession,
    sample_id: int,
    result_data: dict
) -> TranslationResult:
    """
    Create a TranslationResult, ensuring parent exists.

    Service layer validates reference before insert.
    """
    # Check parent exists (replaces FK constraint check)
    sample = await db.get(TranslationSample, sample_id)
    if not sample:
        raise ValueError(f"TranslationSample {sample_id} not found")

    # Now safe to create child
    result = TranslationResult(sample_id=sample_id, **result_data)
    db.add(result)
    await db.commit()

    return result
```

## Implementation Guidelines

**DO:**
- ✅ Add `index=True` on reference columns (e.g., `sample_id`) for query performance
- ✅ Wrap related create/update/delete in service layer transactions
- ✅ Validate parent existence before creating child records
- ✅ Delete children before parents to avoid orphans

**DON'T:**
- ❌ Use `Field(foreign_key="table.column")`
- ❌ Use SQLModel `Relationship()` (requires FKs)
- ❌ Assume database enforces referential integrity
- ❌ Create/delete records outside service layer

---

**Full Document:** `WORKSPACE/ARCHITECTURE/ADR_001-No_Foreign_Keys.md`
**Related Skill:** `sqlmodel-no-foreign-keys`
