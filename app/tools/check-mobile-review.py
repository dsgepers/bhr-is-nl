"""Native regressions for the sole mobile review. No outgoing delivery."""
import argparse,importlib.util,json,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--test',action='append');p.add_argument('--baseline',action='store_true');args=p.parse_args()
class ReviewTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop()
 def setUp(self):
  self.c=self.browser.new_context(viewport={'width':390,'height':844},screen={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce');self.deliveries=[]
  self.c.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
  def guard(r):
   if r.request.method not in ['GET','HEAD','OPTIONS']:self.deliveries.append(r.request.url);r.abort()
   else:r.continue_()
  self.c.route('**/*',guard)
  if args.baseline:
   import subprocess
   for asset,mime in [('mobile.mjs','application/javascript'),('mobile-parity.css','text/css')]:
    data=subprocess.check_output(['git','show','1ffd94d:app/public/'+asset]);self.c.route('**/'+asset+'*',lambda r,request,data=data,mime=mime:r.fulfill(status=200,content_type=mime,body=data))
  self.page=self.c.new_page();self.page.set_default_timeout(3500)
 def tearDown(self):self.assertEqual(self.deliveries,[]);self.c.close()
 def go(self,route):self.page.goto('http://localhost:4173'+route,wait_until='networkidle');self.page.evaluate('document.fonts.ready');self.page.wait_for_timeout(80)
 def test_01_back_history_and_direct_entry(self):
  self.go('/expertises');self.page.locator('[data-mobile-open]').click();self.page.locator('.mobile-appointment').click();self.page.locator('[data-mobile-back-link]').click();self.page.wait_for_url(lambda url:url.rstrip('/').endswith('/expertises'));self.assertEqual(self.page.url.rstrip('/'),'http://localhost:4173/expertises')
  page=self.c.new_page();page.goto('http://localhost:4173/afspraak-maken');page.locator('[data-mobile-back-link]').click();page.wait_for_url('http://localhost:4173/');page.close()
 def test_02_focus_is_visible_and_survives_rotation(self):
  self.go('/vacature/monteur-paneelbouw');p=self.page
  field=p.locator('[name=privacy]');field.focus();p.keyboard.press('Shift+Tab');p.wait_for_timeout(100)
  self.assertTrue(p.evaluate('''()=>{const e=document.activeElement,r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e}'''),'reverse-tab focus is covered')
  self.go('/contact');p.keyboard.press('Tab');p.wait_for_timeout(100)
  self.assertTrue(p.locator('.skip-link').evaluate('''e=>{let r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}'''),'skip link is covered')
  p.locator('[data-mobile-open]').click();p.set_viewport_size({'width':1200,'height':900});p.wait_for_timeout(100)
  self.assertTrue(p.evaluate("document.querySelector('.site-header').contains(document.activeElement)"),'rotation removed focused navigation')
 def test_03_first_visit_consent_owns_focus(self):
  self.c.add_init_script("localStorage.removeItem('bhr-cookie-consent')");self.go('/contact');p=self.page
  for _ in range(6):
   p.keyboard.press('Tab');self.assertTrue(p.evaluate("document.querySelector('.cookie-box').contains(document.activeElement)"))
  p.locator('[data-consent=denied]').click();expect(p.locator('[data-mobile-open]')).to_be_enabled();self.assertFalse(p.locator('.mobile-header').evaluate('(e)=>e.inert'))
 def test_04_failed_module_retains_destinations(self):
  self.c.route('**/mobile.mjs*',lambda r:r.abort());self.go('/contact');p=self.page
  self.assertEqual(p.evaluate('innerWidth'),390)
  p.locator('.site-header .dropdown-toggle').first.click();p.locator('.site-header .dropdown-menu a').first.click();p.wait_for_url(lambda url:url.rstrip('/').endswith('/voor-machinebouwers/voor-machinebouwers'))
  p.locator('.site-header a[href="/afspraak-maken"]').click();p.wait_for_url(lambda url:url.rstrip('/').endswith('/afspraak-maken'))
 def swipe(self,locator):
  locator.scroll_into_view_if_needed();r=locator.bounding_box();x=min(320,r['x']+r['width']*.75);y=r['y']+min(90,r['height']/2)
  session=self.c.new_cdp_session(self.page)
  session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
  for dx in [25,60,100,160]:session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-dx,'y':y+2}]})
  session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});self.page.wait_for_timeout(150);session.detach()
 def test_05_touch_swipes_use_existing_carousel_state(self):
  for route,root,track,nextSelector in [('/expertises','[data-carousel=steps]','[data-carousel-track]','[data-carousel-direction="1"]'),('/branches/agro','.secondary-cards-process','[data-carousel-track]','[data-carousel-direction="1"]'),('/over-ons','[data-secondary-timeline]','[data-timeline-track]','[data-timeline-next]')]:
   with self.subTest(route=route):
    self.go(route);p=self.page;carousel=p.locator(root).first
    if route=='/branches/agro':
     window=carousel.locator('.mobile-process-window');old=carousel.locator('.mobile-process-photo').get_attribute('src');self.swipe(window);self.assertGreater(window.evaluate('(e)=>e.scrollLeft'),30);self.assertNotEqual(carousel.locator('.mobile-process-photo').get_attribute('src'),old);continue
    t=carousel.locator(track);before=t.evaluate('(e)=>e.style.transform');photo=carousel.locator('.parity-step-photo');old=photo.get_attribute('src')if photo.count()else None
    self.swipe(t.locator(':scope>*').first);self.assertNotEqual(t.evaluate('(e)=>e.style.transform'),before)
    if old:self.assertNotEqual(photo.get_attribute('src'),old)
    self.assertFalse(carousel.locator(nextSelector).is_disabled())
 def test_06_missing_phone_image_retains_original(self):
  row=json.loads((ROOT/'app/public/mobile-data.json').read_text())['/'][0]
  self.c.route('**'+row['to'],lambda r:r.abort());self.go('/');p=self.page;im=p.locator('.slide[data-slide="0"] img');p.wait_for_timeout(150)
  self.assertEqual(im.get_attribute('src'),row['from']);self.assertTrue(im.evaluate('(e)=>e.complete&&e.naturalWidth>0'))
  p.set_viewport_size({'width':1200,'height':900});self.assertEqual(im.get_attribute('src'),row['from'])
 def test_07_phone_hero_and_intro_geometry(self):
  self.go('/');p=self.page;self.assertLessEqual(p.locator('.hero-copy p').first.bounding_box()['x']+p.locator('.hero-copy p').first.bounding_box()['width'],360)
  self.assertEqual(p.locator('.hero-title').first.evaluate('e=>getComputedStyle(e).fontSize'),'32px')
  self.go('/expertises/paneelbouw');p=self.page;self.assertAlmostEqual(p.locator('.page-title img').bounding_box()['height'],p.locator('.page-title').bounding_box()['height'],delta=1)
  self.go('/projecten/sc100');self.assertNotEqual(p.locator('.secondary-hero').evaluate("e=>getComputedStyle(e,'::after').display"),'none');self.assertEqual(p.locator('.secondary-lead-title').evaluate('e=>getComputedStyle(e).fontSize'),'40px')
  self.go('/service-en-onderhoud');self.assertEqual(p.locator('.parity-lead h2').evaluate('e=>getComputedStyle(e).fontSize'),'40px')
 def test_08_home_cues_and_article_sections(self):
  self.go('/');p=self.page;expect(p.locator('.industry-copy>.eyebrow')).to_be_visible();expect(p.locator('.industry-title .arrow').first).to_be_visible()
  for index,expected in enumerate([4908.71875,5829.0625,6735.40625]):
   box=p.locator('.how-image img').nth(index).bounding_box();self.assertAlmostEqual(box['y']+p.evaluate('scrollY'),expected,delta=2)
  self.go('/bordenbouwer');self.assertEqual(p.locator('.secondary-article.secondary-reverse').first.evaluate('e=>getComputedStyle(e).paddingTop'),'60px')
 def test_09_tablet_compositions(self):
  p=self.page;p.set_viewport_size({'width':768,'height':1024});self.go('/');self.assertEqual(p.locator('.hero-title').first.evaluate('e=>getComputedStyle(e).fontSize'),'45px');self.go('/over-ons');slide=p.locator('[data-timeline-track]>article').first
  im=slide.locator('img').bounding_box();copy=slide.locator(':scope>div').bounding_box();self.assertAlmostEqual(im['width'],433,delta=2);self.assertGreater(copy['y'],im['y']+im['height']-1);self.assertAlmostEqual(copy['width'],353,delta=2)
  self.go('/branches/agro');copy=p.locator('.secondary-theme .secondary-article-copy h2').first.bounding_box();self.assertAlmostEqual(copy['x'],75,delta=1);self.assertAlmostEqual(copy['width'],251,delta=1)
  self.assertAlmostEqual(p.locator('.secondary-cards-process h2').bounding_box()['x'],440,delta=2)
 def test_10_quote_progress_and_compact_search(self):
  self.go('/expertises/paneelbouw');p=self.page;expect(p.locator('.mobile-quote-intro')).to_be_visible();progress=p.locator('.quote-section .step-indicators');expect(progress).to_be_visible();self.assertEqual(progress.locator('li').count(),3)
  form=p.locator('.quote-section .wizard')
  for select in form.locator('[data-step="0"] select').all():select.select_option(index=1)
  form.locator('.next-step').click();expect(form.locator('[data-step="1"]')).to_be_visible()
  form.locator('[data-step="1"] input').fill('Machine');form.locator('[data-step="1"] textarea').fill('Toelichting');form.locator('.next-step').click();expect(form.locator('[data-step="2"]')).to_be_visible()
  for name in ['name','company','email','phone']:form.locator('[name="'+name+'"]').fill('example@example.com'if name=='email'else'0612345678'if name=='phone'else'Visuele controle')
  self.assertFalse(form.evaluate('(f)=>f.checkValidity()'));form.locator('[name=privacy]').check();self.assertTrue(form.evaluate('(f)=>f.checkValidity()'));form.locator('[type=submit]').click();expect(form.locator('.form-status')).to_contain_text('tijdelijk niet beschikbaar')
  self.go('/expertises');expect(p.locator('.quote-section .step-indicators')).not_to_be_visible()
  self.go('/zoeken');f=p.locator('[data-secondary-search]');self.assertLessEqual(f.bounding_box()['height'],50);self.assertEqual(f.locator('[data-search-clear]').evaluate('e=>getComputedStyle(e).visibility'),'hidden')
  f.locator('input').fill('paneelbouw');expect(f.locator('[data-search-clear]')).to_be_visible();f.locator('button[type=submit]').click();p.wait_for_function("document.querySelector('[data-secondary-results] article')")
 def test_11_evidence_rejects_wrong_served_bytes(self):
  path=ROOT/'app/tools/mobile_evidence.py';self.assertTrue(path.exists(),'shared evidence verifier missing')
  spec=importlib.util.spec_from_file_location('evidence',path);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
  expected=e.build_identity(ROOT);self.assertEqual(expected,e.build_identity(ROOT))
  import tempfile
  from PIL import Image
  with tempfile.TemporaryDirectory()as directory:
   root=Path(directory);dist=root/'app/dist';dist.mkdir(parents=True);data=dist/'mobile-data.json';data.write_text('{}');first=e.build_identity(root);data.write_text('{"updated":true}');self.assertNotEqual(first,e.build_identity(root),'JSON changes must invalidate build identity')
   cached=root/'capture';cached.mkdir();Image.new('RGB',(4,4)).save(cached/'candidate.png');(cached/'capture.json').write_text(json.dumps({'expectedRevision':expected,'revisionBefore':expected,'revisionAfter':expected,'revisionChanged':False}));(cached/'candidate.json').write_text(json.dumps({'viewport':{'width':4,'viewportHeight':4,'documentHeight':4,'dpr':1,'scale':1},'buildRevision':expected,'servedResources':{'/index.html':'verified'}}))
   self.assertTrue(e.cached_capture_valid(cached,['candidate'],4,4,expected));self.assertFalse(e.cached_capture_valid(cached,['candidate'],4,4,'different-build'));(cached/'candidate.png').unlink();self.assertFalse(e.cached_capture_valid(cached,['candidate'],4,4,expected))
  good=e.observe_served(self.page);self.go('/contact');self.assertTrue(e.verify_served(good,ROOT))
  resources=e.observe_served(self.page);self.c.route('**/mobile-parity.css*',lambda r:r.fulfill(status=200,content_type='text/css',body='/* stale served build */'));self.go('/contact')
  with self.assertRaisesRegex(AssertionError,'served bytes'):e.verify_served(resources,ROOT)
suite=unittest.TestSuite(ReviewTests(name)for name in unittest.defaultTestLoader.getTestCaseNames(ReviewTests)if not args.test or any(x in name for x in args.test));result=unittest.TextTestRunner(verbosity=2).run(suite);raise SystemExit(not result.wasSuccessful())
