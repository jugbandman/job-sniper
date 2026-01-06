# Job Hunt Assassin - Usage Guide

**Last Updated**: November 6, 2025

---

## What Is This?

The Job Hunt Assassin is an automated agent that researches companies, finds hiring managers, analyzes your network, and generates customized application materials. It treats job search like enterprise sales: research deeply, personalize heavily, multi-thread intelligently.

**Philosophy**: Don't be another resume in the pile. Be the candidate who understands the company better than their own employees.

---

## Quick Start (5 Minutes)

1. **Open** `/Users/andycarlson/job-search/_agents/job-hunt-assassin-main.md`
2. **Fill in** the USER INPUTS section:
   ```
   JOB_URL: https://jobs.ashbyhq.com/acmesaas/account-executive
   COMPANY_NAME: acme-saas
   RESEARCH_DEPTH: Standard
   ROLE_TYPE: AE
   YOUR_PRIORITY: equity + growth
   ```
3. **Copy** the entire prompt (from "AGENT INSTRUCTIONS" to end)
4. **Paste** into Claude Code or Claude.ai
5. **Wait** 30-45 minutes (agent runs automatically)
6. **Review** outputs in `~/job-search/acme-saas/`

---

## Research Depth Guide

### Quick (15-20 min) - Use for Most Applications
**When**: Decent fit, but not dream job. You're applying to 5+ roles this week.

**What You Get**:
- Company intelligence (overview, news, culture, red flags)
- Hiring manager identification
- Job analysis & fit matrix
- Positioning strategy & resume TLDR
- Custom cover letter
- LinkedIn outreach messages

**What You Don't Get**:
- Network path analysis
- 30/60/90 day plan
- Competitive intelligence
- Take-home research package

**Use Case**: "I'm applying to 10 AE roles. I need good-enough materials fast."

### Standard (30-45 min) - Use for Strong Matches
**When**: Great fit, company you're excited about. Top 20% of applications.

**Everything from Quick, plus**:
- Network path analysis (find warm intros via your LinkedIn connections)
- Deeper competitive intelligence
- Email sequence (follow-up cadence)
- More detailed positioning strategy

**Use Case**: "This role is a strong match. I want to maximize my chances."

### Deep (60+ min) - Use for Dream Jobs Only
**When**: Perfect fit, dream company. Top 5% of applications.

**Everything from Standard, plus**:
- 30/60/90 day plan (if sales/GTM role)
- Full competitive analysis with battlecards
- Interview prep package
- Take-home research package (to attach with application)
- STAR story mapping

**Use Case**: "This is THE role. I'm going all-in."

---

## Prerequisites

### Required (You Have These)
- ✅ Resume: `~/job-search/_templates/Andrew Carlson Resume 2025.pdf`
- ✅ Cover Letter Template: `~/job-search/_templates/About Andy Carlson Intro 2025.pdf`

### Optional (Enhances Output)
- ❓ LinkedIn Contacts CSV: `~/job-search/_templates/linkedin-contacts.csv`
  - Enables network path analysis (warm intro finding)
  - Export from LinkedIn: Settings → Data Privacy → Get a copy of your data → Connections
- ❓ Additional cover letter examples by role type (if you have different templates for AE vs VP Sales vs RevOps)

---

## How to Get LinkedIn Contacts CSV

1. Go to LinkedIn → **Me** → **Settings & Privacy**
2. **Data Privacy** → **Get a copy of your data**
3. Select **"Connections"** only (faster download)
4. **Request Archive** (takes ~10 minutes)
5. LinkedIn emails you a ZIP file
6. Extract `Connections.csv`
7. Save to `~/job-search/_templates/linkedin-contacts.csv`

**Format Expected**:
```csv
First Name,Last Name,Email Address,Company,Position,Connected On
John,Doe,john@example.com,Acme Corp,VP Sales,01 Jan 2023
...
```

---

## Output Structure

After running the agent, you'll have a folder like this:

