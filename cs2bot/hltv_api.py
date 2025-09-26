"""Utilities for interacting with the HLTV API."""


class HLTVApiClient:
    """Client for retrieving data from the HLTV API."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def fetch_latest_results(self) -> list[dict]:
        """Fetch the latest match results.

        This is a placeholder implementation that should be replaced with real
        network calls to the HLTV API.
        """
        raise NotImplementedError("HLTV API integration not implemented yet.")
