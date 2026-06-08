# Deep Dive Guide Series — Methodology & Decision Log
**Created:** May 30 session (guide revision pass, 50-city → 100-city)
**Applies to:** active-frontier.html, value-navigator.html, wellness-blueprint.html, globetrotter-guide.html, urban-walkabout.html
**Commit note:** documentation-only; use [skip netlify] or bundle with the guide deploy.

---

## 1. Data-source rule (governing principle)

Every score, tier placement, budget range, monthly estimate, median home value, and tax score in the guides comes from **CityDatabase xlsx, 'City Database' sheet, header row 2**. This session used **CityDatabase_April_30_v10**.

- Dimension mapping: Active Frontier = D7 Outdoor, Value Navigator = D2 Budget + D5 Tax, Wellness Blueprint = D3 Health, Globetrotter = D1 Airport, Urban Walkabout = D6 Walk.
- Web research and prior editorial prose are **supporting color only** (hospital names, airport codes, trail names). They never set a score or a tier.
- Hospital ratings, tax percentages (e.g. CA 13.3%, PA 3.07%), and Walk Score figures quoted in card prose are editorial research, NOT in the database. Verify against current sources before publish; the DB only carries the 0–10 scores.
- Cross-check result this session: old report scores vs current DB had **zero conflicts** across D1, D3, D5, D6. Scoring has been stable.

## 2. Unified template

All five guides share one structure:

1. Sticky site nav (standard header, Top Cities dropdown)
2. **Report header band** — dark per-guide gradient, "RetireMeHere Deep Dive Series" eyebrow with emoji, big white title with italic lightweight second word, description, three meta pills (100 Cities Scored · method hint · date)
3. Method note (what we looked for)
4. "Before You Scroll" takeaways (4 items, numbered badges in the guide accent)
5. Tier/spotlight sections with city cards (score pill on each card where tiered)
6. Quiz CTA in the guide's band color with glow
7. Standard footer

Per-guide accents (the visual identity that distinguishes guides from Top Cities list pages):

| Guide | Band | Emoji | Tier logic |
|---|---|---|---|
| Active Frontier | forest green #1e4d2b / amber accent | 🏔 | 8 thematic spotlights (not score tiers) |
| Wellness Blueprint | teal-blue #0d4f6b | 🏥 | D3: 9–10 / 7–8 / 5–6 / 3–4 |
| Value Navigator | dark gold #6e4d12 | 💰 | Value spotlights from D2+D5 combination |
| Globetrotter Guide | navy #0f2340 | ✈️ | D1: 9–10 / 7–8 / 5–6 / 3–4 |
| Urban Walkabout | plum #3a2456 | 🚶 | D6: 8–9 / 7 / 5–6 / 3–4 |

## 3. Tiering principle

Guides tier **strictly by the database dimension score**. No editorial promotions or demotions. Card prose carries nuance; the tier carries the number.

**Wellness vs Top Cities for Healthcare:** the two pages use different lenses on the same data. The Wellness Blueprint tiers by quality score (best care first); the Top Cities page sorts by access type (anchor-in-town / regional hub / proximity play). A teal clarify-note near the top of the Wellness Blueprint states this explicitly so a city appearing "World-Class" in one and Tier 3 in the other reads as intentional, not an error. This was a deliberate credibility decision.

## 4. City inclusion (curation rule)

Guides are **curated, not exhaustive**. The rule: all cities from the original 50-city report, plus the clear new high-scorers that would look like oversights if missing (e.g. Salt Lake City D3=10, Provincetown D6=9, Miami D1=10). Low-scoring cities are not padded in just because they exist.

Tier 4 ("limited/car required") consistency decision: keep ALL the original report's bottom-tier cities even if unremarkable (Durango, Boise, Colorado Springs in Walkabout), because a city present in four guides but silently absent from the fifth looks like an oversight. Cross-guide consistency beat tighter curation.

## 5. Honest-labeling rules (credibility fixes made this session)

