import json
from pathlib import Path

from max_slate.cli import main

ROOT = Path(__file__).parents[1]
PERSONA = ROOT / "src" / "max_slate" / "personas" / "einstein.json"


def test_cli_ask_prints_route_and_fixed_answer(capsys) -> None:
    code = main(["ask", "--persona", "einstein", "--question", "What is quantum computing?"])
    out = capsys.readouterr().out
    assert code == 0
    assert out.startswith("[educator] ")
    assert "beyond my historical lifetime" in out


def test_cli_validates_persona_path(capsys) -> None:
    code = main(["validate-persona", str(PERSONA)])
    assert code == 0
    assert "Persona valid: einstein" in capsys.readouterr().out


def test_audit_is_opt_in_and_does_not_store_raw_question(tmp_path: Path) -> None:
    question = "SENSITIVE_SENTINEL question content"
    audit_path = tmp_path / "private" / "audit.jsonl"
    code = main(
        [
            "ask",
            "--persona",
            "einstein",
            "--question",
            question,
            "--audit-file",
            str(audit_path),
        ]
    )
    assert code == 0
    raw = audit_path.read_text(encoding="utf-8")
    assert question not in raw
    record = json.loads(raw)
    assert record["route"] == "historical"
    assert record["question_sha256"]
