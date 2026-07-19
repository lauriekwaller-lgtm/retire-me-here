# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 18, 2026 (pros/cons figure check promoted WARN -> FAIL; profile stat-card +
FAQ JSON-LD drift AUDITED, 4 findings across 4 cities, fixes not yet applied)

**Verified live at last update:** 43 profiles, 19 comparison pages, 5 guides, 7 landing pages.
All 43 profiles carry a Visit block. Validator: **0 failures, 0 warnings**, confirmed on BOTH
`--local .` (the tree that was pushed) and bare (live GitHub). The warn queue reaches zero because
`docs/SUPERLATIVE-LEDGER.md` retires reviewed outside-world claims; anything NOT in the ledger is
unreviewed and shouts. Zero is now the expected reading. If a warning appears, it is new.
The validator now ALSO carries a pros/cons home-figure check (folded into the `figures` group).
As of Jul 18 it ships **FAIL**, not WARN: the Jul-15 34-figure reconciliation held, both `--local .`
and the live bare run read 0 pros/cons warnings, so drift now blocks the gate like every other
figures check. Planted-error tested (Knoxville `$327K` against DB `$368,000`: 1 failure, exit 1).

---

## How to run chats

One job type per chat. Name chats so they are findable:

| Chat name pattern | For | Lifespan |
|---|---|---|
| `BUILD - <City>` | one city profile, end to end | dies when the city ships |
| `COMPARE - <A> vs <B>` | one comparison page | dies when it ships |
| `BATCH - <job>` | repo-wide scripted operations (retrofits, sweeps) | dies when the batch is pushed |
| `OPS - planning & tracking` | this board, decisions, methodology Qs, small one-off fixes | permanent home base |

Rules of thumb:
- A NEW city's Visit block + affiliate codes belong IN that city's `BUILD` chat.
- RETROFITTING existing profiles is a `BATCH` job, never woven into a single city build.
- If a chat shows a "conversation compacted" note, finish the current step, update this board, start fresh.

**Before every deploy:** `python3 tools/validate.py --local .`  <- THIS IS THE GATE
**After every deploy (optional receipt):** `python3 tools/validate.py`

These read different things. `--local .` reads your working checkout: the code you are about to push.
Bare reads live GitHub: the code already deployed. A bare run BEFORE a push grades the OLD site with
your NEW rules and reports failures you have already fixed. This misfired twice on July 14, 2026.

As of July 14 the validator PRINTS WHICH ONE IT IS DOING at the top of every run:

    mode:     PRE-DEPLOY GATE -- reading the files on this machine
    mode:     POST-DEPLOY CHECK -- reading the LIVE files from GitHub, not your working copy

If the header says POST-DEPLOY, the numbers describe the live site, not your work. Read the header
before you read the failure count.

Standard deploy block:

    git pull
    (drag zip into repo root)
    unzip -o <bundle>.zip
    rm <bundle>.zip
    python3 tools/validate.py --local .     # must read PRE-DEPLOY GATE and 0 failures
    git add -A                              # -A, not `git add .` -- catches docs/ and tools/
    git commit -m "..."
    git push

---

## ACTIVE - batch / site-wide operations

- **Superlative rules are now PATTERN-based, not string-based - keep them that way.** The old ban was
  a list of remembered phrases, and every single leak came through the list, never the logic. Six
  distinct shapes were found live on July 14: a modifier the list didn't have (`in ENTIRE database`),
  a region word between modifier and noun (`in our FLORIDA coverage`), a curation verb not on the list
  (`we have COMPARED`), a verb pointing at the corpus with no preposition (`Three cities TOP the
  database`), attribution voice (`our database NOTES NCH as...`), and a different noun (`our Florida
  SET`). All six are now closed structurally. When adding a new one, ban the SHAPE, never the string.
  Counter-check: `high on YOUR list` and `across the board` must NOT fire - the free-word slot is only
  allowed after a real determiner, and page-local objects (the two-city scorecard the reader is looking
  at) are bounded and static, so they cannot rot and are not this policy's business.
  **New leak found Jul 15 (Pensacola):** `Florida's lowest here`, and the bare `[STATE]'s lowest` form,
  scope a rank to the site through the word `here` with no ledger phrase to trip on. Same rot as
  `we cover`, different disguise. Close the SHAPE (a superlative/rank adjacent to a state name, or a rank
  plus site-scoping `here`), surgically enough that an innocent `here` (`the winters are real here too`)
  does not fire.

