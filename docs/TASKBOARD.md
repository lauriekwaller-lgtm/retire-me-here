# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 31, 2026, `san-antonio-vs-fort-worth` rewritten (BATCH, Tier 1 page 2 of 4.
The board sized this one as "gap +145% AND San Antonio drops tier 2 to 1". Both true, and both
undersold it: the SIGN INVERTS. The page had San Antonio $20,000 more expensive than Fort Worth;
under v17 it is $49,000 cheaper and a full budget tier lower. Every sentence ordering the two on
price was backwards rather than stale. A second live error came out of the same read and has
nothing to do with cost rows: FAQ 1 claimed five exact dimension ties including budget, while the
page's own D2 row twelve lines above says 8 against 7. Four tie, and San Antonio wins budget. The
neighborhood-band argument survived untouched, every figure in it re-checked against both
profiles, so the page's CONCLUSION stands and only its premise was wrong. Baseline 35 to 32 over
eight pages.)

**Before that:** July 30, 2026, `st-louis-vs-kansas-city` rewritten (BATCH, step 3 of 3 and the
first Tier 1 page. The page was built on the two cities costing the same. Under v17 they do not:
the citywide gap is $65,000 where the page asserted $15,000, and the monthly estimates are $500
apart where it said $200. Tradeoff #2 was HEADLINED on "structurally identical", so the swap was
never available. The neighborhood argument survived and got sharper: St. Louis' retiree
neighborhoods run $420K to $575K against a $192,000 citywide figure, two to three times the
median, so the citywide gap favors St. Louis and the neighborhood FLOORS do not. Baseline 39 to
35 over nine pages. CTA debt unchanged at 11, because no profile links to this page, which is
itself the orphaned-comparison-page P1.)

**Before that:** July 30, 2026, Tier 3 of the comparison cost-figure repair shipped (BATCH, step
2 of 3. Eight pages, 30 quarantined table mismatches to zero, both ratchets lowered in the same
commit: COST_ROW_BASELINE 69 to 39 across ten remaining pages, CTA_COST_DEBT_BASELINE 21 to 11.
The finding is the SIZE. The board called Tier 3 mechanical at 30 figures, meaning the 30 table
cells the check counts; the actual edit was 184, because every table figure has three to fourteen
copies of itself in prose, in the FAQ, in the FAQPage schema and in the `og:description` meta, and
NONE of those copies is read by anything. `fort-collins-vs-boulder` alone carries the same gap
figure fourteen times. The check counts what it can see, and what it can see was 16% of the
defect. Three edits were not mechanical at all and are written up in the closed entry.)

**Before that:** July 30, 2026, the CTA cost-debt gate shipped (OPS, step 1 of 3 in the cost-row
repair. Two open items pull against each other: the orphaned-CTA P1 wants CTA blocks added to
roughly eleven profiles, and the cost-row P0 has 69 stale figures quarantined across eighteen
comparison pages. Wiring the first while the second is open sends readers into money the validator
already knows is wrong, and NEITHER item's check can see it happening, because one reads the
comparison page and the other reads nothing on the profile at all. The new check counts the EDGES
between them, 21 today, and ratchets both ways like the baseline it rides on. Nothing was found
wrong: this is a gate on a repair in flight, not a fix.)

**Before that:** July 30, 2026, comparison cost-row coverage shipped (OPS. The gate could not
see Typical home value, Estimated retiree budget or Budget tier on any of the 20 comparison pages,
and 18 of them had drifted, 69 figures. Not one D1-D10 score was wrong anywhere, which is the
finding: the rows under a check held, the rows beside them did not. Also fixed dimension-label
matching, which had silently skipped D4, D8 and D10 on every page since the check shipped. The 69
are quarantined in a two-way ratchet and repaired in tiers, see the P0. Note this lands on top of
the same-day lists-heading batch from a parallel session; that batch boarded a
`check_lists_heading_count`, which is the same defect class as this one, a page asserting something
about itself that nothing reads.)

**Before that:** July 30, 2026, lists-section heading counts corrected on six profiles and the
dead Memphis comparison CTA wired to its live page (BATCH. Both defects are the same shape: a page
asserting something about itself that nothing in the toolchain reads. The heading spells a card
count in words; the CTA said "Coming soon" about a page that has been live for weeks and was
edited earlier the same day. `st-louis` is the CANONICAL, which is how the heading defect reached
five other profiles. The wider finding is boarded: 8 of 20 live comparison pages have no CTA link
from either of the two city profiles they compare.)

**Before that:** July 30, 2026, summer-comfort values corrected, Memphis 8 to 4 and
St. Petersburg 7 to 4, and the last two comparison pages relabelled (BATCH. Both checkmarks came
off without being moved, because the gaps were never real. The finding worth keeping:
`Climate Hot Sum` is an ORPHAN COLUMN. The matching engine never reads it, the rubric documents a
weight the code does not implement, and both city profiles had been quietly contradicting it for
months. No quiz result was ever affected. An earlier read of this session claimed otherwise, from
the rubric doc rather than the code.)

**Before that:** July 30, 2026, summer-polarity label cleared on 6 of 8 pages (BATCH. The two
held back are the story: `nashville-vs-memphis` and `tampa-vs-st-petersburg` sit on DB
`Climate Hot Sum` values that contradict every other climate column for the same city, and that
column carries 0.35 weight in the Mild Year-Round match score, so it is a QUIZ defect, not a
display one. Both escalated to P1 pending a scoring decision. Also closed the Jul 30 ranking-CTA
sweep, 15 files, which had shipped with no board entry.)

**Before that:** July 30, 2026, st-augustine vs pensacola dead tier gap closed (BATCH. Both
cities are Range 2 under v17, so the page's organising claim of a tier gap was false on five
surfaces including the headline of tradeoff #1, which was rewritten rather than patched. Twenty
stale v16 figures swapped. A duplicate `Budget dimension score` row in the Cost & money block was
reading 5/10 against a correct 6/10 in the D-score rows on the same page, and is deleted: it is
the unchecked copy of a checked number. Boarded P2 summer-row polarity taken in the same pass, plus two items
that should never have been boarded separately: FAQ 4's "#4 spot on our Top Cities for Healthcare
list", which describes a ranking that does not exist, and a second dead tier gap on
`cities/pensacola/profile.html`. Two new items boarded, both about checks that cannot see the
surface they should be reading. Gate clean at 0/0.)

**Before that:** July 29, 2026, D2 band-mover review closed, no change (BATCH, board only. The
last open piece of the ZHVI rebase, step 5. Charlottesville, Ann Arbor and Columbus all crossed a
D2 median-home band when the figures were rebased. Reviewed against rubric step 4, cross-check
against similar cities rather than the band table, since the rubric states D2 is affordability
RELATIVE TO THE DATABASE AVERAGE. Every city in the DB between $495,000 and $571,000 scores D2 5
or 6 without exception, so Charlottesville at 6 sits with St. George at $521K and Ann Arbor at 5
sits with Pinehurst at $542K. No scores changed. The review's real output is a documentation
defect, now logged as divergence (7) on the Rubric v3.3 item: the rubric publishes $525-$750K as a
3-4 band and the database has never once scored that range below 5, which will mis-score the next
city anyone adds from the rubric alone.)

**Then:** July 29, 2026, stat-card labels unhidden site-wide (BATCH. Every profile was
rendering its stats bar with the label row invisible, so readers saw `9/10` with nothing saying
what was scored. Not a Bozeman bug and not new: it is in the St. Louis canonical, so all 48
profiles inherited it. The stats bar's negative top margin was written to pull the card up over
the HERO; the sticky section-nav was later inserted between them, so the pull-up lands on the nav
instead, and the nav wins on z-index 50 against 3. The hidden band is exactly the label row at
both widths, which is why the 2x2 mobile grid shows row 2's labels and not row 1's. Pull-up
reduced below the top padding at both widths, 8px clearance, 96 edits across 48 files. Found by
reading a live page, not by any check.)

**Earlier:** July 29, 2026, Portland ME shipped as profile 48 (BUILD. Built from the live
St. Louis canonical against CityDatabase_Jul_27_v17. Emphasis brief: three pillars, D3 Health 9,
D6 Walk 9 and D10 Community 9, so the MULTI-PILLAR rule applies and all three land in the hero
tagline and the opening character paragraph rather than one leading. Support at D1 Airport 8 and
D7 Outdoor 7. Hard-flagged D9 Safety 4 and D5 Tax 4 both sit in the No-if column, property crime
first: CrimeGrade has Portland at the 28th percentile OVERALL on a property crime rate about 40%
above national, while violent crime sits BELOW national at the 84th percentile, and writing only
the first half would have been the dishonest version of a 4. No NRC callout and no `.reality-check`
markup: under MEDIAN-HOME-METHODOLOGY.md v1.2 section 4 a note is warranted where retiree-target
neighborhoods run materially ABOVE the citywide figure, and Portland is the opposite case, with the
West End at roughly $554K against a citywide $571,000. The method-callout carries that point
instead and opens on the DB figure. Stat slots 3 and 4 use concrete proof, `Level I` and a Walk
Score band, not a bare N/10; the abbreviated monthly was derived through `monthly_abbrev` rather
than typed. Zero landing-page edits needed: all six Portland cards were already live `city-card`
links, none coming-soon, none carrying a money figure. Two items boarded. Gate clean at 48
profiles.)

**Previously:** July 29, 2026, `bozeman` 2015 anchor sourced and closed (BATCH. The last open
P0 from the rebase. The prose read "The Bozeman of 2015 had typical home values near $734,000.
Today it's near $740,000", which put the v17 figure in the 2015 clause and the superseded v16
figure in today's. No 2015 value had ever been in the file to restore, so it was sourced from the
Zillow ZHVI city series rather than guessed: RegionID 44281, 2015-06-30 = $327,317 against
2026-06-30 = $733,959, which matches DB Median Home to the thousand and confirms the DB's ZHVI
vintage is June 2026. Same series, same month, eleven years apart, so the comparison is
methodology-clean. It also shows "doubled" UNDERSTATES at x2.24, so the three surfaces carrying
that claim now read "more than doubled". Three further stale items on the same page, none boarded:
a `$740K` in the JSON-LD presented as current, a `$734,000with` run-together, and a Budget score of
3 where v17 says 4. The fix then FAILED the gate, which is the more useful half of this
entry: `check_statcard_faq` had no concept of a figure attributed to a past year, so a correct
2015 value under a home-value noun read as a claim about today. Shipped with an OTHER-TIME guard
alongside the existing other-place guard, same window, same backward-only bound, current year
excluded so the "As of 2026," opener stays read. Four new assertions, harness now 21. Gate clean
at 47 profiles.)

