# Median Home Audit Reference

Purpose: Give any future Claude session everything needed to continue the Median Home methodology audit without re-explanation from Laurie. Drop this into RetireMeHere project knowledge.

Last updated: June 2026 (after Batch 1 complete)

---

## Quick-start for a new session

If you're starting a fresh session to continue the audit:

1. Read this entire doc
2. Open `CityDatabase_Jun_9_v14.xlsx` from `/mnt/project/`
3. Identify which cities have NOT yet been audited (see "Audit status" section)
4. Apply the methodology + refinements below to the next batch
5. Deliver a single consolidated Excel workbook at session end
6. Update the "Audit status" section of this doc with what got done

Pace target per session: 25-30 cities (Path C cadence). Slow down for bimodal markets, cross-state metros, or any city with unusual archetype gaps.

---

## The methodology in one paragraph

Every city in the database gets a single Median Home value computed by one of two methods. Citywide basis uses the current Zillow ZHVI for the city as a whole, appropriate for small towns and homogeneous markets. Archetype basket basis identifies one representative submarket per archetype (urban walkable, established premium suburb, newer amenity-rich suburb, value/entry-level, optionally active-adult community, optionally one city-specific archetype), pulls current Zillow ZHVI for each pick, and computes the simple arithmetic mean. The basket caps at 5 picks. Picks must pass a five-question inclusion test and follow tiebreakers when multiple candidates fit one archetype.

---

## The five-question inclusion test

A submarket can be picked for an archetype only if it passes all five:

1. **Safety:** Is the area safe enough that a relocating retiree would seriously consider it?
2. **Quality:** Is the housing stock and infrastructure in good condition (not blighted or distressed)?
3. **Amenity access:** Reasonable access to healthcare, groceries, dining, transportation?
4. **Retiree-realistic:** Would a financially-secure relocating retiree (the target audience) actually consider living here? Not college-student-dominated, not exclusively young-family, not transient/nightlife-dominated.
5. **Editorial credibility:** Would including this submarket pass a sanity check from someone who knows the city?

---

## Tiebreaker hierarchy

When multiple submarkets pass the five tests for the same archetype, apply in order:

