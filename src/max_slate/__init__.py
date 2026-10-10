"""Offline-first, bounded educational character simulation."""

from max_slate.engine import answer_question, read_persona, validate_persona
from max_slate.schemas import Answer, RouteDecision, RouteMode

__all__ = [
    "Answer",
    "RouteDecision",
    "RouteMode",
    "answer_question",
    "read_persona",
    "validate_persona",
]
__version__ = "0.1.0"
