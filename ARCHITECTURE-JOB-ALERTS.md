# Job Alerts Architecture

This document covers the Gmail alert scanning flow for Job Sniper.

## Goal

Turn inbound job alert emails into a lightweight discovery pipeline:

1. scan Gmail for new alert emails
2. parse postings from message bodies
3. score each posting against Andy's profile
4. write a daily digest to the Obsidian vault
5. notify Andy immediately for Tier 1 matches

## Main components

### Alert scanner agent

`_agents/job-alerts/scanner.md`

Responsibilities:
- read user profile and alert source config
- query Gmail for recent job alert emails
- fetch full message bodies
- parse emails into structured job objects
- run the Python scoring pipeline
- write digest markdown
- send notifications for Tier 1 matches

### Python scoring pipeline

`run-discovery.py` and `src/`

Responsibilities:
- parse normalized job objects from stdin
- deduplicate against storage
- score jobs using `_config/scoring-weights.yaml`
- persist discovered jobs and scoring results in `_cache/`

Storage files:
- `_cache/discovered-jobs.jsonl`
- `_cache/scoring-results.jsonl`
- `_cache/applied-jobs.jsonl`

### Alert sources config

`_config/alert-sources.md`

Defines Gmail search queries per source. This keeps the scanner prompt simpler and makes source tuning a config change instead of a prompt rewrite.

### Launchd wrapper

- `_scripts/run-alerts.sh`
- `_scripts/com.job-sniper.alerts.plist`

Responsibilities:
- schedule the scanner 6 times daily
- log each run to `_cache/logs/`
- deliver the prompt into the OpenClaw main agent

## Data flow

```text
Gmail alerts
  -> alert source queries
  -> fetched email bodies
  -> src.email_scanner.parse_email
  -> run-discovery.py score-emails
  -> JSONL cache
  -> digest markdown
  -> Telegram / future Slack + macOS alerts for Tier 1
```

## Notification policy

- Tier 1, score >= 80 and passed filters, notify immediately
- Tier 2, score 60-79, digest only
- Tier 3, score 40-59, digest only
- Filtered, no notification

## Operational notes

- The Python engine is deterministic and tunable
- Gmail connectivity depends on available Google tooling in the runtime
- Notification routing currently targets Telegram through OpenClaw
- Slack or native macOS notification logic can be added later without changing the scoring pipeline

## Known gaps

- The current scanner depends on external Gmail tooling being available in the runtime
- Slack delivery is not yet wired in this reconstructed version
- macOS notifications are not yet emitted directly by `run-alerts.sh`
