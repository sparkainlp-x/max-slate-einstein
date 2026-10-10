# Accessibility

## Current interface

The initial interface is a command-line tool. It uses standard text output, route labels, and conventional argparse options. It does not rely on color, animation, mouse-only controls, audio, or timed interaction. Help is available with `max-slate --help`, `max-slate ask --help`, and `max-slate validate-persona --help`.

## Content

Responses are plain text and concise. The README and policy docs explain that route labels describe deterministic rules, not confidence or expert review. The prototype's fixed answers may still be too terse or unsuitable for some learning needs.

## Limitations and targets

No formal accessibility audit, screen-reader compatibility test, user study, translation, dyslexia review, or WCAG conformance assessment has been completed. These are **TARGET** areas for any future graphical interface; the current CLI should not be described as fully accessible.
