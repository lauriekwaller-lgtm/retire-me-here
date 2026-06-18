# RetireMeHere Median Home Methodology
**Established:** June 17, 2026
**Applies to:** Median Home column in CityDatabase, and the derived Monthly Est via BUDGET-METHODOLOGY.md
**Companion docs:** BUDGET-METHODOLOGY.md, SITE-OPERATIONS-LOG.md

---

## 1. The principle

**The Median Home value for each city represents what a financially-secure relocating retiree would actually pay across the realistic spectrum of submarkets they would consider in that metro.**

The audience this serves: a relocator with $300K to $1M+ in proceeds from a prior home, choosing a destination, prioritizing safety, livability, and value. Not a luxury buyer at the top; not a budget buyer at the bottom; the realistic spread across both.

Citywide statistical medians often misrepresent this number, particularly in large metros where distressed neighborhoods drag the average below anything a relocating retiree would buy. The methodology below corrects for that systematically and consistently.

## 2. Two valid bases

Every city in the database uses one of two bases:

**Citywide.** The citywide median accurately represents the retiree experience. Used for small towns, explicit retiree destinations, and cities without significant internal price variation. Examples: Naples, Bend, Asheville, Carmel, Vail, Park City, Sarasota, Sun Valley.

**Archetype basket.** The citywide median is misleading because the metro has significant internal price variation by neighborhood. A weighted basket of representative submarkets is used instead. Examples: Miami, St. Louis, Phoenix, Atlanta, Dallas, Houston, Cleveland.

The Median Home Basis column in the database records which is used.

## 3. The archetype framework

When a city uses the archetype basket, the basket is constructed from these archetypes:

| Archetype | Description |
|---|---|
| Urban walkable | Dense, walkable neighborhood (city proper or close-in). Condos and small SFHs typical. For retirees who want to reduce car dependence. |
| Established premium suburb | Mature, leafy suburb with a walkable village center. Older housing stock. Highest tier of the basket. |
| Newer amenity-rich suburb | Newer construction, planned or master-planned feel. Conveniences nearby. Mid-to-upper tier of the basket. |
| Value/entry-level option | Farther out or smaller-scale. Same metro, lower price point. Entry tier of the basket. |
| Active-adult community (55+) | Only included for cities with an iconic 55+ example (Sun City Phoenix, The Villages, Robson communities). Skipped otherwise. |
| **City-specific archetype** | A maximum of one additional archetype where the city has a genuinely distinct local pattern not captured by the standard menu (e.g., Miami's coastal/island, New Orleans' historic core). Must be documented and defended. |

The basket includes **one representative submarket per archetype**, not multiple. If a city has both Kirkwood and Webster Groves as candidates for "established premium suburb," you pick one. The other is implicitly represented. The total basket has 3 to 5 picks. Five is the absolute maximum.

## 4. The five-question inclusion test

Each candidate submarket must pass all five to be included in the basket:

1. **Safety.** Crime at or near metro median. Would not require active avoidance by a security-conscious buyer with choices.
2. **Quality.** Housing stock maintained, infrastructure intact, no significant disinvestment trajectory. Stable or appreciating.
3. **Amenity access.** Grocery, healthcare, restaurants within practical reach. Walking distance is a plus, not required.
4. **Retiree-realistic.** Not student-dominated, not exclusively young-family, not transient/nightlife-dominated.
5. **Editorial credibility.** Would appear in a legitimate "best places to retire in [city]" article or in a relocation realtor's materials for retirees.

If a candidate fails any one of the five, it is excluded. No negotiation, no editorial fudge.

## 5. Selecting between candidates within an archetype

When multiple submarkets pass the five tests for the same archetype, apply these tiebreakers in order:

1. **National recognition.** A submarket commonly named in national retirement coverage wins over a hyperlocal favorite. Reduces dependence on the editor's personal knowledge.
2. **Centrality within the metro.** A submarket closer to the metro core wins over one farther out, when other factors are equal. The retiree relocating from out-of-state will weight central submarkets more heavily.
3. **Price representativeness.** If two candidates are equally valid, pick the one whose median sits closer to the middle of the archetype's typical price band, not the extreme.
4. **Editorial judgment.** When tied on all three above, choose and document the reasoning.

The chosen submarket is the representative. The submarkets not chosen are NOT excluded from the city's appeal; they are implicitly represented by their archetype peer. The basket is a sampling frame, not an exhaustive list.

## 6. Computation

The Median Home value is the **simple arithmetic mean** of the chosen submarkets' median home values (sourced from Zillow ZHVI at neighborhood/ZIP level where available, or the closest analog).

Simple mean is used rather than weighted mean for three reasons: it requires no defensible weighting scheme (and any scheme would be debated forever), it is transparent and reproducible by any future operator, and across a basket of 3-5 picks the difference between mean and weighted-mean is rarely material.

