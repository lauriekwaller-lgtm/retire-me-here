# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 28, 2026, validator `layout` group shipped (OPS. New check
`check_stray_artifacts` plus `tools/test_stray_artifacts.py`, 7 planted-error assertions.
It fails on a `<city>-profile.html` or `<city>-hero.jpg` at the repo root, any zip at the
root, rename debris or a missing photo inside `cities/<slug>/`, and a `cities/` directory
that yields nothing. Run it with `--only layout`. Local mode only: it asks what is on disk,
and a bare run cannot list a directory over HTTP, so it is skipped rather than faked in the
post-deploy run. Cause it addresses: every other check reads the CONTENT of a file whose
path it already knows, which left a file with the wrong NAME in the wrong PLACE unwatched.
A build chat delivered the pre-July-14 hand-off shape three times between Jul 25 and Jul 28,
loose `casper-profile.html` and `casper-hero.jpg` to rename by hand, and the gate read 0/0
each time. The skill file was the leak: it lives outside the repo, so section 4a and the
enumeration rule cannot keep it current, and it still specified a shape DEPLOY-CHEATSHEET.md
superseded on Jul 14. Skill rewritten to delegate rather than restate. One item boarded,
see below.)

**Previously:** July 27, 2026, cleanup batch (BATCH: nine stale `Median Home` instances across
five profiles, the tail of the ZHVI rebase, plus board corrections. Salt Lake City `$525,000` and
`$525K` -> `$580K`, Columbus `$235,000` and the visible By the Numbers stat -> `$251K`, Nashville
`$460,000` -> `$437,000`, Kansas City `$250K` -> `$257K` in THREE places (prose, By the Numbers and
the NRC callout), Lexington `$333K` -> `$337K`. Kansas City and Lexington were not in the original
scope: they were surfaced by the post-edit verification scan rather than by hunting, and were folded
in because they are the same stat on the same surface, not a new line of inquiry. Verified before
editing: the monthly figures in the same sentences are all correct against v17, so this was home
value only with no cascade. Post-batch scan across all 46 profiles: zero home-figure disagreements
with v17 on either the JSON-LD or By the Numbers surfaces, and every JSON-LD blob parses.
Also corrected validate.py's usage text, which advertised `no PASS lines` when no check has ever
printed one, boarded since Jul 27 as "fix on the next validator touch" and missed by the last two
validator touches. Board corrections, which were the larger problem: the rebase item still read
NEXT JOB and still blocked Casper, when steps 1-3 had already shipped in v17; the Scottsdale item
still read as open after shipping this morning. Both closed. Nothing else touched, nothing new
investigated. Standing decision as of this session: findings get boarded, not fixed, and the board
is reviewed monthly rather than chased. The site's actual accuracy state after this batch is zero
known reader-visible wrong figures on any profile.)

**Previously:** July 27, 2026, nav batch (BATCH: the budget pillar is now in the site
menu. Added as "Budget-Conscious Retirees" (desktop `index.html`) and "For Budget-Conscious
Retirees" (everywhere else), sorted between Arts Lovers and Foodies, which is the order the
dropdown already followed once you ignore the leading "For". 40 files, 80 rows, 2 per file for
desktop and mobile. Option A of three considered: the item was RENAMED into the "Top Cities
For..." pattern rather than kept as "On a Budget", because every other item completes that
heading and "On a Budget" does not. Decided at the same time NOT to add the other three pillars,
Florida, Midwest and Avoid Natural Disasters: the location lists are thin against a 99-city
database and do not warrant menu placement yet. Also fixed rather than propagated: the budget
page already carried "On a Budget" in its own dropdown, alone among 87 files, sitting between
LGBTQ+ Retirees and Sports Fans, which is alphabetical under no reading. Those 2 rows were
removed and re-inserted correctly, which is the only deletion in the diff. Nothing hardcodes
markup: each file's own Arts Lovers row is cloned and its href and label swapped, so absolute
paths stay absolute on index.html and relative stay relative elsewhere, across all seven nav
variants. Verified: 40 files at exactly 2 rows each, every href resolves from its own directory,
every dropdown still alphabetical, diff is 80 insertions and 2 deletions and nothing else.
Gate 0/0, three harnesses. NOT touched, and this is the real finding: the nav is copy-pasted
into 87 files in SEVEN variants, and the 46 city profiles carry a stripped 3-link nav with no
dropdown at all, so they cannot receive menu items without a nav rework. Boarded below.)

