# RetireMeHere — Complete Scoring Rubric

**All 10 dimensions**
**Version 3.3 · August 8, 2026**

> **Conversion note.** This document replaces `scoring_rubric_v3_2.docx`, which lived in project
> knowledge and never in the repo, in breach of `SITE-OPERATIONS-LOG.md` section 4a. The `.docx` is
> superseded and should be deleted rather than kept as a second copy. Changes made at conversion
> are listed in the changelog at the foot of this document. The largest is that **D4 has been
> restored**: v3.2 declared it retired while it was live in the quiz, scored on all 99 cities, and
> carrying a full priority weight.

---

## How scores work

Each city receives a score of 1–10 on each dimension.

Scores are weighted by the user's quiz priorities:

| Priority | Weight | Notes |
|---|---|---|
| Must Have | 4× | Also applies a minimum threshold filter on D1 |
| Very Important | 3× | |
| Somewhat Important | 2× | |
| Not Important | 1× | |

The final match percentage is a weighted average across all dimensions, plus a budget alignment
bonus (up to +6 points) for cities that closely match the user's stated monthly budget.

### Budget ranges (used for D2 scoring, for filtering, and for the quiz budget question)

| Range | Quiz label | Basis |
|---|---|---|
| Range 1 | Under $5,500 / month | Monthly Est midpoint $4,300–$5,550 |
| Range 2 | $5,500–$6,500 / month | Monthly Est midpoint $5,600–$6,550 |
| Range 3 | $6,500–$7,500 / month | Monthly Est midpoint $6,600–$7,400 |
| Range 4 | $7,500–$9,000 / month | Monthly Est midpoint $7,750–$9,000 |
| Range 5 | $9,000+ / month | Monthly Est midpoint $9,950 and up |

