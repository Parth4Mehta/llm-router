from cli import configured_providers
from health import HealthTracker
from router import Router


class FakeProvider:
    def __init__(self, name, model, response="answer", error=None):
        self.name = name
        self.model = model
        self.response = response
        self.error = error

    def is_available(self):
        return True

    def complete(self, prompt):
        if self.error:
            raise self.error
        return self.response


def test_ask_routes_coding_query_to_code_model():
    general = FakeProvider("groq", "openai/gpt-oss-120b")
    code = FakeProvider("mistral", "codestral-2508", response="code answer")

    router = Router([general, code])

    assert router.ask("Review this Python function") == "code answer"
    assert router.last_provider is code


def test_ask_uses_next_candidate_after_first_failure():
    first = FakeProvider(
        "groq", "openai/gpt-oss-120b", error=RuntimeError("rate limited")
    )
    second = FakeProvider("groq", "openai/gpt-oss-20b", response="fallback answer")
    router = Router([first, second])

    assert router.ask("Tell me something") == "fallback answer"
    assert router.health.status(first).failures == 1
    assert router.health.status(second).successes == 1


def test_ask_skips_candidate_after_quota_is_exhausted():
    limited = FakeProvider("limited", "openai/gpt-oss-120b")
    backup = FakeProvider("backup", "openai/gpt-oss-20b", response="backup answer")
    health = HealthTracker(quotas={"limited": 1})
    health.record_request(limited)

    assert Router([limited, backup], health=health).ask("Tell me something") == (
        "backup answer"
    )


def test_cli_builds_curated_provider_adapters():
    providers = configured_providers()
    models = {provider.model for provider in providers}

    assert "openai/gpt-oss-120b" in models
    assert "groq/compound" in models
    assert "groq/compound-mini" in models
    assert "qwen/qwen3.6-27b" in models
    assert "mistral-small-2603" in models
    assert {provider.name for provider in providers} == {
        "groq",
        "mistral",
        "openrouter",
    }