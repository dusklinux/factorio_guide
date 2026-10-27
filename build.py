import argparse, json, html, csv, zipfile
from pathlib import Path
parser = argparse.ArgumentParser(description='Build the standalone offline Factorio manual and ZIP.')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
P = args.output_dir.resolve()
P.mkdir(parents=True, exist_ok=True)
archive_path = P / 'factorio_2_1_24_offline_manual_and_agent_pack.zip'
chapters=[]
def add(id,title,phase,why,steps,diagram='',tips=None,checks=None,misconceptions=None,src=None):
    chapters.append(dict(id=id,title=title,phase=phase,why=why,steps=steps,diagram=diagram,tips=tips or [],checks=checks or [],misconceptions=misconceptions or [],sources=src or []))
add('setup','Before starting: the correct game','BEGIN','Start a base-game Freeplay save with the right game content and comfortable settings.',[
 'At the main menu, open Mods. Keep the base game enabled. Disable Space Age, Quality, Elevated Rails, and any other overhaul/gameplay mods for this manual. The Space Age expansion is NOT required.',
 'Start with the built-in Tutorial scenarios if you have never placed a drill or inserter. Then create a New Game → Freeplay world. Choose default settings or increase starting area if attacks are stressful.',
 'For a gentler learning save, consider Peaceful mode, or lower enemy frequency. These settings change the challenge; some achievements have restrictions. Save under a clear name and make backups.',
 'Open Settings → Controls to confirm keyboard bindings. Turn on Alt-mode (Alt) after you begin; it exposes recipes, filter icons, and directions.',
 'Your base-game win condition is to build a rocket silo, make a rocket and satellite, place a cargo landing pad, and launch the rocket. The satellite yields space science.'
], 'goal', ['Use one small goal at a time; leave space for future machines.','Do not try to make a perfect megabase or memorize every recipe.'],['I know whether Space Age is disabled.','I can find Controls, Freeplay and Save.'],['“Version 2.1” does not mean Space Age is active.'],['version','rocket','science'])
add('movement','The screen, cursor and first 15 shortcuts','BEGIN','Learn a small set of actions that makes the entire game less confusing.',[
 'W/A/S/D move the engineer. Mouse wheel zooms. E opens the character/inventory. Left-click opens machine windows or places held buildings; hold right-click to mine/remove a structure.',
 'Q clears the held item; when hovering an object, Q pipettes that object to your cursor if available. R rotates; Shift+R reverses rotation; H and V flip compatible layouts.',
 'Alt toggles informative overlays. F collects items from the ground or nearby belt. Z drops one held item. Ctrl+left-click transfers item stacks quickly in contextual situations.',
 'Use Shift+right-click on a configured machine to copy its settings and Shift+left-click on another compatible machine to paste. Press T for research, P for production statistics, Tab/M for map, and B for blueprint library.',
 'Hold a belt, pole, or underground belt and drag to place a repeated run. E closes many opened windows; Esc opens menu or backs out. Learn the controls panel if your Wayland compositor consumes shortcuts.'
], 'input', ['Default controls are context-dependent; the same key can do different things in an inventory versus in the world.','The quickbar is a shortcut bar, not extra item storage.'],['I can rotate, pipette and clear my cursor.','I can move items into/out of a machine without manually dragging each stack.'],[],['controls','hotkeys'])
add('mining','Mining and the first furnace','BEGIN','Understand the first complete production chain: ore becomes metal.',[
 'Locate iron ore, copper ore, stone and coal using the map. Mine a little iron, stone and coal by right-clicking on resources.',
 'Craft or use a burner mining drill and stone furnace. Place the drill over iron ore and point its output arrow toward the furnace or a chest. Open the drill and add coal.',
 'Fuel the furnace with coal as well. The drill places ore into the furnace; the furnace turns ore into iron plates without player intervention.',
 'Repeat for copper. Mine stone for extra furnaces; smelt some stone into stone bricks for later buildings.',
 'If nothing runs, check: resource under drill, fuel in drill, fuel in furnace, drill arrow, blocked output and furnace contents.'
], 'ore', ['Burner drills burn fuel; electric drills need electric power.','A building can be functional even if you have no inserters yet.'],['My miner places ore into a furnace.','I can explain why fuel and output are separate needs.'],[],['quick','machines'])
add('power','Electricity: the first steam plant','BEGIN','Give electric machines reliable, understandable power.',[
 'Place one offshore pump on water. Its water outlet must connect by pipe directly or indirectly to a boiler water input.',
 'Put coal into the boiler or feed coal with an inserter. Connect the boiler steam outlet to two steam engines using pipes or direct adjacency.',
 'Place electric poles so their wire network connects the engines and their blue power supply areas overlap the machines you want powered.',
 'Open any connected electric pole to inspect production, consumption and satisfaction. A working plant with no demand may idle; that is normal.',
 'Expand gradually. The core energy ratio is 1 boiler per 2 steam engines. For version 2.1, the official water-flow calculation says an offshore pump can theoretically feed 200 boilers, but long pipelines may need pumps and practical layouts should be modular.',
 'If a steam setup fails: trace water → boiler fuel → steam outlet → engine → electric wire → pole coverage → consuming building.'
], 'power', ['A boiler uses 1.8 MW of fuel at full output; two steam engines can generate 0.9 MW each.','Power wires connecting poles are not the same thing as the blue coverage area for machines.'],['I can open the electricity graph.','I can tell “no electricity”, “insufficient electricity” and “no fuel” apart.'],['Do not use pre-2.0 “1 offshore pump for 20 boilers” as the current water limit.'],['power','fluid'])
add('belts','Belts, inserters and two lanes','BEGIN','Move things automatically while understanding where every item travels.',[
 'Build an electric mining drill, an inserter, belt, furnace and another inserter. The drill outputs ore directly onto a belt.',
 'Build the first inserter to pick ore from the belt and put it into a furnace; use a second inserter to move plates out to another belt or chest.',
 'Each belt has TWO lanes. Observe which lane receives items and how the inserter drops items. Rotation R changes direction; Alt-mode makes arrows readable.',
 'Learn underground belts to cross another line, and splitters to divide/merge material streams. A splitter does not magically increase throughput.',
 'With a splitter GUI, set input/output priority and filters when needed. A common future use is giving an important machine priority for scarce resources.',
 'Reference rates for unstacked items on both lanes: yellow belt 15/s, red 30/s, blue 45/s. Upgrades need supporting production; a faster belt does not create more ore.'
], 'belt', ['Limit an output chest to a few slots so you do not unintentionally use every available resource on low-priority products.','Drag poles, belts, underground pieces and similar buildings for much faster placement.'],['I can explain both belt lanes.','I can fix a furnace that is missing ore or unable to unload.'],[],['belts','hotkeys'])
add('automation','Automated crafting and reusable factory blocks','EARLY','Make useful items without handcrafting them repeatedly.',[
 'Research Automation, craft an assembling machine, place it inside powered pole coverage and left-click to choose a recipe.',
 'A recipe needs input ingredients, enough power, a valid assembler tier, and somewhere for the output to go. Feed ingredients from belts/chests with inserters; remove results with another inserter.',
 'Build dedicated mini-lines for gears, copper cable, electronic circuits, belts, inserters, ammunition and machines. They need not be fully optimized.',
 'Use Shift+right-click / Shift+left-click to copy recipe/settings among similar assemblers. Use Ctrl+C and Ctrl+V to duplicate a useful layout as ghosts, then build its pieces by hand or by robots later.',
 'Learn the bottleneck rule: the slowest upstream ingredient determines downstream production. If something stops, follow its inputs backward.'
], 'assemble', ['Electronic circuits use iron plates and copper cable; cable is bulky, so make it beside circuit assemblers rather than carrying massive cable belts across the factory.','Machine craft speed, recipe time, module bonuses and inserter speed affect ratios.'],['I have an assembler that runs without my inventory open.','I can identify which ingredient is missing.'],[],['machines','research'])
add('redgreen','Red and green science','EARLY','Turn your factory into a research engine.',[
 'Open T. Choose a technology that needs automation (red) science packs. Feed those packs to a powered lab with an inserter or by hand.',
 'Automate red science from copper plates and iron gears; automate gears in an assembler rather than continuously handcrafting them.',
 'Make transport belts and inserters and automate logistic (green) science: it requires one belt and one inserter per pack.',
 'Feed both science types to labs on belts, by inserters from chests, or by inserter-to-inserter transfer between labs.',
 'Prioritize logistics, steel processing, electronics, automation tiers and anything that solves an immediate limitation. A research queue can handle planned follow-ups.'
], 'science', ['Science packs are not points you manually spend: powered labs consume them over time for the selected technology.','Military (black) science can be optional for launching the base-game rocket, though very useful for defense.'],['My labs research automatically.','I know what a lab is waiting for if its progress stalls.'],[],['science','research'])
add('defense','Pollution, enemies and survival','EARLY','Prevent surprise losses without letting combat dominate the learning experience.',[
 'Open the map and enable pollution display to see the cloud. Pollution spreads and can provoke attacks when it reaches enemy nests; expansion and enemy evolution add future pressure.',
 'Automate basic ammunition, build gun turrets around likely approaches and keep them supplied. Walls can buy time; radars reveal distant threats.',
 'Fight with Space (nearest enemy near the cursor), Shift+Space (selected target) and switch weapons with C. Keep ammo in both turrets and your character.',
 'Before expanding toward enemy bases, prepare spare turrets, ammo, repair packs and a retreat route. Later use laser or flamethrower turrets if appropriate.',
 'Version 2.1 adjusted enemy expansion patterns; do not rely on leaving a map unexplored as a way to make nearby expansion easier.',
 'When you feel overwhelmed, inspect the world settings on a new practice save rather than increasing your factory production blindly.'
], 'defense', ['Build a small perimeter early when attacks are enabled.','Avoid running directly across active train tracks: trains are dangerous.'],['I can read the pollution overlay.','I have automatic ammo production and at least one protected approach.'],[],['combat','version'])
add('steel','Scale iron, copper, steel and stone','EARLY','Prepare for mid-game without rebuilding everything at once.',[
 'Make repeatable rows of electric drills feeding belts. Spread drills across ore patches, taking account of their mining areas.',
 'Separate iron and copper smelting lines. Steel is made by smelting iron plates again; it needs a meaningful share of your iron production.',
 'Leave build space beside every line. When it is slow, first increase miners, then furnace capacity, then belt throughput, then consumers.',
 'Reserve simple lanes or a mall (a collection of assemblers that makes belts, inserters, poles, furnaces, rails and other buildings for your personal use).',
 'Learn why a buffer chest hides brief shortages but does not fix a permanently under-supplied production line.'
], 'steel', ['Do not put every resource through one narrow bottleneck.','Use production statistics P to see whether a needed item is being produced and consumed.'],['I know why steel demand can suddenly drain iron.'],[],['machines','statistics'])
add('trains1','Railways I: your first automatic delivery','MID','Use trains to connect distant ore fields safely and simply.',[
 'Make a small one-way loop with a locomotive and cargo wagon; one-directional tracks are easier to learn than bidirectional shared track.',
 'Put a train stop beside each station track with the correct orientation (its arrow indicates arriving trains). Give stops clear distinct names.',
 'Load the cargo wagon at the mine using inserters from belts or chests. Unload at the main base using inserters into chests or belts; power the station equipment.',
 'Fuel the locomotive. Open the train GUI and create a schedule: Mine → Full cargo; Base → Empty cargo. Switch to Automatic.',
 'For longer railways, add regular rail signals to divide the line into blocks long enough to contain a complete train, including distance before merges.',
 'When No path appears, check the railway is continuous, locomotive faces a viable route, stop alignment, rail signals on the right-hand travel side, and whether the destination is reachable.'
], 'train', ['A train stop is a destination, not a rail signal.','Train limits cap how many trains are permitted to reserve a station; they do not cap cargo.'],['One train travels automatically and returns.','I can identify a valid one-way rail signal position.'],[],['rail','trains'])
add('trains2','Railways II: blocks, chain signals and junctions','MID','Learn how multiple trains share tracks without getting stuck.',[
 'Think of rail signals as doors dividing continuous rail into colored BLOCKS. Only one train can own a block at once (a long train can span several blocks).',
 'Normal rail signal: “enter if the following block is free.” Chain signal: “enter only if the following path is clear far enough to exit.”',
 'For a junction shared by crossing routes, place chain signals before and inside the conflict region where necessary; regular rail signals after the junction only when a full train can fit behind them.',
 'Always signal from the viewpoint of the travel direction: place signals on the RIGHT side. For two-way track segments pair opposite-facing signals, but two independent one-way tracks are much simpler.',
 'A chain signal can display BLUE when some exits are free and some blocked; it is not simply a green/red version of an ordinary signal.',
 'Introduce a second train after verifying each loop and each block. Name same-purpose stations consistently and consider station train limits, stacking areas and future train interrupts.'
], 'signals', ['Mnemonic: chain in, rail out — a starting rule, not a substitute for separating every actual crossing/conflict.','Do not place a normal signal directly before a crossing if the train could stop inside the crossing.'],['I can explain a block in one sentence.','I can explain why a chain signal belongs before an intersection.'],[],['rail','trains'])
add('fluids','Pipes, pumps and fluid networks','MID','Make the transition from solid items to fluids without guessing at pipe behavior.',[
 'Unlike ore and plates, fluids live in pipe connections, tanks, machines and fluid wagons. Inserters cannot grab loose fluid. Barrels are an optional method for transporting fluid as items.',
 'In modern Factorio, all connected pipes/tanks form one fluid segment. Fluid transport within a valid segment is effectively instant, with per-port transfer limits; it is not old-style pipe-by-pipe pressure simulation.',
 'A segment extending beyond a 320×320-tile bounding area becomes overextended. Split long pipelines into new segments with powered pumps; confirm pump direction.',
 'Different-fluid pipelines cannot simply merge. Version 2.1 warns about incompatible fluids and 2.1.24 shows the pipeline overlay when selecting a fluid entity by default.',
 'Use Alt-mode to reveal fluid input/output sockets. Open pipes and tanks to inspect pipeline contents and flow; for complex builds, connect them to red/green circuit wires if you want readouts.',
 'For train fluids: put pumps beside fluid wagons and power them. The 2.1 pump connector supports improved wagon alignment, including ends and curves.'
], 'fluid', ['A machine can stall because its output fluid is full, not because it is short of input.','Pumps require electricity; offshore pumps do not require electricity.'],['I can tell a fluid flow problem from a fuel/recipe problem.'],[],['fluid','version'])
add('oil','Oil processing: plastic, sulfur, cracking','MID','Understand the biggest new resource chain before blue science.',[
 'Place pumpjacks on crude oil wells, supply electric power, and pipe crude oil into a refinery. Use the basic oil processing recipe first: crude oil becomes petroleum gas.',
 'Route petroleum gas to chemical plants. Plastic requires petroleum gas and coal; sulfur requires petroleum gas and water. Both become essential intermediates.',
 'With Advanced oil processing, also supply water to the refinery. It produces heavy oil, light oil and petroleum gas from separate output ports.',
 'Use heavy oil for lubricant; use light oil for solid fuel/rocket fuel. Crack excess heavy oil into light oil, and excess light oil into petroleum gas when petroleum runs short.',
 'A refinery producing several fluids stops if even one output backs up. Store fluids in tanks and use pump conditions to crack only surplus oil.',
 'Use the status icon and fluid GUI, not guesswork: check every pipe, every recipe input, and whether any refinery output is full.'
], 'oil', ['Simple control example: activate heavy-oil cracking pump when heavy oil in tank exceeds a chosen reserve threshold.','Light oil is often a better solid-fuel feedstock than petroleum gas.'],['My plastic plant runs automatically.','I can explain what to do when heavy oil backs up.'],[],['oil','fluid'])
add('blue','Blue science, engines and advanced circuitry','MID','Build the first fully oil-dependent science line.',[
 'Automate sulfur and plastic. Automate advanced circuits from electronic circuits, plastic and copper cable.',
 'Build engine units from steel, iron gears and pipes. Engines must be crafted in an assembler; they cannot be handcrafting shortcuts for everything.',
 'Make chemical (blue) science from advanced circuits, engine units and sulfur in the required recipe counts.',
 'Add blue science to labs; research advanced oil processing and other technologies that unlock logistic robots, modules, better machines and later science.',
 'If blue science is stalled, follow the dependency chain in order: crude → petroleum → plastic/sulfur, plus iron/steel → engines and green circuits → advanced circuits.'
], 'science', ['Place assemblers for low-throughput expensive parts near their supply of circuits and plastic.','Keep a supply of lubricant for electric engines and higher-tier belts.'],['I have automated all ingredients for blue science.'],[],['science','oil'])
add('robots','Robots I: construction vs logistics','MID','Stop manually placing every repeated factory element.',[
 'Research robotics and construct roboports, construction robots and logistics robots. A robot needs a network/home, charge and a compatible task.',
 'Hover a roboport: orange 50×50 is logistics service area, green 110×110 is construction coverage. Two roboports share a logistics network when their orange areas touch.',
 'Place construction robots into a roboport, put needed buildings in available provider/storage chests, and place a blueprint or ghost inside green construction coverage.',
 'A passive provider chest offers items to a network. A storage chest accepts unsorted items. A requester chest requests a specified minimum stock from providers. Active provider and buffer chests have specialized roles.',
 'Logistics robots move items in the orange-connected logistics network; construction robots handle building, deconstruction and repairs within green coverage. Personal roboport equipment is a separate local build network.',
 'If bots idle, verify task coverage, item availability, chest type, power, roboport connection, number of bots and charging congestion.'
], 'bots', ['Do not expect logistic bots to fill a chest outside orange coverage even though construction robots can build there.','Requester chests depend on later research; begin with construction robots and passive/storage chests if requesters are not unlocked yet.'],['I can distinguish construction and logistics bots.','I can explain orange versus green coverage.'],[],['bots','logistics'])
add('blueprints','Blueprints, ghosts and painless rebuilding','MID','Save designs and repeat them with fewer mistakes.',[
 'Ctrl+C drag-selects entities to copy as a temporary blueprint. Ctrl+V pastes it. Ctrl+X cuts/marks for removal. Ctrl+Z undoes certain build/deconstruct actions; Ctrl+Y or Ctrl+Shift+Z redoes.',
 'Create a permanent blueprint with Alt+B. Store it in the blueprint library B or organize several in a blueprint book.',
 'A translucent ghost is a plan, not an automatically built object. Construction robots need the item, construction coverage and power to build it.',
 'Shift+left-click when holding a building makes a ghost even if you do not have the item. Use the upgrade planner Alt+U and deconstruction planner Alt+D for large changes.',
 'Press H/V to flip compatible blueprints. Some buildings and complex recipes cannot be flipped in every orientation; inspect pipe ports and outputs.',
 'Try copy-pasting four working smelters or a small assembler line. Resist the urge to import a giant external blueprint before you understand its flows.'
], 'blueprint', ['Shift+mouse wheel cycles clipboard history while holding paste.','Quickbar slots can store references to blueprints and frequently built items.'],['I know why a ghost is not immediately built.','I can undo a misplaced blueprint and preserve an important layout.'],[],['blueprints','hotkeys'])
add('circuits','Circuit networks: simple switches first','ADVANCED','Use logical conditions without requiring programming experience.',[
 'A circuit network carries named signals (for example “iron plate = 200”) along red/green wires. It is not an electricity cable and it cannot power machines.',
 'Connect a storage tank to a pump with a red or green circuit wire. Set the pump enabled condition to “heavy oil > 10,000” to crack surplus oil.',
 'A constant combinator outputs chosen signals. An arithmetic combinator calculates quantities. A decider combinator compares quantities and outputs a result. A selector combinator chooses among signals.',
 'In version 2.1, circuit-connected machines can choose which wire colors are INPUT and which are OUTPUT. This prevents certain unwanted feedback loops and is especially useful on combinators and request-controlled machines.',
 'Practical first projects: limit inserters based on chest count; turn an alarm light on when ammo is low; set dynamic station train limits from cargo or free capacity.',
 'Debug by hovering a wire connection to read signal values. Trace where the value comes from, which wires are selected, the condition, and what receives the result.'
], 'circuit', ['Keep your first circuits simple: one reader, one condition, one actor.','Decider combinators in 2.1 support else outputs; circuit signals can also control labs, heat devices, mines and pipes.'],['I can wire a pump to a tank.','I can distinguish a red/green signal wire from an electric pole connection.'],[],['circuit','version'])
add('late','Production, utility science and rocket ingredients','LATE','Prepare the final research and the heavy industrial requirements.',[
 'Production (purple) science uses advanced manufacturing, including electric furnaces, rails and productivity modules. Automate these instead of handcrafting stacks.',
 'Utility (yellow) science uses advanced resources such as processing units, low-density structures and flying robot frames. Make them permanent production lines.',
 'Processing units demand advanced circuits, electronic circuits and sulfuric acid. Low-density structures require copper, steel and plastic. Flying robot frames require electric engines, batteries, steel and circuits.',
 'Research the rocket silo technology after you have automated the required red, green, blue, purple and yellow science. Military science is optional for the launch goal.',
 'Scale only the lines that genuinely bottleneck. Check P for long-term consumption, use reserve chests where useful, and upgrade to steel/electric furnaces or faster belts where needed.'
], 'rocket', ['Start small: a steady trickle of purple and yellow science is enough to make progress.','Avoid starving all other factories by letting rocket-component assemblers consume unlimited materials.'],['My late-game science packs are made without handcrafting.'],[],['science','rocket'])
add('nuclear','Optional deep system: nuclear and solar','ADVANCED','Decide how to make reliable large-scale electricity.',[
 'Solar panels produce daytime power; accumulators store excess electricity for night. The standard Nauvis planning rule is about 21 accumulators per 25 solar panels.',
 'For nuclear, mine uranium ore (requires sulfuric acid), centrifuge uranium, create uranium fuel cells and feed a reactor. Pipe reactor heat through heat pipes to heat exchangers.',
 'Supply exchangers with water and transport their high-temperature steam to steam turbines; cool/use spent fuel cell handling if desired.',
 'A lone reactor produces 40 MW of heat; adjacent reactors share a neighbor bonus, making layouts more efficient but harder to design.',
 'Nuclear fuel cells burn for a fixed cycle; a simple insertion-control circuit can reduce waste. Kovarex enrichment helps later fuel supply but is not needed for the first reactor.',
 'Neither nuclear nor solar is required to launch the base-game rocket. Reliable coal steam power is enough if scaled appropriately.'
], 'power', ['Build nuclear for learning and compact steady power, not because rocket victory strictly requires it.','A heat exchanger and steam turbine are not interchangeable with the normal coal boiler/steam-engine pair.'],['I know the direction of heat and water through nuclear power.'],[],['power','nuclear'])
add('modules','Modules, beacons and ratios','ADVANCED','Understand production improvements without prematurely optimizing.',[
 'Speed modules increase machine speed but typically raise electricity use. Efficiency modules lower electricity demand and may reduce pollution indirectly.',
 'Productivity modules create extra products per set amount of input but slow the machine and raise consumption; only allowed in compatible recipes/machines.',
 'Beacons transmit module effects to nearby machines. Machine UI shows crafting speed and productivity effects; do not use pre-2.0 or Space Age-specific beacon ratios blindly.',
 'For throughput, measure products per second = recipe output quantity × crafting speed × (1 + productivity bonus) / recipe time. Check the in-game numbers for your specific setup.',
 'Prioritize productivity on expensive intermediates and science once you understand supply chains. Use speed elsewhere to counter bottlenecks. No modules are necessary for learning the first rocket.'
], 'assemble', ['A ratio is a prediction, not a law: changing modules, machine tiers or technologies changes it.'],['I can explain the trade-off among speed, efficiency and productivity.'],[],['machines','modules'])
add('rocket','Win the base game: launch a satellite','FINISH','Complete the actual base-game win condition for 2.1.24.',[
 'Research Rocket silo. Produce substantial concrete, electric engine units, processing units and the other silo ingredients in automated production lines.',
 'Build the rocket silo inside your electric network and feed it the ingredients shown in its recipe interface. It builds the required rocket parts over time.',
 'Construct a satellite (requires advanced components including solar panels, accumulators, radars, rocket fuel and advanced circuits).',
 'Place a cargo landing pad somewhere on the planet. Insert the satellite into the rocket silo payload. In the 2.1 base game, the rocket requires a satellite to launch.',
 'Launch the rocket and watch the victory event. The launch returns 1,000 space science packs to the cargo landing pad for infinite research.',
 'If the rocket will not launch, confirm that the silo is powered, rocket assembly is complete, the satellite is loaded and a cargo landing pad exists.',
 'You can continue playing after winning: improve production, add more trains, try construction robots or build an exceptionally reliable factory.'
], 'rocket', ['Do not follow a Space Age guide that says your first base-game rocket leaves Nauvis with your character.','Satellite plus cargo landing pad are essential to the 2.1 base-game launch path.'],['I launched a satellite in a rocket.','I understand where base-game space science comes from.'],[],['rocket','science'])
add('qol','Current version 2.1.24: important conveniences','REFERENCE','Use current game features without confusing base game with expansion features.',[
 '2.1.24: selecting a fluid entity again visualizes its pipeline; the relevant interface option is enabled by default. The pipe GUI also explains pipeline content and flow.',
 '2.1.24: holding a wire limits selection to entities that accept that wire. Interface settings now include a separate Quickbar section.',
 '2.1.21: pressing a hotkey for an empty quickbar slot can pipette the object under your cursor into that slot. Some combinators gained more comparison options.',
 '2.1 broadly: flippable burner miners, pumpjacks and supported inserters; better drops onto splitters; fluid mixing warnings; better fluid-wagon pump connections.',
 '2.1 broadly: pin Factoriopedia while working, hide unresearchable/unresearched entries, show interface tooltips, show pipe/tank flow information, and configure circuit input/output separately.',
 '2.1 broadly: revised biter expansion, improved shotgun balance, Spidertron patrol support and easier rolling-stock upgrades.',
 '2.1 Linux: SDL3, automatic video driver choice (prefers Wayland if fifo-v1 is available, otherwise X11), IME and on-screen keyboard support, and Wayland blueprint drag-and-drop.',
 'Not in your base-only game: Space Age planets and space platforms, Quality module progression, elevated rail buildings, foundries, recyclers and interplanetary logistics.'
], 'goal', ['Some newer tools are optional or only useful late in the game. Do not learn them until you need them.'],['I can find new 2.1.24 fluid visualization and Quickbar settings.'],[],['version','controls'])
add('linux','Arch Linux + Wayland practical checklist','REFERENCE','Reduce friction from desktop keyboard shortcuts and keep saves safe.',[
 'Factorio 2.1 uses SDL3. On Linux the “auto” video driver prefers native Wayland when the compositor advertises fifo-v1; otherwise it prefers X11 (which may run through XWayland). Do not assume native Wayland without checking the running environment.',
 'If Alt or Alt+mouse shortcuts are intercepted by your desktop environment, adjust the compositor window-move shortcuts or rebind Factorio controls under Settings → Controls. Do not change many hotkeys at once.',
 'Search your user data directory, commonly ~/.factorio/ for native Linux installations. Some Steam setups store cloud-related data under ~/.steam/steam/userdata/<id>/427520/remote/, and Flatpak paths differ.',
 'Before changing mods, settings or release branches, make a backup of your saves, blueprints and config files. In-game save files generally live in the user data directory under saves/.',
 'Check the game main menu version string, not just the Steam beta setting, to confirm 2.1.24. At the time this manual was researched, 2.1.24 was experimental and 2.1.23 was the confirmed stable branch.',
 'If UI scaling is uncomfortable, adjust interface size within the game; the debug scaling shortcuts are Ctrl+Numpad +/− or Ctrl+Numpad 0. Choose a display/UI scale that makes recipe icons readable.',
 'The updated native non-Steam Linux requirement is GLIBC 2.36 or newer. Arch normally meets it if system packages are reasonably current; do not make blind system changes to fix an unrelated game problem.'
], 'input', ['Keep a clearly named before-update save; save files and blueprints from 2.1 cannot be downgraded safely to 2.0.'],['I know where to inspect the version and back up save files.'],[],['linux','version'])
add('debug','What is wrong? A universal troubleshooting method','REFERENCE','Debug any stopped factory in a predictable order.',[
 'Step 1: Look at the stopped machine and hover/open it. Read its exact status, recipe, input inventory, output inventory and power icon.',
 'Step 2: Follow the item/fluid stream backward. Is the ingredient produced, delivered, accessible to an inserter and on the lane the inserter can reach?',
 'Step 3: Inspect energy and fuel. Are poles connected to a generator? Does the power network have enough electricity? Is an engine/boiler out of water, steam or coal?',
 'Step 4: Check orientation and room. Are inserter arrows backwards? Are pipe connections mismatched? Are output slots, fluid tanks, chests or belts completely full?',
 'Step 5: For trains, check path continuity, signal travel side, signal colors/blocks, stop placement, automatic mode, fuel and train limits.',
 'Step 6: For robots, check green/orange areas, item chests, robot availability, network power and charging. For circuits, check signal counts, wire color, condition and input/output configuration.',
 'Step 7: After changing one thing, observe again before changing more. Record the cause and the one fix that worked.'
], 'debug', ['A saturated belt is often evidence that the downstream consumer is too slow, not that the belt is defective.','Try the in-game Factoriopedia Alt+click, machine status tooltip and P production screen before searching the internet.'],['I can check power → ingredients → outputs → transport in a repeatable order.'],[],['troubleshoot','statistics'])

