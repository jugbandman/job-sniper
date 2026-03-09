---
name: job-sniper
description: Job search tool that treats every application like a sales process. Handles first-time setup, config check, and all research modes (interactive, main, batch, multi-job). Invoke with /job-sniper [url or mode].
---

# Job Sniper

> **Paths:** Always reference `CLAUDE.md` → "Key Paths" section for canonical folder paths. Never hardcode folder paths in this skill.

A job search tool that treats every application like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently. Handles everything from first-time setup to executing research agents.

## Gmail Account

Job alert emails go to `andrewdcarlson@gmail.com`. Always use this as `user_google_email` for Gmail MCP calls in alerts mode.

## Key Paths

- **Tool repo:** `~/Documents/Coding/job-sniper/`
- **Config:** `~/Documents/Coding/job-sniper/_config/user-profile.md`
- **Agent prompts:** `~/Documents/Coding/job-sniper/_agents/job-search/`
- **Setup agent:** `~/Documents/Coding/job-sniper/_agents/setup.md`
- **Materials (Obsidian):** `80-Projects/job-search/Job Search, Data/`
- **Materials (legacy):** `~/Documents/Job Search 2025/`
- **Output destination:** Read from user-profile.md `## Output Path` section
- **Job tracker:** `~/Documents/Coding/job-sniper/job-applications-tracker.csv`
- **Alert scanner:** `~/Documents/Coding/job-sniper/_agents/job-alerts/scanner.md`
- **Alert sources:** `~/Documents/Coding/job-sniper/_config/alert-sources.md`
- **Alert digests:** `80-Projects/job-search/_digests/` (in Obsidian vault)

## On Invocation

**Step 1: Check if configured**

Read `~/Documents/Coding/job-sniper/_config/user-profile.md`.

- If it **does not exist** or contains only placeholder values like `{add value}` → go to **First-Time Setup**
- If it **exists and is populated** → go to **Mode Selection**

---

## First-Time Setup

Run this flow for new users or when config is missing.

### 1. Prerequisites Check

Verify these exist. Report status for each:

```
Checking prerequisites...

[✓/✗] Tool repo cloned at ~/Documents/Coding/job-sniper/
[✓/✗] Resume file found (check _templates/resumes/ for PDFs and markdown)
[✓/✗] Cover letter style guide (_templates/cover-letter-style-guide.md)
[✓/✗] LinkedIn contacts CSV (_templates/linkedin-contacts.csv)
```

For any missing items:

- **Repo not found:** Tell them to clone it: `git clone https://github.com/jugbandman/job-sniper.git ~/Documents/Coding/job-sniper/`
- **Resume missing:** Search common locations (`~/Documents/`, `~/Desktop/`, `~/Downloads/`) for PDF resumes. If found, offer to copy to `_templates/resumes/`. If not found, note placeholder and continue.
- **Style guide missing:** Not critical, defaults work fine. Note it.
- **LinkedIn CSV missing:** Optional. Explain how to export from LinkedIn Settings > Data Privacy > Get a copy of your data. Note as optional and continue.

### 2. Find Existing Materials

Search the user's system for job search materials that could be imported:

```
Scanning for existing materials...
```

Check these locations:
- `~/Documents/Job Search*/` (any year variant)
- `80-Projects/job-search/Job Search, Data/` (Obsidian vault, resolve via CLAUDE.md Key Paths)
- `~/Desktop/Vault Drop/`
- `~/Downloads/` (recent PDFs with "resume" or "cover" in name)

Report what was found and offer to copy relevant files to `_templates/`.

### 3. Run Setup Interview

Read the setup agent prompt from `~/Documents/Coding/job-sniper/_agents/setup.md` and execute it. This collects:

- Basic info (name, email, location)
- Professional background (roles, metrics, strengths)
- Target roles (titles, company types, compensation)
- Materials paths (resume, CSV, style guide)
- Output preferences (where to save research)
- Writing style (tone, length, pet peeves)

The setup agent generates:
- `_config/user-profile.md`
- `_config/user-preferences.md`

### 4. Confirm and Next Steps

After config files are created:

```
Setup complete! Your config is saved at:
→ _config/user-profile.md (your profile and targets)
→ _config/user-preferences.md (writing style and preferences)

Ready to run your first job search. Paste a job URL or pick a mode:
- interactive - Answer questions, get full research package
- batch - Process up to 5 job URLs at once
- multi-job - Compare multiple roles at the same company
```

Then go to **Mode Selection**.

---

## Mode Selection

