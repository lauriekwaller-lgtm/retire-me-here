# DEPLOY: Burlington, VT (profile 49)

**Built:** August 6, 2026
**Database:** `docs/CityDatabase_Jul_27_v17.xlsx` (sheet "City Database", `header=1`)
**Structural base:** live `cities/st-louis/profile.html`, pulled fresh from main at build time.
Burlington is not an NRC city (see the judgment call below), so the `.reality-check` markup and
its CSS block were removed, along with the two `.reality-check` selectors in the forced-dark
hardening rule. `grep -c reality-check cities/burlington/profile.html` returns 0.

---

## Files

**New (in the zip, at final paths):**

```
cities/burlington/profile.html
cities/burlington/hero.jpg          1600x899    Stephen Mease / Unsplash
cities/burlington/detail.jpg        1600x2133   Ronan Furuta / Unsplash
cities/burlington/lifestyle.jpg     1280x1280   Prateek Pisat / Unsplash
docs/DEPLOY-burlington.md
apply-burlington.py
```

All three photos arrived already at final spec and were passed through byte for byte. No crop,
no resample, no re-encode. CSS anchors are `center 72%` on the hero (holds the water band under
the title overlay), `center 10%` on the detail (pushes the snowbank into the corner), and
`center 45%` on the lifestyle.

Seasons run summer / winter / autumn across the three, deliberately. The lifestyle caption names
the season and hands off to the winter rather than closing on the pretty picture.

**Existing (edited only by `apply-burlington.py`):**

| File | Edit |
|---|---|
| `index.html` | one line into `PUBLISHED_PROFILES`; property tax 1.42% to 1.51% on three surfaces; D2 scoreNote median $506K to $520K |
| `pick-and-compare.html` | the same property tax fix in its own `CITIES` array |
| `sitemap.xml` | one `<url>` block |
| `docs/TASKBOARD.md` | new head entry carrying "49 profiles", Wave 1 line, CLOSED section, one new P2 |
| `docs/SITE-OPERATIONS-LOG.md` | section 7 change-log entry |

**Not edited: any landing page.** All seven Burlington cards were already live `city-card` links
routing through `index.html?city=Burlington&state=VT`: five landing pages (hikers, arts lovers,
foodies, LGBTQ retirees, avoid natural disasters) and two guides (urban-walkabout,
active-frontier). None was `coming-soon`, so `check_cards` had nothing to promote. Burlington is
Budget Range 3, so the `DB_ROSTERS` predicate on the budget page does not reach it.
`docs/SUPERLATIVE-LEDGER.md` is untouched: the profile produces zero `BANNED_SUPERLATIVE` hits
and zero unreviewed `claim` warnings, so there is nothing to vouch for.

## Deploy

```bash
git pull
unzip -o burlington-bundle.zip
rm burlington-bundle.zip
python3 apply-burlington.py
python3 tools/validate.py --local .            # the gate. 0 failures, 0 warnings or stop.
git status --short --untracked-files=all       # expect exactly 10 lines
test $(git status --short --untracked-files=all | wc -l) -eq 10 && echo COUNT-OK
rm apply-burlington.py                         # BEFORE git add
git add -A && git commit -m "Burlington VT profile (49); VT property tax + D2 median corrected on index and pick-and-compare; board + ops log"
git push
```

`--untracked-files=all` is not decoration. Plain `git status --short` collapses
`cities/burlington/` to a single `??` line, so the count reads 6 and tells you nothing about
whether all four new files actually landed. The expanded form is 5 new files plus 5 modified.

---

## Emphasis brief

Read off the DB row, not off the city's reputation.

| Dim | Score | Tier |
|---|---|---|
| D7 Outdoor | 9 | **pillar** |
| D3 Health | 8 | support |
| D10 Community | 8 | support |
| D6 Walk | 7 | support |
| D8 Wellness | 7 | support |
| D9 Safety | 7 | support |
| D1 Airport | 6 | middle |
| D2 Budget | 5 | middle |
| D5 Tax | 3 | **hard flag** |

One pillar, not three, so the MULTI-PILLAR rule does not fire. This is the MULTI-STRENGTH
advisory: lead with the standout, but give the eight-cluster real weight in the character section
or the profile reads as a ski page. Burlington is unusually easy to write badly here, because the
lake-and-mountains story writes itself and the hospital story does not.

Also from the row: Range 3, Monthly Est $6,000-$7,500/mo, Median Home $520,000, PropTax 1.51%,
HO insurance $1,063/yr, D4 Resil. 7 (July 2023 flooding, otherwise low exposure), Climate W3,
Jan mean 19F, 70 in annual snow, 49% annual sun.

**Stat cards.** Home Value and Monthly Budget are fixed. Slot 3 is Outdoor Recreation, filled
with "4 ski areas" rather than a score. Slot 4 is Healthcare, filled with "Level I trauma". No
`N/10` anywhere on the page except the health-card grade, which is the one place the template
puts one.

