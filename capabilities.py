"""Static task capabilities for approved models."""

from dataclasses import dataclass

from model_catalog import GROQ_MODELS, MISTRAL_MODELS, OPENROUTER_MODELS


@dataclass(frozen=True)
class ModelCapability:
    """Describes the tasks a model is intended to handle."""

    provider: str
    model: str
    tasks: tuple[str, ...]
    priority: int
    modality: str = "text"
    context_window: str = "unknown"
    rationale: str = ""


MODEL_CAPABILITIES = {
    "openai/gpt-oss-120b:free": ModelCapability(
        provider="openrouter",
        model="openai/gpt-oss-120b:free",
        tasks=("general", "reasoning", "math", "planning", "writing"),
        priority=1,
        context_window="131K",
        rationale="Large general-purpose free model for reasoning and planning.",
    ),
    "openai/gpt-oss-20b:free": ModelCapability(
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        tasks=("general", "chat", "writing", "summarization"),
        priority=2,
        context_window="131K",
        rationale="Smaller general-purpose free model for routine requests.",
    ),
    "google/gemma-4-31b-it:free": ModelCapability(
        provider="openrouter",
        model="google/gemma-4-31b-it:free",
        tasks=("general", "reasoning", "writing", "planning"),
        priority=3,
        modality="text+image",
        context_window="262K",
        rationale="General multimodal model listed with text and image support.",
    ),
    "google/gemma-4-26b-a4b-it:free": ModelCapability(
        provider="openrouter",
        model="google/gemma-4-26b-a4b-it:free",
        tasks=("general", "chat", "writing", "summarization"),
        priority=4,
        modality="text+image",
        context_window="262K",
        rationale="Efficient multimodal model for general requests.",
    ),
    "cohere/north-mini-code:free": ModelCapability(
        provider="openrouter",
        model="cohere/north-mini-code:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=1,
        context_window="256K",
        rationale="Catalog identifies this model as text/code focused.",
    ),
    "poolside/laguna-s-2.1:free": ModelCapability(
        provider="openrouter",
        model="poolside/laguna-s-2.1:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=2,
        context_window="262K",
        rationale="Catalog identifies this model as text/code focused.",
    ),
    "poolside/laguna-xs-2.1:free": ModelCapability(
        provider="openrouter",
        model="poolside/laguna-xs-2.1:free",
        tasks=("coding", "code-review", "technical-writing"),
        priority=3,
        context_window="262K",
        rationale="Catalog identifies this model as text/code focused.",
    ),
    "openai/gpt-oss-120b": ModelCapability(
        provider="groq",
        model="openai/gpt-oss-120b",
        tasks=("general", "reasoning", "math", "planning", "writing"),
        priority=1,
        context_window="131K",
        rationale="Large general-purpose model; Groq catalog lists text support.",
    ),
    "openai/gpt-oss-20b": ModelCapability(
        provider="groq",
        model="openai/gpt-oss-20b",
        tasks=("general", "chat", "writing", "summarization"),
        priority=2,
        context_window="131K",
        rationale="Smaller general-purpose model for routine requests.",
    ),
    "groq/compound": ModelCapability(
        provider="groq",
        model="groq/compound",
        tasks=("general", "reasoning", "planning", "research"),
        priority=3,
        context_window="131K",
        rationale="Groq compound model for general and multi-step workflows.",
    ),
    "groq/compound-mini": ModelCapability(
        provider="groq",
        model="groq/compound-mini",
        tasks=("general", "chat", "summarization"),
        priority=4,
        context_window="131K",
        rationale="Smaller compound model for routine workflows.",
    ),
    "qwen/qwen3.6-27b": ModelCapability(
        provider="groq",
        model="qwen/qwen3.6-27b",
        tasks=("general", "reasoning", "coding", "writing"),
        priority=3,
        context_window="131K",
        rationale="General text model with coding and reasoning suitability.",
    ),
    "mistral-medium-3-5": ModelCapability(
        provider="mistral",
        model="mistral-medium-3-5",
        tasks=("general", "reasoning", "math", "planning", "coding"),
        priority=1,
        modality="text+image+code",
        context_window="256K",
        rationale="Mistral describes it as frontier-class and optimized for agentic/coding use.",
    ),
    "mistral-small-2603": ModelCapability(
        provider="mistral",
        model="mistral-small-2603",
        tasks=("general", "reasoning", "coding", "chat", "writing"),
        priority=2,
        modality="text+image+code",
        context_window="256K",
        rationale="Mistral describes it as an efficient instruct/reasoning/coding hybrid.",
    ),
    "codestral-2508": ModelCapability(
        provider="mistral",
        model="codestral-2508",
        tasks=("coding", "code-review", "technical-writing"),
        priority=1,
        modality="code",
        context_window="128K",
        rationale="Mistral lists Codestral as a specialized code model.",
    ),
}


APPROVED_MODELS = OPENROUTER_MODELS | GROQ_MODELS | MISTRAL_MODELS
if not set(MODEL_CAPABILITIES).issubset(APPROVED_MODELS):
    raise RuntimeError("Capability map contains a model outside the approved catalog")


__all__ = ["MODEL_CAPABILITIES", "ModelCapability"]