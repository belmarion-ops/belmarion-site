#!/usr/bin/env python3
"""Re-export the canonical emblem. Requires Pillow and NumPy; never builds an app."""
from pathlib import Path
from PIL import Image
import numpy as np
import hashlib
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/brand/belmarion-gold-source.jpg'
source=Image.open(SOURCE).convert('RGB')
assert source.size==(2048,2048)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='3a4a24a66efd577043afee0d3ef1e6650d061cc460dbc0f2e6634380a35b343b'
rgb=np.asarray(source).astype(np.int16)
alpha=np.clip(np.minimum(rgb[:,:,0]-rgb[:,:,2],rgb[:,:,1]-rgb[:,:,2])*255/12,0,255).astype(np.uint8)
cutout=source.convert('RGBA');cutout.putalpha(Image.fromarray(alpha))
def foreground(size,content):
 canvas=Image.new('RGBA',(size,size),(0,0,0,0))
 canvas.alpha_composite(cutout.resize((content,content),Image.Resampling.LANCZOS),((size-content)//2,)*2)
 return canvas
def composed(size,content):
 canvas=Image.new('RGBA',(size,size),'#242424');canvas.alpha_composite(foreground(size,content));return canvas.convert('RGB')
def save(im,path):im.save(path,optimize=True,compress_level=9)
if (ROOT/'site.webmanifest').exists():
 tag='gold-20261022-3a4a24a66e'
 for size in [16,32,48,192,512]:save(source.resize((size,size),Image.Resampling.LANCZOS),ROOT/f'assets/brand/favicon-{size}-{tag}.png')
 save(source.resize((180,180),Image.Resampling.LANCZOS),ROOT/f'assets/brand/apple-touch-icon-{tag}.png')
 for size in [192,512]:save(composed(size,round(size*64/108)),ROOT/f'assets/brand/maskable-{size}-{tag}.png')
 source.resize((256,256),Image.Resampling.LANCZOS).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
 save(source.resize((512,512),Image.Resampling.LANCZOS),ROOT/'favicon.png')
 save(source.resize((180,180),Image.Resampling.LANCZOS),ROOT/'apple-touch-icon.png')
 for name in ['icon-maskable.png','icon-maskable-v2.png']:save(composed(512,round(512*64/108)),ROOT/name)
else:
 save(foreground(1080,640),ROOT/'assets/brand/adaptive-foreground.png')
 save(Image.new('RGB',(1080,1080),'#242424'),ROOT/'assets/brand/adaptive-background.png')
 save(composed(1024,940),ROOT/'assets/brand/launcher-standard.png')
 mono=Image.new('RGBA',(1080,1080),'white');mono.putalpha(foreground(1080,640).getchannel('A'));save(mono,ROOT/'assets/brand/adaptive-monochrome.png')
