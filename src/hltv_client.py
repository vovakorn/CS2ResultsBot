"""Minimal HLTV API client for fetching CS2 match results."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests

BASE_URL = "https://hltv-api.vercel.app"
RESULTS_PATH = "/api/results"
TIMEOUT = 5  # seconds


class HLTVClientError(RuntimeError):
    """Raised when the HLTV API cannot be reached or returns invalid data."""


def fetch_results(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch the latest CS2 match results from the HLTV API.

    Args:
        limit: Optionally limit the number of returned results.

    Returns:
        A list of dictionaries describing the latest CS2 match results.

    Raises:
        HLTVClientError: If the API call fails or returns invalid data.
    """

    url = f"{BASE_URL}{RESULTS_PATH}"
    logging.debug("Requesting HLTV results", extra={"url": url, "limit": limit})

    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - defensive
        logging.exception("Failed to fetch HLTV results")
        raise HLTVClientError("Failed to fetch HLTV results") from exc

    try:
        data = response.json()
    except ValueError as exc:  # pragma: no cover - defensive
        logging.exception("HLTV API returned non-JSON response")
        raise HLTVClientError("HLTV API returned invalid JSON") from exc

    if not isinstance(data, list):
        logging.error("Unexpected HLTV API response format: %s", data)
        raise HLTVClientError("HLTV API returned unexpected response format")

    if limit is not None:
        return data[:limit]
    return data
