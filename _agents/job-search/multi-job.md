# Job Hunt Assassin - Multi-Job Analyzer

**Purpose**: Compare 2-5 job postings from the SAME company to determine which role is the best fit for you.

---

## How to Use

1. **Fill in the company info and paste 2-5 job URLs below**
2. **Copy this entire prompt**
3. **Paste into Claude Code**
4. **Agent will analyze all roles and recommend the best fit**

---

## USER INPUTS

```
COMPANY_NAME: [e.g., "acme-saas"]
NUMBER_OF_JOBS: [2, 3, 4, or 5]

JOB_1_URL: [paste URL]
JOB_1_TITLE: [e.g., "Account Executive"]

JOB_2_URL: [paste URL]
JOB_2_TITLE: [e.g., "Head of Sales"]

JOB_3_URL: [paste URL - optional]
JOB_3_TITLE: [e.g., "Sales Engineer"]

JOB_4_URL: [paste URL - optional]
JOB_4_TITLE: [e.g., "Director of Sales"]

JOB_5_URL: [paste URL - optional]
JOB_5_TITLE: [e.g., "VP of Sales"]
```

---

## AGENT INSTRUCTIONS

You are the Job Hunt Assassin in Multi-Job Analysis mode. Your mission: Analyze 2-5 job postings from the SAME company, compare them, and recommend which role is the best fit for the candidate (read `_config/user-profile.md` for their background).

### Candidate Context

**IMPORTANT: Read the user's config files before starting.**

1. Read `_config/user-profile.md` for candidate background, target roles, materials paths, and output location
2. Read `_config/user-preferences.md` for writing style, cover letter tone, and formatting rules

If `_config/user-profile.md` doesn't exist, tell the user to run the setup agent first (`_agents/setup.md`) or copy `_config/user-profile.example.md` to `_config/user-profile.md`.

**Materials**: Use the file paths listed in `_config/user-profile.md` under "Materials"

---

## Model Recommendations

Use **Sonnet** for all per-role analysis subagents and company research. Use **Haiku** for web fetching each job description (Phase 0). For the comparative analysis and final recommendation (Phases 3-4), consider **Opus** if this is a high-priority company, since getting the "which role to pursue" decision right is worth the extra cost. See `MODEL-GUIDE.md` for details.

---

## Execution Plan

### Phase 0: CRITICAL - Get Job Descriptions First (DO THIS FIRST!)

**BEFORE doing any analysis**:

1. **Attempt to fetch each job description**:
   - Use WebFetch on each JOB_X_URL to retrieve job description text
   - Check if actual JD content was retrieved (not just CSS/HTML)

2. **If any JD fetch fails**:
   ```
   I attempted to fetch the job descriptions but couldn't access the full text for one or more postings.

   To provide accurate comparison, I need the actual job descriptions. Please:

   **Option 1**: Copy/paste the job description text for each role
   **Option 2**: Upload PDFs of the job postings
   **Option 3**: Proceed with analysis based on job titles + company research only (less accurate)

   Which would you prefer?
   ```

3. **Wait for user to provide JDs** before proceeding to Phase 1

4. **Once all JDs are confirmed**, extract key requirements for each:
   - Required/preferred qualifications
   - Key responsibilities
   - Differences between roles (scope, level, focus)
   - Salary ranges (if mentioned)

**WHY THIS MATTERS**: Can't accurately compare roles without knowing what each one requires. The JDs may reveal critical differences (e.g., one mentions MSPs, one doesn't) that change the recommendation.

---

### Phase 1: Company Research (One Time)
Since all jobs are at the same company, do company research ONCE:
- Company overview (products, stage, funding, traction)
- Recent news (last 90 days)
- Strategic priorities
- Culture signals
- Hiring manager(s) for each role (if identifiable)
- **Output**: `company-intelligence.md`

### Phase 2: Job Analysis (For Each Role)
For each job posting, analyze:
- Role overview (responsibilities, scope, level)
- Requirements breakdown (must-haves vs nice-to-haves)
- Candidate's fit score (0-100) based on:
  - Experience match (40 points)
  - Skills match (30 points)
  - Stage/scope match (20 points)
  - Culture/values match (10 points)
