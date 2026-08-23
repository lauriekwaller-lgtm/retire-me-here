# RETIREMEHERE TASKBOARD -- ARCHIVE

Completed work, split out of `docs/TASKBOARD.md`.
This file is history. Nothing here is in flight.
The live board is `docs/TASKBOARD.md`; read that one at the start of a session.

Sections are in the order they appeared on the board, newest first.
Nothing was edited on the way across -- these are verbatim.

---
## CLOSED August 6, 2026 (Burlington VT, BUILD) - shipped

**What shipped.** One new profile at `cities/burlington/profile.html` with three photos, the
routing entry in `PUBLISHED_PROFILES`, the sitemap entry, this board and the ops log. Built from
the live St. Louis canonical against `CityDatabase_Jul_27_v17.xlsx`. Gate clean at zero failures
and zero warnings on a fresh clone.

**Emphasis.** D7 Outdoor 9 is the only pillar. Support sits at D3 Health 8, D10 Community 8, and
D6 Walk, D8 Wellness and D9 Safety all at 7. D5 Tax 3 is the single hard flag and leads the "No
if" column, because a permanent annual tax drag binds harder than a preference does. D2 at 5 and
D1 at 6 fill out the honest counterweight. That shape is the MULTI-STRENGTH advisory, so the
profile leads with the outdoor pillar and gives the eight-cluster real weight in the character
section rather than reading as a ski page.

**No NRC callout, deliberately.** `MEDIAN-HOME-METHODOLOGY.md` section 4 makes this judgment,
not a binary test. Citywide is $520,000; the retiree-target areas run South Burlington around
$485K, Williston $500K to $700K, Shelburne $600K to $900K and the Hill Section $600K to $1M and
up. Two of the four sit at or below the citywide figure, so it brackets the range rather than
understating it, which is the doc's explicit "adds noise rather than clarity" case. The spread is
handled in the hood cards and the method callout instead. Reversible in one edit if the read is
wrong.

**Three index.html figures corrected against the database.** Property tax was live at 1.42% on
three separate surfaces (the highlight string, a cons bullet, and the D5 scoreNote) against a DB
`PropTax Rate %` of 1.51. The D2 scoreNote carried a citywide median of $506K attributed to
Redfin against a DB `Median Home` of $520,000, and the attribution went with the figure because
an MLS-shaped source does not belong on a ZHVI-shaped number. All four corrected in the same
commit as the profile, so the profile and the card cannot disagree. `pick-and-compare.html` keeps
its own copy of the highlight string and `check_figures` compares the two surfaces character for
character, so fixing `index.html` alone failed the gate on the first run. Both moved together.

**One conflict left open on purpose.** The DB has `Ann Snow in` at 70 for Burlington; the
`index.html` cons bullet says roughly 80 inches. NOAA's Burlington normal is nearer 81, so the
database cell is the more likely error and editing live copy DOWN to match a suspect cell would
be the wrong direction. The profile uses 70 per the DB rule. Boarded as a P2 below rather than
silently reconciled.

**Board-count trap, noted for the next build.** `check_docs` reads the first
`(\d+)\s+profiles` match in this file. Before this entry that match was in July 29 historical
prose ("all 48 profiles inherited it"), a sentence that is correct as history and must not be
edited. The Last-updated paragraph now carries "49 profiles" above it. The next build has to do
the same thing or the count silently reverts to being graded against a sentence about last month.

---

## CLOSED August 3, 2026 (knoxville-vs-asheville, COMPARE) - shipped

**What shipped.** One new comparison page, wired from both profiles in the same commit, plus the
hub card, the ItemList position, the sitemap entry, and this board. First page built under the
growth cycle boarded above, and the first one to ship wired by default rather than as a follow-up.

**The pairing is lopsided and the page says so.** Knoxville takes eight of the ten dimensions or
ties them. Asheville's case rests on three: outdoor recreation at 10 against 8, walkability at 7
against 5, community at 9 against 8. What makes it a real decision rather than a walkover is that
Asheville's three are the ones people move to the mountains FOR, and Knoxville's two widest,
healthcare at 8 against 5 and tax friendliness at 9 against 6, are the ones people only notice
after they arrive.

