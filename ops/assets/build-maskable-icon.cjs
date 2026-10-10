// Preserve the approved PNG at its native size; only the containing canvas changes.
// Chrome's pinned shortcut path can pass a maskable bitmap directly to Android.
// Keep the entire motif within Android's 66/108 safe diameter, not only the web 80% zone.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');

async function main() {
  const root = path.resolve(__dirname, '../..');
  const source = await fs.readFile(path.join(root, 'favicon.png'));
  const metadata = await sharp(source).metadata();
  if (metadata.width !== 768 || metadata.height !== 768) throw new Error('Expected approved 768px original');
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1280" height="1280" viewBox="0 0 1280 1280">' +
    '<rect width="1280" height="1280" fill="#000000"/>' +
    '<image x="256" y="256" width="768" height="768" xlink:href="data:image/png;base64,' + source.toString('base64') + '"/>' +
    '</svg>';
  await sharp(Buffer.from(svg)).removeAlpha().png().toFile(path.join(root, 'icon-maskable-v2.png'));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
