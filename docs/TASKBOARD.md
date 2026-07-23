# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 23, 2026, second push (em-dash check rebuilt to count every RENDERING of the
character, planted-error tested; 83 live em dashes converted across `pick-and-compare.html` and four
profiles' JSON-LD; DB `Highlight` COLUMN DELETED and bumped to **v16_6**; new
`check_highlight_surfaces` gates the two remaining copies against each other; 72 stale D2 scores
found on `pick-and-compare.html`, boarded below)

**Verified live at last update:** 44 profiles, 20 comparison pages, 5 guides, 7 landing pages.
All 44 profiles carry a Visit block. Validator: **0 failures, 0 warnings** as of the Jul 21 fixes,
on the bare (live GitHub) run. NOTE: the Jul 19 board asserted 0/0 on BOTH `--local .` and bare, but
the Jul 21 bare run found a superlative FAIL that had been live since Jul 19, so that claim was wrong.
Treat any 0/0 line here as stale until re-confirmed by a fresh run. The warn queue reaches zero because
`docs/SUPERLATIVE-LEDGER.md` retires reviewed outside-world claims; anything NOT in the ledger is
unreviewed and shouts. Zero is now the expected reading. If a warning appears, it is new.
The validator now ALSO carries a pros/cons home-figure check (folded into the `figures` group).
As of Jul 18 it ships **FAIL**, not WARN: the Jul-15 34-figure reconciliation held, both `--local .`
and the live bare run read 0 pros/cons warnings, so drift now blocks the gate like every other
figures check. Planted-error tested (Knoxville `$327K` against DB `$368,000`: 1 failure, exit 1).
As of Jul 23 the `figures` group ALSO covers home figures in `highlight` PROSE, on both
`index.html` and `pick-and-compare.html`. Also **FAIL**. Planted-error tested by
`tools/test_highlight_homes.py` (15 assertions, run it after any edit to the `HL_*` patterns).
Exact match, no tolerance band: a figure in thousands must equal `round(DB/1000)`.

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

- **OPEN QUESTION carried out of the Jul 23 check: are the six non-NRC prose figures a second data
  vintage?** Casper, Columbus, Des Moines, La Crosse, Roanoke, Sioux Falls all quoted prose figures
  ABOVE `Median Home`, and the consistent direction still suggests a vintage rather than random
  drift. They were edited DOWN to the DB because the data-source rule makes the DB canonical and
  because a shipped FAIL gate cannot sit red. If the prose was in fact the newer vintage, the fix is
  to correct the DB and let the check re-derive the prose, NOT to revert these edits. Settle it
  before the next DB bump. Philadelphia's profile separately contradicts itself: "citywide typical
  home value is around $234K" against $240K elsewhere in the same file - the profile surface is not
  yet covered by any home-figure check. CONFIRMED and extended Jul 23: a scan of profile JSON-LD
  against `Median Home` found Philadelphia $234,000 vs DB $240,000 (twice, in two FAQ answers) and
  New Orleans $246,000 vs DB $250,000. Both cities' HIGHLIGHTS carry the correct DB figure on both
  surfaces, so this is the JSON-LD alone - the surface search results are built from. This is the
  concrete instance of the already-open "extend figure cross-checking to profile stat cards and FAQ
  JSON-LD" item.

- **LIVE: `pick-and-compare.html` carries 72 stale D2 (Affordability) scores.** Found Jul 23 while
  syncing highlights. Every one of the 99 cities was compared on all ten dimensions across the two
  surfaces: 72 disagree, all of them D2, and in **every single case `index.html` matches the DB and
  `pick-and-compare.html` does not** (Alexandria 3 vs 5, Asheville 5 vs 7, Boise 4 vs 6, Charlottesville
  4 vs 6, and 68 more). D2 is a scored, sorted, checkmarked row on the comparison tool, so the tool is
  ranking cities on affordability using numbers the database disowns. NOT touched in the Jul 23
  em-dash push, deliberately: one confirmed change per deploy, and this is its own change. Take it
  next. The fix is mechanical (adopt the DB value) but it must be gated afterwards, by extending
  `check_highlight_surfaces` from the highlight field to the score block, or the same drift reopens.

