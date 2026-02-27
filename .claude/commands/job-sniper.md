---
name: job-sniper
description: Job search tool that treats every application like a sales process. Handles first-time setup, config check, and all research modes (interactive, main, batch, multi-job). Invoke with /job-sniper [url or mode].
---

# Job Sniper

A job search tool that treats every application like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently. Auto-detects first-time vs returning user and routes accordingly.

## Key Paths (Relative to Repo Root)

- **Config:** `_config/user-profile.md`
- **Config example:** `_config/user-profile.example.md`
- **Preferences:** `_config/user-preferences.md`
- **Agent prompts:** `_agents/job-search/`
- **Setup agent:** `_agents/setup.md`
- **Templates:** `_templates/`
- **Activity log:** `job-tracker.md`
- **Model guide:** `MODEL-GUIDE.md`

## On Invocation

**Step 1: Check if configured**

Read `_config/user-profile.md` in the repo root.

- If it **does not exist** or contains only placeholder values like `{add value}` → go to **First-Time Setup**
- If it **exists and is populated** → go to **Mode Selection**

---

## First-Time Setup

### 1. Prerequisites Check

Verify these and report status:

```
Checking prerequisites...

[✓/✗] Config files exist (_config/user-profile.md)
[✓/✗] Resume found in _templates/resumes/
[✓/✗] Cover letter style guide (_templates/cover-letter-style-guide.md)
[✓/✗] LinkedIn contacts CSV (_templates/linkedin-contacts.csv)
```

For missing items:

- **Config missing:** This is expected for first-time users. The setup interview will create it.
- **Resume missing:** Ask the user where their resume is on disk. Search `~/Documents/`, `~/Desktop/`, `~/Downloads/` for PDF files with "resume" in the name. Offer to copy to `_templates/resumes/`.
- **Style guide missing:** Not critical. The agents use reasonable defaults without it.
- **LinkedIn CSV missing:** Optional. Explain how to export: LinkedIn Settings > Data Privacy > Get a copy of your data > Connections. The agents still work without it (just skip network analysis).

### 2. Run Setup Interview

Read `_agents/setup.md` and execute the setup interview. This collects:

- Resume (extracts profile data automatically)
- Multiple resumes if they have them (different role types)
- Additional context (cover letters as writing samples, 30/60/90 plans, portfolio)
- Target roles, compensation, location
- Writing style (extracted from cover letter sample, or asked if none provided)
- Output preferences

The setup agent generates:
- `_config/user-profile.md`
- `_config/user-preferences.md`

### 3. Initialize Activity Log

Create `job-tracker.md` if it doesn't exist (see **Activity Log** section below for format).

### 4. Confirm and Continue

After config files are created:

```
Setup complete! Your config is saved:
→ _config/user-profile.md (your profile and targets)
→ _config/user-preferences.md (writing style and preferences)
→ job-tracker.md (activity log, tracks every application)

These files are gitignored (your personal data stays local).
You can edit them anytime. The agents read them fresh each run.

Ready to run your first job search. Paste a job URL or pick a mode:
- interactive - Answer questions, get full research package
- batch - Process up to 5 job URLs at once
- multi-job - Compare multiple roles at the same company
```

Then go to **Mode Selection**.

---

## Mode Selection

Parse the invocation argument:

**If a URL was passed** (e.g., `/job-sniper https://jobs.lever.co/...`):
→ Go directly to **Interactive Mode** with that URL

**If a mode keyword was passed** (e.g., `/job-sniper batch`):
→ Go to that mode

**If "tracker" or "log" was passed** (e.g., `/job-sniper tracker`):
→ Show the current activity log (read and display `job-tracker.md`)

**If no argument or just `/job-sniper`:**

Present the mode picker:

```
Job Sniper ready. What are we doing?

1. interactive - Paste a job URL, answer a few questions, get the full package
2. main - Fill in structured inputs, get deep research (best for dream jobs)
3. batch - Process up to 5 URLs at once (quick depth, high volume)
4. multi-job - Compare 2-5 roles at the same company
5. tracker - View your activity log

Paste a URL to jump straight in, or pick a mode (1-5):
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

### Main Mode

1. Read `_agents/job-search/main.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Collect the structured USER INPUTS block:
   - JOB_URL
   - COMPANY_NAME
   - RESEARCH_DEPTH
   - ROLE_TYPE
   - YOUR_PRIORITY
4. Execute the full agent workflow
5. Save outputs, log to tracker
6. Prompt for similar roles → **Similar Role Discovery**

### Batch Mode

1. Read `_agents/job-search/batch.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask user to paste 1-5 job URLs (one per line)
4. Process each URL at Quick depth
5. Save outputs, log each to tracker
6. After all URLs processed, prompt for similar roles → **Similar Role Discovery**

### Multi-Job Mode

1. Read `_agents/job-search/multi-job.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask for company name and 2-5 job URLs
4. Execute comparative analysis
5. Save outputs, log each to tracker

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

Maintain `job-tracker.md` in the repo root as a running log of all job search activity. This file is gitignored (personal data).

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

## Model Recommendations

Reference `MODEL-GUIDE.md` for full details. Quick summary:

| Task | Model | Why |
|------|-------|-----|
| Web scraping, data extraction | Haiku | Fast, cheap, good at structured extraction |
| Company analysis, fit scoring | Sonnet | Strong reasoning, good cost/quality balance |
| Cover letters, strategic positioning | Sonnet | Best default for writing quality |
| 30/60/90 plans, deep strategy | Opus | Worth the cost for dream jobs |

Default to Sonnet unless the user specifies otherwise or picks Deep research depth.

---

## Always

- Read config files fresh every run (user may have updated them)
- Save research outputs to the path in user-profile.md
- Log every research run to `job-tracker.md`
- Prompt for similar roles after research completes
- Update tracker stats after every change

## Never

- Run without checking for config first
- Hardcode personal data in responses (always pull from config)
- Create duplicate tracker entries for the same job URL
- Skip the activity log step
