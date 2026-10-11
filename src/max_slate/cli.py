"""Command-line interface for the offline Max Slate prototype."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from max_slate.audit import write_audit_record
from max_slate.engine import answer_question, read_persona


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="max-slate", description="Offline bounded educational character engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask_parser = subparsers.add_parser("ask", help="route and answer one question locally")
    ask_parser.add_argument("--persona", choices=("einstein",), required=True)
    ask_parser.add_argument("--question", required=True)
    ask_parser.add_argument("--evidence", action="store_true", help="use local curated evidence")
    ask_parser.add_argument("--json", action="store_true", help="output structured answer JSON")
    ask_parser.add_argument(
        "--audit-file",
        type=Path,
        help="opt in to a local metadata-only JSONL audit file; raw questions are not stored",
    )

    validate_parser = subparsers.add_parser(
        "validate-persona", help="validate a local persona JSON file"
    )
    validate_parser.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate-persona":
            persona = read_persona(args.path)
            print(f"Persona valid: {persona['id']}")
            return 0

        persona_path = Path(__file__).parent / "personas" / f"{args.persona}.json"
        answer = answer_question(args.question, persona_path, use_evidence=args.evidence)
        if args.audit_file is not None:
            write_audit_record(args.audit_file, args.question, answer)
        if args.json:
            print(json.dumps(asdict(answer), ensure_ascii=False, sort_keys=True))
        else:
            print(f"[{answer.route.mode.value}] {answer.text}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
