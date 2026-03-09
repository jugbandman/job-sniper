# Job Sniper - Response Watch Agent (Background)

**Purpose**: Headless background agent that scans Gmail for replies from companies in your active pipeline. Detects recruiter responses, scheduling requests, and rejections. Sends a Slack DM for any match found. Runs via `claude -p` on a schedule.

**Execution mode**: Non-interactive. No user prompts. Read config, scan Gmail, report matches, exit.

## Gmail Account

**Always use `andrewdcarlson@gmail.com`** as the `user_google_email` for all Gmail MCP calls in this agent. Company response emails go to the personal account.

## Configuration Files (Read These First)

1. `_config/user-profile.md` - Your profile (fallback for extracting company names)
2. `job-tracker.md` - Active applications (companies to watch for replies)
3. `_cache/seen-jobs.jsonl` - All tracked companies from scoring runs

## Execution Steps

### Step 1: Build tracked company list

Pull active company names from two sources:

**Source A - job-tracker.md:**

Read `~/Documents/Coding/job-sniper/job-tracker.md`. Find all rows with Status containing "Researched", "Applied", "Outreach Sent", or "Interview". Extract the Company column from each row.

**Source B - Obsidian job-search folders:**

Check these folders for company names (extract company from folder name, e.g., "docker-strategic-ae" becomes "Docker"):

```bash
ls ~/Documents/Obsidian\ Vault/80-Projects/job-search/applying/ 2>/dev/null
ls ~/Documents/Obsidian\ Vault/80-Projects/job-search/interviewing/ 2>/dev/null
```

**Source C - JSONL scored jobs cache:**

```bash
cd ~/Documents/Coding/job-sniper && python3 -c "
from src.storage import Storage
s = Storage()
jobs = s.load_jobs()
companies = set(j.get('company', '') for j in jobs if j.get('company'))
for c in sorted(companies):
    print(c)
" 2>/dev/null
```

Merge all three sources into a deduplicated list of company names.

### Step 2: Derive company email domains

For each company name, derive likely email domains:
- "Docker" becomes "docker.com"
- "Acme Corp" becomes "acmecorp.com" and "acme.com"
- Try common patterns: `{company-lowercase}.com`, `{company-lowercase}.io`, `{company-lowercase}.co`

Use the Python domain extractor if available:

```bash
cd ~/Documents/Coding/job-sniper && python3 -c "
from src.response_scanner import extract_company_domains
import json
companies = $(python3 -c "import sys; print(sys.argv[1])" '[LIST_OF_COMPANIES]')
domains = extract_company_domains(companies)
for d in domains:
    print(d)
" 2>/dev/null
```

If the Python module fails, derive domains manually from company names.

### Step 3: Search Gmail for replies (last 24 hours)

Run two searches using `mcp__google-workspace__search_gmail_messages` with `user_google_email: andrewdcarlson@gmail.com`:

**Search 1 - Per-company domain searches:**

For each derived domain, search:
```
from:{domain} newer_than:1d
```
Run up to 10 company searches (pick the highest-priority companies from the tracker first).

**Search 2 - Broad subject search:**

Build a combined subject search across all tracked companies:
```
subject:({company1} OR {company2} OR ...) newer_than:1d -from:builtin.com -from:linkedin.com -from:welcometothejungle.com -from:jobalerts-noreply@linkedin.com
```

### Step 4: Classify each email found

For each email returned by either search, read the full content using `mcp__google-workspace__get_gmail_message_content`. Classify the email as one of:

- **Response - Interested** - Recruiter or hiring manager reaching out, scheduling a call, asking for more info
- **Response - Rejection** - Formal rejection, "not moving forward", "decided to go in a different direction"
- **Response - Auto-confirm** - Automated confirmation of application receipt (low signal, log but don't alert)
- **Not a match** - Email from that domain but unrelated to your job application

Skip any email that:
- Is from a job alert service (LinkedIn, BuiltIn, etc.)
- Is clearly automated marketing (unsubscribe links, promotional)
- Has no connection to a tracked company

### Step 5: Slack alert for matches

For each **Response - Interested** or **Response - Rejection** email found, send a Slack DM to Andy using `mcp__claude_ai_Slack__slack_send_message`:

**For interested responses:**
```
Response Watch: Reply from {Company}

{Sender name} ({sender email}) replied to your application for {role if known}.
Subject: {email subject}

Check your inbox or run /job-sniper to update your tracker.
```

**For rejections:**
```
Response Watch: Update from {Company}

It looks like {Company} sent a rejection notice.
Subject: {email subject}

Run /job-sniper tracker to update your status.
```

### Step 6: Print summary

```
Response Watch Complete
---
Companies tracked: X
Searches run: Y
Emails checked: Z
Responses found: R (X interested, Y rejections, Z auto-confirms)

[If responses found:]
- Company: Subject (From: sender) [Type]
  Slack alert sent.

[If no responses:]
No replies found from tracked companies in the last 24 hours.
```

## Safety Rules

- **Read-only for config**: Never modify `_config/user-profile.md`, `job-tracker.md`, or any config file
- **No email modifications**: Never send, delete, archive, or label any emails
- **No tracker updates**: Surface findings to Andy via Slack. Andy updates the tracker himself.
- **Fail gracefully**: If Python modules fail, fall back to manual domain derivation. If Slack send fails, log it but don't abort.
- **No user interaction**: This runs headlessly. Never ask questions or wait for input.

## Date Format

Use YYYY-MM-DD for all dates. Use YYYY-MM-DD HH:MM (24-hour) for timestamps.

**BEGIN EXECUTION NOW**
