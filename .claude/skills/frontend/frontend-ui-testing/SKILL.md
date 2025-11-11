---
name: frontend-ui-testing
description: Frontend UI testing workflow. Use when verifying UI changes. Critical rule - MANDATORY visual verification for all UI changes before committing.
---

# Frontend UI Testing Workflow

## 🔴 CRITICAL RULE

**Visual verification is MANDATORY for all UI changes.**

Never commit UI changes without verifying they work correctly.

## When to Use This Skill

- After creating/modifying any UI component
- After changing layout or styles
- Before creating MR/PR with frontend changes
- When adding new pages or routes

## UI Verification Workflow

### Step 1: Start Dev Server

```bash
cd frontend
npm run dev  # http://localhost:3000
```

### Step 2: Navigate and Verify

Use browser or Chrome DevTools MCP to:
1. Navigate to the changed page
2. Check visual appearance
3. Test interactive elements
4. Check browser console for errors

### Step 3: Run Through Checklist

Complete the verification checklist below before committing.

## Verification Checklist

When verifying UI changes:

### Visual Checks
- [ ] Dev server running (npm run dev)
- [ ] Page loads without errors
- [ ] New components render correctly
- [ ] Layout not broken
- [ ] Text/content displays properly
- [ ] Images/icons load correctly
- [ ] Spacing and alignment correct

### Interaction Checks
- [ ] Buttons clickable and respond
- [ ] Forms submit correctly
- [ ] Links navigate properly
- [ ] Input fields work
- [ ] Dropdowns/selects functional
- [ ] Modals/dialogs open/close

### Responsive Checks
- [ ] Desktop layout works
- [ ] Mobile layout works (resize browser)
- [ ] Tablet layout works (if applicable)
- [ ] No horizontal scrolling

### Technical Checks
- [ ] No console errors (F12 → Console)
- [ ] No console warnings (check)
- [ ] No network errors (F12 → Network)
- [ ] Loading states work correctly

## Common UI Issues to Check

### 1. Layout Broken
**Symptoms:**
- Elements overlapping
- Misaligned components
- Unexpected scrollbars

**How to check:**
- Visual inspection
- Resize browser window
- Check on different screen sizes

### 2. Components Not Rendering
**Symptoms:**
- Blank page or sections
- Missing elements
- Loading forever

**How to check:**
- Check browser console for errors
- Look for React/component errors
- Check network tab for failed requests

### 3. Interactive Elements Broken
**Symptoms:**
- Buttons don't respond
- Forms don't submit
- Links don't navigate

**How to check:**
- Click all interactive elements
- Fill and submit forms
- Test keyboard navigation (Tab key)

### 4. Console Errors
**Common errors:**
- "Cannot read property of undefined"
- "Module not found"
- "Failed to fetch"
- "Hydration mismatch" (Next.js)

**How to check:**
- Open browser DevTools (F12)
- Check Console tab
- Fix all errors before committing

## Quick Workflow

```bash
# 1. Make UI changes
# Edit components, pages, styles

# 2. Start dev server
cd frontend
npm run dev

# 3. Open in browser
# http://localhost:3000/your-page

# 4. Verify
# - Check visual appearance
# - Test interactions
# - Check console (F12)
# - Test responsive (resize)

# 5. Run through checklist
# Complete all items above

# 6. Pass? → Commit
git add .
git commit -m "feat: add feature UI"

# 7. Fail? → Fix and repeat
```

## Testing Tools

### Browser DevTools (F12)
- **Console**: Check for errors/warnings
- **Network**: Check API calls
- **Elements**: Inspect DOM/styles
- **Application**: Check localStorage/cookies

### Chrome DevTools MCP (Optional)
If available, use MCP tools for automated testing:
- `mcp__chrome-devtools__navigate_page` - Open page
- `mcp__chrome-devtools__take_snapshot` - Get page structure
- `mcp__chrome-devtools__list_console_messages` - Check errors
- `mcp__chrome-devtools__take_screenshot` - Capture visuals

See MCP tool descriptions for detailed usage.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping UI verification | ALWAYS verify visually |
| Not checking console | Check for errors (F12) |
| Not testing interactions | Click buttons, test forms |
| Not checking mobile | Resize browser window |
| Committing broken UI | Complete checklist first |
| Not testing edge cases | Test empty states, errors |

## Quick Reference

```bash
# Verification steps
1. Start: npm run dev
2. Open: http://localhost:3000/your-page
3. Check: Visual, interactions, console, responsive
4. Verify: Complete checklist above
5. Commit: Only if all checks pass

# Essential checks
[ ] Visual appearance ✅
[ ] Interactive elements ✅
[ ] No console errors ✅
[ ] Responsive layout ✅
```

---

💬 **Questions about UI testing? Just ask!**
