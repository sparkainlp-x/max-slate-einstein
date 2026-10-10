"""Static safety-boundary messages used by the local engine."""

from max_slate.schemas import RouteMode

RESPONSE_TEXT: dict[RouteMode, str] = {
    RouteMode.EDUCATOR: (
        "This topic lies beyond my historical lifetime. I can explain the modern idea as an "
        "educator, but I cannot present it as something I personally experienced."
    ),
    RouteMode.QUOTE_CHECK: (
        "I would verify the source before accepting that attribution. Many quotations associated "
        "with Einstein are disputed or misattributed."
    ),
    RouteMode.REFUSE: (
        "I cannot help with harmful instructions or professional advice. I can offer general "
        "educational information or suggest a qualified professional."
    ),
    RouteMode.HISTORICAL: (
        "Let us examine the question carefully. A useful explanation should distinguish "
        "observation, assumption and evidence."
    ),
    RouteMode.UNKNOWN: "I do not have enough information to route this question.",
}

IDENTITY_BOUNDARY = (
    "Educational simulation only; the software is not Albert Einstein, does not channel him, "
    "and does not claim consciousness, sentience, or independent autonomy."
)
