---
name: pr-splitting-strategy
description: This skill should be used when creating pull requests that exceed the recommended size limit (300 lines) or when a large feature needs to be split into multiple PRs. Provides strategies for splitting PRs by documentation, layers, or vertical slices while maintaining logical units and reviewability. Use proactively when planning implementation of complex features.
---

# PR Splitting Strategy

## Overview

Split large pull requests into smaller, reviewable chunks while maintaining logical cohesion and safe rollback points. Apply these strategies before implementation to plan PR sequence.

## When to Split PRs

Split a PR when encountering any of these conditions:

1. **Size threshold**: Total changes exceed 300 lines
2. **Multiple concerns**: Changes mix documentation with implementation, or multiple unrelated features
3. **Dependency chain**: Implementation requires foundational changes first
4. **Risk management**: Experimental code should be separated from stable foundation
5. **Review complexity**: Reviewers cannot easily understand changes in one session

## PR Splitting Patterns

### Pattern 1: Documentation First (Recommended for New Features)

Split design documentation from implementation to enable early feedback on architecture.

**Sequence:**
1. **PR 1: Design Documentation** - WORKSPACE/FEATURES/, ROADMAP updates, architecture diagrams
2. **PR 2: Base Structure** - Empty classes, interfaces, type definitions
3. **PR 3: Utilities** - Helper functions, shared utilities, migrations
4. **PR 4+: Implementation** - Actual business logic, feature components

**Example:**
```
PR #1: Documentation (534 lines)
├─ WORKSPACE/FEATURES/payment_system.md (microservice design)
├─ WORKSPACE/FEATURES/mvp.md (phase updates)
└─ WORKSPACE/ROADMAP.md (timeline updates)

PR #2: payment-service-base (532 lines)
├─ PaymentProcessor (base class)
├─ PaymentGateway (infrastructure)
├─ Settings (configuration)
└─ Tests (16 tests)

PR #3: payment-validation migration (150 lines)
├─ validate_payment() utility
└─ Tests (10 tests)

PR #4: payment-providers/stripe (planned)
└─ Stripe provider implementation
```

**Benefits:**
- Early architecture feedback before writing code
- Clear separation of planning vs execution
- Documentation never lags behind implementation

### Pattern 2: Layer by Layer (Backend/Full-stack Projects)

Split by architectural layers to maintain clean separation of concerns.

**Backend sequence:**
1. **Models** - Database models (SQLModel/SQLAlchemy)
2. **Schemas** - API request/response schemas (Pydantic)
3. **Service** - Business logic layer
4. **Router** - API endpoints (FastAPI/Flask)
5. **Tests** - Comprehensive test coverage

**Full-stack sequence:**
1. **Database layer** - Models, migrations
2. **Backend API** - Services, routers
3. **Frontend types** - TypeScript interfaces
4. **Frontend components** - UI components
5. **Frontend pages** - Page integration
6. **Tests** - E2E tests

**Example:**
```
PR 1: Add Product model (50 lines)
PR 2: Add Product schemas (40 lines)
PR 3: Implement product catalog service (80 lines)
PR 4: Add product catalog endpoints (60 lines)
PR 5: Add product catalog tests (70 lines)
```

**Benefits:**
- Each PR tests a specific layer
- Easy to rollback specific layers
- Clear review focus per PR

### Pattern 3: Vertical Slices (Feature-first)

Complete one feature end-to-end before starting the next. Suitable when features are independent.

**Sequence:**
1. **Feature A** (all layers: model → schema → service → router → tests)
2. **Feature B** (all layers)
3. **Feature C** (all layers)

**Anti-pattern:**
```
❌ PR 1: All models for Features A, B, C
❌ PR 2: All schemas for Features A, B, C
❌ PR 3: All services for Features A, B, C
```

This anti-pattern makes it hard to review and impossible to ship partial functionality.

**Correct:**
```
✅ PR 1: Feature A (model + schema + service + router + tests)
✅ PR 2: Feature B (model + schema + service + router + tests)
✅ PR 3: Feature C (model + schema + service + router + tests)
```

**Benefits:**
- Each PR delivers working functionality
- Can ship features incrementally
- Easier to understand complete feature flow

### Pattern 4: Foundation First (Infrastructure Changes)

When adding infrastructure or refactoring, split by dependency order.

**Sequence:**
1. **Shared library/base classes** - No dependencies
2. **Consumers of shared library** - Depend on PR 1
3. **Integration/glue code** - Depend on PR 1 & 2
4. **Deprecation/cleanup** - Remove old code after new code works

**Example:**
```
PR #1: notification-service-base (foundation)
└─ No dependencies

PR #2: email-provider implementation
└─ Depends on notification-service-base

PR #3: notification-templates
└─ Depends on notification-service-base + email-provider
```

**Benefits:**
- Clear dependency chain
- Each PR builds on stable foundation
- Safe rollback at any point

## PR Size Guidelines

Follow these size recommendations for optimal review quality:

| Size | Lines | Recommendation |
|------|-------|----------------|
| **Ideal** | 100-200 | Perfect for focused review, quick turnaround |
| **Good** | 200-300 | Acceptable, still reviewable in one session |
| **Too Large** | 300-500 | Split if possible, review fatigue sets in |
| **Unacceptable** | 500+ | Must split, cannot be reviewed effectively |