- **Validator: add a climate check group** - the validator compares `index.html` city FIGURES against
  the DB but has never checked the CLIMATE blocks. They happen to match 99/99, but nothing enforces it,
  and the July 13 rebuild added three fields (`janF`, `snow`, `sun`) that live in `index.html` with no
  guard at all. Add a group asserting (1) all five original climate values match the DB per city,
  (2) `janF`, `snow`, `sun` present and non-null for all 99. Silent drift of exactly this kind produced
  the Boulder bug.

- **Profile stat-card + FAQ JSON-LD drift: AUDITED Jul 18, fixes NOT yet applied.** Audit-only pass,
  all 43 profiles, read against `CityDatabase_Jul_13_v16_4_climate.xlsx`. Nothing like the 34-figure
  pros/cons blowout: **4 findings across 4 cities.** In every case `index.html` and the DB agree and
  the PROFILE is the stale side.
    1. `pensacola` stat card Budget Score reads `7/10`, DB D2 is `8`.
    2. `st-paul` stat card Monthly Budget reads `$3.8-5K/mo`, DB is `$4,700-$5,900/mo`.
    3. `columbus` FAQ answer + Article description both read `$249,000`, DB Median Home is `$235,000`.
    4. `st-louis` FAQ answer reads a citywide `$250,000`, DB Median Home is `$235,000`.
       (`tampa` FAQ `$377,000` vs DB `$400,000` was also flagged; see the audit report.)
  **The finding that matters more than the count:** pointing the EXISTING `PROSCONS_HOME` matcher at
  the FAQ schema would have covered 13 of ~45 home figures. The FAQ voice is
  "the typical home value in Columbus **is around** $249,000" - a hedge, and sometimes a place phrase,
  sits between the noun and the figure, and the pros/cons matcher requires them adjacent. It would
  have reported a near-clean FAQ surface and missed Columbus and St. Louis entirely. The new check
  needs a hedge slot, a money token anchored to end on a DIGIT (a token class ending in `[\d.,]+`
  swallows the sentence comma and drags the other-place guard a clause too far, which is exactly how
  St. Louis hid), and an other-place guard bounded to the SAME clause.
  Two more gaps the audit surfaced, both currently unchecked anywhere:
  the stat card's abbreviated monthly (`$4.9-6.1K/mo`) - `RANGE_RE` only knows the `$4,900-$6,100`
  long form, so 43 monthly stat cards have never been checked; and the two variable stat slots, which
  carry real dimension scores under 20-odd different labels (Healthcare, Outdoor, Walkability,
  Community, Safety, Airport Access, Tax Friendliness, Wellness, Budget Score) and are unchecked.
  Six slot labels are non-DB facts (Founded, Elevation, Metro, Coastline, Weather, State Income Tax)
  and must stay unmapped. NEXT: fix the 4 (5) figures, then build the check against the reconciled tree.

- **Latent label bug on `knoxville-vs-chattanooga`: inverted climate scale.** The summer row is labeled
  "Hot summers (lower = milder)" but populated from `Climate Hot Sum`, which the rubric defines as summer
  COMFORT (10 = comfortable, 1 = extreme heat) - so higher is milder, and the label says the opposite.
  Invisible there because both cities score 6, but the label is wrong. The new `knoxville-vs-nashville`
  page uses the correct "Summer comfort (higher = milder)". Fix the Chattanooga label on its next touch;
  audit other comparison pages for the same inverted wording while at it. Latent, not live-wrong.

- **Visit-block hooks: 4 profiles open on a template.** `asheville`, `bend`, `boulder`, `fort-collins`
  all open the Visit hook with "A scoring sheet can't tell you..." / "A scoring sheet only tells you...".
  PROFILE-FORMATTING.md is explicit that the hook must be "the single most concrete, specific, appealing
  thing about the city... never a generic adjective" and "do not open with a template; every hook opens
  differently from every other block." These four are the last scaffolding repeat in the set: the other
  39 hooks are distinct, and the rental-line openers are 42/43 distinct. Small, precise, judgment-based
  rewrite of four opening sentences. Not batchable.

---

## ACTIVE - city profile builds

- **Next in queue:** San Antonio (unlocks Fort Worth vs San Antonio).
- Then: Roanoke, Tulsa.
- Live profiles: 43. Fort Collins, Prescott, Knoxville and Savannah all shipped since the last board update.

---

## ACTIVE - comparison pages

