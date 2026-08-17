# NEXT SESSION BRIEF
**Written:** August 17, 2026
**Suggested repo location:** `docs/BRIEF-2026-08-17-next-session.md`
**Session type:** BATCH (maintenance fixes only, no city builds, no comparison builds)

---

## Read first

1. This brief.
2. `docs/TASKBOARD.md` top section, entries dated Aug 17, 2026.
3. `docs/SITE-OPERATIONS-LOG.md` section 7, entry `2026-08-17`.

Pull everything live from the repo. Do not read a cached or project-knowledge
copy of any file that exists in the repo. Re-derive baselines from live main
before building anything.

---

## Where the site stands

51 profiles, 23 comparison pages. Two pushes landed Aug 16 and Aug 17
(link-form conversion, curated matchup pills). Board and ops log are current
as of the Aug 17 catch-up commit.

Search Console, 3 months to Aug 17: **8,974 impressions, 403 clicks.** The quiz
page alone earns 257 of those clicks at position 4.8. Most comparison pages sit
at position 7 to 21.

**Strategy in force:** growth means comparison pages, tools and pins. Wave 2 and
Wave 3 profile builds are SUSPENDED. Build a profile only when demand names it.
The Aug 3 growth cycle otherwise stands, including the one-debt-day-per-week cap.

---

## The queue, in the order I would work it

### 1. P1 slug resolution (highest value, and a prerequisite)

`check_comparison_scores` and `check_comparison_cost_rows` build their city
lookup as `name.lower().replace(" ","-").replace(".","")` with no state suffix.

Two defects:
- **Silent skip.** `portland-me` never resolves, so `burlington-vs-portland-me`
  has never actually been checked by either function. Exactly one page, measured
  Aug 8.
- **Wrong-city validation.** Wilmington DE and Wilmington NC both key to
  `wilmington`; the dict keeps whichever built last. A future Wilmington page
  would validate against the wrong city's figures and PASS.

Fix: key on `(City, ST)` tuples, matching the pattern already used elsewhere.

**Expect the gate to fail the moment this lands.** Burlington's two
`Estimated retiree budget` cells carry `&ndash;`, and `_dashes()` normalises only
literal en dash, em dash and hyphen. Two cost-row failures, same commit. Fix them
together.

**Planted-error harness required before this ships.** No check goes out that can
silently return zero matches. This is the defect that rule exists for.

### 2. Duplicate URL redirect

Netlify serves every page at two addresses, with and without `.html`, and there
is no redirect between them. Google has indexed both forms for three pages:

| Page | `.html` | extensionless |
|---|---|---|
| naples-vs-sarasota-retirement | pos 21.0, 154 imp | pos 7.4, 8 imp, 2 clicks |
| pensacola-vs-fort-myers-retirement | pos 6.1, 26 imp | pos 6.2, 20 imp |
| visit-before-you-decide | pos 4.6, 5 imp | pos 3.2, 4 imp |

Canonical tags, og:url and sitemap all already use `.html`, and every internal
link in the repo already uses `.html`. So the `.html` form wins; the redirect
should point extensionless traffic at it.

Add to `netlify.toml`. Watch the root case: a blanket rule can catch `index.html`
and break the homepage, which would take down the quiz, the site's single most
valuable page. Test that case explicitly before pushing.

### 3. urban-walkabout vocabulary (low priority, do it opportunistically)

947 impressions, 1 click, position 8.4. It matches Walk Score's stock phrasing
("citywide", "car dependent", "average walk score", 11 occurrences) and pulls
people who want walkscore.com. Meanwhile "walkable cities for retirees" sits at
position 37.

Title and meta description are already correct. Do not change them. Reduce the
stock Walk Score vocabulary in the body and reframe around retirement language:
walkable downtowns, groceries and a doctor without driving, giving up a car.

Zero clicks means this costs nothing today. Fix it when next in the file. Do not
make a project of it.

### 4. D2 figure drift in index.html

D2 monthly budget figures live inside prose strings, not structured fields, so
they drift silently. `$4,500-$5,500` appeared 4 times as of July 9; at least
three cities carry a suspect range. Verify `index.html` D2 monthly against the
DB `Monthly Est` column.

### 5. St. Paul DB update

DB still stores the St. Paul median as a range string. Needs a single figure of
`$297,000` plus a `Monthly Est` recompute per `BUDGET-METHODOLOGY.md`.

### 6. Parked

- Item 6 bolding pass (judgment-based, not batchable).
- Scottsdale sports card: Coyotes moved to Utah; pill recount "5+ teams" to
  "4 teams".
- `affiliate-policy.html` was never written. Decide whether a standalone page is
  wanted; the disclosure prose already carries the substance.
- Taskboard is ~40% closed-work archive and should be split to
  `docs/TASKBOARD-ARCHIVE.md`. See the P2 entry for why it is safe.

---

## Two vocabulary findings worth acting on separately

**"Retirees" vs "retirement."** Zero of 23 comparison page titles contain
"retirees", but the two largest comparison queries both use it: "tampa vs
sarasota for retirees" (78 impressions) and "tampa vs naples for retirees" (44).
Work "for retirees" into descriptions and subheadings.

**Question-shaped city queries work.** "is bentonville arkansas a good place to
retire" ranks at position 9; the Bentonville profile draws 225 impressions at
position 8.5. The losing shape is "best places to retire in Florida", where the
pillar page sits at position 51 with 329 impressions and zero clicks. City
profiles are not dead. The framing is what matters.

**One genuine content gap:** "tampa vs naples for retirees", 44 impressions,
position 35, no page exists. The only true missing-page finding in the export.

---

## Rules that bit during this session

- **Pull from the repo, never from a rendering.** A URL-form defect was
  diagnosed from a markdown conversion of a live page, which strips `.html` from
  hrefs. The repo was always correct. Three turns of work were built on the
  artifact before the clone disproved it.
- **Board and ops log go in the same commit as the work.** The matchup pill push
  shipped without either and needed a retroactive catch-up.
- **A plan that lives in a chat is a plan that dies with the chat.** The Aug 15
  strategy change went unboarded for two days and misled a later session.

---

## Measurement

Grade on **pages indexed, impressions and average position.** Not clicks.
There is a six to twelve week lag between publishing and clicks. Do not read
anything into the Aug 16 and Aug 17 pushes before October.

Baseline to compare against, 3 months to Aug 17, 2026:
- 8,974 impressions, 403 clicks, site-wide
- Quiz page: 1,521 impressions, 257 clicks, position 4.8
- Comparison pages: 2,194 impressions, 36 clicks
- Daily impressions running 100 to 155