1. National recognition (broader name-awareness wins)
2. Centrality within the metro
3. Price representativeness (closer to the archetype's typical price band, not at the extreme)
4. Editorial judgment (your call, document the reasoning)

---

## The 8 methodology refinements (will batch into MEDIAN-HOME-METHODOLOGY.md v1.1)

These emerged from Batch 1. Apply them consistently in future batches.

**1. Archetype price-band discipline.** Each pick must represent that archetype's price band, not just sit in the geographic area where that archetype typically lives. Example: Sunset Hills, MO is geographically in South County (a value-leaning area) but at $540K is mid-tier, not value-tier. Mehlville at $233K or Sappington at $303K are the honest value picks.

**2. Suburb double-counting rule.** Submarkets that are standalone database entries CANNOT be included in a parent metro's archetype basket. Scottsdale is its own DB entry, so it cannot appear in a Phoenix basket. Carmel, Bexley, Coral Gables, Overland Park, Leawood, Germantown, Brentwood, Wayne, Mt. Lebanon are NOT standalone DB entries and CAN be included in their parent metro's basket.

**3. Bimodal market content treatment.** Some markets are bimodal: one cluster of value-tier picks plus one cluster of premium picks with little in between. Miami is the clearest example (Aventura at $505K vs everything else at $1.2M+). For these cities, the database Median Home value is unchanged (single mean), but profile page content MUST lead with the price spectrum ("From $X to $Y") before introducing the median. Flag bimodal cities in the audit workbook with an asterisk.

**4. Cross-state-line metros.** Some metros span state lines. Kansas City spans MO/KS, Cincinnati spans OH/KY. Archetype basket may include submarkets from either side of the line if they pass the inclusion test and are not standalone DB entries. Document the cross-state nature in audit notes.

**5. Value-tier retiree-realistic floor.** Value/entry-level pick is the lowest-tier submarket that squarely passes the "retiree-realistic" test (mature housing, older demographic, manageable upkeep). NOT the absolute floor of the metro's price spectrum. A neighborhood at the absolute bottom of the metro's pricing often fails the retiree-realistic test even if it's safe and decent.

**6. Premium suburb retiree-realistic ceiling.** Established premium suburb pick is the highest tier that's still retiree-realistic for the typical $500K-$1M relocator. NOT the absolute peak of the metro. Belle Meade at $2.7M is too extreme to represent Nashville's retiree-target premium tier; Brentwood at $1.2M is more honest. Belle Meade is implicitly represented as luxury extension.

**7. Archetype skips allowed when no clean pick exists.** Some cities have natural gaps in the standard archetype menu. Memphis lacks a clean urban walkable retiree-target; Las Vegas lacks one too; Nashville lacks a mid-price urban walkable. Skip an archetype with documentation rather than forcing a weak pick. Produces 3-pick basket instead of 4-pick.

**8. Lower-confidence picks flagged for re-verification.** When Zillow neighborhood boundary definitions are ambiguous, or you're working from estimates rather than verified Zillow ZHVI, flag confidence as Medium and list specific picks needing re-verification. New Orleans Batch 1 picks (Garden District, Uptown, Algiers Point) and Las Vegas Sun City Summerlin are current examples.

---

## Process per city

For each city in the audit batch:

1. **Read current DB value.** Pull from `CityDatabase_Jun_9_v14.xlsx`, 'City Database' sheet, header row 2. Note current Median Home (may be single value or range).

2. **Decide basis.** Citywide if the city is small/homogeneous and the citywide median represents the retiree experience. Archetype basket if internal price variation is significant and citywide median misleads (typically large metros with distressed areas dragging the median down).

3. **If Citywide:** Pull current Zillow ZHVI for the city. That's the new value. Done.

4. **If Archetype basket:**
   - Identify candidate submarkets for each archetype (3-5 picks total)
   - Verify candidate submarkets are NOT standalone DB entries (rule #2)
   - Apply the five-question test to each candidate
   - Use tiebreakers to select one pick per archetype
   - Pull current Zillow ZHVI for each pick
   - Compute the simple arithmetic mean
   - Round to nearest $1,000

5. **Document:**
   - The basis decision (Citywide or Archetype basket; note if basis CHANGED from current DB)
   - Each pick with archetype label and Zillow ZHVI value
   - Implicit submarkets (named submarkets that are represented by the basket pick as their archetype peer)
   - Notes (any judgment calls, basis change rationale, bimodal flag, confidence level)

6. **Compare to current DB value.** Note the delta (positive or negative dollar amount and percentage).

---

## Data access pattern

```python
import pandas as pd
df = pd.read_excel('/mnt/project/CityDatabase_Jun_9_v14.xlsx', 
                   sheet_name='City Database', header=1)
df.columns = [c.replace('\n', ' ').strip() for c in df.columns]
df = df[df['City'].notna()].copy()
# City lookup: (str(r.City).strip(), str(r.ST).strip())
```

For Zillow ZHVI lookups, use web_search with queries like:
- "Zillow [city/neighborhood name] home value 2026"
- "Zillow ZHVI [neighborhood] [city] [state]"

Zillow neighborhood pages typically list 15-30 adjacent submarkets with their ZHVI values, so one well-targeted search per city often returns all the data needed for the basket.

---

## Deliverable format per session

Single Excel workbook saved to `/mnt/user-data/outputs/Median-Home-Audit-Batch-N.xlsx` with these sheets:

1. **Summary:** One row per city with City, Current DB, New Value, Delta, Delta %, Basis, Confidence. Highlight basis changes in yellow. Bold red on city names for bimodal markets.

2. **City Details:** For each city, show the basis decision, every pick with archetype + Zillow ZHVI + submarket name, the computed mean, implicitly represented submarkets, and notes.

3. **Refinements Queue:** Carry forward the 8 existing refinements; add any new ones that emerge from this batch.

4. **Remaining for Next Batch (or "Audit Complete"):** List cities still pending.

---

## Audit status

### Batch 1 COMPLETE (18 cities, June 2026)

Cities audited:
- Asheville NC (Citywide, $462K)
- Charlottesville VA (Citywide, $465K)
- Columbus OH (Archetype, $493K, BASIS CHANGE)
- Indianapolis IN (Archetype, $432K)
- Kansas City MO (Archetype, $466K, BASIS CHANGE)
- Las Vegas NV (Archetype, $478K)
- Memphis TN (Archetype, $408K)
- Miami FL (Archetype, $1,128K, BIMODAL)
- Nashville TN (Archetype, $664K, BASIS CHANGE)
- New Orleans LA (Archetype, $532K, BASIS CHANGE, MEDIUM CONFIDENCE)
- Philadelphia PA (Archetype, $684K)
- Pittsburgh PA (Archetype, $526K)
- Portland ME (Citywide, $576K)
- Raleigh NC (Citywide, $436K)
- Salt Lake City UT (Archetype, $714K, BASIS CHANGE)
- San Antonio TX (Archetype, $534K)
- St. Louis MO (Archetype, $494K)
- Tampa FL (Archetype, $732K, BASIS CHANGE)
- Tucson AZ (Archetype, $491K, BASIS CHANGE)

Wait, that's 19 cities listed. Counting carefully: yes, Asheville was added from the earlier 5-city methodology test, then 18 more during the formal Batch 1. Total audited: 19. Remaining: 81 (not 82).

Final canonical workbook for Batch 1: `Median-Home-Audit-Batch-1-FINAL.xlsx`

Cities flagged for re-verification before v15 ships:
- New Orleans: Garden District, Uptown, Algiers Point picks are estimates
- Las Vegas: Sun City Summerlin estimate
- Pittsburgh: Fox Chapel value omitted from basket (pending verification)

### Pending (81 cities)

Use the database to identify which 81 cities are NOT in the Batch 1 list above. They span all the smaller and mid-sized cities, beach towns, mountain towns, mid-sized metros, and additional planned communities in the database.

Logical batch groupings for future sessions:
- Batch 2: Mountain west and Pacific (Bend, Boise, Coeur d'Alene, Sedona, Prescott, Flagstaff, Park City, Boulder, Fort Collins, Eugene, Bellingham, etc.)
- Batch 3: Southeast and beach towns (most of FL beyond Miami/Tampa, coastal Carolinas, Georgia, Alabama coast)
- Batch 4: Northeast and remaining (smaller New England, mid-Atlantic, anything left)

Or batch by state region. The grouping doesn't matter methodologically. What matters is finishing rigorously.

---

## Workflow expectations

After each batch:
1. Deliver the workbook with all sheets populated
2. Update this doc's "Audit status" section
3. Confirm any new refinements added to queue
4. Flag any cities needing re-verification

When all 100 cities are done:
1. Update MEDIAN-HOME-METHODOLOGY.md to v1.1 with the batched refinements
2. Confirm New Orleans, Las Vegas Sun City Summerlin, Pittsburgh Fox Chapel are verified
3. Move to v15 database generation phase

---

## Things that are NOT in scope for this audit

These are separate workstreams handled elsewhere:

- Budget formula recompute (already done in BUDGET-METHODOLOGY.md v1.0, will use new Median Home values when v15 generates)
- D2 Budget tier reassignments (downstream of Monthly Est, downstream of Median Home)
- Quiz BUDGET_OPTIONS update in index.html (post-audit deploy phase)
- Profile page copy updates (post-audit deploy phase; bimodal cities need spectrum framing)
- Pinterest pin updates (separate workstream)
- New city profiles (separate workstream)

The audit produces NEW MEDIAN HOME VALUES. Everything downstream of that flows from the audit but is not part of it.

---

## Final note for future Claude sessions

Laurie's working style: rigorous, careful, values credibility over speed but also values efficient delivery. She reviews per-city judgment calls and pushes back when something feels off (the St. Louis Sappington-over-Mehlville exchange is the model). She approves the framework first, then trusts execution within it. She prefers single-file deliverables over multi-file fragmentation. She works on iPad/iPhone primarily, so deliverables should be readable on a phone screen and Excel workbooks should not require horizontal scrolling for the Summary sheet.

No em dashes in any deliverable (her style preference).

When in doubt on a judgment call, flag it in the workbook and let her decide rather than committing to a pick.
