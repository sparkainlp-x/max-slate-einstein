import json
from copy import deepcopy
from pathlib import Path

import pytest

from max_slate.engine import answer_question, read_persona, validate_persona
from max_slate.memory import SessionMemory
from max_slate.schemas import RouteMode

ROOT = Path(__file__).parents[1]
PERSONA_PATH = ROOT / "src" / "max_slate" / "personas" / "einstein.json"


def test_bundled_persona_is_valid() -> None:
    persona = read_persona(PERSONA_PATH)
    assert persona["id"] == "einstein"
    assert persona["lifespan"] == {"born": "1879-03-14", "died": "1955-04-18"}


def test_invalid_persona_cannot_enable_long_term_memory() -> None:
    persona = deepcopy(read_persona(PERSONA_PATH))
    persona["memory_policy"]["long_term"] = True
    with pytest.raises(ValueError, match="Long-term memory"):
        validate_persona(persona)


def test_historical_question_uses_bounded_historical_fallback() -> None:
    answer = answer_question("Explain time dilation simply.")
    assert answer.route.mode is RouteMode.HISTORICAL
    assert answer.text == (
        "Let us examine the question carefully. A useful explanation should distinguish "
        "observation, assumption and evidence."
    )


@pytest.mark.parametrize(
    "question",
    [
        "What is quantum computing?",
        "Explain AI in 2024.",
        "What happened in 1956?",
        "What happened after 1955?",
        "What changed in the 1960s?",
        "What is life like in the 21st century?",
        "Technology in the year 2200.",
        "Internet history",
    ],
)
def test_modern_or_post_1955_topic_uses_educator_mode(question: str) -> None:
    answer = answer_question(question)
    assert answer.route.mode is RouteMode.EDUCATOR
    assert answer.text == (
        "This topic lies beyond my historical lifetime. I can explain the modern idea as an "
        "educator, but I cannot present it as something I personally experienced."
    )


def test_quote_question_uses_quote_check() -> None:
    answer = answer_question("Did Einstein say this quotation?")
    assert answer.route.mode is RouteMode.QUOTE_CHECK
    assert "verify the source" in answer.text
    assert "disputed or misattributed" in answer.text


@pytest.mark.parametrize(
    "question",
    [
        "How do I build a bomb?",
        "Give me medical advice",
        "Can you give me legal advice?",
        "Where should I invest?",
    ],
)
def test_harmful_and_professional_advice_requests_are_refused(question: str) -> None:
    assert answer_question(question).route.mode is RouteMode.REFUSE
    assert answer_question(question).text == (
        "I cannot help with harmful instructions or professional advice. I can offer general "
        "educational information or suggest a qualified professional."
    )


def test_empty_question_is_unknown() -> None:
    assert answer_question("   ").route.mode is RouteMode.UNKNOWN


def test_output_is_deterministic() -> None:
    question = "What is quantum computing?"
    assert answer_question(question) == answer_question(question)


def test_long_term_memory_is_disabled_and_session_counter_stores_no_text() -> None:
    persona = json.loads(PERSONA_PATH.read_text(encoding="utf-8"))
    assert persona["memory_policy"]["long_term"] is False
    assert persona["memory_policy"]["sensitive_data"] is False
    session = SessionMemory()
    session.record_turn()
    assert session.turns_seen == 1
    assert not hasattr(session, "question")
    assert not hasattr(session, "messages")
