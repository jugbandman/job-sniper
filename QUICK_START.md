# Job Hunt Assassin - Quick Start Guide

**Choose Your Agent Based on Your Situation:**

---

## 🎯 Three Agent Options

### 1. Interactive Mode (Easiest - Start Here!)
**File**: `_agents/job-hunt-assassin-interactive.md`

**When to use**: First time using the agent, or you prefer Q&A format

**How it works**:
1. Copy the entire file
2. Paste into Claude Code
3. Answer 6 simple questions:
   - Job URL?
   - Company name?
   - Quick/Standard/Deep?
   - Role type?
   - Your priority?
   - Any special notes?
4. Agent runs automatically

**Best for**: Beginners, one job at a time

---

### 2. Single Job Mode (For Power Users)
**File**: `_agents/job-hunt-assassin-main.md`

**When to use**: You're comfortable editing markdown, want full control

**How it works**:
1. Open the file
2. Edit USER INPUTS section at top:
   ```
   JOB_URL: [paste URL]
   COMPANY_NAME: acme-saas
   RESEARCH_DEPTH: Quick
   ROLE_TYPE: AE
   YOUR_PRIORITY: equity + growth
   ```
3. Copy entire file
4. Paste into Claude Code
5. Agent runs automatically

**Best for**: Experienced users, batch processing multiple jobs

---

### 3. Multi-Job Analyzer (Compare Multiple Roles)
**File**: `_agents/job-hunt-assassin-multi-job.md`

**When to use**: Same company has 2-5 roles you're interested in

**How it works**:
1. Open the file
2. Fill in company name + paste 2-5 job URLs:
   ```
   COMPANY_NAME: acme-saas
   JOB_1_URL: [AE role]
   JOB_2_URL: [Head of Sales role]
   JOB_3_URL: [Sales Engineer role]
   ```
3. Copy entire file
4. Paste into Claude Code
5. Agent analyzes all roles, recommends best fit

**Best for**: Multiple roles at same company, need help deciding

---

## 📋 Quick Decision Tree

**Start here:**
- ❓ **One company, multiple roles?** → Use **Multi-Job Analyzer**
- ❓ **One job, first time using agent?** → Use **Interactive Mode**
- ❓ **One job, you know the drill?** → Use **Single Job Mode**
- ❓ **Processing 10+ jobs this week?** → Use **Single Job Mode** (faster)

---

## ⚡ Fastest Path to Your First Application

### 5-Minute Quick Start

1. **Open**: `_agents/job-hunt-assassin-interactive.md`
2. **Copy all** (Cmd+A, Cmd+C)
3. **Open Claude Code** (new chat)
4. **Paste** (Cmd+V)
5. **Answer 6 questions** when prompted:
   - Paste job URL
   - Type company name (e.g., "acme-saas")
   - Type "Quick" (for first run)
   - Type role (e.g., "Account Executive")
   - Type priority (e.g., "equity + growth")
   - Type "None" for special instructions
6. **Wait 15-20 minutes** (grab coffee)
7. **Check outputs**: `~/job-search/[company-name]/`
8. **Customize cover letter** (cover-letter.md)
9. **Apply!**

---

## 📊 Research Depth Guide

### Quick (15-20 min)
- Company intel, hiring manager, fit analysis
- Cover letter + LinkedIn messages
- **Use for**: 80% of applications (volume game)

### Standard (30-45 min)
- Everything in Quick, plus:
- Network analysis (warm intros)
- Email follow-up sequence
- Competitive intel
- **Use for**: 15% of applications (strong matches)

### Deep (60+ min)
- Everything in Standard, plus:
- 30/60/90 day plan
- Interview prep
- Take-home package
- **Use for**: 5% of applications (dream jobs)

---

## 🎓 Example: Interactive Mode

**You paste this:**
```
Question 1: Job URL
https://jobs.ashbyhq.com/acme/account-executive

Question 2: Company Name
acme-saas

Question 3: Research Depth
Quick

Question 4: Role Type
Account Executive

Question 5: Your Priority
equity + growth

Question 6: Special Instructions
None
```

**Agent responds:**
```
Got it! I'm researching:
- Job: Account Executive at acme-saas
- Depth: Quick (estimated 15-20 minutes)
- Your priority: equity + growth
- Special notes: None

I'll save all outputs to: ~/job-search/acme-saas/

Starting research now...
```

