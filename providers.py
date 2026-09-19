"""Interfaces for LLM provider adapters."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

from model_catalog import GROQ_MODELS, MISTRAL_MODELS, OPENROUTER_MODELS


load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True)


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


class OpenRouterProvider(Provider):
    """Adapter for OpenRouter's OpenAI-compatible chat completions API."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str = "https://openrouter.ai/api/v1",
        client: httpx.Client | None = None,
    ) -> None:
        if model not in OPENROUTER_MODELS:
            raise ValueError(
                "Model is not in the approved awesome-free-llm-apis catalog: "
                f"{model}"
            )
        self.model = model
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=60.0)

    @property
    def name(self) -> str:
        return "openrouter"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def complete(self, prompt: str, **options: Any) -> str:
        if not self.is_available():
            raise RuntimeError("OPENROUTER_API_KEY is not configured")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            **options,
        }
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise ValueError("OpenRouter returned an unexpected response") from error


class MistralProvider(Provider):
    """Adapter for Mistral's OpenAI-compatible chat completions API."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str = "https://api.mistral.ai/v1",
        client: httpx.Client | None = None,
    ) -> None:
        if model not in MISTRAL_MODELS:
            raise ValueError(
                "Model is not in the approved awesome-free-llm-apis catalog: "
                f"{model}"
            )
        self.model = model
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=60.0)

    @property
    def name(self) -> str:
        return "mistral"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def complete(self, prompt: str, **options: Any) -> str:
        if not self.is_available():
            raise RuntimeError("MISTRAL_API_KEY is not configured")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            **options,
        }
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise ValueError("Mistral returned an unexpected response") from error


class GroqProvider(Provider):
    """Adapter for Groq's OpenAI-compatible chat completions API."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str = "https://api.groq.com/openai/v1",
        client: httpx.Client | None = None,
    ) -> None:
        if model not in GROQ_MODELS:
            raise ValueError(
                "Model is not in the approved awesome-free-llm-apis catalog: "
                f"{model}"
            )
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=60.0)

    @property
    def name(self) -> str:
        return "groq"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def complete(self, prompt: str, **options: Any) -> str:
        if not self.is_available():
            raise RuntimeError("GROQ_API_KEY is not configured")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            **options,
        }
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise ValueError("Groq returned an unexpected response") from error


__all__ = [
    "GroqProvider",
    "MistralProvider",
    "OpenRouterProvider",
    "Provider",
]
