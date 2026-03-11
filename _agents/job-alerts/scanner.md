# Job Sniper Alert Scanner

Purpose: scan Gmail for job alert emails, extract new job postings, score them against the configured profile, write a daily digest, and notify Andy about Tier 1 matches.

Run headlessly. Do not ask follow-up questions. If a dependency is missing, log it clearly in the final summary.

## Files to read first

1. `_config/user-profile.md`
2. `_config/user-preferences.md`
3. `_config/alert-sources.md`
4. `_config/scoring-weights.yaml`
5. `_cache/seen-jobs.jsonl` if present
6. `ARCHITECTURE-JOB-DISCOVERY.md`

## Objective

Find new job postings from Gmail alert emails in the last 3 days. Score them. Write a digest markdown file to the configured output path. For Tier 1 jobs (score >= 80 and passed filters), send a concise alert to Andy in Telegram and surface a macOS notification when the wrapper script is later extended to do so.

## Execution steps

### 1. Load config

Extract from `_config/user-profile.md`:
- candidate name
- primary Gmail account for alerts
- notification target
- notification chat id
- output digest path

Extract from `_config/user-preferences.md`:
- fit scoring thresholds if specified

### 2. Search Gmail

Use the available Gmail / Google Workspace tooling to search for messages matching each query in `_config/alert-sources.md` from the last 3 days.

For each source:
- run the Gmail search query
- collect up to 20 recent matching messages
- fetch full message content for each result
- gather sender, subject, date, and body text

If Gmail tooling is unavailable or auth fails, stop and report that clearly.

### 3. Parse emails into jobs

Write the collected emails to `/tmp/job-sniper-emails.json` as JSON array objects with:
- `sender`
- `subject`
- `body`
- `date`

Then run:

```bash
cd /Users/openclaw/Documents/Coding/job-sniper && source .venv/bin/activate && python3 -c "
import json
from src.email_scanner import parse_email

emails = json.load(open('/tmp/job-sniper-emails.json'))
all_jobs = []
for e in emails:
    jobs = parse_email(e['sender'], e['body'], e['date'], e.get('subject', ''))
    for j in jobs:
        all_jobs.append(j.to_dict())
print(json.dumps(all_jobs))
" | python3 run-discovery.py score-emails
```

### 4. Read scoring results

Parse the JSON output from `score-emails`.

Calculate:
- emails scanned
- new jobs found
- jobs scored
- qualified jobs (passed filters and score >= 50)
- tier 1 jobs (score >= 80)
- hot jobs (score >= 95)

### 5. Write daily digest

Write a markdown digest to the output path from `_config/user-profile.md` using filename:
`YYYY-MM-DD-job-alerts.md`

Structure:

```markdown
# Job Alerts Digest
Date: YYYY-MM-DD

## Summary
- Emails scanned: X
- New jobs found: Y
- Qualified jobs: Z
- Tier 1 jobs: T
- Hot jobs: H

## Tier 1
- Company | Title | Score | URL

## Tier 2
- Company | Title | Score | URL

## Tier 3
- Company | Title | Score | URL

## Filtered Out
- Company | Title | Reason
```

If a section has no items, write `None`.

### 6. Notify Andy for Tier 1 matches

For each Tier 1 job, send a concise Telegram message using OpenClaw messaging. Include:
- company
- title
- score
- URL if available
- one-line recommendation like `Worth immediate review`

Keep it short, one message per match is fine if there are few matches. If there are many, batch them into a single summary.

### 7. Final stdout summary

Print a short machine-friendly summary:

```text
Job alert scan complete: emails=X new_jobs=Y qualified=Z tier1=T hot=H digest=PATH
```

## Safety and behavior rules

- Do not edit `_config/user-profile.md` or `_config/user-preferences.md`
- Only write to `_cache/`, `/tmp/`, and the configured digest output path
- Do not send notifications for jobs below Tier 1
- Deduplicate via the Python storage layer, not by hand
- If Gmail search returns nothing, still write the digest with zero counts
- If one source fails, continue with the others and note the failure in the digest

BEGIN NOW
