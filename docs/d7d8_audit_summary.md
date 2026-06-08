# D7/D8 Scoring Audit — Summary of Changes

**Date:** April 2026  
**Scope:** D7 (Outdoor Recreation) and D8 (Active Wellness) score corrections  
**Files modified:** `index.html`, `CityDatabase_April_26_v2.xlsx`  
**Cities affected:** 11

## Why this audit

Two scoring patterns were inconsistent with the v3.0 rubric anchors:

**D7 inflation in beach/coastal cities** — Naples, Sarasota, Delray Beach, Hilton Head, St. Petersburg, Fort Myers were scoring 7–9 on D7 despite being flat coastal cities. The D7=8–9 anchor requires *"strong trail network, multiple activity types, 3+ seasons of strong outdoor usability"* — these cities have beaches, golf, and water recreation but not the trails-and-mountains profile that D7 actually measures.

**D8 inflation in small mountain towns** — Sun Valley, Sedona, Durango, Steamboat Springs, Whitefish were scoring 7–8 on D8 despite being small towns (1,400–19,000 population) without the built 55+ rec center infrastructure that D8 actually measures. The rubric explicitly notes: *"A city with great hiking but no rec centers scores high on D7, not necessarily D8."*

Your own 3-Dimensions revision document (April 16, 2026) called for similar corrections: *"Cities without dedicated 55+ wellness infrastructure should drop to 4-5. Only cities with genuinely exceptional senior fitness culture should hold 8-10."*

## Score changes — D7 (6 cities)

| City | Old D7 | New D7 | Total impact |
|---|---|---|---|
| Naples FL | 9 | 6 | 71 → 68 |
| Sarasota FL | 9 | 6 | 69 → 66 |
| Delray Beach FL | 8 | 6 | 68 → 66 |
| Hilton Head SC | 8 | 6 | 56 → 54 |
| St. Petersburg FL | 8 | 7 | 69 → 68 |
| Fort Myers FL | 7 | 6 | 64 → 63 |

## Score changes — D8 (5 cities)

| City | Old D8 | New D8 | Total impact |
|---|---|---|---|
| Sun Valley ID | 8 | 5 | 58 → 55 |
| Sedona AZ | 8 | 6 | 51 → 49 |
| Durango CO | 8 | 7 | 51 → 50 |
| Steamboat Springs CO | 8 | 6 | 55 → 53 |
| Whitefish MT | 7 | 5 | 54 → 52 |

Sedona was kept at 6 (not 5) because its scoreNote documents legitimate Sedona Athletic Club + pickleball infrastructure, just at small-town scale. Durango was kept at 7 (not 6) because its scoreNote documents genuine 55+ programming (Silver Sneakers, Renew Active, 65+ specific programming) — a notch above the smaller mountain towns that have no such documentation.

## Defensible at current values (no change applied)

| City | Dimension | Current Score | Why kept |
|---|---|---|---|
| Park City UT | D8 | 9 | Tourism economy supports rec center scale |
| Jackson Hole WY | D8 | 7 | Defensible at this level |
| Naples FL | D8 | 10 | Genuinely has gold-standard 55+ infrastructure |
| Henderson NV | D8 | 8 | Sun City Anthem and large-scale facilities |

## Text changes

Only one scoreNote needed rewriting — Sedona's D8 scoreNote previously claimed *"America's premier small-town wellness destination"* which contradicted a D8=6. Rewritten to match: now describes the actual infrastructure (Sedona Athletic Club, pickleball, Mii amo as luxury wellness rather than retiree fitness) while explaining the small-town scale that drives the score.

All D7 scoreNotes were already honest about their cities' actual recreation profile (beaches, golf, water sports — not "trails") and didn't need rewriting despite the score change.

## Net effect on user matching

For users prioritizing D7 (outdoor recreation) with "Very Important" or "Must Have":
- Naples, Sarasota, Delray Beach, Hilton Head, Fort Myers will now correctly de-rank for these users — they were getting matched as outdoor destinations when they're really beach destinations
- Genuine outdoor cities (Bend, Asheville, Park City, Jackson Hole, Vail at D7=10) now have stronger relative position

For users prioritizing D8 (active wellness) with "Very Important" or "Must Have":
- Small mountain towns will correctly de-rank — they were getting matched on built infrastructure they don't actually have
- The genuine 55+ destinations (Naples 10, Park City 9, Henderson 8) now have stronger relative position

## Top 10 by Total Score after this audit

The leaderboard reshuffled slightly. Florida still dominates the top of the list, but Naples and Sarasota are no longer separated by a wide margin from the next tier:

1. Naples FL — 68
2. St. Petersburg FL — 68
3. Tampa FL — 68
4. Sarasota FL — 66
5. Delray Beach FL — 66
6. Scottsdale AZ — 66
7. Knoxville TN — 66
8. The Woodlands TX — 66
9. Ann Arbor MI — 65
10. Fayetteville AR — 65

Total dimension points removed across all 11 cities: **22 points**

## Validation

- `node --check` on the index.html script tag: **0 errors**
- All 11 score changes verified in both index.html and spreadsheet
- All 87 SUM formulas in spreadsheet recalculated cleanly: **0 errors**

## Combined audit status (D2/D9 + D7/D8)

| Audit | Cities affected | Status |
|---|---|---|
| D2/D9 (variance/neighborhood scoring) | 7 cities | ✅ Complete |
| D7/D8 (recreation vs. wellness overlap) | 11 cities | ✅ Complete |
| Total cities re-scored | 18 unique | |

## Next steps

1. **Test the updated `index.html`** locally before deploying
2. **Update rubric to v3.1** — add the D2/D6/D9 methodology note from earlier audit, and document the D7/D8 anchor clarifications already covered in v3.0
3. **Push to 100 cities** — current count 87, need 13 more
