import argparse
import csv
import json
import shutil
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser(description='Offline browser regression checks (requires Playwright).')
parser.add_argument('--browser',choices=['chromium','firefox'],default='chromium')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
url=(root/'index.html').as_uri()
data=json.loads((root/'manual_data.json').read_text())
assert len({c['id'] for c in data['chapters']})==len(data['chapters'])
assert all(key in data['sources'] for c in data['chapters'] for key in c['sources'])
with (root/'controls.csv').open() as f:
 assert list(csv.DictReader(f))==data['controls']

with tempfile.TemporaryDirectory(prefix='factorio-manual-test-') as scratch, sync_playwright() as p:
 browser=(p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox']) if args.browser=='chromium' else p.firefox.launch(headless=True))
 context=browser.new_context(offline=True, accept_downloads=True)
 page=context.new_page()
 errors=[]; requests=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.on('request',lambda r: requests.append(r.url) if r.url.startswith(('http:', 'https:')) else None)
 page.goto(url)
 assert page.locator('h1').inner_text().startswith('Build your first')
 # Every lesson and reference renders offline.
 for route in [c['id'] for c in data['chapters']]+['home','controls','diagrams','help','glossary','whatsnew','sources']:
  page.locator('#coreNav [data-to="'+route+'"], #lessonNav [data-to="'+route+'"]').click()
  assert page.locator('h1').count()==1, route
  if route in [c['id'] for c in data['chapters']]:
   ch=next(c for c in data['chapters'] if c['id']==route)
   assert page.locator('.step').count()==len(ch['steps'])
   assert page.locator('.refs a').count()==len(ch['sources'])
 page.locator('#lessonNav [data-to="setup"]').click()
 step=page.locator('[data-check="setup:0"]')
 step.check()
 assert step.is_checked()
 assert step.evaluate('(el)=>el===document.activeElement')
 page.reload()
 assert step.is_checked()
 assert '1/140' in page.locator('#sidebarpct').inner_text()
 # Export then restore from a clean browser.
 with page.expect_download() as download_info:
  page.locator('#exportBtn').click()
 export=Path(scratch)/'progress.json';download_info.value.save_as(export)
 assert json.loads(export.read_text())['progress']['setup:0'] is True
 step.uncheck()
 dialogs=[]
 page.on('dialog',lambda d:(dialogs.append(d.message),d.accept()))
 page.locator('#importFile').set_input_files(str(export))
 page.wait_for_function('document.querySelector(\'[data-check="setup:0"]\').checked')
 for invalid in [{'manualVersion':'2.1.24','progress':[]}, {'manualVersion':'2.1.24','progress':{'setup:0':'false'}}, {'manualVersion':'other','progress':{}}, {'manualVersion':'2.1.24','progress':{'unknown:0':True}}, None]:
  with page.expect_event('dialog') as dialog_info:
   page.locator('#importFile').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':json.dumps(invalid).encode()})
  assert dialog_info.value.message.startswith('Could not import'), dialog_info.value.message
  assert step.is_checked()
 with page.expect_event('dialog') as dialog_info:
  page.locator('#importFile').set_input_files({'name':'broken.json','mimeType':'application/json','buffer':b'{broken'})
 assert dialog_info.value.message.startswith('Could not import')
 assert step.is_checked()
 # Search, category filters, empty results.
 page.locator('#coreNav [data-to="controls"]').click()
 page.locator('#lookup').fill('train')
 assert page.locator('tbody tr').count()>0
 page.locator('#lookup').fill('no-such-command-xyz')
 assert page.locator('tbody tr').count()==0
 page.locator('#lookup').fill('')
 for category in set(c['category'] for c in data['controls']):
  page.get_by_role('button',name=category,exact=True).click()
  assert page.locator('tbody tr').count()==sum(c['category']==category for c in data['controls'])
 for route,term in [('help','No path'),('glossary','block')]:
  page.locator('#coreNav [data-to="'+route+'"]').click()
  page.locator('#lookup').fill(term)
  assert term.lower() in page.locator('#content .panel').first.inner_text().lower()
 # All diagram tabs, both signal explanations, planner constraints.
 page.locator('#coreNav [data-to="diagrams"]').click()
 for button in page.locator('[data-diagram]').all():
  button.click()
  assert page.locator('#diagramPic svg').count()==1
 page.locator('[data-rail="regular"]').click()
 assert 'ENTER' in page.locator('#railOutcome').inner_text()
 page.locator('[data-rail="chain"]').click()
 assert 'WAIT' in page.locator('#railOutcome').inner_text()
 page.locator('#boilerCount').fill('10')
 assert '18 MW' in page.locator('#powerCount').inner_text()
 for value in ['0','501','1.5','']:
  page.locator('#boilerCount').fill(value)
  assert 'whole boiler count' in page.locator('#powerCount').inner_text()
 # Bad fragments, including inherited Object property names, must recover.
 for fragment in ['%','toString','__proto__','unknown']:
  page.goto(url+'#'+fragment)
  assert page.locator('h1').inner_text().startswith('Build your first')
 # Browser back navigation restores its route.
 page.goto(url+'#home')
 page.locator('#coreNav [data-to="controls"]').click()
 page.go_back()
 assert page.locator('h1').inner_text().startswith('Build your first')
 # Narrow-screen overflow check on every route.
 page.set_viewport_size({'width':375,'height':812})
 for route in [c['id'] for c in data['chapters']]+['home','controls','diagrams','help','glossary','whatsnew','sources']:
  page.goto(url+'#'+route)
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), route
 page.goto(url+'#setup')
 page.screenshot(path=str(Path(scratch)/'mobile.png'),full_page=True)
 assert not errors, errors
 assert not requests, requests
 # Denied and corrupted storage must not crash the app.
 for script in ["Storage.prototype.getItem=()=>{throw new Error('blocked')};Storage.prototype.setItem=()=>{throw new Error('blocked')}", "localStorage.setItem('factorio_2_1_24_progress',JSON.stringify([]))"]:
  ctx=browser.new_context(offline=True)
  ctx.add_init_script(script)
  pg=ctx.new_page();pg.goto(url+'#setup')
  assert pg.locator('#storageNotice').is_visible()
  pg.locator('[data-check="setup:0"]').check()
  ctx.close()
 browser.close()
print(args.browser+' PASS: 31 offline routes; progress persistence/export/import validation; keyboard focus; search/filters; diagrams; planner; bad routes; mobile overflow; blocked/corrupt storage. No JavaScript errors or network requests.')
