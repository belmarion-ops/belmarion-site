from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib
b=Path(__file__).resolve().parents[2];source=b/'assets/brand/belmarion-maskable-512-r3-20261101.png';im=Image.open(source).convert('RGB');w=round(512*304/388);scaled=im.resize((w,w),Image.Resampling.LANCZOS);tile=Image.new('RGB',(512,512));p=tile.load()
for y in range(512):
 for x in range(512):
  v=round(30-15*y/511);p[x,y]=(v,v,v)
tile.paste(scaled,((512-w)//2,(512-w)//2))
import math
for y in range(512):
 for x in range(512):
  if math.hypot(x-255.5,y-255.5)>160:
   v=round(30-15*y/511);tile.putpixel((x,y),(v,v,v))
for size in [192,512]:tile.resize((size,size),Image.Resampling.LANCZOS).save(b/f'assets/brand/belmarion-shortcut-{size}-r4-20261101.png')
for path in ['favicon.png','icon-maskable.png','icon-maskable-v2.png']:tile.save(b/path)
for size in [192,512]:
 image=Image.open(b/f'assets/brand/belmarion-shortcut-{size}-r4-20261101.png')
 for y in range(size):
  for x in range(size):
   if math.hypot(x-(size-1)/2,y-(size-1)/2)>size*66/216:
    assert max(image.getpixel((x,y)))<45, 'Gold artwork exceeds native safe area'
print('Website shortcut exports and native safe-area checks passed')
