#!/usr/bin/env bash
set -euo pipefail

# Multi-Model CLI Runner
# Usage: run_multi.sh "prompt" [agents...]
# Examples:
#   run_multi.sh "이 브랜치의 변경사항 리뷰해줘"
#   run_multi.sh "보안 취약점 찾아줘" claude gemini
#   run_multi.sh "테스트 전략 제안해줘" codex

PROMPT="${1:?Usage: run_multi.sh \"prompt\" [agents...]}"
shift
AGENTS=("${@:-claude codex gemini}")
[[ ${#AGENTS[@]} -eq 0 ]] && AGENTS=(claude codex gemini)

REPO_ROOT=$(git rev-parse --show-toplevel)
REVIEW_DIR=$(mktemp -d "${TMPDIR:-/tmp}/multi-XXXXXX")
RESULTS_DIR="$REVIEW_DIR/results"
mkdir -p "$RESULTS_DIR"

cleanup() {
  for wt in "$REVIEW_DIR"/wt-*; do
    [ -d "$wt" ] && git -C "$REPO_ROOT" worktree remove --force "$wt" 2>/dev/null || true
  done
}
trap cleanup EXIT

PIDS=()

for agent in "${AGENTS[@]}"; do
  WT_DIR="$REVIEW_DIR/wt-$agent"
  BRANCH_NAME="multi/$agent-$(date +%s)"
  git -C "$REPO_ROOT" worktree add -b "$BRANCH_NAME" "$WT_DIR" HEAD 2>/dev/null
  echo "=== Spawning $agent ===" >&2

  case "$agent" in
    claude)
      (
        cd "$WT_DIR"
        claude -p "$PROMPT" --output-format json > "$RESULTS_DIR/claude.json" 2>/dev/null || \
        echo "{\"agent\": \"claude\", \"error\": \"execution failed\"}" > "$RESULTS_DIR/claude.json"
      ) &
      PIDS+=($!)
      ;;
    codex)
      (
        cd "$WT_DIR"
        codex exec "$PROMPT" --json > "$RESULTS_DIR/codex.json" 2>/dev/null || \
        echo "{\"agent\": \"codex\", \"error\": \"execution failed\"}" > "$RESULTS_DIR/codex.json"
      ) &
      PIDS+=($!)
      ;;
    gemini)
      (
        cd "$WT_DIR"
        npx -y @google/gemini-cli -p "$PROMPT" --output-format json > "$RESULTS_DIR/gemini.json" 2>/dev/null || \
        echo "{\"agent\": \"gemini\", \"error\": \"execution failed\"}" > "$RESULTS_DIR/gemini.json"
      ) &
      PIDS+=($!)
      ;;
    *)
      echo "  unknown agent: $agent, skipping" >&2
      ;;
  esac
done

echo "=== Waiting for ${#PIDS[@]} agent(s) ===" >&2
for pid in "${PIDS[@]}"; do
  wait "$pid" 2>/dev/null || true
done
echo "=== All agents completed ===" >&2

echo "$RESULTS_DIR"
