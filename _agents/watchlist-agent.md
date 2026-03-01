# Job Sniper - Watchlist Agent (Background)

**Purpose**: Headless background agent that checks watched companies for new job postings and verifies active applications are still live. Runs via `claude -p` on a schedule. Writes results to `_cache/watchlist-alerts.md` for the interactive `/job-sniper` skill to surface.

**Execution mode**: Non-interactive. No user prompts. Read config, do checks, write results, exit.

## Configuration Files (Read These First)

Read these files at the start of every run:

1. `_config/watchlist.md` - Companies to monitor (table with Company, Careers URL, Role Filter)
2. `_config/user-profile.md` - Target roles and titles (fallback filter when watchlist row has no Role Filter)
3. `_cache/watchlist-seen.md` - Previously seen postings (create if missing)
4. `job-tracker.md` - Active applications to pulse-check (skip pulse if missing)
5. `_cache/pulse-last-check.txt` - Timestamp of last pulse check (skip pulse if <24hrs)

## Execution Steps

### Step 0: Pre-flight Checks

1. Read `_config/watchlist.md`. Parse the "Watched Companies" table.
2. If the table has zero data rows (only the header row, or file is empty/missing), write this to `_cache/watchlist-alerts.md`:
   ```
   # Watchlist Alerts
   Last background check: [today's date] [current time]

   No companies in watchlist. Add companies to _config/watchlist.md to start monitoring.
   ```
   Print "Watchlist check complete: no companies configured." to stdout and **stop here**.
3. Read `_config/user-profile.md`. Extract target titles from the "Target Roles > Titles" section. These are the fallback filter for watchlist rows with no Role Filter.
4. Read `_cache/watchlist-seen.md` if it exists. Parse it into a lookup: company -> list of (title, URL) pairs. If the file doesn't exist, start with an empty lookup.

### Step 1: Watchlist Check

For each company row in the watchlist table:

1. **Fetch the careers page**: Use WebFetch on the Careers URL.
2. **If WebFetch fails** (timeout, 404, blocked, returns only HTML/CSS with no job listings):
   - Try WebSearch as fallback: search for `[company name] careers [role filter keywords] site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:boards.greenhouse.io OR site:jobs.jobvite.com`
   - If both fail, log this company under "Fetch Errors" and continue to the next company. Do not abort.
3. **Extract job listings**: From the fetched content, extract job titles and URLs. Look for patterns like job title + application link.
4. **Apply the role filter**:
   - If the watchlist row has Role Filter keywords: match titles containing any of the comma-separated keywords (case-insensitive, partial match OK)
   - If the Role Filter is blank: match against the target titles from user-profile.md (case-insensitive, partial match OK)
5. **Diff against seen cache**: Compare matched postings against `_cache/watchlist-seen.md` for this company. A posting is NEW if its URL is not in the seen cache for this company.
6. **Collect results**: Track new matches and all current postings separately.

After processing all companies:

7. **Write seen cache**: Write ALL current postings (new and previously seen) to `_cache/watchlist-seen.md` using this format:
   ```markdown
   # Watchlist Cache
   Last checked: YYYY-MM-DD

   ## [Company Name]
   - [Job Title] | [URL] | first seen YYYY-MM-DD

   ## [Company Name]
   - [Job Title] | [URL] | first seen YYYY-MM-DD
   ```
   Preserve the "first seen" date for postings that were already in the cache. Use today's date for newly discovered postings.

**Pacing**: If processing more than 10 companies, add a 2-second pause between fetches to avoid rate limiting.

### Step 2: Application Pulse Check

1. Read `job-tracker.md`. Find all rows with Status containing "Researched", "Applied", or "Outreach Sent".
2. If no active applications exist, skip this entire step.
3. Read `_cache/pulse-last-check.txt` if it exists. If the timestamp is less than 24 hours ago, skip this step.
4. For each active application:
   - Extract the URL from the tracker row
   - Use WebFetch to check the URL
   - Determine if the posting appears removed:
     - HTTP 404 or error = likely removed
     - Redirects to a generic careers page (not the specific posting) = likely removed
     - Page contains "position has been filled", "no longer accepting", "this job is closed" = likely removed
     - Page loads with the job details visible = still live
   - Record the result
5. Write the current timestamp to `_cache/pulse-last-check.txt` (format: `YYYY-MM-DD HH:MM`).

### Step 3: Write Alert File

Write `_cache/watchlist-alerts.md` with this exact structure:

```markdown
# Watchlist Alerts
Last background check: YYYY-MM-DD HH:MM

## New Roles Found

### [Company Name]
- [Job Title] | [URL] | found YYYY-MM-DD
- [Job Title] | [URL] | found YYYY-MM-DD

### [Company Name]
- [Job Title] | [URL] | found YYYY-MM-DD

## Pulse Check

- [Company] - [Role]: posting appears removed (status was "[Status]", last contact [date])
- [Company] - [Role]: still live

## Fetch Errors

- [Company]: could not fetch careers page ([reason])

## Summary

New roles: X
Pulse alerts: Y
Fetch errors: Z
```

**Rules for the alert file:**
- If a section has no items, include the header but write "None" underneath
- Always include the Summary section
- Overwrite the previous alert file (the `/job-sniper` skill archives it before the next background run)

### Step 4: Summary

Print a one-line summary to stdout:
```
Watchlist check complete: X new roles found, Y pulse alerts, Z fetch errors. See _cache/watchlist-alerts.md
```

## Safety Rules

- **Read-only for config**: Never modify `_config/watchlist.md`, `_config/user-profile.md`, `_config/user-preferences.md`, or `job-tracker.md`
- **Write only to `_cache/`**: Only files this agent writes are `_cache/watchlist-alerts.md`, `_cache/watchlist-seen.md`, and `_cache/pulse-last-check.txt`
- **Idempotent**: Safe to run multiple times per day. The seen cache tracks what's been found, the alert file overwrites each run.
- **Fail gracefully**: Network errors on individual companies don't abort the run. Log the error and continue.
- **No user interaction**: This runs headlessly. Never ask questions or wait for input.
- **Minimal output**: Keep stdout to the one-line summary. Detailed results go in the alert file.

## Date Format

Use YYYY-MM-DD for all dates. Use YYYY-MM-DD HH:MM (24-hour) for timestamps.

**BEGIN EXECUTION NOW**
