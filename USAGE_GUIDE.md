# Usage Guide

Detailed instructions for getting the most out of the Company Research Assistant.

## What This Tool Does

The Company Research Assistant is an automated agent that researches companies, finds hiring managers, analyzes your network, and generates customized application materials. It treats job search like enterprise sales: research deeply, personalize heavily, multi-thread your outreach.

**Philosophy**: Don't be another resume in the pile. Be the candidate who understands the company better than their own employees.

## Quick Start (5 Minutes)

1. **Make sure your config exists.** You need `_config/user-profile.md` and `_config/user-preferences.md`. If you don't have them, run the setup agent first (`_agents/setup.md`).

2. **Open an agent file.** For your first run, use `_agents/job-search/interactive.md`.

3. **Copy the entire file** and paste it into Claude Code.

4. **Answer the questions** when prompted (job URL, company name, research depth, role type, your priority, special notes).

5. **Wait** 15-20 minutes for Quick depth, 30-45 for Standard, 60+ for Deep.

6. **Review outputs** in your configured output folder (set in `_config/user-profile.md`).

## Research Depth Guide

### Quick (15-20 min)

**When to use:** Decent fit, but not a dream job. You're applying to several roles this week.

**What you get:**
- Company intelligence (overview, news, culture, red flags)
- Hiring manager identification
- Job analysis and fit matrix
- Positioning strategy
- Custom cover letter
- LinkedIn outreach messages
- Email follow-up sequence

**What you don't get:** Network path analysis, competitive intelligence, interview prep, 30/60/90 day plan.

**Cost estimate:** $0.40-$1.00 with recommended model mix.

**Use case:** "I'm applying to 10 roles this week. I need solid materials fast."

### Standard (30-45 min)

**When to use:** Strong match at a company you're excited about.

**Everything from Quick, plus:**
- Network path analysis (warm intro opportunities via your LinkedIn connections)
- Competitive intelligence (market positioning, differentiation)
- Deeper positioning strategy with more company-specific angles
- More detailed email follow-up sequence

**Cost estimate:** $1.00-$2.50 with recommended model mix.

**Use case:** "This is a great fit. I want to maximize my chances."

### Deep (60+ min)

**When to use:** Dream job, perfect fit, top 1% opportunity.

**Everything from Standard, plus:**
- Interview prep package (questions to ask, STAR stories mapped to your experience)
- 30/60/90 day plan (especially useful for sales and GTM roles)
- Take-home research package (summary designed to attach with your application)
- Full competitive analysis with battlecards

**Cost estimate:** $5-$12 with recommended model mix (higher if using Opus for strategy).

**Use case:** "This is THE role. I'm going all-in."

### Choosing Your Depth

A practical split for most job searchers:
- **80% Quick** for volume (build pipeline, cast a wide net)
- **15% Standard** for strong matches (invest more where it counts)
- **5% Deep** for dream jobs (maximum effort, maximum differentiation)

## Prerequisites

### Required

