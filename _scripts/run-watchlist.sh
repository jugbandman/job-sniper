#!/bin/bash
# Job Sniper Watchlist Agent - Background Runner
# Called by launchd on schedule. Runs the watchlist agent headlessly.

set -euo pipefail

# Configuration
REPO_DIR="${JOB_SNIPER_DIR:-$HOME/Documents/Coding/job-sniper}"
AGENT_FILE="$REPO_DIR/_agents/watchlist-agent.md"
LOG_DIR="$REPO_DIR/_cache/logs"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
MODEL="${JOB_SNIPER_MODEL:-haiku}"
MAX_BUDGET="${JOB_SNIPER_MAX_BUDGET:-0.50}"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Timestamp for log file
TIMESTAMP=$(date +%Y-%m-%d_%H-%M)
LOG_FILE="$LOG_DIR/watchlist-$TIMESTAMP.log"

echo "Starting watchlist check at $(date)" >> "$LOG_FILE"

# Check prerequisites
if [ ! -f "$AGENT_FILE" ]; then
    echo "ERROR: Agent file not found: $AGENT_FILE" >> "$LOG_FILE"
    exit 1
fi

if [ ! -f "$REPO_DIR/_config/watchlist.md" ]; then
    echo "SKIP: No watchlist configured at $REPO_DIR/_config/watchlist.md" >> "$LOG_FILE"
    exit 0
fi

if ! command -v "$CLAUDE_BIN" &> /dev/null; then
    echo "ERROR: Claude binary not found at $CLAUDE_BIN" >> "$LOG_FILE"
    exit 1
fi

# Run the agent
cd "$REPO_DIR"

"$CLAUDE_BIN" -p \
    --model "$MODEL" \
    --dangerously-skip-permissions \
    --allowedTools "Read,Write,WebFetch,WebSearch,Bash(cat:*),Bash(date:*),Bash(mkdir:*)" \
    --no-session-persistence \
    --max-budget-usd "$MAX_BUDGET" \
    "$(cat "$AGENT_FILE")" \
    >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "Completed at $(date) with exit code $EXIT_CODE" >> "$LOG_FILE"

# Optional: macOS notification when new matches found
ALERTS_FILE="$REPO_DIR/_cache/watchlist-alerts.md"
if [ -f "$ALERTS_FILE" ] && grep -q "New roles: [1-9]" "$ALERTS_FILE" 2>/dev/null; then
    NEW_COUNT=$(grep "New roles:" "$ALERTS_FILE" | grep -o '[0-9]*')
    osascript -e "display notification \"$NEW_COUNT new job matches found\" with title \"Job Sniper\" subtitle \"Run /job-sniper to see details\"" 2>/dev/null || true
fi

# Clean up old logs (keep last 30 days)
find "$LOG_DIR" -name "watchlist-*.log" -mtime +30 -delete 2>/dev/null || true

exit $EXIT_CODE
