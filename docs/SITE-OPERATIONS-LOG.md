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
| CityDatabase_*_vN.xlsx | Authoritative scoring database | `docs/` in the repo | Current: CityDatabase_Jul_27_v17.xlsx. Filename increments with version. `DEFAULT_DB` at the top of `tools/validate.py` must be updated in the same commit. |
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

### 2026-08-15 (second entry) - centering polish after the font sweep

Operator review on laptop and iPhone found three wrap and centering misses,
one shared root: the sweep's balance heuristic looked for centering inside the
same CSS rule, and these elements inherit centering from a parent. Fixed: both
tool-page hero H1s gain text-wrap balance and lose their hard <br> (the tax
tool stranded the word "tax" on iPhone widths); the tax tool's how-it-works
section is centered with its paragraph box auto-centered; index.html's
hero-subline and hero-headline gain balance (the subline stranded "retirement
life." on laptop widths). Cosmetic only; no data, score, or validator change.

### 2026-08-15 (P0) - quiz buttons dead; fixed; check_js_parse ships

**Files:** `index.html` (one line), `tools/validate.py`, new
`tools/test_js_parse.py`, `docs/TASKBOARD.md`, this log.

**What broke.** The font sweep's text-wrap balance pass matched CSS blocks by
braces, and exactly one match sitewide landed inside JavaScript instead:
`function renderIntro(container) { text-wrap: balance;` on index.html. A CSS
declaration inside a function body is a syntax error; one syntax error kills
the entire script; the quiz engine lives in that script; both quiz buttons
called dead code. The operator caught it in production. Duration of breakage:
from the sweep deploy to this fix.

**Why the gate missed it.** Nothing parsed JavaScript. check_tag_balance
strips script bodies by design, check_jsonld reads only ld+json blocks, and
check_typography reads CSS. A sweep that edits mixed HTML and JS by regex had
no JS-shaped safety net. That is a designed gap meeting an undesigned edit.

**The fix and the class-closer.** The injected declaration is removed and
every inline script on index parses again. check_js_parse joins the tags
group: node --check on every inline script of every page, JSON-LD excluded,
node's absence a loud failure rather than a skip, with a scanned-scripts
floor. Planted-error harness at tools/test_js_parse.py. Any future edit that
breaks page JavaScript, from any tool or session, now fails the gate before
it ships.

**Lesson recorded.** Sweeps that regex mixed-content files must be followed
by parsing every language in the file, not only the language the sweep
targeted. The post-conditions verified the CSS outcome and never asked
whether the JavaScript still ran.

### 2026-08-15 - sitewide font sweep to system B; favicon 2

**Files:** every .html page (typography only, no content changes), favicon.svg,
favicon.ico, favicon-16/32/48/192.png, apple-touch-icon.png, `tools/validate.py`,
new `tools/test_typography.py`, `docs/TASKBOARD.md`, this log.

**What changed.** Operator reviewed a side-by-side preview with real site copy and
chose system B: Playfair Display and Fraunces retired sitewide, display type is now
bold Libre Franklin over the existing DM Sans body. Every font-weight 300 retired:
large display rules became 800, body rules became 400 (thin gray text on the sand
background was the biggest readability cost for a retiree audience). text-wrap:
balance added to centered headline and subline rules, ending single-word orphan
lines on tablets. Eight different Google Fonts links collapsed to one canonical
request, and dropping two families makes every page lighter. The favicon's slab
serif R (the university letter) is replaced by a minimal map-pin mark in the site
teal, regenerated at every size.

**Enforcement.** `check_typography` joins the layout group: any page referencing a
retired family, any 300 weight, or any non-canonical Google Fonts request fails the
gate, with a scanned-file floor so an empty scan can never pass as clean. Planted
error harness at `tools/test_typography.py`. This matters because new pages are
built by cloning existing ones; without the check, the next profile cloned from a
stale template would quietly reintroduce the retired fonts.

### 2026-08-14 - unparsable JSON-LD on the tax tool; check_jsonld shipped

**Files:** edits to `states-that-dont-tax-retirement-income.html`,
`tools/validate.py`, new `tools/test_jsonld.py`, `docs/TASKBOARD.md`, this log.
No DB change, no score change, no copy change.

Search Console reported one Unparsable structured data issue: "Parsing error:
Missing ',' or ']' in array declaration". The FAQPage node inside `@graph` on the
tax tool had shipped without its opening brace, so `"@type"` and `"mainEntity"`
sat loose in the array, with a spare `]` closing the hole further down. Google
drops an unparsable block whole, so the three-question FAQ rich result on the
newest tool page was never eligible from the day the tool shipped, August 11. The
page itself rendered correctly throughout, because browsers do not read JSON-LD.

Why a clean gate did not catch it: the validator was already reading that file
for figures, superlatives, em-dashes and tag balance, and had no check asking
whether the one machine-readable block on the page was machine-readable.
`check_tag_balance` strips `<script>` bodies before counting, by design, so the
schema block was the one region of the page nothing inspected.

So `check_jsonld` ships with the fix, in the tags group. It globs every `.html`
in the checkout rather than reading a named target list, because the page this
shipped on would not have been on a hand-maintained list, and it fails loudly on
zero blocks found. A scan of the repo before the fix found eighty-one JSON-LD
blocks across profiles, comparison pages, landing pages and tools, of which
exactly one did not parse, matching what Search Console reported. Harness
`tools/test_jsonld.py`, six assertions, plants the shipped defect on the page it
shipped on and the same defect in a city profile, so a future page cannot fall
off coverage silently.

After deploy, request validation in Search Console under Unparsable structured
data. The fix is invisible to a reader, so that round trip is the only
confirmation that matters.

### 2026-08-12 (second entry) - tax tool heading polish: scope moves to the counter

One-line copy change on `states-that-dont-tax-retirement-income.html`: the filter
H2 reads "Your rules, applied." and the counter line carries the scope, "Showing
N of the 39 states with a profiled retirement city", both numbers computed from
the array. A brand name mid-headline read awkward; scope reads naturally beside a
count. No data change, no board change (board date already 2026-08-12).

### 2026-08-12 - tax tool fixup: URL deep linking and heading scope

**Files:** edits to `states-that-dont-tax-retirement-income.html`,
`docs/DEPLOY-taxtool.md`, `docs/TASKBOARD.md`, this log. The first tool bundle
deployed before two improvements landed; this commit carries them. Filter state
now syncs to the URL query string both ways, making every filter combination a
shareable landing page (the canonical tag keeps variants one page for search),
and the filter heading reads "every state with a RetireMeHere city" so the
state count reads as scope, not omission. The operator's first phrasing for
that heading was rejected by the superlatives check, working as designed. No
DB change, no score change, no validator change.

### 2026-08-11 (fourth session) - the tax filter tool ships

**Files:** new `states-that-dont-tax-retirement-income.html` and
`tools/test_taxtool.py`. Edits to `tools/validate.py`, `sitemap.xml`,
`where-can-i-afford-to-retire.html` (one cross-link), `docs/TASKBOARD.md`, this
log. No DB change, no score change, no city figure change.

**What it is.** The reason the whole tax thread existed: a filter over the State
Tax Facts sheet. Five checkboxes (no income tax, Social Security not taxed,
retirement withdrawals not taxed, no estate tax, no inheritance tax) and two
sliders (property tax, sales tax) against every state with a city in the
database. Surviving states render as cards carrying the enum chips, the note
prose from the sheet, and city chips with each city's D5, linking through the
standard `index.html?city=` route. Checkbox semantics are strict: the box means
the state does not tax it for anyone, so Partial states are excluded when a box
is checked and explain themselves in the note when it is not. Filter state
syncs to the URL query string in both directions, so every filter combination
is a shareable deep link and a Pinterest pin can land on its exact answer;
the canonical tag keeps the variants one page for search. Counts on the page
are computed from the arrays; the copy carries no numbers that can rot.

**Plumbing.** The page is a clone of the calculator's shell (same header,
styles, footer, GA), with TAXFACTS and TAXCITIES embedded as generated JSON
between explicit end markers. `check_taxtool_data` joins the figures group
beside `check_afford_data` and holds the same promises: two-way rosters for
both arrays, every field and every note equal to its workbook cell, every city
D5 equal to its City Database cell, and loud failure when the page or arrays
cannot be read. Notes are compared as exact strings because the note is the
product. Seven planted errors in `tools/test_taxtool.py`, wired into the
harness group.

**Copy discipline.** Zero em-dashes; no dataset-scoped superlatives; the FAQ
answers explain mechanisms (estate against inheritance, what Partial means,
where the data comes from) without enumerating states or counts, so the prose
cannot drift against the sheet; the tax-year vintage renders from the data
rather than living in the copy.

### 2026-08-11 (third session) - Pennsylvania D5 unified at 7; methodology v1.1 (DB v19.1)

**Files:** new `docs/CityDatabase_Jul_27_v19.1.xlsx` (replaces v19, deleted). Edits to
`index.html`, `pick-and-compare.html`, `where-can-i-afford-to-retire.html`,
`docs/D5-TAX-METHODOLOGY.md`, `tools/validate.py` (DEFAULT_DB only), `docs/TASKBOARD.md`,
this log. One score change, operator approved: Philadelphia D5 from 6 to 7. No other
figure moved; the v19.1 workbook differs from v19 by exactly one cell, verified.

**Why.** The populated facts sheet surfaced the tension the July corrections missed:
Pennsylvania fully exempts retirement income, so the 5-6 band's "some retirement income
taxed" cannot hold Philadelphia's 6. Iowa at 8 is the in-set anchor (exempt income,
comparable property tax, no inheritance tax); Pennsylvania's inheritance tax is the
one-notch difference, landing the state at 7. The old one-point Philadelphia spread
rested only on a local sales-tax add-on no other state's cities are differentiated on.
Full rationale in `D5-TAX-METHODOLOGY.md` section 8.

**Surfaces.** Four carriers of the score moved together: the City Database cell, the
quiz CITIES array in `index.html`, the embedded array in `pick-and-compare.html`, and
the score array in `where-can-i-afford-to-retire.html`. The Philadelphia profile
carries no numeric D5 and its tax prose already tells the exempt-income story, so it
needed nothing. No comparison page includes Philadelphia.

**Methodology v1.1 shipped in the same commit.** Scoring a new state is now
"fill the facts row, then assign D5 from the row against the bands." The research
step and the scoring step were the same work done twice; the sheet is where it gets
written down once.

**Found and boarded, not fixed:** the Scores by Dimension sheet is a stale second
copy (89 rows against 99 cities, drifted values, nothing reads it). Boarded P2 for
delete-or-validate rather than silently patching one cell of it here.

### 2026-08-11 (second session) - State Tax Facts population pass (DB v19)

**Files:** new `docs/CityDatabase_Jul_27_v19.xlsx` (replaces v18, deleted). Edits to
`tools/validate.py`, `tools/test_taxfacts.py`, `docs/TASKBOARD.md`, this log. No page
changes, no score change, no city figure change. The date stamp stays Jul 27 for the
same reason as v18: the version is canonical, the date records city-figure vintage.

**What happened.** All thirty-nine state rows populated: income tax type and top rate
from the Tax Foundation's 2026 table, Social Security treatment from the 2026
eight-state list (six of ours: CO, MN, MT, NM, UT, VT), combined sales tax from the
Tax Foundation midyear 2026 table, estate and inheritance status from 2026 reporting
(estate: MA, MD, ME, MN, NY, OR, VT, WA; inheritance: KY, MD, PA), retirement income
treatment classified per row with the mechanism in the Note column. Tax Year 2026 on
every row. One correction against the named source of record: South Carolina's 2026
reform (Act 110, signed March 2026, retroactive to January 1) replaced the bracket
system with 1.99 and 5.21 percent, so SC carries 5.21, not the pre-reform 6.0 in the
Tax Foundation's February table.

**Classification rule worth recording.** Retirement Income Treatment is Exempt only
when relief is broad (no income tax, or a blanket exemption like PA and IA); Partial
requires relief that reaches private pensions and IRA money; government-pension
carve-outs alone do not earn Partial, or nearly every state would qualify. Nuance
lives in the Note column, never in the enum.

**The blank tolerance is retired.** `check_taxfacts` now fails any blank enum,
numeric, Note, or Source cell, and bounds Tax Year to 2025 through the current year.
Two new planted-error assertions hold the retirement in place. No wall-clock aging
of Tax Year: staleness is the annual June rebuild's job per the Section 2 calendar,
matching how every other vintage check anchors to DB_VERSION_DATE rather than today.

**D5 reconciliation.** Ran facts against every state's D5. Seven of eight raw flags
dissolve on the rubric's own offset language (AZ's 8 is the "taxed at a low rate"
band verbatim; MD, ME, NY are held down by local income taxes and death taxes; DE 9,
ID 7, NC 7 are the documented tolerated spreads). Pennsylvania is the one live
tension, boarded for an operator decision. No scores moved in this commit.

### 2026-08-11 - State Tax Facts schema shipped (DB v18)

**Files:** new `docs/CityDatabase_Jul_27_v18.xlsx` (replaces v17, which is deleted)
and `tools/test_taxfacts.py`. Edits to `tools/validate.py` and `docs/TASKBOARD.md`.
No page changes, no score change, no city figure change.

**What happened.** The tax filtering tool needs discrete state-level facts, and D5
cannot supply them: it is a composite, and no composite answers "does this state tax
Social Security" with a yes or a no. So v18 adds a State Tax Facts sheet, one row per
live state, keyed on ST: income tax type, top rate, Social Security treatment,
retirement income treatment plus a note column, combined sales tax, property tax
rate, estate and inheritance tax, tax year, source. Enum columns carry closed
vocabularies so a filter can run on them; nuance goes in the note column.

**Populated now: the ST keys and the PropTax mirror only.** Property tax was already
in the City Database at one value per state, so the mirror ships live and
`check_taxfacts` fails the moment the two copies disagree. Every other column is
blank until the population pass, which is its own session and must add the
completeness check when it lands. Blank until then is deliberate: the alternative
was populating from research inside a schema session, and data entered in a hurry
next to data entered carefully ends up indistinguishable from it.

**The version stamp.** v17 to v18 with the date kept at Jul 27, per section 5 of
this log: the version number is canonical, the date is informational, and the date
records the vintage of the city figures, none of which moved. Bumping the date would
have failed every comparison caption for no reason.

**Coverage is strict in both directions and that is the design.** A state with a
city and no facts row fails the gate, so a new state's facts arrive with its first
city, fresh, rather than pre-loaded and rotting unread. A facts row without a city
also fails, so speculative rows cannot accumulate. Front-loading the eleven missing
states was considered and rejected: rows nothing reads are where this site's worst
defects have hidden.

### 2026-08-10 (third session) - last stray quiz CTA repointed

**Files:** `pick-and-compare.html`, `docs/TASKBOARD.md`, this log. No new pages, no
database change, no score change.

**What happened.** The batch earlier today repointed forty-one body quiz CTAs to
`where-should-i-retire-quiz.html`. It matched on `class="quiz-cta-btn"`.
`pick-and-compare.html` styles the identical button as `class="cta-btn"`, so it was
never matched and kept sending readers to `index.html`.

**How it surfaced, which is the part worth keeping.** Not by re-reading the batch, and
not by grepping for the old href, which would have returned the header buttons and the
landing page's own CTA as false positives. By taking the set of pages with a header
quiz button and the set of pages linking to the landing page and diffing them:
forty-three against forty-two, one page in the gap, and the gap named the page. A
batch that keys on a class name silently skips every page that styles the same element
differently, and the only reliable check is on the property that matters, which is
whether a link exists, not whether a selector matched.

**Also fixed.** That page's CTA copy said the quiz takes three minutes. The landing
page and every other CTA say two. The repoint would have sent readers straight from
one number to the other.

**Decided, not deferred: the header buttons stay on `index.html`.** All forty-three.
The case for repointing them was link equity to the page that ranks. It does not hold
up: forty-two of the forty-three already link to the landing page from their body CTA,
and a second link from the same page to the same target adds little. So the gain would
have been new equity from one page, bought with an extra click for every reader who
presses a header button expecting the quiz to start. Recorded here so it is not
reopened from first principles in three months.

### 2026-08-10 (second session) - where-can-i-afford-to-retire.html shipped

**Files:** new `where-can-i-afford-to-retire.html` and `tools/test_afford_data.py`.
Edits to `tools/validate.py`, `sitemap.xml`, `index.html`,
`where-should-i-retire-quiz.html`, `best-places-to-retire-on-a-budget.html`,
`docs/TASKBOARD.md`, this log. No database change, no score change. Counts unchanged
at fifty-one profiles and twenty-three comparison pages.

**What it is.** An affordability calculator built on BUDGET-METHODOLOGY.md section 14,
the equity-adjusted variant added earlier the same day. The reader gives home equity, a
monthly budget, and whether they are buying or renting. Cities that come in at or under
the budget are shown, ordered by their combined score across nine dimensions: all of
them except D2 Budget, which is excluded because cost is already the filter and
counting it twice would push a cash-rich reader toward cheap housing for a mortgage
payment they are not making. Static
prose sits above the tool so the page has something to index; the hero anchors straight
down to the calculator.

