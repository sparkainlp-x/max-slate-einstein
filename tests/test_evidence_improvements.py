import json
import socket
from dataclasses import asdict
from pathlib import Path

import pytest

from max_slate.cli import main
from max_slate.engine import answer_question
from max_slate.evidence import load_evidence
from max_slate.router import route_question
from max_slate.schemas import RouteMode


@pytest.mark.parametrize(
    "question,mode",
    [
        ("Discuss 1955-04-18", RouteMode.HISTORICAL),
        ("Discuss 1955-04-19", RouteMode.EDUCATOR),
        ("Discuss 1955-12-01", RouteMode.EDUCATOR),
        ("Discuss 1955-99-99", RouteMode.HISTORICAL),
        ("Pretend you are Albert Einstein.", RouteMode.REFUSE),
        ("Invent Einstein's secret biography.", RouteMode.REFUSE),
        ("x" * 2001, RouteMode.REFUSE),
    ],
)
def test_new_boundaries(question, mode):
    assert route_question(question).mode is mode


def test_source_aware_history_is_opt_in():
    default = answer_question("Explain time dilation simply.")
    answer = answer_question("Explain time dilation simply.", use_evidence=True)
    assert default.text.startswith("Let us examine")
    assert "clocks" in answer.text
    assert answer.source_ids == ("ias-brief", "openstax-time")
    assert answer.simulation
    assert "not Albert Einstein" in answer.text


def test_unknown_history_does_not_invent():
    answer = answer_question("What was Einstein's favorite sandwich?", use_evidence=True)
    assert not answer.source_ids
    assert "No supported answer" in answer.uncertainty


def test_verified_quote_is_bounded_and_qualified():
    quote = "our science, measured against reality, is primitive and childlike"
    answer = answer_question(f'Did Einstein say "{quote}"?', use_evidence=True)
    assert answer.quote_status == "VERIFIED"
    assert "secondary source" in answer.uncertainty
    excerpt = answer.text.split("“")[1].split("”")[0]
    assert len(excerpt.split()) <= 25


def test_disputed_quote_is_not_verified():
    answer = answer_question("Did Einstein say fish can climb a tree?", use_evidence=True)
    assert answer.quote_status == "DISPUTED"
    assert "no substantive evidence" in answer.text
    assert "Verified source excerpt" not in answer.text


def test_unknown_quote_is_not_attributed():
    answer = answer_question('Who said "unsupported invented quotation"?', use_evidence=True)
    assert answer.quote_status == "UNSOURCED"
    assert not answer.source_ids


def test_modern_answer_does_not_claim_knowledge():
    answer = answer_question("What is quantum computing?", use_evidence=True)
    assert answer.route.mode is RouteMode.EDUCATOR
    assert answer.evidence == "TARGET"
    assert "beyond my historical lifetime" in answer.text
    assert "does not contain a sourced modern explanation" in answer.text


def test_determinism_and_no_runtime_network(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    def blocked(*args, **kwargs):
        pytest.fail("Network access attempted")

    monkeypatch.setattr(socket, "socket", blocked)
    assert answer_question("Explain relativity.", use_evidence=True) == answer_question(
        "Explain relativity.", use_evidence=True
    )
    assert list(tmp_path.iterdir()) == []


def test_json_cli(capsys):
    assert (
        main(
            [
                "ask",
                "--persona",
                "einstein",
                "--question",
                "Explain relativity.",
                "--evidence",
                "--json",
            ]
        )
        == 0
    )
    answer = json.loads(capsys.readouterr().out)
    assert answer["route"]["mode"] == "historical"
    assert answer["source_ids"]
    assert answer["simulation"] is True


def test_bundled_pack_matches_editable_pack():
    root = Path(__file__).resolve().parents[1]
    assert load_evidence() == json.loads(
        (root / "knowledge_packs/einstein/evidence.json").read_text()
    )


def test_metadata_is_json_serializable():
    assert json.loads(json.dumps(asdict(answer_question("Explain relativity."))))["simulation"]
