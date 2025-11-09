# Using shadcn/ui Components Skill

## 개요

this project의 shadcn/ui 컴포넌트 사용 규칙을 정의한 스킬입니다. **Raw HTML 대신 shadcn/ui 컴포넌트를 필수로 사용**합니다.

## 언제 사용하나요?

- Frontend UI를 개발할 때
- 버튼, 카드, 모달 등 UI 요소가 필요할 때
- 새 shadcn/ui 컴포넌트를 설치해야 할 때
- Form이나 Table을 만들어야 할 때

## 핵심 규칙

1. **Raw HTML 금지** - `<button>`, `<div className="border">` 사용 금지
2. **shadcn/ui 우선** - Button, Card, Dialog 등 사용
3. **CLI로 설치** - `npx shadcn@latest add <component>`
4. **직접 편집 금지** - `components/ui/` 폴더 수정 금지

## 자주 사용하는 컴포넌트

```bash
# 기본 UI
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog

# Form
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add select

# 데이터 표시
npx shadcn@latest add table
npx shadcn@latest add toast
```

## 예시

```tsx
// ❌ WRONG: Raw HTML
<button className="bg-blue-500 px-4 py-2">Click</button>
<div className="border p-4">Content</div>

// ✅ CORRECT: shadcn/ui
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

<Button variant="default">Click</Button>
<Card>
  <CardContent>Content</CardContent>
</Card>
```

## Button 사용법

```tsx
import { Button } from "@/components/ui/button"

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
```

## Card 사용법

```tsx
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

## Dialog (Modal) 사용법

```tsx
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Modal</Button>
  </DialogTrigger>
  <DialogContent>
    Modal content here
  </DialogContent>
</Dialog>
```

## 팁

이 스킬은 Claude가 Frontend UI를 개발할 때 자동으로 로드됩니다. 필요한 컴포넌트는 https://ui.shadcn.com/docs/components 에서 찾을 수 있습니다.