**These bands are display copy derived from data, not the assignment rule.** A city's `Budget
Range` is assigned from its `Monthly Est` in the City Database. The bands above describe where a
*reader's* stated budget falls, and they are derived from the midpoint of each range's `Monthly
Est` span in `CityDatabase_Jul_27_v17`.

**Midpoint, not low end, and this matters.** `Monthly Est` is a range; its low end is the cheapest
month a city ever has. The candidate filter in `index.html` already grants one range of deliberate
stretch (`budgetRange <= quizState.budget + 1`). Deriving the reader-facing bands from the low end
would stack a second, undocumented stretch on top of the first, and the two compound in the same
direction. A reader stating $6,200 would land in Range 3, admitting every Range 4 city, Boulder
among them at $8,000–$10,000 a month.

**Labels are rounded to clean hundreds and the underlying edges are not.** The band edges in
`BUDGET_BANDS` are exact and non-overlapping (`max: 6499`, `min: 6500`); the labels round to
`$6,500`. They therefore disagree by one dollar at each seam, deliberately. Nothing reads the label
as a number.

**Single source of truth.** These bands exist once in `index.html`, as the module-level
`BUDGET_BANDS` constant, read by both `renderBudget()` and the results prose. Do not add a second
copy. Two copies is exactly what produced the August 2026 P0 defect in which the quiz rendered
three byte-identical budget options.

---

## Universal methodology — D2, D6, D9

For three dimensions where a single citywide statistic can mislead — Affordability (D2),
Walkability (D6) and Safety (D9) — RetireMeHere scores the city's retiree-target neighborhoods,
not the citywide average.

Cities like Pittsburgh, Philadelphia, St. Louis and St. Paul have wide internal variation: a
citywide median home price or crime statistic hides both extremes. A retiree choosing where to
live within a city has the practical option of selecting a specific neighborhood, so scoring should
reflect the realistic experience in those neighborhoods, not an average that includes areas no
retiree would actually consider.

**How this works.** For high-variance cities, the `medianHome`, `monthlyEst`, `budgetRange`, D2 and
D9 values reflect the retiree-target neighborhoods identified for that city, typically 3–4 specific
neighborhoods named in the city's profile. For all other cities, citywide statistics are used
because internal variation is small enough that the citywide number is representative.

This approach has always been used for D6, which scores the best walkable neighborhoods rather than
the city average. As of v3.1 the same methodology applies consistently across D2 and D9.

### Cities scored on retiree-target neighborhoods (8)

| City | Retiree-target neighborhoods |
|---|---|
| Indianapolis, IN | Carmel, Zionsville, Fishers, Broad Ripple / Meridian Kessler |
| Memphis, TN | Germantown, Collierville, East Memphis, Bartlett |
| Philadelphia, PA | Rittenhouse Square, Society Hill, Chestnut Hill, Manayunk |
| Pittsburgh, PA | Squirrel Hill, Shadyside, Mount Lebanon, Fox Chapel |
| San Antonio, TX | Alamo Heights, Terrell Hills, Stone Oak, King William |
| St. Louis, MO | Central West End, Clayton, Webster Groves, Kirkwood |
| St. Paul, MN | Summit Hill, Highland Park, Macalester-Groveland, St. Anthony Park |
| Wilmington, DE | Greenville, Hockessin, Brandywine Hundred, Trolley Square |

For these cities the citywide median home price may appear in highlight text for context, but every
score, dollar value and ranking calculation uses the retiree-target neighborhoods as its basis.

> **Open item.** This list of eight is *scoring* methodology. It is not the same thing as the
> Neighborhood Reality Check roster in `MEDIAN-HOME-METHODOLOGY.md`, which is an *editorial*
> mechanism and currently greps to a different count on live. The two lists overlap but are not
> identical, and neither document says so. Reconcile and state the relationship explicitly.

---

## D1 — Airport Access

**Drive time to a major hub, nonstop routes, airlines.**

### What we measure

- Drive time to the nearest major hub airport, not a regional field
- Number of nonstop destinations from the nearest airport
- Quality of airlines serving the city (hub carrier vs. regional only)
- Number of airlines operating

**Special rule.** D1 is the only dimension with a hard filter threshold. *Must Have* admits only
cities scoring 8+. *Very Important*, 6+. *Somewhat Important*, 4+.

| Score | What it means | Example cities |
|---|---|---|
| **10** | Major hub in or adjacent to the city. 100+ nonstop destinations. All major carriers. Under 20 min drive. | Tampa, St. Paul, Fort Worth, Raleigh |
| **8–9** | Strong regional airport, or a major hub 30–45 min out. 50–100 nonstops. Multiple carriers. Reliable connections to most major US cities. | Naples, Delray Beach, Scottsdale, Annapolis |
| **6–7** | Decent regional airport, or a hub 45–60 min out. 25–50 nonstops. Adequate carrier selection. Some gaps in direct service; connections required. | Virginia Beach, Boise, Knoxville, Lexington |
| **4–5** | Limited regional airport, or a hub 60–90 min out. Under 25 nonstops. One or two carriers. Frequent connections required for most travel. | Bloomington, Paducah, Georgetown, Corpus Christi |
| **2–3** | Small regional airport only. Hub 90–120 min out. Under 15 nonstops. Very limited carrier options. | Flagstaff, Sedona, Durango, Jackson Hole |
| **1** | No commercial service nearby. Hub 2+ hrs away. Air travel requires significant logistics. | Very remote locations |

*Data sources: FlightAware nonstop route data, airport passenger statistics, Google Maps drive time
to nearest hub, carrier hub status.*

---

## D2 — Affordability

**Total monthly cost of retiree life: housing plus daily expenses.**

*Database column: `D2 Budget`. Quiz label: "Affordability".*

### What we measure

- Median home price, or median in retiree-target neighborhoods for high-variance cities
- Monthly rental estimates
- Daily living costs: groceries, utilities, transportation, healthcare, dining
- Overall cost of living index vs. national average (100)
- Assigned budget range (1–5) for matching

**Methodology note.** For the high-variance cities listed above, D2 is scored against the median
home price and monthly cost in the retiree-target neighborhoods, not the citywide average. A city
with a $215K citywide median but $700K in the neighborhoods retirees actually buy in is scored on
the $700K figure. Highlight text typically notes both numbers for transparency.

**Scope.** D2 covers both housing and daily living costs. The `monthlyEst` field on each city
represents the full retiree monthly budget: housing, utilities, groceries, healthcare,
transportation and lifestyle.

**This score is relative, not absolute.** It reflects affordability against the national average,
not raw dollars. A city with a $400K median home and COL 105 can score higher than one with a $500K
median and COL 135.

| Score | What it means | Example cities |
|---|---|---|
| **9–10** | Significantly below national average. Median home under $250K. COL under 90. Comfortable on a Range 1 budget. | Chattanooga, Paducah, Hot Springs, Columbus, Kansas City |
| **7–8** | Below or near national average. Median home $250–375K. COL 90–105. Comfortable on a Range 2 budget. | Greenville, Knoxville, Roanoke, Grand Junction, Fayetteville |
| **5–6** | Near to slightly above national average. Median home $375–525K. COL 105–120. Comfortable on a Range 3 budget. | Charleston, Sarasota, Sedona, Santa Fe, Boise |
| **3–4** | Meaningfully above national average. Median home $525–750K. COL 120–145. Comfortable on a Range 4 budget. | Naples, Scottsdale, Fort Myers, Hilton Head, Jackson Hole |
| **1–2** | Significantly above national average. Median home $750K+. COL 145+. Requires a Range 5 budget or higher. | Carlsbad, Napa, Carmel-by-the-Sea, Park City, Vail |

*Data sources: Zillow / Redfin median home prices (2025–2026), NerdWallet / Numbeo cost of living
index, city monthly estimate ranges from local data. Formula and inputs: `BUDGET-METHODOLOGY.md`.
Home value rule: `MEDIAN-HOME-METHODOLOGY.md`.*

---

## D3 — Healthcare Quality

**Hospital ratings, specialist access, senior care.**

### What we measure

- Hospital quality ratings (US News, CMS Stars, Leapfrog grades)
- Number of hospitals in the metro
- Specialist availability: oncology, cardiology, orthopedics
- Drive time to the nearest high-quality hospital where local options are limited
- Senior-specific care availability

| Score | What it means | Example cities |
|---|---|---|
| **10** | Nationally ranked hospital in or adjacent to the city. Top 5% nationally. Multiple CMS 5-star ratings. Full specialist depth on site. No travel needed. | Naples, Sarasota, Tampa, Scottsdale, Ann Arbor, Philadelphia |
| **8–9** | High-performing regional hospital. Leapfrog A. Top 10–25% nationally. Strong specialist access. Minimal travel for complex procedures. | Charleston, Chattanooga, Tucson, Fort Myers, Knoxville, The Woodlands |
| **6–7** | Solid regional hospital. Adequate for most needs. Good general care. Some specialist gaps. Major specialty care may require 30–60 min travel. | Boise, Lexington, Roanoke, Wilmington, Grand Junction |
| **4–5** | Adequate for routine care only. Below-average quality ratings. Limited specialists. Complex care requires travel to a larger city. | Johnson City, Flagstaff, Palm Springs, Sedona, Hot Springs, Paducah |
| **2–3** | Significant quality concerns or very limited access. Serious conditions require substantial travel. | (rare in this rubric's coverage) |
| **1** | No meaningful hospital access in the city. | Extremely remote only |

*Data sources: US News Best Hospitals, CMS Hospital Compare star ratings, Leapfrog Hospital Safety
grades, Healthgrades specialist ratings.*

---

## D4 — Climate Resilience & Insurance

**Disaster exposure, insurance availability and cost.**

*Database column: `D4 Resil.`, with `D4 Resil. Rationale`. Quiz label: "Climate Resilience &
Insurance".*

> **Restored in v3.3.** Version 3.2 stated that "the standalone D4 dimension has been retired
> because it duplicated information already captured in `monthlyEst` and `budgetRange`, and was not
> used by the matching engine." That was true of the *old* D4, which was a daily-cost sub-score
> folded into D2. The D4 slot was subsequently reused for Climate Resilience, and the rubric was
> never updated. As of this version D4 is scored on all 99 cities, is selectable by the reader as a
> quiz priority (`index.html`, `DIMENSIONS`), and carries a full priority weight in the match
> calculation exactly like every other dimension. Every statement in v3.2 describing D4 as retired
> was wrong from the moment the slot was reused.

### What we measure

- Durable hazard geography: FEMA National Risk Index peril patterns
- Current insurance-market conditions, including availability, not only price
- City-specific catastrophic events and their aftermath
- Chronic stressors: drought, heat, smoke, subsidence, sea-level rise
- Scored **higher = safer**, i.e. lower risk

### Scoring

Per-city scores and the one-line rationale behind each sit in
**`docs/D4-resilience-scores-all-100.md`**, which is the authoritative source for D4 values. That
document also records the distribution: minimum 1, maximum 9, mean 5.1, standard deviation 1.83,
which makes D4 the strongest discriminator among the ten dimensions. Florida averages 2.0; the
Great Lakes and inland Northeast set averages 8.0.

> **Gap, and it is a real one.** D4 is the only dimension in this rubric with **no published band
> anchors** — no table saying what separates a 7 from a 5. The scores exist and are reasoned
> individually, but a new city cannot be scored against a written standard the way D1 through D10
> can, and two people scoring the same city would not reliably agree. Anchors should be written
> from the existing 99 rationales rather than invented, then added here. Until that is done, score
> a new city by cross-check against 3–4 named cities with comparable hazard geography and insurance
> market, per step 4 of the new-city sequence below, and record the reasoning.

*Data sources: FEMA National Risk Index, state insurance department filings and market reports,
wildfire and flood hazard mapping, documented catastrophic events. The insurance component moves
fast and should be re-verified at publish.*

---

## D5 — Tax Friendliness

**Social Security, income and property tax burden on retirees.**

### What we measure

- State income tax on Social Security benefits
- State income tax on pension, IRA and 401(k) distributions
- Overall state income tax rate
- Property tax rates and senior exemptions
- Sales tax burden

| Score | What it means | Example cities |
|---|---|---|
| **9–10** | No state income tax on any retirement income. No tax on SS, pension or IRA distributions. Low property tax. Retirement-friendly overall. | Naples, Sarasota (FL); Chattanooga (TN); Henderson (NV); Georgetown (TX) |
| **7–8** | Partial exemptions or a low flat rate. SS exempt but pension / IRA taxed at a low rate. Or: no income tax but higher property taxes. | Bloomington (IN); Fayetteville (AR); Paducah (KY) |
| **5–6** | Moderate burden. Some retirement income taxed. Flat rate 4–5% on most retirement income. Property taxes reasonable. | Boise (ID); Raleigh (NC); Roanoke (VA) |
| **3–4** | Above-average burden for retirees. Higher rates on retirement distributions. SS or pension taxed at a meaningful rate. | Charleston (SC); Annapolis (MD); Portland (ME) |
| **1–2** | High burden. Most retirement income taxed. Top marginal rates apply. No meaningful exemptions. Property taxes also high. | Carlsbad (CA); Napa, Carmel (CA); Palm Springs (CA) |

**Maintenance note.** Tax figures in profile `scoreNotes` carry a year stamp and nothing in the
toolchain ages them. Rates change annually and some change character, not just value: Arkansas was
carried in profile copy as a flat rate when it is graduated. A dated sweep of every tax figure is
an open board item.

*Data sources: state revenue department tax codes, AARP retirement tax guide, Tax Foundation state
rankings, Kiplinger tax-friendly states analysis. Methodology: `D5-TAX-METHODOLOGY.md`.*

---

## D6 — Walkability

**Walk to shops, restaurants and errands without a car.**

*Quiz label: "Walkability & Transit" — the quiz surface names transit explicitly and this rubric
does not. Align the wording at the next revision.*

### What we measure

- Walk Score for the most livable neighborhoods
- Ability to complete daily errands on foot
- Quality and density of walkable retail, dining and services
- Transit support for a car-free or car-light life
- Neighborhood-level walkability, not the city average

**Methodology note.** D6 has always scored the best walkable retiree neighborhoods rather than the
city average. As of v3.1 this is documented as part of the Universal Methodology shared with D2 and
D9. For high-variance cities, the same retiree-target neighborhoods are used across all three.

| Score | What it means | Example cities |
|---|---|---|
| **9–10** | Genuinely car-free living possible. Walk Score 85+. Daily errands on foot. Shops, dining and services within steps. | Portland ME (Old Port), Alexandria VA, Philadelphia |
| **7–8** | Very walkable best neighborhoods. Walk Score 70–85. Most errands walkable. Car optional, not required. Strong pedestrian infrastructure. | Charleston (peninsula), Savannah, Santa Fe, Annapolis |
| **5–6** | Moderately walkable. Walk Score 50–70. Some errands walkable. Car still useful daily. Pockets of walkability, not citywide. | Knoxville, Boise, Bloomington, Lexington |
| **3–4** | Limited walkability. Walk Score 30–50. Car required for most daily needs. Walkable only in small specific areas. | Scottsdale, Naples, St. George, Sedona |
| **1–2** | Car fully required. Walk Score under 30. Suburban or desert grid, not designed for walking. No meaningful pedestrian infrastructure. | Henderson, Georgetown, Fort Myers, Cape Coral |

*Data sources: Walk Score city and neighborhood data, Google Maps walkability assessment, local
knowledge of neighborhood character.*

---

## D7 — Outdoor Recreation

**Trails, hiking, parks, kayaking, cycling.**

### What we measure

- Proximity and quality of trail systems
- Variety of outdoor activities: hiking, cycling, water, winter sports
- Year-round usability of outdoor resources
- Access to natural landscapes: mountains, water, forests, desert
- Quality of urban parks and greenways

| Score | What it means | Example cities |
|---|---|---|
| **10** | World-class, multiple outdoor ecosystems. Year-round usability across activity types. National park or equivalent in or adjacent to the city. | Bend, Asheville, St. George, Park City, Jackson Hole, Vail |
| **8–9** | Excellent access. Strong trail network. Multiple activity types. 3+ seasons of strong outdoor usability. | Chattanooga, Tucson, Boise, Knoxville, Durango, Missoula |
| **6–7** | Good. Solid parks and trails, one strong outdoor feature. Access available but limited in variety. May require driving for the best of it. | Greenville, Roanoke, Virginia Beach, Portland ME, Grand Junction |
| **4–5** | Adequate. Some parks and greenways. Limited variety. Flat or urban terrain. Outdoor recreation is not a city strength. | Corpus Christi, Georgetown, Paducah |
| **2–3** | Weak. Minimal trail or natural access. Flat urban landscape. Requires long drives. Not a viable outdoor destination. | Columbus, Indianapolis, Memphis, Kansas City, Henderson, Rio Rancho |
| **1** | Essentially none within reasonable distance. | Extreme suburban / urban |

**Audit note (April 2026).** Flat coastal cities — Naples, Sarasota, Delray Beach, Hilton Head,
Fort Myers — previously scored 7–9. They have excellent beaches, golf and water recreation but do
not meet the 8–9 anchor of "strong trail network, multiple activity types, 3+ seasons of strong
outdoor usability." Re-scored into the 6–7 range. St. Petersburg retains 7 because the Pinellas
Trail is a genuine long-distance trail asset. Beach access is captured in the Setting tag and the
city's highlight text, not in D7.

*Data sources: AllTrails city trail counts and ratings, Trust for Public Land park rankings,
outdoor recreation audits, local trail authority data.*

---

## D8 — Active Wellness

**Gyms, pickleball, fitness centers, rec centers.**

*Quiz label: "Sports & Fitness". Two names for one dimension; align at the next revision.*

### What we measure

- Dedicated senior fitness infrastructure: rec centers, Silver Sneakers
- Pickleball court availability and culture
- Tennis, golf and swimming infrastructure
- Boutique fitness studios
- 55+ community fitness programming

**This dimension is about built infrastructure, not natural access.** Natural access is D7. A city
with great hiking and no rec centers scores high on D7 and not necessarily on D8.

| Score | What it means | Example cities |
|---|---|---|
| **10** | Gold-standard 55+ wellness infrastructure. Multiple large rec centers. Pickleball everywhere. Silver Sneakers widely accepted. Senior programming. | Naples, Scottsdale, Georgetown (Sun City) |
| **8–9** | Strong senior wellness culture and infrastructure. Good rec centers with dedicated senior programming. Pickleball and tennis well developed. | Sarasota, Delray Beach, St. George, Henderson, Park City |
| **6–7** | Solid. Standard rec center and fitness access. Some pickleball. Adequate gym options. Basic senior programming. | Chattanooga, Boise, Roanoke, Virginia Beach, The Woodlands, Durango |
| **4–5** | Average. Generic gym chains, limited senior focus. Growing pickleball but not a destination. No standout senior wellness infrastructure. | Columbus, Indianapolis, Kansas City, Memphis |
| **2–3** | Below average. Limited options. No dedicated senior fitness culture. Basic gym access only. | Paducah, Hot Springs, some small cities |
| **1** | Essentially no fitness infrastructure. | Extremely small or remote |

**Audit note (April 2026).** Small mountain towns — Sun Valley (pop. ~1,400), Sedona (~10K),
Steamboat Springs (~13K), Whitefish (~9K) — previously scored 7–8. Population scale alone
constrains the built rec-center infrastructure those scores require. Re-scored into the 5–6 range.
Durango is the exception at 7 because the Durango Community Recreation Center has documented Silver
Sneakers, Renew Active, 6 pickleball courts and 60–70 fitness classes a week: genuine 55+
infrastructure at small-town scale.

*Data sources: Silver Sneakers gym locator, USTA tennis facility data, USA Pickleball court
locator, municipal rec center audits, local YMCA data.*

---

## D9 — Safety

**Violent and property crime rates.**

### What we measure

- Violent crime rate per 100,000 residents
- Property crime rate per 100,000 residents
- CrimeGrade.org city score and percentile
- Neighborhood-level safety variation
- Trend direction, improving or worsening

**Methodology note.** For the high-variance cities listed above, D9 is scored against the
retiree-target neighborhoods, not the citywide crime rate. Citywide statistics for Pittsburgh,
Philadelphia, St. Louis and similar cities are dragged down by neighborhoods no retiree would
consider, which obscures genuine 80th–95th-percentile safety in target areas like Squirrel Hill,
Chestnut Hill or Central West End. Where this applies, the city's pros and cons text directs
readers to specific safe neighborhoods.

| Score | What it means | Example cities |
|---|---|---|
| **9–10** | 90th percentile or above nationally. Violent crime well below national average. Retirees consistently report feeling safe. | Naples, Henderson, Georgetown, St. George |
| **7–8** | 70th–90th percentile. Below-average crime. Safe overall. Neighborhood selection still matters. | Sarasota, Boise, Fayetteville, Knoxville, Pittsburgh (target neighborhoods), St. Paul (target neighborhoods) |
| **5–6** | 40th–70th percentile. Near national average. Mixed: some neighborhoods better than others. Typical city caution applies. | Virginia Beach, Lexington, Charlottesville, Napa |
| **3–4** | Below national average. 20th–40th percentile. Crime concentrated in specific areas. Neighborhood selection critical. | Savannah, Chattanooga, Asheville, Bloomington |
| **1–2** | Significant concerns. Below 20th percentile. High crime across many areas. | Citywide figures for Memphis and San Antonio fall here; their retiree-target neighborhoods score 7+ |

*Data sources: CrimeGrade.org city crime percentile rankings (2024–2025), FBI Uniform Crime Report,
NeighborhoodScout crime index.*

---

## D10 — Community & Social Life

**Arts, dining, events, volunteering, sports.**

### What we measure

- Quality and variety of the dining scene
- Arts infrastructure: museums, theater, galleries, music
- Community events and festivals
- Volunteer and civic engagement opportunities
- Spectator sports culture
- Social scene for retirees specifically

| Score | What it means | Example cities |
|---|---|---|
| **10** | World-class cultural destination. Major arts institutions, James Beard dining, signature festivals, deep civic culture. | Santa Fe |
| **8–9** | Excellent. Strong local arts, great dining, active civic life, signature events. Among the best in its size category nationally. | Charleston, Savannah, Philadelphia, Portland ME, St. Augustine, Pittsburgh |
| **6–7** | Good. Solid dining, community events, arts presence, active local culture. Satisfying for most retirees' social needs. | Roanoke, Greenville, Boise, Knoxville, Colorado Springs |
| **4–5** | Moderate. Some dining, limited arts, quiet community life. Basic social infrastructure. Adequate but not enriching for culturally active retirees. | Henderson, Rio Rancho, Johnson City, Grand Junction |
| **2–3** | Thin. Few dining or arts options. Limited social infrastructure. Retirees likely to feel culturally isolated. | Very small towns, remote resort communities |
| **1** | Essentially none. | Extreme rural only |

*Data sources: Yelp dining scene rankings, NEA arts vibrancy index, WalletHub social life rankings,
local cultural organization audits, AARP livability community scores.*

---

## Climate scoring (DC — not a numbered dimension)

The reader selects one climate preference, which determines how climate scores are calculated for
matching.

### Component scores

| Component | Meaning | Scale |
|---|---|---|
| **W** | Winter severity | 10 = warm mild winters, 1 = brutal cold |
| **H** | Summer comfort | 10 = very comfortable, 1 = extreme heat |
| **M** | Humidity / dryness | 10 = very dry, 1 = very humid |

### Mild year-round

`Score = (W × 0.40) + (H × 0.35) + (M × 0.25)`

Rewards comfortable temperatures across all 12 months. Penalizes extreme heat *and* extreme cold.

### Warm & dry

`Score = (W × 0.40) + (M × 0.40) + (H × 0.20)`

Rewards warm winters *and* low humidity. Scottsdale, Sedona and Santa Fe score high. Penalizes
humid cities like Savannah and Tampa regardless of warmth.

### Warm, humidity OK

`Score = W only`

Rewards mild winters. Hot humid summers acceptable. Florida and coastal Southeast cities score
high.

### Four seasons

| Winter severity | Score | Reasoning |
|---|---|---|
| W ≤ 3 | 8 | Real seasons |
| W 4–6 | 9 | Ideal four seasons |
| W 7 | 6 | Not quite four seasons |
| W 8+ | low | No real winter |

*Humidity and heat scoring detail: `HUM-HEAT-Scoring-Guide.md`.*

---

## Budget alignment bonus

The matching engine adds a bonus for cities matching the reader's stated budget range:

| Budget difference | Bonus |
|---|---|
| 0 | +6 |
| 1 | +4 |
| 2 | +2 |
| 3+ | none |

This lets a city priced exactly for the reader's budget float slightly above an equally scored city
outside their range.

> **Note.** The bonus implemented in `index.html` is *asymmetric* — it rewards being under budget
> and penalizes being over, which the symmetric table above does not describe. The implementation
> is the behaviour readers actually get. This table should be rewritten to match it, or the
> implementation changed to match this table. Do not assume the table is authoritative.

---

## Scoring guidelines for new cities

1. Research all 10 dimensions using the primary data sources listed above.
2. Score each dimension 1–10 against the rubric anchors.
3. Assign a budget range (1–5) from the monthly cost estimate, per `BUDGET-METHODOLOGY.md`.
4. **Cross-check.** Compare your scores to 2–3 similar cities already scored. If Roanoke is a 7 on
   D7, a new Appalachian city with similar outdoor access should land within 1 point.
5. **Reserve 9–10 for the genuinely exceptional.** Ask whether this is truly one of the best in the
   country on that dimension. If you are not certain, score 8.
6. **Do not inflate D8 or D10.** Both were historically over-scored. Most cities land 5–7. Reserve
   8–10 for exceptional cases. Apply the audit principles above: flat coastal cities are not D7=8+
   candidates, and small mountain towns are not D8=8+ candidates without documented 55+
   infrastructure.
7. **For high-variance cities**, apply the Universal Methodology: identify retiree-target
   neighborhoods and score D2, D6 and D9 against those rather than the citywide average. Document
   the chosen neighborhoods in the city's profile.
8. **D4 has no published anchors.** Score by cross-check against 3–4 named cities with comparable
   hazard geography and insurance market, and write the rationale into
   `D4-resilience-scores-all-100.md` alongside the existing 99.
9. Document your reasoning for D4, D7, D8 and D10 in the score reasoning document.

**Scores are read from the City Database and never from research.** Research supplies supporting
colour only: price checks, hospital rankings, airport routes. If the database is not to hand, stop
and get it rather than scoring from research.

---

## Changelog

### v3.3 — August 8, 2026 (conversion to markdown, committed to `docs/`)

- **Converted from `scoring_rubric_v3_2.docx` to markdown and committed to `docs/`.** The `.docx`
  lived only in project knowledge, in breach of `SITE-OPERATIONS-LOG.md` section 4a, with no
  version history. It is superseded and should be deleted, not retained as a second copy.
- **D4 restored.** v3.2 declared D4 retired and omitted it entirely, documenting nine of the ten
  dimensions the site scores. D4 is live as Climate Resilience & Insurance, scored 1–9 on all 99
  cities, reader-selectable and fully weighted. Section added, with the `D4-resilience-scores`
  document named as the source of values and the missing band anchors flagged as a gap.
- **Budget ranges reconciled.** v3.2 carried Range 1 as "under $3,500/mo", an empty set against a
  database whose cheapest city starts at $3,800, and the remaining bands did not match anything
  rendered. Replaced with the five bands shipped in `BUDGET_BANDS`, with the derivation, the
  midpoint-not-low-end reasoning, and the label-rounding convention recorded.
- **Three drifts flagged rather than silently resolved**, because each needs a decision, not an
  edit: the retiree-target-neighborhood list of 8 versus the Neighborhood Reality Check roster; the
  symmetric budget-bonus table versus the asymmetric implementation; and dimension names differing
  between this rubric and the quiz (D6, D8).
- Dimension sections annotated with their database column names and quiz labels.

### v3.2 — April 2026

- D2 widened to cover housing and daily living costs.
- Old D4 (daily-cost sub-score) retired into D2. *The D4 slot was later reused for Climate
  Resilience; see v3.3.*
- D7 and D8 audit notes added: flat coastal cities re-scored on D7, small mountain towns re-scored
  on D8.

### v3.1

- Universal Methodology extended from D6 to D2 and D9.

---

*RetireMeHere.com · Scoring Rubric v3.3 · August 8, 2026*