```
~/job-search/acme-saas/
├── company-intelligence.md          # Company overview, news, culture
├── hiring-managers.md                # Who to contact, titles, LinkedIn
├── job-analysis-fit-matrix.md        # Requirements mapped to your experience
├── network-paths.md                  # Warm intro opportunities (if CSV exists)
├── positioning-strategy.md           # How to position yourself, key angles
├── cover-letter.md                   # Customized cover letter (ready to send)
├── linkedin-messages.md              # Messages to hiring manager, connections
├── email-sequence.md                 # Follow-up email templates
├── interview-prep.md                 # Questions to ask, STAR stories (if Deep)
├── 30-60-90-day-plan.md              # Execution plan (if Deep + sales role)
└── competitive-intelligence.md       # Market positioning (if Deep)
```

---

## What to Do with Outputs

### Immediate Actions (Day 0)
1. **Read `company-intelligence.md`** - Understand the company (5 min)
2. **Read `job-analysis-fit-matrix.md`** - Confirm you're a good fit (3 min)
3. **Review `cover-letter.md`** - Tweak if needed, then submit application (10 min)
4. **Check `network-paths.md`** - If warm intro exists, reach out to connection (5 min)

### Follow-Up Actions (Day 1-3)
5. **Use `linkedin-messages.md`** - Reach out to hiring manager or connections
6. **Use `email-sequence.md`** - If no response, follow up Day 3, Day 7

### Interview Prep (If You Get Interview)
7. **Review `company-intelligence.md`** again - Fresh intel before call
8. **Review `interview-prep.md`** - Questions to ask, STAR stories
9. **Use `30-60-90-day-plan.md`** - Present this in interview (if sales role)

---

## Tips for Success

### Do's ✅
- **Run Quick for most jobs** - Don't over-invest in long shots
- **Run Deep for dream jobs** - Top 5% get maximum effort
- **Customize outputs** - Agent gives you 80%, you add 20% personal touch
- **Act fast** - Research is perishable, apply within 24 hours
- **Use network paths** - Warm intros convert 5-10x better than cold applications
- **Follow up** - Use email sequence if no response in 3 days

### Don'ts ❌
- **Don't skip reading outputs** - Agent did research, you need to internalize it
- **Don't copy/paste blindly** - Review cover letter, tweak to your voice
- **Don't apply to jobs you're not qualified for** - Agent can't fix poor fit
- **Don't ignore red flags** - If company-intelligence.md shows problems, reconsider
- **Don't send generic LinkedIn messages** - Use the agent's custom messages

---

## Troubleshooting

### Agent Doesn't Find Hiring Manager
**Why**: Job description doesn't mention name, company is stealth, LinkedIn private
**Fix**:
- Check company website Team/About page
- Search "[Company] [role] hiring" on X/Twitter
- Check LinkedIn job posting (sometimes hiring manager comments)
- If still can't find: Apply anyway, agent will generate generic outreach

### Network Path Analysis Finds Nothing
**Why**: LinkedIn CSV doesn't have connections at this company
**Fix**:
- Search your email for anyone at that company (past intros, conferences, etc.)
- Check if any of your contacts worked there previously (they might still know people)
- Go cold: Agent still generates cold outreach messages

### Cover Letter Feels Too Long
**Why**: Agent includes all research (comprehensive but lengthy)
**Fix**:
- Edit down to 1 page (keep intro, 2-3 key points, strong close)
- Move research details to "take-home package" attachment (if Deep)
- Focus on: Why you, why now, what you'll do Week 1

