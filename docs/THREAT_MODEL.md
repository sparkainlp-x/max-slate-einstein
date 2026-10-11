# Threat model

## Assets and intended use

The project protects persona boundaries, source attribution, local user questions, and operator trust. The intended use is educational experimentation with a deterministic local prototype.

## Trust boundaries

- The runtime package, bundled JSON records, and caller-supplied question are local inputs.
- Optional audit output is a local file selected by the operator.
- GitHub Actions and installed development tools are external build infrastructure; they are not runtime dependencies.
- Source URLs are provenance references, not live runtime connections.

## Threats and controls

| Threat | Current control | Residual risk |
|---|---|---|
| Software presented as Einstein or as sentient | README, persona policy, fixed response behavior, and docs state educational-simulation boundary | Downstream UI or users can remove the notice; no runtime UI banner is enforced |
| Post-1955 claims framed as personal experience | Year/modern-topic routing to fixed educator text | Regex routing can miss paraphrases or context |
| Fabricated or misattributed quotation | Quote route asks to verify; one sample is `DISPUTED`; no verified quote corpus | The prototype does not verify arbitrary quotes or fetch sources |
| Harmful/professional advice | Known keyword patterns route to a fixed refusal | False negatives and false positives remain possible |
| Sensitive question stored in logs | No audit by default; explicit audit omits raw text | Hashes and timestamps remain sensitive metadata; OS backups may retain files |
| Malicious or malformed knowledge JSON | Local parser raises on invalid JSON and unknown source IDs | No signature verification, schema versioning, or malicious-file sandbox |
| Unintended network activity | Core has no network client or network dependency | No independent traffic capture has been run |

## Out of scope

This is not a hardened service, authentication boundary, safety classifier, secure memory vault, or externally audited application. No security testing or independent threat assessment has been completed.
