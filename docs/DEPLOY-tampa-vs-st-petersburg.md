# Deploy — Tampa vs. St. Petersburg comparison (June 2026)

One commit, six files. All edited from live repo copies pulled after your
St. Pete deploy.

## Files
1. tampa-vs-st-petersburg-retirement.html → repo root (NEW)
2. st-petersburg-profile.html → cities/st-petersburg/profile.html
   (compare block now live; built on the live file, so your lists-grid
   centering fix is preserved)
3. tampa-profile.html → cities/tampa/profile.html
   (compare section generalized: "Tampa, head-to-head." with two buttons —
   vs. Sarasota and vs. St. Pete)
4. compare-retirement-cities.html → repo root (7th hub card, Tampa Bay
   region; ItemList schema now 7 entries)
5. sarasota-vs-tampa-retirement.html → repo root (featured pill swapped:
   Asheville out, Tampa vs. St. Pete in — shared-city siblings first;
   its other pill, Naples vs. Sarasota, already shares Sarasota)
6. sitemap.xml → repo root (49 URLs — see incident note)

## SITEMAP INCIDENT (third occurrence — worth a process tweak)
The live sitemap was missing the St. Petersburg PROFILE entry: the sitemap
from the St. Pete profile batch never deployed, same as the Madison incident.
This delivery's sitemap adds BOTH the missing profile entry and the new
comparison entry (47 live → 49). Suggestion: add "confirm sitemap.xml is in
the commit file list" to your deploy ritual — it is the file that keeps
slipping. Also Request Indexing for the St. Pete profile URL if you did it
already, no harm; if the request silently relied on the sitemap, redo it.

## After deploy — Request Indexing for BOTH
- https://retiremehere.com/tampa-vs-st-petersburg-retirement.html
- https://retiremehere.com/cities/st-petersburg/profile.html

## The page, briefly
The verdict line: Tampa owns the practical rows, St. Pete owns the
livability rows, and the bay owns them both. Seven ✓ marks, all DB-verified:
Tampa takes monthly budget, tier, D1 (10 vs 8), D3 (10 vs 7, the biggest
gap), and Hot Summers; St. Pete takes home value ($352K vs $377K) and D6
(8 vs 6). 1-point gaps unmarked (D7, D8, D10). The cost tradeoff is narrated
honestly as a split: St. Pete cheaper to buy, Tampa cheaper to live.
Tradeoff 2 names the honest mechanism: part of St. Pete's own scores IS
Tampa's infrastructure across a bridge. Tradeoff 5: "Choosing between Tampa
and St. Petersburg changes your weekday; it does not change your hurricane
plan."

## DB FLAG for v15 review (not changed anywhere)
Climate Hot Sum: Tampa 4 vs. St. Petersburg 7 — a 3-point gap between
adjacent cities on the same bay. Marked in the table per the data-source
rule, but it looks like a scoring inconsistency worth a v15 look. If you
revise it, this comparison's climate row and ✓ need a matching edit.

## Judgment calls
- TPA described as "perennially rated among the best airports in the
  country" (no specific ranking-year claims).
- 2024 storm season referenced regionally, no storm-by-storm claims.
- Featured pills on the new page: Sarasota vs. Tampa + Naples vs. Sarasota
  (both shared-city/cluster) + hub pill.
- og:image: Tampa hero (lead city per slug order).
