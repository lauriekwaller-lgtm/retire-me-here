# Deploy — Casper, WY profile (July 2026)

Profile 47. Built from the live `cities/st-louis/profile.html` canonical against
`docs/CityDatabase_Jul_27_v17.xlsx` row 85.

## ONE OPEN ITEM: confirm the Hogadon photographer

The lifestyle credit and the footer both name **Milonica** as the author of the
Hogadon Basin ski-run photo. That attribution is inferred, not confirmed: the
Wikipedia Hogadon article's photo is credited to Milonica on third-party mirrors,
and the file dimensions (3072x2304) match a known Hogadon upload from the same
camera. CC BY-SA requires correct attribution, so open the Commons or Wikipedia
file page you downloaded it from and confirm the username before pushing. Two
places to edit if it is wrong: the `lifestyle-banner-credit` div and the footer
Photos line.

Note also that CC BY-SA 3.0 is a share-alike licence. The cropped derivative must
be offered under the same licence, which the footer line now states. The repo has
precedent for this (Yahala / Wikimedia, CC BY-SA 3.0, cropped).

## Bundle contents (final paths, unzip at repo root)

```
cities/casper/profile.html
cities/casper/hero.jpg          1600x899   North Platte at Bessemer Bend
cities/casper/detail.jpg        1600x2133  former Wyoming National Bank dome (1968)
cities/casper/lifestyle.jpg     1280x1280  Hogadon Basin ski run
docs/DEPLOY-casper.md
apply-casper.py
```

## Photo provenance

1. **hero** — Tony Webster via Wikimedia Commons, CC BY 2.0, cropped and resized.
   Location verified from the file's embedded EXIF description, not the filename.
   Bessemer Bend is the last Oregon Trail ford of the North Platte, which is why
   the opening character paragraph and the Sunday day-card both land on it.
2. **detail** — Dclemens1971 via Wikimedia Commons, CC BY 4.0, cropped and
   resized. The former Wyoming National Bank dome, 1968, Casper architect Harold
   Engstrom. Native portrait crop is 2107x2809 against a 1600x2133 spec, so this
   is a clean downscale with no upscaling. Framed to exclude the Wells Fargo
   signage: the sign sits at x 3250-3745 in the source and the crop ends at 3207,
   which leaves 26 red pixels in frame against 4,523 in the full picture. The
   trade is that the 177-foot tower is excluded too, since it stands within about
   45px of the sign and no crop can hold one without the other.
3. **lifestyle** — Milonica via Wikimedia Commons, CC BY-SA 3.0, cropped and
   resized. Attribution pending confirmation, see above.

**Rejected, three:**
- an Unsplash red-rock river image, no EXIF and no findable link to Casper
- `Casperskyline.jpg`, a good frame but only 800x1200, a 2x upscale for this slot
- the Highsmith photograph of Avard Fairbanks's Pony Express statue. Highsmith's
  photograph is public domain, but the sculpture is not. It was designed mid-century
  and never cast; Skylight Studios built it from the design with Fairbanks's sons
  and it was dedicated at the centre in 2001. A c.2001 bronze is well inside
  copyright, the US has no freedom of panorama for sculpture (only architecture,
  17 USC 120(a)), and a photograph of it is a derivative work. Wrong risk to carry
  on a page with affiliate links. The bank photo has no such problem: it is a
  building.

## What `apply-casper.py` edits

Existing files only, idempotent, aborts if any anchor has moved:

1. `index.html` — `PUBLISHED_PROFILES` += `'Casper_WY'`
2. `sitemap.xml` — url block for `cities/casper/profile.html`
3. `best-places-to-retire-on-a-budget.html` — the Casper coming-soon div at rank
   2 becomes a live `city-card` link. Required: `check_cards` fails on a stale
   coming-soon card once the city is in `PUBLISHED_PROFILES`.
4. `docs/TASKBOARD.md` — new Last-updated entry, profile counts 46 to 47, ACTIVE
   builds section, two boarded items
5. `docs/SITE-OPERATIONS-LOG.md` — change-log entry

## Deploy

```bash
git pull
unzip -o casper-bundle.zip
rm casper-bundle.zip
python3 apply-casper.py
python3 tools/validate.py --local .
rm apply-casper.py
git status
git add -A && git commit -m "Casper WY profile (47); budget card live; taskboard + ops log"
git push
```

## Editorial spine

One pillar, D5 Tax at 10, plus a cluster of three 8s (D2 Budget, D7 Outdoor,
D9 Safety). That is the MULTI-STRENGTH shape, so the tax fact leads the hero and
the cluster carries the character section rather than the page riding one hook.
Both sub-5 dimensions are named in the No-if column, D1 Airport 4 first because a
single nonstop route to Denver is the binding constraint on the whole city, then
D6 Walk 3.

No Neighborhood Reality Check. Paradise Valley, the retiree-favoured side of town,
prices at roughly $316K against a $314K citywide figure, so neighbourhood choice
does not move the budget here and a callout would add noise under
`MEDIAN-HOME-METHODOLOGY.md` v1.2 section 4. The unused NRC CSS was stripped from
the clone so the profile does not register in the roster grep.

## After deploy

- Request indexing: https://retiremehere.com/cities/casper/profile.html
- Post-deploy bare validator run (no `--local`) against live main
