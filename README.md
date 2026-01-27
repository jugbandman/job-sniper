# Company Research Assistant

**General-purpose company intelligence platform. Job search is one use case.**

Formerly "Job Hunt Assassin" / "job-sniper". Renamed Jan 2026 to reflect broader scope.

---

## What Is This?

An AI-powered agent system for company research across multiple use cases ("lenses"):

| Lens | Purpose |
|------|---------|
| **Job Search** | Find roles, generate materials, track applications |
| **Prospect Research** | Research companies for sales (Remix Revenue, HyperAdaptive) |
| **Market Intel** | Track companies, funding rounds, competitive landscape |
| **General** | Any company deep dive for any purpose |

**Philosophy**: Don't be another resume in the pile. Be the candidate who did more research than the hiring manager.

---

## Quick Start

### 1. You Already Have:
- Resume: `_templates/Andrew Carlson Resume 2025.pdf`
- Cover Letter Template: `_templates/About Andy Carlson Intro 2025.pdf`
- Agent (single job): `_agents/job-search/main.md`
- Agent (batch): `_agents/job-search/batch.md`
- Agent (interactive): `_agents/job-search/interactive.md`
- Agent (multi-job compare): `_agents/job-search/multi-job.md`
- Usage Guide: `USAGE_GUIDE.md`

### 2. Optional but Recommended:
- ❓ **Export LinkedIn Contacts**:
  1. LinkedIn → Settings & Privacy → Data Privacy
  2. "Get a copy of your data" → Select "Connections"
  3. Download ZIP → Extract `Connections.csv`
  4. Save to `_templates/linkedin-contacts.csv`

  **Why**: Enables automatic warm intro finding (2nd degree connections to hiring managers)

### 3. Run Your First Job Search:
1. **Open**: `_agents/job-hunt-assassin-main.md`
2. **Fill in** USER INPUTS at top:
   ```
   JOB_URL: [paste job posting URL]
   COMPANY_NAME: [e.g., "acme-saas"]
   RESEARCH_DEPTH: Quick
   ROLE_TYPE: AE
   YOUR_PRIORITY: equity + growth
   ```
3. **Copy entire prompt** (from "AGENT INSTRUCTIONS" to end)
4. **Paste into Claude Code** (or Claude.ai)
5. **Wait 15-20 minutes** (Quick research)
6. **Review outputs** in `~/job-search/[company-name]/`

---

## Research Depth Options

| Depth | Time | Use Case | Outputs | Best For |
|-------|------|----------|---------|----------|
| **Quick** | 15-20 min | Most applications (80%) | 7 files | Decent fit, applying to 5+ roles/week |
| **Standard** | 30-45 min | Strong matches (15%) | 10 files | Great fit, excited about company |
| **Deep** | 60+ min | Dream jobs (5%) | 12 files | Perfect fit, top 1% opportunity |

**Rule of Thumb**:
- **Quick**: "I'm qualified and interested" → Apply to 10-15 per week
- **Standard**: "This is a great match" → Apply to 2-3 per week
- **Deep**: "This is THE job" → Apply to 1-2 per month

---

## What You Get (Output Files)

### All Depths:
- ✅ `company-intelligence.md` - Company overview, news, culture, red flags
- ✅ `hiring-managers.md` - Who to contact (names, titles, LinkedIn)
- ✅ `job-analysis-fit-matrix.md` - Your fit for each requirement (A+/A/B/C/Gap)
- ✅ `positioning-strategy.md` - How to position yourself, key talking points
- ✅ `cover-letter.md` - Customized cover letter (ready to send)
- ✅ `linkedin-messages.md` - Outreach messages (hiring manager, connections)
- ✅ `email-sequence.md` - Follow-up templates (Day 0, 3, 7)

### Standard & Deep:
- ✅ `network-paths.md` - Warm intro opportunities (via your LinkedIn)
- ✅ `competitive-intelligence.md` - Market positioning, how company differentiates

### Deep Only:
- ✅ `interview-prep.md` - Questions to ask, STAR stories
- ✅ `30-60-90-day-plan.md` - Execution plan (if sales/GTM role)
- ✅ `take-home-package.md` - Research summary to attach with application

---

## Example: What Kilo Code Research Looked Like

We built this agent by creating comprehensive research for the Kilo Code AE role:

**Inputs**:
- Job URL: https://jobs.ashbyhq.com/kilocode/account-executive
- Research Depth: Deep (60+ min)
- Role Type: Account Executive

