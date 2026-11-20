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
    width, viewport_height = page.evaluate('[innerWidth,innerHeight]')
    height = page.evaluate('document.documentElement.scrollHeight')
    canvas = Image.new('RGB', (width, height), 'white')
    page.add_style_tag(content='html{scroll-behavior:auto!important}')
    args = {k: v for k, v in kwargs.items() if k not in ('path', 'full_page')}
    for target in range(0, height, viewport_height):
        actual = page.evaluate('(y)=>{scrollTo(0,y);return scrollY}', target)
        page.wait_for_timeout(180)
        tile = Image.open(io.BytesIO(native_screenshot(page, full_page=False, **args))).convert('RGB')
        # The last viewport overlaps its predecessor. Preserve already captured
        # pixels, so a sticky header can never overwrite earlier page content.
        start = max(target - actual, 0)
        canvas.paste(tile.crop((0, start, width, min(viewport_height, height - actual))), (0, actual + start))
        if target == 0:
            page.evaluate("""() => document.querySelectorAll('header.site-header,.Element.Header').forEach(e=>{
              e.dataset.visualDiffVisibility=e.style.visibility;
              e.dataset.visualDiffOpacity=e.style.opacity;
              e.style.setProperty('visibility','hidden','important');
              e.style.setProperty('opacity','0','important');
            })""")
        if actual + viewport_height >= height:
            break
    page.evaluate("""() => {document.querySelectorAll('[data-visual-diff-visibility]').forEach(e=>{
      e.style.visibility=e.dataset.visualDiffVisibility;e.style.opacity=e.dataset.visualDiffOpacity;
      delete e.dataset.visualDiffVisibility;delete e.dataset.visualDiffOpacity;
    });scrollTo(0,0)}""")
    page.wait_for_timeout(1200)
    output = io.BytesIO()
    canvas.save(output, format='PNG')
    if kwargs.get('path'):
        Path(kwargs['path']).write_bytes(output.getvalue())
    return output.getvalue()


Page.screenshot = screenshot
if __name__ == '__main__':
    raise SystemExit(module.main())
