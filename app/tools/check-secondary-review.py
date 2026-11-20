"""Regression cases from the one final review. No form or share action is sent."""
import json
from playwright.sync_api import sync_playwright
results=[]
with sync_playwright()as p:
 browser=p.chromium.launch()
 def context(width=1920,height=1080):
  c=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce');c.route('**/*',lambda r:r.abort()if r.request.method not in ['GET','HEAD','OPTIONS']else r.continue_());c.add_init_script("localStorage.setItem('bhr-cookie-consent','accepted')");return c
 def run(name,fn):
  try:fn();results.append({'test':name,'result':'passed'})
  except Exception as e:results.append({'test':name,'result':'failed','error':str(e)})
 def project_rows():
  for w,h in [(1920,1080),(1440,900),(768,1024),(390,844)]:
   c=context(w,h);page=c.new_page();page.goto('http://127.0.0.1:4173/projecten');page.evaluate('document.fonts.ready');page.evaluate('Promise.all([...document.images].map(e=>e.decode().catch(()=>{})))')
   row=page.locator('.secondary-project-row').first;copy=row.locator('.secondary-prose p').first
   styles=copy.evaluate('(e)=>({size:getComputedStyle(e).fontSize,line:getComputedStyle(e).lineHeight})');assert styles=={'size':'18px','line':'30.6px'},f'{w}: {styles}'
   assert row.evaluate('(e)=>getComputedStyle(e).flexDirection')=='row',f'{w}: rows must remain horizontal'
   photo=row.locator('.secondary-project-gallery').bounding_box();text=row.locator('.secondary-project-copy').bounding_box();assert text['x']>photo['x']+photo['width'],f'{w}: copy must be beside photo'
   c.close()
 def recipients():
  for route in ['/vacature/junior-e-plan-engineer','/vacature/monteur-paneelbouw']:
   c=context();page=c.new_page();page.goto('http://127.0.0.1:4173'+route)
   apply=page.locator('.secondary-job-title .secondary-actions a').filter(has_text='Whatsapp');assert apply.get_attribute('href')=='https://wa.me/31162238834',route+' application recipient'
   assert page.locator('.secondary-employee .secondary-whatsapp').get_attribute('href')=='https://wa.me/31640236948',route+' sidebar contact'
   c.close()
 def sidebar():
  c=context();page=c.new_page();page.goto('http://127.0.0.1:4173/vacature/monteur-paneelbouw');page.evaluate('document.fonts.ready');page.evaluate('Promise.all([...document.images].map(e=>e.decode().catch(()=>{})))');aside=page.locator('.secondary-job-description>.secondary-container>aside')
  assert aside.evaluate('(e)=>getComputedStyle(e).position')=='sticky','outer contact aside must be sticky'
  for y in [1500,1900,1500]:
   page.evaluate('(y)=>scrollTo(0,y)',y);page.wait_for_timeout(100);box=aside.bounding_box();bar=page.locator('[data-job-sticky]').bounding_box();assert box['y']>=bar['y']+bar['height']+30 and box['y']<350,(y,box,bar)
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100);assert page.locator('[data-job-sticky]').is_hidden();assert aside.bounding_box()['y']>1000;c.close()
 def sharing():
  for route in ['/vacature/junior-e-plan-engineer','/vacature/monteur-paneelbouw']:
   c=context();page=c.new_page();page.goto('http://127.0.0.1:4173'+route);share=page.locator('[data-job-share]');assert share.count()==1,route+' Delen disclosure'
   summary=share.locator('summary');summary.focus();page.keyboard.press('Enter');assert share.get_attribute('open')is not None
   links=share.locator('a');assert links.count()==5;assert links.all_text_contents()==['Twitter','Facebook','LinkedIn','Pinterest','E-mail']
   for a in links.all():
    href=a.get_attribute('href');assert href.startswith(('https://','mailto:')) and route.split('/')[-1]in href,(route,href)
    if a.get_attribute('target')=='_blank':assert 'noopener'in a.get_attribute('rel')
   page.keyboard.press('Escape');assert share.get_attribute('open')is None;c.close()
 def search_retry():
  c=context();requests=[]
  def index(r):
   requests.append(r.request.url);r.fulfill(status=503,body='unavailable')if len(requests)==1 else r.fulfill(status=200,content_type='application/json',body=json.dumps([{'url':'/expertises/paneelbouw','title':'Paneelbouw','text':'Paneelbouw expertise'}]))
  c.route('**/search-index.json',index);page=c.new_page();page.goto('http://127.0.0.1:4173/zoeken');form=page.locator('[data-secondary-search]');form.locator('input').fill('paneelbouw');form.locator('button[type=submit]').click();page.wait_for_function("document.querySelector('[data-secondary-results]').textContent.includes('tijdelijk')")
  form.locator('button[type=submit]').click();page.wait_for_timeout(300);assert len(requests)==2,'rejected cached request must be retried';assert page.locator('[data-secondary-results] article').count()==1;c.close()
 for name,fn in [('project row source typography/direction at4 widths',project_rows),('separate recruitment and sidebar recipients',recipients),('vacancy sidebar forward/back scroll',sidebar),('vacancy share disclosure/keyboard/destinations',sharing),('search recovers after transient503',search_retry)]:run(name,fn)
 browser.close()
for r in results:print(json.dumps(r))
raise SystemExit(any(r['result']!='passed'for r in results))
