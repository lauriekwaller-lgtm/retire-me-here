# RetireMeHere Median Home Methodology
**Established:** June 17, 2026 (v1.0)
**Current version:** v1.2, June 2026
**Applies to:** the Typical Home Value figure on every city profile, every comparison page, and every other surface on the site; the Median Home column in CityDatabase; and the derived Monthly Est via BUDGET-METHODOLOGY.md
**Companion docs:** BUDGET-METHODOLOGY.md, PROFILE-FORMATTING.md, SITE-OPERATIONS-LOG.md
**Note:** MEDIAN-HOME-LABEL-CONVENTIONS.md was deprecated in v1.2 and slated for deletion. Its content has been folded into this document and into PROFILE-FORMATTING.md.

---

## 1. The principle

Every city's Typical Home Value is derived from Zillow ZHVI data, refreshed annually, and displayed as a **single citywide figure** in the stat card. Where the citywide figure would benefit from context — most often because retiree-target neighborhoods run materially above the citywide median — the profile carries a **Neighborhood Reality Check note** beneath or beside the stat that names the relevant neighborhoods and their typical range.

This prioritizes transparency over editorial precision. A single, defensible source per city (Zillow ZHVI, refreshed annually) is more credible at scale than a per-city archetype basket whose composition is debatable. Where the citywide figure does not tell the full story, the gap is disclosed openly via the Neighborhood Reality Check note — not by computing a different number, and not by carving out special display formats for individual cities.

The label "Typical Home Value" matches what Zillow calls the ZHVI series and is methodologically more accurate than "Median Home" since ZHVI is a smoothed model estimate, not a true statistical median.

**Counts at a glance.** Database: 99 cities total (Henderson NV was collapsed into Las Vegas in June 2026, reducing the count from 100 to 99). All 99 cities use citywide ZHVI as a single figure in the stat card. Some carry a Neighborhood Reality Check note where retiree-target neighborhoods run materially above the citywide median; this is editorial judgment rather than a binary rule.

## 2. The rule

**One pattern, every city.** The Typical Home Value stat card on every profile displays the current citywide Zillow ZHVI as a single figure (for example, $235K for St. Louis, $195K for Memphis, $297K for St. Paul).

**Neighborhood Reality Check note (optional, editorial).** Any profile may carry a Neighborhood Reality Check note that contextualizes the citywide figure. The note names retiree-target neighborhoods and their typical price range, and explains how those neighborhoods relate to the citywide figure shown.

The note is warranted when the citywide figure alone would mislead a typical retiree-shopper — most often where retiree-target neighborhoods run substantially above the citywide median because the citywide figure is pulled down by neighborhoods retirees would not consider. The decision to add a note is editorial judgment, refreshed annually. There is no quantitative threshold; the principle is reader honesty, not categorization.

Cities currently carrying Neighborhood Reality Check notes (as of June 2026): Memphis, Philadelphia, Pittsburgh, St. Louis, New Orleans, Columbus, Kansas City, Tampa, St. Paul, Wilmington DE. This list may grow or shrink with annual review.

The canonical closing phrase for the note is: *"Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice."*

## 3. Why citywide

Three reasons.

**Defensibility.** Citywide Zillow ZHVI is a published number from a single, recognizable source. Anyone can verify it. An archetype-basket mean computed across editor-chosen neighborhoods is defensible only as far as the picks hold up under scrutiny, and small differences in picks can move the basket value by tens of thousands of dollars.

**Consistency.** One display pattern across all 99 cities is simpler to maintain, easier to explain, and more durable than a hybrid system with protected exceptions. Future operators do not need to learn which cities qualify for which format. Comparison pages compare like with like.

**Honesty.** Where the citywide figure misleads, the Neighborhood Reality Check note names the gap explicitly and points readers toward the realistic neighborhoods. This is more honest than burying the gap inside a basket calculation, or inside a range format that obscures the underlying citywide signal.

