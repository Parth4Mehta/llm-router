"""Interfaces for LLM provider adapters."""

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """Common interface that every LLM provider adapter must implement."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider's stable name."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return whether the provider can currently accept a request."""

    @abstractmethod
    def complete(self, prompt: str, **options: Any) -> str:
        """Send a prompt and return the provider's text response."""


__all__ = ["Provider"]
