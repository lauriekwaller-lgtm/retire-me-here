# Deploy — Compare Cities hub (June 2026)

One commit, seven files. All edited from current repo copies.

## Repo root
1. compare-retirement-cities.html  (NEW: the hub)
2. scottsdale-vs-tucson-retirement.html  (nav link + matchup block reworked)
3. santa-fe-vs-tucson-retirement.html  (same)
4. asheville-vs-greenville-retirement.html  (same)
5. sarasota-vs-tampa-retirement.html  (same)
6. madison-vs-ann-arbor-retirement.html  (same)
7. sitemap.xml  (44 URLs: adds the hub AND the Madison entry that did not
   deploy last time — the live sitemap was still at 42 without Madison)

## After deploy
- Search Console: Request Indexing for BOTH
  https://retiremehere.com/compare-retirement-cities.html
  https://retiremehere.com/madison-vs-ann-arbor-retirement.html
  (Madison was never requested since its sitemap entry never went live.)

## What changed on the comparison pages
- Nav: "Compare Cities" link added to the desktop nav (between the Top Cities
  dropdown and the quiz button) and the mobile menu (after Find a City, with a
  scale icon). Phase 1 = these 6 pages only; sitewide nav rides along with
  future page touches.
- "More city matchups" blocks trimmed from 4 pills to 2 featured + a filled
  teal "Browse all city matchups →" pill linking the hub. Featured picks favor
  shared-city matchups first (e.g., the two Tucson pages point at each other),
  then regional contrast.

## Judgment calls
- Hub slug: compare-retirement-cities.html (keyword-bearing) rather than
  compare-cities.html.
- Hub og:image: Asheville hero (the most-searched anchor city among the five);
  swap freely. The branded share-image template remains the future fix.
- Hub schema: CollectionPage + ItemList of the five matchups.
- Hub copy keeps the credibility frame: "decision pages, not rankings," with
  the methodology sentence up top.
- Future pairings now have one extra deploy step: add the new matchup as a
  hub card AND (optionally) as a featured pill on its closest sibling page.
  The standard doc should get this update at the next pairing.
