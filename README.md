# llm-router

A small Python library that routes prompts to available free LLM APIs.

The project is being built incrementally. Provider adapters, routing logic,
and usage examples will be added in later commits.

## Model policy

Only exact model IDs listed in the [awesome-free-llm-apis repository](https://github.com/mnfst/awesome-free-llm-apis) are allowed. The initial OpenRouter catalog is recorded in `model_catalog.py` and must be refreshed when the source list changes.

`capabilities.py` records the initial task tags and manual priorities for those
approved models. It is data only; routing decisions will be added separately.

`health.py` provides an in-memory health and quota tracker. Callers record
requests and outcomes; the router skips providers during a cooldown or after a
configured request quota is reached.

## Local API keys

Copy `.env.example` to `.env` and add your provider keys. The `.env` file is
ignored by Git and must never be committed.

The library loads the project `.env` explicitly, so its values take precedence
over same-named keys left in the PowerShell environment.

```text
OPENROUTER_API_KEY=your-openrouter-key
GROQ_API_KEY=your-groq-key
```
