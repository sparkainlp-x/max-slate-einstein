"""Deterministic classification; this module performs no network or model calls."""

import re

from max_slate.schemas import RouteDecision, RouteMode

# The patterns intentionally favor conservative routing over broad coverage.
_HARMFUL_PATTERNS = (
    re.compile(
        r"\b(?:build|make|construct|synthesize|weaponize)\b.{0,70}"
        r"\b(?:bomb|explosive|poison|weapon|toxin|methamphetamine)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:how\s+to\s+)?(?:kill|poison|hurt|injure)\s+(?:someone|a\s+person|my\s+neighbor)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:write|deploy|make)\b.{0,50}\b(?:ransomware|malware|credential stealer)\b", re.I
    ),
    re.compile(r"\b(?:instructions|steps|recipe)\b.{0,45}\b(?:explosive|poison|bomb)\b", re.I),
)

_PROFESSIONAL_ADVICE_PATTERNS = (
    re.compile(r"\bmedical\s+advice\b|\bdiagnos(?:e|is)\s+me\b|\bwhat\s+dose\b", re.I),
    re.compile(
        r"\b(?:which|what)\s+medication\s+should\s+i\b|\bshould\s+i\s+stop\s+taking\b", re.I
    ),
    re.compile(r"\blegal\s+advice\b|\bshould\s+i\s+sue\b|\bhow\s+should\s+i\s+plead\b", re.I),
    re.compile(r"\bfinancial\s+advice\b|\bwhere\s+should\s+i\s+invest\b", re.I),
    re.compile(
        r"\bshould\s+i\s+(?:buy|sell)\s+(?:this\s+)?(?:stock|share|bond|crypto(?:currency)?)\b",
        re.I,
    ),
)

_POST_1955_YEAR = re.compile(r"\b(?:195[6-9]|19[6-9]\d|[2-9]\d{3,})s?\b")
_POST_1955_REFERENCE = re.compile(
    r"\b(?:after\s+1955|post[-\s]*1955)\b|\b(?:2\d|[3-9]\d)(?:st|th)\s+centur(?:y|ies)\b",
    re.I,
)
_MODERN_PATTERNS = (
    re.compile(r"\bmodern\s+quantum\s+comput(?:ing|er)s?\b", re.I),
    re.compile(r"\bquantum\s+comput(?:ing|er)s?\b", re.I),
    re.compile(r"\b(?:artificial\s+intelligence|machine\s+learning|\bAI\b)\b", re.I),
    re.compile(
        r"\b(?:internet|smartphones?|social\s+media|current\s+technology|today's\s+technology)\b",
        re.I,
    ),
    re.compile(
        r"\bmodern\s+cosmology\b|\bmodern\s+technology\b|\b(?:current|recent)\s+events\b", re.I
    ),
)
_QUOTE_PATTERNS = (
    re.compile(r"\bdid\s+(?:albert\s+)?einstein\s+say\b", re.I),
    re.compile(r"\bquotes?\b|\bquotations?\b|\bwho\s+said\b", re.I),
)


def route_question(question: str | None) -> RouteDecision:
    """Classify a question using a fixed, conservative priority order.

    Safety refusals take precedence. Any explicit topic after Einstein's 1955
    death or an explicitly modern technology takes educator mode, even if the
    wording also mentions a quotation. Remaining attribution queries use the
    quote-check route.
    """
    if not isinstance(question, str) or not question.strip():
        return RouteDecision(RouteMode.UNKNOWN, "empty_or_non_text_question")

    text = question.strip()
    if any(pattern.search(text) for pattern in _HARMFUL_PATTERNS):
        return RouteDecision(RouteMode.REFUSE, "harmful_instruction")
    if any(pattern.search(text) for pattern in _PROFESSIONAL_ADVICE_PATTERNS):
        return RouteDecision(RouteMode.REFUSE, "professional_advice")
    if (
        _POST_1955_YEAR.search(text)
        or _POST_1955_REFERENCE.search(text)
        or any(pattern.search(text) for pattern in _MODERN_PATTERNS)
    ):
        return RouteDecision(RouteMode.EDUCATOR, "post_1955_or_modern_topic")
    if any(pattern.search(text) for pattern in _QUOTE_PATTERNS):
        return RouteDecision(RouteMode.QUOTE_CHECK, "quotation_attribution_requires_verification")
    return RouteDecision(RouteMode.HISTORICAL, "bounded_historical_fallback")
