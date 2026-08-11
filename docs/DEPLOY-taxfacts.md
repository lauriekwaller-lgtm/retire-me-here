# DEPLOY: State Tax Facts schema (DB v17 to v18)

**Bundle:** `taxfacts-bundle.zip`
**New files (land at final paths on unzip):** `docs/CityDatabase_Jul_27_v18.xlsx`,
`tools/test_taxfacts.py`, `docs/DEPLOY-taxfacts.md`, `apply-taxfacts.py`
**Existing files edited by the apply script:** `tools/validate.py`, `docs/TASKBOARD.md`,
`docs/SITE-OPERATIONS-LOG.md`. It also deletes the superseded
`docs/CityDatabase_Jul_27_v17.xlsx`.

No page changes. No score change. No city figure change. The version stamp stays
Jul 27 because the date records the vintage of the city figures and none moved;
the version number is the canonical part (ops log, section 5).

## Sequence

```bash
git pull
unzip -o taxfacts-bundle.zip && rm taxfacts-bundle.zip
python3 apply-taxfacts.py                # must print "patched"
timeout 1200 python3 tools/validate.py --local .   # the gate. 0/0 or stop.
rm apply-taxfacts.py                     # BEFORE git add
git status --short --untracked-files=all # expect exactly 7 lines, listed below
git add -A && git commit -m "State Tax Facts schema (DB v18); check_taxfacts + harness; board + log"
git push
python3 tools/validate.py                # post-deploy live verification
```

Expected `git status` lines (7):

```
 M docs/SITE-OPERATIONS-LOG.md
 M docs/TASKBOARD.md
 M tools/validate.py
 D docs/CityDatabase_Jul_27_v17.xlsx
?? docs/CityDatabase_Jul_27_v18.xlsx
?? docs/DEPLOY-taxfacts.md
?? tools/test_taxfacts.py
```

## What ships

The State Tax Facts sheet in the database: one row per live state (thirty-nine),
keyed on ST, twelve columns. Populated now: the ST keys and the PropTax Rate %
mirror, copied from the City Database sheet. Everything else is blank until the
population pass, which is its own session.

`check_taxfacts` joins the `db` group and holds three promises: two-way coverage
(every state with a city has a facts row, no facts row without a city), closed
enum vocabularies (blank tolerated only until population), and the PropTax mirror
(fails the moment the two copies disagree). `tools/test_taxfacts.py` plants seven
errors and requires the gate to catch each.

## What this deliberately does not do

No tax facts are populated beyond the mirror. No completeness check yet; the
population commit adds it and retires the blank tolerance. No edit to
`D5-TAX-METHODOLOGY.md`; it goes to v1.1 with the population pass, when "score a
new state" becomes "fill its facts row". No front-loading of states without
cities: the coverage check refuses speculative rows by design.
