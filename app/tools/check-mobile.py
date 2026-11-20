"""Browser regressions for mobile parity; never deliver a form."""
import argparse,json,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
P=argparse.ArgumentParser();P.add_argument('--case',choices=['nav','layout','all'],default='all');P.add_argument('--route',action='append');args=P.parse_args()

class MobileTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop()
 def setUp(self):
  self.context=self.browser.new_context(viewport={'width':390,'height':844},screen={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True,reduced_motion='reduce')
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
  page.locator('[data-mobile-back]').click();expect(page.locator('[data-mobile-panel="root"]')).to_be_visible()
  page.locator('[data-mobile-submenu="industries"]').click();expect(page.locator('[data-mobile-panel="industries"]')).to_be_visible()
  page.locator('[data-mobile-back]').click()
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
 def test_nav_simple_appointment_header(self):
  self.go('/afspraak-maken/');p=self.page;expect(p.locator('.mobile-header a[href="tel:+31162238834"]')).to_be_visible();expect(p.locator('.mobile-header [data-mobile-back-link]')).to_be_visible();self.assertEqual(p.locator('[data-mobile-open]').count(),0)
 def test_nav_failed_mobile_module_retains_original_navigation(self):
  self.context.route('**/mobile.mjs*',lambda r:r.abort());self.go('/contact/');expect(self.page.locator('.site-header')).to_be_visible()
 def test_layout_phone_families(self):
  routes=args.route or ['/','/expertises','/voor-machinebouwers/voor-machinebouwers','/voor-machinebouwers/proces-productie','/service-en-onderhoud','/over-ons/partners','/over-ons/werken-bij','/expertises/software-engineering','/projecten','/projecten/sc100','/contact','/afspraak-maken','/over-ons','/vacature/monteur-paneelbouw','/branches/agro','/locaties','/offerteaanvraag','/veelgestelde-vragen']
  for route in routes:
   with self.subTest(route=route):
    self.go(route);p=self.page
    size=p.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})');self.assertEqual(size['width'],390,size);self.assertLessEqual(size['scroll'],390,size)
    self.assertEqual(p.locator('h1').count(),1)
    for field in p.locator('form input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=file]),form textarea,form select').all():
     if not field.is_visible():continue
     box=field.bounding_box();self.assertGreaterEqual(box['width'],180,(route,box));self.assertLessEqual(box['x']+box['width'],391,(route,box))

suite=unittest.TestSuite()
for name in unittest.defaultTestLoader.getTestCaseNames(MobileTests):
 if args.case=='all'or args.case=='nav'and'_nav_'in name or args.case=='layout'and'_layout_'in name:suite.addTest(MobileTests(name))
result=unittest.TextTestRunner(verbosity=2).run(suite);raise SystemExit(not result.wasSuccessful())
