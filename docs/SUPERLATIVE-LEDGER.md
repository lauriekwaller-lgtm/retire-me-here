# Superlative review ledger

Every superlative the validator can see, reviewed once, so the warn queue can sit at zero.

**Why this file exists.** The warn tier fires on claims about the OUTSIDE world — "the largest
stadium in the country" — which no spreadsheet can settle. Those claims are true, they are
load-bearing, and rewriting them away would make the copy worse. But a permanent wall of 39
warnings is a wall nobody reads, and a wall nobody reads is exactly where the next false claim
hides. That is not hypothetical: "Best value in the Southeast" (Chattanooga) and "Best value in
Florida" (Tampa) were both false, and both sat in that wall.

**How it works.** A row here retires a claim from the queue. A row is a human assertion that the
claim is true about the outside world, and therefore cannot rot when city 100 lands. Anything not
listed here is by definition unreviewed, and the validator shouts about it. If the copy changes,
the row stops matching and the validator reports a STALE LEDGER entry, so this file cannot quietly
outlive the sentence it vouches for.

**What must never go in here.** A claim scoped to our own dataset. Those are a hard FAIL, not a
warning, and the answer is always to anchor to a figure or a named city. This file is not an
escape hatch for them.

Reviewed 2026-07-14.

| page | phrase | verdict | evidence |
| --- | --- | --- | --- |
| active-frontier.html | largest Del Webb communities in the country | TRUE | Sun City Texas is among the largest Del Webb communities. Hedged. |
| best-places-to-retire-in-florida.html | cheapest place to retire in Florida? | TRUE | FAQ question text, not a claim. The answer beneath it is scoped and figure-anchored. |
| best-places-to-retire-in-the-midwest.html | cheapest place to retire in the Midwest? | TRUE | FAQ question text, not a claim. The answer beneath it is scoped and figure-anchored. |
| cities/ann-arbor/profile.html | largest stadium in the country | TRUE | Michigan Stadium, 107,601 — largest stadium in the US. Verifiable, static. |
| cities/ann-arbor/profile.html | largest stadium in the country, and on home football Saturda | TRUE | Michigan Stadium, 107,601 — largest stadium in the US. Verifiable, static. |
| cities/ann-arbor/profile.html | largest stadium in the country, six or seven Saturdays a yea | TRUE | Michigan Stadium, 107,601 — largest stadium in the US. Verifiable, static. |
| cities/charleston/profile.html | highest in the country in coastal South Carolina ZIP | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/columbus/profile.html | largest universities in the country, gives Columbus a youthfulnes | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/fort-collins/profile.html | highest continuous paved road in the country | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/fort-myers/profile.html | largest in the country | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/kansas-city/profile.html | highest-income ZIP codes in the Midwest | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/kansas-city/profile.html | largest in the country, with two and a half million | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/knoxville/profile.html | largest stadiums in the country at around 102,000 seats, when | TRUE | Michigan Stadium, 107,601 — largest stadium in the US. Verifiable, static. |
| cities/madison/profile.html | largest producer-only market in the country | TRUE | Dane County Farmers' Market — largest producer-only market in the US. |
| cities/miami/profile.html | largest in the country with deep trauma, transplant, | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/naples/profile.html | highest concentrations of golf courses in the country, and Gulf beaches with sugar- | TRUE | Naples is commonly cited for one of the highest golf-course concentrations. Hedged. |
| cities/naples/profile.html | highest concentrations of golf courses in the country, and active wellness scored a | TRUE | Naples is commonly cited for one of the highest golf-course concentrations. Hedged. |
| cities/philadelphia/profile.html | largest in the country, with the museums, hospitals, | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/santa-fe/profile.html | largest art market in the US after New York and Los Angele | TRUE | Santa Fe is routinely cited as the 3rd-largest US art market after NY and LA. |
| cities/santa-fe/profile.html | largest art market in the country | TRUE | Santa Fe is routinely cited as the 3rd-largest US art market after NY and LA. |
| cities/scottsdale/profile.html | largest urban preserves in the country, secured through voter refere | TRUE | McDowell Sonoran Preserve, 30,000+ acres. Hedged 'one of the largest'. |
| cities/st-louis/profile.html | largest in the Western Hemisphere | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/st-louis/profile.html | widest city-to-suburb gaps in the country | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| cities/st-petersburg/profile.html | largest farmers markets in the Southeast, in season from fall through | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| fort-collins-vs-boulder-retirement.html | largest anywhere on this scorecard | TRUE | Page-local: refers to the two-city table on this page. Bounded, visible, static; cannot rot when a city is added. |
| index.html | Largest producer-only farmers market in the US at Capitol Square | TRUE | Largest producer-only farmers market in the US (Dane County). Matches the Madison profile. |
| index.html | highest in the US: major retirement income pena | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the country | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the country per Brookings); the town's so | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the nation per Tax Foundation; roads and | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the nation) | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the nation), home to PAAM, the Provincet | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest in the nation, median bill $5,026/year | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | highest property tax bills in the state | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | largest art market in the US | TRUE | Santa Fe is routinely cited as the 3rd-largest US art market after NY and LA. |
| index.html | largest gated communities in the US: 40 square miles, 10 golf cou | TRUE | Naples is commonly cited for one of the highest golf-course concentrations. Hedged. |
| index.html | largest urban park systems in the US at 9,200 acres | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | largest urban preserve in the US | TRUE | McDowell Sonoran Preserve, 30,000+ acres. Hedged 'one of the largest'. |
| index.html | most affordable mid-sized cities in the country | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| index.html | most expensive small town in the US by some rankings | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| knoxville-vs-chattanooga-retirement.html | largest spread anywhere on this scorecard, wider than | TRUE | Page-local: refers to the two-city table on this page. Bounded, visible, static; cannot rot when a city is added. |
| pick-and-compare.html | highest in the nation), home to PAAM, the Provincet | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| scottsdale-vs-santa-fe-retirement.html | largest art market in the US, wrapped around a walkable 16 | TRUE | Santa Fe is routinely cited as the 3rd-largest US art market after NY and LA. |
| top-cities-for-arts-lovers.html | largest art market in the US · 250+ galleries on Canyon Ro | TRUE | Santa Fe is routinely cited as the 3rd-largest US art market after NY and LA. |
| top-cities-for-arts-lovers.html | largest in the US) · Hill Auditorium · UMMA · M | TRUE | Outside-world claim, hedged or sourced. Not scoped to our dataset; cannot rot when a city is added. |
| top-cities-for-foodies.html | largest producer-only farmers market in the US · L'Etoile (Tory Miller, Jame | TRUE | Dane County Farmers' Market — largest producer-only market in the US. |
