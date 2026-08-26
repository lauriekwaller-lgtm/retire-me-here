# DEPLOY: Raleigh, NC

**Built:** August 25, 2026
**Profile #:** 53
**Database:** `docs/CityDatabase_Jul_27_v19.1.xlsx`, sheet `City Database`, `header=1`
**Canonical base:** live `cities/st-louis/profile.html`, pulled fresh from GitHub at build time

---

## 1. What is in the bundle

New files only. Every one already at its final path.

```
cities/raleigh/profile.html
cities/raleigh/hero.jpg          1600x899
cities/raleigh/detail.jpg        1600x2133 (portrait)
cities/raleigh/lifestyle.jpg     1280x1280 (square)
docs/DEPLOY-raleigh.md
apply-raleigh.py
```

Photos ride the zip because they are NEW files. The "always dragged, never
patched" rule in `DEPLOY-CHEATSHEET.md` covers REPLACEMENT photos, which are
existing files and therefore cannot ride a zip. Boarded as P2; this build follows
section 4.

## 2. What `apply-raleigh.py` edits

14 edits across 9 files that already exist.

| File | Edit |
| --- | --- |
| `index.html` | `PUBLISHED_PROFILES`: add `'Raleigh_NC'` |
| `index.html` | Raleigh `pros`: NC income tax 4.75% -> 3.99% (2026) |
| `index.html` | Raleigh `scoreNotes.D5`: same, with the pension/IRA treatment spelled out |
| `index.html` | Raleigh `scoreNotes.DW`: Jan avg 39F -> 41F, per DB `Jan Mean F` |
| `sitemap.xml` | insert the Raleigh `<url>` block |
| `tools/validate.py` | `check_pillar_links`: `seen != 52` -> `53` |
| `top-cities-for-healthcare.html` | redirect card -> direct link |
| `top-cities-for-active-retirees.html` | redirect card -> direct link |
| `best-places-to-retire-avoid-natural-disasters.html` | redirect card -> direct link |
| `wellness-blueprint.html` | redirect card -> direct link |
| `urban-walkabout.html` | redirect card -> direct link |
| `globetrotter-guide.html` | redirect card -> direct link |
| `docs/TASKBOARD.md` | ninth entry, 53 profiles, P3 for the remaining NC tax figures |
| `docs/SITE-OPERATIONS-LOG.md` | change-log entry incl. negative findings |

The script refuses to write anything unless every anchor is found exactly once,
refuses to run at all if a photo is missing or `PHOTO_CREDIT_TK` is still in the
profile, chains `tools/build_sitemap.py`, and warns on a shallow clone.

**Idempotence.** Two edits are insertions rather than substitutions (the sitemap
`<url>` block, the ops-log entry), so their anchor survives inside their own
replacement. Those two carry an explicit `sentinel`. Without it a second run
inserts a duplicate, which is exactly what happened on the first draft and was
caught only by running the script twice. Second run now reports
`No-op: all 14 edits are already applied.`

## 3. Deploy sequence

```bash
git pull
unzip -o raleigh-bundle.zip
rm raleigh-bundle.zip
python3 apply-raleigh.py --check
python3 apply-raleigh.py
python3 tools/validate.py --local .        # 0 failures, 0 warnings or stop
rm apply-raleigh.py
git status --short --untracked-files=all
git add -A && git commit -m "Raleigh NC profile (53); 6 dead-end cards now link direct; NC tax rate and Jan mean corrected on Raleigh; board + ops log"
git push
```

Expected `git status`: 4 new files under `cities/raleigh/`, 1 new doc, 9 modified.

## 4. Data, read from the DB and nowhere else

| Field | Value |
| --- | --- |
| D1 Airport | 9 |
| D2 Budget | 7 |
| D3 Health | 10 |
| D4 Resilience | 7 |
| D5 Tax | 7 |
| D6 Walk | **4 (hard flag)** |
| D7 Outdoor | 6 |
| D8 Wellness | 6 |
| D9 Safety | 6 |
| D10 Community | 7 |
| Monthly Est | $5,400-$6,700/mo |
| Median Home | $436,000 |
| Budget Range | 2 |
| PropTax | 0.66% |
| HO Insurance | $3,124/yr |