sources={
'version':('Official complete 2.1 version history incl. 2.1.24','https://wiki.factorio.com/Version_history/2.1.0'),
'controls':('Official current keyboard/mouse controls','https://wiki.factorio.com/Controls'),
'hotkeys':('Keyboard shortcuts tutorial','https://wiki.factorio.com/Tutorial:Keyboard_shortcuts'),
'quick':('Beginner quick start (some ratios are outdated)','https://wiki.factorio.com/Tutorial:Quick_start_guide'),
'machines':('Assembling machine','https://wiki.factorio.com/Assembling_machine'),
'belts':('Belt transport system','https://wiki.factorio.com/Belt_transport_system'),
'power':('Power production (current ratios)','https://wiki.factorio.com/Power_production'),
'fluid':('Fluid system (modern mechanics)','https://wiki.factorio.com/Fluid_system'),
'science':('Science packs and research','https://wiki.factorio.com/Science_pack'),
'research':('Research','https://wiki.factorio.com/Research'),
'combat':('Enemies and pollution','https://wiki.factorio.com/Enemies'),
'statistics':('Production statistics','https://wiki.factorio.com/Production_statistics'),
'rail':('Train signals tutorial','https://wiki.factorio.com/Tutorial:Train_signals'),
 'trains':('Train stops, train limits and priority','https://wiki.factorio.com/Train_stop'),
'oil':('Oil processing and cracking','https://wiki.factorio.com/Oil_processing'),
'bots':('Roboport coverage','https://wiki.factorio.com/Roboport'),
'logistics':('Logistic network and chests','https://wiki.factorio.com/Logistic_network'),
'blueprints':('Blueprint','https://wiki.factorio.com/Blueprint'),
'circuit':('Circuit networks','https://wiki.factorio.com/Circuit_network'),
'modules':('Modules','https://wiki.factorio.com/Module'),
'nuclear':('Nuclear tutorial','https://wiki.factorio.com/Tutorial:Nuclear_power'),
'rocket':('Rocket silo in base game','https://wiki.factorio.com/Rocket_silo'),
'linux':('Linux file locations','https://wiki.factorio.com/Application_directory'),
'goal':('Official 2.1 stable overview','https://factorio.com/blog/post/fff-449'),
 'troubleshoot':('Alerts and icons','https://wiki.factorio.com/Alerts'),
}

