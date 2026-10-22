# Belmarion gold favicon — VERIFIED SOURCE / DEPLOYMENT BLOCKED

Base production source: `7dc7f8f6b1feb23d0d23b6f9fcc1414f4f98808c`.

The original supplied 2048px emblem is retained at
`assets/brand/belmarion-gold-source.jpg`. Its SHA-256 is
`3a4a24a66efd577043afee0d3ef1e6650d061cc460dbc0f2e6634380a35b343b`.

Prepared PNG sizes: 16, 32, 48, 192 and 512px; 180px Apple touch icon; 192/512px
maskable variants. Browser ICO contains 16, 32, 48 and 64px variants. Legacy
root favicon, Apple icon and both maskable aliases are also replaced in source.
New public references use source-hash/date filenames or a new query version.

QA passed: all 9 public HTML pages (including redirects, office receipts, privacy,
legal and Founding Circle) have correct icon/manifest metadata; all 45 references
resolve to files; decoded sizes match declarations; all four manifest variants
exist; no old icon references remain in public pages or the manifest. HTML
comparison proves only icon/manifest metadata changed. Existing navigation,
content, forms, scripts, stylesheet, videos, CNAME and workflow are untouched.
Standard/browser and adaptive-mask previews were visually inspected.

**Not deployed.** The live domain is served by GitHub Pages. The existing
`.github/workflows/pages.yml` deploys on every push to `main` and uses Actions
to generate the film poster and deploy the site. No alternative deployment
credentials are available in the execution environment. Publishing through the
current route would violate the explicit no-GitHub-Actions restriction.

The changes are saved on a separate favicon branch; `main` and live content are
preserved. No workflow was triggered and no hosting/domain change was attempted.
Production display, HTTP asset checks and browser-cache refresh remain pending
until a permitted production deployment route is available.
