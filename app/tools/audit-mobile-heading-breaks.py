"""Record rendered phone heading breaks; the CMS hides some authored br tags."""
import concurrent.futures,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20'
routes=[r for r in json.loads((BASE/'routes.json').read_text())if (BASE/'baseline'/r['key']/'mobile/reference.html').exists()and any('<br' in h for _,h in re.findall(r'<h([1-4])\b[^>]*>([\s\S]*?)</h\1>',(BASE/'baseline'/r['key']/'mobile/reference.html').read_text()))]
def capture(r):
 with sync_playwright()as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844},screen={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1,user_agent='Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/131.0.0.0 Mobile Safari/537.36',reduced_motion='reduce');c.add_cookies([{'name':'device','value':'mobile','domain':'www.bhr-is.nl','path':'/'},{'name':'cookieconsent_status','value':'deny','domain':'www.bhr-is.nl','path':'/'}]);page=c.new_page();page.goto('https://www.bhr-is.nl'+r['route'],wait_until='domcontentloaded');page.wait_for_timeout(1000);page.evaluate('document.fonts.ready')
  assert page.evaluate("[...document.styleSheets].some(s=>(s.href||'').includes('corporate-mobile'))")
  data=page.evaluate('''()=>[...document.querySelectorAll('.maincontainer h1,.maincontainer h2,.maincontainer h3,.maincontainer h4')].filter(h=>h.querySelector('br')).map(h=>{const chunks=[];const walk=n=>{if(n.nodeType===3)chunks.push(n.textContent);else if(n.nodeName==='BR')chunks.push(getComputedStyle(n).display==='none'?' ':'\\nBREAK\\n');else n.childNodes.forEach(walk)};walk(h);const parts=chunks.join('').split('\\nBREAK\\n').map(t=>t.replace(/\\s+/g,' ').trim()).filter(Boolean);return{text:parts.join(' '),parts,breaks:[...h.querySelectorAll('br')].map(e=>getComputedStyle(e).display)}})''');b.close();print(r['route'],len(data),flush=True);return r['route'],data
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:data=dict(pool.map(capture,routes))
(BASE/'heading-breaks.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
