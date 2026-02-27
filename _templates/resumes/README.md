# Resume Templates

Place your resume files here (PDF or markdown). The agents reference these when generating cover letters and positioning strategy.

## Multiple Resumes

If you have different versions for different role types (e.g., leadership vs IC, different industries), put them all here. The setup agent will ask which version to use for which type of role.

## Naming Suggestion

Use descriptive names so you can tell them apart:
- `your-name-leadership-resume.pdf`
- `your-name-ic-resume.pdf`
- `your-name-technical-resume.md`

## Workflow

1. Pick the right version based on the role type
2. The agents read the resume path from `_config/user-profile.md`
3. If you have multiple versions, update user-preferences.md with which version maps to which role type
