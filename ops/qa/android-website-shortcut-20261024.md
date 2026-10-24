# Android website shortcut correction — 24 October 2026

The founder's Pixel launcher screenshot shows a clipped/enlarged rhodium website shortcut beside the bronze PWA and pale-gold APK. Measuring the outer ring near the horizontal center gives about 72px for both installed app variants. Their source geometry and exports are retained.

The public website uses display: browser. Its shortcut now has dedicated round, ordinary bitmap icons (purpose: any), with 82% optical ring diameter, instead of advertising that website favicon as an adaptive maskable foreground. Both large-icon HTML hints and a fresh versioned manifest reference these exports. Chrome's own badge remains a browser-controlled shortcut attribute.

The supplied metallic raster pixels are retained. Website tab favicon/ICO and Apple touch icons, PWA graphite Apple touch icons, PWA bronze installation icons, Android APK launcher exports, screen icons and names remain unchanged. All name/short_name/Apple labels remain Belmarion. No PWA or APK release is required.

Verification: dedicated 192/512 PNG dimensions and alpha mask; matched geometry across export resolutions; generated links resolve to repository assets; PWA/iOS hashes unchanged. The installed APK remains signed 3.0.5. Physical Pixel launcher acceptance of a freshly recreated website shortcut remains outstanding. Existing pinned website shortcuts may keep their original cached icon. Remove/re-add only the public website shortcut; do not uninstall the device-bound membership PWA to refresh this website bookmark.

Reference implementation: Chromium WebappsIconUtils.createHomeScreenIconFromWebIcon and WebappsUtils.addShortcutWithShortcutManager. The reproduction uses launcher clipping to distinguish the raw maskable bitmap from the padded adaptive path; it is a rendering check, not physical-device acceptance.