**The rule that shaped the design.** Section 14.2: the equity-adjusted figure is a
filter and never a sort key. Principal and interest is the largest and most locally
variable line in the budget, so taking it out flattens the differences between cities
and a cost ranking at high equity puts the expensive resort town on top. The page
filters on cost and ranks on scores, and the reason is written into the script comment
next to the sort so that a future edit has to argue with it rather than not notice it.

**Verification before hand-off.** The page's own JavaScript was extracted and run
against the database in Node: it reproduces the published `Monthly Est` string and
`Budget Range` integer for all ninety-nine cities with zero mismatches. Ranges of
equity and budget were exercised across the input space, including both ends, and
checked for cities silently dropping out through a missing state multiplier. None do.

**One ambiguity in section 5, settled by the data.** The utilities line reads "baseline
$400/mo per couple, multiplied by a state cost-of-living modifier" and then lists
climate adjustments, without saying whether the adjustment lands before or after the
multiplier. Applying the modifier to (400 + adjustment) disagrees with the published
`Monthly Est` on six cities: Palm Springs, Fort Collins, St. Louis, Knoxville,
Bentonville and Tulsa. Adding the adjustment after the multiplier reproduces all
ninety-nine exactly. The latter is correct and is now asserted by
`check_afford_data`. Section 5 should get a clarifying clause at the next
methodology-doc audit. Done in this commit: section 5 now states the order explicitly.

**Second copy of the database, defended.** The page embeds Median Home, the property
tax rate, the insurance estimate, two climate fields and ten scores per city, because
section 14.4 requires run-time derivation and a personalised figure cannot be
precomputed. `check_afford_data` asserts roster, cells, the page's constants against
section 6, and finally that the formula rebuilds the published column from the page's
own inputs. `tools/test_afford_data.py` plants one error of each kind and asserts each
is caught.

**Not an orphan on day one.** The August 10 first-session finding was that the quiz
page had exactly one reference to it in the whole repo, its own canonical, and reached
Google through the sitemap alone. This page ships with links from `index.html` header
and mobile navigation, the quiz page, and the budget landing page.

**Known limits, stated on the page rather than hidden.** Renting uses the published
mortgaged figure and ignores equity, per section 14.3, because a landlord does not
lower rent when a reader sells a house and the database has no rent column. Single
retirees are overestimated by roughly $300 a month. HOA fees are excluded and the
omission grows proportionally as equity rises.

### 2026-08-10 - SEO and funnel session, five pushes, no new pages

No page built, no database change, no score change. Counts unchanged at 51 profiles and 23
comparison pages. This session was diagnostic first and the edits followed from the data.

**Files:** edits to `index.html`, `privacy.html`, `sitemap.xml`, `visit-before-you-decide.html`,
`tools/validate.py`, five guide pages, forty-one pages carrying a quiz CTA,
`where-should-i-retire-quiz.html`, `docs/TASKBOARD.md`, this log. New:
`tools/test_canonicals.py`.

**Duplicate URLs, and the half that was already defended.** All forty-five root pages already
carried self-referencing canonicals pointing at the `.html` form, which is why Netlify serving
both `/foo` and `/foo.html` never cost more than fifty-seven impressions in total. `index.html`
carried none, and the site links to it as `index.html?city=NAME&state=ST` in 471 places across
ninety-eight distinct query strings, plus bare `index.html` three hundred times and `/` two
hundred and fifty-six. Up to a hundred URLs serving byte-identical homepage HTML with nothing
declaring which was real; two were already indexed. Same defect class as the extensionless
variants, roughly twenty times the surface, invisible because the landing pages happened to be
right. `check_canonicals` now reads the page list from `sitemap.xml` and asserts each page's
canonical equals its own `<loc>`, so a page and the sitemap can no longer disagree silently.

**Netlify Pretty URLs: checked, inert, left alone.** The checkbox is ticked but the parent Asset
optimization section is off, confirmed by loading a `.html` URL and watching it stay. A redirect
block enforcing the `.html` form would work today and become an infinite redirect loop on every
landing page the moment Asset optimization were ever switched on. Not worth that exposure to
recover fifty-seven impressions the canonicals already handle. **Decision: no redirect block, now
or later, unless the URL form itself changes.**

**affiliate-policy.html, found by the new check on its first run.** In the sitemap since
2026-06-26 and linked from `visit-before-you-decide.html`, but the file has never existed. A 404
served to readers and advertised to Google. The disclosure paragraph on that page is itself
complete: partner names, that a commission is earned, that it costs the reader nothing. Only the
trailing "read our full affiliate policy" pointer was dead. Link and sitemap entry removed;
writing the page remains open.

**Guide titles.** All five ran sixty-eight to eighty-six characters against Google's roughly
sixty-character cut, so each was clipped mid-descriptor with a brand name occupying the opening
twenty. `active-frontier.html` ranks position 5 for "best cities for retirees" and converted at
2.4% against roughly 6% typical for that position. Descriptive phrasing moved to the front on all
five; every URL left untouched, so nothing could lose a ranking. og:title and twitter:title kept
in sync on the three pages that carry them.

**Query data killed a planned edit, correctly.** `urban-walkabout.html` shows 924 impressions at
position 8.32 with one click. Its query report is dominated by Walk Score lookups for specific
cities (Winter Garden FL, Cedar Rapids, Melbourne FL, Cohasset), none of them in the database.
Google is matching the page to a question it cannot answer, which is not a title problem and not
recoverable by retitling. One row in that report, "walkable cities for retirees" at position 37,
is the actual audience. Retitled toward that rather than toward the phantom impressions.

**Results screen.** Of 193 quiz completions in twenty-eight days, six requested a report. The
offer was not broken; it was ignored. Three causes, all structural: the restart bar sat between
the city cards and the offer and read as end-of-page; all five reports rendered every time with
ten controls; and `getRecommendedReports()` already personalised but only added a badge without
reordering, so a recommended report could sit fourth of five under a heading asking the reader to
choose. Recommended now sort to the top, the remainder collapse behind a toggle, the restart bar
moved below. A `reports_expand` event was added so the next read can separate placement from offer.
`report_request` still fires on actual email submission, so the number stays comparable to the six.

**Internal links.** See TASKBOARD for the orphan finding. Forty-one quiz CTAs repointed. Nav and
footer links deliberately left on `index.html`: site-wide repeated links are discounted anyway and
rerouting them would tax every on-site visitor. Existing anchor-text variation across those
buttons was preserved rather than normalised.

**Two hardcoded city counts** removed from `where-should-i-retire-quiz.html`, which claimed the
quiz ranks "100" cities in two visible sentences while the FAQPage schema on the same page already
said "every city on RetireMeHere" correctly. Visible prose had drifted from the structured data it
mirrors, which is the failure mode already recorded here: prose restating a checked number is
itself unchecked and drifts independently.

### 2026-08-08 (sixth push) - fayetteville-vs-bentonville-retirement.html shipped

Shipped after the Saratoga Springs profile the same day, so all counts below are post-Saratoga:
51 profiles, 23 comparison pages.

**Files:** new `fayetteville-vs-bentonville-retirement.html`; edits to
`compare-retirement-cities.html`, `cities/fayetteville/profile.html`,
`cities/bentonville/profile.html`, `sitemap.xml`, `docs/TASKBOARD.md`, this log.
No database change, no score change.

Twenty-third comparison page. Both DB rows re-derived from
`docs/CityDatabase_Jul_27_v17.xlsx` at the start of the session per section 4a; nothing was
inherited from the COMPARE brief.

**The ledger.** D2 budget 8 against 6 is the only dimension gap clearing the two-point bar. D1, D4,
D5, D7, D8 and D10 are level. D3 and D6 favour Fayetteville by a point, D9 favours Bentonville by a
point; all three are near-ties and ship unmarked, per the two-point rule. Cost rows carry three
marks to Fayetteville (home value, monthly estimate, budget tier) on clear differentials. Property
tax and insurance are identical figures and ship unmarked. The climate block ships entirely
unmarked, because Jan mean, snowfall, sunshine and heat severity are identical across both cities.
Four checkmarks on the whole table is the honest result of the pairing, not a build shortfall.

