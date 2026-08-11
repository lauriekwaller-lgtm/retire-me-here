# DEPLOY: State Tax Facts population pass (DB v18 to v19)

**Bundle:** `taxfacts-pop-bundle.zip`
**New files (land at final paths on unzip):** `docs/CityDatabase_Jul_27_v19.xlsx`,
`docs/DEPLOY-taxfacts-pop.md`, `apply-taxfacts-pop.py`
**Existing files edited by the apply script:** `tools/validate.py`,
`tools/test_taxfacts.py`, `docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.
It also deletes the superseded `docs/CityDatabase_Jul_27_v18.xlsx`.

No page changes. No score change. No city figure change. Version stamp stays
Jul 27; only the facts sheet content changed.

## Sequence

```bash
git pull
unzip -o taxfacts-pop-bundle.zip && rm taxfacts-pop-bundle.zip
python3 apply-taxfacts-pop.py            # must print "patched"
timeout 1200 python3 tools/validate.py --local .   # the gate. 0/0 or stop.
rm apply-taxfacts-pop.py                 # BEFORE git add
git status --short --untracked-files=all # expect exactly 7 lines, listed below
git add -A && git commit -m "State Tax Facts populated, 39 states, TY2026 (DB v19); completeness checks; board + log"
git push
python3 tools/validate.py                # post-deploy live verification
```

Expected `git status` lines (7):

```
 M docs/SITE-OPERATIONS-LOG.md
 M docs/TASKBOARD.md
 M tools/validate.py
 M tools/test_taxfacts.py
 D docs/CityDatabase_Jul_27_v18.xlsx
?? docs/CityDatabase_Jul_27_v19.xlsx
?? docs/DEPLOY-taxfacts-pop.md
```

## What ships

Every column of every one of the thirty-nine state rows: income tax type and
top rate (Tax Foundation 2026; South Carolina per Act 110, 1.99 and 5.21
percent), Social Security treatment (six of ours are Partial or Taxed: CO, MN,
MT, NM, UT, VT), retirement income treatment with the mechanism in the Note
column, combined sales tax (Tax Foundation midyear 2026), the PropTax mirror
unchanged, estate tax (MA, MD, ME, MN, NY, OR, VT, WA) and inheritance tax
(KY, MD, PA), Tax Year 2026, and a source string on every row.

`check_taxfacts` now enforces completeness: blank enums, numerics, Notes, or
Sources fail, and Tax Year is bounded to 2025 through the current year. The
harness grows to nine planted errors.

## D5 reconciliation outcome

No score moved. Seven of eight raw flags dissolve on the rubric's own offset
language. The one live tension, boarded for the operator: Pennsylvania at six
and seven against facts reading retirement income fully exempt.
