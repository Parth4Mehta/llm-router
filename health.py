"""Small in-memory health and quota tracker."""

from dataclasses import dataclass
import time
from collections.abc import Callable, Mapping


@dataclass
class ProviderStatus:
    """Runtime counters for one provider."""

    requests: int = 0
    successes: int = 0
    failures: int = 0
    quota_used: int = 0
    unavailable_until: float = 0.0


class HealthTracker:
    """Track provider health and optional request quotas in memory."""

    def __init__(
        self,
        quotas: Mapping[str, int] | None = None,
        cooldown_seconds: float = 30.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.quotas = dict(quotas or {})
        self.cooldown_seconds = cooldown_seconds
        self.clock = clock
        self._statuses: dict[str, ProviderStatus] = {}

    def can_use(self, provider: object) -> bool:
        """Return whether a provider is healthy and below its quota."""
        status = self.status(provider)
        if self.clock() < status.unavailable_until:
            return False
        limit = self.quotas.get(self._key(provider))
        return limit is None or status.quota_used < limit

    def record_request(self, provider: object) -> None:
        status = self.status(provider)
        status.requests += 1
        status.quota_used += 1

    def record_success(self, provider: object) -> None:
        status = self.status(provider)
        status.successes += 1
        status.unavailable_until = 0.0

    def record_failure(self, provider: object) -> None:
        status = self.status(provider)
        status.failures += 1
        status.unavailable_until = self.clock() + self.cooldown_seconds

    def status(self, provider: object) -> ProviderStatus:
        key = self._key(provider)
        return self._statuses.setdefault(key, ProviderStatus())

    @staticmethod
    def _key(provider: object) -> str:
        return str(getattr(provider, "name", type(provider).__name__))


__all__ = ["HealthTracker", "ProviderStatus"]