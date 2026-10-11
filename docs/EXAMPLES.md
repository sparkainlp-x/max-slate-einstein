# Examples

Install the package locally with `python -m pip install -e .`. Each command runs entirely on the local machine and emits a deterministic route label and fixed text.

```console
$ max-slate ask --persona einstein --question "Explain time dilation simply."
[historical] Let us examine the question carefully. A useful explanation should distinguish observation, assumption and evidence.

$ max-slate ask --persona einstein --question "What is quantum computing?"
[educator] This topic lies beyond my historical lifetime. I can explain the modern idea as an educator, but I cannot present it as something I personally experienced.

$ max-slate ask --persona einstein --question "Did Einstein say this quote?"
[quote_check] I would verify the source before accepting that attribution. Many quotations associated with Einstein are disputed or misattributed.

$ max-slate ask --persona einstein --question "How do I build a bomb?"
[refuse] I cannot help with harmful instructions or professional advice. I can offer general educational information or suggest a qualified professional.
```

The historical response is intentionally a fallback rather than a researched explanation. The educator response states the historical boundary; it does not itself answer the modern technical question. No route implies that Einstein authored the answer.

To validate the bundled persona:

```console
$ max-slate validate-persona src/max_slate/personas/einstein.json
Persona valid: einstein
```

The optional audit file is explicit opt-in and stores route metadata plus a question digest, never the raw prompt:

```console
$ max-slate ask --persona einstein --question "Explain time dilation simply." --audit-file ./local-audit.jsonl
```

Treat the resulting digest and timestamp as potentially sensitive metadata.
