"""Android Chrome pinned-shortcut export; approved iOS assets stay unchanged.

Pixel QA established that a raw web maskable bitmap is used as a native
adaptive foreground for browser shortcuts. Native 108dp geometry is required.
An ordinary transparent bitmap invokes a white legacy wrapper and is unsuitable.
"""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/brand/favicon-512-rhodium-metals-20261024.png'
TAG='android-adaptive-v3-20261024'
source=Image.open(SOURCE).convert('RGBA')
# Preserve the full supplied raster. Its motif already occupies 84% of this
# square, so scale the whole export to make that motif 64/108 of a native layer.
ratio=(64/108)/.84
for size in (192,512):
    extent=round(size*ratio)
    mark=source.resize((extent,extent),Image.Resampling.LANCZOS)
    icon=Image.new('RGBA',(size,size),(28,28,28,255))
    icon.alpha_composite(mark,((size-extent)//2,(size-extent)//2))
    icon=icon.convert('RGB')
    target=ROOT/f'assets/brand/shortcut-rhodium-{size}-{TAG}.png'
    icon.save(target,optimize=True)
    print(target.name)
