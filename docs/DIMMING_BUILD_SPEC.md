# Build Spec — Quiz Option Dimming (deferred feature)

## What this feature does
When a user picks one or more **regions** on the location step, options on a later
preference question that **cannot be satisfied by any city in the selected region(s)**
should appear **dimmed + labeled "not available in selected regions"** — visible, not
hidden, not clickable. This answers the user complaint: *"why am I offered beach/cool-mountain
when I only picked the Midwest?"*

## STATUS: deferred on purpose
Defer the CODE. Do NOT defer the DATA discipline below — that's the only time-sensitive part.
Building this later against complete data is easy; retrofitting data onto dozens of
already-scored cities is the painful path we're avoiding.

---

## The data it depends on (capture correctly on EVERY new city, starting now)

Both fields ALREADY EXIST on every city object in index.html. Nothing new to score.
The only requirement is keeping them clean:

### 1. `setting: [...]` array  (terrain)
- Lives on each city object, e.g. `setting: ["Mountain", "Lakeside"]` (see Asheville ~line 2129).
- NOT user-facing — the only misspelling risk is your own data entry when adding a city.
- MUST use these SIX exact strings, spelling/spacing/slashes identical every time:
  - `"Beach / Coastal"`
  - `"Mountain"`
  - `"Lakeside"`
  - `"Forest / Green"`
  - `"Urban / Metro"`
  - `"Desert"`
- A city can have multiple (comma-separated in the xlsx `Setting` column).
- Wanting a 7th value is a real decision — it changes dimming options for every region. Flag it, don't just type it.

### 2. `climate: { W, H, M, HUM, HEAT }` object
- Already captured on every city. No change needed.
- NOTE: the climate→weather-option mapping is an OPEN QUESTION (see below) — must be
  resolved before building dimming for the WEATHER question specifically.

---

## The floor rule (this is what makes dimming honest)
A region's dimming is only truthful once that region has enough published cities.
With few cities, "no beach available" really means "Laurie hasn't published a beach
city there yet" — a roadmap fact masquerading as a geography fact.

**Rule: only run dimming in regions with 10+ published cities. Below the floor, leave
all options lit.** Build this as a per-region check, NOT a global city count. The feature
then ships ONCE and turns itself on region-by-region automatically as each region fills out.

As of May 2026 (~27 published), region counts in the DB:
- Healthy enough to dim today: Southeast (26), Mountain West (20)
- Just at/below floor: Midwest (~10), Mid-Atlantic (~11), South/Texas (~11)
- Too thin, stay lit: Pacific Coast (8), Southwest/Desert (7), New England (4), Plains (3)

---

## Multi-region rule
When a user selects multiple regions, an option is LIT if **any** selected region can
satisfy it (UNION, not intersection). Pick Midwest + Pacific Coast → Beach lights up
because the Pacific side has it.

---

## Where it goes in code
- Region selection is stored in `quizState.regions` (array). See `renderRegion` / `toggleRegion`.
- Region→state mapping is `REGION_MAP`. The 9 buckets are:
  Pacific Coast, New England, Mountain West, Mid-Atlantic, Southwest/Desert,
  Southeast, Plains States, Midwest, South/Texas.
- The TERRAIN question: confirm whether the "Next — Setting →" button (weather step)
  leads to an actual setting/terrain question. If it exists, that's the natural place
  to dim setting options against `setting:` data — clean, because terrain is filter-like.
- The WEATHER question (`renderPriorities`, `CLIMATE_OPTIONS`, keys: mild/warm_dry/warm/
  seasons/cool/none) is SCORED, not hard-filtered. Dimming here is less clearly correct
  (see open question). The shipped inline clarifier note may be sufficient for weather.

## Dimming logic (pseudocode, terrain version)
```
const SETTINGS = ["Beach / Coastal","Mountain","Lakeside","Forest / Green","Urban / Metro","Desert"];
function availableSettings(selectedRegions) {
  const regions = selectedRegions.length ? selectedRegions : ALL_REGIONS;
  const avail = new Set();
  for (const region of regions) {
    const pool = CITIES.filter(c => regionOf(c.state) === region);
    if (pool.length < 10) { SETTINGS.forEach(s => avail.add(s)); continue; } // floor: all lit
    pool.forEach(c => (c.setting || []).forEach(s => avail.add(s)));
  }
  return avail; // any SETTING not in this set → dim + label
}
```
CSS already exists: `.region-btn.eliminated` (terra) and `.region-btn.partial` (gold) —
reuse or mirror this styling for dimmed options.

---

## OPEN QUESTION to resolve before building (weather dimming only)
What exactly makes a city "satisfy" each weather option? i.e. when a user picks
"Cool / Mountain", which climate-score condition (on W/H/M/HUM/HEAT) counts a city as a match?
This logic lives in the scoring code where `quizState.climateChoice` is consumed.
An earlier attempt to guess these thresholds produced clearly-wrong results
(e.g. "Plains States has zero achievable climates"), so DO NOT guess — read the real
mapping from the scoring function, then derive the per-region available-weather table from THAT.
Terrain dimming has no such open question; `setting:` strings map directly.

---

## Build order when ready
1. Confirm whether a setting/terrain quiz step exists.
2. If yes → build terrain dimming first (cleanest, data is direct-match).
3. For weather dimming → first resolve the OPEN QUESTION mapping, then build.
4. Apply the 10+ floor and UNION rule to both.
5. Dimmed = visible, dimmed, not clickable, with label "Not available in selected regions".
