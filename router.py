"""Provider registration and deterministic candidate ranking."""

from collections.abc import Iterable
from dataclasses import dataclass

from capabilities import MODEL_CAPABILITIES
from health import HealthTracker
from providers import Provider


@dataclass(frozen=True)
class Candidate:
    """A provider eligible for a task, with its selection priority."""

    provider: Provider
    priority: int
    registration_order: int


class Router:
    """Choose an available provider using static task capabilities."""

    def __init__(
        self,
        providers: Iterable[Provider] = (),
        health: HealthTracker | None = None,
    ) -> None:
        self.providers = list(providers)
        self.health = health or HealthTracker()

    def register(self, provider: Provider) -> None:
        """Add a provider to the router's ordered provider list."""
        self.providers.append(provider)

    def select(self, task_type: str = "general") -> Provider:
        """Return the highest-priority available provider for a task."""
        candidates = self.rank(task_type)
        if candidates:
            return candidates[0].provider

        task = task_type.strip().lower()
        raise RuntimeError(f"No available provider supports task: {task}")

    def rank(self, task_type: str = "general") -> list[Candidate]:
        """Return available providers ordered by static task priority."""
        task = task_type.strip().lower()
        if not task:
            raise ValueError("task_type must not be empty")

        candidates: list[Candidate] = []
        for registration_order, provider in enumerate(self.providers):
            model = getattr(provider, "model", None)
            capability = MODEL_CAPABILITIES.get(model)
            if (
                capability
                and task in capability.tasks
                and provider.is_available()
                and self.health.can_use(provider)
            ):
                candidates.append(
                    Candidate(
                        provider=provider,
                        priority=capability.priority,
                        registration_order=registration_order,
                    )
                )

        candidates.sort(key=lambda candidate: (candidate.priority, candidate.registration_order))
        return candidates


__all__ = ["Candidate", "Router"]