"""JSONL Storage Layer"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from .models import Job, ScoringResult


class Storage:
    """Manage JSONL storage for jobs and results"""

    def __init__(self, cache_dir: str = "_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        self.jobs_file = self.cache_dir / "discovered-jobs.jsonl"
        self.scores_file = self.cache_dir / "scoring-results.jsonl"
        self.applied_file = self.cache_dir / "applied-jobs.jsonl"

    def _append_line(self, filepath: Path, data: dict) -> None:
        """Append a single JSON line to a file."""
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    def _read_lines(self, filepath: Path) -> List[dict]:
        """Read all JSON lines from a file. Returns empty list if file missing."""
        if not filepath.exists():
            return []
        results = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    results.append(json.loads(line))
        return results

    def save_job(self, job: Job) -> None:
        """Save a job to storage"""
        self._append_line(self.jobs_file, job.to_dict())

    def save_jobs(self, jobs: List[Job]) -> None:
        """Save multiple jobs"""
        for job in jobs:
            self.save_job(job)

    def load_jobs(self, source: Optional[str] = None) -> List[dict]:
        """Load jobs from storage, optionally filtered by source"""
        jobs = self._read_lines(self.jobs_file)
        if source is not None:
            jobs = [j for j in jobs if j.get("source") == source]
        return jobs

    def save_score(self, score: ScoringResult) -> None:
        """Save a scoring result"""
        self._append_line(self.scores_file, score.to_dict())

    def load_scores(self) -> List[dict]:
        """Load all scoring results"""
        return self._read_lines(self.scores_file)

    def mark_applied(self, job_id: str) -> None:
        """Mark a job as already applied"""
        record = {
            "job_id": job_id,
            "applied_at": datetime.now().isoformat(),
        }
        self._append_line(self.applied_file, record)

    def is_applied(self, job_id: str) -> bool:
        """Check if we've already applied to this job"""
        records = self._read_lines(self.applied_file)
        return any(r.get("job_id") == job_id for r in records)

    def deduplicate_jobs(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicate jobs (same URL or fuzzy company+title match)"""
        seen_urls = set()
        seen_company_title = set()
        unique = []

        for job in jobs:
            url = job.url.strip().lower() if job.url else ""
            company_title = (
                job.company.strip().lower() + "|" + job.title.strip().lower()
            )

            if url and url in seen_urls:
                continue
            if company_title in seen_company_title:
                continue

            if url:
                seen_urls.add(url)
            seen_company_title.add(company_title)
            unique.append(job)

        return unique

    def get_job_by_id(self, job_id: str) -> Optional[dict]:
        """Find a specific job by ID"""
        jobs = self._read_lines(self.jobs_file)
        for job in jobs:
            if job.get("job_id") == job_id:
                return job
        return None

    def get_unscored_jobs(self) -> List[dict]:
        """Return jobs that don't have a scoring result yet"""
        jobs = self.load_jobs()
        scores = self.load_scores()
        scored_ids = {s.get("job_id") for s in scores}
        return [j for j in jobs if j.get("job_id") not in scored_ids]
