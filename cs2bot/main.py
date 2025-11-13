"""Entry point for Yandex Cloud Functions."""
from __future__ import annotations

from typing import Any, Dict, List
import logging

import requests

from . import config
from .hltv_api import HLTVApiError, fetch_recent_results, format_match

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _send_to_telegram(channel: config.TelegramChannel, text: str) -> None:
    url = f"https://api.telegram.org/bot{channel.bot_token}/sendMessage"
    payload = {"chat_id": channel.chat_id, "text": text}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Yandex Cloud Functions handler."""

    channel_count = len(config.CHANNELS)
    if channel_count == 0:
        logger.warning("No Telegram channels configured.")
        return {"status": "no_channels"}
    if channel_count > config.MAX_CHANNELS:
        logger.error("Too many channels configured (max %s)", config.MAX_CHANNELS)
        return {"status": "too_many_channels"}

    requested_limit = None
    if isinstance(event, dict):
        requested_limit = event.get("limit")
    max_matches = config.DEFAULT_MATCHES_PER_CHANNEL
    if isinstance(requested_limit, int) and 1 <= requested_limit <= 3:
        max_matches = requested_limit

    try:
        results = fetch_recent_results(limit=max_matches)
    except HLTVApiError:
        return {"status": "hltv_error"}

    dispatched: List[str] = []
    for channel in config.CHANNELS:
        limit = min(channel.max_matches, len(results))
        for match in results[:limit]:
            text = format_match(match)
            try:
                _send_to_telegram(channel, text)
            except requests.RequestException as exc:  # pragma: no cover
                logger.error("Failed to send message to %s: %s", channel.name, exc)
                continue
        dispatched.append(channel.name)

    return {"status": "ok", "channels": dispatched, "matches": len(results)}
