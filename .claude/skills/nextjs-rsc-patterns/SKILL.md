---
name: nextjs-rsc-patterns
description: Next.js React Server Components patterns for Dudaji Dashboard. Use when building frontend features. Critical rules - page.tsx is async Server Component, use *-client.tsx for interactivity, router.refresh() after mutations, apiClient for API calls.
---

# Next.js RSC (React Server Components) Patterns

## 🔴 CRITICAL RULES

1. **`page.tsx` = Server Component (async)**
2. **`*-client.tsx` = Client Component ("use client")**
3. **NO useState/useEffect/onClick in page.tsx**
4. **Use standard file structure (below)**

## File Structure Pattern

**Standard structure for any feature:**

```
feature/
├── _types.ts              # TypeScript types
├── service.ts             # API calls (apiClient)
├── use-feature.ts         # Custom hook (mutations)
├── feature-client.tsx     # Client Component
├── page.tsx               # Server Component
└── create-feature-modal.tsx  # Modal (if needed)
```

## 1. Types (_types.ts)

```typescript
// _types.ts
export interface Feature {
  id: number
  name: string
  created_at: string
}

export interface FeatureFormData {
  name: string
}
```

## 2. API Service (service.ts)

```typescript
// service.ts
import { apiClient } from "@/lib/apiClient"
import type { Feature, FeatureFormData } from "./_types"

export const featureService = {
  async getAll(): Promise<Feature[]> {
    const response = await apiClient.get("/api/v1/features")
    return response.data
  },

  async create(data: FeatureFormData): Promise<Feature> {
    const response = await apiClient.post("/api/v1/features", data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/features/${id}`)
  },
}
```

**Rules:**
- ✅ Use `apiClient.get/post/put/delete`
- ❌ NEVER use `fetch()` directly

## 3. Server Component (page.tsx)

```typescript
// page.tsx - MUST be async
import { featureService } from "./service"
import FeatureClient from "./feature-client"

export default async function FeaturePage() {
  // ✅ Server-side data fetching
  const features = await featureService.getAll()

  // ✅ Pass data to client component
  return <FeatureClient features={features} />
}
```

**Rules:**
- ✅ MUST be `async`
- ✅ Data fetching on server
- ❌ NO `useState`, `useEffect`, `onClick`
- ❌ NO `"use client"`

## 4. Custom Hook (use-feature.ts)

```typescript
// use-feature.ts
"use client"

import { useState, useTransition } from "react"
import { useRouter } from "next/navigation"
import { featureService } from "./service"
import type { FeatureFormData } from "./_types"
import { ApiError } from "@/lib/apiError"

export function useFeature() {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | null>(null)

  const create = async (data: FeatureFormData) => {
    setError(null)

    // ✅ CRITICAL: async function inside startTransition
    startTransition(async () => {
      try {
        await featureService.create(data)

        // ✅ CRITICAL: router.refresh() to re-run page.tsx
        router.refresh()
      } catch (e) {
        const errorMessage =
          e instanceof ApiError
            ? `Error (${e.status}): ${e.message}`
            : "An unknown error occurred."
        setError(errorMessage)
      }
    })
  }

  const deleteFeature = async (id: number) => {
    setError(null)

    startTransition(async () => {
      try {
        await featureService.delete(id)
        router.refresh()
      } catch (e) {
        const errorMessage =
          e instanceof ApiError
            ? `Error (${e.status}): ${e.message}`
            : "An unknown error occurred."
        setError(errorMessage)
      }
    })
  }

  return { create, deleteFeature, isPending, error }
}
```

**Rules:**
- ✅ `"use client"` at top
- ✅ `async` function INSIDE `startTransition`
- ✅ Call `router.refresh()` after successful mutation
- ✅ Error handling with `ApiError`
- ✅ Return `error` state for UI display

## 5. Client Component (feature-client.tsx)

```typescript
// feature-client.tsx
"use client"

import { useState } from "react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import { useFeature } from "./use-feature"
import type { Feature } from "./_types"

interface Props {
  features: Feature[]
}