**The healthcare gap is not a quality gap and the page had to say so.** The obvious read of D3 8
against 5 is that Asheville's hospital is weak. It is not: US News rates Mission seventh in North
Carolina and high performing in seventeen adult procedures, and Healthgrades has named it a top-50
hospital for eleven consecutive years. What Asheville lacks is a SECOND system. Knoxville carries
UT Medical Center and Covenant Health Parkwest, ranked first and second in the metro
independently. Mission's own trouble is on the other axis: two of five stars for patient
experience, and a CMS immediate jeopardy finding in February 2024, since lifted. Writing "Asheville
has worse hospitals" would have been wrong and checkable; writing "Asheville has one hospital
system" is right and is the thing a retiree can act on.

**Containment, caught in draft rather than in a later audit.** The money block wanted to list the
$166 a year insurance advantage next to the $500 a month budget advantage. BUDGET-METHODOLOGY.md
section 4 puts insurance INSIDE the monthly estimate, so that is the bloomington-vs-lexington
defect exactly: a component of a derived figure presented as a second, additive advantage. The
page now states explicitly that the insurance line is part of the $500 rather than on top of it.

**Airport figures softened deliberately.** McGhee Tyson's own site gives two different route counts
on two different pages, 25 and "more than 30", against 41 on the independent trackers. The page
says "more than thirty", which is the airport's own conservative figure and true under every
source. Asheville Regional publishes 26 across five airlines consistently, so that one is stated
exactly. The standard says verify against the airport's own published figures or soften; when the
airport disagrees with itself, soften.

**Two conventions were in circulation and one had to be picked.** Climate row labels differ across
live pages: `asheville-vs-greenville` uses Winters / Summer heat severity / Summer humidity, which
is what COMPARISON-PAGE-STANDARD-v2 describes, while `knoxville-vs-chattanooga` still carries the
older four-row form with "Warm winters" as a score row, which the standard explicitly rules out.
Built on the former. The older form on the Knoxville pages is now a known divergence and is
boarded below.

**Also corrected while in the files.** The board asserted 47 live profiles against a real 48;
Portland ME shipped July 29 and the line was never updated. And the hub carried "let the quiz score
all 100", a live hardcoded city count that `check_hardcoded_counts` cannot see, because its pattern
requires the word "cities" to follow the digits and this one does not.

**No matchup count was restored to the hub.** The July 31 OPS chat found the hub's count wrong by
one and deleted it rather than correcting it, which was right: a count in words rots exactly like a
count in digits. There is nothing on the hub to bump when a page ships, and that is the intended
state.

---

## CLOSED August 3, 2026 (comparison CTA reciprocity) - shipped

- **Fifteen missing edges, not eight.** The P1 counted PAGES with no link from either side, which
  undercounts the work: `nashville-vs-memphis` was already half-wired, and three profiles sit in
  two matchups each. Sized by grepping every profile for every hub-listed page rather than trusting
  the board number. Twelve profiles edited: `bend`, `boulder`, `chattanooga`, `fort-collins`,
  `fort-worth`, `kansas-city`, `knoxville`, `nashville`, `san-antonio`, `santa-fe`, `scottsdale`,
  `st-louis`. Five of them carry two rivals and use the two-button flex row from the Tampa
  canonical; the rest use the single-button block from `cities/memphis/profile.html`.

- **Three of the twelve already had a block in the head-to-head slot, and none of the three was
  doing the job.** `kansas-city` held a Midwest guide CTA under a comment announcing a comparison
  page "not yet built" that has been live for weeks. `santa-fe` and `scottsdale` each linked
  Tucson and not each other, which is the failure mode that reads as done: the slot is filled, the
  section renders, and the missing edge is invisible unless you enumerate. Each of the three was
  replaced wholesale rather than appended to, so the blurb argues about the rivals actually linked.

- **Every blurb figure re-derived from `CityDatabase_Jul_27_v17.xlsx` before drafting.** Nothing was
  carried from the comparison pages themselves, which are a derived surface. One claim was cut in
  draft: the Fort Collins blurb named taxes as a tradeoff axis, and both cities are in Colorado on
  a D5 of 7. A tradeoff paragraph that names an axis with no gap on it is the prose version of a
  checkmark on a tie.

- **`check_comparison_cta_reciprocity` asserts the EDGE, in both directions.** Every hub-listed
  page is linked from both profiles named in its filename, and every comparison href on a profile
  points at a page that exists. The second direction is the rename case and nothing else on the
  gate reads it. Harness at `tools/test_comparison_cta_reciprocity.py`, eight assertions, harness
  count now eleven.

