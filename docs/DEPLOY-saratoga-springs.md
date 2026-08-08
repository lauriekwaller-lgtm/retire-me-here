# DEPLOY: Saratoga Springs, NY (profile 51)

**Built:** August 8, 2026
**Database:** `docs/CityDatabase_Jul_27_v17.xlsx` (sheet "City Database", `header=1`), row 57
**Structural base:** live `cities/st-louis/profile.html`, pulled fresh from main at build time.
Saratoga Springs is not an NRC city (see judgment call 1), so the `.reality-check` markup and its
CSS block were removed, along with the two `.reality-check` selectors in the forced-dark
hardening rule. `grep -c reality-check cities/saratoga-springs/profile.html` returns 0.

---

## Files

**New (in the zip, at final paths):**

```
cities/saratoga-springs/profile.html
cities/saratoga-springs/hero.jpg          1600x899    Joshua Adams / Unsplash
cities/saratoga-springs/detail.jpg        1600x2133   Tyler A. McNeil / Wikimedia, CC BY-SA 4.0
cities/saratoga-springs/lifestyle.jpg     1280x1280   Peter Flass / Wikimedia, CC BY 3.0
docs/DEPLOY-saratoga-springs.md
apply-saratoga-springs.py
```

All three were cropped and resampled down from larger originals. Nothing was upscaled. Source
sizes were 2400x1470 (race course), 3840x2560 (Congress Park) and 3600x2400 (Saratoga Lake).

CSS anchors moved off the canonical defaults in two places. Hero is `center 45%`, not the
inherited `center 60%`: the horses and jockeys occupy the 33 to 67 per cent band of the crop and
60 would clip heads on a wide viewport, while 45 leaves the clean dirt under the tagline and the
stats bar. Lifestyle is `center 40%`, because Snake Hill sits at about 35 per cent height and
needs to stay clear of the banner title. Detail is centred and unchanged.

**Existing (edited only by `apply-saratoga-springs.py`):**

| File | Edit |
|---|---|
| `index.html` | one line into `PUBLISHED_PROFILES`; `highlight` rewritten; `pros` rewritten; `culture_walkable` pairing `s1: 10` to `8` |
| `pick-and-compare.html` | its own copy of the same `highlight` string |
| `value-navigator.html` | budget badge `Range 3` to `Range 4` |
| `sitemap.xml` | one `<url>` block |
| `docs/TASKBOARD.md` | new Last-updated block carrying "51 profiles", old head demoted to Before that |
| `docs/SITE-OPERATIONS-LOG.md` | section 7 change-log entry |

**Not edited: any landing page.** All three Saratoga cards were already live `city-card` links
routing through `index.html?city=Saratoga Springs&state=NY`: arts lovers, avoid natural
disasters, LGBTQ retirees. None was `coming-soon`, so `check_cards` had nothing to promote.
Saratoga also carries cards on four guides (wellness-blueprint, urban-walkabout,
value-navigator, globetrotter-guide); only value-navigator needed a fix, and that was a wrong
budget range rather than a card promotion. Budget Range 4, so the `DB_ROSTERS` predicate on the
budget page does not reach it. `docs/SUPERLATIVE-LEDGER.md` is untouched: the profile produces
zero `BANNED_SUPERLATIVE` hits and zero unreviewed `claim` warnings.

## Deploy

```bash
git pull
unzip -o saratoga-springs-bundle.zip
rm saratoga-springs-bundle.zip
python3 apply-saratoga-springs.py
python3 tools/validate.py --local .            # the gate. 0 failures, 0 warnings or stop.
git status --short --untracked-files=all       # expect exactly 11 lines
test $(git status --short --untracked-files=all | wc -l) -eq 11 && echo COUNT-OK
rm apply-saratoga-springs.py                   # BEFORE git add
git add -A && git commit -m "Saratoga Springs NY profile (51); D10 perfect-10 claim corrected on index + pick-and-compare + pairings; value-navigator budget range fixed; board + ops log"
git push
```

`--untracked-files=all` is not decoration. Plain `git status --short` collapses
`cities/saratoga-springs/` to a single `??` line, so the count reads 7 and tells you nothing
about whether all four new files landed. The expanded form is 5 new files plus 6 modified.

---

## Emphasis brief

Read off the DB row, not off the city's reputation.

| Dim | Score | Tier |
|---|---|---|
| D4 Resil. | 8 | top cluster |
| D6 Walk | 8 | top cluster |
| D9 Safety | 8 | top cluster |
| D10 Comm. | 8 | top cluster |
| D7 Outdoor | 7 | support |
| D1 Airport | 6 | middle |
| D3 Health | 6 | middle |
| D8 Wellness | 6 | middle |
| D2 Budget | 4 | **hard flag** |
| D5 Tax | 2 | **hard flag** |

