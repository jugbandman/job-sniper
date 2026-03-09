"""Configuration Loader"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

class Config:
    """Load and manage configuration"""

    def __init__(self, config_dir: str = "_config"):
        self.config_dir = Path(config_dir)
        self.user_profile = self._load_json("user-profile.json")
        self.scoring_weights = self._load_yaml("scoring-weights.yaml")
        self.company_watchlist = self._load_yaml("company-watchlist.yaml")
        self.email_config = self._load_yaml("email-config.yaml")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON config file"""
        path = self.config_dir / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return json.load(f)

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML config file"""
        path = self.config_dir / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    def get_scoring_weights(self) -> Dict[str, float]:
        """Get scoring weights"""
        defaults = {
            "role_match": 0.30,
            "compensation": 0.20,
            "company_stage": 0.15,
            "market_position": 0.15,
            "growth_opportunity": 0.10,
            "gtm_complexity": 0.10,
        }
        return self.scoring_weights.get("weights", defaults)

    def get_hard_filters(self) -> Dict:
        """Get hard filters (comp, location, industry)"""
        defaults = {
            "min_compensation": 250000,
            "locations_allowed": ["remote", "denver", "colorado"],
            "industries_exclude": ["finance", "insurance", "accounting"],
        }
        return self.scoring_weights.get("hard_filters", defaults)

    def get_thresholds(self) -> Dict:
        """Get scoring thresholds"""
        defaults = {
            "daily_digest_min_score": 50,
            "immediate_alert_min_score": 95,
            "top_n_daily": 10,
        }
        return self.scoring_weights.get("thresholds", defaults)

    def get_watchlist_companies(self, tier: Optional[str] = None) -> List[Dict]:
        """Get companies from watchlist, optionally filtered by tier"""
        if not self.company_watchlist:
            return []

        results = []
        tier_map = {
            "1": "tier_1_direct_competitors",
            "2": "tier_2_adjacent_markets",
            "3": "tier_3_great_companies",
        }

        if tier and tier in tier_map:
            companies = self.company_watchlist.get(tier_map[tier], [])
            for c in companies:
                c["tier"] = int(tier)
            return companies

        for tier_key, tier_num in [("tier_1_direct_competitors", 1),
                                    ("tier_2_adjacent_markets", 2),
                                    ("tier_3_great_companies", 3)]:
            for c in self.company_watchlist.get(tier_key, []):
                c["tier"] = tier_num
                results.append(c)
        return results

    def get_watchlist_company_names(self) -> Dict[str, int]:
        """Get company name -> tier mapping for quick lookup"""
        result = {}
        for company in self.get_watchlist_companies():
            result[company["name"].lower()] = company.get("tier", 3)
        return result
