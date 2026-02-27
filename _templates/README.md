# Templates Folder

This folder contains your personal materials that the Job Sniper agents use to generate customized applications.

---

## What Goes Here

| File | Purpose | Required? |
|------|---------|-----------|
| `resumes/` | Your resume versions (PDF or markdown) | Yes (at least one) |
| `cover-letter-style-guide.md` | Writing style reference for cover letters | No (good defaults built in) |
| `linkedin-contacts.csv` | LinkedIn connections export for network analysis | No (optional) |
| Any cover letters, 30/60/90 plans, writing samples | Extra context for the agents | No (optional) |

---

## LinkedIn Contacts CSV

**File**: `linkedin-contacts.csv`
**Purpose**: Enables network path analysis (find warm intros to hiring managers)
**How to Get**:
1. LinkedIn > Settings & Privacy > Data Privacy
2. "Get a copy of your data" > Select "Connections" only
3. Download ZIP (takes ~10 min)
4. Extract `Connections.csv`
5. Save here as `linkedin-contacts.csv`

---

## Updating Your Materials

- **Resume**: Drop new versions in `resumes/`, update the path in `_config/user-profile.md`
- **LinkedIn contacts**: Re-export every 3-6 months, replace `linkedin-contacts.csv`
- **Writing samples**: Add anytime, reference them in `_config/user-profile.md` Materials section

---

## Security Note

This folder contains personal info (resume, LinkedIn connections). The `.gitignore` keeps these out of the public repo:
- `resumes/*.pdf` and `resumes/*.md` are gitignored
- `linkedin-contacts.csv` is gitignored
- Only this README and the style guide are tracked

If you fork this repo, double-check that your personal files aren't committed.
