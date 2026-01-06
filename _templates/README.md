# Templates Folder

This folder contains your personal materials that the Job Hunt Assassin agent uses to generate customized applications.

---

## Current Files

✅ **Andrew Carlson Resume 2025.pdf** (290KB)
- Your latest resume
- Agent references this for experience, metrics, proof points

✅ **About Andy Carlson Intro 2025.pdf** (408KB)
- Your cover letter template/intro
- Agent uses your voice/style from this document

---

## Missing Files (Optional but Recommended)

### LinkedIn Contacts CSV
**File**: `linkedin-contacts.csv`
**Purpose**: Enables network path analysis (find warm intros to hiring managers)
**How to Get**:
1. LinkedIn → Settings & Privacy → Data Privacy
2. "Get a copy of your data" → Select "Connections" only
3. Download ZIP (takes ~10 min)
4. Extract `Connections.csv`
5. Save here as `linkedin-contacts.csv`

**Format Expected**:
```csv
First Name,Last Name,Email Address,Company,Position,Connected On
John,Doe,john@acme.com,Acme Corp,VP Sales,01 Jan 2023
Jane,Smith,jane@startup.io,Startup Inc,Director,15 Feb 2024
```

---

## Optional: Role-Specific Cover Letters

If you have different cover letter styles for different roles, add them here:

```
_templates/
├── Andrew Carlson Resume 2025.pdf
├── About Andy Carlson Intro 2025.pdf (default)
├── cover-letter-AE.md (for Account Executive roles)
├── cover-letter-head-of-sales.md (for Head of Sales roles)
├── cover-letter-vp-sales.md (for VP Sales roles)
├── cover-letter-revops.md (for RevOps roles)
└── linkedin-contacts.csv
```

**Agent Behavior**:
- If role-specific template exists, use that
- If not, use default `About Andy Carlson Intro 2025.pdf`

---

## Updating Your Materials

### Resume
- Export new resume to PDF
- Replace `Andrew Carlson Resume 2025.pdf`
- Agent uses new version on next run

### Cover Letter
- Update `About Andy Carlson Intro 2025.pdf`
- Or create role-specific versions (see above)

### LinkedIn Contacts
- Re-export every 3-6 months (connections change)
- Replace `linkedin-contacts.csv`

---

## File Naming Convention

- **Resume**: `[Your Name] Resume [Year].pdf`
- **Cover Letter**: `About [Your Name] Intro [Year].pdf`
- **LinkedIn**: `linkedin-contacts.csv` (exact name, lowercase)
- **Role-Specific**: `cover-letter-[role-type].md` (lowercase, hyphen-separated)

---

## Security Note

This folder contains your personal info (resume, LinkedIn connections). Keep it private:
- Don't commit to public GitHub repos
- Don't share folder publicly
- Add to `.gitignore` if in version control:
  ```
  job-search/_templates/*.pdf
  job-search/_templates/*.csv
  ```

---

## Next Steps

1. ✅ You have resume and cover letter (ready to go!)
2. ❓ Export LinkedIn contacts (recommended for network analysis)
3. ❓ Create role-specific cover letters (optional, if you apply to diverse roles)

**Ready?** Open `~/job-search/USAGE_GUIDE.md` to learn how to use the agent!
