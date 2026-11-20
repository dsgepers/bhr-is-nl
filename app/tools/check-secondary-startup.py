"""Verify valid forms cannot submit while either browser module is delayed."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from urllib.parse import urlparse
PUBLIC=Path(__file__).resolve().parent.parent/'public'
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True)
 for route in ['/contact','/offerteaanvraag','/nieuws','/test','/vacature/junior-e-plan-engineer']:
  context=browser.new_context(viewport={'width':1920,'height':1080});deliveries=[]
  def network(request):
   url=request.request.url
   if request.request.method not in ['GET','HEAD','OPTIONS']:deliveries.append(url);request.abort()
   elif urlparse(url).path.endswith('/site.mjs')or urlparse(url).path.endswith('/secondary.mjs'):
    source=PUBLIC/urlparse(url).path.rsplit('/',1)[-1];request.fulfill(status=200,content_type='application/javascript',body='await new Promise(resolve=>setTimeout(resolve,2200));\n'+source.read_text())
   else:request.continue_()
  context.route('**/*',network);page=context.new_page();page.add_init_script("localStorage.setItem('bhr-cookie-consent','accepted')")
  page.goto('http://127.0.0.1:4173'+route,wait_until='commit');form=page.locator('form[data-form-submit]').first;form.wait_for(state='attached')
  start_url=page.url;assert form.locator('button[type="submit"]').is_disabled(),route+' allows submit before binding'
  form.evaluate('''f=>{for(const e of f.elements){if(e.name==='botcheck')continue;if(e.tagName==='SELECT'){const option=[...e.options].find(o=>o.value);if(option)e.value=option.value}else if(e.type==='checkbox')e.checked=true;else if(!['hidden','file','button','submit'].includes(e.type))e.value=e.type==='email'?'example@example.com':e.type==='tel'?'0612345678':'Visual controle'} }''')
  field=form.locator('input:not([type="hidden"]):not([type="file"]):not([type="checkbox"])').first;field.focus();page.keyboard.press('Enter');page.wait_for_timeout(100)
  assert not deliveries,route+' attempted early delivery';assert page.url==start_url,route+' escaped before readiness'
  page.wait_for_function("[...document.querySelectorAll('form[data-form-submit]')].every(f=>!f.querySelector('button[type=submit]').disabled)")
  assert not deliveries;print(json.dumps({'route':route,'startup':'passed','deliveryRequests':0}),flush=True);context.close()
 browser.close()
