"""Original teaching content and corrections for the 2.1.24 offline manual.

Recipe/technology quantities are injected from the pinned data/reference.json.
Tutorial advice is identified separately from exact prototype facts.
"""
from pathlib import Path
import json

TOPICS=[]
def topic(id, title, category, summary, sections, *, sources=(), recipes=(), entities=(), related=(), experiment='', pitfalls=(), diagram='debug'):
    TOPICS.append(dict(id=id,title=title,category=category,summary=summary,
        sections=[dict(title=h,text=t) for h,t in sections],sources=list(sources),recipes=list(recipes),entities=list(entities),related=list(related),experiment=experiment,pitfalls=list(pitfalls),diagram=diagram))

topic('orientation','Reading the game: cursor, inventories and machine status','Foundations',
 'Learn what you are looking at before making a bigger factory.',[
 ('Three different places for an item','An item can be in your character inventory, held by the cursor, or stored in a machine. A quickbar slot points to an item or tool; it adds no storage. A ghost is a building order. Clearing your cursor with Q puts real items back into inventory; it does not delete a factory.'),
 ('Use the status as evidence','Hover a machine and inspect its recipe and exact status. An idle machine may be behaving correctly: its output is full, its target inventory has enough ingredients, or its products are not currently needed. Open the machine to distinguish ingredients from fuel, products, modules and fluid connections. Alt-mode adds labels; it does not supply power or configure a recipe.'),
 ('A useful learning loop','Choose one output, assemble the smallest working chain, watch it produce, interrupt one input, and explain the resulting status. Then repair it. This makes failure understandable before you copy the chain across a large area. Save a separate experiment world for testing configurations.')],
 sources=['controls','prototypes'],related=['flow','diagnosis'],experiment='Make one furnace produce one iron plate. Remove its fuel, observe the status, restore fuel, then deliberately block its output.',diagram='input')

topic('flow','The factory as a flow network','Foundations',
 'Inventory, production rate, capacity and demand describe different things.',[
 ('Stock and rate','Stock is the number of items currently stored. Rate is items per second or per minute. A chest containing 2,000 plates does not tell you how quickly the factory makes plates. A belt rated at 15 items/s is transport capacity; its actual flow may be lower because supply or demand is lower.'),
 ('Conservation explains most stalls','Over an interval, inventory change equals incoming items minus outgoing items. A growing buffer means inflow exceeds outflow during that interval. A shrinking buffer means demand exceeds supply. Once a buffer fills, upstream machines stop; that may be normal demand control rather than a fault.'),
 ('Separate three limits','A line can be supply-limited, processing-limited or transport-limited. If ore arrives sparsely, adding furnaces does not help. If furnaces are busy and ore backs up while plates are scarce, add processing. If plate output backs up before one narrow belt, improve that transport segment. One downstream consumer can also be the limiting demand.')],
 sources=['prototypes','statistics'],related=['ratios','statistics','scaling'],experiment='Limit a gear chest to one slot. Watch gears back up; reopen slots and see the line restart without changing any machine.',diagram='assemble')

topic('world','World settings, saves and a peaceful learning route','Foundations',
 'Choose a world that supports the kind of learning you want.',[
 ('What resource sliders mean','Frequency controls how often patches appear; size controls their area; richness controls how much each ore tile contains. A richer tile lasts longer; it does not make a drill mine faster. Preview the map to check starting iron, copper, coal, stone, water, and room to expand.'),
 ('Choose difficulty intentionally','Default Freeplay teaches resource depletion and defense together. For a learning route, peaceful mode reduces enemy pressure; enemies may still retaliate when provoked. Enemy expansion, pollution and evolution are separate settings. A rail-world preset emphasizes distant deposits and changes enemy expansion. Check achievement restrictions in your own game before choosing settings if achievements matter.'),
 ('Use durable checkpoints','Make named saves before major rebuilds and updates. Keep a copy outside a rotating autosave set. A map exchange string recreates generation settings, not your built factory. A blueprint saves a design, not your inventory, research or world. The manual’s progress export records checkboxes only.')],
 sources=['mapgen','linux'],related=['pollution','outposts','backups'],experiment='Preview the same seed at different richness values. Compare patch size and listed resource amounts rather than assuming the slider changes drill output.',diagram='goal')

topic('iron','Iron: mining, plates, gears and steel demand','Materials',
 'Iron is shared by construction, circuits, transport, steel and science.',[
 ('From patch to plate','A drill consumes finite ore tiles in its mining area and outputs directly to the indicated destination. For ordinary iron without bonuses, an electric drill with mining speed 0.5 and mining time 1 yields 0.5 ore/s. Thirty continuously working drills can therefore supply 15 ore/s, provided their outputs and both belt lanes can carry it.'),
 ('Find the actual constraint','A drill with a blocked output is not short of ore. A depleted drill needs a new location. A powered drill may run slowly during a power shortage. Mining productivity adds output without an equivalent increase in patch depletion; it changes the drill count needed for a belt.'),
 ('Budget competing consumers','Iron plates become gears, belts, inserters, circuits, ammunition and steel. Steel takes five plates per unmodified craft, so a new steel line can consume iron that previously fed the whole base. Use limited mall chests and a deliberate split of supply before expanding science. Keep ore, plate and steel rates in different columns when planning.')],
 sources=['mining','prototypes'],recipes=['iron-plate','iron-gear-wheel','steel-plate'],entities=['electric-mining-drill','stone-furnace'],related=['smelting','scaling','outposts'],experiment='Supply 30 drills to one yellow belt, without bonuses, and inspect both lanes. If it falls short, count active drills and check output placement and power.',diagram='ore')

topic('copper','Copper: why circuits consume so much','Materials',
 'Copper demand becomes dominant when circuits and late science expand.',[
 ('Ore and plates','Copper uses the same baseline mining and smelting times as iron, but it has a separate supply chain. A common early mistake is letting convenient iron infrastructure determine the size of copper production. Copper needs grow sharply with advanced circuits, processing units and low-density structures.'),
 ('Cable expands the item flow','One copper plate becomes two copper cables. Transporting the plates and making cable beside a consumer can reduce belt traffic. One electronic circuit uses three cables and one iron plate, equivalent to 1.5 copper plates and one iron plate without productivity. For equal machine speeds, three cable assemblers can feed two continuously working circuit assemblers.'),
 ('Direct insertion has a reason','Placing cable assemblers beside circuit assemblers avoids moving a bulky intermediate along a shared bus. This is a layout choice, not a requirement: a short cable belt is fine where its capacity is sufficient. When circuits slow down, check copper plates, cable transfer and iron independently before increasing the circuit assembler count.')],
 sources=['prototypes'],recipes=['copper-plate','copper-cable','electronic-circuit','advanced-circuit','processing-unit','low-density-structure'],related=['circuits-production','ratios'],experiment='Calculate the plate demand of 2 electronic circuits/s: 2 iron plates/s and 3 copper plates/s. Build a small line and compare its steady input with that prediction.',diagram='assemble')

topic('stone-coal','Stone, coal, wood, landfill and construction materials','Materials',
 'Small early resource lines become essential infrastructure later.',[
 ('Stone has several jobs','Raw stone supplies furnaces, rail recipes and landfill. Two stone become one brick in smelting; bricks feed walls, paving, concrete and other buildings. Reserve raw stone as well as bricks. A brick furnace that consumes every incoming stone can starve rail production even with a full brick chest.'),
 ('Coal is fuel and a chemical ingredient','Coal fuels early drills, furnaces, boilers and vehicles, but plastic, grenades and explosives also use it as an ingredient. A power station that loses coal can stop the drills and inserters delivering more coal, creating a restart problem. A burner inserter feeding the boiler and an accessible emergency coal reserve can help bootstrap recovery.'),
 ('Permanent construction choices','Landfill consumes stone and creates buildable ground; paving creates faster walking surfaces. Keep a route to water extraction and room for poles and pipes. Use a filtered deconstruction planner when removing paving or clearing terrain, and inspect its selection before issuing a large order. Wood is useful for early poles and fuel; later pole types remove the dependency on tree cutting.')],
 sources=['prototypes','deconstruction'],recipes=['stone-brick','concrete','refined-concrete','landfill','plastic-bar','explosives'],related=['smelting','power-recovery'],experiment='Create separate limited outputs for stone and bricks. Confirm that both a rail assembler and a wall assembler can obtain their different ingredients.',diagram='steel')

topic('smelting','Smelting arrays and exact baseline ratios','Materials',
 'Size furnaces from recipe time and crafting speed, then test the transport.',[
 ('The plate calculation','Iron and copper plates each take 3.2 recipe seconds at crafting speed 1. A stone furnace makes 1/3.2 = 0.3125 plates/s; 48 produce 15/s. Steel and electric furnaces both have crafting speed 2, so 24 make the same 15/s before modules. These counts assume continuous input, correct fuel or power, and full unloading.'),
 ('Steel and bricks are different','Steel uses five iron plates in 16 recipe seconds. At equal furnace speeds, one iron furnace’s output supplies one steel furnace’s input. The steel item rate is five times lower than the iron plate rate. Bricks use two stone per craft and have their own output rate. A familiar plate blueprint may have the wrong lane arrangement for these inputs.'),
 ('Fuel and upgrades','A steel furnace doubles stone-furnace processing speed without doubling its listed fuel power. An electric furnace needs no fuel inserter, but it is physically larger, consumes electricity and accepts modules. Moving pollution from the furnace to coal-fired generators does not eliminate it. Decide the upgrade from power availability, modules and layout, not only its technology tier.')],
 sources=['prototypes'],recipes=['iron-plate','copper-plate','steel-plate','stone-brick'],entities=['stone-furnace','steel-furnace','electric-furnace'],related=['iron','copper','ratios'],experiment='Use the calculator to predict one furnace’s output, then compare 48 stone furnaces with 24 steel furnaces on the same plate recipe.',diagram='steel')

topic('circuits-production','Electronic circuits, advanced circuits and processing units','Materials',
 'Treat each circuit tier as a different production problem.',[
 ('Green circuits','Electronic circuits combine iron plate with copper cable. Cable is the bulky fast intermediate; direct insertion is useful. The classic 3 cable machines : 2 circuit machines follows from their recipe quantities and times only when crafting speeds and bonuses match.'),
 ('Red circuits','Advanced circuits add plastic and more cable to electronic circuits. Oil supply therefore becomes part of the electronics chain. Their longer recipe time means a few green-circuit machines can feed many red-circuit machines, but the extra cable and plastic still need adequate belts and inserters.'),
 ('Blue circuits','Processing units add sulfuric acid to electronic and advanced circuits. They require a machine with fluid-capable crafting. Check the correct fluid port after rotation or flipping, and verify the acid supply rather than adding ordinary inserters. Low production rates are normal for an initially small blue-circuit line; steady automated output is more useful than a large hand-fed batch.')],
 sources=['prototypes'],recipes=['electronic-circuit','advanced-circuit','processing-unit','sulfuric-acid'],related=['oil-products','copper','ratios'],experiment='Disconnect only the processing unit acid input. Identify its status, reconnect it, and check whether its solid inputs can sustain the resumed rate.',diagram='assemble')

topic('ratios','Production mathematics: derive a ratio instead of memorizing it','Design and scale',
 'Use quantities, time, speed, productivity and availability with explicit units.',[
 ('Start with crafts per second','For a continuously working machine, crafts/s = effective crafting speed ÷ recipe time. Output/s = crafts/s × output quantity × (1 + productivity) for an ordinary productivity-eligible output. Ingredient/s = crafts/s × ingredient quantity. Productivity increases output without proportionally increasing ingredient use; it does not reduce the input of an individual normal craft.'),
 ('Count the machines','For target output R, machine count = R × recipe time ÷ [crafting speed × output quantity × (1 + productivity)]. Round up for a whole-machine build, then expect excess capacity. The displayed recipe seconds are measured at speed 1: an assembler 1 at speed 0.5 takes twice as long. If an installation is active only 80% of the time, its long-run output is at most 80% of the ideal value.'),
 ('Know where the formula stops','Catalysts, probabilistic outputs, temperature, research and multiple products need extra care. Kovarex returns most of its U-235 input: gross output is not net gain. Uranium processing gives a distribution, not a guaranteed U-235 every fixed number of crafts. The calculator labels unsupported productivity cases and reports expected outputs separately from deterministic quantities.')],
 sources=['prototypes','recipe-api'],related=['science-ratios','modules-math','statistics'],experiment='Predict 2 electronic circuits/s in assembler 2: 2 × 0.5 ÷ 0.75 = 1⅓ machines before bonuses. Two machines provide spare capacity, but need ingredient flow to use it.',diagram='assemble')

topic('scaling','Scaling: starter base, bus, direct insertion and modular blocks','Design and scale',
 'Choose a layout for its tradeoffs and measure the bottleneck before expanding.',[
 ('Starter layouts are allowed to be temporary','A compact irregular starter base can make a rocket. Leave corridors for belts, poles, pipes and walking; use limited supply chests for the machines you repeatedly place. Rebuild a small troublesome section when the time saved exceeds the cost, rather than restarting the whole world for symmetry.'),
 ('Compare layout patterns','A main bus offers predictable access to shared materials but its early segments must carry all downstream demand. Direct insertion reduces transport for bulky intermediates and ties neighboring machine ratios together. Rail-connected blocks isolate production and allow repetition, at the cost of stations, buffers, train traffic and more space. No pattern creates resources or removes conservation of flow.'),
 ('Scale one measured constraint','Pick a target such as 30 science packs/min and trace backward. Add mining and smelting before increasing a downstream line that is already input-starved. Test a representative block at full demand before copying it. Record its input/output rate, power, train length and connector positions so future modules really are compatible.')],
 sources=['prototypes','statistics'],related=['flow','outposts','rail-throughput'],experiment='Limit your next expansion to one bottleneck. Record output before and after over the same time window and explain where the next constraint appeared.',diagram='goal')

