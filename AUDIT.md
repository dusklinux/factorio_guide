# Factorio manual audit — 2.1.24 base game

Audit date: 2026-10-27. This audit covers the structure, teaching content, numerical reference and offline application. It does not certify a complete Freeplay playthrough or every engine rule.

## Macro audit

The original manual had 24 brief lessons, a single large build script, 121 controls and two small interactions. Advanced material interrupted the first-launch sequence. Recipes lacked quantities and dependencies in many places; several systems were reduced to a few steps. The “all shortcuts” label overstated the coverage, and contextual and expansion controls were mixed together. Search worked only inside selected screens.

The revised manual keeps the original progress IDs and step positions, puts the first-launch sequence before optional advanced systems, and links each lesson to deeper topics. The topic library covers materials, production mathematics, transport, energy, chemistry, science, defense, outposts, rail dispatch, robotics, construction tools, circuits, nuclear, player tools, launches, statistics and diagnosis. Each topic has a purpose, a causal explanation, a testable exercise, related topics and source links. A global search connects the teaching material and numerical catalogues.

Content, interface assets, extraction tools and validation are separate files. The builder embeds everything in one HTML file, so the reader still needs no server, installation, network connection or build step. Reading options include larger text, high contrast and optional one-step views; the full lesson remains available for printing.

## Micro audit: corrections and omitted prerequisites

- **Mod scope:** Recycler is a separate expansion mod in 2.1. Setup explicitly disables it along with Space Age, Quality and Elevated Rails, ensuring the base-only recipe set applies.
- **Early research triggers:** produce 50 iron plates for Steam power, 10 copper plates for Electronics, and craft a lab after the prerequisites to unlock red science. Then supply 10 red packs to research Automation. Crude extraction and uranium mining have their own trigger gates. The original walkthrough did not explain these gates.
- **Rocket payload:** an accepted payload is required; a satellite is not the only accepted payload. A satellite yields science; raw fish is the special achievement alternative. The useful learning route still launches a satellite.
- **Satellite ingredient:** 100 processing units, not advanced circuits. Satellite, rocket parts, silo and pad are distinct budgets.
- **Rocket research:** the prerequisites include speed-module-3 and productivity-module-3 technologies even though installing modules is optional. The five required pack types and the silo research cost are explicit.
- **Rail blocks:** automatic reservations and signal colors are explained separately from overlay colors. Manually driven trains ignore protection. Train stop capacity, dispatch priority, groups, interrupts and station handling are no longer omitted.
- **Inserters:** ordinary inserters can pick from either belt lane. Insertion limits, filters, power, hand size and orientation have separate explanations. Bulk and expansion stack inserters are distinguished.
- **Chemistry:** multi-output back pressure, heavy/light reserves, cracking ratios, catalyst returns, barrel cycling, coal liquefaction and the difference between fluid storage and transfer are explicit.
- **Nuclear:** used cells must be removed. U-235 expectations are probabilistic; Kovarex gross output is not net gain. Heat, steam and electrical capacity are separate limits.
- **Numbers and units:** crafting speed, recipe seconds, products per craft, productivity, per-tick prototype fields, MJ versus MW and gross versus net output are labeled.

## Exact numerical evidence

The factual dataset is extracted from [Wube factorio-data 2.1.24](https://github.com/wube/factorio-data/tree/2.1.24), commit `acf5a342afcb66c066b9d88d202e8622112da117`. The provenance record includes SHA-256 hashes of input files. Recipes, technologies, fluids and mod-defined custom inputs are evaluated as declarative Lua. Visual icon helpers are removed. Generated barrel recipes follow `base/data-updates.lua`; parameter placeholders are excluded. Declared entity and item fields are read from the Lua syntax tree. Computed fields are deliberately omitted rather than guessed.

Recipe defaults (including 0.5 seconds and productivity disabled by default) were checked against the [official prototype API](https://lua-api.factorio.com/latest/prototypes/RecipePrototype.html), which identified version 2.1.24 when checked. The reference currently contains 206 recipes, 196 technologies, 304 entity records, 241 item records and 8 fluids. These counts describe this extraction boundary, not every runtime prototype.

The build validates unique IDs, contiguous lesson phases, all internal teaching links, all recipe and technology links, every technology prerequisite, absence of prerequisite cycles, valid ingredient amounts, source URLs and complete control metadata. Reference values are not typed a second time into calculator tables.

## Source conflicts

Official pages were researched directly and linked in the manual, but their passages are not equally current:

- The [general fluid page](https://wiki.factorio.com/Fluid_system) includes old pressure-model discussion alongside modern connected-segment rules. The modern rules are used.
- The [general logistics page](https://wiki.factorio.com/Logistic_network) describes 1 MW robot charging slots, while the [roboport page](https://wiki.factorio.com/Roboport) and pinned definitions specify 500 kW per slot. The pinned value is used.
- The [nuclear tutorial](https://wiki.factorio.com/Tutorial:Nuclear_power) itself warns that tank-based control advice needs updating. Direct reactor circuit readings are acknowledged.
- The [older time page](https://wiki.factorio.com/Time) has a day-length table inconsistent with current references. The manual avoids deriving solar planning from that stale table.
- The [controls table](https://wiki.factorio.com/Controls) contains a duplicated scroll-up label for tooltip scrolling. Opposite scroll directions are explained without repeating the typo.

## Verification boundary

The application is tested through `file:///` with browser networking disabled. Regression coverage includes navigation, reference rendering, all topic and data links, search, filters, progress persistence and validation, edition-1 progress imports, keyboard focus, reading options, calculators, printing state, invalid URLs, mobile overflow and blocked/corrupt storage. Numerical tests cover known recipe/science/rocket examples and catalyst/probability handling.

Final regression results: **10 dependency-free tests passed**, including archive extraction/rebuild consistency. **Chromium and Firefox each passed all 1,052 offline routes** and the functional checks above, including 375px mobile layouts at standard and 130% text size, with no JavaScript errors or network requests. Diagram enlargement and keyboard dismissal were checked as well.

No automated check proves that every instruction succeeds in the actual game. There was no 2.1.24 Freeplay replay, and no exhaustive inspection of a live 2.1.24 Controls panel. The installed game log available during the audit was 2.1.14; it was not treated as authoritative 2.1.24 gameplay evidence. The manual states these limits in its own coverage screen.

## Remaining depth

The recipe and technology catalogues provide broad numerical coverage. This is still not a complete scripting API encyclopedia, exhaustive achievement strategy guide, placement simulator, raw-resource optimization solver, or proof of every combat/pathfinding edge case. Adding those requires separate verified models and runtime evidence. They are not represented by fabricated precision or an unsupported “PhD complete” label.
