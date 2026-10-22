#!/usr/bin/env python3
"""Match the approved iOS PWA gold icon; retain Android maskable safe space."""
from pathlib import Path
from PIL import Image
import hashlib, json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/brand/belmarion-dark-gradient-source.png'
source = Image.open(SOURCE).convert('RGB')
digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
tag = 'gold-ios-scale-20261022-' + digest[:10]
rgb = np.asarray(source).astype(np.int16)
alpha = np.clip((np.minimum(rgb[:, :, 0] - rgb[:, :, 2], rgb[:, :, 1] - rgb[:, :, 2]) - 3) * 255 / 12, 0, 255).astype(np.uint8)
cutout = source.convert('RGBA')
cutout.putalpha(Image.fromarray(alpha))
cutout = cutout.crop(cutout.getbbox())

def icon(size, fraction=.84):
    background = Image.new('RGB', (size, size))
    pixels = background.load()
    for y in range(size):
        t = y / max(1, size - 1)
        colour = tuple(round(a * (1 - t) + b * t) for a, b in zip((48, 48, 51), (16, 16, 18)))
        for x in range(size):
            pixels[x, y] = colour
    motif = cutout.copy()
    # Full ring and tick occupy 84% on iOS, matching the approved PWA.
    # Android maskable assets use their separate 64% safe area.
    motif.thumbnail((round(size * fraction), round(size * fraction)), Image.Resampling.LANCZOS)
    background.paste(motif, ((size - motif.width) // 2, (size - motif.height) // 2), motif)
    return background

master = icon(512)
for size in [16, 32, 48, 192, 512]:
    master.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/favicon-{size}-{tag}.png', optimize=True)
for size in [192, 512]:
    icon(512, .64).resize((size, size), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/maskable-{size}-{tag}.png', optimize=True)
master.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/apple-touch-icon-{tag}.png', optimize=True)
master.save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
for name in ['favicon.png']:
    master.save(ROOT / name, optimize=True)
for name in ['icon-maskable.png', 'icon-maskable-v2.png']:
    icon(512, .64).save(ROOT / name, optimize=True)
master.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / 'apple-touch-icon.png', optimize=True)
for path in [*ROOT.glob('*.html'), ROOT / 'site.webmanifest']:
    path.write_text(path.read_text().replace('ring-safe-20261022-0265f7cfa9', tag))
print(json.dumps({'tag': tag, 'motifFraction': .84, 'maskableFraction': .64}))