topic('belts-lanes','Belts: lanes, side-loading, undergrounds and compression','Transport',
 'A belt has two independently occupied lanes moving in the same direction.',[
 ('Capacity is per lane as well as per belt','Without belt stacking, yellow, red and blue belts carry 15, 30 and 45 items/s across both lanes. Each lane carries half. A nominally half-full belt can therefore have one lane at capacity and the other unused. A single side-load or inserter drop may only populate one lane.'),
 ('Connections preserve structure','Side-loading feeds one destination lane; it is not the same as merging two fully usable belts. Inserters can pick from either lane, but drop placement follows orientation rules. Underground entrances and exits have different collision and access behavior from an ordinary straight belt. Inspect actual item movement, not just the drawn arrows.'),
 ('Buffering is not throughput','Belts store items along their length, which delays the appearance of shortages and surpluses. Upgrading one yellow segment helps only if it is the limiting segment; a yellow underground or splitter in the route still restricts flow. The green turbo belt and the belt-stacking inserter are outside this base-only manual.')],
 sources=['belts','inserters','prototypes'],entities=['transport-belt','fast-transport-belt','express-transport-belt','underground-belt','fast-underground-belt','express-underground-belt'],related=['splitters','inserter-details'],experiment='Feed only one lane of a yellow belt and draw 10 items/s from it. Explain why a 7.5 items/s lane cannot satisfy that demand even though the belt’s combined rating is 15.',diagram='belt')

topic('splitters','Splitters: priority, filtering and balancing','Transport',
 'A splitter routes existing items; it does not manufacture additional capacity.',[
 ('What gets shared','A splitter distributes available input between its available outputs. It preserves lane structure rather than freely shuffling every item between lanes. If one output is blocked, items can use the other allowed output. Two inputs at maximum belt rate cannot both fit on one output belt at that same tier.'),
 ('Use priority for a reason','Output priority can protect boiler coal, ammunition or a critical production line. Input priority can prefer reclaimed items or an older supply. A configured filter separates a chosen item; ensure the filtered destination has somewhere to go, or that item may back up. Priority is not a promise that supply is sufficient.'),
 ('Balancers solve a specific problem','Belt balancing distributes between belts; lane balancing distributes between lanes. A symmetric-looking design is not proof that it balances correctly under partial input or blocked output. Test the input/output states you actually need before repeating a design. Often a small priority split is sufficient.')],
 sources=['prototypes','splitter'],related=['belts-lanes','flow'],experiment='Supply one splitter with a mixed iron/copper belt. Filter iron to one output, then block it; observe which items can still leave and explain the backup.',diagram='belt')

topic('inserter-details','Inserters: pickup, drop, filters and useful limits','Transport',
 'The swing, hand size, target and source all affect throughput.',[
 ('Direction and reach','The pickup is behind an inserter and the drop is ahead. A long-handed inserter reaches farther; a fast inserter swings faster; a bulk inserter carries a larger hand after the relevant research. Bulk inserters are base game. The Space Age stack inserter has a different belt-stacking role.'),
 ('Why it waits with a nonempty source','Inserters usually insert only a useful working quantity into crafting and fuel slots. They need not fill the entire input inventory. A wrong filter, a full destination, a circuit condition, inadequate power or an unacceptable item can also prevent movement. A wagon moving or waiting at a signal is not a normal automatic loading station.'),
 ('Measure the real transfer','Chest-to-chest throughput differs from belt pickup and belt drop. Hand capacity research, lane occupancy and source timing can change the result. Avoid promising one universal items/s number per inserter. For a high-volume station, inspect whether inserters, chests or downstream belts are the limiting stage.')],
 sources=['inserters','prototypes'],entities=['inserter','long-handed-inserter','fast-inserter','bulk-inserter'],related=['belts-lanes','rail-loading'],experiment='Put an ordinary inserter between a plate chest and a gear assembler. When it waits, open the assembler and check whether it already has enough input for its next crafts.',diagram='assemble')

topic('steam-power','Steam power: water, fuel, steam and electricity','Power',
 'Trace four separate systems instead of treating the plant as one machine.',[
 ('The baseline chain','Water extraction needs no electricity. A boiler burns up to 1.8 MW of fuel and converts 6 water/s into 60 steam/s at 165°C. Two steam engines together use that steam and can generate 1.8 MW. An offshore pump’s 1,200 water/s gives a theoretical water budget for 200 boilers, subject to valid segments and sufficient connections.'),
 ('Match supply with demand','Steam engines throttle down when electricity is not needed. Their low current output does not imply failure. At high demand, check boiler fuel, water, steam connections and the electric network. A pipe full of water does not mean the steam outlet is connected. An engine connected to poles can still belong to an isolated power island.'),
 ('Fuel budget','Coal has 4 MJ per item. A boiler burning 1.8 MJ/s therefore needs 0.45 coal/s at full use. Twenty boilers need 9 coal/s for power alone. This is a fuel-flow calculation, not a requirement to run all boilers constantly. Preserve access to coal and a way to restart fuel inserters during a blackout.')],
 sources=['power','prototypes'],entities=['offshore-pump','boiler','steam-engine'],related=['electricity','power-recovery','fuel'],experiment='Calculate the maximum output and coal demand of 10 boilers: 18 MW and 4.5 coal/s before other fuel consumers.',diagram='power')

topic('electricity','Electric networks, coverage, load and storage','Power',
 'Pole wire reach and machine coverage are separate constraints.',[
 ('Follow the actual wire network','Connected poles share one electrical network. A machine needs to be within a connected pole’s supply area, not merely near a copper wire. Big poles are useful for transmission; substations and medium poles offer different supply footprints. A power switch can intentionally divide networks.'),
 ('Read capacity and demand together','A demand spike can slow mining, inserters and crafting at the same time. A self-reinforcing brownout appears when the machines supplying boiler fuel also slow down. Isolate critical loads or add reliable generation and restart reserves rather than increasing downstream machine counts.'),
 ('Energy is not power','Watts measure energy per second; joules measure stored energy. A 5 MJ accumulator could ideally supply 1 MW for 5 seconds if its discharge limit allowed it. The actual accumulator discharge limit is 300 kW, so one cannot serve a 1 MW load by itself. Both energy capacity and instantaneous power capacity matter. Idle drain and roboport recharge demand also belong in the budget.')],
 sources=['electric','prototypes'],entities=['small-electric-pole','medium-electric-pole','big-electric-pole','substation','accumulator','power-switch'],related=['steam-power','solar','robot-throughput'],experiment='Disconnect a pole bridging two factory sections. Use each section’s electricity window to identify the separated networks before reconnecting.',diagram='power')

topic('power-recovery','Recovering a blackout without losing the coal loop','Power',
 'Restart the dependency that powers everything else.',[
 ('Identify the failed stage','First inspect one connected pole: are generators unavailable, or has total load exceeded capacity? Then trace fuel and water at the boilers. If the coal belt is empty, inspect its miners and power supply. Adding steam engines cannot help boilers that have no fuel.'),
 ('Bootstrap deliberately','Temporarily disconnect nonessential loads if useful. Hand-feed a few boilers from an emergency stock, and ensure their engines power coal extraction and fuel delivery. A burner inserter can feed itself from accessible fuel while delivering boiler coal, but its direction, source and startup fuel still matter. Wait until the fuel belt has recovered before reconnecting large loads.'),
 ('Prevent recurrence','Set a low-fuel warning, reserve coal throughput before discretionary chemical consumers, and expand generation before heavy robotics or laser defenses. Solar or a separately supplied critical network can protect the coal loop, but complex isolation is optional for a first rocket. Practice the restart procedure while your factory is small.')],
 sources=['prototypes','electric'],related=['steam-power','circuit-recipes'],experiment='In an experiment save, stop the coal supply, observe the failure cascade, then restart with a small manual fuel reserve. Record the minimum chain that had to be restored.',diagram='debug')

topic('solar','Solar and accumulators: average power and night reserve','Power',
 'Daytime peak output is not continuous all-day power.',[
 ('Nauvis baseline','A solar panel produces up to 60 kW during full daylight. Averaged over the default Nauvis day-night cycle, the planning value is 42 kW per panel. The common balanced ratio is 21 accumulators per 25 panels, assuming normal base-game panels, accumulators and the standard day cycle.'),
 ('Compute a target','For a steady 10 MW load, about 10,000/42 = 238.1 panels and 0.84 times as many accumulators give an ideal starting estimate; round up and allow margin. Accumulators need enough daytime surplus to recharge as well as enough capacity and discharge power to last through the dark period.'),
 ('Diagnose the night failure','If storage empties before dawn, check daytime charging, new load, connected poles and both panel and accumulator counts. A single sunny afternoon snapshot is not a full-cycle test. Keep steam backup while testing the design under ordinary factory and defense loads.')],
 sources=['power','prototypes'],entities=['solar-panel','accumulator'],related=['electricity','nuclear-heat'],experiment='Watch accumulator charge across a full day and night with a steady load. Compare the next dawn’s charge with the previous dawn instead of judging only at noon.',diagram='power')

topic('fuel','Fuel choices and vehicle performance','Power',
 'Energy per item and vehicle bonuses answer different questions.',[
 ('Compare energy quantities','Wood, coal, solid fuel and rocket fuel have different fuel values. Divide a burner’s power use by energy per item to estimate item consumption. An efficient fuel line may reduce item traffic without changing the energy demand. Nuclear fuel for locomotives is an item distinct from the uranium fuel cell consumed by reactors.'),
 ('Fuel as chemistry','Making solid fuel from light oil is generally a better use of that oil than making it from petroleum gas. Solid fuel is itself an ingredient of rocket fuel. A fuel recipe can be valuable as a controlled oil outlet, but indiscriminately converting petroleum can starve plastic and science.'),
 ('Fuel as performance','Some fuels give locomotives and vehicles acceleration or top-speed bonuses in addition to their energy content. Use the item record and in-game tooltip rather than assuming that a tenfold energy value means tenfold speed. A fuel choice that is sensible for a train is not automatically the best boiler fuel.')],
 sources=['prototypes'],recipes=['solid-fuel-from-light-oil','solid-fuel-from-heavy-oil','solid-fuel-from-petroleum-gas','rocket-fuel','nuclear-fuel'],related=['oil-balancing','rail-throughput'],experiment='Use a fuel’s MJ/item to calculate how long one item can run a continuously loaded 1.8 MW boiler, then compare with observed throttling at low demand.',diagram='power')

topic('fluids-modern','Fluid segments: modern pipes and the 320×320 boundary','Fluids and oil',
 'Pipes within a valid segment share fluid; pumps connect separate segments.',[
 ('A segment is one connected vessel','Directly connected pipes and tanks form a segment. Within a valid segment, transfer is effectively instant rather than the old pipe-by-pipe distance simulation. Machine ports and pumps still have transfer limits. Increasing pipe count inside a valid segment does not create more production.'),
 ('Overextension is geometric','A segment must fit within the allowed 320×320-tile bounding area. It is not a count of 320 pipe entities. A winding or underground line can cross the boundary with fewer visible pieces. Use the pipeline overlay and warning, then insert powered, correctly oriented pumps to create smaller segments.'),
 ('Ports carry a specific fluid','Set the machine recipe first, enable Alt-mode and connect the labeled input or output socket. Neighboring ordinary pipes connect in all four directions; underground pipes make controlled crossings. Different fluids need separate systems. Read the pipe GUI before flushing: flushing destroys the stored fluid and does not fix a wrongly connected layout.')],
 sources=['fluid','prototypes','version'],entities=['pipe','pipe-to-ground','storage-tank','pump'],related=['fluid-pumps','oil-processing'],experiment='Trace one valid fluid segment from tank to refinery. Identify the next pump and explain why the segment after it is separate.',diagram='fluid')

topic('fluid-pumps','Pumps, tanks, barrels and fluid wagons','Fluids and oil',
 'Choose the transport method and distinguish storage from transfer capacity.',[
 ('Pumps are powered one-way boundaries','A pump can move up to 1,200 fluid/s at the normal base setting. That is a maximum, not a promise: upstream availability, downstream fullness and conditions matter. An unpowered or disabled pump blocks flow. More pumps in series do not add up to more throughput; parallel routes can increase the transfer boundary’s capacity.'),
 ('Tanks expose reserves','A tank provides storage and a readable circuit quantity. Additional tanks delay a surplus problem but do not remove it. A tank holding 10,000 units can feed a 100 fluid/s net deficit for about 100 seconds. Count downstream requirements before choosing a reserve threshold.'),
 ('Barrels versus wagons','A barrel carries 50 fluid and needs filling, emptying and an empty-barrel return path. Steam cannot be barreled. A fluid wagon transports bulk fluid directly through powered pumps. In 2.1, valid wagon connectors include more alignments and curved positions; start with a simple straight station, use the visible connection, and check that the train is actually stopped for loading.')],
 sources=['pump','prototypes','version'],recipes=['barrel','water-barrel','empty-water-barrel'],entities=['pump','storage-tank','fluid-wagon'],related=['rail-loading','oil-balancing'],experiment='Place a pump between two tanks and reverse it. Then disable it with a condition. Predict which side can receive fluid in each case.',diagram='fluid')

topic('oil-extraction','Oil fields: yield, depletion and expansion','Fluids and oil',
 'An oil well’s percentage describes output rate, not a finite chest of crude.',[
 ('Read the well','A normal unmodified pumpjack at 100% yield produces 10 crude/s. Pumpjacks fit a specific well location and require electricity plus an available fluid output. Aggregate field yield is useful for planning, but blocked pipes can reduce actual flow to zero.'),
 ('Depletion does not mean disappearance','Crude wells gradually reduce to a minimum yield rather than exhausting like iron ore. Their floor depends on initial yield and the minimum rule. A familiar field can therefore keep producing while no longer feeding the refinery count you built around its initial rate.'),
 ('Respond to declining supply','Inspect actual crude production before adding refineries. Additional wells, speed improvements or another outpost can raise supply. A tank buffer helps ride out delivery gaps but hides a persistent deficit only temporarily. Keep petroleum production separate from your count of installed pumpjacks.')],
 sources=['pumpjack','prototypes'],entities=['pumpjack'],related=['oil-processing','outposts'],experiment='Compare the sum of producing pumpjack rates with refinery crude consumption. Use the same observation interval and verify that your crude tank is not silently draining.',diagram='oil')

