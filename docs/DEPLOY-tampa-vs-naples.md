# Deploy — Tampa vs. Naples comparison (August 18, 2026)

One commit. Two NEW files in the zip, nine existing files edited by
`apply-tampa-vs-naples.py`. Built from a live tarball of main pulled
August 18; validator green at 0 failures, 0 warnings on that clone before
anything was written, and again after.

## Why this page exists

The Aug 17 Search Console read named exactly one genuine content gap:
"tampa vs naples for retirees", 44 impressions, position 35, no page. It is
the only missing-page finding in that export.

## Deploy sequence

```bash
git pull
unzip -o tampa-vs-naples-bundle.zip
rm tampa-vs-naples-bundle.zip
python3 apply-tampa-vs-naples.py
python3 tools/validate.py --local .      # must read 0 failures, 0 warnings
rm apply-tampa-vs-naples.py              # BEFORE git add
git status --short --untracked-files=all # expect 11 paths (2 new, 9 modified)
git add -A
git commit -m "Tampa vs. Naples comparison page (24); hub card, both profile CTAs, sitemap; 3 garbled strings + 5 stale highlight figures"
git push
```

## Files

**New (in the zip, final paths):**
1. `tampa-vs-naples-retirement.html`
2. `docs/DEPLOY-tampa-vs-naples.md` (this file)

**Edited by the apply script:**
3. `sitemap.xml` (new entry, lastmod 2026-08-18)
4. `compare-retirement-cities.html` (hub card in the Florida Gulf Coast
   section, ItemList position 24, CollectionPage dateModified to 2026-08-18)
5. `cities/tampa/profile.html` (third matchup CTA; "two real rivals" prose
   reworded rather than the count bumped)
6. `cities/naples/profile.html` (same)
7. `docs/TASKBOARD.md`
8. `docs/SITE-OPERATIONS-LOG.md`
9. `tampa-vs-st-petersburg-retirement.html` (text repair, see below)
10. `index.html` (text repair + stale figure)
11. `pick-and-compare.html` (same stale figure, mirrored surface)

Items 9 to 11 carry Sections B and C. Two flags at the top of the apply
script control them independently: `INCLUDE_TEXT_REPAIRS` (three garbled
strings) and `INCLUDE_FIGURE_REPAIRS` (five stale price figures). Set either
to False to drop that section; the comparison page itself is unaffected.

## Scores, read from docs/CityDatabase_Jul_27_v19.1.xlsx

Tampa 10-6-10-2-9-6-6-7-6-8 against Naples 8-5-10-2-9-5-6-10-9-8.

Six marks, all DB-verified. Tampa takes typical home value ($380,000 vs.
$549,000), retiree budget, budget tier (2 of 5 vs. 3 of 5), and D1 at a
two-point gap. Naples takes D8 (10 vs. 7) and D9 (9 vs. 6), both three-point
gaps. D2 and D6 are one-point gaps: unmarked in the table, reported in prose
with both numbers, never described as a row anyone "takes". Five outright
ties, including healthcare at a perfect 10 in both cities.

Warm winters is 9 against 10. That is a climate row, so it keeps the context
rule rather than the two-point rule: no mark, inline context instead
(January mean 61F against 65F).

## Judgment calls

- **Title breaks the convention, deliberately.** "Tampa vs. Naples for
  Retirees", where the other twenty-three say "for Retirement". The Aug 18
  vocabulary pass left existing titles alone to protect rankings; this page
  has none to protect, so it is a free test of the phrasing the query
  actually uses. The slug still carries "retirement", so both tokens reach
  Google. Revert by editing the title, og:title, twitter:title and the
  schema headline together.
- **Naples' own airport described as private and charter aviation.** Sources
  disagree on whether it currently carries scheduled service; softened to
  qualitative language rather than guessing, per the standard.
- **Curated pills:** Sarasota vs. Tampa and Tampa vs. St. Petersburg
  (shared city, Tampa), Naples vs. Sarasota and Naples vs. Fort Myers
  (shared city, Naples), plus the picker and the hub. Four is the ceiling
  and this pairing genuinely has four siblings.
- **og:image:** Tampa hero, lead city per slug order.

## Colour claims verified before publishing

- Tampa to Naples: about 165 miles on I-75, two and a half to three hours.
- TPA: six miles west of downtown, nonstop service to roughly 100
  destinations.
- RSW: about 35 miles north of Naples, roughly 45 minutes outside of season;
  over eleven million passengers in 2025.
- NCH "#1 hospital in Florida multiple years running" and the Naples 97th
  percentile safety line both match the wording already live on the Naples
  profile and on naples-vs-sarasota.

## Text repairs shipped alongside (Sections B and C)

**Section B, three garbled strings.** All cut-scar text from the superlative
scrub, all rendering to readers:

- `tampa-vs-st-petersburg`, tradeoff 3: "with our databSt. Pete's Walk Score
  of 94 leads Florida"
- same page, FAQ 4: "and os Walk Score of 94", present in BOTH anchors, the
  visible copy and the FAQPage schema
- `index.html`, Naples cons array: "typical home value $549Konthly costs
  $6,500+"

**Section C, five stale price figures** (Tampa's sits in Section B with the
other Naples edit). Every one is mirrored byte for byte in
`pick-and-compare.html`, so both surfaces move in the same run;
`check_highlight_surfaces` fails if they ever disagree.

| Highlight on | Said | DB | Now |
|---|---|---|---|
| Tampa | Naples $585K | $549,000 | $549K |
| Chattanooga | Asheville $462K | $464,000 | $464K |
| Corpus Christi | Pensacola $264K | $269,000 | $269K |
| New Orleans | own citywide median $250K | $248,000 | $248K |
| Tulsa | own citywide median $194K | $223,000 | $223K |

Tulsa is the largest miss, and its own profile already carried $223K in
rendered copy; the $194K survived only in a build comment there and live on
the home page and the picker.

## Correction to an earlier diagnosis, and the P2 it opens

The Tampa figure was first written up as `cross_city()` skipping a figure
that names another city. That is wrong, and the wrong version is recorded in
the ops log rather than deleted, so the next session does not go reading
`cross_city()` and find it innocent.

What actually happens: `HL_HOME_FIG` only matches a dollar figure anchored to
a home-value noun ("typical home value", "median home"). A bare "$585K" is
never a candidate, so the cross-city gate is never reached. Measured across
all 198 highlight strings, that gate is currently inert: zero anchored
figures are being skipped for naming another city.

The audit that followed found 32 dollar figures in highlight strings read by
neither pattern. Most are correctly out of scope. Five were price claims and
all five were wrong, which is the table above.

The two own-city cases are the ones that generalise: "citywide median $194K"
says *median* without saying *home*, so nothing about it is cross-city. The
fix, on the board as P2 and not shipped here:

1. extend `HL_NOUN` to catch a bare "citywide median $X"
2. resolve a cross-city figure against the NAMED city's row instead of
   skipping it, keyed on (City, ST), because a name-only lookup is how the
   two Wilmingtons collided before

Neither ships without a planted-error harness.

## After deploy

Request Indexing for
`https://retiremehere.com/tampa-vs-naples-retirement.html`.

Grade on impressions and average position on "tampa vs naples for retirees",
not clicks, and not before October.
