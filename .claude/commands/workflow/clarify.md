---
description: Clarify feature requirements and design architecture before implementation
---

# Feature Specification Clarification and Architecture Design

Execute after `/new-feature` and before `/start-phase` to clarify requirements and design architecture.

## Purpose

1. **Phase 3 (feature-dev):** Identify unclear parts of specification
2. **Phase 4 (feature-dev):** Compare and select among multiple architecture design options

## Prerequisites

- WORKSPACE/FEATURES/ document must be created via `/new-feature`
- Before `/start-phase` execution

---

## Part 1: Clarifying Questions

### Goal
**Remove all ambiguity before implementation**

### Steps

#### 1️⃣ Read FEATURES document

Ask user:
```
Which feature would you like to clarify?
```

Read and understand the FEATURES document.

#### 2️⃣ Identify unclear parts

Review the following items and find unclear parts:

**Required review items:**

1. **Edge Cases**
   - What if input is empty?
   - What if concurrent requests occur?
   - Are there limits (quota, rate limit)?
   - How to display when no data?

2. **Error Handling**
   - What if API call fails?
   - What if network timeout?
   - What message to show user?
   - Retry policy?

3. **Integration Points**
   - How to integrate with existing features?
   - Dependencies with other teams/services?
   - Data sharing method?

4. **Backward Compatibility**
   - Migrate existing data?
   - Keep existing API as-is?
   - Any breaking changes?

5. **Performance & Scale**
   - Expected traffic/data volume?
   - Response time requirements?
   - Caching needed?
   - DB index strategy?

6. **Design Preferences**
   - UI/UX style? (Follow existing patterns?)
   - Component reuse vs create new?
   - Responsive design needed?

7. **Security & Permissions**
   - Authentication/authorization needed?
   - Data access permissions?
   - How to handle sensitive info?

8. **Testing & Validation**
   - What are success criteria?
   - How to validate?
   - E2E test scope?

#### 3️⃣ Generate and present question list

**Format:**
```markdown
## Clarifying Questions

Need to clarify the following before implementation:

### 1. Edge Cases
1. [Question1]
2. [Question2]

### 2. Error Handling
1. [Question1]
2. [Question2]

### 3. Integration Points
...

**Priority:**
- 🔴 Critical: Must answer (cannot implement)
- 🟡 Important: Recommended to answer (can use defaults)
- 🟢 Optional: Optional

If you can't decide, I can recommend.
```

#### 4️⃣ Wait for user answers and record

**CRITICAL: Don't proceed to next step until answers received!**

If user says "do as you think":
- Present recommendation for each question
- Explain rationale
- Request explicit confirmation

#### 5️⃣ Add Q&A to FEATURES document

Add user answers to FEATURES document:

```markdown
## Clarifications

**Date:** 2025-01-XX

### Edge Cases
- Q: [Question]
- A: [Answer]

### Error Handling
- Q: [Question]
- A: [Answer]

...
```

---

## Part 2: Architecture Design

### Goal
**Compare multiple design options and select optimal approach**

### Steps

#### 1️⃣ Architecture design (3 approaches)

**Option A: Minimal Changes**
- Reuse existing code as much as possible
- Fast implementation
- Trade-off: Possible increased coupling

**Option B: Clean Architecture**
- New abstractions, clean boundaries
- Best maintainability
- Trade-off: More files, refactoring needed

**Option C: Pragmatic Balance**
- Abstract only as needed
- Balance speed and quality
- Trade-off: Medium complexity

**Content for each option:**
```markdown
### Option A: Minimal Changes

**Structure:**
- Backend: Add functions to existing [module]
- Frontend: Add props to existing [component]

**Pros:**
- Fast implementation (estimated time: X hours)
- Low risk

**Cons:**
- Increased coupling
- Harder to test

**File changes:**
- backend/app/[existing-module]/service.py (modify)
- frontend/app/[existing-page]/page.tsx (modify)
```

#### 2️⃣ Present recommendation

**Analysis criteria:**
- Feature complexity (simple/complex)
- Change scope (small/large)
- Maintenance need (short/long term)
- Team context (fast deploy vs quality)