topic('oil-processing','Basic oil, advanced oil and coal liquefaction','Fluids and oil',
 'Understand the recipe transition before expanding the refinery.',[
 ('Begin with one useful output','Basic oil processing consumes 100 crude in 5 recipe seconds and produces 45 petroleum gas. It does not need water in that recipe. Petroleum enables plastic and sulfur, so begin with a small working chemical line rather than waiting for a perfectly balanced advanced refinery.'),
 ('Advanced oil has three coupled outputs','Advanced oil consumes 100 crude and 50 water in 5 recipe seconds, producing 25 heavy oil, 45 light oil and 55 petroleum. All outputs must have room. A refinery can be full of petroleum demand yet stop because heavy oil is backed up. Draw all three output routes and label their destinations.'),
 ('Coal liquefaction is a distinct alternative','The base recipe consumes coal, steam and an initial heavy-oil input. Some of its heavy output must return to keep the process running. The gross heavy output is not all surplus. Do not confuse this recipe with the expansion’s simple coal liquefaction. Use it where coal logistics and local demand justify the extra handling.')],
 sources=['prototypes','oil'],recipes=['basic-oil-processing','advanced-oil-processing','coal-liquefaction'],entities=['oil-refinery','chemical-plant'],related=['oil-balancing','oil-products'],experiment='On an advanced refinery, deliberately block one output. Read the status and verify that the other two outputs stop too.',diagram='oil')

topic('oil-balancing','Cracking, lubricant reserves and refinery control','Fluids and oil',
 'A refinery needs an outlet for every co-product.',[
 ('Crack the excess in the useful direction','Heavy oil cracking consumes 40 heavy oil and 30 water to make 30 light oil in 2 recipe seconds. Light oil cracking consumes 30 light oil and 30 water to make 20 petroleum in 2 seconds. These are directional conversions; petroleum cannot simply be cracked back into lubricant.'),
 ('Derive a steady petroleum ratio','One speed-1 advanced refinery produces 5 heavy/s. Cracking that heavy requires 0.25 heavy-cracking plants and adds 3.75 light/s to its 9 light/s. Cracking all 12.75 light/s requires 0.85 light-cracking plants. Thus 20 refineries : 5 heavy crackers : 17 light crackers is a theoretical petroleum-only ratio, with no productivity, no lubricant or fuel diversion, and sufficient water.'),
 ('Control before copying','Keep heavy oil for lubricant, then enable heavy cracking only above a reserve threshold, such as 10,000 in the measured tank. Preserve light oil for rocket fuel if needed and crack its surplus. Thresholds are design choices. Add hysteresis if a simple threshold oscillates undesirably; check which tank or segment the circuit actually reads.')],
 sources=['prototypes','cookbook'],recipes=['heavy-oil-cracking','light-oil-cracking','lubricant'],related=['circuit-recipes','rocket-plan','oil-processing'],experiment='At stable demand, make a tank inventory trend nearly flat. Explain why a permanently rising heavy-oil level eventually stops petroleum production.',diagram='circuit')

topic('oil-products','Plastic, sulfur, acid, batteries, explosives and lubricant','Fluids and oil',
 'Chemistry feeds several independent late-game dependencies.',[
 ('Two branches from petroleum','Plastic consumes petroleum gas and coal; sulfur consumes petroleum and water. Sulfur becomes sulfuric acid with iron plates and water. Acid goes to batteries, processing units and uranium drills. These consumers compete even when the original refinery appears large.'),
 ('Track solid versus fluid intermediates','Sulfur and plastic are items moved by belts or inserters. Sulfuric acid and lubricant are fluids moved through the correct pipe ports. Batteries use iron, copper and acid. Electric engines need ordinary engines, electronic circuits and lubricant; robot frames then add batteries, steel and circuits.'),
 ('Defense shares the chemical plant','Explosives use coal, sulfur and water. Rockets, shells and other military products can increase demand on the same inputs as science. Give urgent defenses a controlled reserve instead of an unlimited chest that drains all sulfur. Choose a new production target from actual consumption, not only the size of the stored petroleum buffer.')],
 sources=['prototypes'],recipes=['plastic-bar','sulfur','sulfuric-acid','battery','explosives','lubricant','electric-engine-unit','flying-robot-frame'],related=['circuits-production','science-ratios','robot-networks'],experiment='Build a dependency sketch for one flying robot frame. Mark which ingredients need fluid-capable crafting and which can be delivered as ordinary items.',diagram='oil')

topic('science-progression','Research: unlocks, triggers, pack colors and the rocket route','Science',
 'Research units require a specified set of packs, not a pool of interchangeable colors.',[
 ('Early trigger checklist','Produce 50 iron plates for Steam power and 10 copper plates for Electronics; after both prerequisites, craft a lab for Automation science pack. Select Automation and supply its 10 red packs to powered labs. Oil processing triggers when crude is extracted after Oil gathering; uranium processing likewise needs its mining trigger. These gates explain why an expected recipe may be missing.'),
 ('Technology has two kinds of prerequisites','A technology can require earlier technologies and either lab research or a gameplay trigger. Read its record rather than assuming every early unlock consumes red science. For a lab technology, each research unit consumes the listed amounts of all required colors. One hundred units needing red and green means 100 of each when the amount is one.'),
 ('Follow the first-rocket chain','Automate red and green, then oil products and blue science. Production and utility science open the late rocket path; military science serves combat technologies and is not part of the base rocket-silo science set. Purple and yellow production can be developed in either order according to your factory’s needs.'),
 ('Research throughput has several limits','Labs need electricity, the active technology and all required packs. Faster labs do not create missing packs. Lab productivity stretches pack value; research speed changes how quickly labs can consume them. A science production graph measures item output, which is not identical to effective research progress under productivity.')],
 sources=['research','prototypes'],recipes=['automation-science-pack','logistic-science-pack','military-science-pack','chemical-science-pack','production-science-pack','utility-science-pack'],related=['science-ratios','rocket-plan'],experiment='Open the technology reference for rocket silo. Trace its prerequisite tree and distinguish technology dependencies from the immediate list of science colors.',diagram='science')

topic('science-ratios','Science ratios: packs per craft and machines per minute','Science',
 'Recipe output counts matter as much as crafting time.',[
 ('The six baseline rates','At crafting speed 1, red makes one pack in 5 seconds; green one in 6; military two in 10; blue two in 24; purple three in 21; yellow three in 21. These imply assembler counts proportional to 5 : 6 : 5 : 12 : 7 : 7 when all machine speeds and bonuses match.'),
 ('Choose an achievable target','For 30 packs/min using assembler 2 at speed 0.75, ideal counts are 3⅓ red, 4 green, 3⅓ military if needed, 8 blue, 4⅔ purple and 4⅔ yellow. Round up for installed machines. Red/green can start much smaller; a steady stream is sufficient for progressing rather than racing.'),
 ('Budget the intermediates','Blue science consumes engines, advanced circuits and sulfur. Purple consumes rails, electric furnaces and productivity modules; yellow consumes processing units, low-density structures and flying robot frames. These chains share steel, circuits, copper and oil products. Use the recipe calculator on each output and work backward. A required module ingredient is not the same as a module installed in the science assembler.')],
 sources=['prototypes'],related=['ratios','circuits-production','oil-products'],experiment='Set blue science to 30/min in the calculator. Explain why eight assembler 2s are needed even though each craft yields two packs.',diagram='science')

topic('pollution','Pollution, enemy attacks and evolution are different systems','Defense and environment',
 'Reduce emissions, watch the cloud and understand what actually changes enemy strength.',[
 ('The cloud creates attack pressure','Pollution spreads over map chunks and can be absorbed by terrain, trees and nests. Nests consuming pollution can send units into attack groups. The pollution overlay and production screen help reveal pressure outside your visible factory. Pollution is not stopped by a wall.'),
 ('Evolution has separate causes','Enemy evolution responds to elapsed time, pollution produced and destroyed spawners under the world’s settings. Absorbing pollution in trees does not undo the evolution contribution of producing it. Killing individual biters is different from destroying their spawners. Clearing a threatening nest can reduce local attacks while contributing to evolution.'),
 ('Choose a response with tradeoffs','Efficiency modules can lower electricity and direct machine emissions. Cleaner generation can reduce boiler pollution. Defenses let you continue operating under pressure; selective nest clearing buys local room; scouting detects expansion. Trees are a limited environmental buffer, not a permanent guarantee that the factory is safe.')],
 sources=['pollution','combat','prototypes'],related=['defense-design','modules-math','world'],experiment='Compare pollution production and absorption graphs, then find a nest inside the cloud. Explain why low pollution at the factory edge does not prove no distant nest is absorbing it.',diagram='defense')

topic('defense-design','Layered defense: guns, flames, lasers, repairs and resupply','Defense and environment',
 'A defense is a supply system with a combat front attached.',[
 ('Make the early loop reliable','Gun turrets need ammunition; walls buy time but do no damage. Use overlapping coverage, a replenishment route and access for repairs. Leave enough space for inserters, poles and future upgrades. Research damage and firing improvements when enemy resistance makes your current ammunition ineffective.'),
 ('Match the weapon to its dependency','Flamethrower turrets need fluid fuel and time for their damage to take effect; guns can handle close stragglers. Lasers need substantial power during attacks and do not consume magazines. Mixing weapon roles avoids relying on one vulnerable supply chain, but a small well-fed gun line is preferable to an unpowered elaborate perimeter.'),
 ('Observe actual damage','Repair packs and construction robots can maintain walls and replace destroyed entities when materials and coverage exist. Robots may fly into danger during combat; losing them is a cost to monitor. New pollution outposts and enemy expansion change the threatened perimeter. Treat an ammunition or power shortage as a factory problem and inspect the supply before adding more empty turrets.')],
 sources=['prototypes','combat'],recipes=['firearm-magazine','piercing-rounds-magazine','uranium-rounds-magazine','gun-turret','laser-turret','flamethrower-turret','repair-pack'],related=['pollution','outposts','electricity'],experiment='Watch one defended attack and identify which supply determines sustained protection: magazines, fluid fuel, charging power, repair stock or robot replacement.',diagram='defense')

topic('outposts','Outposts: depletion, scouting, power and delivery','Design and scale',
 'Replace a declining deposit before its buffer is empty.',[
 ('Plan the next source early','Track active drill coverage and ore delivery. A patch can retain ore in inaccessible corners while most drills have depleted. Scout for the next iron, copper, coal or oil source before the main bus is starved. An outpost needs extraction, power, transport, defense and a way to maintain it.'),
 ('Choose a transport boundary','Short belts are simple for nearby material. Rail handles distant bulk flow and can combine many sources with named stations. Pumped pipelines serve fluids within valid segments. Compare the complete route and maintenance burden rather than choosing transport from distance alone.'),
 ('Commission and retire safely','Bring poles, drills, transport pieces, repair materials and fuel. Test a full delivery into an active consumer, not just an output chest. At retirement, stop new dispatches, allow existing reservations to finish, remove unused equipment and keep defenses as needed. A train limit change does not instantly divert trains already en route.')],
 sources=['prototypes','trains'],related=['rail-loading','pollution','scaling'],experiment='Build an outpost checklist and do one delivery cycle end to end. Include the return trip, train fuel, station limit and what happens when the receiving buffer fills.',diagram='train')

topic('rail-foundations','Rail fundamentals: route, direction, stops and train length','Railways',
 'A connected drawing is not always a usable route.',[
 ('Build a route the locomotive can follow','Automatic trains need a forward-facing locomotive for the direction of travel. A loop allows one forward locomotive; a shuttle needs powered locomotives facing both directions. Crossing two rails does not itself create a turning connection. Rails follow a two-tile placement grid.'),
 ('Stop and signal orientation','Stops belong on the right from the arriving train’s viewpoint. Signals also apply on the right; a signal only on the left makes that direction unusable in automatic mode. For bidirectional track, opposing signals must be paired. Two separate one-way tracks simplify multi-train learning.'),
 ('Choose a maximum train length','All platforms, waiting bays, exit blocks and approaches must fit the intended train. A train’s tail can obstruct a junction while its locomotive is already well beyond it. Design stations off the mainline, use clear names and provide regular fueling. Manual driving ignores signal protection; it does not demonstrate that automatic routing is valid.')],
 sources=['railway','prototypes'],entities=['locomotive','cargo-wagon','train-stop'],related=['rail-blocks','rail-loading'],experiment='Run one fueled train between two stops with no shared traffic. Verify a complete automatic cycle before adding a second train or an intersection.',diagram='train')

topic('rail-blocks','Rail blocks, reservations and the four signal colors','Railways',
 'Signals divide connected track into protected regions; they do not attach to a particular train.',[
 ('Read the block boundary','Holding a signal shows colored track blocks. The overlay colors identify regions; they are unrelated to the signal lamp colors. Stops do not divide blocks. Crossings that remain the same block conflict even if the routes look visually separate.'),
 ('Read a regular signal','Green means the following block is available; yellow means reserved; red means occupied or unavailable. A long train can occupy several blocks. Signals protect automatic movement, and a train can reserve ahead before it physically enters.'),
 ('Read a chain signal along the chosen path','A chain considers downstream exit availability as well as the immediate block. Blue means some routes are available and some blocked, so the approaching train’s route matters. Place chains before and within crossing conflicts and ordinary signals at exits where a complete train can wait clear. A blinking signal indicates an invalid block separation or placement, not ordinary busy traffic.')],
 sources=['rail','chain','prototypes'],related=['rail-deadlocks','rail-foundations'],experiment='Hold a signal at your junction. Identify each region, then trace whether two trains on the intended nonconflicting routes actually occupy distinct blocks.',diagram='signals')

topic('rail-deadlocks','Junction design and diagnosing deadlocks','Railways',
 'Separate conflicting routes and provide space for every waiting train.',[
 ('Why chain in, rail out is only a start','The mnemonic prevents a train from waiting in a simple intersection, but complex junctions also need internal conflict separation. An ordinary exit signal is useful only if the following waiting block fits the entire train. Otherwise its tail can still obstruct the crossing.'),
 ('Two different kinds of failure','No path is a routing or destination problem: broken rail, forbidden direction, wrong stop side or missing named destination. A train waiting at red has a route but cannot enter a block. Destination full means the named station capacity is currently unavailable. Diagnose these statuses separately.'),
 ('Break the dependency cycle','In a deadlock, trace each waiting train to the block or station it needs. A ring of trains each occupying the next train’s required space cannot fix itself just by adding more locomotives. Temporarily remove or redirect one train in the experiment save, then fix the structural cause: short exits, inadequate waiting bays, opposing single-track access or overcommitted stations.')],
 sources=['rail','chain','trains'],related=['rail-dispatch','rail-blocks'],experiment='Draw the waiting dependency as A needs B’s block, B needs C’s, C needs A’s. Identify one safe extra waiting space that would have prevented the cycle.',diagram='signals')

