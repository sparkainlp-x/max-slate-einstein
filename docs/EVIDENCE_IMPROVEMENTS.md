# Compatible evidence improvements

This branch builds on the implementation merged into main at `2b70c52`, rather than replacing it. The existing API, CLI defaults, original source registry, tests, documents, and audit format are preserved. Added behavior is opt-in with `--evidence`; structured output is opt-in with `--json`.

```bash
max-slate ask --persona einstein --question "Explain time dilation simply." --evidence --json
max-slate ask --persona einstein --question 'Did Einstein say "our science, measured against reality, is primitive and childlike"?' --evidence --json
```

The equivalent Python API is `answer_question(question, use_evidence=True)`. Without this argument, default fixed answers are unchanged. All `Answer` objects now include `simulation: true`, identity disclosure, source IDs, quote status, uncertainty, and an evidence label. These are added fields; existing fields remain. The evidence CLI also includes identity in the visible text.

The packaged evidence contains a small, manually checked source-linked historical inventory. NobelPrize.org supports lifespan and Nobel motivation. The IAS historical exhibit supports milestones and a short exact quotation excerpt; the excerpt is verified against that secondary institutional exhibit, not independently against an original manuscript. OpenStax/Rice University supports the time-dilation clock explanation. Quote Investigator supplies a separately marked DISPUTED fish/tree attribution. No bulk quote collection is accepted as proof. Unmatched questions receive uncertainty; modern explanations remain TARGET.

The exact ISO date `1955-04-19` and later routes to educator mode. The prior implementation's precedence is retained: explicit modern topics take educator mode before quote-check mode, even if quotation words are present. This differs from the attached simple routing list; it preserves an existing tested historical boundary rather than silently changing main behavior. Natural-language dates and indirect modern concepts are not comprehensively recognized.

Unicode input is normalized, questions longer than 2,000 characters are refused, and explicit identity impersonation or invented biography requests are refused. These remain English heuristics, not a validated semantic safety classifier. No hidden network calls or long-term memory were added.

The inherited opt-in audit stores a SHA-256 of the question. That hash is **not anonymization**: predictable questions can be guessed and matched. Audits are local, plaintext, unsigned, and not tamper-proof; users should not submit real personal data. CLI arguments may be visible in shell history and process listings. No independent security, historical, accessibility, or human evaluation has been conducted.

Speech, lip-sync, a hosted avatar, broad modern explanations, multilingual semantic routing, and holographic-fan export are TARGET. This repository change does not make the existing beaver speak and does not modify its website. CI outcomes apply only to the exact recorded branch run.