- **The check had a real bug that the harness caught, and the assertion stayed in.** The first
  draft tested `'href="/page"' in html`, which is satisfied by `data-href="/page"`. The check would
  have passed on markup that links nothing. Fixed with a leading boundary in the pattern, and
  assertion 5 exists to pin it down. Assertion 4 pins the matching decision that a relative href
  does not count: it resolves fine for a reader, and one absolute form site-wide is what makes this
  greppable at all.

- **Build-order finding, unchanged and now guarded.** A comparison page ships without any step that
  returns to the two profiles. That is why this accumulated for months while every figure on those
  same pages sat under three separate checks. The gate now fails the day a page ships unwired, so
  the COMPARE chat no longer depends on remembering.

---

## CLOSED July 31, 2026 (hardcoded counts, prose scores, data vintage - OPS) - shipped

- **Three conventions that lived only as prose in a doc, all three drifted, all three now gated.**
  `check_hardcoded_counts` rewritten, `check_comparison_prose_scores` and
  `check_comparison_vintage` shipped, each with a planted-error harness. Plus a new
  `meta_content()` surface helper. 40 content edits across 15 files.

- **[P1 -> CLOSED] The count was 23 instances across 11 files, not 3.** The earlier sizing on
  this board was wrong, from a `grep -lc` that collapsed its own output; correcting it is how the
  real number surfaced. `check_hardcoded_counts` was shipped, passing, and blind to every one of
  them THREE separate ways: the regex matched `100 cities` but not the adjectival `100-city`; the
  page set read index, the profiles and the comparison pages but silently excluded the hub
  ITSELF, `pick-and-compare.html` and `where-should-i-retire-quiz.html`, which held twelve of the
  23; and no text surface on the site ever read `<meta ... content="...">`, which held four more.
  **A check that reads the wrong pages reports clean for the same reason a check that reads no
  pages does.** Two instances read `99-city`, correct today, retired with the rest.

- **[P1 -> CLOSED] `pick-and-compare.html` line 920 was wrong three ways in nine words.**
  "Scores are 1 to 10 from the RetireMeHere 100-city database (v14)": the count is wrong, the
  version is three releases stale against v17, and the hyphen hid the whole string from the one
  check that would have caught it.

- **[P1 -> CLOSED] The hub told readers "Nineteen honest head-to-head matchups" on two surfaces.**
  There are twenty, and the hub links all twenty. Both are `og:description` and
  `twitter:description`, so the wrong number was what Google, Facebook and every answer engine
  quoted back. Now count-free. **Judgment call to override if you want it:** a corrected "Twenty"
  is wrong again on page 21, which is the failure this policy exists to prevent, so the number
  came out rather than getting bumped.

- **[P1 -> CLOSED] Prose scores are now gated, and the check found instances ten and eleven while
  it was being written.** `madison-vs-columbus` said Columbus had "a budget score of 7 to
  Madison's 6" above a row reading 8; `scottsdale-vs-tucson` said "cost (8 of 10 vs. 3 of 10)" on
  two surfaces against a row reading 4. **Eleven instances in four days and D2 in all eleven**,
  which continues to trace to the July 13 D2 rebuild editing table rows and nothing else.
  The check binds a number pair TIGHTLY to the dimension word; an earlier cut used a proximity
  window and flagged 219 claims on 20 pages, nearly all of them the neighbouring dimension in a
  list. It now matches 90 real claims site-wide and, after this batch, disagrees with none.

- **[P2 -> CLOSED] Data vintage gated.** Eleven captions said June 2026 and twelve `dateModified`
  values predated `CityDatabase_Jul_27_v17.xlsx`, on pages whose every cost row is asserted
  against that database and passes. The caption was understating the data and the schema was
  telling Google the pages were older than they are. New `DB_VERSION_DATE` constant sits beside
  `DEFAULT_DB` and self-checks against the filename, so the two cannot drift apart.

- **[P2] NEW: two em-dash fallbacks in `index.html` that would render if they ever fired.**
  `city.medianHome || '—'` and `city.monthlyEst || '—'` in the enrichment stat-card
  builder. Every city in v17 has both fields, so neither has ever fired, which is why
  `check_emdash` has never seen one: it scopes out script placeholders and these are only em
  dashes at render time. Harmless today and a rendered em dash on the day a field goes blank.
  Two-character fix to `'n/a'` whenever `index.html` is next open. The other 271 literals on the
  site are all in CSS and HTML comments, correctly scoped out, and were audited during this batch.

