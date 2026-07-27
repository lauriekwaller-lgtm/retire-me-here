# RetireMeHere Budget Methodology
**Established:** June 16, 2026
**Applies to:** Monthly Est column and Budget Range column in CityDatabase
**Audit file:** Budget-Audit-Jun-16-2026.xlsx
**Refresh cadence:** Mortgage rate quarterly, Medicare premiums annually (each November), full recompute annually or when a major input shifts

---

## 1. Why this document exists

The original Monthly Est values for the 100 cities had no documented methodology. Reverse-engineering them showed an implicit cash-buyer or partial-budget framing that broke down at the low end (Johnson City's published $2,500 to $3,200/mo would not cover Medicare premiums plus housing for a couple with a mortgage). This document replaces that legacy with a transparent, reproducible formula and names every source.

The result is a single canonical budget number per city, computed the same way for all 100 cities, defensible to a reader with a calculator.

## 2. Scope and assumptions

The figure represents the realistic monthly cost for a retired couple (both age 65+) relocating to the city in 2026 and **buying with a mortgage**. The mortgaged framing is deliberate. It tracks what a relocating retiree without large home equity actually faces, and it also reasonably approximates a renter in most markets (a landlord's P&I plus taxes plus insurance plus a small margin is roughly what passes through to monthly rent). It does NOT represent a retiree who bought their home outright with proceeds from a previous sale. A cash-buyer toggle is a future site feature; until then, the published number is mortgaged.

The figure includes housing, healthcare, utilities, food, transportation, and discretionary. It excludes state income tax (D5 already carries that signal independently), federal income tax, long-term care insurance, large discretionary travel, gifts, and savings.

## 3. The formula

For each city, the **central monthly estimate** is:

```
central = housing + healthcare + utilities + food + transportation + discretionary
```

The **published range** is:

```
lean (low end) = central × 0.90
comfortable (high end) = central × 1.12
```

Both ends are rounded to the nearest $100. The asymmetry around the central is intentional: discretionary spending has more upside (dining out, travel, hobbies) than downside (you cannot meaningfully cut Medicare).

## 4. Housing line items

| Component | Formula | Source |
|---|---|---|
| Principal and interest | 30-year fixed, 20% down, on Median Home value | Freddie Mac PMMS 6.52% (week of 06/11/2026) |
| Property tax | Median Home × PropTax Rate % column ÷ 12 | Existing DB column, retained as-is |
| Homeowners insurance | HO Insur Est $/yr column ÷ 12 | Existing DB column, retained as-is |

Median Home uses the existing DB value, which the database header already documents: Zillow ZHVI (City geography, All Homes SFR+Condo, Smoothed & Seasonally Adjusted), snapshot 2026-06-30. The column was rebased for all 99 cities on 2026-07-27, the first execution of the annual refresh described in MEDIAN-HOME-METHODOLOGY.md section 6; before that date it was a 2020-2026 patchwork. All 99 cities use the citywide Zillow ZHVI, per MEDIAN-HOME-METHODOLOGY.md v1.2. No city uses a retiree-target neighborhood basis. The earlier eight-city carve-out (Indianapolis, Memphis, Philadelphia, Pittsburgh, San Antonio, St. Louis, St. Paul, Wilmington DE) was retired by v1.2 and this paragraph is its fossil, struck 2026-07-13. Where retiree-target neighborhoods run materially above the citywide median, that is disclosed in prose via a Neighborhood Reality Check note on the city profile, not by altering the number.

## 5. Non-housing line items

All figures are per couple, per month, in 2026 dollars.

### Healthcare
Federal components (Medicare Part B at $202.90/person and Part D at $38.99/person) are fixed across cities. Medigap Plan G has a base of $165/person, multiplied by a per-state factor. The exact factor for every state in the database is tabulated in Section 6; do not read the factor off a range. Out-of-pocket (dental, vision, copays, deductibles) is $150/couple. Total range across the 99 cities: $924/mo (SD, factor 0.88) to $1,096/mo (NY, factor 1.40). Nine distinct values, one per Medigap factor.

**Sources:** CMS 2026 Premium Announcement (Nov 14 2025); KFF Medicare Supplement Insurance briefs; AHIP 2025 Medigap buyer's guide.

### Utilities
Baseline $400/mo per couple, multiplied by a state cost-of-living modifier (see Section 6). Climate adjustments: HEAT score 8+ adds $80 (heavy summer AC), HEAT 6–7 adds $40, HEAT ≤3 subtracts $20. Climate Warm-W 1–3 adds $80 (heavy winter heating), 4–5 adds $30, 9+ subtracts $30.

**Sources:** BLS Consumer Expenditure Survey 65+ households (2024 reference year); EIA state-level residential electricity rates.

### Food
Baseline $750/mo per couple, multiplied by the state cost-of-living modifier. This sits at the USDA Moderate Plan for an age 51–70 couple in 2026.

**Sources:** USDA Cost of Food at Home plans (Moderate, June 2026); MIT Living Wage Calculator for metro-level cross-check.

### Transportation
Walkability-tiered, using the existing D6 score:

| D6 score | Monthly | Implied profile |
|---|---|---|
| 8 or 9 | $400 | One car or none; transit available |
| 6 or 7 | $550 | Two cars, lower mileage |
| 4 or 5 | $650 | Two cars, typical retiree use |
| 3 or below | $700 | Car-required, full two-car costs |

**Sources:** AAA "Your Driving Costs" 2025; BLS CE Survey 65+ transportation expenditures.

### Discretionary
Baseline $500/mo per couple, multiplied by the state cost-of-living modifier. Covers dining out, entertainment, hobbies, gifts, and household discretionary. Does not include large travel or major purchases.

**Sources:** BLS Consumer Expenditure Survey 65+, entertainment + misc categories.

## 6. State cost-of-living modifier

Two per-state multipliers are used. Both are exact values, not ranges.
Earlier versions of this document published them as ranges ("low-cost rural
states 0.88-0.95"), which is not precise enough to recompute a city from, and
which silently collapsed real distinctions: OR and CO were both "1.07-1.08"
but are 1.08 and 1.07; SC and GA were both "0.94-0.95" but are 0.94 and 0.95.

**Cost-of-living modifier (COL).** Applied to the utilities, food, and
discretionary baselines. Anchored at 1.00 (national baseline).

| COL | States |
|---|---|
| 0.88 | AL, AR, OK |
| 0.90 | KY, LA |
| 0.92 | IN, TN |
| 0.93 | IA, MO, SD |
| 0.94 | OH, SC |
| 0.95 | GA, MI, NC, WI |
| 0.96 | TX |
| 0.98 | NM, PA |
| 1.00 | DE, ID, ME, WY |
| 1.02 | FL, MN, MT |
| 1.03 | AZ, UT, VA |
| 1.05 | NH, NV, VT |
| 1.07 | CO, MD |
| 1.08 | OR |
| 1.10 | WA |
| 1.15 | MA, NY |
| 1.20 | CA |

**Medigap state factor.** Applied to the $165/person Plan G base in Section 5.
It is a separate scale from COL and the two do not track each other: TX is 0.96
on COL but 1.05 on Medigap; MN is 1.02 on COL but 0.95 on Medigap.

| Factor | States |
|---|---|
| 0.88 | SD |
| 0.90 | IA, WY |
| 0.92 | AL, AR, KY, OK, TN |
| 0.95 | MN, WI |
| 1.00 | AZ, CO, DE, GA, ID, IN, LA, MD, ME, MI, MO, MT, NC, NH, NM, NV, OH, OR, SC, UT, VA, VT, WA |
| 1.05 | PA, TX |
| 1.15 | FL |
| 1.25 | CA, MA |
| 1.40 | NY |

**Coverage.** These tables cover the 39 states with a city in the database, and
nothing else. That is deliberate: an unexercised value is an unverified value.
Adding a city in a 40th state requires deriving both multipliers for that state
first (BLS regional CPI for COL, KFF/AHIP state Medigap averages for the
factor), adding the rows here, and recording the derivation in the ops log.
Do not infer a value from a neighboring state.

**Sources:** BLS regional CPI; EPI Family Budget Calculator metro-level cross-checks (calibration only, not direct input).

## 7. EPI/MIT cross-check protocol

After computing the formula, the non-housing total for each city is cross-checked against EPI Family Budget Calculator (metro level) and MIT Living Wage Calculator (county level). Any city where the formula non-housing total diverges from EPI by more than 15% is flagged for manual review. Note: EPI and MIT are working-family budgets, not retiree budgets, so they are calibration tools, not primary sources. The retiree healthcare cost (Medicare) is substantially higher than the working-age cost they assume, and is treated as the dominant non-housing line.

## 8. Range spread justification

The published range is central × 0.90 to central × 1.12. The 22-point spread mirrors the typical width of the original DB ranges (~$1,000 to $2,000) without overstating precision. Wider spreads imply false certainty about granular city differences the data cannot support. Narrower spreads understate the real variance between a frugal retiree and a comfortable one.

## 9. Tier structure

Cities are grouped into five Budget Ranges using the central estimate:

| Tier | Central estimate | Cities | Framing |
|---|---|---|---|
| R1 — Most Affordable | Under $5,500/mo | 30 | The cheapest in the database. Healthcare and basics covered, with margin. Largest tier. |
| R2 — Affordable | $5,500 to $6,499 | 29 | Mainstream affordable. |
| R3 — Mid-Range | $6,500 to $7,499 | 19 | Typical major-metro and Sun Belt prices. |
| R4 — Premium | $7,500 to $8,999 | 12 | Established retiree destinations and high-cost cities. |
| R5 — Luxury | $9,000+/mo | 9 | Resort towns and luxury enclaves. |

The quiz rollout is complete. `index.html` carries these boundaries
verbatim ('$5,500','$5,500-6,499','$6,500-7,499','$7,500-8,999','$9,000') and
no longer references the retired Under-$3,500 set.

The counts above are as of the 2026-07-27 ZHVI rebase, which moved 14 cities
across a tier boundary. They are a snapshot, not an invariant: any rebase of
`Median Home` moves them. Treat a mismatch between this table and the database
as this table being stale.

**Reproducibility.** The formula in Sections 3 through 6 is complete. With the
exact multipliers tabulated in Section 6, it reproduces all 99 rows of
CityDatabase_Jul_27_v17.xlsx exactly, both the published Monthly Est string and
the Budget Range integer, with zero mismatches. Anything less than an exact
reproduction means an input drifted, and that is the condition the boarded
`Monthly Est == f(Median Home)` gate check asserts.

## 10. Limitations and known caveats

The formula assumes a relocating couple buying with a mortgage. Single retirees subtract roughly $200/mo from healthcare and ~$100 from food. Cash buyers subtract the P&I line entirely (typically $1,500 to $9,000/mo).

The formula does not adjust for HOA fees in master-planned communities (Sun City, Villages, etc.), which can add $200 to $600/mo. Editorial card prose may note this where relevant.

No city uses a neighborhood basis. See Section 4.

There is no budget bonus in the quiz scoring engine. An earlier version of this document described one (`Math.max(score, 5)` when `city.budgetRange <= quizState.budget`) as live. It was not. Git history shows the line was present in the first upload of index.html (2026-03-29) and that D2 has never once appeared in the DIMENSIONS array the scoring loop iterates, so the guard could never evaluate true. It never executed. Both guards were deleted 2026-07-13, a no-op by construction.

Budget is not a weighted dimension and by design never has been. Asking a reader how important affordability is has no discriminating power (everyone answers 'very'), so the quiz asks for their monthly budget instead, which is a fact about them, and applies it as a hard filter: `candidates.filter(c => c.budgetRange <= quizState.budget + 1)`. D2 is a reader-facing display score on profiles and comparison tables. It is not a matching input.

## 11. Refresh and versioning

The mortgage rate is the most volatile input. A 1-point swing in mortgage rates moves the central estimate by roughly $200 to $400/mo on a typical home. Quarterly rechecks of Freddie Mac PMMS are reasonable; a full recompute is justified when the rate moves 50 basis points or more from the snapshot value.

Medicare premiums refresh in mid-November each year (CMS announcement). The annual rebuild should incorporate the new Part B, Part D, and Medigap figures.

Each rebuild increments the DB filename (current: CityDatabase_Jun_9_v14.xlsx). The new methodology produces a v15 once the audit is approved.

## 12. Future enhancements

**Cash-buyer toggle.** A reader who funded the move from prior home-sale proceeds drops the P&I line entirely. A site-level toggle that switches between mortgaged and cash views would broaden the audience without compromising the published number's default framing. Defer until traffic signal warrants the engineering.

**HOA-inclusive variant.** Naples, The Villages, Scottsdale active-adult communities, Sun City, and similar markets carry meaningful HOA fees. A flag in the DB plus a card-level note ("HOA fees common, typically $X/mo") would preserve accuracy without altering the headline number.

**State-by-state Medigap precision.** The current state modifier is a coarse five-bucket approximation. KFF publishes annual state-level data; a finer-grained version would be straightforward once an annual refresh process is in place.

---

*Methodology v1.0 — June 16, 2026*
*Inputs snapshot: Freddie Mac PMMS 06/11/2026 (6.52%), CMS 2026 Part B announcement (Nov 14 2025)*
*Audit file: Budget-Audit-Jun-16-2026.xlsx*


---

## 13. D2 Budget scoring (added 2026-07-13)

D2 is scored from the **central monthly estimate**, on fixed dollar thresholds:

| D2 | Central estimate |
|---|---|
| 10 | under $4,600 |
| 9 | $4,600 to $4,999 |
| 8 | $5,000 to $5,499 |
| 7 | $5,500 to $5,999 |
| 6 | $6,000 to $6,499 |
| 5 | $6,500 to $7,499 |
| 4 | $7,500 to $8,499 |
| 3 | $8,500 to $9,499 |
| 2 | $9,500 to $11,499 |
| 1 | $11,500+ |

**Why this replaced the old rule.** Scoring Rubric v3.2 anchors D2 on median home price plus a
COL index. The COL index column does not exist in the database and never has, so half that rule
was unauditable. The rubric's own example cities also contradict its bands: Fort Myers (central
$5,785) is listed at D2 3-4 while Grand Junction (central $6,193) is listed at 7-8, so a city
that costs $400/mo more scores four points better. There was nothing coherent to recover.

The central estimate is the better basis regardless. It already contains housing, healthcare,
utilities, food, transport, and discretionary, computed identically for all 99 cities with every
source named in this document. It is a cost-of-living measure, retiree-specific, and better than
any index we could buy. No new data source is needed.

**Thresholds are absolute, not percentile.** A percentile scale would re-rank every city each
time one is added. Absolute dollar thresholds do not drift.

**Why D2 was wrong before.** The V15.1 rebuild (June 19) recomputed Median Home, Monthly Est, and
Budget Range. It did not touch D2. The D2 column therefore stayed scored against the pre-June
budget figures, which were far too low, producing a uniform downward offset across the database:
72 of 99 cities were wrong, mean shift +0.97. Rebuilt 2026-07-13.
