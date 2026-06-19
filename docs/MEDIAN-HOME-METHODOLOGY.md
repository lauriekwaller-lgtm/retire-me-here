# RetireMeHere Median Home Methodology

**Version:** 1.1
**Established:** June 19, 2026
**Supersedes:** Multi-basis approach (Citywide / Archetype / Neighborhood), v1.0
**Database:** CityDatabase_Jun_19_v15_1.xlsx onward

---

## 1. Why this document exists

The previous methodology (v1.0) used three bases — Citywide ZHVI, Archetype basket, and Neighborhood — chosen city by city based on whether the citywide median appeared to misrepresent retiree-target neighborhoods. After auditing all 99 cities, the multi-basis approach proved harder to defend than the problem it solved. Archetype basket composition was prone to over-premium-weighting and inadvertent inclusion of out-of-city neighborhoods. The single-MEAN output for cities with genuine geographic income polarization (Memphis, Philadelphia, Pittsburgh, St. Louis) compressed a real range into a single point that misled in the opposite direction.

This document replaces v1.0 with a simpler default and a profile-copy discipline rule.

## 2. The rule

**Default:** Every city's Median Home is its citywide Zillow ZHVI (City geography, All Homes SFR+Condo, Smoothed & Seasonally Adjusted). One source, one number, consistently applied.

**Two exceptions:** St. Paul MN and Wilmington DE retain a published range. Their profile pages are already built around the range framing and the original neighborhood-basis decisions remain documented. These two stay as range cities for historical-continuity reasons only; no new cities will be added to this exception list.

**The Median Honesty Rule.** When a city's citywide ZHVI is significantly dragged below the price of any neighborhood a retiree would realistically target — typically because of distressed-core areas that are not safe retirement options — the profile must carry a visible **Neighborhood Reality Check** callout, above the fold, anchoring the reader before they reach the stat card numbers. The callout names retiree-target neighborhoods and their typical price range. It applies equally to Median Home and Monthly Budget framing, since the budget formula propagates from Median Home.

**Trigger threshold:** retiree-target neighborhoods (documented in the audit log) typically priced **more than 50% above** the citywide median.

**Editorial constraint:** cities meeting the criterion must not be described as "affordable" — in profile copy, comparison pages, landing-page cards, Pinterest pins, or quiz results — without the Neighborhood Reality Check context attached. Their R1 or R2 budget-tier badges must carry a contextual qualifier on the surface where they appear.

## 3. Cities requiring the Neighborhood Reality Check callout

As of v15.1 generation, eight cities meet the trigger threshold:

| City | Citywide median | Retiree-target range | Gap | v15.1 tier |
|---|---|---|---|---|
| Memphis, TN | $195K | ~$408K | +109% | R1 |
| Philadelphia, PA | $240K | ~$684K | +185% | R1 |
| Pittsburgh, PA | $240K | ~$526K | +119% | R1 |
| St. Louis, MO | $235K | ~$494K | +110% | R1 |
| New Orleans, LA | $250K | ~$532K | +113% | R1 |
| Columbus, OH | $235K | ~$493K | +110% | R1 |
| Kansas City, MO | $250K | ~$466K | +86% | R1 |
| Tampa, FL | $400K | ~$569K | +42% | R2 (included as borderline; review during profile pass) |

The Tampa inclusion is borderline (42% gap, below the 50% trigger). It was included because Tampa's archetype-research findings during the v15 audit showed retiree-target neighborhoods consistently above citywide. Reviewer judgment during the profile copy pass: keep the callout if the gap reads as misleading, drop it if the citywide of $400K reads as a fair midpoint.

## 4. The retiree-target neighborhood research is preserved

The v15 audit work (Batches 1–4 plus revisions) identified retiree-target neighborhoods for every city, with documented Zillow ZHVI or proxy values. That research is not discarded with this methodology revision. It becomes the **authoritative editorial reference** for the Neighborhood Reality Check callouts, for comparison-page neighborhood notes, and for any future profile-copy revision that benefits from neighborhood-level color.

See `MedianHomeAuditMASTER.xlsx` City Details sheet for the per-city basket research.

## 5. Refresh cadence

Citywide Zillow ZHVI snapshots refresh monthly. A full database refresh is justified annually, or sooner if the rate environment moves significantly enough to warrant a Monthly Est rebuild (per BUDGET-METHODOLOGY.md Section 11).

## 6. What the Neighborhood Reality Check callout looks like

The callout sits above the stat card in profile pages. Suggested template:

> **A note on the citywide median.** The citywide figure of $X reflects significant neighborhood variation across [City]. Retiree-target neighborhoods like [A], [B], and [C] typically run $Y to $Z. Use the citywide number as a starting reference; the realistic budget for relocating retirees depends on neighborhood choice.

Each callout city's specific neighborhoods are listed in `v14-to-v15_1-audit-log.xlsx` (Callout Cities sheet).

## 7. Relationship to BUDGET-METHODOLOGY.md

This methodology produces the Median Home value that feeds BUDGET-METHODOLOGY.md as a key input. The budget formula does not need to change — it applies the same arithmetic to whatever Median Home value is stored. When this methodology revision is applied, every city's Monthly Est is recomputed against its citywide-based Median Home, and tier assignments follow.

The Neighborhood Reality Check callout therefore acknowledges that BOTH the published Median Home AND the published Monthly Est are honest representations of a city's citywide statistics, while the realistic retiree experience may be measurably different — and the profile reader needs that context before drawing conclusions from the stat card.

## 8. Cities affected by this revision

The v14 → v15.1 transition moved 18 cities from Archetype basis or Neighborhood-range basis back to Citywide. Each of those cities is documented in the audit log with v14 value, v15.1 value, delta, and audit basis history.

Going forward, no new city enters the Archetype or Neighborhood-range pathway. All new additions to the database use Citywide ZHVI from the day they are added.

---

*Methodology v1.1 — June 19, 2026*
*Replaces:* MEDIAN-HOME-METHODOLOGY.md v1.0 and MEDIAN-HOME-AUDIT-REFERENCE.md (12 refinements)
*Audit reference:* MedianHomeAuditMASTER.xlsx, v14-to-v15_1-audit-log.xlsx
