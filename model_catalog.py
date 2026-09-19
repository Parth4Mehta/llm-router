"""Models allowed by llm-router.

Source: https://github.com/mnfst/awesome-free-llm-apis
This small catalog is intentionally explicit and should be refreshed when the
source repository changes.
"""

MODEL_SOURCE_URL = "https://github.com/mnfst/awesome-free-llm-apis"
MODEL_SOURCE_DATE = "2026-09-20"

OPENROUTER_MODELS = frozenset(
    {
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free",
        "google/gemma-4-31b-it:free",
        "google/gemma-4-26b-a4b-it:free",
        "cohere/north-mini-code:free",
        "poolside/laguna-s-2.1:free",
        "poolside/laguna-xs-2.1:free",
    }
)

MISTRAL_MODELS = frozenset(
    {
        "mistral-medium-3-5",
        "mistral-small-2603",
        "mistral-large-2512",
        "ministral-8b-2512",
        "codestral-2508",
        "ministral-3b-2512",
        "ministral-14b-2512",
    }
)

GROQ_MODELS = frozenset(
    {
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "groq/compound",
        "groq/compound-mini",
        "qwen/qwen3.6-27b",
    }
)


__all__ = [
    "GROQ_MODELS",
    "MISTRAL_MODELS",
    "MODEL_SOURCE_DATE",
    "MODEL_SOURCE_URL",
    "OPENROUTER_MODELS",
]