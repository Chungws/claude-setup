---
name: python-monorepo-with-uv
description: uv monorepo patterns for Python projects with dependency isolation. Use when managing multi-package Python projects with conflicting dependencies (different ML frameworks, Python versions) or when setting up workspace structure with uv.
---

# Python Monorepo with uv

## Overview

Manage Python monorepos using uv's workspace feature, with special focus on **dependency isolation** for services with conflicting requirements.

## When to Use This Skill

- Setting up uv workspace configuration
- Managing services with conflicting dependencies
- Microservice architecture with shared libraries
- Need to understand workspace vs path dependencies

## uv Workspace Patterns

### Pattern 1: Traditional Monorepo (Unified Dependencies)

**Configuration:**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib", "service-a", "service-b"]
```

**Characteristics:**
- ✅ Single lockfile, unified dependency resolution
- ✅ Faster installs, easier management
- ❌ ALL members must use same Python version
- ❌ ALL members must have compatible dependencies

**Use when:** Services have compatible dependencies and same Python version

### Pattern 2: Dependency Isolation (Independent Lockfiles)

**Configuration:**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib"]
exclude = ["services/*"]
```

**Characteristics:**
- ✅ Each service has independent lockfile
- ✅ Can use different Python versions
- ✅ Can have conflicting dependencies
- ❌ Separate lockfiles, independent sync per service

**Use when:** Services have conflicting dependencies or different Python versions

## Dependency Types

### Workspace Dependencies

**When to use:** Package is a workspace member

```toml
# service-a/pyproject.toml (service-a is in workspace.members)
[project]
dependencies = ["shared-lib"]

[tool.uv.sources]
shared-lib = { workspace = true }
```

- Requires shared-lib in `[tool.uv.workspace.members]`
- Single unified lockfile
- All packages must be compatible

### Path Dependencies

**When to use:** Package is excluded from workspace

```toml
# service-a/pyproject.toml (service-a is excluded)
[project]
dependencies = ["shared-lib"]

[tool.uv.sources]
shared-lib = { path = "../shared-lib", editable = true }
```

- Works even if shared-lib not in workspace members
- Independent lockfile per service
- Allows incompatible dependencies

**Always use `editable = true` for local development:**
- Changes immediately visible (no reinstall)
- Better IDE support

## Example: Dependency Isolation Setup

**Problem:** Service A needs TensorFlow (Python 3.11), Service B needs PyTorch (Python 3.12)

**Solution:**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib"]
exclude = ["services/*"]
```

```toml
# shared-lib/pyproject.toml - Framework-agnostic
[project]
name = "shared-lib"
requires-python = ">=3.11"
dependencies = ["numpy>=1.24.0", "pydantic>=2.0.0"]
```

```toml
# services/service-a/pyproject.toml
[project]
dependencies = ["shared-lib", "tensorflow==2.15.0"]

[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }
```

```toml
# services/service-b/pyproject.toml
[project]
dependencies = ["shared-lib", "torch>=2.9.0"]

[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }
```

**Directory:**
```
project-root/
├── pyproject.toml
├── uv.lock (shared-lib only)
├── shared-lib/
└── services/
    ├── service-a/uv.lock (TensorFlow)
    └── service-b/uv.lock (PyTorch)
```

**Commands:**
```bash
uv sync                      # Install shared-lib
cd services/service-a && uv sync  # Service A with TensorFlow
cd services/service-b && uv sync  # Service B with PyTorch
```

## Best Practices

**Shared Library:**
- Keep framework-agnostic (no TensorFlow, PyTorch, etc.)
- Support wide Python version range (`requires-python = ">=3.11"`)
- Only essential dependencies

**Workspace Members (include in `members`):**
- Shared libraries with compatible dependencies
- Utility packages used across services

**Excluded Services (add to `exclude`):**
- Services with conflicting dependencies (ML frameworks)
- Services needing different Python versions
- Services with version conflicts

**Python Versions:**
```toml
# Shared lib: wide range
requires-python = ">=3.11"

# Service: pin if needed
requires-python = ">=3.11,<3.12"
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Package not found in workspace` | Change `workspace = true` → `path = "../shared-lib", editable = true` |
| `Conflicting dependencies` | Move services to `exclude = ["services/*"]` |
| Changes not visible | Add `editable = true` to path dependency |
| Lockfiles out of sync | Run `uv sync` in each service after shared-lib changes |

## Pattern Comparison

| Pattern | Configuration | Dependency Type | Lockfiles | Use Case |
|---------|--------------|-----------------|-----------|----------|
| **Traditional Monorepo** | `members = ["pkg-a", "pkg-b"]` | `workspace = true` | Single | Compatible deps, same Python |
| **Dependency Isolation** | `members = ["shared"]`<br>`exclude = ["services/*"]` | `path = "..."` | Multiple | Conflicting deps, different Python |

## Key Principles

1. **Shared library as workspace member** - Framework-agnostic, wide Python support
2. **Services excluded** - Independent lockfiles for conflicting dependencies
3. **Path dependencies** - Always use `editable = true` for development
4. **Minimal shared library** - Only framework-agnostic dependencies

**When dependency conflicts arise, exclude services and use path dependencies.**

---

💬 **Questions about uv monorepo patterns? Just ask!**
