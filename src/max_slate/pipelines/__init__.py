"""Local deterministic question pipeline."""

from max_slate.engine import answer_question
from max_slate.memory import SessionMemory
from max_slate.schemas import Answer


def run_local(question: str | None, session: SessionMemory | None = None) -> Answer:
    """Route and answer locally; session state never includes question text."""
    answer = answer_question(question)
    if session is not None:
        session.record_turn()
    return answer
