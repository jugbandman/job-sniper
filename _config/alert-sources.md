# Alert Sources

Gmail search queries for job alert emails. These should favor real alert senders and job match emails over generic newsletters.

| Source | Gmail Query | Notes |
|--------|-------------|-------|
| LinkedIn Job Alerts | `from:jobalerts-noreply@linkedin.com newer_than:7d` | Core LinkedIn job alerts |
| Welcome to the Jungle | `from:(welcometothejungle.com) newer_than:7d` | WTJ alerts and job matches |
| Built In | `from:support@builtin.com subject:(job OR matches) newer_than:7d` | Built In job matches, avoids generic content |
| Greenhouse Alerts | `from:(greenhouse.io OR boards.greenhouse.io) newer_than:7d` | Broad Greenhouse alerts, may need tightening |
| Lever Alerts | `from:(jobs@lever.co OR lever.co) newer_than:7d` | Lever alerts or role notifications |
| Indeed | `from:(alerts@indeed.com OR noreply@indeed.com) newer_than:7d` | Indeed alerts |
| Wellfound | `from:(wellfound.com OR angel.co) newer_than:7d` | Startup roles |
| Otta | `from:(otta.com) newer_than:7d` | Otta recommendations |
| ZipRecruiter | `from:(ziprecruiter.com) newer_than:7d` | Often noisy, keep if useful |
| Glassdoor | `from:(glassdoor.com) newer_than:7d` | Optional, often noisy |

## Guidance

- Prefer sender-based queries first.
- Tighten noisy sources with `subject:(job alert OR matches)` if needed.
- The scanner should deduplicate downstream via the Python storage layer.
- If Greenhouse alerts come from a different sender in your inbox, update this file to match the actual sender.
