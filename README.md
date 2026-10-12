# Max Slate Einstein

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23307947.svg)](https://doi.org/10.5281/zenodo.23307947)

Offline-first, bounded character engine for an Einstein-inspired educational avatar.

> Design principle: maximize persona consistency and evidence quality—not the number of questions answered.

**Status:** Research prototype. This is an educational simulation. It does not claim consciousness, sentience, autonomy, historical omniscience, psychological realism, or that Albert Einstein is speaking through the software.

“Max Slate” means a **maximum permitted answer space**: the system prefers a small, deterministic, policy-bounded response over unsupported elaboration. This repository is a local Python prototype, not a general-purpose language model.

## What it does

- Separates persona policy, local knowledge records, session memory policy, routing/safety, and response pipeline into distinct modules.
- Routes historical questions to a fixed, evidence-conscious fallback; quote-attribution questions to quote checking; unsafe and professional-advice requests to refusal; and modern topics to **educator mode**.
- Treats Albert Einstein’s lifespan as **1879-03-14 through 1955-04-18**. Topics explicitly dated after 1955, and configured modern-technology topics, route to educator mode and are not represented as Einstein’s personal knowledge or experience.
- Includes source provenance records, including NobelPrize.org, the Institute for Advanced Study, the Einstein Papers Project editorial method, and a separate source documenting disputed quote attribution.
- Includes a small, local quote-attribution record. A disputed attribution is not presented as Einstein’s words; quote status is `VERIFIED`, `DISPUTED`, or `UNSOURCED`.

## Memory, privacy, and safety

Long-term user memory is **disabled by default**. The prototype does not persist conversational content. Optional audit records are written only when an explicit local audit path is provided, and contain routing metadata rather than question text. The core engine makes no network requests, does not browse, and has no unrestricted retrieval. The package has no runtime third-party dependencies.

This is **not medical, legal, financial, or safety-critical software**. It refuses requests for professional advice and harmful instructions. Its static replies are intentionally limited; they are not a substitute for sourced research, expert judgment, or emergency help.

Synthetic tests establish deterministic software behavior only. **Synthetic tests do not establish human or historical authenticity**, and this prototype has not undergone independent human, security, historical, or domain evaluation.

## Install and try it

Requires Python 3.11 or 3.12.

```bash
python -m pip install -e .
max-slate ask --persona einstein --question "Explain time dilation simply."
max-slate ask --persona einstein --question "What is quantum computing?"
max-slate validate-persona src/max_slate/personas/einstein.json
```

The first question receives a bounded historical fallback. The second routes to educator mode. No answer is generated from a remote model or external service.

For development and tests:

```bash
python -m pip install -e '.[dev]'
pytest -q
python -m compileall -q src
ruff check src tests
```

## Repository map

- `src/max_slate/personas/` — persona identity, dates, style, and constraints.
- `src/max_slate/knowledge/` — local JSON loading and validation only.
- `src/max_slate/memory/` — ephemeral session bookkeeping; no long-term storage.
- `src/max_slate/safety/` — static policy-bounded response text.
- `src/max_slate/pipelines/` — deterministic route-then-answer flow.
- `knowledge_packs/einstein/` — small source-linked demonstration facts and quote-attribution metadata.
- `docs/` — architecture, policy, threat, accessibility, evidence, examples, and roadmap.

See [Evidence Status](docs/EVIDENCE_STATUS.md) for what is implemented, synthetic, targeted, unrun, or unvalidated. See [Sources and provenance](knowledge_packs/einstein/provenance/sources.json) for source records and their limits.

## Cite

Concept DOI (all versions): [10.5281/zenodo.23307947](https://doi.org/10.5281/zenodo.23307947). v0.1.0: [10.5281/zenodo.23307948](https://doi.org/10.5281/zenodo.23307948). See [CITATION.cff](CITATION.cff).