**No pillar at all.** Nothing reaches 9. This is the first profile built on a vector with no
standout, and it is the case the MULTI-PILLAR rule was written for even though the rule's own
threshold does not fire: four dimensions tie at the top, so the hero tagline and the opening
character paragraph both have to carry the cluster or the page becomes an arts brochure. The
character section's topic-sentence bold states the actual argument in one line, that none of the
city's strengths depend on a car, and the second bold states the seasonal split.

The failure mode this profile was most at risk of is the one the live `index.html` copy had
already fallen into: leading on culture because SPAC and the race course are the vivid hooks,
and quietly overstating the community score to justify it.

Also from the row: Range 4, Monthly Est $6,900-$8,600/mo, Median Home $663,000, PropTax 1.30%,
HO insurance $1,683/yr, Setting Lakeside, Character Historic / Arts & Culture / Nature-Centric,
D4 rationale "Upstate; low catastrophic exposure", Climate W2 H7 M6, HUM 6, HEAT 5, Jan mean
22F, 60 in annual snow, 52% annual sun.

**Stat cards.** Home Value and Monthly Budget are fixed. Slot 3 is Summer Arts, filled with
"SPAC" rather than a score. Slot 4 is Healthcare, filled with "Saratoga Hospital" and a bed
count in the sub-line per the Prescott pattern. No `N/10` anywhere on the page except the
health-card grade at 6, which is the one place the template puts one.

---

## Judgment calls

Each is one edit to reverse.

**1. No Neighborhood Reality Check.** `MEDIAN-HOME-METHODOLOGY.md` section 4 asks whether the
citywide figure understates the realistic retiree budget. Here it does not. The $663,000 citywide
value already sits near the top of what the city costs; the East Side runs above it, the West
Side below it, and the Northway towns below again. A callout would have to argue in two
directions at once, which is section 4's "adds noise rather than clarity" case. The spread is
carried by the method callout in the neighbourhoods section instead. To reverse: add the
`<aside class="reality-check">` block between the stats bar and the cost strip, restore the CSS
from any NRC profile, and restore the two selectors in the forced-dark rule.

**2. Slot 3 went to Summer Arts on a four-way tie at 8.** Walkability, safety, community and
resilience all score 8, and only one can have a card. Community won because SPAC is the single
most externally verifiable credential the city has, and because walkability and safety both get
named figures elsewhere on the page. Safety at 84th percentile is the obvious alternate. Swap
if you disagree.

**3. Neighbourhood prices are directional, not sourced medians.** The four hood cards use
relative language ("well above the citywide figure", "the city's value end") plus one hard
number for downtown condos. Three sources disagreed by roughly $330,000 because they are
different measures: a Zillow ZHVI typical value near $619K, a listing median near $770K in July
2026, and a Redfin sold median of $913K in a month with 22 sales. `PROFILE-FORMATTING.md` v1.7
forbids reading one against another, and a per-neighbourhood figure that cannot name its series
is worse than a directional sentence. Hood cards are exempt from `check_statcard_faq`, so precise
figures were permitted here; none was defensible. Replace with real local numbers if you have
them.

**4. Related cities: Burlington VT, Portland ME, Charlottesville VA.** Burlington is the genuine
nearest vector among published profiles at a Euclidean distance of 3.74, well clear of the next
(Madison at 5.57). The other two are a deliberate price ladder rather than same-budget-tier
peers. The Range 4 cities are Bend and Bozeman, both mountain-outdoor cities that are expensive
for reasons that have nothing to do with why Saratoga is expensive, and sending a reader from a
walkable Victorian arts town to Bozeman is a worse answer than sending them to Portland. No
comparison page exists for Saratoga Springs yet, so the profile carries no compare CTA block and
`check_comparison_cta_reciprocity` has no pair to assert.

**5. Three list cards, so `lists-grid` not `lists-grid-four`.** Three live placements, all
verified against their scoring analyses where one exists: `arts-lovers-cities-scoring-analysis.md`
puts Saratoga at rank 10 with a score of 8.9, and `lgbtq-retirees-cities-scoring-analysis.md`
carries it on state protections and the upstate tradition. The natural-disasters placement is
consistent with D4 Resil. 8 and the DB rationale. Nothing was dropped.

---

## Corrections made on the way through

All four were invisible to the validator. None trips any existing check, which is why they had
survived.

