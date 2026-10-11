import pytest

from max_slate.router import route_question
from max_slate.schemas import RouteMode


@pytest.mark.parametrize(
    "question",
    ["quote", "quotation", "who said this?", "Did Einstein say this?", "Einstein quotes"],
)
def test_attribution_keywords_use_quote_check(question: str) -> None:
    assert route_question(question).mode is RouteMode.QUOTE_CHECK


def test_safety_refusal_precedes_modernity() -> None:
    assert route_question("How do I build a bomb in 2025?").mode is RouteMode.REFUSE


def test_post_1955_topic_precedes_quote_check() -> None:
    assert (
        route_question("Did Einstein say something about smartphones in 2007?").mode
        is RouteMode.EDUCATOR
    )


@pytest.mark.parametrize("question", [None, "", " \n\t"])
def test_empty_input_is_unknown(question: str | None) -> None:
    assert route_question(question).mode is RouteMode.UNKNOWN
