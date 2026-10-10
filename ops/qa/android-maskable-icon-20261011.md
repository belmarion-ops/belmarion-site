# Android maskable website icon — 11 October 2026

The Android home-screen shortcut displayed the ordinary square icon within a white launcher tile. The manifest supplied only purpose `any`.

Added a separate opaque 1254 × 1254 PNG with black padding and purpose `maskable`. The original favicon and Apple touch artwork remain unchanged. Public-page manifest URLs use a new cache key; website launch mode remains `browser`.

Validation: every pixel brighter than 128 lies within the circular safe zone, radius 40% of image width; maximum visible radius measured 38.4063%. Confirmed RGB output (no transparency), six public pages point to the updated manifest. Pixel installation requires a fresh shortcut; physical-device QA is performed by the founder.

Asset: `icon-maskable.png`. Source: `favicon.png`. Preparation: built-in imagegen tool, precise-object-edit mode. Generated output `exec-ba8a4527-a446-4b9b-ab42-f2125c0c19b8.png` copied unchanged into the repository.

Final prompt:

Use case: precise-object-edit. Edit target: the attached BELMARION black-and-white icon. Create a square Android maskable icon asset on a completely opaque pure black #000000 full-bleed background. Preserve the exact supplied motif: thin circular white outline, thick white annulus centered inside, short vertical white tick at twelve o'clock. Do not redesign, stylize, change proportions, or add anything. Only uniformly reduce the existing whole artwork and center it on a larger pure black canvas, adding even black padding. The complete original square must occupy exactly 75 percent of the new square width and height, centered, so every white feature remains within a circular safe zone of radius 40 percent of the total image width. Crisp clean white-on-black edges, no text, no shadow, no texture, no transparency, no rounded corners, no white tile or border. Output a high-resolution square PNG.
