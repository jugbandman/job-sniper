"""Response Scanner - detects replies from companies in the pipeline.

Called by the Claude Code skill with email search results.
Checks if any emails are from companies being tracked in Obsidian.
"""

import re
from typing import List, Dict, Optional
from datetime import datetime


def extract_company_domains(companies: List[str]) -> Dict[str, str]:
    """Given a list of company names, generate likely email domains.

    Args:
        companies: List of company names like ["Docker", "Atlassian", "Stripe"]

    Returns:
        Dict mapping domain pattern -> company name
        e.g. {"docker.com": "Docker", "atlassian.com": "Atlassian"}
    """
    domains = {}
    for company in companies:
        # Generate likely domains from company name
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', company).strip().lower()
        parts = clean.split()

        # Single word -> company.com
        if len(parts) == 1:
            domains[f"{parts[0]}.com"] = company
        else:
            # Try concatenated and hyphenated
            domains[f"{''.join(parts)}.com"] = company
            domains[f"{'-'.join(parts)}.com"] = company
            # Also just the first word
            domains[f"{parts[0]}.com"] = company

        # Common patterns
        domains[f"{clean.replace(' ', '')}.io"] = company

    return domains


def check_email_for_company_match(
    sender: str,
    subject: str,
    company_domains: Dict[str, str]
) -> Optional[Dict]:
    """Check if an email is from a tracked company.

    Args:
        sender: Email From header
        subject: Email Subject header
        company_domains: Output from extract_company_domains()

    Returns:
        Dict with {company, sender, subject} if match found, else None
    """
    sender_lower = sender.lower()

    for domain, company in company_domains.items():
        if domain in sender_lower:
            return {
                "company": company,
                "sender": sender,
                "subject": subject,
                "matched_domain": domain,
                "detected_at": datetime.now().isoformat(),
            }

    # Also check subject line for company names
    subject_lower = subject.lower()
    for domain, company in company_domains.items():
        company_lower = company.lower()
        if company_lower in subject_lower and len(company_lower) > 3:
            return {
                "company": company,
                "sender": sender,
                "subject": subject,
                "matched_domain": f"subject_match:{company_lower}",
                "detected_at": datetime.now().isoformat(),
            }

    return None


def format_alert_message(match: Dict) -> str:
    """Format a response match into a Telegram-friendly alert message."""
    company = match["company"]
    subject = match["subject"]
    sender = match["sender"]
    return (
        f"📬 Response from {company}!\n\n"
        f"Subject: {subject}\n"
        f"From: {sender}\n\n"
        f"Check Gmail and take action."
    )
