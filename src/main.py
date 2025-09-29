"""Entry point for the Yandex Cloud Function handler."""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Iterable

import requests

from .hltv_client import HLTVClientError, fetch_results

logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
MAX_POSTS = int(os.environ.get("MAX_POSTS", "3"))


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing."""


def _build_message(entry: Dict[str, Any]) -> str:
    team1 = entry.get("team1", {}).get("name", "Unknown")
    team2 = entry.get("team2", {}).get("name", "Unknown")
    score = entry.get("result", "?")
    map_played = entry.get("maps", "?")
    date = entry.get("date", "?")

    return (
        f"🆚 <b>{team1}</b> vs <b>{team2}</b>\n"
        f"📅 {date}\n"
        f"🗺 {map_played} — {score}\n"
        "Источник: HLTV"
    )


def _send_messages(token: str, chat_id: str, messages: Iterable[str]) -> None:
    url = TELEGRAM_API_TEMPLATE.format(token=token)
    for text in messages:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        logging.info("Sending message to Telegram", extra={"chat_id": chat_id})
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()


def handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Yandex Cloud Function entrypoint."""

    logging.info("Function started")
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logging.error("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID")
        raise ConfigurationError("Missing Telegram configuration")

    try:
        results = fetch_results(limit=MAX_POSTS)
    except HLTVClientError as exc:
        logging.error("Failed to fetch results: %s", exc)
        return {"statusCode": 502, "body": json.dumps({"error": str(exc)})}

    if not results:
        logging.info("No results returned by HLTV API")
        return {"statusCode": 200, "body": json.dumps({"message": "No results"})}

    messages = (_build_message(entry) for entry in results)

    try:
        _send_messages(token, chat_id, messages)
    except requests.RequestException as exc:
        logging.exception("Failed to send message to Telegram")
        return {"statusCode": 502, "body": json.dumps({"error": "Telegram API request failed"})}

    logging.info("Function completed successfully")
    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
