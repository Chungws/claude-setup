---
name: git-branching
description: Git branching strategy (Git Flow) for software projects. Use when creating/managing branches. Critical rules - ALWAYS check branch before work, NEVER work on main branch directly, use feature branches, target main development branch for PRs. Framework and language agnostic.
---

# Git Branching Strategy (Git Flow)

## 🔴 CRITICAL RULES

1. **ALWAYS check branch before work** - `git branch --show-current`
2. **NEVER work on develop directly** - Create feature branch first
3. **Main branch is `develop`**
4. **All PRs target `develop`**

## Branch Verification (MANDATORY)

**Before ANY work:**

```bash
# ALWAYS run this first!
git branch --show-current

# If output is "develop":
# ❌ STOP! Create feature branch immediately!

# If output is "feature/something":
# ✅ OK to work
```

## Branch Types

| Branch | Purpose | Branch From | Merge To |
|--------|---------|-------------|----------|
| `develop` | Main development | - | - |
| `feature/*` | Feature development | `develop` | `develop` |
| `hotfix/*` | Emergency fixes | `develop` | `develop` |

**Project-specific:**
- Main branch: `develop`
- Feature branches: `feature/*`
- All PRs target: `develop`

## Feature Branch Workflow

### Step 1: Check Current Branch

```bash
# Always check first!
git branch --show-current

# Expected: feature/your-feature
# If develop → go to Step 2
```

### Step 2: Create Feature Branch

```bash
# Update develop first
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/translation-eval-phase-1

# Verify you're on new branch
git branch --show-current
# Output: feature/translation-eval-phase-1 ✅
```

### Step 3: Work on Feature

```bash
# Make changes
# ...

# Commit (see committing-changes skill)
git add .
git commit -m "feat: add translation evaluation"
```

### Step 4: Push to Remote

```bash
# First push (set upstream)
git push -u origin feature/translation-eval-phase-1

# Subsequent pushes
git push
```

### Step 5: Create PR

```bash
# Use /create-pr command or GitHub MCP
# Target branch: develop
```

See `creating-pull-requests` skill for PR creation.

### Step 6: After Merge - Cleanup

```bash
# Switch to develop
git checkout develop

# Pull merged changes
git pull origin develop

# Delete local feature branch
git branch -d feature/translation-eval-phase-1

# Verify clean state
git branch --show-current
# Output: develop
```

## Branch Naming

### ✅ CORRECT Naming

```bash
feature/translation-eval-phase-1
feature/fix-login-bug
feature/add-user-profile
feature/refactor-api-client
```

### ❌ WRONG Naming

```bash
bugfix/issue-123          # Use feature/ instead
refactor/cleanup          # Use feature/ instead
translation-eval          # Missing feature/ prefix
feature/TRANSLATION-EVAL  # Use lowercase
```

**Pattern:** `feature/<descriptive-name-with-hyphens>`

## Common Scenarios

### Scenario 1: Started Working on develop (Before Commit)

```bash
# Oh no! I'm on develop
git branch --show-current
# Output: develop

# Solution: Stash changes and create branch
git stash
git checkout -b feature/my-new-feature
git stash pop

# Verify
git branch --show-current
# Output: feature/my-new-feature ✅
```

### Scenario 2: Started Working on develop (After Commit)

```bash
# Oh no! I committed to develop
git branch --show-current
# Output: develop

# Solution: Create branch from current state
git checkout -b feature/my-new-feature
# This creates branch with your commits

# Reset develop to remote state
git checkout develop
git reset --hard origin/develop

# Continue work on feature branch
git checkout feature/my-new-feature
```

### Scenario 3: Need to Switch Branch Mid-Work

```bash
# Currently on feature/feature-a
# Need to work on feature-b

# Option 1: Commit current work
git add .
git commit -m "wip: partial implementation"
git checkout -b feature/feature-b

# Option 2: Stash current work
git stash
git checkout -b feature/feature-b
# Later: git stash pop
```

### Scenario 4: Update Feature Branch with Latest develop

```bash
# Your feature branch is behind develop
git checkout develop
git pull origin develop

git checkout feature/your-feature
git merge develop
# Or: git rebase develop (advanced)

# Resolve conflicts if any
git push
```

## Multiple Feature Branches

**Pattern:** One branch per Phase or logical unit

```bash
# Phase 1: Models and schemas
feature/translation-eval-phase-1

# Phase 2: Service layer
feature/translation-eval-phase-2

# Phase 3: API endpoints
feature/translation-eval-phase-3
```

**Workflow:**
1. Create `feature/feature-name-phase-1`
2. Complete Phase 1 → Create PR → Merge
3. Create `feature/feature-name-phase-2` from updated develop
4. Repeat

## Branch Protection

**develop branch is protected:**
- ❌ Cannot push directly
- ❌ Cannot force push
- ✅ Must create PR
- ✅ PR must be approved (if configured)

## Emergency Fixes (Hotfix)

**For critical bugs only:**

```bash
# Create hotfix from develop
git checkout develop
git pull origin develop
git checkout -b hotfix/critical-security-patch

# Fix and commit
git commit -m "fix: patch security vulnerability"

# Push and create PR to develop
git push -u origin hotfix/critical-security-patch
```

**Note:** Hotfixes are rare. Most fixes go through feature branches.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Working on develop directly | Create feature branch first |
| Forgot to check branch | Run `git branch --show-current` |
| Wrong branch name | Use `feature/*` pattern |
| PR targets wrong branch | Target `develop` instead |
| Not updating develop first | `git pull origin develop` |
| Force push to develop | Never force push protected branches |

## Quick Reference

```bash
# 1. ALWAYS check branch first
git branch --show-current

# 2. If on develop → create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 3. Work and commit
git add .
git commit -m "feat: add feature"

# 4. Push
git push -u origin feature/your-feature-name

# 5. Create PR (target: develop)
# Use /create-pr command

# 6. After merge → cleanup
git checkout develop
git pull origin develop
git branch -d feature/your-feature-name
```

## Integration with Other Skills

- **committing-changes**: Commit format and guidelines
- **creating-pull-requests**: PR creation after branch work
- **reviewing-code**: Pre-PR checklist

## Visual Flow

```
develop (main development branch)
  ↓
feature/your-feature (your work)
  ↓
PR to develop
  ↓
Merged → Back to develop
  ↓
New feature branch for next task
```

---

💬 **Questions about Git branching? Just ask!**