- **[P2] NEW: the meta description surface is newly readable and only ONE check reads it.**
  `meta_content()` exists now, and `check_hardcoded_counts` uses it. `check_superlatives` and
  `check_emdash` do not, and both have exactly the same blind spot they had before this batch.
  Cheap to extend, worth doing deliberately rather than discovering it the same way again: read
  the descriptions on all 69 pages by hand once, first, so the size is known before the regex runs.

## CLOSED July 31, 2026 (Tier 2 batch B: naples-vs-fort-myers, naples-vs-sarasota, nashville-vs-memphis) - shipped. COST-FIGURE REPAIR COMPLETE.

- **The P0 is closed. All twenty comparison pages agree with v17 on every cost row.**
  `COST_ROW_BASELINE` is now empty, and `CTA_COST_DEBT_BASELINE` and
  `check_comparison_cta_cost_debt` were DELETED in the same commit, which is what that
  function's docstring asks for at zero debt. `check_comparison_cost_rows` survives as a plain
  assertion rather than a ratchet, which is the state it was built to reach. Final tally for the
  repair: 20 pages, 8 batches, and a baseline that counted three table rows per page against a
  reality of roughly 25 to 30 figure surfaces per page throughout.

- **All three gaps WIDEN, two by enough to change the sentences around them.**
  `naples-vs-fort-myers` $213,000 -> $239,000 and 36% -> 44%, so two roundings that read "worth
  more than $200,000" now understate the table by nearly $40,000 and were rewritten to
  "nearly $240,000". `nashville-vs-memphis` $265,000 -> $290,000 and 58% -> 66%.
  `naples-vs-sarasota` $123,000 -> $136,000, and its 25% survives untouched at 24.8%.
  No price ordering inverted.

- **[P1 -> CLOSED] Four more live D2 prose errors, and `naples-vs-fort-myers` disagreed with
  ITSELF three ways.** That page variously claimed "budget scoring 7 vs. 3", "budget scores 6 vs.
  5", and "budget score of 7 against Naples' 3" on four surfaces; v17 and its own table both say
  7 and 5. `nashville-vs-memphis` claimed "Memphis's budget score of 7 against Nashville's 5"
  when v17 has Memphis at **10, a perfect score**, and Nashville at 7, understating both cities
  and erasing one of the highest budget scores on the site. That is instances six through nine of
  the same defect class in four days, **D2 every single time**. The proposed check in the batch A
  entry above is no longer speculative: it would have caught nine of nine.

- **[P1 -> CLOSED] A figure that was never right, and the first CROSS-PAGE contamination in this
  repair.** `naples-vs-sarasota` said the monthly budget ran "roughly $1,300 lower". On the old
  figures the gap was $700 to $900; on the new ones it is $800 to $900. It was never $1,300 on
  any version of the data. `naples-vs-fort-myers` genuinely was $1,000 to $1,300, and the number
  appears to have been carried across when the second page was built from the first. Worth
  knowing that the quarantine list would never have surfaced this: the figure is derived, it sits
  in prose, and it was wrong before the repair started.

- **[P1 -> CLOSED] A dataset-scoped superlative of a new shape: scoped to the COMPARISON SET, not
  the city database.** `naples-vs-sarasota` said it had "more identical rows than any other
  pairing here". Re-anchored to the figure, four of ten dimensions tie outright (D3, D4, D5, D7),
  which stays true as pages are added. Plus the two remaining `100-city retirement database`
  strings in Article schema, matching the four cleared in batch A.

