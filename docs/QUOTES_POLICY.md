# Quotes policy

## Allowed statuses

Every quote-attribution record uses one of exactly these statuses:

- `VERIFIED` — an attributable primary source or reliable critical edition has been located and checked in context.
- `DISPUTED` — attribution is contested or available provenance is insufficient; the uncertainty and sources are stated.
- `UNSOURCED` — no adequate source has been identified. It must not be presented as a verified quotation.

A quote-search result or unrestricted quote collection is not proof. Prefer an original document, reliable archival facsimile, or scholarly/critical edition, using its context, date, language, translation, and editorial notes. The Einstein Papers Project editorial method describes why manuscript/transcription and contextual checks matter.

## Demonstration record

`knowledge_packs/einstein/quotes/attributions.json` includes a familiar saying about repeating an action and expecting a different result. It is marked **DISPUTED**, not verified. Quote Investigator reports no substantive evidence Einstein wrote or said it and traces early documented formulations decades after his death. That is a secondary investigation, so the record also preserves that limitation. This example is never spoken as Einstein's words.

No VERIFIED Einstein quotation is included in this initial prototype. For any future quote, store a provenance record separately, retain the exact source and page/document locator, and keep the quoted text within the persona's 25-word cap or paraphrase instead. Do not silently upgrade `DISPUTED` or `UNSOURCED` to `VERIFIED`.
