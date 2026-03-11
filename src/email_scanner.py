"""Email Alert Scanner - parses job alert emails into Job objects"""

import re
import html
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from .models import Job


def parse_builtin_email(body: str, email_date: str) -> List[Job]:
    """Parse a Built In HTML email into Job objects.

    Current Built In alerts are rich HTML emails where each job lives inside an
    anchor tag pointing at a Built In job URL. Parsing the raw HTML as plain text
    produces garbage, so this parser extracts jobs directly from the repeated
    anchor blocks.
    """
    jobs = []

    # Find Built In job links and grab a bounded block around each one.
    pattern = re.compile(
        r'<a[^>]+href="(?P<href>https://[^"]*builtin\.com%2Fjob%2F[^"]+)"[^>]*>'
        r'(?P<content>.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )

    for match in pattern.finditer(body):
        href = html.unescape(match.group('href'))
        content = match.group('content')

        company_match = re.search(r'<div style=margin-bottom:8px;font-size:16px>(.*?)</div>', content, re.IGNORECASE | re.DOTALL)
        title_match = re.search(r'<div style=margin-bottom:8px;font-size:20px;font-weight:700>(.*?)</div>', content, re.IGNORECASE | re.DOTALL)

        if not company_match or not title_match:
            continue

        company = _clean_html_text(company_match.group(1))
        title = _clean_html_text(title_match.group(1))
        if not company or not title:
            continue

        loc_parts = re.findall(r'<span style=vertical-align:middle>(.*?)</span>', content, re.IGNORECASE | re.DOTALL)
        loc_parts = [_clean_html_text(x) for x in loc_parts if _clean_html_text(x)]
        location = ' | '.join(loc_parts[:2])

        salary_min = None
        salary_max = None
        salary_match = re.search(r'\$([\d,]+)\s*-\s*\$([\d,]+)', content)
        if salary_match:
            salary_min = int(salary_match.group(1).replace(',', ''))
            salary_max = int(salary_match.group(2).replace(',', ''))
        else:
            single_salary = re.search(r'\$([\d,]+)', content)
            if single_salary:
                salary_min = int(single_salary.group(1).replace(',', ''))
                salary_max = salary_min

        clean_url = _clean_builtin_tracking_url(href)
        job_id = hashlib.md5(f"builtin:{company}:{title}".lower().encode()).hexdigest()[:12]

        jobs.append(Job(
            job_id=job_id,
            title=title,
            company=company,
            url=clean_url,
            source='builtin',
            posted_date=email_date,
            salary_min=salary_min,
            salary_max=salary_max,
            location=location,
            description='',
            company_stage=None,
            company_size=None,
            industry=None,
        ))

    return _dedupe_jobs(jobs)


def _parse_builtin_segment(segment: str, email_date: str) -> Optional[Job]:
    """Parse a single Built In job segment into a Job object."""
    segment = segment.strip()
    if not segment or len(segment) < 5:
        return None

    # Extract salary if present
    salary_min = None
    salary_max = None
    salary_match = re.search(r'\$([\d,]+)\s*-\s*\$([\d,]+)', segment)
    if salary_match:
        salary_min = int(salary_match.group(1).replace(',', ''))
        salary_max = int(salary_match.group(2).replace(',', ''))
        segment = segment[:salary_match.start()].strip()
    else:
        single_salary = re.search(r'\$([\d,]+)', segment)
        if single_salary:
            salary_min = int(single_salary.group(1).replace(',', ''))
            salary_max = salary_min
            segment = segment[:single_salary.start()].strip()

    # Extract location - common patterns at the end
    location = ""
    location_patterns = [
        r'((?:Remote|Hybrid|In Office)\s+.*?)$',
        r'((?:Remote)\s+(?:United States|USA|US))$',
        r'((?:Hybrid|In Office)\s+\w[\w\s,]+)$',
    ]
    for pat in location_patterns:
        loc_match = re.search(pat, segment, re.IGNORECASE)
        if loc_match:
            location = loc_match.group(1).strip()
            segment = segment[:loc_match.start()].strip()
            break

    # What remains should be "Company Name Title"
    # This is the hardest part - company and title are concatenated
    # Heuristic: look for common title keywords
    title = ""
    company = ""
    title_keywords = [
        r'((?:Regional |Senior |Sr\.? |Chief |Vice |Head |Global |Strategic )?(?:Director|VP|Vice President|Head|CRO|SVP|EVP|Manager|Lead)[\w\s,\-—()]*)',
        r'((?:Enterprise |Strategic |Named |Senior |Sr\.? )?(?:Account Executive|AE|Sales Director|Sales Manager|BDR|SDR)[\w\s,\-—()]*)',
    ]

    for kw_pat in title_keywords:
        title_match = re.search(kw_pat, segment, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip().rstrip(',')
            company = segment[:title_match.start()].strip().rstrip(',')
            break

    if not title:
        # Fallback: use the whole segment as title, company unknown
        title = segment
        company = "Unknown"

    if not title or len(title) < 3:
        return None

    job_id = hashlib.md5(f"builtin:{company}:{title}".lower().encode()).hexdigest()[:12]

    return Job(
        job_id=job_id,
        title=title,
        company=company,
        url="",  # Built In emails don't include URLs in plain text
        source="builtin",
        posted_date=email_date,
        salary_min=salary_min,
        salary_max=salary_max,
        location=location,
        description="",
        company_stage=None,
        company_size=None,
        industry=None,
    )


def parse_linkedin_email(body: str, email_date: str) -> List[Job]:
    """Parse a LinkedIn job alert email body into Job objects."""
    jobs = []

    # Ignore account-management emails like "your job alert has been created"
    if 'your job alert has been created' in body.lower():
        return []

    sections = re.split(r'-{10,}', body)

    for section in sections:
        section = section.strip()
        if not section or 'View job' not in section:
            continue

        url_match = re.search(r'View job:\s*(https://www\.linkedin\.com/comm/jobs/view/(\d+)\S*)', section)
        if not url_match:
            continue

        linkedin_job_id = url_match.group(2)
        pre_url = section[:url_match.start()].strip()
        lines = [l.strip() for l in pre_url.split('\n') if l.strip()]
        lines = [l for l in lines if not l.startswith('This company is actively')
                 and not re.match(r'^\d+ connections?$', l)
                 and 'job alert' not in l.lower()]

        if len(lines) < 2:
            continue

        title = lines[0]
        company = lines[1]
        if 'you’ll receive notifications' in company.lower() or "you'll receive notifications" in company.lower():
            continue
        location = lines[2] if len(lines) > 2 else ""

        clean_url = f"https://www.linkedin.com/jobs/view/{linkedin_job_id}"
        job_id = hashlib.md5(f"linkedin:{linkedin_job_id}".encode()).hexdigest()[:12]

        jobs.append(Job(
            job_id=job_id,
            title=title,
            company=company,
            url=clean_url,
            source="linkedin",
            posted_date=email_date,
            salary_min=None,
            salary_max=None,
            location=location,
            description="",
            company_stage=None,
            company_size=None,
            industry=None,
        ))

    return jobs


def parse_wtj_email(body: str, subject: str, email_date: str) -> List[Job]:
    """Parse a Welcome to the Jungle job alert email.

    WTJ sends HTML emails with two formats:
    1. Multi-job: "There are new jobs matching your search preferences"
       - Company/title alternate in <strong> tags
       - Salary as "Salary: $250-333K OTE"
       - Location in small <span> tags
    2. Single job (followed company): "Docker just posted a new job"
       - Same structure, one job block

    Subject line: "New match: Title at Company"
    """
    jobs = []
    is_html = "<html" in body.lower() or "<strong>" in body

    if is_html:
        jobs = _parse_wtj_html(body, email_date)

    # Fallback to subject line if we got nothing
    if not jobs:
        subject_match = re.match(r'New match:\s*(.+?)\s+at\s+(.+)', subject)
        if subject_match:
            title = subject_match.group(1).strip()
            company = subject_match.group(2).strip()
            job_id = _make_job_id("wtj", f"{company}:{title}")

            # Try to get salary from body snippet
            salary_min, salary_max = None, None
            sal_match = re.search(r'Salary:\s*(\$[\d\-,KkMm\s]+(?:OTE)?)', body)
            if sal_match:
                salary_min, salary_max = _parse_salary_k(sal_match.group(1))

            # Try to get location
            location = ""
            loc_match = re.search(
                r'(?:Remote|Denver|Colorado|United States|USA)[\w\s()]*',
                body, re.IGNORECASE
            )
            if loc_match:
                location = loc_match.group(0).strip()

            jobs.append(Job(
                job_id=job_id, title=title, company=company, url="",
                source="wtj", posted_date=email_date,
                salary_min=salary_min, salary_max=salary_max,
                location=location, description="",
                company_stage=None, company_size=None, industry=None,
            ))

    return jobs


def _make_job_id(source: str, key: str) -> str:
    """Generate a deterministic job ID from source + key."""
    return hashlib.md5(f"{source}:{key}".lower().encode()).hexdigest()[:12]


def _parse_salary_k(text: str):
    """Parse salary strings like '$250-333K' or '$304K' into integers."""
    # $250-333K or $250K-$333K
    match = re.search(r'\$(\d+)\s*-\s*\$?(\d+)\s*K', text, re.IGNORECASE)
    if match:
        return int(match.group(1)) * 1000, int(match.group(2)) * 1000
    # $304K single
    match = re.search(r'\$(\d+)\s*K', text, re.IGNORECASE)
    if match:
        val = int(match.group(1)) * 1000
        return val, val
    # $140,000-$200,000
    match = re.search(r'\$([\d,]+)\s*-\s*\$([\d,]+)', text)
    if match:
        return int(match.group(1).replace(',', '')), int(match.group(2).replace(',', ''))
    # $150000 single
    match = re.search(r'\$([\d,]+)', text)
    if match:
        val = int(match.group(1).replace(',', ''))
        if val > 10000:
            return val, val
    return None, None


def _parse_wtj_html(body: str, email_date: str) -> List[Job]:
    """Parse WTJ HTML email body.

    Company names and job titles alternate in <strong> tags.
    Salary info appears as "Salary: $250-333K OTE".
    Locations appear in small font spans.
    """
    jobs = []

    # Extract all strong tag contents
    strongs = re.findall(r'<strong>\s*(.*?)\s*</strong>', body, re.DOTALL)
    strongs = [re.sub(r'<[^>]+>', '', s).strip().replace('\r', '').replace('\n', ' ')
               for s in strongs if s.strip() and len(s.strip()) > 1]

    # Filter out boilerplate strongs
    strongs = [s for s in strongs if s
               and "posted" not in s.lower()
               and "new job" not in s.lower()
               and "matching" not in s.lower()
               and "preferences" not in s.lower()]

    # Extract salary info
    salaries = re.findall(r'Salary:\s*(.*?)(?:<|$)', body)
    salaries = [re.sub(r'<[^>]+>', '', s).strip() for s in salaries]

    # Extract locations (small font spans with location-like text)
    locations = re.findall(r'<span style="font-size:13px">(.*?)</span>', body)
    locations = [re.sub(r'<[^>]+>', '', l).strip() for l in locations
                 if l.strip() and any(kw in l.lower() for kw in
                                       ("remote", "denver", "colorado", "us", "united states",
                                        "new york", "san francisco", "chicago", "austin"))]

    # Pair strongs as (company, title) - they alternate
    i = 0
    job_idx = 0
    while i + 1 < len(strongs):
        company = strongs[i]
        title = strongs[i + 1]

        if not company or not title:
            i += 1
            continue

        salary_min, salary_max = None, None
        if job_idx < len(salaries):
            salary_min, salary_max = _parse_salary_k(salaries[job_idx])

        location = locations[job_idx] if job_idx < len(locations) else ""

        job_id = _make_job_id("wtj", f"{company}:{title}")
        jobs.append(Job(
            job_id=job_id, title=title, company=company, url="",
            source="wtj", posted_date=email_date,
            salary_min=salary_min, salary_max=salary_max,
            location=location, description="",
            company_stage=None, company_size=None, industry=None,
        ))

        i += 2
        job_idx += 1

    return jobs


def _clean_html_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _clean_builtin_tracking_url(url: str) -> str:
    url = html.unescape(url)
    m = re.search(r'https:%2F%2Fbuiltin\.com%2Fjob%2F[^\s"<>]+', url, re.IGNORECASE)
    if m:
        clean = m.group(0)
        clean = clean.replace('https:%2F%2F', 'https://').replace('%2F', '/').replace('%3F', '?')
        clean = clean.split('?')[0]
        return clean
    return ''


def _dedupe_jobs(jobs: List[Job]) -> List[Job]:
    seen = set()
    out = []
    for job in jobs:
        key = (job.company.strip().lower(), job.title.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(job)
    return out


def parse_email(sender: str, body: str, email_date: str, subject: str = "") -> List[Job]:
    """Route email to the correct parser based on sender."""
    sender_lower = sender.lower()
    if 'builtin.com' in sender_lower or 'built in' in sender_lower:
        return parse_builtin_email(body, email_date)
    elif 'linkedin.com' in sender_lower and 'jobalerts' in sender_lower:
        return parse_linkedin_email(body, email_date)
    elif 'welcometothejungle' in sender_lower:
        return parse_wtj_email(body, subject, email_date)
    return []
