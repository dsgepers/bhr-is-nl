"""Browser regressions for mobile parity; never deliver a form."""
import argparse,json,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
P=argparse.ArgumentParser();P.add_argument('--case',choices=['nav','layout','all'],default='all');P.add_argument('--route',action='append');P.add_argument('--mode',choices=['phone','tablet'],default='phone');P.add_argument('--width',type=int);args=P.parse_args()

class MobileTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop()
 def setUp(self):
  self.width=args.width or (768 if args.mode=='tablet'else 390)
  self.context=self.browser.new_context(viewport={'width':self.width,'height':1024 if args.mode=='tablet'else 844},screen={'width':self.width,'height':1024 if args.mode=='tablet'else 844},device_scale_factor=1,is_mobile=args.mode!='tablet',has_touch=True,reduced_motion='reduce')
  self.context.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
  self.deliveries=[]
  def guard(r):
   if r.request.method not in ['GET','HEAD','OPTIONS']:self.deliveries.append(r.request.url);r.abort()
   else:r.continue_()
  self.context.route('**/*',guard);self.page=self.context.new_page();self.page.set_default_timeout(4000)
 def tearDown(self):self.assertEqual(self.deliveries,[]);self.context.close()
 def go(self,route='/'):
  self.page.goto('http://localhost:4173'+route,wait_until='networkidle');self.page.evaluate('document.fonts.ready')
 def test_nav_scroll_submenus_focus_escape(self):
  self.go();page=self.page;self.assertEqual(page.locator('.mobile-header').count(),1)
  page.evaluate('scrollTo(0,850)');page.locator('[data-mobile-open]').click();expect(page.locator('.mobile-drawer')).to_be_visible()
  self.assertEqual(page.locator('[data-mobile-open]').get_attribute('aria-expanded'),'true')
  self.assertEqual(page.evaluate('getComputedStyle(document.body).overflowY'),'hidden')
  page.locator('[data-mobile-submenu="about"]').click();expect(page.locator('[data-mobile-panel="about"]')).to_be_visible()
  expect(page.locator('[data-mobile-panel="about"] a[href="/over-ons/partners"]')).to_be_visible()
  page.locator('[data-mobile-submenu="about"]'if args.mode=='tablet'else'[data-mobile-back]').click();expect(page.locator('[data-mobile-panel="root"]')).to_be_visible()
  page.locator('[data-mobile-submenu="industries"]').click();expect(page.locator('[data-mobile-panel="industries"]')).to_be_visible()
  page.locator('[data-mobile-submenu="industries"]'if args.mode=='tablet'else'[data-mobile-back]').click()
  for _ in range(12):
   page.keyboard.press('Tab');self.assertTrue(page.evaluate("document.querySelector('.mobile-drawer').contains(document.activeElement)"))
  page.keyboard.press('Escape');expect(page.locator('.mobile-drawer')).not_to_be_visible()
  self.assertTrue(page.locator('[data-mobile-open]').evaluate('(e)=>e===document.activeElement'))
  self.assertAlmostEqual(page.evaluate('scrollY'),850,delta=2)
 def test_nav_resize_releases_mobile_state(self):
  self.go('/expertises/');p=self.page;p.locator('[data-mobile-open]').click();p.set_viewport_size({'width':1920,'height':1080});p.wait_for_timeout(150)
  self.assertEqual(p.locator('.mobile-header').count(),0);self.assertEqual(p.locator('.mobile-drawer').count(),0)
  self.assertNotEqual(p.evaluate('getComputedStyle(document.body).overflowY'),'hidden');expect(p.locator('.site-header')).to_be_visible()
  p.set_viewport_size({'width':390,'height':844});expect(p.locator('[data-mobile-open]')).to_be_visible()
 def test_nav_tablet_original_media_restores_desktop(self):
  if args.mode!='tablet':return
  record=json.loads((ROOT/'app/public/tablet-data.json').read_text())['/'][0]
  self.go();p=self.page
  self.assertEqual(p.locator('.slide[data-slide="0"] img').get_attribute('src'),record['to'])
  p.set_viewport_size({'width':1920,'height':1080});p.wait_for_timeout(150)
  self.assertEqual(p.locator('.slide[data-slide="0"] img').get_attribute('src'),record['from'])
 def test_nav_tablet_half_panel_inline_submenus(self):
  if args.mode!='tablet':return
  self.go();p=self.page;p.locator('[data-mobile-open]').click();box=p.locator('.mobile-drawer').bounding_box()
  self.assertAlmostEqual(box['x'],384,delta=1);self.assertAlmostEqual(box['width'],384,delta=1)
  p.locator('[data-mobile-submenu="about"]').click();expect(p.locator('[data-mobile-panel="root"]')).to_be_visible();expect(p.locator('[data-mobile-panel="about"]')).to_be_visible()
  expect(p.locator('.mobile-drawer-aux a[href="/nieuws"]')).to_be_visible()
  p.mouse.click(50,300);expect(p.locator('.mobile-drawer')).not_to_be_visible()
 def test_nav_simple_appointment_header(self):
  self.go('/afspraak-maken/');p=self.page;expect(p.locator('.mobile-header a[href="tel:+31162238834"]')).to_be_visible();expect(p.locator('.mobile-header [data-mobile-back-link]')).to_be_visible();self.assertEqual(p.locator('[data-mobile-open]').count(),0)
 def test_nav_failed_mobile_module_retains_original_navigation(self):
  self.context.route('**/mobile.mjs*',lambda r:r.abort());self.go('/contact/');expect(self.page.locator('.site-header')).to_be_visible()
 def test_nav_async_phone_media_restores_desktop(self):
  if args.mode=='tablet':return
  media=json.loads((ROOT/'app/public/mobile-data.json').read_text())
  self.context.add_init_script("const normalFetch=window.fetch.bind(window);window.fetch=(url,...args)=>String(url)==='/mobile-data.json'?new Promise(resolve=>{window.resolveMobileMedia=()=>resolve(new Response(JSON.stringify("+json.dumps(media)+"),{headers:{'content-type':'application/json'}}))}):normalFetch(url,...args)")
  self.go();p=self.page;original=p.locator('.slide[data-slide="0"] img').get_attribute('src');originalHeading=p.locator('.how-copy h3').first.inner_html()
  p.set_viewport_size({'width':1200,'height':900});p.wait_for_timeout(100)
  p.set_viewport_size({'width':390,'height':844});p.wait_for_timeout(100)
  p.evaluate('resolveMobileMedia()');p.wait_for_timeout(100)
  p.set_viewport_size({'width':1200,'height':900});p.wait_for_timeout(100)
  self.assertEqual(p.locator('.slide[data-slide="0"] img').get_attribute('src'),original)
  self.assertEqual(p.locator('.how-copy h3').first.inner_html(),originalHeading)
 def test_nav_delayed_phone_content_has_one_instance(self):
  if args.mode=='tablet':return
  content=json.loads((ROOT/'app/public/mobile-content.json').read_text())
  self.context.add_init_script("const normalContentFetch=window.fetch.bind(window);window.fetch=(url,...args)=>String(url)==='/mobile-content.json'?new Promise(resolve=>{window.resolveMobileContent=()=>resolve(new Response(JSON.stringify("+json.dumps(content)+"),{headers:{'content-type':'application/json'}}))}):normalContentFetch(url,...args)")
  self.go('/expertises/paneelbouw/');p=self.page;p.wait_for_function('Boolean(window.resolveMobileContent)')
  p.set_viewport_size({'width':768,'height':1024});p.wait_for_timeout(100)
  p.set_viewport_size({'width':390,'height':844});p.wait_for_timeout(100)
  p.evaluate('resolveMobileContent()');p.wait_for_timeout(100)
  self.assertEqual(p.locator('.mobile-branch-window').count(),1)
  self.assertEqual(p.locator('.mobile-region').count(),1)
 def test_nav_touch_and_breakpoint_cleanup(self):
  self.go();p=self.page;p.tap('[data-mobile-open]');expect(p.locator('.mobile-drawer')).to_be_visible();p.keyboard.press('Escape')
  for width in [767,768,1199,1200]:
   p.set_viewport_size({'width':width,'height':900});p.wait_for_timeout(100)
   self.assertEqual(p.locator('.mobile-header').count(),int(width<1200))
  self.assertEqual(p.locator('.mobile-footer-socials').count(),0)
 def test_layout_legacy_phone_media_and_teardown(self):
  if args.mode=='tablet':return
  self.go('/expertises/paneelbouw/');p=self.page
  expect(p.locator('.mobile-branch-window img').first).to_be_visible()
  expect(p.locator('.mobile-region img')).to_be_visible()
  self.go('/expertises/retrofit/');expect(p.locator('.mobile-region img')).to_be_visible()
  p.set_viewport_size({'width':1920,'height':1080});p.wait_for_timeout(150)
  self.assertEqual(p.locator('.mobile-branch-window,.mobile-region,.mobile-project-more').count(),0)
 def test_layout_phone_heading_break_restores_desktop(self):
  if args.mode=='tablet':return
  self.go('/');p=self.page
  self.assertEqual(p.locator('.how-copy h3').first.locator('br').count(),1)
  self.assertEqual(p.locator('.vacancy-section h2 br').count(),0)
  expect(p.locator('.mobile-expertise-more')).to_be_visible()
  p.set_viewport_size({'width':1920,'height':1080});p.wait_for_timeout(150)
  self.assertEqual(p.locator('.how-copy h3').first.locator('br').count(),0)
  self.assertEqual(p.locator('.mobile-expertise-more').count(),0)
 def test_layout_birth_controls_share_one_row(self):
  self.go('/vacature/monteur-paneelbouw/');p=self.page
  boxes=[p.locator(f'select[name={name}]').bounding_box()for name in ['birth_day','birth_month','birth_year']]
  self.assertLess(max(b['y']for b in boxes)-min(b['y']for b in boxes),1)
  self.assertEqual(round(boxes[1]['width']),100)
 def test_layout_tablet_uses_actual_theme_metrics(self):
  if args.mode!='tablet':return
  self.go('/expertises/');p=self.page
  self.assertAlmostEqual(p.locator('h1').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)'),48.3333,delta=.02)
  self.assertAlmostEqual(p.locator('.parity-container').first.bounding_box()['width'],668,delta=1)
 def test_layout_phone_families(self):
  routes=args.route or ['/','/expertises','/voor-machinebouwers/voor-machinebouwers','/voor-machinebouwers/proces-productie','/service-en-onderhoud','/over-ons/partners','/over-ons/werken-bij','/expertises/software-engineering','/projecten','/projecten/sc100','/contact','/afspraak-maken','/over-ons','/vacature/monteur-paneelbouw','/branches/agro','/locaties','/offerteaanvraag','/veelgestelde-vragen']
  for route in routes:
   with self.subTest(route=route):
    self.go(route);p=self.page
    size=p.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})');self.assertEqual(size['width'],self.width,size);self.assertLessEqual(size['scroll'],self.width,size)
    self.assertEqual(p.locator('h1').count(),1)
    for field in p.locator('form input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=file]),form textarea,form select').all():
     if not field.is_visible():continue
     box=field.bounding_box();self.assertGreaterEqual(box['width'],50 if (field.get_attribute('name')or'').startswith('birth_')else 180,(route,field.get_attribute('name'),box));self.assertLessEqual(box['x']+box['width'],self.width+1,(route,field.get_attribute('name'),box))

suite=unittest.TestSuite()
for name in unittest.defaultTestLoader.getTestCaseNames(MobileTests):
 if args.case=='all'or args.case=='nav'and'_nav_'in name or args.case=='layout'and'_layout_'in name:suite.addTest(MobileTests(name))
result=unittest.TextTestRunner(verbosity=2).run(suite);raise SystemExit(not result.wasSuccessful())
