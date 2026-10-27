"""Rebuild factual reference data from Wube's pinned 2.1.24 checkout.

Requires Python 3.15+, Lua and luaparser (development tools only). This evaluates only
recipe/technology/fluid declarations. Entity/item fields are literal AST reads,
not a substitute for the game's runtime prototype dump; omissions stay omitted.
"""
import argparse
lazy import hashlib
lazy import json
lazy import subprocess
from operator import add, sub, mul, truediv, pow
from pathlib import Path
lazy from luaparser import ast, astnodes as n

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('checkout', type=Path)
args = parser.parse_args()
# Resolve required parser support after help handling, before extraction starts.
UNKNOWN=sentinel('UNKNOWN')
BINARY_OPERATORS=frozendict({n.AddOp:add,n.SubOp:sub,n.MultOp:mul,n.FloatDivOp:truediv,n.ExpoOp:pow})
checkout = args.checkout.resolve()
commit = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],encoding='utf-8').strip()
if commit != 'acf5a342afcb66c066b9d88d202e8622112da117':
    raise SystemExit('Expected Wube factorio-data tag 2.1.24, commit acf5a342afcb66c066b9d88d202e8622112da117')
raw = json.loads(subprocess.check_output(['lua',str(ROOT/'tools/extract_prototypes.lua'),str(checkout)],encoding='utf-8'))
recipe_fields = ('name','ingredients','results','energy_required','categories','category','allow_productivity','maximum_productivity','enabled','hidden','hide_from_player_crafting','main_product','subgroup','allow_decomposition')
recipes = []
for r in raw['recipe'].values():
    if r.get('parameter'): continue
    x = {k:r[k] for k in recipe_fields if k in r}
    x.setdefault('energy_required',0.5)
    x['categories'] = x.get('categories',[x.get('category','crafting')])
    x.setdefault('allow_productivity',False)
    x.setdefault('enabled',True)
    x['source']='base/prototypes/recipe.lua'
    recipes.append(x)
fluids = [{k:v for k,v in f.items() if k in ('name','default_temperature','max_temperature','heat_capacity','auto_barrel','fuel_value')} for f in raw['fluid'].values() if not f.get('parameter')]
for f in fluids:
    if f.get('auto_barrel',True):
        for empty in (False,True):
            fluid={'type':'fluid','name':f['name'],'amount':50}
            barrel={'type':'item','name':f['name']+'-barrel','amount':1}
            shell={'type':'item','name':'barrel','amount':1}
            recipes.append(dict(name=('empty-' if empty else '')+f['name']+'-barrel',
                ingredients=[barrel] if empty else [shell,fluid],results=[shell,fluid] if empty else [barrel],
                energy_required=0.2,categories=['crafting-with-fluid'],allow_productivity=False,enabled=False,source='base/data-updates.lua'))
techs=[]
for t in raw['technology'].values():
    x={k:t[k] for k in ('name','prerequisites','unit','research_trigger','effects','max_level','upgrade','hidden','enabled') if k in t}
    if 'unit' in x:
        x['unit']={k:v for k,v in x['unit'].items() if k in ('count','count_formula','time','ingredients')}
    x['prerequisites']=x.get('prerequisites') or []
    x['effects']=x.get('effects') or []
    for f in fluids:
        if f.get('auto_barrel',True) and x['name']=='fluid-handling':
            x['effects'].extend([{'type':'unlock-recipe','recipe':prefix+f['name']+'-barrel'} for prefix in ('','empty-')])
    techs.append(x)

def literal(node):
    if isinstance(node,n.String): return node.s.decode() if isinstance(node.s,bytes) else node.s
    if isinstance(node,n.Number): return node.n
    if isinstance(node,n.TrueExpr): return True
    if isinstance(node,n.FalseExpr): return False
    if isinstance(node,n.Nil): return None
    if isinstance(node,n.UMinusOp):
        x=literal(node.operand); return -x if isinstance(x,int | float) else UNKNOWN
    if isinstance(node,n.Table):
        result={};array=[]
        for field in node.fields:
            value=literal(field.value)
            if value is UNKNOWN: continue
            if field.key is None: array.append(value)
            else:
                key=field.key.id if isinstance(field.key,n.Name) else literal(field.key)
                if key is not UNKNOWN: result[key]=value
        return result if result else array
    if isinstance(node,n.AddOp | n.SubOp | n.MultOp | n.FloatDivOp | n.ExpoOp):
        a,b=literal(node.left),literal(node.right)
        if isinstance(a,int | float) and isinstance(b,int | float):
            return BINARY_OPERATORS[type(node)](a,b)
    return UNKNOWN

