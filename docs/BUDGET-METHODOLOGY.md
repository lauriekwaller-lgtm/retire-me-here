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

Median Home uses the existing DB value, which the database header already documents: Zillow ZHVI (City geography, All Homes SFR+Condo, Smoothed & Seasonally Adjusted), snapshot 2026-04-30. Eight cities (Indianapolis, Memphis, Philadelphia, Pittsburgh, San Antonio, St. Louis, St. Paul, Wilmington DE) use a retiree-target neighborhood basis instead, per Scoring Rubric v3.2 Universal Methodology. The new budget formula applies the same arithmetic to whatever Median Home value is stored, so those eight cities continue to reflect the neighborhood-target experience.

## 5. Non-housing line items

All figures are per couple, per month, in 2026 dollars.

### Healthcare
Federal components (Medicare Part B at $202.90/person and Part D at $38.99/person) are fixed across cities. Medigap Plan G has a base of $165/person, multiplied by a state factor: NY 1.40, NJ 1.30, CA/MA/CT 1.25, FL 1.15, IL 1.10, TX/PA 1.05, baseline 1.00, low-cost rural states 0.88–0.95. Out-of-pocket (dental, vision, copays, deductibles) is $150/couple. Total typical range: $920 to $1,020/mo.

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

Applied to utilities, food, and discretionary line items. Anchored at 1.00 (national baseline). High-cost states: HI 1.25, CA/DC 1.20, NY/MA/AK 1.15, NJ/CT 1.12, WA 1.10, OR/CO/MD 1.07–1.08, AZ/UT/NH/VT/RI/NV 1.03–1.05. Low-cost states: MS 0.86, AR/AL/WV/OK 0.88, KY/LA 0.90, TN/IN/KS 0.92, IA/MO/SD/NE 0.93, SC/MI/WI/OH/NC/GA 0.94–0.95. Baseline 0.96–1.02 for everything else.

**Sources:** BLS regional CPI; EPI Family Budget Calculator metro-level cross-checks (calibration only, not direct input).

## 7. EPI/MIT cross-check protocol

After computing the formula, the non-housing total for each city is cross-checked against EPI Family Budget Calculator (metro level) and MIT Living Wage Calculator (county level). Any city where the formula non-housing total diverges from EPI by more than 15% is flagged for manual review. Note: EPI and MIT are working-family budgets, not retiree budgets, so they are calibration tools, not primary sources. The retiree healthcare cost (Medicare) is substantially higher than the working-age cost they assume, and is treated as the dominant non-housing line.

## 8. Range spread justification

The published range is central × 0.90 to central × 1.12. The 22-point spread mirrors the typical width of the original DB ranges (~$1,000 to $2,000) without overstating precision. Wider spreads imply false certainty about granular city differences the data cannot support. Narrower spreads understate the real variance between a frugal retiree and a comfortable one.

## 9. Tier structure

Cities are grouped into five Budget Ranges using the central estimate:

| Tier | Central estimate | Cities | Framing |
|---|---|---|---|
| R1 — Most Affordable | Under $5,500/mo | 23 | The cheapest in the database. Healthcare and basics covered, with margin. |
| R2 — Affordable | $5,500 to $6,499 | 39 | Mainstream affordable. Largest tier. |
| R3 — Mid-Range | $6,500 to $7,499 | 17 | Typical major-metro and Sun Belt prices. |
| R4 — Premium | $7,500 to $8,999 | 12 | Established retiree destinations and high-cost cities. |
| R5 — Luxury | $9,000+/mo | 9 | Resort towns and luxury enclaves. |

The published quiz currently uses different boundaries (Under $3,500, $3,500–$4,500, $4,500–$6,000, $6,000–$8,000, $8,000+). The quiz boundaries should be updated to match this tier structure as part of the rollout.

## 10. Limitations and known caveats

The formula assumes a relocating couple buying with a mortgage. Single retirees subtract roughly $200/mo from healthcare and ~$100 from food. Cash buyers subtract the P&I line entirely (typically $1,500 to $9,000/mo).

The formula does not adjust for HOA fees in master-planned communities (Sun City, Villages, etc.), which can add $200 to $600/mo. Editorial card prose may note this where relevant.

The eight neighborhood-basis cities reflect retiree-target neighborhood costs in the Median Home value, which then propagates through the formula. The resulting Monthly Est is internally consistent with their D2 score and neighborhood framing. Miami is structurally similar (citywide median is a blend), and may warrant moving onto the neighborhood-basis list in a future revision.

The asymmetric budget bonus in the quiz scoring engine (`Math.max(score, 5)` when city.budgetRange ≤ quizState.budget) does not need to change. Its logic depends on the relative ordering of Budget Range tiers, not the absolute monthly figures.

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
