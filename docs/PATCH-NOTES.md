# Patch Notes — 28 City Profiles (monetization-readiness pass)

Applied to all 28 batch profiles. St. Louis is intentionally NOT included — see flag below.

## Applied to every profile
1. **GA4 analytics** — gtag.js snippet (Measurement ID `G-BTL743DSJQ`) added high in <head>.
   The existing `report_request` capture event now actually fires (it was a silent no-op before).
2. **Open Graph / social tags** — added to the 22 that lacked them (title, description, url, hero image, site_name, twitter card). The 6 that already had them were left as-is.
3. **Article + FAQ structured data (JSON-LD)** — added to the 22 that lacked it. 4 city-specific
   Q&As each, grounded strictly in on-page content + the CityDatabase. The 6 that already had it kept theirs (with numbers corrected where needed — see below).
4. **Reserved display-ad slot** — hidden `<aside class="ad-slot" hidden>` before the "Appears on lists"
   section + supporting CSS. Inert until you remove `hidden` at the ads phase.

## Health pills standardized (your "consistency without sacrificing value" call)
- **Ann Arbor**: pill "Top 10 / U.S. News National" → "10/10 Healthcare Match". The "top-10 nationally" detail already lives in the adjacent prose, so nothing was lost.
- **Scottsdale**: pill "Honor Roll / U.S. News 2025–26" → "10/10 Healthcare Match". "Honor Roll" remains in the prose.

## Data corrections — pages reconciled to CityDatabase v12 (DB wins)
All stat bars + any prose/meta/schema mentions updated to the v12 figure:

| City | Field | Was (page) | Now (v12) |
|---|---|---|---|
| Greenville | median | $480K | $335K |
| Columbus | median | $290K | $260K |
| Charlottesville | median | $510K | $460K |
| Nashville | median | $490K | $532K |
| Salt Lake City | median | $590K | $575K |
| St. George | median / monthly | $525K / $4.2–5.6K | $530K / $4.5–6K |
| Bozeman | median / monthly | $725K / $4.8–6.2K | $700K / $6–8K |
| Carlsbad | median / monthly | $1.5M / $6.5–8.5K | $1.45M / $10–12K |

### Review these — judgment calls worth your eye
- **Greenville (biggest swing, $480K → $335K):** the profile's prose and neighborhood cards were
  written around the higher number; the $335K city-proper figure now sits below some neighborhood
  prices shown (consistent with "city median, neighborhoods vary," but please confirm $335K is right).
- **Carlsbad reframe:** monthly jumped to $10–12K, so the old "Tier 4 · Alongside Scottsdale, Napa,
  Santa Barbara" (those are $6.5–8.5K cities) was reworded to "Among the database's most expensive,"
  and the cost-constraint paragraph's "alongside Scottsdale" → "alongside the priciest coastal markets."
- **Bozeman:** the "Bozeman of 2015 was $325K, today near $725K" prose now reads $700K.

## FLAG: project's St. Louis template file is stale
`/mnt/project/st-louis-city-profile-template.html` has NO capture section, guide picker, or analytics
event — it predates your current/live St. Louis. I did not ship a St. Louis built from it (that would
delete the capture block). Send the current St. Louis file and I'll apply the same four items to it.

## Other notes
- GA stream URL still reads wheretoretire.netlify.app (old project). The ID collects regardless, but
  consider renaming the stream + URL to retiremehere.com so the property reflects reality.
- Swap CityDatabase_v12.xlsx into project knowledge to replace v11 (v11 lacks the tax/insurance columns).
- Not done here (your side): photos, sitemap.xml. PUBLISHED_PROFILES already has all keys.
