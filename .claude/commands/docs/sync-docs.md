---
description: Check if WORKSPACE documentation is in sync with actual code
---

# Documentation-Code Sync Check

Check if WORKSPACE documents are synchronized with actual code.

## Steps

1. **Verify code patterns**

   a. **Frontend reference structure verification**
   - Use existing `announcements/` module as reference structure
   - Check actual `frontend/app/(dashboard)/announcements/` folder structure
   - Verify filename pattern matches (page.tsx, *-client.tsx, service.ts, use-*.ts)

   b. **Backend pattern verification**
   - Use existing module structure as reference pattern
   - Compare with actual backend folder structure (models.py, schemas.py, service.py, router.py)

2. **Verify FEATURES checklists**

   a. **Check checklist items**
   ```bash
   # Find checklists in all FEATURES .md files
   grep -r "- \[ \]" WORKSPACE/FEATURES/
   grep -r "- \[x\]" WORKSPACE/FEATURES/
   ```

   b. **Check implementation status**
   - Read each FEATURES document checklist
   - Check if actual code exists for the feature
     - Backend: `backend/app/<feature>/` folder
     - Frontend: `frontend/app/(dashboard)/<feature>/` folder
   - Check if test files exist

   c. **Report mismatches**
   - Items checked as ✅ but code doesn't exist
   - Code exists but checked as ❌

3. **Verify code examples**

   a. **Verify Skills pattern compliance**
   - DO/DON'T patterns defined in Skills
   - Search for patterns in actual codebase
   - Check if bad patterns are actually used (FK usage, raw HTML, etc.)

   b. **Verify referenced file paths**
   - File paths mentioned in docs (e.g., `backend/app/middo/models.py`)
   - Check if files actually exist

4. **Verify WORKSPACE folder structure**

   a. **Check 00_PROJECT.md structure**
   - Folder structure shown in `00_PROJECT.md`
   - Compare with actual WORKSPACE folder structure

   b. **Verify README index**
   - Sub-documents listed in each README.md
   - Check if files actually exist

5. **Report results**

   **Matching items:**
   - ✅ Frontend announcements/ structure matches
   - ✅ Backend module pattern matches
   - ✅ FEATURES checklist synchronized

   **Mismatches:**
   - ❌ `<file path>`: In docs but actual file missing
   - ❌ `<checklist item>`: Checked as complete but code not implemented
   - ⚠️ `<code pattern>`: Pattern forbidden in docs is used in actual code

6. **Suggest fixes**

   When mismatch found:
   - If doc update needed: Suggest which parts to update
   - If code fix needed: Suggest which code to update
   - Checklist update: Suggest complete/incomplete status change

## Verification Scope

### Required verification items

1. **Code pattern consistency**
   - Frontend: Check announcements/ module structure (page.tsx, *-client.tsx, service.ts, use-*.ts)
   - Backend: Check existing module structure (models.py, schemas.py, service.py, router.py)

2. **FEATURES checklists**
   - Checklists in all `FEATURES/*.md` files
   - Completion status by phase

3. **File path references**
   - All file paths directly referenced in docs
   - Example: `backend/app/middo/models.py:line_number`

### Optional verification items

1. **Skills rule compliance** (when time permits)
   - NO FK rule (sqlmodel-no-foreign-keys skill)
   - No raw HTML (using-shadcn-components skill)
   - Check if bad practice examples are actually used

2. **Comment language verification** (Backend)
   - Search for Korean comments (refer to committing-changes skill)

## Important

- **Don't auto-fix**: Only report when mismatch found, confirm with user
- **Consider false positives**: Some docs may be examples
- **Understand context**: Semantic validation, not just string matching

## Next Steps

After doc-code sync check:
- Fix mismatches
- Run `/verify-phase` for code quality check
- Run `/review-phase` to prepare MR
