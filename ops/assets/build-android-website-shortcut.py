"""Export the public website's Android bookmark separately from its favicon.

The website opens in a browser; it is not the installed membership PWA.
Do not advertise its ordinary favicon as an adaptive/maskable foreground.
The approved iOS Apple touch icon and installed PWA/APK exports stay intact.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/brand/favicon-512-rhodium-metals-20261024.png'
TAG = 'android-shortcut-v2-20261024'

# The existing export's full motif is 84% high. This centered 504px crop
# gives an optical ring diameter of 82%, matching the photographed Android
# PWA/APK (about 72px inside an 88px launcher body). Keep the metallic pixels.
source = Image.open(SOURCE).convert('RGBA').crop((4, 4, 508, 508))
for size in (192, 512):
    icon = source.resize((size, size), Image.Resampling.LANCZOS)
    # An ordinary round bitmap is recognized by the launcher without being
    # recropped as a 108dp adaptive foreground. Supersample the outer alpha.
    mask = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    icon.putalpha(mask.resize((size, size), Image.Resampling.LANCZOS))
    target = ROOT / f'assets/brand/shortcut-rhodium-{size}-{TAG}.png'
    icon.save(target, optimize=True)
    print(target.name)