**The structural decision, recorded because it was raised.** The brief proposed cutting the
five-block tradeoff narrative to three on the grounds that a pairing this tight cannot support five
tradeoffs. The premise was wrong and no override was taken. `COMPARISON-PAGE-STANDARD-v2` item 4 is
not five tradeoffs; it is a fixed arc of five named blocks, two of which ("What they share", "The
honest shared downside") are explicitly about similarity and become easier to write, not harder, as
dimensions converge. The page ships with all five. Anyone tempted to reopen this on the next tight
pairing should read item 4 before reading the argument.

**Three flags carried in from the brief were stale and are closed.** (1) The affiliate-codes
spreadsheet no longer lists Fayetteville AR under state code AK; the row reads AR and there are
zero AK rows. Nothing to correct. (2) The brief stated that neither profile mentioned the other. In
fact each already referenced the other substantively as metro geography: Fayetteville's profile
points readers to Crystal Bridges thirty minutes north, Bentonville's points to Washington Regional
thirty-five minutes south. What was genuinely missing was the reciprocal comparison CTA, which is
gated by `check_comparison_cta_reciprocity` and could not have shipped without it. (3) The hub was
at twenty-two pages, not twenty-one.

**Slug resolution confirmed rather than assumed, and it paid for itself.** `Fayetteville` and
`Bentonville` lowercase cleanly onto their slugs, so `check_comparison_scores` and
`check_comparison_cost_rows` genuinely ran on this page. That mattered: the first gate run failed
four times on cell formatting inherited from `burlington-vs-portland-me`, which was used as the
reference build. The monthly cells carried `&ndash;` and the checkmarks carried `&#10003;`, and
neither entity form is normalised by `_cost_row()` or `_dashes()`. The reason the reference build
carries them and passes is that `portland-me` does not resolve, so that page is the ONE page of the
23 on the hub that these two checks silently skip. The new page ships with the literal en dash and
the literal tick character.

Three consequences boarded as P1: the skip has a measured size (one page, not many); the same
lookup has a worse second mode, where Wilmington DE and Wilmington NC collide on one key so a
future wilmington page would be validated against the wrong row rather than skipped; and fixing the
slug resolution will immediately surface two real cost-row failures on
`burlington-vs-portland-me`, which should be fixed in the same commit so the gate does not look
like the slug fix broke something.

**Boarded, not fixed:** the Wilmington slug collision, and a `Climate Hot Sum` inconsistency
between two cities thirty minutes apart with identical heat severity. Both are in TASKBOARD.

### 2026-08-08 (fifth push) - Saratoga Springs NY profile (51)

Profile fifty-one. Built from live `cities/st-louis/profile.html`, non-NRC, so the callout and
its CSS were stripped. Three photos: Saratoga Race Course (Joshua Adams, Unsplash) as hero,
Congress Park (Tyler A. McNeil, Wikimedia Commons, CC BY-SA 4.0, crop offered under the same
licence) as the portrait detail, Saratoga Lake with Snake Hill (Peter Flass, Wikimedia Commons,
CC BY 3.0) as the lifestyle square. Two Lake George candidates were rejected: Lake George
village is twenty-five miles north and is not this city, and one of the two carried an Unsplash
geotag naming Saratoga Springs for a photograph that plainly shows Lake George.

Three lists carry Saratoga cards already, all live rather than coming-soon, so no landing page
needed editing: arts lovers, natural disasters, LGBTQ retirees. Three list cards, so
`lists-grid` rather than `lists-grid-four`.

Corrections riding along, all found in the ranked-brief step and all silent to the validator:
`index.html` highlight and `pros[0]` claimed a perfect ten on community against a database
eight, `pick-and-compare.html` carried the same highlight, the `culture_walkable` pairings
block carried `s1: 10`, and `value-navigator.html` badged Range three against a database
Budget Range of four.

Open item boarded, not fixed: database Median Home for Saratoga Springs is $663,000 against a
late-June 2026 Zillow ZHVI of $618,681. The profile displays the database figure per the
data-source rule.

### 2026-08-08 (fourth push) - check_budget_labels shipped; the P0 is closed

**Files:** new `tools/test_budget_labels.py`, `tools/validate.py`, `docs/TASKBOARD.md`, this log.
No site change. Push two of two on the budget-label P0.

Push one fixed the quiz budget labels. This stops them rotting again. `check_budget_labels` asserts
that BUDGET_BANDS exists and parses; that there are exactly five bands numbered one to five with
five distinct labels; that the numeric edges ascend, do not overlap and leave no gap with the top
band open-ended; that each label's upper figure names the next band's floor rather than its own
max; and that the boundaries still sit where the database puts them. That last one is recomputed
from Monthly Est at run time. A check holding its own copy of the five strings would have been a
fourth copy of the thing that broke and would have passed forever while the database moved
underneath it.

**The harness found a hole in the check before either shipped, and this is the entry's real
content.** `tools/test_budget_labels.py` plants eleven defects. On the first run, ten passed and
one failed: the assertion that `renderBudget()` still reads the constant was satisfied by the
constant's name appearing in a COMMENT inside that function, so replacing the actual loop with an
empty array still passed. A check written specifically to close a silent-pass hole had a smaller
silent-pass hole inside it, and no amount of reading it would have shown that. Fixed by stripping
comments before the membership test.

The generalisable point, and the reason the no-check-without-a-harness rule exists: **a check
cannot test itself, and reviewing a check tells you what it was intended to do rather than what it
does.** The only way to know a check can fail is to make it fail. Ten of eleven passing on the
first attempt is roughly the hit rate to expect, which means roughly one in eleven checks shipped
without a harness is decorative.

**The database assertion encodes a policy on purpose.** The bands derive from the midpoint of each
range's Monthly Est span, not the low end, because the candidate filter already grants one range of
deliberate stretch and low-end labels would stack a second on top of it. The low-end set originally
specified on the board is planted in the harness as a defect that must be rejected. If that
decision is ever reversed the gate will fail until someone edits the check deliberately, which is
the intent: a policy argued out once should not be reversible by quietly editing five strings.

**A note on the per-city test that was NOT written.** Asserting that every city's Monthly Est
midpoint falls inside its own band would fail on correct data today: five of ninety-nine cities sit
within fifty dollars of a boundary (Fayetteville, Knoxville, St. George, Charlottesville, Boulder),
because Budget Range is not a pure function of the midpoint. The check tests the boundaries against
the MEDIAN midpoint of each range instead, which separates cleanly and moves slowly. A check that
fires on its own correct input gets loosened rather than fixed, and a loosened check is how the
original defect survived a clean gate for weeks.

**The suspension is lifted.** The growth-versus-debt split resumes. Next build is Saratoga Springs
NY, then fayetteville-vs-bentonville.

### 2026-08-08 (third push) - scoring rubric converted to markdown; D4 restored

**Files:** new `docs/SCORING-RUBRIC.md` (v3.3), `docs/TASKBOARD.md`, this log.

`scoring_rubric_v3_2.docx` lived in project knowledge and never in the repo, with no version
history, in breach of section 4a. Converted to markdown, committed to `docs/`, version bumped to
3.3 because the content changed. **The `.docx` must now be deleted rather than kept.** A superseded
copy left in place is the two-copies condition 4a exists to prevent, and it reads as authoritative
to anyone who opens it.

**The find that justifies the version bump: the rubric documented nine of the ten dimensions the
site scores.** v3.2 stated that "the standalone D4 dimension has been retired because it duplicated
information already captured in monthlyEst and budgetRange, and was not used by the matching
engine", and carried no D4 section. Every clause of that was true when written and none of it is
true now. D4 is `D4 Resil.` in the database, scored one to nine across all ninety-nine cities with
a written rationale each; it sits in the `DIMENSIONS` array in `index.html` as "Climate Resilience
& Insurance" where the reader sets it as a priority like any other dimension; and it takes a full
priority weight in the match calculation. The old D4 was a daily-cost sub-score and was genuinely
retired into D2. The slot was later reused for resilience and the rubric was never revisited.

**This is the same defect class as the budget labels, one week apart, and that is the point.** A
governing document described a surface that had moved underneath it, and nothing in the toolchain
compares the two. The budget labels were caught because a reader would eventually have hit them.
The D4 gap would not surface that way at all: the quiz behaves correctly, the scores are real, and
only someone scoring a new city against the written standard would find that the standard has no
entry for a dimension worth up to four times weight. **The generalisable rule: when a slot is
reused for a new concept, the retirement note for the old concept becomes a false statement about
the new one.** Retiring something and reusing its identifier are two separate edits and the second
one is the one that gets skipped.

**Also reconciled.** The rubric's budget ranges read Range 1 as under $3,500 per month, an empty
set against a database whose cheapest city starts at $3,800, and matched nothing rendered anywhere.
Replaced with the five bands now in `BUDGET_BANDS`, carrying the derivation, the
midpoint-not-low-end reasoning and the label-rounding convention. That closes item four of the P0
fix spec, which could not ship in the first two pushes because the file was not in the repo.

**Three further drifts were flagged inline rather than silently fixed**, because each needs a
decision rather than an edit: the symmetric budget-bonus table in the rubric versus the asymmetric
bonus actually implemented in `index.html`; D4 having no published band anchors at all; and
dimension names differing between the rubric and the quiz on D6 and D8. All boarded.

### 2026-08-08 (second push) - budget band labels rounded

**Files:** `index.html`, `docs/TASKBOARD.md`, this log. Display copy only.

The five band labels shipped this morning read `$5,500-$6,499`, `$6,500-$7,499`, `$7,500-$8,999`.
Rounded to `$5,500-$6,500`, `$6,500-$7,500`, `$7,500-$9,000`. Operator call, on readability: a
column of figures ending in 499 and 999 is harder to scan than round hundreds, and this is the
highest-leverage question in the quiz.

The numeric `min`/`max` fields on `BUDGET_BANDS` were NOT changed. They remain exact and
non-overlapping, because they are the assignment math and the thing the guard will assert. Only
the `label` string moved. The split is now explicit in a comment above the constant so that a
later reader does not see the one-dollar disagreement and "correct" it back.

**The trade, recorded so it is not relitigated.** Display and edges now disagree by one dollar at
each seam. A reader stating exactly $6,500 sees it named in two bands. At a boundary the two
adjacent bands admit result sets one range apart, and the reader knows better than the quiz does
whether they sit above or below their own stated figure. The precision that was lost was false
precision: it implied the bands know something about $6,499 that they do not.

**Consequence for push two.** `check_budget_labels` must assert each label's upper figure against
the NEXT band's `min`, not against its own `max`. Written that way the rounding is legal and a
genuine mis-set band still fails. Written the obvious way, it fails on correct data on day one.
Worth stating because a guard that fires on its own correct input gets loosened rather than fixed,
and a loosened guard is how the original defect survived.

### 2026-08-08 - budget-label P0 fixed (push one of two)

**Files:** `index.html`, `docs/TASKBOARD.md`, this log. Push one of two; the guard is push two.

The quiz budget question rendered three byte-identical options. Fixed. `BUDGET_BANDS` is now a
single module-level constant in `index.html`, read by `renderBudget()` for the Step three buttons
and by the results prose for the "your budget fits here" line. The local `BUDGET_LABELS` array
inside `renderBudget()` is gone and `BUDGET_OPTIONS` is deleted rather than repaired.

**The spec was overridden on which statistic to derive from, and this is the part worth keeping.**
The board called for the database `Budget Range` LOW-END bands. `Monthly Est` is a range, and its
low end is the cheapest month a city ever has. The candidate filter already grants one range of
deliberate stretch, commented as such at the filter. Deriving the labels from the low end puts a
second, undocumented stretch on top of the first, and the two compound in the same direction. A
reader stating $6,200 would have selected Range three, admitting every Range four city, Boulder
among them at $8,000-$10,000 per month. Shipped instead on midpoints: `Under $5,500`,
`$5,500-$6,499`, `$6,500-$7,499`, `$7,500-$8,999`, `$9,000+`.

The generalisable form: when a label set maps a reader's single number onto a stored range, name
which statistic of that range the mapping uses, and check whether any other stage of the pipeline
is already applying slack in the same direction. Two stages each granting a reasonable-looking
stretch produce an unreasonable one.

**A correction to yesterday's entry.** That entry called the results-prose set "directionally
right and internally consistent; still approximate." It is not approximate. It is the midpoint
bands, derived correctly and rounded at the seams. The correct set had been in the file the whole
time, twenty lines from the broken one, in the surface nobody looks at. The defect was never a
missing derivation. It was two copies, one of which was never filled in past its first and last
slots, and no gate that could tell.

**Checked while in there.** All ninety-nine rows of the `CITIES` array were compared to v17 on
`budgetRange` and `monthlyEst`. Zero mismatches on either field. Worth recording because the
reader-facing filter runs on the `CITIES` copy, not on the database, so a drift there would have
been a second silent defect behind the first one.

**Found while fixing, P1:** `scoring_rubric_v3_2` is not in `docs/` under any filename. The only
copy is a `.docx` in project knowledge. Same shape as the `MEDIAN-HOME-AUDIT-REFERENCE` gap in
section 4 above: a governing document outside the repo, no version history, in the place 4a
forbids. Boarded to convert to markdown, commit, reconcile its budget ranges to the shipped bands,
and delete the outside copy. Item four of the original fix spec cannot ship as a repo edit until
that happens.

**Still open, push two:** `check_budget_labels` with its planted-error harness, asserting the
midpoint bands, recomputed from the database at run time rather than hardcoded. Until it ships,
nothing in the toolchain reads quiz option labels, which is the condition that let this run live
under a clean gate for an unknown length of time.

### 2026-08-07 (second entry)

**Budget-label defect raised P2 to P0 (OPS).** Board only. No site change: `index.html` was not
touched, and the defect ships live until the fixing BATCH. Files: `docs/TASKBOARD.md`, this log.

`renderBudget()` in `index.html` renders the quiz budget question from a local `BUDGET_LABELS`
array whose middle three entries are byte-identical strings. Three indistinguishable buttons,
each setting a different `quizState.budget`, which drives a hard candidate filter, the
alignment bonus and the over-budget penalty. Three different result sets behind three buttons a
reader cannot tell apart, on Step three of four of the primary conversion path.

Correct bands already exist twenty lines below as `budgetLabels` in the results prose, so the
quiz array was never filled past its first and last slots. `BUDGET_OPTIONS` near line 6352 is
dead code with the same defect and is marked for deletion rather than repair. Neither set is
derived from the database; the fix spec on the board derives one set from the v17 low-end
bands, writes it once, and references it from both surfaces.

**Two process notes worth keeping.**

First, the original P2 grade was wrong and the reason is generalisable. The item was boarded
from the rubric-versus-database disagreement, which is real, and the rendered quiz was never
opened. A doc-versus-data mismatch and a live broken control look the same from the
spreadsheet. When a doc and the data disagree about a field, open what the reader sees that
field through before setting a priority.

Second, the validator read 0 failures 0 warnings across every run in this session, including
the pre-deploy gate for the Fayetteville profile, while this sat live. Nothing in the toolchain
reads quiz option labels. `check_budget_labels` is specified on the board with a planted-error
harness required before it ships, and with zero matches defined as a failure, per the
no-silent-no-op rule.

**Priority consequence:** this outranks the Wave one and Wave two profile queue. The
growth-versus-debt split is suspended until the fixing BATCH ships.

### 2026-08-07

**Fayetteville, AR profile shipped (BUILD).** 50 profiles live. Files: new
`cities/fayetteville/{profile.html,hero.jpg,detail.jpg,lifestyle.jpg}`; edits to `index.html`
(PUBLISHED_PROFILES plus eleven copy corrections), `sitemap.xml`,
`best-places-to-retire-on-a-budget.html`, `docs/TASKBOARD.md`, this log.

Built from live `cities/st-louis/profile.html`. Not an NRC city, so the Neighborhood Reality
Check callout and the `.reality-check` CSS were both stripped; the `lists-grid-four` rule inside
the shared media query was kept.

Judgment calls, all overridable:
1. No dimension reaches nine. The hero tagline and opening character paragraph carry all four
   eights rather than leading with one. The skill has no tuning for this shape.
2. Stat card four is Outdoors ("40+ trail mi") over Community, because the D2 figure is already
   spent on two cards and the Greenway is the asset Fayetteville owns rather than borrows.
3. Healthcare card uses "425 beds" per the deployed Prescott pattern rather than a hospital name.
4. Crystal Bridges is attributed to Bentonville everywhere it appears, in body copy and in the
   `index.html` D10 note, rather than being folded into Fayetteville's own culture claim.
5. Lists section ships with one card. Precedent is live Prescott.

Photos: all three from Brandon Rush via Wikimedia Commons. Hero (Square, poppies) and lifestyle
(Razorback Greenway at Lake Fayetteville) are CC0. Detail (534 Willow Avenue, Washington-Willow
Historic District) is CC BY-SA 3.0, so the crop is offered under the same licence and that is
stated in both the photo credit and the footer. Detail crop carries a 2.7% upscale, inside the
ten percent ceiling. Four candidate images were rejected before these: two were Burlington VT,
one was a three-megapixel University of Arkansas frame that could not make the portrait spec
without a thirty percent upscale, and one was a lower-resolution Willow Avenue shot.

Affiliate codes confirmed by the operator before build and checked for collisions against all
live profiles: expedia `iSurfAX`, vrbo `32xKR9x`.

### 2026-08-07 - comparison cross-link rule retired, board hygiene boarded

**What shipped.** One governing-doc edit and three board items. No HTML changed, no database
change, no scoring change. Gate clean at 0 failures, 0 warnings.

**The retired rule.** `COMPARISON-PAGE-STANDARD-v2` item 6 required every comparison page to link
to ALL other live comparison pages, and required updating every existing page whenever a new one
shipped. Three findings, in the order they mattered:

1. The rule had already expired on its own terms. Its text ended "until the hub page exists".
   `compare-retirement-cities.html` exists, lists all 22 matchups, and is linked from all 22
   comparison pages. The condition it was waiting on was met and nobody went back to close it.
2. It was never followed at scale. Measured: 1 to 4 outbound links per page across 22 pages. No
   page has ever carried 21.
3. The practice that replaced it is better. A curated 2-to-4 set of related matchups is
   navigation; 21 undifferentiated pills are a wall.

Replaced with the curated pattern and the reasoning kept inline so it does not get reinvented.
The general lesson, worth more than this instance: a rule nobody follows is not neutral. It is a
trap for whoever reads the doc literally and does the wrong work carefully. Retiring it is the
change; documenting why is what stops it coming back.

**Priority raise, not a new item.** The `check_docs` profile-count anchor went P4 to P2. It was
already boarded on August 3 by the knoxville-vs-asheville build. I proposed it in the Burlington
session as though it were new, without grepping the board first, which is precisely the failure
the board exists to prevent and would have produced two entries for one defect. Raised because
the Burlington build had to hand-work around it and every future build now has to remember the
same workaround.

**Board split boarded, not done.** 40% of `TASKBOARD.md` is closed-work archive, and every
shipped item is recorded three times across the board ladder, the board's CLOSED sections, and
this log. Boarded as a P2 with the explicit warning that the split does not fix the count anchor,
because a third of the historical counts live in the front matter and would survive it.

### 2026-08-06 (second push) - burlington-vs-portland-me shipped

**What shipped.** One new comparison page at `burlington-vs-portland-me-retirement.html`,
plus the hub card and JSON-LD ItemList position twenty-two, the sitemap entry, COMPARE THESE
CTA blocks on both profiles, the board and this entry. No new photo assets: both profiles are
published, so og:image points at the Burlington hero and the two profile cards carry lazy
thumbnails. No database change and no scoring change. Gate clean at 0 failures, 0 warnings on
a fresh clone with the package applied.

**Baselines re-derived, not trusted.** Live main was pulled and both rows re-read from
`docs/CityDatabase_Jul_27_v17.xlsx` before anything was drafted. Burlington: Range 3, Monthly
Est $6,000-$7,500/mo, Median Home $520,000, PropTax 1.51%, HO insurance $1,063/yr, D1 6, D2 5,
D3 8, D4 7, D5 3, D6 7, D7 9, D8 7, D9 7, D10 8. Portland ME: Range 3, Monthly Est
$5,900-$7,300/mo, Median Home $571,000, PropTax 0.98%, HO insurance $1,335/yr, D1 8, D2 5,
D3 9, D4 8, D5 4, D6 9, D7 7, D8 6, D9 4, D10 9.

**The page's actual finding.** Burlington's house is cheaper by $51,000 and costs more to hold.
Property tax on the two medians is about $7,852 against $5,596, so Burlington runs about $2,256
a year higher there; insurance runs the other way by $272; net about $1,984 a year, roughly $165
a month. That lands almost exactly on the Monthly Est gap, so the database is internally coherent
and neither figure should be "corrected" against the other. The page states explicitly that
property tax and insurance are already inside Monthly Est, because counting them additively is
the double-count that shipped once before.

**Judgment call one: the two headline cost rows ship unmarked.** Burlington wins median home,
Portland wins Monthly Est, budget tier ties at three. Marking each on its own row would have
split a single axis into two competing verdicts, and a lone median-home mark to Burlington would
assert "Burlington is cheaper" on a page whose own property-tax row says otherwise. The monthly
ranges overlap almost entirely ($6,000-$7,500 against $5,900-$7,300), so that gap is not a clear
differential under the standard either. Property tax and insurance ARE marked, one to each city,
because each of those rows is unambiguous within itself; that is what puts the inversion in the
table rather than only in prose.

**Judgment call two: the climate figure rows ship unmarked.** January mean, snowfall and sunshine
all favour Portland, by four degrees, eight inches and eight points. Climate rows keep the context
rule rather than the two-point rule, and marking all three would have read as a climate sweep on
differences that are real but modest. The prose says plainly that Portland is milder on every
figure and still not mild.

**Judgment call three: the page stays off Climate Warm W.** W has Portland at two against
Burlington's three, meaning the model rates Portland's winter as the harsher, while the Jan-mean,
snowfall and sunshine rows printed in the same table all say the opposite. Prose built on W would
have contradicted the page's own figures, which is exactly what `check_comparison_prose_scores`
exists to catch. The page uses the plain figures. The W row itself is boarded for an OPS look and
was NOT changed here.

**Validator gap found while building, boarded P1.** `check_comparison_scores` and
`check_comparison_cost_rows` both build their city lookup by lowercasing the DB city name and
replacing spaces with hyphens, which yields `portland` and never `portland-me`. The page slug is
`portland-me`, so `by_slug.get(b_slug)` returns None and both checks hit `if not a or not b:
continue` and skip THE WHOLE PAGE, Burlington's cells included. Neither reports anything; both
count as clean. This is the silent-no-op shape the rest of this validator refuses by design, and
it will apply to every future state-suffixed slug, not just this one. `check_comparison_checkmarks`
is unaffected because it reads only the table markup. Every figure on this page was verified
against the database by hand in place of the missing coverage. The fix belongs in an OPS pass:
resolve through `slug_to_city`, which already carries `portland-me`, and fail rather than
`continue` when a slug cannot be resolved.

**Doc debt, boarded P3, not done here.** Architecture item six of `COMPARISON-PAGE-STANDARD-v2 .md`
requires every new comparison page to add pill links to all other live matchups "until the hub page
exists". The hub exists and no live page carries the full set; every one carries a curated handful.
The rule is dead in practice and live in the doc, and following it literally would mean editing
twenty-one files for no reader benefit. It should be struck from the standard.

### 2026-08-06 - Burlington VT shipped as profile 49

**What shipped.** One new city profile at `cities/burlington/profile.html` with hero, detail and
lifestyle photos, plus the `PUBLISHED_PROFILES` routing entry, the sitemap entry, four corrected
Burlington figures in `index.html`, the board and this entry. No database change and no scoring
change. Gate clean at 0 failures, 0 warnings on a fresh clone with the package applied.

**Baselines re-derived, not trusted.** Live main was pulled and every figure re-read from
`docs/CityDatabase_Jul_27_v17.xlsx` before anything was written: Range 3, Monthly Est
$6,000-$7,500/mo, Median Home $520,000, PropTax 1.51%, HO insurance $1,063/yr, D1 6, D2 5, D3 8,
D5 3, D6 7, D7 9, D8 7, D9 7, D10 8, D4 Resil. 7.

**Emphasis brief, MULTI-STRENGTH.** One pillar (D7 Outdoor 9) over a cluster at 8 (D3, D10) and
7 (D6, D8, D9). Under the skill's advisory the profile leads with the pillar but gives the
cluster real weight in the character section, because a single-pillar city written to its pillar
alone reads as one trick. D5 Tax 3 is the only hard flag and leads the "No if" column.

**Judgment calls, all reversible.**
1. No Neighborhood Reality Check. Retiree-target towns bracket the $520,000 citywide figure
   (South Burlington ~$485K below it, Shelburne and the Hill Section above), which is section 4's
   "adds noise rather than clarity" case rather than the St. Louis case.
2. Stat slot four went to healthcare on a D3/D10 tie at 8, on the reasoning that retirees weight
   healthcare hardest and D10 already carries the character section and a list card.
3. The healthcare stat card states "Level I trauma" rather than a bed count. UVMMC bed counts in
   public sources run 481, 562 and 620 depending on what is being counted, and a contested number
   has no business being a headline fact.
4. Lists section shows four of five live placements. Best Places to Retire and Avoid Natural
   Disasters was dropped because Burlington sits in that page's second-tier bucket on the back of
   the July 2023 flooding, while hikers, arts, foodies and LGBTQ retirees are all top-tier. The
   card stays live on that page.

**Four figures corrected in index.html.** Property tax read 1.42% on three surfaces against a DB
PropTax Rate of 1.51, and the D2 scoreNote read a $506K citywide median attributed to Redfin
against a DB Median Home of $520,000. The Redfin attribution was dropped with the figure: an MLS
median sale price and a ZHVI typical value are different measures and should not be swapped under
one source line. Corrected in the same commit as the profile so the surfaces cannot disagree.
Worth recording: correcting the highlight in `index.html` alone FAILED the gate, because
`pick-and-compare.html` carries its own copy of the same string and `check_figures` compares them.
The check caught a half-finished fix that would otherwise have shipped as a new inconsistency.

**One conflict deliberately left open.** DB `Ann Snow in` is 70; `index.html` says approximately
80; the NOAA normal is about 81. The profile uses 70 per the data-source rule, and the DB cell is
boarded as a P2 rather than quietly reconciled, because editing live copy down to match a suspect
database cell propagates the error instead of finding it.

**No landing-page edits.** All seven Burlington cards were already live `city-card` links, five
on landing pages and two on guides, none of them coming-soon, so `check_cards` had nothing to
promote. Burlington is Range 3, so the budget-page roster predicate does not reach it.

### 2026-08-03 (second push) - knoxville-vs-asheville shipped, growth cycle boarded

**What shipped.** One new comparison page at `knoxville-vs-asheville-retirement.html`, wired from
both city profiles in the same commit, plus the hub card, ItemList position 21, the sitemap entry,
the three-week growth cycle boarded in full, and two corrections found while in the files. No
database change, no scoring change. Gate clean at 0 failures, 0 warnings on a fresh clone.

**Baselines re-derived, not trusted.** Live main was pulled and every number re-read from
`docs/CityDatabase_Jul_27_v17.xlsx` before anything was written. Two board assertions were wrong:
"Live profiles: 47" against a real 48, and the memory of Portland ME as an unbuilt Wave 1 city when
it shipped July 29. Both corrected. This is the argument for re-deriving rather than reading the
board: the board is a record of intent and drifts from the repo between sessions.

**The cycle plan was untracked for a week.** It was drafted at the end of the CTA-reciprocity
session and never committed, so the 80/20 split, the three rules, the wave order and the week-1
indexing gate all governed real work while living nowhere. Reconstructed onto the board in full.
The wave order as boarded puts Burlington VT ahead of Fayetteville AR, which inverts score order,
71 to 67, because that is the order the builds are actually happening in.

**The Traverse City line is a reconstruction, flagged as such.** Traverse City MI at 73 is the
highest-scoring unbuilt city and is on no wave. The repo records no reason anywhere. The reason
boarded, that it has no live pairing partner and so unlocks zero comparison pages, is consistent
with the cycle's own logic but was supplied here, not recovered. Overwrite it if the real reason
was different.

**Editorial finding worth keeping: a wide dimension gap is not always a quality gap.** D3 reads
Knoxville 8, Asheville 5, and the obvious sentence to write is that Asheville's hospital is weak.
It is not. Mission Hospital is US News seventh in North Carolina, high performing in seventeen
adult procedures, and a Healthgrades top-50 hospital eleven years running. What Asheville lacks is
a second system, while Knoxville carries UT Medical Center and Covenant Health Parkwest ranked
first and second in the metro independently. Mission's real weakness is on a different axis: two of
five stars for patient experience and a February 2024 CMS immediate jeopardy finding, since lifted.
The score is right; the obvious explanation for it was wrong.

**Containment caught in draft.** The money block wanted to add the $166 a year insurance advantage
to the $500 a month budget advantage. `BUDGET-METHODOLOGY.md` section 4 puts insurance inside the
monthly estimate, so those do not add. Same defect as bloomington-vs-lexington, caught before
publishing this time rather than in a later audit. The page now says so explicitly.

**Airport route counts softened on purpose.** McGhee Tyson's own site publishes two different
counts on two pages, 25 and "more than 30", while independent trackers say 41. The page uses "more
than thirty", the airport's own conservative figure, true under every source. Asheville Regional
publishes 26 across five airlines consistently and is stated exactly. The standard's rule is
verify against the airport's own figures or soften; it does not cover the case where the airport
disagrees with itself, and softening is the safe reading.

**Also corrected.** The hub carried "let the quiz score all 100", a hardcoded city count that
`check_hardcoded_counts` cannot see because its pattern requires the word "cities" after the
digits. Replaced with count-free language. No matchup count was restored to the hub: the July 31
chat deleted it rather than correcting it, and that remains the right state.

**Two P4s boarded.** Two climate-row conventions are live across the comparison pages, and
`check_docs` is reading a line-wrapped `48` in July 29 prose as its profile-count anchor rather
than the "Live profiles:" line. Both are in the board.

---

### 2026-08-03 (first push) - comparison CTA reciprocity

**What shipped.** Fifteen CTA edges added across twelve city profiles, one new check, one new
planted-error harness, and two doc updates. No database change, no scoring change, no new page.
Gate clean at 0 failures, 0 warnings on a fresh clone.

**What was actually broken.** Eight of the twenty live comparison pages could not be reached from
either profile they compare. The board carried this as an eight-page item; enumerated against the
repo it is fifteen missing edges over twelve profiles, because one page was already half-wired and
three profiles appear in two matchups. Size by grepping, never by the board number, holds again.

**The half-wired state is the one that hides.** `nashville-vs-memphis` was linked from Memphis and
not from Nashville for four days and read as finished from whichever end you opened.
`santa-fe` and `scottsdale` were worse: both had a populated head-to-head section linking Tucson,
so the slot looked filled while the edge between the two of them did not exist.

**Editorial, not mechanical.** Each block carries a one-sentence tradeoff blurb written from the
database rather than from the comparison page it links, since a comparison page is a derived
surface. Five blocks carry two rivals and use the two-button flex row from the Tampa canonical.
One blurb claim was cut in draft: naming taxes as a Fort Collins against Boulder tradeoff, where
both cities are Colorado at D5 7. An axis with no gap on it is the prose version of a checkmark on
a tie.

**`check_comparison_cta_reciprocity`.** Asserts that every hub-listed page is linked from both
profiles its filename names, and that every comparison href on a profile points at a page that
exists. The second direction is the rename case, which nothing else on this gate reads. The check
shipped with a bug its own harness caught: the first draft used a bare substring test for
`href="/page"`, which `data-href="/page"` satisfies, so it would have passed on markup that links
nothing. The boundary fix is in, and the assertion that found it stayed in the harness.


### 2026-07-31 (eighth push) - hardcoded counts, prose scores, data vintage

**What shipped.** Two new checks, one rewritten check, one new surface helper, three planted-error
harnesses, and 40 content edits across 15 files. No database change, no scoring change, no new page.
Gate clean at 0 failures, 0 warnings on a fresh clone.

**The count.** 23 live instances of the adjectival "100-city" (and two of "99-city") across 11
files. `check_hardcoded_counts` had been shipped and passing throughout, blind three ways: its
regex knew only "100 cities", its page set excluded the comparison hub itself, `pick-and-compare`
and the quiz, and no text surface on the site read meta description attributes. All three closed.
`pick-and-compare.html` line 920 was the worst single instance: wrong count, stale version "(v14)"
against v17, and hidden by the hyphen. The hub's `og:description` and `twitter:description` claimed
"Nineteen honest head-to-head matchups" against a real twenty.

**Prose scores.** `check_comparison_prose_scores` asserts that a score restated in prose matches the
table row it restates, set-equal, on comparison pages only. It found two more live instances while
being written, `madison-vs-columbus` and `scottsdale-vs-tucson`, taking the run to eleven in four
days with D2 the offender in all eleven. The binding is adjacency, not proximity: a window-based
first cut flagged 219 claims, nearly all of them a neighbouring dimension in the same list.

**Data vintage.** `check_comparison_vintage` asserts the caption month and the schema
`dateModified` are not older than `DB_VERSION_DATE`, a new constant beside `DEFAULT_DB` that
self-checks against the database filename. Eleven captions and twelve dateModified values were
behind. The rule was already written in COMPARISON-PAGE-STANDARD-v2 and had been missed by hand
twice.

**The pattern across all three.** Every one of these was a convention that existed only as prose in
a governing doc, and every one drifted within weeks of being written down. The check is the
convention; the doc is the explanation.

### 2026-07-31 (seventh push) - Tier 2 batch B; the comparison cost-figure repair is complete

**What shipped.** The last three comparison pages repaired against `CityDatabase_Jul_27_v17.xlsx`,
plus the removal of the scaffolding the repair needed: `COST_ROW_BASELINE` is now empty, and
`CTA_COST_DEBT_BASELINE` and `check_comparison_cta_cost_debt` were deleted in the same commit, as
that function's docstring asks at zero debt. `check_comparison_cost_rows` remains as a plain
assertion. No new files, no database change, no scoring change. Gate clean at 0 failures, 0
warnings on a fresh clone.

**What moved.** Naples $585,000 to $549,000, Fort Myers $372,000 to $310,000, widening that gap
from $213,000 to $239,000 and 36% to 44%. Sarasota $462,000 to $413,000 against the same Naples
figure, $123,000 to $136,000, with its 25% surviving at 24.8%. Nashville $460,000 to $437,000 and
Memphis $195,000 to $147,000, from $265,000 to $290,000 and 58% to 66%. Every monthly range moved.
No ordering inverted.

**Four more live D2 prose errors, taking the run to nine in four days.** Naples vs. Fort Myers
carried three mutually contradictory versions of the same budget claim across four surfaces, none
matching its own table. Nashville vs. Memphis understated Memphis at 7 when v17 has it at 10, a
perfect score. D2 is the offender in all nine, which continues to trace to the July 13 D2 rebuild
landing on table rows and not on prose.

**A figure that was never right.** Naples vs. Sarasota claimed a monthly gap of "roughly $1,300"
that was $700 to $900 before this repair and is $800 to $900 after it. The value matches the gap on
Naples vs. Fort Myers and appears to have been carried across when the page was built from that
template. The quarantine list could not have surfaced it: derived, in prose, and wrong from the
start.

**Correction to batch A.** The caption data-vintage bump required by COMPARISON-PAGE-STANDARD-v2
was missed on all three of its pages, and stale `dateModified` values with it. Corrected here across
all six Tier 2 pages. That rule has now been missed by hand twice, on Tier 3 and on Tier 2, and is
boarded to be gated.

### 2026-07-31 (sixth push) - Tier 2 batch A, three comparison pages rewritten

**What shipped.** Three comparison pages repaired against `CityDatabase_Jul_27_v17.xlsx`, with both
validator ratchets lowered in the same commit: `COST_ROW_BASELINE` from 24 mismatches over six pages
to 12 over three, and `CTA_COST_DEBT_BASELINE` from 7 to 5. No new files, no database change, no
scoring change. Gate clean at 0 failures, 0 warnings on a fresh clone.

**What moved.** Sarasota $462,000 to $413,000 and Tampa $400,000 to $380,000, narrowing that gap
from $62,000 to $33,000. Knoxville $368,000 to $377,000 and Nashville $460,000 to $437,000, from
$92,000 to $60,000. Chattanooga $328,000 to $324,000, which against the new Knoxville figure WIDENS
that gap from $40,000 to $53,000. Every monthly range moved except Knoxville's floor. No price
ordering inverted.

**Sizing, again by grepping.** Twelve table cells were quarantined; 82 figure surfaces carried the
figures. The copies nothing reads: Article schema descriptions, `meta name="description"`, hero
taglines, verdict boxes, a tradeoff HEADING that carried the gap in its text, and the profile-card
blurbs at the foot of each page.

**Two live prose errors, both D2.** Sarasota vs. Tampa claimed a 6-to-5 budget split in three places
against a table and a database that both say 6 and 6. Knoxville vs. Chattanooga claimed "budget
scores 9 against 8" against two 8s. The D2 column is the repeat offender in every instance of this
defect class so far, because the July 13 D2 rebuild landed on the table rows the check reads and
never touched the prose copies it does not.

**Four dataset-scoped claims.** Two visible on Knoxville vs. Chattanooga, "the midpoint of our
100-city database", and one in each Knoxville page's Article schema, "from a 100-city retirement
database". Banned by the superlative rule and wrong on the count. The hyphenated form is invisible
to `check_hardcoded_counts`; it is on three further files and is boarded with them.

### 2026-07-31 (fifth push) - checkmark rule settled, written, and gated

**What shipped.** No new comparison page and no figure change. Twenty-two checkmarks
removed from eight pages, one added, five captions and five table sub-heads brought onto
the current template, one wrong score corrected in prose, the rule written into
`COMPARISON-PAGE-STANDARD-v2`, and `check_comparison_checkmarks` shipped with
`tools/test_comparison_checkmarks.py` behind it. Gate clean at 0 failures, 0 warnings on
a fresh clone. Database unchanged: `CityDatabase_Jul_27_v17.xlsx`.

**The rule.** On dimension rows D1-D10, a cell is marked only where the score gap is two
points or more, the mark sits on the higher score, and shading and the literal tick
character always travel together. Cost rows are out of scope, having no score gap.
Climate rows keep the older clause in the standard that allows a marked 9 vs. 10 with
inline context, because readers feel that one and the numbers alone do not say so.

**Why it diverged.** Not two competing rules. Five pages never got the caption update the
other fifteen got, kept saying "ties are left unmarked" where the rest say "ties and
near-ties", and their tables correctly followed their own captions. The July 31 Madison
edit was defensible against that page's stale caption and wrong against the site.

**What measuring added that the board did not have.** `naples-vs-fort-myers` was
UNDER-marking a two-point D2 gap, so the check asserts the rule in both directions.
`santa-fe-vs-tucson` carried a prose score of "Santa Fe's 6" against a table and a
database that both say 5. All 200 dimension cells otherwise agree with v17, including
the D4 and D10 rows that were invisible to `check_comparison_scores` until the label fix,
and shading/tick parity is clean on every page. The two clean audits are now asserted so
they stay clean.

**Boarded, not fixed.** Cost-row and climate-row marks are inconsistent by a different
measure and nothing gates them; a cost row needs a percentage threshold nobody has
written. And the standard is filed with a space in its filename,
`COMPARISON-PAGE-STANDARD-v2 .md`, which is why several sessions concluded it contained
no checkmark rule: it was never opened.

### 2026-07-31 (fourth push) - bloomington-vs-lexington rewritten, Tier 1 complete

**What shipped.** One comparison page rewritten, plus both validator ratchets lowered in the same
commit: `COST_ROW_BASELINE` from 27 mismatches over seven pages to 24 over six, and
`CTA_COST_DEBT_BASELINE` from 9 to 7. No new files, no database change, no scoring change. Gate
clean at 0 failures, 0 warnings on a fresh clone. **Tier 1 of the cost-figure repair is complete**;
everything left is Tier 2.

**The only Tier 1 gap that narrows.** Bloomington $296,000 to $321,000, Lexington $333,000 to
$337,000, so the housing gap closes from $37,000 to $16,000, and Bloomington's monthly estimate
rose enough to halve the monthly spread from $200 to $100. Every other page in this repair had a
gap widen or invert.

**The page was counting the same money twice, and had been before the rebase.** Tradeoff #2 and
FAQ 3 both presented the monthly advantage and the insurance advantage as separate savings that
combine into a lower all-in cost of ownership. BUDGET-METHODOLOGY.md section 4 lists homeowners
insurance as a housing line item of the monthly estimate, at HO Insur Est / 12, so Bloomington's
$1,155 a year insurance advantage is already inside the $1,200 a year its monthly figure shows,
and is very nearly the whole of it. Adding them turned a 2% monthly difference into a decisive
one. Corrected in both places, with the arithmetic written onto the page.

**Defect class worth carrying forward:** a published derived figure that is a COMPONENT of another
published derived figure on the same page. Nothing in the toolchain knows which figures contain
which, so any page that totals up a cost advantage can do this silently. Several do total one.

**The checkmark rule is now measured, and yesterday's Madison edit was wrong.** Across all twenty
comparison pages, eleven leave every one-point score gap unmarked, four mark them, and three are
internally inconsistent. The captions diverge the same way: most say "ties and near-ties are left
unmarked" while madison-vs-ann-arbor says only "ties are left unmarked". The Madison edit followed
its own caption and moved that page away from the site majority. Boarded as a P1 to revert, with
the two-point rule to be written into COMPARISON-PAGE-STANDARD-v2, the seven off-convention pages
brought into line, and a gate added.


### 2026-07-31 (third push) - madison-vs-ann-arbor rewritten

**What shipped.** One comparison page rewritten, plus both validator ratchets lowered in the same
commit: `COST_ROW_BASELINE` from 32 mismatches over eight pages to 27 over seven, and
`CTA_COST_DEBT_BASELINE` from 11 to 9. No new files, no database change, no scoring change. Every
figure read from `CityDatabase_Jul_27_v17.xlsx`. Gate clean at 0 failures, 0 warnings on a fresh
clone.

**What moved.** Madison $413,000 to $435,000, Ann Arbor $489,000 to $541,000, so the housing gap
goes from $76,000 to $106,000. Both monthly ranges moved, turning a $200 difference into $400 at
the low end and $500 at the high. Ann Arbor crossed into budget tier 3 while Madison stayed at 2.

**Why it needed prose work and not a swap.** Tradeoff #2 opens by listing five things the two
cities share, and the budget tier and the monthly estimate are two of the five. The same claim sits
in FAQ 2 in visible copy and in FAQPage schema, and tradeoff #3 said the money "gets more even"
after the house. All of that is now false. Unlike the San Antonio pairing the direction never
inverted, so the page's argument held and four sentences were rewritten rather than the premise.

**A checkmark defect predating the rebase, fixed here.** The page declares its rule twice: the
stronger city in each row takes the mark, ties are unmarked, with no score-gap threshold. It was
under-marking against its own rule, leaving `D2 Budget` unmarked at Madison 6 against Ann Arbor 5
and the monthly row unmarked while the figures differed. Both are marked now, as is the tier row
that has stopped being a tie.

**Boarded, because two versions of the checkmark rule are in circulation.** This page's caption
says stronger-city-wins. Working notes from an earlier comparison pass say marks only at a
two-point gap, and `st-louis-vs-kansas-city` was reasoned about that way on Jul 30. Under one rule
this page was under-marked; under the other its D4 and D9 marks are wrong. Nothing in the toolchain
reads a checkmark, so neither version is enforced. Settle it, write it into
COMPARISON-PAGE-STANDARD-v2, audit all twenty pages, then gate it.


### 2026-07-31 (first push) - san-antonio-vs-fort-worth rewritten

**What shipped.** One comparison page rewritten, plus `COST_ROW_BASELINE` lowered from 35
mismatches over nine pages to 32 over eight in the same commit. No new files, no database change,
no scoring change. Every figure read from `CityDatabase_Jul_27_v17.xlsx`, and every neighborhood
figure re-checked against the two city profiles rather than sourced fresh. Gate clean at 0
failures, 0 warnings on a fresh clone.

**The price ordering was backwards, not stale.** The page had San Antonio at $320,000 against Fort
Worth's $300,000. Under v17 San Antonio is $251,000, so it is $49,000 cheaper and a full budget
tier lower, with a monthly estimate $300 to $400 lighter. The board had sized this page by the
magnitude of the gap change, +145%, which is correct and does not convey that every sentence
ordering the two cities on price now says the opposite of the truth. Worth carrying into the
remaining Tier 1 pages: check the sign, not only the size.

**A second error, unrelated to the rebase.** FAQ 1 claimed five exact dimension ties including
budget. San Antonio scores D2 8 against Fort Worth's 7, which the page's own scored table states
correctly twelve lines above. `check_comparison_scores` reads the table row and not the paragraph,
so both passed. This is the second batch running in which prose restating a checked number was the
thing that had drifted, after the Asheville tier claim in Tier 3.

**The neighborhood argument was already right.** Both bands and all nine neighborhood figures were
current against the profiles, so tradeoff #3 and FAQ 2 kept their substance and only their opening
premise changed. The bands still overlap almost exactly, which means the page's conclusion holds
on better reasoning than before: San Antonio's citywide advantage is a fact about the territory
each city averages over, not about what a retiree pays.

**One boarded FAQ-sync mismatch closed in passing.** Q2's schema copy wrote the neighborhood bands
long form and the visible copy wrote them short. Both now use the short form and normalise equal,
leaving six of the seven boarded Jul 30.

**A near-miss on the board, corrected in a follow-up commit.** This page tells the reader that
San Antonio's Safety score is built on retiree-target neighborhoods and Fort Worth's is not. That
looked like a fossil of the carve-out retired by MEDIAN-HOME-METHODOLOGY.md v1.2, and shipped in
`c20fd1f` as a new P2 saying the methodology was unsettled. It is settled: the Rubric v3.3 item
already records at divergence (5) that D9 remains neighborhood-scored by design and only the D2
grouping was retired. The page is correct, no rescore is implied, and the stale artifact is the
rubric .docx rather than any score. The board entry is corrected in the following commit. Cause
worth keeping: the board was not searched before a new item was written, which is how a duplicate
came to contradict a resolved entry.


### 2026-07-30 (eighth push) - st-louis-vs-kansas-city rewritten

**What shipped.** One comparison page rewritten, plus `COST_ROW_BASELINE` lowered from 39
mismatches over ten pages to 35 over nine in the same commit. No new files, no database change, no
scoring change. Every figure read from `CityDatabase_Jul_27_v17.xlsx`. Gate clean at 0 failures, 0
warnings on a fresh clone.

**Why a rewrite and not a swap.** The page was organised around the two cities costing the same.
Under v17 St. Louis is $192,000 citywide against Kansas City's $257,000, a $65,000 gap where the
page asserted $15,000, and the monthly estimates are $500 apart at both ends where it said $200.
Tradeoff #2 was headlined "The cost story: structurally identical", so there was no figure to
swap; the premise was the thing that was wrong.

**The claim was load-bearing on eleven surfaces.** The H3 and its opening sentence, the meta
description, both social card descriptions, the hero tagline, the verdict paragraph twice, and FAQ
1 and FAQ 2 in both visible text and FAQPage schema. Worth recording because the board sized this
page from its headline: the headline was correct about the defect and wrong about the size, the
same way Tier 3's quarantine count was.

**The neighborhood argument got better, not weaker.** It previously explained why a non-gap should
be ignored. It now resolves a real one: St. Louis' retiree neighborhoods run $420K to $575K
against a $192,000 citywide median while Kansas City's run $300K to $900K against $257,000, so the
citywide advantage does not survive into the neighborhoods retirees actually buy in. The NRC
convention on this page was already settled, "Typical home value (citywide)" plus named
neighborhoods, so no methodology decision was needed.

**Verified rather than assumed.** Checkmarks stay on St. Louis for both cost rows because it is
still cheaper on both. D2 stays unmarked at 9 against 8 under the two-point rule. FAQ visible text
and schema were rewritten together and normalise equal.

**CTA debt unchanged at 11.** Retiring a page from quarantine usually retires the profile CTA
edges into it. This one has none: neither city profile links to it, because it is one of the eight
orphans on the open P1. `cities/kansas-city/profile.html` still carries a comment describing this
page as not yet built.


### 2026-07-30 (seventh push) - Tier 3 comparison cost figures

**What shipped.** 184 figure edits across eight comparison pages, plus both validator ratchets
lowered in the same commit: `COST_ROW_BASELINE` from 69 mismatches over eighteen pages to 39 over
ten, and `CTA_COST_DEBT_BASELINE` from 21 to 11. No new files, no database change, no scoring
change. Every figure read from `CityDatabase_Jul_27_v17.xlsx`. Gate clean at 0 failures, 0
warnings on a fresh clone.

**Pages.** `asheville-vs-greenville`, `bend-vs-boulder`, `fort-collins-vs-boulder`,
`madison-vs-columbus`, `santa-fe-vs-tucson`, `scottsdale-vs-santa-fe`, `scottsdale-vs-tucson`,
`tampa-vs-st-petersburg`.

**30 quarantined mismatches, 184 actual edits.** This is the operational finding. The quarantine
count comes from `check_comparison_cost_rows`, which reads three table rows per page. Each of
those figures is restated three to fourteen more times on the same page, in prose, in visible FAQ
text, in the FAQPage schema, and in `og:description` and `twitter:description`. None of those
copies is read by any check. The lesson generalises past this batch: a baseline number describes a
check's coverage, not a defect's size, and using it to plan work will undercount by whatever the
check cannot see.

**Derived figures are copies of copies.** Six of the eight pages publish the home-price gap as its
own number, which no database column contains. Those were recomputed, not swapped. Every ratio
claim was re-derived as well; four came out unchanged and were left alone, which is why the diff
looks smaller than the audit.

**Three edits were not mechanical.** `asheville-vs-greenville` claimed "Asheville's tier 3" twelve
lines below a table row correctly reading `2 of 5`, a pre-existing error the cost-row check cannot
see because it reads the row that was right. `fort-collins-vs-boulder` published a percentage
computed on the wrong denominator, wrong before the rebase too, and was recomputed rather than
carried forward. `tampa-vs-st-petersburg` published a single-value monthly delta that is now a
range. All three are written up on the board.

**The batch broke a harness, and the harness was right to break.**
`tools/test_comparison_cost_rows.py` hardcoded the page it used for its ratchet assertions, which
Tier 3 released from quarantine. Every tier batch would have hit this. Both the page and its
expected values are now derived from `COST_ROW_BASELINE` and the database at run time, so the
remaining tiers can land without editing the test. A test pinned to the thing it watches fails on
the gate, and a failure on the gate invites editing the test rather than the code.

**Two Tier 3 pages did not meet the tiering criterion.** Tier 3 was defined as gap movement under
6%; `santa-fe-vs-tucson` moved 10.9% and `scottsdale-vs-tucson` 6.4%, because Tucson's median fell
while its pair partners rose. Both batched safely anyway, for a different reason: neither page
publishes a gap figure. Recorded because it changes how Tier 1 and Tier 2 should be sized.

**Open question closed.** The suspected uniform $100 monthly offset, which would have implied a
budget recompute rather than drift, is not there. The deltas run 0, +$100, +$200 and -$100 and
track each city's own median move. Ordinary rebase drift.


### 2026-07-30 (sixth push) - CTA cost-debt gate

**What shipped.** One new file, `tools/test_comparison_cta_debt.py`, and three edits to
`tools/validate.py`: a new check, its ratchet constant, and its harness registration. No content
change of any kind. No database change. Gate clean at 0 failures, 0 warnings on a fresh clone,
harness 7.

**Why a gate and not a fix.** Two repairs are open at the same time and they pull against each
other. The orphaned-CTA item wants CTA blocks added to roughly eleven profiles. The cost-row item
has 69 stale figures quarantined across eighteen comparison pages, being repaired in tiers. Doing
the first while the second is open wires new reader traffic into money the validator already knows
is wrong.

**Neither existing check could see it.** `check_comparison_cost_rows` reads the comparison page.
Nothing reads a profile's outbound links at all. Both checks would have stayed correct about their
own surface while the site got worse across the join between them, which is the coverage lesson
from the cost rows restated one level up: coverage is a property of each field, and now of each
edge, not of a page.

**Shape.** `CTA_COST_DEBT_BASELINE = 21`, failing in both directions. Up is a new CTA into
known-bad figures. Down means a page left quarantine and the constant is overstating the debt, so
it must be lowered in the same commit. The number falls on its own as tiers land, because deleting
a `COST_ROW_BASELINE` entry retires every edge into it: Tier 3 takes it from 21 to 11.

**Judgment call worth flagging.** The check gates DEBT, not linking. Adding a CTA to one of the
two comparison pages that were never quarantined still passes, so the orphaned-CTA batch is not
blocked outright, only steered. Two of the seven planted-error assertions exist to hold that line.


### 2026-07-30 (fifth push) - lists heading counts, Memphis comparison CTA

**What shipped.** Seven edits across six profiles: a corrected lists-section heading on
`chattanooga`, `lexington`, `tucson`, `memphis`, `pittsburgh` and `st-louis`, plus a rewired
comparison CTA on `memphis`. No new files, no database change, no scoring change. Gate clean at
0 failures, 0 warnings on a fresh clone.

**Both defects are self-description that nothing validates.** The lists heading spells its card
count in English ("Three lists where Memphis earned its place") while the truth is the number of
sibling `.list-card` anchors. The Memphis comparison block described its own target page as
"Coming soon" while that page had been live for weeks. In each case the page made a claim about
itself, the claim went stale, and no check in the toolchain reads the surface that carries it.
Both were found by reading a live page, not by a run.

**The canonical is the propagation path.** `cities/st-louis/profile.html` is the build template.
Its heading said "Three" over four cards, so every profile built or retrofitted from it inherited
the pattern. The Jul 14 `.lists-grid-four` batch corrected the grid class on four of these files
and did not look at the sentence above the grid. This is the second time a canonical defect has
reached the whole set (see 2026-07-29, stat-card labels): worth treating a canonical edit as a
site-wide edit by default.

**Wider finding, boarded not shipped.** A reciprocity sweep of all 20 live comparison pages
against all 48 profiles found 8 pages with no CTA link from either of the two cities they
compare. Wiring them needs a short tradeoff paragraph per profile, which is editorial work on
roughly 11 files, so it is boarded as its own batch rather than stacked onto a verified fix. Two
validator checks are boarded alongside it, `check_comparison_cta_reciprocity` and
`check_lists_heading_count`, each pending a planted-error test.


### 2026-07-29 (fourth push) - Portland, ME shipped as profile 48

**What shipped.** `cities/portland-me/profile.html` plus three photos, one line in
`PUBLISHED_PROFILES`, one `sitemap.xml` entry, and the board and log updates. No landing page
changed: all six Portland cards were already live `city-card` links routing through
`index.html?city=Portland&state=ME`, none marked coming-soon, none carrying a monthly range.

**The build is the first MULTI-PILLAR case since the rule was written down.** D3, D6 and D10 all
score 9. The skill's failure mode is a profile that latches onto whichever pillar writes the
prettiest sentence, which here would have been the food scene, and lets healthcare and
walkability fade into the body. Hero tagline and opening paragraph both carry all three.

**A `4` that needed both halves.** D9 Safety is 4, and the obvious sentence is "crime is a
problem". CrimeGrade actually splits: 28th percentile overall, property crime roughly 40% above
the national rate, violent crime BELOW it at the 84th percentile. Writing only the aggregate
would have been technically defensible and materially misleading for a reader deciding whether
to walk home at night. Both halves are on the page, property crime leading.

**No NRC, deliberately, and the reasoning is the reusable part.** Every NRC city so far has been
one where a cheap citywide figure hides expensive retiree neighborhoods. Portland inverts it: the
citywide $571,000 is already high, and the West End, the neighborhood most retirees picture, runs
roughly $554K, BELOW it. What moves the number is the town line, not the neighborhood, so the
point belongs in the method-callout. A note here would have added noise, which is the exact test
MEDIAN-HOME-METHODOLOGY.md v1.2 section 4 sets.

**Photo note.** The detail image is Portland Head Light, which is in Cape Elizabeth rather than
Portland. Kept because it is the signature image of Greater Portland and does double duty as the
honest-about-winter break, but Cape Elizabeth is named explicitly in both the caption and the day
card rather than left to imply otherwise. The Pexels credit `Ssorsch` is an account handle, not a
confirmed name; Pexels does not require attribution and `Szora / Pexels` on Knoxville is the
existing precedent for crediting a handle.

### 2026-07-29 (third push) - pensacola vs. fort myers: the money argument rebuilt

**What shipped.** 24 edits across `pensacola-vs-fort-myers-retirement.html` and one on
`compare-retirement-cities.html`. The boarded P0 plus four defects the board did not carry.

**The board called this an argument rewrite and it was right, but the interesting part is what
replaced the argument.** v17 closed the gap the page was built on: `$108,000` to `$41,000`, D2
8-vs-6 to tied at 7, tier 1-vs-2 to both Range 2, monthly floor `$600` to `$200`. The reflex is to
find a different row for Pensacola to win on. There isn't one: under the 2-point checkmark rule the
rebuilt table gives Pensacola a single mark (home value) against Fort Myers' four (D1, D3, D8, warm
winters). **The fix was to change what the money figure MEANS rather than to hunt for a substitute.**
`$41,000` stopped being Pensacola's saving and became Fort Myers' asking price, which turns
tradeoff #1 into the setup and tradeoff #3 into the itemised answer. Those two blocks had been
litigating the same premium against each other since the page was built; the rewrite is a better
page than the pre-v17 one, not a salvage of it.

