#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
JOB_SNIPER_DIR="${JOB_SNIPER_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG_DIR="$JOB_SNIPER_DIR/_cache/logs"
LOCAL_RUNNER="$SCRIPT_DIR/run-alerts-local.sh"

mkdir -p "$LOG_DIR"
STAMP=$(date +%Y-%m-%d-%H%M%S)
LOG_FILE="$LOG_DIR/alerts-$STAMP.log"

if [[ ! -x "$LOCAL_RUNNER" ]]; then
  echo "Missing or non-executable local runner: $LOCAL_RUNNER" >&2
  exit 1
fi

{
  echo "[$(date -Iseconds)] starting job alert scan via local runner"
  JOB_SNIPER_DIR="$JOB_SNIPER_DIR" "$LOCAL_RUNNER"
  echo "[$(date -Iseconds)] finished job alert scan via local runner"
} >> "$LOG_FILE" 2>&1