---

## Judgment calls

Each is one edit to reverse.

**1. No Neighborhood Reality Check.** `MEDIAN-HOME-METHODOLOGY.md` section 4 makes this a
judgment, not a binary. Citywide is $520,000. Retiree-target areas run South Burlington around
$485K, Williston $500K-$700K, Shelburne $600K-$900K, Hill Section $600K-$1M and up. Two of the
four sit at or below the citywide figure, so it brackets the range rather than understating it.
That is section 4's explicit "adds noise rather than clarity" case, and it is not the St. Louis
case ($192K citywide against $420K-$575K). The spread is carried by the method callout and the
hood cards instead. To reverse: add the `<aside class="reality-check">` block between the stats
bar and the cost strip, restore the CSS from any NRC profile, and restore the two selectors in
the forced-dark rule.

**2. Slot 4 went to healthcare on a D3/D10 tie at 8.** Reasoning: retirees weight healthcare
hardest, and D10 already carries the character section, a week card and a list card. Swap to an
Arts & Culture slot if you disagree.

**3. The healthcare card says "Level I trauma", not a bed count.** The Prescott pattern prefers a
bed count, but UVMMC's public bed figures run 481, 562 and 620 depending on what is counted, and
a contested number should not be a headline fact. "Vermont's only Level I Trauma Center" is
uncontested and verifiable.

**4. Four list cards out of five live placements.** Dropped: Best Places to Retire and Avoid
Natural Disasters, where Burlington sits in the page's second-tier bucket ("a notable seasonal
hazard or localized flood risk") on the back of the July 2023 flooding. Hikers, arts lovers,
foodies and LGBTQ retirees are all top-tier placements, checked against
`hikers-cities-scoring-analysis.md` (7.8), `arts-lovers-` (8.0), `foodie-` (7.2) and
`lgbtq-retirees-`. The dropped card stays live on its own page.

**5. Related cities: Portland ME, Madison WI, Salt Lake City UT.** Range 3 peers with the closest
vector. Madison and Salt Lake City already carry reciprocal Burlington cards, so those two edges
close in both directions on this deploy. No comparison page exists for Burlington yet, so the
profile carries no compare CTA block; `check_comparison_cta_reciprocity` has no pair to assert.

---

## Corrections made on the way through

**Property tax, three surfaces plus one.** `index.html` carried 1.42% in the Burlington highlight
string, in a cons bullet and in the D5 scoreNote, against a DB `PropTax Rate %` of 1.51.
`pick-and-compare.html` carries its own copy of the highlight string, and `check_figures`
compares the two character for character, so the first gate run FAILED on a half-finished fix.
That is the check working. Both surfaces now move together in the same script.

**D2 scoreNote median.** Was "Citywide median $506K (Redfin Feb 2026)" against a DB `Median Home`
of $520,000. Now "Citywide typical home value $520K". The Redfin attribution went with the
figure: an MLS median sale price and a ZHVI typical value are different measures, and
`PROFILE-FORMATTING.md` v1.7 is explicit that they must not be swapped under one source line.

**Left open on purpose: snowfall.** DB `Ann Snow in` is 70. `index.html` says approximately 80
inches. The NOAA 1991-2020 normal for Burlington is about 81. The profile uses 70 per the
data-source rule, and the DB cell is boarded as a new P2 rather than reconciled, because editing
live copy down to match a suspect database cell propagates the error instead of finding it.

---

## Board-count trap

`check_docs` reads the FIRST `(\d+)\s+profiles` match in `TASKBOARD.md`. Before this deploy that
match sat at line 164, inside July 29 historical prose reading "so all 48 profiles inherited it",
which is correct as history and must not be edited. The apply script puts "49 profiles" in the
new Last-updated paragraph at the top of the file, which becomes the first match. **The next
build has to do the same thing**, or the count silently reverts to being graded against a
sentence about last month.

---

## Verified before hand-off

- `python3 tools/validate.py --local .` on a fresh clone with the package applied: **0 failures,
  0 warnings**, all eleven harnesses passing
- `apply-burlington.py` re-run on an already-applied tree: five no-ops, nothing written
- `<strong>` balance 26 / 26
- JSON-LD parses; FAQ figures agree with the DB ($520,000 and $6,000 to $7,500)
- zero em-dashes in rendered content, meta tags or JSON-LD
- exactly one `back-to-top-wrap` per major section (6)
- sticky chip nav present, Visit chip last, `'visit'` in the scroll-spy ids array
- no `DOMContentLoaded` auto-open of the guide form
- no `_TK` placeholders; per-city Expedia (`Gy4FiIj`) and Vrbo (`xedaytz`) codes in place with
  `rel="sponsored nofollow"`
- Deep Dive block in the lower cluster, before Visit and the Quiz CTA
- quiz copy says "the quiz", no question count
