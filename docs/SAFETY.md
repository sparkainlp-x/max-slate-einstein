# Safety

The engine is an educational research prototype, not medical, legal, financial, or safety-critical software. It must not be used as a substitute for a qualified professional or emergency services.

## Current behavior

- Explicitly matched harmful instructions route to `refuse`.
- Matched medical, legal, or financial advice requests route to `refuse`.
- The refusal text offers general education or suggests a qualified professional; it does not provide steps or a diagnosis.
- Modern/post-1955 questions route to educator mode and use the specified historical-boundary text.
- Other requests receive fixed, bounded text. The engine does not generate a detailed answer by inventing facts.

## Limitations

The rules are keyword/regular-expression checks, not a comprehensive intent or context model. They can miss euphemisms, other languages, obfuscation, novel hazards, and indirect requests; they can also refuse benign questions that match a pattern. They do not moderate arbitrary downstream systems. There is no adversarial or independent safety evaluation.

The core package has no network calls or unrestricted browsing. Its lack of network access reduces exposure to remote data but does not provide sandboxing, operating-system hardening, dependency scanning, or protection from unsafe use of local files. No real personal data is included in the repository fixtures.

Synthetic tests demonstrate only the tested rule behavior; they do not establish human, historical, or safety authenticity.
