# RetireMeHere — City Profile Build SOP

**This doc is the source of truth for building a city profile.** The
`retiremehere-city-profile` skill is a pointer to this file and nothing more.

Adopted August 26, 2026, consolidating the skill file plus four profile docs that
had drifted apart. Written because every profile defect this month traced to a
restated fact going stale in a copy, not to anyone misunderstanding the rule.

---

## 0. The rule this doc lives by

**Own or delegate. Never restate.**

A fact belongs in exactly one file. Where another doc owns a subject, this file
points at it and says nothing else about it. When you find yourself about to
summarize what another doc says "for convenience," stop: that convenience copy is
the defect. It has happened four times.

### What this doc owns

Nothing else in the repo carries these, which is why they are here:

- The brief: pillar and support thresholds, hard flags, the MULTI-PILLAR and
  MULTI-STRENGTH shapes
- Where a score may and may not be displayed
- Photo specs and the sourcing standard
- The live-canonical rule and the known stale-template regressions
- Build order, and the file list a new profile changes

### What this doc delegates

| Subject | Owner |
| --- | --- |
| Formatting, bolding, NRC callouts, em-dash policy | `PROFILE-FORMATTING.md` |
| Heading emphasis, pull-quote and dropcap conventions | `PROFILE_CONVENTIONS.md` |
| FAQ format, score citation, what makes a profile citable | `CITATION-RECIPE-city-profiles.md` |
| Hand-off shape, deploy sequence | `DEPLOY-CHEATSHEET.md` section 4 |
| Median home figures and NRC warrant | `MEDIAN-HOME-METHODOLOGY.md` |
| Monthly budget derivation | `BUDGET-METHODOLOGY.md` |
| What D5 is and is not | `D5-TAX-METHODOLOGY.md` |
| Landing-list tier placement | the seven `*-cities-scoring-analysis.md` |
| Comparison page structure | `COMPARISON-PAGE-STANDARD-v2 .md` |
| What is in flight, what is parked | `TASKBOARD.md` |

Two docs look like owners and are not. `city-profile-template-spec.md` still
describes nine dimensions and a character-section pull-quote that
`PROFILE_CONVENTIONS.md` removed. `DEPLOY-CHECKLIST.md` is a mid-session snapshot
from the May cleanup. Read them for history; do not build from them.

This table is not a complete list of docs. Before writing, list `docs/` in the live
repo and open anything profile-shaped, whether or not it appears above. On August 25
a build read the six subjects its table named, missed `PROFILE_CONVENTIONS.md`
entirely, and shipped two heading defects the gate cannot see.

---

## 1. Non-negotiable data rule

Dimension scores (D1-D10), healthcare grade, budget tier, Monthly Est and Median
Home come ONLY from the CityDatabase xlsx. Never from web research, never from a
brief, never from session memory. Read the DB row before writing anything. If the
DB is not available, STOP and ask.

Research is allowed only for supporting color: price spot-checks, hospital
rankings, airport routes, park acreage.

```python
import pandas as pd
df = pd.read_excel(path, sheet_name='City Database', header=1)   # header row 2
df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
row = df[(df['City'] == city) & (df['ST'] == state)]             # BOTH, always
```

Filter on City AND ST. Name-only lookup silently collides Wilmington DE with
Wilmington NC. The same applies to `AFFILIATE-CODES.csv`.

**Check the DB filename; do not assume it.** It is versioned and it moves. On
August 26 2026 it was `docs/CityDatabase_Jul_27_v19.1.xlsx`, while the skill file
said `v17` and a project brief said `v17`. List `docs/` and read what is there.
Note the trap: the date in the filename is not the version date, so `Jul_27` has
covered v17 through v19.1.

**There is no `Highlight` column.** Older docs told builds to parse a distinctions
checklist out of one. No sheet in v19.1 has it. The per-city `highlight:` strings
live in `index.html` and are editorial copy, not data.

---

## 2. The brief

Emphasis follows the scores, not whichever attribute is easiest to write a lyrical
sentence about. This step exists because of the Miami case: a profile latched onto
multilingualism while the data ranked four dimensions equally high.

| Band | Threshold | Treatment |
| --- | --- | --- |
| Pillar | 9 or above | Must appear in the hero tagline AND the opening character paragraph |
| Support | 7 to 8 | Real weight in the character section |
| Hard flag | 4 or below | Must lead the "Skip [City] if" column |

