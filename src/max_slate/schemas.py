"""Typed objects shared by the deterministic routing and answer pipeline."""

from dataclasses import dataclass
from enum import StrEnum


class RouteMode(StrEnum):
    """Only supported route destinations."""

    HISTORICAL = "historical"
    EDUCATOR = "educator"
    QUOTE_CHECK = "quote_check"
    REFUSE = "refuse"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class RouteDecision:
    """A classification plus a short machine-readable rationale."""

    mode: RouteMode
    reason: str


@dataclass(frozen=True, slots=True)
class Answer:
    """Bounded response and its route metadata."""

    persona_id: str
    text: str
    route: RouteDecision
    source_ids: tuple[str, ...] = ()
    quote_status: str | None = None
    uncertainty: str = ""
    evidence: str = "IMPLEMENTED"
    simulation: bool = True
    identity: str = "Educational simulation inspired by Einstein; not Albert Einstein."
