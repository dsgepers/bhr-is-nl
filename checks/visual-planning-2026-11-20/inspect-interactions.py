from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent;out=ROOT/'interaction-audit';out.mkdir(exist_ok=True);results={}
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1920,'height':1080},reduced_motion='reduce',locale='nl-NL');c.route('**/*',lambda r:r.abort() if r.request.method not in ['GET','HEAD','OPTIONS'] else r.continue_());page=c.new_page()
 def visit(path):
  page.goto('https://www.bhr-is.nl'+path,wait_until='domcontentloaded');page.wait_for_timeout(1000);page.evaluate("document.querySelector('button.cc-allow')?.click()");page.mouse.move(-20,-20)
 def state():return page.evaluate("""()=>({url:location.href,selected:[...document.querySelectorAll('form.Refines input')].map(e=>({value:e.value,checked:e.checked,label:e.parentElement.innerText.trim(),display:getComputedStyle(e.parentElement).display})),projects:[...document.querySelectorAll('article.Project.Item')].filter(e=>e.getBoundingClientRect().height>0&&getComputedStyle(e).display!=='none').map(e=>e.querySelector('h3')?.innerText)})""")
 visit('/projecten');results['projectsDefault']=state()
 try:
  page.locator('.titlecolumn form.Refines label').filter(has=page.locator('input[value="2"]')).first.click();page.wait_for_timeout(1400);results['projectsPaneelbouw']=state();page.screenshot(path=str(out/'projects-paneelbouw.png'),full_page=False)
 except Exception as e:results['projectsFilterError']=str(e)
 visit('/projecten')
 try:
  a=page.locator('article.Project.Item').filter(has_text='Energiebesparing door frequentieregelaars').first;a.scroll_into_view_if_needed();page.wait_for_timeout(300)
  def gallery():return a.evaluate("""e=>({slides:[...e.querySelectorAll('.projectSlider>[id]')].map(s=>({id:s.id,active:s.classList.contains('tns-slide-active'),src:s.querySelector('img')?.src})),prev:e.querySelector('.sliderPrev')?.disabled,next:e.querySelector('.sliderNext')?.disabled})""")
  states=[gallery()]
  for i in range(6):a.locator('.sliderNext').click();page.wait_for_timeout(300);states.append(gallery())
  results['galleryNextSequence']=states;page.screenshot(path=str(out/'project-gallery-selected.png'),full_page=False)
 except Exception as e:results['galleryError']=str(e)
 visit('/contact')
 try:
  trigger=page.locator('article.Employee.Item').last;trigger.scroll_into_view_if_needed();results['teamTrigger']=trigger.evaluate('e=>e.outerHTML');trigger.click();page.wait_for_timeout(1000);results['teamAfterClick']=page.evaluate("""()=>({url:location.href,dialogs:[...document.querySelectorAll('[role=dialog],.fancybox-container,.fancybox__container,.mfp-wrap,.lightbox,.popup')].map(e=>({cls:e.className,text:e.innerText.slice(0,1200)})),frames:[...document.querySelectorAll('iframe')].map(f=>({src:f.src,visible:f.getBoundingClientRect().height>0})),bodyText:document.body.innerText.slice(-2500)})""");page.screenshot(path=str(out/'contact-team-open.png'),full_page=False)
 except Exception as e:results['teamError']=str(e)
 c.close();b.close()
(out/'states.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in results.items() if k not in ['teamTrigger','galleryNextSequence']},ensure_ascii=False)[:4500])
