# Git

## Commits
- Format: `<type>: <subject>` (feat, fix, refactor, test, chore, perf, docs, style)
- Imperative mood, lowercase, no period, ≤50 chars.
- One logical change per commit. Keep 10-100 lines per commit.
- Never commit to main/develop directly — use feature branches.

## Branches
- Create from main/develop: `feature/`, `fix/`, `chore/` prefixes.
- Keep branches short-lived. Rebase before PR.

## Phase / PR Size
- One phase = max 3-4 commits, ~300 lines.
- If a phase looks larger during planning, split into sub-phases first.
- Estimate change volume in the plan step; propose a split before implementation starts.

For detailed patterns → see `git/git-committing`, `git/git-branching` skills.
