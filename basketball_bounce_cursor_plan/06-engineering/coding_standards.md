# Coding Standards & Review Checklist

## Python
- Readable functions, type hints, `pathlib`, explicit exceptions.
- Pure domain logic where possible; don’t hide state in globals.
- Use dataclass for typed `Frame`, `Track`, `Event`, `Experiment`.
- Prefer standard libs and a few familiar packages to complex frameworks.
- No web server, message broker, DB or Docker as default.

## Logging
Include `run_id`, module, video timestamp/frame, warning reason and stage. Log a summary of missing detections, track resets and output file paths.

## Review checklist
- [ ] Input/output units explicit.
- [ ] No event counter increments inside video overlay code.
- [ ] No GT leakage into model thresholds.
- [ ] No silent ID-switch assumptions.
- [ ] Seed/config/weight hash saved.
- [ ] Tests cover 2 simultaneous contacts.
- [ ] Baseline results preserved.
- [ ] Frame timestamp correct.
- [ ] README reproducible on Windows.

## Docs
Every public CLI command documented, with one valid runnable example. File headers short; architecture decisions live in markdown rather than large code comments.
