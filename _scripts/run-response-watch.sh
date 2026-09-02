#!/bin/bash
# Job Sniper Response Watch Agent - Background Runner
# Scans Gmail for replies from companies in active pipeline.
# Sends Slack DM for matches. Runs via claude -p on schedule.

set -euo pipefail

# Configuration
REPO_DIR="${JOB_SNIPER_DIR:-$HOME/Documents/Coding/job-sniper}"
AGENT_FILE="$REPO_DIR/_agents/job-discovery/response-watch.md"
CONTEXT_BUNDLE="$REPO_DIR/_config/vault-context-bundle.md"
LOG_DIR="$REPO_DIR/_cache/logs"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
MODEL="${JOB_SNIPER_MODEL:-sonnet}"
MAX_BUDGET="${JOB_SNIPER_MAX_BUDGET:-1.00}"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M)
LOG_FILE="$LOG_DIR/response-watch-$TIMESTAMP.log"

echo "Starting response watch at $(date)" >> "$LOG_FILE"

# Check prerequisites
if [ ! -f "$AGENT_FILE" ]; then
    echo "ERROR: Agent file not found: $AGENT_FILE" >> "$LOG_FILE"
    exit 1
fi

if ! command -v "$CLAUDE_BIN" &> /dev/null; then
    echo "ERROR: Claude binary not found at $CLAUDE_BIN" >> "$LOG_FILE"
    exit 1
fi

# Build prompt with context bundle prefix
PROMPT=""
if [ -f "$CONTEXT_BUNDLE" ]; then
    PROMPT="## Vault Context (follow these rules for all output)

$(cat "$CONTEXT_BUNDLE")

---

## Agent Task

"
    echo "Context bundle loaded ($(wc -l < "$CONTEXT_BUNDLE") lines)" >> "$LOG_FILE"
else
    echo "WARNING: No context bundle, running without vault rules" >> "$LOG_FILE"
fi
PROMPT+="$(cat "$AGENT_FILE")"

# Run the agent
cd "$REPO_DIR"

"$CLAUDE_BIN" -p \
    --model "$MODEL" \
    --dangerously-skip-permissions \
    --allowedTools "Read,Write,Glob,Grep,WebFetch,WebSearch,Bash(cat:*),Bash(date:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*),mcp__google-workspace__search_gmail_messages,mcp__google-workspace__get_gmail_message_content,mcp__claude_ai_Slack__slack_send_message" \
    --no-session-persistence \
    --max-budget-usd "$MAX_BUDGET" \
    "$PROMPT" \
    >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "Completed at $(date) with exit code $EXIT_CODE" >> "$LOG_FILE"

# Clean up old logs (keep last 30 days)
find "$LOG_DIR" -name "response-watch-*.log" -mtime +30 -delete 2>/dev/null || true

exit $EXIT_CODE
