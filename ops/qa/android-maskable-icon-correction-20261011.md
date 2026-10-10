# Android home-screen icon crop correction — 11 October 2026

Physical Pixel QA showed the outer ring disappearing from the first maskable variant. Its foreground radius was 38.486% of the source image width, within the web manifest 40% zone but outside Android's tighter adaptive bounds when Chrome passes the bitmap directly.

The correction preserves the approved original 768px PNG RGB pixels exactly, centered at (256, 256) inside a 1280px opaque black SVG canvas, then rasterizes that code-native wrapper with Sharp. No logo redraw or imagegen is used. `ops/assets/build-maskable-icon.cjs` reproduces the asset; it requires Sharp. The ordinary favicon and Apple artwork remain unchanged.

Checks: original RGB pixels exactly equal the native-sized central region; RGB output has no transparency; maximum foreground radius is 28.64435% of width, within Android's 30.55556% safe radius (66/108 diameter), and within the direct circular crop radius 33.33333%. Full ring and tick are retained. This is a crop model, not physical Pixel acceptance.

Primary source inspected: Chromium `components/webapps/browser/android/java/src/org/chromium/components/webapps/WebappsUtils.java`, `WebappsIconUtils.java`, and `components/webapps/browser/android/add_to_homescreen_data_fetcher.cc`, current main on 11 October 2026. Shortcut creation passes maskable bitmaps to `Icon.createWithAdaptiveBitmap`; the native safe ratio constant is 66/108.

Public pages link to a new manifest cache key. A new filename avoids cached bitmap reuse. Existing shortcuts must be removed and recreated for device QA. Website launch behavior and all existing copy/styles are preserved.