**Brief.** Pillars (>=9): D3 and D1. Two, not three, so this is the
MULTI-STRENGTH shape rather than MULTI-PILLAR: the standout leads, the second
pillar is established in the same hero line, and the 7-cluster (D2, D4, D5, D10)
carries real weight in the character section. Support (7-8): D2, D4, D5, D10.
Hard flag (<=4): D6 at 4, which leads the "Skip Raleigh if" column.

**No `/10` on the stats bar.** The healthcare card shows 10/10, matching deployed
`cities/st-louis/profile.html`. The skill file says never; the canonical says
otherwise; the board carries this as P3 and the skill file is the bug. Noted
again here so the next build does not relitigate it.

**Not an NRC city.** $436K is a real Raleigh figure, not a city-versus-suburb
artifact, so no callout. The unused `.reality-check` CSS was stripped from the
clone, including its two selector-group appearances in the forced-dark block, so
`grep -l 'reality-check-eyebrow' cities/*/profile.html` does not count Raleigh.
The `.lists-grid-four` mobile rule that lived inside the same `@media` block was
kept.

## 5. Judgment calls, flagged for override

1. **NC tax fix scoped to Raleigh only.** index.html gives NC as a flat 4.75%
   (the 2023 rate) in six places; the DB State Tax Facts sheet and the
   validator-checked TAXFACTS array both say 3.99% for 2026. Only Raleigh's two
   are fixed. Asheville, Wilmington NC, Beaufort and Pinehurst are boarded as P3
   with line numbers. Widening this to all six is a one-line change to the apply
   script if you would rather sweep it now.
2. **Three list cards, not four.** Healthcare, Active Retirees, Natural
   Disasters. Raleigh is deliberately absent from Sports Fans:
   `docs/sports-fans-cities-scoring-analysis.md` holds a 2-team minimum for Tier 2
   and Raleigh has one (Hurricanes). Uses `.lists-grid` (3-up), not
   `.lists-grid-four`.
3. **Related cities: Nashville, Columbus, Asheville.** Nashville is the nearest
   same-tier vector match, Columbus the nearest overall, Asheville the in-state
   comparison a reader naturally weighs and a deliberate inversion of the
   healthcare story.
4. **RDU nonstop count not printed.** Three flight aggregators agree on 91-92
   destinations as of August 2026; one SEO page says "over 60". Rather than print
   a count that drifts and disagrees with itself, the profile names the routes:
   London, Paris, Frankfurt, Dublin. Change it to a number if you prefer.
