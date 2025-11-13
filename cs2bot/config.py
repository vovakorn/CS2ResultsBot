"""Configuration objects for Telegram channels and bot behavior."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List
import os

DEFAULT_MATCHES_PER_CHANNEL = 3
MAX_CHANNELS = 50


@dataclass
class TelegramChannel:
    """Settings required to send CS2 results to a Telegram channel."""

    name: str
    bot_token: str
    chat_id: str
    max_matches: int = DEFAULT_MATCHES_PER_CHANNEL

    def __post_init__(self) -> None:
        if not self.bot_token or not self.chat_id:
            raise ValueError(
                f"Channel '{self.name}' is missing bot token or chat id."
            )
        if self.max_matches < 1 or self.max_matches > 3:
            raise ValueError("max_matches must be between 1 and 3")


def load_channels() -> List[TelegramChannel]:
    """Read channel configuration from environment variables.

    The defaults below expect the user to set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
    for the single-channel setup. Additional channels can be added by extending the
    CHANNELS list (up to MAX_CHANNELS entries).
    """

    single_channel_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    single_channel_chat = os.getenv("TELEGRAM_CHAT_ID", "")

    channels: List[TelegramChannel] = []
    if single_channel_token and single_channel_chat:
        channels.append(
            TelegramChannel(
                name="primary",
                bot_token=single_channel_token,
                chat_id=single_channel_chat,
                max_matches=DEFAULT_MATCHES_PER_CHANNEL,
            )
        )
    return channels


# Placeholder list that can be extended manually when multiple channels are needed.
CHANNELS: List[TelegramChannel] = load_channels()
