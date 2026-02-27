# Company Research Assistant - Product Requirements Document

*A tool that treats job search like enterprise sales prospecting.*

## Problem Statement

Job search is fundamentally broken for both sides of the table.

Candidates spray-and-pray generic resumes across 50-100 postings per week. Hiring managers open their inbox to 200 nearly identical applications, scanning each for maybe 6 seconds before moving on. Industry response rates sit around 2-5%. Everybody loses.

The irony is that great salespeople already know how to solve this. Enterprise sales methodology (deep research, personalized outreach, multi-threading, disciplined follow-up) maps perfectly onto job search. The best AEs don't cold-blast 500 prospects with the same email. They research the account, find the right contact, build a warm path in, and show up with insight the prospect hasn't heard before.

This tool applies that same discipline to job applications. Instead of submitting another generic resume, you show up with company intelligence, a customized positioning strategy, warm intro paths through your network, and outreach materials that prove you did more homework than anyone else in the pile.

The result is a 20-40% response rate instead of 2-5%. That's not a marginal improvement. That's a fundamentally different experience.

## Solution Overview

An AI-powered agent system that runs on Claude Code (or Claude.ai). Give it a job URL, and it researches the company, identifies the hiring manager, analyzes your fit against every requirement, maps your LinkedIn network for warm intros, and generates a full set of customized application materials.

Think of it as having a research team that works in 15 minutes.

The system is built entirely from markdown agent prompts, user configuration files, and templates. There's no code to build, no dependencies to install, no deployment pipeline. You paste a prompt into Claude Code, fill in a few inputs, and the agent executes a multi-phase research workflow that would take a human 4-6 hours to replicate manually.

Everything outputs to markdown files in an organized folder structure, ready to copy/paste into applications, emails, and LinkedIn messages.

## Target Users

**Primary audience.** Job seekers in sales, GTM, and leadership roles. These people already understand the "research and personalize" mindset from their day jobs. They just need the tooling to apply it to their own search.

**Secondary audience.** Anyone applying to knowledge-worker roles where differentiation matters (product, engineering management, marketing, strategy). The methodology works for any role where showing up prepared gives you an edge.

**Power users.** People comfortable with CLI tools and Claude Code. They'll run batch processing, parallel sessions, customize agent prompts, and build their own templates.

**Aspirational users.** Non-technical job seekers who can use the Interactive mode (answer 6 questions, agent handles the rest). No markdown editing required, no terminal knowledge needed. This is the gateway to making the tool accessible to everyone.

## Key Features

### Four Agent Modes

| Mode | Agent File | What It Does | Best For |
|------|-----------|-------------|----------|
| **Main** | `job-search/main.md` | Single job deep dive with full research | Standard applications, dream jobs |
| **Batch** | `job-search/batch.md` | Process 1-5 job URLs in one session | Volume applications, weekly pipeline building |
| **Interactive** | `job-search/interactive.md` | Q&A format, agent asks 6 questions | First-time users, non-technical users |
| **Multi-Job** | `job-search/multi-job.md` | Compare 2-5 roles at the same company | When you're deciding which role to pursue |

### Three Research Depths

| Depth | Time | Outputs | Use Case | % of Applications |
|-------|------|---------|----------|-------------------|
| **Quick** | 15-20 min | 7 files | Decent fit, applying to many roles | 80% |
| **Standard** | 30-45 min | 10 files | Strong match, excited about company | 15% |
| **Deep** | 60+ min | 12+ files | Dream job, going all-in | 5% |

Quick gives you company intel, hiring manager identification, fit analysis, a customized cover letter, LinkedIn outreach messages, and a follow-up email sequence. Standard adds network path analysis (warm intros via your LinkedIn contacts) and competitive intelligence. Deep adds a 30/60/90 day plan, interview prep with STAR story mapping, and a take-home research package you can attach to your application.

### Output Types (12+ File Types)

Every run produces a structured folder of ready-to-use materials.

**All depths generate these.**
- `company-intelligence.md` - Company overview, recent news, culture signals, red flags
- `hiring-managers.md` - Who to contact, their titles, LinkedIn profiles, backgrounds
- `job-analysis-fit-matrix.md` - Every requirement mapped to your experience (A+/A/B/C/Gap)
- `positioning-strategy.md` - How to position yourself, key talking points, proof points
- `cover-letter.md` - Customized cover letter using your voice and company-specific insights
- `linkedin-messages.md` - Outreach messages for hiring managers and connections
- `email-sequence.md` - Follow-up templates for Day 0, Day 3, Day 7