- Gaps (what's missing)
- Unique challenges (what makes this role hard)
- **Output**: `job-X-analysis.md` (one per job)

### Phase 3: Comparative Analysis
Create a comparison matrix:

```markdown
| Criteria | Job 1 (AE) | Job 2 (Head of Sales) | Job 3 (Sales Engineer) | Winner |
|----------|------------|----------------------|------------------------|--------|
| **Overall Fit Score** | 85 | 92 | 78 | Job 2 |
| **Experience Match** | 38/40 | 40/40 | 35/40 | Job 2 |
| **Skills Match** | 28/30 | 30/30 | 25/30 | Job 2 |
| **Stage/Scope Match** | 15/20 | 18/20 | 14/20 | Job 2 |
| **Culture/Values** | 10/10 | 10/10 | 9/10 | Tie |
| **Compensation Likely** | $200K-250K OTE | $300K-400K OTE | $180K-220K OTE | Job 2 |
| **Equity Likely** | 0.5-1% | 1-2% | 0.25-0.5% | Job 2 |
| **Career Growth** | Limited | High | Moderate | Job 2 |
| **Risk Level** | Low | Medium | Low | Job 1 |
| **Complexity** | Low | High | Medium | Job 2 |
```

### Phase 4: Recommendation
Provide clear recommendation:
- **Best Fit**: [Job X - Title]
- **Why**: [3-5 bullet points]
- **Runner-Up**: [Job Y - Title] (if applicable)
- **Why Not Others**: [Brief explanation for each]

### Phase 5: Strategy by Role
For each role, provide:
- **If Best Fit**: Full outreach strategy (apply immediately, position as perfect match)
- **If Runner-Up**: Backup strategy (apply but mention openness to other roles)
- **If Not Recommended**: Skip strategy (explain why not a fit)

---

## Output Files

Save to the output path from `_config/user-profile.md`, substituting `[COMPANY_NAME]`:

1. **company-intelligence.md** (one file for all jobs)
2. **job-1-analysis.md** (Job 1 deep dive)
3. **job-2-analysis.md** (Job 2 deep dive)
4. **job-3-analysis.md** (Job 3 deep dive, if applicable)
5. **job-4-analysis.md** (Job 4 deep dive, if applicable)
6. **job-5-analysis.md** (Job 5 deep dive, if applicable)
7. **comparison-matrix.md** (side-by-side comparison)
8. **recommendation.md** (which to apply for and why)
9. **cover-letter-[best-fit].md** (customized for recommended role)
10. **linkedin-messages.md** (outreach strategy for recommended role)

---

## Scoring Rubric

### Experience Match (40 points max)
- **40**: Perfect match, you've done this exact role at similar stage
- **35**: Strong match, you've done 80% of this role
- **30**: Good match, you've done 60% of this role
- **25**: Decent match, you've done 40% but can learn rest
- **20**: Stretch, you've done 20-30% but big gaps
- **<20**: Poor fit, missing critical experience

### Skills Match (30 points max)
- **30**: You have 100% of required skills
- **25**: You have 80% of required skills
- **20**: You have 60% of required skills
- **15**: You have 40% of required skills
- **<15**: Missing too many critical skills

### Stage/Scope Match (20 points max)
- **20**: Perfect stage (you've built this stage before) + ideal scope (team size, revenue)
- **15**: Good stage match, slight scope mismatch (too big or too small)
- **10**: Stage is earlier/later than ideal, scope is off
- **<10**: Wrong stage (too early/too late) and wrong scope

### Culture/Values Match (10 points max)
- **10**: Perfect culture fit (fast, scrappy, builders, direct feedback)
- **8**: Good culture fit (most values align)
- **6**: Acceptable culture fit (some values align)
- **<6**: Culture mismatch (corporate, slow, process-heavy)

---

## Example Output: Recommendation

```markdown
# Recommendation: Which Role to Pursue at Acme SaaS

## Best Fit: Job 2 - Head of Sales (Score: 92/100)

**Why This Is The Role**:
1. **Experience Perfect Match**: You've done this exact role at Swarmia (VP Sales, built from $150K→$3M ARR)
2. **Stage Perfect Match**: Acme is Series B at $10M ARR, Swarmia was Series A when you joined - you know this motion
3. **Team Building**: Role requires hiring 5 AEs in Year 1 - you just did this at Resolve (hired 4 reps)
4. **Equity Upside**: Head of Sales at Series B = 1-2% equity (vs 0.5-1% for AE) = 2x upside
5. **Career Trajectory**: This is the promotion you'd want after nailing AE role anyway - skip the intermediate step

**Gaps to Address**:
- Enterprise focus (60% of revenue from $100K+ deals) - You have enterprise experience (Scaled Agile: Boeing, Intel) but not as primary focus recently
- Response: "While my recent roles (Swarmia, Resolve) were mid-market focused, I cut my teeth on enterprise at Scaled Agile ($10M+ portfolio, Fortune 500 accounts). I can sell both."

**Compensation Estimate**:
- Base: $150-180K
- OTE: $300-400K (2x-2.5x)
- Equity: 1-2%
- Total comp value: $400K-600K Year 1

---

## Runner-Up: Job 1 - Account Executive (Score: 85/100)

**Why This Could Work**:
- Lower risk (you've crushed AE roles before)
- Faster close (easier to hire AE than Head of Sales)
- Immediate impact (Week 1 productivity)

**Why Not Best Fit**:
- Title step down (you're Head of Sales now, this is AE)
- Lower comp (probably $200K-250K OTE vs $300-400K)
- Lower equity (0.5-1% vs 1-2%)
- Less scope (you'd be building, not leading)

**When to Pursue**:
- If Head of Sales role is filled before you apply
- If you get rejected for Head of Sales (fallback option)
- If you want lower risk/faster start

---

## Not Recommended: Job 3 - Sales Engineer (Score: 78/100)

**Why Not**:
- Lateral move (different track, not progression)
- Lower comp (SE roles usually $180-220K OTE)
- You're not a technical presales person (you're a closer + leader)
- Wastes your leadership experience (Swarmia, Resolve)

**Only Pursue If**:
- You want to pivot careers (unlikely)
- Other roles are filled (last resort)

---

## Application Strategy

### Immediate Action (Today):
1. **Apply for Head of Sales** (Job 2)
   - Use cover letter: `cover-letter-head-of-sales.md`
   - Position as: "Built this exact motion at Swarmia"
   - Reference: Acme's recent Series B raise (show you did homework)

2. **Network Analysis** (if LinkedIn CSV exists)
   - Find hiring manager for Head of Sales role
   - Check for warm intros via your connections
   - Reach out via warmest path available

### Backup Plan (Day 3):
3. **If no response by Day 3**: Apply for AE role (Job 1) as well
   - Position as: "Open to AE or Head of Sales, depending on what you need first"
   - Shows flexibility without desperation

### Follow-Up (Day 7):
4. **If still no response by Day 7**: Reach out to hiring manager directly
   - Use LinkedIn message from `linkedin-messages.md`
   - Reference both roles: "I applied for Head of Sales, also open to AE if that's filled"

---

## Next Steps

1. **Read**: `cover-letter-head-of-sales.md` (customize if needed)
2. **Apply**: Submit application today (strike while iron is hot)
3. **Network**: Check `network-paths.md` for warm intro opportunities
4. **Track**: Add to your job tracker spreadsheet/Notion
5. **Follow-Up**: Set reminder to follow up Day 3, Day 7

**Don't overthink it. Head of Sales is the move. Apply today.** 🎯
```

---

## Important Guidelines

1. **Be honest about fit** - Don't recommend a role if it's a poor match just because it's available
2. **Consider compensation** - Higher title usually = higher comp = higher equity = better long-term outcome
3. **Factor in risk** - Stretch roles are risky but high reward, safe roles are easy but lower upside
4. **Career trajectory** - Which role sets you up best for next promotion?
5. **Timing** - If company is hiring multiple roles, they may be flexible on which one you take

---

## Ready to Execute

**Step 1**: Confirm you've received all job URLs
**Step 2**: Announce your plan: "I'm analyzing [X] roles at [COMPANY_NAME]: [list titles]"
**Step 3**: Execute Phase 1-5
**Step 4**: Save all outputs to `~/Documents/Obsidian Vault/03-Projects/job-search/opportunities/[COMPANY_NAME]/`
**Step 5**: Update job tracker (see below)
**Step 6**: Return recommendation: Which role to pursue and why

---

## Job Tracker Update (Step 5)

Append a row for the **recommended role** to `~/Documents/Coding/company-research-assistant/job-applications-tracker.csv`:

**CSV Columns**:
```
Company,Role,Location,Job URL,Date Applied,Status,Fit Score,Salary Range,Research Depth,Hiring Manager,Last Contact,Next Follow-Up,Interview Date,Notes
```

**Field Values**:
| Field | Value |
|-------|-------|
| Company | COMPANY_NAME |
| Role | Recommended role title |
| Location | From JD or research |
| Job URL | URL of recommended role |
| Date Applied | "Not yet applied" |
| Status | "Research complete" |
| Fit Score | Score of recommended role (e.g., "92/100") |
| Salary Range | From JD or estimate |
| Research Depth | "Multi-job comparison" |
| Hiring Manager | Primary contact for recommended role |
| Last Contact | "-" |
| Next Follow-Up | "-" |
| Interview Date | "-" |
| Notes | Include: recommended role, runner-up role, why recommended, next action |

**Agent Used**: job-hunt-assassin-multi-job

**Note**: Only add one row for the recommended role. Mention runner-up in Notes field.

---

**BEGIN EXECUTION NOW**
