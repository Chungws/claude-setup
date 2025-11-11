---
name: reviewing-typescript
description: TypeScript code review checklist. Use before creating PR for TypeScript/JavaScript projects. Covers type safety, linting, testing, and common TypeScript patterns.
---

# TypeScript Code Review Checklist

## 🔴 CRITICAL RULE

**Self-review is MANDATORY before creating PR.**

Use `/review-phase` command for automated checks.

## Pre-PR Review Checklist

```
[ ] Git Flow: Using feature/* branch (NOT develop/main)
[ ] Commits: Conventional format (<type>: <subject>)
[ ] PR Size: Under 300 lines
[ ] Target Branch: develop
[ ] Linting: npm run lint ✅
[ ] Type Check: npm run type-check ✅ (if available)
[ ] Tests: npm test ✅ (if available)
[ ] UI Verification: Manual verification ✅ (MANDATORY for UI changes!)
```

## Code Quality Checks

### 1. TypeScript Type Safety

**Type annotations:**
```typescript
// ✅ CORRECT - Explicit types
function getUser(userId: number): User | null {
  return users.find(u => u.id === userId) ?? null
}

// ❌ WRONG - Missing types
function getUser(userId) {
  return users.find(u => u.id === userId)
}
```

**Avoid `any`:**
```typescript
// ❌ WRONG
const data: any = await fetch(...)

// ✅ CORRECT
interface Response {
  data: User[]
}
const data: Response = await fetch(...)
```

### 2. React/Next.js Patterns

**Server Component (page.tsx):**
```typescript
// ✅ CORRECT: async, no "use client"
export default async function Page() {
  const data = await service.getAll()
  return <Client data={data} />
}

// ❌ WRONG: useState in Server Component
export default function Page() {
  const [data, setData] = useState([])  // NO!
}
```

**Client Component (*-client.tsx):**
```typescript
// ✅ CORRECT: "use client" at top
"use client"
export default function FeatureClient({ data }: Props) {
  const { mutate } = useFeature()
  return <Button onClick={...}>
}
```

### 3. Component Library Usage

Check your project's component library documentation (e.g., shadcn/ui, Material-UI):

```tsx
// ❌ WRONG: Raw HTML
<button className="bg-blue-500">Click</button>

// ✅ CORRECT: Use project's component library
import { Button } from "@/components/ui/button"
<Button variant="default">Click</Button>
```

### 4. API Calls

Use project's API client (e.g., apiClient, axios instance):

```typescript
// ❌ WRONG: Direct fetch
const data = await fetch('/api/users')

// ✅ CORRECT: Use apiClient
import { apiClient } from '@/lib/apiClient'
const data = await apiClient.get('/api/users')
```

### 5. Linting

```bash
npm run lint

# If you need to fix issues:
npm run lint -- --fix
```

### 6. UI Verification (MANDATORY for UI changes)

**If you changed any UI:**
1. Start dev server: `npm run dev`
2. Manually verify in browser:
   - Page loads correctly
   - Components render properly
   - No console errors (F12)
   - Layout not broken
   - Test interactions (buttons, forms, etc.)

See `frontend-ui-testing` skill for detailed verification process.

## PR Size Guidelines

```bash
# Check changes
git diff develop --shortstat

# ✅ GOOD: Under 300 lines
25 files changed, 142 insertions(+), 37 deletions(-)

# ⚠️ WARNING: Over 300 lines - consider splitting
45 files changed, 523 insertions(+), 189 deletions(-)
```

**If over 300 lines:**
- Split into multiple PRs
- Separate code and documentation changes
- Break down Phase into smaller tasks

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Working on develop directly | Create feature/* branch first |
| Using `any` type | Define proper interfaces |
| Missing type annotations | Add types to all functions |
| Raw HTML elements | Use project's component library |
| Direct fetch calls | Use apiClient |
| UI not verified | Manual browser verification |
| PR over 300 lines | Split into multiple PRs |
| Not running lint | Run `npm run lint` |

## Quick Reference

```bash
# 1. Check current branch
git branch --show-current
# If develop/main → create feature branch!

# 2. Run quality checks
npm run lint
npm run type-check  # if available
npm test            # if available

# 3. Check PR size
git diff develop --shortstat

# 4. If UI changed: Manual verification
npm run dev
# Open browser, test UI, check console

# 5. Create PR with /create-pr
```

---

💬 **Questions about TypeScript code review? Just ask!**
