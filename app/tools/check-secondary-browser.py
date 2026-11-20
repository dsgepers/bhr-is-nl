"""Exercise authored secondary controls locally; never deliver a form."""
import argparse,json
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--route',action='append',required=True);args=p.parse_args()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for route in args.route:
  context=browser.new_context(viewport={'width':1920,'height':1080},reduced_motion='reduce');requests=[];errors=[]
  def network(r):
   if r.request.url.endswith('/config.js') and route in ['/nieuws','/test']:r.fulfill(status=200,content_type='application/javascript',body="window.BHR_CONFIG={staticFormsKey:'dummy-key-must-never-send',formKeys:{}};")
   elif r.request.method not in ['GET','HEAD','OPTIONS']:requests.append(r.request.url);r.abort()
   else:r.continue_()
  context.route('**/*',network);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script("if(!localStorage.getItem('bhr-cookie-consent'))localStorage.setItem('bhr-cookie-consent','accepted')")
  page.goto('http://127.0.0.1:4173'+route);page.wait_for_timeout(200);page.evaluate('Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))')
  assert page.locator('h1').count()==1,route+' must expose one main heading'
  assert page.locator('img').evaluate_all('(els)=>els.filter(e=>e.hasAttribute("src")).every(e=>e.complete&&e.naturalWidth>0)'),route+' has broken images'
  if page.locator('[data-local-only-form]').count():
   page.evaluate("window.BHR_CONFIG={staticFormsKey:'dummy-key-must-never-send'}")
   for form in page.locator('[data-local-only-form]').all():
    assert 'static-form' not in (form.get_attribute('class') or '').split()
    assert form.locator('button[type="submit"]').is_enabled(),'local-only handler must enable only after binding'
    if form.get_attribute('data-local-wizard') is not None:
     for _ in range(2):form.locator('.next-step').click()
     assert form.locator('[data-step="2"]').is_visible()
     for name in ['company','name','email','phone']:
      form.locator('[name="'+name+'"]').fill('example@example.com' if name=='email' else '0612345678' if name=='phone' else 'Visual controle')
     form.locator('[name="privacy"]').check()
    else:form.locator('[name="email"]').fill('example@example.com')
    form.locator('button[type="submit"]').click();assert form.locator('.form-status').inner_text()=='Dit formulier is nog niet aangesloten.'
  if page.locator('[data-secondary-search]').count():
   form=page.locator('[data-secondary-search]');form.locator('input').fill('paneelbouw');form.locator('button[type="submit"]').click()
   page.wait_for_function("document.querySelector('[data-secondary-results] article')")
   assert 'search=paneelbouw' in page.url
   form.locator('input').fill('<none>&geenresultaat');form.locator('button[type="submit"]').click();page.wait_for_timeout(150)
   assert 'Geen resultaten' in page.locator('[data-secondary-results]').inner_text()
   form.locator('[data-search-clear]').click();assert page.locator('[data-secondary-results]').inner_text()==''
  if page.locator('[data-secondary-cookies]').count():
   form=page.locator('[data-secondary-cookies]');assert form.locator('[name="necessary"]').is_checked() and form.locator('[name="necessary"]').is_disabled()
   form.locator('[name="analytics"]').uncheck();form.locator('button[type="submit"]').first.click();page.reload()
   assert not page.locator('[data-secondary-cookies] [name="analytics"]').is_checked()
   page.locator('[data-cookie-all]').first.click();assert page.locator('[data-secondary-cookies] [name="analytics"]').is_checked()
  for carousel in page.locator('[data-carousel="steps"]').all():
   next_button=carousel.locator('[data-carousel-next]');track=carousel.locator('[data-carousel-track]')
   if next_button.count() and next_button.is_enabled() and track.locator(':scope > *').count()>1:
    carousel.scroll_into_view_if_needed();before=track.evaluate('(e)=>e.style.transform');next_button.click();after=track.evaluate('(e)=>e.style.transform')
    assert before!=after,'process next control must advance its track'
    carousel.locator('[data-carousel-prev]').click();assert track.evaluate('(e)=>e.style.transform')==before
  for timeline in page.locator('[data-secondary-timeline]').all():
   timeline.scroll_into_view_if_needed();track=timeline.locator('[data-timeline-track]');timeline.locator('[data-timeline-index="1"]').focus();page.keyboard.press('Enter')
   assert timeline.locator('[data-timeline-index="1"]').get_attribute('aria-pressed')=='true'
   assert track.evaluate('(e)=>e.style.transform')!='translateX(0px)'
   for _ in range(9):timeline.locator('[data-timeline-next]').click(force=True)
   assert timeline.locator('[data-timeline-index="7"]').get_attribute('aria-pressed')=='true'
   assert timeline.locator('[data-timeline-next]').is_disabled()
   timeline.locator('[data-timeline-index="0"]').click();assert timeline.locator('[data-timeline-prev]').is_disabled()
  for details in page.locator('.secondary-faq details').all()[:1]:
   question=details.locator('summary').inner_text();details.locator('summary').focus();page.keyboard.press('Enter');assert details.get_attribute('open') is not None
   assert details.locator('summary').inner_text()==question and details.locator('.secondary-prose').is_visible()
  for card in page.locator('.secondary-team-card').all():
   overlay=card.locator('.secondary-team-overlay');overlay.focus();assert overlay.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
  if route.split('?')[0]=='/projecten':
   controls=page.locator('[data-project-filter]');assert controls.count()==4
   controls.filter(has=page.locator('none')) if False else None
   page.locator('[data-project-filter][value="2"]').first.check(force=True)
   assert 'filter_projectgroup%5B%5D=2' in page.url,'filter must update source query'
   assert page.locator('.secondary-project-row:visible').count()==4
   assert page.locator('[data-project-filter][value="2"]:checked').count()==2
   page.locator('[data-project-reset]').first.click();assert page.locator('.secondary-project-row:visible').count()==8
   page.go_back();assert page.locator('.secondary-project-row:visible').count()==4
   page.go_forward();assert page.locator('.secondary-project-row:visible').count()==8
   gallery=page.locator('[data-project-gallery]').nth(3);gallery.scroll_into_view_if_needed()
   for _ in range(6):gallery.locator('[data-project-next]').click()
   assert gallery.locator('[data-project-thumb="4"]').get_attribute('aria-pressed')=='true'
   for _ in range(6):gallery.locator('[data-project-prev]').click()
   assert gallery.locator('[data-project-thumb="0"]').get_attribute('aria-pressed')=='true'
   gallery.locator('[data-project-thumb="2"]').focus();page.keyboard.press('Enter')
   assert gallery.locator('[data-project-thumb="2"]').get_attribute('aria-pressed')=='true'
   page.evaluate('scrollTo(0,1200)');page.wait_for_timeout(100);assert page.locator('[data-project-sticky]').is_visible()
  for form in page.locator('.static-form').all():
   assert not form.evaluate('(f)=>f.checkValidity()'),'empty form must be invalid'
   if form.locator('[name="message"]').count():assert form.locator('[name="message"]').get_attribute('required') is None
   privacy=form.locator('[name="privacy"]');assert not privacy.is_checked() and privacy.get_attribute('required') is not None
   for name in ['company','name','email','phone']:
    field=form.locator('[name="'+name+'"]')
    if field.count():field.fill('example@example.com' if name=='email' else '0612345678' if name=='phone' else 'Visual controle')
   if form.locator('[name="firstname"]').count():
    form.locator('[name="firstname"]').fill('Visual');form.locator('[name="lastname"]').fill('Controle')
    for name,value in [('birth_day','1'),('birth_month','1'),('birth_year','2000')]:form.locator('[name="'+name+'"]').select_option(value)
    form.locator('[name="bewaren"]').check();form.locator('[name="cv"]').set_input_files({'name':'controle.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4 visual check'})
    assert form.locator('[name="birthdate"]').input_value()=='2000-01-01'
   if form.locator('[data-step]').count():
    for _ in range(form.locator('[data-step]').count()-1):
     for select in form.locator('[data-step]:visible select[required]').all():
      options=select.locator('option').all();option=next(o for o in options if o.get_attribute('value')!='' and o.inner_text());select.select_option(label=option.inner_text())
     form.locator('.next-step').click()
   privacy.check();assert form.evaluate('(f)=>f.checkValidity()')
   form.locator('button[type="submit"]').click();page.wait_for_timeout(100)
   assert 'tijdelijk niet beschikbaar' in form.locator('.form-status').inner_text()
  assert not requests,'attempted delivery '+str(requests)
  assert not errors,'browser errors '+str(errors)
  print(json.dumps({'route':route,'result':'passed','deliveryRequests':len(requests)}),flush=True);context.close()
 browser.close()
