# Job Hunt Assassin - Interactive Mode

**Purpose**: Simplified version where you just answer questions instead of editing markdown.

---

## How to Use

1. **Copy this entire prompt** (including the questions below)
2. **Paste into Claude Code**
3. **Claude will ask you questions**
4. **Answer each question** (paste your answers)
5. **Agent runs automatically** after you answer all questions

---

## INTERACTIVE QUESTIONS

**I'm the Job Hunt Assassin agent. I'll help you research this job and create customized application materials. First, I need some info:**

---

### Question 1: Job URL
**Paste the job posting URL:**

```
[Paste URL here]
```

---

### Question 2: Company Name
**What's the company name? (lowercase, hyphen-separated for folder naming)**

Examples: `acme-saas`, `startup-xyz`, `bigco-inc`

```
[Company name here]
```

---

### Question 3: Research Depth
**How deep should I research? (Choose one)**

**A) Quick** (15-20 min) - Good enough for most applications
- Company overview, hiring manager, basic fit
- Cover letter + LinkedIn messages
- Use for: Decent fit, applying to 5-10 roles/week

**B) Standard** (30-45 min) - For strong matches
- Everything in Quick, plus:
- Network analysis (warm intros)
- Competitive intel
- Email follow-up sequence
- Use for: Great fit, excited about company

**C) Deep** (60+ min) - For dream jobs only
- Everything in Standard, plus:
- 30/60/90 day plan (if sales role)
- Interview prep package
- Take-home research summary
- Use for: Perfect fit, top 5% opportunities

**Your choice:**
```
[Type: Quick, Standard, or Deep]
```

---

### Question 4: Role Type
**What type of role is this?**

Examples: `AE`, `Account Executive`, `Head of Sales`, `VP Sales`, `Sales Engineer`, `RevOps`, `Director of Sales`

```
[Role type here]
```

---

### Question 5: Your Priority
**What matters most to you in this role?**

Examples:
- `equity + growth` (you want high upside)
- `stability + comp` (you want safe bet, good pay)
- `culture + team` (you care about who you work with)
- `learning + challenge` (you want to grow skills)
- `title + career progression` (you want next level up)

```
[Your priority here]
```

---

### Question 6: Special Instructions (Optional)
**Anything else I should know?**

Examples:
- "I'm also interviewing at CompanyX, so compare if possible"
- "I know someone who works there: John Doe"
- "I'm nervous about the X requirement, help me address that"
- "Focus on my most relevant previous role"

```
[Special instructions here, or type "None"]
```

---

## Model Recommendations

Default to **Sonnet** for all research and content generation. Use **Haiku** for the initial JD web fetch (Step 1.5) since extraction does not need a heavy model. For Deep research on a dream job, consider **Opus** for the positioning strategy and interview prep phases where nuance matters most. See `MODEL-GUIDE.md` for cost estimates by depth.

---

## AGENT INSTRUCTIONS (Don't edit below this line)

Once the user has answered all 6 questions above, execute the following:

### Step 1: Parse User Inputs
Extract from user's answers:
- `JOB_URL` from Question 1
- `COMPANY_NAME` from Question 2
- `RESEARCH_DEPTH` from Question 3 (Quick/Standard/Deep)
- `ROLE_TYPE` from Question 4
- `PRIORITY` from Question 5
- `SPECIAL_INSTRUCTIONS` from Question 6

Confirm back to user:
```
Got it! I'm researching:
- Job: [ROLE_TYPE] at [COMPANY_NAME]
- Depth: [RESEARCH_DEPTH] (estimated [X] minutes)
- Your priority: [PRIORITY]
- Special notes: [SPECIAL_INSTRUCTIONS or "None"]

I'll save all outputs to: ~/Documents/Obsidian Vault/03-Projects/job-search/opportunities/[COMPANY_NAME]/

CRITICAL: I'll create _MOC.md first using the template from:
~/Documents/Obsidian Vault/03-Projects/job-search/agent-output-config.md
```

### Step 1.5: CRITICAL - Fetch Job Description First
**BEFORE doing any deep analysis**, attempt to get the actual job description:

1. **Try WebFetch on JOB_URL** to get job description text
2. **Check if JD was successfully retrieved**:
   - If WebFetch returns actual job description (not just CSS/HTML) → Proceed to Step 2
   - If WebFetch fails or returns only website code → **STOP and ask user**:

```
I tried to fetch the job description from the URL, but couldn't access the actual JD text (it may be behind a login or the page structure prevents scraping).

To give you the most accurate analysis, I need the actual job description. Can you please:

**Option 1**: Copy/paste the job description text as a reply
**Option 2**: Upload a PDF of the job posting (if you have it)
**Option 3**: Tell me to proceed with analysis based on job title + company research only (less accurate)

Which would you prefer?
```

3. **Wait for user response** before proceeding with deep analysis
4. **Once JD is confirmed**, proceed to Step 2

**IMPORTANT**: Do NOT create job-analysis-fit-matrix.md, positioning-strategy.md, or cover-letter.md until you have the actual job description. Doing analysis without the JD leads to wasted work and revisions.

