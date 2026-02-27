# Model Guide

Practical guidance on which Claude model to use for each part of the Job Hunt Assassin workflow, plus cost estimates by research depth.

## Model Recommendations

### Haiku ($0.25/1M input, $1.25/1M output)

Best for simple, high-volume tasks where speed and cost matter most.

**Use Haiku for:**
- Job description scraping and extraction (WebFetch + parse)
- CSV parsing (LinkedIn contacts, job tracker updates)
- Formatting and file creation (MOCs, markdown templates)
- Simple data extraction from structured pages

Haiku is the fastest and cheapest option. If a task is mostly "read this, extract that," Haiku handles it fine.

### Sonnet ($3/1M input, $15/1M output)

Best balance of quality and cost. This should be your default for most research work.

**Use Sonnet for:**
- Company research and intelligence gathering
- Fit analysis and positioning strategy
- Cover letter generation
- LinkedIn and email outreach drafts
- Network path analysis
- Job requirement breakdown and comparison
- Batch mode processing (all subagent tasks)

Sonnet produces strong analytical output without burning through your budget. For 90% of job research tasks, Sonnet is the right call.

### Opus ($15/1M input, $75/1M output)

Best quality, but expensive. Reserve for high-stakes work where nuance matters.

**Use Opus for:**
- Deep strategic reasoning (dream job positioning)
- Interview prep and 30/60/90 day plans
- Competitive analysis with synthesis across multiple sources
- Complex multi-role comparison (the "which role should I pursue" decision)
- Anything where a wrong conclusion wastes more time than the model cost

Opus is 5x the cost of Sonnet. Only use it when the quality difference actually changes the outcome, like when you are researching your top-choice company and need the sharpest possible positioning.

## Cost Estimates by Research Depth

These are rough estimates assuming a mix of web fetching, analysis, and content generation.

### Quick Research (~15-20 min)

| Model Mix | Estimated Cost |
|-----------|---------------|
| All Sonnet | $0.50 - $1.50 |
| All Opus | $2 - $5 |
| **Recommended** (Haiku scraping + Sonnet analysis) | **$0.40 - $1.00** |

### Standard Research (~30-45 min)

| Model Mix | Estimated Cost |
|-----------|---------------|
| All Sonnet | $1.50 - $3.00 |
| All Opus | $5 - $15 |
| **Recommended** (Haiku scraping + Sonnet analysis) | **$1.00 - $2.50** |

### Deep Research (~60+ min)

| Model Mix | Estimated Cost |
|-----------|---------------|
| All Sonnet | $3 - $8 |
| All Opus | $15 - $40 |
| **Recommended** (Haiku scraping + Sonnet analysis + Opus strategy) | **$5 - $12** |

### Batch Mode (5 jobs)

| Model Mix | Estimated Cost |
|-----------|---------------|
| All Sonnet | $2 - $5 total |
| **Recommended** (Haiku scraping + Sonnet analysis) | **$1.50 - $4.00 total** |

## Default Recommendation

**For everyday use, default to Sonnet for all research tasks.** Use Haiku for web fetching and scraping subtasks. Only reach for Opus when you are doing Deep research on a dream job where quality of strategic insight matters more than cost.

The cost difference between "all Sonnet" and "all Opus" is roughly 5x. For a standard job research session, that is the difference between $2 and $10. Worth it for your top pick, not worth it for job #47 in a batch.

## Quick Reference

| Task Type | Recommended Model |
|-----------|------------------|
| Scrape job description | Haiku |
| Parse CSV / format files | Haiku |
| Company research | Sonnet |
| Fit analysis | Sonnet |
| Cover letter | Sonnet |
| LinkedIn messages | Sonnet |
| Batch processing (subagents) | Sonnet |
| Interview prep (Deep only) | Sonnet or Opus |
| 30/60/90 day plan | Sonnet or Opus |
| Competitive analysis (Deep only) | Opus |
| Dream job positioning strategy | Opus |
