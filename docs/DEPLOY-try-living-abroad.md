# DEPLOY: Try Living Abroad page (October 23, 2026)

## Deploy (Codespaces terminal)

```bash
git pull
ls *.zip                                  # after dragging the zip to the top level
unzip -o try-living-abroad-bundle.zip
rm try-living-abroad-bundle.zip
python3 apply-try-living-abroad.py        # expect 13 "applied", 2 "already in"
python3 tools/validate.py --local .       # 0 failures, 0 warnings
rm apply-try-living-abroad.py
git status        # expect 7 modified, 2 new (the page and this file)
git add -A && git commit -m "Try Living Abroad page; links from results, footers, quiz FAQ"
git push
```

On a later day than October 23, expect 15 "applied" (two sitemap dates are
included then).

## What changes

- New `try-living-abroad.html`.
- `index.html`: one line under the quiz results, and a footer link.
- `where-should-i-retire-quiz.html`: the international FAQ answer links the page;
  footer link.
- `sitemap.xml`, `docs/GA4-EVENT-REFERENCE.md` (`abroad_click`),
  `docs/try-living-abroad-guide.md` (marked superseded), `docs/TASKBOARD.md`,
  `docs/SITE-OPERATIONS-LOG.md`.

## Live check

retiremehere.com/try-living-abroad.html on your phone. Then take the quiz: under
the "More cities that fit" list, "Thinking about retiring abroad? Try living
there first" opens the page.
