"""Storage module for the CS2 bot."""

from collections.abc import Iterable


class StorageBackend:
    """Interface for persisting bot data."""

    def save_results(self, results: Iterable[dict]) -> None:
        """Persist match results to storage."""
        raise NotImplementedError

    def load_results(self) -> list[dict]:
        """Load match results from storage."""
        raise NotImplementedError
