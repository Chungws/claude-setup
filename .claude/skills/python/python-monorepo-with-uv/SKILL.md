---
name: python-monorepo-with-uv
description: uv monorepo patterns for Python projects with dependency isolation. Use when managing multi-package Python projects with conflicting dependencies (different ML frameworks, Python versions) or when setting up workspace structure with uv. Covers workspace members vs excluded packages, dependency types, and real-world microservice patterns.
---

# Python Monorepo with uv

## Overview

Manage Python monorepos using uv's workspace feature, with special focus on **dependency isolation** for services with conflicting requirements (e.g., different ML frameworks, Python versions).

## When to Use This Skill

Use this skill when:
1. **Setting up uv workspace**: Need to configure `[tool.uv.workspace]` correctly
2. **Dependency conflicts**: Services require incompatible packages (TensorFlow vs PyTorch, Python 3.11 vs 3.12)
3. **Microservice architecture**: Independent services sharing common library
4. **Path dependencies**: Need to understand `workspace` vs `path` dependencies in uv

## uv Workspace Fundamentals

### Workspace Members vs Excluded Packages

uv supports two workspace patterns:

**Pattern 1: All packages as workspace members (traditional monorepo)**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib", "service-a", "service-b"]
```

- ✅ **Benefits**: Single lockfile, unified dependency resolution, faster installs
- ❌ **Limitation**: ALL members must use same Python version and compatible dependencies
- **Use when**: Services have compatible dependencies and same Python version

**Pattern 2: Excluded packages with path dependencies (dependency isolation)**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib"]
exclude = ["services/*"]
```

- ✅ **Benefits**: Each excluded package has independent lockfile, can use different Python versions and conflicting dependencies
- ❌ **Tradeoff**: Separate lockfiles, independent uv sync per service
- **Use when**: Services have conflicting dependencies or different Python versions

### Dependency Types in uv

**1. Workspace Dependencies** (`workspace = true`)
```toml
# service-a/pyproject.toml (when service-a is a workspace member)
[project]
dependencies = ["shared-lib"]

[tool.uv.sources]
shared-lib = { workspace = true }
```

- Requires shared-lib to be in `[tool.uv.workspace.members]`
- Single unified lockfile
- All packages must be compatible

**2. Path Dependencies** (`path = "..."`)
```toml
# service-a/pyproject.toml (when service-a is excluded)
[project]
dependencies = ["shared-lib"]

[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }
```

- Works even if shared-lib is not in workspace members
- Independent lockfile for service-a
- Allows incompatible dependencies

## Dependency Isolation Pattern

### Problem: Conflicting ML Framework Dependencies

**Scenario from VLA Server project:**
- `vla-server-openvla`: Requires TensorFlow 2.15 (OpenVLA model), Python 3.11
- `vla-server-octo`: Requires PyTorch 2.9 (Octo model), Python 3.12
- Both need shared library: `vla-server-base` (MuJoCo environment, config)

**❌ Won't work with traditional workspace members:**
```toml
# This FAILS - TensorFlow and PyTorch conflict in unified lockfile
[tool.uv.workspace]
members = ["vla-server-base", "vla-server-openvla", "vla-server-octo"]
```

**✅ Solution: Exclude services, use path dependencies**

### Implementation

