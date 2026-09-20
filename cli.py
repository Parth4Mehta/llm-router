"""Small command-line entry point for testing a configured provider."""

import argparse

from capabilities import MODEL_CAPABILITIES
from providers import GroqProvider, MistralProvider, OpenRouterProvider, Provider
from router import Router


DEFAULT_MODELS = {
    "groq": "openai/gpt-oss-120b",
    "mistral": "mistral-small-2603",
    "openrouter": "openai/gpt-oss-120b:free",
}

PROVIDERS = {
    "groq": GroqProvider,
    "mistral": MistralProvider,
    "openrouter": OpenRouterProvider,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send one prompt to an LLM provider")
    parser.add_argument("prompt", help="Prompt to send")
    parser.add_argument(
        "--provider",
        choices=PROVIDERS,
        help="Explicit provider override; omit to route automatically",
    )
    parser.add_argument("--model", help="Approved model ID; defaults by provider")
    return parser.parse_args()


def configured_providers() -> list[Provider]:
    """Build adapters for the curated models in the capability registry."""
    return [
        PROVIDERS[capability.provider](model=capability.model)
        for capability in MODEL_CAPABILITIES.values()
        if capability.provider in PROVIDERS
    ]


def main() -> None:
    args = parse_args()
    if args.provider:
        model = args.model or DEFAULT_MODELS[args.provider]
        provider: Provider = PROVIDERS[args.provider](model=model)
        if not provider.is_available():
            raise SystemExit(f"{provider.name} API key is missing from .env")
        print(provider.complete(args.prompt))
        return

    if args.model:
        raise SystemExit("--model requires --provider")
    print(Router(configured_providers()).ask(args.prompt))


if __name__ == "__main__":
    main()