"""Basic provider registration and selection."""

from collections.abc import Iterable

from capabilities import MODEL_CAPABILITIES
from providers import Provider


class Router:
    """Choose an available provider using static task capabilities."""

    def __init__(self, providers: Iterable[Provider] = ()) -> None:
        self.providers = list(providers)

    def register(self, provider: Provider) -> None:
        """Add a provider to the router's ordered provider list."""
        self.providers.append(provider)

    def select(self, task_type: str = "general") -> Provider:
        """Return the highest-priority available provider for a task."""
        task = task_type.strip().lower()
        if not task:
            raise ValueError("task_type must not be empty")

        candidates: list[tuple[int, int, Provider]] = []
        for registration_order, provider in enumerate(self.providers):
            model = getattr(provider, "model", None)
            capability = MODEL_CAPABILITIES.get(model)
            if capability and task in capability.tasks and provider.is_available():
                candidates.append((capability.priority, registration_order, provider))

        if candidates:
            candidates.sort(key=lambda candidate: (candidate[0], candidate[1]))
            return candidates[0][2]

        raise RuntimeError(f"No available provider supports task: {task}")


__all__ = ["Router"]