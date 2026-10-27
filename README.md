# Factorio 2.1.24 beginner manual

1. Double-click `index.html` in a browser. No server or internet required.
2. Work through the numbered lessons; check a step only when you complete it in the game.
3. Use keyboard controls, troubleshooting, glossary, diagrams and current-version reference as needed.
4. Use **Export progress** to save progress as a JSON file and **Import progress** to move it to another browser/computer.
5. For a local AI builder, start with `AGENT_HANDOFF.md` and `manual_data.json`; `controls.csv` is a searchable/exportable controls table.

To rebuild after editing `build.py`, run `python3 build.py`. It writes the HTML, data, references and ZIP beside the script. Use `python3 build.py --output-dir /path/to/output` for a separate output folder. Python 3 is needed only for rebuilding.

Browser regression checks (development only): install Playwright in a virtual environment with `pip install playwright`, then run `python tests/test_manual.py`. This uses system Chromium when available; otherwise run `playwright install chromium` first. For Firefox, run `playwright install firefox` and `python tests/test_manual.py --browser firefox`. Tests open the manual via `file:///` with networking disabled.

Progress is saved in this browser when local storage is available. If saving is blocked, the manual displays a notice; export a backup before closing. Imports accept exports from manual version 2.1.24 and replace current progress only after validation.

This is a broad, usable first-pass manual and research handoff, **not an exhaustive verified representation of every vanilla game prototype, machine, recipe or Lua/debug binding**. The handoff identifies how to reach that standard.
