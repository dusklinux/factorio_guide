# Factorio 2.1.24 — Offline beginner manual | Implementation handoff

**As-of date:** 2026-10-27  
**Target:** Factorio **2.1.24 base game** on Linux/Wayland, *without* Space Age, Quality, Elevated Rails, or overhaul mods.  
**Current provenance:** Official Factorio wiki has published 2.1.24 changelog; Factorio team release notice dated 27 Oct. At observation 2.1.24 is experimental; 2.1.23 is the latest confirmed stable branch.  
**Delivery:** `index.html` is a genuinely offline prototype and usable manual; `manual_data.json` is structured content to extend; `controls.csv` is an editable command reference.

## User experience contract

The user learns mainly visually, can be overwhelmed by complexity, and has basic hands-on experience without ever completing the base game. **Do not teach historical version progression.** Assume a first-time player in the current 2.1.24 game. Prioritize: one idea per screen; a labeled diagram; one small set of steps; a test the user can perform in game; an explanation of why it works; a quick path to 'why is this broken?'. Progress is user-confirmed, not automatically inferred from gameplay. Support opening fully offline in Chromium/Firefox from `file:///` with no network or build step.

## Non-negotiable scope safeguards

- Base-game victory **rocket + satellite + cargo landing pad**. In 2.1 base, satellite is required to launch; cargo landing pad receives **1,000 space science packs**. No Space Age destinations.
- Exclude content that requires Space Age, Quality, or Elevated Rails: Vulcanus/Fulgora/Gleba/Aquilo, space platforms, quality items, green/turbo belts, elevated rail ramps, foundries, recycler, biological production, interplanetary logistics. Do not mislabel newer base-game circuit/fluids UI as DLC-only.
- Base science: automation (red), logistic (green), optional military (black), chemical (blue), production (purple), utility (yellow); space science is post-launch.
- Rail rules: blocks, red/yellow/green state, chain blue partial paths, signals on right side of travel, chain before conflicting crossings and normal exits with train-length clearance.
- Fluid rules: 320×320-tile maximum pipeline-segment bounding box; powered pumps divide segments; 2.1 fluid mixing prevention and UI; 2.1.24 restored selection visualization.
- Power: 1 boiler = 2 steam engines = 1.8 MW maximum, one offshore pump theoretically supplies 200 boilers under current water balance. **Older official Quick Start is outdated on pump-to-boiler count.**
- Robots: roboport orange logistics 50×50 tiles, green construction 110×110 tiles; logistic network connection requires touching orange areas. Separate construction and logistics functions.
- Linux 2.1: SDL3, `auto` driver prefers Wayland only with compositor fifo-v1 support, otherwise X11; actual display mode depends on compositor and game. No claim that every Arch setup runs native Wayland.

## Current 2.1.24 particulars (not version history for players)

1. Restored selection fluid pipeline visualization; corresponding interface setting enabled by default.
2. Wire-cursor can select only eligible entities.
3. Quickbar settings section added to Interface settings.
4. Testing CLI switches added (not a beginner-facing game mechanic).
5. Bug fixes of saves, robot module insertion, map search, fluid throughput, GUI; not things the learner needs to memorize.

Other meaningful 2.1 base-game quality-of-life to teach contextually: flippable pumpjacks/burner drills/inserters; reliable belt splitter insertion; fluid mixing warnings; pipe/tank real-time UI; pipe/boiler/lab/mine circuit connections; separate circuit Input/Output wire selectors; decider else-output; selector signal/time/index modes; Factoriopedia pin/hide-unresearched; Spidertron patrol; train wagon pump flexibility; rail rolling-stock upgrades; empty quickbar quick-pipette; Linux SDL3/Wayland changes; improved enemy expansion and shotgun balance. Keep Quality, orbital rockets and landing-pad unloading bay tagged as expansion features.

## What the starter prototype already provides

- 24 tutorial chapters with **140 checkable, ordered steps**, each chapter with labeled original SVG diagram, actionable self-checks, useful habits, official-source links.
- 121 searchable contextual PC keyboard/mouse commands; advanced and DLC-only controls explicitly labeled where known.
- 27 symptom → likely cause → first fix entries; 31 plain-language glossary entries.
- Current 2.1 QoL comparison, official source register and a simple interactive train signal thought experiment + steam capacity sandbox.
- Offline progress via localStorage plus portable JSON export/import; responsive layout; print stylesheet; no external scripts, images, fonts or APIs.

## Upgrade backlog for an advanced local AI build

**P0 — Correctness + accessibility:** Compare every control and recipe against 2.1.24's live Settings → Controls and Factoriopedia with base-only mods. Annotate all values with confidence/provenance. Add user-selectable text size and high-contrast diagrams; every picture needs text equivalents and keyboard focus. Persist multiple saves/profiles without online sync. Optional cross-platform keybinding customizer, which never claims to modify Factorio itself.

**P1 — Interactive microsimulations:** draggable machines with orientation/ports and arrows; 2-lane belt splitter; inserter pick/drop; separate wire/circuit signal browser; connect-power-poles coverage explorer; schematic oil refinery with visible input/output and back-pressure warnings; track-block coloring with chain vs regular rail signals and multi-train deadlock examples; roboport logistic vs construction coverage painter; science recipe dependency graph; interactive rocket checklist. Visuals must be **explicitly conceptual** until placement and crafting correctness are tested against the game.

