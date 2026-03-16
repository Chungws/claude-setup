#!/bin/bash
# Safety net: mark any in-progress session logs as "interrupted" on session end.
# If Phase 4 ran properly, status is already "done" and this does nothing.

LOG_DIR="$HOME/dapi-ssot/SOT/session-logs"
END_TIME=$(date +"%Y-%m-%d %H%M%S")

[ -d "$LOG_DIR" ] || exit 0

for f in "$LOG_DIR"/*.md; do
  [ -f "$f" ] || continue
  if head -10 "$f" | grep -q 'status: in-progress'; then
    sed -i '' 's/status: in-progress/status: interrupted/' "$f"
    sed -i '' "s/종료: (완료 시 채울 것)/종료: $END_TIME (auto-closed by hook)/" "$f"
  fi
done

exit 0