topic('rail-loading','Cargo and fluid stations: loading, buffers and wait conditions','Railways',
 'A useful train service needs both station handling and a working schedule.',[
 ('Align and inspect','Place a stop, hover it to inspect wagon positions, then position inserters or pumps. Cargo wagon filters and slot limits can constrain loading. A locomotive fuel slot is not cargo storage. In automatic mode, loading equipment needs the train stopped appropriately, not just halted at a signal.'),
 ('Buffer for intermittent arrival','Station chests let belts load steadily while a train is away and unload rapidly when it arrives. Balance the actual wagon draw so one full buffer does not coexist with another empty wagon. A large chest reserve smooths arrival timing but does not fix long-run insufficient trains or mining.'),
 ('Use conditions that can finish','A simple single-item route uses full cargo at the source and empty cargo at the destination. A mixed train may never become full if one requested ingredient is absent, so use item counts and sensible inactivity or time conditions. Understand AND versus OR: full cargo OR inactivity lets a partially loaded train leave; full cargo AND inactivity requires both. Fluid wagons need powered pumps, correct direction and compatible fluid.')],
 sources=['railway','prototypes'],entities=['cargo-wagon','fluid-wagon','pump'],related=['rail-dispatch','rail-throughput','fluid-pumps'],experiment='Remove one requested item from a mixed loading station. Check whether the schedule can still finish and whether that behavior matches the station’s purpose.',diagram='train')

topic('rail-dispatch','Train limits, priorities, groups and schedule interrupts','Railways',
 'Control where trains are allowed to go before increasing fleet size.',[
 ('Limits allocate destination capacity','A limit counts trains reserving a station, including a train at it. Start with limit 1 when there is no safe queue. Reducing the limit does not cancel already committed trains. A disabled stop behaves like limit zero for new dispatch, rather than simply being skipped.'),
 ('Priorities and groups','Among available same-name stops, higher priority is preferred; the base priority range is 0–255. Priority does not make room in a full station. Train groups share schedules so an edit can affect multiple trains; use distinct group names when behavior should differ.'),
 ('Interrupts express exceptional work','An interrupt can insert temporary destinations when its condition is satisfied, such as low fuel sending a train to refuel. Named interrupts can be shared. First verify a fixed two-stop route; then add one interrupt and test its trigger, destination capacity and completion. Generic cargo interrupts require consistent station naming and correct wildcard use, so test them with one item before pooling a fleet.')],
 sources=['trains','train-improvements','generic-trains'],related=['rail-throughput','circuit-recipes'],experiment='Make two same-name loading stops, both limit 1. Observe reservations; change one priority and check that it influences new dispatch without instantly rerouting committed trains.',diagram='train')

topic('rail-throughput','Rail throughput, buffers and fleet sizing','Railways',
 'Cargo per cycle and cycle time predict a service’s ideal delivery rate.',[
 ('Measure the complete cycle','Average rate per train = delivered items per trip ÷ round-trip seconds, including waiting, loading and unloading. For N equivalent trains, multiply by N only while routes and stations still support it. More trains can increase queues and lengthen the cycle.'),
 ('Use item stack sizes','A cargo wagon has inventory slots, so capacity depends on the transported item’s stack size and any filters or limits. A plate, ore and circuit train of the same length can carry different item counts. Fluid wagon capacity is a volume, not a stack count. Use the extracted item and wagon records for your version.'),
 ('Give buffers a purpose','A receiver consuming 30 items/s through a 120-second delivery gap needs at least 3,600 items of usable reserve, plus margin. That reserve must be accessible to its unload belts, not merely present in a distant chest. Design stations and their downstream belts for sustained demand as well as burst unloading.')],
 sources=['prototypes'],related=['flow','rail-loading','scaling'],experiment='Time five complete cycles and measure delivered cargo. Compare the observed items/min with the ideal capacity calculation, then identify the largest source of delay.',diagram='train')

topic('robot-networks','Construction and logistics: networks, ranges and personal ports','Robotics',
 'Construction jobs and item delivery use different robots and coverage rules.',[
 ('Two jobs, two areas','Construction robots place ghosts, repair and remove entities. Logistic robots carry requested items between eligible inventories. A roboport provides orange 50×50 logistics coverage and green 110×110 construction coverage. Adjacent orange areas join networks; merely overlapping green areas do not share an item inventory.'),
 ('A task needs a complete supply path','A ghost needs the exact item, construction coverage, an available construction robot and enough power. An ordinary wooden chest does not offer its contents to robots. A requester outside orange coverage cannot be served merely because construction bots can build its chest there.'),
 ('Personal construction is separate','A personal roboport uses the character or vehicle inventory, its own equipment power and construction robots carried there. It does not merge with a stationary network. Logistic robots serve personal inventory requests from the surrounding stationary network. These are two different systems even when both operate around the same player.')],
 sources=['roboport','logistics','prototypes'],entities=['roboport','construction-robot','logistic-robot'],recipes=['construction-robot','logistic-robot','roboport'],related=['robot-chests','robot-throughput','equipment'],experiment='Place two ports so green areas overlap but orange areas do not. Try building from a provider in only one network and explain which ghosts each network can supply.',diagram='bots')

topic('robot-chests','The five logistic chests and request groups','Robotics',
 'Use chest behavior deliberately to avoid moving items in circles.',[
 ('Offer, store, request or push','Passive provider chests offer output when needed. Storage chests accept returned items and can offer them again; filters help organize them. Requester chests ask for specified items. Buffer chests request and offer items for local staging. Active provider chests force their contents out, so they require available destinations and are easy to overuse.'),
 ('Start with a simple path','Put assembler output into a passive provider, request a small amount at the consumer, and provide storage for returns and deconstruction. A requester normally does not serve as a provider for unrelated construction. When using buffers, inspect the requester option for requesting from buffer chests; an unintended eligibility setting can make a visible stock unavailable.'),
 ('Requests are configuration, not production','Named request groups share configuration. Editing one group can affect other users of the same name. A request minimum cannot conjure an unavailable item, and excessive requested reserves tie up materials. Configure excess-item handling with care so the chest or character does not repeatedly return what another request is trying to supply.')],
 sources=['logistics','constant','prototypes'],entities=['passive-provider-chest','active-provider-chest','storage-chest','requester-chest','buffer-chest'],related=['robot-networks','robot-throughput'],experiment='Trace one item from passive provider to requester, then deconstruct a building into storage. Confirm which chests supply the item when it is needed again.',diagram='bots')

topic('robot-throughput','Robot throughput: distance, cargo, charging and shape','Robotics',
 'More robots help only when the rest of the network can support them.',[
 ('A cycle has travel and service time','Approximate transport capacity as robot count × cargo per trip ÷ average trip-cycle time. The cycle includes flight, charging and delays. Speed and cargo research change the calculation. Short local trips may support dense production; a huge network with long crossings can consume many robots for modest delivered flow.'),
 ('Charging is infrastructure','The pinned base data specifies four charging offsets and 500 kW per charging slot, plus the port’s 50 kW usage. Adding robots without charging locations can lengthen the queue. A large internal battery does not mean the port can recharge indefinitely without grid supply. Watch actual charge queues and the electrical network.'),
 ('Shape routes sensibly','Robots fly direct paths, including across gaps or hostile territory between distant network endpoints. A concave network may create poor charging routes. Separate local networks and use trains between them when that simplifies traffic and maintenance. Do not assume construction coverage forms a safe flight corridor.')],
 sources=['prototypes','roboport'],related=['robot-networks','rail-throughput','electricity'],experiment='Keep total cargo demand constant, move the provider farther away and observe the change in busy robots and charging queues. Compare adding robots with adding a well-placed port.',diagram='bots')

topic('blueprint-workflow','Blueprints, library, parameterization and recovery','Building tools',
 'Save a proven design and understand what a placement order actually preserves.',[
 ('From working block to reusable plan','Test a small design before saving it. Ctrl+C creates a temporary copy; Ctrl+V selects the paste tool. A permanent blueprint can carry a name, icons and description and live in a book or library. A placed blueprint creates ghosts; material, coverage and construction capacity still determine whether it becomes real.'),
 ('Parameterize behavior intentionally','Parameters can let one design request a chosen item or configure different recipes and constants at placement. Start with a simple constant or recipe parameter, label it clearly and test every related setting. A visually identical configuration can contain a wrong circuit threshold or request because a parameter was not applied where expected.'),
 ('Make reversibility concrete','Keep a known-good copy before editing a library design. Undo can restore ghosts and cancel some orders; it does not reverse all consequences or restore mined terrain. Inspect rotations, fluid ports, grid alignment, modules, train settings and filters before stamping a large area. Export a blueprint string as a backup distinct from a world save.')],
 sources=['blueprints','prototypes'],related=['planner-tools','backups'],experiment='Copy a four-machine block, rotate it, and identify every input and output before construction. Check that the copied recipes and conditions match your intended use.',diagram='blueprint')

topic('planner-tools','Deconstruction, upgrade planners, ghosts and force building','Building tools',
 'A planner selects a job; the robots, items and filters determine its result.',[
 ('Filter before clearing','A deconstruction planner can select only certain entities or terrain. Use a stored filtered planner for trees and rocks so a clearing sweep does not mark factory equipment. Shift-drag cancels pending deconstruction in the selected area. Read the highlighted selection before releasing the mouse.'),
 ('Upgrade is a mapping','An upgrade planner can map one compatible entity or module to another; it can also downgrade. Its geometry and supported replacement rules matter. The job requires replacement items and construction service. A faster belt replacement does not increase upstream supply or ensure its underground and splitter segments were upgraded too.'),
 ('Force is not immediate construction','Ghost and force-build tools can mark obstructions and terrain work, including prerequisites that robots must finish before machines are placed. Super-force can also mark existing factory entities for removal. Use a small test area and inspect the pending changes. Q cancels the held planning tool; it is not an undo of an order already issued.')],
 sources=['deconstruction','upgrade','prototypes'],related=['blueprint-workflow','robot-networks'],experiment='Mark one belt for deconstruction, cancel with Shift and confirm it resumes. Then make a filtered upgrade and verify that only the chosen entity type changes.',diagram='blueprint')

topic('signals','Circuit signals: values, wire colors and read modes','Circuits',
 'A wire carries numbers about items, not the items themselves.',[
 ('Signal identity and addition','An iron-plate signal with value 200 is a number named iron plate. It does not contain 200 plates. Signals broadcast onto the same connected color network add. Red and green are separate networks; a receiver selecting both may sum their values. Missing signals act as zero for ordinary numeric comparisons.'),
 ('Read the intended inventory','A chest can broadcast its contents, a tank its fluid, and a belt its observed items. Pulse mode emits an event for a tick; hold mode maintains a reading. A single belt tile’s hold reading and an entire belt line’s hold reading answer different questions. Count each physical inventory once to avoid double-counting your supply.'),
 ('Device configuration matters','Select the sender’s output wire color and the receiver’s input color. A wire on a pole carries circuit signals only because the pole is being used as a circuit junction; it is not the pole’s electric copper connection. Most signal values are signed 32-bit integers, so overflowing a large calculation can change the sign.')],
 sources=['circuit','prototypes'],related=['combinators','circuit-recipes'],experiment='Wire two chests holding 100 plates each to one lamp input. Observe a plate signal of 200, then disconnect one chest and explain the change.',diagram='circuit')

topic('combinators','Constant, arithmetic, decider and selector combinators','Circuits',
 'Choose a device by the operation it performs.',[
 ('Constant and arithmetic','A constant combinator broadcasts configuration values and does not require electrical power. An arithmetic combinator calculates an operation on selected inputs. Each can apply the same calculation independently to incoming signals. Integer division truncates toward zero: 19/10 gives 1, and −19/10 gives −1. Use the sign intentionally when calculating shortages. Other operations include subtraction, multiplication, modulo, exponentiation, bit shifts and bitwise AND, OR and XOR.'),
 ('Decider','A decider tests comparisons, combines conditions with AND/OR and emits configured normal or else outputs. AND has higher precedence than OR. Output a constant one for a Boolean flag, or pass an input count when the quantity itself matters. Verify that you selected the output signal you need, rather than assuming the condition’s signal is automatically forwarded.'),
 ('Selector','In the base game, selector uses include choosing sorted input positions, counting signal types, selecting random inputs, obtaining item stack size and reading time. The index starts at zero. Do not confuse counting distinct signals with adding their values. Expansion-specific quality and orbital modes do not belong to the base-game production route.')],
 sources=['arithmetic','decider','selector','constant','prototypes'],entities=['constant-combinator','arithmetic-combinator','decider-combinator','selector-combinator'],related=['circuit-timing','circuit-recipes'],experiment='Use a constant input of iron = 19. Divide by 10 into signal A, then test A ≥ 2 in a decider. Predict the result before inspecting the output.',diagram='circuit')

topic('circuit-timing','Timing, feedback, latches and Boolean reasoning','Circuits',
 'A feedback circuit is a small state machine; its wiring and update delay define it.',[
 ('One tick is a real dependency','Arithmetic and decider combinators add a one-tick delay before their outputs can feed the next stage. At the nominal simulation rate there are 60 ticks per game second. A chain of several devices responds later than a direct wire. Pulse signals can disappear before a differently delayed path is ready.'),
 ('Combinational versus stored state','A simple threshold is a direct function of current input. A feedback loop can remember an earlier state. To make hysteresis, define a lower threshold that turns a process on and a higher threshold that turns it off, retaining the state between them. Specify the initial state and which action wins if conflicting inputs occur.'),
 ('Boolean tools and missing inputs','AND means all required conditions, OR means at least one. Each applies per signal, Anything asks for a match, and Everything asks whether all relevant signals match. With no input signals, Everything is true and Anything is false; Each has no input signals to process. Test this case rather than treating it like a chest that always contains a zero-valued item. Keep input and feedback networks separate unless addition is intentional.')],
 sources=['decider','arithmetic','logic','time'],related=['signals','circuit-recipes'],experiment='Write a four-row truth table for two Boolean inputs. For a memory circuit, also write how previous state changes the result when both inputs are false.',diagram='circuit')

