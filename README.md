# Factorio 2.1.24 offline field manual

Open **index.html** in Firefox or Chromium. No server, internet connection or build step is needed for reading.

Start with the numbered walkthrough. Use the topic library for deeper explanations and global search for lessons, keybinds, troubleshooting, recipes, technologies, machines, items and fluids. The manual includes worked examples, experiments, production/science/launch calculators, larger text, high contrast and one-step reading. Scope: **base game, without Space Age, Quality, Recycler or Elevated Rails**.

Checkboxes remember what you tried; the manual does not read your game save. Use **Export progress** for a backup and **Import progress** to restore or transfer it. Imports replace progress only after validation. Original 2.1.24 progress exports remain supported. A storage warning appears if the browser cannot save locally. Keep game saves and blueprint exports separately.

Exact recipe and technology records come from Wube’s pinned 2.1.24 prototype definitions. Read **AUDIT.md** or the in-app **Audit & coverage** page for corrections, evidence and remaining limits. This is a substantial researched reference, not a certified in-game replay or an exhaustive account of every engine edge case.

## Rebuild

Python 3.15+ is required only for development. Run:

```sh
python3 build.py
```

This validates content and writes `index.html`, `manual_data.json`, `controls.csv` and `factorio_2_1_24_offline_manual_and_agent_pack.zip`. Use `--output-dir /path/to/output` for a separate delivery folder. The archive includes sources, tests and documentation for rebuilding after extraction. Edit the source files listed in **AGENT_HANDOFF.md**, not the generated files.

The Python sources use 3.15 lazy imports, `frozendict`, immutable JSON decoding, `sentinel` and unpacking comprehensions where applicable. Reference data stays immutable during the build; generated JSON and HTML retain their existing formats. CLI help works without installing optional browser or extraction dependencies. Text files use explicit UTF-8, including when Python's UTF-8 mode is disabled.

## Test

Content and archive checks need only Python:

```sh
python3 -m unittest discover -s tests -p 'test_data.py' -v
```

For real-browser checks, install development dependencies in a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/pip install playwright
.venv/bin/playwright install chromium firefox
.venv/bin/python tests/test_manual.py
.venv/bin/python tests/test_manual.py --browser firefox
```

The Chromium check uses system Chromium when available. Tests open `file:///` with networking disabled.

## Refresh the pinned data

A normal rebuild uses the committed JSON and needs no Lua, parser or network access. To reproduce extraction, install Lua and the Python development package `luaparser`, check out Wube’s `factorio-data` tag `2.1.24`, then run:

```sh
python3 tools/extract_reference.py /path/to/factorio-data
```

The extractor rejects a checkout with a different commit. Computed entity fields are omitted; see the provenance in `data/reference.json`. Original text and schematic diagrams are authored for this manual. The factual data source is [Wube factorio-data](https://github.com/wube/factorio-data); no proprietary game sprites are bundled.