# An independently searchable PC keyboard/mouse command reference.
controls=[]
def ctl(cat,key,action,detail,scope='Base',note=''):
    controls.append(dict(category=cat,key=key,action=action,detail=detail,scope=scope,note=note))
for k,move in [('W','Move up'),('A','Move left'),('S','Move down'),('D','Move right')]:ctl('Movement',k,move,'Move engineer on the surface.')
for row in [
 ('E','Open inventory/character GUI','Also confirms/closes some game panels.'),
 ('Left mouse','Build / open GUI','Place held entity, or open selected entity interface.'),('Right mouse','Mine / use item','Hold over entities/resources to mine; contextual item use.'),
 ('Q','Pipette / clear cursor','Hover placed object to select matching build item; otherwise clear cursor.'),
 ('R','Rotate clockwise','Rotate held entity or currently selected entity.'),('Shift+R','Rotate anticlockwise','Reverse rotate.'),('H','Flip horizontally','Works only for flippable objects/blueprints.'),('V','Flip vertically','Works only for flippable objects/blueprints.'),
 ('Alt','Toggle Alt-mode','Show recipes, item icons, inserter arrows.'),('F','Pick up nearby items','Pick loose items up off belts or the ground.'),('Z','Drop one item','Drop one held item into world, belt or machine.'),
 ('Shift+Left mouse','Build ghost','Requires holding a buildable item; contextual other action in GUI.'),('Ctrl+Shift+Left mouse','Super-force build','Prepare terrain and mark obstructions for robot deconstruction.'),
 ('Space','Shoot enemy','Shoot near cursor with equipped weapon.'),('Shift+Space','Shoot selected target','Shoot precise selection/contextual targeted shot.'),('C','Cycle weapons','Next equipped weapon.'),('Enter','Enter/exit vehicle','Stand near a car/tank/train.'),
 ('Mouse wheel','Zoom world in/out','Scroll to zoom; mouse position handling configurable.'),('Shift+Alt+Mouse wheel','Zoom minimap','Pointer must be over minimap.'),
 ('Shift+Right mouse','Copy machine settings','Copy source recipe/filter/schedule/circuit configuration.'),('Shift+Left mouse','Paste machine settings','Apply copied settings to compatible target.'),
 ('Grave / backtick','Toggle chat/console','Avoid commands that disable achievements.'),
 ('Alt+Left mouse','Open Factoriopedia','Hover an object then use this shortcut.'),
 ('Alt+Right mouse','Pin entity or location','Contextual entity/location pin.'),
 ('Ctrl+Alt+Left mouse','Ping map location','Share a location in chat.'),
]:ctl('World',*row)
for row in [
 ('Left click recipe','Craft 1','In character crafting screen.'),('Right click recipe','Craft 5','In crafting screen.'),('Shift+Left click recipe','Craft maximum','In crafting screen.'),
 ('Left click crafting queue','Cancel 1','In crafting queue.'),('Right click crafting queue','Cancel 5','In crafting queue.'),('Shift+Left click crafting queue','Cancel all','In crafting queue.'),
 ('Left mouse on inventory','Pick up/drop full stack','Within inventory.'),('Right mouse on inventory','Half-stack / place one','Right-click takes half or places one held item.'),
 ('Shift+Left mouse','Move one stack','Transfer between inventories.'),('Ctrl+Left mouse','Move all matching stacks','Inventory bulk transfer; in world fast transfer into/out of machines.'),
 ('Shift+Right mouse','Transfer half stack','Inventory context.'),('Ctrl+Right mouse','Transfer half of item type','Inventory context; world transfers half via entity.'),
 ('Middle mouse','Filter slot','Filters inventory/quickbar or clears quickbar slot.'),('Shift+Right mouse on slot','Copy inventory filter','Use with Shift+Left mouse paste filter.'),('Shift+Left mouse on slot','Paste inventory filter','Compatible inventory slots.'),
]:ctl('Inventory / craft',*row)
for row in [('1–0','Select quickbar slot','Slots 1–10 on active quickbar.'),('Shift+1–0','Activate quickbar N','Select quickbar numbered 1 through 10.'),('X','Rotate active quickbars','Switch which shortcut bars display.'),('Empty quickbar slot key','Quick pipette (2.1.21)','If enabled, key for empty slot can pipette hovered object into that slot.')]:ctl('Quickbar',*row)
for row in [
 ('Ctrl+C','Copy area','Drag rectangle for temporary blueprint.'),('Ctrl+X','Cut area','Copy and mark entities for removal.'),('Ctrl+V','Paste clipboard','Ghost-paste copied entities.'),('Ctrl+Z','Undo','Undo certain placements/deconstruction.'),('Ctrl+Y / Ctrl+Shift+Z','Redo','Redo an undo.'),('Shift+Mouse wheel','Cycle clipboard history','While paste tool is held.'),('Alt+B','Make blueprint','Open permanent blueprint creation tool.'),('Alt+D','Make deconstruction planner','Mark entities for robot removal.'),('Alt+U','Make upgrade planner','Mark entities for robot upgrading.'),('Alt+C','Copper wire tool','Electric-pole wire connecting/disconnecting.'),('Alt+R','Red wire tool','Circuit wire connection mode.'),('Alt+G','Green wire tool','Circuit wire connection mode.'),('Alt+A','Spidertron remote','Only after researching/building Spidertron.'),('Alt+T','Artillery targeting remote','Late-game artillery targeting.'),('Alt+E','Toggle exoskeleton','Equipment dependent.'),('Alt+L','Toggle personal logistics','Equipment / research dependent.'),('Alt+F','Toggle personal roboport','Equipment dependent.'),('Alt+Y','Discharge defense remote','Equipment dependent.')
]:ctl('Plans / tools',*row)
for row in [('T','Technology / research','Open research tree.'),('P','Production statistics','Open production and consumption graphs.'),('L','Logistic networks','View robot network details.'),('B','Blueprint library','Saved blueprint and book UI.'),('O','Train overview','Train list and status.'),('Tab / M','Map','Open map.'),('Esc','Menu / cancel','Open pause menu or back out of interface.'),('F1','Character logistics','Character logistics panel.'),('F2','Character info','Character info panel.'),('F3','Character crafting','Character crafting panel.'),('Alt+Left / Alt+Right','UI navigation back/forward','Go to previous or next previously opened UI window.'),('Ctrl+F','Focus GUI search','Contextual search boxes.'),('Pause','Pause simulation','Dedicated Pause key.')]:ctl('Panels',*row)
for row in [('G','Toggle rail layer','Applies when rail planner used; elevated rails depend on DLC.'),('Ctrl+Left mouse with rail','Avoid obstacles','Contextual rail-building ghost/obstacle avoidance.'),('Ctrl+Left mouse on map','Temporary train stop','From locomotive GUI or map, adds a temporary stop.'),('Shift+Left mouse on train map','Schedule train stop','Add selected stop to locomotive schedule.'),('J','Connect trains','Couple selected rolling stock.'),('K','Disconnect trains','Uncouple selected rolling stock.'),('Numpad + / −','Change tile brush size','While laying terrain tiles.'),('Shift+Left mouse on pole','Remove pole cables','Contextual cable removal.'),('Ctrl+Arrow','Adjust blueprint absolute grid','Only in blueprint placement contexts.'),('Shift+Arrow','Shift blueprint entities','Only in blueprint placement contexts.'),('Alt+Mouse wheel','Change quality selection','Requires Quality mod: NOT base-game feature.'),('Ctrl+Numpad + / −','Change UI scale','Debug shortcut; scaling is also available in settings.'),('Ctrl+Numpad 0','Automatic UI scale','Debug shortcut.'),('F4','Debug settings','Advanced diagnostics.'),('F5','Debug display','Advanced diagnostics.'),('F9','Reset zoom','Debug shortcut.'),('Ctrl+Shift+E','Prototype viewer','Advanced/debug.'),('Ctrl+Shift+F','Prototype explorer','Advanced/debug.')]:ctl('Advanced',*row)


