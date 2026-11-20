"""Verify native form-provider payloads/redirects locally. Every POST is intercepted; no email is sent."""
import argparse,json
from pathlib import Path
from email.parser import BytesParser
from email.policy import default
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--base',default='http://127.0.0.1:4173/')
parser.add_argument('--output',default='qa/forms-browser')
args=parser.parse_args();base=args.base.rstrip('/')+'/'
output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
cases=[('contact','contact','contact'),('service-en-onderhoud','quick','service'),('afspraak-maken','appointment','afspraak'),('expertises','quote','offerte'),('expertises/retrofit','quote','offerte'),('offerteaanvraag','quote','offerte'),('test','quote','offerte'),('over-ons/werken-bij','application','sollicitatie'),('vacature/junior-e-plan-engineer','application','sollicitatie'),('vacature/monteur-paneelbouw','application','sollicitatie'),('nieuws','newsletter','nieuwsbrief')]
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width,height in [(1920,1080),(430,932)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  context.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
  deliveries=[];errors=[]
  def network(route):
   request=route.request
   if request.method=='POST':
    assert request.url=='https://api.web3forms.com/submit',request.url
    mime=BytesParser(policy=default).parsebytes(('Content-Type: '+request.headers['content-type']+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+request.post_data_buffer)
    fields={};files={}
    for part in mime.iter_parts():
     name=part.get_param('name',header='content-disposition')
     if part.get_filename():files[name]={'filename':part.get_filename(),'bytes':len(part.get_payload(decode=True))}
     else:fields[name]=part.get_payload(decode=True).decode()
    deliveries.append({'fields':fields,'files':files,'method':request.method,'url':request.url})
    destination=fields['redirect']
    assert destination.startswith(base+'bedankt/')
    route.fulfill(status=303,headers={'Location':destination},body='')
   elif urlparse(request.url).netloc!=urlparse(base).netloc:route.abort()
   else:route.continue_()
  context.route('**/*',network)
  page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
  for route,kind,thanks in cases:
   count=len(deliveries)
   page.goto(base+route+'/');form=page.locator(f'[data-form-submit="{kind}"]').first
   form.locator('button[type=submit]').wait_for(state='attached')
   page.wait_for_function("[...document.querySelectorAll('[data-form-submit]')].every(f=>!f.querySelector('button[type=submit]').disabled)")
   assert form.locator('[name=redirect]').input_value()==base+'bedankt/'+thanks+'/'
   trap=form.locator('[name=botcheck]')
   assert not trap.is_visible()
   # A blank form must neither navigate nor report success.
   form.evaluate('(f)=>f.requestSubmit()');assert len(deliveries)==count
   def fill_visible():
    for control in form.locator('input,select,textarea').all():
     name=control.get_attribute('name');typ=control.get_attribute('type') or ''
     if name=='botcheck' or not control.is_visible() or typ in ['hidden','file']:continue
     if control.evaluate('(e)=>e.tagName')=='SELECT':
      if name=='birth_day':control.select_option('20')
      elif name=='birth_month':control.select_option('6')
      elif name=='birth_year':control.select_option('2000')
      else:control.evaluate("(e)=>{e.value=[...e.options].find(o=>o.value).value;e.dispatchEvent(new Event('change',{bubbles:true}))}")
     elif typ=='checkbox':control.check()
     else:control.fill('test@example.invalid' if typ=='email' else '0612345678' if typ=='tel' else 'Lokale formuliercontrole')
   while True:
    fill_visible()
    next_button=form.locator('.next-step')
    if not next_button.count() or not next_button.is_visible():break
    next_button.click()
   if form.locator('[data-step]').count():
    # Invalid earlier steps must be revealed rather than escaping native validation.
    email=form.locator('[name=email]');email.evaluate("e=>e.value=''")
    form.evaluate('(f)=>f.requestSubmit()');assert len(deliveries)==count
    assert email.is_visible();email.fill('test@example.invalid')
    while form.locator('.next-step').is_visible():form.locator('.next-step').click()
   upload=form.locator('input[type=file]')
   if upload.count():
    # Impossible dates cannot submit, even when all split controls are populated.
    form.locator('[name=birth_month]').select_option('2');form.locator('[name=birth_day]').select_option('31')
    upload.set_input_files({'name':'cv.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4 local test'})
    form.evaluate('(f)=>f.requestSubmit()');assert len(deliveries)==count
    form.locator('[name=birth_day]').select_option('20');form.locator('[name=birth_month]').select_option('6')
    upload.set_input_files({'name':'large.pdf','mimeType':'application/pdf','buffer':b'x'*(4*1024*1024+1)})
    form.evaluate('(f)=>f.requestSubmit()');assert len(deliveries)==count
    assert 'maximaal 4 MB' in form.locator('.form-status').inner_text()
    upload.set_input_files({'name':'cv.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4 local test'})
   # Honeypot must never cause a real or simulated successful submission.
   trap.evaluate('e=>e.checked=true');form.evaluate('(f)=>f.requestSubmit()');assert len(deliveries)==count
   trap.evaluate('e=>e.checked=false')
   form.locator('button[type=submit]').click()
   page.wait_for_url(base+'bedankt/'+thanks+'/')
   assert len(deliveries)==count+1
   submission=deliveries[-1];fields=submission['fields']
   assert fields['email']=='test@example.invalid' and fields['pagina'].startswith(base+route)
   assert submission['url']=='https://api.web3forms.com/submit'
   assert fields['access_key']=='87d4dc81-dc01-415e-8050-426d0824b6a0'
   assert fields['subject'] and 'botcheck' not in fields
   assert not any(field in fields for field in ['_next','_subject','_template','_honey'])
   if kind=='application':
    assert submission['files']['attachment']['filename']=='cv.pdf'
    assert fields['birthdate']=='2000-06-20'
   assert page.locator('h1').count()==1
   assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,follow'
   results.append({'route':'/'+route,'width':width,'purpose':kind,'redirect':page.url,'fields':sorted(fields),'files':submission['files'],'passed':True})
  # Capture every new design and check for horizontal overflow.
  for kind,thanks in [('contact','contact'),('quick','service'),('appointment','afspraak'),('quote','offerte'),('application','sollicitatie'),('newsletter','nieuwsbrief')]:
   page.goto(base+'bedankt/'+thanks+'/');page.evaluate('document.fonts.ready');page.wait_for_timeout(200)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(kind,width,'overflow')
   if width<768:assert page.locator('.mobile-header .mobile-brand img').get_attribute('src').endswith('/bhr-brand.svg')
   page.screenshot(path=str(output/f'{kind}-{width}.png'),full_page=True)
  assert not errors,errors
  context.close()
 browser.close()
(output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'passed':len(results),'viewports':[1920,430],'externalFormRequests':0,'output':str(output)}))
