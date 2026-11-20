from pathlib import Path
from playwright.sync_api import sync_playwright
import json
out=Path(__file__).resolve().parent/'interaction-audit';results={}
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1920,'height':1080},reduced_motion='reduce');c.route('**/*',lambda r:r.abort() if r.request.method not in ['GET','HEAD','OPTIONS'] else r.continue_());s=c.new_page()
 for path in ['/branches','/solliciteer','/expertises/paneelbouw']:
  r=s.goto('https://www.bhr-is.nl'+path,wait_until='domcontentloaded');s.wait_for_timeout(650);results[path]={'status':r.status,'url':s.url,'title':s.title(),'headings':s.locator('h1').all_text_contents()}
 s.goto('https://www.bhr-is.nl/vacature/monteur-paneelbouw',wait_until='domcontentloaded');s.wait_for_timeout(900);s.evaluate("document.querySelector('button.cc-allow')?.click()");s.locator('a.apply').first.evaluate('e=>e.click()');s.wait_for_timeout(900);results['vacancyApply']={'url':s.url,'scroll':s.evaluate('scrollY'),'forms':s.locator('article.Form.Detail').evaluate_all('es=>es.map(e=>({id:e.id,top:e.getBoundingClientRect().y,height:e.getBoundingClientRect().height}))'),'dialogs':s.locator('[role=dialog]').evaluate_all('es=>es.map(e=>({cls:e.className,text:e.innerText.slice(0,500)}))')};s.screenshot(path=str(out/'vacancy-apply.png'))
 c.close();b.close()
(out/'link-targets.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n');print(json.dumps(results,ensure_ascii=False))