The Monthly Est figure derives from this Median Home value via the BUDGET-METHODOLOGY.md formula, unchanged.

## 7. Documentation requirement

Every city in the database carries two columns:

**Median Home Basis** — either "Citywide" or "Archetype basket"

**Median Home Source** — for Citywide: "Zillow ZHVI [snapshot date]". For Archetype basket: a comma-separated list of the representative submarkets, e.g., "Central West End, Clayton, Chesterfield, Sunset Hills"

This makes every Median Home value auditable by anyone reading the database. A future operator (or a skeptical reader) can see immediately how the number was constructed and challenge it on the methodology, not on opaque editorial choice.

## 8. Worked examples

### Example A: St. Louis (archetype basket)

| Archetype | Representative | Notes |
|---|---|---|
| Urban walkable | Central West End | Healthcare-adjacent, walkable, condo-rich; the cleanest "urban walkable" archetype representative in the metro |
| Established premium suburb | Clayton | National recognition; the metro's premier address; Kirkwood/Webster Groves/Ladue are implicitly represented |
| Newer amenity-rich suburb | Chesterfield | More central than Wildwood; stronger amenity profile for retirees |
| Value/entry-level | Sunset Hills (South County) | Closer to metro core than Cottleville; common retiree choice |

Active-adult: skipped (no iconic 55+ community at national stature in this metro).
City-specific: none.

Submarkets implicitly represented (not in basket but covered by archetype peer): Ladue, Kirkwood, Webster Groves, Wildwood, Cottleville, Affton, Crestwood, Olivette.

### Example B: Miami (archetype basket, with city-specific addition)

| Archetype | Representative | Notes |
|---|---|---|
| Established premium suburb | Coral Gables | Mediterranean Revival, walkable Miracle Mile, UM-adjacent; the obvious premier choice |
| Newer amenity-rich suburb | Pinecrest | Master-planned feel, amenity-rich, secure |
| Value/entry-level | Aventura | The "most affordable retiree-target" by the profile's own framing; condos at $354K-$500K |
| City-specific: bohemian/character | Coconut Grove | Distinct enough from the suburb archetypes to warrant its own slot; tree canopy, marinas, mid-premium |
| City-specific: coastal/island | Key Biscayne | Causeway island; security profile and home values both genuinely distinctive |

Note: Miami uses both city-specific archetype slots (bohemian and coastal). The methodology caps city-specific archetypes at one per city as a general rule. Miami is the documented exception because both archetypes pass the five-test and the profile content already names them.

This is the kind of exception that must be documented (here, in the change log, and in the database) rather than tacit.

### Example C: Naples, FL (citywide)

Citywide median represents retiree experience accurately. The city is small enough and explicitly retiree-oriented enough that no archetype basket adds value. Median Home value = Zillow ZHVI citywide, current snapshot.

## 9. Cities where the basis may shift over time

For some cities, the basis can change as the market evolves. A city currently best served by Citywide may need to shift to Archetype basket if neighborhood-level price divergence grows. The annual rebuild (June, per SITE-OPERATIONS-LOG.md) is the natural moment to review.

Two cities to flag for review at the next rebuild:
- **Tampa.** Currently citywide-leaning, but Hyde Park, South Tampa, and Westchase may justify an archetype basket as the metro continues to bifurcate.
- **Charleston, SC.** Mount Pleasant, Daniel Island, and West Ashley may warrant archetype treatment if Charleston proper continues to outpace.

Adding these to the open items list in SITE-OPERATIONS-LOG.md.

## 10. The discipline that makes this work

Two habits are non-negotiable for this methodology to deliver:

1. **Run the five-question test on each candidate, not on the basket as a whole.** Editorial drift starts when you let a borderline candidate slide because the basket as a whole "feels right."
2. **Cap the basket at 5 picks.** When you find yourself wanting a sixth, it means you have an archetype overlap. Resolve it by collapsing two picks into one. The point of the framework is that it forces this discipline.

If you can do both, the methodology runs itself.

## 11. Refresh cadence

Median Home values refresh annually with the database rebuild (June). The basis (Citywide vs Archetype basket) is reviewed at the same time but rarely changes. The Zillow ZHVI snapshot date is recorded in the database header note.

Out-of-cycle refresh is triggered by any of the following:
- A Zillow methodology change affecting ZHVI computation
- A submarket's identity changing materially (gentrification flip, major disinvestment)
- A reader-credibility event where a published number is challenged and the audit reveals a basis problem

---

*Median Home Methodology v1.0 — June 17, 2026*
*Companion docs: BUDGET-METHODOLOGY.md (v1.0), SITE-OPERATIONS-LOG.md (v1.0)*
