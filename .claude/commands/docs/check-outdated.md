---
description: Check if WORKSPACE documentation is outdated
---

# Check Outdated Documentation

Check if WORKSPACE documents are up-to-date and find outdated information.

## Steps

### 1. Verify 00_ROADMAP.md

#### a. Verify "Current Focus"

**Items to check:**
```bash
# Check recent 10 commits
git log --oneline -10

# Check current active feature branches
git branch -a | grep feature

# Check recent PRs (GitHub MCP)
mcp__github__list_pull_requests({
  owner: "owner-name",
  repo: "repo-name",
  state: "closed",
  perPage: 5
})
```

**Verification logic:**
1. Read "Current Focus" in ROADMAP
2. Extract feature names from recent commits
3. Check titles of recently merged PRs
4. If mismatch found:
   - ❌ "ROADMAP: Phase 6 in progress vs Actual: Only doc cleanup work in progress"
   - 💡 "Need ROADMAP update: Change current focus to 'XXX'"

#### b. Verify Phase completion status

**Items to check:**
```bash
# Extract completed/in-progress Phases from ROADMAP
grep -E "(Phase [0-9]+|✅|In Progress|Complete)" WORKSPACE/00_ROADMAP.md

# Check checklist in corresponding FEATURES document
grep -E "\[x\]|\[ \]" WORKSPACE/FEATURES/*.md
```

**Verification logic:**
1. Parse "Phase X complete" or "Phase X in progress" from ROADMAP
2. Find corresponding Phase's FEATURES document
3. Check FEATURES checklist:
   - Phase marked complete but many `[ ]` in checklist → ❌ Mismatch
   - Phase in progress but all checklist `[x]` → ⚠️ Need ROADMAP update

#### c. "Next Development Features" vs actual priority

**Items to check:**
```bash
# Check all documents in FEATURES folder
ls -la WORKSPACE/FEATURES/*.md

# Guess next feature from git branches
git branch -a | grep feature | grep -v merged
```

**Verification logic:**
1. Read ROADMAP "Next Development Features"
2. Check if feature document exists in FEATURES folder
3. Check recently created feature branches
4. Mismatch:
   - ⚠️ "Not in ROADMAP but in FEATURES: API_VERSIONING.md"
   - 💡 "Recommend adding to ROADMAP"

---

### 2. Verify CLAUDE.md

#### a. Verify "Current Status"

**Items to check:**
```bash
# Read Current Status section in CLAUDE.md
grep -A 10 "Current Status" CLAUDE.md

# Read current focus in ROADMAP
grep -A 5 "현재 집중 기능" WORKSPACE/00_ROADMAP.md
```

**Verification logic:**
1. CLAUDE.md "Active Feature" vs ROADMAP "Current Focus"
2. If mismatch:
   - ❌ "CLAUDE.md: Translation Evaluation Phase 6 vs ROADMAP: (different content)"
   - 💡 "Need to update either CLAUDE.md or ROADMAP"

#### b. "Latest Branch" vs actual branch

**Items to check:**
```bash
# Current branch
git branch --show-current

# Recent active feature branches
git for-each-ref --sort=-committerdate refs/heads/feature --format='%(refname:short)' | head -5
```

**Verification logic:**
1. Read CLAUDE.md "Latest Branch"
2. Check actual recent branches
3. Mismatch:
   - ⚠️ "CLAUDE.md: feature/fix-suggested-translation-logic vs Actual: feature/reduce-md-cross-references"

#### c. Verify "Recent Achievements"

**Items to check:**
```bash
# Check recently merged PRs
git log --oneline --merges -10
```

**Verification logic:**
1. Read CLAUDE.md "Recent Achievements" checklist
2. Check recently merged commits
3. Missing completed items:
   - 💡 "Recommend adding: ✅ CONVENTIONS doc simplification complete"

---

### 3. Verify FEATURES documents

#### a. Bidirectional ROADMAP ↔ FEATURES verification

**Items to check:**
```bash
# All .md files in FEATURES folder
ls WORKSPACE/FEATURES/*.md

# Extract features mentioned in ROADMAP
grep -E "Phase|Feature" WORKSPACE/00_ROADMAP.md
```

**Verification logic:**

**Direction 1: ROADMAP → FEATURES**
1. Extract all features mentioned in ROADMAP
2. Check if FEATURES document exists for each feature
3. If missing:
   - ⚠️ "Mentioned in ROADMAP: 'Infra Dashboard' but no FEATURES doc"
   - 💡 "Recommend running /new-feature"

**Direction 2: FEATURES → ROADMAP**
1. List all documents in FEATURES folder
2. Check if each document is mentioned in ROADMAP
3. If missing:
   - ⚠️ "In FEATURES: API_VERSIONING.md but not mentioned in ROADMAP"
   - 💡 "Recommend updating ROADMAP: Add to 'Next Development Features' or 'Future Ideas'"

#### b. Verify Status vs checklist match

**Items to check:**
```bash
# Check Status header in each FEATURES document
grep -h "Status:" WORKSPACE/FEATURES/*.md
```