fields={'type','name','stack_size','fuel_value','fuel_acceleration_multiplier','fuel_top_speed_multiplier','place_result','placed_as_equipment_result','spoil_ticks','crafting_speed','mining_speed','resource_searching_radius','energy_usage','energy_consumption','energy_production','consumption','pumping_speed','rotation_speed','extension_speed','filter_count','max_belt_stack_size','bulk','inventory_size','fluid_capacity','capacity','module_slots','allowed_effects','crafting_categories','collision_box','selection_box','supply_area_distance','maximum_wire_distance','wire_max_distance','max_distance','logistics_radius','construction_radius','charging_offsets','rocket_parts_required','fixed_recipe','rocket_launch_products','minable','resource_categories','max_underground_distance','underground_distance','fluid_box','output_fluid_box','input_fluid_box','filter_count','max_energy','energy_per_move','energy_per_tick','max_to_charge','recharge_minimum','robot_slots_count','material_slots_count','charging_energy','charging_station_count','speed','max_speed','max_health','heat_buffer','neighbour_bonus','burner','energy_source','effect','distribution_effectivity','distribution_effectivity_bonus_per_quality_level','profile','target_temperature','fluid_usage_per_tick','effect_receiver','max_power_output','min_temperature','max_temperature','mining_time'}
entities={};items={};manifest={}
paths=[checkout/'base/prototypes/item.lua',checkout/'base/prototypes/equipment.lua',*sorted((checkout/'base/prototypes/entity').glob('*.lua'))]
for path in paths:
    source=path.relative_to(checkout).as_posix()
    manifest[source]=hashlib.sha256(path.read_bytes()).hexdigest()
    tree=ast.parse(path.read_text(encoding='utf-8'))
    for node in ast.walk(tree):
        if not isinstance(node,n.Table):continue
        keys={f.key.id:f.value for f in node.fields if isinstance(f.key,n.Name)}
        if 'name' not in keys or 'type' not in keys:continue
        name,typ=literal(keys['name']),literal(keys['type'])
        if not isinstance(name,str) or not isinstance(typ,str):continue
        # Only standalone entity/item records have geometry, placement or inventory metadata.
        if not any(k in keys for k in ('collision_box','selection_box','stack_size','placed_as_equipment_result','shape')):continue
        x={k:literal(v) for k,v in keys.items() if k in fields}
        x={k:v for k,v in x.items() if v is not UNKNOWN}
        for k in ('energy_source','burner','heat_buffer','effect_receiver'):
            if isinstance(x.get(k),dict):
                x[k]={a:b for a,b in x[k].items() if a in ('type','usage_priority','drain','emissions_per_minute','buffer_capacity','input_flow_limit','output_flow_limit','effectivity','max_temperature','specific_heat','max_transfer','min_working_temperature','base_effect','uses_module_effects','uses_beacon_effects')}
        x['source']=source
        x['source_line']=node.line if hasattr(node,'line') else node.first_token.line
        (items if 'stack_size' in x else entities)[name]=x
for name in ('recipe','technology','fluid','custom-inputs'):
    path=checkout/f'base/prototypes/{name}.lua';manifest[path.relative_to(checkout).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
for f in fluids:
    if f.get('auto_barrel',True):
        items[f['name']+'-barrel']={'type':'item','name':f['name']+'-barrel','stack_size':items['barrel']['stack_size'],'source':'base/data-updates.lua','generated':True}
manifest['base/data-updates.lua']=hashlib.sha256((checkout/'base/data-updates.lua').read_bytes()).hexdigest()
result=dict(provenance=dict(version='2.1.24',commit=commit,repository='https://github.com/wube/factorio-data',date='2026-10-27',method='Recipe, technology and fluid declarations evaluated with only visual icon helpers removed; barrel recipes generated from base/data-updates.lua. Entity and item numeric fields read from literal Lua tables; computed fields omitted. This is not a runtime prototype dump.',sha256=manifest),recipes=sorted(recipes,key=lambda r:r['name']),technologies=sorted(techs,key=lambda t:t['name']),fluids=fluids,entities=sorted(entities.values(),key=lambda e:e['name']),items=sorted(items.values(),key=lambda e:e['name']),custom_inputs=list(raw['custom-input'].values()))
(ROOT/'data/reference.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print({k:len(result[k]) for k in ('recipes','technologies','entities','items','fluids')})