export default function FeatureClient({ features }: Props) {
  const { create, deleteFeature, isPending, error } = useFeature()
  const [showCreate, setShowCreate] = useState(false)

  return (
    <>
      {/* Header with action */}
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Features</h1>
        <Button
          onClick={() => setShowCreate(true)}
          disabled={isPending}
        >
          <Plus className="h-4 w-4" />
          Create
        </Button>
      </div>

      {/* Error display */}
      {error && (
        <p className="mb-4 rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </p>
      )}

      {/* Loading state */}
      {isPending && (
        <div className="text-center text-muted-foreground py-4">
          Processing...
        </div>
      )}

      {/* Empty state */}
      {features.length === 0 ? (
        <div className="text-center text-muted-foreground py-12">
          No features yet.
        </div>
      ) : (
        /* List rendering */
        <div className="space-y-6">
          {features.map((feature) => (
            <Card key={feature.id}>
              <CardHeader>
                <CardTitle>{feature.name}</CardTitle>
                <CardDescription>
                  Created {new Date(feature.created_at).toLocaleDateString()}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={() => deleteFeature(feature.id)}
                  disabled={isPending}
                  variant="destructive"
                >
                  Delete
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </>
  )
}
```

**Rules:**
- ✅ `"use client"` at top
- ✅ Receive data from page.tsx as props
- ✅ Use custom hook for mutations
- ✅ Use shadcn/ui components
- ✅ Display `error` from hook
- ✅ Show loading state with `isPending`
- ✅ Handle empty state

## Data Flow

### Read (Initial Load)

```
page.tsx (server) → service.ts → Backend API
    ↓
props → feature-client.tsx
```

### Write (Create/Update/Delete)

```
User clicks in feature-client.tsx
    ↓
use-feature.ts hook → service.ts → Backend API
    ↓
router.refresh()
    ↓
Re-run page.tsx on server (fresh data)
    ↓
New data flows to client
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `useState` in page.tsx | Move to `*-client.tsx` |
| Forgot `"use client"` | Add to client components |
| No `router.refresh()` | Add after mutations |
| Using `fetch()` | Use `apiClient` |
| Not async page.tsx | Add `async` |

## Quick Reference

```typescript
// page.tsx (Server)
export default async function Page() {
  const data = await service.getAll()
  return <Client data={data} />
}

// client.tsx (Client)
"use client"
export default function Client({ data }: Props) {
  const { mutate, isPending, error } = useFeature()

  return (
    <>
      {error && <p className="text-destructive">{error}</p>}
      {isPending && <p>Processing...</p>}
      {/* UI + interactions */}
    </>
  )
}

// use-feature.ts (Hook)
"use client"
export function useFeature() {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | null>(null)

  const mutate = async () => {
    setError(null)
    startTransition(async () => {
      try {
        await service.mutate()
        router.refresh()  // ← KEY!
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "Unknown error")
      }
    })
  }

  return { mutate, isPending, error }
}
```

## Advanced Patterns

### 1. Server Actions (Optional Alternative)

Instead of `service.ts` + `router.refresh()`, you can use Server Actions:

```typescript
// actions.ts
"use server"

import { revalidatePath } from "next/cache"
import { createFeature as _createFeature } from "./service"

export async function createFeatureAction(data: FeatureFormData) {
  const result = await _createFeature(data)
  revalidatePath("/features")  // Instead of router.refresh()
  return result
}
```

```typescript
// use-feature.ts
"use client"

import { createFeatureAction } from "./actions"

export function useFeature() {
  const [isPending, startTransition] = useTransition()

  const create = async (data: FeatureFormData) => {
    startTransition(async () => {
      await createFeatureAction(data)
      // NO router.refresh() needed!
    })
  }

  return { create, isPending }
}
```

**Trade-offs:**
- ✅ Simpler (no `router.refresh()`)
- ✅ Automatic revalidation
- ❌ Server Actions only (can't call from regular functions)

### 2. Component Splitting

Split large client components into smaller pieces:

```
feature/
├── feature-client.tsx       # State management + layout
├── feature-table.tsx        # Presentation only (no state)
└── feature-modal.tsx        # Modal component
```

```typescript
// feature-client.tsx
"use client"
export default function FeatureClient({ features }: Props) {
  const [filter, setFilter] = useState("")

  return (
    <>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      <FeatureTable features={features.filter(f => f.name.includes(filter))} />
    </>
  )
}

// feature-table.tsx - Pure presentation
"use client"
export default function FeatureTable({ features }: Props) {
  return (
    <Table>
      {features.map(f => <TableRow key={f.id}>{f.name}</TableRow>)}
    </Table>
  )
}
```

**Benefits:**
- Easier to test
- Better performance (smaller re-renders)
- Cleaner code organization

### 3. Tabs Pattern

```typescript
// feature-client.tsx
"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useMemo } from "react"

export default function FeatureClient({ features }: Props) {
  const [activeTab, setActiveTab] = useState("active")

  const filteredFeatures = useMemo(() => {
    return features.filter(f => f.status === activeTab)
  }, [features, activeTab])

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <TabsList>
        <TabsTrigger value="active">Active</TabsTrigger>
        <TabsTrigger value="archived">Archived</TabsTrigger>
      </TabsList>
      <TabsContent value={activeTab}>
        <FeatureTable features={filteredFeatures} />
      </TabsContent>
    </Tabs>
  )
}
```

### 4. Expose Refresh Function

```typescript
// use-feature.ts
export function useFeature() {
  const router = useRouter()

  const refresh = () => {
    router.refresh()  // Expose for external use
  }

  return { create, delete, refresh }
}

// feature-client.tsx
export default function FeatureClient() {
  const { refresh } = useFeature()

  return (
    <Modal onSuccess={refresh}>  {/* Pass to child */}
      {/* Modal calls refresh() on success */}
    </Modal>
  )
}
```

### 5. Empty State in Table

```typescript
<Table>
  <TableHeader>...</TableHeader>
  <TableBody>
    {features.length === 0 ? (
      <TableRow>
        <TableCell colSpan={5} className="text-center text-muted-foreground">
          No features yet.
        </TableCell>
      </TableRow>
    ) : (
      features.map(feature => <TableRow key={feature.id}>...</TableRow>)
    )}
  </TableBody>
</Table>
```

---

💬 **Questions about RSC patterns? Just ask!**