- **Walkability tiers relabeled** to describe reality: Car-Optional (8–9), Walkable Core (7), Walkable Pockets (5–6), Car Required (3–4). Nothing is called "walkable" unless it supports daily life on foot. The old labels implied 5–6 cities weren't car-dependent; they are.
- The Car Required blurb explicitly notes many other database cities are equally car-dependent, so the tier doesn't read as a complete bottom-of-the-ranking.
- **Superlative phrasing rule:** bare "the lowest/cheapest in the database" implies the full ranked list is on the page. Replace with "the lowest **score** in the database" or "of any city **we scored**" (points at the data, not the page). Hedged ("among the lowest") and scoped ("cheapest beach city") superlatives are fine as-is. Fixed: St. George (Walkabout), Paducah and Johnson City (Value Navigator).
- **Superlatives reference "any city we scored"**, never imply all 100 are displayed.

## 6. Standard corrections applied to all guides

- "50+ cities" → "100 Cities Scored"
- "9 dimensions" → 10 (CTA phrasing: "the nine other dimensions")
- Date → May 2026 (update at publish if needed)
- Old standalone mobile-only layouts (600px max-width) → full site template with nav

## 7. Verification protocol (run before every hand-off)

1. Tag balance (section/div/a/header/footer/main/style/script open = close)
2. JS parses (node --check on inline script)
3. Every city link resolves to a real City+ST pair in the DB
4. Every score pill / tax badge matches the DB value exactly
5. Tier counts sanity-checked

## 8. Review flags left in files (HTML comments, invisible to readers)

- **wellness-blueprint.html — St. George (D3=10):** DB places it World-Class; old prose was more modest (U of Utah 4 hrs for complex care). Decide if wording should match the 10.
- **wellness-blueprint.html — The Woodlands (D3=9):** World-Class here, "proximity play" on Top Cities page. Clarify-note covers it; prose leans on the in-town Houston Methodist facility.
- **wellness-blueprint.html — Wilmington NC (D3=5):** distinct from Wilmington DE (D3=8) on the Top Cities page. Two different cities; never merge.

## 9. Deployment notes

- All five files live in the **repo root** (same level as index.html), matching their canonical URLs (retiremehere.com/<guide>.html).
- Confirm the five MailerLite delivery emails link to these exact filenames (forms: Globetrotter fwB9NA, Wellness f03tJB, Value Navigator W6rMh2, Urban Walkabout dJJ40D, Active Frontier g4M1M8).
- Open decision: do Deep Dive guides get their own nav group, or stay email-gated? (Nav currently lists only the seven Top Cities pages.)
- Open item: hospital ratings, tax percentages, and airport route detail in card prose need a current-sources verification pass before publish (editorial research, not DB-governed).
- This session was built against **CityDatabase_April_30_v10**. If the June v13.1 database has score changes, re-run the verification protocol (section 7) against it before deploy.


---

## Addendum — June 7, 2026 session (v13.1 re-verification + Frisco swap)

- Full section 7 protocol re-run against **CityDatabase_Jun_6_v13_1**. All score pills, Range badges, monthly badges, and tax badges verified clean. 36 stale prose medians corrected in Value Navigator and 3 in Active Frontier (ZHVI re-baselining).
- **The Woodlands TX** (now Parked) removed from Active Frontier, Value Navigator, and Wellness Blueprint. Its section 8 review flag is resolved by removal.
- **Frisco TX** (Rubric v3.2, total 59) added per the curation rule: Globetrotter Elite Access (D1 = 9, clear high-scorer), Value Navigator Premium Tier (D2 = 4 / D5 = 8), Wellness Strong Care (D3 = 8, judgment call, lean-add), Active Frontier Pickleball & Golf Capitals (thematic basis: PGA of America HQ; judgment call). **Not** added to Urban Walkabout (D6 = 3, would be padding).
- Link fix: Active Frontier Coeur d'Alène link used a straight apostrophe and no accent, so it never matched the CITIES array. Corrected to the exact array spelling.
- Note for the editorial verification pass (section 9 open item): the eight neighborhood-basis cities quote *citywide* medians in their index.html highlights as contrast figures. These are editorial, not DB-governed, and were left untouched; verify against current ZHVI city figures when running the pass. Provincetown's $2.1M figure is a sourced single-family stat (Boston Globe / Warren Group), distinct from the DB ZHVI value, and was also left.