**Outputs** (17 files, 444KB):
- Market intelligence (verified #1 on OpenRouter, 420K downloads)
- Competitive battlecards (Cursor, Windsurf, Copilot, Cody)
- Lead scoring rubric (how to qualify inbound leads)
- Sales playbooks (discovery, demo, objection handling)
- ICP analysis (who buys, why, how)
- Strategic analysis (opportunity strengths/risks, recommendation: PURSUE)
- 30/60/90 day plan (week-by-week action plan)
- Customized cover letter (with company-specific insights)
- Application one-pager (executive summary)

**Result**: Not just an application, but a complete "take-home" package proving you've done deeper research than anyone else.

---

## How This Beats Normal Job Applications

### Normal Candidate:
- Submits generic resume
- Generic cover letter (or no cover letter)
- Waits for response
- **Response rate: 2-5%**

### You (Using Job Hunt Assassin):
- Submits resume + customized cover letter with company-specific insights
- Attaches "take-home" research package (Deep mode)
- Reaches out to hiring manager via warm intro (if network path exists)
- Sends follow-up emails Day 3, Day 7 (from agent-generated templates)
- **Expected response rate: 20-40%** (10x better)

**Why It Works**:
- Shows you did homework (hiring managers respect this)
- Proves you're serious (not spamming 100 jobs)
- Demonstrates skills (research, analysis, communication)
- Builds relationships (warm intros convert 5-10x better)

---

## Files in This Repo

```
company-research-assistant/
├── README.md (this file)
├── USAGE_GUIDE.md (detailed instructions)
├── QUICK_START.md
├── job-applications-tracker.csv
│
├── _templates/
│   ├── Andrew Carlson Resume 2025.pdf
│   ├── About Andy Carlson Intro 2025.pdf
│   ├── resumes/ (multiple resume versions)
│   ├── cover-letter-style-guide.md
│   ├── resume-tldr-template.md
│   ├── linkedin-contacts.csv (export from LinkedIn)
│   └── README.md
│
├── _agents/
│   ├── AGENT-WORKFLOW-IMPROVEMENTS.md
│   ├── core/ (shared research capabilities)
│   │   └── company-research.md (general company research - future)
│   └── job-search/ (job search lens)
│       ├── batch.md (batch URL processing)
│       ├── interactive.md (Q&A mode)
│       ├── main.md (single job deep dive)
│       └── multi-job.md (compare roles at same company)
│
└── Output goes to Obsidian:
    03-Projects/job-search/opportunities/{company}-{role}/
    ├── _MOC.md (source of truth, frontmatter syncs to Notion)
    ├── cover-letter.md
    ├── resume-tldr.md
    └── research-notes.md
```

---

## Next Steps

### Today (Test It):
1. **Export LinkedIn contacts** (optional but recommended)
2. **Find a job posting** you're interested in
3. **Run Quick research** (15-20 min) to test the agent
4. **Review outputs** - are they useful? What needs tweaking?

### This Week:
1. **Run Quick on 5-10 jobs** - Build pipeline, see what converts
2. **Run Standard on top 2** - Strong matches get deeper research
3. **Track results** - Which depth gets best response rate?

### Ongoing:
1. **A/B test messaging** - Try different cover letter angles, see what works
2. **Build network** - Leverage warm intros when network-paths.md finds them
3. **Iterate** - Agent gets better as you refine your templates and inputs

---

## Troubleshooting

**Agent can't find hiring manager?**
→ Check company website Team page, LinkedIn job posting, or search X/Twitter

**Network path analysis finds nothing?**
→ That's OK, agent still generates cold outreach messages

**Cover letter too long?**
→ Edit down to 1 page, move research to take-home attachment

**Job description vague?**
→ Agent will do its best, but garbage in = garbage out. Better JDs = better outputs.

**Agent slow?**
→ Use Quick (15-20 min) for most jobs, save Deep (60+ min) for dream roles

---

## Advanced Tips

### Parallel Processing
Run multiple Quick searches simultaneously in different Claude sessions. Review all outputs, prioritize best matches, then run Standard/Deep on top choices.

### A/B Testing
Run agent twice on similar roles, try different positioning angles in cover letter. Track which gets more responses.

### Pipeline Management
Create simple spreadsheet:
```
| Company | Role | Stage | Applied | Last Touch | Next Action | Hiring Manager | Network Path |
```
Update after each action (applied, reached out, interviewed, offer, rejected).

---

## Success Metrics

Track these over time:
- **Volume**: How many Quick/Standard/Deep runs per week?
- **Response rate**: % that get callbacks
- **Interview rate**: % that lead to interviews
- **Network success**: Do warm intros convert better?
- **Time saved**: How much faster than manual research?

**Goal**: 20-40% response rate (vs industry 2-5%)

---

## Future Enhancements

**Phase 2** (Coming Later):
- Google Docs integration (auto-create cover letter doc)
- Notion DB tracker (auto-log applications)
- Automated follow-up reminders (Day 3, Day 7)

**Phase 3** (Future):
- Email integration (auto-send follow-ups)
- CRM-style pipeline management
- Interview scheduling automation

---

## Built From Kilo Code Success

This agent is the productized version of the Kilo Code job exploration, which created:
- 17 files, 65,000 words, 444KB of research
- Market intelligence, competitive analysis, ICP analysis
- Lead scoring system, sales playbooks, 30/60/90 day plan
- Customized cover letter and application one-pager
- All in ~2 hours using parallel AI agents

**Result**: Proved you can hit Week 1 objectives on Day 1. Showed deeper company understanding than most employees. Became the obvious hire.

**Now**: You can do this for every job, not just one.

---

## Questions?

**Read**: `USAGE_GUIDE.md` (comprehensive instructions)
**Start**: Open `_agents/job-hunt-assassin-main.md` and run your first search
**Iterate**: Test on 5-10 jobs this week, refine as you learn what works

---

**Ready to hunt? Let's turn job search into a sales pipeline. 🎯**

*"Treat job search like enterprise sales: research deeply, personalize heavily, multi-thread intelligently, follow up consistently."*
