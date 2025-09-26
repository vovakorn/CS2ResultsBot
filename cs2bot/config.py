"""Configuration management for the CS2 bot."""

from dataclasses import dataclass


@dataclass
class BotConfig:
    """Basic configuration values for the bot."""

    hltv_base_url: str
    hltv_api_key: str | None = None
