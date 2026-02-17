# claude-setup

Personal Claude Code configuration — skills, CLAUDE.md, and MCP servers.

## Structure

```
CLAUDE.md                    # Global coding principles
.mcp.json.example            # MCP server config template
.claude/
  rules/                     # Always-on rules (loaded every session)
    testing.md               # TDD, test quality
    git.md                   # Commit format, branch strategy
    quality.md               # Pre-commit lint/format/test checks
  skills/
    backend/                 # FastAPI, SQLModel, Alembic
    frontend/                # UI testing
    git/                     # Detailed commit, branching, PR patterns
    python/                  # Linting, deps, review
    testing/                 # TDD detailed patterns
    typescript/              # Code review
```

## Setup

```bash
# Clone
git clone https://github.com/Chungws/claude-setup.git ~/claude-setup

# Copy global config
cp ~/claude-setup/CLAUDE.md ~/.claude/CLAUDE.md

# Copy MCP config
cp ~/claude-setup/.mcp.json.example ~/.claude/.mcp.json

# Symlink skills into projects as needed
```

## Skills

| Skill | Description |
|-------|-------------|
| `backend/fastapi-patterns` | 4-layer FastAPI architecture |
| `backend/sqlmodel-patterns` | SQLModel database patterns |
| `backend/alembic-migrations` | Database migration workflow |
| `frontend/frontend-ui-testing` | UI testing patterns |
| `git/git-committing` | Conventional commits guide |
| `git/git-branching` | Branch strategy |
| `git/creating-pull-requests` | PR creation workflow |
| `git/pr-splitting-strategy` | Splitting large PRs |
| `python/quality-check-python` | Ruff + pytest checks |
| `python/fixing-linting-errors` | Lint error fixes |
| `python/managing-python-deps` | Dependency management |
| `python/python-monorepo-with-uv` | uv monorepo patterns |
| `python/reviewing-python` | Python code review |
| `testing/tdd-principles` | TDD Red-Green-Refactor |
| `typescript/reviewing-typescript` | TypeScript code review |

## Recommended Plugins

Install via Claude Code plugin marketplace:

```
/plugin marketplace add anthropics/claude-code
/plugin install feature-dev@anthropics-claude-code
/plugin install commit-commands@anthropics-claude-code
/plugin install code-review@anthropics-claude-code
/plugin install pr-review-toolkit@anthropics-claude-code
/plugin install hookify@anthropics-claude-code
```

| Plugin | Description |
|--------|-------------|
| `feature-dev` | Guided feature development (discovery → codebase exploration → clarifying questions → architecture → implementation) |
| `commit-commands` | `/commit` and `/commit-push-pr` for git workflow |
| `code-review` | Multi-agent PR review (CLAUDE.md compliance + bug detection) |
| `pr-review-toolkit` | 6 specialized review agents (silent-failure-hunter, type-design-analyzer, etc.) |
| `hookify` | Create hooks conversationally (`/hookify` → describe what you want) |

### LSP Plugins (for terminal Claude Code users)

```
/plugin install pyright-lsp@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official
```

### Optional Plugins

```
/plugin marketplace add mixedbread-ai/mgrep
/plugin install mgrep@Mixedbread-Grep
```

- **mgrep** — Better search than ripgrep, supports local + web search

## Recommended External Skills

```bash
# Vercel — React/Next.js best practices
npx skills add vercel-labs/agent-skills

# Skill finder — search and install skills interactively
npx skills add vercel-labs/skills@find-skills
```

- **react-best-practices** — 40+ React/Next.js performance rules
- **web-design-guidelines** — 100+ UI/UX audit rules
- **composition-patterns** — React composition patterns
- **find-skills** — Search and discover skills (`npx skills find [query]`)

## MCP Servers

See `.mcp.json.example`:
- **context7** — Auto-fetches up-to-date library documentation
- **sequential-thinking** — Step-by-step reasoning for complex problems

## ⚠️ Context Window Warning

MCP servers and plugins consume context. Too many enabled tools can shrink your
effective 200k context to ~70k before compaction kicks in.

**Rule of thumb:** Keep under 10 MCPs enabled / under 80 tools active.
Disable unused MCPs via `/mcp` or `/plugins`.