## 4. When to add a Neighborhood Reality Check note

Editorial judgment, not a binary test. Useful prompts:

1. Pull current citywide Zillow ZHVI for the city.
2. Identify 3 to 5 named retiree-target neighborhoods from the existing profile copy or local research.
3. Pull ZHVI for each neighborhood.
4. Compare the neighborhood values to the citywide figure.

A note is generally warranted when retiree-target neighborhoods sit materially above the citywide figure — enough that a retiree relying on the citywide number alone would significantly underestimate the realistic budget. Where retiree-target neighborhoods cluster near or below the citywide figure, a note adds noise rather than clarity and should be omitted.

The 10 cities currently carrying notes (Section 2) passed this judgment in June 2026. The list is reviewed at each annual rebuild. Cities approaching the editorial line are flagged for explicit review — as of June 2026, Charleston SC and Tampa are watch-list cities where the spread may grow or shrink with future market movement.

## 5. Documentation in the database

The CityDatabase carries one Typical Home Value column per city across all 99 rows, as the current citywide Zillow ZHVI in single-figure form (for example, `$235,000`). No city uses a range string. The Neighborhood Reality Check note is not flagged in the database itself — the note requirement lives in the profile HTML and in this document. The database remains a single source per city for clean downstream computation (Monthly Est, quiz tiers, comparison pages).

## 6. Refresh cadence

Typical Home Values refresh annually with the database rebuild in June. At each rebuild:

1. Pull current Zillow ZHVI for all 99 cities.
2. Spot-check neighborhood ZHVI for cities currently carrying a Neighborhood Reality Check note to confirm the note content is still accurate, refreshing the cited ranges as needed.
3. Review watch-list cities (Charleston SC, Tampa as of June 2026) and any new cities where the citywide-vs-target gap may have widened.
4. Update the database, then ripple downstream: profile stat cards, Monthly Est recompute via BUDGET-METHODOLOGY.md, quiz CITIES array in index.html, comparison pages.

Out-of-cycle refresh is triggered by:

- A Zillow methodology change affecting ZHVI computation.
- A single-city ZHVI movement of more than 15% in one quarter (data error versus real market shift; investigate before updating).
- A reader-credibility event where a published figure is challenged.

## 7. Comparison page treatment

Comparison pages quote the citywide figure for each city. When one or both cities carry a Neighborhood Reality Check note, mention the relevant neighborhood context in the prose under the cost section. When neither city carries a note, standard citywide framing applies.

Example for a both-with-note comparison (Kansas City vs St. Louis):

> "Both Kansas City ($250K) and St. Louis ($235K) carry citywide medians that significantly understate retiree-target neighborhoods. KC's Plaza, Brookside, Waldo, and Kansas-side suburbs (Mission Hills, Leawood, Overland Park) run $300K–$900K. STL's Tower Grove South, Central West End, Soulard, and Lafayette Square run $420K–$575K. The citywide numbers are a starting reference; budget by neighborhood choice."

## 8. Pinterest and off-site treatment

Off-site copy uses the citywide ZHVI directly ("Typical Home Value: $235K"). The Neighborhood Reality Check note is profile-page-only because the limited pin canvas cannot carry the context, and the destination profile page carries the full transparency.

## 9. Files this methodology touches

- All 99 city profile stat cards (Typical Home Value label and value): every city shows a single ZHVI figure
- Profiles carrying a Neighborhood Reality Check note (currently 10, list in Section 2)
- All comparison pages (citywide figures, with note context where applicable)
- /methodology.html (the public-facing explanation page)
- CityDatabase (one Typical Home Value column across all 99 rows, all single-figure)

## 10. Files this methodology does NOT touch

- Quiz logic (uses budgetRange tier, not raw dollars)
- Deep Dive guide HTML pages
- Pinterest assets
- Email content via MailerLite

---

## Appendix A: Migration from v1.1 to v1.2 (June 2026)