**Previously:** July 29, 2026, the v17 argument rewrites shipped (BATCH, editorial. The two
P0 items the July 27 rebase left behind, both the same cause: v17 collapsed a price ordering that
two pages argued from, so both wanted an ARGUMENT rewrite rather than a figure swap.
`best-places-to-retire-in-florida.html` lost its budget ladder entirely, since Pensacola, Fort
Myers and Delray Beach are now all D2=7 and all Range 2; the cheapest-FAQ is rebuilt on what the
$73,000 of spread buys, and the banned "Of the Florida cities scored on RetireMeHere" opener is
re-anchored to named cities and figures. `st-augustine` lost its price bracket, since v17 puts it
above both Sarasota and Tampa; rebuilt on the scale mismatch, a town of 15,000 pricing above two
Gulf Coast metros. The same page's eight-row comparison table was folded in by decision rather
than left to contradict the rewritten FAQ three screens up: six stale home figures and five stale
Budget/D2 scores, none of which any check reads. 18 edits, two files. Two items boarded, both
comparison pages with the same cause. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, `check_statcard_faq` shipped with the 36 figures it reports (OPS.
The profile stat-card, score-slot and prose/FAQ surfaces are now gated. New harness
`tools/test_statcard_faq.py`, 16 assertions, five harnesses in the list. Every figure the check
reports is fixed in the same commit, plus eight cross-city figures it deliberately excuses and three
unanchored ones it cannot see. Four items boarded, two of them P0 editorial. Gate clean at 47
profiles.)

**Previously:** July 28, 2026, P0 figure batch and board triage scale (BATCH + OPS. Thirteen
reader-visible figures corrected across ten profiles, ten abbreviated monthly stat cards off by
$300 to $600 and three home figures each contradicted by their own page. Every open item on this
board now carries a P0-P4 rank; the scale and the two rules that make it hold are the first
section below. The stat-card + FAQ validator check that found all of this did NOT ship: it is
P2, its findings are recorded on its own board item, and the 26 P1 figures it also found are
deliberately still in place as its regression corpus. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, Casper WY profile shipped as profile 47 (BUILD. Built from the
live St. Louis canonical against CityDatabase_Jul_27_v17. Emphasis brief: one pillar, D5 Tax 10,
with a cluster of three 8s (D2 Budget, D7 Outdoor, D9 Safety), so the MULTI-STRENGTH pattern
applies: tax leads, cluster carries the character section. Hard-flagged weaknesses D1 Airport 4
and D6 Walk 3 both sit in the No-if column, airport first. No NRC callout: Paradise Valley
prices within a few thousand dollars of the $314K citywide figure, so a callout would add noise
under MEDIAN-HOME-METHODOLOGY.md v1.2 section 4. Casper card on
best-places-to-retire-on-a-budget.html promoted from coming-soon to a live link; the Value
Navigator, Active Frontier and natural-disasters cards were already live. Two items boarded,
see below. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, validator `layout` group shipped (OPS. New check
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

**Verified live at last update:** 48 profiles, 20 comparison pages, 5 guides, 11 category pages
(7 `top-cities-for-*` plus 4 `best-places-to-*` pillars; the old "7 landing pages" line counted
only the first set).
All 48 profiles carry a Visit block with per-city Expedia and Vrbo codes (Roanoke's are still
placeholders pending Creator Hub; Tulsa's, Casper's and Portland ME's are live).
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

## HOW TO RANK ANYTHING ON THIS BOARD (adopted July 28, 2026)

Every open item below carries a rank. An item without one is not tracked, because a board on
which everything looks equally urgent gets read as a pile rather than a queue.

Rank on one question: who is harmed, and how fast.

| Rank | Test | What it means for the schedule |
|---|---|---|
| **P0** | A reader sees a wrong number that could change a decision, or a page is broken | Fix in the chat that finds it |
| **P1** | Wrong, but a reader cannot see it or would not act on it: machine-only surfaces, rounding, low-traffic pages, dated triggers not yet due | Batch. Monthly, or the next time you are in the file |
| **P2** | Nothing is wrong today; nothing prevents it going wrong tomorrow. Every validator check lives here | Its own scheduled OPS chat |
| **P3** | Structural debt. The nav in 87 files, the rubric living outside the repo | Only when it blocks something you actually want to do |
| **P4** | Cosmetic, wording, doc version numbers, enumeration accuracy | Only while already in the file. Never its own job |

Two rules make the scale hold:

1. **No board line without a rank.** A chat that cannot rank a finding does not board it.
2. **Only P0 may interrupt a city profile build.** With 52 cities left to score into profiles,
   builds are the default work and findings are the interruption, never the other way round.

Ranks are cheap to change and are a judgment, not a measurement. Move one the moment it reads
wrong; do not open a discussion about the scale to do it.

One exception, and only one: **queue entries carry no rank.** `Next in queue`, the comparison-page
queue and the per-city follow-up lists are the WORK, not findings about the work. Four such bullets
are unranked today and that is correct, not an oversight.

Why this exists, recorded so the reasoning does not have to be reconstructed: on July 28 an OPS
chat scoped to a single validator check turned up 44 wrong figures across 36 profiles. Ten moved
a headline monthly budget by $300 to $600. Twenty moved it by $100. Before today those two
classes read identically on this board, and the effect was that the $100 ones felt as blocking
as the $600 ones. Nothing was wrong with the finding. What was missing was the rank.

---

## CLOSED July 31, 2026 (san-antonio-vs-fort-worth, Tier 1) - shipped

- **Three quarantined figures, and the price ordering inverts.** San Antonio $320,000 ->
  $251,000, its monthly $5,100-$6,400 -> $4,700-$5,800, its tier 2 -> 1. Fort Worth was correct on
  all three. The page presented San Antonio as $20,000 dearer; it is $49,000 cheaper. The board
  recorded the magnitude, +145%, and not the sign, which is the more useful half: a stale figure
  reads as approximately right, a reversed one reads as confidently wrong.

- **A live error the cost check could never see, found by reading the page.** FAQ 1 said "five of
  the ten are exact ties: budget, healthcare, climate resilience, walkability, and active
  wellness". D2 is San Antonio 8 against Fort Worth 7, which the scored table on the same page
  states correctly. So the page contradicted itself twelve lines apart, and
  `check_comparison_scores` passed both times because it reads the table row and not the
  paragraph. Corrected to four ties, with San Antonio taking budget alongside tax friendliness,
  outdoor recreation, safety and community. Same shape as the `asheville-vs-greenville` tier
  claim closed in Tier 3, and the second sighting in two batches: **prose that restates a checked
  number is unchecked, and it drifts in the same places every time.**

- **The neighborhood argument needed nothing.** Tradeoff #3 and FAQ 2 already carried both bands
  with figures, and all nine were re-checked against `cities/fort-worth/profile.html` and
  `cities/san-antonio/profile.html` and are current. The bands still overlap almost exactly, so
  the page's conclusion, that the cost side should not decide this move, survives its premise
  being wrong. Only the opening sentence and the H3 were rewritten. Nothing was invented: every
  neighborhood figure on this page is already published on a profile.

- **One boarded P3 closes for free.** This page's FAQ Q2 is one of the seven visible-versus-schema
  mismatches boarded Jul 30: the schema wrote the bands long form, `$350,000 to $550,000`, and the
  visible copy wrote them short, `$350K to $550K`. Q2 was being rewritten anyway, so both now use
  the short form and normalise equal. **Six remain on that item, not seven:** `bend-vs-boulder`
  Q2, `scottsdale-vs-santa-fe` Q3 and Q5, `visit-before-you-decide` Q2.

- **Checkmarks added, and that is a judgment call.** The three cost rows carried no mark, which
  was right when the figures were $20,000 apart inside one tier. San Antonio now wins all three on
  a $49,000 gap, a $300-$400 monthly gap and a full tier, so it takes the mark on all three, in
  line with every other comparison page. Easy to reverse if the house rule is that cost rows go
  unmarked when the neighborhood bands contradict them.

- **[P2] NEW: the D9 neighborhood-basis claim on this page has no settled methodology behind it.**
  Tradeoff #4 and FAQ 5 both say San Antonio's Safety score is built on its retiree-target areas
  and Fort Worth's is not, and warn the reader not to compare them directly. That is rubric v3.2's
  documented treatment of D2, D6 and D9 for high-variance cities. But
  `MEDIAN-HOME-METHODOLOGY.md` v1.2 retired the eight-city neighborhood carve-out, and
  `BUDGET-METHODOLOGY.md` section 4 says flatly that no city uses a neighborhood basis, both of
  which are about MEDIAN HOME. Nobody has said whether D9 went with it. So this page publishes a
  methodology caveat that may describe a retired practice, on the one dimension where it would
  change how a reader reads a score. Left untouched here because it is a rubric decision and not
  a figure, and folded into the Rubric v3.3 item. San Antonio is the only page in the set making
  this claim.

## CLOSED July 30, 2026 (st-louis-vs-kansas-city, Tier 1) - shipped

- **Four quarantined figures, and the page could not absorb them as a swap.** St. Louis
  $235,000 -> $192,000, Kansas City $250,000 -> $257,000, and both monthly ranges. The gap moves
  from $15,000 to $65,000, a 333% change and the reason this was Tier 1. `COST_ROW_BASELINE` 39
  to 35 over nine pages.

- **The same-price claim was load-bearing on eleven surfaces, not one.** Tradeoff #2's H3, its
  opening sentence, the meta description, `og:description`, `twitter:description`, the hero
  tagline, the verdict paragraph twice, FAQ 1 and FAQ 2 in visible text AND in FAQPage schema.
  The board sized this page as an argument rewrite on the strength of the headline alone, which
  was right, but the headline was the smallest part of it. Same lesson as Tier 3 one page up: the
  figure the check reads is one copy among many.

- **The neighborhood argument survives and is now doing real work.** It used to elaborate a
  non-gap: the cities cost the same, and here is why the citywide number misleads anyway. It now
  RESOLVES a real one. St. Louis' retiree neighborhoods run $420K to $575K against a $192,000
  citywide median, two to three times the figure; Kansas City's run $300K to $900K against
  $257,000. So the $65,000 citywide advantage does not survive into the neighborhoods retirees
  actually buy in, because St. Louis' floor sits above Kansas City's. That is a better paragraph
  than the one it replaces.

- **Checkmarks did not move and were checked, not assumed.** St. Louis stays marked on both cost
  rows because it is still cheaper on both after the swap. D2 stays unmarked at 9 against 8, a
  one-point gap under the two-point rule. FAQ visible text and FAQPage schema were rewritten in
  the same pass and normalise equal, so this page does not join the six on the P3 sync item.

- **Two judgment calls, flagged in the script rather than buried.** Tradeoff #1 opened "Most
  cost-matched pairings split healthcare narrowly", which a $65,000 gap does not support though
  the budget TIER still does; it now reads "Most pairings this close on budget". FAQ 1's clause
  "because little else separates them" was dropped rather than rewritten, since D7 and D8 are
  also two-point gaps and the clause was loose before this batch touched it.

- **CTA debt unchanged at 11, and that is the item talking to itself.** Retiring a page from
  quarantine normally retires every profile CTA edge into it. This one retires none, because
  neither `cities/st-louis/profile.html` nor `cities/kansas-city/profile.html` links to it. It is
  one of the eight orphans on the P1. `cities/kansas-city/profile.html` still carries the stale
  comment calling this page a placeholder that has not been built.

## CLOSED July 30, 2026 (Tier 3 cost figures) - shipped

- **Eight pages, 184 edits, 30 quarantined mismatches to zero.** `asheville-vs-greenville`,
  `bend-vs-boulder`, `fort-collins-vs-boulder`, `madison-vs-columbus`, `santa-fe-vs-tucson`,
  `scottsdale-vs-santa-fe`, `scottsdale-vs-tucson`, `tampa-vs-st-petersburg`. Every figure taken
  from `CityDatabase_Jul_27_v17.xlsx`, none from research. Both ratchets lowered in this commit:
  `COST_ROW_BASELINE` 69 to 39 over ten pages, `CTA_COST_DEBT_BASELINE` 21 to 11.

- **30 versus 184 is the entry worth keeping.** The board sized Tier 3 from the check's own count,
  which reads three table rows per page. The same figures are restated three to fourteen times per
  page in prose, in visible FAQ text, in the FAQPage schema and in `og:description` and
  `twitter:description` meta tags. `fort-collins-vs-boulder` carries its gap figure fourteen
  times; `bend-vs-boulder` and `scottsdale-vs-santa-fe` carry theirs ten. A quarantine count is a
  count of what one check can see, and it was 16% of the real surface here. Size Tier 1 and Tier 2
  by grepping the page, not by reading the baseline.

- **DERIVED figures move too, and they are not in any table.** The gap between two home values is
  a published number on six of these eight pages and is a copy of a copy. Recomputed rather than
  left: Bend $238,000 to $235,000, Fort Collins $411,000 to $403,000, Madison $178,000 to
  $184,000, Santa Fe $262,000 to $268,000. Every ratio claim was re-derived and four survived
  unchanged, which is why they are not in the diff: Bend stays "roughly 25% less" (24.2%),
  Scottsdale/Santa Fe stays "roughly 31% less" (31.2%), Tucson stays "about 38% of Scottsdale"
  (38.0%), and Santa Fe/Tucson's "nearly double" and "barely half" both get MORE true, 1.71x to
  1.81x.

- **Three edits were not mechanical and are called out rather than buried.**
    - `asheville-vs-greenville` prose read "Asheville's tier 3" against a DB tier of 2 and a table
      row reading `2 of 5` on the same page. Wrong before the rebase and nothing to do with it.
      `check_comparison_cost_rows` reads the table row, which was correct, so the check was
      passing over a false claim twelve lines below the true one. Exactly the shape of the
      `st-augustine-vs-pensacola` duplicate-row incident: the unchecked copy of a checked number.
    - `fort-collins-vs-boulder` read "roughly $411,000 or 74% less". $411,000 is 74% of Fort
      Collins' own price, not of the gap to Boulder, so the sentence was arithmetically wrong in
      the old figures too. Recomputed on the correct basis as "41% less" rather than swapped to a
      new wrong number. Judgment call: the alternative was carrying the broken basis forward at
      "71%".
    - `tampa-vs-st-petersburg` read "about $300 lower across the range". Under v17 the gap is $200
      at the low end and $300 at the high, so it now reads "about $200 to $300 lower".

- **Tier 3 broke the cost-row harness, and that is a finding, not an accident of ordering.**
  `tools/test_comparison_cost_rows.py` named `asheville-vs-greenville` as its quarantined page and
  carried `$464,000` as that page's correct home value, both as literals. Releasing the page from
  quarantine made assertion 4 unplantable and the harness failed on the gate. EVERY tier batch
  would have done this, and a harness that fails on the gate is the worst possible place to learn
  that a test is pinned to the thing it watches, because the obvious move is to edit the test until
  it goes green. Both the page and the values are now derived from `COST_ROW_BASELINE` and the
  database at run time: the harness looks for a quarantined page carrying both a wrong cell and a
  right one, sets the wrong one correct to test the downward ratchet, and breaks the right one to
  test the upward. Tier 1 and Tier 2 will not need to touch it. Assertion 5 also tightened from
  `"got WORSE" in out or "budget tier" in out` to `"got WORSE"` alone; the `or` branch would have
  passed on any budget-tier failure anywhere in the run, including one the assertion did not cause.
  The new `test_comparison_cta_debt.py` was written this way from the start for the same reason.

- **The board's tiering criterion does not survive the arithmetic on two pages.** Tier 3 was
  defined as gap movement under 6%. `santa-fe-vs-tucson` moves 10.9% ($238,000 to $264,000) and
  `scottsdale-vs-tucson` moves 6.4% ($500,000 to $532,000), because Tucson is the only Tier 3 city
  whose median went DOWN in the rebase while everything around it went up. Both were still safe to
  batch, but for a different reason than the one boarded: neither page publishes a gap figure at
  all, so there was nothing derived to rewrite. Movement is the wrong proxy. What decides whether
  a page is mechanical is whether it ARGUES from the number.

- **The "$100 recompute" open question is answered, and the answer is no.** The board suspected
  the monthly estimates were off by a uniform $100, implying a `BUDGET-METHODOLOGY.md` recompute
  rather than drift. Across the eight pages the monthly deltas run 0, +$100, +$200 and -$100, in
  both directions, and they track each city's own median-home move. This is ordinary rebase drift.
  Tier 3 does not grow.

## CLOSED July 30, 2026 (CTA cost-debt gate) - shipped

- **`check_comparison_cta_cost_debt` counts the edges between two open repairs.** 21 profile CTA
  links currently point at one of the 18 comparison pages quarantined in `COST_ROW_BASELINE`.
  Adding a CTA to a quarantined page now fails the gate; so does the count falling without
  `CTA_COST_DEBT_BASELINE` being lowered in the same commit. Nothing on the site changed.

- **The gap it closes is between two checks, not inside one.** `check_comparison_cost_rows` reads
  the comparison page and knows exactly which figures are stale. Nothing reads a profile's
  outbound links. So the orphaned-CTA batch could have wired eleven profiles into known-bad money
  with the gate at 0/0 the whole way, and each check would have been correct about its own
  surface. This is the same shape as the coverage lesson from the cost rows themselves: the rows
  under a check held, the rows beside them drifted.

- **The count falls on its own as batches land, and that is deliberate.** Deleting a
  `COST_ROW_BASELINE` entry retires every edge into it, so the debt drops without anyone touching
  a profile. The downward failure then forces the constant down in the same commit, which is what
  stops it becoming a number nobody trusts. Tier 3 will take it from 21 to 11.

- Planted-error test at `tools/test_comparison_cta_debt.py`, 7 assertions, harness now 7. Two of
  the seven exist only to pin down what is being counted: a second CTA to an ALREADY-linked
  quarantined page must fail (counting distinct pages instead of links passes a naive test and
  misses this), and a relative `href` with no leading slash must still be counted (every CTA on
  the site today is written with one).

## CLOSED July 30, 2026 (lists heading counts + Memphis compare CTA) - shipped

- **Six profiles stated a lists-section card count that disagreed with the cards rendered
  beside it.** `chattanooga`, `lexington` and `tucson` said "Two lists" over three cards;
  `memphis`, `pittsburgh` and `st-louis` said "Three lists" over four. Heading corrected in
  every case, cards untouched: all four Memphis destinations were verified reciprocal
  (`top-cities-for-healthcare`, `top-cities-for-foodies`, `top-cities-for-arts-lovers`,
  `best-places-to-retire-on-a-budget` each carry a live Memphis card), so the cards were right
  and the sentence was wrong.

- **`st-louis` is the canonical, which is the mechanism.** The Jul 14 `.lists-grid-four` fix
  touched `st-louis`, `columbus`, `memphis` and `pittsburgh` because each had gained a fourth
  card. The grid class was corrected; the heading above it was not, on any of them. `columbus`
  escaped only because its heading carries no number at all.

- **Nothing can see this class of defect.** The count lives in English prose in an `<h2>` and
  the truth lives in the number of sibling `.list-card` anchors. No check compares them. Found
  by reading the page. A `check_lists_heading_count` is boarded below.

- **The Memphis comparison CTA pointed at the quiz.** `cities/memphis/profile.html` carried a
  block headed "Memphis or Nashville?" whose paragraph ended "Coming soon." and whose button
  read "Take the quiz" against `href="/"`. `nashville-vs-memphis-retirement.html` has been live
  for weeks and was itself edited on Jul 30 in the summer-polarity batch. Wired to the real page
  and relabelled "Compare Nashville vs. Memphis", matching the live pattern in
  `cities/tampa/profile.html`. Placeholder text and the stale `(placeholder)` comment removed.

- **`kansas-city` was checked and needs no edit.** It carries the same
  `(placeholder - comparison page not yet built)` comment, but the block below it was quietly
  repurposed into a working Midwest guide CTA. The comment is stale, the page is correct. Left
  alone rather than stacked onto a verified change; boarded as a one-line cleanup.

## CLOSED July 30, 2026 (comparison cost-row coverage) - shipped

- **`check_comparison_scores` was matching dimension rows by DIMS LABEL, and three never
  matched.** The label is the database column name, the page uses a reader-facing one.
  "D3 Health" is a prefix of "D3 Healthcare" so D3 worked; "D4 Resil.", "D8 Wellness" and
  "D10 Comm." are not prefixes of "D4 Climate resilience & insurance", "D8 Active wellness"
  and "D10 Community & culture", so all three were skipped on all twenty pages from the day the
  check shipped, and the loop did `continue` on no match so nothing ever said so. Now matched on
  the D-number token with `(?![0-9])` so D1 cannot swallow D10, and a missing row FAILS. The board
  had this as D4 and D10; D8 was the third. All three are correct everywhere today, so this closed
  a hole rather than surfacing errors.

- **`check_comparison_cost_rows` is new and covers the rows that actually drifted.** Typical home
  value, Estimated retiree budget, Budget tier. The Jul 30 audit found 69 mismatches on 18 of 20
  pages and NOT ONE was in D1-D10. The rows under a check held across twenty pages; the rows
  beside them drifted on eighteen. Fort Myers was showing $372,000 against a DB figure of
  $310,000, San Antonio was a full budget tier out, Ann Arbor a tier the other way.

- **The baseline is a ratchet and fails in both directions.** The 18 known-bad pages are
  quarantined with exact counts so the gate holds at 0/0 during repair. Going UP is new drift.
  Going DOWN also fails, because a baseline that outlives its fix is how a quarantine list
  quietly becomes a permanent exemption. Lower the number in the same commit as the batch;
  delete the entry at zero; delete the dict when it is empty.

- Planted-error test at `tools/test_comparison_cost_rows.py`, 8 assertions, including one that
  plants a D8 error specifically to guard the label fix, and one that deletes the cost rows
  outright to prove the check fails loudly rather than reading zero and reporting clean.

## CLOSED July 30, 2026 (summer-comfort values) - shipped

- **Memphis 8 -> 4 and St. Petersburg 7 -> 4 in `Climate Hot Sum`.** Both were the only
  outliers in their comparison set. Every city in the DB with HEAT 7 and HUM 9 scores 4:
  Naples, Fort Myers, Sarasota, Delray Beach, Tampa, St. Augustine, Corpus Christi. The only
  other exceptions are Pensacola at 5, justified by latitude at Jan 52F, and Wilmington NC at 6,
  which is boarded. St. Petersburg at 7 was the highest score in Florida, above St. Augustine
  130 miles north, with identical HEAT, identical HUM and a January mean one degree off Tampa's.
  Memphis at 8 was the most summer-comfortable city in the entire southern set while being
  hotter than Nashville on every other column.

- **The two city profiles were already right and had been contradicting the DB.**
  `cities/memphis/profile.html` says "Summers are hot and humid (HUM 9, HEAT 8)" and
  `cities/st-petersburg/profile.html` says "summers are long, hot, and humid". Both cite HEAT
  and HUM rather than the summer score, which is why they stayed correct while the score drifted.
  Neither needed an edit.

- **Both checkmarks came off without being moved.** Nashville 5 vs Memphis 4 is a one-point gap
  and Tampa 4 vs St. Petersburg 4 is a tie, so both fall under the 2-point rule on their own.
  The marks were a SYMPTOM of the bad values, exactly as boarded: only an implausible gap was
  ever wide enough to generate one in this column.

- **`Climate Hot Sum` is an orphan column, and that is the real finding.** `getCityScore` in
  `index.html` destructures W, M, HUM, HEAT and janF, and never touches H. The rubric's
  Mild Year-Round formula gives summer comfort a 0.35 weight; the CODE does not implement it and
  uses `10 - 1.15 * max(0, HEAT - 3)` instead. So no quiz result was ever affected by either bad
  value. The column is maintained in the DB and published on comparison pages while being
  consumed by nothing, which is precisely why it drifted unnoticed.

## CLOSED July 30, 2026 (summer polarity, 6 of 8) - shipped

- **Six pages relabelled `Hot summers (lower = milder)` -> `Summer comfort (10 = most
  comfortable)`.** `bloomington-vs-lexington`, `knoxville-vs-chattanooga`, `madison-vs-columbus`,
  `naples-vs-fort-myers`, `naples-vs-sarasota`, `st-louis-vs-kansas-city`. No values changed; the
  label was reversing the meaning of correct numbers. A reader seeing Naples at 4 under the old
  label concluded "fairly mild summers" when 4 means the opposite, and Naples' own HEAT column
  agrees at 7 of 10 exposure. Third and fourth sightings of this label were already fixed on
  `pensacola-vs-fort-myers` (Jul 29) and `st-augustine-vs-pensacola` (Jul 30).

- **Prose checked on all six before relabelling.** Four mention summer not at all.
  `bloomington-vs-lexington` says "warm and humid but not extreme on either side", consistent with
  7 and 6. `st-louis-vs-kansas-city` says "hot, humid summers", which sits a little awkwardly
  beside 7 and 7 but is not contradicted by it; that tension is boarded as the calibration
  question, not treated as a defect here.

- **Two pages held back and escalated to P1.** See the open items. The audit that was supposed to
  confirm a mechanical relabel instead found two DB values that do not survive scrutiny, and the
  column turns out to carry 0.35 weight in the Mild Year-Round climate score, so it is a quiz
  defect rather than a display one.

## CLOSED July 30, 2026 (ranking CTA) - shipped

- **`rank all every city on RetireMeHere` on 15 pages.** A fossil of the hardcoded-count fix:
  someone replaced `all 99 cities` with the count-free `every city on RetireMeHere` to satisfy
  `check_hardcoded_counts` and the `all` was left stranded. Byte-identical across 8 landing pages,
  6 comparison pages and `compare-retirement-cities.html`, all in the `quiz-cta-h3` block.
  Fixed to `we'll rank every city on RetireMeHere for you`. Diffed against a pristine clone before
  shipping: 15 files, 15 lines, one word each. The word `all` appears 1,079 times site-wide and the
  other 1,064 were untouched, because the anchor was the full 44-character string including the
  `<span class="accent">` markup, not the word.

- **A hand edit on `top-cities-for-healthcare.html` shipped a rendering bug to production while
  doing it.** The `all` was deleted along with the space in front of the span, so the page read
  `we'll rankevery city on RetireMeHere for you` on live main. Deleting `all ` and deleting `all`
  are indistinguishable in an editor. This is the argument FOR the apply-script convention on
  edits that look too small to script: a scripted swap names both the old and the new string in
  full and cannot make that mistake. Fixed in the same push.

- **This is the second sighting in one day of a defect class the gate cannot see, and the first
  one that reached production.** `rankevery` and `$269,000with` are the same shape: a character
  immediately followed by a letter where a space belongs. The boarded P2 has been rewritten from
  "43 run-together money figures" to the general pattern, because that is what the check needs to
  match. Site-wide scan for the `[a-z]<span class="accent">[a-z]` variant came back clean, so
  `rankevery` was the only instance of that particular shape.

## CLOSED July 30, 2026 (st-augustine vs pensacola) - shipped

- **[P1] The dead tier gap is gone, and the tier was never the story.** Both cities are Range 2
  under v17, so the page's organising claim, "Pensacola sits at budget tier 1 against
  St. Augustine's tier 2", was false on five surfaces: hero tagline, verdict close, the table's
  tier row, tradeoff #1, and both FAQ 1 and FAQ 3 in visible text and in FAQPage schema. Tradeoff
  #1 was rewritten rather than patched, as boarded. The replacement argument is stronger than the
  one it lost: the tier is a five-bucket instrument and both cities sit in the same bucket with
  $164,000 of house between them, so the tier label FLATTENS this pairing instead of explaining
  it, and the same flattening shows up again in a D2 that splits only 6 against 7. Figures swapped
  throughout: Pensacola `$264,000` -> `$269,000` x7, St. Augustine `$432,000` -> `$433,000` x6,
  the gap `$168,000` -> `$164,000` x6, and the monthly `$4,900-$6,100` -> `$5,000-$6,200`.

- **The Cost & money block carried a second copy of D2 and it had drifted.** The block held a
  `Budget dimension score` row reading 5/10 while the `D2 Budget` row twelve lines below read the
  correct 6/10, on the same page, in the same table. `check_comparison_scores` reads the D-score
  rows only, which is exactly why the July 13 D2 rebuild landed on one and not the other. The
  duplicate row is deleted rather than corrected: a second copy of a checked number, sitting in an
  unchecked region, is the defect. The tier row stays and now renders the Range 2 tie the way the
  corrected Pensacola/Fort Myers page renders it, two plain cells and no mark.

- **D2's checkmark came off.** 6 against 7 is one point, and the page already leaves D1 (6/7),
  D3 (8/7) and D7 (6/7) unmarked. Pensacola still wins the two dollar rows outright, which is where
  the money argument belongs.

- **[P2] Summer polarity fixed in the same pass, as boarded.** `Hot summers (lower = milder)` ->
  `Summer comfort (10 = most comfortable)`, matching the fix already live on Pensacola/Fort Myers.
  Values were correct at 4 and 5; only the label inverted them. No prose on the page mentions
  summer, so the label was the whole of it.

- **One superlative-rule violation cleaned while FAQ 1 was open anyway.** "the gentlest resilience
  score WE GIVE in Florida (3)" is scoped to our own scoring, which is the possessive form
  SUPERLATIVE-LEDGER line 95 calls out. Re-anchored to named cities: 3 of 10, a point clear of
  Pensacola, Sarasota and Tampa at 2. True against v17 and it fails loudly rather than silently if
  a Florida city ever scores 3.

- **FAQ 4's healthcare rank was false, not merely rot-prone, and false in the flattering
  direction.** "it earns the #4 spot on our Top Cities for Healthcare list" describes a ranking
  that does not exist: `top-cities-for-healthcare.html` is three tiers, alphabetical within each,
  per the landing-page convention. St. Augustine is 4th ALPHABETICALLY in tier THREE, "Strategic
  proximity to a top hospital", the weakest of the three, behind Annapolis, Frisco and Silver
  Spring. The claim reads as fourth-best of 33 cities and it was sitting in FAQPage schema, which
  is the copy an answer engine lifts. Replaced with the substance the tier actually encodes:
  the strength is proximity, not a top-tier hospital inside the city. This was boarded as a
  separate item and should not have been; it was one edit inside an FAQ block already open.

- **A second dead tier gap, same root cause, found on `cities/pensacola/profile.html`.**
  "a full budget tier below the peninsula's coastal cities" is false under v17: Pensacola is
  Range 2 and so are Tampa, Sarasota, St. Petersburg, Fort Myers, Delray Beach and St. Augustine.
  Only Naples and Miami sit above. Re-anchored to named cities and figures, `$87,000` against
  St. Petersburg and `$144,000` against Sarasota. The missing space in `$269,000with` was in the
  same sentence and went with it. Only file on the site carrying that phrase.

- Caption data vintage `June 2026` -> `July 2026` per COMPARISON-PAGE-STANDARD-v2, since the
  figures were refreshed from a new DB version. Schema `dateModified` bumped to 2026-07-30.

## CLOSED July 29, 2026 (pensacola vs fort myers) - shipped at `bf28c12`, see SITE-OPERATIONS-LOG 2026-07-29 (third push)

- **[P0] The money argument rebuilt on the $41,000 frame.** Entry written Jul 29 as a continuity
  repair: the item was removed from this board when the work shipped and no closed entry replaced
  it, so the board could not show a P0 had been resolved even though the ops log carried the full
  account. Recorded here in summary, with the log as the record of reference.
  **What v17 broke.** `$108,000` -> `$41,000`, D2 8-vs-6 -> tied at 7, tier 1-vs-2 -> both Range 2,
  monthly floor `$600` -> `$200`. The thesis sentence, "unlike some near-twin pairings, cost
  genuinely weighs here", had inverted: on cost they now ARE near twins.
  **What replaced it, which is the part worth keeping.** There was no substitute row for Pensacola
  to win on. Under the 2-point checkmark rule the rebuilt table gives Pensacola one mark against
  Fort Myers' four. Rather than hunt for a different win, the rewrite changed what the figure MEANS:
  `$41,000` stopped being Pensacola's saving and became Fort Myers' asking price, turning tradeoff
  #1 into the setup and tradeoff #3 into the itemised answer. 24 edits on the page plus one on
  `compare-retirement-cities.html`, and four defects the board had not carried, including a "#3 on
  our healthcare list" rank that was never a rank.
  **Also closes** the cross-page split carried on purpose since the pillar rewrite: the pillar and
  this page now agree that Fort Myers is `$310,000`.
  **Two follow-ons were boarded from it** and remain open: the `check_comparison_dims` prefix-match
  blind spot on `D4 Resil.` / `D10 Comm.`, and the inverted `Climate Hot Sum` label, fixed on this
  page and still live on `knoxville-vs-chattanooga`.

---

## CLOSED July 29, 2026 (D2 band-mover review) - reviewed, no change

- **[P1] D2 band-mover review, the last open piece of the ZHVI rebase (step 5).** Closed with NO
  score changes. All three cities are already correct; the review was worth running anyway, because
  of what it turned up.
  **What was flagged.** Charlottesville `$465K -> $528K` and Ann Arbor `$489K -> $541K` both crossed
  `$525K`, which the rubric publishes as the 5-6 / 3-4 boundary. Columbus `$235K -> $251K` crossed
  `$250K` out of the 9-10 band. Knoxville (over `$375K` by ~$2,000) and New Orleans (moved the
  favourable way) were set aside as not worth the thought, correctly.
  **Method.** Rubric step 4 says cross-check a score against 2-3 similar cities already in the
  database rather than reading the band table alone, and the rubric itself states D2 reflects
  affordability RELATIVE TO THE DATABASE AVERAGE, not absolute cost. So the test applied was peer
  consistency, not band arithmetic.
  **Result.** Every city in the database between `$495,000` and `$571,000` scores D2 5 or 6, without
  exception: Bentonville $497K/6, Boise $508K/6, Nashua $517K/5, Burlington $520K/5, St. George
  $521K/6, Charlottesville $528K/6, Ann Arbor $541K/5, Pinehurst $542K/5, Naples $549K/5, Silver
  Spring $557K/5, Fort Collins $569K/5, Portland ME $571K/5. Charlottesville at 6 sits with
  St. George at $521K; Ann Arbor at 5 sits with Pinehurst at $542K and Naples at $549K. Columbus at
  8 is already inside its new band. Nothing to change.
  **The finding, moved to the Rubric v3.3 item.** The rubric's published D2 band table and the
  database's actual practice have diverged: the rubric calls `$525-$750K` a 3-4 band and the
  database has never scored that range below 5. This is not a scoring error, it is a documentation
  error, and it is the dangerous kind. Anyone scoring a new $530K city from the rubric alone would
  assign a 4 and land two points out of step with twelve existing cities.
  **This also closes the ZHVI rebase.** Step 5 was the last open piece.

---

## CLOSED July 29, 2026 (stat-card labels) - shipped

- **[P1] Every profile hid its stat-card labels behind the sticky nav.** Surfaced by a reader
  question that could not be answered from the page: what does `9/10` mean? The label saying
  OUTDOOR was there in the markup and painted behind the nav.
  **Cause.** DOM order is `site-header` -> `hero` -> `section-nav` (sticky) -> `stats-bar`. The
  stats bar's `margin-top: -56px` was written to pull the card up over the hero image. The sticky
  nav was later inserted between the two, so the pull-up now lands on the NAV, and the nav paints
  over it at `z-index: 50` against the stats bar's `3`. The covered band is 56px; the label row
  occupies 32px padding + 10px label + 8px margin = 50px. It fits inside the covered band exactly.
  **Why mobile looked different.** At 2x2 the pull-up is 40px against 24px padding, so row 1's
  labels are covered and row 2's clear. That asymmetry is what confirmed the diagnosis: a
  scroll-offset bug would have hidden both rows or neither.
  **Fix.** Pull-up reduced below the top padding at both widths, `-56px` -> `-24px` desktop and
  `-40px` -> `-16px` mobile, leaving 8px of clearance so the nav can only ever cover padding. The
  tucked band is invisible either way, since the nav is opaque with a backdrop blur, so the only
  visual change is the card sitting 32px lower. 96 edits, 48 files.
  **Not fixed, boarded below.** `.site-header` and `.section-nav` are BOTH pinned to `top: 0`, and
  the header's `z-index: 100` beats the nav's `50`, so the chips are clipped along their top edge
  rather than stacking below the header. Same block of CSS, visible in the same screenshot, but it
  wants a browser to confirm before touching.
  **No check covers this.** Nothing on the site reads rendered geometry, and nothing would have
  caught a label that exists in the markup and is painted over. Boarded as a question rather than
  a task, because a CSS-geometry check may cost more than it returns.

---

## CLOSED July 29, 2026 (bozeman 2015 anchor) - shipped

- **Follow-on, same day: `PROFILE-FORMATTING.md` v1.6 -> v1.7.** The guard imposes a house
  style, year before the figure, and shipping it undocumented meant the next profile with a
  price-history paragraph would hit the same wall from scratch. New section covers the clause
  rule with the three shapes that pass and fail, the same-series sourcing requirement (ZHVI
  against ZHVI, never an MLS median sale price), and the accepted false negative. One QA
  checklist line added. Checked first that no file cites `PROFILE-FORMATTING.md v1.6`, so the
  bump strands nothing, which is the check the July 25 MEDIAN-HOME bump failed.

- **The last P0 from the ZHVI rebase, and the one that could not be fixed by swapping.** The board
  item was right that the rebase had been applied to the wrong clause. What it could not know is
  that there was nothing to restore: `$740,000` was the superseded v16 figure for TODAY, not a 2015
  value that had been overwritten. The page had never carried a 2015 number.
  **Sourced, not guessed.** Zillow ZHVI city-level series, RegionID 44281 (Bozeman city, MT), the
  same RegionID Zillow's own Bozeman page uses. `2015-06-30 = $327,317`, `2026-06-30 = $733,959`.
  Same series, same geography, same seasonal adjustment, same calendar month eleven years apart.
  Rounded to `$327,000` per the site's whole-thousand convention.
  **Rejected on the way there:** a local brokerage figure of roughly $300,000 for 2015. Wrong metric
  (MLS median SALE price against a ZHVI typical-value index, which is the mixed-methodology
  comparison MEDIAN-HOME-METHODOLOGY.md exists to prevent), and the same page contradicts itself
  elsewhere, stating an 84.1% rise equal to $391,000 while giving endpoints that work out to 61%.
  **The sourcing changed the argument.** June 2015 to June 2026 is x2.24, +124%, so "doubled"
  understates rather than overstates. Corrected on all three surfaces that carried it: the intro
  ("doubled in a decade"), the cons card ("roughly doubled since 2015") and the history paragraph.
  Worth noting the decade claim is exact if anchored to 2016 instead: `2016-06-30 = $370,015` is
  x1.98. 2015 was kept because the whole page, meta description included, is built on "post-2015".
  **Three stale items on the same page, none of them boarded.** A `$740K` in the JSON-LD downsides
  answer presented as the current typical value, the same `$734,000with` run-together shape found on
  `st-augustine`, and "Budget scored 3 of 10" against a v17 D2 of 4.
  **Side confirmation.** DB `Median Home` for Bozeman is `$734,000` and ZHVI `2026-06-30` is
  `$733,959`, which pins the DB's ZHVI vintage to June 2026 and independently confirms the "as of
  June 2026" caption on `best-places-to-retire-in-florida.html` is correct as written.
  **The rebase overwrote a CORRECT figure, and git proves it.** Before `cff99a6` the sentence read
  "The Bozeman of 2015 had typical home values near `$325,000`. Today it's near `$740,000`", which
  was right, and had been stable since the profile was built. The rebase replaced the FIRST money
  figure in the paragraph rather than the one describing today, so it destroyed the 2015 value and
  left the superseded one standing. Swept all 45 profiles the rebase touched for the same shape,
  a money figure sitting in a clause that names a past year: **Bozeman is the only one.**
  **It also needed a validator change, which is the real lesson.** Restoring a sourced 2015 figure
  FAILED the gate. `check_statcard_faq` grades every home figure against Median Home and had an
  other-PLACE guard but no other-TIME guard, so a correct historical value under a home-value noun
  read as a claim about today. Two wrong ways out were available and both were rejected: rewording
  to drop the noun would have made the figure invisible to every money check on the site, which is
  the P2 "money with no anchor" shape already boarded, and falling back to a geographic contrast
  would have thrown away the sourcing. The guard shipped instead.
  **The guard.** Same window and same backward-only bound as the other-place guard: walk back to
  the nearest clause break, and if that window names a year older than the current one, the figure
  is historical and is skipped. The current year cannot excuse, or the commonest opener on the site
  stops being read. Note the corpus is protected twice, because in "As of 2026, the typical home
  value is..." the comma already puts the year outside the window, which is why a New Year rollover
  does not silently unwatch 47 profiles.
  **Accepted false negative, recorded on purpose.** "Since 2015 the value has risen to $999,000"
  is excused though it claims today. Reaching it needs tense parsing, which fails in worse ways.
  The house style this implies, year BEFORE figure, wants a line in PROFILE-FORMATTING.md.
  **Four assertions, harness 17 -> 21:** a past-year figure is silent; a current-year mention does
  NOT excuse a wrong figure; the comma-walled "As of <year>," opener still fails on a wrong figure;
  and a year AFTER the figure does not excuse it, pinning the bound against a later refactor.

---

## CLOSED July 29, 2026 (v17 argument rewrites) - shipped

- **Both P0 editorial items from the rebase, closed together because they were one cause.** v17
  collapsed a price ordering that two pages had built arguments on. Neither was fixable by swapping
  figures: correcting the numbers alone would have published false claims in accurate digits.
  **`best-places-to-retire-in-florida.html`, three prose surfaces.** The cheapest-FAQ ran a
  three-city budget ladder. Under v17 Pensacola, Fort Myers and Delray Beach are ALL D2=7 and ALL
  Range 2, so the ladder is gone entirely and not just the Pensacola/Fort Myers rung the item
  described. Rebuilt on the spread: the budget score no longer separates them, so what the $73,000
  between them buys does. Fort Myers is +$41K for healthcare 9 and airport 9 against resilience 1;
  Delray is +$73K for walkability 8 and community 9 against healthcare 5; Pensacola holds the floor
  and pays in Panhandle winters. Figures: Pensacola `$264,000` -> `$269,000` and `$4,900` ->
  `$5,000`, Delray `$341,000` -> `$342,000`, Fort Myers `$372,000` -> `$310,000`. The banned
  dataset-scoped opener is gone, re-anchored to named cities and figures. The `bestfor-why` value
  card keeps Pensacola and Fort Myers as its named picks: Delray now has an equal claim on D2=7 /
  Range 2, but that is a placement call and there is no Florida scoring-analysis doc to govern it.
  **The same page's comparison table, folded in by decision.** Not part of the boarded item, which
  scoped to three prose surfaces, but leaving it would have published a page disagreeing with
  itself: six stale home figures (Pensacola `$266K`, Fort Myers `$312K`, Delray `$340K`, Tampa
  `$377K`, St. Pete `$352K`, St. Augustine `$432K`) and five stale Budget/D2 scores (Naples 3->5,
  St. Augustine 5->6, Sarasota 5->6, St. Pete 6->7, Delray 6->7). D3, D6, D9 and D4 all verified
  correct. Row order is by home value and survived the rebase unchanged. Nothing on the site reads
  this table.
  **`cities/st-augustine/profile.html`, six figures in four places.** The old frame was a price
  BRACKET, above Tampa and under Sarasota, meaning expensive but not extreme. v17 puts St. Augustine
  above both, so the bracket could not be repaired. Rebuilt on the scale mismatch: a town of about
  15,000 pricing above two Gulf Coast metros. Tampa `$400,000` -> `$380,000` x3, Sarasota `$462,000`
  -> `$413,000` x2 (the inverting one), Fort Myers `$372,000` -> `$310,000` x1. Also closed the
  `$433,000above` run-together in the JSON-LD, a doubled resilience clause that stated the same
  thing twice in one sentence, and the cost-strip DB citation `v14` -> `Jul 27 v17` (0.78% and
  $7,136 both verify).
  **One v14 reference deliberately NOT relabelled.** The related-city picks comment records a
  COMPUTATION, not a figure: "Sarasota and St. Petersburg tie as closest published Florida matches
  (distance 11)". Recomputed under v17, the Manhattan D1-D10 distance does reproduce 11 for both,
  which confirms the metric, but **Miami also lands at 11 and Miami is published**, so it is a
  three-way tie now and stamping v17 on a two-way-tie claim would make it newly false. Dated
  instead: `Jun 9 v14, not recomputed against v17`. Miami reviewed and rejected on editorial
  grounds Jul 29 (not the same retiree as St. Augustine), so the picks themselves stand.
  **What no check caught.** The five stale D2 scores in the table, and the banned "Of the Florida
  cities scored on RetireMeHere" phrasing, which `check_superlatives` does not match. Both found by
  hand.

---

## CLOSED July 28, 2026 (P0 figure batch + triage scale) - shipped

- **13 P0 figures fixed, and the scale that decided they were the only 13.** An OPS chat scoped
  to the stat-card + FAQ check ran a draft of that check across all 47 profiles and found 44
  figures that disagree with v17 on surfaces nothing has ever read. The check itself did NOT
  ship in this batch, deliberately: see the P2 item below. What shipped is the subset a reader
  can see and act on.
  **Ten abbreviated monthly stat cards**, all off by $300 to $600 per month: Carlsbad
  `$10.9-13.6K` -> `$10.4-13K`, San Antonio `$5.1-6.4K` -> `$4.7-5.8K`, Charlottesville
  `$5.5-6.8` -> `$5.8-7.3`, Ann Arbor `$5.6-6.9K` -> `$5.9-7.3K`, Charleston `$5.6-7K` ->
  `$6-7.4K`, Salt Lake City `$5.7-7.1` -> `$6-7.5`, Fort Myers `$5.5-6.8` -> `$5.2-6.5`,
  Memphis `$4.1-5.1K` -> `$3.8-4.8K`, Roanoke `$4.4-5.4K` -> `$4.6-5.7K`, St. Louis
  `$4.4-5.4K` -> `$4.1-5.2K`.
  **Three visible home figures**, all contradicted by the same page elsewhere: San Antonio
  `~$320K` -> `~$251K` and St. Louis `~$235K` -> `~$192K`, both in the `method-callout` box at
  the head of the Where to live section; Memphis `$195K` -> `$147K` in the `hoods-intro`.
  Carlsbad is the one to remember: its `stat-sub` on the very next line already read
  "Tier 5 - $10,400 to $13,000 a month", so the card contradicted its own subtitle, and the
  gate read 0/0 over it.
  Not in this batch, and boarded as P1 rather than fixed: twenty monthly cards off by exactly
  $100, five home figures off by $1K to $9K, and Pensacola's Budget Score tile reading 8 where
  v17 says D2 = 7. (CORRECTED Jul 28: twenty-six is wrong, the remainder was 31, and the shipped
  check reports 36. See the third-push log entry.) All real, none of them changes what a reader
  does, and all twenty-six are
  what the P2 check exists to hold. Fixing them by hand before the guard ships means doing it
  again after the next DB refresh.

---

## BOARDED - opened by the stat-card check (Jul 28)

- **[P1] `.site-header` and `.section-nav` are both pinned to `top: 0`.** Found July 29 alongside
  the stat-label fix, same block of CSS. The header carries `z-index: 100` and the nav `z-index:
  50`, so when the nav sticks it slides UNDER the header instead of stacking below it, and the
  chips are clipped along their top edge. Visible in the same screenshot that surfaced the label
  bug. Likely fix is `top: <site-header height>` on `.section-nav` plus a matching
  `scroll-padding-top`, which is currently `64px` and looks too small for the two bars stacked.
  Not touched, because unlike the label bug the arithmetic cannot be settled from the CSS alone:
  the header's height is padding plus content and wants measuring in a browser. All 48 profiles.

- **[P3] Nothing on the site reads rendered geometry.** The stat-label bug lived in the canonical
  template and shipped into 48 profiles, and no check could have caught it, because the markup was
  correct and the pixels were wrong. Open question rather than a task: a check asserting the
  stats-bar pull-up stays smaller than its top padding would have caught this exact bug and
  nothing else, which may not earn its keep. Worth deciding deliberately rather than by default.

- **[P2]** **43 run-together money figures across 40 of 48 profiles.** `$326,000with`,
  `$223,000though`, `$858,000with`. Found Jul 30 while fixing a single instance on
  `cities/pensacola/profile.html`, which turned out to be 1 of 44, not a typo. It is
  template-inherited: 17 sit in the identical stat-card FAQ sentence "As of 2026, the typical home
  value is around $X" and the rest in three close variants. Trailing words are `with` x28,
  `though` x6, `but` x2, `and` x2. The Pensacola one is fixed only because it shared a sentence
  with a false tier claim; the other 43 are untouched deliberately, since fixing 1 of 44 hides the
  pattern. `check_statcard_faq` passes 21/21 and cannot see any of them, which is the more
  interesting half: these are in FAQPage schema, so they are what gets quoted. Fix is one BATCH
  plus a check with a planted-error test.

- **[P0]** **69 stale cost figures on 18 of 20 comparison pages. Quarantined, not fixed.**
  Audited Jul 30 across every DB-derived field. All 69 are in Typical home value, Estimated
  retiree budget or Budget tier; zero are in D1-D10. The ZHVI rebase never reached these pages.
  Now held by `COST_ROW_BASELINE` in the validator, so the gate stays honest while they are
  repaired. Attack in three tiers, hardest first, lowering the baseline in each commit:
    - **Tier 1, argument rewrites, one page per pass.** ~~`st-louis-vs-kansas-city` (gap
      $15,000 -> $65,000, a 333% change, any "same price" framing is dead)~~ **CLOSED Jul 30**,
      eleven surfaces, not the one the headline suggested;
      ~~`san-antonio-vs-fort-worth` (gap +145% AND San Antonio drops tier 2 -> 1)~~
      **CLOSED Jul 31**, and the sizing missed that the price ordering INVERTS. Check the sign,
      not just the magnitude, on the two remaining Tier 1 pages;
      `madison-vs-ann-arbor` (Ann Arbor rises tier 2 -> 3, gap +39%);
      `bloomington-vs-lexington` (gap $37,000 -> $16,000, near noise on a $321,000 house, so
      the "meaningfully cheaper" spine of the page probably cannot stand).
    - **Tier 2, figures plus prose reconciliation, 2-3 per batch.** `sarasota-vs-tampa`,
      `knoxville-vs-nashville`, `knoxville-vs-chattanooga` on gap movement of 30-50%; plus
      `naples-vs-fort-myers`, `naples-vs-sarasota`, `nashville-vs-memphis`, which move under 12%
      but cite the gap 8 to 14 times each, so volume puts them here.
    - **Tier 3, mechanical, one script. CLOSED Jul 30**, 8 pages, 184 edits, baseline 69 -> 39.
      Read the closed entry before sizing Tier 1 or Tier 2: the quarantine count is table rows
      only and undercounted the real surface by a factor of six, and the "under 6% gap movement"
      criterion was wrong on two of the eight. Size by grepping the page for the figure, and tier
      by whether the page ARGUES from it.
  OPEN QUESTION before Tier 3: most monthly estimates are off by exactly $100, which smells like
  a `BUDGET-METHODOLOGY.md` recompute rather than drift. Confirm, and Tier 3 grows.
  GATED Jul 30 by `check_comparison_cta_cost_debt`: 21 profile CTA links point into the 18
  quarantined pages, and that number cannot rise while this P0 is open. Do the orphaned-CTA P1
  after this one, or do it only on the two pages that were never quarantined.
  SECOND: Memphis $195,000 -> $147,000 and St. Louis $235,000 -> $192,000 are NRC cities.
  Check the comparison pages use the citywide-plus-callout convention before swapping, or a
  $147,000 figure ends up stranded beside prose about Germantown at $280K-$500K.


  Found Jul 30. Distinct from the D4/D10 item below, which is about the DIMS label prefix. This one
  is about coverage: the check reads `<td class="metric">D<n> ...` rows ONLY, so typical home value,
  estimated retiree budget and budget tier are unchecked on all 19 comparison pages. That is exactly
  how `st-augustine-vs-pensacola` held a `Budget dimension score` of 5/10 twelve lines above a
  `D2 Budget` of 6/10, in the same table, with the gate green. The July 13 D2 rebuild landed on the
  row the check reads and not the row it does not. Worth a hand-audit of the other 18 pages BEFORE
  writing the check, to size how much stale money is sitting in the blind spot. Ship with a
  planted-error test on a cost row, together with the D4/D10 fix below.

- **[P2]** **`check_comparison_scores` cannot see the D4 or D10 rows on any comparison page.**
  Found Jul 29 while rewriting the Pensacola pairing. The check matches
  `<td class="metric">{dim_label}` as a PREFIX, and `DIMS` carries the DB's column names:
  `D4 Resil.` and `D10 Comm.`, both with a trailing period. Comparison pages write the rows out
  in full as `D4 Climate resilience & insurance` and `D10 Community & culture`, neither of which
  starts with the DIMS label, so `re.search` returns None and the `if not m: continue` guard skips
  them silently. Eight dimensions are checked on every comparison page and two are not, and the
  gate reads 0/0 either way. Both rows happened to be correct on this page (2/1 and 7/7 against
  v17), so nothing shipped as a fix here. The same shape as the D2-column incident this check was
  written for: a check that cannot fail on a surface is indistinguishable from a check that passes.
  Fix is to match on the `D<n>` token rather than the DB column name, with a planted-error test on
  a D4 row before it ships.





- **[P2]** **Money with no anchor at all is still unreadable, and it is not hypothetical.** Three
  figures in this batch were found by hand and by hand only, because they sit under no home-value
  noun, in no structured region, and name no city: `st-augustine`'s "At $432,000 this is a pricey
  small town", the same page's "Price: at $432,000", and `carlsbad`'s "At $1,481,000, Carlsbad sits
  among the priciest coastal markets" against a `$1,388,000` DB figure and a `$1.39M` stat card two
  sentences earlier. All three are fixed here; the SHAPE is not closed. Reaching them means grading
  every dollar figure on the page against Median Home, which fires on monthly budgets, property-tax
  bills and neighborhood prices. The cheaper move is probably a PROFILE-FORMATTING rule that a
  citywide figure must carry its noun, enforced on new builds rather than retrofitted.

- **[P4]** **`prescott` was the only profile writing money as "585,000 dollars".** Three occurrences,
  all in the JSON-LD, all invisible to every money pattern on the site, and all three were stale: the
  home figure twice and the monthly top end once (`7,400` against a DB `$7,500`). Normalised to the
  `$` form the other 46 profiles use, which brings them under `RANGE_RE` and the new check rather than
  adding a spelled-out variant to the token. Worth a glance on the next build that a profile has not
  invented a third money style.

---

## ACTIVE - batch / site-wide operations

- **GAP CLOSED Jul 28, 2026.** `check_statcard_faq` now reads profile prose, the JSON-LD FAQ, the
  method-callout and the NRC. The fourth figure this item predicted turned out to be ten. Original
  text below.
  **[P2]** **Three stale home figures in profile PROSE: FIXED Jul 27. The GAP THAT ALLOWED THEM IS STILL
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

- **[P4]** **Em-dash target list: two pages added Jul 27, two remain out, both already clean.**
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

- **[P2]** **Superlative rules are now PATTERN-based, not string-based - keep them that way.** The old ban was
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

- **[P2]** **Validator: add a climate check group** - the validator compares `index.html` city FIGURES against
  the DB but has never checked the CLIMATE blocks. They happen to match 99/99, but nothing enforces it,
  and the July 13 rebuild added three fields (`janF`, `snow`, `sun`) that live in `index.html` with no
  guard at all. Add a group asserting (1) all five original climate values match the DB per city,
  (2) `janF`, `snow`, `sun` present and non-null for all 99. Silent drift of exactly this kind produced
  the Boulder bug.

- **CLOSED Jul 28, 2026 (shipped).** ~~**[P2]** **Validator: build the profile stat-card + FAQ figure
  check.**~~ Shipped as `check_statcard_faq` in the `profiles` group, with `tools/test_statcard_faq.py`
  as its planted-error test, 16 assertions, five harnesses now in the list. Proof it works on the real
  fault and not only on plants: run against the PRE-batch tree it reports 36 failures naming every one
  of them, and reports nothing else. All 36 are fixed in the same commit.
  Two things changed from the design boarded on Jul 27, both because the sizing pass was wrong about
  them. First, the method-callout is not a NOUN problem, it is a REGION problem: the first money figure
  in a `method-callout` or a `reality-check` block is the citywide home value, always, verified across
  all 22 such blocks. Three were wrong and NONE of the three is reachable by any home-value noun,
  because Tulsa's two blocks and Prescott's both open on the phrase "the $X figure". Tulsa's NRC
  callout was still built on `$194K` after the rebase moved it 14.9% to `$223K`. Second, the region
  walk must accept `aside` as well as `div`: the NRC is an `<aside>`, a div-only walk skipped it
  silently, and that alone would have left Tulsa's NRC unread.
  Original text below.
  **[P2]** **Validator: build the profile stat-card + FAQ figure check.** The 13 drifted figures are now
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
  **SIZED Jul 28, and it is bigger than a check.** A draft of all three sub-checks was run across
  the 47 live profiles. Findings, so the next chat does not re-derive them: 35 of 47 abbreviated
  monthly cards disagree with v17; 1 variable slot disagrees (Pensacola Budget Score 8, D2 = 7);
  8 prose home figures disagree out of 157 matched. Ten of the monthly cards and three of the home
  figures shipped as P0 on Jul 28. (CORRECTED: the remainder was 31, not 26, and the shipped check
  reports 36.) The remaining 26 are P1 and are deliberately left in place: they
  are the check's own regression corpus, and hand-fixing them before the guard exists means doing
  it twice.
  Design settled while sizing, so it does not have to be re-argued: the money token must be
  `\$\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?`, which can only end on a digit or K/M and is what
  stops `$314,000, with` swallowing the comma. The hedge slot is a bounded run that crosses no
  comma, no second `$` and no bound word, which is enough for "the typical home value in Salt Lake
  City is around $580,000" at 28 characters. `hood-card` blocks are excluded structurally, which is
  what keeps Bentonville's Bella Vista `~$300K` and Tampa's Water Street range out; note Pittsburgh's
  Brookline card reads `around $246K` and passes today only because it happens to equal the citywide
  figure. `method-callout` is a THIRD sub-surface where a bare "median" is admissible, because that
  box only ever discusses the citywide home figure: 3 matches site-wide, all three were wrong, and
  San Antonio and St. Louis are reachable no other way. The variable-slot rule fires only on a
  `N/10` value, so `Healthcare: Barnes-Jewish` is out of scope, and a `N/10` under an unmapped label
  is a FAIL rather than a skip.

- **[CLOSED Jul 30]** **Two DB summer-comfort values do not survive scrutiny, and they feed the QUIZ, not just
  two pages.** Found Jul 30 while clearing the inverted summer label. `Climate Hot Sum` carries
  0.35 weight in the Mild Year-Round climate score, so this is a matching-engine defect that
  happens to also be visible on two comparison pages.
    - **Memphis = 8.** Memphis is hotter than Nashville on every other column (HEAT 8 vs 7,
      HUM 9 vs 8, Jan 42F vs 39F) and scores THREE POINTS MORE COMFORTABLE. At 8 it is the most
      summer-comfortable city in the entire southern set, ahead of Knoxville 6, St. Louis 7 and
      Kansas City 7, all of which are cooler in July. Memphis is Mississippi Delta. Compare
      New Orleans 2, Miami 2, San Antonio 3, Tampa 4. A defensible value is 3 to 4.
    - **St. Petersburg = 7 against Tampa = 4.** Identical HEAT (7), identical HUM (9), Jan means
      one degree apart, twenty miles apart. St. Pete's peninsula breeze is real but it is not
      three points of it. One of the two is wrong; the pair cannot both be right.
  Both need a scoring decision from Laurie, not a mechanical fix, because the correct value is a
  judgment against the rubric anchors. Everything downstream waits on it: the DB cell, `index.html`,
  the two profiles, the two comparison pages, and the quiz.

- **[CLOSED Jul 30]** **`nashville-vs-memphis` and `tampa-vs-st-petersburg` carried the inverted summer
  label, deliberately.** Held back from the Jul 30 batch. Relabelling them without fixing the DB
  first would convert a currently-buried wrong number into a prominent confident claim: the table
  would assert Memphis has 8 of 10 summer comfort. Worse on `nashville-vs-memphis`, where the PROSE
  is factually RIGHT about reality (it says Memphis "sits in the Mississippi Delta and is
  meaningfully hotter") while citing the numbers through the inverted label, explicitly, in the
  words "hot summers (5 vs. 8, where lower is milder)". Two errors currently cancel and the page
  reads correctly by accident. Fixing either one alone breaks it. Four prose sites need rewriting,
  including the claim that "Nashville wins every climate-comfort row". Both pages also carry a
  checkmark on the wrong city, which is a SYMPTOM of the bad value rather than a separate bug:
  the 2-point rule means only an implausible gap is wide enough to generate a mark in this column.

- **[P3]** **Visible FAQ text and FAQPage schema are out of sync on 6 pages, 7 Q&As.** Audited
  Jul 30 across all 24 pages carrying FAQ schema. Two were fixed in the same pass because this
  batch already opened those files: `nashville-vs-memphis` Q2 (`Franklin/Brentwood` in schema vs
  `Franklin and Brentwood` visible) and `tampa-vs-st-petersburg` Q5 (schema reads "and Tampa Bay
  is among", visible reads "with Tampa Bay among"). Still open: `bend-vs-boulder` Q2,
  `san-antonio-vs-fort-worth` Q2, `scottsdale-vs-santa-fe` Q3 and Q5, `visit-before-you-decide` Q2.
  All seven are wording-level, none change a figure, so this is P3 rather than P2. The check is
  cheap and mechanical: parse the JSON-LD, strip tags from the visible pairs, compare normalised.
  Worth shipping WITH the check rather than as a one-off sweep, since nothing prevents recurrence.

- **[P2]** **A published figure on `nashville-vs-memphis` matches no formula anyone can find.**
  The page cited "a mild-year-round score of 7 vs. 5" in two places. The rubric's documented
  formula (W*0.40 + H*0.35 + M*0.25) gives 6 and 6. The code in `getCityScore` gives 4 and 3.
  Neither is 7 and 5. The clause was CUT on Jul 30 rather than recomputed, because publishing a
  third unsourced number would be worse than publishing none. Two questions behind it: where did
  7 and 5 come from, and do other comparison pages cite a mild-year-round score from the same
  unknown source? Grep before assuming this page is the only one.

- **[P2]** **The rubric documents a climate formula the code does not run.** Second instance of
  rubric-vs-code drift, alongside the D1 filter item already boarded. `scoring_rubric_v3.2`
  publishes Mild Year-Round as (Winter x 0.40) + (Summer comfort x 0.35) + (Humidity x 0.25).
  `getCityScore` implements a worst-of-winter-and-summer model driven by janF, HEAT and HUM, and
  never reads `Climate Hot Sum` at all. Warm & Dry, Four Seasons and Cool/Mountain also differ
  from their documented forms. Either the rubric or the code is the spec; right now neither is,
  and the rubric is the one being used to score new cities by hand. Fold into the Rubric v3.3 item.

- **[P3]** **`Climate Hot Sum` is maintained but unread. Decide whether to keep it.** It is
  published on comparison pages and hand-maintained across 99 rows, and no code path consumes it.
  Either wire it into the climate scoring, in which case the two bad values were a live defect
  waiting to happen, or retire the column and drive the comparison rows off HEAT and HUM, which
  are what the engine and the profiles already use. Leaving it as decorative data guarantees it
  drifts again.

- **[P4]** **Wilmington NC scores 6 on `Climate Hot Sum` with HEAT 7 and HUM 9.** Same twin group
  as the Florida 4s. May be justified by latitude the way Pensacola's 5 is, may not. Cheap to
  settle next time the climate columns are open.

- **[P2]** **Climate rows have no validator coverage of any kind.** Nothing reads them, which is why
  an inverted label survived on eight pages and two bad DB values survived in the quiz. Two checks
  worth having, each with a planted-error test: (1) label-to-column polarity, asserting the rendered
  label agrees with the column's direction, and (2) a DB-side consistency assertion that
  `Climate Hot Sum` does not contradict `HEAT (0-10)` beyond a tolerance. On the second, note the
  crude form (`10 - HEAT`) has a correlation of only -0.693 and flags plausible cities like
  Burlington and Traverse City, so the check needs to be RELATIVE (within-pair, or against
  same-region peers) rather than absolute, or it will cry wolf.

- **[P3]** **Open question from the same audit: is `Climate Hot Sum` calibrated absolutely or on a
  curve?** St. Louis and Kansas City both score 7 with HEAT 8 and 8/7 humidity, and
  `st-louis-vs-kansas-city` describes "hot, humid summers" in prose two paragraphs from a 7 of 10
  comfort score. If the column is graded relative to the database rather than absolutely, that is
  fine and should be written down. If it is meant to be absolute, a cluster of Midwest cities is
  three points high. Not blocking, but it decides whether the check above is even well-defined.

- **[P1]** **Latent label bug on `knoxville-vs-chattanooga`: inverted climate scale.** The summer row is labeled
  "Hot summers (lower = milder)" but populated from `Climate Hot Sum`, which the rubric defines as summer
  COMFORT (10 = comfortable, 1 = extreme heat) - so higher is milder, and the label says the opposite.
  Invisible there because both cities score 6, but the label is wrong. The new `knoxville-vs-nashville`
  page uses the correct "Summer comfort (higher = milder)". Fix the Chattanooga label on its next touch;
  audit other comparison pages for the same inverted wording while at it. Latent, not live-wrong.

- **[P4]** **Visit-block hooks: 4 profiles open on a template.** `asheville`, `bend`, `boulder`, `fort-collins`
  all open the Visit hook with "A scoring sheet can't tell you..." / "A scoring sheet only tells you...".
  PROFILE-FORMATTING.md is explicit that the hook must be "the single most concrete, specific, appealing
  thing about the city... never a generic adjective" and "do not open with a template; every hook opens
  differently from every other block." These four are the last scaffolding repeat in the set: the other
  39 hooks are distinct, and the rental-line openers are 42/43 distinct. Small, precise, judgment-based
  rewrite of four opening sentences. Not batchable.

---

## BOARDED - opened by the layout-check work (Jul 28)

- **[P3]** **Any doc that lives outside the repo is unwatchable.** Section 4a makes the repo
  canonical and the enumeration rule keeps repo docs honest, but `SKILL.md` sits in
  `/mnt/skills/user/` and this project's own instructions sit in project settings. Both
  restated the hand-off shape, both went stale on Jul 14, and neither could be caught by
  anything. The skill is now rewritten to delegate to the repo docs instead of restating
  them. **The project instructions still say the old thing** and should get the same
  treatment: they currently ask for `<city>-profile.html` and city-prefixed photos to
  rename at deploy time. Worth a periodic audit of both against the repo, since no tool
  can do it.

## BOARDED - opened by the Casper build (Jul 28)

- **[P4]** **The NRC roster grep over-counts.** `PROFILE-FORMATTING.md` v1.6 names
  `grep -l 'reality-check-eyebrow' cities/*/profile.html` as the enumeration of record, but that
  matches the CSS selector as well as the markup, so profiles carrying the inherited stylesheet
  and no callout are counted. Knoxville, Roanoke and Prescott are three such today; the grep
  returns 17. Tighten it to `grep -l 'class="reality-check-eyebrow"'` and re-count. Casper was
  built with the unused NRC CSS stripped, so it does not add to the problem.
- **[P1]** **index.html Casper scoreNotes name the hospital "Wyoming Medical Center".** It has been
  Banner Wyoming Medical Center since the Banner Health acquisition. Low urgency: with
  `Casper_WY` now in PUBLISHED_PROFILES the inline detail view never renders. Fold into the
  next BATCH.

## ACTIVE - city profile builds

- **Next in queue:** open. Casper shipped Jul 28.
- Live profiles: 47. Casper shipped Jul 28; Tulsa Jul 24; Roanoke the same day; San Antonio Jul 19; Fort Collins,
  Prescott, Knoxville and Savannah shipped earlier in the same window.
- NRC city count: **17 profiles carry a callout**, not 10 and not 12. Both the June count and the
  Jul 24 "San Antonio makes 11, Tulsa makes 12" note were wrong. Closed Jul 25: neither
  `PROFILE-FORMATTING.md` nor `MEDIAN-HOME-METHODOLOGY.md` enumerates NRC cities any more. The
  enumeration of record is `grep -l 'reality-check-eyebrow' cities/*/profile.html`. Do not
  reintroduce a list in either doc.
- **Tulsa follow-ups:**
  - **CLOSED Jul 28, 2026, verified.** ~~`pick-and-compare.html` carries Tulsa at `d2:7`; DB and
    `index.html` both say **D2 = 9**. Stale.~~ The 72-score job carried it: the live blob now reads
    `d2: 9` for Tulsa, and Coeur d'Alene, boarded separately as unreachable by name-keyed checks,
    now reads `$611,000` against a v17 `$611,000`. Both checked against live `main` on Jul 28. The
    SHAPE of the Coeur d'Alene hole is still open and is boarded as P2; only its data is clean.
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

- **[P2] `check_docs` reads its profile count from the first regex hit anywhere in the board, so it
  passes by coincidence.** Found Jul 29 while auditing board currency. The check's docstring asks
  whether TASKBOARD and SITE-OPERATIONS-LOG are current with the live repo, and it tests that by
  comparing a profile count. It finds that count with `re.search(r"(\d+)\s+profiles", board)`,
  which takes the FIRST match in the file. Today that resolves to a fragment of narrative prose
  inside a header entry, "so all 48 profiles inherited it", which happens to be right.
  **Why it will break.** The board currently holds twelve `<N> profiles` strings reading
  48, 48, 47, 47, 47, 47, 47, 46, 48, 48, 36, 45. Session notes routinely name historical counts.
  The next entry written above the assertion that says 47 will fail the gate on a correct board.
  Worse in the other direction: the deliberate claim the check exists to guard,
  `**Verified live at last update:** N profiles`, could go stale and still pass because some
  paragraph above it names the right number.
  **Fix.** Anchor to the labelled assertion rather than the first match: read the
  `**Verified live at last update:**` line specifically, so the board has exactly one place that
  has to be true. Needs a planted-error test both ways, a stale assertion must fail and a
  historical count in prose above it must NOT.
  **Same family as two items already on this board:** the `check_comparison_dims` prefix-match on
  `D4 Resil.` / `D10 Comm.`, and the `check_hardcoded_counts` hyphen variant that hides
  "100-city database (v14)". Three instances of one pattern, a check that can pass for the wrong
  reason. Worth reading the other checks for the same shape while in there.

- **[P2] The recency chain has no structural check and silently grew a second `Before that:`.**
  Found Jul 29. The header ladder is Last updated -> Before that -> Earlier -> Previously, and each
  session is meant to demote the one above it. A chat inserted an entry without demoting, so two
  `Before that:` blocks coexisted and nothing noticed. Three assertions would close it: exactly one
  `**Last updated:**`, one `**Before that:**`, one `**Earlier:**`. Stateless, unambiguous, no
  false-positive risk, and cheap enough to fold into `check_docs`.
  **Deliberately NOT proposed: orphan detection.** Catching an item removed from the board with no
  CLOSED entry is the failure that lost the `pensacola-vs-fort-myers` record, but it needs the
  previous board version, which means git working-tree state. The gate runs on fresh clones where
  that state is unreliable, and a check that behaves differently depending on how it was invoked is
  worse than the gap it closes. Left uncaught on purpose.
  **The cause this does not reach.** Board edits are remembered rather than structural: they live
  in whatever apply script gets written that session. Three of five board updates on Jul 29 were
  complete. A `tools/apply-template.py` skeleton with the board block pre-stubbed would make
  omission require deletion rather than recall, which is the only fix that addresses the actual
  failure mode. Not boarded as a task, because it is a convention decision rather than a defect.

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

- **[P2]** **Two pillar pages have no city cards at all, so `check_cards` reads them and finds nothing.**
  `best-places-to-retire-in-florida.html` and `best-places-to-retire-in-the-midwest.html` are both
  in the `check_cards` target list and both parse to ZERO cards: they use `bestfor-card` markup, not
  `city-card`. The check fetches them, iterates nothing, and passes. This is the silent-no-op shape
  the emdash harness already exists to prevent, sitting in a different check. Note this is NOT the
  same hole as the roster gap just closed: those pages carry no per-city cards to check, so their
  figures live in prose instead, and see the Florida item directly below for what that let through.
  Fix is a decision, not a patch: either bring their money prose under a check, or drop them from the
  `check_cards` list and say in the code why they are exempt. Leaving them listed-but-unread is the
  worst of the three, because the target list currently reads as coverage.



- **[P3]** **The site nav is copy-pasted into 87 files in seven variants, and 46 of them cannot take a menu
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

- **[P1]** **Florida and Midwest pillar titles both claim "The 8 Best Places" and both render six cards.**
  Noticed while listing the pillars for the menu decision. Not verified further and not fixed: the
  count may be stale, or the pages may deliberately narrate 8 while carding 6. Worth ten minutes
  before either page gets promoted anywhere, since the title tag is what search results show.
  Note `check_hardcoded_counts` does not catch these, for the same reason it missed the "100-city
  database (v14)" string already boarded: the number is fused into prose it does not scan.



- **[P3]** **Rubric v3.3.** `scoring_rubric_v3.2` is wrong in six places, four of which are already resolved
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
  **(7) The D2 median-home band table does not describe what the database does.** Added Jul 29
  from the band-mover review. The rubric publishes `$525-$750K` as a 3-4 band; every one of the
  twelve cities the database holds between `$495,000` and `$571,000` scores 5 or 6, none lower.
  The scores are peer-consistent and correct, so this is the table that is wrong, and it is the
  most actively harmful of the seven: the other six are stale descriptions of settled decisions,
  whereas this one will actively mis-score the next city anyone adds from the rubric alone.
  Either restate the bands to match practice or say plainly that the bands are indicative and
  the peer cross-check governs.

- **[P4]** **MEDIAN-HOME-METHODOLOGY.md needs three lines and was deliberately not touched on Jul 27.**
  (1) Section 1 says the figure is "refreshed annually"; the first annual refresh has now actually
  run, so record the date and that it used the 2026-06-30 ZHVI column. (2) Note that the refresh is a
  column swap against a file already in hand, not research; section 6 currently reads like a research
  task ("pull current Zillow ZHVI for all 99 cities") and will mislead the next operator. (3) Section
  6's out-of-cycle triggers should record that this refresh fired OUTSIDE the June cycle and why
  (Memphis 33% off was the credibility trigger in practice); a doc that says "annual" with no record
  of an off-cycle run invites the next operator to wait until June. Separately, section 9 lists
  `/methodology.html` as a surface this methodology touches. It 404s and is not in the sitemap.
  Either build it or strike the line.

- **[P2]** **`check_highlight_surfaces` enforces highlight parity but not SCORE parity.** `pick-and-compare.html`
  carries its own JSON blob (`monthlyEst`, `monthlyMid`, `medianHome`, `medianHomeMid`, `budgetTier`,
  `d2`) and nothing held it to the DB, so d2 drifted on 72 of 99 cities unnoticed. All ten dimensions
  now agree across both surfaces, but nothing stops it recurring. Extend the check to every `dN` field
  plus the four cost fields. Planted-error test required.
- **[P2]** **A city whose name contains non-ASCII is invisible to the surface checks.** Coeur d'Alene is stored
  `Coeur d\u2019Al\u00e8ne` in the pick-and-compare blob, so name-keyed checks skip it. Its record was
  stale at $553K against a DB $611K and the gate read clean. Any check that joins the two surfaces by
  literal name has this hole.
- **CLOSED Jul 28, 2026 (shipped).** ~~**[P2]** **The abbreviated stat-card money form is
  unparsed.**~~ Now parsed and gated by `check_statcard_faq`. Final count on the profile surface was
  35 of 47 wrong, of which 10 shipped as P0 on Jul 28 and the remaining 25 in this commit.
  **[P2]** **The abbreviated stat-card money form is unparsed.** The editorial modal renders
  `value: '$3.5–4.8K<span>/mo</span>'`. The validator reads `$X,XXX–$X,XXX` only, so St. Louis sat at
  $3.5-4.8K against a DB $4,100-$5,200, wrong before the rebase and never flagged. Same hole for the
  `$192<span>K</span>` home form.
  **Measured Jul 28: 35 of 47 live profiles carry a wrong abbreviated monthly.** Not a St. Louis
  quirk. Ten were off by $300 to $600 and shipped as P0 the same day; twenty are off by exactly
  $100 and are P1 pending the check. The rendering convention is one decimal with a trailing `.0`
  dropped, established by the 12 cards that were already correct, and both span variants are live
  (`$5.9-7.3K<span>/mo</span>` and `$5.8-7.3<span>K/mo</span>`), so a comparison has to normalise
  HTML entities before it reads.
- **[P2]** **No vintage check on `Median Home`.** The rebase fixed the values; nothing prevents the column
  ageing into a patchwork again. Add a gate check that flags any DB figure more than N% off the
  current ZHVI CSV, as boarded on July 26. This is the mechanism fix, not the data fix.
- **[P2]** **A `Monthly Est == f(Median Home)` assertion would have caught 31 cities. Now unblocked.**
  The doc dependency is CLOSED as of the July 27 doc push: BUDGET-METHODOLOGY.md sections 5 and 6
  now publish the exact per-state multipliers as tables rather than ranges, and the formula is
  confirmed to reproduce all 99 rows of v17 exactly, zero mismatches, on both the Monthly Est
  string and the Budget Range integer. Nothing further is needed from the docs. What remains is
  building the check itself and its planted-error test. Asserting it on the gate makes an entire
  class of drift impossible. Highest-value single check on this board.
- **[P1]** **DB title cell still reads "100 cities"** against 99 rows, and `pick-and-compare.html` line 918
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
- **[P1]** **Memphis card and arts doc will go stale in autumn 2026.** `top-cities-for-arts-lovers.html` and
  `docs/arts-lovers-cities-scoring-analysis.md` both name `Brooks Museum of Art`. It is genuinely
  open in Overton Park today, so nothing was changed. It closes there in autumn 2026 and reopens
  downtown in December 2026 as the **Memphis Art Museum**. Two edits, both dated, both known now.
  Do them at the autumn close, not before.
- **[P4]** **Enrichment-vs-DB property tax is a category mismatch, not a set of bugs.** The Jul 24 board read
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
- **[P3]** **Institution-status checks are still manual.** Gilcrease was caught twice by hand. The validator
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

**[P1] 8 of 20 live comparison pages have no CTA link from either city profile.** Built, indexed,
in `sitemap.xml`, and unreachable from the two pages whose readers most want them. Orphaned:
`bend-vs-boulder`, `fort-collins-vs-boulder`, `knoxville-vs-chattanooga`, `knoxville-vs-nashville`,
`san-antonio-vs-fort-worth`, `scottsdale-vs-santa-fe`, `st-louis-vs-kansas-city`, and
`nashville-vs-memphis` until the Jul 30 fix above. The other 12 are correctly linked from both
sides, so the pattern is established and this is wiring, not design. Needs a CTA block on roughly
eleven profiles, each with its own short tradeoff paragraph, so it is an editorial batch and not a
mechanical one. Build-order note: a comparison page ships without any step that returns to the two
profiles, which is why this accumulates.

**[P2] Add `check_comparison_cta_reciprocity` to the validator.** For every
`*-vs-*-retirement.html` in the repo root, assert that both named city profiles link to it, and
that no profile links to a comparison page that does not exist. Planted-error test required before
ship, per the standing rule. Would have caught all 8 orphans and would catch the reverse case the
day a comparison page is renamed.

**[P3] Add `check_lists_heading_count` to the validator.** Parse the `lists-section` `<h2>`, map
the number word to an integer, compare against the count of `.list-card` anchors in the same
section, fail on mismatch and skip cleanly when the heading carries no number. Would have caught
all six headings closed above. Planted-error test required.

**[P3] Stale placeholder comment on `cities/kansas-city/profile.html`.** Line reads
`<!-- COMPARE THESE: Kansas City vs. St. Louis (placeholder - comparison page not yet built) -->`
above a block that is now a working Midwest guide CTA, and `st-louis-vs-kansas-city-retirement.html`
is live regardless. Invisible to readers, misleading to the next person editing the file. Fold into
the CTA wiring batch above.

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty)

---

## PARKED / BACKLOG

- **[P1]** **Four CityDatabase / index.html data conflicts on San Antonio, surfaced during the Jul 19 build.**
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
- **[P4]** **San Antonio landing-page placements: Healthcare Tier 2 and Arts Lovers Tier 2.** BATCH scope.
  Neither scoring-analysis doc evaluated the city at all (zero mentions), so these are omissions, not
  rejections. Healthcare Tier 2 is defined as "major university medical center or state flagship";
  San Antonio has University Hospital plus UT Health San Antonio with the Mays Cancer Center holding
  NCI designation, the same credential that places Miami in Tier 2. Arts Tier 2 runs 8.3 to 8.8;
  San Antonio reads 8.3 to 8.5 against Fort Worth at 8.4. Touches five files: the two landing pages,
  the two scoring-analysis docs, and a return trip to `cities/san-antonio/profile.html` to take the
  Lists section from 2 cards to 4.
- **[P4]** **`PROFILE-FORMATTING.md` NRC list is stale at ten cities.** San Antonio is the eleventh.
- **[P2]** **Validator superlative check matches `on this list` literally and fires on within-page lists.**
  Caught `cities/san-antonio/profile.html` ("the most genuinely urban option on this list") on Jul 21,
  where "this list" meant the four neighborhood cards in the same section, not the city dataset. The
  claim does not rot when a city is added, so this is a scoping false positive. Two sibling phrases in
  the same section ("the most expensive of the inner-loop municipalities", "the most house per dollar
  of the retiree-target areas") pass, which confirms the check is keying on the string and not the
  shape. Copy was rewritten rather than the check loosened. If the pattern is scoped later, it needs a
  planted-error test first.
- **[P2]** **`scripts/generate_brief.py` is referenced by the `retiremehere-city-profile` skill but is not in
  the repo** (404 on raw). The Jul 19 brief was computed by hand against the thresholds documented in
  the skill. Either commit the script or amend the skill; as written it points the next build at a
  file that is not there.
- **[P4]** **Landing-page card counters are positional, not ranks.** `top-cities-for-foodies.html` numbers
  restart at 1 per tier and each tier is alphabetical, so the on-page number never has to match the
  scoring-analysis doc's rank. Recorded because it was raised as a discrepancy during the San Antonio
  build and was not one.
- **[P3]** **Rubric doc drift: `scoring_rubric_v3.2` describes a filter the code does not run.** The rubric says
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
- **[P3]** **`D4` key reuse for Climate Resilience & Insurance.** The dimension occupies the internal key `'D4'`,
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