- **Claude Code** installed and configured. See the [official guide](https://docs.anthropic.com/en/docs/claude-code).
- **Your config files** in `_config/`. Run `_agents/setup.md` to create them, or copy `_config/user-profile.example.md` to `_config/user-profile.md` and edit manually.
- **A resume** in `_templates/` (PDF or markdown).

### Optional (Enhances Output)

- **LinkedIn Contacts CSV** at `_templates/linkedin-contacts.csv`. Enables network path analysis, which finds warm intros through your existing connections. Without it, the agent skips network analysis and generates cold outreach instead.
- **Cover letter examples** in `_templates/`. If you have existing cover letters you like, the agent can match your voice and tone.

## Exporting LinkedIn Contacts

1. Go to LinkedIn > **Me** > **Settings & Privacy**
2. **Data Privacy** > **Get a copy of your data**
3. Select **Connections** only (faster download)
4. **Request Archive** (takes about 10 minutes)
5. LinkedIn emails you a ZIP file
6. Extract `Connections.csv`
7. Save to `_templates/linkedin-contacts.csv`

The expected format:
```csv
First Name,Last Name,Email Address,Company,Position,Connected On
Jane,Smith,jane@example.com,Acme Corp,VP Sales,01 Jan 2023
```

Export a fresh CSV every 3-6 months to keep network analysis current.

## Output Structure

After running the agent, you get a folder of markdown files at your configured output path.

```
{your-output-path}/{company}-{role}/
├── company-intelligence.md          # Company overview, news, culture
├── hiring-managers.md                # Who to contact, titles, LinkedIn
├── job-analysis-fit-matrix.md        # Requirements mapped to your experience
├── positioning-strategy.md           # How to position yourself, key angles
├── cover-letter.md                   # Customized cover letter (ready to send)
├── linkedin-messages.md              # Messages to hiring manager, connections
├── email-sequence.md                 # Follow-up email templates
├── network-paths.md                  # Warm intro opportunities (Standard+)
├── competitive-intelligence.md       # Market positioning (Standard+)
├── interview-prep.md                 # Questions, STAR stories (Deep)
├── 30-60-90-day-plan.md              # Execution plan (Deep)
└── take-home-package.md              # Research summary to attach (Deep)
```

Your output path is configured in `_config/user-profile.md` under "Output Path."

## What to Do with Outputs

### Day 0 (Immediate)
1. Read `company-intelligence.md` for a quick company overview (5 min)
2. Check `job-analysis-fit-matrix.md` to confirm you're a good fit (3 min)
3. Review and tweak `cover-letter.md`, then submit your application (10 min)
4. If `network-paths.md` found warm intros, reach out to your connection (5 min)

### Day 1-3 (Follow Up)
5. Use `linkedin-messages.md` to reach out to the hiring manager or mutual connections
6. If no response, use `email-sequence.md` for the Day 3 follow-up

### If You Get an Interview
7. Re-read `company-intelligence.md` for fresh intel before the call
8. Review `interview-prep.md` for questions to ask and STAR stories
9. Use `30-60-90-day-plan.md` as a conversation piece (especially for sales/GTM roles)

## Model Recommendations

Different tasks benefit from different Claude models. The short version:

| Task | Recommended Model | Why |
|------|------------------|-----|
| Scraping, parsing, formatting | Haiku | Cheapest, fastest, good enough for extraction |
| Research, analysis, cover letters | Sonnet | Best balance of quality and cost |
| Dream job strategy, competitive analysis | Opus | Highest quality for high-stakes work |

**Default to Sonnet for everything.** Only use Opus for Deep research on your top-choice companies where the quality difference justifies 5x the cost.

Full cost tables and model selection guidance are in `MODEL-GUIDE.md`.

## Customizing Your Config

### Profile (`_config/user-profile.md`)

This is your identity. The agents read it to understand who you are and what you're targeting.

Common updates:
- New resume uploaded to `_templates/`
- Changed target role or industry focus
- Updated compensation expectations
- New LinkedIn CSV exported
- Changed output path

### Preferences (`_config/user-preferences.md`)

This controls how your materials sound. Edit these to tune the agent's writing style.

Key settings:
- Cover letter tone and length
- Writing rules (formatting preferences you care about)
- LinkedIn message style
- Email follow-up cadence
- Fit scoring thresholds

Both files are read fresh every run. Edit and save, your next agent run picks up the changes.

## Agent Modes in Detail

### Interactive (`_agents/job-search/interactive.md`)

The agent asks you 6 questions, then runs automatically. Best for first-time users or when you prefer a guided experience.

### Main (`_agents/job-search/main.md`)

Fill in variables at the top of the file (job URL, company name, depth, role type, priority), copy, paste, go. Fastest workflow for experienced users.

### Batch (`_agents/job-search/batch.md`)

Feed it multiple job URLs at once. The agent processes them sequentially, running Quick research on each. Good for weekly pipeline building.

### Multi-Job (`_agents/job-search/multi-job.md`)

Give it 2-5 job URLs at the same company. The agent researches the company once, then analyzes each role, compares them, and recommends which to pursue. Saves time and money versus researching each role separately.

## Tips for Getting the Most Out of It

**Run Quick for volume.** Don't over-invest in long shots. Quick produces strong-enough materials for most applications.

**Customize the last 20%.** The agent gives you 80% of what you need. Read the outputs, add your personal touch, and make the cover letter sound like you.

**Act fast.** Research is perishable. Apply within 24 hours of running the agent.

**Use network paths when they exist.** Warm intros convert significantly better than cold applications. If the agent finds a path, use it.

**Follow up.** Use the email sequence templates. Most candidates never follow up, which means you stand out just by doing it.

**Don't copy/paste blindly.** Read the cover letter, check the company intel for accuracy, and make sure the positioning feels right before sending.

## Parallel Processing

You can run multiple Quick searches simultaneously in different Claude Code sessions. Research 3-5 companies at once, review all the outputs, then run Standard or Deep on the strongest matches.

## Pipeline Tracking

The repo includes `job-applications-tracker.csv` for basic tracking. Update it after each action (applied, outreach sent, interview scheduled, offer, rejected).

## Troubleshooting

### Agent Doesn't Find the Hiring Manager
The job description might not include a name, the company might be stealthy, or LinkedIn profiles could be private. Check the company website Team page, search "[Company] [role] hiring" on X/Twitter, or look at who posted the LinkedIn job listing. The agent still generates outreach templates even without a specific name.

### Network Path Analysis Finds Nothing
This means your LinkedIn CSV doesn't have connections at that company, or you haven't exported it yet. Try searching your email for past contacts there. The agent still generates cold outreach messages.

### Cover Letter Feels Too Long
Edit down to one page. Keep the intro, 2-3 key points, and a strong close. If you ran Deep research, move the extra detail into the take-home package attachment.

### Agent Says "Gap" in Fit Matrix
That's useful information. Address it proactively in your cover letter ("While I haven't done X, my experience with Y translates directly because..."). If the gap is fundamental (the role needs 10 years of something you've never done), it might not be the right fit.

### Outputs Feel Generic
Make sure the job URL is publicly accessible (not behind a login). Add more context in the "Special Instructions" field, like what specifically excites you about the role or any inside knowledge you have about the company.

### Config Not Being Picked Up
Check that your files are named exactly `_config/user-profile.md` and `_config/user-preferences.md`. The agents look for these specific filenames.

## FAQ

**Can I use this for non-sales roles?**
Yes. The 30/60/90 day plan and some sales-specific outputs are most useful for sales and GTM roles, but the core research, cover letter, and outreach tools work for any position. The agent adapts based on the role type you specify.

**What if I don't have a LinkedIn CSV?**
Everything works except network path analysis. You'll get all other outputs. The agent generates cold outreach messages instead of warm intro paths.

**How often should I re-export my LinkedIn contacts?**
Every 3-6 months, or after a networking push when you've added a lot of new connections.

**Can I share the research with a recruiter?**
Absolutely. The Deep research package is designed as a "take-home" that demonstrates you've done your homework. Recruiters and hiring managers both respond well to that level of preparation.

**What if company research finds red flags?**
The agent flags them in `company-intelligence.md`. Read them carefully and decide whether they're deal-breakers or acceptable risks. Better to know before you invest time in the process.
