# Next.js RSC Patterns Skill

## 개요

this project의 Next.js React Server Components(RSC) 패턴을 정의한 스킬입니다. Server Component와 Client Component를 명확히 분리합니다.

## 언제 사용하나요?

- Frontend 페이지를 새로 만들 때
- Server Component와 Client Component를 구분해야 할 때
- 데이터 페칭 및 상태 관리를 설계할 때
- API 호출 후 UI를 자동으로 업데이트해야 할 때

## 핵심 규칙

1. **page.tsx = async Server Component** - 데이터 페칭
2. **\*-client.tsx = Client Component** - 인터랙션 ("use client")
3. **NO useState/onClick in page.tsx** - Server Component에서 금지
4. **router.refresh() after mutations** - 데이터 변경 후 서버 재실행

## 파일 구조

```
feature/
├── _types.ts              # TypeScript 타입
├── service.ts             # API 호출 (apiClient)
├── use-feature.ts         # 커스텀 훅 (mutations)
├── feature-client.tsx     # Client Component
└── page.tsx               # Server Component (async)
```

## 데이터 흐름

### Read (초기 로드)
```
page.tsx (server) → service.ts → Backend API
    ↓
props → feature-client.tsx (렌더링)
```

### Write (생성/수정/삭제)
```
User clicks → use-feature.ts → service.ts → Backend API
    ↓
router.refresh()  ← 핵심!
    ↓
page.tsx 서버에서 재실행 → 새 데이터 받아옴
```

## 예시

```typescript
// ✅ CORRECT
// page.tsx - Server Component
export default async function FeaturePage() {
  const data = await featureService.getAll()
  return <FeatureClient data={data} />
}

// feature-client.tsx - Client Component
"use client"
export default function FeatureClient({ data }: Props) {
  const { create } = useFeature()
  return <Button onClick={() => create()}>Add</Button>
}

// use-feature.ts - Hook with error handling
"use client"
export function useFeature() {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | null>(null)

  const create = async () => {
    setError(null)
    startTransition(async () => {
      try {
        await service.create()
        router.refresh()  // ← 필수!
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "Error")
      }
    })
  }

  return { create, isPending, error }
}

// ❌ WRONG
// page.tsx
export default function Page() {  // async 없음!
  const [data, setData] = useState([])  // useState 금지!
  return <button onClick={...}>  // onClick 금지!
}
```

## 팁

- **Error handling**: `ApiError` 사용하여 에러 타입 구분
- **Loading state**: `useTransition`의 `isPending` 활용
- **Empty state**: 데이터 없을 때 UI 처리
- **startTransition**: `async` 함수를 내부에서 실행 (외부 X)

자세한 예시는 `SKILL.md`를 참고하세요.
