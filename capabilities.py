"""Static task capabilities for approved models."""

from dataclasses import dataclass

from model_catalog import OPENROUTER_MODELS


@dataclass(frozen=True)
class ModelCapability:
    """Describes the tasks a model is intended to handle."""

    model: str
    tasks: tuple[str, ...]
    priority: int


MODEL_CAPABILITIES = {
    "openai/gpt-oss-120b:free": ModelCapability(
        model="openai/gpt-oss-120b:free",
        tasks=("general", "reasoning", "math", "planning", "writing"),
        priority=1,
    ),
    "openai/gpt-oss-20b:free": ModelCapability(
        model="openai/gpt-oss-20b:free",
        tasks=("general", "chat", "writing", "summarization"),
        priority=2,
    ),
    "google/gemma-4-31b-it:free": ModelCapability(
        model="google/gemma-4-31b-it:free",
        tasks=("general", "reasoning", "writing", "planning"),
        priority=3,
    ),
    "google/gemma-4-26b-a4b-it:free": ModelCapability(
        model="google/gemma-4-26b-a4b-it:free",
        tasks=("general", "chat", "writing", "summarization"),
        priority=4,
    ),
    "cohere/north-mini-code:free": ModelCapability(
        model="cohere/north-mini-code:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=1,
    ),
    "poolside/laguna-s-2.1:free": ModelCapability(
        model="poolside/laguna-s-2.1:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=2,
    ),
    "poolside/laguna-xs-2.1:free": ModelCapability(
        model="poolside/laguna-xs-2.1:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=3,
    ),
}


if set(MODEL_CAPABILITIES) != OPENROUTER_MODELS:
    raise RuntimeError("Capability map and approved model catalog are out of sync")


__all__ = ["MODEL_CAPABILITIES", "ModelCapability"]