**Standard and Deep add these.**
- `network-paths.md` - Warm intro opportunities found by parsing your LinkedIn contacts CSV
- `competitive-intelligence.md` - Market positioning, how the company differentiates

**Deep adds these.**
- `interview-prep.md` - Company-specific questions to ask, STAR stories mapped to likely interview questions
- `30-60-90-day-plan.md` - Week-by-week execution plan (for sales/GTM roles)
- `take-home-package.md` - One-page research summary designed to attach with your application

### Network Analysis via LinkedIn CSV

Export your LinkedIn connections as a CSV, drop it in the `_templates/` folder, and the agent automatically cross-references your network against each company's hiring team. It finds 1st and 2nd degree connections, suggests warm intro paths, and generates customized outreach messages for each connection type. Warm intros convert 5-10x better than cold applications.

## Architecture

The entire system is prompt-based. No traditional code.

```
company-research-assistant/
  _agents/
    job-search/
      main.md          # Single job deep dive prompt
      batch.md         # Batch processing prompt
      interactive.md   # Q&A mode prompt
      multi-job.md     # Multi-role comparison prompt
    core/
      company-research.md  # Shared research capabilities (future)
  _templates/
    resume.pdf             # Your resume
    cover-letter-intro.pdf # Your intro/style reference
    cover-letter-style-guide.md  # Writing rules for generated letters
    resume-tldr-template.md      # Summary paragraph templates
    linkedin-contacts.csv  # LinkedIn export (optional)
```

**How it works.** Each agent file is a self-contained markdown prompt. You paste it into Claude Code (or Claude.ai), the LLM reads the instructions, and executes a multi-phase research workflow using web search, file reading, and file writing. The agent launches parallel sub-agents for independent research tasks (company research, hiring manager identification, job analysis) and then runs sequential phases that synthesize the findings into positioning strategy and outreach materials.

**No build step.** No package.json, no Docker, no API keys (beyond Claude). The agent prompts are the product. Configuration lives in markdown files. Output goes to markdown files. The entire system is human-readable and human-editable.

**Runs on Claude Code or Claude.ai.** Claude Code gives you the full experience (file system access, parallel agents, automatic file saving). Claude.ai works too, with manual copy/paste of outputs. The prompts are platform-agnostic.

## Multi-Lens Vision

Job search is the first and most developed use case, but the underlying architecture is a general-purpose company research platform. The same research workflow, the same agent structure, the same output patterns apply to multiple "lenses."

| Lens | Status | Use Case |
|------|--------|----------|
| **Job Search** | Built, 4 agent modes | Find roles, research companies, generate application materials |
| **Prospect Research** | Planned | Research companies for sales outreach (for consulting, agency, or SaaS sales) |
| **Market Intel** | Planned | Track companies, funding rounds, competitive landscapes for strategy work |
| **General** | Planned | Any company deep dive for any purpose |

The multi-lens architecture means a single investment in agent infrastructure pays dividends across multiple workflows. A sales team using this for prospect research gets the same depth of intelligence that a job seeker gets for application prep.

## Success Metrics

### Response Rate
**Target.** 20-40% response rate on applications (vs. 2-5% industry average).

The thesis is that quality beats quantity. A personalized application with company-specific insights, warm intro paths, and a structured follow-up cadence should convert at 10x the rate of a generic application.

### Time Savings
**Target.** 2-3 hours saved per application.

Manual research for a single strong application takes 4-6 hours (company research, hiring manager identification, cover letter writing, LinkedIn stalking, follow-up planning). The agent compresses this to 15-60 minutes depending on depth, and the output quality is more consistent.

### Quality Consistency
Every application gets the same structured research process. No more "I was tired when I wrote that cover letter" variance. The agent applies the same methodology every time, and the quality floor is high.

### Trackable Metrics
- Volume per week (Quick/Standard/Deep runs)
- Response rate by depth level
- Interview conversion rate
- Network path success rate (warm intros vs. cold applications)
- Time from research to application submission

## Technical Requirements

### Required
- **Claude Code** (preferred) or **Claude.ai** (works with manual copy/paste)
- **Resume** in PDF or markdown format
- **Cover letter or intro document** for voice/style reference

### Optional (Recommended)
- **LinkedIn contacts CSV** for network path analysis
- **Multiple resume versions** for role-specific positioning (IC vs. leadership vs. GTM)