**Previously:** July 27, 2026, budget-roster batch (BATCH: `best-places-to-retire-on-a-budget.html`
rebased on v17. Roster moved from a 31-card set to tier R1's 30. Four came off, Beaufort NC,
Pensacola FL, Rio Rancho NM and Sioux Falls SD, all now R2; three went on, Indianapolis IN and
Wilmington DE as coming-soon cards and San Antonio TX as a live card. Per the boarded Jul 27
decision the methodology prose moved in the SAME commit: the bar stopped describing the low end
of the published range, "starts under about $5,500", which admitted 47 cities and was the sentence
justifying all four departures, and now describes the CENTRAL estimate, "centers at $5,550 or below",
which is the basis the DB and quiz already use. R1 midpoints run $4,300 to $5,550 and R2 opens at
$5,600, so the band is cleanly separable and a reader can check the claim against the midpoints
printed on the cards. Verified before the edit: all 27 surviving cards already carried correct v17
monthly figures, so this was purely a roster and prose fault. Ranks renumbered 1-30, roster
alphabetical, 18 live and 12 coming-soon. Reciprocal link added: San Antonio's profile gained a
budget list card and moved from `lists-grid-four` to `lists-grid` per the 3-card convention.
Pensacola needed no reciprocal removal, its profile carries no list cards at all. Meta descriptions
corrected 31 -> 30, and "ranked by" changed to "measured by" in three places where it contradicted
the page's own "alphabetically, not ranked" one line below. Gate 0/0 on a fresh clone, both
harnesses ran. Shipped in the same commit, because it is the fix for the reason this rotted:
`check_roster` in validate.py, wired into the `cards` group, with `tools/test_roster.py` as its
planted-error test at 7 assertions. `check_cards` only ever asked per-card questions, so the page
could be wrong about WHICH cities belong while every card on it was individually correct, and the
gate confirmed that by passing the stale page at 0 failures. Run the new check against the PRE-batch
page and it reports 7 failures naming exactly the four extras and the three omissions. Also cleared
the boarded Scottsdale fossil: the `Mullett` entry and the `5+ teams` pill, both left over from the
Coyotes' 2024 move to Utah, corrected on the sports page and in the scoring doc to `4 teams`.
Four leagues still clears the Tier 1 bar of "4 or more", so placement did not move. Two new faults
found en route and boarded below, neither shipped: the Florida and Midwest pillars parse to ZERO
cards inside `check_cards`, and the Florida pillar carries a stale comparison passage on three
surfaces whose fix changes an argument rather than a figure.)

**Previously:** July 27, 2026, batch (BATCH: three stale prose home figures corrected
and two unscanned pages brought under the `emdash` check. Philadelphia `$234K` x2 ->
`$237K`, New Orleans `$246K` -> `$248K`, matching v17 and matching the correct figure each
file already carried elsewhere. `privacy.html` and `scouting-trip-workbook.html` added to
the `emdash` named target list and their one em dash each converted. The feared sprawl did
not happen: both pages held exactly one, and a raw scan finds nothing further in either
file, not even in `<style>` or comments. Gate 0/0 on a fresh clone, both harnesses ran.
Three planted-error tests confirm the two new targets are genuinely scanned rather than
silently clean, including the escaped `&mdash;` form. Note what this does NOT close: the
coverage gap that let the three figures live is still open, see the item below.)

**Previously:** July 27, 2026, latest (OPS: VALIDATOR HARNESS REPAIR SHIPPED, commit
`b13edf1`. `tools/test_highlight_homes.py` no longer hardcodes home figures; it reads them from
the DB at runtime through validate.py's own loader, so the next annual ZHVI refresh cannot break
it again. Both harnesses are now a `harness` check group and gate the deploy. Gate 0/0 on a fresh
clone; bare post-deploy run also 0/0 on live main. Two things the board did not have: the harness
hardcoded TEN figures, not nine - Wilmington NC sat at $418,000 against a v17 $423,000, which would
have failed test 3 silently once the crash cleared - and one of the 18 assertions was passing
vacuously, matching nothing at all. Both fixed.)

**Previously:** July 27, 2026, later (OPS: BUDGET-METHODOLOGY.md made independently
reproducible. Exact per-state COL and Medigap multipliers written into section 6 as tables,
recovered from BudgetAuditJun162026.xlsx; section 4 snapshot date corrected to 2026-06-30;
section 5 healthcare range corrected to $924-$1,096; section 9 tier counts corrected to
30/29/19/12/9 and the stale quiz-rollout paragraph replaced. Verified: the formula now
reproduces all 99 rows of v17 exactly, both the Monthly Est string and the Budget Range
integer. Gate 0/0. Board swept: three items below were already dead and one was mislabeled.)

**Previously:** July 27, 2026 (OPS: ZHVI REBASE SHIPPED. `Median Home` rebuilt for all 99 cities
from the 2026-06-30 Zillow column; Monthly Est, Budget Range and D2 recomputed; every derived surface
figure re-derived. Three further faults found and closed en route: Monthly Est did not equal
f(Median Home) for 31 cities, `pick-and-compare.html` disagreed with `index.html` on d2 for 72 cities
(the boarded item, now closed), and seven carve-out fossils still framed cities on the retired
retiree-target-neighborhood basis. Validator 0/0.)

**Previously:** July 26, 2026 (board-only: six-city vintage question RESOLVED against the DB;
`Median Home` found to be a 2020-2026 patchwork never rebased, full audit boarded below; two
TASKBOARD header nits fixed. No content surfaces touched, no scores changed.)

**Previously:** July 25, 2026 (BATCH: Gilcrease Museum corrected on the arts landing card and
in the arts scoring doc; NRC fixed list removed from PROFILE-FORMATTING.md and
MEDIAN-HOME-METHODOLOGY.md, live count is 17 not 10; Tulsa property tax 0.77% -> 0.79% in
index.html; Wilmington DE phantom NRC entry removed. Four items boarded, see below.)

**Previously:** July 24, 2026 (Tulsa, OK profile shipped, profile 46; Tulsa card on
best-places-to-retire-on-a-budget.html promoted from coming-soon to a live link; two Saint Francis
"largest hospital" claims retired to the ledger. Earlier the same day: Roanoke, VA shipped as profile
45, with four stale Roanoke index.html figures fixed en route: $280K->$251K, hospital 16->15, D1
routes refreshed, D7 "Range 2"->"Range 1"; Carvins Cove second-largest-municipal-park claim retired)