topic('circuit-recipes','Useful circuits: stock limit, oil reserve, alarm and station limit','Circuits',
 'Begin with direct measurements and add combinators only when they solve a defined need.',[
 ('Limit stock and protect oil','Wire a product chest to its output inserter; enable that inserter while the product count is below your target. Its hand may overshoot the target. For oil, wire the relevant heavy-oil tank to the pump feeding heavy cracking and enable above a reserve. Confirm the tank’s output color and pump’s input color before debugging the threshold.'),
 ('Make an actionable alarm','Wire an ammunition reserve to a programmable speaker and set a low-stock condition with a recognizable alert. Choose a threshold that leaves time for replenishment. An alarm measuring a central reserve cannot guarantee a distant turret’s belt is intact; measure the place whose failure you want to detect.'),
 ('Advertise complete train loads','Sum only a loading station’s available cargo. Divide by the intended items per train, output a train-limit signal and cap it to the number of safe waiting positions. For an unloading station, calculate free capacity instead. Account for already reserved trains and the throughput of the unload belts. Begin with a fixed limit and test before adding dynamic dispatch.')],
 sources=['cookbook','trains','prototypes'],related=['signals','rail-dispatch','oil-balancing'],experiment='Set an inserter target of 100 gears. Watch the final count, explain any overshoot from its hand, then decide whether the application requires tighter control.',diagram='circuit')

topic('modules-math','Modules: speed, productivity, energy and pollution','Advanced production',
 'Compare throughput, input efficiency and energy per useful output separately.',[
 ('Three normal base families','Speed modules trade more energy for faster processing. Productivity modules add extra eligible output while usually slowing the machine and increasing energy use. Efficiency modules lower energy use. A machine must accept the effect and the recipe must permit productivity. Inspect the exact recipe flag rather than putting productivity into every building.'),
 ('Effects combine before the rate calculation','For ordinary crafting, effective speed = base speed × max(0.2, 1 + total speed modifier). Add the allowed productivity bonuses for the output calculation. Machine energy demand and pollution also have their own modifiers and floors. Productivity’s direct pollution modifier and increased energy usage can both matter; clean electrical generation does not remove a machine’s own emissions.'),
 ('A worked tradeoff','An assembler 3 at speed 1.25 with four normal productivity module 3s has −60% speed and +40% productivity before beacons: speed 0.5. On a 0.5-second electronic-circuit recipe it performs one normal craft/s and averages 1.4 circuits/s while using one recipe’s ingredients per second. This saves input per output, but produces less per second than the same bare assembler’s 2.5 circuits/s.')],
 sources=['prototypes','modules'],recipes=['speed-module','speed-module-2','speed-module-3','productivity-module','productivity-module-2','productivity-module-3','efficiency-module','efficiency-module-2','efficiency-module-3'],related=['beacon-math','ratios'],experiment='For the worked example, calculate iron per circuit as 1/1.4. Compare material efficiency with throughput rather than calling one setup universally better.',diagram='assemble')

topic('beacon-math','Beacons and diminishing returns','Advanced production',
 'Use the current transmission model instead of old fixed-per-beacon ratios.',[
 ('What a beacon contributes','Normal base beacons have two module slots and distribution efficiency 1.5. They transmit compatible module effects to eligible nearby machines. Productivity modules cannot be used in a beacon. A beacon consumes power even when the machines it affects are idle.'),
 ('Count coverage per machine','For n identical normal beacons affecting one machine, a useful expression is 1.5/√n transmission per beacon. Total transmitted identical effects therefore scale approximately as 1.5√n, not linearly with n. The game’s prototype uses a profile with rounded values; use the machine UI for the exact resulting speed.'),
 ('Design for the full cost','Beacon modules need ingredients and energy; machines need sufficient ingredient delivery and product removal to use the speed. One beacon serving several continuously active machines can be economical, while surrounding an idle assembler may just waste power. Count how many beacons affect each machine, not the total number built in the block.')],
 sources=['beacon','prototypes'],entities=['beacon'],related=['modules-math','scaling'],experiment='Compare one and four normal beacons with the same speed modules. Predict the total effect multiplier, then confirm the displayed machine speed and its input demand.',diagram='assemble')

topic('uranium','Uranium processing, probability and Kovarex net gain','Nuclear',
 'A random processing line needs buffers; catalyst circulation is not net production.',[
 ('Mine and separate','Uranium drills need sulfuric acid and output ore. The baseline centrifuge recipe processes 10 ore in 12 seconds. Its mutually exclusive outputs have expected probabilities 0.007 U-235 and 0.993 U-238 per craft. An average yield is not a schedule: unlucky stretches can be much longer than the mean interval.'),
 ('Fuel does not require Kovarex','A uranium fuel cell craft consumes 1 U-235, 19 U-238 and 10 iron plates to make 10 cells. A modest initial reactor can run from ordinary processing if supply and reserves are adequate. Preserve enough U-235 for future enrichment rather than allowing an unlimited fuel chest to consume all of it.'),
 ('Understand enrichment','Kovarex consumes 40 U-235 and 5 U-238, returning 41 U-235 and 2 U-238 before bonuses. Its net is +1 U-235 and −3 U-238 per craft. The returned 40 U-235 is working inventory needed to keep the next craft running. Output handling should preserve that circulation before exporting surplus. Productivity treatment of returned catalysts requires the recipe’s ignored-output rules.')],
 sources=['prototypes'],recipes=['uranium-processing','uranium-fuel-cell','kovarex-enrichment-process','nuclear-fuel-reprocessing'],entities=['centrifuge'],related=['nuclear-heat','ratios'],experiment='For 1,000 ordinary processing crafts, compute expected U-235 as 7. Explain why you cannot promise exactly seven in a particular run.',diagram='ore')

topic('nuclear-heat','Nuclear heat, exchangers, turbines and fuel control','Nuclear',
 'Reactor heat must pass through several different capacity limits before it becomes electricity.',[
 ('Heat source and neighbor bonus','A lone reactor produces 40 MW while burning a cell. Each valid active neighboring reactor adds its neighbor bonus; a pair can make 160 MW total, and a 2×2 block 480 MW total. Fuel cells burn for their cycle even when electrical demand is low, so a large reactor can waste useful potential unless energy is stored or fuel loading is controlled.'),
 ('Convert heat into usable steam','Heat pipes transfer heat to exchangers. An exchanger needs sufficient temperature and water and transfers up to 10 MW. A turbine converts high-temperature steam to electricity. A 40 MW isolated reactor therefore needs four exchangers and enough turbine capacity; seven ordinary turbines provide a small margin over 40 MW at 500°C steam. More turbines cannot fix cold exchangers or empty water inputs.'),
 ('Start simple, then add control','Warm-up takes time. Keep pipe routes reasonable and inspect temperatures along the route. Remove used cells and preserve electric power for any essential pumps. Modern reactors can be wired for readings, which can simplify fuel control, but the first working plant does not require a complex tank-and-latch design. Backup power protects startup and handling.')],
 sources=['prototypes','nuclear'],entities=['nuclear-reactor','heat-exchanger','heat-pipe','steam-turbine'],related=['uranium','electricity','circuit-timing'],experiment='Trace one reactor to one turbine and name the unit at every boundary: fuel items, heat energy, water volume, steam volume and electrical power.',diagram='power')

topic('rocket-plan','The base-game rocket: exact ingredients and a useful first launch','Rocket and beyond',
 'Separate silo construction, rocket assembly, payload and landing-pad requirements.',[
 ('Four separate jobs','Research the silo, construct and power it, provide the rocket-part ingredients, then load an accepted payload and provide a cargo landing pad. A rocket uses 100 parts. Before productivity, each part consumes 10 processing units, 10 low-density structures and 10 rocket fuel: 1,000 of each for the rocket itself.'),
 ('The science payload','A satellite additionally needs 100 low-density structures, 100 solar panels, 100 accumulators, 5 radars, 100 processing units and 50 rocket fuel. It returns 1,000 space science packs to the cargo landing pad. The satellite’s circuit ingredient is processing units, not advanced circuits. Only one planetary landing pad can be placed in this base-game context.'),
 ('Victory and space science differ','A successful first base-game launch triggers victory. A satellite is the useful payload for science; raw fish is also an accepted payload for its special achievement and does not return space science. An empty payload is not a working launch plan. Do not substitute the much cheaper Space Age rocket-part recipe or assume the engineer leaves on a base-game rocket.')],
 sources=['prototypes','rocket','silo-script'],recipes=['rocket-silo','rocket-part','satellite','cargo-landing-pad'],entities=['rocket-silo','cargo-landing-pad'],related=['rocket-budget','after-launch'],experiment='Use the rocket budget calculator to distinguish one-time structures from recurring launch ingredients. Verify the recipe totals in the silo before enabling repeat launches.',diagram='rocket')

topic('rocket-budget','Rocket budgeting and productivity','Rocket and beyond',
 'A useful bill of materials must state its boundary and assumptions.',[
 ('Immediate components are auditable','For one satellite launch without productivity, combine 100 rocket-part crafts with one satellite craft: 1,100 low-density structures, 1,100 processing units and 1,050 rocket fuel, plus the satellite’s panels, accumulators and radars. The silo, landing pad and enabling research are separate costs. The calculator lets you include the one-time structures explicitly.'),
 ('Productivity reduces part crafts','If an otherwise valid silo supplies +40% productivity, 100 parts need 100/1.4 normal crafts on average. For a single rocket starting with an empty productivity bar, whole crafts and bonus timing matter; use the in-game part count rather than promising a fractional craft. Other production stages can also have productivity, which compounds through the chain.'),
 ('Raw totals need a complete process model','Oil has multiple products and alternatives, furnaces need energy, and a whole factory also consumes construction materials and science. A naive recursive sum can double-count shared oil products or ignore catalyst returns. This manual reports direct ingredient budgets and recipe-by-recipe rates; it does not label them a complete optimized ore-to-rocket bill of materials.')],
 sources=['prototypes','recipe-api'],related=['rocket-plan','oil-balancing','modules-math'],experiment='Turn one rocket-part recipe into 100 crafts and add the satellite recipe component by component. Explain why this result is not yet a raw-ore budget.',diagram='rocket')

topic('after-launch','After the rocket: infinite research and sustained production','Rocket and beyond',
 'A first launch proves a chain works; repeated launches test whether it is sustainable.',[
 ('Move from a milestone to a rate','Choose a recurring target: launches/hour, science packs/min or a construction supply rate. Supply the landing pad’s space science to labs along with the other packs required by the chosen infinite technology. Automating launches still needs a complete satellite and a way to clear returned science.'),
 ('Test a long interval','A factory can launch from stored buffers even while current production is insufficient. Run long enough for buffers, ore depletion, train scheduling and fuel use to reveal persistent deficits. Record which material falls first, then expand that chain rather than increasing everything at once.'),
 ('Explore advanced systems by purpose','Mining productivity can extend resource supply; stronger combat research supports expansion; robot speed changes local logistics; modules and beacons change material and power economics. Set an explicit problem before optimizing it. A larger factory is optional: a reliable first-rocket base is a valid completed learning goal.')],
 sources=['prototypes','statistics'],related=['scaling','performance','rocket-plan'],experiment='Track one full hour of science production and launch activity after reserves stabilize. Compare the sustainable rate with your initial burst rate.',diagram='goal')

topic('equipment','Armor grids, personal robots, shields and portable power','Player tools',
 'Equipment needs both grid space and a working energy budget.',[
 ('Install the right kind of upgrade','Modular and power armor provide equipment grids. Right-click the armor to configure it. Manufacturing modules such as productivity modules do not belong in this grid. Equipment can provide power, storage, movement, shielding, construction control or other utility, depending on the item.'),
 ('Generation and storage are separate','Portable solar and a portable fission reactor generate energy. Personal batteries store it; a battery by itself is not a power source. Shields, exoskeletons and personal roboports can compete for that energy. An inactive personal roboport may be disabled, out of power, missing construction robots, missing material or outside its build range.'),
 ('Build a useful construction kit','Carry construction robots, building items and repair packs. A personal port uses your carried inventory rather than silently requesting everything from a distant warehouse. Learn its toggle so robots do not deploy into combat unintentionally. Check the technology record before assuming an equipment item is available at the first modular-armor stage.')],
 sources=['equipment','armor','prototypes'],recipes=['modular-armor','power-armor','power-armor-mk2','personal-roboport-equipment','solar-panel-equipment','fission-reactor-equipment'],related=['robot-networks','vehicles'],experiment='Build a personal construction kit with generation, storage and a roboport. Remove only generation and explain why it can work briefly before the battery empties.',diagram='bots')

topic('vehicles','Car, tank, Spidertron, artillery and combat tools','Player tools',
 'Use transport and combat tools according to their logistics and control needs.',[
 ('Vehicles solve different problems','A car offers early movement and trunk storage. A tank is more robust, has several weapon types and an equipment grid, and can be driven remotely where you can observe it. Bring fuel, the right ammunition and repair supplies. Getting stuck among obstacles can turn armor into a liability.'),
 ('Spidertron is a mobile project','Spidertron travels over obstacles, has an equipment grid, logistics requests and remote orders, and does not consume vehicle fuel for walking. Construction equipment lets it serve as a mobile builder. Queue and inspect waypoints before sending it through enemy territory. Automatic targeting can spend ammunition or initiate combat when that was not your intended task.'),
 ('Combat has a supply and damage model','Match weapon ammunition to the weapon; bring armor and an escape route. Damage bonuses and enemy resistances affect effectiveness. Artillery attacks distant structures and can provoke a large response, so prepare perimeter defenses and shell resupply before firing. Capsules, mines and combat robots are situational tools, not prerequisites for the first rocket.')],
 sources=['tank','spidertron','prototypes'],recipes=['car','tank','spidertron','artillery-turret','artillery-shell','land-mine','defender-capsule','poison-capsule'],related=['defense-design','equipment'],experiment='Before a remote tank trip, list its visibility, fuel, ammunition, equipment power, repair and return-route requirements. Test the route in a safe area.',diagram='defense')

topic('statistics','Statistics: distinguish a real bottleneck from a buffered snapshot','Analysis',
 'Observe the same system over a useful interval and interpret the graph’s units.',[
 ('Choose the measurement window','The production screen has item, fluid and other graphs over selectable intervals. A short window reveals immediate response; a longer one reveals average supply and consumption. Sparse production looks noisy over a few seconds. Compare before and after changes using the same window and workload.'),
 ('Read inventory trend too','Produced minus consumed explains net stock change only within the statistic’s counting rules and chosen scope. Construction, hand-held inventories and transport stock can complicate a quick visual comparison. Use a known buffer as an additional measurement. If it is shrinking, the current process is borrowing from the past.'),
 ('Separate progress from consumption','Productivity can create research progress without consuming proportionally more packs. Production figures are useful evidence, not a complete performance model. For a bottleneck experiment, name the suspected constraint, predict the graph change, modify one thing and verify whether the prediction held.')],
 sources=['statistics','prototypes'],related=['flow','ratios','performance'],experiment='Turn off a consuming line and observe its input buffer and production graph. Explain why upstream production can drop even though your factory now has more spare capacity.',diagram='debug')

