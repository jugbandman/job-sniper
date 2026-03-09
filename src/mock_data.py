"""Mock Data Generator for Testing"""

from .models import Job, ScoringResult
from datetime import datetime, timedelta
import random
import hashlib

class MockDataGenerator:
    """Generate realistic mock jobs for testing"""
    
    COMPANIES = [
        ("Atlassian", "series_d", 1000),
        ("Databricks", "series_d", 800),
        ("Stripe", "late_stage", 5000),
        ("Anthropic", "series_c", 400),
        ("Zapier", "series_d", 500),
        ("HashiCorp", "series_c", 600),
        ("Snyk", "series_d", 700),
        ("DataDog", "late_stage", 3000),
        ("HubSpot", "public", 4000),
        ("Notion", "series_b", 350),
    ]
    
    ROLES = [
        ("VP of Sales", 280000, 320000),
        ("Head of GTM", 250000, 300000),
        ("Enterprise Account Executive", 150000, 200000),
        ("Sales Director", 200000, 280000),
        ("Strategic Account Executive", 180000, 240000),
        ("GTM Manager", 140000, 180000),
        ("Account Executive", 100000, 160000),
    ]
    
    LOCATIONS = ["remote", "denver", "sf", "new york", "austin"]
    
    @staticmethod
    def generate_job(
        job_id: str = None,
        company: str = None,
        title: str = None,
        salary_min: int = None,
        salary_max: int = None
    ) -> Job:
        """Generate a single mock job"""
        
        if not company:
            company, stage, size = random.choice(MockDataGenerator.COMPANIES)
        
        if not title:
            title, sal_min, sal_max = random.choice(MockDataGenerator.ROLES)
            salary_min = salary_min or sal_min
            salary_max = salary_max or sal_max
        else:
            salary_min = salary_min or random.randint(150000, 300000)
            salary_max = salary_max or salary_min + random.randint(20000, 80000)
        
        location = random.choice(MockDataGenerator.LOCATIONS)
        url = f"https://linkedin.com/jobs/view/{random.randint(100000, 999999)}"
        
        if not job_id:
            job_id = hashlib.md5(url.encode()).hexdigest()
        
        return Job(
            job_id=job_id,
            title=title,
            company=company,
            url=url,
            source="mock",
            posted_date=(datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
            salary_min=salary_min,
            salary_max=salary_max,
            location=location,
            description=f"Mock job posting for {title} at {company}",
            company_stage=random.choice(["seed", "series_a", "series_b", "series_c", "series_d", "late_stage"]),
            company_size=random.randint(10, 5000),
            industry="Technology"
        )
    
    @staticmethod
    def generate_jobs(count: int = 10) -> list:
        """Generate multiple mock jobs"""
        return [MockDataGenerator.generate_job() for _ in range(count)]
    
    @staticmethod
    def generate_high_match_jobs(count: int = 3) -> list:
        """Generate jobs that should score high for Andy"""
        jobs = []
        for i in range(count):
            jobs.append(Job(
                job_id=f"high-match-{i}",
                title=random.choice(["VP of Sales", "Head of GTM", "Sales Director"]),
                company=random.choice(["Stripe", "Databricks", "Anthropic", "Zapier"]),
                url=f"https://linkedin.com/jobs/view/{1000000 + i}",
                source="mock",
                posted_date=datetime.now().strftime("%Y-%m-%d"),
                salary_min=280000,
                salary_max=320000,
                location=random.choice(["remote", "denver"]),
                description="High-quality job match",
                company_stage=random.choice(["series_c", "series_d", "late_stage"]),
                company_size=random.randint(500, 5000),
                industry="Technology"
            ))
        return jobs
