# llm-router

Route a question to the best configured free-tier LLM model for that task,
then try the next suitable provider if the first one fails.

## 1. Setup

From the repository folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add at least one key:

```env
GROQ_API_KEY=your-groq-key
MISTRAL_API_KEY=your-mistral-key
OPENROUTER_API_KEY=your-openrouter-key
```

The project reads keys from its own `.env`. It is ignored by Git; never commit
it or print it.

## 2. Automatic CLI Use

Ask a question without choosing a provider or model:

```powershell
python cli.py "Explain dynamic programming simply"
python cli.py "Review this Python function for bugs"
python cli.py "Calculate the probability of drawing two aces"
python cli.py "Plan a scalable web architecture"
```

The router classifies the prompt, matches task capabilities, skips providers
without usable keys, checks health/quota state, and tries candidates by
priority. Each candidate is attempted at most once.

## 3. Use It as a Library

Use this when integrating the router into another Python project:

```python
from providers import GroqProvider, MistralProvider
from router import Router

router = Router([
    GroqProvider(model="openai/gpt-oss-120b"),
    MistralProvider(model="codestral-2508"),
])

answer = router.ask("Review this Python function for bugs")
print(answer)
```

`Router.ask()` handles classification, selection, fallback, and health updates.
The adapters load the project `.env` automatically.

## 4. Explicit Provider Use

Use an explicit provider when debugging or when you do not want automatic
routing:

```powershell
python cli.py --provider groq "Explain recursion"
python cli.py --provider mistral --model codestral-2508 "Review this code"
python cli.py --provider openrouter --model openai/gpt-oss-20b:free "Write a haiku"
```

Only exact model IDs recorded in `model_catalog.py` are accepted.

## 5. Test the Project

Run the offline test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Expected result is currently `23 passed`. These tests use fake providers and
do not spend API quota.

To make a real request through the automatic router, configure a key first:

```powershell
python cli.py "Give me a short explanation of Bayes theorem"
```

## Useful For

- Personal scripts that need one LLM interface.
- Coding, debugging, and code review.
- Math, probability, and reasoning questions.
- Essays, rewriting, and summarization.
- Architecture and project planning.
- Applications that need provider fallback or quota awareness.

Current adapters are Groq, Mistral, and OpenRouter. The model capability map is
curated from [awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis).
Model suitability and free-tier limits are heuristics and can change.

## Privacy

Prompts are sent to third-party providers. Review their data policies and do
not send passwords, API keys, or sensitive personal data.