Live: 19. Shipped since last board update: Knoxville vs Nashville, Fort Collins vs Boulder,
Knoxville vs Chattanooga, Bend vs Boulder, Bloomington vs Lexington, Madison vs Ann Arbor,
Madison vs Columbus, and others.

Unlocked and ready to build now (both cities live):
- **Knoxville vs Asheville**
- **Arizona three-way cluster** (Prescott now live, so this is unblocked)

Unlocks pending a build:
- Fort Worth vs San Antonio (needs San Antonio)

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty)

---

## PARKED / BACKLOG

- **Rubric doc drift: `scoring_rubric_v3.2` describes a filter the code does not run.** The rubric says
  "D1 is the only dimension with a hard filter threshold" and describes a priority ladder (Must Have 8+,
  Very Important 6+, Somewhat Important 4+). Live code does neither. `MUST_HAVE_THRESHOLD = 7` filters
  EVERY dimension marked Must Have, and D1 is not special. `D1_THRESHOLDS` (index.html ~line 6346) is
  defined and referenced nowhere: dead code. Decision made Jul 18, 2026 after checking the D1 spread
  (99 cities: 44 at 7+, 32 at 8+) and the D1=7 cohort city by city: KEEP generic-7. Raising the floor to
  8 would strand Bozeman, Boise, Tulsa, Pensacola, Sarasota, Spokane, Des Moines, Virginia Beach and
  Georgetown, all of which carry real air access. Restoring the ladder would also make "Very Important"
  silently cut 29 of 99 cities while the quiz only ever warns about Must Have. Resolution: delete
  `D1_THRESHOLDS`, rewrite the rubric to describe generic-7 as shipped. Doc + dead-code only, no
  matching-logic change.
- **`D4` key reuse for Climate Resilience & Insurance.** The dimension occupies the internal key `'D4'`,
  the slot the retired cost-of-living dimension vacated. Functionally harmless; it is a trap for anyone
  cross-referencing the rubric, where D4 means something else. Fix ONLY as its own scoped rename with a
  full grep (DIMENSIONS array, every city score object, `quizState.priorities`, `getCityScore`, the
  filter loop, results render) plus a validator run. Never bolt onto other work. Low value, wide blast
  radius: leaving it is a defensible permanent answer.
- Site-wide bolding pass (PROFILE-FORMATTING item 6, judgment-based, not batchable)
- Booking.com affiliate (Awin) - applied; deploy deferred until Expedia fully verified
- Pinterest save-rate optimization (ongoing; cadence + pin copy)
- `Ann Sun %` provenance: ~30 of 99 values are interpolated from the nearest NOAA station. Fine behind
  the 55% dealbreaker cutoff. Do NOT print these figures on a profile page without verifying that city.
- Weather weighting: picking a weather preference auto-sets `DC` to "Very Important" (weight 3) while
  nine other dimensions sit at 1, so climate is 25% of the match score. This is why Florida leads a
  "Mild Year-Round" search ahead of Santa Barbara. Working as designed, not a bug. Raising weather's
  influence is a product decision and needs testing against every quiz path.

---

## RECENTLY SHIPPED (rolling, trim as it grows)

- Jul 18, 2026: PROS/CONS FIGURE CHECK PROMOTED WARN -> FAIL (`tools/validate.py`, one line plus its
  comment). Preconditions re-confirmed first: `--local .` on a fresh clone of main read 0 failures,
  0 warnings, so the Jul-15 reconciliation of 34 stranded figures is holding. Planted-error tested
  three ways: clean tree 0/0, a planted Knoxville `$327K` against DB `$368,000` produces
  `[FAIL] ... figures` and exit 1 (not a warning), revert returns to 0/0.

- Jul 18, 2026: QUIZ DIMENSION DESCRIPTIONS REFRAMED to name the desirable trait (5 of 10, `index.html`
  DIMENSIONS array only). The importance scale asks "how important is this to you?" against four shared
  labels, so a desc naming the neutral topic or the bad end does not parse: "Must Have ... disaster
  exposure" dangles. Fixed: Climate Resilience (`Disaster exposure, insurance cost & availability` ->
  `Low disaster risk, affordable and available insurance`), Airport Access (`Drive time to major hub,
  nonstop routes, airlines` -> `Flying easily from an airport nearby, or a major hub a short drive
  away`), Healthcare (`Hospital ratings...` -> `Top hospital ratings...`), Tax Friendliness (`...property
  tax burden` -> `Low to no tax on Social Security, income, and property`), Safety (`Violent and property
  crime rates by city` -> `Low crime and feeling safe day to day`). The other five already named the good
  version; Weather uses a different pattern. The Airport rewrite is also the RESOLUTION of the Georgetown
  question: Georgetown TX has no field of its own and leans on Austin (AUS) 35 min out, which felt like
  "drive far, then connect" but is not: AUS runs ~87 nonstops incl. direct to JFK/LGA, Boston, Charlotte,
  Atlanta, Miami, DCA/IAD, plus year-round London, Amsterdam, Frankfurt. Chose to name both the
  own-airport and hub-drive cases honestly rather than encode a proximity cap and re-score the
  drive-to-hub cities. Validator 0/0 pre-deploy. Ops-log writeup still to be added.

