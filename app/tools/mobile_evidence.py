"""Build and served-byte identity for mobile visual evidence (read-only)."""
import hashlib,json
from pathlib import Path
from urllib.parse import urlparse,unquote
from PIL import Image

def build_identity(root):
 root=Path(root);h=hashlib.sha256()
 for file in sorted((root/'app/dist').rglob('*')):
  if file.is_file()and file.suffix in ['.html','.css','.mjs','.js','.json']:
   h.update(str(file.relative_to(root/'app/dist')).encode());h.update(file.read_bytes())
 return h.hexdigest()

def observe_served(page):
 responses=[]
 page.on('response',lambda response:responses.append(response)if response.request.resource_type in ['document','stylesheet','script','fetch','font','image']else None)
 return responses

def verify_served(responses,root):
 dist=(Path(root)/'app/dist').resolve();verified={}
 for response in responses:
  url=urlparse(response.url)
  if url.hostname not in ['localhost','127.0.0.1']:continue
  if 300<=response.status<400:continue
  assert response.status==200,f'served resource HTTP{response.status}: {response.url}'
  path=(dist/unquote(url.path).lstrip('/')).resolve()
  if path.is_dir():path/='index.html'
  assert path.is_relative_to(dist)and path.is_file(),f'unknown served resource: {url.path}'
  expected=path.read_bytes();actual=response.body()
  assert actual==expected,f'served bytes differ from expected build: {url.path}'
  verified[url.path]=hashlib.sha256(actual).hexdigest()
 assert verified,'no served resources verified'
 return verified

def assert_source_theme(styles,device):
 assert any('corporate-'+device in(s or'')for s in styles),f'wrong source theme, expected corporate-{device}: {styles}'

def cached_capture_valid(directory,roles,width,height,expected):
 directory=Path(directory)
 try:
  if(directory/'error.json').exists():return False
  capture=json.loads((directory/'capture.json').read_text())
  if capture.get('expectedRevision')!=expected or capture.get('revisionBefore')!=expected or capture.get('revisionAfter')!=expected or capture.get('revisionChanged'):return False
  for role in roles:
   data=json.loads((directory/(role+'.json')).read_text())
   if data.get('status',200)>=400:
    if role!='reference':return False
    continue
   v=data['viewport']
   if v['width']!=width or v['viewportHeight']!=height or v['dpr']!=1 or v['scale']!=1:return False
   with Image.open(directory/(role+'.png'))as im:
    if im.width!=width or im.height!=v['documentHeight']:return False
   if role=='candidate'and(not data.get('servedResources')or data.get('buildRevision')!=expected):return False
  return True
 except(Exception):return False