**"Perfect 10 community", three surfaces.** `index.html` asserted it in the Saratoga `highlight`
string and again in `pros[0]`, and `pick-and-compare.html` carries its own copy of the same
highlight. The DB says D10 Comm. is **8**. The `culture_walkable` pairings block near the foot of
`index.html` carried `s1: 10` for the same city. All four now read 8 or drop the claim. Note that
five other cities legitimately carry "Perfect 10 community" (Santa Fe, Portland ME,
St. Augustine, Prescott, Santa Barbara) and were left alone; a blanket grep-and-replace here
would be wrong.

**`value-navigator.html` budget badge.** Read `Range 3 · $6,900–$8,600` against a DB Budget Range
of 4. Frisco TX on the same page, at $7,000-$8,700, badges Range 4 correctly, so this is a
one-off typo rather than a different convention.

**`pros[2]` superlative.** "Most walkable small city in Upstate NY" is an outside-world
superlative with nothing behind it and no ledger entry. Replaced with "Walkable Victorian
downtown: walkability 8 of 10", which is anchored to the DB.

**The New York tax framing.** The live D5 scoreNote reads "NY income tax up to 10.9%: among the
worst nationally for retirees". True and misleading in the same breath: 10.9% is the top marginal
bracket and reaches almost no retiree. The profile prose states the position properly, that New
York exempts Social Security entirely and exempts federal, state and local government pensions,
with a $20,000 exclusion at 65 on other retirement income, and that the property side at 1.30%
is what actually bites. Tax is still honestly a 2 of 10. The scoreNote itself was left alone as
out of scope for a build.

**Left open on purpose: the home-value gap.** DB `Median Home` is $663,000. Zillow's live ZHVI
page for Saratoga Springs read $618,681 at the end of June 2026, a gap of about seven per cent.
The profile displays the DB figure in all five places it names one, per the data-source rule, and
the gap is boarded rather than reconciled, on the Burlington snowfall precedent: a build chat is
the wrong place to overwrite a database cell. Worth a look during the next DB pass, because the
June 2026 ZHVI rebase was meant to have closed exactly this kind of gap, so one stale row may
mean others.

---

## Board-count trap

`check_docs` reads the FIRST `(\d+)\s+profiles` match in `TASKBOARD.md`. The apply script puts
"51 profiles live" in the new Last-updated paragraph at the top of the file, which becomes the
first match, and demotes the previous head to `**Before that:**` so the ladder stays single. The
board prose added by this deploy spells its numbers out ("fifty-one", "eight", "four") for the
same reason. **The next build has to do the same thing.**

---

## Verified before hand-off

- `python3 tools/validate.py --local .` on a fresh clone with the package applied: **0 failures,
  0 warnings**, all twelve harnesses passing
- `apply-saratoga-springs.py` re-run on an already-applied tree: six no-ops, nothing written
- `<strong>` balance 28 / 28
- HTML tag balance: no stray or unclosed tags
- JSON-LD parses; FAQ figures agree with the DB ($663,000 and $6,900 to $8,600)
- stat-card monthly renders `$6.9–8.6K/mo`, which is what `monthly_abbrev` derives from the DB
- zero em-dashes in rendered content, meta tags or JSON-LD; the five remaining are inside
  inherited `<style>` comments, non-rendered, same as the canonical
- exactly one `back-to-top-wrap` per major section (7)
- sticky chip nav present, Visit chip last, `'visit'` in the scroll-spy ids array
- no `DOMContentLoaded` auto-open of the guide form
- no `_TK` placeholders; per-city Expedia (`sl8dEUv`) and Vrbo (`Gx2IoHs`) codes in place with
  `rel="sponsored nofollow"`
- Deep Dive block in the lower cluster, before Visit and the Quiz CTA
- quiz copy says "the quiz", no question count
- all four internal `href` targets resolve to files that exist
- routing confirmed end to end: `PUBLISHED_PROFILES['Saratoga Springs_NY']` resolves, sitemap
  entry present, all three landing-page cards live rather than coming-soon

## Two open items for the operator

**1. Photo licence links.** The two Wikimedia credits name the author and link the licence, per
the Fayetteville pattern, but do not link the Commons file pages, because
commons.wikimedia.org was unreachable from the build container and the skill forbids guessing a
URL. If you want the file-page links in (the Prescott pattern does link them), paste the two
Commons URLs and it is a two-line edit to the footer and the two inline credits.

**2. Share-alike obligation is live.** The Congress Park detail photo is CC BY-SA 4.0, so the
cropped derivative RetireMeHere publishes is itself offered under CC BY-SA 4.0. That is stated in
both the inline credit and the footer. It is a licence condition, not a courtesy, and it should
survive any future crop or replacement of that image.