### Agent Says "Gap" in Fit Matrix
**Why**: Job requires skill/experience you don't have
**Fix**:
- Address proactively in cover letter ("While I haven't done X, I've done similar Y...")
- Show how you'd close gap quickly ("I'd ramp on X in first 30 days by...")
- Position as "growth opportunity" not "deal-breaker"
- If gap is major (e.g., you've never done sales but role needs 10 years experience), reconsider applying

---

## Advanced Usage

### Running Multiple Jobs in Parallel
1. Open 3 terminal windows
2. Run Quick research on 3 different jobs simultaneously
3. Review all outputs, prioritize best matches
4. Run Standard on top 2, Deep on #1

### A/B Testing Cover Letters
1. Run agent, get cover letter v1
2. Edit cover letter, create v2 (different angle)
3. Apply to similar roles with v1 vs v2
4. Track which gets more responses
5. Iterate

### Building a Pipeline Tracker
Create simple spreadsheet:
```
| Company | Role | Stage | Last Touch | Next Action | Hiring Manager | Network Path | Applied Date |
|---------|------|-------|------------|-------------|----------------|--------------|--------------|
| Acme    | AE   | Applied | 11/6    | Follow up Day 3 | Sarah J. | 2nd via Mike | 11/6/25 |
```

Update after each action (applied, reached out, interviewed, offer, rejected)

---

## Examples

### Example 1: Quick Application
```
JOB_URL: https://jobs.lever.co/startup/ae-role
COMPANY_NAME: startup-xyz
RESEARCH_DEPTH: Quick
ROLE_TYPE: AE
YOUR_PRIORITY: growth + equity
```
**Time**: 15-20 min
**Output**: 7 files
**Use Case**: Decent fit, applying to 10 roles this week

### Example 2: Strong Match
```
JOB_URL: https://boards.greenhouse.io/bigco/head-of-sales
COMPANY_NAME: bigco-series-b
RESEARCH_DEPTH: Standard
ROLE_TYPE: Head of Sales
YOUR_PRIORITY: equity + team building
```
**Time**: 30-45 min
**Output**: 10 files (includes network analysis)
**Use Case**: Great fit, excited about company

### Example 3: Dream Job
```
JOB_URL: https://jobs.ashbyhq.com/dreamco/vp-sales
COMPANY_NAME: dreamco
RESEARCH_DEPTH: Deep
ROLE_TYPE: VP Sales
YOUR_PRIORITY: equity + leadership + culture
```
**Time**: 60+ min
**Output**: 12 files (includes 30/60/90, interview prep, take-home package)
**Use Case**: Perfect fit, top 1% opportunity

---

## Updating Templates

### Adding New Cover Letter Templates
If you have different cover letter styles by role:
```
~/job-search/_templates/
├── Andrew Carlson Resume 2025.pdf
├── About Andy Carlson Intro 2025.pdf (default)
├── cover-letter-AE.md (for AE roles)
├── cover-letter-VP-Sales.md (for VP Sales roles)
├── cover-letter-RevOps.md (for RevOps roles)
└── linkedin-contacts.csv
```

Modify main agent to use role-specific template:
```
If ROLE_TYPE = "AE", use cover-letter-AE.md
If ROLE_TYPE = "VP Sales", use cover-letter-VP-Sales.md
etc.
```

### Updating Resume
1. Export new resume to PDF
2. Save to `~/job-search/_templates/Andrew Carlson Resume 2025.pdf` (replace old)
3. Agent will use new version on next run

---

## FAQ

**Q: How accurate is the network path analysis?**
A: Depends on your LinkedIn CSV being current. Export fresh CSV every 3-6 months.

**Q: Can I use this for non-sales roles?**
A: Yes, but 30/60/90 plan and some sales-specific outputs won't apply. Agent adapts based on ROLE_TYPE.

**Q: What if I don't have LinkedIn CSV?**
A: Agent still works, just skips network path analysis. You'll get all other outputs.

**Q: How often should I run this?**
A: Quick: 10+ times per week. Standard: 2-3 times per week. Deep: 1-2 times per month.

**Q: Can I share outputs with recruiter?**
A: Yes! Deep research package is designed as "take-home" to show you did homework.

**Q: What if company research finds red flags?**
A: Agent will flag them in `company-intelligence.md`. Decide if deal-breakers or acceptable risks.

---

## Support

**Issues?** Check:
1. Did you fill in all USER INPUTS?
2. Is your resume/cover letter in `_templates/` folder?
3. Is JOB_URL accessible (not behind login)?
4. Is company name spelled correctly (for folder naming)?

**Feature Requests**:
- Future: Google Docs integration
- Future: Notion DB tracker
- Future: Automated follow-up reminders

---

## Success Metrics

Track these over time:
- **Application rate**: How many Quick/Standard/Deep runs per week?
- **Response rate**: % of applications that get response
- **Interview rate**: % that lead to interviews
- **Network path success**: Do warm intros convert better?
- **Time saved**: How much faster is this than manual research?

**Goal**:
- Quick: 80% of applications (volume game)
- Standard: 15% of applications (strong matches)
- Deep: 5% of applications (dream jobs)
- Overall response rate: >20% (vs industry average ~2-5%)

---

**Ready to hunt? Open `_agents/job-hunt-assassin-main.md` and start your first run!** 🎯