- Jul 15, 2026: PENSACOLA profile 3-fix correction shipped. (1) Removed a doubled figure in the
  character section (`a typical home of $264,000, a $264,000 median` -> single figure). (2) Fixed a
  stale FAQ monthly buried in the FAQPage JSON-LD (`$3,000` -> `$4,900`; DB `$4,900-$6,100`), invisible
  in prose. (3) Retired `Florida's lowest here` in all 5 spots (meta, og, JSON-LD, stat-sub, character):
  a rank scoped to the site via `here` that goes false the moment a cheaper FL city is added. Replaced
  with `well under Florida's peninsula prices` (panhandle vs peninsula, rot-proof). Verified live: 5x new
  phrase, 0 old rank, 0 stale figure, JSON-LD parses. Ops-log writeup still to be added.

- Jul 15, 2026: PROS/CONS FIGURE-DRIFT CHECK built + 34-CITY RECONCILIATION shipped. The board item
  assumed one stale figure (Knoxville `$327K`, already fixed). The check found 34: a third of the
  CITIES-array pros/cons home figures had drifted from the Jul-13 DB, in both directions (21 high, 13
  low), which reads as accumulated staleness across refreshes rather than one migration. Built into the
  `figures` group, anchored to home-value CONTEXT only, so monthly/bill figures, ranges, explicitly-
  `citywide` figures on high-variance cities, and cross-city comparison figures (`above Georgetown at
  $457K`) do not misfire; 0 false positives across all 99 cities. Shipped WARN, not FAIL, so the 34
  could be reconciled without red-lighting the gate. Reconciled with a two-pass scripted batch (audit
  all, then apply; abort if any anchor is missing or non-unique; re-run-safe), which caught a real
  anchor collision: Santa Barbara's STALE `$1.85M` equalled Jackson Hole's CORRECT `$1.85M`, resolved
  by quoting the anchor to the array literal. Deployed `index.html` (34 fixes) + `tools/validate.py`;
  live bare run reads 0 failures, 0 pros/cons warnings. FOLLOW-UPS now on the ACTIVE board: promote the
  check WARN->FAIL, and extend the same cross-check to profile stat cards + FAQ schemas. Ops-log writeup
  still to be added.

- Jul 15, 2026: WORKING-ENVIRONMENT CLARIFICATION logged in SITE-OPERATIONS-LOG.md (Section 9 +
  change log). Laurie works from a Mac laptop but the repo working tree lives in Codespaces at
  `/workspaces/retire-me-here`; all terminal, git, deploy, and file-management commands run there.
  Operator-facing instructions use bare Codespaces commands and paths, never Mac-local paths or a
  leading `cd`. Docs-only; no site or scoring impact.

- Jul 14, 2026: KNOXVILLE vs NASHVILLE comparison page shipped (page 19). Built from the
  `knoxville-vs-chattanooga` template against COMPARISON-PAGE-STANDARD-v2; scores/figures/tiers from
  `CityDatabase_Jul_13_v16_4_climate.xlsx`. Checkmarks at 2+ point gaps only (D1 Nashville; D7, D9
  Knoxville) plus the three cost rows. Also fixed a stale `index.html` figure: the Knoxville `pros`
  array read `$327K` while its own `medianHome` read `$368,000` (DB agrees $368K); corrected. Deploy
  hit and cleared a real gate failure: a session-start `index.html` copy, packaged whole, reintroduced
  five superlatives that live had been cleaned of in between; rebuilt on a fresh pull as a one-line
  diff. See SITE-OPERATIONS-LOG.md change log for the full note.