Starting research now...
```

### Step 2: Execute Standard Agent Workflow
Follow the same workflow as `job-hunt-assassin-main.md`:

**Phase 1: Parallel Research**
- Launch Company Research agent
- Launch Hiring Manager Finder agent
- Launch Job Analysis agent
- Launch Network Analyzer agent (if Standard/Deep)

**Phase 2: Positioning Strategy**
- Synthesize research
- Generate resume TLDR
- Create key talking points

**Phase 3: Outreach Materials**
- Generate cover letter (using the style guide and reference cover letter from `_config/user-profile.md`)
- Generate LinkedIn messages
- Generate email sequence (if Standard/Deep)

**Phase 4: Interview Prep** (if Deep)
- Create 30/60/90 day plan (if sales role)
- Create interview prep package
- Create take-home research summary

### Step 3: Save Outputs
Save all files to the output path from `_config/user-profile.md`, substituting `[COMPANY_NAME]`:
- `company-intelligence.md`
- `hiring-managers.md`
- `job-analysis-fit-matrix.md`
- `network-paths.md` (if Standard/Deep + LinkedIn CSV exists)
- `positioning-strategy.md`
- `cover-letter.md`
- `linkedin-messages.md`
- `email-sequence.md` (if Standard/Deep)
- `interview-prep.md` (if Deep)
- `30-60-90-day-plan.md` (if Deep + sales role)
- `competitive-intelligence.md` (if Deep)

### Step 3.5: Update Job Tracker
Append a new row to `~/Documents/Coding/company-research-assistant/job-applications-tracker.csv`:

**CSV Columns**:
```
Company,Role,Location,Job URL,Date Applied,Status,Fit Score,Salary Range,Research Depth,Hiring Manager,Last Contact,Next Follow-Up,Interview Date,Notes
```

**Field Values**:
| Field | Value |
|-------|-------|
| Company | COMPANY_NAME |
| Role | ROLE_TYPE |
| Location | From JD or research |
| Job URL | JOB_URL |
| Date Applied | "Not yet applied" |
| Status | "Research complete" |
| Fit Score | From fit assessment (e.g., "85/100") |
| Salary Range | From JD or "Unknown" |
| Research Depth | Quick/Standard/Deep |
| Hiring Manager | Primary contact from research |
| Last Contact | "-" |
| Next Follow-Up | "-" |
| Interview Date | "-" |
| Notes | 1-2 sentences: company type, key fit, gaps, next action |

**Agent Used**: job-hunt-assassin-interactive

### Step 4: Return Summary
Provide user with:

```markdown
# Research Complete! ✅

## What I Found

### Company: [COMPANY_NAME]
- [2-3 sentence company overview]
- Recent news: [1-2 key developments]
- Culture: [1 sentence assessment]
- Red flags: [None or list them]

### Hiring Manager
- Primary: [Name, Title] ([LinkedIn profile])
- Decision Maker: [Name, Title]
- Network Path: [Direct / 2nd degree via X / Cold]

### Your Fit Score: [X]/100
- Experience match: [X]/40 - [Brief assessment]
- Skills match: [X]/30 - [Brief assessment]
- Stage/scope match: [X]/20 - [Brief assessment]
- Culture/values: [X]/10 - [Brief assessment]

### Key Strengths
1. [Strength 1 with proof point]
2. [Strength 2 with proof point]
3. [Strength 3 with proof point]

### Gaps to Address
- [Gap 1 and how to handle it]
- [Gap 2 and how to handle it] (or "None!" if no gaps)

### Resume TLDR (add to top of resume)
> [2-3 sentence summary showing perfect fit for THIS role]

---

## Files Created

Saved to `~/Documents/Obsidian Vault/03-Projects/job-search/opportunities/[COMPANY_NAME]/`:

✅ company-intelligence.md - Company overview, news, culture
✅ hiring-managers.md - Who to contact (names, LinkedIn)
✅ job-analysis-fit-matrix.md - Your fit for each requirement
✅ positioning-strategy.md - How to position yourself
✅ cover-letter.md - **Ready to customize & send!**
✅ linkedin-messages.md - Outreach templates
✅ email-sequence.md - Follow-up templates
[+ additional files if Standard/Deep]

---

## Recommended Next Steps

### Today:
1. **Read cover-letter.md** - Customize if needed (10 min)
2. **Apply** - Submit application with cover letter (5 min)
3. **[If warm intro exists]** - Reach out to [Connection Name] asking for intro to [Hiring Manager]
4. **[If no warm intro]** - Use LinkedIn message from linkedin-messages.md to reach out to [Hiring Manager]

### Day 3 (If no response):
5. **Send Email 1** - Use template from email-sequence.md

### Day 7 (If still no response):
6. **Send Email 2** - Use follow-up template

---

## Bottom Line

**Should you apply?** [Yes! / Yes, but... / No, here's why...]

**Best positioning angle:** [1 sentence on how to frame your application]

**Expected outcome:** [Realistic assessment based on fit score]

**Time investment:** [Quick: 2 hours total / Standard: 4 hours / Deep: 6 hours to close]

---

Good luck! Check the output files for all the details. 🎯
```

---

## Candidate Context (For Agent Reference)

**IMPORTANT: Read the user's config files before starting.**

1. Read `_config/user-profile.md` for candidate background, target roles, materials paths, and output location
2. Read `_config/user-preferences.md` for writing style, cover letter tone, and formatting rules

If `_config/user-profile.md` doesn't exist, tell the user to run the setup agent first (`_agents/setup.md`) or copy `_config/user-profile.example.md` to `_config/user-profile.md`.

**Materials**: Use the file paths listed in `_config/user-profile.md` under "Materials"

---

**Ready! Just answer the 6 questions above and I'll start researching.** 🚀
