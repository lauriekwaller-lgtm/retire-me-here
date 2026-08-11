# DEPLOY: where-can-i-afford-to-retire.html

**Built:** August 10, 2026
**Type:** new tool page. No database change, no score change, no profile or comparison count change.
**Implements:** BUDGET-METHODOLOGY.md section 14 (equity-adjusted variant).

---

## 1. What ships

**New files (in the zip, already at final paths):**

```
where-can-i-afford-to-retire.html
tools/test_afford_data.py
docs/DEPLOY-afford.md
apply-afford.py
```

**Existing files edited (all of it inside `apply-afford.py`):**

| File | Edit |
|---|---|
| `tools/validate.py` | `AFFORD_COL` / `AFFORD_MEDIGAP` tables, `afford_central()`, `check_afford_data()`, registered in the `figures` group, page added to four target lists, harness added to `HARNESSES` |
| `tools/test_hardcoded_counts.py` | its own anchor into `validate.py` drifted when the page joined the `standalone` list; anchor updated and all three of its replacements now assert rather than no-op |
| `sitemap.xml` | one `<url>` entry, `lastmod` 2026-08-10 |
| `index.html` | header nav and mobile nav link |
| `where-should-i-retire-quiz.html` | header nav, mobile nav, and a hero cross-link |
| `best-places-to-retire-on-a-budget.html` | cross-link under the quiz CTA |
| `docs/BUDGET-METHODOLOGY.md` | section 5 gains an explicit order-of-operations clause for the utilities line |
| `docs/TASKBOARD.md` | session entry, counts unchanged |
| `docs/SITE-OPERATIONS-LOG.md` | change-log entry |

No image assets. Nothing to drag.

## 2. Deploy sequence

```bash
git pull
unzip -o afford-bundle.zip && rm afford-bundle.zip
python3 apply-afford.py                      # must print "patched"
timeout 1200 python3 tools/validate.py --local .   # the gate. 0 failures, 0 warnings, or stop.
rm apply-afford.py                           # AFTER "patched", BEFORE git add
git status --short --untracked-files=all     # expect 3 new files, 9 modified
git add -A && git commit -m "where-can-i-afford-to-retire.html: equity-adjusted affordability tool; check_afford_data + harness; internal links; board + log"
git push
python3 tools/validate.py                    # post-deploy, reads live GitHub
```

`apply-afford.py` is idempotent and anchor-verified. A second run prints `no-op` on
every edit and exits clean. If any anchor has moved it writes nothing at all and
says which one.

## 3. What the page does

Three inputs: cash down, monthly budget, buying or renting.

For each city it computes, at run time, `base + P&I(max(0, Median Home - cash))`,
where `base` is the section 3 central estimate with principal and interest removed.
Property tax and homeowners insurance stay in `base` at full value on `Median Home`,
because they attach to the house and not to the loan. Cities at or under the budget
are shown; the survivors are ordered by their combined score across nine dimensions,
D1 and D3 through D10. **D2 Budget is excluded from the ranking on purpose.** Cost is
already the filter, so counting it again in the ordering lets price decide twice, and
it misleads exactly the reader this page serves: someone with a large cash-down figure
would be pushed toward cheap-housing cities on account of a mortgage they are not
paying. `RANK_SKIP` names the excluded index rather than burying it in a loop bound.
Scores render out of 90.

**Cost filters. It never sorts.** Section 14.2. Removing principal and interest
strips out most of the cost variance between cities, so a cost ranking at high cash
down inverts. The rule is stated in the page prose and again in the script comment
directly above the sort, so a future edit has to argue with it rather than not
notice it.

Renting uses the published mortgaged figure and ignores the cash input, per section
14.3: a landlord does not lower rent because the reader sold a house. The equity
slider disables itself and the page says why in three places.

City handoff is `index.html?city=NAME&state=ST`, which the existing load handler in
`index.html` picks up and passes to `showCityDetail`, exactly as the landing pages do.
All 99 database cities resolve against the `CITIES` array; verified, not assumed.

## 4. Verification performed before hand-off

- The page's own JavaScript was extracted and run in Node against
  `docs/CityDatabase_Jul_27_v17.xlsx`: it reproduces the published `Monthly Est`
  string and `Budget Range` integer for **all 99 cities, zero mismatches**.
- 420 combinations of cash down and budget swept in a headless DOM. No exceptions,
  no empty renders, no city silently dropping out through a missing state multiplier.
- Every handoff link parsed and checked against the `CITIES` array in `index.html`.
- Both JSON-LD blocks parse; all six FAQ answers appear verbatim in visible copy.
- `tools/test_afford_data.py`: 9 planted errors, 9 caught.
- Full gate on a fresh clone with the patch applied: **0 failures, 0 warnings**,
  14 harnesses green.

## 5. One thing left open

**Renting has no basis of its own.** Section 14.3 says a rent view needs one and this
is not it. There is no rent column in the database, and inventing one from web research
would break the data-source rule, so renting reuses the published mortgaged figure with
the caveat stated plainly in the helper text, the limits section, and the FAQ. A real
rent basis needs its own data source and is a separate job.

## 6. The BUDGET-METHODOLOGY.md fix, included in this commit

Section 5 says the utilities baseline is "multiplied by a state cost-of-living
modifier" and then lists climate adjustments, without saying which happens first.
Applying the modifier to `(400 + adjustment)` disagrees with the published
`Monthly Est` on six cities: Palm Springs, Fort Collins, St. Louis, Knoxville,
Bentonville, and Tulsa. `400 x COL + adjustment` reproduces all 99 exactly.

The latter is correct and is now asserted by `check_afford_data`. `apply-afford.py`
adds the clause to section 5 in this same commit, so the ambiguity does not have to be
rediscovered from the data a second time.

## 7. A note on the second copy of the database

The page embeds `Median Home`, `PropTax Rate %`, `HO Insur Est $/yr`,
`Climate Warm W`, `HEAT (0-10)` and all ten scores for every city. It has to: a
personalised figure cannot be precomputed, and section 14.4 requires run-time
derivation from current data.

A second copy of the database is exactly the drift the validator exists to catch, so
`check_afford_data` asserts four things in order: roster membership, every cell, the
page's constants against section 6, and finally that the page's own inputs rebuild the
published `Monthly Est` and `Budget Range` through the formula. That last one is the
`Monthly Est == f(Median Home)` gate section 9 has been asking for. It now runs on
every deploy, over the whole database, not just this page.

**When the database is rebuilt,** regenerate the `AFFORD_CITIES` array from the new
xlsx and nothing else on this page changes. If you forget, the gate fails and names
the city and the column.