- Jul 14, 2026: `.lists-grid-four` UNDEFINED-CLASS BUG FIXED. Four profiles (`st-louis` the CANONICAL,
  `columbus`, `memphis`, `pittsburgh`) carried `class="lists-grid-four"` on the four-card container but
  never defined the rule, and had no base `.lists-grid` on the div to fall back on, so the cards stacked
  full-width instead of forming the centered 2x2. Added a self-contained `.lists-grid-four` rule (display
  grid, `repeat(2, minmax(0,340px))`, centered) to all four, matching the standalone form `st-paul`
  already used. Also added the mobile single-column collapse (`minmax(0,340px)` at max-width 768px) the
  build spec calls for, which no profile was enforcing: on a phone the 2-col grid was squeezing cards to
  ~151px instead of stacking. All 7 profiles that use the class now render identically: desktop 2x2,
  mobile 1-col. `new-orleans` and `philadelphia` were already correct via the two-class combo
  (`lists-grid lists-grid-four`) and needed no change. Nothing in the validator sees CSS, so this class
  of bug does not self-report; caught by audit. Verified with tag-balance; visual behavior reasoned from
  the grid track math, NOT rendered, so eyeball the 2x2 on one rebuilt profile after deploy to be sure.

- Jul 14, 2026: v1.3 TEMPLATE RETROFIT VERIFIED COMPLETE (was "NOT VERIFIED"). Checked against all 43
  profiles, not assumed: forced-dark hardening block 43/43; Visit chip present, in LAST nav position,
  and wired into the scroll-spy ids array 43/43; Deep Dive block correctly placed after Related Cities
  and before Visit 43/43; zero "N-question quiz" copy 43/43. The "comment em-dash cleanup" the old board
  carried as an open v1.3 task was never a deliverable: PROFILE-FORMATTING.md explicitly exempts them
  ("legacy comments carrying em-dashes are cosmetic only and do not require sweeping unless touched").
  219 remain in `<style>`/`<!-- -->` blocks across 36 profiles and are fine there. Rendered em-dashes
  across all 43 profiles: 0.
- Jul 14, 2026: CLOSER-VARIETY SWEEP RETIRED AS OBSOLETE. The item predated v1.4 and had the standard
  backwards. It flagged that the Visit blocks all end on "the highlight reel" as a defect. v1.4 makes
  that closer MANDATORY: "Test the daily routine, not the highlight reel" is the site's signature
  sign-off, "used on every block; it does not rotate." Verified 43/43 carry it verbatim, which is
  compliance, not drift. What the standard DOES require to vary is hooks and openers: 38/43 distinct
  hook openers, 42/43 distinct rental-line openers. The real residual is 4 templated hooks, now its
  own board item.

- Jul 14, 2026: SUPERLATIVE POLICY CLOSED OUT (4 batches). The 41 warnings were the wrong target:
  most were TRUE outside-world facts that should stay. But they formed a wall nobody reads, and false
  claims were hiding in it. Killed: Chattanooga "best value in the Southeast" (8th-cheapest SE city);
  Tampa "best value in Florida" (D2=6, four FL cities beat it, and our own Florida page already said
  Pensacola was cheapest); BOTH FAQPage schema answers wrong (Google can serve those as direct
  answers); St. Augustine claiming FOUR TIMES that "only Naples costs more" when Miami and Sarasota
  both exceed it; three stale D2 scores on comparison pages; "Lee Health #3 on our healthcare list"
  x6 (landing pages are alphabetical, not ranked - that rank never existed). Then 46 instances of
  "our database notes/calls/flags", which launders outside facts (US News rates NCH, not us) through
  a private spreadsheet the reader cannot open. **docs/SUPERLATIVE-LEDGER.md** now retires reviewed
  true claims so the warn queue sits at zero and a NEW claim shouts. See SITE-OPERATIONS-LOG.md
  2026-07-14.
- Jul 14, 2026: GUIDE EM-DASH SWEEP. 231 across all five guides, not the 64 first counted.
  `GUIDES_TOO = True`, planted-error tested. PROFILE-FORMATTING.md -> v1.5. The flag was never a
  decision: its comment claimed the guides were "grandfathered; see PROFILE-FORMATTING.md" and that
  doc grandfathers nothing. It was an unfinished job written in the grammar of a decision, which is
  why it went unquestioned for weeks. Also: all five guides said "Our database has 100." It has 99.
- Jul 14, 2026: VALIDATOR MODE BANNER. One command, two different jobs, nothing on screen saying
  which. Bare runs before a push grade the OLD site with NEW rules and report already-fixed failures;
  this misfired twice in one session. It now prints PRE-DEPLOY GATE or POST-DEPLOY CHECK at the top.

