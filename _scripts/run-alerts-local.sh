#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
JOB_SNIPER_DIR="${JOB_SNIPER_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG_DIR="$JOB_SNIPER_DIR/_cache/logs"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y-%m-%d-%H%M%S)
LOG_FILE="$LOG_DIR/alerts-local-$STAMP.log"

cd "$JOB_SNIPER_DIR"
{
  echo "[$(date -Iseconds)] starting local job alert scan"
  python3 scripts_scan_alerts.py
  echo "[$(date -Iseconds)] finished local job alert scan"
} | tee -a "$LOG_FILE"
