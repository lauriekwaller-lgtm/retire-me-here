# tools/

## validate.py

Checks every live page against the City Database and reports drift.

```bash
python3 tools/validate.py              # check the live site
python3 tools/validate.py --local .    # check your working copy BEFORE you push
python3 tools/validate.py --only figures
python3 tools/validate.py --only superlatives
```

One-time setup: `python3 -m pip install pandas openpyxl`. Use `python3 -m pip`, not bare
`pip` — Codespaces has two Pythons and bare `pip` can install where `python3` cannot see it.

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
| `figures` | `CITIES` array and `CITY_ENRICHMENT` modal prose in `index.html` vs the DB. Scores, monthly, home value, budget tier. This is where the quiz gets its numbers. |
| `profiles` | Profile pages: monthly ranges and citywide home-value claims. |
| `routing` | `PUBLISHED_PROFILES` ↔ profile files ↔ `sitemap.xml`, all directions. |
| `cards` | Landing pages: cards still saying "Coming soon" for a live city, stale card figures. |
| `superlatives` | Every database-wide affordability claim, printed next to the DB's real answer. |
| `emdash` | Em-dash policy on profiles and comparison pages. |
| `db` | Database hygiene: column types, duplicate rows. |

Superlatives are **warnings, not failures**. Scope is an editorial judgment a script
cannot make, so it puts the claim and the truth side by side and you decide. Read them
all. This is the check that catches a "most affordable X we cover" that is not true.

### A note on Wilmington

Wilmington NC and Wilmington DE are both in the database. Anything keyed by city name
alone will silently drop one of them. The validator keys by `City_ST` and refuses a
name-only lookup when the name is ambiguous. `CITY_ENRICHMENT` in `index.html` handles
this the same way, with `_NC` and `_DE` suffixed keys. Keep that convention.

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