topic('performance','FPS, UPS, benchmarking and practical optimization','Analysis',
 'Keep simulation speed separate from rendering speed and factory throughput.',[
 ('Two clocks','FPS describes rendered frames. UPS describes simulation updates. The ordinary target is 60 simulation updates per game second; a machine struggling to simulate may run slower in wall-clock time. A beautifully rendered screen does not prove the simulation is keeping up.'),
 ('Measure representative work','Use the debug display intentionally and compare the same save under a comparable workload. A paused factory or a fully backed-up module is not a meaningful throughput stress test. Rendering settings may help FPS while production design or hardware limits affect UPS. Avoid claiming a universal cheapest design without measuring the actual save.'),
 ('Optimize the useful path','Reduce unnecessary logistics and circuit work only after identifying a meaningful constraint. Direct insertion and local networks can reduce transport work, but building huge idle infrastructure also has costs. Keep a backup before performance experiments and check that any change still meets functional demand and remains maintainable.')],
 sources=['time','prototypes'],related=['statistics','scaling'],experiment='Record both FPS and UPS before and after a controlled change. State whether you improved rendering, simulation speed, useful output or more than one.',diagram='debug')

topic('backups','Offline manual use, save backups, mods and reproducible experiments','Analysis',
 'Keep your game data, blueprints and learning progress distinct.',[
 ('Three kinds of backup','A world save holds your factory and researched state. Blueprint exports preserve reusable layouts. The manual’s JSON export holds learning progress and reading preferences. None substitutes for the others. Browser storage may be unavailable or cleared; export progress before moving the manual to another machine.'),
 ('Version and mod state','This reference targets base 2.1.24 with Space Age, Quality, Recycler and Elevated Rails disabled. A save’s enabled mods and changed recipes can invalidate reference numbers. Keep a separate pre-update backup and compare the in-game version and Factoriopedia before applying an exact ratio. Do not downgrade a newer save expecting it to remain compatible.'),
 ('Reproduce an experiment','Record the version, enabled mods, relevant research, machine tier, modules, power condition and input/output demand. Change one variable at a time. Screenshots should show Alt-mode, orientation and enough context to identify the supply path. This is more useful than recording only that a line is broken.')],
 sources=['linux','prototypes'],related=['world','diagnosis'],experiment='Export manual progress, make a separate game save and export one blueprint. Explain exactly what each file can restore.',diagram='debug')

topic('diagnosis','A complete diagnostic decision path','Analysis',
 'Use the first failed requirement to choose the next observation.',[
 ('Is the machine meant to be working?','Confirm the active recipe, researched unlock and current demand. If output is full, find the next consumer or accept deliberate idling. If a control condition disables it, read the measured signal and comparison. Check whether the entity is marked for deconstruction or has a pending replacement.'),
 ('Can every input reach it?','Check power or fuel, then each ingredient and its actual pickup lane or pipe socket. Follow the first missing ingredient upstream until you find a producer that is blocked, depleted, unpowered or undersupplied. For fluids, also inspect segment overextension, mixing and pump direction.'),
 ('Can the product leave?','Check output inventory, inserter filter and direction, belt capacity, tank capacity, station handling and request eligibility. For trains, separate No path from Destination full and red-signal waiting. For robots, separate missing coverage, missing items, missing robot type and charging queues. After one fix, observe again: several independent faults can coexist.')],
 sources=['prototypes','troubleshoot'],related=['flow','rail-deadlocks','robot-networks'],experiment='Choose a stopped line and write one evidence-based sentence per dependency. Stop guessing as soon as a specific machine status identifies the failed requirement.',diagram='debug')

topic('map-remote','Map, radar, pins and remote work','Player tools',
 'Distinguish explored terrain from current visibility and from construction capability.',[
 ('The map remembers old information','Explored terrain can be known without being currently visible. Radar provides local observation and periodic wider scans. An old map image is not proof that an enemy nest or building still has the same state. Keep useful observation near junctions and distant stations.'),
 ('Remote orders need local workers','You can inspect and plan remotely, but ghosts still require construction coverage and items. Opening a remote inventory does not make your character carry those items across the world. Train orders, robot tasks and remote vehicle control each have their own prerequisites.'),
 ('Pins make a working notebook','Name stations and add useful map labels or pins for oil, future ore, broken lines and planned expansions. Prefer a concrete note such as copper supply below 15/s to a vague todo. Revisit and remove obsolete markers so the map remains useful.')],
 sources=['radar','controls','prototypes'],recipes=['radar'],related=['outposts','blueprint-workflow','vehicles'],experiment='Compare an area under continuous radar coverage with a previously explored dim area. State which observations are live and which are last known.',diagram='train')

topic('inventory-workflow','Inventory, crafting queue, filters and the quickbar','Foundations',
 'Learn the context of a click before using bulk-transfer shortcuts.',[
 ('Inventory operations have a target','Left-click moves a full stack into or out of the cursor. Right-click can split a stack or place one held item. Shift transfers a stack between open inventories; Ctrl transfers matching items more broadly. An empty-slot Ctrl operation can affect many item types. Check which inventory and slot the mouse is over.'),
 ('Handcrafting is a dependency queue','Crafting may queue available intermediate recipes automatically. It cannot replace a machine-only process such as engine-unit assembly or a fluid recipe. A long queue can consume plates intended for construction, so automate recurring supplies and cancel carefully when priorities change.'),
 ('Quickbar entries are references','Put frequently built machines and planning tools on the quickbar. Clearing a shortcut does not discard the referenced inventory item. Slot filters can reserve cargo space for selected items. Learn the difference between an inventory filter, a quickbar reference and an inserter filter: each constrains a different operation.')],
 sources=['controls','prototypes'],related=['orientation','circuits-production'],experiment='In a spare chest, test one-stack, all-matching and half-stack transfer with small quantities. Predict the result in each inventory before using the shortcut on valuable production stock.',diagram='input')

SOURCE_ADDITIONS=frozendict({
 'prototypes':('Wube 2.1.24 prototype definitions (pinned tag)','https://github.com/wube/factorio-data/tree/2.1.24'),
 'silo-script':('Wube base-game victory script','https://github.com/wube/factorio-data/blob/2.1.24/core/lualib/silo-script.lua'),
 'releases':('Official stable and experimental version status (live)','https://factorio.com/api/latest-releases'),
 'recycler-mod':('Wube Recycler mod dependency manifest','https://github.com/wube/factorio-data/blob/2.1.24/recycler/info.json'),
 'recipe-api':('Recipe prototype defaults and productivity rules','https://lua-api.factorio.com/latest/prototypes/RecipePrototype.html'),
 'mining':('Mining mechanics','https://wiki.factorio.com/Mining'),
 'pollution':('Pollution production, spread and absorption','https://wiki.factorio.com/Pollution'),
 'electric':('Electric networks and storage','https://wiki.factorio.com/Electric_system'),
 'inserters':('Inserter behavior and insertion limits','https://wiki.factorio.com/Inserters'),
 'splitter':('Splitter behavior','https://wiki.factorio.com/Splitter'),
 'beacon':('Current beacon transmission model','https://wiki.factorio.com/Beacon'),
 'pump':('Pump transfer, direction and wagon connections','https://wiki.factorio.com/Pump'),
 'pumpjack':('Oil yield and extraction','https://wiki.factorio.com/Pumpjack'),
 'roboport':('Roboport charging, coverage and personal networks','https://wiki.factorio.com/Roboport'),
 'railway':('Rail infrastructure and automatic transport','https://wiki.factorio.com/Railway'),
 'chain':('Chain signal paths and states','https://wiki.factorio.com/Rail_chain_signal'),
 'train-improvements':('Wube: train groups and schedule interrupts','https://factorio.com/blog/post/fff-389'),
 'generic-trains':('Wube: generic interrupts and stop priorities','https://factorio.com/blog/post/fff-395'),
 'cookbook':('Circuit cookbook (check current GUI settings)','https://wiki.factorio.com/Tutorial:Circuit_network_cookbook'),
 'arithmetic':('Arithmetic operations and integer division','https://wiki.factorio.com/Arithmetic_combinator'),
 'decider':('Decider conditions, outputs and latency','https://wiki.factorio.com/Decider_combinator'),
 'selector':('Selector modes and index behavior','https://wiki.factorio.com/Selector_combinator'),
 'constant':('Constant signals and named groups','https://wiki.factorio.com/Constant_combinator'),
 'logic':('Circuit wildcards and logic signals','https://wiki.factorio.com/Tutorial:Combinator_tutorial'),
 'deconstruction':('Deconstruction, cancellation and undo limits','https://wiki.factorio.com/Deconstruction_planner'),
 'upgrade':('Upgrade planner filters and replacement rules','https://wiki.factorio.com/Upgrade_planner'),
 'armor':('Armor families','https://wiki.factorio.com/Armor'),
 'equipment':('Equipment grids and portable power','https://wiki.factorio.com/Equipment_modules'),
 'tank':('Tank remote control and equipment','https://wiki.factorio.com/Tank'),
 'spidertron':('Spidertron control, inventory and equipment','https://wiki.factorio.com/Spidertron'),
 'mapgen':('World generation and settings','https://wiki.factorio.com/Map_generator'),
 'radar':('Radar observation and map coverage','https://wiki.factorio.com/Radar'),
 'time':('Simulation ticks and crafting speed (day table may be stale)','https://wiki.factorio.com/Time'),
})

CHAPTER_TOPICS=frozendict({
 'setup':['world','orientation','backups'], 'movement':['orientation','inventory-workflow','map-remote'],
 'mining':['iron','copper','stone-coal'], 'power':['steam-power','electricity','power-recovery'],
 'belts':['belts-lanes','splitters','inserter-details'], 'automation':['flow','ratios','circuits-production'],
 'redgreen':['science-progression','science-ratios'], 'defense':['pollution','defense-design'],
 'steel':['smelting','scaling','outposts'], 'fluids':['fluids-modern','fluid-pumps'],
 'oil':['oil-extraction','oil-processing','oil-balancing','oil-products'],
 'blue':['circuits-production','science-ratios'], 'trains1':['rail-foundations','rail-loading','rail-throughput'],
 'trains2':['rail-blocks','rail-deadlocks','rail-dispatch'], 'robots':['robot-networks','robot-chests','robot-throughput'],
 'blueprints':['blueprint-workflow','planner-tools','equipment'], 'circuits':['signals','combinators','circuit-timing','circuit-recipes'],
 'late':['science-progression','science-ratios','rocket-budget'], 'nuclear':['uranium','nuclear-heat','solar'],
 'modules':['modules-math','beacon-math'], 'rocket':['rocket-plan','rocket-budget','after-launch'],
 'qol':['map-remote','backups'], 'linux':['backups','performance'], 'debug':['diagnosis','statistics','flow'],
})

CONTROL_ADDITIONS=[
 ('Build and interact','Shift+Left mouse with planner','Cancel planned deconstruction or upgrade','Drag over pending orders with the appropriate planner held to cancel them.','Base'),
 ('Build and interact','Right mouse with upgrade planner','Select downgrade','Use the planner reverse-selection action to apply its reverse mapping. Inspect the highlighted replacements.','Base'),
 ('Build and interact','Ctrl+Left mouse with selection tool','Deselect tool selection','A selection-tool context, distinct from Ctrl-click inventory transfer.','Base'),
 ('Map and trains','Left mouse drag on map','Pan the map','Drag the map background to change the viewed area.','Base'),
 ('Build and interact','Shift+Mouse wheel with blueprint book','Cycle blueprint in book','Select the next or previous design while holding the book; clipboard cycling is a different context for the same gesture.','Base'),
 ('Quickbar','Unbound','Next active quickbar','Optional control: bind it in Settings → Controls if you want to advance only the top active bar.','Base'),
 ('Quickbar','Unbound','Previous active quickbar','Optional control for the preceding top active bar.','Base'),
 ('Quickbar','Unbound','Secondary quickbar shortcuts 1–10','The second row has separate optional bindings; its slots are not automatically Shift+number.','Base'),
 ('Plans / tools','Unbound','Make blueprint book','Create a reusable book from the shortcut toolbar or bind this optional action.','Base'),
 ('Panels','Tab when message is open','Confirm message','The active modal message takes this action; the map action has a different context.','Base'),
 ('Contextual','Unbound','Next music track','Optional music control; has no production effect.','Base'),
 ('Contextual','Unbound','Previous music track','Optional music history control.','Base'),
 ('Contextual','Unbound','Pause or resume music','Pauses audio playback, not factory simulation.','Base'),
 ('Expansion controls','Up / Down in remote view','Previous or next surface','Surface selection is meaningful with multiple surfaces; the base learning route remains on Nauvis.','Expansion'),
 ('Editor / debug','Shift+Right mouse with clone tool','Select clone source','Editor clone tool: set the area to copy. This is different from normal machine-settings copy.','Editor / debug'),
 ('Editor / debug','Shift+Left mouse with clone tool','Select clone destination','Editor clone tool: choose where the prepared source is cloned.','Editor / debug'),
 ('Editor / debug','Shift+Right mouse on scripting object','Remove scripting object','Map editor scripting-object context.','Editor / debug'),
 ('Editor / debug','Unbound','Toggle selected entity','Optional advanced debug action; bind only if you need it for controlled testing.','Editor / debug'),
]

CONTROL_EXAMPLES=frozendict({
 'Pipette / clear cursor':('World; hover the object you want, or clear a held item/tool.','Hover a furnace and press Q to select the matching available item; press Q again to clear your cursor.','It selects the type from your inventory; it does not copy a real machine into existence.'),
 'Move all matching stacks':('Open inventory over a matching item, or world fast transfer.','Ctrl-click iron in a chest inventory to move matching plates; use a small test chest to learn the empty-slot behavior.','Over an empty slot this can transfer many item types. World transfer with an empty cursor can take entity contents.'),
 'Move one stack':('Two compatible inventories are open; hover a stack.','Shift-click one coal stack in your inventory to put it in the open chest.','The hovered stack and selected inventory determine direction.'),
 'Build ghost':('World with a buildable item selected.','Hold an assembler, then Shift-click a clear location to plan it for later construction.','A ghost needs a real item and construction work; checking a manual step does not build it.'),
 'Paste machine settings':('World; after copying a compatible source.','Copy a gear assembler with Shift-right-click, then Shift-left-click another assembler.','Copy/paste settings is different from placing a building ghost. Inspect filters and circuit settings as well as recipes.'),
 'Copy machine settings':('World; hover the configured source entity.','Shift-right-click the configured assembler before pasting onto its neighbor.','The source must remain available for the intended copy/paste operation; incompatible entity types cannot receive every setting.'),
 'Filter slot':('Supported inventory or quickbar slot.','Use middle-click on a cargo-wagon slot to reserve it for a selected item.','Clearing a quickbar reference does not discard your real inventory item.'),
 'Super-force build':('World with a supported building or blueprint placement.','Inspect a small blocked blueprint placement with Ctrl+Shift held before placing it.','It can order existing factory equipment removed. Confirm the visible selection before releasing the mouse.'),
 'Temporary train stop':('Locomotive map or supported train-control context.','Ctrl-click a reachable rail location to send the selected train there once.','An arbitrary map click without a selected train context is not a destination order.'),
 'Change quality selection':('Cursor quality selection; Quality enabled.','Use this only in a separate game with the Quality mod enabled.','This manual’s base-game ratios assume normal quality and exclude quality progression.'),
})

