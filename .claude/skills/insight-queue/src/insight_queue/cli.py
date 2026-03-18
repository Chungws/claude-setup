"""Track which Claude Code sessions need insight analysis."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
LEARNINGS_DIR = Path.home() / "dapi-ssot" / "SOT" / "learnings"
STATE_FILE = LEARNINGS_DIR / ".analyzed.json"

MIN_SIZE_BYTES = 10 * 1024  # 10KB — skip trivial sessions
DEFAULT_DAYS = 3


def _load_state() -> dict[str, dict[str, str]]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def _save_state(state: dict[str, dict[str, str]]) -> None:
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def _get_mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def _get_project_name(jsonl: Path) -> str:
    """Read cwd from JSONL records, fallback to directory name decoding."""
    try:
        with jsonl.open() as f:
            for i, line in enumerate(f):
                if i >= 50:
                    break
                data = json.loads(line)
                cwd = data.get("cwd")
                if cwd:
                    home = str(Path.home())
                    return "~" + cwd[len(home) :] if cwd.startswith(home) else cwd
    except (json.JSONDecodeError, OSError):
        pass
    return jsonl.parent.name


def _find_pending(days: int = DEFAULT_DAYS) -> list[tuple[str, Path, str]]:
    """Return (session_id, jsonl_path, project_display) for sessions needing analysis."""
    if not PROJECTS_DIR.is_dir():
        return []

    state = _load_state()
    cutoff = time.time() - days * 86400
    pending: list[tuple[str, Path, str]] = []

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue
        project_display = None  # lazy — read from JSONL

        for jsonl in project_dir.glob("*.jsonl"):
            if jsonl.stat().st_size < MIN_SIZE_BYTES:
                continue
            if jsonl.stat().st_mtime < cutoff:
                continue

            session_id = jsonl.stem
            current_mtime = _get_mtime_iso(jsonl)

            entry = state.get(session_id)
            if entry is None or entry.get("source_mtime") != current_mtime:
                if project_display is None:
                    project_display = _get_project_name(jsonl)
                pending.append((session_id, jsonl, project_display))

    return pending


def _find_session(session_id: str) -> Path | None:
    """Find a session JSONL by ID across all projects."""
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / f"{session_id}.jsonl"
        if candidate.exists():
            return candidate
    return None


# --- Entry points ---


def cmd_pending_main() -> None:
    """List sessions needing analysis."""
    parser = argparse.ArgumentParser(description="List pending sessions")
    parser.add_argument("--quiet", action="store_true", help="No output if empty")
    args = parser.parse_args()

    pending = _find_pending()
    if not pending:
        if not args.quiet:
            print("분석 대기 중인 세션 없음.")
        return

    print(f"분석 대기 중인 세션 {len(pending)}건:")
    for session_id, jsonl, project in pending:
        mtime = datetime.fromtimestamp(jsonl.stat().st_mtime).strftime("%m-%d %H:%M")
        size_kb = jsonl.stat().st_size // 1024
        print(f"  - {session_id[:8]} | {project} | {mtime} | {size_kb}KB")
    print()
    print("인사이트 분석을 진행하려면 '인사이트 분석해줘'라고 요청하세요.")


def cmd_done_main() -> None:
    """Mark a session as analyzed."""
    parser = argparse.ArgumentParser(description="Mark session as analyzed")
    parser.add_argument("session_id", help="Session ID (UUID, prefix OK)")
    args = parser.parse_args()

    state = _load_state()
    jsonl = _find_session(args.session_id)

    if jsonl is None:
        # Try prefix match
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            for candidate in project_dir.glob(f"{args.session_id}*.jsonl"):
                jsonl = candidate
                break
            if jsonl:
                break

    if jsonl is None:
        print(f"세션을 찾을 수 없음: {args.session_id}", file=sys.stderr)
        sys.exit(1)

    session_id = jsonl.stem
    state[session_id] = {
        "analyzed_at": datetime.now(tz=timezone.utc).isoformat(),
        "source_mtime": _get_mtime_iso(jsonl),
    }
    _save_state(state)
    print(f"완료 마킹: {session_id[:8]}")


def cmd_reset_main() -> None:
    """Re-queue a session for analysis."""
    parser = argparse.ArgumentParser(description="Re-queue session for analysis")
    parser.add_argument("session_id", help="Session ID (UUID, prefix OK)")
    args = parser.parse_args()

    state = _load_state()
    # Support prefix match
    match = args.session_id
    matched_key = None
    for key in state:
        if key.startswith(match):
            matched_key = key
            break

    if matched_key:
        del state[matched_key]
        _save_state(state)
        print(f"재분석 대기로 복귀: {matched_key[:8]}")
    else:
        print(f"분석 기록 없음: {args.session_id}")


def cmd_list_main() -> None:
    """Show analyzed sessions."""
    state = _load_state()
    if not state:
        print("분석 완료된 세션 없음.")
        return

    print(f"분석 완료된 세션 {len(state)}건:")
    for session_id, entry in sorted(state.items(), key=lambda x: x[1]["analyzed_at"]):
        print(f"  - {session_id[:8]} (analyzed: {entry['analyzed_at'][:10]})")