Constants: `PILLAR_FLOOR` 9, `MIN_PILLARS` 3, `SUPPORT_FLOOR` 7, `WEAK_CEIL` 4.

**MULTI-PILLAR.** Three or more dimensions at 9+. Both the hero tagline and the
opening character paragraph must gesture at the cluster. Lead with the cluster.

**MULTI-STRENGTH (soft).** One standout plus a tight cluster below the pillar floor
(St. Louis 10/8/8/8, Chattanooga 10/9/8/8, Casper 10/8/8/8, Raleigh 10/9 over a
four-way 7). Lead with the standout, but give the cluster real weight so the profile
reads as depth rather than one trick.

**Honest counterweight.** Never omit a hard-flagged weakness, and lead that column
with the one that actually binds the reader's life. This is where credibility lives.

Derive distinctiveness from the scored dimensions plus `Type`, `Setting`,
`Character` and `D4 Resil. Rationale`.

---

## 3. Where a score may appear

Not "never." It is per-surface, and getting this wrong in either direction has
shipped defects.

| Surface | Show a /10? |
| --- | --- |
| Stats bar, all four cards | **No.** Never a bare "9/10" |
| Body prose, fit columns, neighborhoods | **No.** Translate to a verifiable fact |
| Healthcare card grade | **Yes.** Deployed `cities/st-louis/profile.html` shows 10/10 |
| FAQ answers in the JSON-LD | **Yes, and it is the point** |

The FAQ row is not a loophole. `CITATION-RECIPE-city-profiles.md` is explicit that
FAQ answers naming real numbers and scores are what gets lifted into an AI Overview,
and deployed St. Louis writes "healthcare scores a 10 of 10" for that reason. A build
that strips scores from the FAQ to honor a stats-bar rule has applied the right rule
to the wrong surface. That happened on the Raleigh build.

Where the answer is No, translate the score into a concrete, externally-verifiable
proof: a CMS star rating, a named ranked hospital, "no state income tax", a drive
time. Prescott's healthcare card uses a bed count because that is the honest proof
for a hospital that is not nationally ranked, not because a grade is banned.

**Stat cards.** Four cards. Home Value and Monthly Budget are fixed dollar figures.
The other two use strong dimensions as LABELS with a short concrete proof point as
the value. Score decides which dimension earns a card; a fact fills it.

---

## 4. Build from the LIVE canonical

Pull it fresh from GitHub every time. Never from a local or project-knowledge copy.

```
https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main/cities/st-louis/profile.html
```

St. Louis is the canonical named in `PROFILE-FORMATTING.md`. It is an NRC city, so
it carries a Neighborhood Reality Check callout. Remove the callout unless the city
you are building is itself on the current NRC list, and strip the unused
`.reality-check` CSS with it, or the profile registers as an NRC city in the roster
grep. Watch for shared `@media` blocks when stripping: on the Raleigh build the
`.lists-grid-four` mobile rule lived inside the reality-check media block.

Known regressions that appear when an old template is used, and that must be absent
from every hand-off:

- A `DOMContentLoaded` listener auto-opening a Deep Dive guide form on load. Removed
  site-wide. Forms open ONLY on click.
- A missing sticky chip nav (`<nav class="section-nav" id="sectionNav">`).
- Back-to-top buttons missing or duplicated. Exactly one
  `<div class="back-to-top-wrap">` per major section. When placing by text anchor,
  make the anchor class-qualified and unique.

Three structural defaults a live pull inherits and that must survive unchanged:

- The forced-dark hardening `@media (prefers-color-scheme: dark)` block at the end of
  the `<style>`. It protects the warm-cream design in Android Chrome force-dark,
  Samsung Internet and in-app webviews, which bypass `color-scheme: light`.
- The Deep Dive email-capture block in the LOWER cluster, after Related Cities and
  before the Visit block and Quiz CTA. Do not move it up near the stats bar.
- Plain "the quiz" copy with no question count anywhere.

---

## 5. Build order

State upfront, at the start of each city, exactly which files will change.

1. Confirm the DB is present and read the row. If absent, stop and ask.
2. Derive the brief from the DB row using section 2.
3. Pull the live canonical St. Louis profile as the structural base.
4. Write the profile against the brief.
5. Apply `PROFILE-FORMATTING.md` and `PROFILE_CONVENTIONS.md`. Open both; do not
   re-derive them here. Zero em-dashes from the first draft.
