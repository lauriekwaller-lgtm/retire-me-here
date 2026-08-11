# DEPLOY: Pennsylvania D5 unified at 7 + methodology v1.1 (DB v19 to v19.1)

**Operator-approved scoring change, Aug 11 2026.**
**Bundle:** `pa-d5-bundle.zip`
**New files (land at final paths on unzip):** `docs/CityDatabase_Jul_27_v19.1.xlsx`,
`docs/DEPLOY-pa-d5.md`, `apply-pa-d5.py`
**Existing files edited by the apply script:** `index.html`, `pick-and-compare.html`,
`where-can-i-afford-to-retire.html`, `docs/D5-TAX-METHODOLOGY.md`,
`tools/validate.py`, `docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.
It also deletes the superseded `docs/CityDatabase_Jul_27_v19.xlsx`.

One score changes: Philadelphia D5, 6 to 7. The v19.1 workbook differs from v19
by exactly one cell (verified byte-level). No other figure, page, or profile moves.

## Sequence

```bash
git pull
unzip -o pa-d5-bundle.zip && rm pa-d5-bundle.zip
python3 apply-pa-d5.py                   # must print "patched"
timeout 1200 python3 tools/validate.py --local .   # the gate. 0/0 or stop.
rm apply-pa-d5.py                        # BEFORE git add
git status --short --untracked-files=all # expect exactly 10 lines, listed below
git add -A && git commit -m "Philadelphia D5 6->7, PA unified (DB v19.1); D5-TAX-METHODOLOGY v1.1; board + log"
git push
python3 tools/validate.py                # post-deploy live verification
```

Expected `git status` lines (10):

```
 M docs/D5-TAX-METHODOLOGY.md
 M docs/SITE-OPERATIONS-LOG.md
 M docs/TASKBOARD.md
 M index.html
 M pick-and-compare.html
 M tools/validate.py
 M where-can-i-afford-to-retire.html
 D docs/CityDatabase_Jul_27_v19.xlsx
?? docs/CityDatabase_Jul_27_v19.1.xlsx
?? docs/DEPLOY-pa-d5.md
```

## What ships

Philadelphia D5 moves 6 to 7 on every surface that carries it: the City Database
cell, the quiz CITIES array in index.html, the embedded array in
pick-and-compare.html, and the score array in where-can-i-afford-to-retire.html.
The Philadelphia profile carries no numeric D5 and needed nothing; no comparison
page includes Philadelphia. Rationale: rubric 5-6 requires some retirement income
taxed and Pennsylvania taxes none; Iowa (8) minus the inheritance tax lands 7.
Full write-up in D5-TAX-METHODOLOGY.md section 8.

D5-TAX-METHODOLOGY.md ships as v1.1: scoring a new state is now "fill the State
Tax Facts row, then assign D5 from the row against the bands."

Boarded, not fixed: the Scores by Dimension sheet is a stale second copy (89 rows
against 99 cities, drifted values, no reader). P2, delete-or-validate.
