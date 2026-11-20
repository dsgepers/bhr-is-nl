from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parent;rows=json.loads((ROOT/'catalog.json').read_text());out=ROOT/'inspection'
def sheet(items,roles,name):
 for start in range(0,len(items),12):
  imout=Image.new('RGB',(1320,1600),'#ddd');d=ImageDraw.Draw(imout)
  for i,(r,vp) in enumerate(items[start:start+12]):
   x=i%3*440;y=i//3*400;d.rectangle((x,y,x+439,y+399),fill='white');d.text((x+4,y+4),f'{r["number"]:02d} {vp} {r["route"][:55]}',fill='black');d.text((x+4,y+18),' / '.join(roles)+': top, middle, footer',fill='black')
   for col,role in enumerate(roles):
    source=Image.open(ROOT/'baseline'/r['key']/f'{vp}-{role}.png').convert('RGB');w,h=source.size;crop=min(h,round(w*1050/1920));tops=[0,max(0,(h-crop)//2),max(0,h-crop)]
    for j,t in enumerate(tops):
     cut=source.crop((0,t,w,min(h,t+crop)));cut.thumbnail((220,121));imout.paste(cut,(x+col*220,y+36+j*121))
  imout.save(out/f'{name}-{start//12+1:02d}.jpg',quality=89)
sheet([(r,'wide') for r in rows if r['localExists']],['heatmap','overlay'],'diagnostics')
sheet([(r,vp) for r in rows if r['priority'] for vp in ['desktop','tablet','mobile']],['reference','candidate'],'regressions')
print('Saved direct diagnostic and responsive review sheets.')