**Exceptions:**
- **Documentation PRs**: Can exceed 300 lines if it's pure markdown
- **Generated code**: Auto-generated migrations, OpenAPI specs
- **New packages**: Initial package structure with tests may exceed 300

**Checking PR size:**
```bash
git diff --stat develop...feature-branch
```

## Granular Commits Within PRs

Even within a single PR, create granular commits for logical units:

**Good commit sequence:**
```bash
# 50 lines
git commit -m "feat: add User model"

# 40 lines
git commit -m "feat: add User schema"

# 80 lines
git commit -m "feat: add user registration service"

# 60 lines
git commit -m "feat: add user registration endpoint"

# 70 lines
git commit -m "test: add user registration tests"
```

**Bad commit sequence:**
```bash
# 300 lines - everything at once
git commit -m "feat: add user registration feature"
```

**Benefits of granular commits:**
- Easier to review commit-by-commit
- Better git bisect for debugging
- Clear history of how feature was built
- Safer cherry-picking and reverting

## Decision Tree: How to Split This PR

Use this decision tree when a PR becomes too large:

```
Is PR > 300 lines?
├─ No → Proceed with single PR
└─ Yes → Does it mix documentation + code?
    ├─ Yes → Split into PR 1 (docs) + PR 2 (code)
    └─ No → Does it contain foundational changes?
        ├─ Yes → Split into PR 1 (foundation) + PR 2 (consumers)
        └─ No → Can it be split by layers?
            ├─ Yes → Split by architectural layers
            └─ No → Split by vertical feature slices
```

## Common Mistakes to Avoid

1. **Mixing concerns in one PR**
   - ❌ Documentation + implementation + refactoring
   - ✅ Separate PRs for each concern

2. **Creating dependent PRs without clear order**
   - ❌ PR A and PR B both modify same files, unclear which merges first
   - ✅ Clear dependency chain: PR A must merge before PR B

3. **Splitting too much**
   - ❌ 10-line PRs that are too fragmented
   - ✅ Aim for 100-200 lines per PR

4. **Artificial splits that break logical units**
   - ❌ Half of a feature in PR 1, other half in PR 2 (both incomplete)
   - ✅ Complete feature in PR 1, next feature in PR 2

5. **Not documenting dependencies between PRs**
   - ❌ PR description doesn't mention it depends on PR #32
   - ✅ Clear "Depends on #32" in PR description

## Examples

### Example 1: Large Microservice Architecture

**Total changes**: ~1,200 lines

**Split strategy**: Documentation First + Foundation First

```
PR #1 (534 lines): Design docs
├─ microservice architecture
├─ API versioning policy
└─ component diagrams

PR #2 (532 lines): Common library
├─ MessageBroker base class
├─ DatabaseConnection wrapper
├─ Settings configuration
└─ 16 tests

PR #3 (150 lines): Utility migration
├─ message_validator utility
└─ 10 tests

PR #4 (planned): Mock service
└─ Implementation using foundation from #1, #2, #3
```

**Result**: 4 reviewable PRs instead of 1 massive 1,200-line PR

### Example 2: User Authentication Feature

**Total changes**: ~600 lines

**Split strategy**: Layer by Layer

```
PR 1 (60 lines): User model
├─ User SQLModel
└─ Alembic migration

PR 2 (50 lines): User schemas
├─ UserCreate schema
├─ UserResponse schema
└─ UserUpdate schema

PR 3 (120 lines): Auth service
├─ register_user()
├─ login_user()
├─ verify_token()
└─ hash_password()

PR 4 (80 lines): Auth endpoints
├─ POST /auth/register
├─ POST /auth/login
└─ GET /auth/me

PR 5 (290 lines): Tests
├─ Model tests (20)
├─ Service tests (50)
└─ API tests (40)
```

**Result**: 5 focused PRs, each testable in isolation

## Tips for Planning PR Splits

1. **Plan splits before implementation** - Don't start coding until you know the PR sequence
2. **Document dependencies** - Use "Depends on #XX" in PR descriptions
3. **Merge in order** - Don't skip ahead in dependency chain
4. **Keep related changes together** - Don't split artificially just to hit line count
5. **Test each PR** - Every PR should have tests and pass CI
6. **Use draft PRs** - Mark dependent PRs as draft until prerequisites merge

## Summary

PR splitting is about balancing **reviewability** with **logical cohesion**:

- **Too large (>300 lines)**: Review fatigue, hard to understand, slow feedback
- **Too small (<50 lines)**: Context switching overhead, fragmented changes
- **Just right (100-200 lines)**: Focused review, clear purpose, quick turnaround

Choose the splitting pattern that best fits the change:
- **Documentation First**: New features with architecture changes
- **Layer by Layer**: Full-stack features following clean architecture
- **Vertical Slices**: Independent features that can ship separately
- **Foundation First**: Infrastructure changes or refactoring

Always prioritize **logical units** over strict line counts. A 350-line PR that completes a cohesive feature is better than two 175-line PRs that split the feature awkwardly.