### Not Required
- No programming language runtime
- No database
- No API keys (beyond Claude subscription)
- No deployment infrastructure
- No Docker, npm, pip, or any package manager

## Future Roadmap

### Near-term (next quarter)
- **Job watcher** - Monitor specific job boards and companies for new postings, alert when relevant roles appear
- **Notion sync** - Auto-create database entries from Obsidian output files, track pipeline in Notion
- **Setup wizard** - Interactive onboarding agent that creates user config from a conversation

### Mid-term (3-6 months)
- **Email integration** - Auto-draft follow-up emails in Gmail at Day 3, Day 7
- **CRM pipeline** - Track applications, contacts, and follow-ups in a lightweight CRM view
- **Cowork mode** - Run the agent alongside you as you browse job postings, researching in real-time

### Long-term (6-12 months)
- **Automated follow-ups** - Agent sends follow-up emails on schedule with human approval
- **Interview scheduling** - Integrate with calendar to propose times
- **Multi-lens agents** - Prospect research, market intel, and general company deep-dive agents
- **Community templates** - Shared agent prompts, cover letter styles, and research workflows from other users

## Competitive Landscape

### LinkedIn Easy Apply
LinkedIn optimizes for volume. Click a button, send a generic profile, move on. The platform incentivizes quantity over quality, which is exactly why hiring managers ignore most Easy Apply submissions. This tool takes the opposite approach, investing more time per application to generate significantly higher response rates.

### Huntr / Teal / JobScan
These tools track applications and optimize resume keywords. They're useful for organization but don't do the actual research. They help you manage the spreadsheet, not fill it with better opportunities. This tool does the research, generates the materials, AND creates trackable output.

### AI Resume Builders (Kickresume, Rezi, etc.)
Most AI resume tools do surface-level keyword matching against a job description. They might suggest adding "Python" because the JD mentions it. This tool goes deeper, researching the company's actual situation, finding the hiring manager, analyzing your network for warm paths in, and generating a full outreach strategy. The resume is just one output among twelve.

### ChatGPT / Generic AI
You can paste a JD into ChatGPT and ask for a cover letter. You'll get a generic, AI-sounding letter with no company-specific intelligence, no hiring manager research, no network analysis, no follow-up strategy. This tool structures the AI interaction as a multi-phase research workflow with specific outputs, quality standards, and a methodology that consistently produces better results.

### Manual Research
The "old school" approach works. Spending 4-6 hours researching a company, writing a custom cover letter, finding the hiring manager on LinkedIn, and planning your follow-up cadence produces great results. This tool replicates that process in 15-60 minutes with the same (or better) output quality, and does it consistently every time.

## What Makes This Different

**It's a methodology, not just a tool.** The agent prompts encode enterprise sales best practices (research, personalization, multi-threading, follow-up) into a repeatable workflow. The AI is the execution engine, but the methodology is the product.

**It's human-editable all the way down.** Every agent prompt, every template, every configuration file is a markdown document you can read and modify. No black boxes. If you don't like how the cover letter sounds, edit the style guide. If you want different research depth tiers, modify the agent prompt. The system is designed to be customized.

**It treats the candidate like the product.** Most job search tools treat the application as a form to fill out. This tool treats the candidate as a product to position, using the same frameworks that great salespeople use to position their products in competitive deals.

**It generates a complete "campaign," not just a document.** A cover letter is table stakes. This tool generates company intelligence, a fit matrix, a positioning strategy, network paths, outreach messages, follow-up sequences, interview prep, and a take-home research package. That's not an application. That's a campaign.

## Origin Story

This tool was born from a real job search. The first version was built to research a single role (Account Executive at Kilo Code), and the output was staggering: 17 files, 65,000 words, 444KB of research. Market intelligence, competitive battlecards, lead scoring rubrics, sales playbooks, ICP analysis, strategic recommendations, a 30/60/90 day plan, and a customized application package.

The insight was simple. If you can do this for one job, you can do it for every job. The agent prompts are the productized version of that first research sprint. What took 2 hours with manual AI orchestration now takes 15-60 minutes with structured agent prompts.

The name evolved too. "Job Hunt Assassin" became "Job Sniper" became "Company Research Assistant" as the scope expanded from job search to general company intelligence. The job search lens is the most developed, but the architecture supports any use case where deep company research creates an advantage.
