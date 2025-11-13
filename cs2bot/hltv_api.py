"""Helpers for fetching the latest CS2 results from the HLTV community API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import logging

import requests

HLTV_RESULTS_URL = "https://hltv-api.vercel.app/api/results"
DEFAULT_LIMIT = 3


class HLTVApiError(RuntimeError):
    """Raised when the HLTV API cannot be reached."""


@dataclass
class MatchResult:
    event: str
    map_score: str
    team1: str
    team2: str
    time: str
    match_id: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "MatchResult":
        return cls(
            event=payload.get("event", {}).get("name") or payload.get("event", "Unknown event"),
            map_score=payload.get("result", ""),
            team1=payload.get("team1", {}).get("name") or payload.get("team1", "Team 1"),
            team2=payload.get("team2", {}).get("name") or payload.get("team2", "Team 2"),
            time=payload.get("time", ""),
            match_id=str(payload.get("id", "")),
        )


def fetch_recent_results(limit: int = DEFAULT_LIMIT) -> List[MatchResult]:
    """Return up to ``limit`` recent match results from HLTV."""

    try:
        response = requests.get(HLTV_RESULTS_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - requests not tested
        logging.error("Failed to fetch HLTV results: %s", exc)
        raise HLTVApiError("Unable to reach HLTV API") from exc

    data = response.json()
    if not isinstance(data, list):
        raise HLTVApiError("Unexpected response format from HLTV API")

    matches: List[MatchResult] = []
    for raw in data[:limit]:
        matches.append(MatchResult.from_payload(raw))
    return matches


def format_match(result: MatchResult) -> str:
    """Compose a human-readable message for Telegram."""

    headline = f"{result.team1} vs {result.team2}"
    pieces = [headline]
    if result.map_score:
        pieces.append(f"Score: {result.map_score}")
    if result.event:
        pieces.append(f"Event: {result.event}")
    if result.time:
        pieces.append(f"Time: {result.time}")
    if result.match_id:
        pieces.append(f"Match ID: {result.match_id}")
    return "\n".join(pieces)