When the user is already configured. Parse the invocation argument:

**If a URL was passed** (e.g., `/job-sniper https://jobs.lever.co/...`):
→ Go directly to **Interactive Mode** with that URL

**If a mode keyword was passed** (e.g., `/job-sniper batch`):
→ Go to that mode

**If "tracker" or "log" was passed** (e.g., `/job-sniper tracker`):
→ Show the current activity log (read and display `job-tracker.md` from the job-sniper repo)

**If "alerts" was passed** (e.g., `/job-sniper alerts`):
→ Read the latest digest from `80-Projects/job-search/_digests/` (sort by filename, pick most recent)
→ Display it with obsidian:// deep link to the file
→ Show Tier 1 and Tier 2 matches with action links

**If "alerts run" was passed** (e.g., `/job-sniper alerts run`):
→ Execute the alert scanner agent at `~/Documents/Coding/job-sniper/_agents/job-alerts/scanner.md`
→ This triggers a manual Gmail scan, scores new postings, writes a digest
→ Show results when complete

**If "response-watch" was passed** (e.g., `/job-sniper response-watch`):
→ Execute the response watch agent at `~/Documents/Coding/job-sniper/_agents/job-discovery/response-watch.md`
→ Scans Gmail for replies from companies in your active pipeline (last 24 hours)
→ Sends Slack DM for any matches found, prints summary

**If "build-watchlist" was passed** (e.g., `/job-sniper build-watchlist`):
→ Execute the watchlist builder agent at `~/Documents/Coding/job-sniper/_agents/job-discovery/build-watchlist.md`
→ Researches competitors, adjacent markets, and unconventional role titles
→ Proposes additions to `_config/company-watchlist.yaml` and confirms before writing

**If no argument or just `/job-sniper`:**

Present the mode picker:

```
Job Sniper ready. What are we doing?

1. interactive - Paste a job URL, answer a few questions, get the full package
2. main - Fill in structured inputs, get deep research (best for dream jobs)
3. batch - Process up to 5 URLs at once (quick depth, high volume)
4. multi-job - Compare 2-5 roles at the same company
5. tracker - View your activity log
6. alerts - View today's job alert digest
7. alerts run - Trigger a manual alert scan now
8. response-watch - Scan Gmail for replies from companies in your pipeline
9. build-watchlist - Research and expand your target company watchlist

Paste a URL to jump straight in, or pick a mode (1-9):
```

Wait for user input.

---

## Mode Execution

For each mode, read the corresponding agent prompt, load the user's config, and execute.

### Interactive Mode

1. Read `_agents/job-search/interactive.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask the user for:
   - Job URL (if not already provided)
   - Research depth: Quick / Standard / Deep (default: Quick)
   - What matters most to them about this role (optional)
4. Execute the agent workflow
5. Save outputs to the path defined in user-profile.md
6. Log to activity tracker → **Activity Log**
7. Prompt for similar roles → **Similar Role Discovery**
8. Link deliverables in today.md and Recent Work MOC per CLAUDE.md rules

### Main Mode

1. Read `_agents/job-search/main.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Collect the structured USER INPUTS block from the agent prompt:
   - JOB_URL
   - COMPANY_NAME
   - RESEARCH_DEPTH
   - ROLE_TYPE
   - YOUR_PRIORITY
4. Execute the full agent workflow
5. Save outputs, log to tracker, link deliverables
6. Prompt for similar roles → **Similar Role Discovery**

### Batch Mode

1. Read `_agents/job-search/batch.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask user to paste 1-5 job URLs (one per line)
4. Process each URL at Quick depth
5. Save outputs, log each to tracker, link deliverables
6. After all URLs processed, prompt for similar roles → **Similar Role Discovery**

### Multi-Job Mode

1. Read `_agents/job-search/multi-job.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask for company name and 2-5 job URLs
4. Execute comparative analysis
5. Save outputs, log each to tracker, link deliverables

### Response Watch Mode

1. Read `~/Documents/Coding/job-sniper/_agents/job-discovery/response-watch.md`
2. Execute the agent headlessly (no user prompts needed)
3. Agent reads job-tracker.md + Obsidian applying/interviewing folders to build company list
4. Searches Gmail for replies from those companies (last 24 hours)
5. Sends Slack DM for any interested responses or rejections found
6. Print summary to stdout when complete

### Build Watchlist Mode

