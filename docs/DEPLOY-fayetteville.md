# DEPLOY: Fayetteville, AR (profile 50)

**Built:** August 7, 2026
**Database:** `docs/CityDatabase_Jul_27_v17.xlsx` (sheet "City Database", `header=1`)
**Structural base:** live `cities/st-louis/profile.html`, pulled fresh at build time.
Fayetteville is not on the live NRC roster (which greps to thirteen cities, not the ten the
board records), so the Neighborhood Reality Check callout and the `.reality-check` CSS were
both removed. The `lists-grid-four` rule that shares the reality-check media query was kept.

---

## Files

**New (in the zip, at final paths):**

```
cities/fayetteville/profile.html
cities/fayetteville/hero.jpg          1600x899
cities/fayetteville/detail.jpg        1600x2133
cities/fayetteville/lifestyle.jpg     1280x1280
docs/DEPLOY-fayetteville.md
apply-fayetteville.py
```

**Existing (edited only by `apply-fayetteville.py`, nineteen edits across six files):**

| File | Edit |
|---|---|
| `index.html` | one line into `PUBLISHED_PROFILES`, plus thirteen copy corrections |
| `pick-and-compare.html` | the same highlight string, second surface |
| `sitemap.xml` | one `<url>` block |
| `best-places-to-retire-on-a-budget.html` | rank-8 card, `coming-soon` div to live anchor |
| `docs/TASKBOARD.md` | new head entry, profile count 49 to 50, four items boarded |
| `docs/SITE-OPERATIONS-LOG.md` | section 7 change-log entry |

**Not edited: `docs/SUPERLATIVE-LEDGER.md`.** The profile produces zero `BANNED_SUPERLATIVE`
hits and zero unreviewed `claim` warnings on both the rendered and JS surfaces, so there is
nothing to vouch for. "Ranked first in Arkansas" is an outside-world claim, but it carries no
word from the `claim` regex's first group and does not reach the warn queue.

**Expected file count before commit:** eleven.

```bash
test $(git status --porcelain --untracked-files=all | wc -l) -eq 11
```

`--untracked-files=all` is load-bearing. The default collapses the four new files under
`cities/fayetteville/` into one `?? cities/fayetteville/` line and the assertion reads eight.

## Deploy

```bash
git pull
unzip -o fayetteville-bundle.zip
rm fayetteville-bundle.zip
python3 apply-fayetteville.py
python3 tools/validate.py --local .        # the gate. 0 failures, 0 warnings or stop.
git status --porcelain --untracked-files=all | wc -l    # expect 11
rm apply-fayetteville.py                   # BEFORE git add
git add -A && git commit -m "Fayetteville AR profile (50); budget card live; index copy corrections; taskboard + ops log"
git push
```

`apply-fayetteville.py` is idempotent. Each edit is keyed to a marker string present only
after that edit has landed, so a second run reports "already" and writes nothing new. It
aborts before writing anything at all if any anchor is missing or matches more than once.

---

## The brief this was built against

**No pillar.** Nothing in the row reaches nine. Four dimensions tie at eight: D2 Budget,
D3 Health, D7 Outdoor, D10 Community. Three sit at seven (D5 Tax, D8 Wellness, D9 Safety),
two at six (D1 Airport, D6 Walk), D4 Resilience at six. Nothing is hard-flagged at four or
below. Total seventy-one.

The skill tunes `PILLAR_FLOOR` at nine with a `MIN_PILLARS` of three, and its MULTI-STRENGTH
advisory assumes one standout plus a cluster. Neither fires here, and the skill has no case
for a flat cluster with no peak. The reading taken, and approved before build: treat the four
eights as a de facto pillar cluster, and require the hero tagline and the opening character
paragraph to touch all four. **This is a gap in `retiremehere-city-profile`, not in the data.**
Boarded as an OPS item.

**Honest counterweight.** Nothing is hard-flagged, so the "skip if" column is built from the
sixes and the climate rather than from a flagged score. It leads with winter (January mean
36F, about eleven inches of snow, sixty percent sun), then the regional airport, then car
dependence, then humid summers and spring storm season.

**Stat cards.** Home $385K and monthly $4.9 to 6.1K are fixed. Card three is Healthcare with
"425 beds", per the deployed Prescott bed-count pattern rather than a hospital name. Card four
is Outdoors with "40+ trail mi": chosen over Community because the D2 figure is already spent
on two cards, and because the Greenway is the asset Fayetteville owns rather than borrows.

---

## Judgment calls, all overridable

1. **Crystal Bridges is attributed to Bentonville everywhere it appears**, in the body copy,
   the week grid and the `index.html` D10 note. It is a thirty-minute drive and a genuine part
   of the weekly reality, but it is not Fayetteville's, and the previous D10 note read as
   though it were.
2. **The lists section ships with one card**, under `lists-grid` rather than `lists-grid-four`.
   Precedent is live `cities/prescott/profile.html`, which ships a single card the same way.
   Fayetteville appears on no other landing list; the other five hits are guide pages, which
   carry no cards.
