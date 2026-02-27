# Company Research Assistant - Workflow Improvements

**Repo renamed**: `job-sniper` → `company-research-assistant` (Jan 2026)
**Agents restructured**: `_agents/job-search/` for job-specific, `_agents/core/` for shared

---

## Jan 2026: Batch Mode + Multi-Lens Architecture

### What Changed
- Renamed from "Job Hunt Assassin" / "job-sniper" to "Company Research Assistant"
- Tool is now a general-purpose company intelligence platform
- Job search is one "lens" among several (prospect research, market intel, general)
- Added batch processing mode (`_agents/job-search/batch.md`)
- Added resume TLDR template (`_templates/resume-tldr-template.md`)
- Restructured agents into `core/` and `job-search/` directories

### New Workflow Modes

| Mode | Agent | Description |
|------|-------|-------------|
| **Batch** | `job-search/batch.md` | Process 1-5 job URLs in one session, lean research |
| **Interactive** | `job-search/interactive.md` | Q&A mode for single job |
| **Main** | `job-search/main.md` | Single job deep dive |
| **Multi-Job** | `job-search/multi-job.md` | Compare roles at same company |

### Token Efficiency (from HyperAdaptive Learnings)

Applied lessons from Jan 23 session that wasted 40% of tokens:

| Principle | Implementation |
|-----------|---------------|
| Ask scope first | Before researching, confirm depth needed |
| Read lean | Extract only required fields from JD |
| One fetch + ask | One web search per company, summarize, ask if more needed |
| Don't over-document | Light research = 1 paragraph per company |
| Check before reading | Don't read duplicates |

**Token budget**: ~500 tokens research + ~300 tokens materials per job in batch mode.

### Obsidian Output Structure

```
03-Projects/job-search/opportunities/{company}-{role}/
  _MOC.md        # Source of truth with YAML frontmatter
  cover-letter.md
  resume-tldr.md
  research-notes.md (only for deep research)
```

### Notion Integration (Future)

- Database ID: `b16f92737cc04fd6b638c4af3996e039`
- Blocked: Notion MCP not yet configured in Claude Code
- Plan: Obsidian is source of truth, Notion gets synced from frontmatter

### Future Modes (Not Yet Built)

- **Incremental**: "I applied to Glean today" → updates Obsidian + Notion
- **Research**: "Check if Figma has roles" → scans careers page
- **Cleanup**: Triage stale Research/Interested entries
- **Company Prep**: Quick overview or deep interview prep

---

## Nov 2025: Always Get JD First

**Date**: November 6, 2025
**Source**: User feedback from early application

---

## Issue: Doing Analysis Before Getting Job Description

### What Happened:
1. User provided a job URL hosted on Lever
2. Agent tried WebFetch, only got CSS code, no actual JD
3. Agent proceeded with deep analysis based on:
   - Job title from the URL
   - Company research (website, Crunchbase, etc.)
   - Assumptions about the role type
4. Created initial materials:
   - Fit score: 78/100
   - Cover letter without JD specifics
   - Positioning strategy based on assumptions
5. User later provided actual JD text
6. Had to revise everything:
   - Fit score jumped from 78 to 90/100 (+12 points)
   - JD mentioned a specific skill the user had that was missed
   - Had to rewrite cover letter, positioning, analysis
   - Wasted tokens and time

### Why This Was Wasteful:
- Did deep analysis twice (before JD, after JD)
- Missed critical info (MSPs mentioned in JD)
- Fit score was inaccurate initially
- Had to revise materials that were already drafted

---

## Solution: Always Get JD First

### New Workflow (Implemented):

#### Step 0: Fetch Job Description (BEFORE any deep analysis)

1. **Try to fetch JD via WebFetch**
   - Attempt to scrape job description from URL
   - Check if actual content was retrieved (not just CSS/HTML)

2. **If fetch fails or returns only code**:
   - **STOP** - Don't proceed with deep analysis
   - Ask user:
     ```
     I tried to fetch the job description but couldn't access the full text.

     To provide accurate analysis, please:
     - Option 1: Copy/paste the job description text
     - Option 2: Upload a PDF of the job posting
     - Option 3: Proceed with job title + company research only (less accurate)

     Which would you prefer?
     ```

3. **Wait for user to provide JD**
   - Don't create job-analysis-fit-matrix.md yet
   - Don't create positioning-strategy.md yet
   - Don't create cover-letter.md yet
   - Only do company research (can be done in parallel)

4. **Once JD is confirmed**:
   - Extract key requirements from JD
   - Proceed with fit assessment based on ACTUAL requirements
   - Create materials once, accurately

