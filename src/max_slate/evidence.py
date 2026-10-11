"""Opt-in curated evidence responses; default routing and templates remain compatible."""

import json
import re
import unicodedata
from importlib.resources import files

from max_slate.schemas import Answer, RouteMode


def _normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split()).strip(".?!")


def load_evidence() -> dict:
    pack = json.loads(files("max_slate.knowledge").joinpath("evidence.json").read_text("utf-8"))
    source_ids = {item["id"] for item in pack["sources"]}
    if len(source_ids) != len(pack["sources"]):
        raise ValueError("Duplicate evidence source IDs")
    for item in pack["facts"] + pack["quotes"]:
        if not item["sources"] or not set(item["sources"]).issubset(source_ids):
            raise ValueError("Unresolved evidence source IDs")
    for item in pack["quotes"]:
        if item["status"] not in {"VERIFIED", "DISPUTED", "UNSOURCED"}:
            raise ValueError("Invalid quotation status")
    return pack


def enrich_answer(question: str | None, answer: Answer) -> Answer:
    """Return only local source-linked content, never an unrestricted model answer."""
    pack = load_evidence()
    text = _normalized(question or "")
    prefix = answer.identity + " "
    kwargs = {"persona_id": answer.persona_id, "route": answer.route}
    if answer.route.mode == RouteMode.HISTORICAL:
        for fact in pack["facts"]:
            if any(
                re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text) for term in fact["terms"]
            ):
                return Answer(
                    **kwargs,
                    text=prefix + fact["text"],
                    source_ids=tuple(fact["sources"]),
                    uncertainty=fact.get("qualification", "Educational paraphrase."),
                )
        return Answer(
            **kwargs,
            text=prefix + answer.text,
            uncertainty="No supported answer in the small local knowledge pack.",
        )
    if answer.route.mode == RouteMode.QUOTE_CHECK:
        candidates = re.findall(r'["“]([^"”]+)["”]', question or "")
        record = None
        for quote in pack["quotes"]:
            if any(
                _normalized(candidate) == _normalized(quote["text"]) for candidate in candidates
            ):
                record = quote
                break
        if record is None and "fish" in text and "climb" in text:
            record = next(item for item in pack["quotes"] if item["id"] == "fish-disputed")
        if record is None:
            return Answer(
                **kwargs,
                text=prefix + answer.text,
                quote_status="UNSOURCED",
                uncertainty="No exact quote record in the local pack.",
            )
        if record["status"] != "VERIFIED":
            return Answer(
                **kwargs,
                text=prefix + answer.text + " " + record["qualification"],
                source_ids=tuple(record["sources"]),
                quote_status=record["status"],
                uncertainty=record["qualification"],
            )
        if len(record["text"].split()) > 25:
            return Answer(
                **kwargs,
                text=prefix + "Verified excerpt exceeds the 25-word limit; consult the source.",
                source_ids=tuple(record["sources"]),
                quote_status="VERIFIED",
            )
        return Answer(
            **kwargs,
            text=prefix
            + "Verified source excerpt: “"
            + record["text"]
            + "”. "
            + record["qualification"],
            source_ids=tuple(record["sources"]),
            quote_status="VERIFIED",
            uncertainty=record["qualification"],
        )
    if answer.route.mode == RouteMode.EDUCATOR:
        return Answer(
            **kwargs,
            text=prefix + answer.text + " The local pack does not contain "
            "a sourced modern explanation of this topic.",
            evidence="TARGET",
            uncertainty="Broad modern explanation coverage is not implemented.",
        )
    return Answer(**kwargs, text=prefix + answer.text)
