---
description: Check if WORKSPACE documentation is outdated
---

# Check Documentation-Code Sync

Check if documentation is synchronized with actual code implementation.

## Purpose

Verify that documentation accurately reflects the current state of the codebase:
- Feature checklists match actual implementation
- Referenced files exist in the codebase
- Documentation status aligns with code reality

## Steps

### 1. Verify Feature Documentation

**Check feature checklists:**
- Find all feature documents (e.g., WORKSPACE/FEATURES/)
- For each checklist item marked as complete:
  - Verify corresponding code exists
  - Check if implementation matches description
- Report mismatches:
  - ❌ Marked complete but code missing
  - ⚠️ Code exists but not marked complete

**Example checks:**
```bash
# Find feature documentation
find . -name "*.md" -path "*FEATURES*" -o -path "*features*"

# Check for checklist items
grep -r "\[x\]" <feature-docs-path>
grep -r "\[ \]" <feature-docs-path>
```

### 2. Verify File References

**Check referenced file paths:**
- Extract file paths mentioned in documentation
- Verify each file exists in the codebase
- Report missing files

**Example checks:**
```bash
# Common documentation locations
ls -la WORKSPACE/ docs/ README.md

# Verify specific paths mentioned in docs
# (Extract from documentation and check)
```

### 3. Verify Implementation Status

**Check documentation status fields:**
- Look for "Status:", "State:", or similar markers
- Compare status with actual implementation:
  - Status: "Complete" → All related code should exist
  - Status: "In Progress" → Partial implementation expected
  - Status: "Planning" → No implementation expected
- Report inconsistencies

### 4. Verify Code Examples

**If documentation contains code examples:**
- Check if examples follow current project conventions
- Verify example file paths exist
- Check if example patterns are used in actual code

## Report Format

### ✅ Synchronized
```
- ✅ Feature X checklist matches implementation
- ✅ All referenced files exist
- ✅ Status "Complete" matches code state
```

### ❌ Needs Update (Critical)
```
- ❌ Feature X marked complete but code missing
  - Missing: <file-path> or <implementation>
  - Action: Update checklist or implement feature

- ❌ File referenced in docs but not found
  - Referenced: <file-path>
  - Action: Update documentation or create file
```

### ⚠️ Inconsistencies (Warning)
```
- ⚠️ Feature Y implemented but not documented
  - Found: <implementation>
  - Action: Update documentation

- ⚠️ Status mismatch
  - Docs: "Planning"
  - Code: Fully implemented
  - Action: Update status field
```

### 💡 Suggestions
```
- 💡 Consider adding documentation for <feature>
- 💡 Update last modified date
- 💡 Add implementation notes
```

## Priority Levels

### 🔴 High Priority
- Documentation claims feature complete but code missing
- Referenced files don't exist
- Critical mismatches between docs and code

### 🟡 Medium Priority
- Status fields don't match implementation state
- Code exists but not documented
- Examples outdated

### 🟢 Low Priority
- Missing dates or metadata
- Documentation could be more detailed
- Style inconsistencies

## Important

- **No auto-fix**: Always confirm with user before making changes
- **Context matters**: Some mismatches may be intentional (future plans, etc.)
- **Verify carefully**: Check actual implementation, not just file existence

## Next Steps

```bash
# After finding issues:
# 1. Fix documentation → Update markdown files
# 2. Fix code → Implement missing features
# 3. Verify sync → Run this command again
```