# Additional official default bindings are separated from everyday controls to avoid overwhelming first-time players.
for row in [
 ('Shift+Right mouse','Queue command','When commanding a remote-controlled unit, append rather than replace an order.'),
 ('Ctrl+Left mouse','Rename all','Some rename dialogs can rename all identically named stops.'),
 ('Shift+Left mouse','Place chat tag','With chat open, insert a link to the hovered item/location.'),
 ('Shift','Force tooltip','Immediately show a tooltip if tooltip delay is long or Never.'),
 ('Shift+Mouse wheel','Scroll tooltip','When the contextual detailed tooltip supports scrolling.'),
 ('Backspace / Mouse button 4','Previous mod','Only in the mod-selection dialog.'),
 ('F10','Next replay player','Only when watching a replay.'),
]: ctl('Contextual',*row)
for row in [
 ('Middle mouse','Next editor variation','Editor mode only; not normal Freeplay.'),
 ('Shift+Middle mouse','Previous editor variation / clone','Editor mode; the same combination is context-dependent.'),
 ('Ctrl+Middle mouse','Delete editor item','Editor mode only.'),
 ('Numpad 0','Pause selected editor entity','Editor mode only.'),
 ('Numpad .','Advance one simulation tick','Editor mode only.'),
 ('Shift+Numpad +','Increase simulation speed','Editor mode only.'),
 ('Shift+Numpad −','Decrease simulation speed','Editor mode only.'),
 ('Shift+Numpad *','Reset simulation speed','Editor mode only.'),
 ('Ctrl+number','Select editor surface','Editor mode, if available.'),
 ('Ctrl+Shift+F11','Enter editor','Advanced/editor command, not needed for winning.'),
 ('Ctrl+F3','Toggle sprite atlas display','Debug only.'),
 ('Ctrl+Shift+F4','Toggle GUI visibility','Debug only.'),
 ('Ctrl+F5','Toggle GUI debug','Debug only.'),
 ('Ctrl+F6','Toggle GUI style inspection','Debug only.'),
 ('Ctrl+F7','Toggle GUI shadows','Debug only.'),
 ('Ctrl+F8','Toggle GUI glows','Debug only.'),
 ('Shift+F9','Set zoom to 2×','Debug only.'),
]: ctl('Editor / debug',*row)

