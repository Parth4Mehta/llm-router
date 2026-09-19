# llm-router

Small Python library for routing prompts across free-tier LLM APIs.

## Install

For local development:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For use from another Python project:

```powershell
python -m pip install .
```

## Configure keys

Copy `.env.example` to `.env` and add keys for the providers you use. The
`.env` file is ignored by Git and must never be committed.

```text
OPENROUTER_API_KEY=your-openrouter-key
MISTRAL_API_KEY=your-mistral-key
GROQ_API_KEY=your-groq-key
```

The library loads the project `.env` explicitly, so its values take precedence
over same-named keys left in the PowerShell environment.

## CLI

Send one prompt through a selected provider:

```powershell
python cli.py "Explain dynamic programming in one paragraph"
python cli.py --provider mistral "Summarize the idea of recursion"
python cli.py --provider openrouter --model openai/gpt-oss-20b:free "Write a haiku"
```

The same adapters can be imported directly by another project:

```python
from providers import GroqProvider

provider = GroqProvider(model="openai/gpt-oss-120b")
answer = provider.complete("Explain probability simply")
```

## Routing

`Router.select(task_type)` chooses an available model using the static task
capability map and manual priority. `HealthTracker` adds in-memory cooldown and
quota checks. Retries, persistence, and automatic task classification are not
included yet.

## Model policy

Only exact model IDs listed in the [awesome-free-llm-apis repository](https://github.com/mnfst/awesome-free-llm-apis) are allowed. The snapshot date and provider model IDs are recorded in `model_catalog.py`; refresh that file when the source list changes.

Current adapters: OpenRouter, Mistral, and Groq.

## Privacy

Prompts are sent to the selected third-party provider. Free-tier providers may
log or use prompts according to their terms. Do not send secrets or sensitive
personal data unless you have reviewed the provider's policy.

## Tests

```powershell
pytest
```

The GitHub Actions workflow runs the same test suite on pushes and pull requests.
