#!/usr/bin/env python3
"""Job Discovery Pipeline

Modes:
  score-emails  Parse job alert emails (JSON from stdin), score, store results
  score-jobs    Score all unscored jobs in storage
  digest        Print top scored jobs as formatted table
  test          Run with mock data
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.storage import Storage
from src.scorer import Scorer
from src.email_scanner import parse_email
from src.models import Job, ScoringResult


def score_emails(config: Config, storage: Storage, scorer: Scorer):
    """Read parsed email jobs from stdin (JSON array), score and store them."""
    raw = sys.stdin.read().strip()
    if not raw:
        print("No input on stdin")
        return

    jobs_data = json.loads(raw)
    jobs = []
    for jd in jobs_data:
        jobs.append(Job(**jd))

    # Deduplicate against existing storage
    existing = storage.load_jobs()
    existing_ids = {j.get("job_id") for j in existing}
    new_jobs = [j for j in jobs if j.job_id not in existing_ids]
    new_jobs = storage.deduplicate_jobs(new_jobs)

    if not new_jobs:
        print(json.dumps({"new_jobs": 0, "scored": 0, "results": []}))
        return

    # Save and score
    storage.save_jobs(new_jobs)
    hard_filters = config.get_hard_filters()
    results = []
    for job in new_jobs:
        result = scorer.score_job(job, hard_filters)
        storage.save_score(result)
        results.append(result.to_dict())

    results.sort(key=lambda r: r["total_score"], reverse=True)
    output = {
        "new_jobs": len(new_jobs),
        "scored": len(results),
        "qualified": len([r for r in results if r["passed_filters"] and r["total_score"] >= 50]),
        "hot": len([r for r in results if r["total_score"] >= 95]),
        "results": results,
    }
    print(json.dumps(output, indent=2))


def score_unscored(config: Config, storage: Storage, scorer: Scorer):
    """Score any jobs in storage that haven't been scored yet."""
    unscored = storage.get_unscored_jobs()
    if not unscored:
        print(json.dumps({"unscored": 0, "results": []}))
        return

    hard_filters = config.get_hard_filters()
    results = []
    for jd in unscored:
        job = Job(**{k: v for k, v in jd.items() if k in Job.__dataclass_fields__})
        result = scorer.score_job(job, hard_filters)
        storage.save_score(result)
        results.append(result.to_dict())

    results.sort(key=lambda r: r["total_score"], reverse=True)
    print(json.dumps({"scored": len(results), "results": results}, indent=2))


def digest(storage: Storage):
    """Print current pipeline digest."""
    jobs = storage.load_jobs()
    scores = storage.load_scores()

    # Build job lookup
    job_lookup = {j["job_id"]: j for j in jobs}

    # Sort scores
    scores.sort(key=lambda s: s.get("total_score", 0), reverse=True)

    qualified = [s for s in scores if s.get("passed_filters") and s.get("total_score", 0) >= 50]
    hot = [s for s in scores if s.get("total_score", 0) >= 95]

    output = {
        "total_discovered": len(jobs),
        "total_scored": len(scores),
        "qualified": len(qualified),
        "hot": len(hot),
        "top_10": [],
    }

    for s in qualified[:10]:
        job = job_lookup.get(s["job_id"], {})
        output["top_10"].append({
            "score": s.get("total_score", 0),
            "company": job.get("company", "?"),
            "title": job.get("title", "?"),
            "location": job.get("location", "?"),
            "salary_max": job.get("salary_max"),
            "resume": s.get("matched_resume", "?"),
            "source": job.get("source", "?"),
        })

    print(json.dumps(output, indent=2))


def test_mode(config: Config, scorer: Scorer):
    """Run with mock data to verify scoring works."""
    from src.mock_data import MockDataGenerator
    mock_gen = MockDataGenerator()
    mock_jobs = mock_gen.generate_jobs(count=10)
    hard_filters = config.get_hard_filters()

    results = []
    for job in mock_jobs:
        result = scorer.score_job(job, hard_filters)
        results.append(result)

    results.sort(key=lambda r: r.total_score, reverse=True)
    print(f"Generated {len(mock_jobs)} mock jobs")
    print(f"Top 5:")
    for i, r in enumerate(results[:5]):
        job = mock_jobs[next(j for j, mj in enumerate(mock_jobs) if mj.job_id == r.job_id)]
        status = "PASS" if r.passed_filters else f"FAIL({','.join(r.filter_failures)})"
        print(f"  {i+1}. {r.total_score:5.1f} | {status:20s} | {r.matched_resume:20s} | {job.company} - {job.title}")


def main():
    parser = argparse.ArgumentParser(description="Job Discovery Pipeline")
    parser.add_argument("mode", choices=["score-emails", "score-jobs", "digest", "test"],
                        help="Pipeline mode")
    parser.add_argument("--config-dir", default=str(Path(__file__).parent / "_config"))
    parser.add_argument("--cache-dir", default=str(Path(__file__).parent / "_cache"))
    args = parser.parse_args()

    config = Config(config_dir=args.config_dir)
    storage = Storage(cache_dir=args.cache_dir)
    scorer = Scorer(
        weights=config.get_scoring_weights(),
        watchlist_companies=config.get_watchlist_company_names(),
    )

    if args.mode == "score-emails":
        score_emails(config, storage, scorer)
    elif args.mode == "score-jobs":
        score_unscored(config, storage, scorer)
    elif args.mode == "digest":
        digest(storage)
    elif args.mode == "test":
        test_mode(config, scorer)


if __name__ == "__main__":
    main()
