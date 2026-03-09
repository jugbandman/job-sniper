# Job Sniper

**Treats job search like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently.**

An AI-powered agent system that researches companies, analyzes job postings, identifies hiring managers, maps your network, and generates customized application materials. It runs on [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and produces a folder of ready-to-use files for every job you target.

Don't be another resume in the pile. Be the candidate who did more research than the hiring manager.

## How It Works

The system is built from three layers that work together:

1. **Agent prompts** (`_agents/`) define what research to do and how to structure it
2. **Your config** (`_config/`) tells the agents who you are, what you're targeting, and how you like to write
3. **Templates** (`_templates/`) hold your resume, cover letter examples, and LinkedIn contacts

You paste an agent prompt into Claude Code, the agent reads your config, researches the company, and writes everything to a structured output folder.

## Quick Start

1. **Clone this repo** (skip this if you already have it)
   ```bash
   git clone https://github.com/jugbandman/job-sniper.git
   cd job-sniper
   ```

2. **Install Claude Code** (skip this if you already have it)
   Follow the [official install guide](https://docs.anthropic.com/en/docs/claude-code). You need a Claude API key or a Claude Pro/Max subscription.

3. **Open the repo in Claude Code and run `/job-sniper`**
   ```bash
   claude   # launch Claude Code from the repo root
   ```
   Then type `/job-sniper`. On first run, it detects you're a new user and walks you through setup: checks prerequisites, finds your resume, runs a 5-minute interview to build your profile, and generates your config files.

4. **Add your resume** to `_templates/resumes/` (PDF or markdown) if the setup didn't find it

5. **Run it again with a job URL**
   ```
   /job-sniper https://jobs.lever.co/some-company/some-role
   ```
   It reads your config, researches the company, and generates a full application package.

**Manual setup alternative:** If you prefer not to use the `/job-sniper` command, you can copy `_config/user-profile.example.md` to `_config/user-profile.md`, edit it by hand, then copy-paste any agent prompt from `_agents/job-search/` directly into Claude Code.

## Prerequisites

**Required:**
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- A resume (PDF or markdown, saved in `_templates/`)
- Your personal config files in `_config/` (the setup agent creates these)

**Optional but recommended:**
- LinkedIn contacts CSV (see below)
- A cover letter you've written (the agents match your writing voice from it)

## Warm Intros via LinkedIn

Cold applications convert at 2-5%. Warm intros convert at 10-20x that rate.

When you import your LinkedIn connections, the agents scan your network for every company you research. They find mutual connections, second-degree paths, and anyone at the company you already know, then draft personalized outreach messages for the warmest path to the hiring manager.

**How to export your connections (2 minutes):**

1. Go to [linkedin.com/mypreferences/d/download-my-data](https://www.linkedin.com/mypreferences/d/download-my-data)
2. Check **"Connections"** only (you don't need the rest)
3. Click **"Request archive"**
4. LinkedIn emails you a download link (usually within 10 minutes)
5. Download the ZIP, extract `Connections.csv`
6. Save it to `_templates/linkedin-contacts.csv`

The setup agent walks you through this during onboarding, and the agents pick up the file automatically on every run. You can re-export every few months to keep it current.

## Agent Modes

| Mode | Agent File | Best For |
|------|-----------|----------|
| **Interactive** | `_agents/job-search/interactive.md` | First-time users, guided Q&A format |
| **Main** | `_agents/job-search/main.md` | Power users, fill in variables and go |
| **Batch** | `_agents/job-search/batch.md` | Processing 5+ job URLs at once |
| **Multi-Job** | `_agents/job-search/multi-job.md` | Comparing 2-5 roles at the same company |

**Decision tree:**
- First time? Start with **Interactive**
- One job, you know the drill? Use **Main**
- Multiple jobs this week? Use **Batch**
- Same company, multiple roles? Use **Multi-Job**

## Discovery Features

Beyond scanning Gmail alerts, job-sniper includes two active discovery tools:

### Response Watch

Scans Gmail for replies from companies in your active pipeline. Run it after sending outreach to catch responses quickly.

```
/job-sniper response-watch
```

It builds a company list from your tracker and Obsidian applying/interviewing folders, derives email domains, searches Gmail for replies in the last 24 hours, and sends a Slack DM for any interested responses or rejections.

### Build Watchlist

Research-driven watchlist expansion. Analyzes your background and current watchlist, finds competitor companies, adjacent markets, and unconventional role titles you might be missing.

```
/job-sniper build-watchlist
```

It proposes tiered additions to `_config/company-watchlist.yaml` and confirms before writing anything. Run it monthly or whenever your pipeline feels thin.

**First time:** Copy the example config first:
```bash
cp _config/company-watchlist.example.yaml _config/company-watchlist.yaml
```

### Python Scoring Engine (Optional)

The `src/` directory contains a Python-based scoring engine that scores jobs deterministically using 6 weighted factors. It complements the LLM-based alert scanner for bulk processing or when you want reproducible scores you can tune via YAML.

```bash
pip install -r requirements.txt
python3 run-discovery.py test        # verify setup with mock data
python3 run-discovery.py --mode score  # score jobs in JSONL cache
```

Tune scoring by editing `_config/scoring-weights.yaml`. No code changes needed.

See `ARCHITECTURE-JOB-DISCOVERY.md` for the full discovery architecture.

---

## Watchlist & Pulse Check

Every time you run `/job-sniper`, it automatically:

1. **Watchlist check** - Scans career pages of companies you're watching (`_config/watchlist.md`) for new postings matching your profile. Only alerts on new roles, not ones you've already seen.

2. **Application pulse check** - Revisits URLs from your active applications to see if postings are still live. If one disappears, it flags it as a signal to follow up.

Add companies to your watchlist anytime:

```markdown
| Company   | Careers URL                        | Role Filter              |
|-----------|------------------------------------|--------------------------|
| Datadog   | https://careers.datadoghq.com/     | sales, account executive |
| Figma     | https://www.figma.com/careers/     | sales leadership         |
```

### Background Monitoring (Optional)

Want Job Sniper to check your watchlist automatically, even when you're not running it? Set up the background agent to run daily via macOS launchd.

The agent runs on the Haiku model ($0.05-$0.15 per check) and writes alerts to a file. Next time you run `/job-sniper`, your new matches appear instantly. You also get a macOS notification when new roles are found.

Setup takes 2 minutes. See `_scripts/README.md` for instructions.

## Research Depths

| Depth | Time | Cost Estimate | Files | Best For |
|-------|------|---------------|-------|----------|
| **Quick** | 15-20 min | $0.40-$1.00 | 7 | Most applications (volume play, 80% of your pipeline) |
| **Standard** | 30-45 min | $1.00-$2.50 | 10 | Strong matches you're excited about |
| **Deep** | 60+ min | $5-$12 | 12 | Dream jobs, top 1% opportunities |

Cost estimates assume API usage with the recommended model mix (Haiku for scraping, Sonnet for analysis). **If you have a Claude Pro or Max subscription, this runs within your existing plan at no additional cost.** See `MODEL-GUIDE.md` for full breakdown and model selection guidance.

## Output Files

Every research run creates a folder of markdown files at your configured output path.

**All depths produce:**
- `company-intelligence.md` - Company overview, news, culture, red flags
- `hiring-managers.md` - Who to contact (names, titles, LinkedIn)
- `job-analysis-fit-matrix.md` - Your fit for each requirement (A+/A/B/C/Gap)
- `positioning-strategy.md` - How to position yourself, key talking points
- `cover-letter.md` - Customized cover letter (ready to send)
- `linkedin-messages.md` - Outreach messages for hiring managers and connections
- `email-sequence.md` - Follow-up templates (Day 0, 3, 7)

**Standard and Deep add:**
- `network-paths.md` - Warm intro opportunities (requires LinkedIn CSV)
- `competitive-intelligence.md` - Market positioning, how the company differentiates

**Deep adds:**
- `interview-prep.md` - Questions to ask, STAR stories mapped to your experience
- `30-60-90-day-plan.md` - Execution plan (especially useful for sales/GTM roles)
- `take-home-package.md` - Research summary to attach with your application

## Job Alerts (Email Discovery)

The alert scanner monitors your Gmail for job alert emails from LinkedIn, Indeed, Greenhouse, Lever, Wellfound, Glassdoor, ZipRecruiter, BuiltIn Colorado, and Otta. It extracts new postings, scores them against your profile, deduplicates against a local cache, and writes a daily digest to your Obsidian vault. Tier 1 matches trigger a Slack DM and a macOS notification.

The scanner runs on a schedule via macOS launchd (every 3 hours from 6am to 9pm) and costs roughly $0.05-$0.20 per run on the Haiku model.

### How It Works

1. **Email scanning** - Reads job alert emails from Gmail using sender/subject patterns configured in `_config/alert-sources.md`
2. **Deduplication** - Checks extracted job URLs against `_cache/seen-jobs.jsonl` (90-day rolling window) so you only see new postings
3. **Job fetching** - Fetches the full posting page to extract requirements, salary, location
4. **Scoring** - Scores each job 0-100 against your profile (role fit, company stage, technical buyer, location, compensation) and assigns Tier 1/2/3
5. **Output** - Writes a markdown digest to `~/Documents/Obsidian Vault/80-Projects/job-search/_digests/YYYY-MM-DD-job-alerts.md`
6. **Notifications** - Sends a Slack DM and macOS notification for any Tier 1 matches

### Setup

1. Configure your alert sources (or use the defaults):
   ```bash
   open _config/alert-sources.md
   ```

2. Make the runner script executable:
   ```bash
   chmod +x _scripts/run-alerts.sh
   ```

3. Copy the plist to your LaunchAgents:
   ```bash
   cp _scripts/com.job-sniper.alerts.plist ~/Library/LaunchAgents/
   ```

4. Load the agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.job-sniper.alerts.plist
   ```

5. Verify it loaded:
   ```bash
   launchctl list | grep job-sniper.alerts
   ```

### Manual Test Run

```bash
bash _scripts/run-alerts.sh
```

Check results:
```bash
cat ~/Documents/Obsidian\ Vault/80-Projects/job-search/_digests/$(date +%Y-%m-%d)-job-alerts.md
cat _cache/logs/alerts-*.log
```

### Integration with Research Agents

The digest includes an "Action" line for every scored job: `Run /job-sniper [url] for full research`. This connects discovery to the existing research workflow. Find an interesting posting in your digest, run `/job-sniper` on it, and the research agents handle the rest.

### Adding Custom Alert Sources

Edit `_config/alert-sources.md` to add any email source you receive job alerts from. Any Gmail search query works. Test your query in Gmail search first, then add a row to the table.

### Scoring Breakdown

| Category | Max Points | What It Measures |
|----------|-----------|-----------------|
| Role Fit | 25 | Title match to your target roles |
| Company Stage | 20 | Series A-C, B2B SaaS, $5M-$50M ARR |
| Technical Buyer | 20 | Sells to eng/data/devops teams |
| Location | 15 | Denver/Boulder, remote, or compatible timezone |
| Compensation | 20 | $200K+ OTE target |

Jobs scoring 80+ are Tier 1 (apply now). 60-79 are Tier 2 (worth reviewing). 40-59 are Tier 3 (stretch). Hard filters (requires relocation, pure SMB, no PMF, wrong industry) instantly disqualify regardless of score.

## Configuration

Your personal setup lives in `_config/`. Two files control everything:

| File | What It Controls |
|------|-----------------|
| `user-profile.md` | Who you are, your background, target roles, resume path, output location |
| `user-preferences.md` | Writing style, cover letter tone, research depth defaults, scoring thresholds |

**First time?** Run the setup agent (`_agents/setup.md`) to generate both files interactively.

**Already set up?** Edit the files directly. Agents read them fresh every run, so changes take effect immediately.

See `_config/README.md` for details on what goes where, and `_config/user-profile.example.md` for a complete reference configuration.

## Model Guide

The agents work with any Claude model, but different tasks benefit from different models.

| Task Type | Recommended Model |
|-----------|------------------|
| Scraping and parsing | Haiku (cheapest, fastest) |
| Research, analysis, cover letters | Sonnet (best balance) |
| Dream job strategy, competitive analysis | Opus (highest quality) |

**For everyday use, Sonnet handles 90% of tasks well.** Only reach for Opus on Deep research for your top-choice companies.

Full cost estimates and model selection guidance are in `MODEL-GUIDE.md`.

## File Structure

```
job-sniper/
├── README.md                          # This file
├── QUICK_START.md                     # Condensed getting-started guide
├── USAGE_GUIDE.md                     # Detailed usage instructions
├── MODEL-GUIDE.md                     # Model recommendations and cost estimates
├── ARCHITECTURE-JOB-ALERTS.md        # Alert scanner architecture
├── ARCHITECTURE-JOB-DISCOVERY.md     # Discovery subsystem architecture
├── run-discovery.py                   # Python scoring engine CLI
├── requirements.txt                   # Python dependencies (for scoring engine)
├── job-tracker.md                     # Activity log (auto-created, gitignored)
│
├── _config/                           # Your personal configuration
│   ├── README.md                      # Config documentation
│   ├── user-profile.md                # Your background and targets (you create this)
│   ├── user-profile.example.md        # Example configuration for reference
│   ├── user-preferences.md            # Writing style and preferences (you create this)
│   ├── watchlist.md                   # Companies to monitor for new postings
│   ├── alert-sources.md              # Gmail patterns for job alert scanning
│   ├── scoring-weights.yaml           # Python scorer: 6-factor weights + filters (tunable)
│   ├── company-watchlist.yaml         # Your 3-tier target company list (gitignored)
│   └── company-watchlist.example.yaml # Example watchlist to start from
│
├── _cache/                            # Watchlist cache and pulse check data (gitignored)
│   └── README.md
│
├── src/                               # Python scoring engine modules
│   ├── models.py                      # Job, ScoringResult dataclasses
│   ├── scorer.py                      # 6-factor scoring algorithm + resume picker
│   ├── storage.py                     # JSONL read/write with deduplication
│   ├── config.py                      # Config loader
│   ├── email_scanner.py               # Email parsing for Built In, LinkedIn, WTJ
│   ├── response_scanner.py            # Domain extraction and email matching
│   ├── notifier.py                    # Telegram notifications (optional)
│   ├── mock_data.py                   # Test data generator
│   └── ...                            # Additional modules (researcher, emailer, scrapers)
│
├── templates/                         # HTML email templates (for emailer module)
│   ├── daily-digest.html              # Daily digest template
│   └── immediate-alert.html           # Immediate alert template
│
├── _agents/                           # Agent prompts (the brains)
│   ├── setup.md                       # Interactive onboarding agent
│   ├── watchlist-agent.md             # Background watchlist checker (runs via claude -p)
│   ├── job-alerts/                    # Email-based job discovery
│   │   └── scanner.md                # Gmail alert scanner (runs via claude -p)
│   ├── job-discovery/                 # Pipeline monitoring and watchlist building
│   │   ├── response-watch.md          # Scan Gmail for company replies
│   │   └── build-watchlist.md         # Research and expand target company list
│   └── job-search/                    # Job search agents
│       ├── main.md                    # Single job deep dive
│       ├── batch.md                   # Batch URL processing
│       ├── interactive.md             # Guided Q&A mode
│       └── multi-job.md              # Compare roles at same company
│
├── _scripts/                          # Automation (background monitoring)
│   ├── README.md                      # Setup instructions for launchd
│   ├── run-watchlist.sh               # Shell wrapper for watchlist agent
│   ├── com.job-sniper.watchlist.plist # macOS launchd schedule (daily 7am)
│   ├── run-alerts.sh                  # Shell wrapper for alert scanner
│   └── com.job-sniper.alerts.plist   # macOS launchd schedule (every 3hrs)
│
└── _templates/                        # Your materials
    ├── README.md                      # Template documentation
    ├── resumes/                       # Your resume versions
    ├── cover-letter-style-guide.md    # Cover letter tone reference
    ├── resume-tldr-template.md        # Resume summary template
    └── linkedin-contacts.csv          # Your LinkedIn export (optional)
```

## Contributing and Customization

This tool is designed to be forked and personalized. Some ways to make it yours:

- **Add new agent modes** in `_agents/job-search/` for different research workflows
- **Customize templates** in `_templates/` with your own cover letter formats
- **Tune preferences** in `_config/user-preferences.md` to match your voice
- **Add new lenses** beyond job search (prospect research, market intel) in `_agents/core/`

The agent prompts are plain markdown. Read one, understand the pattern, and adapt it however you want.

## Troubleshooting

**Agent can't find the hiring manager?**
That happens. The agent will note it and generate generic outreach. You can check the company website Team page, LinkedIn job posting, or search on X/Twitter.

**Network path analysis finds nothing?**
Expected if you haven't exported your LinkedIn CSV, or if you don't have connections at that company. The agent still generates cold outreach messages.

**Cover letter too long?**
Edit down to one page. Move the extra research into a take-home attachment (Deep mode generates this automatically).

**Job description is vague?**
The agent does its best, but better input produces better output. Add context in the "special instructions" field.

**Agent running slow?**
Use Quick depth (15-20 min) for most jobs. Save Deep (60+ min) for the ones that really matter.

**Config not being picked up?**
Make sure your files are named exactly `_config/user-profile.md` and `_config/user-preferences.md`. The agents look for these specific filenames.

## Why This Works

The normal application process looks like this: submit a generic resume, maybe write a cover letter, wait and hope. Response rates sit around 2-5%.

This tool flips that. Every application comes with company-specific research, a tailored cover letter, hiring manager outreach, and (for dream jobs) a take-home research package that proves you've done the homework. When a hiring manager sees that level of preparation, you stand out.

It works because it treats job search like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently.

---

Useful? Buy Andy a coffee (or beer): **venmo:@jugbandman**
