# DEPLOY: the state tax filter tool

**Bundle:** `taxtool-bundle.zip`
**New files (land at final paths on unzip):** `states-that-dont-tax-retirement-income.html`,
`tools/test_taxtool.py`, `docs/DEPLOY-taxtool.md`, `apply-taxtool.py`
**Existing files edited by the apply script:** `tools/validate.py`, `sitemap.xml`,
`where-can-i-afford-to-retire.html` (one cross-link), `docs/TASKBOARD.md`,
`docs/SITE-OPERATIONS-LOG.md`.

No DB change. No score change. No city figure change. One new page.

## Sequence

```bash
git pull
unzip -o taxtool-bundle.zip && rm taxtool-bundle.zip
python3 apply-taxtool.py                 # must print "patched"
timeout 1500 python3 tools/validate.py --local .   # the gate. 0/0 or stop.
rm apply-taxtool.py                      # BEFORE git add
git status --short --untracked-files=all # expect exactly 8 lines, listed below
git add -A && git commit -m "State tax filter tool; check_taxtool_data + harness; sitemap + cross-link; board + log"
git push
python3 tools/validate.py                # post-deploy live verification
```

Expected `git status` lines (8):

```
 M docs/SITE-OPERATIONS-LOG.md
 M docs/TASKBOARD.md
 M sitemap.xml
 M tools/validate.py
 M where-can-i-afford-to-retire.html
?? docs/DEPLOY-taxtool.md
?? states-that-dont-tax-retirement-income.html
?? tools/test_taxtool.py
```

## What ships

The page the whole tax thread was for: five checkbox filters and two sliders
over the State Tax Facts sheet, state cards with enum chips, the sheet's note
prose, and city chips carrying each city's D5 and linking through the standard
`index.html?city=` route. Checkboxes are strict (the box means the state does
not tax it for anyone); Partial states explain themselves in the note. All
counts computed from the arrays; the copy carries no figures that can rot; the
tax-year vintage renders from the data. Shell cloned from the calculator so
header, styles, footer, and GA match.

`check_taxtool_data` joins the figures group beside `check_afford_data`:
two-way rosters for both embedded arrays, every field and note equal to its
workbook cell (notes as exact strings), every city D5 equal to the City
Database, loud failure when nothing can be parsed. Eight planted errors in
`tools/test_taxtool.py`, wired into the harness group.

## After deploy

Netlify picks the page up on push. Worth a manual click-through on the live
URL: check a few boxes, drag the sliders, click a city chip through to a
profile. Pinterest content angle whenever wanted: the filter outcomes make
strong data pins ("Nine states will not touch your retirement withdrawals").
