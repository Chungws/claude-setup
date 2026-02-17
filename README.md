# claude-setup

Personal Claude Code configuration — skills, commands, and MCP servers.

## Structure

```
CLAUDE.md                    # Global coding principles
.mcp.json.example            # MCP server config template
.claude/
  commands/
    docs/                    # Documentation management
    workflow/                # Feature development workflow
  skills/
    backend/                 # FastAPI, SQLModel, Alembic
    frontend/                # UI testing
    git/                     # Commits, branching, PRs
    python/                  # Linting, deps, review
    testing/                 # TDD principles
    typescript/              # Code review
```

## Setup

```bash
# Clone to home
git clone https://github.com/Chungws/claude-setup.git ~/claude-setup

# Copy CLAUDE.md to global config
cp ~/claude-setup/CLAUDE.md ~/.claude/CLAUDE.md

# Copy MCP config
cp ~/claude-setup/.mcp.json.example ~/.claude/.mcp.json

# Symlink skills and commands into projects as needed
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

## Recommended External Skills

Install via Claude Code plugin marketplace:
- `vercel-labs/agent-skills` — React/Next.js best practices, web design guidelines
- `anthropics/skills` — Document processing (PDF, PPTX, DOCX)
