#!/usr/bin/env python3
"""Export the approved emblem with launcher-safe padding on every icon route."""
from pathlib import Path
from PIL import Image
import hashlib, json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/brand/belmarion-dark-gradient-source.png'
source = Image.open(SOURCE).convert('RGB')
digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
tag = 'ring-safe-20261022-' + digest[:10]
rgb = np.asarray(source).astype(np.int16)
alpha = np.clip((np.minimum(rgb[:, :, 0] - rgb[:, :, 2], rgb[:, :, 1] - rgb[:, :, 2]) - 3) * 255 / 12, 0, 255).astype(np.uint8)
cutout = source.convert('RGBA')
cutout.putalpha(Image.fromarray(alpha))
cutout = cutout.crop(cutout.getbbox())

def icon(size):
    background = Image.new('RGB', (size, size))
    pixels = background.load()
    for y in range(size):
        t = y / max(1, size - 1)
        colour = tuple(round(a * (1 - t) + b * t) for a, b in zip((48, 48, 51), (16, 16, 18)))
        for x in range(size):
            pixels[x, y] = colour
    motif = cutout.copy()
    # Keep the entire outer ring and top tick inside the central 64%.
    # Regular shortcut icons need this too: Chrome may use an 'any' icon.
    motif.thumbnail((round(size * .64), round(size * .64)), Image.Resampling.LANCZOS)
    background.paste(motif, ((size - motif.width) // 2, (size - motif.height) // 2), motif)
    return background

master = icon(512)
for size in [16, 32, 48, 192, 512]:
    master.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/favicon-{size}-{tag}.png', optimize=True)
for size in [192, 512]:
    master.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/maskable-{size}-{tag}.png', optimize=True)
master.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / f'assets/brand/apple-touch-icon-{tag}.png', optimize=True)
master.save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
for name in ['favicon.png', 'icon-maskable.png', 'icon-maskable-v2.png']:
    master.save(ROOT / name, optimize=True)
master.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / 'apple-touch-icon.png', optimize=True)
for path in [*ROOT.glob('*.html'), ROOT / 'site.webmanifest']:
    path.write_text(path.read_text().replace('dark-gold-20261022-0265f7cfa9', tag))
print(json.dumps({'tag': tag, 'motifFraction': .64}))
