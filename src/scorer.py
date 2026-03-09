"""Scoring Algorithm"""

import re
from typing import Tuple, Dict, List, Optional
from .models import Job, ScoringResult


class Scorer:
    """Score jobs based on fit"""

    def __init__(self, weights: dict = None, watchlist_companies: dict = None):
        """Initialize with scoring weights and watchlist.

        Args:
            weights: Dict of dimension -> weight (should sum to 1.0)
            watchlist_companies: Dict of company_name_lower -> tier_number (1, 2, or 3)
        """
        self.weights = weights or {
            "role_match": 0.30,
            "compensation": 0.20,
            "company_stage": 0.15,
            "market_position": 0.15,
            "growth_opportunity": 0.10,
            "gtm_complexity": 0.10,
        }
        self.watchlist_companies = watchlist_companies or {}

    def score_job(self, job: Job, hard_filters: dict = None) -> ScoringResult:
        """Score a single job.

        Args:
            job: Job dataclass instance
            hard_filters: Dict with optional keys:
                - min_compensation (int)
                - locations_allowed (List[str])
                - industries_exclude (List[str])
        """
        filters = hard_filters or {}

        # 1. Apply hard filters
        passed, failures = self._apply_hard_filters(job, filters)

        # 2. Score each dimension
        role_match = self._score_role_match(job)
        compensation = self._score_compensation(job)
        company_stage = self._score_company_stage(job)
        market_position = self._score_market_position(job)
        growth_opportunity = self._score_growth_opportunity(job)
        gtm_complexity = self._score_gtm_complexity(job)

        # 3. Calculate weighted total
        total_score = (
            role_match * self.weights["role_match"]
            + compensation * self.weights["compensation"]
            + company_stage * self.weights["company_stage"]
            + market_position * self.weights["market_position"]
            + growth_opportunity * self.weights["growth_opportunity"]
            + gtm_complexity * self.weights["gtm_complexity"]
        )

        # 4. Pick resume
        matched_resume = self._pick_resume(job)

        breakdown = {
            "role_match": role_match,
            "compensation": compensation,
            "company_stage": company_stage,
            "market_position": market_position,
            "growth_opportunity": growth_opportunity,
            "gtm_complexity": gtm_complexity,
        }

        return ScoringResult(
            job_id=job.job_id,
            total_score=round(total_score, 2),
            role_match_score=role_match,
            compensation_score=compensation,
            stage_score=company_stage,
            market_position_score=market_position,
            growth_opportunity_score=growth_opportunity,
            gtm_complexity_score=gtm_complexity,
            matched_resume=matched_resume,
            breakdown=breakdown,
            passed_filters=passed,
            filter_failures=failures,
        )

    def _score_role_match(self, job: Job) -> float:
        """Score how well the role matches target roles."""
        title = job.title.lower()

        if any(kw in title for kw in ("vp", "vice president", "director", "head of")):
            return 100.0
        if any(kw in title for kw in ("enterprise ae", "enterprise account")):
            return 90.0
        if "strategic" in title:
            return 80.0
        if any(kw in title for kw in ("gtm", "go-to-market")):
            return 70.0
        if any(kw in title for kw in ("sales manager", "regional")):
            return 60.0
        return 40.0

    def _score_compensation(self, job: Job, min_target: int = 250000) -> float:
        """Score compensation."""
        salary = job.salary_max if job.salary_max is not None else job.salary_min

        if salary is None:
            return 50.0
        if salary >= 300000:
            return 100.0
        if salary >= 250000:
            return 80.0
        if salary >= 200000:
            return 50.0
        return 0.0

    def _score_company_stage(self, job: Job) -> float:
        """Score company stage."""
        stage = (job.company_stage or "").lower().strip()

        if not stage:
            return 60.0
        if stage in ("series_c", "series_d", "late_stage", "public"):
            return 100.0
        if stage == "series_b":
            return 90.0
        if stage == "series_a":
            return 80.0
        if stage == "seed":
            return 60.0
        if stage in ("pre_seed", "pre-seed"):
            return 40.0
        return 60.0

    def _score_market_position(self, job: Job) -> float:
        """Score market position based on watchlist tier."""
        company_lower = job.company.lower().strip()
        tier = self.watchlist_companies.get(company_lower)

        if tier == 1:
            return 100.0
        if tier == 2:
            return 75.0
        if tier == 3:
            return 60.0
        return 50.0

    def _score_growth_opportunity(self, job: Job) -> float:
        """Score growth/opportunity signals."""
        stage = (job.company_stage or "").lower().strip()
        size = job.company_size

        late_stages = ("series_c", "series_d", "late_stage", "public")

        if size is not None and size > 500 and stage in late_stages:
            return 100.0
        if size is not None and 100 <= size <= 500:
            return 80.0
        if size is not None and size < 100:
            return 70.0
        return 60.0

    def _score_gtm_complexity(self, job: Job) -> float:
        """Score GTM complexity (enterprise + technical = higher)."""
        title = job.title.lower()

        has_enterprise = "enterprise" in title
        has_leadership = any(kw in title for kw in ("director", "vp"))

        if has_enterprise and has_leadership:
            return 100.0
        if has_enterprise:
            return 85.0
        if "mid-market" in title:
            return 70.0
        if "smb" in title:
            return 50.0
        return 65.0

    def _pick_resume(self, job: Job) -> str:
        """Determine which resume best fits this job."""
        title = job.title.lower()
        stage = (job.company_stage or "").lower().strip()
        size = job.company_size

        is_leadership = any(kw in title for kw in ("vp", "director", "head"))
        is_enterprise = "enterprise" in title
        is_ae = any(kw in title for kw in ("ae", "account executive"))
        is_founding = "founding" in title

        if is_leadership and stage in ("series_b", "series_c"):
            return "growth_stage_hybrid"
        if is_enterprise and size is not None and size > 500:
            return "revenue_leader"
        if stage in ("seed", "series_a") and is_ae:
            return "early_stage_ae"
        if stage in ("pre_seed", "pre-seed", "seed") and is_founding:
            return "founding_ae"
        return "growth_stage_hybrid"

    def _apply_hard_filters(self, job: Job, filters: dict) -> Tuple[bool, List[str]]:
        """Check hard filters (compensation, location, industry).

        Returns:
            Tuple of (passed: bool, failures: list of failure reason strings)
        """
        failures = []

        # Compensation filter
        min_comp = filters.get("min_compensation")
        if min_comp is not None and job.salary_max is not None:
            if job.salary_max < min_comp:
                failures.append("comp_too_low")

        # Location filter
        locations_allowed = filters.get("locations_allowed")
        if locations_allowed is not None:
            job_location = (job.location or "").lower().strip()
            if job_location:
                matched = any(
                    loc.lower().strip() in job_location
                    for loc in locations_allowed
                )
                if not matched:
                    failures.append("location_mismatch")

        # Industry exclusion filter
        industries_exclude = filters.get("industries_exclude")
        if industries_exclude is not None:
            job_industry = (job.industry or "").lower().strip()
            if job_industry:
                excluded = any(
                    ind.lower().strip() == job_industry
                    for ind in industries_exclude
                )
                if excluded:
                    failures.append("excluded_industry")

        passed = len(failures) == 0
        return (passed, failures)