v1.1 of this document established a three-pattern framework: 97 cities used single-figure citywide ZHVI (standard pattern), 2 cities used a protected range format (Wilmington DE and St. Paul MN), and 8 cities required a Neighborhood Reality Check callout (Memphis, Philadelphia, Pittsburgh, St. Louis, New Orleans, Columbus, Kansas City, Tampa). The Median Honesty Rule was defined by a quantitative threshold (retiree-target neighborhoods running 50% or more above citywide ZHVI).

v1.2 consolidates these three patterns into one. Reasons:

1. **The three-pattern framework created a category-boundary problem.** Whether a city qualified for "range city" vs "NRC city" vs "standard" required a judgment call at each annual rebuild. The Median Honesty Rule's 50% threshold was a sharp line on a continuous variable; cities near the threshold (Tampa at 43% as of June 2026) sat in an ambiguous zone.

2. **The gap-magnitude rationale for the range cities did not hold up under inspection.** St. Louis's retiree-target neighborhoods run as high as $600K against a citywide $235K (155% above). St. Paul's run $415K–$550K against a citywide $297K (40–85% above). By gap magnitude alone, St. Louis would qualify for range treatment more than St. Paul. The actual distinguishing factor in v1.1 was editorial heritage (St. Paul's profile copy had already been written around a range framing; St. Louis's had not), which is not a principled methodological criterion.

3. **Comparison pages were carrying three display formats** (single value, range, single-value-with-callout), which complicated the comparison table structure and required per-pair handling.

4. **Exception-based methodologies do not scale.** As the site grows and the database expands, each carved-out category becomes a recurring decision point. Folding all cities into one pattern with editorial flexibility in the optional note eliminates the maintenance debt.

Under v1.2:

- The 8 former NRC cities continue to carry their existing notes, framed as the universal Neighborhood Reality Check note rather than a special-rule callout.
- St. Paul MN moves from range format to single-figure citywide ($297K) with a Neighborhood Reality Check note naming the retiree-target neighborhood range ($415K–$550K).
- Wilmington DE follows the same pattern when its profile is built.
- The 50% quantitative threshold is replaced by editorial judgment about when a note adds clarity for the reader.

The database is updated to use single-figure values for all 99 cities. Profile HTML is updated for St. Paul; Wilmington DE has no live profile to migrate.

## Appendix B: Superseded methodology (v1.0)

v1.0 of this document (June 17, 2026) established an archetype basket framework. Large-metro cities were each assigned a value computed as the simple arithmetic mean of one representative submarket per archetype (urban walkable, established premium suburb, newer amenity-rich suburb, value/entry-level, optionally active-adult). The framework included a five-question inclusion test and a tiebreaker hierarchy.

After the full audit (Batches 1 through 4, all 99 cities) and a deeper review during v15.1 generation, the archetype framework was retired in favor of the citywide-default approach, first documented in v1.1 and refined in v1.2. Three reasons:

1. **Basket composition was systematically over-premium-weighted.** The archetype-pick discipline kept favoring nicer submarkets, producing values that did not reflect the broader retiree-target range.
2. **Refinement #2 violations surfaced during audit.** The Tampa basket had included Brandon and Riverview as picks despite their being separate municipalities, which violated the no-double-counting rule. Similar errors were possible in other baskets.
3. **The Neighborhood Reality Check note achieves the same goal more honestly.** Naming the citywide-versus-neighborhood gap on the profile page is more transparent than burying the gap inside a basket calculation.

The audit data and the archetype basket values are preserved in `MedianHomeAuditMASTER.xlsx` for institutional memory but are not used in the live site or the current database.

---

*Median Home Methodology v1.2 — June 2026*
*Canonical methodology for the site. Supersedes v1.1 and v1.0.*
*Companion docs: BUDGET-METHODOLOGY.md (v1.0), PROFILE-FORMATTING.md (v1.0), SITE-OPERATIONS-LOG.md*
