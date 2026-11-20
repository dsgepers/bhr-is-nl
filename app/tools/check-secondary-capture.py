"""Prove source and candidate sidebars are each captured once during tiling."""
import importlib.util,io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];spec=importlib.util.spec_from_file_location('bhr_capture',root/'checks/visual-planning-2026-11-20/capture-normalized.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
with sync_playwright()as p:
 b=p.chromium.launch()
 for attrs in ['class="sidecolumn"','data-job-sidebar']:
  page=b.new_page(viewport={'width':400,'height':400});page.set_content('<style>body{margin:0;height:1600px}main{height:1500px;padding-top:50px}aside{position:sticky;top:0;width:40px;height:40px;background:rgb(250,0,255)}</style><main><aside '+attrs+'></aside></main>');png=page.screenshot(full_page=True,scale='css');im=Image.open(io.BytesIO(png)).convert('RGB');count=sum(pixel==(250,0,255)for pixel in im.getdata());assert count==1600,(attrs,count);page.close()
 b.close();print('source and candidate sidebar tiling: passed')
