# tools/

## validate.py

Checks every live page against the City Database and reports drift.

```bash
python3 tools/validate.py              # check the live site
python3 tools/validate.py --local .    # check your working copy BEFORE you push
python3 tools/validate.py --only figures
python3 tools/validate.py --only superlatives
```

**No setup. No installs. No dependencies.** The validator uses only the Python standard
library, including reading the `.xlsx`. Codespaces rebuilds and wipes pip packages; a

validator that cannot run is a validator that is not run.

Exit code 0 = clean, 1 = failures.

It reads the database straight from `docs/`. Nothing else to set up.

### When you bump the database version

Open `validate.py` and update one line near the top:

```python
DEFAULT_DB = "docs/CityDatabase_Jul_06_v16_1_stpaul-corrected.xlsx"
```

Do it in the same commit that adds the new xlsx. If you forget, the script will tell
you it cannot find the file rather than silently checking against stale data.

### Check groups

| Group | What it catches |
|---|---|
| `figures` | `CITIES` array and `CITY_ENRICHMENT` modal prose in `index.html` vs the DB. Scores, monthly, home value, budget tier. Also every home figure written into `highlight` PROSE, on both `index.html` and `pick-and-compare.html`. This is where the quiz gets its numbers. |
| `profiles` | Profile pages: monthly ranges and citywide home-value claims. |
| `routing` | `PUBLISHED_PROFILES` ↔ profile files ↔ `sitemap.xml`, all directions. |
| `cards` | Landing pages: cards still saying "Coming soon" for a live city, stale card figures. |
| `superlatives` | **FAILS** on any superlative scoped to our own dataset (policy, below). **WARNS** on other sweeping claims, printed next to the DB's real answer. |
| `emdash` | Em-dash policy on profiles and comparison pages. |
| `affiliate` | Affiliate codes on every profile: a code reused by two cities, a missing brand, or two codes for one brand on one page. |
| `db` | Database hygiene: column types, duplicate rows. |

Superlatives are **warnings, not failures**. Scope is an editorial judgment a script
cannot make, so it puts the claim and the truth side by side and you decide. Read them
all. This is the check that catches a "most affordable X we cover" that is not true.

### A note on Wilmington

Wilmington NC and Wilmington DE are both in the database. Anything keyed by city name
alone will silently drop one of them. The validator keys by `City_ST` and refuses a
name-only lookup when the name is ambiguous. `CITY_ENRICHMENT` in `index.html` handles
this the same way, with `_NC` and `_DE` suffixed keys. Keep that convention.

### Home figures in `highlight` prose

`medianHome` is a field, so it was checked. The same number written into the `highlight`
sentence four lines below it was prose, so it was not. Nine cities had drifted, and the
validator read 0 failures the whole time.

The rule is exact, with no tolerance band: a figure written in thousands must equal
`round(DB Median Home / 1000)`. `$224K` against a `$224,000` cell passes and `$223K` does
not. A band is how the nine hid, because 3% forgives `$275K` against `$273K` and does not
forgive `$217K` against `$191K`, and both are equally false.

Scope is anchored, not blanket. A dollar figure is only in scope when it is attached to a
home-value noun. Three things in these strings are supposed to disagree with `medianHome`,
and a blanket "every figure must match" check red-lights all of them forever:

| Shape | Example | Why it is not drift |
|---|---|---|
| The NRC range | "Citywide median home $195K but retirees target Germantown ($280K–$500K)" | The range is the point of the sentence |
| A cross-city reference | Tampa's "Naples matches it at $585K" | Correct, and not our figure |
| A figure that is not a home | Tulsa's "$465M Gathering Place" | Not a home value at all |

Bounds are checked as bounds. "Homes under $260K" is not a claim that the median IS $260K,
so it is not held to equality, but it is still a factual claim, and Roanoke shipped "median
homes under $230K" against a DB `$251,000`. The check fails when the inequality is false.

## test_highlight_homes.py

```bash
python3 tools/test_highlight_homes.py
```

The planted-error test for the check above. Fifteen assertions: the real Wilmington DE
`$215K` bug on both surfaces, the two-Wilmingtons key guard, six legitimate shapes that must
stay silent, three wrong figures that must not, and a renamed `CITIES` array that must fail
loudly rather than scan nothing and report a clean site.

Run it after any edit to the `HL_*` patterns. A check that has never been watched fail is
not a check.


## Run this before every deploy

Every error this script finds is a string that either matches a spreadsheet cell or
does not. It should never again be a person's job to notice.

## What the validator cannot check

The `superlatives` group flags every sweeping claim it finds, but it can only resolve
the ones that are **claims about the database** (cheapest, priciest, most affordable).
Claims about the outside world — "largest art market in the country", "largest farmers
market in the Southeast", "largest in the Western Hemisphere" — get surfaced for you to
verify, because no spreadsheet can settle them. Read those with a skeptical eye. They
are exactly the sort of thing that gets written once, confidently, and never rechecked.

Vague superlatives ("highest of any city in the database") are flagged without the
subject, because the script cannot tell what "highest" refers to. Open the page.


## The superlative policy (adopted July 12, 2026)

**No superlative may be scoped to our own dataset.** These phrasings are banned when
attached to a ranking word:

> "in the database" · "in our database" · "we cover" · "in our coverage" ·
> "we've published" · "of any city we…" · "on this site"

**Why.** A claim like "the most affordable city we cover" is a claim about a private,
moving object the reader cannot see. The day a city is added to the database, every
such claim silently becomes a potential lie, and nothing tells you. Fort Myers and
Pensacola both went wrong exactly this way, and reconciling them by hand across every
profile on every database expansion is not sustainable.

**Anchor to a number or a named comparison. Never to a rank.**

| Instead of | Write |
|---|---|
| "the most affordable Gulf Coast entry we cover" | "at $372K, well below Sarasota ($462K) and Naples ($585K)" |
| "the most affordable Florida city in our coverage" | "$264K, among the lowest on the Florida Gulf Coast" |
| "highest healthcare score in our database" | "Healthcare 9 of 10" |
| "the only city we've published with…" | just describe the thing |

Numbers stay true when the database grows. Ranks do not.

The validator enforces this as a hard failure, because unlike scope-correctness it is
mechanically decidable. It cannot tell whether "most affordable Gulf city" is true. It
can absolutely tell that you wrote "we cover".


## There is no affiliate-code spreadsheet, on purpose

The profiles are the record. 84 codes, 42 cities, Expedia and Vrbo each.

A separate spreadsheet of codes is a stale copy of data that already lives in the HTML.
The one that existed covered about 30 cities and was never kept up, which makes it worse
than nothing: eventually somebody trusts it. It was deleted.

To read the current codes, read them from the source:

```bash
grep -rhoE 'https?://(www\.)?(expedia|vrbo)\.com/affiliate/[A-Za-z0-9]+' cities/
```

The `affiliate` check exists because a bad code is the one error that costs money while
looking completely fine. A duplicated code does not throw, does not render wrong, and
does not break a link. It just sends a Savannah reader to Charleston's hotel page. No
human catches that by reading the page.