**A rank that was never a rank.** The page claimed Lee Health "earns Fort Myers the #3 spot on our
Top Cities for Healthcare list", on three surfaces. `top-cities-for-healthcare.html` is TIERED and
alphabetical within tiers, and Fort Myers is the third card in **Tier 2**, not third overall. Someone
counted cards. The near-miss worth recording: the first replacement drafted was "sits in the top
tier of our healthcare list", which reads as a safe softening and is flatly false. **Softening an
unverified claim is not the same as verifying it**, and both drafts would have passed the gate,
because no check reads landing-page tier membership. Removed rather than reworded.

**A scoring column read backwards for as long as the page has existed.** The climate row labelled
`Hot summers (lower = milder)` is fed by `Climate Hot Sum`, which is SUMMER COMFORT: higher is
better, per the rubric and per the DB (Bend 8, Scottsdale 1). The label inverted it, so the table
implied Fort Myers had the milder summers while tradeoff #2, two screens down, correctly said
Pensacola did. The prose was right and the structured surface was wrong, which is the opposite of
the usual failure and the reason it survived: a reader who trusts the table never reaches the
contradiction. Fixed here, boarded for `st-augustine-vs-pensacola-retirement.html`, which carries
the identical label.

**Two guard gaps found, neither fixed here.** `check_comparison_scores` skips the D4 and D10 rows on
every comparison page, because `DIMS` holds the DB column names (`D4 Resil.`, `D10 Comm.`) and the
pages spell the rows out in full, so the prefix match returns None and the row is skipped silently.
And `check_hardcoded_counts` missed `"a 100-city retirement database"` in this page's JSON-LD,
because its pattern wants `100 cities` and not `100-city`: the same hyphen-variant gap already
boarded for `pick-and-compare.html`. Both boarded; a check change needs a planted-error test and
this chat was scoped to one page.

