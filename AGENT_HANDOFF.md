# Maintaining the Factorio 2.1.24 offline manual

Read `AUDIT.md` before extending claims of correctness or completeness. The game target is base 2.1.24 with Space Age, Quality, Recycler and Elevated Rails disabled. Keep the first-rocket route approachable and put advanced explanations in the topic library.

## Source files

- `build.py`: the original ordered lesson definitions and the deterministic offline build entry point.
- `content.py`: researched corrections, topic articles, links, controls enrichment and the audit/coverage data.
- `data/reference.json`: factual recipe, technology, entity, item and fluid records from the exact Wube commit recorded inside it.
- `tools/extract_prototypes.lua` and `tools/extract_reference.py`: reproducible extraction. Entity records are literal fields, not a complete runtime dump.
- `web/template.html`, `web/styles.css`, `web/app.js`: maintainable interface sources embedded into the generated `index.html`.
- `validate.py`: dependency-free build-time structural validation.
- `tests/test_data.py`, `tests/test_manual.py`: content/provenance and real-browser regression checks.

## Invariants

Keep original chapter IDs and original step indexes stable so existing progress exports remain meaningful. Update an instruction in place when correcting it; do not silently reinterpret a completed checkbox by inserting steps before it. New manual editions have a separate edition field; `manualVersion` identifies game-version compatibility.

Do not edit generated `index.html`, `manual_data.json` or `controls.csv` directly. Rebuild with `python3 build.py`. The default output is beside the script; `--output-dir` supports a separate delivery folder. The archive includes everything needed to rebuild after extraction.

No CDN, remote fonts, remote images, telemetry or runtime fetches. External links are optional source verification only. Keep file-URL support and test both Chromium and Firefox offline. Preserve keyboard focus and avoid using color alone to explain diagrams. Include text equivalents for visual material.

For numerical facts, prefer Wube's exact-version declarations and current in-game Factoriopedia. Wiki pages can contain expansion tabs, stale sections or contradictory figures. Keep source attribution and clearly label uncertain, computed and experimental claims. Respect copyrighted prose and sprites: author original explanations and schematic visuals.

Do not replace honest extraction limits with “complete runtime data.” Do not treat a unit test or browser test as an in-game Freeplay certification. Do not claim a raw-ore solver when reporting only direct ingredients. Controls are contextual; some have no default key and optional mod controls must remain separate.
