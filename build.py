import argparse, json, csv, zipfile
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
from content import enrich
from validate import validate
payload = enrich(payload)
validate(payload)
(P/'manual_data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (P/'controls.csv').open('w',newline='',encoding='utf8') as f:
    fields = ['category','key','action','detail','scope','note','context','example','pitfall','level','source','verification','id']
    writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
    writer.writeheader();writer.writerows(payload['controls'])
source_root=Path(__file__).resolve().parent
template=(source_root/'web/template.html').read_text()
serialized=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
# Tokens are substituted in one pass so authored text cannot be interpreted as a template token.
import re
substitutions={'STYLE':(source_root/'web/styles.css').read_text(),'DATA':serialized,'SCRIPT':(source_root/'web/app.js').read_text()}
page=re.sub(r'__(STYLE|DATA|SCRIPT)__',lambda match:substitutions[match[1]],template)
(P/'index.html').write_text(page,encoding='utf8')
source_files=['build.py','content.py','validate.py','README.md','AGENT_HANDOFF.md','AUDIT.md','data/reference.json',
              'web/template.html','web/styles.css','web/app.js','tools/extract_prototypes.lua','tools/extract_reference.py',
              'tests/test_manual.py','tests/test_data.py']
for name in ['README.md','AGENT_HANDOFF.md','AUDIT.md']:
    if P != source_root:(P/name).write_bytes((source_root/name).read_bytes())
with zipfile.ZipFile(archive_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for name in ['index.html','manual_data.json','controls.csv']:
        z.write(P/name,arcname=name)
    for name in source_files:z.write(source_root/name,arcname=name)
print(f"Built {len(payload['chapters'])} lessons, {len(payload['topics'])} topics, {len(payload['controls'])} controls, "
      f"{len(payload['reference']['recipes'])} recipes and {len(payload['reference']['technologies'])} technologies.")
print(f"Offline HTML: {P/'index.html'} ({(P/'index.html').stat().st_size:,} bytes)")
print(f"Archive: {archive_path} ({archive_path.stat().st_size:,} bytes)")