**Step 1: Root workspace configuration**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["vla-server-base"]  # Only shared library
exclude = ["vla-servers/*"]     # Exclude all services
```

**Step 2: Shared library (workspace member)**
```toml
# vla-server-base/pyproject.toml
[project]
name = "vla-server-base"
requires-python = ">=3.11"  # Compatible with both services
dependencies = [
    "mujoco>=3.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]
```

**Step 3: Service A with TensorFlow (excluded package)**
```toml
# vla-servers/vla-server-openvla/pyproject.toml
[project]
name = "vla-server-openvla"
requires-python = ">=3.11,<3.12"
dependencies = [
    "vla-server-base",
    "tensorflow==2.15.0",
    "transformers>=4.40.0",
]

[tool.uv.sources]
vla-server-base = { path = "../../vla-server-base", editable = true }
```

**Step 4: Service B with PyTorch (excluded package)**
```toml
# vla-servers/vla-server-octo/pyproject.toml
[project]
name = "vla-server-octo"
requires-python = ">=3.12"
dependencies = [
    "vla-server-base",
    "torch>=2.9.0",
    "octo-models>=1.0.0",
]

[tool.uv.sources]
vla-server-base = { path = "../../vla-server-base", editable = true }
```

### Directory Structure

```
project root/
├── pyproject.toml                        # Root: workspace config
├── uv.lock                               # Lockfile for vla-server-base only
├── vla-server-base/                      # Shared library (workspace member)
│   ├── pyproject.toml
│   └── src/vla_server_base/
│       ├── adapters/base.py              # VLAModelAdapter
│       ├── services/mujoco_env.py        # MuJoCoEnvironment
│       └── config/settings.py            # Settings
└── vla-servers/                          # Services (excluded)
    ├── vla-server-openvla/
    │   ├── pyproject.toml                # TensorFlow 2.15, Python 3.11
    │   ├── uv.lock                       # Independent lockfile
    │   └── src/vla_server_openvla/
    │       └── adapter.py                # OpenVLAAdapter(VLAModelAdapter)
    └── vla-server-octo/
        ├── pyproject.toml                # PyTorch 2.9, Python 3.12
        ├── uv.lock                       # Independent lockfile
        └── src/vla_server_octo/
            └── adapter.py                # OctoAdapter(VLAModelAdapter)
```

### Running Commands

```bash
# Install shared library (from root)
uv sync

# Install service A (TensorFlow)
cd vla-servers/vla-server-openvla
uv sync  # Creates independent lockfile with TensorFlow

# Install service B (PyTorch)
cd vla-servers/vla-server-octo
uv sync  # Creates independent lockfile with PyTorch

# Run service A
cd vla-servers/vla-server-openvla
uv run python -m vla_server_openvla.main

# Run service B
cd vla-servers/vla-server-octo
uv run python -m vla_server_octo.main
```

## Best Practices

### 1. Shared Library Design

**Keep shared library minimal and compatible:**
```toml
# vla-server-base/pyproject.toml
[project]
requires-python = ">=3.11"  # Support widest range of services
dependencies = [
    # Only framework-agnostic dependencies
    "mujoco>=3.0.0",
    "pydantic>=2.0.0",
    "numpy>=1.24.0",
]

# NO ML frameworks in shared library
# ❌ "tensorflow"  - conflicts with PyTorch services
# ❌ "torch"       - conflicts with TensorFlow services
```

**Design pattern: Abstract base classes**
```python
# vla-server-base/src/vla_server_base/adapters/base.py
from abc import ABC, abstractmethod

class VLAModelAdapter(ABC):
    """Base class for VLA model adapters - framework-agnostic"""

    @abstractmethod
    def predict(self, observation: dict, instruction: str) -> np.ndarray:
        """Predict action from observation and instruction"""
        pass
```

### 2. Workspace Member Selection

**Choose workspace members carefully:**

✅ **Good workspace members:**
- Shared libraries with framework-agnostic dependencies
- Utility packages used across services
- Packages that MUST use same Python version

❌ **Bad workspace members (use exclude instead):**
- Services with ML framework dependencies (TensorFlow, PyTorch, JAX)
- Services requiring different Python versions
- Services with conflicting dependency versions

### 3. Path Dependency Configuration

**Always use editable path dependencies for local development:**
```toml
[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }
```

**Benefits of `editable = true`:**
- Changes to shared-lib immediately visible in services (no reinstall)
- Better development experience
- Proper source navigation in IDEs

### 4. Python Version Compatibility

**Shared library: Support wide range**
```toml
# vla-server-base/pyproject.toml
[project]
requires-python = ">=3.11"  # Supports 3.11, 3.12, 3.13...
```

**Services: Pin specific versions if needed**
```toml
# vla-server-openvla/pyproject.toml (TensorFlow only supports 3.11)
[project]
requires-python = ">=3.11,<3.12"

# vla-server-octo/pyproject.toml (PyTorch prefers 3.12)
[project]
requires-python = ">=3.12"
```

## Troubleshooting

### Error: "Package not found in workspace"

**Error:**
```
error: Failed to resolve dependencies: Package `vla-server-base` not found in workspace
```

**Cause:** Using `workspace = true` for a package not in `[tool.uv.workspace.members]`

**Fix:** Use path dependency instead
```toml
# Change from:
[tool.uv.sources]
shared-lib = { workspace = true }

# To:
[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }
```

### Error: Conflicting dependencies in lockfile

**Error:**
```
error: Conflicting dependencies for `numpy`:
  - tensorflow requires numpy<1.27
  - torch requires numpy>=2.0
```

**Cause:** Services with conflicting deps are workspace members (unified lockfile)

**Fix:** Exclude services from workspace
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["shared-lib"]      # Keep shared library
exclude = ["services/*"]       # Exclude conflicting services
```

### Changes to shared library not visible

**Problem:** Modified shared-lib code, but service still uses old version

**Fix 1:** Ensure editable installation
```toml
[tool.uv.sources]
shared-lib = { path = "../../shared-lib", editable = true }  # Add editable
```

**Fix 2:** Re-sync if not editable
```bash
cd service-a
uv sync  # Reinstall shared-lib
```

### Multiple lockfiles out of sync

**Problem:** Shared library version differs across service lockfiles

**Fix:** Update all services after changing shared library
```bash
# After modifying vla-server-base
cd vla-servers/vla-server-openvla && uv sync
cd ../vla-server-octo && uv sync
cd ../vla-server-mock && uv sync
```

**Prevention:** Use a script
```bash
#!/bin/bash
# scripts/sync-all.sh
uv sync  # Root
for service in vla-servers/*/; do
    (cd "$service" && uv sync)
done
```

## Real-World Example: VLA Server Microservices

**Example context:**

**Problem:**
- OpenVLA requires TensorFlow 2.15 (incompatible with PyTorch)
- Octo requires PyTorch 2.9 (incompatible with TensorFlow)
- Both need shared MuJoCo environment and config management

**Solution:**
```toml
# root/pyproject.toml
[tool.uv.workspace]
members = ["vla-server-base"]
exclude = ["vla-servers/*"]
```

**Result:**
- ✅ vla-server-base: Framework-agnostic shared library (1 lockfile)
- ✅ vla-server-openvla: TensorFlow 2.15 + Python 3.11 (independent lockfile)
- ✅ vla-server-octo: PyTorch 2.9 + Python 3.12 (independent lockfile)
- ✅ vla-server-mock: Minimal deps for testing (independent lockfile)

**PRs created:**
- PR #32: vla-server-base (foundation)
- PR #33: model_loader migration (shared utility)
- PR #34: vla-servers/mock (first service implementation)

**Pattern used:** Documentation First → Foundation First (see pr-splitting-strategy skill)

## Summary

**uv workspace patterns:**

| Pattern | Workspace Config | Dependency Type | Lockfiles | Use Case |
|---------|-----------------|-----------------|-----------|----------|
| **Traditional Monorepo** | `members = ["pkg-a", "pkg-b"]` | `workspace = true` | Single | Compatible dependencies, same Python version |
| **Dependency Isolation** | `members = ["shared"]`<br>`exclude = ["services/*"]` | `path = "..."` | Multiple | Conflicting deps, different Python versions |

**Key principles:**
1. **Shared library as workspace member** - Framework-agnostic, wide Python support
2. **Services excluded** - Independent lockfiles for conflicting dependencies
3. **Path dependencies** - Always use `editable = true` for development
4. **Minimal shared library** - Only include framework-agnostic dependencies

**When dependency conflicts arise, exclude services and use path dependencies instead of forcing them into a unified workspace.**
