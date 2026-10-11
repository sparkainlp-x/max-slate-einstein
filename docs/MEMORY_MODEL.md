# Memory model

## Default

Long-term user memory is disabled by default. The persona sets `long_term: false` and `sensitive_data: false`. The engine is stateless between calls unless a caller supplies a `SessionMemory` object.

## Session state

The current `SessionMemory` stores a turn counter only. It never stores question text, answers, personal profiles, or inferred preferences. It exists in process memory and disappears when that process exits. There is no persistence, database, embedding store, or synchronization mechanism.

## Optional audit file

The CLI accepts `--audit-file PATH` only as an explicit opt-in. Each JSONL record contains a UTC timestamp, persona ID, route, routing reason, and SHA-256 digest of the question; it does not contain the raw question or response. A digest is pseudonymous metadata, not a guarantee of anonymity, and may be vulnerable to guessing when the question has low entropy. Users should protect and delete audit files according to their own retention needs. The file is created with owner-only permissions where supported; existing file permissions are not changed.

## Not implemented

There is no long-term memory feature, consent workflow, deletion API, encryption-at-rest layer, or automated sensitive-data detection. Such features are not enabled by this prototype and should not be inferred from the presence of a transient turn counter.