**Split closed.** The pillar page said Fort Myers `$310,000` while this page said `$372,000`. It was
carried on purpose since Jul 29 and is now closed on both sides.

### 2026-07-29 (second push) - bozeman 2015 anchor sourced

**What shipped.** Six edits to `cities/bozeman/profile.html`. The boarded P0 (a 2015 clause holding
today's figure), the "doubled" claim on three surfaces, and three unboarded stale items on the same
page.

**Where the number came from, and why it took a source rather than a guess.** Zillow ZHVI
city-level series, RegionID 44281, `2015-06-30 = $327,317` against `2026-06-30 = $733,959`. The
temptation was a readily-findable local-brokerage figure of about $300,000 for 2015. That is an MLS
median SALE price and ours is a ZHVI typical-value index, so putting them in one sentence would have
been the exact mixed-methodology comparison MEDIAN-HOME-METHODOLOGY.md prohibits, and it would have
read as sourced. **When a historical figure is needed, the series has to match the series already on
the page, not merely the city and the year.**

**Sourcing can move the argument in the direction you did not expect.** The paragraph claimed prices
doubled. The real multiple is x2.24, so the page was understating its own case on three surfaces.
The reflex when a claim cannot be verified is to soften it; here the correct move was to strengthen
it.

**Side benefit worth recording.** DB `Median Home` `$734,000` matches ZHVI `2026-06-30` at
`$733,959`, which pins the current DB's ZHVI vintage to June 2026. That resolves the open question
on the `best-places-to-retire-in-florida.html` table caption: "as of June 2026" is correct as
written and needs no change.

**A rebase can destroy a correct figure, not just fail to update one.** Git shows the pre-rebase
sentence read "The Bozeman of 2015 had typical home values near $325,000. Today it's near
$740,000", correct and stable since the profile was built. `cff99a6` replaced the FIRST money
figure in the paragraph instead of the one describing today. The mental model that a rebase can
only leave figures STALE is wrong: it can also overwrite a correct historical one with a correct
current one and leave no trace that anything was lost. All 45 profiles the rebase touched were
swept for the same shape and Bozeman is the only instance.

**The fix needed a validator change, and the shortcut was the wrong answer.** Restoring the sourced
2015 figure failed the gate: `check_statcard_faq` had an other-PLACE guard but no other-TIME guard,
so a correct historical value under a home-value noun read as a claim about today. The ninety-second
fix was to reword until the check could not see it, which works by removing the home-value noun and
therefore makes the figure invisible to every money check on the site. **When a correct edit trips a
check, the question is whether the check is wrong, not how to phrase around it.** Here it was
incomplete, and the guard that fixed it is nine lines.

### 2026-07-29 - v17 argument rewrites: Florida pillar and st-augustine

**What shipped.** 18 edits across two files, all editorial rather than mechanical.
`best-places-to-retire-in-florida.html`: the cheapest-FAQ on three surfaces (JSON-LD, visible FAQ,
`bestfor-why` card) plus all eight rows of the comparison table. `cities/st-augustine/profile.html`:
six cross-city figures in four places, plus three cleanups.

**The rule this batch is an example of.** When a data refresh moves a figure that prose ARGUES from,
the figure swap is the smaller half of the job. Both pages here would have published false claims in
accurate numbers if only the digits had been corrected: the Florida FAQ compared a budget gap that
v17 had closed to zero, and st-augustine claimed to sit under a Sarasota figure it now sits above.
Check whether a number is load-bearing before treating it as a swap.

**Scope decision worth recording.** The Florida comparison table was NOT part of the boarded item,
which named three prose surfaces. It was folded in anyway, because shipping the rewritten FAQ
against a stale table would have left the page contradicting itself three screens apart. Six home
figures and five Budget/D2 scores were stale there and no check reads that table.

**Provenance, and when not to relabel.** Two `CityDatabase v14` references in st-augustine were
treated differently. The cost-strip citation labels FIGURES (0.78%, $7,136) that verify against v17,
so it was relabelled. The related-city comment records a COMPUTATION, and recomputing it under v17
showed Miami now tying with Sarasota and St. Petersburg at distance 11, so relabelling would have
made a stale-but-true note into a current-and-false one. It was dated instead. A citation that
records how something was derived is not the same object as a citation that records where a number
came from.

### 2026-07-28 (third push) - `check_statcard_faq`: three profile surfaces brought under the gate

**What shipped.** `check_statcard_faq`, wired into the existing `profiles` group, plus
`tools/test_statcard_faq.py` with 16 planted-error assertions. Five harnesses now run on the gate.
It checks three things `check_profiles` never read:

1. **The abbreviated monthly stat card.** Derived from `Monthly Est`, compared after HTML entities
   are resolved. Entity handling is not tidiness: four profiles write the range as `&ndash;` and
   Savannah's card is correct, so a byte comparison reports it as drift.
2. **The variable score slots.** Fires only when the value is literally `N/10`, because the same
   labels carry free text on thirty slots (`Healthcare: Barnes-Jewish`, `Airport: 48 nonstops`). A
   score under a label that maps to no dimension is a FAIL, not a skip, so the next new label cannot
   arrive unwatched.
3. **Home figures in prose**, across profile body, the JSON-LD FAQ, and two structured regions.

**Three design decisions, each of which cost a wrong answer first.**

*The money token must end on a digit or K/M.* A class ending `[\d.,]+` matches `$314,000,` including
the sentence comma, which drags the same-clause guard a clause forward. That is exactly how St.
Louis's wrong figure hid behind an unrelated later mention of "suburbs".

*The hedge slot.* `PROSCONS_HOME` requires the noun and the figure to be adjacent. Profile voice does
not: "the typical home value in Salt Lake City is around $580,000" puts 28 characters between them.
Reusing the pros/cons matcher unchanged covered 13 of about 45 figures and reported a near-clean
surface.

*The other-place guard is bounded in BOTH directions,* to the same clause and to text before the
figure. Unbounded forward it excuses real drift; unbounded backward it stops seeing our own figure as
ours. Both St. Augustine's "$433,000 above Tampa's $400,000" and Fort Myers' "$310,000 against
Naples' $585,000" are our own correct figures, and a looser guard skips them and calls the surface
clean.

**The correction the sizing pass got wrong.** The July 27 board framed the method-callout as a noun
problem. It is a region problem. The first money figure in a `method-callout` or a `reality-check`
block is the citywide home value, always, verified across all 22 such blocks on the site. Three were
wrong, and **not one of the three is reachable by any home-value noun**, because Tulsa's two blocks
and Prescott's both open on the phrase "the $X figure". Tulsa is the one that matters: its
Neighborhood Reality Check was still built on `$194K` after the ZHVI rebase moved Tulsa 14.9% to
`$223K`, so the callout explaining the citywide figure was explaining the wrong number, on a profile
that shipped four days ago. The region walk also has to accept `aside`, not just `div`, because the
NRC is an `<aside>` and a div-only walk skipped it in silence.

**What it found, and what was fixed.** Against the pre-batch tree the check reports **36 failures**
and nothing else: 25 abbreviated monthly cards, 1 score slot (Pensacola's Budget Score tile reading 8
against a v17 D2 of 7), and 10 home figures. All 36 are fixed in this commit.

Fixed alongside them, and NOT reported by the check, because they are outside its scope by design:

- **Eight cross-city figures** the other-place guard correctly excuses but which are stale anyway.
  Fort Myers names Sarasota at `$462,000` (now `$413,000`, twice) and Naples at `$585,000` (now
  `$549,000`, four times). Pensacola names Delray Beach at `$341,000` (now `$342,000`), Fort Myers at
  `$372,000` (now `$310,000`), and its own entry price at `$264,000` (now `$269,000`). Every swap
  keeps its sentence true; each was re-verified after applying.
- **Three unanchored figures** found by hand only, sitting under no noun and in no region:
  `st-augustine` twice at `$432,000`, and `carlsbad` at `$1,481,000` against a DB `$1,388,000` and a
  `$1.39M` stat card in the same paragraph.
- **Prescott's spelled-out money.** It was the only profile writing `585,000 dollars`, three times,
  all in the JSON-LD and all stale, including a monthly top end of `7,400` against a DB `$7,500`.
  Normalised to the `$` form rather than teaching the token a spelled-out variant, which brings those
  sentences under `RANGE_RE` as well.

**What was deliberately not fixed, and why it is P0 rather than P4.** St. Augustine's comparison to
Tampa, Sarasota and Fort Myers is stale on three surfaces, and one of the three INVERTS under v17:
the page says it sits "under Sarasota's $462,000", and at `$433,000` against a Sarasota `$413,000` it
no longer does. Swapping the figures alone would publish a false claim in corrected numbers. Same
cause as the Florida pillar page: v17 collapsed a price ordering the prose was built on, and both
want one editorial pass. Bozeman is the other: it now states `$734,000` for 2015 and `$740,000` for
today, in a paragraph arguing prices doubled in a decade, and the 2015 figure has to be sourced
rather than guessed.

**Verification.** `python3 tools/validate.py --local .` on a fresh clone: 0 failures, 0 warnings,
five harnesses green including `tools/test_statcard_faq.py 16/16 passed`. The harness plants eight
errors and demands a failure, and plants seven things that look like errors and demands silence,
because on this surface the false positives are the hard part: a correct `&ndash;` range, free text
under a mapped label, another city's figure named before it, a wrong figure inside a hood-card, and a
range. The cross-city and unanchored fixes were re-verified by a separate scan after applying, since
the gate cannot see them.

### 2026-07-28 (second push) - P0 figure batch: 13 reader-visible figures; board triage scale adopted

**What happened.** An OPS chat scoped to building the profile stat-card + FAQ figure check ran a
draft of that check across all 47 live profiles before writing it, to size the job. The draft found
**44 figures that disagree with CityDatabase_Jul_27_v17** on surfaces no check has ever read. The
gate read 0 failures, 0 warnings over every one of them, because `RANGE_RE` recognises only the long
`$4,500-$5,600` money form and the abbreviated stat card is written `$4.5-5.6K/mo`.

**What shipped.** The 13 a reader can see and act on, and nothing else.

Ten abbreviated monthly stat cards, each off by $300 to $600 per month:

| City | Card read | v17 Monthly Est | Now |
|---|---|---|---|
| Carlsbad | `$10.9-13.6K` | $10,400-$13,000 | `$10.4-13K` |
| San Antonio | `$5.1-6.4K` | $4,700-$5,800 | `$4.7-5.8K` |
| Charlottesville | `$5.5-6.8` | $5,800-$7,300 | `$5.8-7.3` |
| Ann Arbor | `$5.6-6.9K` | $5,900-$7,300 | `$5.9-7.3K` |
| Charleston | `$5.6-7K` | $6,000-$7,400 | `$6-7.4K` |
| Salt Lake City | `$5.7-7.1` | $6,000-$7,500 | `$6-7.5` |
| Fort Myers | `$5.5-6.8` | $5,200-$6,500 | `$5.2-6.5` |
| Memphis | `$4.1-5.1K` | $3,800-$4,800 | `$3.8-4.8K` |
| Roanoke | `$4.4-5.4K` | $4,600-$5,700 | `$4.6-5.7K` |
| St. Louis | `$4.4-5.4K` | $4,100-$5,200 | `$4.1-5.2K` |

Three home figures, each contradicted by the same page elsewhere: San Antonio `~$320K` to `~$251K`
and St. Louis `~$235K` to `~$192K`, both in the `method-callout` at the head of Where to live;
Memphis `$195K` to `$147K` in the `hoods-intro`.

**The one to remember.** Carlsbad's `stat-sub`, rendered on the line directly beneath the wrong
figure, already read "Tier 5 - $10,400 to $13,000 a month". The card contradicted its own subtitle
on screen, roughly two centimetres apart, and had done so for as long as the card existed.

**CORRECTION, same day, third push: the count below is wrong.** It says 26 and the true figure was
31, because "twenty monthly cards off by exactly $100" was the $100 CLASS, not the remainder: 35
were wrong, 10 shipped as P0, so 25 monthly cards were left, not 20. The final number the check
reports is 36, higher again because the region rule added on the third push reaches four figures no
noun pattern could. Left standing rather than edited, because a change log that quietly corrects
itself is not a log. Original paragraph follows.

**What did not ship, and why.** The check itself, and the other 26 figures: twenty monthly cards off
by exactly $100, five home figures off by $1K to $9K, and Pensacola's Budget Score tile reading 8
against a v17 D2 of 7. All are real. None changes what a reader does. They are left in place on
purpose as the check's regression corpus, because hand-fixing them before the guard exists means
doing the work twice, and because a corpus of 26 known-wrong figures is the only honest way to prove
the check catches the class rather than the plants.

**Board triage scale adopted, and every open item ranked.** The second half of this push is
procedural. `docs/TASKBOARD.md` gained a `HOW TO RANK ANYTHING ON THIS BOARD` section defining P0
through P4 on one question, who is harmed and how fast, and all 34 open items now carry a rank
inline. Two rules attach: no board line without a rank, and only P0 may interrupt a city profile
build.

The cause it addresses is not a missing process, it is a missing field. Every finding was being
boarded with full reasoning and no priority, so a 1,100-line board presented a $100 rounding
difference and a nav copied into 87 files in the same visual weight. The operator reported the
predictable effect: every cleanup chat surfaced more work of unknown importance, and the queue felt
undifferentiated. Ranking is cheap, reversible, and restores the distinction the board was already
capable of making.

**Verification.** `python3 tools/validate.py --local .` on a fresh clone: 0 failures, 0 warnings,
four harnesses green. Note what that proves and what it does not: the existing gate passed before
this batch and passes after it, and could not have told the two states apart. That is precisely the
gap the P2 check closes.

### 2026-07-28 - Casper, WY profile (47); budget-page card promoted; NRC roster grep found leaky

**Built.** `cities/casper/profile.html`, cloned from the live St. Louis canonical rather than a
session copy, against `CityDatabase_Jul_27_v17.xlsx` row 85. Scores read from the DB only:
D1 4, D2 8, D3 6, D5 10, D6 3, D7 8, D8 6, D9 8, D10 6; Range 1; $4,800-$5,900/mo; $314,000;
PropTax 0.53%; HO insurance $2,075. Research supplied supporting colour only (Banner Wyoming
Medical Center bed count and ACS Level II trauma verification, CPR's single nonstop route,
Casper Mountain and River Trail mileage, Wyoming exemption mechanics).

**Emphasis.** One pillar (D5 Tax 10) plus a cluster of three 8s, which is the MULTI-STRENGTH
shape, so the tax fact leads the hero and the cluster carries the character section rather than
the profile riding a single hook. Both sub-5 dimensions (D1 Airport 4, D6 Walk 3) are named in
the No-if column, the airport first, since one nonstop route is the binding constraint.

**Two superlatives caught by the gate, not by eye.** A services card read "Casper ranks second on
the value list" and a JSON-LD FAQ answer read "the lowest of the five budget tiers used on this
site". Both are dataset-scoped and both were rewritten to anchor on figures. Worth noting that
they were written by someone who had read the policy immediately beforehand: the check is
carrying real weight, not duplicating care that already exists.

**No NRC callout.** Paradise Valley, the retiree-favoured side of town, prices at roughly $316K
against a $314K citywide figure, so neighbourhood selection does not move the budget here and a
callout would add noise under MEDIAN-HOME-METHODOLOGY.md v1.2 section 4. The unused NRC CSS was
stripped from the clone so the profile does not register in the roster grep.

**One process note.** The $314,000 figure was queried during the build against Zillow city-page
and Redfin city-median values and wrongly reported as a possible 15% error. Natrona County ZHVI
at 2026-06-30 is $314,485, which rounds to the DB value exactly; the mismatch was reading a city
figure against a county-based column. Nothing in the tooling raised it. Worth recording because
the docs do not state anywhere which geography the rebased column uses, so the same wrong
comparison is available to the next person who checks a figure by hand.

**Files changed.** `cities/casper/profile.html` (new), `index.html` (PUBLISHED_PROFILES),
`sitemap.xml`, `best-places-to-retire-on-a-budget.html` (coming-soon card promoted to a live
link at rank 2), `docs/TASKBOARD.md`, this log.

### 2026-07-28 - validator `layout` group: the hand-off shape is now checked

**Problem.** Every check in `validate.py` reads the CONTENT of a file whose path it already
knows. That leaves a whole class of fault unwatched: a file with the wrong NAME, in the wrong
PLACE, which no check has any reason to open. `DEPLOY-CHEATSHEET.md` section 4 has specified
the hand-off shape since Jul 14 (a zip of new files at final repo paths, plus
`apply-<city>.py` for edits to existing files), but nothing enforced it. A build chat
delivered the older shape three times between Jul 25 and Jul 28, loose `casper-profile.html`
and `casper-hero.jpg` to be renamed by hand at deploy time, and the gate read 0 failures
every time, correctly by its own lights.

The ways that ships wrong are all quiet: three photos renamed by hand at 11pm with one
missed, so a profile goes live with a broken image nobody sees until a reader does; the loose
copy left at the root beside the correct one, so a stray `-PROFILE.html` sits live and
unscanned, which is how a `scottsdale-vs-santa-fe` stray carried four banned superlatives
past `check_superlatives`; or a bundle zip committed because `rm` came after `git add`.

**Cause.** Not forgetfulness. Three documents described the hand-off shape and two were
stale. The one a build chat reads at step zero, `SKILL.md`, lives OUTSIDE the repo, so
neither section 4a nor the enumeration rule can reach it. It is the single document
guaranteed to be read on every build and the single document the currency machinery cannot
see. The project instructions have the same problem and still carry the old shape.

**Fix, two parts.** `check_stray_artifacts` plus `tools/test_stray_artifacts.py` (7 planted
assertions, both directions: strays present, and expected files absent, and a `cities/` that
yields nothing failing loudly rather than comparing an empty set). Local mode only, since a
bare run cannot list a directory over HTTP. And `SKILL.md` rewritten to delegate rather than
restate, with a table naming which repo doc owns which subject and an explicit rule that if
the skill and a repo doc disagree, the repo doc wins and the skill is the bug.

Three further stale claims in the skill were fixed while there: it described
`PUBLISHED_PROFILES` as a structured entry with `hospitalRating` and `scoreNotes` (that is a
different map further up `index.html`; the real one is a flat key-to-path map), it told a
build chat to run a `scripts/generate_brief.py` that is not bundled with no fallback, so the
ranking step could be skipped for want of a tool, and its photo section carried no EXIF
verification or licence-attribution guidance.

**Verified.** Reproduced the original mistake against the new check: `casper-profile.html`
and `casper-hero.jpg` dropped at the root of a clean checkout produce 2 failures naming both
files and pointing at section 4. Full gate 0/0 with four harnesses.

**Limit worth stating.** This catches the wrong shape at the operator's end, on unzip. It
cannot stop a chat producing it. The skill rewrite is what addresses that and it is the
weaker half, since it depends on the next chat reading the delegation and pulling the
cheatsheet.

### 2026-07-27 - ZHVI rebase: Median Home rebuilt for all 99 cities (v17)

**Problem.** `Median Home` was never one vintage. Joined against Zillow's city-level mid-tier ZHVI
series, the 99 DB figures dated from 2020 to 2026: one 2020, five 2021, twenty-six 2022, twenty 2023,
eighteen 2024, twenty-one 2025-26. The project started in April 2026, so every value was entered
within four months and was already stale when typed. Cause: the column was seeded from web research,
which returns cached crawls and articles quoting whatever was current when written. The data-source
rule was working downstream; the leak was upstream of it.

**Fix.** All 99 rebased from the 2026-06-30 ZHVI column. The eight cities that do not join on name
were normalised and each geography verified by county, not just by name: Saint Augustine (Saint Johns,
not Saint Augustine Beach), Saint Petersburg (Pinellas), Coeur d'Alene (Kootenai), Saint Paul (Ramsey,
not South/West/North Saint Paul), Saint Louis (Saint Louis City), Hilton Head Island (Beaufort),
Saint George (Washington), Jackson (Teton) for Jackson Hole. Both Wilmingtons resolved separately
(DE/New Castle, NC/New Hanover) and Beaufort NC to Carteret, the coastal town.

