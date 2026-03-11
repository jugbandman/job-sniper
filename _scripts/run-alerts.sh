#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
JOB_SNIPER_DIR="${JOB_SNIPER_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG_DIR="$JOB_SNIPER_DIR/_cache/logs"
PROMPT_FILE="$JOB_SNIPER_DIR/_agents/job-alerts/scanner.md"
OPENCLAW_BIN="${OPENCLAW_BIN:-$(command -v openclaw)}"
TARGET_CHAT_ID="${TARGET_CHAT_ID:-8143350442}"
TARGET_CHANNEL="${TARGET_CHANNEL:-telegram}"

mkdir -p "$LOG_DIR"
STAMP=$(date +%Y-%m-%d-%H%M%S)
LOG_FILE="$LOG_DIR/alerts-$STAMP.log"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt file: $PROMPT_FILE" >&2
  exit 1
fi

MESSAGE=$(cat "$PROMPT_FILE")

{
  echo "[$(date -Iseconds)] starting job alert scan"
  "$OPENCLAW_BIN" agent \
    --agent main \
    --message "$MESSAGE" \
    --deliver \
    --reply-channel "$TARGET_CHANNEL" \
    --reply-to "$TARGET_CHAT_ID"
  echo "[$(date -Iseconds)] finished job alert scan"
} >> "$LOG_FILE" 2>&1
