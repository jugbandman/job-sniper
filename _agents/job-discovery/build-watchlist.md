# Job Sniper - Build Watchlist Agent

**Purpose**: Research-driven watchlist expansion. Analyzes your background and current watchlist, then finds competitor companies, adjacent markets, and unconventional role titles you might be missing. Updates `_config/company-watchlist.yaml` with new targets.

**Execution mode**: Interactive. May ask clarifying questions. Writes to config at the end.

## Configuration Files (Read These First)

1. `_config/user-profile.md` - Your background, target roles, industries, experience
2. `_config/company-watchlist.yaml` - Current watchlist (create from `company-watchlist.example.yaml` if missing)
3. Job Search AI Advisor persona (if present): `~/Documents/Obsidian Vault/80-Projects/job-search/Job Search, AI Advisor/Job Search, Project Persona (Job Seeker).md`

## Execution Steps

### Step 1: Read profile and current watchlist

Read `~/Documents/Coding/job-sniper/_config/user-profile.md`.

Extract:
- Past employers and industries
- Target role titles
- Location preference
- Compensation target

Read `~/Documents/Coding/job-sniper/_config/company-watchlist.yaml` (or the example if it doesn't exist yet). Note how many companies are in each tier.

Also read the Obsidian job search persona if available (see path above).

### Step 2: Analyze past employers, generate competitors

From the profile, identify past employers and their industries.

For each past employer, use web search to find competitors:

```
WebSearch: "{company_name}" competitors B2B SaaS leadership
```

Also search for companies hiring in the same space:

```
WebSearch: "{industry}" companies hiring "VP Sales" OR "Director of Sales" 2026
```

Collect company names, industry, estimated stage, and careers URL.

### Step 3: Build tiered additions

Classify each company you found into a tier:

**Tier 1 (Direct fit):** Companies in Andy's exact industries with history of hiring senior sales and GTM roles. Stage typically Series B-D or late-stage. Technical buyer or technical product.

**Tier 2 (Adjacent):** Companies in adjacent markets (e.g., adjacent SaaS category, related buyer persona) that value the same GTM skillset. May be different product but similar sales motion.

**Tier 3 (Aspirational):** Top-tier companies worth watching even if a slot isn't open now. Proven PMF, strong growth, great reputation for GTM leaders.

For each company found:
- Verify a careers page exists (WebFetch if unsure)
- Note the company stage if findable
- Note employee count if findable
- Mark it as "new" vs "already in watchlist"

### Step 4: Edge searches for unconventional titles

Search for roles that match the profile's skills but use different titles:

```
WebSearch: "Revenue Operations Director" OR "Head of RevOps" site:linkedin.com/jobs remote OR Denver 2026
```

```
WebSearch: "GTM Strategy" OR "Head of GTM" site:lever.co OR site:greenhouse.io 2026
```

```
WebSearch: "Commercial Strategy" OR "Head of Growth" B2B SaaS 2026
```

Collect any job postings that seem like strong matches. Extract company name and note the unconventional title pattern.

Add new companies surfaced by edge searches to the appropriate tier.

Also define the unconventional title patterns as `edge_searches` in the config (see format below) so the alert scanner can watch for them.

### Step 5: Present findings and confirm

Before writing anything, present a summary:

```
Watchlist Expansion Analysis
---
Current watchlist: X companies (T1: A, T2: B, T3: C)

Proposed additions:
- Tier 1: [Company A (Series C, 400 employees, dev tools)] [NEW]
- Tier 1: [Company B (Series B, 150 employees, AI infra)] [NEW]
- Tier 2: [Company C (Series D, 1200 employees, analytics)] [NEW]
...

Unconventional titles to watch:
- "RevOps Director" - strategic ops with sales leadership background
- "Head of GTM Strategy" - full-cycle enterprise, cross-functional

Companies already in watchlist (skipping):
- Atlassian, Databricks, ...

Total new additions: N
```

Ask: "Want me to update the watchlist with these additions? You can also tell me to skip specific companies or change their tier."

### Step 6: Write updated watchlist

After confirmation, write the updated watchlist to `~/Documents/Coding/job-sniper/_config/company-watchlist.yaml`.

Format for each tier:

```yaml
tier_1_direct:
  - name: CompanyName
    careers_url: https://company.com/careers
    industry: Category / Subcategory
    priority: high

tier_2_adjacent:
  - name: CompanyName
    careers_url: https://company.com/careers
    industry: Category
    priority: medium

tier_3_great:
  - name: CompanyName
    careers_url: https://company.com/careers
    industry: Category
    priority: low

# Unconventional title patterns to watch in alert scanning
edge_searches:
  - title_pattern: "RevOps Director"
    why: Strategic revenue operations, maps to senior sales leadership background
  - title_pattern: "Head of GTM Strategy"
    why: Full-cycle enterprise GTM, cross-functional execution
```

Preserve any existing companies already in the watchlist. Only append new ones.

### Step 7: Print final summary

```
Watchlist Updated
---
Tier 1: X companies (Y new)
Tier 2: X companies (Y new)
Tier 3: X companies (Y new)
Edge titles: N patterns defined

New additions:
- CompanyA (Tier 1, Series B, 300 employees, dev tools)
- CompanyB (Tier 2, Series C, 1200 employees, analytics)
...

Config saved to: ~/Documents/Coding/job-sniper/_config/company-watchlist.yaml

Next: Run /job-sniper alerts run to start scanning for new postings from these companies.
```

## Safety Rules

- **Config file only**: Only write to `_config/company-watchlist.yaml`. Never modify `user-profile.md`, `user-preferences.md`, or agent prompts.
- **Confirm before writing**: Always show the proposed additions and ask for confirmation before updating the file.
- **Preserve existing entries**: Never remove companies that are already in the watchlist. Only add new ones.
- **No personal data in config**: The watchlist is committed to git. Never add personal notes, application status, or private info to this file.

## Date Format

Use YYYY-MM-DD for all dates.