94 median home values changed, 80 Monthly Est, 14 Budget Range, 23 D2. Median gap +2.8%. Largest
movers: Beaufort NC +36.5%, Rehoboth Beach +27.8%, Memphis -24.6%, San Antonio -21.6%, St. Louis
-18.3%. Monthly Est recomputed via BUDGET-METHODOLOGY.md sections 3-6.

**Second fault found en route: Monthly Est did not equal f(Median Home) for 31 of 99 cities.** An
input had moved and nothing re-derived the budget. Sedona and Grand Junction were traced to a
`Climate Warm W` edit after the June audit, which moves the utilities climate adjustment. The rebase
wipes this out by construction: the recompute now reproduces all 99 from the DB, up from 68.

**Third fault: `pick-and-compare.html` disagreed with `index.html` on d2 for 72 of 99 cities.** This
is the boarded "72 stale D2 scores" item, now closed. Root cause: that page carries its own JSON blob
(`monthlyEst`, `monthlyMid`, `medianHome`, `medianHomeMid`, `budgetTier`, `d2`) and nothing held it to
the DB. `check_highlight_surfaces` enforces highlight parity between the two surfaces but not score
parity. All ten dimensions now agree across both surfaces for all 99 cities.

**Seven carve-out fossils rewritten.** San Antonio, Memphis, Indianapolis, Wilmington DE, Tulsa and
two St. Louis surfaces still framed the city on the retiree-target-neighborhood basis retired by
MEDIAN-HOME-METHODOLOGY.md v1.2 on 2026-07-13. Tulsa's note cited "v3.2 high-variance methodology" by
name. All now lead with the citywide figure and carry neighborhoods as a Neighborhood Reality Check.
The phrase "Monthly costs ... in target areas" was false on every one of them: per
BUDGET-METHODOLOGY.md section 4 the monthly figure is computed from the citywide home value for all
99 cities, never from target neighborhoods. Struck.

