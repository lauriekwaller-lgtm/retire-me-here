# HANDOFF: Favicon Rollout

**Design locked:** Cream background, deep-orange half-sun with five rays, teal horizon line. Cream #F5E6CD, Orange #B85C3A, Teal #2A5E5A.

## Files generated (in favicon-files.zip)

| File | Purpose |
|---|---|
| `favicon.ico` | Multi-resolution ICO (16, 32, 48). Required by older browsers and many crawlers. |
| `favicon.svg` | Vector source. Modern browsers use this for crisp scaling. |
| `favicon-16.png` | Explicit 16px PNG. |
| `favicon-32.png` | Explicit 32px PNG. |
| `favicon-48.png` | Explicit 48px PNG. |
| `favicon-192.png` | Android home screen icon. |
| `favicon-512.png` | PWA manifest, large-screen reference. |
| `apple-touch-icon.png` | 180×180 for iOS. Square (no internal rounding); iOS adds the rounded corners automatically. |
| `site.webmanifest` | PWA manifest declaring the icon set, theme color, background color. |

## Rollout steps

### Step 1: Upload all 9 files to the repo root

All paths in the HTML reference root-level URLs (`/favicon.ico`, `/favicon.svg`, etc.), so files must sit alongside `index.html` at the top of the repo.

### Step 2: Find-and-replace the existing favicon block

Every page with a favicon currently uses the identical placeholder data-URI. Find:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%232A5E5A'/><text x='16' y='22' font-family='serif' font-size='18' font-weight='bold' fill='%23C4724A' text-anchor='middle'>H</text></svg>">
```

Replace with:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Run this find-and-replace across the entire repo. It will apply cleanly to:

- `index.html`
- All 5 deep dive guides (active-frontier, value-navigator, wellness-blueprint, globetrotter-guide, urban-walkabout)
- All landing pages (top-cities-for-* plus best-places-to-retire-avoid-natural-disasters)
- All 29 published city profile pages in `/cities/`
- All 5 comparison pages

### Step 3: Add the block to profile.html

`profile.html` currently has NO favicon declaration. Open it and paste the same 6-line block above into the `<head>`, ideally right after the `<meta charset>` line.

### Step 4: Verify after deploy

1. Visit `retiremehere.com/favicon.ico` directly in a browser. It should display the icon, not 404.
2. Hard-refresh any page (Ctrl+Shift+R / Cmd+Shift+R) to bypass favicon caching, which is aggressive.
3. Paste a profile URL into [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) or [Twitter Card Validator](https://cards-dev.twitter.com/validator). The scraper preview should show your favicon, not a generic globe.
4. After 24–48 hours, search a profile-related query in Google. If an AI Overview surfaces and cites RetireMeHere, the favicon should appear in the citation strip.

## Notes

- **Browser favicon caching is aggressive.** A regular refresh will not show the new icon. Hard-refresh, or close and reopen the tab.
- **The SVG favicon will be used by modern browsers for tab display.** It's vector, so it stays crisp at any zoom. The PNG/ICO fallbacks cover older browsers and scrapers that don't handle SVG.
- **No design uplift expected for AI Overview citations until Google recrawls.** This typically happens within a few days but can take longer for individual pages.
- **The locked palette differs from the existing site palette.** The favicon background is cream (#F5E6CD) rather than the site's teal. The teal horizon line ties it back to the existing brand. If you later want to align the site palette toward warmer tones, the favicon is already there.
