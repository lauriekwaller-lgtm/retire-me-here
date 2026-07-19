# RetireMeHere Site Operations Log
**Purpose:** Single source of truth for what gets reviewed, updated, and refreshed across the site. Forward-looking calendar plus backward-looking change log. Written to be handover-ready, not personal shorthand.
**Owner:** Laurie Waller (solo founder/operator)
**Created:** June 17, 2026
**Last full review:** July 19, 2026

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
| Monthly | Zillow ZHVI spot-check | Mid-month | Pull 10 random cities, compare to Typical Home Value in current DB. Flag any with >10% move for the next quarterly review. | Operator |
| Monthly | Pinterest performance | End of month | Top-performing pins, board engagement, click-throughs to site. Adjust pin cadence accordingly. | Operator |
| Quarterly | Mortgage rate check | Mar / Jun / Sep / Dec, first week | Open Freddie Mac PMMS (https://www.freddiemac.com/pmms). Compare to rate documented in BUDGET-METHODOLOGY.md. If gap >50 basis points, trigger budget recompute (see SOP-2). | Operator |
| Quarterly | Watch-list review | Same week as rate check | Open most recent Budget-Audit-*.xlsx, review Watch List sheet. Decide whether any flagged cities need a Typical Home Value or framing update. | Operator |
| Quarterly | Profile audit (1/4 of cities) | Rotating | Pick ~25 profiles, spot-check airport routes, hospital rankings, and any external links. Refresh photos where dated. | Operator |
| Annually | Medicare premium refresh | Mid-November | CMS announces next year's Part B premium ~Nov 14. Update BUDGET-METHODOLOGY.md and trigger annual recompute (see SOP-3). | Operator |
| Annually | Full database rebuild | June | Roll mortgage rate, Medicare numbers, USDA food plan, BLS utilities, Zillow ZHVI snapshot. Increment DB filename (vN → vN+1). | Operator |
| Annually | Tier boundary review | June (with rebuild) | Confirm current boundaries still produce sensible distribution. Adjust if any tier has <5 or >50 cities. | Operator |
| Annually | Methodology doc audit | June | Review BUDGET-METHODOLOGY.md, MEDIAN-HOME-METHODOLOGY.md, PROFILE-FORMATTING.md, GUIDE-METHODOLOGY-DECISIONS.md, scoring-analysis docs. Update for any drift. | Operator |
| Annually | Sitemap & indexing health | June | Resubmit sitemap.xml to Search Console. Spot-check for orphaned profile pages. | Operator |

## 3. Event-driven triggers

These bypass the calendar. If any of these happen, act in the window indicated.

| Trigger | Action | Window |
|---|---|---|
| Mortgage rate moves ≥75 bp from BUDGET-METHODOLOGY.md snapshot | Recompute budget (SOP-2). Bump methodology doc snapshot. | 2 weeks |
| Major Florida or California insurance market event (state-mandated rate change, insurer pullout) | Re-source HO Insur Est $/yr column for affected states. Recompute affected cities. | 4 weeks |
| Zillow changes ZHVI methodology | Audit how the change affects Typical Home Values. Document in change log. | 4 weeks |
| First affiliate contract signed | Trigger trademark filing and LLC formation. Flip display ad switches. Activate affiliate placeholders. | Same week as contract |
| Google Search Console flags a structural indexing problem | Investigate within 1 week, fix within 2 weeks. | 2 weeks |
| Major new retiree-relevant CMS rule (Medicare, Medicare Advantage) | Assess impact on healthcare line in budget formula. | 4 weeks |
| A city's citywide Zillow ZHVI moves >15% in a single refresh | Investigate (data error vs real market shift). Update if real. | 4 weeks |
| A non-NRC city's retiree-target neighborhood premium becomes editorially significant | Review whether the city should be added to the NRC list. If yes, add a Neighborhood Reality Check callout per PROFILE-FORMATTING.md v1.2. | Next refresh |

## 4. Key files and where they live

| File | Purpose | Location | Notes |
|---|---|---|---|
| CityDatabase_*_vN.xlsx | Authoritative scoring database | `docs/` in the repo | Current: CityDatabase_Jul_13_v16_4_climate.xlsx. Filename increments with version. `DEFAULT_DB` at the top of `tools/validate.py` must be updated in the same commit. |
| MedianHomeAuditMASTER.xlsx | Full audit history including superseded v1.0 archetype values | Project knowledge | Reference only. Not authoritative for live values. |
| Budget-Audit-*.xlsx | Per-rebuild audit trail | Project knowledge | Current: Budget-Audit-Jun-16-2026.xlsx |
| BUDGET-METHODOLOGY.md | Budget formula and sources | `docs/` in the repo | Current: v1.0 (June 16 2026) |
| MEDIAN-HOME-METHODOLOGY.md | Citywide-default rule, NRC list, callout requirement | `docs/` in the repo | Current: v1.2. Upstream of budget; Typical Home Values feed BUDGET-METHODOLOGY.md. |
| MEDIAN-HOME-LABEL-CONVENTIONS.md | (Deprecated, deleted) | Nowhere | Retired with MEDIAN-HOME-METHODOLOGY.md v1.2 and removed. NRC callout markup lives in PROFILE-FORMATTING.md v1.2. Do not resurrect. |
| MEDIAN-HOME-AUDIT-REFERENCE.md | Audit history and annual refresh playbook | **GAP: not in the repo** | Aligned with v1.2. Governing doc still outside `docs/`, in breach of 4a. Move it in and delete the outside copy. |
| PROFILE-FORMATTING.md | Profile-page formatting standard (light-mode lock, cost-strip alignment, em-dash policy, NRC callout structure, bolding convention) | `docs/` in the repo | Current: v1.2 (June 29 2026). Canonical reference profile: cities/st-louis/profile.html |
| GUIDE-METHODOLOGY-DECISIONS.md | Scoring decisions across guides | `docs/` in the repo | |
| HUM-HEAT-Scoring-Guide.md | Humidity and heat scoring rubric | `docs/` in the repo | |
| *-cities-scoring-analysis.md | Per-guide scoring analysis | `docs/` in the repo | Six confirmed live: active-retirees, arts-lovers, foodie, healthcare, hikers, sports-fans. **GAP: the LGBTQ analysis is not in `docs/` under any expected filename.** Locate it and commit it. Authoritative for landing-page placement decisions; read the rubric before any placement call. |
| index.html | Quiz engine, landing structure, PUBLISHED_PROFILES map, CITIES array | GitHub repo (lauriekwaller-lgtm/retire-me-here) | Source of truth for what profiles are live and for the v15.1 city data shown on the quiz |
| sitemap.xml | Search engine discovery | GitHub repo only | **Derived artifact, not an index.** It is only current if step 5 of SOP-1 ran. Never use it to enumerate what exists. See 4b. |
| cities/*/profile.html | Profile pages | GitHub repo | One folder per city slug |
| compare-retirement-cities.html and *-vs-*-retirement.html | Comparison pages | GitHub repo | Derived from CityDatabase; rebuild from current data, not prior page versions |
| pin-studio.html | Pinterest pin generator | GitHub repo | Uses localStorage to persist field inputs |
| visit-before-you-decide.html | Scouting-trip pillar page | GitHub repo | Anchors the affiliate integration; links from every Visit block |
| scouting-trip-workbook.html + .pdf | MailerLite lead magnet (planning workbook) | GitHub repo | Downloadable PDF gated via MailerLite form |
| affiliate-policy.html | Affiliate disclosure page | GitHub repo | Footer link; states commission model and honest-alternatives framing |
| This document (SITE-OPERATIONS-LOG.md) | Operations and handover | `docs/` in the repo | Update at the time of the work, not later |
| TASKBOARD.md | Live work queue and profile counts | `docs/` in the repo | The validator `docs` check warns when its counts drift from live reality |
| tools/validate.py | Pre-deploy gate | GitHub repo | Pre-deploy: `python3 tools/validate.py --local .` Post-deploy confirmation only: `python3 tools/validate.py` |

**Storage convention.** Every governing document lives in `docs/` in the repo and nowhere else. This reverses the pre-July-12 convention, which stored them in project knowledge. That earlier paragraph survived in this table until July 14, 2026 and was actively contradicting section 4a below, telling readers to look in exactly the place 4a forbids. Two `.xlsx` audit artifacts (MedianHomeAuditMASTER, Budget-Audit-*) remain outside the repo as reference-only history and are not governing documents.

### 4a. Canonical source rule (adopted July 12, 2026)

**The GitHub repo is the single source of truth for every file. Nothing lives in two places.**

| Where | What lives there |
|---|---|
| `docs/` in the repo | Every governing `.md` document and the current `CityDatabase_*.xlsx`. This is canonical. |
| Project knowledge | Nothing that also exists in the repo. Working copies only, treated as disposable. |
| Live site files | `raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main/<path>`. Always pull fresh. Never trust a cached or documented copy. |

**Why the repo and not project knowledge.** Git gives version history; project knowledge does not. The database moved from v15.1 to v16.1 with nothing recording it, which is how St. Paul ended up correct in four places and wrong in a fifth. Project-knowledge files can also change silently mid-session. A source of truth that can change without a record is not a source of truth.

**Reading rule for any session, human or model.** Pull the file live from the repo. Do not read a project-knowledge copy of anything that also exists in the repo. On July 12, 2026, all fifteen HTML files then in project knowledge were checked against live: fifteen of fifteen were stale. They have been removed and must not be re-added.

**Only one copy of a governing doc may exist.** If you find two, stop and reconcile before doing anything else. Do not assume the newer-looking one is newer. On July 12, 2026, four documents had diverged: three were ahead in project knowledge and one was ahead in the repo.

**When the database version changes**, in the same commit: add the new xlsx to `docs/`, delete the superseded one, update `DEFAULT_DB` at the top of `tools/validate.py`, and record it in the change log below.

**No repo snapshots in project knowledge. Ever.** (Added July 14, 2026.) A GitHub connector attached to the project ingests a point-in-time *snapshot* of the repo into project knowledge. It does not read live. It sits in the context window of every chat that opens, looking exactly like the real repo, and it goes stale the moment you push. This is the same failure as a stale pasted file, except it is invisible, it covers every file at once, and nothing about it announces that it is a copy. Do not attach a GitHub connector to this project. If one appears, remove it before doing any other work.

**A file sitting in context is not evidence that it is current.** This is the rule that catches everything above. Staleness is not detectable by reading the file. A June sitemap and a July sitemap are both well-formed XML. The only way to know is to fetch from `raw.githubusercontent.com` and compare. So: fetch, always, even when a copy is already sitting right there.

### 4b. Enumeration rule: how to find out what exists (adopted July 14, 2026)

**Never enumerate the site from `sitemap.xml`.** It is a *derived* file, hand-maintained at step 5 of SOP-1. It is only accurate if that step ran. A slug missing from the sitemap means the sitemap is behind, not that the city does not exist, and a chat that assumes otherwise will conclude a live profile is missing.

**The directory listing is the enumeration of record.** It cannot be stale, because it is the repo:

```
https://api.github.com/repos/lauriekwaller-lgtm/retire-me-here/contents/cities?ref=main
```

Filter for `type == "dir"`. Each directory is one live city slug. As of July 14, 2026 this returns 43.

The old grep-the-sitemap pattern (`grep -oE 'cities/[a-z0-9-]+/'`) is retired. It is still fine as a way to audit *the sitemap itself* for drift, which is a different and useful job: diff the directory listing against the sitemap and any delta is a step-5 miss that needs fixing.

**Cache note.** `raw.githubusercontent.com` serves through a CDN with roughly a five-minute TTL. If you have just pushed, append a cache-buster (`?v=$(date +%s)`) or you will read the previous commit and not know it.

### 4c. Session start gate (adopted July 14, 2026)

Before any work touching cities, comparison pages, landing pages, or the sitemap, a session must first fetch the live `cities/` directory listing (4b) and echo the count and slug list. No work proceeds until that is done.

This exists because the failure mode is silent. On July 14, 2026 a comparison-page session reported that Savannah did not exist in the repo. Savannah had been live for hours. The session was reading a project-knowledge snapshot listing 29 cities and 3 comparison pages while the repo held 43 and 18. Fourteen live cities were invisible to it: chattanooga, delray-beach, fort-collins, fort-myers, kansas-city, knoxville, memphis, miami, naples, pensacola, prescott, savannah, st-augustine, st-petersburg. Nothing in the session looked wrong. It had a plausible file and no reason to doubt it.

The gate costs one API call. Skipping it costs a rebuild on bad data.

---

## 5. Version conventions

**Database files** follow the pattern `CityDatabase_<Month>_<Day>_v<N>.xlsx`. The version number is canonical; the date is informational. Each rebuild bumps v. A point-release (for example v15.1) indicates a methodology or formula change within the same annual cycle. A trailing point-point release (v15.1.1) indicates a single-city data correction that does not warrant a full recompute.

**Audit files** are dated, not versioned: `Budget-Audit-<Month>-<Day>-<Year>.xlsx`. One audit file per rebuild.

**Methodology docs** carry a version number in the footer (for example "v1.2 — June 29, 2026"). Bump the major version for any formula change, minor version for source refreshes.

**Profile HTML files** are not versioned; the GitHub commit history serves that role.

## 6. Standard operating procedures (SOPs)

These are the short playbooks for the most common operations. Detailed walkthroughs and prompts live in the project knowledge or can be reconstructed from the change log.

### SOP-1: Add a new city profile

1. Confirm the city is in the current DB and has all 10 dimension scores plus budget data.
2. Source three photos: hero 1600×899, detail 1600×2133 (portrait), lifestyle 1280×1280 (square). Vet for licensing and editorial fit.
3. Build the profile HTML matching PROFILE-FORMATTING.md v1.2 (canonical reference: `cities/st-louis/profile.html`). Ensure zero em-dashes in rendered content per the em-dash policy.
4. If the city qualifies for NRC treatment (see MEDIAN-HOME-METHODOLOGY.md v1.2 for the current 10-city list and the editorial rationale), include the Neighborhood Reality Check callout per PROFILE-FORMATTING.md v1.2.
5. Add a Visit Before You Decide block above `<!-- QUIZ CTA -->` with city-specific hook, neighborhoods, hospital, and Expedia/Vrbo affiliate codes generated from Creator Hub.
6. Update PUBLISHED_PROFILES in index.html (key = `cityName_state`).
7. Update sitemap.xml with the new URL.
8. Fix reciprocal landing-page links if the city's card isn't already on relevant landing pages.
9. Submit URL to Search Console for indexing.
10. Log in Section 7 below.

### SOP-2: Budget recompute (quarterly trigger)

1. Pull current Freddie Mac PMMS rate.
2. Open the current Budget-Audit file's Formula Inputs sheet, update the mortgage rate constant.
3. Run the formula across all 99 cities (Python notebook).
4. Spot-check 5 cities (one per tier) for sanity. If reasonable, proceed.
5. Generate new Budget-Audit-<date>.xlsx.
6. Update BUDGET-METHODOLOGY.md snapshot date and rate value.
7. Generate new CityDatabase_*_vN+1.xlsx with updated Monthly Est and Budget Range columns.
8. Deploy: replace database, deploy code if quiz boundaries change, refresh any pages with hardcoded budget numbers.
9. Log in Section 7.

### SOP-3: Annual full rebuild (June)

1. Run SOP-2 first to refresh the mortgage rate.
2. Pull November Medicare Part B/D announcement values, update healthcare constants.
3. Pull current USDA Cost of Food at Home (Moderate Plan, age 51-70 couple).
4. Pull current BLS Consumer Expenditure Survey 65+ data for utilities and discretionary baselines.
5. Pull fresh Zillow ZHVI snapshot for all 99 cities. For the 10 NRC cities, also re-pull ZHVI for the named retiree-target neighborhoods and reconfirm the citywide-vs-neighborhood gap remains editorially significant enough to warrant the callout (per MEDIAN-HOME-METHODOLOGY.md v1.2).
6. Review whether any non-NRC city's neighborhood premium has grown enough to warrant adding it to the NRC list. Check borderline cases (currently Tampa and Charleston SC are the closest to the editorial threshold).
7. Update KFF Medigap state-level data.
8. Generate new audit file and database version.
9. Update BUDGET-METHODOLOGY.md to v(N+1). Update MEDIAN-HOME-METHODOLOGY.md if any methodology refinement occurred.
10. Deploy.
11. Log in Section 7.

### SOP-4: Deploy a database update

1. Drag-drop the new DB file into the GitHub repo, replacing the prior version (rename if filename changed).
2. Refresh the CITIES array in index.html with the new monthlyEst, medianHome, and budgetRange values for all cities.
3. Refresh profile stat cards for any city whose Typical Home Value or Monthly Budget changed.
4. If quiz logic depends on Budget Range tier boundaries, edit BUDGET_OPTIONS array in index.html.
5. Commit. Netlify auto-deploys.
6. Verify on production: load index.html, run the quiz, confirm budget tier matches.
7. Submit Search Console indexing request for any page with materially changed copy.

### SOP-5: Batch profile edit via Codespaces (bulk operations)

1. Open Codespaces on main. Run `git status` and `git pull origin main` to confirm clean sync.
2. Upload the change bundle (zip of modified files organized as `cities/<slug>/profile.html`) into the workspace file panel.
3. `unzip -o <bundle>.zip` from the terminal to overwrite target files in place.
4. `rm <bundle>.zip`, then `git status` to confirm expected modification count and no stray untracked files.
5. Spot-check one or two diffs with `git diff cities/<slug>/profile.html | head -30`.
6. `git add cities/`, `git commit -m "<descriptive scoped message>"`, `git push origin main`.
7. Watch Netlify deploy log; verify on production in an incognito window.
8. Log in Section 7.

## 7. Change log

### 2026-07-19 - San Antonio, TX profile; a false UNESCO claim caught by the rubric check

**Shipped.** `cities/san-antonio/profile.html`, profile 44, plus hero/detail/lifestyle photos. Built
from a live pull of the canonical `cities/st-louis/profile.html` rather than any local copy. All
dimension scores, `Monthly Est` and `Median Home` read from
`docs/CityDatabase_Jul_13_v16_4_climate.xlsx` row 75. Research was used only for supporting color:
SAT nonstop and carrier counts, University Hospital and Methodist credentials, Bexar County property
tax rates.

**Emphasis brief.** Two dimensions at 9 (D1 Airport, D5 Tax) and two at 8 (D3 Health, D10 Community).
That is the MULTI-STRENGTH shape rather than MULTI-PILLAR, so the hero tagline and opening character
paragraph carry all four. The hard-flagged counterweight is not a D-score: `Climate Hot Sum` = 3 with
HEAT 9 and HUM 8, which leads the "Skip if" column. D6 and D7 at 5 fill out the honest column.

**Bug caught pre-publish.** The draft claimed San Antonio was "the first U.S. city named a UNESCO
Creative City of Gastronomy." It is not. `docs/foodie-cities-scoring-analysis.md` records Tucson at
2015 and San Antonio at 2017, both in the database. Corrected to "one of only two in the United
States" in the two places it appeared. The claim was invented during drafting, not read from any
source document, and it would have shipped if the landing-page rubric review had been treated as
out-of-scope for a city BUILD. **Consequence: consult the relevant `*-cities-scoring-analysis.md`
before publishing a profile, not only before making a landing-page placement decision.** Those docs
carry verified credential facts, not just tier assignments.

**Editorial correction after operator review.** The first draft led on the Spanish missions because
that is where the UNESCO World Heritage credential sits, and left the River Walk to a fast-fact and
the Alamo to a single clause. Operator flagged that a reader arriving at a San Antonio page expects
those two first. Revised: the hero tagline opens on the River Walk and the Alamo, character P1 makes
the river the reason the city exists and the River Walk its modern axis, and the Visit block hook
opens on both before pivoting to the four missions south of downtown. Final counts: River Walk 10
mentions, Alamo 16. General lesson: the credential and the landmark a reader is actually looking for
are not always the same thing, and the profile has to serve both.

**NRC callout added off-list.** San Antonio is not one of the ten NRC cities in
`PROFILE-FORMATTING.md`, but the DB row makes the case on its own: `Median Home` `$320,000` against
retiree-target neighborhoods at `$400K-$900K`. MEDIAN-HOME-METHODOLOGY.md v1.2 treats the NRC as a
universal editorial mechanism rather than a fixed list, so the callout was added and approved.
San Antonio is the eleventh NRC city; the formatting doc still says ten.

**Four data conflicts surfaced, none fixed here.** All four are logged on the taskboard. The serious
one is the DB `Highlight` string, which says "Citywide median home $260K" while the structured
`Median Home` field says `$320,000`. Because `Highlight` renders on `pick-and-compare.html` and the
foodies landing card, the site is currently publishing two different medians for the same city. The
other three: `PropTax Rate %` 1.4 against real Bexar effective rates of 1.55% to 1.96%,
`Budget Range` 2 against a `Monthly Est` midpoint in Range 3, and a `scoreNotes.DW` January mean of
44 F against the DB's 52. This repeats the July 14 Knoxville pattern: hard-coded prose figures inside
`index.html`, and inside DB free-text fields, drift away from the structured fields and nothing checks
them. The pros/cons figure check covers one such surface; `Highlight` is another.

**Landing pages.** No edits were required. Existing San Antonio cards on `top-cities-for-foodies.html`
and `urban-walkabout.html` already linked via `index.html?city=San Antonio&state=TX`, which the new
`PUBLISHED_PROFILES` entry resolves. A rubric review of all seven landing pages found San Antonio
explicitly excluded from Sports Fans (Spurs only, against a documented 2-team Tier 2 minimum), with no
case on Hikers (D7=5) or Active Retirees (D8=6), and unevaluated on Healthcare and Arts Lovers where
it reads as a Tier 2 candidate on both. Those two placements are parked as BATCH work.

**Also confirmed, not a bug.** The numbered counters on landing-page city cards restart at 1 within
each tier and each tier is alphabetical, so they are positional, not rankings, and are not expected to
match the rank column in a scoring-analysis doc.

**Files changed.** `cities/san-antonio/profile.html` (new), three photos (new), one
`PUBLISHED_PROFILES` line in `index.html`, one url block in `sitemap.xml`, `TASKBOARD.md`,
`SITE-OPERATIONS-LOG.md`.

### 2026-07-15 - Working-environment clarification (Codespaces, not Mac-local paths)

Clarified in Section 9 ("Where the work happens") that although Laurie works from a Mac laptop, the
repo working tree lives in Codespaces at `/workspaces/retire-me-here`, and all interactive terminal,
git, deploy, and file-management commands run in the Codespaces shell. Operator-facing instructions
must use bare Codespaces commands and paths, not Mac-local filesystem paths or a leading `cd`. Prompted
by a deploy where Mac-style `cd ~/path/to/repo` guidance failed (harmlessly) because the shell was
already in the Codespaces repo root. Docs-only change; no site or scoring impact.

### 2026-07-14 - Knoxville vs. Nashville comparison page; stale index.html median fixed

**Shipped.** `knoxville-vs-nashville-retirement.html`, comparison page 19. Built from
`knoxville-vs-chattanooga-retirement.html` against COMPARISON-PAGE-STANDARD-v2. All scores,
dollar figures, and budget tiers read from `docs/CityDatabase_Jul_13_v16_4_climate.xlsx`.
Checkmarks at 2+ point gaps only (D1 to Nashville; D7, D9 to Knoxville) plus the three cost rows.
Airport counts verified against carrier route data, July 2026: TYS 40 nonstops / 7 airlines, all
domestic; BNA 122 nonstops / 18 airlines including transatlantic.

**Bug fixed.** The Knoxville record in `index.html` carried `"$327K typical home value"` in its
`pros` array while its own `medianHome` field read `$368,000`; the DB agrees with $368,000. The
string appeared nowhere else in the repo and the profile was already correct. Corrected to $368K.
The `pros`/`cons` arrays hold hard-coded figures no check ties back to `medianHome` or the DB;
this is the likely place for a stale number to survive a refresh. Candidate for a validator check.

**Deploy note (stale-snapshot near-miss).** The first build of this deploy shipped a full
`index.html` copied at session start. Between that pull and the push, live `index.html` had been
cleaned of five dataset-scoped superlatives. Unzipping the session-start copy over the pulled tree
reintroduced all five, and the pre-deploy gate (correctly) failed with 5 errors. Rebuilt the entire
deploy against a fresh pull and reduced the `index.html` change to the single `$327K -> $368K` line
rather than shipping the whole file. Reinforces section 4a: never ship a whole file copied at
session start; re-pull immediately before packaging and apply the minimum diff.

**Also updated.** `sitemap.xml`, `compare-retirement-cities.html` (hub card, ItemList position 19,
og/twitter description), reciprocal pills on the two sibling Tennessee matchups, `TASKBOARD.md`.

### 2026-07-14 - Stale repo snapshot removed; enumeration and session-start rules added

**Symptom.** A comparison-page session reported that it could not find the Savannah profile in the
repo, and was working from figures that did not match live. Savannah had been deployed and was
returning HTTP 200.

**Cause.** A GitHub connector was attached to the project. It had ingested a point-in-time snapshot
of the repo into project knowledge. That snapshot loads into the context window of every chat in the
project before any tool call runs. Sessions were reading it, reasonably, as the repo. It was not the
repo. It was a June copy: 29 city profiles and 3 comparison pages, against 43 and 18 live. Fourteen
live cities were invisible to every session in the project.

The failure was silent by construction. The snapshot is well-formed and complete-looking. There is no
signal, from inside a session, that distinguishes a current file from a three-week-old one. Section 4a
already said "do not read a project-knowledge copy of anything that also exists in the repo," and the
sessions were not knowingly breaking that rule. They did not know they had one.

**Second cause, latent.** The section 4 file table still carried the pre-July-12 storage convention,
listing seven governing docs as "project knowledge only" and stating outright that methodology docs
do not live in GitHub. Section 4a, adopted July 12, says the exact opposite. Both were in the same
document, forty lines apart, for two days. Any session that read the table before the rule got the
wrong instruction from its own governing doc.

**Third cause, structural.** The documented way to enumerate cities was to grep `sitemap.xml`. The
sitemap is a hand-maintained derived file, updated at step 5 of SOP-1. Using it as the index means a
missed step 5 presents as a missing city. The sitemap should never have been the index.

**Fixed.**
- GitHub connector removed from the project. Verified: a fresh session now returns 43 profiles.
- Section 4 table corrected. Seven docs relocated on paper to `docs/`, where they had already been
  living since July 12. The contradictory storage-convention paragraph is gone.
- Section 4a extended: explicit ban on repo snapshots and connectors, plus the general rule that a
  file sitting in context is not evidence that it is current.
- Section 4b added: the GitHub contents API directory listing is the enumeration of record. The
  grep-the-sitemap pattern is retired for enumeration and repurposed as a sitemap drift audit.
- Section 4c added: session start gate. Fetch the live city list and echo the count before any work
  touching cities, comparison pages, landing pages, or the sitemap.

**Two gaps surfaced and left open** (see section 8): MEDIAN-HOME-AUDIT-REFERENCE.md is not in `docs/`,
and the LGBTQ scoring analysis is not in `docs/` under any expected filename. Both are governing docs
sitting outside the repo, which is what 4a exists to prevent.

**Judgment call.** The section 4 table now marks those two as GAP rather than quietly dropping them.
A visible gap in the canonical doc is worth more than a tidy table that lies.

### 2026-07-14 - Superlative policy closed out, guide em-dash sweep, validator mode banner

Four batches, pushed in sequence. All four started as "clean up 41 warnings" and turned into
something else, which is the useful part of the record.

**Batch 1 - the warnings were the wrong target.** Of the 39 real superlative warnings, most were
TRUE claims about the outside world (Michigan Stadium is the largest stadium in the country) that
should stay. But they formed a 39-line wall nobody reads, and false claims were hiding in it.
Found and fixed: Chattanooga "best value in the Southeast" (8th-cheapest SE city; D2=8 loses to
Paducah and Memphis at 10); Tampa "best value in Florida" (D2=6 at $400K, beaten by four FL cities,
and our own Florida page already said Pensacola was cheapest, so the site contradicted itself);
BOTH FAQPage schema answers were wrong (Florida named Fort Myers second-cheapest when Delray is
$341K; Midwest named Columbus cheapest when Des Moines is $191K) - Google can serve those as direct
answers. Florida's best-for-budget card had all four figures wrong. Corpus Christi listed at $214K
against a DB value of $219K.

Gate leaks closed: "in ENTIRE database" and "we have COMPARED" walked through because both halves of
the ban were still closed word-lists. Six live violations sat behind them, three in index.html.

**docs/SUPERLATIVE-LEDGER.md created.** The warn tier fires on outside-world claims no spreadsheet
can settle. Those cannot be rewritten away and should not be. But an unclearable warning is worse
than no warning. The ledger retires a reviewed claim from the queue, with evidence, so the queue can
sit at zero and a NEW claim actually shouts. Stale entries self-report. Dataset-scoped claims may
never go in it; those are a hard FAIL.

**Batch 2 - the "in our Florida coverage" family.** ~25 dataset-scoped rank claims hiding behind a
region word between the modifier and the noun. St. Augustine's profile carried fourteen alone. All
re-anchored to a figure or a named city. Rewriting them exposed five factual errors: St. Augustine
claimed FOUR TIMES that "only Naples costs more" when Miami ($575K) and Sarasota ($462K) both exceed
its $432K (it is fourth-priciest, not second); Naples vs Fort Myers listed budget "7 vs. 3" against a
DB of 6 vs. 5; Pensacola vs Fort Myers said budget "ties at 7" when it is 8 vs. 6; Madison vs Columbus
gave Columbus $249K (DB: $235K) and "best airport access in our Midwest coverage" when St. Paul scores
10 to Columbus's 8; Nashville vs Memphis claimed Nashville had Tennessee's deepest walkability at
D6=5, against Chattanooga's 6. Also killed "Lee Health, #3 on our healthcare list" (x6): landing pages
are alphabetical within tiers, not ranked, so that rank never existed.

**Batch 3 - guide em-dash sweep. It was 231, not 64.** All five guides, not two: globetrotter (71),
wellness-blueprint (55), urban-walkabout (41), value-navigator (36), active-frontier (28). Swept per
the PROFILE-FORMATTING.md substitution rules. `GUIDES_TOO` flipped to True and planted-error tested.

The flag was never a decision. Its comment said guides were "grandfathered; see PROFILE-FORMATTING.md",
and that document grandfathers nothing - its scope is profiles, and its sweep status only ever covered
the 38 profiles. The flag was recording an UNFINISHED JOB in the grammar of a DECISION, which is why
nobody questioned it, and it hid 231 em-dashes for as long as it stayed False. Worth watching for
elsewhere in the codebase.

Also found: all five guides said "Our database has 100." It has 99. The count was removed rather than
swapped for another number that would rot.

**Batch 4 - database-voice attribution.** 46 instances of "our database notes / calls / flags / scores"
across 18 files. Two faults in one phrase. It is dataset-scoped, so it rots. And worse, it LAUNDERS AN
OUTSIDE FACT through our own spreadsheet: US News rates NCH, NOAA models the surge, Motley Fool made
the Motley Fool call. Attributing those to "our database" points the reader at a private document they
cannot open, in place of the real source. It reads as evasive and it is weaker than the truth. State
the fact, drop the attribution. Four more found wearing a different noun ("the gentlest in our Florida
SET"). Rehoboth Beach was billed as "one of the pricier additions to the database" at $632K; Carmel is
$2,281,000 and Park City $1,522,000.

**Validator mode banner.** `validate.py` is one command doing two entirely different jobs, and nothing
on screen said which. Run bare before a push and it grades the OLD live site with the NEW rules, then
reports failures already fixed. This misfired twice in one session. It now prints PRE-DEPLOY GATE
(reading this machine) or POST-DEPLOY CHECK (reading live GitHub, not your working copy) at the top of
every run.

**Net:** validator 0 failures, 0 warnings, local and live agreed. Superlative gate now catches every
shape found leaking: bare/modified corpus nouns, curation verbs, "of any X here", verb-to-corpus
("top the database"), attribution voice ("our database notes"), and "our REGION set".

### 2026-07-13 — Climate engine rebuild: dealbreakers, mild scoring, and a mislabeled column

**Problem.** A quiz run with Weather Preference set to "Mild Year-Round" and
dealbreakers set to "cold winters (below freezing)" and "grey / cloudy winters"
returned Boulder as the #1 match, followed by Scottsdale and St. Petersburg.
Boulder has a January mean of 33F and 88 inches of snow a year. The dealbreaker
UI promises "we'll remove those cities from your results." It was not doing that.

Four separate faults were compounding. Each is worth recording, because none of
them is visible from the surface behavior and all four were mutually concealing.

**Fault 1 — the cold dealbreaker was calibrated against the wrong scale.**
The filter read `climate.W > 3`, where `W` is winter comfort on a 1-10 scale.
That removes only the 29 harshest-winter cities. Boulder is `W:5` and passed.
So did Bend, Fort Collins, Grand Junction, Flagstaff, Colorado Springs, Boise,
Santa Fe, Pittsburgh and St. Louis, all of which have January means at or below
freezing. Raising the threshold could not fix this: the `W:5` bucket holds both
Boulder (33F, 88 inches of snow) and Greenville SC (42F, 3 inches). No cutoff on
`W` separates them. `W` is a comfort-preference score and cannot carry a hard
factual promise about temperature.

**Fault 2 — the `Climate Mild YR` database column was mislabeled.** The column
does not hold a mildness score. It holds the dryness/humidity score, `M`, exactly
as defined in scoring rubric v3.2 (10 = very dry, 1 = very humid). Proof: Tucson
is 9 and Scottsdale is 10 on this column, and neither is a mild-year-round city.
The grey-winter dealbreaker had been wired to it (`climate.M > 4`), so "no grey
winters" was filtering on humidity. It removed Naples, Miami, Tampa, Charleston
and Savannah, the sunniest cities on the site, while keeping Pittsburgh (45%
possible sunshine, among the cloudiest in the country). It also split Tampa from
St. Petersburg, twenty miles apart under the same sky. The column is renamed to
`Climate Dryness M` in v16.4. Values are unchanged; only the header was ever wrong.

**Fault 3 — the `mild` formula was a weighted average, so extremes cancelled.**
`0.40*W + 0.40*(10-HEAT) + 0.20*(10-HUM)`. An average lets a great season offset
a terrible one. Boulder scored 6 (cool summers, dry air, freezing winter ignored).
Scottsdale scored 5 (perfect winter, lethal summer, the two cancelling). Under the
old formula Boulder genuinely was a better "Mild Year-Round" city than Scottsdale.
"Mild year-round" means no bad season, so the score must reflect the WORSE of
winter and summer, never the blend. `warm_dry` carried the identical flaw: a cold
dry city could pass as "warm and dry." Both are rewritten as worst-of.

**Fault 4 — a guard was silently discarding the climate filter.** The climate hard
filter ended with `if (climateFiltered.length >= 5) candidates = climateFiltered;`.
When fewer than five cities cleared the threshold, the filter was dropped entirely
and the user's climate preference stopped applying at all. It failed open and said
nothing. Now it falls back to the fifteen best-matching climates instead of to no
filter. This one was invisible until the `mild` formula was sharpened, at which
point it immediately began firing.

**Resolution.** Three real data columns added, sourced from NOAA-NWS 1991-2020
normals: `Jan Mean F`, `Ann Snow in`, `Ann Sun %`. The two broken dealbreakers now
read the data that matches the promise printed on the button:

- cold  →  `janF >= 34 && snow <= 15`
- grey  →  `sun >= 55`

`mild` and `warm_dry` rewritten as worst-of-season, with the winter term read from
`janF` directly rather than from `W`. Climate hard-filter threshold raised from
5/3 to 7/5. The fail-open guard closed.

**Deliberately NOT done.** An earlier version of this work recalibrated `W` across
all 99 cities from January temperature. It moved 66 of 99 values and would have
churned `warm`, `cool` and `seasons` as collateral. It was withdrawn. Once the
dealbreakers read real temperature and `mild` reads `janF` directly, recalibrating
`W` buys nothing. `W`, `H`, `M`, `HUM` and `HEAT` are otherwise untouched: zero
score churn.

**Data corrections (2).** Sedona `Climate Warm W` 7 -> 5 (January mean 41F; it was
scored warmer than Fort Worth at 47F). Grand Junction 5 -> 3 (January mean 29F; it
was scored warmer than Boise). These were the only two cities whose `W` was off by
2 or more against actual normals. Neither changes any ranking.

**Verification.** The patched JavaScript was executed directly in Node against the
live `CITIES` array, not reimplemented. All four climate paths regression-tested:

| Preference | Top matches after patch |
|---|---|
| Mild Year-Round | Delray Beach, St. Petersburg, Tampa, Sarasota |
| Warm & Dry | Scottsdale, Las Vegas, Tucson, Palm Springs |
| Cool / Mountain | Ann Arbor, Salt Lake City, Jackson Hole, Boulder |
| Four Seasons | Ann Arbor, Salt Lake City, Pittsburgh, St. Paul |

Boulder now surfaces on Cool / Mountain, where it belongs, and nowhere else.
Scottsdale surfaces on Warm & Dry and is absent from Mild. The reported quiz
returns 17 matches instead of 41, with Boulder, Scottsdale, Bend and Pittsburgh
all correctly removed.

**Not a bug: weather is 25% of the match score.** After the fix, Florida cities
still lead a Mild Year-Round search ahead of Santa Barbara and Carmel, which score
higher on climate. This is the weighting working as designed, not a fault. Picking
a weather preference auto-sets `DC` to "Very Important" (weight 3) while the nine
other dimensions sit at 1, so climate is 3 of 12 weight units. Florida's tax,
healthcare and senior-fitness scores outrun a three-point climate edge. Raising
weather's influence is a product decision, not a defect, and would need testing
against every other quiz path before being attempted.

**Files updated:** `index.html` (99 climate blocks extended; `mild`, `warm_dry`,
both dealbreakers, the climate threshold and the fail-open guard rewritten),
`docs/CityDatabase_Jul_13_v16_4_climate.xlsx` (3 columns added, 1 header renamed,
2 values corrected), `tools/validate.py` (`DEFAULT_DB` bumped to v16.4).

**Files removed:** `docs/CityDatabase_Jul_13_v16_3_d2-rebuild.xlsx`.

**Open items.**
1. `Ann Sun %` is the softest of the three new columns. Percent-possible-sunshine
   is published for only a subset of NOAA stations, so roughly 30 of the 99 values
   are interpolated from the nearest reporting station. Adequate behind a 55%
   filter cutoff. Do not print these figures on a profile page without verifying
   the specific city.
2. The validator does not yet check climate data. A future pass should assert that
   the `CITIES` array climate blocks in `index.html` match the database
   (they matched exactly, 99 of 99, on all five original fields as of this entry)
   and that `janF`, `snow` and `sun` are present and non-null for every city.
3. Beaufort is coded `NC` in the database and is Beaufort, North Carolina. Confirmed
   2026-07-13. Normals sourced accordingly. Recorded here because "Beaufort" reads
   as South Carolina to most people and this will be second-guessed.

### 2026-07-12 — Source-of-truth reconciliation and site validator

**Problem.** Governing documents existed in two places, `docs/` in the repo and project knowledge, and had silently diverged. Four of thirteen did not match, and the direction of staleness was not consistent: `MEDIAN-HOME-METHODOLOGY.md` (repo v1.1 vs project v1.2), `PROFILE-FORMATTING.md` (repo v1.3 vs project v1.4), and `SITE-OPERATIONS-LOG.md` (repo June 19 vs project June 29) were behind in the repo, while `GUIDE-METHODOLOGY-DECISIONS.md` was behind in project knowledge, missing its June 7 addendum entirely. Separately, all fifteen HTML files in project knowledge were stale against the live site.

**Resolution.** Adopted the canonical source rule in section 4a: the repo is the single source of truth, `docs/` holds every governing doc and the current database, and project knowledge holds nothing that also exists in the repo. Reconciled the four diverged documents file by file. Removed all HTML from project knowledge.

**Files updated in `docs/`:** `MEDIAN-HOME-METHODOLOGY.md` to v1.2, `PROFILE-FORMATTING.md` to v1.4, `SITE-OPERATIONS-LOG.md` to the June 29 base plus this entry. `GUIDE-METHODOLOGY-DECISIONS.md` was already current in the repo and was left alone.

**Files removed:** `docs/CityDatabase_Jun_19_v15_1 (1).xlsx` (superseded by v16.1; leaving both invites a future session to read the wrong one). `data/` folder (redundant; the validator reads the xlsx already in `docs/`).

**Files added:** `tools/validate.py`, `tools/README.md`.

**Validator.** Checks every live page against the current database in seven groups: figures (the `CITIES` array and `CITY_ENRICHMENT` modal prose in `index.html`), profiles, routing, cards, superlatives, em-dash policy, and database hygiene. Exit code 1 on failure, so it can gate a deploy. Run `python3 tools/validate.py` before every deploy.

**First run: 163 failures, 45 warnings.** 143 in `index.html` (the quiz results modal, the largest single exposure on the site), 21 across profile pages, 10 on landing cards, 1 database hygiene. Routing and em-dash both clean. Remediation queued as Passes A through D.

**Notable errors surfaced.** Fort Myers claims to be "the most affordable Gulf Coast entry we cover" in five separate places; it is false, since Corpus Christi ($219K) and Pensacola ($264K) are both cheaper. Pensacola carries the same failure mode: a true scoped claim ("most affordable Florida city") restated elsewhere with the scope dropped ("most affordable city in our coverage"), which is false, as Paducah is cheapest at $185K. The superlative check exists to catch exactly this class of error and reports it as a warning for human judgment, because scope is editorial.

**Open decision.** The em-dash policy is recorded as site-wide but is enforced only on profiles and comparison pages, which are clean. The guides and landing pages carry 294 em-dashes in rendered text and have never been swept. `tools/validate.py` has a `GUIDES_TOO` flag, currently `False`, matching actual practice. Either amend `PROFILE-FORMATTING.md` to scope the rule to profiles and comparison pages, or schedule the fifteen-file guide sweep. The doc and the practice must be made to agree.


Reverse chronological. Add to the top of this list as work happens.

### 2026-06-29 — Florida Visit blocks + line update to Asheville, Boulder, Bend
**What:** Two changes shipped as one deploy (12 modified profiles).

First, deployed **9 Florida Visit Before You Decide blocks** on Miami, Naples, Delray Beach, Fort Myers, Pensacola, Sarasota, St. Augustine, St. Petersburg, and Tampa. Each block follows the established 5-paragraph pattern (city-specific hook / neighborhoods + hospital / Expedia link / Vrbo link / disclaimer) inserted between the closing `</section>` of the prior block and the `<!-- QUIZ CTA -->` marker. Hooks are tailored per city, leading with what's genuinely real about the place, then framing the honest test the visit should run. Each block carries a unique Expedia and Vrbo affiliate code generated in Creator Hub.

Second, applied a **paragraph-2 line update to all 12 Visit blocks** (the 9 new plus the 3 existing on Asheville, Boulder, Bend). The closer changed from *"Do the boring things you'd do as a resident, not the things you'd do as a tourist."* to *"Test the daily routine, not the highlight reel."* Removed the standalone "Price a grocery run." sentence from Boulder and Bend to eliminate redundancy with the new closer. All 12 paragraph 2s now follow the same rhythm.

**Files touched:** 12 profile HTML files (9 Florida + Asheville, Boulder, Bend); one commit.
**Total Visit blocks live:** 12 of 38 profiles.

### 2026-06-28 — Em-dash sweep across 36 profiles
**What:** Applied PROFILE-FORMATTING.md v1.1 em-dash policy retroactively to all previously-legacy profiles. 1,391 em-dashes substituted, zero remaining in rendered zones. Substitution rules applied by context: colon for the label + amplification patterns (cost-strip, stat-sub, section-eyebrow, fast-fact-desc, list-card-tier, section-title, day-activity, hero-tagline single-em-dash), colon for page-title patterns (`<title>`, JSON-LD `headline`, og:title), `, and` for compound-list closers, period + capitalize for genuine independent-clause conjunctions, comma for the default parenthetical majority, and en-dash for day-time placeholders. CSS and HTML comments preserved untouched (207 em-dashes remain there per policy).
**How:** Batch Python script in Codespaces with per-profile diff review; validated tag balance and JSON-LD parse across all 36 files.
**Files touched:** 36 profile HTML files (Asheville was already clean and excluded from the bundle); one commit.

### 2026-06-24 — PROFILE-FORMATTING.md v1.1 (em-dash policy added)
**What:** Added the em-dash policy section codifying zero em-dashes in rendered content, with substitution guidance (period / comma / colon / parentheses in that preference order). Applied to Miami, Asheville, Boulder, Bend as pilot profiles.

### 2026-06-23 — MEDIAN-HOME-METHODOLOGY.md v1.2 + St. Paul refresh + LABEL-CONVENTIONS deprecation
**What:** Three related changes.

First, **methodology to v1.2.** Unified all 99 cities under a single Typical Home Value display pattern: single citywide ZHVI figure. Retired the two-city range-string exception (Wilmington DE and St. Paul MN previously carried a range format). Retired the quantitative 50%-gap threshold for the "Median Honesty Rule"; replaced with editorial judgment about when the citywide-vs-neighborhood gap is significant enough to warrant a Neighborhood Reality Check callout. Expanded the NRC list from 8 to 10 by adding St. Paul MN and Wilmington DE.

Second, **St. Paul refresh to the Memphis pattern.** Updated the St. Paul profile from range-string display ($297K in citywide ZHVI stat card, NRC callout naming Highland Park, Macalester-Groveland, Summit Hill, St. Anthony Park at $415K-$550K).

Third, **MEDIAN-HOME-LABEL-CONVENTIONS.md deprecated.** The NRC callout markup and copy conventions moved into PROFILE-FORMATTING.md. Doc slated for deletion from project knowledge.

### 2026-06-23 — Visit Before You Decide pillar + Expedia Group affiliate integration
**What:** Shipped the standalone scouting-trip pillar page (`visit-before-you-decide.html`) and integrated the Expedia Group Travel Creator Program affiliate links (Expedia, Hotels.com, Vrbo) into the pillar page and into three sample profiles (Asheville, Boulder, Bend). Commission routing via Partnerize (last-click, 7-day cookie, $30 minimum payout). Also shipped `affiliate-policy.html` in the footer and applied for Booking.com through Awin as a secondary channel.

Also shipped `scouting-trip-workbook.html` and `scouting-trip-workbook.pdf` as a MailerLite-gated lead magnet (form ID for the Scouting Workbook capture wired into the pillar page).

### 2026-06-22 — Site polish batch: auto-open removal and Memphis wiring
**What:** Two related fixes shipped same day.

First, removed the inline `DOMContentLoaded` listener that auto-opened one Deep Dive guide form on every profile page load. The original rationale was "so the section never sits empty," but the auto-opened form pushed useful content below the fold. The chip row and `pickGuide` click handler remain; forms now open only on explicit click.

Second, wired Memphis into the live site. The profile had been built in an earlier session and committed to the repo but was never added to PUBLISHED_PROFILES, leaving it unreachable from the site. Added `Memphis_TN` to the map and inserted a sitemap entry.

**How:** Auto-open removal was a single regex find-and-replace in GitHub Codespaces across `cities/**/profile.html`, applied as one commit (37 files modified). Memphis wiring was a separate two-file upload (index.html + sitemap.xml) committed together.
**Files touched:** All 37 profile HTML files; index.html (PUBLISHED_PROFILES); sitemap.xml.

### 2026-06-21 — Median Home methodology v1.1 + v15.1 database ship + profile formatting v1.0
**What:** Three coordinated changes that complete the v15 transition.

First, **methodology reversal to v1.1.** The archetype basket framework from v1.0 (June 17) was retired after the full audit (Batches 1-4, all 99 cities) revealed systematic over-premium-weighting and a Refinement #2 violation in the Tampa basket (Brandon and Riverview included despite being separate municipalities). Replaced with a single rule: citywide Zillow ZHVI as a single Typical Home Value figure for 97 of 99 cities, range format preserved for 2 cities (Wilmington DE, St. Paul MN), plus a Median Honesty Rule for 8 cities (Memphis, Philadelphia, Pittsburgh, St. Louis, New Orleans, Columbus, Kansas City, Tampa, all drawn from the 97 single-figure set) requiring an above-fold Neighborhood Reality Check callout.

Second, **v15.1 database shipped.** `CityDatabase_Jun_19_v15_1.xlsx` generated. Database structure: 99 cities total (Henderson NV collapsed into Las Vegas, reducing from 100 to 99). 97 cities show citywide Zillow ZHVI as a single Typical Home Value figure. 2 cities (Wilmington DE, St. Paul MN) preserve a range format anchored to verified neighborhood ZHVIs. Monthly Est recomputed for all 99 cities using BUDGET-METHODOLOGY.md's mortgaged-buyer formula at 6.52% PMMS with 20% down. `index.html` updated with new BUDGET_OPTIONS tier boundaries ($5,500 / $6,500 / $7,500 / $9,000), refreshed CITIES array data for all 99 cities, and quiz subtitle reframed to explicit PITI plus six-category framing.

Third, **PROFILE-FORMATTING.md v1.0 adopted.** Canonical reference profile is `cities/st-louis/profile.html`. Six mechanical fixes required per profile: light-mode CSS lock, cost-strip alignment, label-only bolding in cost strip, hood-card hover wrapped in `@media (hover: hover)`, week-intro paragraph deleted, structured bolding pass (1-2 topic-sentence whole-clause bolds per character section). All 36 currently-live profiles brought to v1.0.

**Files added or updated:** MEDIAN-HOME-METHODOLOGY.md (v1.1, supersedes v1.0); MEDIAN-HOME-LABEL-CONVENTIONS.md (aligned with v1.1); MEDIAN-HOME-AUDIT-REFERENCE.md (transitioned from audit playbook to historical record plus annual refresh playbook); PROFILE-FORMATTING.md (v1.0); CityDatabase_Jun_19_v15_1.xlsx (new); index.html (updated); 36 profile files (formatting v1.0 pass).
**Files retired:** archetype basket framework in v1.0 of MEDIAN-HOME-METHODOLOGY.md; per-city archetype basket details in v1.0 of MEDIAN-HOME-AUDIT-REFERENCE.md and MEDIAN-HOME-LABEL-CONVENTIONS.md. Superseded content preserved in `MedianHomeAuditMASTER.xlsx` for institutional memory.

### 2026-06-17 — Median Home methodology v1.0 established (superseded June 21)
**What:** Original archetype basket framework for Median Home values. See appendix in MEDIAN-HOME-METHODOLOGY.md v1.1 for the full superseded record.
**Status:** Superseded by v1.1 on June 21, 2026. Retained in change log for institutional memory.

### 2026-06-16 — Budget methodology v1.0 established
**What:** Replaced legacy Monthly Est numbers (no documented source) with a transparent mortgaged-buyer formula. All 100 cities recomputed.
**Why:** Original numbers had no audit trail and produced inconsistent results at the low end.
**Files added:** BUDGET-METHODOLOGY.md (v1.0), Budget-Audit-Jun-16-2026.xlsx.
**Key inputs:** Freddie Mac PMMS 6.52% (06/11/2026), CMS Medicare Part B $202.90 (2026 standard), CMS Part D $38.99 (2026 national avg), KFF Medigap state variance, BLS Consumer Expenditure Survey 65+ baselines.
**Tier boundaries changed:** Old ($3,500 / $4,500 / $6,000 / $8,000) → new ($5,500 / $6,500 / $7,500 / $9,000). Quiz BUDGET_OPTIONS deployed in v15.1.

### Pre-2026-06-16 — Database evolution (incomplete record)
The database progressed through versions ending at CityDatabase_Jun_9_v14.xlsx. The full history was not logged; this is the institutional reset point. Future versions are tracked from v15 forward.

## 8. Open items and future enhancements

**Doc location breaches (opened July 14, 2026, blocking nothing but violating 4a).**
- `MEDIAN-HOME-AUDIT-REFERENCE.md` is not in `docs/`. Commit it, delete the outside copy.
- The LGBTQ `*-cities-scoring-analysis.md` is not in `docs/` under any expected filename. The other
  six are. Locate it and commit it. Until then, LGBTQ landing-page placement calls have no readable
  rubric, and the standing rule is to consult the rubric before any placement decision.

**Validator enhancement (proposed July 14, 2026).** The `docs` check group already warns on taskboard
drift and a stale ops-log registry. Add: diff the `cities/` directory listing against `sitemap.xml`
and fail on any city present in the repo but missing from the sitemap. This converts a silent step-5
miss into a hard pre-deploy failure, and is the mechanical backstop for the 4b rule.


Not commitments. Things worth doing when time and traffic justify.

| Item | Priority | Trigger to start | Notes |
|---|---|---|---|
| 26 non-Florida Visit blocks | High | When affiliate codes generated | Remaining profiles for the Visit Before You Decide rollout. Each needs a unique Expedia and Vrbo code from Creator Hub. |
| Chip nav "Visit" tab activation | Medium | After all 38 profiles have Visit blocks | Currently parked to avoid broken anchors. Flip on after Visit block coverage is complete. |
| Delete deprecated MEDIAN-HOME-LABEL-CONVENTIONS.md from project knowledge | Low | Any time | Superseded by MEDIAN-HOME-METHODOLOGY.md v1.2 and PROFILE-FORMATTING.md v1.2. Slated for deletion. |
| value-navigator.html copy review | Medium | When ready | Budget references and "most affordable" framing for any tier-shift impacts from v15.1. |
| Thematic landing page review for tier-shift impacts | Medium | When ready | Seven landing pages: foodies, healthcare, arts, sports, hikers, LGBTQ, active retirees. |
| Comparison page review for v15.1 dollar updates | Medium | When ready | 13 comparison pages quote dollar figures that may have shifted. |
| /methodology.html ship | Medium | When ready | Public-facing methodology page. Draft content in MEDIAN-HOME-METHODOLOGY.md v1.2 appendix. |
| Memphis Healthcare landing page placement | Medium | When ready | Tier 1 or Tier 2 decision, per Healthcare Confidence Index rubric. |
| Tampa NRC continuation review | Annual | Next June rebuild | Confirm continued inclusion under editorial gap threshold. |
| Charleston SC NRC consideration | Annual | Next June rebuild | Mount Pleasant, Daniel Island, West Ashley diverging from Charleston proper. Recheck editorial significance. |
| Florida hub cluster page | Medium | After remaining Florida Visit blocks and pillar SEO signals | Previously identified as high-traffic opportunity |
| South regional pillar page | Medium | After Memphis Healthcare placement | Memphis currently has no regional pillar home. |
| Cash-buyer toggle / page | Low | Traffic signal or affiliate ask | Adds reach to readers funding moves from prior home sale |
| Independent-living scoring dimension | Low | After current methodology stabilizes | Differentiation moat |
| HOA-inclusive variant for Sun City / Villages / Naples | Low | If reader feedback warrants | Could be a per-city note rather than a database column |
| State-by-state Medigap precision | Low | Annual rebuild cycle | Replace coarse 5-bucket modifier with KFF state-level data |
| Frisco TX placement audit | Low | When refreshing landing pages | Was previously flagged for evaluation |
| Stat card score labels (dimension eyebrows) | Low | Future design pass | Scores currently render as `10/10` without dimension eyebrow labels. |
| Healthcare landing page toggle affordance | Low | Future design pass | Toggle not obvious enough; to be addressed separately. |
| Methodology disclosure block portability | Low | Future design pass | `.methodology-block` CSS pattern designed to port to all seven landing pages. |
| Display ad activation | Triggered | First affiliate contract | Containers deployed, switches off |
| LLC and business banking | Triggered | Revenue signal or contract complexity | Revisit when affiliate revenue lands or a contract requires |
| Trademark filing | Triggered | First affiliate contract | USPTO search confirmed zero conflicting marks |

## 9. Handover essentials (for a future operator)

If you are reading this because Laurie has handed you the site, start here.

**What this site is.** A retirement-city discovery platform that scores 99 U.S. cities across 10 dimensions, helps readers match via a quiz, and monetizes through SEO-driven affiliate revenue. Credibility and accuracy come first; promotional polish never overrides honesty.

**What you should not do until you understand the system.** Do not change the database without reading BUDGET-METHODOLOGY.md and MEDIAN-HOME-METHODOLOGY.md. Do not add cities to landing pages without verifying they have full DB scores and without consulting the corresponding *-cities-scoring-analysis.md document. Do not change tier boundaries or scoring rubrics without documenting in Section 7 above. Do not pin cities to Pinterest before their profile page is live and in the sitemap.

**The single most important habit.** When you do work, log it in Section 7 the same session. The reason this doc exists is that institutional memory disappears when one person carries it all.

**Tools you'll need access to.** GitHub repo `lauriekwaller-lgtm/retire-me-here` (deploy), Netlify (auto-deploys from GitHub), Google Analytics 4 (property G-BTL743DSJQ, tracked under "Destination Retired" account name), Google Search Console, Microsoft Clarity, MailerLite (email capture, form IDs in project knowledge), Pinterest business account, Zillow Research portal (for ZHVI refresh), Freddie Mac PMMS (for mortgage rate), CMS.gov (for Medicare premiums), Expedia Group Creator Hub (affiliate link generation), Partnerize (commission dashboard).

**Where the work happens.** Editing is primarily through GitHub's web interface. For repo-wide operations that github.dev cannot handle (large refactors, bulk file moves, batch profile edits), use GitHub Codespaces from a Mac laptop. See SOP-5 for the batch-edit workflow. Note on the device vs. the working tree: Laurie sits at a Mac laptop, but the repo working tree lives in Codespaces, so every terminal, git, deploy, and file-management command runs in the Codespaces shell at `/workspaces/retire-me-here`, which opens in the repo root already. Instructions handed to Laurie or a future operator should use bare Codespaces commands and Codespaces paths, never Mac-local filesystem paths (e.g. `~/path/to/repo`) and never a leading `cd` to a Mac path.

**Decisions a new operator can make autonomously.** Routine refreshes following the SOPs above. Photo refreshes. Copy edits that don't change scoring. Pinterest content. Small UI polish.

**Decisions that need a conversation.** Adding or removing cities from the database. Changing scoring methodology. Adding new scoring dimensions. Changing tier boundaries. Activating affiliate/ad revenue mechanics. Anything that touches monetization or the trademark.

---

*Site Operations Log v1.3 — June 29, 2026*
*Companion docs: BUDGET-METHODOLOGY.md (v1.0), MEDIAN-HOME-METHODOLOGY.md (v1.2), MEDIAN-HOME-AUDIT-REFERENCE.md (v1.2), PROFILE-FORMATTING.md (v1.2), GUIDE-METHODOLOGY-DECISIONS.md*
*Next review: September 2026 (quarterly cycle)*
