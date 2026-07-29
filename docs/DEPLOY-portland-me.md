# DEPLOY: Portland, ME (profile 48)

**Built:** July 29, 2026
**Database:** `docs/CityDatabase_Jul_27_v17.xlsx` (sheet "City Database", `header=1`)
**Structural base:** live `cities/st-louis/profile.html`, taken via `cities/casper/profile.html`,
which is a byte-verified clone of the canonical minus the `.reality-check` block. Section and
comment-marker diffs between the two are exactly one item, the NRC. Portland is not an NRC city,
so starting from the already-stripped clone avoids re-deleting the callout and its CSS by hand.

---

## Files

**New (in the zip, at final paths):**

```
cities/portland-me/profile.html
cities/portland-me/hero.jpg          1600x899
cities/portland-me/detail.jpg        1600x2133
cities/portland-me/lifestyle.jpg     1280x1280
docs/DEPLOY-portland-me.md
apply-portland-me.py
```

**Existing (edited only by `apply-portland-me.py`):**

| File | Edit |
|---|---|
| `index.html` | one line into `PUBLISHED_PROFILES` |
| `sitemap.xml` | one `<url>` block |
| `docs/TASKBOARD.md` | new head entry, three label demotions, two count bumps |
| `docs/SITE-OPERATIONS-LOG.md` | section 7 change-log entry |

**Not edited: any landing page.** All six Portland cards were already live `city-card` links
routing through `index.html?city=Portland&state=ME`. None was marked `coming-soon`, so
`check_cards` had nothing to promote, and none carried a monthly range that v17 could have
staled. `docs/SUPERLATIVE-LEDGER.md` is also untouched: the profile produces zero
`BANNED_SUPERLATIVE` hits and zero unreviewed `claim` warnings on both the rendered and JS
surfaces, so there is nothing to vouch for.

## Deploy

```bash
git pull
unzip -o portland-me-bundle.zip
rm portland-me-bundle.zip
python3 apply-portland-me.py
python3 tools/validate.py --local .        # the gate. 0 failures, 0 warnings or stop.
python3 tools/test_statcard_faq.py         # plus the rest of the harness list
rm apply-portland-me.py                    # BEFORE git add
git status --short
git add -A && git commit -m "Portland ME profile (48); board + ops log"
git push
```

---

## Emphasis brief

Read off the DB row, not off the city's reputation.

| Dimension | Score | Role |
|---|---|---|
| D3 Health | 9 | **pillar** |
| D6 Walk | 9 | **pillar** |
| D10 Community | 9 | **pillar** |
| D1 Airport | 8 | support |
| D4 Resilience | 8 | support |
| D7 Outdoor | 7 | support |
| D8 Wellness | 6 | mid |
| D2 Budget | 5 | mid |
| D5 Tax | 4 | **hard-flagged** |
| D9 Safety | 4 | **hard-flagged** |

Three dimensions at 9 makes this a **MULTI-PILLAR** build, so the hero tagline and the opening
character paragraph both gesture at the whole cluster rather than leading with one. The trap this
rule exists to catch was live here: the food scene writes the best sentence, and a profile that
opened on it would have let a Level I trauma center and a Walk Score of 90 fade into the body.

Monthly Est `$5,900–$7,300/mo` derived through `monthly_abbrev()` to `$5.9–7.3K/mo`, not typed.
Median Home `$571,000` renders `$571K` in the stat card, which is in `home_forms()`.

## Decisions worth being able to reverse

**No Neighborhood Reality Check, and no `.reality-check` markup at all.** Under
`MEDIAN-HOME-METHODOLOGY.md` v1.2 section 4 a note is warranted where retiree-target neighborhoods
run materially *above* the citywide figure. Portland is the inverse: citywide `$571,000`, and the
West End, the neighborhood most retirees picture, runs roughly `$554K`. What moves the number is
the town line, South Portland near `$520K` against Cape Elizabeth near `$838K`, and that belongs in
the method-callout, which is where it went. The callout opens on the DB figure, per
`_sc_region_first`.

**Stat slots 3 and 4 carry proof, not scores.** `Level I` (D3) and a Walk Score band (D6). Both are
free text to `SC_SCORE`, so neither is graded, which is correct: a bare `9/10` means nothing to a
reader with no rubric in front of them.

**The D9 bullet states both halves.** CrimeGrade has Portland at the 28th percentile overall on a
property crime rate roughly 40% above the national figure, and simultaneously below the national
average on violent crime at the 84th percentile. Writing only the aggregate would have passed every
check and misled anyone deciding whether to walk home.

**Four list cards from six eligible surfaces.** Foodies, Healthcare, Urban Walkabout, Arts Lovers,
which is one per pillar plus the second D10 surface. Held back: Active Retirees (D8 is 6, the
weakest of the six claims) and LGBTQ Retirees. Natural-disasters also held back; D4 is support, not
a pillar, and the card would have displaced one.

**Related cities.** Alexandria VA and Charleston SC tie at dimension distance 7 and share the budget
tier. Philadelphia is a judgment pick at distance 13, included as the same walkable-cultured-medical
package at less than half the housing cost. Ann Arbor is the alternative at the same distance and
shares Portland's exact Monthly Est.

**Slug is `portland-me`, not `portland`.** No collision exists in the DB, but Portland OR is the
city a reader assumes, and the disambiguated slug costs nothing.

## Open items

**The detail photo is Cape Elizabeth, not Portland.** Portland Head Light stands in Fort Williams
Park, over the bridge. Kept because it is the signature image of Greater Portland and does double
duty as the honest-about-winter break, but the caption and the Anytime day card both name Cape
Elizabeth rather than letting it pass.

**`Ssorsch` is a Pexels account handle, not a confirmed name.** No EXIF on the file and the account
does not resolve to a person. Pexels does not require attribution at all, and `Szora / Pexels` on
Knoxville is the existing precedent for crediting a handle, so this ships rather than guessing a
name.

**Boarded, not fixed:** the Portland highlight string on `index.html` and `pick-and-compare.html`
opens "Perfect 10 community", but v17 has D10 at 9. Nothing reads it, so the gate is clean. It is a
BATCH item, not a BUILD one.
