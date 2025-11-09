---
name: using-shadcn-components
description: shadcn/ui component usage. Use when building UI. Critical rules - ALWAYS use shadcn/ui components (NOT raw HTML), npx shadcn@latest add to install components, NEVER edit components/ui/ directly.
---

# shadcn/ui Component Usage

## 🔴 CRITICAL RULES

1. **ALWAYS use shadcn/ui components**
2. **NEVER use raw HTML** (`<button>`, `<div className="border">`, etc.)
3. **Install components via CLI** (`npx shadcn@latest add`)
4. **NEVER manually edit** `components/ui/` folder

## Installation

### Adding New Components

```bash
# ✅ CORRECT: Use CLI
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog

# ❌ WRONG: Manual creation
touch components/ui/button.tsx  # DON'T DO THIS
```

### Common Components

```bash
# UI Elements
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add badge
npx shadcn@latest add avatar

# Layout
npx shadcn@latest add separator
npx shadcn@latest add tabs
npx shadcn@latest add sheet

# Forms
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add select
npx shadcn@latest add checkbox
npx shadcn@latest add radio-group
npx shadcn@latest add switch
npx shadcn@latest add textarea

# Data Display
npx shadcn@latest add table
npx shadcn@latest add dialog
npx shadcn@latest add alert
npx shadcn@latest add toast

# Navigation
npx shadcn@latest add dropdown-menu
npx shadcn@latest add navigation-menu
```

## Usage Patterns

### Button Component

```tsx
// ❌ WRONG: Raw HTML
<button className="bg-blue-500 px-4 py-2 rounded">
  Click me
</button>

// ✅ CORRECT: shadcn Button
import { Button } from "@/components/ui/button"

<Button variant="default" size="default">
  Click me
</Button>

// ✅ Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// ✅ Sizes
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">🔍</Button>
```

### Card Component

```tsx
// ❌ WRONG: Raw HTML
<div className="border rounded-lg p-4">
  <h2 className="text-xl font-bold">Title</h2>
  <p>Content</p>
</div>

// ✅ CORRECT: shadcn Card
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Content</p>
  </CardContent>
</Card>

// ✅ Full structure
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>
    Main content here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Dialog Component

```tsx
// ❌ WRONG: Custom modal
<div className="fixed inset-0 bg-black/50">
  <div className="bg-white p-4 rounded">
    Modal content
  </div>
</div>

// ✅ CORRECT: shadcn Dialog
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    {/* Dialog content */}
  </DialogContent>
</Dialog>
```

### Table Component

```tsx
// ❌ WRONG: Raw HTML table
<table className="w-full">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John</td>
      <td>john@example.com</td>
    </tr>
  </tbody>
</table>

// ✅ CORRECT: shadcn Table
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Email</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>John</TableCell>
      <TableCell>john@example.com</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Form Component

```tsx
// ❌ WRONG: Raw form
<form>
  <label htmlFor="email">Email</label>
  <input id="email" type="email" className="border p-2" />
  <button type="submit">Submit</button>
</form>

// ✅ CORRECT: shadcn Form + react-hook-form
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  email: z.string().email(),
})

function MyForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

## Common Patterns

### Input Fields

```tsx
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

// ✅ Basic input
<div>
  <Label htmlFor="name">Name</Label>
  <Input id="name" placeholder="Enter name" />
</div>

// ✅ With error state
<Input
  type="email"
  placeholder="Email"
  className={errors.email ? "border-red-500" : ""}
/>
```

### Select Dropdown

```tsx
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select an option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

### Toast Notifications

```tsx
import { useToast } from "@/hooks/use-toast"
import { Button } from "@/components/ui/button"

function MyComponent() {
  const { toast } = useToast()

  return (
    <Button
      onClick={() => {
        toast({
          title: "Success",
          description: "Your changes have been saved.",
        })
      }}
    >
      Save
    </Button>
  )
}
```

## Component Discovery

**When you need a UI element:**

1. Check if shadcn/ui has it: https://ui.shadcn.com/docs/components
2. Install via CLI: `npx shadcn@latest add <component>`
3. Import and use

**Common component mapping:**

| Need | shadcn Component | Command |
|------|------------------|---------|
| Button | Button | `npx shadcn@latest add button` |
| Container | Card | `npx shadcn@latest add card` |
| Modal | Dialog | `npx shadcn@latest add dialog` |
| Dropdown | DropdownMenu | `npx shadcn@latest add dropdown-menu` |
| Data table | Table | `npx shadcn@latest add table` |
| Form input | Input, Form | `npx shadcn@latest add input form` |
| Notification | Toast | `npx shadcn@latest add toast` |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `<button>` | Use `<Button>` from shadcn |
| Using `<div className="border">` | Use `<Card>` |
| Manually creating modal | Use `<Dialog>` |
| Raw `<table>` | Use `<Table>` components |
| Editing `components/ui/*.tsx` | Don't edit, reinstall if needed |
| Custom form styling | Use `<Form>` + react-hook-form |

## Quick Reference

```tsx
// Button
import { Button } from "@/components/ui/button"
<Button variant="default" size="default">Click</Button>

// Card
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
<Card><CardHeader><CardTitle>Title</CardTitle></CardHeader></Card>

// Dialog
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"
<Dialog><DialogTrigger><Button>Open</Button></DialogTrigger></Dialog>

// Table
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table"
<Table><TableBody><TableRow><TableCell>Data</TableCell></TableRow></TableBody></Table>

// Form
import { Form, FormField, FormItem, FormLabel } from "@/components/ui/form"
<Form {...form}><form>...</form></Form>
```

---

💬 **Questions about shadcn/ui components? Just ask!**
