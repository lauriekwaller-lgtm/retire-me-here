# DEPLOY: Indianapolis, IN

**Built:** August 25, 2026
**Against:** `lauriekwaller-lgtm/retire-me-here` @ `5a989ae` (full clone, not shallow)
**Database:** `docs/CityDatabase_Jul_27_v19.1.xlsx`, sheet `City Database`, `header=1`
**Template base:** `cities/st-louis/profile.html`, pulled live from GitHub at build time
**Profile count after this deploy:** 52

---

## 1. Photos: in the zip, at final paths

All three ship INSIDE the zip at `cities/indianapolis/`, per DEPLOY-CHEATSHEET section 4.
Nothing to rename, no folder to create, no `mv` step. Unzip at the repo root and every
file lands where it belongs.

(The first cut of this bundle wrongly held the photos back as loose files, on a misread
of the "Images, and anything else a script cannot diff" subsection. That subsection
governs a photo REPLACING an existing one: it cannot go in the zip, because unzipping
over a pulled tree silently reverts anything that landed since, and it cannot be
patched, because a script cannot diff a JPEG, so dragging is all that is left. A new
city's photos do not exist in the repo yet, so they are new files like any other and
belong in the zip.)

| slot | subject | source | licence |
|---|---|---|---|
| hero 1600x899 | Monument Circle | Bryan Dickerson / Unsplash | Unsplash |
| detail 1600x2133 | Monon Trail bridge | Dmytro Sergiyenko / Wikimedia Commons | CC BY-SA 4.0 |
| lifestyle 1280x1280 | Garfield Park sunken garden | IndyTaylor / Wikimedia Commons | CC BY-SA 4.0 |

Both Commons files are **CC BY-SA 4.0 and both crops are adaptations**, so each credit
carries author, a link to the licence, an indication that the file was cropped, and, in
the footer block, a statement that the adaptation is offered under the same licence.
There are no `_TK` placeholders left in the file.

**Open item, cosmetic not legal.** The inline credits link the LICENCE but not the
Commons file page, because a source URL was not supplied and a guessed URL is worse than
none. CC BY-SA requires a link to the material only where reasonably practicable; author
plus licence link plus modification notice satisfies the licence as shipped. Paste the
two Commons file-page URLs and they become source links, matching
`cities/prescott/profile.html`.

**One missing photo produces SIX failures across THREE check groups, not three.** Worth
recognising on sight. `check_stray_artifacts` reports the three missing files under
LAYOUT; then `tools/test_stray_artifacts.py` and `tools/test_typography.py` both fail
their "control run is clean" assertion, because both stage a copy of the tree and run
`validate.py --only layout`, which is the group that owns the photo check. Nothing is
wrong with the harnesses or with typography. Put the photos in place and all six clear
together.

**Crop notes, recorded so a future refresh does not redo the analysis.** The hero is
locked to Monument Circle by resolution: at 2400x1600 a portrait crop yields 1200x1600
and would need a 33% upscale. The detail is a NATIVE 1600x2133 pixel cut from the
3264x2448 Monon original with zero resampling. The lifestyle banner is NOT rendered
square: `.lifestyle-banner` is `56vh` tall with `background-size: cover`, so on desktop
only the middle band of the 1280x1280 shows, while on a narrow phone the aspect is close
to 1:1 and nearly all of it shows. The Garfield crop is centred on the conservatory so
it survives both.

A Broad Ripple streetscape and a Canal Walk frame were both considered and rejected on
editorial grounds, not technical ones: the first carried a bar-promotion marquee reading
"$1 BUD LT" and was EXIF-dated 2013, the second was leafless March under flat grey light
and would have illustrated the winter objection in the "No if" column at the exact spot
the page makes its appeal.

## 2. Deploy sequence

```bash
git pull                                  # first, always
unzip -o indianapolis-bundle.zip          # profile.html + this doc + apply script
rm indianapolis-bundle.zip
python3 apply-indianapolis.py --check     # verify anchors, writes nothing
python3 apply-indianapolis.py             # writes; chains build_sitemap.py
python3 tools/validate.py --local .       # 0 failures, 0 warnings or STOP
rm apply-indianapolis.py                  # BEFORE git add
git status --short --untracked-files=all  # expect 14 paths (section 3)
git add -A && git commit -m "Indianapolis IN profile (52); 7 dead-end cards now link direct; index.html quiz neighborhood figures and Indiana tax rate corrected; board + ops log"
git push
```

## 3. Files this deploy touches

**New (in the zip, final paths, nothing to rename):**

| path | note |
|---|---|
| `cities/indianapolis/profile.html` | the profile |
| `cities/indianapolis/hero.jpg` | 1600x899 |
| `cities/indianapolis/detail.jpg` | 1600x2133 portrait |
| `cities/indianapolis/lifestyle.jpg` | 1280x1280 square |
| `docs/DEPLOY-indianapolis.md` | this file |

**New (in the zip):** `cities/indianapolis/hero.jpg`, `detail.jpg`, `lifestyle.jpg`

**Existing, edited only by `apply-indianapolis.py` (19 anchors, 12 files):**

