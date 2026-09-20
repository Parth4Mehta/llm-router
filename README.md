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

Send a prompt in automatic mode. The router classifies the query, chooses a
compatible configured model, and tries the next candidate if the first fails:

```powershell
python cli.py "Explain dynamic programming in one paragraph"
python cli.py "Review this Python function for bugs"
python cli.py "Plan a scalable web architecture"
```

Use an explicit provider/model only when you want to override automatic
routing:

```powershell
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

The main library API is automatic:

```python
from providers import GroqProvider, MistralProvider
from router import Router

router = Router(
	[
		GroqProvider(model="openai/gpt-oss-120b"),
		MistralProvider(model="codestral-2508"),
	]
)

answer = router.ask("Review this Python function for bugs")
print(answer)
```

`Router.ask(prompt)`:

1. Classifies the prompt using deterministic keyword and phrase rules.
2. Matches the task to the static model capability registry.
3. Skips providers without credentials, during cooldown, or over quota.
4. Tries candidates in manual priority order.
5. Records health and returns the first successful response.

Available task categories include coding, math, reasoning, research,
summarization, writing, chat, planning, and general. Use `Router.rank(task)`
to inspect candidates without sending a request. `Router.select(task)` remains
available when only the first candidate is needed.

Fallback is bounded: each ranked candidate is attempted at most once. The
router does not retry indefinitely or use another LLM to classify the prompt.

## Model policy

Only exact model IDs listed in the [awesome-free-llm-apis repository](https://github.com/mnfst/awesome-free-llm-apis) are allowed. The snapshot date and provider model IDs are recorded in `model_catalog.py`; refresh that file when the source list changes.

Current adapters: OpenRouter, Mistral, and Groq.

The capability registry currently contains a curated subset of models from
each adapter. It records heuristic task suitability, not guaranteed quality;
model quality and free-tier availability can change over time.

Current curated roles include:

- Groq GPT-OSS 120B: general reasoning, math, and planning.
- Groq GPT-OSS 20B: general chat, writing, and summarization.
- Mistral Medium 3.5: reasoning, planning, coding, and multimodal work.
- Mistral Small 4: efficient general, reasoning, coding, and writing tasks.
- Mistral Codestral: coding and code review.
- OpenRouter free models: general, reasoning, writing, and code roles as
	recorded in `capabilities.py`.

These are starting heuristics based on provider descriptions and the linked
free-model catalog, not benchmark guarantees.

## Privacy

Prompts are sent to the selected third-party provider. Free-tier providers may
log or use prompts according to their terms. Do not send secrets or sensitive
personal data unless you have reviewed the provider's policy.

## Tests

```powershell
pytest
```

The GitHub Actions workflow runs the same test suite on pushes and pull requests.

## Current limitations

- The classifier is rule-based and intentionally simple.
- Capability metadata is manually curated and should be refreshed when the
	upstream free-model list changes.
- Health and quota state is in memory only.
- No streaming, multimodal request contract, persistent quota store, or HTTP
	service is included yet.
