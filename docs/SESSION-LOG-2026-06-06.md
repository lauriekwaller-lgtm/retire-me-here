# Session Log — June 6, 2026
*Repo reference doc, same spirit as ROADMAP.md. What changed, what was decided, what's open.*

## How we got here
Started as "verify 29 revised city profiles before deploy." Verification surfaced data-source
inconsistencies → led to single-source decision (Zillow ZHVI) → database overhaul → The Woodlands
parked → Frisco scored and added. One city swap became a data-integrity pass. Worth it; now logged.

## COMPLETED ✅

### Database — CityDatabase_Jun_6_v13_1.xlsx (new master; replace v11/v12 in project files)
- Median Home repopulated for 91 cities from **Zillow ZHVI** (City, All Homes, Smoothed SA, Apr-2026
  snapshot). Source stamped in header row. Quarterly refresh = download new CSV, re-run.
- **8 high-variance cities untouched** (Indianapolis, Memphis, Philadelphia, Pittsburgh, San Antonio,
  St. Louis, St. Paul, Wilmington DE) — they keep retiree-target-neighborhood basis per Rubric v3.2
  Universal Methodology. DB number ≠ profile display number for these, BY DESIGN.
- **Frisco, TX added** (#77): D-scores 9/4/8/8/3/4/8/8/7 (D1..D10 order), total 59, Range 4,
  $5.5–7.5K/mo, ZHVI $663K, climate W6 H3 M4 HUM7 HEAT9. Approved by Laurie 6/6.
- **The Woodlands parked** → "Parked — Future Build" tab, full row preserved, awaits
  planned-communities phase (ROADMAP).
- **D2 reconciliation** after ZHVI re-baselining (14 movers reviewed): Steamboat Springs 3→2,
  Delray Beach 4→6, Ann Arbor held at 5 (boundary case, COL supports). Totals synced across all
  3 sheets. 11 of 14 movers confirmed in-band, no change.

### 28 city profiles — city-profiles-final.zip (supersedes all earlier zips)
- GA4 wired: G-BTL743DSJQ on every profile; report_request capture event now live.
- OG/social tags + Article+FAQ JSON-LD on all 28 (22 were missing both).
- Reserved hidden display-ad slot (.ad-slot) on all 28 — activate at ads phase by removing `hidden`.
- Health pills standardized (Ann Arbor, Scottsdale → 10/10; editorial detail kept in prose).
- **Stat relabeled "Median Home" → "Typical Home Value"** (ZHVI is a typical-value index, not a
  sale median). Sub-labels: "Citywide · neighborhoods vary" (split cities: "City-limits value ·
  neighborhoods vary"). All values updated to Apr-2026 ZHVI; FAQ/prose/meta wording swept to match.
  Neighborhood-card "Median home: $X" lines deliberately unchanged (separate neighborhood claims).
- Scottsdale related-card: The Woodlands → **Frisco**.
- All 28 re-verified: tag balance, JSON-LD validity, JS syntax, GA once, no stale values.

### Decisions recorded (don't reopen)
- **One source for home values: Zillow ZHVI**, city geography, smoothed SA. Label = "Typical Home Value."
- **DB wins** on any page-vs-DB conflict; profiles never source prices from ad-hoc web research.
- Stat cards show factual citywide figure; housing nuance lives in neighborhood sections (re-confirmed).
- GA property: stream still named DestinationRetired / wheretoretire URL — collects fine; rename when convenient.

## OPEN QUEUE 🔜
1. **Deploy the 28** (Laurie): photos per workflow, sitemap.xml, push. PUBLISHED_PROFILES already has all keys.
2. **Frisco profile build** — full production workflow (DB row ready; needs photos + profile HTML + sitemap + PUBLISHED_PROFILES key exists? verify).
3. **Frisco → index.html CITIES array** — needs full city object; climate: { W:6, H:3, M:4, HUM:7, HEAT:9 }.
   Remove The Woodlands object (or leave until planned-communities phase? decide).
4. **Frisco landing-page/guide placements** — pre-assessment vs documented criteria:
   - *Sports Fans*: Tier-2 candidate at best. FC Dallas (Toyota Stadium IS in Frisco); Mavericks/Stars
     at AAC ~30 min (borderline — needs the same drive-time verification as the Annapolis call);
     Cowboys/Rangers in Arlington 40+ min = past threshold. ALSO: Henderson/Las Vegas precedent —
     Fort Worth already represents DFW Tier 1; decide if Frisco duplicates or earns its own entry
     via in-city MLS. Laurie's methodology call.
   - *Healthcare* (D3=8), *Hikers* (D7=4), *Arts*, *Foodie*, *Active Retirees*: likely no placement.
   - *Deep Dives*: Globetrotter Guide candidate (D1=9, DFW hub). Wellness Blueprint depends on tier
     cutoffs (D3=8). Value Navigator / Active Frontier / Urban Walkabout: no.
   - The Woodlands stays in published guides until its parked status is acted on — or pull now? Decide.
5. **The Woodlands references in live site** — appears in index.html, active-frontier, value-navigator,
   wellness-blueprint. Keep (city data still served) or remove with parking? Currently HARMLESS but
   inconsistent with DB once v13.1 deploys quiz logic... NOTE: quiz reads CITIES array in index.html,
   not the xlsx — so site behavior unchanged until index.html is edited. No urgency, but track it.
6. **D2/median sync for index.html CITIES array** — the quiz's medianHome/budget data in index.html
   predates v13.1. Needs a reconciliation pass so quiz, DB, and profiles agree. (Biggest remaining
   consistency gap.)
7. Earlier still-open items: MailerLite delivery-link filename check; Deep Dive nav-group decision;
   Florida hub (Month-2 roadmap); affiliate activation (Month 3).

## PROJECT-FILES HYGIENE 📁
Add/replace in project knowledge: CityDatabase_Jun_6_v13_1.xlsx (replace v11), scoring_rubric_v3_2.docx,
HUM-HEAT-Scoring-Guide.md, this log, PATCH-NOTES.md.
