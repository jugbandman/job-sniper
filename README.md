# Company Research Assistant

Treats job search like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently.

An AI-powered agent system that researches companies, analyzes job postings, identifies hiring managers, maps your network, and generates customized application materials. It runs on [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and produces a folder of ready-to-use files for every job you target.

**Philosophy**: Don't be another resume in the pile. Be the candidate who did more research than the hiring manager.

## How It Works

The system is built from three layers that work together:

1. **Agent prompts** (`_agents/`) define what research to do and how to structure it
2. **Your config** (`_config/`) tells the agents who you are, what you're targeting, and how you like to write
3. **Templates** (`_templates/`) hold your resume, cover letter examples, and LinkedIn contacts

You paste an agent prompt into Claude Code, the agent reads your config, researches the company, and writes everything to a structured output folder.

## Quick Start

1. **Clone this repo** (skip this if you already have it)
   ```bash
   git clone https://github.com/jugbandman/job-sniper.git
   cd job-sniper
   ```

2. **Install Claude Code** (skip this if you already have it)
   Follow the [official install guide](https://docs.anthropic.com/en/docs/claude-code). You need a Claude API key or a Claude Pro/Max subscription.

3. **Open the repo in Claude Code and run `/job-sniper`**
   ```bash
   claude   # launch Claude Code from the repo root
   ```
   Then type `/job-sniper`. On first run, it detects you're a new user and walks you through setup: checks prerequisites, finds your resume, runs a 5-minute interview to build your profile, and generates your config files.

4. **Add your resume** to `_templates/resumes/` (PDF or markdown) if the setup didn't find it

5. **Run it again with a job URL**
   ```
   /job-sniper https://jobs.lever.co/some-company/some-role
   ```
   It reads your config, researches the company, and generates a full application package.

**Manual setup alternative:** If you prefer not to use the `/job-sniper` command, you can copy `_config/user-profile.example.md` to `_config/user-profile.md`, edit it by hand, then copy-paste any agent prompt from `_agents/job-search/` directly into Claude Code.

## Prerequisites

**Required:**
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- A resume (PDF or markdown, saved in `_templates/`)
- Your personal config files in `_config/` (the setup agent creates these)

**Optional but recommended:**
- LinkedIn contacts CSV for network/warm-intro analysis. Export from LinkedIn under Settings > Data Privacy > Get a copy of your data > Connections. Save to `_templates/linkedin-contacts.csv`.
- A cover letter example or style guide in `_templates/` for tone matching

## Agent Modes

| Mode | Agent File | Best For |
|------|-----------|----------|
| **Interactive** | `_agents/job-search/interactive.md` | First-time users, guided Q&A format |
| **Main** | `_agents/job-search/main.md` | Power users, fill in variables and go |
| **Batch** | `_agents/job-search/batch.md` | Processing 5+ job URLs at once |
| **Multi-Job** | `_agents/job-search/multi-job.md` | Comparing 2-5 roles at the same company |

**Decision tree:**
- First time? Start with **Interactive**
- One job, you know the drill? Use **Main**
- Multiple jobs this week? Use **Batch**
- Same company, multiple roles? Use **Multi-Job**

## Research Depths

| Depth | Time | Cost Estimate | Files | Best For |
|-------|------|---------------|-------|----------|
| **Quick** | 15-20 min | $0.40-$1.00 | 7 | Most applications (volume play, 80% of your pipeline) |
| **Standard** | 30-45 min | $1.00-$2.50 | 10 | Strong matches you're excited about |
| **Deep** | 60+ min | $5-$12 | 12 | Dream jobs, top 1% opportunities |

Cost estimates assume API usage with the recommended model mix (Haiku for scraping, Sonnet for analysis). **If you have a Claude Pro or Max subscription, this runs within your existing plan at no additional cost.** See `MODEL-GUIDE.md` for full breakdown and model selection guidance.

## Output Files

Every research run creates a folder of markdown files at your configured output path.

**All depths produce:**
- `company-intelligence.md` - Company overview, news, culture, red flags
- `hiring-managers.md` - Who to contact (names, titles, LinkedIn)
- `job-analysis-fit-matrix.md` - Your fit for each requirement (A+/A/B/C/Gap)
- `positioning-strategy.md` - How to position yourself, key talking points
- `cover-letter.md` - Customized cover letter (ready to send)
- `linkedin-messages.md` - Outreach messages for hiring managers and connections
- `email-sequence.md` - Follow-up templates (Day 0, 3, 7)

**Standard and Deep add:**
- `network-paths.md` - Warm intro opportunities (requires LinkedIn CSV)
- `competitive-intelligence.md` - Market positioning, how the company differentiates

**Deep adds:**
- `interview-prep.md` - Questions to ask, STAR stories mapped to your experience
- `30-60-90-day-plan.md` - Execution plan (especially useful for sales/GTM roles)
- `take-home-package.md` - Research summary to attach with your application

## Configuration

Your personal setup lives in `_config/`. Two files control everything:

| File | What It Controls |
|------|-----------------|
| `user-profile.md` | Who you are, your background, target roles, resume path, output location |
| `user-preferences.md` | Writing style, cover letter tone, research depth defaults, scoring thresholds |

**First time?** Run the setup agent (`_agents/setup.md`) to generate both files interactively.

**Already set up?** Edit the files directly. Agents read them fresh every run, so changes take effect immediately.

See `_config/README.md` for details on what goes where, and `_config/user-profile.example.md` for a complete reference configuration.

## Model Guide

The agents work with any Claude model, but different tasks benefit from different models.

| Task Type | Recommended Model |
|-----------|------------------|
| Scraping and parsing | Haiku (cheapest, fastest) |
| Research, analysis, cover letters | Sonnet (best balance) |
| Dream job strategy, competitive analysis | Opus (highest quality) |

**For everyday use, Sonnet handles 90% of tasks well.** Only reach for Opus on Deep research for your top-choice companies.

Full cost estimates and model selection guidance are in `MODEL-GUIDE.md`.

## File Structure

```
company-research-assistant/
├── README.md                          # This file
├── QUICK_START.md                     # Condensed getting-started guide
├── USAGE_GUIDE.md                     # Detailed usage instructions
├── MODEL-GUIDE.md                     # Model recommendations and cost estimates
├── job-applications-tracker.csv       # Application tracking spreadsheet
│
├── _config/                           # Your personal configuration
│   ├── README.md                      # Config documentation
│   ├── user-profile.md                # Your background and targets (you create this)
│   ├── user-profile.example.md        # Example configuration for reference
│   └── user-preferences.md            # Writing style and preferences (you create this)
│
├── _agents/                           # Agent prompts (the brains)
│   ├── setup.md                       # Interactive onboarding agent
│   ├── core/                          # Shared research capabilities
│   │   └── company-research.md        # General company research (future)
│   └── job-search/                    # Job search agents
│       ├── main.md                    # Single job deep dive
│       ├── batch.md                   # Batch URL processing
│       ├── interactive.md             # Guided Q&A mode
│       └── multi-job.md              # Compare roles at same company
│
└── _templates/                        # Your materials
    ├── README.md                      # Template documentation
    ├── resumes/                       # Your resume versions
    ├── cover-letter-style-guide.md    # Cover letter tone reference
    ├── resume-tldr-template.md        # Resume summary template
    └── linkedin-contacts.csv          # Your LinkedIn export (optional)
```

## Contributing and Customization

This tool is designed to be forked and personalized. Some ways to make it yours:

- **Add new agent modes** in `_agents/job-search/` for different research workflows
- **Customize templates** in `_templates/` with your own cover letter formats
- **Tune preferences** in `_config/user-preferences.md` to match your voice
- **Add new lenses** beyond job search (prospect research, market intel) in `_agents/core/`

The agent prompts are plain markdown. Read one, understand the pattern, and adapt it however you want.

## Troubleshooting

**Agent can't find the hiring manager?**
That happens. The agent will note it and generate generic outreach. You can check the company website Team page, LinkedIn job posting, or search on X/Twitter.

**Network path analysis finds nothing?**
Expected if you haven't exported your LinkedIn CSV, or if you don't have connections at that company. The agent still generates cold outreach messages.

**Cover letter too long?**
Edit down to one page. Move the extra research into a take-home attachment (Deep mode generates this automatically).

**Job description is vague?**
The agent does its best, but better input produces better output. Add context in the "special instructions" field.

**Agent running slow?**
Use Quick depth (15-20 min) for most jobs. Save Deep (60+ min) for the ones that really matter.

**Config not being picked up?**
Make sure your files are named exactly `_config/user-profile.md` and `_config/user-preferences.md`. The agents look for these specific filenames.

## Why This Works

The normal application process looks like this: submit a generic resume, maybe write a cover letter, wait and hope. Response rates sit around 2-5%.

This tool flips that. Every application comes with company-specific research, a tailored cover letter, hiring manager outreach, and (for dream jobs) a take-home research package that proves you've done the homework. When a hiring manager sees that level of preparation, you stand out.

It works because it treats job search like a sales process: research deeply, personalize heavily, multi-thread your outreach, and follow up consistently.

---

Useful? Buy Andy a coffee (or beer): **venmo:@jugbandman**