### What to Do While Waiting for JD:
✅ **Can do in parallel** (won't need revision):
- Company research (revenue, funding, team size, etc.)
- Leadership research (who's the CRO, hiring manager)
- Partner program research (if channel role)
- Competitive landscape

❌ **Don't do until JD confirmed** (will need revision):
- Fit assessment (need actual requirements)
- Positioning strategy (need to know what they're looking for)
- Cover letter (need to reference JD specifics)
- Gap analysis (need to know what gaps exist)

---

## Implementation

### Updated Files:
1. ✅ **job-hunt-assassin-interactive.md** - Added Step 1.5 (fetch JD first)
2. ✅ **job-hunt-assassin-main.md** - Added Phase 0 (get JD before research)
3. ✅ **AGENT-WORKFLOW-IMPROVEMENTS.md** (this file) - Documents the improvement

### What Changed:

**BEFORE** (inefficient):
```
Step 1: Parse user inputs
Step 2: Launch parallel research agents
  - Company research
  - Job analysis (based on assumptions!)
  - Fit assessment (based on assumptions!)
Step 3: Create positioning strategy (based on assumptions!)
Step 4: Create cover letter (based on assumptions!)
[User provides JD]
Step 5: Revise everything
```

**AFTER** (efficient):
```
Step 0: Try to fetch JD
  - If fail → ASK USER for JD text/PDF
  - Wait for confirmation
Step 1: Parse user inputs + JD requirements
Step 2: Launch parallel research agents
  - Company research
  - Job analysis (based on ACTUAL JD!)
  - Fit assessment (based on ACTUAL requirements!)
Step 3: Create positioning strategy (accurate first time)
Step 4: Create cover letter (references JD specifics)
[No revisions needed]
```

---

## Benefits of New Workflow

### Time Saved:
- No need to revise materials after getting JD
- Analysis is accurate the first time
- User gets better quality output faster

### Token Efficiency:
- Don't generate content twice
- Don't update multiple files after JD arrives
- More efficient use of context window

### Accuracy:
- Fit scores are accurate from start (not 78 → 85 → 90)
- Cover letter references actual JD language from start
- Positioning strategy addresses actual requirements

### User Experience:
- Clear expectation setting (tell user we need JD first)
- Faster turnaround (no back-and-forth revisions)
- Higher quality output (built on accurate foundation)

---

## Exception: When to Proceed Without JD

**Only proceed without JD if**:
1. User explicitly chooses "Option 3: Proceed with job title + research only"
2. User confirms they don't have JD text/PDF available
3. JD is truly inaccessible (behind login, expired posting, etc.)

**If proceeding without JD**:
- Note prominently in all files: "Analysis based on job title + company research only - not based on actual JD"
- Set expectation: "This analysis may need revision if/when JD becomes available"
- Focus on company research, general role analysis, not specific fit assessment
- Keep materials flexible and easy to update

---

## Lessons Learned

### What Worked Well:
- Company research was accurate (didn't need revision)
- Leadership research was correct
- Industry research was solid
- User's niche experience was identified early (from their profile, not JD)

### What Was Wasteful:
- Created fit assessment without knowing actual requirements
- Wrote cover letter without knowing JD language
- Missed that JD specifically called out a skill the user had (perfect match!)
- Had to update 6+ files when JD finally arrived

### Key Takeaway:
**Don't assume what the JD says. Get it first, then analyze.**

---

## For Future Improvements

### Potential Enhancements:
1. **JD Parser**: If user pastes JD, automatically extract:
   - Required qualifications (bullet list)
   - Preferred qualifications (bullet list)
   - Key responsibilities (bullet list)
   - Keywords/technologies mentioned
   - Salary range (if mentioned)

2. **JD Quality Check**: Before proceeding, verify JD has enough info:
   - Does it have requirements section?
   - Does it have responsibilities section?
   - Is it just a short blurb or full description?

3. **Smart Waiting**: While waiting for JD, do company research in parallel
   - Don't sit idle
   - Have something to show user while they find JD
   - But mark clearly: "Waiting for JD before fit assessment"

---

## Template: Asking User for JD

```markdown
I attempted to fetch the job description from [URL] but couldn't access the full text (the page may be behind a login, expired, or structured in a way that prevents scraping).

To provide you with the most accurate analysis, I need the actual job description text. This ensures:
- Accurate fit assessment (matching your experience to actual requirements)
- Cover letter that references specific JD language
- Positioning strategy that addresses what they're actually looking for

**Please choose one**:

**Option 1 (Recommended)**: Copy/paste the job description text from the posting
**Option 2**: Upload a PDF screenshot of the job posting
**Option 3**: Proceed with analysis based on job title + company research only
  - Note: This will be less accurate and may need revision later if JD becomes available

While you're getting that, I'll start researching the company in parallel.

Which option works best for you?
```

---

**Status**: Workflow improvements implemented in both agent files (interactive + main). Future job searches will ask for JD upfront before doing deep analysis.
