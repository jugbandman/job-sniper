# Job Discovery Architecture

This document covers the discovery subsystem: finding new jobs, tracking pipeline responses, and expanding the target company watchlist. It complements `ARCHITECTURE-JOB-ALERTS.md` (Gmail alert scanning) and the core agent system.

## What Is Job Discovery

Discovery is everything upstream of researching a specific posting. Where the alert scanner converts email alerts into scored job leads, the discovery subsystem handles:

1. **Response watching** - Detecting when companies in your pipeline reply to you
2. **Watchlist building** - Research-driven expansion of target companies and role titles
3. **Python scoring engine** - Deterministic 6-factor scoring and resume auto-picker (optional, complements the LLM-based scanner scoring)

---

## Components

### Response Watch Agent

`_agents/job-discovery/response-watch.md`

Scans Gmail for replies from tracked companies. Runs headlessly or via `/job-sniper response-watch`.

**What it does:**
1. Builds a company list from `job-tracker.md`, Obsidian applying/interviewing folders, and the JSONL cache
2. Derives email domains from company names
3. Searches Gmail for replies in the last 24 hours
4. Classifies each email (interested, rejection, auto-confirm, not a match)
5. Sends Slack DM for interested responses and rejections

**What it does NOT do:**
- Update the job tracker (Andy does that)
- Send emails on your behalf

**When to run:** Daily, or after sending outreach. Can run via launchd.

---

### Build Watchlist Agent

`_agents/job-discovery/build-watchlist.md`

Interactive agent that researches competitors, adjacent markets, and unconventional role titles, then proposes additions to `_config/company-watchlist.yaml`.

**What it does:**
1. Reads your profile and current watchlist
2. Researches competitors of past employers via web search
3. Finds companies in adjacent markets hiring senior sales/GTM leaders
4. Searches for unconventional title patterns (RevOps Director, Head of GTM Strategy, etc.)
5. Presents proposed additions and confirms before writing

**Output:** Updated `_config/company-watchlist.yaml` with tiered company list and `edge_searches` patterns.

**When to run:** Monthly, or when pipeline feels thin.

---

### Python Scoring Engine

`src/` directory - Python 3.10+ modules for systematic job scoring.

**Core modules:**
- `src/scorer.py` - 6-factor scoring algorithm (role match, compensation, company stage, market position, growth opportunity, GTM complexity)
- `src/models.py` - Job, ScoringResult, CompanyResearch dataclasses
- `src/storage.py` - JSONL read/write with deduplication
- `src/config.py` - Config loader for YAML/JSON config files
- `src/response_scanner.py` - Domain extraction and email matching for response watch
- `src/notifier.py` - Telegram Bot API notifications (optional, complement to Slack)
- `src/email_scanner.py` - Email parsing for Built In, LinkedIn, WTJ alert emails
- `src/mock_data.py` - Test data generator
- `src/rate_limiter.py` - Rate limiting for scrapers

**Supporting modules** (partially implemented, scaffolded):
- `src/researcher.py` - Company research agent
- `src/emailer.py` - SMTP email delivery
- `src/discovery_orchestrator.py` - Full pipeline orchestration
- `src/linkedin_scraper.py` - LinkedIn job search
- `src/wtj_scraper.py` - Welcome to the Jungle scraper
- `src/career_page_scraper.py` - Company career page scraper

**CLI:**
- `run-discovery.py` - Entry point. Supports `--mode discover|score|research|full|test`, `--limit`, `--dry-run`, `--debug`
- `requirements.txt` - Python dependencies

**How the scoring engine relates to the alert scanner:**

The alert scanner (`_agents/job-alerts/scanner.md`) scores jobs via LLM reasoning. The Python engine scores deterministically via YAML-configured weights. They use different rubrics. The Python engine is more tunable (change `_config/scoring-weights.yaml`, no code change) but requires job data in the Job dataclass format. The LLM scorer works directly on raw email/posting text.

For most users, the alert scanner is sufficient. The Python engine is useful if you want to score a large batch of jobs programmatically, or tune weights and re-score your full history.

---

### Configuration Files

| File | Purpose | Committed? |
|------|---------|-----------|
| `_config/scoring-weights.yaml` | 6-factor scoring weights + hard filters + resume picker rules | Yes (no personal data) |
| `_config/company-watchlist.yaml` | Your personal 3-tier target company list | No (gitignored, personal) |
| `_config/company-watchlist.example.yaml` | Template for starting your watchlist | Yes (generic companies) |

**Scoring weights** (`scoring-weights.yaml`) are the most important tuning lever. Adjust the `weights` section to change what matters most. Adjust `hard_filters` for compensation floor, location, and excluded industries. Adjust `thresholds` to change what score triggers an alert vs. digest inclusion.

---

### Email Templates (Optional)

`templates/daily-digest.html` and `templates/immediate-alert.html` - HTML email templates for the emailer module. Used if you configure SMTP delivery via `src/emailer.py`. Not required for the default Slack notification flow.

---

## Data Flow

```
Gmail alerts → alert scanner (scanner.md) → digest (LLM scoring)
                                           → JSONL cache (seen-jobs.jsonl)

Pipeline companies → response-watch.md → Gmail search → Slack DM

Company list + profile → build-watchlist.md → web research → company-watchlist.yaml

Raw job objects → run-discovery.py → Python scorer → scoring-results.jsonl
```

---

## Setup

### Response Watch (standalone)

No additional setup beyond the base job-sniper config. Reads `job-tracker.md` and Obsidian folders automatically.

Run manually:
```bash
claude -p "$(cat _agents/job-discovery/response-watch.md)"
```

Or run via `/job-sniper response-watch`.

### Build Watchlist

Requires `_config/company-watchlist.yaml` (copy from example if missing):
```bash
cp _config/company-watchlist.example.yaml _config/company-watchlist.yaml
```

Then run via `/job-sniper build-watchlist`.

### Python Scoring Engine

Install dependencies:
```bash
pip install -r requirements.txt
```

Test it works:
```bash
python3 run-discovery.py test
```

Score jobs from a JSONL file:
```bash
python3 run-discovery.py --mode score --debug
```

For Telegram notifications, set environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

---

## What Came From job-discovery

This subsystem was built by merging `jugbandman/job-discovery` into job-sniper. The following components were integrated:

- `_agents/job-discovery/response-watch.md` - Adapted from `job-discovery/skills/response-watch.md` (updated paths, Slack instead of Telegram as primary alert)
- `_agents/job-discovery/build-watchlist.md` - Adapted from `job-discovery/skills/build-watchlist.md` (updated config paths)
- `src/` - Copied from `job-discovery/src/` (all modules)
- `_config/scoring-weights.yaml` - Copied from `job-discovery/_config/scoring-weights.yaml`
- `_config/company-watchlist.example.yaml` - Copied from `job-discovery/_config/company-watchlist.yaml` (already generic, no personal data)
- `run-discovery.py` and `requirements.txt` - Copied from `job-discovery/`
- `templates/` - Copied from `job-discovery/templates/`

**What was NOT integrated** (job-sniper's versions are more complete):
- Gmail alert scanning (`_agents/job-alerts/scanner.md` kept over `job-discovery/skills/job-scan.md`)
- Job digest reporting (`alerts` mode kept over `job-discovery/skills/job-digest.md`)
- Watchlist monitoring (`_agents/watchlist-agent.md` kept over `job-discovery`'s config-only approach)