1. Read `~/Documents/Coding/job-sniper/_agents/job-discovery/build-watchlist.md`
2. Read `_config/user-profile.md` for background context
3. Read `_config/company-watchlist.yaml` (create from example if missing)
4. Agent researches competitors, adjacent markets, and unconventional role titles
5. Proposes additions to watchlist, confirms before writing
6. Writes updated `_config/company-watchlist.yaml`

---

## Similar Role Discovery

After research completes for any mode (except multi-job, which already compares roles), prompt the user:

```
Research complete. Want me to look for similar roles?

1. More [role type] roles (e.g., "more sales leadership roles")
2. Other roles at [company name]
3. Similar roles in [location from the posting]
4. Skip

Pick one or describe what you're looking for:
```

**If they pick an option:**

1. Use web search to find matching job postings on the company's careers page, LinkedIn, Lever, Greenhouse, Ashby, etc.
2. Present results as a quick list:

```
Found X roles that might match:

1. [Title] at [Company] - [Location] - [URL]
2. [Title] at [Company] - [Location] - [URL]
3. [Title] at [Company] - [Location] - [URL]

Want to research any of these? (enter numbers, "all", or "skip")
```

3. If they select roles, process them through the appropriate mode (interactive for 1, batch for 2+)
4. After processing, prompt again: "Want to keep looking, or done for now?"

**If they skip**, move to the summary.

---

## Activity Log

Maintain `job-tracker.md` in the CRA repo root (`~/Documents/Coding/job-sniper/job-tracker.md`) as a running log of all job search activity. This file is gitignored (personal data).

### Format

If `job-tracker.md` doesn't exist, create it with this structure:

```markdown
# Job Search Activity Log

> Track every application, research run, and follow-up in one place.

## Applications

| Date | Company | Role | Location | Fit | Status | Follow-up | URL | Notes |
|------|---------|------|----------|-----|--------|-----------|-----|-------|

## Stats

**Total researched:** 0
**Total applied:** 0
**Interviews:** 0
**Last activity:** n/a
```

### Logging Rules

After every research run, append a row to the Applications table:

| Field | Value |
|-------|-------|
| **Date** | YYYY-MM-DD |
| **Company** | Company name |
| **Role** | Job title |
| **Location** | City/Remote from the posting |
| **Fit** | Fit score from analysis (e.g., "85% Tier 1") |
| **Status** | `Researched`, `Applied`, `Outreach Sent`, `Interview`, `Offer`, `Rejected`, `Withdrawn`, `No Response` |
| **Follow-up** | Next follow-up date (Date + 3 days for first follow-up) or "n/a" |
| **URL** | `[link](full-url)` |
| **Notes** | Key info: hiring manager name, referral source, what stood out, red flags |

### Status Updates

When the user mentions updating a status (e.g., "I applied to Acme" or "got an interview at Acme"), find the row in the tracker and update:
- Change Status column
- Update Follow-up date
- Add to Notes

### Stats

Update the Stats section at the bottom after every change:
- Count rows by status
- Update "Last activity" date

---

## After Every Run

Regardless of mode, always:

1. **Log to activity tracker:** Append row to `job-tracker.md` (see Activity Log section)
2. **Link in today.md:** Find or create a JOB SEARCH task entry and append wiki-link to the research output
3. **Log to Recent Work MOC:** Add entry to `++Home/MOC !Recent Work.md`
4. **Show summary:** Display what was created with clickable obsidian:// deep links

---

## Model Recommendations

When executing agent workflows, suggest optimal model usage:

| Task | Model | Why |
|------|-------|-----|
| Web scraping, data extraction | Haiku | Fast, cheap, good at structured extraction |
| Company analysis, fit scoring | Sonnet | Strong reasoning, good cost/quality balance |
| Cover letters, strategic positioning | Sonnet | Best default for writing quality |
| 30/60/90 plans, deep strategy | Opus | Worth the cost for dream jobs |

Default to Sonnet for everything unless the user specifies otherwise or picks Deep research depth (suggest Opus for strategic sections).

---

## Always

- Read config files fresh every run (user may have updated them between sessions)
- Use obsidian:// deep links for all vault file references in output
- Save research outputs to the path in user-profile.md, not hardcoded paths
- Log every research run to `job-tracker.md`
- Prompt for similar roles after research completes
- Update tracker stats after every change
- Follow CLAUDE.md writing style rules (no em-dashes, no colons in prose)

## Never

- Run without checking for config first
- Hardcode personal data in responses (always pull from config)
- Skip the deliverable linking steps (today.md, Recent Work MOC)
- Skip the activity log step
- Create duplicate tracker entries for the same job URL
- Edit AI Advisor folders
