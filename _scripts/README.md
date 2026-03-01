# Automation Scripts

Scripts for running Job Sniper agents in the background.

## Watchlist Agent (Background Job Checking)

The watchlist agent runs daily via macOS launchd, checking your watched companies for new job postings and verifying your active applications are still live.

### What It Does

1. Reads your watchlist (`_config/watchlist.md`)
2. Fetches each company's careers page
3. Filters for roles matching your criteria
4. Diffs against the cache to find NEW postings
5. Checks active application URLs (pulse check)
6. Writes alerts to `_cache/watchlist-alerts.md`
7. Next time you run `/job-sniper`, you see the alerts

### Setup

1. Make the runner script executable:
   ```bash
   chmod +x _scripts/run-watchlist.sh
   ```

2. Edit the plist to match your system paths:
   ```bash
   # Update the paths in the plist if your repo is in a different location
   open _scripts/com.job-sniper.watchlist.plist
   ```

3. Copy the plist to your LaunchAgents:
   ```bash
   cp _scripts/com.job-sniper.watchlist.plist ~/Library/LaunchAgents/
   ```

4. Load the agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.job-sniper.watchlist.plist
   ```

5. Verify it's loaded:
   ```bash
   launchctl list | grep job-sniper
   ```

### Manual Test Run

Run the agent once to verify it works:

```bash
bash _scripts/run-watchlist.sh
```

Check the results:

```bash
cat _cache/watchlist-alerts.md
cat _cache/logs/watchlist-*.log
```

### Configuration

The shell script reads environment variables for customization. Set these in the plist's `EnvironmentVariables` section or export them in your shell:

| Variable | Default | Description |
|----------|---------|-------------|
| `JOB_SNIPER_DIR` | `~/Documents/Coding/job-sniper` | Repo location |
| `CLAUDE_BIN` | `~/.local/bin/claude` | Claude binary path |
| `JOB_SNIPER_MODEL` | `haiku` | Model to use (haiku recommended for cost) |
| `JOB_SNIPER_MAX_BUDGET` | `0.50` | Max spend per run in USD |

### Changing the Schedule

Edit the plist's `StartCalendarInterval` section. Examples:

**Every day at 7am (default):**
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>7</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

**Twice daily (7am and 6pm):**
```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

After editing, unload and reload:

```bash
launchctl unload ~/Library/LaunchAgents/com.job-sniper.watchlist.plist
launchctl load ~/Library/LaunchAgents/com.job-sniper.watchlist.plist
```

### Disabling

```bash
launchctl unload ~/Library/LaunchAgents/com.job-sniper.watchlist.plist
```

### Logs

| Log | Location | Contents |
|-----|----------|----------|
| Quick status | `/tmp/job-sniper-watchlist.log` | launchd stdout |
| Errors | `/tmp/job-sniper-watchlist.error.log` | launchd stderr |
| Detailed | `_cache/logs/watchlist-*.log` | Full agent output per run |

Old detailed logs are automatically cleaned up after 30 days.

### Cost

Runs on the Haiku model with a $0.50 safety cap per run.

| Companies Watched | Per Run | Monthly (daily runs) |
|-------------------|---------|---------------------|
| 3-5 | $0.03-$0.08 | ~$1-2.50 |
| 5-10 | $0.05-$0.15 | ~$1.50-4.50 |
| 10-20 | $0.10-$0.30 | ~$3-9 |

### Notifications

By default, a macOS notification pops up when new matches are found. This runs automatically from the shell script. To disable it, comment out the `osascript` block in `run-watchlist.sh`.

For Slack or email notifications, see the comments at the bottom of `run-watchlist.sh`.
