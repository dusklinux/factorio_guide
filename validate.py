"""Build-time structural and provenance checks, with no external dependencies."""
import re
from urllib.parse import urlparse

def validate(data):
    def require(condition,message):
        if not condition:raise ValueError(message)
    def unique(rows,key,label):
        ids=[r[key] for r in rows]
        require(len(ids)==len(set(ids)),f'Duplicate {label}')
        require(all(re.fullmatch(r'[a-z0-9][a-z0-9-]*',id) for id in ids),f'Invalid {label} ID')
        return set(ids)
    chapter_ids=unique(data['chapters'],'id','chapter')
    topic_ids=unique(data['topics'],'id','topic')
    ref=data['reference']
    recipe_ids=unique(ref['recipes'],'name','recipe')
    tech_ids=unique(ref['technologies'],'name','technology')
    entity_ids=unique(ref['entities'],'name','entity')
    unique(ref['items'],'name','item')
    unique(data['controls'],'id','control')
    for id,(label,url) in data['sources'].items():
        require(urlparse(url).scheme=='https' and bool(label),f'Invalid source {id}')
    phase_sequence=[]
    for c in data['chapters']:
        require(c['steps'] and c['checks'] and c['diagram'],f'Incomplete chapter {c["id"]}')
        require(set(c['topics'])<=topic_ids,f'Missing topic in {c["id"]}')
        require(set(c['sources'])<=data['sources'].keys(),f'Missing chapter source in {c["id"]}')
        if not phase_sequence or phase_sequence[-1]!=c['phase']:phase_sequence.append(c['phase'])
    require(len(phase_sequence)==len(set(phase_sequence)),'Lesson phases must stay contiguous')
    for t in data['topics']:
        require(t['summary'] and t['sections'] and t['experiment'],f'Incomplete topic {t["id"]}')
        require(set(t['sources'])<=data['sources'].keys(),f'Missing topic source in {t["id"]}')
        require(set(t['recipes'])<=recipe_ids,f'Missing topic recipe in {t["id"]}')
        require(set(t['entities'])<=entity_ids,f'Missing topic entity in {t["id"]}')
        require(set(t['related'])<=topic_ids,f'Missing related topic in {t["id"]}')
    for r in ref['recipes']:
        require(isinstance(r['energy_required'],(int,float)) and r['energy_required']>0,f'Invalid recipe time {r["name"]}')
        require(r['ingredients'] and r['results'] and r['categories'],f'Incomplete recipe {r["name"]}')
        for ingredient in r['ingredients']:
            require(ingredient.get('amount',0)>0 and ingredient['type'] in ('item','fluid'),f'Invalid ingredient {r["name"]}')
        for product in r['results']:
            require('amount' in product or 'amount_min' in product,f'Invalid output {r["name"]}')
    graph={t['name']:t['prerequisites'] for t in ref['technologies']}
    seen=set();active=set()
    def visit(id):
        require(id not in active,f'Technology prerequisite cycle at {id}')
        if id in seen:return
        require(id in graph,f'Missing prerequisite {id}')
        active.add(id)
        for pre in graph[id]:visit(pre)
        active.remove(id);seen.add(id)
    for t in ref['technologies']:
        require(isinstance(t['effects'],list) and isinstance(t['prerequisites'],list),f'Invalid technology arrays {t["name"]}')
        visit(t['name'])
        for e in t['effects']:
            if e['type']=='unlock-recipe':require(e['recipe'] in recipe_ids,f'Missing unlock {e["recipe"]}')
    for c in data['controls']:
        require(c['scope'] in ('Base','Expansion','Editor / debug'),f'Invalid control scope {c["action"]}')
        require(all(c.get(k) for k in ('key','action','context','example','pitfall','verification')),f'Incomplete control {c["action"]}')
    require(ref['provenance']['commit']=='acf5a342afcb66c066b9d88d202e8622112da117','Unpinned reference')
