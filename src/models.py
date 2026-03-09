"""Data Models for Job Discovery System"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, List
import json

@dataclass
class Job:
    """Job posting"""
    job_id: str                    # Unique ID (URL hash)
    title: str
    company: str
    url: str
    source: str                    # "linkedin", "wtj", "company-website"
    posted_date: str               # ISO format YYYY-MM-DD
    salary_min: Optional[int]      # e.g., 250000
    salary_max: Optional[int]      # e.g., 300000
    location: str
    description: str
    company_stage: Optional[str]   # "seed", "series_a", "series_b", "late_stage"
    company_size: Optional[int]    # headcount estimate
    industry: Optional[str]
    job_type: str = "Full-time"
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class ScoringResult:
    """Scoring result for a job"""
    job_id: str
    total_score: float             # 0-100
    role_match_score: float        # 0-100
    compensation_score: float
    stage_score: float
    market_position_score: float
    growth_opportunity_score: float
    gtm_complexity_score: float
    matched_resume: str            # "growth_stage_hybrid", "revenue_leader", etc.
    breakdown: Dict[str, float] = field(default_factory=dict)
    passed_filters: bool = True
    filter_failures: List[str] = field(default_factory=list)
    scored_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class CompanyResearch:
    """Company research data"""
    company_name: str
    crunchbase_url: Optional[str]
    summary: str
    recent_news: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    hiring_managers: List[Dict] = field(default_factory=list)  # {name, title, linkedin_url}
    glassdoor_rating: Optional[float] = None
    culture_signals: List[str] = field(default_factory=list)
    researched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class EmailDelivery:
    """Email delivery record"""
    job_id: str
    email_type: str                # "daily_digest", "immediate_alert"
    recipient: str
    sent_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"        # "pending", "sent", "failed"
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