**Verification logic:**
1. Check FEATURES document "Status: Complete/In Progress/Planning"
2. Check checklist:
   - Status: Complete but has `[ ]` → ❌ Mismatch
   - Status: Planning but all `[x]` → ❌ Mismatch
3. Suggest correction

---

### 4. Verify date information

#### a. "Last Updated" vs actual modification date

**Items to check:**
```bash
# Parse "Last Updated" in documents
grep -h "Last Updated" *.md WORKSPACE/*.md

# Check actual file modification date (git log)
git log -1 --format="%ai" -- WORKSPACE/00_ROADMAP.md
git log -1 --format="%ai" -- CLAUDE.md
git log -1 --format="%ai" -- README.md
```

**Verification logic:**
1. Extract "Last Updated: YYYY-MM-DD" from document
2. Check actual last modification date with git log
3. If difference > 1 week:
   - ⚠️ "00_ROADMAP.md: Last Updated 2025-01-15 vs Actual modification 2025-01-10"
   - 💡 "Need date update"

#### b. Verify "Created" date

**Items to check:**
```bash
# Created date in FEATURES documents
grep -h "Created:" WORKSPACE/FEATURES/*.md

# Actual file creation date
git log --diff-filter=A --follow --format=%ai -- WORKSPACE/FEATURES/API_VERSIONING.md
```

**Verification logic:**
1. Extract "Created: YYYY-MM-DD" from document
2. Check actual file creation date with git log
3. Mismatch:
   - ⚠️ "Created date inaccurate"

---

### 5. Verify 00_PROJECT.md policy table

#### a. CLAUDE.md vs 00_PROJECT.md policy match

**Items to check:**
```bash
# Read policy table sections in both files
grep -A 20 "Project Policies|프로젝트 정책" CLAUDE.md WORKSPACE/00_PROJECT.md
```

**Verification logic:**
1. Parse policy table in CLAUDE.md
2. Parse policy table in 00_PROJECT.md
3. Compare each policy item:
   - Foreign Keys
   - Main Branch
   - MR Language
   - MR Assignee
   - MR Reviewer
4. Mismatch:
   - ❌ "CLAUDE.md: MR Assignee: dapi vs 00_PROJECT.md: (different value)"

---

## Report Format

### ✅ Up-to-date

```
- ✅ CLAUDE.md "Current Status" ↔ ROADMAP "Current Focus" match
- ✅ README.md Last Updated date accurate
- ✅ FEATURES/HUMAN_EVALUATION.md Status ↔ checklist match
```

### ❌ Outdated Documents Found (Critical)

```
- ❌ 00_ROADMAP.md: "Current Focus" outdated
  - Document: "Phase 6 LLM Judge in progress"
  - Actual: Phase 6 complete, recent work is doc cleanup (refactor/reduce-md-cross-references)
  - Recommend: Update ROADMAP "Current Focus" to "Documentation cleanup and maintenance"

- ❌ CLAUDE.md "Latest Branch" outdated
  - Document: "feature/fix-suggested-translation-logic"
  - Actual: "feature/reduce-md-cross-references"
  - Recommend: Update CLAUDE.md
```

### ⚠️ Needs Attention (Warning)

```
- ⚠️ Feature in FEATURES but not in ROADMAP:
  - API_VERSIONING.md (Status: Ready for Implementation)
  - Recommend: Add to ROADMAP "Next Development Features"

- ⚠️ 00_ROADMAP.md Last Updated date old
  - Document: 2025-01-10
  - Actual modification: 2025-01-05
  - Recommend: Update date after updating
```

### 💡 Improvement Suggestions

```
- 💡 Recommend adding to CLAUDE.md "Recent Achievements":
  - ✅ CONVENTIONS doc simplification complete (86% reduction)
  - ✅ Integrated SPECS folder into FEATURES

- 💡 Add Created date to new FEATURES documents:
  - HUMAN_EVALUATION.md (No Created date)
```

---

## Fix Priority

### 🔴 High Priority (Fix immediately)
1. Update ROADMAP "Current Focus"
2. Fix CLAUDE.md vs 00_PROJECT.md policy mismatch
3. Fix FEATURES Status vs checklist mismatch

### 🟡 Medium Priority (When time permits)
1. Add missing FEATURES to ROADMAP
2. Update Last Updated dates
3. Add CLAUDE.md "Recent Achievements"

### 🟢 Low Priority (Optional)
1. Fill missing Created dates
2. Suggest documentation structure improvements

---

## Usage Example

```bash
# Verify outdated documents
/check-outdated

# Example output:
#
# ❌ Outdated found (2 items)
# ⚠️ Needs attention (3 items)
# 💡 Improvements (2 items)
#
# Please run again after fixing.
```

---

## Important

- **Consider false positives**: Some "outdated" may be intentional (e.g., future plans)
- **Clear judgment criteria**: "outdated" criteria is difference from **actual implementation status**
- **No auto-fix**: Always only suggest fixes after user confirmation

## Next Steps

When outdated documents found:
1. Fix according to priority
2. Re-run `/check-outdated` after fixes
3. Run `/sync-docs` to verify code synchronization
4. Run `/verify-phase` to commit
