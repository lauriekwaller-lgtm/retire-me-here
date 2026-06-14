# Deploy — Florida pillar page (June 2026)

THE FRONT DOOR. First head-term page on the site: targets "best places to
retire in Florida" and funnels down into all 8 profiles + 6 comparisons,
which is exactly what makes it non-thin. One commit, three files.

## Files
1. best-places-to-retire-in-florida.html → repo root (NEW)
   slug chosen to match the head term exactly.
2. compare-retirement-cities.html → repo root (adds a one-line callout under
   the Florida Gulf Coast header pointing up to the pillar)
3. sitemap.xml → repo root (55 → 56)

## After deploy
- Request Indexing: https://retiremehere.com/best-places-to-retire-in-florida.html
- This is the page to watch in Search Console. It is aimed at a
  high-volume head term, so it will take longer to rank than the
  comparisons did, but it is the one with real upside.

## What's on the page
- Hero + intro that states the two universal Florida facts once (no income
  tax; every city is a hurricane city ~$7,136/yr) so individual sections
  don't have to repeat them.
- An 8-city sortable-by-eye table (home value high to low) linking each
  city to its profile, with Budget/Healthcare/Walk/Safety/Resilience scores
  and a one-line identity.
- "Start with what you actually need" — 6 cards (value, healthcare,
  walkability, safety, arts, lower storm risk), each naming the cities the
  SCORES point to and linking to a profile or comparison. Every pick was
  verified against the database, not asserted.
- A teal caveat card: the honest hurricane-cost section (1-3 of 10
  resilience across the board), named storms, the insurance/flood-map/
  evacuation triad.
- All 6 comparison links, grouped Gulf Coast + oldest-city matchup.
- 5-question FAQ (best place, cheapest, income tax, least hurricane risk,
  Gulf vs Atlantic) — all answers sourced from the scores.
- Schema: Article + ItemList (8 cities) + FAQPage.

## Build integrity notes
- Built from the live hub shell (head/nav/footer/CSS/scripts) so it matches
  the rest of the site exactly; GA4 present; dropdown nav works.
- New CSS classes reuse existing design tokens (--teal, --terra, --sand-dk,
  etc.); no new colors introduced.
- SITEMAP + HUB CAUTION HANDLED: I first built these on a stale earlier
  pull (looked like 54 URLs), caught the discrepancy, re-pulled the live
  files (confirmed 55 URLs + 10 hub cards, i.e. the St-Aug-vs-Pensacola
  batch IS deployed), and rebuilt both edits on the true current state.
  Final sitemap = 56, no duplicates; hub = 10 cards + the new callout.
- 0 em dashes, all figures DB-verified, all 14 internal links resolve to
  pages that are live now.

## Optional follow-on (not in this commit)
- A nav-menu entry for the pillar (e.g. under "Top Cities For…" or a new
  "Best of [State]" item) would make it reachable sitewide, not just via
  the hub callout and sitemap. Worth doing once you decide whether more
  state pillars are coming (Carolinas, Southwest) — if so, a "Best of
  [State]" dropdown is the clean pattern. Say the word and I'll wire it.

## Strategic note
This is the model for every future region. The playbook that built Florida
(profiles -> comparisons -> pillar) is now proven end to end and repeats
cleanly: pick a region with anchor cities, build 3-5 profiles, add the
obvious comparisons, crown it with a "best places to retire in [state]"
pillar. The Carolinas and the Southwest already have published anchors.