def enrich(payload):
    payload['troubleshooting']=[list(row) for row in payload['troubleshooting']]
    payload['glossary']=[list(row) for row in payload['glossary']]
    payload['sources'].update(SOURCE_ADDITIONS)
    ref=json.loads((Path(__file__).parent/'data/reference.json').read_text(encoding='utf-8'),object_pairs_hook=frozendict,array_hook=tuple)
    payload['reference']=ref
    payload['topics']=TOPICS
    payload['meta'].update(edition=2,notes='Numerical reference extracted from Wube 2.1.24 commit '+ref['provenance']['commit']+'. Explanations researched against official references; not an in-game replay certification.')
    byid={c['id']:c for c in payload['chapters']}
    # Preserve original step positions: progress exported by edition 1 remains meaningful.
    byid['setup']['steps'][0]='At the main menu, open Mods. Keep Base enabled. Disable Space Age, Quality, Recycler and Elevated Rails, plus other gameplay-changing mods. Recycler is a separate expansion mod in 2.1 and must also be off for this base-only reference.'
    payload['meta']['content']='Base game only; no Space Age, Quality, Recycler, Elevated Rails or other gameplay mods'
    byid['mining']['steps'][3]='Produce at least 50 iron plates to trigger Steam power and at least 10 copper plates to trigger Electronics. These early 2.1 unlocks are automatic research triggers. Mine stone for more furnaces and later stone bricks.'
    byid['power']['steps'][0]='After producing 50 iron plates to unlock Steam power, place an offshore pump on water and connect its water outlet to a boiler water input. Electronics unlocks from producing 10 copper plates and provides small poles.'
    byid['automation']['steps'][0]='After Steam power and Electronics are unlocked, craft a lab to trigger Automation science pack. Handcraft 10 red packs from copper plates and gears, power the lab and insert the packs, select Automation in T, then craft and configure an assembling machine.'
    byid['oil']['steps'][0]='Research Oil gathering, craft and power pumpjacks on crude wells, and extract crude to trigger Oil processing. Then craft and power a refinery and select Basic oil processing: crude becomes petroleum gas.'
    byid['late']['steps'][3]='Automate red, green, blue, purple and yellow science. Follow the Rocket silo prerequisite tree, including speed module 3 and productivity module 3 research, even though installing modules is optional. The silo research itself needs 1,000 of each required pack; military packs are not required.'
    byid['setup']['steps'][4]='Your first-rocket route is to build a rocket silo, construct a rocket, load a satellite payload, place a cargo landing pad, and launch. The satellite returns space science; another accepted payload exists for a special achievement.'
    byid['rocket']['steps'][2]='Construct a satellite: 100 low-density structures, 100 solar panels, 100 accumulators, 5 radars, 100 processing units and 50 rocket fuel before any upstream productivity.'
    byid['rocket']['steps'][3]='Place a cargo landing pad on the planet. Load the satellite into the silo payload. Base-game launch needs an accepted payload; a satellite is the payload that returns space science.'
    byid['rocket']['steps'][5]='If the rocket will not launch, confirm that the silo is powered, all 100 rocket parts are complete, an accepted payload is loaded and the cargo landing pad exists.'
    byid['rocket']['tips'][1]='A satellite plus cargo landing pad provides the useful first-launch science route. Raw fish is also an accepted special-achievement payload; it does not produce space science.'
    byid['rocket']['why']='Complete the first-rocket goal and receive base-game space science.'
    byid['trains2']['steps'][0]='Signals divide connected rail into blocks. Automatic trains reserve blocks to prevent conflicting entry; a long train can occupy several blocks. A stop does not divide a block. Manually driven trains ignore signals.'
    byid['qol']['title']='Current-version tools you can use when needed'
    byid['qol']['steps'][2]='Use an empty quickbar slot hotkey to pipette a hovered object when the relevant option is enabled. Find its setting under Interface → Quickbar.'
    byid['qol']['steps'][3]='Supported miners, pumpjacks and inserters can be flipped; inserter drops onto splitters and fluid-wagon pump connections have current-version improvements.'
    byid['qol']['steps'][4]='Use Factoriopedia pinning and hiding unresearched content, fluid flow information, and the circuit interface’s separate input/output wire selections.'
    byid['qol']['steps'][5]='Learn Spidertron patrol, rolling-stock upgrades and enemy expansion alerts only when they solve a problem in your current factory.'
    byid['nuclear']['steps'][2]='Supply exchangers with water and route their hot steam to steam turbines. Remove used uranium fuel cells from the reactor so the output does not block refueling.'
    byid['debug']['steps'][1]='Step 2: Follow the item/fluid stream backward. Is the ingredient produced, delivered, accessible at the inserter’s pickup position and within its available throughput? Ordinary inserters can pick from either belt lane.'
    byid['modules']['steps'][3]='For a simple eligible recipe, output/s = recipe output quantity × effective crafting speed × (1 + productivity bonus) / recipe time. Read the displayed machine speed; catalyst returns and probabilistic products need special treatment.'
    byid['movement']['title']='The screen, cursor and essential shortcuts'
    # Put the first-rocket route before optional deep systems and keep phase groups contiguous.
    order=['setup','movement','mining','power','belts','automation','redgreen','defense','steel','fluids','oil','blue','trains1','trains2','robots','blueprints','late','rocket','circuits','modules','nuclear','qol','linux','debug']
    for id in ('circuits','modules','nuclear'):byid[id]['phase']='ADVANCED'
    payload['chapters']=[byid[id] for id in order]
    for ch in payload['chapters']:
        ch['topics']=CHAPTER_TOPICS[ch['id']]
        ch['optional']=ch['id'] in ('trains1','trains2','robots','blueprints','circuits','modules','nuclear','qol','linux','debug')
        ch['sources']=list(dict.fromkeys([*ch['sources'],'prototypes']))
        ch['experiment']=next(t['experiment'] for t in TOPICS if t['id']==ch['topics'][0])
    for entry in payload['troubleshooting']:
        if entry[0]=='Rocket unable to launch':entry[1]='Finish 100 rocket parts, provide an accepted payload and build the cargo landing pad. A satellite returns science; raw fish is a special achievement payload.'
        if entry[0]=='One lane starves':entry[1]='Check supply and pickup/drop locations. A lane carries half the belt rating. Ordinary inserters can pick from either lane; they do not automatically balance a belt’s two lanes.'
        if entry[0]=='Train “No path”':entry[1]='Check connected rails, locomotive facing, stop side and name, and legal signal direction. Elevated rails are outside this base-game scope.'
    payload['troubleshooting'].extend([
      ['Power fails repeatedly after restart','Restore coal mining and boiler feeding before reconnecting large loads. Keep emergency coal and check that recovery inserters themselves have power.'],
      ['Uranium-235 has not appeared','Its baseline chance is 0.007 per processing craft, with mutually exclusive U-238 output. Random gaps are normal; check ore, power, output space and buffers.'],
      ['Kovarex never starts again','Keep its 40 U-235 working input available. Gross output 41 does not mean 41 surplus; net gain is one before bonuses.'],
      ['Research pack count looks too small','Some recipes output two or three packs per craft. Compare packs/min, machine speed and active research requirements, not only recipe seconds.'],
      ['A personal roboport does nothing','Check toggle, equipment power, carried construction robots, exact materials and range. The stationary network and personal inventory are separate.'],
      ['A requester and provider move items forever','Inspect overlapping requests, excess-item removal and buffer eligibility. Avoid a cycle that returns exactly what the same configuration requests.'],
      ['A blueprint looks right but does not work','Inspect recipes, filters, rotations, fluid ports, copied circuit settings, modules and parameters, not only positions.'],
      ['The bus is full but a machine starves','Trace the specific item and lane through every split, side-load and pickup position. Total belt capacity is shared across two lanes.'],
      ['Beacons make less improvement than expected','Count beacons affecting each machine, apply diminishing transmission and inspect compatible effects. Then check ingredient and output transport.'],
      ['Space science is missing after launch','Use a satellite payload, find the cargo landing pad and allow delivery time. A fish payload does not return science.'],
      ['Nuclear plant has fuel but no electricity','Trace heat, exchanger temperature and water, hot steam, turbine input and pole connection. Remove used fuel cells and provide startup power for essential pumps.'],
      ['Train has fuel but will not reverse automatically','Automatic travel needs a locomotive facing the desired direction. A one-locomotive train can use a loop; a shuttle needs opposing locomotives.'],
      ['Stock is large but the factory cannot sustain output','Stored buffers can hide a rate deficit. Measure a stable interval and check whether the reserve trends down.'],
    ])
    glossary_extra=[('Crafting speed','Multiplier that converts recipe seconds into actual craft time.'),('Productivity','Extra eligible output for normal recipe input; distinct from crafting speed.'),('Catalyst','An input returned by a recipe, so gross output differs from net production.'),('Saturation','A transport path running at its available capacity.'),('Back pressure','A full downstream output stopping upstream production.'),('Hysteresis','Different turn-on and turn-off thresholds with memory between them.'),('SPM','Science packs per minute; specify which packs and whether this means item production or effective research.'),('Reservation','An automatic train’s claim on route or station capacity.'),('Train group','Named shared schedule configuration for multiple trains.'),('Interrupt','A conditional train-schedule detour with its own destinations and completion rules.'),('Input starved','Unable to work continuously because a required input is missing.'),('Throughput limited','Unable to carry or process the requested sustained rate.'),('Working inventory','Material that must stay inside a production cycle, such as Kovarex catalyst.'),('Supply area','Pole coverage for machines; different from maximum wire reach.'),('Brownout','Insufficient electric supply causing consumers to slow.'),('Tick','One simulation update; normally 60 per game second.'),('Net output','Gross output minus the amount consumed or recirculated within the process.'),('Research trigger','A gameplay event requirement that unlocks a technology instead of lab pack consumption.'),('Provider','An inventory eligible to offer its contents to a robot network.'),('Buffer','A stored reserve that smooths a timing gap; also a specialized logistic chest type.'),('Module slot','A manufacturing machine’s effect-module space, distinct from an armor equipment grid.')]
    payload['glossary'].extend(glossary_extra)
    for g in payload['glossary']:
        if g[0]=='Cargo landing pad':g[1]='Planetary receiving structure required for base-game rocket launch and satellite science delivery.'
    for cat,key,action,detail,scope in CONTROL_ADDITIONS:
        payload['controls'].append(dict(category=cat,key=key,action=action,detail=detail,scope=scope,note=''))
    # Group by the work the player is doing, rather than placing unrelated actions
    # under one catch-all World/Advanced category.
    for c in payload['controls']:
        action=c['action'];key=c['key']
        if c['category']=='World':
            if action in ('Shoot enemy','Shoot selected target','Cycle weapons','Enter/exit vehicle'):c['category']='Combat & vehicles'
            elif 'Zoom' in action:c['category']='Movement & view'
            elif action in ('Pin entity or location','Ping map location'):c['category']='Map & navigation'
            elif action in ('Toggle chat/console','Open Factoriopedia'):c['category']='Panels & reference'
            else:c['category']='Build & interact'
        elif c['category']=='Movement':c['category']='Movement & view'
        elif c['category']=='Inventory / craft':c['category']='Crafting' if 'Craft' in action or 'Cancel' in action else 'Inventory & filters'
        elif c['category']=='Plans / tools':
            if 'wire' in action:c['category']='Wires & circuits'
            elif action.startswith('Toggle '):c['category']='Equipment & logistics'
            elif 'remote' in action:c['category']='Combat & vehicles'
            else:c['category']='Blueprints & planners'
        elif c['category']=='Panels':c['category']='Panels & reference'
        elif c['category']=='Advanced':
            if action in ('Toggle rail layer','Avoid obstacles','Temporary train stop','Schedule train stop','Connect trains','Disconnect trains'):c['category']='Trains & rail'
            elif 'blueprint' in action.lower():c['category']='Blueprints & planners'
            elif action=='Remove pole cables':c['category']='Wires & circuits'
            elif action=='Change tile brush size':c['category']='Build & interact'
        elif c['category']=='Build and interact':c['category']='Blueprints & planners'
        elif c['category']=='Map and trains':c['category']='Map & navigation'
    contexts={
      'Movement & view':'World movement or camera view; vehicle movement follows its configured driving mode.',
      'Build & interact':'World view with the stated cursor item, target entity or building tool.',
      'Combat & vehicles':'A compatible weapon, vehicle, remote or equipment action must be available.',
      'Map & navigation':'Map view or the stated navigation interface; the selected object controls the result.',
      'Panels & reference':'The named interface or modal window; UI focus determines how a repeated key behaves.',
      'Crafting':'Character recipe panel or crafting queue; mouse gestures do different work in these two places.',
      'Inventory & filters':'Supported inventory or slot, with the relevant other inventory open for transfers.',
      'Blueprints & planners':'The named copy, paste, blueprint, upgrade or deconstruction tool is selected.',
      'Equipment & logistics':'The relevant equipment, research, network or personal request configuration is available.',
      'Wires & circuits':'World view with a selected wire tool or a compatible pole/circuit connection.',
      'Trains & rail':'The rail planner, selected rolling stock or a train’s map/schedule interface.',
      'Movement':'World movement; when driving, the selected vehicle movement mode applies.',
      'World':'World view. The object under the cursor and the held tool determine the action.',
      'Build and interact':'World with the relevant entity, blueprint or selection tool active.',
      'Inventory / craft':'Inventory, crafting recipe or crafting queue; these contexts change the same mouse buttons.',
      'Quickbar':'An active quickbar or a supported quickbar configuration action.',
      'Plans / tools':'Tool shortcut; availability and effect depend on research, equipped items or selected tool.',
      'Panels':'Open or close the named game interface. Modal windows can take precedence.',
      'Advanced':'The described rail, blueprint or debug context must be active.',
      'Contextual':'Only in the specific interface or tool state described in the action.',
      'Editor / debug':'Scenario editor or debug context; separate from normal Freeplay progression.',
      'Expansion controls':'Requires the relevant expansion/mod context; excluded from this base-game route.',
      'Map and trains':'Map or the selected train’s GUI; the same gesture can have other uses elsewhere.'}
    essentials={'Pipette / clear cursor','Build / open GUI','Mine / use item','Rotate clockwise','Toggle Alt-mode','Open inventory/character GUI','Copy machine settings','Paste machine settings','Move one stack','Move all matching stacks','Map','Technology / research','Production statistics','Pick up nearby items','Undo','Menu / cancel'}
    for i,c in enumerate(payload['controls']):
        if c['key']=='G' or 'quality' in c['action'].lower():c['scope']='Expansion'
        if c['category']=='Editor / debug' or 'Debug shortcut' in c['detail'] or c['action'] in ('Debug settings','Debug display','Reset zoom','Prototype viewer','Prototype explorer'):
            c['scope']='Editor / debug'
        if c['action']=='Cargo wagon fluid loading fails':c['scope']='Base'
        if c['action']=='Quick pipette (2.1.21)':c['action']='Empty-slot quick pipette'
        context,example,pitfall=CONTROL_EXAMPLES.get(c['action'],(contexts.get(c['category'],contexts['Contextual']),
            'Try “'+c['action']+'” in the stated context, then inspect the resulting cursor, window, selection or inventory before repeating it at scale.',
            'A rebound key or a different active context can change the result. Confirm the action under Settings → Controls.'))
        example=CONTROL_PRACTICE.get(c['action'],example)
        if c['category']=='Editor / debug':pitfall='Editor and script commands can change the world and affect achievements. Use an experiment save; they are not part of the first-rocket route.'
        if c['scope']=='Editor / debug':c['category']='Editor / debug'
        if c['scope']=='Expansion':c['category']='Expansion controls'
        c.update(id='control-'+str(i),context=context,example=example,pitfall=pitfall,level='Essential' if c['action'] in essentials or c['category']=='Movement & view' else 'Reference',source='controls',verification='Official default reference; rebound keys and active contexts take precedence.')
    payload['audit']={
       'version':'2.1.24','edition':2,'checked':'2026-10-27',
       'completed':['Reordered the first-rocket route before optional advanced systems.','Added topic explanations, worked examples and reproducible in-game exercises.','Replaced remembered recipe and technology quantities with the pinned Wube definitions.','Corrected satellite ingredients and the distinction between accepted rocket payloads and science payloads.','Separated everyday, expansion and editor/debug control contexts; added unbound actions.','Added global search, progressive lesson reading, text settings, data references and assumption-labeled calculators.'],
       'limits':['No full Freeplay replay in Factorio 2.1.24 was performed.','Entity/item records are extracted literal fields; generated or computed fields can be absent. They are not a complete runtime prototype dump.','Game-defined control defaults cannot all be extracted from the public prototype repository. Controls were cross-checked with the official table; personal rebindings take precedence.','No raw-ore optimization solver or simulation of exact entity placement is claimed.','Official wiki pages can contain stale passages and expansion tabs. Source conflicts are resolved using pinned definitions where possible.'],
       'sourceConflicts':['The general fluid page contains old pressure-model text alongside modern segment rules. The manual uses modern connected-segment behavior.','The general logistics article still mentions 1 MW charging slots; the dedicated roboport page and pinned data specify 500 kW per slot.','The older nuclear tutorial recommends tank-based control; direct reactor circuit readings are available.','The old Time page’s day-length table differs from current data/documentation; no outdated exact day duration is used in the solar calculation.'],
    }
    return payload

