# Configuration

This folder contains your personal configuration for Job Sniper. The agents read these files to customize their output for you.

## Files

| File | Purpose | Required? |
|------|---------|-----------|
| `user-profile.md` | Your background, target roles, materials paths, output location | Yes |
| `user-preferences.md` | Writing style, cover letter tone, research depth defaults | Yes (but defaults work fine) |
| `user-profile.example.md` | Example configuration for reference | No, just a reference |

## Getting Started

**Option 1 (Recommended):** Run the setup agent to generate your config interactively.
```
Open _agents/setup.md, copy the entire prompt, paste into Claude Code
```

**Option 2:** Copy the example and edit manually.
```
cp _config/user-profile.example.md _config/user-profile.md
```
Then edit `user-profile.md` with your own details.

## What Goes Where

**user-profile.md** is your identity. It answers "who are you?" for the agents.
- Your name, contact info, LinkedIn
- Professional background, key metrics, unique strengths
- Target roles, companies, industries
- Things to avoid
- File paths for your resume, cover letter template, LinkedIn CSV
- Where to save output files

**user-preferences.md** is your style. It answers "how should materials sound?" for the agents.
- Cover letter tone and structure
- Writing rules (formatting preferences)
- Research depth defaults
- Message and email style preferences
- Fit scoring thresholds

## Updating Your Config

Edit these files anytime. The agents read them fresh each run, so changes take effect immediately.

Common updates:
- New resume version uploaded to `_templates/`
- Changed target role or industry focus
- Updated compensation expectations
- New LinkedIn CSV exported
