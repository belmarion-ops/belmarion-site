#!/usr/bin/env python3
"""Export the approved dark iPhone-style emblem; no app build is performed."""
from pathlib import Path
from PIL import Image
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/brand/belmarion-dark-gradient-source.png'
source=Image.open(SOURCE).convert('RGB')
assert source.width==source.height
digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
tag='dark-gold-20261022-'+digest[:10]
rgb=np.asarray(source).astype(np.int16)
alpha=np.clip((np.minimum(rgb[:,:,0]-rgb[:,:,2],rgb[:,:,1]-rgb[:,:,2])-3)*255/12,0,255).astype(np.uint8)
cutout=source.convert('RGBA');cutout.putalpha(Image.fromarray(alpha));cutout=cutout.crop(cutout.getbbox())
for size in [16,32,48,192,512]:
 source.resize((size,size),Image.Resampling.LANCZOS).save(ROOT/f'assets/brand/favicon-{size}-{tag}.png',optimize=True)
source.resize((180,180),Image.Resampling.LANCZOS).save(ROOT/f'assets/brand/apple-touch-icon-{tag}.png',optimize=True)
for size in [192,512]:
 # Extract only the motif, avoiding a visible square inset in the gradient.
 background=Image.new('RGB',(size,size));pixels=background.load()
 for y in range(size):
  t=y/max(1,size-1);colour=tuple(round(a*(1-t)+b*t)for a,b in zip((48,48,51),(16,16,18)))
  for x in range(size):pixels[x,y]=colour
 motif=cutout.copy();motif.thumbnail((round(size*.75),round(size*.75)),Image.Resampling.LANCZOS)
 background.paste(motif,((size-motif.width)//2,(size-motif.height)//2),motif)
 background.save(ROOT/f'assets/brand/maskable-{size}-{tag}.png',optimize=True)
source.resize((256,256),Image.Resampling.LANCZOS).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
source.resize((512,512),Image.Resampling.LANCZOS).save(ROOT/'favicon.png',optimize=True)
source.resize((180,180),Image.Resampling.LANCZOS).save(ROOT/'apple-touch-icon.png',optimize=True)
for name in ['icon-maskable.png','icon-maskable-v2.png']:
 Image.open(ROOT/f'assets/brand/maskable-512-{tag}.png').save(ROOT/name,optimize=True)
for file in ROOT.glob('*.html'):
 text=file.read_text();text=text.replace('gold-20261022-3a4a24a66e',tag);file.write_text(text)
manifest=ROOT/'site.webmanifest';manifest.write_text(manifest.read_text().replace('gold-20261022-3a4a24a66e',tag))
print(json.dumps({'sourceSha256':digest,'tag':tag}))