**20 minutes later, you get:**
- 7 files in `~/job-search/acme-saas/`
- Summary of company, hiring manager, your fit
- Cover letter ready to customize
- LinkedIn messages ready to send
- Recommended next steps

---

## 🔥 Example: Multi-Job Analyzer

**You have 3 roles at same company:**
1. Account Executive
2. Head of Sales
3. Sales Engineer

**You paste:**
```
COMPANY_NAME: acme-saas
NUMBER_OF_JOBS: 3

JOB_1_URL: https://acme.com/jobs/ae
JOB_1_TITLE: Account Executive

JOB_2_URL: https://acme.com/jobs/head-of-sales
JOB_2_TITLE: Head of Sales

JOB_3_URL: https://acme.com/jobs/se
JOB_3_TITLE: Sales Engineer
```

**Agent responds with:**
- Company intel (one time, applies to all roles)
- Analysis of each role (fit score, gaps, challenges)
- Comparison matrix (side-by-side)
- **Recommendation**: "Apply for Head of Sales (92/100 fit), use AE as backup (85/100), skip SE (78/100)"
- Cover letter for recommended role
- Application strategy (which to apply for, when, how to follow up)

---

## 💡 Pro Tips

### For Volume Applications (10+ per week)
- Use **Interactive Mode** or **Single Job Mode** with **Quick** depth
- Batch process: Run 3-5 in parallel (different Claude tabs)
- Review all outputs, apply to top 3-5
- Track in spreadsheet

### For Strategic Applications (2-3 per week)
- Use **Single Job Mode** with **Standard** depth
- Network analysis enabled (export LinkedIn CSV first)
- Leverage warm intros when available
- Follow up consistently

### For Dream Jobs (1-2 per month)
- Use **Single Job Mode** with **Deep** depth
- Include 30/60/90 plan as take-home
- Research company for 30 min BEFORE running agent (add insights to special instructions)
- Multi-thread: warm intros + direct application + hiring manager outreach

---

## 📁 What You'll Get (Output Files)

### All Depths:
- ✅ `company-intelligence.md` - Company overview
- ✅ `hiring-managers.md` - Who to contact
- ✅ `job-analysis-fit-matrix.md` - Your fit score
- ✅ `positioning-strategy.md` - How to position yourself
- ✅ `cover-letter.md` - **Ready to send!**
- ✅ `linkedin-messages.md` - Outreach templates
- ✅ `email-sequence.md` - Follow-up templates

### Standard & Deep add:
- ✅ `network-paths.md` - Warm intro opportunities
- ✅ `competitive-intelligence.md` - Market context

### Deep adds:
- ✅ `interview-prep.md` - Questions, STAR stories
- ✅ `30-60-90-day-plan.md` - Execution plan (if sales role)
- ✅ `take-home-package.md` - Research summary to attach

---

## 🚨 Prerequisites

### Required (You have these):
- ✅ Resume: `_templates/Andrew Carlson Resume 2025.pdf`
- ✅ Cover letter: `_templates/About Andy Carlson Intro 2025.pdf`

### Optional but Recommended:
- ❓ **LinkedIn Contacts CSV**: Export from LinkedIn
  - Enables warm intro finding
  - See `_templates/README.md` for export instructions

---

## 🆘 Troubleshooting

**Agent can't find hiring manager?**
→ That's OK, agent will note this and generate generic outreach

**No network paths found?**
→ Expected if you don't have LinkedIn CSV or no connections at company

**Cover letter too long?**
→ Edit down to 1 page, move extra research to separate doc

**Agent takes longer than expected?**
→ Deep research on complex companies can take 60+ min (get coffee)

**Outputs look generic?**
→ Make sure job URL is accessible (not behind login)
→ Add more context in "Special Instructions"

---

## 📞 Next Steps

1. **Choose your agent** (Interactive for first time)
2. **Find a job posting** you're interested in
3. **Run the agent** (paste into Claude Code)
4. **Review outputs** (30 min to 1 hour later)
5. **Customize cover letter** (add personal touch)
6. **Apply!** (don't overthink it)

---

## 📚 More Help

- **Detailed Guide**: Read `USAGE_GUIDE.md` (comprehensive)
- **Templates Help**: See `_templates/README.md` (how to update materials)
- **Main README**: See `README.md` (philosophy and examples)

---

**Ready? Open `_agents/job-hunt-assassin-interactive.md` and start your first search!** 🚀
