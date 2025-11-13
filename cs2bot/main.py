"""Entry point for Yandex Cloud Functions."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Iterable, List, Sequence

import requests

from .config import CHANNELS, TELEGRAM_TOKEN
from .hltv_api import HLTVApiError, MatchResult, fetch_recent_results as fetch_results

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org"
TELEGRAM_METHOD = "sendMessage"
MIN_MATCHES = 1
MAX_MATCHES = 3


def send_to_telegram(chat_id: str, text: str, timeout: int = 7) -> Dict[str, Any]:
    """Send ``text`` to ``chat_id`` via Telegram Bot API."""

    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is not configured")

    url = f"{TELEGRAM_API_URL}/bot{TELEGRAM_TOKEN}/{TELEGRAM_METHOD}"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _get_attr(obj: Any, key: str, default: str = "") -> str:
    if hasattr(obj, key):  # dataclass MatchResult
        value = getattr(obj, key)
        if value is not None:
            return str(value)
    if isinstance(obj, dict):
        value = obj.get(key)
        if value is not None:
            return str(value)
    return default


def format_match(match: MatchResult) -> str:
    """Convert a match result into a multi-line Telegram message."""

    team1 = _get_attr(match, "team1", "Team 1")
    team2 = _get_attr(match, "team2", "Team 2")
    map_score = _get_attr(match, "map_score")
    event = _get_attr(match, "event")
    time = _get_attr(match, "time")
    match_id = _get_attr(match, "match_id")

    pieces: List[str] = [f"{team1} vs {team2}"]
    if map_score:
        pieces.append(f"Score: {map_score}")
    if event:
        pieces.append(f"Event: {event}")
    if time:
        pieces.append(f"Time: {time}")
    if match_id:
        pieces.append(f"Match ID: {match_id}")
    return "\n".join(pieces)


def _match_matches_channel(match: MatchResult, teams: Sequence[str] | None) -> bool:
    if not teams:
        return True
    team1 = _get_attr(match, "team1").lower()
    team2 = _get_attr(match, "team2").lower()
    match_teams = {team1, team2}
    for team in teams:
        if team and team.lower() in match_teams:
            return True
    return False


def _iter_channels() -> Iterable[Dict[str, Any]]:
    for channel in CHANNELS:
        chat_id = channel.get("chat_id")
        if not chat_id:
            logger.warning("Skipping channel without chat_id: %s", channel)
            continue
        yield channel


def handler(event: Dict[str, Any] | None, context: Any) -> Dict[str, Any]:
    """Yandex Cloud Functions entry point."""

    limit = MAX_MATCHES
    if isinstance(event, dict):
        requested = event.get("limit")
        if isinstance(requested, int):
            limit = max(MIN_MATCHES, min(MAX_MATCHES, requested))

    try:
        matches = fetch_results(limit=limit)
    except HLTVApiError as exc:
        logger.error("Failed to fetch results: %s", exc)
        return {"statusCode": 502, "body": json.dumps({"error": str(exc)})}

    channel_stats: Dict[str, int] = {}
    sent_messages = 0
    for channel in _iter_channels():
        name = channel.get("name", "unknown")
        teams = channel.get("teams")
        filtered_matches = [m for m in matches if _match_matches_channel(m, teams)]
        channel_stats[name] = len(filtered_matches)
        for match in filtered_matches:
            text = format_match(match)
            send_to_telegram(channel["chat_id"], text)
            sent_messages += 1

    body = {
        "requested_limit": limit,
        "matches_received": len(matches),
        "messages_sent": sent_messages,
        "per_channel": channel_stats,
    }
    return {"statusCode": 200, "body": json.dumps(body)}
