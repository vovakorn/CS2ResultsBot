"""Utilities for fetching match results from the community HLTV API."""
from __future__ import annotations

from typing import Any, Dict, List

import requests

HLTV_RESULTS_URL = "https://hltv-api.vercel.app/api/results"
DEFAULT_LIMIT = 3


def fetch_results(limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    """Return the first ``limit`` match results from the HLTV API."""

    response = requests.get(HLTV_RESULTS_URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Unexpected HLTV API response format")

    if limit < 0:
        raise ValueError("limit must be non-negative")

    return data[:limit]
