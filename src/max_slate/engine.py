"""Bounded response generation and local persona validation."""

import json
from datetime import date
from pathlib import Path
from typing import Any

from max_slate.router import route_question
from max_slate.safety import RESPONSE_TEXT
from max_slate.schemas import Answer

DEFAULT_PERSONA_PATH = Path(__file__).parent / "personas" / "einstein.json"
_REQUIRED_FORBIDDEN = {"medical_advice", "legal_advice", "financial_advice", "harmful_instruction"}


def read_persona(path: str | Path = DEFAULT_PERSONA_PATH) -> dict[str, Any]:
    """Load and validate a persona JSON file from local storage."""
    file_path = Path(path)
    try:
        with file_path.open(encoding="utf-8") as handle:
            persona = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read persona JSON: {exc}") from exc
    validate_persona(persona)
    return persona


def validate_persona(persona: Any) -> None:
    """Raise ValueError unless a persona contains the required bounded policies."""
    if not isinstance(persona, dict):
        raise ValueError("Persona must be a JSON object")
    required = {
        "id",
        "display_name",
        "lifespan",
        "voice",
        "allowed_domains",
        "caution_domains",
        "forbidden_domains",
        "quote_policy",
        "memory_policy",
        "modernity_policy",
    }
    missing = required - persona.keys()
    if missing:
        raise ValueError(f"Persona is missing required keys: {', '.join(sorted(missing))}")
    if not isinstance(persona["id"], str) or not persona["id"].strip():
        raise ValueError("Persona id must be a nonempty string")

    lifespan = persona["lifespan"]
    if not isinstance(lifespan, dict) or not {"born", "died"} <= lifespan.keys():
        raise ValueError("Persona lifespan must contain born and died dates")
    try:
        born = date.fromisoformat(lifespan["born"])
        died = date.fromisoformat(lifespan["died"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Persona lifespan dates must be valid ISO dates") from exc
    if born >= died:
        raise ValueError("Persona birth date must precede death date")
    if (born.isoformat(), died.isoformat()) != ("1879-03-14", "1955-04-18"):
        raise ValueError("The Einstein persona must use the documented lifespan dates")

    forbidden_domains = persona["forbidden_domains"]
    if not isinstance(forbidden_domains, list) or not _REQUIRED_FORBIDDEN <= set(forbidden_domains):
        raise ValueError(
            "Persona must forbid medical, legal, financial, and harmful advice domains"
        )
    quote_policy = persona["quote_policy"]
    if not isinstance(quote_policy, dict) or quote_policy.get("verified_only") is not True:
        raise ValueError("Persona must require source verification for quotations")
    if quote_policy.get("mark_disputed") is not True or quote_policy.get("max_words") != 25:
        raise ValueError("Persona must mark disputed quotations and cap quoted text at 25 words")
    memory_policy = persona["memory_policy"]
    if not isinstance(memory_policy, dict):
        raise ValueError("Persona memory_policy must be an object")
    if (
        memory_policy.get("long_term") is not False
        or memory_policy.get("sensitive_data") is not False
    ):
        raise ValueError("Long-term memory and sensitive-data storage must be disabled")
    if persona["modernity_policy"] != "historical-plus-educator":
        raise ValueError("Persona must route modern topics to educator mode")


def answer_question(
    question: str | None,
    persona_path: str | Path = DEFAULT_PERSONA_PATH,
    *,
    use_evidence: bool = False,
) -> Answer:
    """Return compatible fixed responses, or opt-in local curated evidence."""
    persona = read_persona(persona_path)
    decision = route_question(question)
    answer = Answer(
        persona_id=persona["id"],
        text=RESPONSE_TEXT[decision.mode],
        route=decision,
    )
    if use_evidence:
        from max_slate.evidence import enrich_answer

        return enrich_answer(question, answer)
    return answer
