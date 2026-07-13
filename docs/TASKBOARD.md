# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 13, 2026 (reconciled against live repo; climate engine rebuilt and deployed)

**Verified live at last update:** 42 profiles, 18 comparison pages, 5 guides, 7 landing pages.
All 42 profiles carry a Visit block. Validator: 0 failures, 41 warnings.

---

## How to run chats

One job type per chat. Name chats so they are findable:

| Chat name pattern | For | Lifespan |
|---|---|---|
| `BUILD - <City>` | one city profile, end to end | dies when the city ships |
| `COMPARE - <A> vs <B>` | one comparison page | dies when it ships |
| `BATCH - <job>` | repo-wide scripted operations (retrofits, sweeps) | dies when the batch is pushed |
| `OPS - planning & tracking` | this board, decisions, methodology Qs, small one-off fixes | permanent home base |

Rules of thumb:
- A NEW city's Visit block + affiliate codes belong IN that city's `BUILD` chat.
- RETROFITTING existing profiles is a `BATCH` job, never woven into a single city build.
- If a chat shows a "conversation compacted" note, finish the current step, update this board, start fresh.

**Before every deploy:** `python3 tools/validate.py --local .`
**After every deploy:** `python3 tools/validate.py`
These read different things. `--local .` reads your working checkout: the code you are about to push.
Bare reads live GitHub: the code already deployed. A bare run BEFORE a deploy validates the old site
and returns a green light that says nothing about your changes.

---

## ACTIVE - batch / site-wide operations

- **Superlative warning cleanup** - 41 warnings, 0 failures. Two distinct jobs, do not mix:
  - **(a) ~11 dataset-scoped superlatives.** Claims ranked against our own data, which rot every time
    a city is added. Live: "best value in Florida" (sarasota-vs-tampa x2, tampa-vs-st-petersburg);
    "largest anywhere on this scorecard" and "widest home-price gaps of any pairing here"
    (fort-collins-vs-boulder); "highest of any pairing we have compared" (madison-vs-ann-arbor);
    "largest spread anywhere on this scorecard" (knoxville-vs-chattanooga); "most affordable cities
    in the Southeast" (value-navigator); plus arts-lovers and foodies landing pages. Re-anchor each
    to a figure or a named city, never to a rank within our own dataset. The validator prints two DB
    truth lines to check against (cheapest home: Paducah $185,000; priciest: Carmel-by-the-Sea $2,281,000).
  - **(b) ~30 per-profile warnings.** Ann Arbor (3), St. Louis (2), Santa Fe (2), Naples (2),
    Kansas City (2), Chattanooga (2), St. Petersburg, Scottsdale, Philadelphia, Miami,
    active-frontier (2), others. Bulkier and more repetitive than (a).
  - Run as a `BATCH` chat with `python3 tools/validate.py --only superlatives` output pasted in.
    NOT an OPS job.

- **Guide em-dash sweep** - 232 em-dashes in rendered text across all 5 lead-magnet guides:
  globetrotter-guide (71), wellness-blueprint (55), urban-walkabout (41), value-navigator (37),
  active-frontier (28). Profiles, comparison pages, landing pages and index.html are all clean.
  The guides were skipped by the earlier sweep, and `GUIDES_TOO = False` in `tools/validate.py` has
  been hiding them. **When the sweep ships, flip `GUIDES_TOO` to `True`** so the win is guarded.
  Until then PROFILE-FORMATTING.md says site-wide while practice says everything-but-guides.
  The doc and the practice must be made to agree.

- **Validator: add a climate check group** - the validator compares `index.html` city FIGURES against
  the DB but has never checked the CLIMATE blocks. They happen to match 99/99, but nothing enforces it,
  and the July 13 rebuild added three fields (`janF`, `snow`, `sun`) that live in `index.html` with no
  guard at all. Add a group asserting (1) all five original climate values match the DB per city,
  (2) `janF`, `snow`, `sun` present and non-null for all 99. Silent drift of exactly this kind produced
  the Boulder bug.

- **v1.3 template retrofit** - status NOT VERIFIED. The prior board listed dark-mode hardening, Deep Dive
  relocation, plain-quiz wording, and comment em-dash cleanup as NOT STARTED, but the profile markup no
  longer matches the greps that would confirm it either way. First task of the BATCH chat is to establish
  actual status against the canonical (`cities/st-louis/profile.html`), not to assume.

- **Closer-variety sweep** - status NOT VERIFIED, same reason. Originally: the ~12 Visit-block profiles
  all ended on "highlight reel." All 42 profiles now carry Visit blocks, so if this is still open the
  scope is 42, not 12. Confirm before scoping.

---

## ACTIVE - city profile builds

- **Next in queue:** San Antonio (unlocks Fort Worth vs San Antonio).
- Then: Savannah, Roanoke, Tulsa.
- Live profiles: 42. Fort Collins, Prescott and Knoxville all shipped since the last board update.

---

## ACTIVE - comparison pages

Live: 18. Shipped since last board update: Fort Collins vs Boulder, Knoxville vs Chattanooga,
Bend vs Boulder, Bloomington vs Lexington, Madison vs Ann Arbor, Madison vs Columbus, and others.

Unlocked and ready to build now (both cities live):
- **Knoxville vs Nashville**
- **Knoxville vs Asheville**
- **Arizona three-way cluster** (Prescott now live, so this is unblocked)

Unlocks pending a build:
- Fort Worth vs San Antonio (needs San Antonio)

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty)

---

## PARKED / BACKLOG

- Site-wide bolding pass (PROFILE-FORMATTING item 6, judgment-based, not batchable)
- Booking.com affiliate (Awin) - applied; deploy deferred until Expedia fully verified
- Pinterest save-rate optimization (ongoing; cadence + pin copy)
- `Ann Sun %` provenance: ~30 of 99 values are interpolated from the nearest NOAA station. Fine behind
  the 55% dealbreaker cutoff. Do NOT print these figures on a profile page without verifying that city.
- Weather weighting: picking a weather preference auto-sets `DC` to "Very Important" (weight 3) while
  nine other dimensions sit at 1, so climate is 25% of the match score. This is why Florida leads a
  "Mild Year-Round" search ahead of Santa Barbara. Working as designed, not a bug. Raising weather's
  influence is a product decision and needs testing against every quiz path.

---

## RECENTLY SHIPPED (rolling, trim as it grows)

- Jul 13, 2026: Climate engine rebuild. Four compounding faults fixed: the cold dealbreaker was
  calibrated against the wrong scale (Boulder, 33F and 88in of snow, passed a "no freezing winters"
  filter); the `Climate Mild YR` column was actually the dryness score and the grey-winter filter was
  wired to it (removing Naples and Miami while keeping Pittsburgh); `mild` and `warm_dry` were weighted
  averages, so a great summer cancelled a freezing winter; and a `length >= 5` guard was silently
  failing open and discarding the climate filter entirely. Added NOAA 1991-2020 normals to all 99
  cities. DB v16.4. Zero score churn. See SITE-OPERATIONS-LOG.md 2026-07-13.
- Jul 13, 2026: Wilmington DE, Indianapolis and St. Paul median-home corrections confirmed live in both
  DB and index.html. MEDIAN-HOME-LABEL-CONVENTIONS.md deleted. D2 rebuild cleared the suspect
  `$4,500-$5,500` range (the one remaining instance is La Crosse WI's genuine DB value).
- Jul 13, 2026: Visit-block rollout COMPLETE. All 42 live profiles carry a Visit block.
- Jul 9, 2026: Knoxville deployed; v1.3 canonical + docs deployed; St. Paul DB fix done.
