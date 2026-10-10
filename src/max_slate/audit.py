"""Opt-in, local audit records that omit raw questions and answers."""

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from max_slate.schemas import Answer


def write_audit_record(path: str | Path, question: str | None, answer: Answer) -> None:
    """Append one metadata-only JSONL record, creating a private file if new."""
    question_bytes = (question or "").encode("utf-8")
    record = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "persona_id": answer.persona_id,
        "route": answer.route.mode.value,
        "reason": answer.route.reason,
        "question_sha256": hashlib.sha256(question_bytes).hexdigest(),
    }
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
