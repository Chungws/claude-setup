"""Track which Claude Code sessions have been analyzed for feedback."""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
STATE_FILE = Path.home() / "dapi-ssot" / "SOT" / "learnings" / ".analyzed.json"

MIN_SIZE_BYTES = 10 * 1024  # 10KB
DEFAULT_DAYS = 3


def _load_state() -> dict[str, dict[str, str]]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def _save_state(state: dict[str, dict[str, str]]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def _project_name(jsonl: Path) -> str:
    try:
        with jsonl.open() as f:
            for i, line in enumerate(f):
                if i >= 50:
                    break
                cwd = json.loads(line).get("cwd")
                if cwd:
                    home = str(Path.home())
                    return "~" + cwd[len(home):] if cwd.startswith(home) else cwd
    except (json.JSONDecodeError, OSError):
        pass
    return jsonl.parent.name


def cmd_pending(days: int = DEFAULT_DAYS) -> None:
    if not PROJECTS_DIR.is_dir():
        print("세션 없음.")
        return

    state = _load_state()
    cutoff = time.time() - days * 86400

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue
        for jsonl in project_dir.glob("*.jsonl"):
            st = jsonl.stat()
            if st.st_size < MIN_SIZE_BYTES or st.st_mtime < cutoff:
                continue
            sid = jsonl.stem
            entry = state.get(sid)
            if entry is None or entry.get("source_mtime") != _mtime_iso(jsonl):
                mtime = datetime.fromtimestamp(st.st_mtime).strftime("%m-%d %H:%M")
                project = _project_name(jsonl)
                print(f"{sid[:8]} | {project} | {mtime} | {st.st_size // 1024}KB | {jsonl}")


def cmd_done(session_id: str) -> None:
    state = _load_state()

    # Find JSONL by exact or prefix match
    jsonl: Path | None = None
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for candidate in project_dir.glob(f"{session_id}*.jsonl"):
            jsonl = candidate
            break
        if jsonl:
            break

    if jsonl is None:
        print(f"세션을 찾을 수 없음: {session_id}", file=sys.stderr)
        sys.exit(1)

    sid = jsonl.stem
    state[sid] = {
        "analyzed_at": datetime.now(tz=timezone.utc).isoformat(),
        "source_mtime": _mtime_iso(jsonl),
    }
    _save_state(state)
    print(f"done: {sid[:8]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tracker.py <pending|done> [session_id]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "pending":
        cmd_pending()
    elif cmd == "done":
        cmd_done(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