- **CORRECTION TO BATCH A, shipped here.** The caption data-vintage bump required by
  COMPARISON-PAGE-STANDARD-v2 ("update the month whenever scores are refreshed from a new DB
  version") was missed on all three batch A pages. `sarasota-vs-tampa` and
  `knoxville-vs-chattanooga` still read `June 2026` under refreshed July figures; all three had
  stale `dateModified`. Fixed here for all six Tier 2 pages. **The rule is prose in a doc and
  nothing reads it**, which is how it was missed twice: it was also missed on the Tier 3 batch and
  caught by hand then too.

- **[P2] NEW: gate the data vintage, since it has now been missed twice by hand.**
  If a page's cost rows are read from the DB, its caption month and its schema `dateModified`
  should not be older than the DB file's own version date. Both are already parsed by other
  checks. This is the third convention in this repair that lived only as prose in
  COMPARISON-PAGE-STANDARD-v2 and drifted (checkmarks, cost-row marks, vintage).

- **[P1] STILL OPEN, unchanged: the hyphenated hardcoded count on three remaining files.**
  `compare-retirement-cities.html`, `pick-and-compare.html`, `where-should-i-retire-quiz.html`.
  `check_hardcoded_counts` reads "100 cities" and misses "100-city". Six instances cleared across
  Tier 2 by hand; the last three need the regex, not another manual pass.

## CLOSED July 31, 2026 (Tier 2 batch A: sarasota-vs-tampa, knoxville-vs-nashville, knoxville-vs-chattanooga) - shipped

- **Twelve quarantined cells, 82 figure surfaces, and the baseline was wrong by a factor of
  seven again.** Sized by grepping each page: 25 raw occurrences on `sarasota-vs-tampa`, 30 on
  `knoxville-vs-nashville`, 27 on `knoxville-vs-chattanooga`, against a baseline of 4 apiece.
  The extra copies sit in prose, visible FAQ, FAQPage schema, ARTICLE schema, `meta name` and
  `og`/`twitter` descriptions, the hero tagline, the verdict box, a tradeoff HEADING, and the
  profile-card blurbs at the foot of the page. `COST_ROW_BASELINE` 24 -> 12 over three pages;
  `CTA_COST_DEBT_BASELINE` 7 -> 5, recounted rather than assumed: neither Knoxville page has a
  single profile CTA pointing at it, so only `sarasota-vs-tampa` retired edges, and it retired two.

- **Direction holds on all three. Sizes move a lot.** `sarasota-vs-tampa` $62,000 -> $33,000, a
  47% narrowing, so the page's "Tampa simply costs less" spine now carries the number: 8% on the
  house, $200 to $300 a month. `knoxville-vs-nashville` $92,000 -> $60,000 and 25% -> 16%, with
  the monthly advantage halving from $500-$600 to a flat $300, which is why "several hundred
  dollars lighter" had to become a figure. `knoxville-vs-chattanooga` is the one page in Tier 2
  where the gap WIDENS, $40,000 -> $53,000, 11% -> 14%, so "none of the wins are large" was
  retired rather than renumbered.

- **[P1 -> CLOSED] Two live prose errors, both D2, both contradicting their own tables.**
  `sarasota-vs-tampa` said "Tampa's budget dimension scores 6 to Sarasota's 5" in THREE places
  (tradeoff, visible FAQ, FAQPage schema); the table and v17 both say 6 and 6, a tie.
  `knoxville-vs-chattanooga` said "budget scores 9 against 8"; both are 8. That is the fourth and
  fifth instance of the same defect class in four days, and the D2 column is the repeat offender
  every time, because the July 13 D2 rebuild landed on table rows and never touched prose copies.
  **Worth a check.** For every dimension, if prose states "N of 10" or "N against M" beside a
  dimension keyword, assert N appears in that dimension's table row. Cheap, and it would have
  caught all five.

- **[P1 -> CLOSED] Four dataset-scoped claims, on pages nothing was watching.**
  `knoxville-vs-chattanooga` twice: "comfortably above the midpoint of our 100-city database".
  Both Knoxville pages once each in ARTICLE SCHEMA: "from a 100-city retirement database". Banned
  by the superlative rule outright, and wrong on the count as well, since there are 99 cities.
  `check_superlatives` does not fire because the phrase is not a superlative, and
  `check_hardcoded_counts` does not fire because of the hyphen, which is the same blind spot as
  the boarded `pick-and-compare.html` line 918 item.

- **[P1] STILL OPEN and now sized: the hyphenated hardcoded count is on FIVE files, not one.**
  `compare-retirement-cities.html`, `pick-and-compare.html`, `where-should-i-retire-quiz.html`
  and, until this batch, both Knoxville pages. `check_hardcoded_counts` reads "100 cities" and
  misses "100-city". One regex closes it. Do it with the count fix, not separately, or the next
  page built from an old template puts it straight back.

- **Prose claims of the form "sweeps every cost row" are false on every page that has them**, and
  they contradict the visible table, which leaves identical rows unmarked. Three fixed here
  (`knoxville-vs-nashville`, `knoxville-vs-chattanooga` twice). Both Tennessee pairings share a
  state property tax rate and insurance estimate, so two of five cost rows are always ties.
  Check the remaining Tier 2 pages for the same phrasing before renumbering them.

- **Next: Tier 2 batch B**, `naples-vs-fort-myers`, `naples-vs-sarasota`, `nashville-vs-memphis`,
  12 mismatches. `nashville-vs-memphis` carries the NRC convention question from the P0: Memphis
  $195,000 -> $147,000 is a neighborhood-callout city and the page must use citywide-plus-callout
  or it strands a $147,000 figure beside prose about Germantown.

## CLOSED July 31, 2026 (checkmark rule, BATCH) - shipped

- **The rule is TWO POINTS on dimension rows, and it is now written down and gated.**
  `CHECKMARK_MIN_GAP = 2` in `tools/validate.py`, the prose rule in
  `COMPARISON-PAGE-STANDARD-v2`, and `check_comparison_checkmarks` with
  `tools/test_comparison_checkmarks.py` behind it. Twenty-two marks came off eight
  pages, one went on, five captions and five sub-heads were brought onto the current
  template. Scope is D1-D10 rows only: cost rows have no score gap, climate rows keep
  the older context rule that allows a marked 9 vs. 10 WITH an inline explanation.

- **The board said two rules were in circulation. Measuring found one rule and five
  stale pages.** The caption divergence maps almost exactly onto the mark behaviour:
  `asheville-vs-greenville`, `madison-vs-ann-arbor`, `santa-fe-vs-tucson`,
  `sarasota-vs-tampa` and `scottsdale-vs-tucson` still carried the v1 `compare-sub`
  ("The shaded, checkmarked cell on each row is the stronger one. Ties are left
  unmarked.") AND the short caption, while the other fifteen had replaced the sub with
  a pattern sentence and moved to "ties and near-ties". Their tables followed their own
  captions, correctly. It was never a disagreement about the rule; it was five pages
  that never got the template update.
  **Correction to the entry below:** it lists twelve pages and calls them eleven. The
  list was right, the count was wrong.

- **The rule was under-marking too, which the previous entry did not have.**
  `naples-vs-fort-myers` D2 Budget reads Naples 5 against Fort Myers 7, a two-point
  gap, and NEITHER cell was marked, on a page whose own sub-head says Fort Myers
  "sweeps the money rows". The only case site-wide, which is why the check asserts the
  rule in BOTH directions rather than only "marked implies a gap of 2+". Mark added to
  Fort Myers.

- **[P1 -> CLOSED] A live prose error, carry-forward #5 for the third time.**
  `santa-fe-vs-tucson` read "Tucson takes the budget dimension 8 of 10 to Santa Fe's
  6." The table on the same page says 5 and so does v17. One surface only, not
  duplicated into the FAQ. Corrected to 5. Found by scanning prose for the dimensions
  whose marks were changing, which is the only reason it surfaced at all.

- **Prose survived the removals almost everywhere, and that is the evidence the
  two-point rule was always the intended one.** Most pages already hedge one-point
  gaps in words: "slightly safer (7 of 10 to 6)", "Tucson also edges the airport
  comparison", "Active wellness modestly favors Boulder (8 against 7)". Only
  `bend-vs-boulder` described the MARKS rather than the numbers, in a sub-head that
  enumerated rows Boulder and Bend each "take" (four of which lose their mark) and in
  two "Bend takes healthcare / safety" sentences. Rewritten to name the marked rows and
  the near-ties separately. The rule this produced is now in the standard: report a
  one-point gap with both numbers, never as a row a city "takes".

- **Two audits that came back clean and are now gated so they stay that way.** All 200
  dimension cells across the twenty pages agree with v17, including the D4 and D10 rows
  `check_comparison_scores` could not see until the label fix. Shading and the literal
  tick character agree on every marked cell on every page. Both are asserted by the new
  check.

- **[P2] NEW: cost-row and climate-row marks are inconsistent site-wide by a different
  measure, and nothing gates either.** Deliberately out of scope here, boarded with the
  evidence. `knoxville-vs-chattanooga` leaves a $300/mo gap unmarked while
  `asheville-vs-greenville` marks a $700 one; `bloomington-vs-lexington` marks a
  $16,000 home-value gap while other pages leave larger ones alone. On climate,
  `nashville-vs-memphis` and `st-louis-vs-kansas-city` mark one-point rows with NO
  inline context, against the clause in the standard that permits such a mark only with
  context. A cost row needs a percentage threshold, not a point threshold, and nobody
  has written one. Do it as its own BATCH, not inside a Tier 2 page.

- **[P2] NEW: the standard is filed as `docs/COMPARISON-PAGE-STANDARD-v2 .md`, with a
  SPACE before the extension.** Four sessions have referred to it by the clean name and
  nothing matches it; `raw.githubusercontent.com` 404s on every obvious spelling. It is
  why an earlier session concluded the doc had no checkmark rule in it: the doc was
  never opened. It does have one, the climate-context clause, which this batch had to
  reconcile with rather than overwrite. Rename to `COMPARISON-PAGE-STANDARD-v2.md` in
  the next OPS batch and grep the docs for the old string.

## CLOSED July 31, 2026 (bloomington-vs-lexington, Tier 1) - shipped. TIER 1 COMPLETE.

- **Three quarantined figures, and the only Tier 1 gap that closes.** Bloomington $296,000 ->
  $321,000, Lexington $333,000 -> $337,000, Bloomington's monthly $4,600-$5,700 ->
  $4,700-$5,800. The gap narrows from $37,000 to $16,000 and the monthly spread halves from $200
  to $100. `COST_ROW_BASELINE` 27 to 24 over six pages; `CTA_COST_DEBT_BASELINE` 9 to 7.
  **Tier 1 is now closed**: all four pages done, 24 mismatches left, all in Tier 2.

- **The page counted the same money twice, and that predates the rebase.** Tradeoff #2 said
  Bloomington's lower home price "combined with" a monthly estimate below Lexington's makes the
  all-in cost of ownership "meaningfully below". FAQ 3 said the monthly saving "plus" the buy-in
  saving, then called insurance "the standout difference" on top of both.
  `BUDGET-METHODOLOGY.md` section 4 lists homeowners insurance as a HOUSING LINE ITEM of the
  monthly estimate, `HO Insur Est $/yr / 12`. So the $1,155 a year insurance advantage is INSIDE
  the $1,200 a year monthly advantage and is very nearly all of it. Adding them made a 2% monthly
  difference read as a decisive one. Both instances corrected, with the arithmetic written onto
  the page so the next reader can check it rather than trust it.
  **Defect class worth naming: a derived figure that is a COMPONENT of another derived figure on
  the same page.** Nothing in the toolchain models which figures contain which. Worth a look on
  any page that totals a cost advantage, and there are several.

- **Checkmarks left alone here, correctly, and that is how the rule got settled.** This page marks
  only the two-point D3 gap and leaves all three one-point gaps unmarked, matching its own caption:
  "ties and near-ties are left unmarked."

- **[CLOSED Jul 31, second batch] The `madison-vs-ann-arbor` checkmark edit from earlier today went
  the WRONG WAY and should be reverted.** DONE: reverted, together with that page's D4 and D9 marks,
  its caption and its sub-head, and all seven other off-convention pages, in the checkmark-rule
  batch above. Two corrections to what follows. The list of pages leaving every one-point gap
  unmarked has TWELVE names in it and is called eleven; the list is right. And the divergence was
  not two rules, it was five pages still on the v1 caption template.
  The rule was boarded as unsettled that morning, and it is now measured across all
  twenty comparison pages. **Eleven pages leave every one-point gap unmarked** (the two-point rule):
  `bloomington-vs-lexington`, `fort-collins-vs-boulder`, `knoxville-vs-chattanooga`,
  `knoxville-vs-nashville`, `madison-vs-columbus`, `naples-vs-fort-myers`, `naples-vs-sarasota`,
  `pensacola-vs-fort-myers`, `san-antonio-vs-fort-worth`, `scottsdale-vs-santa-fe`,
  `st-augustine-vs-pensacola`, `tampa-vs-st-petersburg`. Four mark them (`nashville-vs-memphis`,
  `santa-fe-vs-tucson`, `sarasota-vs-tampa`, `scottsdale-vs-tucson`) and three are internally
  inconsistent (`asheville-vs-greenville`, `bend-vs-boulder`, `st-louis-vs-kansas-city`).
  The CAPTIONS diverge too, and that is the root: most say "ties and near-ties are left unmarked",
  while `madison-vs-ann-arbor` says only "ties are left unmarked". The Madison edit was defensible
  against its own caption and wrong against the site, and it moved that page from MIXED to fully
  stronger-city, further from the majority. Revert the D2 mark, review its D4 and D9 marks under
  the two-point rule, and restore the "and near-ties" clause to its caption.
  Then: write the two-point rule into `COMPARISON-PAGE-STANDARD-v2`, fix the seven off-convention
  pages, and gate it. The check is cheap once the rule is written: for every marked dimension cell,
  assert the gap is 2 or more and the mark sits on the stronger value. Planted-error test required.

## CLOSED July 31, 2026 (madison-vs-ann-arbor, Tier 1) - shipped

- **Five quarantined figures, and a tier crossing.** Madison $413,000 -> $435,000, Ann Arbor
  $489,000 -> $541,000, both monthly ranges, and Ann Arbor's tier 2 -> 3. The gap widens from
  $76,000 to $106,000. `COST_ROW_BASELINE` 32 to 27 over seven pages;
  `CTA_COST_DEBT_BASELINE` 11 to 9, because both city profiles link to this page and retiring it
  from quarantine retires two edges.

- **The rewrite is small because the direction holds.** Madison was the cheaper city and still is,
  so unlike `san-antonio-vs-fort-worth` nothing had to be reversed. What broke is a SHARED-ITEMS
  list: tradeoff #2 opens by naming five things the two cities have in common, and the budget tier
  and the monthly estimate are two of them. Neither is true now. Same claim restated in FAQ 2 in
  visible copy and in FAQPage schema, and in tradeoff #3's "After that it gets more even". Four
  sentences, one derived property-tax range, and the meta/og/twitter/hero/verdict gap figure.

- **[CLOSED HERE] A checkmark defect that has nothing to do with the rebase.** The page states its
  own rule twice, in the table sub-head and in the caption: "Checkmarks mark the stronger city in
  each row; ties are left unmarked." No two-point threshold anywhere in
  `COMPARISON-PAGE-STANDARD-v2` either. By that rule the page was UNDER-marking: `D2 Budget` read
  Madison 6 against Ann Arbor 5 with no mark on either row cell, and `Estimated retiree budget`
  had none while the figures differed. Both marked for Madison. The `D4` and `D9` marks at
  one-point gaps are correct under the stated rule and were left alone.
  **Worth settling site-wide:** an earlier session recorded a "checkmarks only at 2+ point gaps"
  convention, and this page's own caption says otherwise. One of the two is wrong and nothing
  reads either. Boarded below.

- **[CLOSED Jul 31, second batch] The checkmark rule is not written down anywhere that a check could
  read it, and two versions of it are in circulation.** DONE: settled at TWO POINTS on dimension
  rows, written into `COMPARISON-PAGE-STANDARD-v2` under Table rules, and gated by
  `check_comparison_checkmarks` with `tools/test_comparison_checkmarks.py` behind it. Cost rows and
  climate rows are excluded, for reasons recorded in the closed entry above.
  This page's caption says stronger city wins the mark, ties
  unmarked, full stop. Working notes from an earlier comparison-page pass say marks only appear at
  a two-point score gap. Under the first rule `madison-vs-ann-arbor` was under-marked on D2; under
  the second, its D4 and D9 marks are both wrong. They cannot both be right, `st-louis-vs-kansas-city`
  was reasoned about using the two-point version as recently as Jul 30, and no validator check
  reads a checkmark at all. Settle which rule governs, write it into
  `COMPARISON-PAGE-STANDARD-v2`, then audit all twenty pages against it. Cheap check once the rule
  exists: compare each marked cell against the DB and assert the mark sits on the stronger value.

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

- **The D9 neighborhood-basis caveat on this page is CORRECT, and was briefly boarded as a defect
  in error.** Tradeoff #4 and FAQ 5 tell the reader San Antonio's Safety score is built on
  retiree-target areas and Fort Worth's is citywide. The first read of this batch flagged that as a
  possible fossil of the retired eight-city carve-out, since `MEDIAN-HOME-METHODOLOGY.md` v1.2
  dropped it and `BUDGET-METHODOLOGY.md` section 4 says no city uses a neighborhood basis. Both of
  those are about MEDIAN HOME. The Rubric v3.3 item already settles the rest, at divergence (5):
  the D2/D6/D9 grouping becomes D6/D9 precisely because **D9 is still genuinely
  neighborhood-scored**, with Memphis and San Antonio both at D9=7 where the rubric's own anchor
  puts their citywide figures at 1-2. So the practice is consistent across the site, the page is
  right, and nothing needs rescoring. The stale artifact is the rubric .docx, not any score.
  The wrong version of this entry shipped in `c20fd1f` and is corrected here. Recorded rather than
  quietly deleted, because a duplicate item that CONTRADICTS a resolved one is a worse failure than
  a missing item, and the cause is worth naming: the board was not searched before the item was
  written. The remaining rescoring exposure on Rubric v3.3 is (7), the D2 anchor bands, which were
  calibrated against the pre-rebase median-home column.

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
