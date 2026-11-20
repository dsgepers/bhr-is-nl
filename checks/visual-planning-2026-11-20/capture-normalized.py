"""Run visual-diff with viewport-tiled full-page capture for BHR's 3D layers.

Chromium's captureBeyondViewport drops BHR's composited hero text and captures
off-canvas slider overflow. Capture real viewports and stitch at actual scroll
positions instead. Keep the first header; suppress repeated sticky headers.
The upstream skill still handles preparation, DOM/content audits and metrics.
"""
import importlib.util
import io
from pathlib import Path
import sys
from PIL import Image
from playwright.sync_api import Page

SKILL = Path.home() / '.codex/skills/visual-diff/scripts/compare_page.py'
spec = importlib.util.spec_from_file_location('bhr_visual_diff', SKILL)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
native_screenshot = Page.screenshot


def screenshot(page, **kwargs):
    if not kwargs.get('full_page') or kwargs.get('clip'):
        return native_screenshot(page, **kwargs)
    # Cookie dismissal leaves the pointer over different coordinates on each
    # origin. Park it outside the viewport so scroll tiles cannot hover cards,
    # buttons or the full-width partner strip by accident.
    page.mouse.move(-20, -20)
    # Inline SVG media can hydrate after the skill's first lazy-scroll pass.
    # Settle the footer and document height before allocating the stitched image.
    if not page.evaluate('Boolean(window.__bhrCaptureSettled)'):
        page.evaluate('scrollTo(0,document.documentElement.scrollHeight)')
        page.wait_for_timeout(1600)
        page.evaluate('document.fonts.ready')
        page.evaluate('scrollTo(0,0)')
        page.wait_for_timeout(1200)
        page.evaluate('window.__bhrCaptureSettled=true')
    # Normalize only the carousel state, keeping its real geometry and media.
    # Tiny Slider has no exposed controls on the reference; hold its first
    # original item to prevent different slides appearing in successive tiles.
    page.evaluate("""() => {document.querySelectorAll('.partnerSlider').forEach((track,index)=>{
      const first=track.querySelector('[id$="-item0"]');
      if(first){const offset=-(first.getBoundingClientRect().x-track.getBoundingClientRect().x);
        track.dataset.bhrFrozenSlider=String(index);
        // Tiny Slider rewrites inline transform on every autoplay tick. A
        // stylesheet priority survives those ticks without changing dimensions.
        const style=document.createElement('style');
        style.textContent=`[data-bhr-frozen-slider="${index}"]{transition-duration:0s!important;transform:translate3d(${offset}px,0,0)!important}`;
        document.head.append(style);}
    });document.querySelectorAll('[data-carousel="partners"]').forEach(root=>{
      root.dispatchEvent(new Event('mouseenter'));const track=root.querySelector('[data-carousel-track]'),first=track?.querySelector('[data-partner]');
      if(first){track.style.setProperty('transition-duration','0s','important');track.style.setProperty('transform',`translateX(${- (first.getBoundingClientRect().x-track.getBoundingClientRect().x)}px)`,'important');}
    })}""")
    page.add_style_tag(content='#banner_header>.tns-item{opacity:0!important;visibility:hidden!important;animation:none!important}#banner_header>#banner_header-item0{opacity:1!important;visibility:visible!important;left:0!important;z-index:2!important}')
    page.wait_for_timeout(100)
    width, viewport_height = page.evaluate('[innerWidth,innerHeight]')
    height = page.evaluate('document.documentElement.scrollHeight')
    canvas = Image.new('RGB', (width, height), 'white')
    page.add_style_tag(content='html{scroll-behavior:auto!important}.sidecolumn,[data-job-sidebar]{position:relative!important;top:auto!important}')
    args = {k: v for k, v in kwargs.items() if k not in ('path', 'full_page')}
    for target in range(0, height, viewport_height):
        actual = page.evaluate('(y)=>{scrollTo(0,y);return scrollY}', target)
        page.wait_for_timeout(200)
        # Wait for finite entrance transitions rather than capturing mid-fade.
        page.wait_for_function("""() => !document.getAnimations().some(a=>a.playState==='running' && Number.isFinite(a.effect.getComputedTiming().endTime))""",timeout=5000)

        tile = Image.open(io.BytesIO(native_screenshot(page, full_page=False, **args))).convert('RGB')
        # The last viewport overlaps its predecessor. Preserve already captured
        # pixels, so a sticky header can never overwrite earlier page content.
        start = max(target - actual, 0)
        canvas.paste(tile.crop((0, start, width, min(viewport_height, height - actual))), (0, actual + start))
        if target == 0:
            # A stylesheet survives CMS/Vue scroll handlers rewriting inline
            # visibility/opacity and also catches floating clones created later.
            page.evaluate("""() => {const style=document.createElement('style');style.id='bhr-tiling-hide-floating';style.textContent='header.site-header,header.Element,.stickycolumn,[data-project-sticky],[data-job-sticky]{visibility:hidden!important;opacity:0!important}';document.head.append(style)}""")
        if actual + viewport_height >= height:
            break
    page.evaluate("""() => {document.querySelector('#bhr-tiling-hide-floating')?.remove();scrollTo(0,0)}""")
    page.wait_for_timeout(1200)
    output = io.BytesIO()
    canvas.save(output, format='PNG')
    if kwargs.get('path'):
        Path(kwargs['path']).write_bytes(output.getvalue())
    return output.getvalue()


Page.screenshot = screenshot
if __name__ == '__main__':
    raise SystemExit(module.main())
