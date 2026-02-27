# Quick Start

Pick the path that matches where you are.

## First-Time Setup (5 minutes)

If you just cloned this repo and haven't set anything up yet.

1. **Install Claude Code** if you don't have it already. Follow the [official guide](https://docs.anthropic.com/en/docs/claude-code).

2. **Run the setup agent.** Open `_agents/setup.md`, copy the entire file, paste into Claude Code. It walks you through creating your personal config (background, target roles, writing preferences). Takes about 5 minutes.

3. **Add your resume** to `_templates/`. PDF or markdown, either works.

4. **(Optional) Export LinkedIn contacts.** LinkedIn > Settings & Privacy > Data Privacy > Get a copy of your data > Connections. Save the CSV to `_templates/linkedin-contacts.csv`. This enables warm intro analysis.

5. **Run your first search.** Open `_agents/job-search/interactive.md`, copy the entire file, paste into Claude Code. Answer 6 questions. Wait 15-20 minutes.

That's it. Your output folder will have 7 files including a ready-to-send cover letter, hiring manager info, and outreach messages.

## Returning User

You already have config files in `_config/` and a resume in `_templates/`. Just run an agent.

1. **Pick a job posting** you want to research
2. **Choose your agent mode:**
   - `_agents/job-search/interactive.md` for guided Q&A
   - `_agents/job-search/main.md` for power-user mode (edit variables, paste, go)
   - `_agents/job-search/batch.md` for processing multiple URLs
   - `_agents/job-search/multi-job.md` for comparing roles at the same company
3. **Copy the agent file, paste into Claude Code**
4. **Review outputs** in your configured output folder

## Experienced User (Quick Reference)

You know how this works, you just need the file paths.

| What | Where |
|------|-------|
| Single job agent | `_agents/job-search/main.md` |
| Batch agent | `_agents/job-search/batch.md` |
| Interactive agent | `_agents/job-search/interactive.md` |
| Multi-job agent | `_agents/job-search/multi-job.md` |
| Your profile | `_config/user-profile.md` |
| Your preferences | `_config/user-preferences.md` |
| Resume/templates | `_templates/` |
| Setup/re-setup | `_agents/setup.md` |
| Model guidance | `MODEL-GUIDE.md` |
| Full usage guide | `USAGE_GUIDE.md` |

## Research Depth Cheat Sheet

| Depth | Time | Cost | When to Use |
|-------|------|------|-------------|
| **Quick** | 15-20 min | ~$0.50-$1 | Most jobs, volume applications |
| **Standard** | 30-45 min | ~$1-$2.50 | Strong matches, worth the extra investment |
| **Deep** | 60+ min | ~$5-$12 | Dream jobs only, produces take-home research package |

## What You Get

**Quick (7 files):** Company intel, hiring managers, fit analysis, positioning strategy, cover letter, LinkedIn messages, email sequence.

**Standard adds (10 files):** Network paths (warm intros), competitive intelligence.

**Deep adds (12 files):** Interview prep, 30/60/90 day plan, take-home research package.

## Need More Detail?

- `USAGE_GUIDE.md` for comprehensive instructions and tips
- `MODEL-GUIDE.md` for model selection and cost estimates
- `_config/README.md` for configuration documentation
- `README.md` for project overview and file structure
