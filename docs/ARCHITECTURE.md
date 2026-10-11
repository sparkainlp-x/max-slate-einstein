# Architecture

## System boundary

Max Slate Einstein is a deterministic Python package. At runtime it reads the bundled persona JSON and routes one question to one fixed response. It does not invoke a language model, access the network, browse, or search beyond local JSON files. There are no runtime third-party dependencies.

## Separated components

- **Persona** (`personas/einstein.json`): identity boundary, lifespan, allowed/caution/forbidden topics, quote policy, memory policy, and style.
- **Knowledge** (`knowledge/` plus `knowledge_packs/einstein/`): local JSON parsing and source-ID checks. Facts do not become validated merely because they parse.
- **Memory** (`memory/`): in-process turn counter only. It does not hold question, answer, or profile text.
- **Safety and routing** (`router.py`, `safety/`): fixed deterministic rules and fixed route text.
- **Engine and pipeline** (`engine.py`, `pipelines/`): validate persona, classify, return a bounded response, and optionally increment ephemeral session state.
- **Audit** (`audit.py`): opt-in JSONL metadata record. It omits raw question and answer text; the question digest can still reveal information if an attacker can guess candidate questions.
- **CLI** (`cli.py`): runs `ask` and persona validation locally.

## Request flow

1. Load and validate the local persona.
2. Classify in a fixed priority: empty/non-text → `unknown`; harmful or professional-advice request → `refuse`; explicit post-1955 year or configured modern topic → `educator`; quote-attribution phrase → `quote_check`; otherwise → `historical`.
3. Return one static response associated with the route. The current engine does not generate a source-specific scientific explanation.
4. If a session counter was explicitly provided, increment its turn count without retaining user text. If an audit path was explicitly provided in the CLI, append metadata locally.

## Invariants

- No first-person experiential claim about events or technologies after 1955.
- No claim that the software is Einstein, channels him, or is conscious or autonomous.
- No quote attribution without source verification; disputed status is preserved.
- Long-term and sensitive-data memory are disabled.
- Unsupported questions do not trigger unrestricted retrieval or fabricated detail.

The implementation is a research prototype, not a production-grade conversational AI or safety filter.
