# tools/

## validate.py

Checks every live page against the City Database and reports drift.

```bash
# check the live site
python3 tools/validate.py

# check your working copy BEFORE you push
python3 tools/validate.py --local .

# one group at a time
python3 tools/validate.py --only figures
python3 tools/validate.py --only superlatives
```

Requires `pandas`. Exit code is 0 when clean, 1 when failures exist.

### Check groups

| Group | What it catches |
|---|---|
| `figures` | `CITIES` array and `CITY_ENRICHMENT` modal prose in `index.html` vs the DB. Scores, monthly, home value, budget tier. |
| `profiles` | Profile pages: monthly ranges and citywide home-value claims vs the DB. |
| `routing` | `PUBLISHED_PROFILES` ↔ profile files ↔ `sitemap.xml`, checked in every direction. |
| `cards` | Landing pages: cards still saying "Coming soon" for a live city, and stale card figures. |
| `superlatives` | Every database-wide affordability claim on the site, printed next to the DB's real answer. This is the check that catches a "most affordable X we cover" that is not true. |
| `emdash` | Em-dash policy on profiles and comparison pages. |
| `db` | Database hygiene: column type consistency, duplicate rows. |

Superlatives are reported as **warnings, not failures**, because scope is an editorial
judgment a machine cannot make. The script's job is to put the claim and the truth
side by side so a human decides. Read every one.

## data/city-database.csv

A CSV export of the current `CityDatabase_*.xlsx`. The validator reads this.

**Regenerate it whenever you bump the database version**, in the same commit:

```python
import pandas as pd
df = pd.read_excel("CityDatabase_<Month>_<Day>_v<N>.xlsx",
                   sheet_name="City Database", header=1)
df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]
df.to_csv("data/city-database.csv", index=False)
```

Keeping it in git means the database finally has version history. The v15.1 → v16.1
transition happened with nothing recording it, which is how St. Paul ended up correct
in four places and wrong in a fifth.

## Run this before every deploy

That is the whole point. Every error this script finds is a string that either matches
a spreadsheet cell or does not. It should never again be a person's job to notice.
