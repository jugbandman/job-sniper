"""Welcome to the Jungle Job Discovery (stub)"""

from typing import List
from .models import Job

class WTJScraper:
    """Scrape Welcome to the Jungle for tech jobs"""
    
    def __init__(self):
        # TODO: Initialize WTJ API client (if available)
        # Otherwise use browser scraping
        pass
    
    def search_jobs(
        self,
        keywords: str,
        location: str = "United States",
        limit: int = 100
    ) -> List[Job]:
        """Search WTJ for jobs"""
        # TODO: Implement
        # 1. Call WTJ API or scrape search results
        # 2. Filter by tech keywords
        # 3. Parse → Job objects
        # 4. Return list
        return []
    
    def search_by_company(self, company_name: str, limit: int = 50) -> List[Job]:
        """Search for jobs at specific company"""
        # TODO: Implement
        return []
    
    def search_by_location(self, location: str, limit: int = 100) -> List[Job]:
        """Search by location"""
        # TODO: Implement
        return []
    
    def _parse_job_posting(self, posting: dict) -> Job:
        """Parse WTJ posting → Job object"""
        # TODO: Implement
        return None
