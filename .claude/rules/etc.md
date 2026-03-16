# ETC — Easy To Change

Every code decision must pass one test: **"Will this be easy to change later?"**

## When writing new code
- Prefer small, focused functions over long procedural blocks.
- Separate "what to do" from "how to do it" — caller decides what, callee decides how.
- Avoid hardcoding values that represent decisions (config, thresholds, messages).
- If two things change for different reasons, they belong in different modules.

## When adding to existing code
- Before adding, ask: "Does the current structure accommodate this change naturally?"
- If no → restructure first, then add. Don't force new logic into a shape that resists it.
- If a file/function is already doing too much, split before extending.

## What to avoid
- Writing code that "works" but only for the current exact requirement.
- Coupling unrelated concerns because it's faster right now.
- Letting files grow past ~200 lines without questioning the structure.
