---
name: project-init
description: Scaffolds project-specific .claude/rules/ and CLAUDE.md for new projects. Reads architecture references, proposes rules, generates on approval.
---

# Project Init

Scaffolds project-specific rules and CLAUDE.md for a new project.

## Step 1: Gather Project Info

Ask the user (skip what's already provided):
1. Project directory path
2. What the project does (one-line description)
3. Language and framework (e.g., Python/FastAPI, TypeScript/Next.js)

## Step 2: Read References

Read BOTH reference documents in this skill's directory:
- `~/.claude/skills/project-init/software-architecture.md` — layered architecture, dependency rules, project templates
- `~/.claude/skills/project-init/agent-development.md` — agent loop, tools, guardrails, benchmarking, prompt management

These contain the full knowledge base. Extract what's relevant for this project.

## Step 3: Propose Rules (Briefing)

Based on the project description, propose which rules to generate. Present to the user:

```
이 프로젝트에 대한 규칙 제안입니다:

✅ 적용:
1. {rule name} — {one-line description}
2. ...

⏭️ 미적용:
3. {rule name} — {why it's excluded}
4. ...

조정하고 싶으면 말씀해주세요.
```

Requirements for the briefing:
- **Applied rules**: explain what each rule enforces in one line
- **Excluded rules**: explain WHY each is excluded — the user may disagree and add it back
- Cover all major topics from both reference documents (architecture layers, dependency direction, naming, agent loop, prompt management, benchmarking, guardrails, CI/CD, observability)
- The user does NOT need to know the reference documents exist

Wait for user approval before proceeding.

## Step 4: Generate

After approval, generate into `<project-dir>`:

### Rules (`<project-dir>/.claude/rules/`)
- Create only the approved rules
- Each file: **50 lines max** — these are always-loaded per conversation
- Content must be **enforceable constraints**, not educational material
- File names: descriptive, kebab-case (e.g., `dependency-rules.md`, `prompt-management.md`)

### CLAUDE.md (`<project-dir>/CLAUDE.md`)
- Project name and description
- Architecture overview (based on generated rules)
- Dependency rules summary
- Lint & test commands (language-appropriate)

## Step 5: Summary

Show the user:
- List of created files
- Brief purpose of each
- Reminder: global rules (testing.md, git.md, quality.md, etc.md) are already applied — not duplicated

## Important

- Do NOT duplicate global rules from `~/.claude/rules/`
- Do NOT hardcode project types (web/agent) — judge from the project description
- If `.claude/rules/` or `CLAUDE.md` already exists, ask before overwriting
- If the project directory doesn't exist, ask whether to create it
- Match the user's language in the briefing and generated files
