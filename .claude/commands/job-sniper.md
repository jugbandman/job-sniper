---
name: job-sniper
description: Run the Company Research Assistant for job search. Handles first-time setup, config check, and all research modes (interactive, main, batch, multi-job). Invoke with /job-sniper [url or mode].
---

# Job Sniper

Run the Company Research Assistant for job search research and application generation. Auto-detects first-time vs returning user and routes accordingly.

## Key Paths (Relative to Repo Root)

- **Config:** `_config/user-profile.md`
- **Config example:** `_config/user-profile.example.md`
- **Preferences:** `_config/user-preferences.md`
- **Agent prompts:** `_agents/job-search/`
- **Setup agent:** `_agents/setup.md`
- **Templates:** `_templates/`
- **Job tracker:** `job-applications-tracker.csv`
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

- Basic info (name, email, location)
- Professional background (roles, metrics, strengths)
- Target roles (titles, company types, compensation)
- Materials paths (resume location, other docs)
- Output preferences (where to save research)
- Writing style (tone, length, pet peeves)

The setup agent generates:
- `_config/user-profile.md`
- `_config/user-preferences.md`

### 3. Confirm and Continue

After config files are created:

```
Setup complete! Your config is saved:
→ _config/user-profile.md (your profile and targets)
→ _config/user-preferences.md (writing style and preferences)

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

**If no argument or just `/job-sniper`:**

Present the mode picker:

```
Job Sniper ready. What are we doing?

1. interactive - Paste a job URL, answer a few questions, get the full package
2. main - Fill in structured inputs, get deep research (best for dream jobs)
3. batch - Process up to 5 URLs at once (quick depth, high volume)
4. multi-job - Compare 2-5 roles at the same company

Paste a URL to jump straight in, or pick a mode (1-4):
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
6. Update `job-applications-tracker.csv` with a new row

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
5. Save outputs, update tracker

### Batch Mode

1. Read `_agents/job-search/batch.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask user to paste 1-5 job URLs (one per line)
4. Process each URL at Quick depth
5. Save outputs, update tracker for each

### Multi-Job Mode

1. Read `_agents/job-search/multi-job.md`
2. Read `_config/user-profile.md` and `_config/user-preferences.md`
3. Ask for company name and 2-5 job URLs
4. Execute comparative analysis
5. Save outputs, update tracker

---

## After Every Run

Regardless of mode, always:

1. **Update job tracker:** Add row to `job-applications-tracker.csv`
2. **Show summary:** Display what files were created and where they were saved

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
- Update the job tracker CSV after every research run

## Never

- Run without checking for config first
- Hardcode personal data in responses (always pull from config)
- Create duplicate tracker entries for the same job URL
