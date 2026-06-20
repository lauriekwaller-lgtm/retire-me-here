# RetireMeHere Site Operations Log
**Purpose:** Single source of truth for what gets reviewed, updated, and refreshed across the site. Forward-looking calendar plus backward-looking change log. Written to be handover-ready, not personal shorthand.
**Owner:** Laurie Waller (solo founder/operator)
**Created:** June 17, 2026
**Last full review:** June 19, 2026

---

## 1. How to use this document

This doc has three jobs.

First, the **recurring maintenance calendar** (Section 2) lists every task that has to happen on a schedule for the site to stay credible. Anything you do regularly should be here. If you find yourself doing something every few months that isn't listed, add it.

Second, the **event-driven triggers** (Section 3) cover things that don't run on a calendar but require action when the world changes. Mortgage rate shocks, insurance market changes in Florida, a Zillow methodology shift.

Third, the **change log** (Section 7) is the running record of what's actually been done. Every methodology change, every database version bump, every major content refresh. This is the part that matters most for handover: a new operator needs to be able to read backward and understand why things are the way they are.

Update this doc at the same time you do the work. If you defer the documentation, it doesn't get done.

## 2. Recurring maintenance calendar

| Frequency | Task | Trigger / Window | What it involves | Owner |
|---|---|---|---|---|
| Monthly | Analytics review | First Monday | GA4 traffic, Search Console queries, Microsoft Clarity heatmaps, MailerLite signups. Note anomalies. | Operator |
| Monthly | Zillow ZHVI spot-check | Mid-month | Pull 10 random cities, compare to Median Home in current DB. Flag any with >10% move for the next quarterly review. | Operator |
| Monthly | Pinterest performance | End of month | Top-performing pins, board engagement, click-throughs to site. Adjust pin cadence accordingly. | Operator |
| Quarterly | Mortgage rate check | Mar / Jun / Sep / Dec, first week | Open Freddie Mac PMMS (https://www.freddiemac.com/pmms). Compare to rate documented in BUDGET-METHODOLOGY.md. If gap >50 basis points, trigger budget recompute (see SOP-2). | Operator |
| Quarterly | Watch-list review | Same week as rate check | Open most recent Budget-Audit-*.xlsx, review Watch List sheet. Decide whether any flagged cities need a Median Home or framing update. | Operator |
| Quarterly | Profile audit (1/4 of cities) | Rotating | Pick ~25 profiles, spot-check airport routes, hospital rankings, and any external links. Refresh photos where dated. | Operator |
| Annually | Medicare premium refresh | Mid-November | CMS announces next year's Part B premium ~Nov 14. Update BUDGET-METHODOLOGY.md and trigger annual recompute (see SOP-3). | Operator |
| Annually | Full database rebuild | June | Roll mortgage rate, Medicare numbers, USDA food plan, BLS utilities, Zillow ZHVI snapshot. Increment DB filename (vN → vN+1). | Operator |
| Annually | Tier boundary review | June (with rebuild) | Confirm current boundaries still produce sensible distribution. Adjust if any tier has <5 or >50 cities. | Operator |
| Annually | Methodology doc audit | June | Review BUDGET-METHODOLOGY.md, GUIDE-METHODOLOGY-DECISIONS.md, scoring-analysis docs. Update for any drift. | Operator |
| Annually | Sitemap & indexing health | June | Resubmit sitemap.xml to Search Console. Spot-check for orphaned profile pages. | Operator |

## 3. Event-driven triggers

These bypass the calendar. If any of these happen, act in the window indicated.

| Trigger | Action | Window |
|---|---|---|
| Mortgage rate moves ≥75 bp from BUDGET-METHODOLOGY.md snapshot | Recompute budget (SOP-2). Bump methodology doc snapshot. | 2 weeks |
| Major Florida or California insurance market event (state-mandated rate change, insurer pullout) | Re-source HO Insur Est $/yr column for affected states. Recompute affected cities. | 4 weeks |
| Zillow changes ZHVI methodology | Audit how the change affects Median Home values. Document in change log. | 4 weeks |
| First affiliate contract signed | Trigger trademark filing and LLC formation. Flip display ad switches. Activate affiliate placeholders. | Same week as contract |
| Google Search Console flags a structural indexing problem | Investigate within 1 week, fix within 2 weeks. | 2 weeks |
| Major new retiree-relevant CMS rule (Medicare, Medicare Advantage) | Assess impact on healthcare line in budget formula. | 4 weeks |
| A city's Median Home value moves >15% in a single Zillow refresh | Investigate (data error vs real market shift). Update if real. | 4 weeks |

## 4. Key files and where they live

| File | Purpose | Location | Notes |
|---|---|---|---|
| CityDatabase_*_vN.xlsx | Authoritative scoring database | Project knowledge / synced to working session each session | Current: CityDatabase_Jun_9_v14.xlsx. Filename increments with version. |
| Budget-Audit-*.xlsx | Per-rebuild audit trail | Project knowledge | Current: Budget-Audit-Jun-16-2026.xlsx |
| BUDGET-METHODOLOGY.md | Budget formula and sources | Project knowledge + repo | Current: v1.0 (June 16 2026) |
| MEDIAN-HOME-METHODOLOGY.md | Archetype framework, five-question inclusion test, basis documentation | Project knowledge + repo | Current: v1.0 (June 17 2026). Upstream of budget; Median Home values feed BUDGET-METHODOLOGY.md. |
| GUIDE-METHODOLOGY-DECISIONS.md | Scoring decisions across guides | Project knowledge + repo | |
| HUM-HEAT-Scoring-Guide.md | Humidity and heat scoring rubric | Project knowledge + repo | |
| *-cities-scoring-analysis.md (7 files) | Per-guide scoring analysis | Project knowledge + repo | Active, Arts, Foodie, Healthcare, Hikers, LGBTQ, Sports Fans |
| index.html | Quiz engine, landing structure, PUBLISHED_PROFILES map | GitHub repo (lauriekwaller-lgtm/retire-me-here) | Source of truth for what profiles are live |
| sitemap.xml | Search engine discovery | GitHub repo | Edit the live repo version, not the project copy (which goes stale) |
| cities/*/  | Profile pages | GitHub repo | One folder per city slug |
| pick-and-compare.html | Interactive city compare | GitHub repo | Embeds full city dataset as inline JSON |
| pin-studio.html | Pinterest pin generator | GitHub repo | Uses localStorage to persist field inputs |
| This document (SITE-OPERATIONS-LOG.md) | Operations and handover | Project knowledge + repo | Update at the time of the work, not later |

## 5. Version conventions

**Database files** follow the pattern `CityDatabase_<Month>_<Day>_v<N>.xlsx`. The version number is canonical; the date is informational. Each rebuild bumps v.

**Audit files** are dated, not versioned: `Budget-Audit-<Month>-<Day>-<Year>.xlsx`. One audit file per rebuild.

**Methodology docs** carry a version number in the footer (e.g., "v1.0 — June 16, 2026"). Bump the major version for any formula change, minor version for source refreshes.

**Profile HTML files** are not versioned; the GitHub commit history serves that role.

## 6. Standard operating procedures (SOPs)

These are the short playbooks for the most common operations. Detailed walkthroughs and prompts live in the project knowledge or can be reconstructed from the change log.

### SOP-1: Add a new city profile

1. Confirm the city is in the current DB and has all 10 dimension scores plus budget data.
2. Source three photos: hero 1600×899, detail 1600×2133 (portrait), lifestyle 1280×1280 (square). Vet for licensing and editorial fit.
3. Build the profile HTML matching the established template (use a recent profile as the reference).
4. Update PUBLISHED_PROFILES in index.html (key = `cityName_state`).
5. Update sitemap.xml with the new URL.
6. Fix reciprocal landing-page links if the city's card isn't already on relevant landing pages.
7. Submit URL to Search Console for indexing.
8. Log in Section 7 below.

### SOP-2: Budget recompute (quarterly trigger)

1. Pull current Freddie Mac PMMS rate.
2. Open the current Budget-Audit file's Formula Inputs sheet, update the mortgage rate constant.
3. Run the formula across all 100 cities (Python notebook, see `budget-recompute.ipynb` in project knowledge once created).
4. Spot-check 5 cities (one per tier) for sanity. If reasonable, proceed.
5. Generate new Budget-Audit-<date>.xlsx.
6. Update BUDGET-METHODOLOGY.md snapshot date and rate value.
7. Generate new CityDatabase_*_vN+1.xlsx with updated Monthly Est and Budget Range columns.
8. Deploy: replace database, deploy code if quiz boundaries change, refresh any pages with hardcoded budget numbers.
9. Log in Section 7.

### SOP-3: Annual full rebuild (June)

1. Run SOP-2 first to refresh the mortgage rate.
2. Pull November Medicare Part B/D announcement values, update healthcare constants.
3. Pull current USDA Cost of Food at Home (Moderate Plan, age 51–70 couple).
4. Pull current BLS Consumer Expenditure Survey 65+ data for utilities and discretionary baselines.
5. Pull fresh Zillow ZHVI snapshot for Median Home values. Re-source archetype basket submarkets at the same time (per MEDIAN-HOME-METHODOLOGY.md).
6. Review Median Home Basis assignments. Flag any city where the basis should shift (Citywide → Archetype basket or vice versa). Tampa and Charleston are pre-flagged for this review.
7. Update KFF Medigap state-level data.
8. Generate new audit file and database version.
9. Update BUDGET-METHODOLOGY.md to v(N+1). Update MEDIAN-HOME-METHODOLOGY.md if any methodology refinement occurred.
10. Deploy.
11. Log in Section 7.

### SOP-4: Deploy a database update

1. Drag-drop the new DB file into the GitHub repo, replacing the prior version (rename if filename changed).
2. If quiz logic depends on Budget Range tier boundaries, edit BUDGET_OPTIONS array in index.html.
3. Commit. Netlify auto-deploys.
4. Verify on production: load index.html, run the quiz, confirm budget tier matches.
5. Submit Search Console indexing request for any page with materially changed copy.

## 7. Change log

Reverse chronological. Add to the top of this list as work happens.

### 2026-06-19 — Median Home methodology v1.1 + v15.1 database transition
**What:** Replaced multi-basis Median Home methodology (Citywide / Archetype / Neighborhood) with citywide-default + Median Honesty Rule. Generated CityDatabase_Jun_19_v15_1.xlsx with citywide medians for 97 cities and 2 range exceptions (Wilmington DE, St. Paul MN). Recomputed Monthly Est for all 99 cities. Updated index.html with new BUDGET_OPTIONS boundaries and refreshed all 99 city card data fields.
**Why:** The v1.0 multi-basis methodology proved harder to defend than the problem it solved. Archetype basket composition was prone to over-premium-weighting (Tampa basket included Brandon/Riverview, which are separate municipalities) and inadvertent skew. Single-MEAN output for cities with genuine geographic income polarization (Memphis, Philadelphia, Pittsburgh, St. Louis) compressed real ranges into single points that misled in the opposite direction. Citywide + visible callouts is the simpler, defensible answer.
**Files updated:**
- MEDIAN-HOME-METHODOLOGY.md → v1.1 (citywide-default, Median Honesty Rule, 8 callout cities listed)
- CityDatabase_Jun_19_v15_1.xlsx (replaces v14; 99 cities, Henderson NV collapsed into Las Vegas)
- index.html (BUDGET_OPTIONS, BUDGET_LABELS, budgetLabels, quiz subtitle PITI framing, console.log, 99 city data fields, 7 Range-number prose fixes)
**Files added:**
- v14-to-v15_1-audit-log.xlsx (per-city delta log + tier distribution + callout cities reference)
- V15_1-TRANSITION-CHECKLIST.xlsx (tracking artifact for outstanding work; delete when all rows ✅)
**Files retired:**
- MEDIAN-HOME-METHODOLOGY.md v1.0 (replaced)
- MEDIAN-HOME-AUDIT-REFERENCE.md (12 refinements specific to v1.0 multi-basis approach; obsolete)
- MEDIAN-HOME-LABEL-CONVENTIONS.md (basis labeling no longer applicable under v1.1)
**Tier boundaries (v15.1 final, applied to index.html quiz):** R1 Under $5,500/mo | R2 $5,500–$6,499 | R3 $6,500–$7,499 | R4 $7,500–$8,999 | R5 $9,000+. Distribution: 30 / 31 / 20 / 10 / 8 = 99.
**Median Honesty Rule (new):** 8 cities (Memphis, Philadelphia, Pittsburgh, St. Louis, New Orleans, Columbus, Kansas City, Tampa) require above-fold Neighborhood Reality Check callout because retiree-target neighborhoods run >50% above citywide median. These cities must not be described as "affordable" in any site copy without the callout context attached.
**Quiz subtitle reframed:** "Total monthly cost for a couple — housing (mortgage, property taxes, homeowners insurance), healthcare, utilities, food, transportation, and lifestyle." Replaces incomplete 4-category framing.
**Henderson NV collapsed into Las Vegas:** Henderson row removed from database; Las Vegas profile narrative absorbs the Henderson context. Database sits at 99 cities.
**Outstanding work:** Profile copy pass (35 live profiles), Neighborhood Reality Check callouts (8 cities), index.html prose review (60 tier-shift cities), thematic landing page copy review, value-navigator.html review, comparison pages, Pinterest pin review. Tracked in V15_1-TRANSITION-CHECKLIST.xlsx.
**Future methodology items deferred:** HOA fees in budget formula, home maintenance line, range-city midpoint documentation. Tracked in checklist sheet 6.

### 2026-06-17 — Median Home methodology v1.0 established
**What:** Established the canonical methodology for Median Home values across all 100 cities. Introduced the archetype framework, five-question inclusion test, and per-city basis documentation requirement.
**Why:** The June 16 budget methodology audit surfaced a deeper inconsistency. Eight cities used a retiree-target neighborhood basis (per Scoring Rubric v3.2) while the other 92 used citywide medians, even where the citywide figure misrepresents the retiree experience (Miami being the obvious example). The methodology was inconsistent and editorially debatable on a city-by-city basis, which is unsustainable for a credibility-first brand. Standardizing the framework now, before traffic scales, was the right window.
**Files added:** MEDIAN-HOME-METHODOLOGY.md (v1.0).
**Core principle:** Median Home represents what a financially-secure relocating retiree would pay across the realistic spectrum of submarkets they would consider. Two valid bases: Citywide (small towns and explicit retiree destinations) or Archetype basket (metros with significant internal price variation).
**Archetype framework:** Five standard archetypes (urban walkable, established premium suburb, newer amenity-rich suburb, value/entry-level, active-adult community), plus up to one city-specific archetype where genuinely distinct. One representative submarket per archetype; basket capped at 5 picks. Simple arithmetic mean across the basket.
**New database columns required (in v15):** Median Home Basis ("Citywide" or "Archetype basket") and Median Home Source (citywide source + date, or comma-separated submarket list).
**Key distinction:** The methodology governs back-office computation only. Editorial content on profile pages remains unconstrained by archetype caps; profile pages can name as many neighborhoods as local credibility warrants.
**Pre-flagged for next-rebuild review:** Tampa and Charleston as candidates for basis shift from Citywide to Archetype basket as their metros continue to bifurcate.
**Audit pass status:** Pending. Order of operations confirmed: Median Home audit → corrected values → v15 budget recompute → database generation → quiz boundary update → page copy diff → one coherent deploy.

### 2026-06-16 — Budget methodology v1.0 established
**What:** Replaced legacy Monthly Est numbers (no documented source) with a transparent mortgaged-buyer formula. All 100 cities recomputed.
**Why:** Original numbers had no audit trail and produced inconsistent results at the low end (Johnson City's $2,500–$3,200 didn't cover Medicare + housing for a couple with a mortgage). Path 2 chosen: full recompute with documented sources.
**Files added:** BUDGET-METHODOLOGY.md (v1.0), Budget-Audit-Jun-16-2026.xlsx.
**Files pending update:** CityDatabase_*_v15.xlsx (replace v14), index.html (quiz BUDGET_OPTIONS), several published pages (value-navigator.html, Johnson City and Casper profiles, affordability-themed star tags).
**Key inputs:** Freddie Mac PMMS 6.52% (06/11/2026), CMS Medicare Part B $202.90 (2026 standard), CMS Part D $38.99 (2026 national avg), KFF Medigap state variance, BLS Consumer Expenditure Survey 65+ baselines.
**Tier boundaries changed:** Old (Under $3,500 / $3,500-4,500 / $4,500-6,000 / $6,000-8,000 / $8,000+) → new (Under $5,500 / $5,500-6,500 / $6,500-7,500 / $7,500-9,000 / $9,000+).
**Watch list:** 12 cities flagged for editorial review, especially Miami (Median Home blend question), Portland ME and New Orleans (2-tier moves).
**Decided:** Cash-buyer toggle as future enhancement, not built now.
**Follow-up:** Audit revealed a deeper Median Home methodology inconsistency. Addressed June 17 in MEDIAN-HOME-METHODOLOGY.md. v15 database generation now waits on the Median Home audit pass to avoid shipping the budget recompute twice.

### Pre-2026-06-16 — Database evolution (incomplete record)
The database progressed through versions ending at CityDatabase_Jun_9_v14.xlsx. The full history was not logged; this is the institutional reset point. Future versions will be tracked from v15 forward.

## 8. Open items and future enhancements

Not commitments. Things worth doing when time and traffic justify.

| Item | Priority | Trigger to start | Notes |
|---|---|---|---|
| Median Home audit pass (all 100 cities) | ~~High~~ ✅ | ~~Now (gates v15)~~ Done 2026-06-19 | Completed and superseded. Methodology shifted to citywide-default (v1.1). v15.1 database deployed. |
| Publish Pensacola profile | High | Now | Built but not yet live. Add to sitemap and PUBLISHED_PROFILES. Do not pin until published. |
| Quiz BUDGET_OPTIONS update | ~~High~~ ✅ | ~~With v15 deploy~~ Done 2026-06-19 | Updated in v15.1 transition. Quiz boundaries now $5,500 / $6,500 / $7,500 / $9,000. |
| Page copy diff (value-navigator, affected profiles) | High | In progress | Tracked in V15_1-TRANSITION-CHECKLIST.xlsx. Profile copy pass + thematic landing pages outstanding. |
| Tampa Median Home basis review | ~~Medium~~ ✅ | ~~Next annual rebuild~~ Done 2026-06-19 | Reviewed during v15 audit. Archetype basket considered then rejected; Tampa stays Citywide with Neighborhood Reality Check callout (43% gap, borderline). |
| Charleston SC Median Home basis review | Medium | Next annual rebuild (June) | Candidate to shift Citywide → Archetype basket. Mount Pleasant, Daniel Island, West Ashley diverging from Charleston proper. |
| Florida hub cluster | Medium | After v15 deploys cleanly | Previously identified as high-traffic opportunity |
| Cash-buyer toggle / page | Low | Traffic signal or affiliate ask | Adds reach to readers funding moves from prior home sale |
| Independent-living scoring dimension | Low | After current methodology stabilizes | Differentiation moat |
| HOA-inclusive variant for Sun City / Villages / Naples | Low | If reader feedback warrants | Could be a per-city note rather than a database column |
| State-by-state Medigap precision | Low | Annual rebuild cycle | Replace coarse 5-bucket modifier with KFF state-level data |
| Reconcile index.html CITIES array against database | Medium | Next major code touch | Manual sync risk |
| Frisco TX placement audit | Low | When refreshing landing pages | Was previously flagged for evaluation |
| Display ad activation | Triggered | First affiliate contract | Containers deployed, switches off |
| Affiliate placeholders activation | Triggered | First contract signed | In place, ready |
| Trademark filing + LLC formation | Triggered | First affiliate contract | USPTO search confirmed zero conflicting marks |

## 9. Handover essentials (for a future operator)

If you are reading this because Laurie has handed you the site, start here.

**What this site is.** A retirement-city discovery platform that scores 100 U.S. cities across 10 dimensions, helps readers match via a quiz, and monetizes through SEO-driven affiliate revenue. Credibility and accuracy come first; promotional polish never overrides honesty.

**What you should not do until you understand the system.** Do not change the database without reading BUDGET-METHODOLOGY.md and GUIDE-METHODOLOGY-DECISIONS.md. Do not add cities to landing pages without verifying they have full DB scores. Do not change tier boundaries or scoring rubrics without documenting in Section 7 above. Do not pin cities to Pinterest before their profile page is live and in the sitemap.

**The single most important habit.** When you do work, log it in Section 7 the same session. The reason this doc exists is that institutional memory disappears when one person carries it all.

**Tools you'll need access to.** GitHub repo `lauriekwaller-lgtm/retire-me-here` (deploy), Netlify (auto-deploys from GitHub), Google Analytics 4 (property G-BTL743DSJQ), Google Search Console, Microsoft Clarity, MailerLite (email capture, form IDs in project knowledge), Pinterest business account, Zillow Research portal (for Median Home refresh), Freddie Mac PMMS (for mortgage rate), CMS.gov (for Medicare premiums).

**Where the work happens.** Editing is primarily through GitHub's web interface. For repo-wide operations that github.dev cannot handle (large refactors, bulk file moves), use GitHub Codespaces. Laurie works heavily on iPad and iPhone, so the patterns here favor lightweight web tooling over a local dev environment.

**Decisions a new operator can make autonomously.** Routine refreshes following the SOPs above. Photo refreshes. Copy edits that don't change scoring. Pinterest content. Small UI polish.

**Decisions that need a conversation.** Adding or removing cities from the database. Changing scoring methodology. Adding new scoring dimensions. Changing tier boundaries. Activating affiliate/ad revenue mechanics. Anything that touches monetization or the trademark.

---

*Site Operations Log v1.1 — June 17, 2026 (revised same-day to incorporate Median Home methodology)*
*Companion docs: BUDGET-METHODOLOGY.md (v1.0), MEDIAN-HOME-METHODOLOGY.md (v1.0), GUIDE-METHODOLOGY-DECISIONS.md*
*Next review: September 2026 (quarterly cycle)*