**P2 — Exhaustive reference:** official machine list including footprints, energy, recipes, rates, inventories, module support; every science pack and dependency; rail train scheduling/interrupts/groups/limits/priorities/temporary stops; circuit cookbook + truth tables + combinator delay; full oil chemistry; nuclear and solar; defensive tactics; production statistics; remote view and pins; blueprints filtering/parameterization/import-export; practical ratios with caveats; editor/debug controls separated from gameplay; a searchable “why did this stop?” decision tree; a first-rocket bill of materials calculator driven from extracted **base game 2.1.24 prototype data** not remembered numbers.

**P3 — Visual learning:** author original in-game screenshots (taken legally by the user) with Alt-mode and annotated arrows, create a before/after for every action, embed captions and keyboard keycaps, use progressive disclosure (“show why”, “show more detail”, “hint”), contextual glossary popovers, 1-minute recall questions, optional learning route for peaceful worlds. Avoid dumping whole chapters by default; users should be able to choose step-by-step mode.

**P4 — Offline package QA:** test Firefox/Chromium browser with internet disabled and from `file:///`; test smaller viewports and keyboard navigation; ensure no CDN/cross-origin images; progress survives ordinary restarts and export/import works; print-friendly; proper base-only coverage tests; role/content metadata; source URLs kept as optional references only; no analytics or telemetry.

## Source quality and provenance rules

Use Factorio's official wiki as primary reference, official Factorio 2.1 stable announcement for major changes, *actual 2.1.24 version-history page* for exact patch, and the in-game changelog (Main menu → About → Changelog) as final installation check. On wiki entries with Base game and Space Age tabs, base tab exclusively; avoid third-party modded tips unless cross-checked. The older Quick Start is conceptual only; prefer up-to-date dedicated Power production, Fluid system, Controls and Rocket silo pages. As UI can be rebound, the user's live Controls list is authoritative.

### Official reference links
- [Official complete 2.1 version history incl. 2.1.24](https://wiki.factorio.com/Version_history/2.1.0)
- [Official current keyboard/mouse controls](https://wiki.factorio.com/Controls)
- [Keyboard shortcuts tutorial](https://wiki.factorio.com/Tutorial:Keyboard_shortcuts)
- [Beginner quick start (some ratios are outdated)](https://wiki.factorio.com/Tutorial:Quick_start_guide)
- [Assembling machine](https://wiki.factorio.com/Assembling_machine)
- [Belt transport system](https://wiki.factorio.com/Belt_transport_system)
- [Power production (current ratios)](https://wiki.factorio.com/Power_production)
- [Fluid system (modern mechanics)](https://wiki.factorio.com/Fluid_system)
- [Science packs and research](https://wiki.factorio.com/Science_pack)
- [Research](https://wiki.factorio.com/Research)
- [Enemies and pollution](https://wiki.factorio.com/Enemies)
- [Production statistics](https://wiki.factorio.com/Production_statistics)
- [Train signals tutorial](https://wiki.factorio.com/Tutorial:Train_signals)
- [Train stops, train limits and priority](https://wiki.factorio.com/Train_stop)
- [Oil processing and cracking](https://wiki.factorio.com/Oil_processing)
- [Roboport coverage](https://wiki.factorio.com/Roboport)
- [Logistic network and chests](https://wiki.factorio.com/Logistic_network)
- [Blueprint](https://wiki.factorio.com/Blueprint)
- [Circuit networks](https://wiki.factorio.com/Circuit_network)
- [Modules](https://wiki.factorio.com/Module)
- [Nuclear tutorial](https://wiki.factorio.com/Tutorial:Nuclear_power)
- [Rocket silo in base game](https://wiki.factorio.com/Rocket_silo)
- [Linux file locations](https://wiki.factorio.com/Application_directory)
- [Official 2.1 stable overview](https://factorio.com/blog/post/fff-449)
- [Alerts and icons](https://wiki.factorio.com/Alerts)

## Licensing

Diagrams here are newly drawn HTML SVG abstractions, not redistributions of Factorio proprietary sprites. The official wiki has its own terms. Do **not** scrape all wiki prose or copyrighted diagrams into the finished manual. Summarize facts, link sources and use original visuals; only use third-party media if rights and attribution are verified.

## Research acceptance checklist for your local agent

- Can a complete beginner finish the sequence without prior game concepts? Check each step by replaying it in 2.1.24 Freeplay.
- Does each diagram show the correct input/output flow AND an explanation of what to do when the flow stops?
- Does searching “Q”, “chain”, “steam”, “no path”, “satellite”, “Wayland” find an actionable explanation?
- Does the research map distinguish stable 2.1 and experimental 2.1.24 without misleading about content?
- Are Space Age-only visuals/items excluded from the novice route and explicitly labeled when mentioned?
- Can all important instructions be followed with offline internet disconnected?
- Has every hard-coded recipe, production ratio or item count been verified against unmodded 2.1.24 base game rather than a stale 1.x wiki page?