- **RESOLVED Jul 23 by deleting the column.** The question was which surface the DB `Highlight`
  column was the master of. The answer was neither: nothing read it, nothing validated it, and it
  disagreed with `pick-and-compare.html` on 16 rows, with `index.html` on 67, while the two HTML
  surfaces disagreed with each other on 65. Three copies, three answers, no arbiter. The column is
  gone as of v16_6 and the two surfaces that actually render are now gated against each other by
  `check_highlight_surfaces`. Same reasoning as `check_affiliate`: the HTML IS the record, and a
  half-current reference is worse than none because eventually someone trusts it.

- **Two live em dashes sit on pages the `emdash` check has never scanned.** `privacy.html` line 12,
  in the `<title>`, and `scouting-trip-workbook.html` line 1020, in a rendered `<span>`. Neither page
  is in the check's target list, which is the FOURTH axis of the same blind-spot family (surface,
  target membership, spelling, and now coverage). Left alone in the Jul 23 push on purpose: adding
  them breaks the invariant that push was verified against, which was that every page except the five
  being converted reads zero. Small job: add both to the named target list, convert the two, re-run.
  The check now fails loudly on a named target that matches no file, so the list can be trusted once
  it is right.

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

- **Validator: build the profile stat-card + FAQ figure check.** The 13 drifted figures are now
  reconciled (see RECENTLY SHIPPED), so this can be built against a clean tree. Three things the
  audit proved the check needs, each of which cost a wrong answer while sizing the job:
  (1) a HEDGE SLOT between the noun and the figure. The existing `PROSCONS_HOME` matcher requires them
  adjacent, but the profile voice is "the typical home value in Columbus IS AROUND $249,000". Reusing
  the pros/cons matcher as-is covers 13 of ~45 home figures and reports a near-clean surface.
  (2) a money token anchored to end on a DIGIT. A class ending `[\d.,]+` swallows the sentence comma
  and drags the other-place guard a clause forward, which is exactly how St. Louis hid behind an
  unrelated "suburbs".
  (3) the other-place guard bounded to the SAME clause, so it still skips Bentonville's Bella Vista
  figure and Tampa's Water Street range without excusing a real citywide drift.
  Also still unguarded: the stat card's ABBREVIATED monthly (`$4.9-6.1K/mo`) - `RANGE_RE` only knows
  the `$4,900-$6,100` long form, so all 43 monthly stat cards are unchecked; and the two variable stat
  slots, which carry real dimension scores under ~20 labels (Healthcare, Outdoor, Walkability,
  Community, Safety, Airport Access, Tax Friendliness, Wellness, Budget Score). Six slot labels are
  non-DB facts (Founded, Elevation, Metro, Coastline, Weather, State Income Tax) and must stay unmapped.
  Planted-error test the whole surface: the audit pass caught 5 of 5 planted errors across both.

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

- **Next in queue:** Roanoke, then Tulsa.
- Live profiles: 44. San Antonio shipped Jul 19; Fort Collins, Prescott, Knoxville and Savannah
  shipped earlier in the same window.
- San Antonio carries a Neighborhood Reality Check callout, making it the 11th NRC city.
  `PROFILE-FORMATTING.md` still lists ten and needs updating.

---

## ACTIVE - comparison pages

Live: 20. Shipped since last board update: San Antonio vs Fort Worth, Knoxville vs Nashville, Fort Collins vs Boulder,
Knoxville vs Chattanooga, Bend vs Boulder, Bloomington vs Lexington, Madison vs Ann Arbor,
Madison vs Columbus, and others.

Unlocked and ready to build now (both cities live):
- **Knoxville vs Asheville**
- **Arizona three-way cluster** (Prescott now live, so this is unblocked)
- (Fort Worth vs San Antonio SHIPPED Jul 21, see RECENTLY SHIPPED)

Unlocks pending a build:
- (none)

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty)

---

## PARKED / BACKLOG

- **Four CityDatabase / index.html data conflicts on San Antonio, surfaced during the Jul 19 build.**
  Not fixed in the build chat because three of them touch shared surfaces, which makes them BATCH work:
    - DB `Highlight` says "Citywide median home $260K" while DB `Median Home` reads `$320,000` and
      `CITY_ENRICHMENT` scoreNotes D2 reads "~$320K". The Highlight string renders on
      `pick-and-compare.html` and the foodies landing card, so the site currently publishes two
      different medians for the same city. Worst of the four.
      **Jul 21: escalated out of PARKED. This is a seven-city cohort bug, not a San Antonio bug.
      See the top of ACTIVE - batch / site-wide operations.**
    - DB `PropTax Rate %` = 1.4 for San Antonio. External sources put Bexar County effective rates at
      1.55% to 1.96%, and index.html cons/scoreNotes already publish ~1.8%. The profile shipped with
      1.8% for internal consistency. The DB field is the thing to fix.
    - DB `Budget Range` = 2, but `Monthly Est` `$5,100-$6,400/mo` puts the midpoint in Range 3.
    - `CITY_ENRICHMENT["San Antonio"].scoreNotes.DW` says "Jan avg 44 F"; DB `Jan Mean F` = 52.
