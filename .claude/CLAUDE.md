# Job Sniper

AI-powered job search tool that treats every application like a sales process. Job search is the primary lens, with future support for prospect research, market intel, and general company deep dives.

## Key Files

- `_agents/job-search/` - Job search agent prompts (main, batch, interactive, multi-job)
- `_config/` - User configuration (profile, preferences)
- `_templates/` - Resume, cover letter templates, LinkedIn CSV
- `MODEL-GUIDE.md` - Which models to use for which tasks

## How to Run

**Recommended:** Use the `/job-sniper` command. It handles setup, config detection, and mode selection automatically.

**Manual:** Configure your profile in `_config/user-profile.md` (or copy from `_config/user-profile.example.md`), choose an agent from `_agents/job-search/`, fill in the inputs and run.

## Output Location

Outputs go to Obsidian vault or a user-configured path. Check `_config/user-profile.md` for the output path.

## Rules

- Always fetch the JD before doing analysis
- Use Sonnet for research subagents, Haiku for scraping
- Save all outputs to the configured output path
- See `MODEL-GUIDE.md` for full model recommendations