# Examples describe concrete task contexts rather than merely repeating action names.
CONTROL_PRACTICE=frozendict({
 'Move up':'Hold W in world view to walk toward the top of the screen; release it to stop.',
 'Move down':'Hold S to walk away from your starter drill; try the same movement in a safe vehicle test to learn its driving mode.',
 'Move left':'Walk left around your furnace row with A and leave enough corridor for future movement.',
 'Move right':'Use D to move right past a line of machines without clicking their inventories.',
 'Open inventory/character GUI':'Press E, find a stack of plates and the crafting recipes, then close the panel before placing a building.',
 'Build / open GUI':'With no building held, click a furnace to inspect it. With a furnace held, click a valid clear tile to place it.',
 'Mine / use item':'Hold right-click on a spare placed belt to pick it up. With a usable capsule selected, right-click performs that item’s action instead.',
 'Rotate clockwise':'Hold an inserter, press R and inspect the pickup/drop preview before placement.',
 'Rotate anticlockwise':'Rotate a held assembler backward with Shift+R to put its fluid socket on the intended side.',
 'Flip horizontally':'Select a compatible asymmetric layout, press H and inspect both its geometry and port labels before placement.',
 'Flip vertically':'Press V on a compatible held pumpjack or layout; verify its output connection rather than assuming a cosmetic mirror.',
 'Toggle Alt-mode':'Press Alt beside a configured assembler and compare the visible recipe and direction labels before and after.',
 'Pick up nearby items':'Stand beside a belt carrying spare plates and hold F to collect accessible items into your inventory.',
 'Drop one item':'Hold a small stack of plates and press Z above a belt to put one item onto it; inspect which lane receives it.',
 'Shoot enemy':'Equip a weapon with compatible ammunition and use Space near an enemy in an experiment save.',
 'Shoot selected target':'Hover the exact target and use Shift+Space when the selected-target action is intended.',
 'Cycle weapons':'Equip two weapons, press C and check the selected weapon before consuming ammunition.',
 'Enter/exit vehicle':'Stand beside a parked fueled car, press Enter to enter, and practice exiting in a safe location.',
 'Zoom world in/out':'Scroll near a belt junction to inspect lanes, then zoom out to trace the whole source-to-consumer route.',
 'Zoom minimap':'Hover the minimap first, then use Shift+Alt with the wheel to change only its zoom.',
 'Toggle chat/console':'Open the console to read chat. Do not run a script command merely to inspect production; use P for that.',
 'Open Factoriopedia':'Hover a recipe, item or entity and Alt-click it to open the relevant built-in reference.',
 'Pin entity or location':'Alt-right-click an important location, then use the pin to return to an unfinished outpost task.',
 'Ping map location':'Ctrl+Alt-click a relevant map location to create a chat-linked ping when coordinating a factory.',
 'Craft 1':'In character crafting, left-click a furnace recipe when you need one, and inspect the queued ingredients.',
 'Craft 5':'Right-click a gear recipe in the crafting panel, then count the crafts added to the queue.',
 'Craft maximum':'Shift-left-click a recipe only after checking that consuming your available plates will not block another task.',
 'Cancel 1':'Click the corresponding crafting queue entry once and inspect the refunded ingredients and remaining queue.',
 'Cancel 5':'Right-click a queued repeated craft to cancel a batch of five when that many remain.',
 'Cancel all':'Shift-click the relevant crafting queue entry when you intend to cancel all its remaining crafts.',
 'Pick up/drop full stack':'Left-click one plate stack to hold it, then click an empty chest slot to place the held stack.',
 'Half-stack / place one':'With an empty cursor, right-click a stack to take half. With items held, right-click an eligible slot to place one.',
 'Transfer half stack':'With a chest open, Shift-right-click one stack and compare the amounts in both inventories.',
 'Transfer half of item type':'Ctrl-right-click one item type in an open inventory to transfer a portion of matching stacks; test this with small quantities first.',
 'Copy inventory filter':'Copy a configured cargo-slot filter with Shift-right-click before pasting it into a compatible slot.',
 'Paste inventory filter':'After copying a cargo-slot filter, Shift-left-click a compatible slot and verify its reserved item icon.',
 'Select quickbar slot':'Put belts in quickbar slot 1, press 1 in world view and verify that the cursor selects belts from inventory.',
 'Activate quickbar N':'Press Shift+2 to activate quickbar 2; this selects the bar, not automatically its second item.',
 'Rotate active quickbars':'Press X and inspect which configured bars are now active before using the number keys.',
 'Empty-slot quick pipette':'With the relevant Interface option enabled, hover a furnace and press the key for an empty quickbar slot.',
 'Copy area':'Press Ctrl+C and drag a rectangle around a small tested machine block. Inspect the copied boundary.',
 'Cut area':'Use Ctrl+X on a small noncritical block; verify that the source receives removal orders before pasting elsewhere.',
 'Paste clipboard':'Press Ctrl+V, inspect the selected copied layout and click a valid area to place its ghosts.',
 'Undo':'After a small accidental ghost placement, press Ctrl+Z and verify which order was actually reversed.',
 'Redo':'After a deliberate undo of a placement, use the redo binding and inspect the restored order.',
 'Cycle clipboard history':'Hold the paste tool and Shift-scroll to a previous copy, verifying its preview before clicking.',
 'Make blueprint':'Press Alt+B, select a working block and give the resulting permanent blueprint a useful name.',
 'Make deconstruction planner':'Press Alt+D and inspect the planner selection on a small area; store and filter it for repeated safe use.',
 'Make upgrade planner':'Press Alt+U, select a small belt section and inspect the proposed replacements.',
 'Copper wire tool':'Press Alt+C and select two compatible poles to change their electric-wire connection; inspect network continuity.',
 'Red wire tool':'Press Alt+R, connect a tank and a pump, clear the cursor and configure the pump’s red input condition.',
 'Green wire tool':'Use Alt+G for an independent circuit network when a nearby red network should remain separate.',
 'Spidertron remote':'After building a Spidertron, select its remote and issue a simple safe waypoint before attempting a long route.',
 'Artillery targeting remote':'With a supplied artillery system and ready defense, use its remote to identify a deliberate target.',
 'Toggle exoskeleton':'With powered exoskeleton equipment installed, toggle it and compare movement in a safe corridor.',
 'Toggle personal logistics':'Disable personal requests temporarily while reorganizing inventory, then re-enable them in a supplied network.',
 'Toggle personal roboport':'Turn the personal port off before a risky combat approach and back on for repairs and construction.',
 'Discharge defense remote':'Install and power discharge defense, then practice its remote trigger in a controlled combat test.',
 'Technology / research':'Press T and inspect the prerequisites and pack requirements of the next technology before building its ingredients.',
 'Production statistics':'Press P, choose a suitable time window and compare iron production and consumption.',
 'Logistic networks':'Press L to inspect the selected network’s available robots and material counts.',
 'Blueprint library':'Press B and organize a tested blueprint into a named book instead of relying only on temporary clipboard history.',
 'Train overview':'Press O and locate a train reporting No path, then inspect its destination and route.',
 'Map':'Press Tab or M and trace the pollution cloud, resource patches and outpost labels.',
 'Menu / cancel':'Press Esc to back out of a panel or reach the menu; inspect the current context before pressing repeatedly.',
 'Character logistics':'Use F1 to find personal requests and verify their amounts before waiting for logistic delivery.',
 'Character info':'Use F2 to inspect character information instead of searching an unrelated production machine window.',
 'Character crafting':'Use F3 to reach character crafting, then inspect whether the intended recipe is actually handcraftable.',
 'UI navigation back/forward':'After following several Factoriopedia entries, use the back/forward binding to revisit the earlier entry.',
 'Focus GUI search':'In a searchable interface, press Ctrl+F and enter a technology or item name.',
 'Pause simulation':'Use the dedicated Pause key in a supported game context and distinguish paused simulation from a stopped music track.',
 'Toggle rail layer':'In a separate Elevated Rails-enabled game, use G in the rail planner. This action does not add elevated rails to a base-only save.',
 'Avoid obstacles':'While planning rail, use Ctrl-click in the supported rail-tool context and inspect the proposed route around obstructions.',
 'Schedule train stop':'With the train’s map or schedule context active, Shift-click an appropriate stop to add it to the schedule.',
 'Connect trains':'Bring compatible rolling stock together, select the intended connection and press J, then inspect the complete train.',
 'Disconnect trains':'Select the intended rolling stock connection and press K, then verify that you separated the expected sections.',
 'Change tile brush size':'Hold paving tiles and use Numpad plus/minus to preview a larger or smaller placement area.',
 'Remove pole cables':'Shift-click a selected pole and check the removed electric and circuit connections before continuing.',
 'Adjust blueprint absolute grid':'While placing an absolute-grid blueprint, Ctrl-arrow its grid and inspect alignment against an existing module.',
 'Shift blueprint entities':'Use Shift-arrow in the blueprint placement context and inspect how the planned entities move relative to the grid.',
 'Change UI scale':'Use Interface settings for a readable game UI, or the debug scale binding when deliberately testing scale.',
 'Automatic UI scale':'Use Ctrl+Numpad 0 to return the game’s UI scale to its automatic setting.',
 'Debug settings':'Open F4 and select only the diagnostic information needed for a controlled performance test.',
 'Debug display':'Use F5 to toggle configured basic debug information and distinguish FPS from UPS.',
 'Reset zoom':'Use F9 after a diagnostic zoom experiment to restore the normal zoom setting.',
 'Prototype viewer':'In a test context, inspect prototype information with Ctrl+Shift+E without treating it as an ordinary crafting interface.',
 'Prototype explorer':'Use Ctrl+Shift+F for advanced prototype inspection and compare internal names with the manual’s data records.',
 'Queue command':'With a compatible remote-controlled unit selected, Shift-right-click a second waypoint and inspect its queued orders.',
 'Rename all':'In a train-stop rename dialog, use the modifier deliberately only when every identically named stop should change.',
 'Place chat tag':'Open chat, then Shift-click a relevant object to include its contextual link in the message you are composing.',
 'Force tooltip':'Hold Shift over an item whose tooltip is delayed, then read its recipe or power information.',
 'Scroll tooltip':'With a supported anchored detailed tooltip, Shift-scroll to reach information beyond its visible portion.',
 'Previous mod':'While browsing the mod-selection interface, use Backspace or the alternative mouse button to return to the previous selection.',
 'Next replay player':'While watching a replay with multiple players, press F10 to cycle whose perspective you follow.',
})
