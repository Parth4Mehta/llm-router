"""Basic provider registration and selection."""

from collections.abc import Iterable

from providers import Provider


class Router:
    """Route requests to the first currently available provider."""

    def __init__(self, providers: Iterable[Provider] = ()) -> None:
        self.providers = list(providers)

    def register(self, provider: Provider) -> None:
        """Add a provider to the router's ordered provider list."""
        self.providers.append(provider)

    def select(self) -> Provider:
        """Return the first available provider.

        Task-aware selection and fallback behavior will be added later.
        """
        for provider in self.providers:
            if provider.is_available():
                return provider

        raise RuntimeError("No available LLM provider")


__all__ = ["Router"]