6. Add the Visit block, after the Deep Dive block and immediately above the
   `<!-- QUIZ CTA -->` marker. Affiliate codes from `AFFILIATE-CODES.csv`, keyed on
   city AND state.
7. Cross-check lists-section placement against the relevant
   `*-cities-scoring-analysis.md` rubric. Those rubrics carry explicit thresholds and
   "considered but not included" reasoning; a city absent from a list is often absent
   on purpose.
8. Run the gate on a fresh clone with the package applied.
   `python3 tools/validate.py --local .` at 0 failures, 0 warnings. Not "should."
9. Hand off in the shape `DEPLOY-CHEATSHEET.md` section 4 specifies.

---

## 6. Photos

- hero 1600x899
- detail 1600x2133 (portrait)
- lifestyle 1280x1280 (square)

The portrait is usually the hard one to source; most city stock is shot landscape,
and cropping a wide skyline to 3:4 leaves a column of sky. Ask for it first.

Photos cannot be sourced or licensed by an assistant; the operator supplies them.
Crop to spec, never upscale more than about 10%, and verify the subject is actually
the city being built. Check EXIF: a Wikimedia or LOC file usually carries `Artist`
and `ImageDescription` fields that settle both authorship and location. A stock photo
with no EXIF and no findable location gets rejected rather than assumed.

**Write the caption to the photo, not the photo to the caption.** If the supplied
lifestyle image does not show what the banner copy describes, rewrite the copy. On
the Raleigh build the banner described greenway mileage and the photo showed a
shopping street; the copy changed.

Attribution is a licence condition, not a courtesy. CC BY needs author, licence link,
and an indication that the file was cropped. CC BY-SA needs all of that plus a
same-licence statement for the derivative. Unsplash and Pexels require no
attribution; credit them anyway as house practice, by name and platform, with no
fabricated deep link. Match `cities/prescott/profile.html`. Never guess an author's
name; flag it as the one open item instead.

---

## 7. Files a new profile changes

- `PUBLISHED_PROFILES` in `index.html`. A flat map of `'City_ST'` to profile path,
  nothing more. A DIFFERENT map further up the file holds `hospitalRating` and
  `scoreNotes` and is usually already populated for an unpublished city. Read the
  live file before editing either.
- `sitemap.xml`. `build_sitemap.py` refreshes dates only and will NOT add your page:
  deciding page membership is an editorial judgment. Insert the `<url>` block as an
  apply-script edit, then chain the generator. Never run it on a shallow clone.
- `tools/validate.py`. `check_pillar_links` hardcodes the profile count on purpose,
  so a profile that stops being read fails loudly. Bump it every build.
- Cards on any page where the city is not already linked direct. A city with a
  `coming-soon` card must be promoted in the same commit or `check_cards` fails.
  Guide pages are not landing pages, but their city cards do link straight to
  profiles; re-derive both by grep rather than trusting a queue.
- `docs/TASKBOARD.md`, always. The board asserts a profile count and `check_docs`
  compares it to reality.
- `docs/SITE-OPERATIONS-LOG.md`, a change-log entry.

Every one of these already exists, so every one is edited by `apply-<city>.py` and
never shipped in the zip.

**Apply-script discipline.** Verify every anchor across every file in a first pass
before any write; a moved anchor stops the script rather than half-applying. Give
each edit an explicit sentinel: an edit that INSERTS rather than substitutes leaves
its anchor intact inside the replacement, looks pending forever, and duplicates on a
second run. Run the script twice; the second run must be a no-op.

---

## 8. Verify before declaring done

`<strong>` balance, JSON-LD parse, routing, zero em-dashes in rendered content, no
placeholder token left in the file, and the gate at 0/0 on a fresh clone. Note
judgment calls inline so they can be overridden. Review happens once.

Two habits the gate rewards:

**Count causes, not failure lines.** One missing photo produces six failures across
three check groups. One dataset-scoped superlative produced nine, eight of them
harnesses reporting a dirty control run. Find the cause before fixing anything.

**Grepping one string is not enumerating a subject.** A sweep built by grepping a
single figure misses every surface that phrases the same fact differently, and every
surface that is not shaped like the ones you were looking for. Enumerate the subject.
