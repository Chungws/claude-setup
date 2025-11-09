---
name: frontend-ui-testing
description: Frontend UI testing with Chrome DevTools MCP for VLA Arena. Use when verifying UI changes. Critical rule - MANDATORY Chrome DevTools MCP verification for all UI changes before committing.
---

# Frontend UI Testing with Chrome DevTools MCP

## 🔴 CRITICAL RULE

**UI verification with Chrome DevTools MCP is MANDATORY for all UI changes.**

Never commit UI changes without visual verification.

## When to Use This Skill

- After creating/modifying any UI component
- After changing layout or styles
- Before creating MR with frontend changes
- When adding new pages or routes

## Chrome DevTools MCP Verification (REQUIRED)

### Step 1: Start Dev Server

```bash
cd frontend
npm run dev  # http://localhost:3000
```

### Step 2: Navigate to Page

Use Chrome DevTools MCP to open the page:

```typescript
// Example: Open battle page
mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/battle"
})
```

### Step 3: Take Snapshot

Capture current UI state:

```typescript
mcp__chrome-devtools__take_snapshot()
```

This returns:
- Current page structure (accessibility tree)
- Visible elements with unique IDs (uid)
- Text content
- Interactive elements (buttons, inputs, etc.)

### Step 4: Take Screenshot (Optional)

Save visual evidence:

```typescript
mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/battle-page.png"
})
```

### Step 5: Check Console Errors

Verify no JavaScript errors:

```typescript
mcp__chrome-devtools__list_console_messages()
```

Look for:
- ❌ Errors (error type)
- ⚠️ Warnings (warn type)
- ✅ Clean console (no errors)

## Verification Checklist

When verifying UI changes:

```
[ ] Dev server running (npm run dev)
[ ] Page loads without errors
[ ] New components render correctly
[ ] Layout not broken
[ ] Responsive design works (resize browser if needed)
[ ] Interactive elements clickable
[ ] No console errors
[ ] Text/content displays properly
[ ] Images/icons load correctly
```

## Chrome DevTools MCP Tools

### Available Tools

```typescript
// Navigate to page
mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/path"
})

// Get page structure (accessibility tree with uids)
mcp__chrome-devtools__take_snapshot()

// Take screenshot
mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/feature.png",
  fullPage: false  // true for full page screenshot
})

// Check console messages
mcp__chrome-devtools__list_console_messages()

// Click element by uid (from snapshot)
mcp__chrome-devtools__click({
  uid: "12"  // uid from snapshot
})

// Fill input/select by uid
mcp__chrome-devtools__fill({
  uid: "15",  // uid from snapshot
  value: "Test input"
})

// Wait for text to appear
mcp__chrome-devtools__wait_for({
  text: "Success message",
  timeout: 5000
})

// Resize viewport
mcp__chrome-devtools__resize_page({
  width: 375,   // Mobile width
  height: 812
})

// Execute JavaScript
mcp__chrome-devtools__evaluate_script({
  function: "() => { return document.title; }"
})

// Close page
mcp__chrome-devtools__close_page({
  pageIdx: 0
})
```

## Example Verification Session

### Scenario: Created new Battle page

```typescript
// 1. Start dev server first
// cd frontend && npm run dev

// 2. Navigate to new page
mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/battle"
})

// 3. Check page structure
mcp__chrome-devtools__take_snapshot()

// Expected output:
// - Instruction input field visible
// - Submit button visible
// - Side-by-side viewer containers
// - Navigation working

// 4. Check console (no errors)
mcp__chrome-devtools__list_console_messages()

// 5. Test interaction: Fill instruction
// First take snapshot to get uid
mcp__chrome-devtools__take_snapshot()
// Look for input uid in output

mcp__chrome-devtools__fill({
  uid: "5",  // Example uid from snapshot
  value: "Pick up the red cube"
})

// 6. Click submit button
mcp__chrome-devtools__click({
  uid: "7"  // Submit button uid
})

// 7. Verify loading state appears
mcp__chrome-devtools__wait_for({
  text: "Executing",
  timeout: 5000
})

// 8. Take screenshot for reference
mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/battle-executing.png"
})

// 9. Test responsive (optional)
mcp__chrome-devtools__resize_page({
  width: 375,
  height: 812
})

mcp__chrome-devtools__take_snapshot()
// Verify mobile layout works

// 10. Close
mcp__chrome-devtools__close_page({
  pageIdx: 0
})
```

## Common UI Issues to Check

### 1. Layout Broken

**Symptoms:**
- Elements overlapping
- Misaligned components
- Overflow scrollbars

**How to detect:**
```typescript
mcp__chrome-devtools__take_snapshot()
// Look for missing elements or incorrect structure

mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/layout-check.png"
})
// Visual inspection
```

### 2. Components Not Rendering

**Symptoms:**
- Blank page
- Missing elements
- Loading forever

**How to detect:**
```typescript
mcp__chrome-devtools__list_console_messages()
// Look for:
// - React errors
// - Failed fetch requests
// - Missing component imports
```

### 3. Interactive Elements Broken

**Symptoms:**
- Buttons don't respond
- Forms don't submit
- Links don't navigate

**How to detect:**
```typescript
// Take snapshot to get element uid
mcp__chrome-devtools__take_snapshot()

// Try clicking
mcp__chrome-devtools__click({
  uid: "10"  // Button uid
})

// Check if action happened
mcp__chrome-devtools__take_snapshot()
```

### 4. Console Errors

**Common errors:**
- "Cannot read property of undefined"
- "Module not found"
- "Failed to fetch"
- "Hydration mismatch"

**How to detect:**
```typescript
mcp__chrome-devtools__list_console_messages()
```

## Quick Workflow

```bash
# 1. Make UI changes
# Edit components, pages, styles

# 2. Start dev server
cd frontend
npm run dev

# 3. Use Chrome DevTools MCP to verify
# - Navigate to page
# - Take snapshot
# - Check console
# - Test interactions

# 4. Pass? → Commit
git add .
git commit -m "feat: add battle page UI"

# 5. Fail? → Fix and repeat
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping UI verification | ALWAYS use Chrome DevTools MCP |
| Not checking console | Check for errors |
| Not testing interactions | Click buttons, test forms |
| Not checking mobile | Resize viewport |
| Committing broken UI | Verify before commit |

## Quick Reference

```typescript
// Essential verification flow
1. mcp__chrome-devtools__navigate_page({ url: "..." })
2. mcp__chrome-devtools__take_snapshot()
3. mcp__chrome-devtools__list_console_messages()
4. mcp__chrome-devtools__take_screenshot({ filePath: "..." })

// Checklist
[ ] Page loads ✅
[ ] Components render ✅
[ ] No console errors ✅
[ ] Interactions work ✅
```

---

💬 **Questions about UI testing? Just ask!**