**Seven dated attributions dropped.** Des Moines, Iowa City, La Crosse, Salt Lake City, Traverse City,
Tulsa and Provincetown attributed a figure to a named source and often a date ("per Boston Globe /
Warren Group April 2026", "Redfin Feb 2026"). A June ZHVI number cannot inherit a February Redfin
citation, so the attributions were removed and the ZHVI figure stated plainly rather than re-sourced.

**Also fixed.** Durango stated a county median and an in-town figure, neither of which was the
published city basis; now the city ZHVI. Knoxville claimed "median home is under $377,000" against a
DB of exactly $377K. Coeur d'Alene's pick-and-compare record was stale ($553K against $611K) and
invisible to the gate because that entry stores its name JSON-escaped. St. Louis's abbreviated
"Monthly Budget" stat card read $3.5-4.8K against a DB of $4,100-$5,200, and was wrong before the
rebase too; the validator does not parse that abbreviated form.

**DB header note corrected.** It claimed snapshot 2026-04-30 and still described the eight-city
retiree-target carve-out retired on 2026-07-13. Both replaced.

**Net:** validator 0 failures, 0 warnings on `--local .`. `apply-batch.py` verified idempotent.
Audited: only D2 changed across both surfaces, zero unintended edits to D1 or D3-D10.

### 2026-07-26 - The Median Home column was stale on the day it was written

Board-only session. No content surface changed, no score changed, no DB written. What changed is
what we know.

**The six-city question resolved, and it resolved the other way.** Casper, Columbus, Des Moines,
La Crosse, Roanoke and Sioux Falls had quoted prose figures ABOVE `Median Home`, and on Jul 23 they
were edited DOWN to the DB on the data-source rule. Checked against Zillow's own city-level
mid-tier ZHVI CSV, June 2026 column: **all six DB figures are low**, by +6.9% to +18.8%. The prose
was the newer vintage. The Jul 23 edits pushed better numbers back to worse ones. Per the standing
note, the fix is to correct the DB and re-derive, never to hand-revert.

**Then the column itself.** Dating each DB figure by finding the month in the ZHVI series it best
matches gives 1 city at 2020, 5 at 2021, 26 at 2022, 20 at 2023, 18 at 2024, 21 at 2025-26. It is
not one vintage that drifted. It is a patchwork.

**The part worth writing down: this project started in April 2026.** Every value in that column was
entered within the last four months, yet the vintages run back to 2020. They were not entered fresh
and left to age. **They were already stale the moment they were typed in.** The cause was
demonstrated live in-session: a Zillow page returned in a web search served Casper at $273,235,
which is a late-2022 value, while the CSV for the identical RegionID said $314,485. Nothing on the
page marks it as old. Web research returns cached crawls and licensed snapshots, and they look
current. The data-source rule (DB canonical, research for colour only) was working correctly the
whole time; the leak is that the DB was itself seeded from research, upstream of the rule.

**Magnitude, honestly.** Median gap +2.7%. 49 of 91 within +/-5%. **81 of 91 do not change D2
median-home band.** Ten move; five have live profiles; two of those five are noise (Knoxville
crosses $375K by $1,600; New Orleans moves favourably). The real review list is three cities. Seven
live profiles carry a figure more than 8% stale, worst being Tulsa at +14.9% with a DB vintage of
July 2022 - which shipped as profile 46 two days ago with an NRC callout built on it - and Salt
Lake City at an August 2021 vintage, the oldest on any live profile.

**Not fixed here, deliberately.** The rebase is an OPS job of its own: normalise the 8 name
variants that do not join, rewrite all 99 figures, recompute Monthly Est, re-derive the profile
surfaces, review D2 on the band-movers, ship a new DB version. Doing any of that inside a BATCH
chat would be exactly the scope creep the chat taxonomy exists to stop. Casper was queued as the
next BUILD and has been pushed behind the rebase; building it today would write a 15%-stale figure
into a stat card, JSON-LD and pros/cons, all to be edited out weeks later.

**The pattern, now four for four.** Gilcrease was a status copied once and never re-checked. The
NRC roster was a list copied out of the profiles and never re-checked. The Tulsa property tax was a
figure copied with no source. `Median Home` is the same failure at 99x scale. In every case the
authoritative answer existed elsewhere and something held a copy. The open question for the rebase
is therefore not just "what are the right numbers" but "what re-checks them next year" - most
likely a validator vintage check against the CSV, so drift lands on the gate instead of waiting to
be noticed.

**Also fixed:** two TASKBOARD header nits. The inventory line said 7 landing pages and counted only
`top-cities-for-*`, omitting the 4 `best-places-to-*` pillars; it now reads 11 and names both sets.
The validator line still referenced the Roanoke push and now cites commit `0699f7f`, with the bare
post-deploy run noted as still outstanding.

### 2026-07-25 - BATCH: a closed museum, a stale NRC roster, and a property-tax premise that was wrong

**Four items in, four items out, four boarded.** No new files, no city builds. Every edit shipped
through `apply-batch.py` against a fresh clone; `python3 tools/validate.py --local .` returned
0 failures, 0 warnings before and after.

**1. Gilcrease Museum, the second and third surfaces.** The July 24 Tulsa build caught this in the
profile and boarded the other two. Both are now closed. `top-cities-for-arts-lovers.html` and
`docs/arts-lovers-cities-scoring-analysis.md` now read `Gilcrease Museum (reopens spring 2027)` and
`Gilcrease Museum (closed for rebuild since 2021, reopens spring 2027)` respectively. Verified
before writing: closed since 2021, reopening spring 2027 rather than 2026, and $140.9M against an
original $83.6M plan, which is the roughly 70% overrun the board recorded. **Marked, not deleted.**
The collection is a real reason Tulsa scores 8.5 on the arts list, and deleting the name would have
quietly weakened a tier rationale to fix a status error.

**Swept the other city pages for the same shape, and found no second instance.** Checked every
`city-teams` strip on all seven landing pages. Three near misses, all cleared: Park Square Theatre
(St. Paul) survived its 2023 fiscal crisis and is producing a five-play Hatcher cycle; the Minnesota
Museum of American Art is open Thursday to Sunday; and the Diana Wortham Theatre was **not** renamed
out of existence, it is the 500-seat main stage inside the Wortham Center complex, so the arts card
is correct as written. Two real finds, both boarded rather than shipped, see below.

**2. The NRC roster was not two cities behind. It was seven, and one city did not exist.**
`PROFILE-FORMATTING.md` listed ten. The board said twelve. `grep -l 'reality-check-eyebrow'
cities/*/profile.html` returns **17**. The eight undocumented cities are Fort Collins, Knoxville,
Miami, Prescott, Roanoke, San Antonio, Savannah and Tulsa. Worse, the listed tenth city was
**Wilmington DE, which has no profile at all** and therefore has never carried a callout on any
surface. It had been sitting in a governing document since June.

**Both docs were carrying the roster, so fixing one would only have relocated the bug.**
`MEDIAN-HOME-METHODOLOGY.md` v1.2 states the principle correctly in sections 1 and 2, that the note
is a universal editorial mechanism with no quantitative threshold, and then contradicts itself by
enumerating ten cities in section 2 and calling them "the 10 cities" in section 4. Both
enumerations are gone. `PROFILE-FORMATTING.md` now governs structure and placement only and defers
to MEDIAN-HOME-METHODOLOGY section 4 for the when, with an explicit instruction not to reintroduce
a list. **A governing document should hold the test, not the answers.** A roster in a doc is a
snapshot that starts rotting the moment the next profile ships; the repo already knows the answer
and cannot be out of date with itself.

**Judgment call, flagged for override.** MEDIAN-HOME-METHODOLOGY was corrected **within v1.2**
rather than bumped to v1.3. The roster was descriptive and the doc's own section 2 already called
it editorial, so no methodology changed. Bumping would have stranded the
`per MEDIAN-HOME-METHODOLOGY.md v1.2` comment in all 17 NRC profiles, which is a 17-file cascade to
buy nothing. A dated correction line sits in the doc header instead. PROFILE-FORMATTING did change
substantively and went 1.5 to 1.6.

**3. The property-tax item had a false premise, and the sweep is the finding.** The board read
"index.html says 0.77, DB says 0.79, one is wrong." Neither was wrong in the way that implies.
`D5-TAX-METHODOLOGY.md` section 2 defines `PropTax Rate %` as **one value per state**, and the DB
holds exactly one value per state across all 39 states in the file. The `index.html` D5 enrichment
carries **county or city** rates, and several say so in the prose (Nueces, Tarrant, Williamson,
Escambia counties). A sweep of all 38 property-tax figures in the enrichment found **17 cities**
where the two disagree by design. That is not 17 bugs; it is two fields measuring two different
things, which nothing in the docs says out loud.

**Tulsa was a real error for a reason specific to Tulsa: it is the only Oklahoma city in the
database.** With no other OK row there is no city-versus-state distinction to preserve, so the two
fields should agree and they did not. 0.77 also matched nothing external: sourced Tulsa County
effective rates run 0.94% to 1.06%, so 0.77 was not a county figure that had been correctly
recorded. Fixed to 0.79 in both places it appears, the pros bullet and the D5 scoreNote, matching
the DB, `cities/tulsa/profile.html` (which computes 0.79% as roughly $2,370 on a $300K home), and
the D5 methodology. The paired median bill of $1,672 stays: at 0.79% it implies a home of about
$212K, which is the right order for the Tulsa County median.

**4. The one-line residue was the Wilmington DE phantom**, closed as part of item 2. The two other
finds are both genuinely more than one line and were boarded rather than expanded into:
`top-cities-for-sports-fans.html` still lists `Mullett` on the Scottsdale card, but the Arizona
Coyotes were sold and relocated to Utah in April 2024, so that is a text edit **plus** a pill
recount from `5+ teams` to `4 teams`. And the Memphis `Brooks Museum of Art` entries are correct
today and become wrong in autumn 2026 when it closes in Overton Park and reopens downtown as the
**Memphis Art Museum**, so they are dated rather than deferred.

**The lesson that keeps recurring, one level further out again.** July 19 caught a UNESCO claim.
July 24 caught a closed museum in a profile. July 25 caught the same museum on two more surfaces, a
roster that had drifted seven cities in one month, and a phantom city sitting in a governing doc.
**In every case the repo already held the right answer and a document held a copy of it.** The
Gilcrease status lived in the world, the NRC list lived in the profiles, the property tax lived in
the DB. Every one of these bugs is a cached copy that nobody invalidated. Prefer a query to a list.

### 2026-07-24 (second push) - Tulsa, OK profile; a closed museum caught pre-publish; build hand-off format standardized

**Shipped.** `cities/tulsa/profile.html`, profile 46, plus hero/detail/lifestyle photos. Built from a
live pull of the canonical `cities/st-louis/profile.html`. All dimension scores, `Monthly Est`, and
`Median Home` read from `docs/CityDatabase_Jul_23_v16_6_nohighlight.xlsx` row 96 (D1 7 / D2 9 / D3 8 /
D5 7 / D6 5 / D7 5 / D8 6 / D9 7 / D10 8, D4 Resil 4, Range 1, $4,200-$5,300/mo, $194,000). Research
used only for supporting color: Saint Francis and Ascension St. John credentials, Gilcrease
construction status, Route 66 centennial dates, Oklahoma retirement-tax rules.

**Emphasis brief.** One pillar at 9 (D2 Budget) with D3 Health and D10 Community both at 8 and
D1/D5/D9 at 7. MULTI-STRENGTH, not MULTI-PILLAR, so the hero leads with value and the
culture-plus-healthcare cluster carries real weight in the character section rather than fading behind
the price story. The hard-flagged counterweight is D4 Resilience at 4, Tornado Alley, which leads the
"Skip if" column alongside summer heat (`Climate Hot Sum` 3, HEAT 8).

**Bug caught pre-publish: a museum that has been closed for five years.** The first draft listed
Gilcrease Museum among Tulsa's open institutions, which is what `top-cities-for-arts-lovers.html` shows
on its Tulsa card and what `docs/arts-lovers-cities-scoring-analysis.md` lists in the Tier 2 rationale.
Gilcrease has been closed since 2021. Its replacement building now opens spring 2027, a year later
than planned and roughly 70% over budget at $140.9M total. Corrected before publish: the profile
treats it as under construction with a dated reopening. **Consequence: a landing-page card and a
scoring-analysis doc record why a city earned a tier, not whether each named institution is currently
open.** Institution status is a live fact and needs checking at build time, the same lesson as the
July 19 San Antonio UNESCO claim, one level further out.

**NRC callout added off-list.** Citywide `Median Home` $194,000 against retiree-target neighborhoods
at $300K-$500K, with the Maple Ridge mansion blocks past seven figures. MEDIAN-HOME-METHODOLOGY.md
v1.2 treats the Neighborhood Reality Check as a universal editorial mechanism rather than a fixed
list, so the callout was added and approved. Tulsa is the twelfth NRC city. `PROFILE-FORMATTING.md`
still says ten and is now two behind, San Antonio having made eleven on July 19.

**Superlative handling: copy tightened before the ledger, not instead of it.** The Saint Francis bed
count fired three UNREVIEWED warnings for one fact, across the health card, a fit bullet, and the
JSON-LD FAQ. Rather than ledger the same claim three times, the vague hedge "among the largest in the
country" was replaced with the sourced figure "the 11th largest in the nation", and the redundant
third mention was cut from the fit bullet. Two ledger rows remain, both TRUE, evidenced to Saint
Francis Health System and the Premier 15 Top Health Systems 2025 study. **The ledger is for claims
that cannot be improved, not for claims that have not been edited yet.**

**Affiliate codes live.** Expedia `TtKUzzx`, Vrbo `W5AR3HO`, from the operator's
`visit-block-affiliate-codes.numbers`, both with `rel="sponsored nofollow"`. Note the sheet has blank
State cells on its last four rows (Tulsa, Virginia Beach, Iowa City, Carmel); the codes themselves are
in the correct columns, verified by cross-checking the St. Louis row against the live St. Louis
profile.

**Build hand-off format standardized.** The operator flagged that consecutive build chats deliver
their files in different shapes, which is true and was costing a rename step or a wrong-folder drop
each time. Reviewing `roanoke-deploy.zip` against this build: that zip carried whole copies of
`index.html` (674K), `sitemap.xml`, `best-places-to-retire-on-a-budget.html`, `TASKBOARD.md`,
`SUPERLATIVE-LEDGER.md`, and `SITE-OPERATIONS-LOG.md`, against section 4a. All six happened to be
byte-identical to live main, so nothing was reverted, but that is the empty-window case rather than a
safe method. The July 14 Knoxville near-miss is the same pattern caught only because the reverted
content was itself a hard-FAIL class; a whole-file zip that reverts a corrected photo credit or a
reciprocal link ships silently. Tulsa shipped instead as a new-files-only bundle plus an idempotent
patch script (`apply-tulsa.py`) holding every edit to an existing file, each guarded by an exact
anchor match that refuses to write if the file has drifted. Standard now recorded in
DEPLOY-CHEATSHEET.md section 4. **New files arrive in a zip already in their final repo paths; every
existing file is edited by script, never shipped as a copy.**

**Found, boarded, NOT fixed here.** `top-cities-for-arts-lovers.html` lists Gilcrease on the Tulsa
card as an open institution. `index.html` enrichment gives Tulsa `PropTax` 0.77% against the DB 0.79%.
`PROFILE-FORMATTING.md` NRC list is two cities behind. Tulsa's `pick-and-compare.html` D2 of 7 against the DB 9 is one of the 72 stale D2
scores already boarded on July 23, not a new finding.

**Same-day photo swap, and two process failures.** The detail photo shipped as a placeholder and was
replaced the same day with Boston Avenue Methodist Church (CPacker at English Wikipedia, CC BY 2.0),
credited on the image and in the footer with a license link and a cropped note. **A CC BY image
cannot ship until the author name is in hand; the license text alone is not enough.** Two failures,
both caused by the deploy instructions rather than the operator. The one-time patch scripts were
committed twice, because the hand-off put `rm apply-<city>.py` after `git push` while `git add -A`
ran before it. `apply-*.py` is now in `.gitignore`: **a guard that has to be remembered will
eventually be forgotten, so it belongs in the tooling.** Separately, the replacement photo was
committed to the repo root because the instruction asked for a hand-rename plus a drag into a nested
folder, and for a period the live page credited Boston Avenue while displaying the Prayer Tower.
**Images are dragged to the repo root and moved with one `mv` line; never hand-renamed, never
dragged into a subfolder.**

**Landing pages.** `top-cities-for-arts-lovers.html` already carried a live Tulsa card.
`best-places-to-retire-on-a-budget.html` carried Tulsa as a `coming-soon` div, promoted to a live
link. No other landing page needed editing.

**Gate.** `python3 tools/validate.py --local .` reads PRE-DEPLOY GATE, 0 failures, 0 warnings,
verified end to end on a fresh `--depth 1` clone with the patch script applied before hand-off, not
only on the build machine. Bare post-deploy run confirmed 0 failures, 0 warnings after the push.

**Files changed.** `cities/tulsa/profile.html` (new), three photos (new), one `PUBLISHED_PROFILES`
line in `index.html`, one url block in `sitemap.xml`, one card in
`best-places-to-retire-on-a-budget.html`, `SUPERLATIVE-LEDGER.md`, `TASKBOARD.md`,
`SITE-OPERATIONS-LOG.md`, `DEPLOY-CHEATSHEET.md`.

### 2026-07-24 - Roanoke, VA profile; four stale index.html figures fixed en route

**Shipped.** `cities/roanoke/profile.html`, profile 45, plus hero/detail/lifestyle photos. Built from
a live pull of the canonical `cities/st-louis/profile.html`. All dimension scores, `Monthly Est`, and
`Median Home` read from `docs/CityDatabase_Jul_23_v16_6_nohighlight.xlsx` row 81 (D1 5 / D2 9 / D3 7 /
D5 6 / D6 6 / D7 8 / D8 7 / D9 7 / D10 7, Range 1, $4,400-$5,400/mo, $251,000). Research used only for
supporting color: ROA nonstop and carrier counts, Carilion credentials and trauma level, Virginia
retirement-tax rules, Carvins Cove and McAfee Knob facts, neighborhood price spot-checks.

**Emphasis brief.** One pillar at 9 (D2 Budget) with D7 Outdoor at 8 and a wide 7-band. That is the
MULTI-STRENGTH shape, not MULTI-PILLAR, so the hero and character lead with the value-plus-mountains
cluster rather than a single hook, and give the 7-band real weight. Honest counterweight leads the
"Skip if" column: D1 Airport = 5 (about 10 nonstops, most trips connect), plus D5 = 6 (Virginia taxes
retirement income up to 5.75%) and D6 = 6 (car needed outside downtown and Grandin Village). Not an
NRC city, so no Reality Check aside or method-callout; the wide citywide-to-South-Roanoke gap
($251K vs ~$580K) is carried honestly in the hood cards instead.

**Detail photo = the Roanoke Star**, used as the civic-identity photo break (parallel to St. Louis
baseball). Valley-from-overlook shot handed off as an alternate. Taubman Museum photo is CC BY-SA 3.0
(Warfieldian / Wikimedia), credited with the license named, not as Unsplash.

**Four stale index.html figures fixed while in the file.** The existing Roanoke `CITIES`/enrichment
entry carried: a `$280K` pro that contradicted its own `$251K` highlight (DB says $251,000); a "16
procedures" hospital count (U.S. News 2025-26 says 15); a D1 scoreNote naming only Atlanta and
Charlotte (ROA now flies 7 hubs plus a new June 2026 DFW daily); and a D7 scoreNote calling Roanoke
"a Range 2 city" when it is Range 1. All corrected.

**Deploy.** `PUBLISHED_PROFILES` gained `'Roanoke_VA'`; `sitemap.xml` gained the url block; the budget
landing page's Roanoke card flipped from "Coming soon" to a live link. Roanoke was already carded on
the hikers and disaster-safe landing pages, so no other reciprocal edits. Carvins Cove
"second-largest municipal park" retired to `SUPERLATIVE-LEDGER.md` as a verified outside-world fact.
Visit block ships with `EXPEDIA_CODE_TK` / `VRBO_CODE_TK` placeholders pending Creator Hub codes;
grep-gate `CODE_TK` before deploy. `python3 tools/validate.py --local .`: **0 failures, 0 warnings**.

### 2026-07-23 (second push) - em-dash check rebuilt to count renderings; DB `Highlight` column deleted (v16_6)

**The bug.** `check_emdash` counted the literal character `\u2014` and nothing else. Every string on
`pick-and-compare.html` is stored as JSON, where an em dash is written as the six characters
`\u2014`, so the check read ZERO while 85 escaped em dashes sat live in five files, one of which had
been in its own target list the whole time. This is the THIRD instance of the family the check's own
docstring already documented twice: `visible_text()` stripping `<script>`, then `index.html` not
being a target at all, now the escape form. The through-line is a check written against one spelling
on one surface.

**The fix is the shape, not the spelling.** `emdash_forms()` counts every rendering that reaches a
reader: the literal character, `\u2014`, `&mdash;`, `&#8212;`, `&#x2014;`. Three exclusions are
deliberate and each is named in the docstring: em dashes inside `<style>` and `<script>` code;
the short `'\u2014'` UI placeholder, which survives because `script_strings()` only returns literals
of 25+ characters; and regex character classes that match em dashes on purpose.

**That third exclusion is new and it is load-bearing.** Two of the 85 were
`/[\u2013\u2014\-].*\$/`, twice in `pick-and-compare.html`. `script_strings()` pairs quotes naively
and hands the code around that line back as if it were a literal, so counting escape forms without
removing whitespace-free bracket groups first puts two permanent failures on correct code. A gate
with permanent noise in it is a gate nobody reads. The real count was 83.

**A named target that matches no file now FAILS.** It used to be skipped in silence, which is a
fourth way for this check to read zero: rename a landing page and its em-dash coverage retires
without a word.

**Converted.** 61 on `pick-and-compare.html`, 22 in the JSON-LD of `cities/new-orleans`,
`cities/philadelphia`, `cities/salt-lake-city` and `cities/st-louis`. Four of the 22 were the Article
`headline` separator, brought into line with the colon the other 44 profiles already use. The JSON-LD
ones do not render on the page but they are what search results are built from.

**The page conversion was already written.** `index.html` was swept on Jul 13 and
`pick-and-compare.html` was missed. Same field, same 99 keys, and the two had disagreed on 65 rows
ever since, in silence, because nothing compared them. All 99 were synced FROM `index.html`, which is
newer on every one of the 24 rows differing by more than punctuation: the `median home` ->
`typical home value` terminology sweep, the Jul 12 superlative sweep, and corrected figures for
Boulder ($800K-$1M -> $964K), Bentonville ($300K-$500K -> $488K) and New Orleans (neighborhood
figures added).

**The DB `Highlight` column is DELETED, not converted.** The same sentence lived in three places and
all three disagreed: DB vs `pick-and-compare.html` 16 rows, DB vs `index.html` 67, the two surfaces
65. `load_db()` never read the column, no tool consumed it, no check validated it. It was a master
nothing read, which is the exact shape `check_affiliate` already refuses: the HTML IS the record, and
a half-current reference is worse than none because eventually someone trusts it. Deleting it also
retired twelve banned dataset-scoped superlatives, Chattanooga's unanchored "Best value city in the
Southeast", and two cells that contradicted the `Median Home` in their own row (New Orleans $267K
against $250,000; Tulsa $245K against $194,000). Confirmed with the founder that `Median Home` is
the correct figure in both cases.