troubles=[
('No power icon','Check pole blue coverage, connected wires, generator, steam/fuel and network satisfaction.'),
('Low power','Open a pole: supply is below consumption. Add generation or reduce loads.'),
('Steam engines idle','If electricity demand is low, engines may deliberately produce almost nothing.'),
('Boiler does not run','Check coal fuel, water connection, steam output orientation and demand.'),
('Miner stopped','Check resource under mining area, electricity/fuel, output belt and potential depletion.'),
('Assembler stuck','Check chosen recipe, unlocked recipe tier, ingredients, power, output space and fluid ports.'),
('Inserter frozen','Check power, pickup/drop positions, filters, disabled condition, input and destination full.'),
('Items on wrong belt lane','Inspect drill/inserter drop arrow in Alt-mode and where belt turns/side-loads.'),
('One lane starves','Side-load/merge lanes deliberately or feed each lane independently.'),
('Oil refinery blocked','An advanced recipe stops when ANY output is full. Add tanks and cracking.'),
('Fluid pipe overextended','Find the >320×320 segment; add a powered pump to split the network.'),
('Fluid mixing warning','Separate conflicting fluid systems; check rotated chemical machines and wrong pipe joins.'),
('Pump inactive','Check electric power, direction, input fluid, output capacity and circuit condition.'),
('Train “No path”','Check connected rails, direction of signals on train’s right, stop orientation and bridges if enabled.'),
('Train “Destination full”','Train limit is zero/used up, all same-name stations unavailable or disabled.'),
('Deadlocked intersection','Check crossing blocks, normal signals inside junctions, chain signals before and sufficient waiting lengths.'),
('Train misses loading','Check stop side, wagon/inserter alignment, wagon filters, cargo capacity and power.'),
('Cargo wagon fluid loading fails','Use FLUID wagon plus powered pumps with actual valid connectors, not inserters.'),
('Bot ghost not built','Check ghost in green zone, providers holding exact item, construction bots available and power.'),
('Logistics bot ignores requester','Check orange shared network, logistic bots, available source and unlock of requester chest.'),
('Bots charge slowly','Spread charging load across more powered roboports.'),
('Circuit does opposite action','Verify comparator, selected red/green input, condition, output and negative counts.'),
('Research stuck','Check tech chosen, ALL science pack colors available, lab power and lab input.'),
('Rocket unable to launch','For base 2.1: finish rocket parts, provide satellite and build cargo landing pad.'),
('Enemies suddenly attack','View pollution overlay, strengthen ammo/turrets, clear threatening nests or reduce pollution.'),
('A key does nothing on Wayland','Check compositor shortcuts/keyboard layout; test binding in Factorio Settings → Controls.'),
('Shortcut missing','Look at controls category; some hotkeys unbound by default or only work with an equipped tool.'),
]
glossary=[
('Belt','Two-lane solid-item transport line.'),('Inserter','Swinging arm that moves solid items between machines, belts and chests.'),('Lane','One half of a belt’s item flow.'),('Throughput','Number of items or fluid units delivered per second.'),('Bottleneck','The stage that limits the total output of a production chain.'),('Recipe','The input items and time required to produce an output in a machine.'),('Handcrafting','The engineer personally crafting in the character panel; not always possible.'),('Fuel','Consumable energy source (often coal, solid fuel, rocket fuel or uranium cells).'),('Power network','Electricity wiring between generators, poles and consumers.'),('Pollution','Factory emissions which spread and can trigger biter attacks.'),('Science pack','Consumed by powered labs to progress technology research.'),('Ghost','A planned, not yet physically placed object.'),('Blueprint','Saved arrangement of structures/settings that can be placed as ghosts.'),('Block','Section of connected railway controlled by signals.'),('Rail signal','Allows train entry if the protected block is available.'),('Chain signal','Allows entry only if the train can follow its planned path onward.'),('Station train limit','Number of trains allowed to reserve the station as their destination.'),('Fluid segment','Connected pipes/tanks sharing fluid and fluid-level behavior.'),('Cracking','Conversion of a heavier oil product into a lighter one.'),('Orange zone','Roboport logistic-service coverage.'),('Green zone','Roboport construction coverage.'),('Circuit signal','Named quantity carried on red/green circuit wires.'),('Combinator','Circuit-network building for constant, arithmetic, decision or selection logic.'),('Mall','Factory section that supplies the player with construction materials.'),('Alt-mode','Visibility overlay for recipes, arrow directions and item contents.'),('Factoriopedia','Built-in searchable reference of entities/recipes/technologies.'),('FPS / UPS','Frames per second and game simulation updates per second.'),('Nauvis','Starting planet in Factorio; the entire base-game campaign stays there.'),('Space science','Base game: 1,000 packs produced by launching a rocket with satellite.'),('Cargo landing pad','Base game rocket science is delivered here; one must exist for launch.'),('Quickbar','Reference slots for selecting items/tools; not extra inventory.')]

qol=[('2.1.24','Base','Selected fluid entities show pipeline visualization again; enabled by default.'),('2.1.24','Base','Only wire-compatible entities selectable while holding wire.'),('2.1.24','Base','Quickbar settings get their own interface section.'),('2.1.21','Base','Empty quickbar hotkey can pipette hovered item into that slot.'),('2.1.21','Base','Selector combinator index selection; read empty slots for containers; silo launched signal.'),('2.1.13','Base','Zoom-to-cursor setting where supported; new alert for detected enemy expansion.'),('2.1.9','Base','Decider combinator else output.'),('2.1.7','Base','Flippable burner drills, pumpjacks, compatible inserters.'),('2.1.7','Base','Circuit input/output red/green wire selection separately.'),('2.1.7','Base','Pipes, boilers, labs, land mines, heat pipes gain circuit options.'),('2.1.7','Base','Fluid mixing warnings and expanded pipe GUI/overlay.'),('2.1.7','Base','Fluid pumps connect to curved, non-aligned and end-of-wagon positions.'),('2.1.7','Base','Factoriopedia pinning and hiding unresearched content.'),('2.1.7','Base','Spidertron patrol and easier rolling-stock upgrades.'),('2.1.7','Base','Shotgun behavior/damage rebalance and changed enemy expansion.'),('2.1.7','Base','New assembler, refinery and rocket silo appearance.'),('2.1.7','Linux','SDL3, Wayland auto fallback behavior, IME, virtual keyboard and blueprint drag/drop.'),('2.1','Space Age only','Mixed rockets and platform logistics; ignore in base game.'),('2.1','Space Age only','Quality locomotives/wagons, landing-pad unloading bay and orbital transfers.'),('2.1','Space Age only','New planetary visuals/asteroid balancing; do not learn for base victory.')]

payload=dict(meta=dict(title='Factorio 2.1.24 — Base-game field manual',version='2.1.24',date='2026-10-27',content='Base game, no Space Age / Quality / Elevated Rails',notes='Verified against official wiki 2026-10-27; learn in-game by doing; no automatic integration with game save.'),chapters=chapters,controls=controls,troubleshooting=troubles,glossary=glossary,qol=qol,sources=sources)
if len({c['id'] for c in chapters}) != len(chapters):
 raise ValueError('Chapter IDs must be unique.')
for chapter in chapters:
 for source in chapter['sources']:
  if source not in sources:
   raise ValueError(f"Unknown source {source!r} in chapter {chapter['id']!r}")