**Verified live at last update:** 46 profiles, 20 comparison pages, 5 guides, 11 category pages
(7 `top-cities-for-*` plus 4 `best-places-to-*` pillars; the old "7 landing pages" line counted
only the first set).
All 46 profiles carry a Visit block with per-city Expedia and Vrbo codes (Roanoke's are still
placeholders pending Creator Hub; Tulsa's are live).
Validator: **0 failures, 0 warnings** on `--local .`, confirmed on a fresh clone at commit
`b13edf1` (Jul 27 harness push). The bare (live GitHub) post-deploy run was also made at that
commit and also reads 0/0, so the outstanding bare run from the Jul 25 push is closed.
The validator now ALSO carries a pros/cons home-figure check (folded into the `figures` group).
As of Jul 18 it ships **FAIL**, not WARN: the Jul-15 34-figure reconciliation held, both `--local .`
and the live bare run read 0 pros/cons warnings, so drift now blocks the gate like every other
figures check. Planted-error tested (Knoxville `$327K` against DB `$368,000`: 1 failure, exit 1).
As of Jul 23 the `figures` group ALSO covers home figures in `highlight` PROSE, on both
`index.html` and `pick-and-compare.html`. Also **FAIL**. Planted-error tested by
`tools/test_highlight_homes.py` (now **18 assertions**, run it after any edit to the `HL_*` patterns).
Exact match, no tolerance band: a figure in thousands must equal `round(DB/1000)`.
As of Jul 23 the `figures` group ALSO carries `check_highlight_surfaces`, which fails when a city's
highlight differs between `index.html` and `pick-and-compare.html` byte for byte. Three of the 18
assertions cover it. And the `emdash` group counts every RENDERING of the character rather than one
spelling, with its own planted-error test, `tools/test_emdash_forms.py` (**10 assertions**).
As of Jul 27 BOTH test files run automatically as the `harness` check group, so the gate covers
them and you no longer have to remember. A gate run prints two extra lines:

    harness:  tools/test_highlight_homes.py 18/18 passed
    harness:  tools/test_emdash_forms.py 10/10 passed

If either line is absent from a gate run, the group did not execute; that is itself the failure.
Three ways the group fails, all planted-error tested: a failing assertion (named individually on
the gate, plus `17/18 passed`), a harness file that has been deleted, and a harness that exits 0
having run nothing.

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

- **Three stale home figures in profile PROSE: FIXED Jul 27. The GAP THAT ALLOWED THEM IS STILL
  OPEN.** Philadelphia `$234K` x2 -> `$237K` and New Orleans `$246K` -> `$248K`, both now equal to
  v17 and to the correct figure each file already carried elsewhere. Read the fix narrowly: three
  characters of drift were corrected by hand, and nothing was built that would catch the fourth.
  Profile prose remains outside every figures check. One detail the earlier framing got slightly
  wrong and worth keeping straight, because it changes what a covering check has to match: the
  three were described as visible BOLDED body copy, and two of them are, but Philadelphia's second
  (`that $234K figure is citywide`) sat in plain unbolded prose inside the same `<span>`. A matcher
  keyed to `<strong>` would have found two of three and reported the surface handled. Confirmed
  correct: none of the three was in JSON-LD. Real fix is the profile stat-card + FAQ figure check
  boarded below, which must reach prose, bolded or not.

- **Em-dash target list: two pages added Jul 27, two remain out, both already clean.**
  `privacy.html` and `scouting-trip-workbook.html` are now named targets and their one em dash each
  is converted (the `<title>` moved to the ` | RetireMeHere` form the other 88 titles use; the
  workbook label took a comma). The risk boarded against this job did not materialise: the workbook
  is long, but a raw scan of both files finds exactly one em dash each and nothing else, in any
  region, scanned or not. Nothing to defer.
  What the sweep turned up: only TWO top-level pages are still outside the target list,
  `visit-before-you-decide.html` and `where-should-i-retire-quiz.html`, and both already read zero
  on both surfaces today. Adding them is a two-line edit that converts nothing and closes the
  target-membership axis for the whole top level. Deliberately not done here, because a target
  added is a target that must stay true and this chat was scoped to two characters.
  Also unscanned and out of scope by nature: `scouting-trip-workbook.pdf`, a separate built
  artifact that no HTML check reaches. If it was generated from the HTML it now differs from it by
  one label. Worth a look next time the workbook is regenerated, not before.

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

## BOARDED - opened by the layout-check work (Jul 28)

- **Any doc that lives outside the repo is unwatchable.** Section 4a makes the repo
  canonical and the enumeration rule keeps repo docs honest, but `SKILL.md` sits in
  `/mnt/skills/user/` and this project's own instructions sit in project settings. Both
  restated the hand-off shape, both went stale on Jul 14, and neither could be caught by
  anything. The skill is now rewritten to delegate to the repo docs instead of restating
  them. **The project instructions still say the old thing** and should get the same
  treatment: they currently ask for `<city>-profile.html` and city-prefixed photos to
  rename at deploy time. Worth a periodic audit of both against the repo, since no tool
  can do it.

## ACTIVE - city profile builds

- **Next in queue:** open. Roanoke and Tulsa both shipped Jul 24.
- Live profiles: 46. Tulsa shipped Jul 24; Roanoke the same day; San Antonio Jul 19; Fort Collins,
  Prescott, Knoxville and Savannah shipped earlier in the same window.
- NRC city count: **17 profiles carry a callout**, not 10 and not 12. Both the June count and the
  Jul 24 "San Antonio makes 11, Tulsa makes 12" note were wrong. Closed Jul 25: neither
  `PROFILE-FORMATTING.md` nor `MEDIAN-HOME-METHODOLOGY.md` enumerates NRC cities any more. The
  enumeration of record is `grep -l 'reality-check-eyebrow' cities/*/profile.html`. Do not
  reintroduce a list in either doc.
- **Tulsa follow-ups:**
  - `pick-and-compare.html` carries Tulsa at `d2:7`; DB and `index.html` both say **D2 = 9**. Stale.
    Part of the 72-score job boarded Jul 23, not a Tulsa-specific fix.
  - Detail photo resolved Jul 24: Boston Avenue Methodist Church, CPacker at English Wikipedia,
    CC BY 2.0, credited on the image and in the footer with a license link and a cropped note.
  - Gilcrease Museum: CLOSED Jul 25 on both surfaces (landing card and scoring doc), marked as
    reopening spring 2027 rather than deleted, since the collection still earns Tulsa its arts tier.
  - `index.html` Tulsa property tax: CLOSED Jul 25, 0.77% -> 0.79% in both the pros bullet and the
    D5 scoreNote.

---

## CLOSED July 27, 2026 (ZHVI rebase) - shipped, see SITE-OPERATIONS-LOG 2026-07-27

- **`Median Home` is not one vintage. It is a 2020-2026 patchwork, and it has never been rebased.**
  Found Jul 26 while settling the six-city question above. Joined all 99 DB rows against Zillow's
  city-level mid-tier ZHVI CSV (91 join cleanly on name+state) and dated each DB figure by finding
  the month in the series it best matches:

  | vintage of DB figure | cities |
  |---|---|
  | 2020 | 1 |
  | 2021 | 5 |
  | 2022 | 26 |
  | 2023 | 20 |
  | 2024 | 18 |
  | 2025-26 | 21 |

  **The project started in April 2026. Every one of these values was entered within the last four
  months.** So they were not entered fresh and left to age; they were already stale on the day they
  were typed in. Cause is near-certain: the column was seeded from web research, and web research
  returns cached crawls, licensed snapshots, and articles quoting whatever was current when written.
  This was demonstrated live during the Jul 26 session, when a Zillow page in search results served
  Casper at $273,235 (a late-2022 value) while the CSV for the same RegionID said $314,485. The
  data-source rule was doing its job downstream; the leak is that the DB itself was seeded upstream
  of it from a dirty source.

- **Magnitude: a tail problem, not a collapse.** Median gap is +2.7%, 49 of 91 cities are within
  +/-5%, and **81 of 91 do not change D2 median-home band at all.** Ten move bands, of which only
  five have live profiles, and two of those are noise: Knoxville crosses $375K by $1,600, and
  New Orleans moves the favourable way (7-8 -> 9-10). Real review list is Charlottesville
  ($465K -> $528K), Ann Arbor ($489K -> $541K) and Columbus ($235K -> $251K). **D2 is not median
  home alone** (the rubric scores COL index and monthly cost too), so a band crossing is a flag for
  review, not an automatic rescore.

- **Live profiles carrying a figure stale by more than 8%** (7 of 41 matched): Tulsa
  $194K -> $223K (+14.9%, DB vintage ~Jul 2022, and this shipped as profile 46 on Jul 24 with an NRC
  callout built on it), Charleston $526K -> $598K, Roanoke $251K -> $285K, Charlottesville
  $465K -> $528K, Ann Arbor $489K -> $541K, Salt Lake City $525K -> $580K (DB vintage ~Aug 2021,
  the oldest on a live profile), Bloomington $296K -> $321K.

- **MOSTLY CLOSED Jul 27, 2026.** ~~NEXT JOB, own OPS chat: rebase `Median Home` from the ZHVI
  CSV.~~ **Steps 1-3 already shipped in v17 and nobody closed this**, so the board spent a week
  telling the next session to redo finished work and to hold Casper behind it. Verified against
  `CityDatabase_Jul_27_v17.xlsx`: every value this item lists as pending is already in the DB
  (Tulsa $223K, Charleston $598K, Salt Lake City $580K, Roanoke $285K, Charlottesville $528K,
  Ann Arbor $541K, Bloomington $321K, Columbus $251K, Casper $314K), all 8 non-joining city names
  normalised, `Median Home` is a single figure in all 99 rows with no ranges left, no row missing a
  `Monthly Est`, and St. Paul is now `$301,000` which also closes the separate St. Paul item.
  Step 4 finished this session: 43 of 46 profiles were already fully re-derived, and the last three
  (Salt Lake City, Columbus, Nashville) were fixed in this batch. **Step 5 is the only part still
  open** and is carried as its own item below. Original scope text kept below for the record.
  Not a BATCH item and not a
  BUILD item. Scope: (1) normalise the 8 cities that do not join on name (`St. Augustine`,
  `St. Petersburg`, `St. Louis`, `St. Paul`, `St. George`, `Coeur d'Alene`, `Hilton Head`,
  `Jackson Hole` - all spelling/abbreviation variants, none actually missing from Zillow);
  (2) rewrite `Median Home` for all 99 from the June 2026 column; (3) recompute `Monthly Est` via
  `BUDGET-METHODOLOGY.md`; (4) re-derive every prose and stat-card figure on the affected profiles;
  (5) review D2 on the ten band-movers. Ships a new DB version. **Do this before the next city
  build,** or the new profile is written against a stale figure and immediately needs editing.

- **Mechanism, not just the fix.** `MEDIAN-HOME-METHODOLOGY.md` v1.2 s1 says the figure is
  "refreshed annually" and the doc was established Jun 17 2026, so no annual cycle has been missed -
  the first one simply has not run. Worth deciding at the rebase whether the validator should carry
  a vintage check (flag any DB figure more than N% off the current CSV) so this surfaces on the gate
  rather than by chance. Same family as every other find this month: a value copied once with
  nothing re-checking it against source.

- **Casper is the intended next BUILD. UNBLOCKED Jul 27, 2026.** ~~It is 15% stale (DB $273K,
  actual $314K), build it after the rebase.~~ The rebase shipped; v17 carries `$314,000`. Nothing
  stands in the way of this build.

---

## CLOSED July 27, 2026 (validator harness repair) - shipped at `b13edf1`

- **`tools/test_highlight_homes.py` was broken on main. CLOSED.** It crashed on an assert because
  the rebase moved Wilmington DE from $321,000 to $336,000. Fixed, but NOT by swapping constants:
  every home figure in the harness is now read from the DB at runtime via `validate.load_db` /
  `validate.db_get`. Swapping nine constants would have bought until the 2027 refresh and no
  further - and by then the harness gates the deploy, so it would have taken the gate down with it.
  A fixture that names a number the annual refresh moves is a fixture with an expiry date on it.
  **It was TEN occurrences, not nine.** Wilmington NC was hardcoded at $418,000 against a v17
  $423,000. That one does not crash; it fails quietly, inside the two-Wilmingtons key guard whose
  whole job is to assert silence on NC's own correct figure. Fixing only the nine would have
  produced 17/18 and a confusing failure in the one test designed to catch city-key bugs.

- **Wire BOTH harnesses into the gate. CLOSED.** New `harness` check group, runs last (it shells
  out, and is the slowest group by a wide margin). Recursion is stopped twice over: the harnesses
  invoke `--only figures` / `--only emdash`, which excludes the group, and an `RMH_IN_HARNESS` env
  sentinel survives someone widening a harness's `--only` later. Runs in both modes, because these
  test the VALIDATOR's logic, not the live site. Costs about 7 seconds on a gate run.

- **One of the 18 assertions was passing vacuously.** The `cross-city reference` fixture read
  `" Naples matches it at $585K."`, which carries no home-value noun and so matched neither
  `HL_HOME_FIG` nor `HL_HOME_BOUND`. It matched nothing, therefore it was silent, therefore it
  passed - forever, and it never once exercised the `cross_city()` veto it is named for. Reworded to
  `" Naples' median home is $549K."`, the sentence validate.py's own `HL_*` comment says the veto
  exists for. Verified both ways: the old form matches nothing, the new form matches and is silenced
  only by the veto. **This is the harness's own stated failure mode found inside the harness.** When
  touching any planted-error fixture, confirm the regex actually MATCHES it before trusting a PASS.

- **`.gitignore` gained `__pycache__/` and `*.pyc`.** The harness now imports `validate`, which
  writes bytecode into `tools/`. With `git add -A` as the deploy convention, the next commit would
  have carried it.

- **Lesson for every future `apply-batch.py`: "is the old string gone?" is the wrong idempotency
  test.** The first cut of this batch used it, and three of its edits keep their anchor and add
  around it (a docstring line with a new line appended, a `def main():` with a block inserted
  before it). On a second run they matched again and applied twice. `edit()` now takes an explicit
  MARKER that exists only after the edit lands, and aborts if the marker is not in its own
  replacement. Verified 16/0 then 0/16 across repeated runs.

- **CLOSED Jul 27, 2026.** ~~Doc nit: validate.py's usage block advertises `--quiet` as hiding PASS
  lines that no check has ever printed.~~ Corrected to describe what `--quiet` actually suppresses,
  the `harness:` lines. Worth noting how long this took: the note said "correct on the next
  validator touch", and the next two validator touches both edited text within three lines of it
  and missed it. A boarded instruction attached to someone else's future action is the weakest
  form of a task. Original text below. validate.py's usage block still advertises
  `--quiet   # failures only, no PASS lines`, but no check has ever printed a PASS line. The two
  `harness:` lines are the first, and they do respect `--quiet`. Correct the usage text on the next
  validator touch.

---

## ACTIVE - boarded July 27, 2026 (validator blind spots found during the rebase)

- **CLOSED Jul 27, 2026 (shipped).** ~~`best-places-to-retire-on-a-budget.html` roster is stale against v17.~~ Shipped exactly as decided: roster = R1 (30), prose = central estimate, both in one
  commit. Delta as boarded proved correct against v17: off Beaufort/Pensacola/Rio Rancho/Sioux Falls,
  on Indianapolis/San Antonio/Wilmington DE, 31 - 4 + 3 = 30. Original text kept below for the record.
  The page was built off
  tier R1 (under v16.6, R1 was 33 and the page carried 31, missing only Indianapolis and Wilmington;
  nothing on the page was outside R1). R1 is now 30. The page therefore carries FOUR cities that
  left the tier - Pensacola, Beaufort, Rio Rancho, Sioux Falls - and is MISSING San Antonio, which
  dropped into R1 when its Median Home fell from $320,000 to $251,000. Per-city monthly figures on
  the page are all correct against v17; it is the roster that did not move.
  **Delta re-derived against v17 on Jul 27, use these numbers:** page carries 31 cards (18 live,
  13 coming-soon), R1 is 30. Four come OFF - Beaufort (now R2, $5,300 start), **Pensacola (now R2,
  $5,000 start, and this is a LIVE card for a Tier 1 profile, so removing it is an editorial call,
  not a mechanical one)**, Rio Rancho (R2), Sioux Falls (R2). Three go ON - Indianapolis
  ($4,300-$5,400), San Antonio ($4,700-$5,800), Wilmington DE ($4,700-$5,800); note Wilmington NC
  is R2 and must NOT be added. Net 31 - 4 + 3 = 30.
  The prose bar as written ("starts under about $5,500") admits **47** cities in v17, not 46 as
  first boarded. Note which way that cuts: the prose as written currently JUSTIFIES all four cities
  the tier says should come off. So this is not a stale roster against agreed prose; it is two rules
  that were never the same rule. Fix both in one pass or the page contradicts itself either way.
  **Decide before fixing:** the page's methodology block says the bar is "every city whose all-in
  monthly estimate STARTS under about $5,500". That describes the LOW end of the published range,
  not the central estimate the tier uses, and it admits 46 cities in v17 rather than 30. The prose
  and the tier have been describing different rules all along; the page only ever sat close to R1 by
  luck. Pick one basis and restate the prose to match, because a reader can check that claim against
  the numbers printed on the same page. Recommendation: keep R1, say "central estimate".
  **DECIDED Jul 27, 2026: keep R1.** The roster is tier R1 and the prose is restated to describe
  the CENTRAL estimate, not the low end of the published range. Rationale: R1 is the basis the quiz
  and the DB actually use, so the page then agrees with the rest of the site instead of inventing a
  private rule, and 47 cards is a worse page than 30. Consequence to carry into the fix: the
  methodology sentence must stop saying "starts under about $5,500", because that sentence is what
  currently justifies keeping Beaufort, Pensacola, Rio Rancho and Sioux Falls. Roster and prose move
  in the SAME commit; shipping either alone leaves the page contradicting itself.

- **CLOSED Jul 27, 2026 (shipped in the same commit).** ~~`check_cards` does not validate tier
  membership.~~ `check_roster` added, wired into the `cards` group, with `tools/test_roster.py`
  as its planted-error test, 7 assertions. Proof it works on the real fault, not just on plants:
  run against the PRE-batch page it reports 7 failures naming exactly the four extras and the
  three omissions. Only pages whose roster is a DB PREDICATE are in `DB_ROSTERS`, which today is
  the budget page alone. Test 5 is the one that matters longest: markup that yields zero cards
  fails loudly instead of comparing nothing.

- **Two pillar pages have no city cards at all, so `check_cards` reads them and finds nothing.**
  `best-places-to-retire-in-florida.html` and `best-places-to-retire-in-the-midwest.html` are both
  in the `check_cards` target list and both parse to ZERO cards: they use `bestfor-card` markup, not
  `city-card`. The check fetches them, iterates nothing, and passes. This is the silent-no-op shape
  the emdash harness already exists to prevent, sitting in a different check. Note this is NOT the
  same hole as the roster gap just closed: those pages carry no per-city cards to check, so their
  figures live in prose instead, and see the Florida item directly below for what that let through.
  Fix is a decision, not a patch: either bring their money prose under a check, or drop them from the
  `check_cards` list and say in the code why they are exempt. Leaving them listed-but-unread is the
  worst of the three, because the target list currently reads as coverage.

- **`best-places-to-retire-in-florida.html` carries a stale comparison passage, found Jul 27.**
  Not shipped in this batch: fixing it changes an ARGUMENT, not just figures, so it wants its own
  pass. The passage repeats on three surfaces: the JSON-LD FAQ blob, the `bestfor-why` card, and the
  visible FAQ answer. Against v17:
    - Pensacola home `$264,000` -> `$269,000`; "budgets from about $4,900" -> `$5,000`.
    - Delray Beach `$341,000` -> `$342,000`.
    - Fort Myers `$372,000` -> `$310,000`, a $62K move.
    - ORDERING IS NOW WRONG. The sentence reads "Delray Beach is next, then Fort Myers". v17 order
      is Pensacola $269K, Fort Myers $310K, Delray Beach $342K, so Fort Myers is second.
    - "Pensacola scores 8 of 10 on budget and sits in budget tier 1" is wrong twice: D2 is 7 and
      Pensacola is Budget Range 2 as of the rebase. Note this is the SAME departure that took it off
      the budget page in this batch.
    - "Fort Myers scores 6 and sits in tier 2" -> D2 is 7. So Pensacola and Fort Myers are now BOTH
      D2=7 and BOTH Range 2, which collapses the passage's whole contrast. That is the editorial
      call: the trade-off has to be rewritten around resilience and healthcare, since it can no
      longer be framed on a budget gap that no longer exists. Fort Myers D4=1 is still correct.
  Also flagged while in there, not a v17 error: the passage opens "Of the Florida cities scored on
  RetireMeHere, Pensacola is the cheapest". That is a rank scoped to our own dataset, which is the
  banned shape, and `check_superlatives` does not catch this phrasing. Anchor it to the figure.

- **The site nav is copy-pasted into 87 files in seven variants, and 46 of them cannot take a menu
  item at all.** Found while adding the budget pillar to the menu. There is no template, no include,
  no build step: every header is a literal copy. The variants differ in path style (absolute on
  `index.html`, relative elsewhere), in class names (`nav-dropdown-item` on 38 pages, bare `<a>` on
  `index.html`), in label form ("Arts Lovers" on index desktop, "For Arts Lovers" on all mobile and
  all other desktop), and in which top-level links are present (`index.html` alone carries "Plan a
  Visit"). Three consequences, in the order they will bite:
    1. The 46 city profiles carry a 3-link nav, Home / Top Cities For... / Find My Match, with NO
       dropdown. They did not get the budget item and cannot get any future one. Roughly half the
       site's pages are therefore permanently one menu behind, and a reader who lands on a profile
       from search sees a different site than one who lands on the homepage.
    2. `visit-before-you-decide.html` has flat links and no dropdown either, a seventh variant of one.
    3. Every future menu change is a 40-file edit that must be scripted, and any hand-edit
       reintroduces drift. The "On a Budget" entry that existed on exactly one page out of 87 is
       what that looks like after one occurrence.
  Nothing validates nav parity today, so none of this fails a gate. The cheap first move is a check
  that asserts every page's dropdown contains the same set of hrefs, which would have caught the
  single-page "On a Budget" the day it shipped. The real fix is one nav partial and a build step,
  which is a bigger call about whether this site stays hand-authored HTML.

- **Florida and Midwest pillar titles both claim "The 8 Best Places" and both render six cards.**
  Noticed while listing the pillars for the menu decision. Not verified further and not fixed: the
  count may be stale, or the pages may deliberately narrate 8 while carding 6. Worth ten minutes
  before either page gets promoted anywhere, since the title tag is what search results show.
  Note `check_hardcoded_counts` does not catch these, for the same reason it missed the "100-city
  database (v14)" string already boarded: the number is fused into prose it does not scan.

- **D2 band-mover review: the last open piece of the ZHVI rebase (step 5).** Three cities crossed a
  D2 median-home band when the figures were rebased and none has been reviewed: Charlottesville
  ($465K -> $528K), Ann Arbor ($489K -> $541K), Columbus ($235K -> $251K). This is a JUDGMENT task,
  not a mechanical one, which is why it keeps getting deferred: per the rubric, D2 weighs the COL
  index and monthly cost as well as median home, so crossing a band is a flag for review and not an
  automatic rescore. Two others move but need no thought: Knoxville crosses $375K by $1,600, and
  New Orleans moves the favourable way. Do this in a session where the rubric is open, not as a
  rider on something else.

- **Rubric v3.3.** `scoring_rubric_v3.2` is wrong in six places, four of which are already resolved
  elsewhere on this board: (1) budget ranges still published as Under $3,500 through $8,000+, when
  both the DB and the quiz use Under $5,500 through $9,000+; (2) the D1 hard-filter ladder, resolved
  Jul 18 as keep-generic-7, pairs with deleting dead `D1_THRESHOLDS` from index.html; (3) D4
  described as retired and folded into D2, when it is live as Climate Resilience & Insurance with 99
  of 99 cities scored and no anchors documented anywhere; (4) the Universal Methodology section still
  scopes D2 to retiree-target neighborhoods, which BUDGET-METHODOLOGY.md section 4 already calls "its
  fossil, struck 2026-07-13"; (5) consequently the D2/D6/D9 grouping must become D6/D9, since D9 IS
  still genuinely neighborhood-scored (Memphis and San Antonio both sit at D9=7 where the rubric's
  own anchor puts their citywide figures at 1-2); (6) the D2 data-source line reads "Zillow/Redfin"
  and should be Zillow ZHVI only.
  Also check while in there: D2's anchor bands key off median-home breakpoints at $250K / $375K /
  $525K / $750K, and 23 D2 scores moved in the rebase. Those bands were calibrated against the old
  patchwork column.
  **Structural question to settle first:** the rubric is the only governing doc NOT in the repo. It
  lives in project knowledge as a .docx. That is a direct conflict with the source-of-truth rule in
  SITE-OPERATIONS-LOG section 4a, and it is the likeliest reason this doc drifted further than any
  other: nothing pulls it, nothing validates it, no commit touches it. Ship v3.3 as markdown in
  `docs/`, not as another .docx.

- **MEDIAN-HOME-METHODOLOGY.md needs three lines and was deliberately not touched on Jul 27.**
  (1) Section 1 says the figure is "refreshed annually"; the first annual refresh has now actually
  run, so record the date and that it used the 2026-06-30 ZHVI column. (2) Note that the refresh is a
  column swap against a file already in hand, not research; section 6 currently reads like a research
  task ("pull current Zillow ZHVI for all 99 cities") and will mislead the next operator. (3) Section
  6's out-of-cycle triggers should record that this refresh fired OUTSIDE the June cycle and why
  (Memphis 33% off was the credibility trigger in practice); a doc that says "annual" with no record
  of an off-cycle run invites the next operator to wait until June. Separately, section 9 lists
  `/methodology.html` as a surface this methodology touches. It 404s and is not in the sitemap.
  Either build it or strike the line.

- **`check_highlight_surfaces` enforces highlight parity but not SCORE parity.** `pick-and-compare.html`
  carries its own JSON blob (`monthlyEst`, `monthlyMid`, `medianHome`, `medianHomeMid`, `budgetTier`,
  `d2`) and nothing held it to the DB, so d2 drifted on 72 of 99 cities unnoticed. All ten dimensions
  now agree across both surfaces, but nothing stops it recurring. Extend the check to every `dN` field
  plus the four cost fields. Planted-error test required.
- **A city whose name contains non-ASCII is invisible to the surface checks.** Coeur d'Alene is stored
  `Coeur d\u2019Al\u00e8ne` in the pick-and-compare blob, so name-keyed checks skip it. Its record was
  stale at $553K against a DB $611K and the gate read clean. Any check that joins the two surfaces by
  literal name has this hole.
- **The abbreviated stat-card money form is unparsed.** The editorial modal renders
  `value: '$3.5–4.8K<span>/mo</span>'`. The validator reads `$X,XXX–$X,XXX` only, so St. Louis sat at
  $3.5-4.8K against a DB $4,100-$5,200, wrong before the rebase and never flagged. Same hole for the
  `$192<span>K</span>` home form.
- **No vintage check on `Median Home`.** The rebase fixed the values; nothing prevents the column
  ageing into a patchwork again. Add a gate check that flags any DB figure more than N% off the
  current ZHVI CSV, as boarded on July 26. This is the mechanism fix, not the data fix.
- **A `Monthly Est == f(Median Home)` assertion would have caught 31 cities. Now unblocked.**
  The doc dependency is CLOSED as of the July 27 doc push: BUDGET-METHODOLOGY.md sections 5 and 6
  now publish the exact per-state multipliers as tables rather than ranges, and the formula is
  confirmed to reproduce all 99 rows of v17 exactly, zero mismatches, on both the Monthly Est
  string and the Budget Range integer. Nothing further is needed from the docs. What remains is
  building the check itself and its planted-error test. Asserting it on the gate makes an entire
  class of drift impossible. Highest-value single check on this board.
- **DB title cell still reads "100 cities"** against 99 rows, and `pick-and-compare.html` line 918
  still hardcodes "100-city database (v14)". Both invisible to `check_hardcoded_counts`.

---

## ACTIVE - boarded July 25, 2026 (BATCH: Gilcrease, NRC list, Tulsa PropTax)

- **CLOSED Jul 27, 2026 (shipped).** ~~`top-cities-for-sports-fans.html` Scottsdale card names a
  franchise that left in 2024.~~ Shipped in the roster commit: `Mullett` dropped from the card and
  the pill changed `5+ teams` -> `4 teams`, and the same fossil corrected in
  `docs/sports-fans-cities-scoring-analysis.md`. Placement checked before editing and did NOT move:
  Tier 1 requires four or more leagues and Cardinals, Diamondbacks, Suns and Mercury is four.
  **The open sub-question is answered: Cactus League does NOT count as a team.** It stays listed on
  the card as a genuine draw but is excluded from the count, which is what makes the pill 4 and not
  5. Original text kept below for the record. The
  card reads `Cardinals · Diamondbacks · Suns · Mullett · Mercury (WNBA) · Cactus League spring
  training` with a `5+ teams` pill. Mullett Arena was the Arizona Coyotes' venue; the NHL board of
  governors approved the sale and relocation to Utah in April 2024 and the Phoenix metro has had no
  NHL team since. The site already knows this, because the Salt Lake City card correctly reads
  `Mammoth`. Fix is two lines, not one, which is why it was boarded rather than shipped Jul 25:
  drop `Mullett ·` from line 584, and change the pill on line 586 from `5+ teams` to `4 teams`
  (Cardinals, Diamondbacks, Suns, Mercury). Decide separately whether Cactus League counts.
- **Memphis card and arts doc will go stale in autumn 2026.** `top-cities-for-arts-lovers.html` and
  `docs/arts-lovers-cities-scoring-analysis.md` both name `Brooks Museum of Art`. It is genuinely
  open in Overton Park today, so nothing was changed. It closes there in autumn 2026 and reopens
  downtown in December 2026 as the **Memphis Art Museum**. Two edits, both dated, both known now.
  Do them at the autumn close, not before.
- **Enrichment-vs-DB property tax is a category mismatch, not a set of bugs.** The Jul 24 board read
  "index.html says 0.77, DB says 0.79, one is wrong". The premise was wrong. `D5-TAX-METHODOLOGY.md`
  section 2 defines `PropTax Rate %` as **one value per state**, and the DB holds exactly one value
  per state across all 39 states. The `index.html` D5 enrichment carries **county or city** rates,
  several of which name their county in the prose (Nueces, Tarrant, Williamson, Escambia). A sweep
  of all 38 property-tax figures in the enrichment found 17 cities where the two disagree by design:
  Ann Arbor, Burlington, Charleston, Charlottesville, Corpus Christi, Delray Beach, Fort Myers,
  Fort Worth, Georgetown, Greenville, Miami, Naples, Pensacola, Provincetown, Sarasota, Tampa,
  Traverse City. None of these is a bug. Tulsa was the one real error only because it is the sole
  Oklahoma city, so there is no city-versus-state distinction to preserve, and 0.77 matched neither
  the state figure nor any sourced Tulsa county rate (which run 0.94% to 1.06%). **Open question,
  not a defect:** neither doc says the enrichment may hold county rates. Either write that down in
  `D5-TAX-METHODOLOGY.md` or add the `Local Tax Adj` column that doc already proposes.
- **Institution-status checks are still manual.** Gilcrease was caught twice by hand. The validator
  cannot know whether a named museum is open. Consider a thin `docs/INSTITUTION-WATCH.md` listing
  every named institution with a known status change and its date, so landing cards get checked on a
  schedule instead of when someone happens to notice.

---

## ACTIVE - comparison pages

Live: 20. Shipped since last board update: San Antonio vs Fort Worth, Knoxville vs Nashville, Fort Collins vs Boulder,
Knoxville vs Chattanooga, Bend vs Boulder, Bloomington vs Lexington, Madison vs Ann Arbor,
Madison vs Columbus, and others.

Unlocked and ready to build now (both cities live):
- **Knoxville vs Asheville**
- **Arizona three-way cluster** (Prescott now live, so this is unblocked)

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
      **Jul 23: CLOSED by deletion. The DB `Highlight` column no longer exists (v16_6), so there is
      no second median to conflict with. `Median Home` is the only DB home figure now, and both
      rendering surfaces are gated against it and against each other. The `PropTax Rate %` and
      `Budget Range` items below are untouched and still open.**
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

- Jul 27, 2026 (batch): STALE PROSE FIGURES + EM-DASH TARGET LIST. Six edits in five files
  through one idempotent `apply-batch.py`, marker-gated per edit rather than keyed to the old
  string being gone. Philadelphia `$234K` x2 -> `$237K`, New Orleans `$246K` -> `$248K`.
  `privacy.html` + `scouting-trip-workbook.html` added to `check_emdash`'s named list, one em
  dash converted on each. Gate: `PRE-DEPLOY GATE`, 0 failures / 0 warnings on a fresh clone,
  harnesses 18/18 and 10/10. Planted-error tested three ways, because a passing gate on a newly
  added target proves nothing on its own: a literal em dash planted in `privacy.html` fails, an
  ESCAPED `&mdash;` planted in the workbook fails (so the new targets run through
  `emdash_forms()`, not a literal scan), and a deliberately misspelled target name still trips
  the matched-no-file failure. Control run after each: 0/0.

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