**New check: `check_highlight_surfaces`**, in the `figures` group. Fails when a city's highlight
differs between `index.html` and `pick-and-compare.html`, byte for byte, or when a city has one on
only one surface, or when either extractor reads nothing. Byte-for-byte on purpose: "near enough" is
how a terminology sweep half-lands and one surface says median home while the other says typical home
value. This check is what makes "one record" true rather than aspirational, and it would have caught
the em-dash gap on the day it opened.

**Tests.** `tools/test_emdash_forms.py` is NEW, 10 assertions, all passing: the escape form in prose
is caught; `<style>` stays silent; the short placeholder stays silent in BOTH spellings; a regex
character class stays silent; prose sitting beside a character class is still caught; `&mdash;`,
`&#8212;` and `&#x2014;` are caught; a named target matching no file fails loudly.
`tools/test_highlight_homes.py` grew from 15 to 18 for the new check. Its older assertions were
RETIGHTENED, not loosened: a single-surface plant now legitimately trips two checks, so each
assertion states what it expects from each rather than counting failures.

**Database.** Column removed as inline strings in `xl/worksheets/sheet1.xml` and rezipped. No
openpyxl, no pandas. Column V dropped, W through AF shifted left, `<dimension>` and the `<cols>`
widths adjusted. Verified: every other zip part byte-identical, part order preserved, `Highlight`
the only header removed, zero data cells changed outside it, and `load_db()` output identical old vs
new. Superseded file deleted BEFORE the gate run, since the `docs` group counts CityDatabase files
on disk.

**Found, boarded, NOT fixed here.** `pick-and-compare.html` carries 72 stale D2 (Affordability)
scores. All 99 cities were compared on all ten dimensions across both surfaces: 72 disagree, every
one of them D2, and in every case `index.html` matches the DB and `pick-and-compare.html` does not.
D2 is a sorted and checkmarked row on the comparison tool. Also boarded: two live em dashes on pages
the check has never scanned (`privacy.html` `<title>`, `scouting-trip-workbook.html` line 1020), and
profile JSON-LD home figures contradicting `Median Home` for Philadelphia ($234,000 vs $240,000,
twice) and New Orleans ($246,000 vs $250,000) while both cities' highlights carry the correct figure.

**Gate.** `python3 tools/validate.py --local .` reads PRE-DEPLOY GATE, 0 failures, 0 warnings.

### 2026-07-23 - highlight home-figure check shipped; DB `Highlight` column reconciled (v16_5)

**Shipped.** `check_highlight_homes()` in `tools/validate.py`, folded into the `figures` group,
FAIL not WARN, with `tools/test_highlight_homes.py` as its planted-error test (15 assertions). The
check holds every home figure written into `highlight` PROSE to that city's `Median Home`, on both
`index.html` and `pick-and-compare.html`. Exact match, no tolerance band: a figure in thousands must
equal `round(DB/1000)`.

**Why anchored, not blanket.** Three shapes in these strings are supposed to disagree with
`Median Home`, and a check that fires on every dollar figure red-lights all of them forever: the NRC
neighborhood range, the cross-city reference (Tampa naming Naples' figure), and figures that are not
homes at all (Tulsa's $465M park, Traverse City's $132K tax deduction). A figure is in scope only
when it is attached to a home-value noun. A cross-city veto sits behind the anchor. Bounds are
checked as inequalities, not equalities, which is what caught Roanoke's "median homes under $230K"
against a `Median Home` of $251,000.

**16 drifted figures on the two HTML surfaces**, all real, all reconciled in the same push:
`index.html` 9, `pick-and-compare.html` 7. Sioux Falls carried two DIFFERENT wrong figures, $333K on
one surface and $285K on the other, against $314,000. Provincetown's $2.1M resolved to $924K, which
its own `D2` modal already said, sourced to Boston Globe / Warren Group April 2026.

**Then the source.** Running the same matcher over the DB's own `Highlight` column found 16 more, a
DIFFERENT 16: the column was a pre-Jul-23 vintage still holding every NRC citywide figure from
before that sweep, including Wilmington DE at $215K against $321,000, the exact string used as the
planted error in the test. Fixing two renderings does not fix a master, and the next regen would
have reintroduced all of it. Database bumped to
`docs/CityDatabase_Jul_23_v16_5_highlights.xlsx`, `DEFAULT_DB` updated in the same commit, old file
deleted. Also removed from Miami's cell: "The only city in the database with all four major pro
sports leagues," a dataset-scoped superlative banned since Jul 12, sitting in the master where a
regen would have pushed it back onto the site.

**How the xlsx was edited.** Inline strings in `xl/worksheets/sheet1.xml`, rezipped. No openpyxl, no
pandas, same zero-dependency posture as the validator. Verified afterwards: every other zip part
byte-identical, the other four sheets row-identical, `load_db()` output identical old vs new (so no
score, monthly, home value or budget tier moved), exactly 16 rows changed, exactly one column
touched.

**Still open.** The column is clean but ungated: run the same matcher over it inside the `db` group.
It also carries em dashes on most rows where `index.html` does not, and it matches
`pick-and-compare.html` on only 68/99 rows and `index.html` on 26/99, so there is no single
"regenerate from source" path today. All three are on the taskboard.

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
