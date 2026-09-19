import httpx
import pytest

from health import HealthTracker
from providers import GroqProvider, MistralProvider
from router import Router


class FakeProvider:
    def __init__(self, name, model, available=True):
        self.name = name
        self.model = model
        self.available = available

    def is_available(self):
        return self.available


def test_router_selects_highest_priority_matching_model():
    general = FakeProvider("general", "openai/gpt-oss-120b:free")
    code = FakeProvider("code", "cohere/north-mini-code:free")

    assert Router([general, code]).select("coding") is code
    assert Router([general, code]).select("GENERAL") is general


def test_router_skips_provider_in_cooldown():
    first = FakeProvider("first", "openai/gpt-oss-120b:free")
    second = FakeProvider("second", "openai/gpt-oss-20b:free")
    health = HealthTracker(cooldown_seconds=60)
    health.record_failure(first)

    assert Router([first, second], health=health).select("general") is second


def test_health_tracker_enforces_quota():
    provider = FakeProvider("limited", "openai/gpt-oss-20b:free")
    health = HealthTracker(quotas={"limited": 1})

    assert health.can_use(provider)
    health.record_request(provider)
    assert not health.can_use(provider)


@pytest.mark.parametrize(
    ("provider_class", "model", "url"),
    [
        (GroqProvider, "openai/gpt-oss-120b", "https://api.groq.com/openai/v1/chat/completions"),
        (MistralProvider, "mistral-small-2603", "https://api.mistral.ai/v1/chat/completions"),
    ],
)
def test_provider_normalizes_chat_response(provider_class, model, url):
    def handler(request):
        assert str(request.url) == url
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "test response"}}]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    provider = provider_class(model=model, api_key="test-key", client=client)

    assert provider.complete("hello") == "test response"


def test_unlisted_model_is_rejected():
    with pytest.raises(ValueError, match="awesome-free-llm-apis"):
        GroqProvider(model="unlisted-model", api_key="test-key")