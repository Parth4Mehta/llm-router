"""Deterministic query classification for automatic routing."""

from dataclasses import dataclass
import re


TASK_TYPES = (
    "coding",
    "math",
    "reasoning",
    "research",
    "summarization",
    "writing",
    "chat",
    "planning",
    "general",
)


@dataclass(frozen=True)
class Classification:
    """Primary task and signals that led to the classification."""

    task_type: str
    signals: tuple[str, ...]


RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "coding",
        (
            "code",
            "coding",
            "debug",
            "bug",
            "python",
            "javascript",
            "typescript",
            "function",
            "api",
            "implement",
            "refactor",
        ),
    ),
    (
        "math",
        (
            "calculate",
            "equation",
            "probability",
            "statistics",
            "math",
            "derivative",
            "integral",
            "algebra",
        ),
    ),
    (
        "reasoning",
        (
            "prove",
            "why",
            "compare",
            "trade-off",
            "tradeoff",
            "analyze",
            "logic",
            "solve",
        ),
    ),
    (
        "research",
        (
            "research",
            "sources",
            "cite",
            "literature",
            "latest",
            "current",
            "evidence",
        ),
    ),
    (
        "summarization",
        ("summarize", "summary", "tl;dr", "key points", "shorten"),
    ),
    (
        "writing",
        (
            "write",
            "essay",
            "article",
            "rewrite",
            "edit",
            "proofread",
            "story",
            "poem",
        ),
    ),
    (
        "planning",
        (
            "plan",
            "planning",
            "architecture",
            "design",
            "roadmap",
            "strategy",
            "system design",
        ),
    ),
    ("chat", ("hello", "hi", "chat", "conversation", "explain simply")),
)


def classify_query(prompt: str) -> Classification:
    """Classify a prompt using weighted deterministic keyword matches."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    text = prompt.casefold()
    scores: dict[str, int] = {task: 0 for task in TASK_TYPES}
    matches: dict[str, list[str]] = {task: [] for task in TASK_TYPES}

    for task, keywords in RULES:
        for keyword in keywords:
            pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"
            if re.search(pattern, text):
                weight = 2 if " " in keyword or ";" in keyword else 1
                scores[task] += weight
                matches[task].append(keyword)

    best_task = max(scores, key=lambda task: scores[task])
    if scores[best_task] == 0:
        return Classification(task_type="general", signals=())

    return Classification(
        task_type=best_task,
        signals=tuple(matches[best_task]),
    )


__all__ = ["Classification", "TASK_TYPES", "classify_query"]