| file | edit |
|---|---|
| `index.html` | `PUBLISHED_PROFILES` entry |
| `index.html` | 4 quiz neighborhood figures (judgment call, section 5) |
| `index.html` | 2 stale Indiana tax figures (judgment call, section 5) |
| `sitemap.xml` | `<url>` block; `build_sitemap.py` then stamps lastmod from git |
| `top-cities-for-healthcare.html` | redirect card to direct link |
| `top-cities-for-active-retirees.html` | redirect card to direct link |
| `top-cities-for-sports-fans.html` | redirect card to direct link |
| `best-places-to-retire-avoid-natural-disasters.html` | redirect card to direct link |
| `wellness-blueprint.html` | redirect card to direct link |
| `best-places-to-retire-on-a-budget.html` | `coming-soon` promoted to live card |
| `cities/kansas-city/profile.html` | reciprocal Related Cities link |
| `tools/validate.py` | `check_pillar_links` hardcoded 51 to 52 |
| `docs/TASKBOARD.md` | header block + build-queue line |
| `docs/SITE-OPERATIONS-LOG.md` | change-log entry |

The board said "Indianapolis IN (4 pages)". Grep said five live redirect cards plus a
`coming-soon` card plus the Kansas City reciprocal: seven surfaces, not four. The
board's four is defensible if it counted topic landing pages only.

## 4. The brief this was built to

Read from the DB row before any copy was written. Home $234,000 · Monthly
$4,300&ndash;$5,400 · Budget Range 1 · D1 8, **D2 9**, D3 8, D4 7, D5 6, D6 5,
**D7 3**, D8 5, D9 7, D10 7.

One dimension reaches the pillar floor of 9, so under `MIN_PILLARS 3` the pillar
cluster is **Budget 9 / Airport 8 / Healthcare 8**. This is the MULTI-STRENGTH
advisory case: lead with the standout, give the cluster real weight. All three are
established in the hero tagline and again in the opening character paragraph.

**D7 Outdoor 3 is the single hard flag** and leads the "No if" column, per the rule
that the flagged weakness goes first. Central Indiana is flat, there is no coast and
no mountains, and that is the honest reason to skip this city.

Stat cards carry no bare N/10. Slots 3 and 4 use the two strongest remaining
dimensions as labels (Airport D1 8, Healthcare D3 8) with concrete proof points as
values: `IND, 12 mi` and `IU Health`.

List placement was taken from the scoring-analysis docs, not editorial judgment:
active retirees Tier 1 (FI 8.0, rank 3), healthcare Tier 2, sports fans Tier 2. The
city is carded on five landing pages; the profile shows four, led by the defining
strength (budget), and drops natural disasters, which is the weakest of the five and
a negative-space claim.

Neighborhood Reality Check is warranted and present: citywide $234K against Carmel
(~$525K), Zionsville (~$689K), Fishers (~$425K) and Broad Ripple / Meridian Kessler
($400&ndash;500K), stated as $425K&ndash;$700K.

## 5. Judgment calls, flagged so they can be overridden

**a. Four quiz neighborhood figures in `index.html` were wrong and are corrected
here.** All four Indianapolis `neighborhoods[]` cards read `~$234K`, the citywide
figure pasted into four suburbs, while `scoreNotes.D2` three lines below gave the
real values. No check reads that array, which is why it sat. The new profile makes
the contradiction reader-visible. Delete edits 2a&ndash;2d from the apply script to
board this instead.

**b. Two stale Indiana tax figures in `index.html` are corrected here.** The D5 note
and the cons array said a flat 3.05% with Social Security "partially exempt". The
DB's `State Tax Facts` sheet (authoritative per D5-TAX-METHODOLOGY) and the
validator-checked `TAXFACTS` array both say **2.95% and fully Exempt**, and
Bloomington's own D5 note 1,430 lines up the same file already used the correct
figures. Delete edit 3 to board this instead.

**c. The healthcare card shows `8/10`, and the skill file says never display a /10.**
The deployed canonical `cities/st-louis/profile.html` shows `10/10` in exactly this
slot, and PROFILE-FORMATTING names St. Louis as the canonical reference. Per the
skill's own "the repo doc wins and this file is the bug" rule, the canonical was
matched. The skill's hard rule, no bare N/10 in the **stats bar**, is honoured. This
is a real disagreement between `retiremehere-city-profile/SKILL.md` and the deployed
canonical and should be resolved in one of the two.

**d. No "Compare these" CTA band.** There is no Indianapolis comparison page. 19 of
the 51 existing profiles are in the same position and none carries the band.

**e. `fix_nav_breakpoint.py` is deliberately NOT chained.** A profile built from the
live canonical already carries the 1000px nav block. Running it would be a no-op, and
chaining a no-op teaches the wrong habit. `build_sitemap.py` IS chained, and it does
accept `--repo` (verified at `5a989ae`; an earlier note said otherwise).

## 6. Gate

`python3 tools/validate.py --local .` on a fresh full clone with this package applied
and placeholder photos in place: **0 failures, 0 warnings.** Baseline before the
build was also 0/0, so the delta is attributable.

Two real defects were caught by the gate during the build and fixed, recorded because
they will recur: the phrases **"on this list"** and **"on this site"** are banned
dataset scopes and both were written into the first draft by someone who had read the
superlative rule an hour earlier. They also broke eight harnesses, because those
harnesses run `--only superlatives` against a full copy of the tree and their control
runs stopped being clean. Eight harness failures, one root cause.

## 7. Not fixed here, boarded instead

`pick-and-compare.html` line 952 still tells readers that eight cities including
Indianapolis "use retiree-target neighborhood data rather than citywide figures and
are shown as ranges". MEDIAN-HOME-METHODOLOGY v1.2 retired that carve-out and
BUDGET-METHODOLOGY section 4 calls the same sentence "its fossil, struck 2026-07-13".
It is a live false statement about a number every profile displays, but it is a
tool-page copy edit, not part of a city build.

---

*RetireMeHere.com · DEPLOY-indianapolis.md · August 25, 2026*
