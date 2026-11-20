"""Native viewport menu evidence, without full-page header normalization."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
P=argparse.ArgumentParser();P.add_argument('--role',default='reference',choices=['reference','candidate']);P.add_argument('--phase',default='baseline');args=P.parse_args()
root=Path(__file__).resolve().parents[2];out=root/'checks/mobile-parity-2026-11-20'/args.phase/'states';out.mkdir(parents=True,exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844},screen={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True,user_agent='Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',reduced_motion='reduce')
 c.route('**/*',lambda r:r.abort()if r.request.method not in ['GET','HEAD','OPTIONS']else r.continue_())
 if args.role=='reference':c.add_cookies([{'name':'device','value':'mobile','domain':'www.bhr-is.nl','path':'/'},{'name':'cookieconsent_status','value':'deny','domain':'www.bhr-is.nl','path':'/'}])
 else:c.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
 page=c.new_page();page.goto('https://www.bhr-is.nl/'if args.role=='reference'else'http://localhost:4173/',wait_until='networkidle');page.evaluate('document.fonts.ready')
 def snap(name):
  page.wait_for_timeout(650);page.screenshot(path=str(out/(args.role+'-'+name+'.png')))
  data=page.evaluate("""()=>{const box=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return{cls:e.className,text:e.innerText,box:r.toJSON(),size:s.fontSize,line:s.lineHeight,padding:s.padding,margin:s.margin,color:s.color,bg:s.backgroundColor}};const r=document.querySelector('#headerFancyNav,.mobile-drawer');return{viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale},items:r?[...r.querySelectorAll('button,a,.Heading,.fancyTop,.fancyMiddle,.fancyBottom')].filter(e=>e.getBoundingClientRect().width).map(box):[]}}""")
  (out/(args.role+'-'+name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 snap('closed')
 toggle=page.locator('.FancymenuToggle').first if args.role=='reference'else page.locator('[data-mobile-open]')
 toggle.click();snap('menu')
 for title,key in [('Over BHR','about'),('Industrie','industries')]:
  if args.role=='reference':page.locator('#headerFancyNav .main button').filter(has_text=title).first.click()
  else:page.locator('[data-mobile-submenu="'+('about'if key=='about'else'industries')+'"]').click()
  snap(key)
  page.locator('#headerFancyNav .backtoarrow'if args.role=='reference'else'[data-mobile-back]').click();page.wait_for_timeout(300)
 page.locator('#headerFancyNav .FancymenuToggle'if args.role=='reference'else'[data-mobile-close]').click();page.evaluate('scrollTo(0,850)');snap('scrolled')
 (out/(args.role+'-menu.html')).write_text(page.content());b.close()
print('State captures:',args.role)
