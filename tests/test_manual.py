"""Real browser regression checks against the standalone file URL, offline."""
import argparse
import json
import shutil
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--browser',choices=['chromium','firefox'],default='chromium')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
url=(root/'index.html').as_uri()
data=json.loads((root/'manual_data.json').read_text())
base_routes=['home','search','library','controls','recipes','technology','machines','calculator','diagrams','help','glossary','whatsnew','sources','audit']
lesson_routes=[c['id'] for c in data['chapters']]
topic_routes=['topic/'+t['id'] for t in data['topics']]
data_routes=[kind+'/'+r['name'] for kind,key in [('recipe','recipes'),('tech','technologies'),('entity','entities'),('item','items'),('fluid','fluids')] for r in data['reference'][key]]
all_routes=base_routes+lesson_routes+topic_routes+data_routes

with tempfile.TemporaryDirectory(prefix='factorio-browser-test-') as scratch, sync_playwright() as p:
    browser=(p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox']) if args.browser=='chromium' else p.firefox.launch(headless=True))
    context=browser.new_context(offline=True,accept_downloads=True,viewport={'width':1440,'height':1000})
    page=context.new_page();errors=[];requests=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda request:requests.append(request.url) if request.url.startswith(('http:','https:')) else None)
    page.goto(url)
    assert page.locator('h1').inner_text().startswith('Build your first')
    def go(path):
        page.goto(url+'#'+path)
        expected=path.split('?')[0]
        page.wait_for_function('(expected)=>route===expected',arg=expected)
    # Real navigation through all reference entry points and original lessons.
    for path in base_routes+lesson_routes:
        page.locator('.side [data-to="'+path+'"]').click()
        page.wait_for_function('(expected)=>route===expected',arg=path)
        assert page.locator('h1').count()==1,path
        if path in lesson_routes:
            chapter=next(c for c in data['chapters'] if c['id']==path)
            assert page.locator('.step').count()==len(chapter['steps'])
            assert page.locator('.refs a').count()==len(chapter['sources'])
    # Every article/data-detail route must render, not just the first page of each catalogue.
    failures=page.evaluate('''paths=>{const failures=[];for(const path of paths){route=path;render();const h=document.querySelectorAll('#content h1');if(h.length!==1||!h[0].textContent)failures.push(path);for(const a of document.querySelectorAll('#content [data-to]')){const target=a.dataset.to.split('?')[0];const [type,id]=target.split('/');if(!coreLinks.some(([key])=>key===target)&&!maps.chapter.has(target)&&!maps[type]?.has(id))failures.push(path+' -> '+target)}}return failures}''',topic_routes+data_routes)
    assert not failures,failures[:10]
    page.reload();go('setup')
    checkbox=page.locator('[data-check="setup:0"]')
    checkbox.check();assert checkbox.evaluate('(el)=>el===document.activeElement')
    page.reload();assert checkbox.is_checked();assert '1/140' in page.locator('#sidebarpct').inner_text()
    # Reading preferences persist, step mode preserves whole-lesson print access.
    page.locator('.reading-settings summary').click()
    page.locator('#textSize').select_option('115');page.locator('#highContrast').check();page.locator('#stepMode').check()
    assert page.locator('.step:visible').count()==1
    shown=int(page.locator('.step:visible .number').inner_text().rstrip('.'))
    page.get_by_role('button',name='Next step →',exact=True).click()
    assert page.locator('.step:visible .number').inner_text()==str(shown+1)+'.'
    page.evaluate("dispatchEvent(new Event('beforeprint'))")
    assert page.locator('.step:visible').count()==5
    page.evaluate("dispatchEvent(new Event('afterprint'))")
    assert page.locator('.step:visible').count()==1
    page.reload();assert page.locator('body').evaluate('(el)=>el.classList.contains("high-contrast")')
    assert page.locator('#textSize').input_value()=='115'
    # Export and restore, including old edition exports and all-or-nothing validation.
    with page.expect_download() as info:page.locator('#exportBtn').click()
    exported=Path(scratch)/'progress.json';info.value.save_as(exported)
    assert json.loads(exported.read_text())['progress']['setup:0'] is True
    dialogs=[]
    page.on('dialog',lambda dialog:(dialogs.append(dialog.message),dialog.accept()))
    def import_json(value,name='progress.json'):
        with page.expect_event('dialog') as info:
            page.locator('#importFile').set_input_files({'name':name,'mimeType':'application/json','buffer':json.dumps(value).encode()})
        return info.value.message
    assert import_json({'manualVersion':'2.1.24','progress':{'setup:0':False}})=='Progress imported.'
    assert not checkbox.is_checked()
    assert import_json(json.loads(exported.read_text()))=='Progress imported.'
    assert checkbox.is_checked()
    for invalid in [None,{}, {'manualVersion':'2.1.24','progress':[]},{'manualVersion':'2.1.24','progress':{'setup:0':'false'}},{'manualVersion':'other','progress':{}},{'manualVersion':'2.1.24','progress':{'missing:0':True}},{'manualVersion':'2.1.24','progress':{'setup:0':False},'preferences':{'textSize':'900'}}]:
        assert import_json(invalid).startswith('Could not import')
        assert checkbox.is_checked()
    with page.expect_event('dialog') as info:
        page.locator('#importFile').set_input_files({'name':'broken.json','mimeType':'application/json','buffer':b'{broken'})
    assert info.value.message.startswith('Could not import')
    # Return to standard reading settings for viewport and functional checks.
    if not page.locator('#stepMode').is_visible():page.locator('.reading-settings summary').click()
    page.locator('#textSize').select_option('100');page.locator('#highContrast').uncheck();page.locator('#stepMode').uncheck()
    go('controls');page.locator('#lookup').fill('Q')
    assert page.locator('.control-card').count()==1
    assert 'Pipette' in page.locator('.control-card').inner_text()
    page.locator('#lookup').fill('');page.locator('#levelFilter').select_option('Essential')
    assert 5<page.locator('.control-card').count()<len(data['controls'])
    page.locator('#levelFilter').select_option('All')
    for scope in ['Base','Expansion','Editor / debug','All']:
        page.locator('#scopeFilter').select_option(scope)
        assert page.locator('.control-card').count()==sum(c['scope']==scope or scope=='All' for c in data['controls'])
    page.locator('#scopeFilter').select_option('Base')
    page.locator('#lookup').fill('no-such-command-xyz');assert page.locator('.control-card').count()==0
    # Search respects live input focus and searches the complete dataset.
    go('library');page.locator('#lookup').fill('oil');assert page.locator('#results .card').count()>0
    assert page.locator('#lookup').evaluate('(el)=>el===document.activeElement')
    for term,kind in [('Q','Control'),('satellite','Recipe'),('No path','Troubleshooting'),('Kovarex','Topic'),('pollution','Topic')]:
        page.locator('#globalQuery').fill(term);page.locator('#globalSearch button').click()
        page.wait_for_function('route==="search"')
        assert kind in page.locator('#results').inner_text(),term
    go('search?q=science')
    before=page.locator('#results article.result').count()
    page.locator('[data-more]').focus();page.keyboard.press('Enter')
    assert page.locator('#results article.result').count()>before
    assert page.locator('#results article.result').nth(before).locator('a').first.evaluate('(el)=>el===document.activeElement')
    # Clicking encoded search links must preserve query and scope.
    go('search?q=Prototype%20explorer')
    page.locator('#results a').filter(has_text='Prototype explorer').first.click()
    page.wait_for_function('route==="controls"')
    assert page.locator('.control-card').count()==1
    assert page.locator('#scopeFilter').input_value()=='Editor / debug'
    page.evaluate("nav('controls?q=Prototype%20explorer&scope=Editor%20%2F%20debug')")
    assert page.locator('h1').inner_text()=='Find a shortcut by task and context'
    assert page.locator('#lookup').input_value()=='Prototype explorer'
    assert page.locator('#scopeFilter').input_value()=='Editor / debug'
    assert page.locator('.control-card').count()==1
    for path,term in [('recipes','processing-unit'),('technology','rocket-silo'),('machines','roboport'),('help','No path'),('glossary','catalyst')]:
        go(path);page.locator('#lookup').fill(term)
        assert page.locator('#results').inner_text().strip()
    go('recipes');before=page.locator('.record').count();page.locator('[data-more]').focus();page.keyboard.press('Enter');assert page.locator('.record').count()>before
    assert page.locator('.record').nth(before).locator('a').first.evaluate('(el)=>el===document.activeElement')
    # Calculator code against independently known quantities.
    go('calculator')
    known=page.evaluate('''()=>{
      const circuit=calculateProduction(maps.recipe.get('electronic-circuit'),{speed:.75,quantity:120,productName:'electronic-circuit',machine:maps.entity.get('assembling-machine-2')});
      const uranium=calculateProduction(maps.recipe.get('uranium-processing'),{speed:1,quantity:1,mode:'machines',productName:'uranium-235',machine:maps.entity.get('centrifuge')});
      const kov=maps.recipe.get('kovarex-enrichment-process');
      const rocket=rocketBudget(1,0,false),productive=rocketBudget(1,.4,false);
      return {machines:circuit.machines,iron:circuit.inputs.find(p=>p.name==='iron-plate').rate,cable:circuit.inputs.find(p=>p.name==='copper-cable').rate,u235:uranium.outputs[0].rate*60,kov235:expectedOutput(kov.results[0],.4),kov238:expectedOutput(kov.results[1],.4),rocket:Object.fromEntries(rocket.totals),crafts:productive.crafts,productive:Object.fromEntries(productive.totals)}
    }''')
    assert abs(known['machines']-4/3)<1e-9
    assert known['iron']==2 and known['cable']==6
    assert abs(known['u235']-.035)<1e-9
    assert known['kov235']==41.4 and known['kov238']==2
    assert known['rocket']['processing-unit']==1100 and known['rocket']['rocket-fuel']==1050
    assert known['crafts']==72 and known['productive']['processing-unit']==820
    page.locator('#calcRecipe').select_option('chemical-science-pack')
    page.locator('#calcMachine').select_option('assembling-machine-2')
    page.locator('#calcQuantity').fill('30');assert '8 ideal machines' in page.locator('#productionResult').inner_text()
    page.locator('#calcQuantity').fill('0');assert 'positive finite' in page.locator('#productionResult').inner_text()
    page.locator('#calcQuantity').fill('30');page.locator('#calcProductivity').fill('999');assert 'recipe limit' in page.locator('#productionResult').inner_text()
    page.locator('#calcProductivity').fill('40');assert 'at most 20%' in page.locator('#productionResult').inner_text()
    page.locator('#calcProductivity').fill('0')
    go('recipe/satellite');page.get_by_role('link',name='Open production calculator').click()
    page.wait_for_function('route==="calculator"')
    assert page.locator('#calcRecipe').input_value()=='satellite'
    page.evaluate("nav('calculator?recipe=satellite')")
    assert page.locator('#calcRecipe').input_value()=='satellite'
    page.locator('#siloProductivity').fill('40');assert '72 normal' in page.locator('#rocketResult').inner_text()
    # All visual interactions and keyboard-operable understanding checks.
    go('diagrams')
    for el in page.locator('[data-diagram]').all():el.click();assert page.locator('#diagramPic svg').count()==1
    page.locator('[data-expand-diagram]').first.click();assert page.locator('#diagramDialog').is_visible()
    page.keyboard.press('Escape');assert not page.locator('#diagramDialog').is_visible()
    page.locator('[data-rail="regular"]').click();assert 'ENTER' in page.locator('#railOutcome').inner_text()
    page.locator('[data-rail="chain"]').click();assert 'WAIT' in page.locator('#railOutcome').inner_text()
    page.locator('#boilerCount').fill('10');assert '18 MW' in page.locator('#powerCount').inner_text()
    for value in ['0','501','1.5','']:
        page.locator('#boilerCount').fill(value);assert 'whole boiler count' in page.locator('#powerCount').inner_text()
    page.locator('[data-quiz="lane"][data-choice="1"]').click();assert 'Correct' in page.locator('#quiz-lane').inner_text()
    # Invalid routes must recover without inherited-property dispatch or decode crashes.
    for path in ['%','__proto__','constructor','toString','topic/missing','recipe/missing']:
        page.goto(url+'#'+path);page.wait_for_function('route==="home"')
        assert page.locator('h1').inner_text().startswith('Build your first')
    go('home');page.locator('.side [data-to="controls"]').click();page.go_back();page.wait_for_function('route==="home"')
    # Check every route for mobile overflow with normal and enlarged text.
    for width,text_size in [(375,'100'),(375,'130'),(820,'100')]:
        page.set_viewport_size({'width':width,'height':900})
        overflows=page.evaluate('''({paths,size})=>{prefs.textSize=size;applyPreferences();const bad=[];for(const path of paths){route=path;render();if(document.documentElement.scrollWidth>innerWidth+1)bad.push({path,width:document.documentElement.scrollWidth})}return bad}''',{'paths':all_routes,'size':text_size})
        if overflows:
            page.evaluate('(path)=>{route=path;render()}',overflows[0]['path'])
            page.screenshot(path=str(Path(scratch)/'overflow.png'),full_page=True)
        assert not overflows,(width,text_size,overflows[:12])
    page.set_viewport_size({'width':1440,'height':1000});page.evaluate("prefs.textSize='100';applyPreferences()")
    page.reload();go('home')
    if args.browser=='chromium':page.screenshot(path=str(root/'preview.png'),full_page=True)
    go('topic/oil-balancing')
    if args.browser=='chromium':page.screenshot(path=str(root/'screenshot.png'),full_page=True)
    assert not errors,errors
    assert not requests,requests
    # Denied/corrupt storage: usable content and explicit export advice.
    for script in ["Storage.prototype.getItem=()=>{throw new Error('blocked')};Storage.prototype.setItem=()=>{throw new Error('blocked')}","localStorage.setItem('factorio_2_1_24_progress','[]')"]:
        ctx=browser.new_context(offline=True);ctx.add_init_script(script);pg=ctx.new_page();pg.goto(url+'#setup')
        assert pg.locator('#storageNotice').is_visible()
        pg.locator('[data-check="setup:0"]').check();assert pg.locator('[data-check="setup:0"]').is_checked();ctx.close()
    browser.close()
print(f'{args.browser} PASS: {len(all_routes)} offline routes; all links; persistent progress and preferences; old/new imports; search and scope filters; numerical calculators; diagrams and quizzes; print state; invalid hashes; mobile and enlarged-text layout. No JavaScript errors or network requests.')