- Jul 13, 2026: Climate engine rebuild. Four compounding faults fixed: the cold dealbreaker was
  calibrated against the wrong scale (Boulder, 33F and 88in of snow, passed a "no freezing winters"
  filter); the `Climate Mild YR` column was actually the dryness score and the grey-winter filter was
  wired to it (removing Naples and Miami while keeping Pittsburgh); `mild` and `warm_dry` were weighted
  averages, so a great summer cancelled a freezing winter; and a `length >= 5` guard was silently
  failing open and discarding the climate filter entirely. Added NOAA 1991-2020 normals to all 99
  cities. DB v16.4. Zero score churn. See SITE-OPERATIONS-LOG.md 2026-07-13.
- Jul 13, 2026: Wilmington DE, Indianapolis and St. Paul median-home corrections confirmed live in both
  DB and index.html. MEDIAN-HOME-LABEL-CONVENTIONS.md deleted. D2 rebuild cleared the suspect
  `$4,500-$5,500` range (the one remaining instance is La Crosse WI's genuine DB value).
- Jul 14, 2026: VALIDATOR BLIND SPOT CLOSED. check_superlatives picked its targets from a
  hand-maintained list of filenames plus a hub regex matching only *-retirement.html. Anything not
  on that list shipped unchecked. privacy.html was never on it. Neither was a stray
  scottsdale-vs-santa-fe-PROFILE.html, which sat live on Netlify with FOUR banned superlatives and
  passed the gate clean. Local mode now discovers pages by globbing the disk: the filesystem is the
  only list that cannot drift from what actually ships. Planted-error tested with a brand-new
  unlinked page. The gate went from a false "0 failures" to a true 6, now cleared to 0.
- Jul 14, 2026: SCOTTSDALE vs SANTA FE deduplicated. Two files existed. The orphan (-profile.html,
  Jul 6) was NEWER and better than the live page (-retirement.html, Jun 22): proper favicon set, and
  a body that names the healthcare drop, the 3-of-10 safety, and wildfire directly. It was a rebuild
  saved under the wrong suffix that never replaced the original. Its body was promoted onto the live
  -retirement.html URL and **the orphan file was deleted with `git rm`**. A zip cannot express a
  deletion, so this step is easy to skip and it is the step that turns the new globbing validator from
  green to 4 failures. D2 scores corrected on the promoted page (Scottsdale 3->4, Santa Fe 6->5, both
  verified against CityDatabase_Jul_13_v16_4_climate.xlsx) and the D2 checkmark dropped, since 4 vs 5
  is a 1-point gap and the table rule is 2+. All dollar figures already matched the DB.
  SECOND PASS: promoting the orphan's body carried in three NEW dataset-scoped claims that the
  validator's literal phrase list does not match: "in the lower third of our 100-city database",
  "which our database records as", and "matched only by Miami and New Orleans among cities to score
  it". All three re-anchored before push. The lesson is below, under the validator item.
- Jul 14, 2026: FAVICON UNIFIED site-wide. 20 pages fixed: 14 carried an inline SVG data-URI, 6
  (privacy.html + Chattanooga, Delray Beach, Pensacola, St. Augustine, St. Petersburg) had none at
  all. All 84 pages now carry the real favicon set exactly once. Verified post-merge: 84/84 pages
  carry `/favicon.ico`, zero pages carry it twice, zero data-URI stragglers remain. Diff-reviewed:
  the batch touched only favicon markup. The 9 asset files were already in the repo root.
- Jul 14, 2026: SAVANNAH, GA profile shipped. No pillar city (nothing scores 9+); built on the
  D2 Budget 8 / D10 Community 8 cluster, with Safety 4 and Resilience 3 stated in the character
  section rather than buried. Carries an NRC callout under MEDIAN-HOME-METHODOLOGY v1.2 (citywide
  $326K vs retiree-target hoods $500K-$790K) despite not being one of the ten legacy NRC cities.
  Savannah is on TWO lists (arts-lovers, budget); it is a documented near-miss on foodies.
  Built with `lists-grid` (2 cards), not `lists-grid-four`: see the undefined-class bug below.
  OPEN: DB scores Savannah D1=5, but SAV runs 38 nonstops on 9 airlines, which the rubric's own
  anchors put at 6-7. Score NOT changed; prose written consistent with a 5. Worth a D1 review.
- Jul 14, 2026: Visit-block rollout COMPLETE. All 43 live profiles carry a Visit block.
- Jul 9, 2026: Knoxville deployed; v1.3 canonical + docs deployed; St. Paul DB fix done.