- **San Antonio landing-page placements: Healthcare Tier 2 and Arts Lovers Tier 2.** BATCH scope.
  Neither scoring-analysis doc evaluated the city at all (zero mentions), so these are omissions, not
  rejections. Healthcare Tier 2 is defined as "major university medical center or state flagship";
  San Antonio has University Hospital plus UT Health San Antonio with the Mays Cancer Center holding
  NCI designation, the same credential that places Miami in Tier 2. Arts Tier 2 runs 8.3 to 8.8;
  San Antonio reads 8.3 to 8.5 against Fort Worth at 8.4. Touches five files: the two landing pages,
  the two scoring-analysis docs, and a return trip to `cities/san-antonio/profile.html` to take the
  Lists section from 2 cards to 4.
- **`PROFILE-FORMATTING.md` NRC list is stale at ten cities.** San Antonio is the eleventh.
- **Validator superlative check matches `on this list` literally and fires on within-page lists.**
  Caught `cities/san-antonio/profile.html` ("the most genuinely urban option on this list") on Jul 21,
  where "this list" meant the four neighborhood cards in the same section, not the city dataset. The
  claim does not rot when a city is added, so this is a scoping false positive. Two sibling phrases in
  the same section ("the most expensive of the inner-loop municipalities", "the most house per dollar
  of the retiree-target areas") pass, which confirms the check is keying on the string and not the
  shape. Copy was rewritten rather than the check loosened. If the pattern is scoped later, it needs a
  planted-error test first.
- **`scripts/generate_brief.py` is referenced by the `retiremehere-city-profile` skill but is not in
  the repo** (404 on raw). The Jul 19 brief was computed by hand against the thresholds documented in
  the skill. Either commit the script or amend the skill; as written it points the next build at a
  file that is not there.
- **Landing-page card counters are positional, not ranks.** `top-cities-for-foodies.html` numbers
  restart at 1 per tier and each tier is alphabetical, so the on-page number never has to match the
  scoring-analysis doc's rank. Recorded because it was raised as a discrepancy during the San Antonio
  build and was not one.
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

- Jul 23, 2026 (second push): EM-DASH CHECK REBUILT + DB `Highlight` COLUMN DELETED (**v16_6**).
  `docs/CityDatabase_Jul_23_v16_5_highlights.xlsx` -> **`docs/CityDatabase_Jul_23_v16_6_nohighlight.xlsx`**;
  `DEFAULT_DB` and the SITE-OPERATIONS-LOG "Current:" line updated in the same commit, old file
  deleted before the gate ran.
  `check_emdash` counted ONE SPELLING of the character, so 85 escaped em dashes were live while the
  gate read 0. It now counts every rendering that reaches a reader: the literal character, `\u2014`,
  `&mdash;`, `&#8212;`, `&#x2014;`. Two of the 85 turned out to be regex character classes
  (`/[\u2013\u2014\-].*\$/`, twice in `pick-and-compare.html`), which are code doing the right thing,
  so whitespace-free bracket groups are excluded and named as a third deliberate exclusion alongside
  `<style>` and the short `'\u2014'` UI placeholder. Real count was 83, not 85.
  Converted: 61 on `pick-and-compare.html` and 22 in the JSON-LD of New Orleans, Philadelphia, Salt
  Lake City and St. Louis (4 of those were the `headline` separator, brought into line with the colon
  the other 44 profiles already use).
  The page conversion turned out to be already written. `index.html` was swept Jul 13 and
  `pick-and-compare.html` was missed, so the two surfaces had disagreed on 65 of 99 highlights ever
  since, silently. All 99 were synced from `index.html`, which is newer on every one of the 24 rows
  that differed by more than punctuation (the `median home` -> `typical home value` sweep, the Jul 12
  superlative sweep, and corrected figures for Boulder, Bentonville and New Orleans).
  The DB `Highlight` column is deleted rather than converted. It was a master nothing read: `load_db()`
  never touched it, no tool consumed it, no check validated it, and it disagreed with both surfaces.
  Deleting it also retired, at zero cost, the twelve banned dataset-scoped superlatives sitting in it
  (Fayetteville AR, Carmel-by-the-Sea CA, Santa Barbara CA, Vail CO, Delray Beach FL, Boise ID,
  Paducah KY, Beaufort NC, Johnson City TN, Corpus Christi TX, Jackson Hole WY, Burlington VT), plus
  Chattanooga's unanchored "Best value city in the Southeast", plus two cells that contradicted the
  `Median Home` in their own row (New Orleans $267K vs $250,000, Tulsa $245K vs $194,000).
  NEW CHECK: `check_highlight_surfaces`, in the `figures` group, fails when the same city's highlight
  differs between `index.html` and `pick-and-compare.html`, byte for byte. It is what makes "one
  record" true rather than aspirational, and it would have caught the em-dash gap on the day it opened.
  Tested: `tools/test_emdash_forms.py` NEW, 10/10 (escape form caught; `<style>` silent; short
  placeholder silent in both spellings; regex character class silent; prose beside a character class
  still caught; entity forms caught; a named target matching no file fails loudly).
  `tools/test_highlight_homes.py` extended to 18/18, with three plants for the new check. Its older
  assertions were retightened rather than loosened: a single-surface plant now legitimately trips two
  checks, so each assertion names what it expects from each.
  Column removed as inline strings in `xl/worksheets/sheet1.xml` and rezipped; no openpyxl, no pandas.
  Verified: every other zip part byte-identical, part order preserved, only `Highlight` gone,
  0 data cells changed outside it, `load_db()` output identical old vs new.
  Gate: `python3 tools/validate.py --local .` reads PRE-DEPLOY GATE, **0 failures, 0 warnings**.

- Jul 23, 2026: DB `Highlight` COLUMN RECONCILED. `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` ->
  **`docs/CityDatabase_Jul_23_v16_5_highlights.xlsx`**; `DEFAULT_DB` and the SITE-OPERATIONS-LOG
  "Current:" line updated in the same commit, old file deleted.
  Running the freshly shipped `HL_*` matcher over the column found **16 drifted home figures**, and
  it was a DIFFERENT 16 than the two HTML surfaces carried. The column was a pre-Jul-23 vintage: it
  still held every NRC citywide figure from before that sweep, including **Wilmington DE at $215K
  against a `Median Home` of $321,000** - the exact string used as the planted error in
  `tools/test_highlight_homes.py`, sitting live in the master the whole time. Also stale: Memphis
  $170K/$195K, San Antonio $260K/$320K, Philadelphia $270K/$240K, Pittsburgh $265K/$240K, St. Paul
  $280K/$297K, St. Louis $250K/$235K, Indianapolis $223K/$224K, Miami $430K/$575K, plus the six
  non-NRC cities and Provincetown.
  One extra fix in the same pass: Miami's cell opened "The only city in the database with all four
  major pro sports leagues" - a dataset-scoped superlative, banned since Jul 12, sitting in the
  master where a regen would have pushed it back onto the site. Now "A rare city with all four major
  pro sports leagues," matching both surfaces.
  Edited as inline strings in `xl/worksheets/sheet1.xml` and rezipped; no openpyxl, no pandas.
  Verified: every other zip part byte-identical, the other four sheets row-identical, `load_db()`
  output identical across old and new (so no score, monthly, home value or tier moved), exactly 16
  rows changed, exactly one column touched, and 0 drifted figures on the re-read.

- Jul 23, 2026: HIGHLIGHT HOME-FIGURE CHECK SHIPPED. `check_highlight_homes()` in
  `tools/validate.py`, folded into the `figures` group, **FAIL** not WARN. Holds every home figure in
  `highlight` prose to `Median Home` on both surfaces: `index.html` (JS object literals) and
  `pick-and-compare.html` (single-line JSON under `const CITIES =`), parsed separately because they
  are not the same format. Exact match, **no tolerance band** - a figure in thousands must equal
  `round(DB/1000)`. A band was the whole reason the nine hid: 3% forgives Casper's $275K against
  $273K and does not forgive Des Moines' $217K against $191K, and both are equally false.
  Scope is ANCHORED, not blanket: a figure counts only when attached to a home-value noun. That one
  rule keeps three legitimate shapes silent forever - the NRC neighborhood range, the cross-city
  reference (Tampa naming Naples' figure), and figures that are not homes at all (Tulsa's $465M
  Gathering Place, Traverse City's $132K deduction, Provincetown's $2M estate cliff). A cross-city
  veto sits behind the anchor for the day someone writes "Naples' median home is $585K" inside
  Tampa's string. Bounds are checked as bounds, not equalities.
  **16 failures on the unpatched tree, all real**, all reconciled to the DB in the same push:
  `index.html` 9 (Des Moines, Sioux Falls, Casper, Columbus, Roanoke, Miami, La Crosse, Boulder,
  Provincetown), `pick-and-compare.html` 7 (Des Moines, Columbus, Sioux Falls, Roanoke, Casper,
  La Crosse, Provincetown). Sioux Falls carried TWO DIFFERENT wrong figures, $333K on one surface and
  $285K on the other, against a DB $314,000. Roanoke's was a false BOUND, "median homes under $230K"
  against $251,000. Provincetown's $2.1M was resolved to $924K, which is what its own `D2` modal
  already said, sourced to Boston Globe / Warren Group April 2026 - so the $2.1M was simply wrong and
  the earlier $326K paste is already gone.
  Planted-error tested by `tools/test_highlight_homes.py`, 15 assertions, all passing. The plant is
  the bug that actually shipped: Wilmington DE's highlight at `$215K` against a DB `$321,000`, one
  failure, exit 1. Test 3 is the (City, ST) key guard - Wilmington NC carrying its own $418K must be
  silent AND Wilmington NC carrying DE's $321K must fail, which is only true if the lookup keys on
  state. That is the Jul 21 mistake, now mechanically prevented. Test 6 plants a renamed `CITIES`
  array and asserts the check fails LOUDLY rather than scanning nothing and reporting a clean site.
  Files: `tools/validate.py`, `tools/test_highlight_homes.py` (new), `tools/README.md`, `index.html`,
  `pick-and-compare.html`, this board. Validator 0 failures, 0 warnings, exit 0 on `--local .`.

- Jul 23, 2026: NRC HIGHLIGHT PROSE RECONCILED with `Median Home`. Recorded on this board as seven
  cities; the actual count was **nine** across **two** surfaces - the board omitted New Orleans and
  Tulsa, and the `pick-and-compare.html` surface it flagged had never been swept.
  `index.html`: 9 highlight figures, the Indianapolis $223K/$224K rounding, and the St. Louis
  stat-card `sub`, which read "Citywide $250K" while its own `methodologyNote` two lines below said
  $235,000. `pick-and-compare.html`: the same 9 figures, plus Indianapolis, Wilmington DE and
  St. Paul still holding pre-v1.2 retiree-target values in `medianHome` / `medianHomeMid` /
  `monthlyEst` (two stored as ranges, which v1.2 abolished). `medianHomeMid` drives the comparison
  sort, so Indianapolis had been sorting at $432,000 against a real $224,000 - that one corrupted
  output, not just copy. Also two $100 monthlyEst drifts (Burlington, Nashua). City profiles audited
  clean. Both patches idempotent with abort-on-miss; validator 0/0 exit 0 on `--local .`.
  **CORRECTION to the Jul 21 entry:** it listed Wilmington DE `Median Home` as $418,000, an apparent
  $203,000 gap. $418,000 is **Wilmington NC**. The measurement matched on city name without state.
  True DE figure is $321,000 and the real gap was $106,000. Two Wilmingtons in the DB, and two
  Columbuses - always key on (City, ST).

- Jul 21, 2026: SAN ANTONIO vs FORT WORTH comparison page shipped (page 20). Built from a live pull of
  `st-louis-vs-kansas-city-retirement.html`; all scores, Monthly Est, Median Home, tier, property tax
  and insurance read from `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` rows 73 and 75. Four files:
  the new page, `sitemap.xml`, `compare-retirement-cities.html` (new Texas hub region + ItemList
  position 20), and `cities/fort-worth/profile.html`.
  **Zero checkmarks on the whole table, and that is the finding, not an omission.** All ten dimensions
  are a tie or a one-point gap: five exact ties (D2, D3, D4, D6, D8), San Antonio +1 on D5/D7/D9/D10,
  Fort Worth +1 on D1. Cost rows are $20,000 and $200/mo apart with identical tier, property tax and
  insurance, so the two cost rows were left unmarked as well rather than manufacturing separation
  the data does not support. The D9 row is disclosed in prose as apples-to-oranges: San Antonio is
  scored on retiree-target areas (three of which are independent municipalities with their own police
  departments), Fort Worth citywide.
  Two deviations from the template, both deliberate: the climate row is labelled "Summer comfort
  (higher = milder)" rather than the template's inverted "Hot summers (lower = milder)", so the page
  does not propagate the known `knoxville-vs-chattanooga` label bug (both cities score 3, so it is
  invisible either way); and the caption carries a property-tax variance note because the DB ships the
  Texas state average while the San Antonio profile publishes a Bexar-specific 1.8%.
  `cities/fort-worth/profile.html`: Tulsa removed from the related-cities grid and replaced with San
  Antonio. Tulsa was the only one of the three with no live profile, so the card dead-ended at the
  matcher, and its `related-card-why` text was a verbatim duplicate of Memphis's. Kansas City's
  "The closest overall match" line was also rewritten, since San Antonio now holds that position.
  Deployed by drag-and-drop through the GitHub web UI rather than Codespaces, so `--local .` was not
  run as a pre-deploy gate; structural checks (tag balance, JSON-LD parse, sitemap XML, em-dash count,
  banned-superlative scan) were run on all four files before upload and the bare live validator was
  run after.
- Jul 21, 2026: PRE-EXISTING SUPERLATIVE FAIL CLEARED IN `cities/san-antonio/profile.html`. The bare
  live validator run after the comparison-page deploy returned 1 failure + 1 warning. Neither came
  from the deploy. The failure was the King William hood-card reading "the most genuinely urban option
  on this list", live since the Jul 19 San Antonio ship and never caught because live mode had not
  been run since. Rewritten to "the most genuinely urban of the four retiree-target areas here". The
  warning was this board asserting 19 comparison pages against 20 live, cleared by this update.
  **Process note: the Jul 19 board claims validator 0/0 confirmed on both `--local .` and bare. The
  bare run cannot have covered the San Antonio profile, or it would have failed then.** Worth
  distrusting that line and re-running bare mode before relying on any 0/0 claim on this board.
- Jul 19, 2026: SAN ANTONIO, TX SHIPPED. Profile 44. Built from a live pull of
  `cities/st-louis/profile.html`; all scores, Monthly Est and Median Home read from
  `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` row 75. Carries an NRC callout (11th NRC city), a
  Visit block with live per-city Expedia and Vrbo codes, and the Visit chip wired into the scroll-spy
  ids array. No landing-page edits were needed: existing foodies and urban-walkabout cards already
  routed through `index.html?city=San Antonio&state=TX`, and `CITY_ENRICHMENT` plus the `cities[]`
  object already existed, so `index.html` took a single `PUBLISHED_PROFILES` line. The pre-publish
  rubric check caught a false UNESCO claim in the draft (see ops log).
- Jul 18, 2026: PROFILE FIGURE DRIFT AUDITED AND RECONCILED. 13 fixes across five city profiles. The audit was
  scoped to stat cards + FAQ JSON-LD and found 5 figures in 4 cities; reading each one IN CONTEXT before
  editing showed the scope was wider, and the failure was worse than "a stale schema field": three
  profiles CONTRADICTED THEIR OWN STAT CARD.
    - `columbus` 8 fixes. Stat card read `$235K` while EIGHT other places on the same page read `$249K`:
      meta description, og:description, JSON-LD Article description, two FAQ answers, hero tagline, a
      fit-list bullet, and a fast-fact box. The meta description is what Google shows in results, so
      the stale figure was the most publicly visible number on the page.
    - `st-louis` 2 fixes. FAQ `$250,000` and the "Reading the numbers here" callout `~$250K`; stat card
      already read `$235K`.
    - `tampa` 1 fix. FAQ `$377,000` -> `$400,000`. The Water Street hood-card range `$377K-$800K` is a
      NEIGHBORHOOD figure and was deliberately left alone.
    - `pensacola` 1 fix. Stat card Budget Score `7/10` -> `8/10` (DB D2 = 8).
    - `st-paul` 1 fix. Stat card Monthly Budget `$3.8-5K/mo` -> `$4.7-5.9K/mo`, already contradicted by
      its own FAQ, which read `$4,700 to $5,900`.
  In every case `index.html` and the DB agreed and the PROFILE was the stale side, so nothing in the
  matching engine was affected. Applied with an abort-on-count-mismatch batch. Verified: 0 leftovers of
  the old figures, JSON-LD parses on all five, 0 rendered em-dashes introduced, gate 0 failures /
  0 warnings, and both audit passes re-read zero. LESSON: the audit surface was too narrow. A figure
  that drifts drifts EVERYWHERE it was typed, including meta and og tags that no on-page read catches.

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