(P/'manual_data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
with (P/'controls.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=['category','key','action','detail','scope','note']);w.writeheader();w.writerows(controls)
print('content:',len(chapters),'lessons,',sum(len(c['steps']) for c in chapters),'steps,',len(controls),'control entries,',len(troubles),'symptoms,',len(glossary),'terms')
# This is a standalone offline site: all diagrams are original inline SVG; no CDN or external fonts.
TEMPLATE=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><title>Factorio 2.1.24 | Base Game Field Manual</title>
<style>
:root{--bg:#10161e;--pane:#17212c;--pane2:#1b2937;--line:#34475a;--txt:#e8eef4;--muted:#afbfcc;--gold:#f2c979;--mint:#75d5bd;--blue:#83bce9;--danger:#ff9b96;--chip:#263647;--radius:14px}*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--txt);line-height:1.65}button,input,select{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--gold);outline-offset:2px}a{color:var(--blue)}.layout{display:grid;grid-template-columns:270px minmax(0,1fr);min-height:100vh}.side{background:#121d28;border-right:1px solid var(--line);padding:20px 13px;height:100vh;overflow:auto;position:sticky;top:0}.brand{font-weight:850;font-size:20px;line-height:1.3;letter-spacing:-.4px;padding:6px 8px 15px}.brand span{display:block;color:var(--gold);font-size:12px;text-transform:uppercase;letter-spacing:.15em;font-weight:650;margin-bottom:6px}.side small{color:var(--muted)}.side-button{display:block;width:100%;text-align:left;margin:3px 0;padding:9px 11px;background:transparent;color:var(--txt);border:1px solid transparent;border-radius:9px}.side-button:hover,.side-button[aria-current=true]{background:var(--pane2);border-color:var(--line)}.side-button[aria-current=true]{color:var(--gold)}.side-button span{display:inline-block;min-width:21px;color:var(--muted)}.side-label{margin:19px 8px 6px;font-size:11px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;font-weight:700}.main{width:min(1120px,100%);padding:26px clamp(16px,4vw,54px) 80px;margin:0 auto}.top{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;border-bottom:1px solid var(--line);padding-bottom:17px}.tag{color:var(--gold);background:#342d26;display:inline-block;padding:3px 9px;border-radius:99px;font-size:12px;border:1px solid #665036}.btn{background:var(--chip);color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:9px 13px}.btn:hover{border-color:var(--gold)}.btn.primary{background:var(--gold);color:#1b1b15;font-weight:800}.btn:disabled{opacity:.4;cursor:not-allowed}.navflex{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.pagehead{margin:32px 0 20px}.eyebrow{color:var(--mint);text-transform:uppercase;font-size:12px;letter-spacing:.12em;font-weight:800}.pagehead h1{font-size:clamp(27px,4vw,42px);line-height:1.17;margin:9px 0;letter-spacing:-.03em}.lead{font-size:17px;color:var(--muted);max-width:800px}.progress{height:10px;background:#293a48;border-radius:99px;overflow:hidden;margin:16px 0 5px}.progress>div{height:100%;background:linear-gradient(90deg,#80bdaf,#f3ca7a);transition:width .2s}.tiny{font-size:12px;color:var(--muted)}.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(270px,.72fr);gap:16px;align-items:start}.panel{border:1px solid var(--line);border-radius:var(--radius);background:var(--pane);padding:18px;margin:12px 0}.panel h2{font-size:20px;margin:0 0 12px;letter-spacing:-.02em}.panel h3{font-size:16px;margin:14px 0 8px;color:var(--gold)}.panel p{margin:9px 0}.panel ul{margin:7px 0;padding-left:22px}.panel li{margin-bottom:9px}.step{display:grid;grid-template-columns:28px minmax(0,1fr);gap:12px;align-items:start;padding:13px 4px;border-bottom:1px solid #304355}.step:last-child{border:0}.step input{width:21px;height:21px;accent-color:var(--mint);margin-top:4px}.step.done .step-text{text-decoration:line-through;color:#94adba}.step-text{font-size:15px;overflow-wrap:anywhere}.number{color:var(--gold);font-size:12px;font-weight:800;margin-right:8px}.visual{min-height:220px;display:grid;place-items:center;background:#101b27;border:1px solid #324c61;border-radius:12px;padding:10px;overflow:auto}.visual svg{max-width:100%;height:auto}.caption{font-size:13px;color:var(--muted);margin-top:9px}.pill{display:inline-block;border:1px solid var(--line);border-radius:20px;padding:2px 9px;font-size:12px;margin:4px;color:var(--muted)}.callout{border-left:3px solid var(--mint);padding:10px 13px;background:#17312f;border-radius:4px}.warn{border-left-color:var(--gold);background:#2d281d}.check{display:flex;gap:9px;align-items:center;margin:8px 0}.check input{width:18px;height:18px;accent-color:var(--mint)}.stat-row{display:flex;flex-wrap:wrap;gap:12px}.stat{background:var(--pane);padding:14px;border:1px solid var(--line);border-radius:10px;min-width:150px;flex:1}.stat b{display:block;font-size:26px;color:var(--gold)}.stat small{color:var(--muted)}.actions{margin-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}.search{width:100%;background:#0e1720;border:1px solid var(--line);border-radius:8px;color:var(--txt);padding:12px 14px;margin:12px 0}.result{overflow-wrap:anywhere;padding:13px;border-bottom:1px solid var(--line)}.result:last-child{border:0}.result strong{color:var(--gold)}.kbd{font:600 12px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace;background:#314254;border:1px solid #66798d;border-radius:5px;padding:4px 6px;color:#fff;white-space:nowrap;display:inline-block}.rowlabel{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.filter{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 16px}.filter button{border:1px solid var(--line);background:var(--chip);color:var(--txt);border-radius:99px;padding:7px 12px;font-size:13px}.filter button.active{background:var(--gold);color:#242015}.tablewrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{font-size:12px;text-transform:uppercase;color:var(--muted);letter-spacing:.08em}tr:hover td{background:#1c2b39}.expand{border-bottom:1px solid var(--line);padding:10px 2px}summary{cursor:pointer;font-weight:700;color:var(--gold)}.refs{font-size:13px}.refs a{display:block;padding:6px 0;overflow-wrap:anywhere}.railbuttons{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.diagram-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.diagram-tabs button{background:#263949;border:1px solid #476175;border-radius:6px;color:var(--txt);padding:6px 10px}.diagram-tabs button.active{background:#365949}.subtle{color:var(--muted)}.mobile-nav{display:none}.topinfo{display:none}footer{color:var(--muted);font-size:12px;margin-top:35px;border-top:1px solid var(--line);padding-top:18px}@media(max-width:820px){.layout{display:block}.side{height:auto;max-height:40vh;overflow:auto;position:static;border-right:0;border-bottom:1px solid var(--line)}.main{padding:18px 15px 60px}.cols{grid-template-columns:minmax(0,1fr)}.mobile-nav{display:block}.topinfo{display:block}}@media print{body{background:#fff;color:#000}.side,.top button,.actions,.filter,.search,.diagram-tabs{display:none!important}.layout{display:block}.main{width:100%;padding:8px}.panel{background:#fff;color:#000;border:1px solid #777;break-inside:avoid}.step-text{color:#000}.lead,.tiny,.caption{color:#444}.visual{background:#fafafa}.pagehead h1{font-size:28px}}
</style></head><body><div class="layout"><aside class="side"><div class="brand"><span>October 27, 2026 · 2.1.24</span>FACTORIO FIELD MANUAL</div><div style="padding:0 8px"><small>Base game · No Space Age · Works offline</small><div class="progress"><div id="sidebarprogress" style="width:0"></div></div><small id="sidebarpct">0% of lesson steps checked</small></div><div class="side-label">Reference</div><div id="coreNav"></div><div class="side-label">Walkthrough · in order</div><div id="lessonNav"></div></aside>
<main class="main"><div class="top"><div><span class="tag">2.1.24 · BASE GAME</span> <span class="tiny" style="margin-left:8px">Offline interactive handbook</span></div><div class="navflex"><button class="btn mobile-nav" id="lessonsBtn">Lessons</button><button class="btn" id="exportBtn">Export progress</button><button class="btn" id="importBtn">Import progress</button><input id="importFile" type="file" accept="application/json" hidden></div></div><p id="storageNotice" class="callout warn" role="status" hidden></p><div id="content"></div><footer>Version target: Factorio 2.1.24 (released 2026-10-27, experimental when checked). This is a standalone teaching reference, not a live connection to your save. Official links in the Sources screen require internet; all lessons, diagrams, search and progress features work offline. © Original explanatory text and diagrams; game names and mechanics belong to their respective owners.</footer></main></div>
<script id="manualdata" type="application/json">__DATA__</script><script>
'use strict';const DATA=JSON.parse(document.getElementById('manualdata').textContent);const $=id=>document.getElementById(id);let route='home',filter='All',searchTerm='';const phaseNames={BEGIN:'01 · Getting started',EARLY:'02 · Early factory',MID:'03 · Middle game',LATE:'04 · Late game',ADVANCED:'05 · Deep systems',FINISH:'06 · Win',REFERENCE:'07 · Further reference'};
const escapeHTML=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const progressKeys=new Set(DATA.chapters.flatMap(ch=>[...ch.steps.map((_,i)=>ch.id+':'+i),...ch.checks.map((_,i)=>ch.id+':quiz'+i)]));
function validateProgress(value){
 if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('Progress must be an object.');
 const clean={};
 for(const [key,checked] of Object.entries(value)){
  if(!progressKeys.has(key)||typeof checked!=='boolean')throw new Error('Progress contains an unknown step or an invalid checkbox value.');
  clean[key]=checked;
 }
 return clean;
}
function storageNotice(message){$('storageNotice').textContent=message;$('storageNotice').hidden=!message}
let progress={};try{progress=validateProgress(JSON.parse(localStorage.getItem('factorio_2_1_24_progress')||'{}'))}catch(_){storageNotice('Saved progress could not be loaded. Use Import progress to restore a backup, and Export progress to keep your work.');}
function persist(){try{localStorage.setItem('factorio_2_1_24_progress',JSON.stringify(progress));storageNotice('')}catch(_){storageNotice('This browser cannot save progress locally. Use Export progress before closing the manual.')}};
const referenceRoutes=['home','controls','diagrams','help','glossary','whatsnew','sources'];
function readRoute(){try{const r=decodeURIComponent(location.hash.slice(1));return referenceRoutes.includes(r)||DATA.chapters.some(c=>c.id===r)?r:'home'}catch(_){return 'home'}}
function visited(ch){return ch.steps.filter((_,i)=>!!progress[ch.id+':'+i]).length}
function stats(){const total=DATA.chapters.reduce((n,c)=>n+c.steps.length,0),done=DATA.chapters.reduce((n,c)=>n+visited(c),0);return {total,done,pct:Math.round(100*done/total)}};
function nav(to){route=to;searchTerm='';render();window.scrollTo(0,0);location.hash=encodeURIComponent(to)}
function totalNav(){let html='';for(const [id,label] of [['home','Learning map'],['controls','All keyboard shortcuts'],['diagrams','Visual playground'],['help','Troubleshooting'],['glossary','Visual-language glossary'],['whatsnew','2.1.24 & QoL'],['sources','Verification sources']])html+=`<button class="side-button" aria-current="${route===id}" data-to="${id}">${label}</button>`;$('coreNav').innerHTML=html;html='';let last='';DATA.chapters.forEach((c,i)=>{if(last!==c.phase){last=c.phase;html+=`<div class="side-label">${escapeHTML(phaseNames[last]||last)}</div>`}html+=`<button class="side-button" aria-current="${route===c.id}" data-to="${c.id}"><span>${visited(c)===c.steps.length?'✓':(i+1)+'.'}</span> ${escapeHTML(c.title)}</button>`});$('lessonNav').innerHTML=html;const st=stats();$('sidebarprogress').style.width=st.pct+'%';$('sidebarpct').textContent=`${st.done}/${st.total} steps (${st.pct}%)`;document.querySelectorAll('[data-to]').forEach(b=>b.onclick=()=>nav(b.dataset.to))}
function heading(eyebrow,title,desc){return `<header class="pagehead"><div class="eyebrow">${escapeHTML(eyebrow)}</div><h1>${escapeHTML(title)}</h1><div class="lead">${escapeHTML(desc||'')}</div></header>`}
function box(x,y,w,h,t,color='#263949'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="11" fill="${color}" stroke="#7692a5" stroke-width="1.5"/><text x="${x+w/2}" y="${y+h/2+5}" text-anchor="middle" fill="#f1f6fa" font-family="system-ui" font-size="15" font-weight="650">${escapeHTML(t)}</text>`}
function arrow(x1,y1,x2,y2,color='#f2c979'){return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="4" marker-end="url(#arr)"/>`}
function caption(x,y,t){return `<text x="${x}" y="${y}" text-anchor="middle" fill="#b9cbd4" font-size="13" font-family="system-ui">${escapeHTML(t)}</text>`}
function graphic(kind){const a=[];let sub='Illustrative topology, not an exact placeable Factorio blueprint.';
 switch(kind){
case 'goal':a.push(box(22,90,120,70,'Ore'),arrow(144,125,190,125),box(193,90,120,70,'Machines'),arrow(315,125,365,125),box(368,90,120,70,'Science'),arrow(490,125,535,125),box(537,90,120,70,'Rocket','#3b5144'));a.push(caption(338,40,'A chain of tiny automatic systems'));break;
case 'input':a.push(box(40,45,200,130,'WASD: move'),box(375,45,200,130,'Mouse: interact'),box(207,220,200,58,'Q · R · Alt · E','#3c554b'),caption(340,345,'Learn these before memorizing anything else'));break;
case 'ore':a.push(box(35,96,150,70,'Burner drill','#564b31'),arrow(190,128,280,128),box(282,96,150,70,'Stone furnace','#744b35'),arrow(435,128,505,128),box(507,96,140,70,'Iron plate','#3c554b'),caption(323,48,'Coal fuels BOTH drill and furnace'));break;
case 'power':a.push(box(16,90,125,70,'Water pump'),arrow(144,125,195,125,'#83bce9'),box(198,90,130,70,'Boiler','#6b4938'),arrow(330,125,385,125),box(390,50,145,64,'Steam engine'),box(390,145,145,64,'Steam engine'),arrow(540,122,625,122,'#75d5bd'),caption(630,145,'To poles'),caption(325,270,'1 boiler → 2 engines → up to 1.8 MW'));break;
case 'belt':a.push(box(22,87,118,82,'Drill'),arrow(143,127,190,127),`<rect x="193" y="87" width="285" height="90" fill="#385066" stroke="#89a5b9"/><line x1="193" y1="132" x2="478" y2="132" stroke="#f2c979" stroke-width="3"/>`,caption(330,114,'Lane A → → →'),caption(330,162,'Lane B → → →'),arrow(477,130,523,130),box(526,87,125,82,'Inserter →'),caption(330,48,'Both lanes share the same belt direction'));break;
case 'assemble':a.push(box(25,80,150,65,'Input belt'),arrow(177,113,232,113),box(234,80,172,65,'Assembler','#395349'),arrow(409,113,465,113),box(468,80,174,65,'Output belt'),caption(337,221,'Recipe + ingredients + power + room for output'));break;
case 'science':a.push(box(17,38,167,63,'Red science','#634444'),box(17,172,167,63,'Green science','#426341'),arrow(188,70,330,125),arrow(188,204,330,150),box(332,90,156,80,'LAB','#3b5555'),arrow(494,130,542,130),box(545,91,120,77,'Research','#5c4f35'));break;
case 'defense':a.push(`<circle cx="342" cy="148" r="130" fill="#51482f" fill-opacity=".4" stroke="#d4a95d" stroke-dasharray="8 8"/>`,box(280,112,123,66,'Factory','#325548'),box(33,110,128,66,'Biters','#603535'),box(519,110,128,66,'Turrets','#375165'),caption(342,312,'Pollution can reach enemy nests beyond walls'));break;
case 'steel':a.push(box(32,76,150,70,'Iron ore'),arrow(184,111,233,111),box(236,76,170,70,'Furnace'),arrow(408,111,456,111),box(458,76,174,70,'Iron plate'),arrow(546,148,546,196),box(457,200,174,67,'Steel furnace','#5a5335'),caption(345,315,'Steel is another smelting step from iron plates'));break;
case 'train':a.push(box(10,42,168,68,'Mine stop'),box(512,42,168,68,'Base stop'),`<path d="M 170 112 L 170 260 Q170 288 200 288 H 491 Q 521 288 521 258 V112" stroke="#8aa3b4" stroke-width="9" fill="none"/><path d="M 200 122 H 490" stroke="#8aa3b4" stroke-width="9" fill="none"/>`,box(246,240,155,54,'Locomotive','#4b563e'),caption(344,190,'One-way loop with clear stops'));break;
case 'signals':a.push(`<path d="M 20 152 H 665 M 350 25 V285" stroke="#9bb3c1" stroke-width="9"/>`,box(65,70,145,53,'Chain BEFORE','#4e4932'),box(475,75,150,53,'Rail AFTER','#31594c'),`<circle cx="261" cy="152" r="12" fill="#eeae56"/><circle cx="423" cy="152" r="12" fill="#70d6b6"/>`,caption(346,318,'A waiting train must never obstruct the crossing'));break;
case 'fluid':a.push(box(20,85,140,65,'Oil source'),arrow(164,116,238,116,'#83bce9'),box(240,85,180,65,'Pipe segment'),arrow(423,116,486,116,'#83bce9'),box(488,85,155,65,'Powered pump'),caption(337,241,'New segment beyond pump; no more than 320×320 tiles per segment'));break;
case 'oil':a.push(box(16,95,156,70,'Crude oil'),arrow(174,130,219,130),box(222,95,146,70,'Refinery'),arrow(370,130,417,130),box(420,95,220,70,'Petroleum gas','#554636'),caption(530,208,'Plastic + sulfur'),caption(335,35,'Later: heavy → light → petroleum cracking'));break;
case 'bots':a.push(`<rect x="55" y="35" width="590" height="264" rx="6" fill="#1f3834" stroke="#85d7bd" stroke-width="4" stroke-dasharray="10 7"/>`,`<rect x="192" y="70" width="313" height="200" rx="3" fill="#544a24" fill-opacity=".55" stroke="#f2c979" stroke-width="4"/>`,box(273,127,153,65,'Roboport','#4b5145'),caption(349,55,'ORANGE = logistics'),caption(352,322,'GREEN (outer) = construction; illustrative coverage'));break;
case 'blueprint':a.push(box(22,94,180,72,'Working block'),arrow(205,130,260,130),box(264,94,172,72,'Ghost plan','#44516a'),arrow(439,130,495,130),box(499,94,150,72,'Robot builds','#3b5445'),caption(337,235,'Needs materials + construction coverage + robot'));break;
case 'circuit':a.push(box(25,85,160,70,'Tank: 12000'),arrow(190,120,258,120,'#ef777d'),box(263,85,190,70,'Condition >10000'),arrow(456,120,514,120,'#75d5bd'),box(515,85,136,70,'Pump ON'),caption(350,238,'Red/green wires carry SIGNALS, not electrical power'));break;
case 'rocket':a.push(box(20,75,165,77,'Rocket silo'),arrow(190,116,235,116),box(239,75,160,77,'Satellite'),arrow(402,116,451,116),box(456,75,210,77,'Launch + victory','#496144'),caption(340,245,'Cargo landing pad collects 1,000 space science packs'));break;
case 'debug':a.push(box(25,78,130,75,'Power?'),arrow(160,115,208,115),box(212,78,145,75,'Inputs?'),arrow(362,115,410,115),box(415,78,145,75,'Output?'),arrow(565,115,601,115),caption(335,235,'Inspect one possible cause at a time'));break;
 default:a.push(box(100,80,160,72,'Input'),arrow(264,116,370,116),box(374,80,160,72,'Output'));}
return `<svg viewBox="0 0 690 345" role="img" aria-label="${escapeHTML(kind)} concept diagram" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arr" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto"><path d="M0,0 L0,7 L8,3.5 Z" fill="#f2c979"/></marker></defs>${a.join('')}</svg><div class="caption">${escapeHTML(sub)}</div>`}
function list(items){return items.length?`<ul>${items.map(x=>`<li>${escapeHTML(x)}</li>`).join('')}</ul>`:''}
function renderHome(){const st=stats();const phases=['BEGIN','EARLY','MID','LATE','ADVANCED','FINISH','REFERENCE'];let h=heading('Learning map','Build your first working factory, one system at a time','Use the numbered walkthrough. Every chapter is self-contained, includes a picture and a checklist, and remembers your progress on this browser.');h+=`<div class="stat-row"><div class="stat"><b>${DATA.chapters.length}</b><small>guided chapters</small></div><div class="stat"><b>${st.total}</b><small>checkable steps</small></div><div class="stat"><b>${st.pct}%</b><small>completed</small></div></div><section class="panel"><h2>Your one-sentence goal</h2><div class="visual">${graphic('goal')}</div><p><strong>Ore → machines → science → rocket.</strong> Each new machine should solve one need from the previous step. You do not need a perfect factory to win.</p><div class="callout warn">This manual targets <strong>Factorio 2.1.24 without Space Age</strong>. Your base-game rocket carries a satellite and requires a cargo landing pad. It does not carry the engineer to other planets.</div></section>`;h+=`<section class="panel"><h2>Start here</h2><p>When overwhelmed, read only one chapter and complete one step. Use the <b>All keyboard shortcuts</b> and <b>Troubleshooting</b> screens only when you need them.</p><button class="btn primary" data-to="setup">Open chapter 1 →</button></section>`;for(const phase of phases){const cc=DATA.chapters.filter(x=>x.phase===phase);if(!cc.length)continue;h+=`<div class="eyebrow" style="margin-top:30px">${escapeHTML(phaseNames[phase])}</div><div class="panel">${cc.map(c=>`<div class="result"><strong>${escapeHTML(c.title)}</strong> <span class="tiny">${visited(c)}/${c.steps.length} steps</span><div>${escapeHTML(c.why)}</div><button class="btn" data-to="${c.id}">Open lesson</button></div>`).join('')}</div>`}return h}
function renderLesson(ch){const idx=DATA.chapters.findIndex(x=>x.id===ch.id);const s=visited(ch),total=ch.steps.length;let h=heading(`${phaseNames[ch.phase]} · Chapter ${idx+1}/${DATA.chapters.length}`,ch.title,ch.why);h+=`<div class="cols"><div><section class="panel"><h2>Follow these steps</h2><div class="progress"><div style="width:${Math.round(s/total*100)}%"></div></div><div class="tiny">${s} of ${total} steps checked. Checking means you actually tried it in Factorio.</div>${ch.steps.map((step,i)=>`<label class="step ${progress[ch.id+':'+i]?'done':''}"><input type="checkbox" data-check="${ch.id+':'+i}" ${progress[ch.id+':'+i]?'checked':''}><span class="step-text"><span class="number">${i+1}.</span>${escapeHTML(step)}</span></label>`).join('')}</section><section class="panel"><h2>Self-check: Can I explain this?</h2>${ch.checks.map((c,i)=>`<label class="check"><input type="checkbox" data-check="${ch.id+':quiz'+i}" ${progress[ch.id+':quiz'+i]?'checked':''}><span>${escapeHTML(c)}</span></label>`).join('')}</section></div><div><div class="panel"><h2>Picture first</h2><div class="visual">${graphic(ch.diagram)}</div><p class="tiny">These are simplified diagrams, not precise placement blueprints.</p></div>${ch.tips.length?`<section class="panel"><h2>Useful habits</h2>${list(ch.tips)}</section>`:''}${ch.misconceptions.length?`<section class="panel"><h2>Common misunderstanding</h2><div class="callout warn">${list(ch.misconceptions)}</div></section>`:''}<section class="panel"><h2>Check the official reference</h2><div class="refs">${ch.sources.map(k=>DATA.sources[k]?`<a target="_blank" rel="noopener" href="${DATA.sources[k][1]}">${escapeHTML(DATA.sources[k][0])}</a>`:'').join('')}</div><p class="tiny">Links need internet; the chapter does not.</p></section></div></div>`;h+=`<div class="actions"><button class="btn" ${idx===0?'disabled':''} data-to="${DATA.chapters[idx-1]?.id||'setup'}">← Previous chapter</button><button class="btn primary" data-to="${DATA.chapters[idx+1]?.id||'home'}">${idx===DATA.chapters.length-1?'Back to map':'Next chapter →'}</button></div>`;return h}
function renderControls(){let categories=['All',...new Set(DATA.controls.map(x=>x.category))];let filtered=DATA.controls.filter(x=>(filter==='All'||x.category===filter)&&([x.key,x.action,x.detail].join(' ').toLowerCase().includes(searchTerm.toLowerCase())));return heading('Reference','Every default keyboard and mouse shortcut','Search by task, key or words such as “train”, “filter”, “copy”. Controls are contextual, some are DLC-only and some are unbound by default.')+`<input class="search" id="lookup" placeholder="Search keys or actions (e.g. train, Ctrl, paste)" value="${escapeHTML(searchTerm)}" aria-label="Search shortcuts"><div class="filter">${categories.map(c=>`<button data-filter="${escapeHTML(c)}" class="${filter===c?'active':''}">${escapeHTML(c)}</button>`).join('')}</div><div class="panel tablewrap"><div class="tiny">${filtered.length} matching commands. Verify any rebound keys under Settings → Controls.</div><table><thead><tr><th>Key / gesture</th><th>Action</th><th>Meaning</th></tr></thead><tbody>${filtered.map(r=>`<tr><td><span class="kbd">${escapeHTML(r.key)}</span></td><td><strong>${escapeHTML(r.action)}</strong></td><td>${escapeHTML(r.detail)}${r.scope!=='Base'?` <span class="tag">${escapeHTML(r.scope)}</span>`:''}</td></tr>`).join('')}</tbody></table></div>`}
function renderHelp(){let f=DATA.troubleshooting.filter(([q,a])=>(q+' '+a).toLowerCase().includes(searchTerm.toLowerCase()));return heading('Rapid diagnosis','Find out why the factory stopped','Always follow the same sequence: machine status → power/fuel → input → output → transport → wires.')+`<input class="search" id="lookup" placeholder="Search symptom: No path, robot, oil, power…" value="${escapeHTML(searchTerm)}" aria-label="Search problems"><div class="panel"><h2>${f.length} problems and first checks</h2>${f.map(([q,a])=>`<details class="expand"><summary>${escapeHTML(q)}</summary><p>${escapeHTML(a)}</p></details>`).join('')}</div><div class="panel"><h2>Diagnostic picture</h2><div class="visual">${graphic('debug')}</div></div>`}
function renderGlossary(){const f=DATA.glossary.filter(x=>x.join(' ').toLowerCase().includes(searchTerm.toLowerCase()));return heading('Learning the vocabulary','Plain-language glossary','Every new concept gets one short description. Search by any word you do not understand.')+`<input class="search" id="lookup" placeholder="Look up: block, orange, throughput…" value="${escapeHTML(searchTerm)}" aria-label="Search glossary"><div class="panel">${f.map(([term,definition])=>`<div class="result"><strong>${escapeHTML(term)}</strong><div>${escapeHTML(definition)}</div></div>`).join('')}</div>`}
function renderWhatsnew(){return heading('Current facts','What 2.1.24 means for you','Features relevant to the modern base game are separated from expansion-only features. This section is about how the current game behaves, not a historical changelog.')+`<section class="panel"><h2>Changes that matter while playing</h2><div class="tablewrap"><table><thead><tr><th>Introduced</th><th>Applies to</th><th>Available behavior</th></tr></thead><tbody>${DATA.qol.map(([v,scope,ex])=>`<tr><td>${escapeHTML(v)}</td><td><span class="tag">${escapeHTML(scope)}</span></td><td>${escapeHTML(ex)}</td></tr>`).join('')}</tbody></table></div><div class="callout warn">2.1.24 was experimental when researched, not the latest confirmed stable build. The official 2.1.24 patch notes and 2.1 stable announcement are in Sources.</div></section>`}
function renderSources(){return heading('Verified references','Official sources and scope','Source links are intentionally online-only; the manual itself is offline. These resources are where the local AI building agent should check factual claims and game-data changes.')+`<section class="panel"><h2>Primary source register</h2>${Object.entries(DATA.sources).map(([id,[name,url]])=>`<div class="result"><strong>${escapeHTML(name)}</strong><div><a href="${url}" target="_blank" rel="noopener">${escapeHTML(url)}</a></div></div>`).join('')}</section><section class="panel"><h2>Important verification caveats</h2><ul><li>Official Factorio wiki pages can contain both base-game and Space Age tabs. Always use the base-game values.</li><li>The official older Quick Start Guide is helpful for concepts but has outdated boiler/pump ratios; prefer current Power production.</li><li>Player-changed hotkeys override defaults. The live game Controls panel is authoritative for the user’s installation.</li><li>The manuals explicitly exclude modded recipe or progression changes.</li><li>Current patch is version 2.1.24. This handbook is not guaranteed correct for releases later than October 27, 2026.</li></ul></section>`}
function renderDiagrams(){let kinds=[['goal','Factory goal'],['ore','First smelting'],['power','Electric power'],['belt','Belt lanes'],['science','Science and labs'],['signals','Train signals'],['bots','Robot zones'],['fluid','Fluid pipes'],['oil','Refining'],['circuit','Oil circuit'],['rocket','Rocket victory']];return heading('Visual reference','Learn with diagrams','Select a system. These are conceptual maps to explain flow, not importable or tile-accurate blueprints.')+`<div class="panel"><div class="diagram-tabs">${kinds.map(([id,name],i)=>`<button class="${(window._diagram||'goal')===id?'active':''}" data-diagram="${id}">${name}</button>`).join('')}</div><div class="visual" id="diagramPic">${graphic(window._diagram||'goal')}</div></div><div class="panel"><h2>Train signal thought experiment</h2><p>A train approaches an intersection. The immediate crossing block is empty, but its exit block is occupied. What happens?</p><div class="railbuttons"><button class="btn" data-rail="regular">Try regular signal</button><button class="btn" data-rail="chain">Try chain signal</button></div><div id="railOutcome" class="callout">Choose one signal above.</div><p class="tiny">Simplified case: one path, chain signal guarding the junction, with a regular signal at its exit.</p></div><div class="panel"><h2>Steam power mini-planner</h2><label for="boilerCount">How many boilers?</label> <input id="boilerCount" type="number" min="1" max="500" value="4" class="search" style="width:120px;display:inline-block"><div id="powerCount" class="callout">4 boilers supply 8 engines → 7.2 MW maximum generation.</div><p class="tiny">Assumes full boiler fuel, 165°C steam, and sufficient water and power demand; a layout is constrained by actual pipe and machine connections.</p></div>`}
function render(){totalNav();const ch=DATA.chapters.find(c=>c.id===route);let h=ch?renderLesson(ch):({home:renderHome,controls:renderControls,diagrams:renderDiagrams,help:renderHelp,glossary:renderGlossary,whatsnew:renderWhatsnew,sources:renderSources}[route]||renderHome)();$('content').innerHTML=h;document.querySelectorAll('[data-to]').forEach(b=>b.onclick=()=>nav(b.dataset.to));document.querySelectorAll('[data-check]').forEach(b=>b.onchange=()=>{progress[b.dataset.check]=b.checked;persist();const key=b.dataset.check;render();document.querySelector('[data-check=\"'+key+'\"]')?.focus({preventScroll:true})});document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;render();$('lookup')?.focus()});const inp=$('lookup');if(inp){inp.addEventListener('input',e=>{searchTerm=e.target.value;const pos=e.target.selectionStart;render();const ii=$('lookup');ii?.focus();ii?.setSelectionRange(pos,pos)});}document.querySelectorAll('[data-diagram]').forEach(b=>b.onclick=()=>{window._diagram=b.dataset.diagram;render()});document.querySelectorAll('[data-rail]').forEach(b=>b.onclick=()=>{let isChain=b.dataset.rail==='chain';$('railOutcome').innerHTML=isChain?'<strong>Chain: WAIT before entering.</strong> The crossing is empty, but the path beyond its exit is not free. The train stays outside the intersection.':'<strong>Regular: ENTER the empty crossing block.</strong> It can then stop inside the intersection at the next red signal, blocking other paths. This is why a regular signal alone is dangerous at a junction entrance.'});const bc=$('boilerCount');if(bc){bc.oninput=()=>{let n=Number(bc.value);$('powerCount').textContent=Number.isInteger(n)&&n>0&&n<=500?`${n} boilers supply ${2*n} steam engines → ${(1.8*n).toLocaleString()} MW maximum generation.`:'Enter a whole boiler count from 1 to 500.'}}}
$('exportBtn').onclick=()=>{const blob=new Blob([JSON.stringify({manualVersion:DATA.meta.version,exported:new Date().toISOString(),progress},null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='factorio-manual-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
$('importBtn').onclick=()=>$('importFile').click();$('importFile').onchange=async e=>{
 const f=e.target.files[0];if(!f)return;
 try{
  const obj=JSON.parse(await f.text());
  if(!obj||obj.manualVersion!==DATA.meta.version)throw new Error('Choose a progress export for manual version '+DATA.meta.version+'.');
  const imported=validateProgress(obj.progress);
  progress=imported;persist();render();alert('Progress imported.');
 }catch(err){alert('Could not import progress. '+err.message)}
 finally{e.target.value=''}
};
$('lessonsBtn').onclick=()=>{document.querySelector('.side').scrollIntoView({behavior:'smooth'})};window.addEventListener('hashchange',()=>{const r=readRoute();if(r!==route){route=r;searchTerm='';render()}});route=readRoute();render();
</script></body></html>'''
html_path=P/'index.html'
serialized=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
html_path.write_text(TEMPLATE.replace('__DATA__',serialized),encoding='utf8')

spec=f'''# Factorio 2.1.24 — Offline beginner manual | Implementation handoff

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

- {len(chapters)} tutorial chapters with **{sum(len(c['steps']) for c in chapters)} checkable, ordered steps**, each chapter with labeled original SVG diagram, actionable self-checks, useful habits, official-source links.
- {len(controls)} searchable contextual PC keyboard/mouse commands; advanced and DLC-only controls explicitly labeled where known.
- {len(troubles)} symptom → likely cause → first fix entries; {len(glossary)} plain-language glossary entries.
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
'''
for name,url in sources.values():spec+=f'- [{name}]({url})\n'
spec+='''
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
'''
(P/'AGENT_HANDOFF.md').write_text(spec,encoding='utf8')
readme='''# Factorio 2.1.24 beginner manual

1. Double-click `index.html` in a browser. No server or internet required.
2. Work through the numbered lessons; check a step only when you complete it in the game.
3. Use keyboard controls, troubleshooting, glossary, diagrams and current-version reference as needed.
4. Use **Export progress** to save progress as a JSON file and **Import progress** to move it to another browser/computer.
5. For a local AI builder, start with `AGENT_HANDOFF.md` and `manual_data.json`; `controls.csv` is a searchable/exportable controls table.

To rebuild after editing `build.py`, run `python3 build.py`. It writes the HTML, data, references and ZIP beside the script. Use `python3 build.py --output-dir /path/to/output` for a separate output folder. Python 3 is needed only for rebuilding.

Browser regression checks (development only): install Playwright in a virtual environment with `pip install playwright`, then run `python tests/test_manual.py`. This uses system Chromium when available; otherwise run `playwright install chromium` first. For Firefox, run `playwright install firefox` and `python tests/test_manual.py --browser firefox`. Tests open the manual via `file:///` with networking disabled.

Progress is saved in this browser when local storage is available. If saving is blocked, the manual displays a notice; export a backup before closing. Imports accept exports from manual version 2.1.24 and replace current progress only after validation.

This is a broad, usable first-pass manual and research handoff, **not an exhaustive verified representation of every vanilla game prototype, machine, recipe or Lua/debug binding**. The handoff identifies how to reach that standard.
'''
(P/'README.md').write_text(readme,encoding='utf8')
with zipfile.ZipFile(archive_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for fname in ['index.html','manual_data.json','controls.csv','AGENT_HANDOFF.md','README.md','build.py','tests/test_manual.py']:
  z.write(Path(__file__).resolve().parent/fname if fname in ('build.py','tests/test_manual.py') else P/fname,arcname=fname)
print('HTML',html_path.stat().st_size,'bytes, ZIP',archive_path.stat().st_size)