3. **Related cities are Roanoke, Knoxville and Bentonville.** Roanoke is the nearest D1 to D10
   vector among published profiles at 2.0, Knoxville next at 2.24 and the closest same-tier
   college-and-mountains peer. Bentonville is included at 2.65 as the in-corridor comparison a
   reader will make whether or not the vector recommends it.
4. **No comparison-page CTA.** No Fayetteville comparison page exists yet. The chip nav's
   "compare" target is the related-cities section, as on Prescott.
5. **`Budget Range` left at 1** despite the v3.2 rubric putting Range 1 under $3,500/mo. Live
   Range 1 profiles ship at $4,100 to $6,100, so the field has drifted from the rubric
   site-wide and Fayetteville is consistent with practice. Changing it here would have made
   this profile the outlier. Boarded as a P2 OPS item instead.

---

## Corrections made to existing `index.html` copy

Two were flagged before build. Four more were found while building.

| # | Was | Now |
|---|---|---|
| 1 | "Fastest growing city in Arkansas" | False in percentage terms. Centerton has led three years running at about forty-nine percent since 2020; Bentonville grew 16.3 percent 2020 to 2025. Replaced with figures: second-largest city, near 109,000, adding about 2,900 a year. |
| 2 | hoods listed "Bentonville / Rogers" | A separate city twenty to thirty minutes north. Replaced with Washington-Willow / Mount Nord. |
| 3 | Lake Leatherwood, four instances | **In Eureka Springs, about forty-five minutes northeast.** One instance read "Lake Leatherwood trails in city". Replaced across pros, D6, D7 and D8 with Mount Kessler, the Greenway, Lake Fayetteville and Lake Sequoyah. |
| 4 | D5 "Arkansas income tax 4.4% flat" | Wrong twice: the rate is graduated, not flat, and 4.4 percent was the 2025 figure. The 2026 top rate is 3.9 percent, down from 5.9 percent in 2022. |
| 5 | D3 "adequate for routine and moderate care" | Undersold a D3 of eight. Washington Regional is 425 beds, a U.S. News Best Regional Hospital ranked first in Arkansas, high performing in thirteen adult procedures, CMS four stars. The old note also muddled UAMS, which is in Little Rock. |
| 6 | D1 "surprisingly strong for an Arkansas city" | Oversold a D1 of six, and placed XNA in Fayetteville. It is in Highfill, about thirty-five minutes out, six airlines, twenty-seven nonstops, no hub carrier. |
| 7 | D7 listed Petit Jean State Park | About two and a half hours away, near Morrilton. Replaced with Devil's Den at thirty minutes and the Buffalo National River at about two hours. |
| 8 | highlight displayed "budget 8 of 10" | A bare score means nothing to a reader with no rubric in front of them. Dropped. |

**The `pick-and-compare.html` edit was found by the gate, not by reading.** The highlight
string lives on two surfaces and `check_figures` compares them. Editing `index.html` alone
left the compare tool still showing the false rank claim, and the gate failed on the mismatch.
Worth remembering as the same shape as the Lake Leatherwood finding: the copy that survives
longest is the copy nothing reads.

---

## Photos

All three by Brandon Rush via Wikimedia Commons.

| Slot | Subject | Licence | Crop |
|---|---|---|---|
| hero | Poppies and old buildings on the Square | CC0 | y 60 to 2178, full width, downsampled |
| detail | 534 Willow Avenue, Washington-Willow Historic District | **CC BY-SA 3.0** | x 700 to 2258, full height, 2.7% upscale |
| lifestyle | Razorback Regional Greenway at Lake Fayetteville | CC0 | 2100px square at x 1250 y 300, downsampled |

**The detail image carries a share-alike obligation.** The crop is offered under CC BY-SA 3.0,
and that is stated in both the photo credit and the footer. Do not swap that image without
also editing both statements.

The detail upscale is 2.7 percent, inside the ten percent ceiling. Four candidate images were
rejected before these: two were Burlington, Vermont; one was a three-megapixel University of
Arkansas frame that could not reach the portrait spec without a thirty percent upscale, and
which also showed a campus monument under an active removal dispute; and one was a
lower-resolution Willow Avenue shot needing a thirty percent upscale.

---

## Affiliate

Confirmed by the operator before build. Expedia `iSurfAX`, Vrbo `32xKR9x`. Both checked
against every live profile for collisions: none. `check_affiliate` hard-fails a profile with
no Expedia or Vrbo link, so the Visit block could not have been held back for a later ship
without the gate going red.

---

## Gate

`python3 tools/validate.py --local .` on a fresh clone with this bundle applied:
**0 failures, 0 warnings.** All eleven harnesses pass. Verified again after a second run of
the apply script to confirm idempotency.

Also verified by hand: `PUBLISHED_PROFILES` resolves `Fayetteville_AR` to a file that exists
(map size fifty), the budget card is a live `<a>` routing through
`index.html?city=Fayetteville&state=AR`, all three related-card targets resolve in the map,
no broken internal links, `<strong>` and `<section>` balanced at 24 and 14, both JSON-LD
blocks parse, and the sitemap is well-formed XML.
