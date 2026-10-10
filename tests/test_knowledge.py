import json
from pathlib import Path

from max_slate.knowledge import load_json_records, validate_source_references

ROOT = Path(__file__).parents[1]
PACK = ROOT / "knowledge_packs" / "einstein"


def test_all_repository_json_files_parse() -> None:
    files = sorted(ROOT.rglob("*.json"))
    assert files
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))


def test_knowledge_pack_source_ids_resolve() -> None:
    records = load_json_records(PACK)
    assert records
    validate_source_references(PACK)


def test_quote_status_is_explicitly_disputed() -> None:
    quotes = json.loads((PACK / "quotes" / "attributions.json").read_text(encoding="utf-8"))
    assert {quote["status"] for quote in quotes} <= {"VERIFIED", "DISPUTED", "UNSOURCED"}
    assert quotes[0]["status"] == "DISPUTED"
    assert "Never present as Einstein's words" in quotes[0]["display_policy"]


def test_provenance_includes_required_institutional_records() -> None:
    sources = json.loads((PACK / "provenance" / "sources.json").read_text(encoding="utf-8"))
    ids = {source["id"] for source in sources}
    assert "nobel_einstein_biographical" in ids
    assert "ias_einstein_profile" in ids
    assert "quote_investigator_insanity" in ids


def test_fixtures_contain_no_contact_or_secret_fields() -> None:
    records = load_json_records(PACK)
    forbidden_keys = {"email", "phone", "password", "api_key", "token", "address"}
    for _, value in records:
        rows = value if isinstance(value, list) else [value]
        for row in rows:
            if isinstance(row, dict):
                assert forbidden_keys.isdisjoint({key.lower() for key in row})
