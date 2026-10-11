"""Local knowledge-pack loading; deliberately no web or network retrieval."""

import json
from pathlib import Path
from typing import Any


def load_json_records(root: str | Path) -> list[tuple[Path, Any]]:
    """Parse every JSON file below root and return path/value pairs."""
    base = Path(root)
    if not base.is_dir():
        raise ValueError(f"Knowledge pack directory does not exist: {base}")
    records: list[tuple[Path, Any]] = []
    for file_path in sorted(base.rglob("*.json")):
        try:
            records.append((file_path, json.loads(file_path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid knowledge JSON at {file_path}: {exc}") from exc
    return records


def validate_source_references(root: str | Path) -> None:
    """Ensure any source_ids in records point to a local provenance record."""
    base = Path(root)
    source_file = base / "provenance" / "sources.json"
    try:
        sources = json.loads(source_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read provenance source registry: {exc}") from exc
    if not isinstance(sources, list) or any(not isinstance(item, dict) for item in sources):
        raise ValueError("Provenance registry must be a JSON array of source objects")
    known_ids = {item.get("id") for item in sources if isinstance(item.get("id"), str)}
    for path, value in load_json_records(base):
        if path == source_file:
            continue
        rows = value if isinstance(value, list) else [value]
        for row in rows:
            if not isinstance(row, dict):
                continue
            refs = row.get("source_ids", [])
            if not isinstance(refs, list) or any(ref not in known_ids for ref in refs):
                raise ValueError(f"Unknown or malformed source_ids in {path}")