5. **Hood-card figures.** Zillow ZHVI, July 31 2026, same series as the DB:
   North Raleigh $496,802, Cary $628,913 (city page $600,054; stated as "around
   $600K"). Wake Forest median sale $450-454K, Garner around $380K, stated as a
   $380K-$500K range. Inside-the-Beltline $650K-$1M from multiple brokerage
   sources, with Hayes Barton noted as higher. Hood-card figures are deliberately
   outside `check_statcard_faq`, so these are on the editor, not the gate.

## 6. Negative findings

Recorded so nobody re-checks them.

* No Raleigh `coming-soon` card exists anywhere, so `check_cards` had nothing to
  promote.
* No `raleigh-vs-*-retirement.html` exists, so the profile carries no
  "Compare these" section, matching Indianapolis.
* index.html's Raleigh D2 monthly prose already agreed with the DB at
  $5,400-$6,700. The standing D2 reconciliation found nothing here.
* Raleigh's affiliate row already existed in `docs/AFFILIATE-CODES.csv`
  (`uBa19iT` / `kU2Cctg`). No table edit.
* `docs/healthcare-cities-scoring-analysis.md` explicitly places Raleigh in
  Tier 1 under the "within 30 minutes" threshold; `active-retirees` has it at #15.
  Both consulted before the list cards were chosen.

## 7. Two things the gate taught this build

**`build_sitemap.py` will not add a page.** It reads the existing `<loc>` list and
only refreshes dates, on purpose: "deciding page membership is an editorial
judgment; deciding a date is not." Chaining it is not enough. The `<url>` block is
an apply-script edit, and the generator stamps the date afterwards. A first pass
that chained the generator and skipped the edit produced a silent 99-URL sitemap
with no Raleigh in it.

**One superlative failure cascades into eight harness failures.** The first gate
run reported 9 failures. Eight were harnesses reporting "control run is clean"
false, and all eight were downstream of a single real failure: the phrase
"two restaurants on site" in a day card matched `BANNED_SUPERLATIVE`, whose
clause (a) is preposition + optional determiner + `(database|dataset|coverage|
site|list)`. "on site" reads as "on this site". Those harnesses run
`--only superlatives` because the comparison checks report to that group, so a
dirty control run fails every one of them. This is the same recognise-on-sight
shape the board records for a missing photo: **count the distinct causes, not the
failure lines.** Phrase rewritten to "two restaurants of its own".

## 8. Photos

Operator-supplied, cropped to spec, never upscaled. All three are downscales.

| Slot | Source | Original | Output | Subject |
| --- | --- | --- | --- | --- |
| `hero.jpg` | `pexels-curtis-adams-1694007-5900810.jpg` | 1920x1080 | 1600x899 | Downtown Raleigh skyline in autumn |
| `detail.jpg` | `kathleen-culbertson-hTUi268kPIw-unsplash.jpg` | 1920x2560 | 1600x2133 | Yates Mill on its pond |
| `lifestyle.jpg` | `gene-gallin-e82KFOxT9wg-unsplash.jpg` | 4032x3024 | 1280x1280 | North Hills, Main Street fountain |

The two portrait uploads were both a native 3:4 or taller, so the hard crop was
not hard this time: `kathleen-culbertson` is exactly 0.750 and needed only a
downscale, no cropping at all.

Credits use the no-link Unsplash/Pexels form already deployed in
`cities/prescott/profile.html` (`Photo &middot; Kyle Fritz / Unsplash`). Prescott
links out only on its CC BY Flickr image, where author, licence link and a
cropped notice are licence CONDITIONS. Unsplash and Pexels licences require no
attribution, so these are credited as house practice and carry no fabricated
deep link.

**Two captions were rewritten to match the photos actually supplied**, rather
than leaving copy describing a picture that is not there:
* The detail break was a caption about the Triangle as one metro. It is now about
  Yates Mill, because that is what the photo shows.
* The lifestyle banner was about greenway mileage and Umstead. It is now about
  North Hills as Raleigh's built-on-purpose walkable centre, which is what the
  photo shows and which carries the D6 tradeoff honestly. The greenway figures
  were not lost: they remain in the fast-facts card and two day cards.

### Not used

* `pexels-andrettibrown-30435314.jpg` (1920x1278). Confirmed Raleigh: Union
  Square with the PNC Plaza spire behind. Held back for one reason: the fenced
  statue flanked by cannons is the visual centre, and a reader who does not know
  that the Capitol's Confederate monuments were removed in 2020 may read it as
  one. It is almost certainly the Houdon Washington. Almost certainly is not a
  standard worth applying to a hero image. Usable if you can confirm the subject.
* `ross-joyner-2le8ULtLgSU-unsplash.jpg` (1920x2880). **Rejected on provenance.**
  No EXIF, no `Artist` or `ImageDescription` field, and the photographer's
  Unsplash profile lists no location beyond "USA" and no Raleigh work. I could
  not confirm the building is in Raleigh, and the skill's rule is that a stock
  photo with no EXIF and no findable location gets rejected rather than assumed.
  If you know the building, it is a good portrait frame and worth reinstating.

## 9. Repo docs I should have read at step zero, and what they changed

Four profile docs exist in `docs/` that the skill file's delegation table does not
name. Reading them after the first build was written found three real defects and
one stale doc.

**`docs/PROFILE_CONVENTIONS.md` (the post-"de-tell" pass). Two fixes.**
Its heading-emphasis rule is the important one: `<em>` is earned, not automatic,
and the neighborhoods heading is named explicitly as one that stays PLAIN. The
first draft read "Four ways to live in `<em>`Wake County`</em>`." Every deployed
profile checked (St. Louis, Indianapolis, Prescott) has that heading plain, so
this was a divergence from both the doc and the tree. It is now plain. Second: the
doc allows `<em>` on a healthcare heading only when it carries a real
honest-tradeoff beat, and Prescott shows the emphasis belongs ON the tradeoff
("Everyday care covered in town, `<em>`complex care down the hill`</em>`"). Raleigh's
now reads "...half an hour apart, and `<em>`neither one is in Raleigh`</em>`."

**`docs/CITATION-RECIPE-city-profiles.md`. One fix, one stale section.**
The fix: FAQ answers are supposed to name real numbers and cite scores, because
that is what gets lifted into an AI Overview, and deployed St. Louis does exactly
this ("healthcare scores a 10 of 10"). The first draft deliberately stripped every
score from the FAQ, reasoning from the skill file's "never display a /10". That
reasoning was wrong on this surface: the rule is about the STATS BAR, and the FAQ
is where the scores earn citations. Scores are back in FAQ answers 1, 3 and 4. The
stats bar remains score-free.

The stale section, boarded below: its "Build & file conventions" still says to hand
off `bentonville-hero.jpg` and `<city>-profile.html` for renaming at deploy.
`DEPLOY-CHEATSHEET.md` section 4 superseded that on July 14 and is explicit
("No `tulsa-hero.jpg` to rename by hand"). Same rot as the skill file, this time
inside the repo where a commit CAN fix it. It also names
`CityDatabase_Jun_9_v14.xlsx` as current, five versions behind.

**`docs/city-profile-template-spec.md`.** Section order confirmed and matched. Also
stale in places: it describes nine dimensions, Fraunces display type, and a
character-section pull-quote that `PROFILE_CONVENTIONS.md` removed. Not acted on.

**`docs/DEPLOY-CHECKLIST.md`.** A mid-session snapshot from the May cleanup, not a
standing checklist. Nothing to apply.

### Boarded from this build

* `CITATION-RECIPE-city-profiles.md` hand-off conventions contradict
  `DEPLOY-CHEATSHEET.md` section 4, and its DB filename is five versions stale.
  Two lines to fix, and it is inside the repo.
* The skill file's delegation table lists six owning docs and misses
  `PROFILE_CONVENTIONS.md`, which is the one that governs heading emphasis. Every
  build that reads only the table will get the emphasis wrong the same way.

## 10. The guide pages, re-derived by grep

Raised at review: guides are not landing pages, and we may not have been linking
cities to them. Both directions grepped on the live repo before answering.

**Guide page -> profile.** Well established, and not something this build
introduced:

| Page | city-cards linking direct to a profile | still on the `index.html?city=` redirect |
| --- | --- | --- |
| `wellness-blueprint.html` | 43 | 26 |
| `globetrotter-guide.html` | 44 | 24 |
| `urban-walkabout.html` | 38 | 23 |
| `active-frontier.html` | 32 | 29 |
| `value-navigator.html` | 25 | 17 |

182 direct links across the five guides. The Indianapolis commit converted
`wellness-blueprint.html` on the same basis. So converting Raleigh's three guide
cards follows the tree rather than inventing a policy.

**Profile -> guide.** Rare and not the pattern: across all 52 profiles the lists
section points at guide pages only four times (`urban-walkabout` twice,
`value-navigator` once, `active-frontier` once) against 152 links to topic pages.
Raleigh's three list cards point at topic pages only, which matches.

**Where the language was wrong:** the board, the ops log and section 5 of this doc
called all six converted pages "landing pages". Three of them are guides. Corrected
throughout: three topic landing pages, three guide pages.

If you would rather guides stay on the redirect, drop these three lines from
`apply-raleigh.py` and the build still gates clean:

```
             "wellness-blueprint.html",
             "urban-walkabout.html",
             "globetrotter-guide.html"):
```