**Recommendation format:**
```markdown
## Architecture Recommendation

**Recommended: Option C (Pragmatic Balance)**

**Rationale:**
- This feature has [complexity], so appropriate abstraction needed
- Maintains consistency with existing [pattern]
- Considering future extensibility, Option C is suitable

**Concrete implementation plan:**
1. Backend:
   - app/[feature]/models.py (new)
   - app/[feature]/schemas.py (new)
   - app/[feature]/service.py (new)
   - app/[feature]/router.py (new)

2. Frontend:
   - app/(dashboard)/[feature]/page.tsx (new)
   - app/(dashboard)/[feature]/[feature]-client.tsx (new)
   - app/(dashboard)/[feature]/service.ts (new)
   - app/(dashboard)/[feature]/use-[feature].ts (new)

Which option would you like to choose?
```

#### 3️⃣ Wait for user selection

**CRITICAL: Don't implement until user selects!**

#### 4️⃣ Add design to FEATURES document

Add selected design to FEATURES document:

```markdown
## Architecture Design

**Selected Option:** Option C (Pragmatic Balance)
**Decision Date:** 2025-01-XX

### Backend Structure
```
app/
  [feature]/
    models.py
    schemas.py
    service.py
    router.py
```

### Frontend Structure
```
app/(dashboard)/
  [feature]/
    page.tsx
    [feature]-client.tsx
    service.ts
    use-[feature].ts
```

### Key Decisions
- [Decision1]
- [Decision2]

### Implementation Priority
1. Phase 1: [...]
2. Phase 2: [...]
```

---

## Completion Report

```markdown
✅ Clarification and design complete!

**Clarified items:**
- Edge cases: [N items]
- Error handling: [N items]
- Integration: [N items]

**Selected architecture:**
- Option [X]: [Name]

**Updated documents:**
- WORKSPACE/FEATURES/[FEATURE].md
  - Added "Clarifications" section
  - Added "Architecture Design" section

**Next steps:**
```bash
/start-phase
```

Now ready to start implementation!
```

---

## Important

### Critical Rules

1. **Stop at question step**
   - Must wait for user answers after Part 1 complete
   - Don't guess

2. **Stop at design step**
   - Must wait for user selection after Part 2 complete
   - Don't start implementation

3. **Documentation first**
   - Record all decisions in FEATURES document
   - Verbal agreements must be documented

### Can skip when

- Very simple feature (single file modification)
- Specification already very concrete
- Urgent bug fix

---

## Workflow Integration

```
/new-feature (Draft initial spec)
    ↓
/clarify (Clarify + Design) ← Current
    ↓
/start-phase (Create branch + Implement)
    ↓
/verify-phase (Quality check)
    ↓
/review-phase (Review + Docs)
    ↓
/create-mr (Create MR)
    ↓
/end-phase (Cleanup)
```

---

## Examples

### Clarification question example

```
User: /clarify

Claude: Read WORKSPACE/FEATURES/API_VERSIONING.md.
        Need to clarify the following:

## Clarifying Questions

### 🔴 Critical

1. **Edge Cases**
   - Q: If cannot get API version info (network failure)?
   - Q: If evaluate multiple times with same version?

2. **Error Handling**
   - Q: What message to user if version info parsing fails?

### 🟡 Important

3. **Integration**
   - Q: Add version field to existing TranslationResult model? New model?

4. **Performance**
   - Q: Cache version info? (TTL?)

### 🟢 Optional

5. **UI/UX**
   - Q: Where to display version info? (Card? Table?)

Please answer and I'll proceed to design phase.
```

### Architecture design example

```
User: [Answers complete]

Claude: After analyzing codebase, presenting 3 options:

## Option A: Minimal Changes
- Just add version field to TranslationResult
- Fast (1-2 hours)
- Con: Hard to add version-specific analysis later

## Option B: Clean Architecture
- Create new APIVersionInfo model
- Separate VersionTracker service
- Elegant, best extensibility
- Con: Many files, refactoring needed (4-6 hours)

## Option C: Pragmatic Balance
- Add version_info (JSON) to TranslationResult
- Add helper functions to service.py
- Balanced (2-3 hours)

**Recommended: Option C**
- API Versioning has medium complexity
- JSON field provides flexibility
- Can split to model later if needed

Which option would you like to choose?
```
