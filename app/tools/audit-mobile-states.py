"""Native viewport menu evidence, without full-page header normalization."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
from mobile_evidence import build_identity,observe_served,verify_served,assert_source_theme
P=argparse.ArgumentParser();P.add_argument('--role',default='reference',choices=['reference','candidate']);P.add_argument('--phase',default='baseline');P.add_argument('--mode',choices=['mobile','tablet'],default='mobile');args=P.parse_args()
root=Path(__file__).resolve().parents[2];out=root/'checks/mobile-parity-2026-11-20'/args.phase/'states';out.mkdir(parents=True,exist_ok=True)
expected=build_identity(root)
with sync_playwright()as p:
 w,h=(768,1024)if args.mode=='tablet'else(390,844)
 ua='Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1'if args.mode=='tablet'else'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
 b=p.chromium.launch();c=b.new_context(viewport={'width':w,'height':h},screen={'width':w,'height':h},device_scale_factor=1,is_mobile=args.mode!='tablet',has_touch=True,user_agent=ua,reduced_motion='reduce')
 c.route('**/*',lambda r:r.abort()if r.request.method not in ['GET','HEAD','OPTIONS']else r.continue_())
 if args.role=='reference':c.add_cookies([{'name':'device','value':args.mode,'domain':'www.bhr-is.nl','path':'/'},{'name':'cookieconsent_status','value':'deny','domain':'www.bhr-is.nl','path':'/'}])
 else:c.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
 page=c.new_page();served=observe_served(page)if args.role=='candidate'else[];page.goto('https://www.bhr-is.nl/'if args.role=='reference'else'http://localhost:4173/',wait_until='networkidle');page.evaluate('document.fonts.ready');page.add_style_tag(content='#banner_header>.tns-item{opacity:0!important;visibility:hidden!important}#banner_header>#banner_header-item0{opacity:1!important;visibility:visible!important;left:0!important;z-index:2!important}.home .slide{opacity:0!important;visibility:hidden!important}.home .slide[data-slide="0"]{opacity:1!important;visibility:visible!important;z-index:2!important}')
 def snap(name):
  page.wait_for_timeout(650);page.screenshot(path=str(out/(args.role+'-'+name+'.png')))
  data=page.evaluate("""()=>{const box=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return{cls:e.className,text:e.innerText,box:r.toJSON(),size:s.fontSize,line:s.lineHeight,padding:s.padding,margin:s.margin,color:s.color,bg:s.backgroundColor}};const r=document.querySelector('#headerFancyNav,.mobile-drawer');return{viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale},items:r?[...r.querySelectorAll('button,a,.Heading,.fancyTop,.fancyMiddle,.fancyBottom')].filter(e=>e.getBoundingClientRect().width).map(box):[]}}""")
  assert data['viewport']['width']==w and data['viewport']['height']==h and data['viewport']['dpr']==1 and data['viewport']['scale']==1,data['viewport']
  data['normalization']='Native viewport, fixed first hero image on both sides; no full-page tiling or masks'
  data['styles']=page.evaluate('[...document.styleSheets].map(s=>s.href)')
  if args.role=='reference':assert_source_theme(data['styles'],args.mode)
  else:
   assert build_identity(root)==expected,'candidate build changed'
   data['buildRevision']=expected;data['servedResources']=verify_served(served,root)
  (out/(args.role+'-'+name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 snap('closed')
 toggle=page.locator('.FancymenuToggle').first if args.role=='reference'else page.locator('[data-mobile-open]')
 toggle.click();snap('menu')
 for title,key in [('Over BHR','about'),('Industrie','industries')]:
  if args.role=='reference':page.locator('#headerFancyNav .main button').filter(has_text=title).first.click()
  else:page.locator('[data-mobile-submenu="'+('about'if key=='about'else'industries')+'"]').click()
  snap(key)
  if args.mode=='tablet':
   page.locator('#headerFancyNav .FancymenuToggle'if args.role=='reference'else'[data-mobile-close]').click();page.wait_for_timeout(300);toggle.click()
  else:page.locator('#headerFancyNav .backtoarrow'if args.role=='reference'else'[data-mobile-back]').click()
  page.wait_for_timeout(300)
 page.locator('#headerFancyNav .FancymenuToggle'if args.role=='reference'else'[data-mobile-close]').click();page.evaluate('scrollTo(0,850)');snap('scrolled')
 (out/(args.role+'-menu.html')).write_text(page.content());b.close()
print('State captures:',args.role)
