# DEPLOY: report offer removal (October 23, 2026)

TASKBOARD P1. Removes the paid relocation report from the quiz results screen.

## Before you run it

Get the final all-time `offer_click` count from GA4 (Reports, Engagement, Events,
date range September 17 to today). The script will not run without it.

## Deploy

```bash
git pull
unzip -o report-offer-removal-bundle.zip
rm report-offer-removal-bundle.zip
python3 apply-report-offer-removal.py --offer-clicks N    # N = the GA4 count
python3 tools/validate.py --local .                        # 0 failures, 0 warnings
rm apply-report-offer-removal.py
git status          # expect: index.html, sitemap.xml, docs/TASKBOARD.md,
                    # docs/SITE-OPERATIONS-LOG.md modified; this file new
git add -A && git commit -m "Remove relocation report offer; board + log; sitemap dates"
git push
```

Run it on the same day you commit. It stamps today's date on the home page's
sitemap `lastmod`; if the commit slips a day, the gate will say so and
`python3 tools/build_sitemap.py` fixes it.

## What changes

- `index.html`: offer block and CSS, `CITY_COST`, `offerClick()`, the "Launching
  in October" modal, the `ETbvqw` form node, one stale comment. About 320 lines out.
- `sitemap.xml`: home page `lastmod` to today; quiz page `lastmod` to 2026-10-12
  (stale since the October 12 title edit, already failing the gate on main).
- `docs/TASKBOARD.md`: new top entry with the closing count; P1 marked done.
- `docs/SITE-OPERATIONS-LOG.md`: change-log entry.

Kept: Deep Dive guides capture (`g4M1M8`), both `breakdown_click` events,
`signup_submit`.

## After deploy, outside the repo

- MailerLite: unpublish form `ETbvqw`; tag or archive its subscribers.
- Live check: take the quiz on your phone. Three cards, then "More cities that
  fit", no price buttons.
