# RetireMeHere — Back-Catalog Audit (29 city profiles)
*Generated for review. Three audit dimensions: (1) Range labels in stats, (2) Median Home pricing convention, (3) Neighborhood spread/bias.*

---
## Summary — size of the job
- **Range labels to remove:** 18 of 29 cities
  - alexandria, ann-arbor, asheville, bend, boulder, bozeman, carlsbad, charleston, lexington, madison, pittsburgh, santa-fe, scottsdale, st-george, st-louis, st-paul, tampa, tucson
- **Pricing convention to review** (old range/neighborhood method, needs city-median refresh): 5 cities
  - boulder, new-orleans, pittsburgh, st-louis, st-paul
- **Neighborhood urban-premium skew (auto-flagged, needs your judgment):** 2 cities
  - asheville, madison

> Note: the neighborhood flagger is keyword-based and crude. The full per-city table below shows all four neighborhoods for every city so you can spot skews the heuristic missed (e.g., the St. Louis case) and dismiss false positives.

---
## Per-city detail

### alexandria
- **Median Home stat:** $970K — Premium pricing · Range 4  ⚠ HAS RANGE
- **Neighborhoods:**
  - Old Town — *Historic · Walkable · Premium*
  - Del Ray — *Walkable · Quirky · Family-friendly*
  - Rosemont / Beverley Hills — *Quiet · Established · Tree-lined*
  - West End / Cameron Station — *Newer · Condo-friendly · Convenient*

### ann-arbor
- **Median Home stat:** $425K — Mid-tier · Range 3 · Below Boulder, Madison, Charleston  ⚠ HAS RANGE
- **Neighborhoods:**
  - Burns Park — *Historic · Walkable · Family-classic*
  - Old West Side — *Historic · Walkable · Downtown-adjacent*
  - Downtown / Kerrytown — *Walkable · Condo · Lock-and-leave*
  - North Campus / Plymouth Road — *Newer construction · Medical-adjacent · Wooded*

### asheville
- **Median Home stat:** $465K — Moderate · Range 3  ⚠ HAS RANGE
- **Neighborhoods  ⚠ POSSIBLE SKEW:**
  - Montford — *Historic · Walkable · Premium*
  - North Asheville — *Established · Tree-canopied · UNCA-adjacent*
  - Kenilworth — *Quiet · Hilly · Walkable to downtown*
  - West Asheville — *Eclectic · Younger feel · Mixed Helene impact*

### bend
- **Median Home stat:** $800K — Mountain-town pricing · Range 3  ⚠ HAS RANGE
- **Neighborhoods:**
  - Downtown / Old Mill District — *Walkable · Riverside · Premium*
  - Westside (NorthWest Crossing) — *Newer · Family-popular · Walkable pockets*
  - Awbrey Butte — *Established · View · Quiet*
  - Southeast Bend / DRW (Deschutes River Woods) — *Treed · Larger lots · Best relative value*

### bentonville
- **Median Home stat:** $400K — Bella Vista ~$300K · Bentonville $400–490K
- **Neighborhoods:**
  - Downtown Bentonville — *Walkable · Premium · In-town*
  - Bella Vista — *Planned community · 12 min north · Best value*
  - South Bentonville / Pinnacle Hills — *Suburban · Newer · Family-and-corporate*
  - Rogers (Pinnacle / Prairie Creek) — *Adjacent city · Beaver Lake access · Suburban*

### bloomington
- **Median Home stat:** $345K — Affordable college-town pricing · below national
- **Neighborhoods:**
  - Elm Heights — *Historic · Walkable · Near campus*
  - Bryan Park — *Central · Green · Best value near downtown*
  - Prospect Hill — *Historic · Trail access · West of downtown*
  - Park Ridge / Park Ridge East — *Quiet · Suburban · Strong safety*

### boulder
- **Median Home stat:** $800K–$1M — Aspirational pricing · Range 4  ⚠ HAS RANGE  ⚠ PRICING-REVIEW
- **Neighborhoods:**
  - Mapleton Hill — *Historic · Walkable · Premium*
  - North Boulder (NoBo) — *Trail-adjacent · Newer · Best value*
  - Newlands — *Family · Quiet · Tree-canopied*
  - Table Mesa / South Boulder — *Foothills · Trail access · Larger lots*

### bozeman
- **Median Home stat:** $725K — High · Range 4 · Doubled since 2015  ⚠ HAS RANGE
- **Neighborhoods:**
  - Bon Ton / Cooper Park — *Historic · Walkable · Downtown-adjacent*
  - South Tracy / South Willson — *Historic · Walkable · MSU-adjacent*
  - Northeast Bozeman — *Eclectic · Established · Mixed character*
  - Valley West / Baxter Meadows — *Newer master-planned · Single-family · West-side*

### carlsbad
- **Median Home stat:** $1.5M — High · Range 4 · Coastal CA premium  ⚠ HAS RANGE
- **Neighborhoods:**
  - Carlsbad Village — *Walkable · Coastal · Condo + cottage*
  - Olde Carlsbad / Barrio — *Established · Coastal-adjacent · Single-family*
  - Aviara — *Master-planned · Resort-adjacent · Newer*
  - La Costa — *Established master-planned · Golf · Single-family*

### charleston
- **Median Home stat:** $523K — Moderate · Range 3  ⚠ HAS RANGE
- **Neighborhoods:**
  - South of Broad — *Historic · Premium · Walkable*
  - Mount Pleasant — *Suburban · Family · Less flood exposure*
  - West Ashley — *Mainland · Best value · Mixed character*
  - Daniel Island — *Master-planned · Newer · Walkable village*

### charlottesville
- **Median Home stat:** $510K — Well above national · UVA &amp; lifestyle premium
- **Neighborhoods:**
  - North Downtown — *Historic · Walkable · Premium*
  - Belmont — *Arts · Food · Walk to downtown*
  - Fry's Spring / JPA — *Near UVA · Established · Convenient*
  - Crozet — *Small town · Mountain views · Newer*

### columbus
- **Median Home stat:** $290K — Well below national average · condos from ~$250K
- **Neighborhoods:**
  - German Village — *Historic · Walkable · In-town premium*
  - Clintonville — *Established · Leafy · Best in-city value*
  - Upper Arlington &amp; Bexley — *Suburban · Prestigious · Quiet*
  - Worthington &amp; Westerville — *North suburbs · Newer options · Value*

### fort-worth
- **Median Home stat:** $340K — Below national average · Tarrant County ~$345K
- **Neighborhoods:**
  - Tanglewood &amp; TCU-Westcliff — *Established · Leafy · Near everything*
  - Fairmount &amp; the Near Southside — *Historic · Walkable · Restored*
  - Mira Vista &amp; SW golf country — *Gated · Golf · Suburban premium*
  - Alliance / North Fort Worth — *Newer · Planned · Best value*

### greenville
- **Median Home stat:** $480K — City median sale price
- **Neighborhoods:**
  - North Main — *Walkable · Historic · Premium*
  - Five Forks — *Suburban · Space · Family-safe*
  - Travelers Rest — *Small-town · Outdoors · Trailhead*
  - Overbrook — *Historic · Close-in · Attainable*

### lexington
- **Median Home stat:** $330K — Affordable · Range 2  ⚠ HAS RANGE
- **Neighborhoods:**
  - Chevy Chase — *Historic · Walkable · Established*
  - Beaumont — *Suburban · Family-friendly · Master-planned*
  - Andover / Hartland — *Affluent · Golf · Spacious*
  - Hamburg / Beaumont East — *Amenity-rich · Newer · Convenient*

### madison
- **Median Home stat:** $375K — Approachable pricing · Range 3  ⚠ HAS RANGE
- **Neighborhoods  ⚠ POSSIBLE SKEW:**
  - Downtown / Capitol Isthmus — *Walkable · Urban · Lake-flanked*
  - Tenney-Lapham (Near East) — *Historic · Charming · Lake Mendota*
  - Marquette / Williamson (Wil-Mar) — *Eclectic · Festival-loving · Lake Monona*
  - Monroe Street / Nakoma — *Leafy · Established · West-side*

### nashville
- **Median Home stat:** $490K — Above U.S. average · condos from ~$350K
- **Neighborhoods:**
  - 12 South &amp; Sylvan Park — *Walkable · Leafy · In-town favorite*
  - East Nashville &amp; Germantown — *Artsy · Restored · Creative*
  - Green Hills &amp; Belle Meade — *Upscale · Established · Central*
  - Franklin &amp; Brentwood — *Suburban · Small-town · Premium*

### new-orleans
- **Median Home stat:** $370K — Citywide · historic neighborhoods pricier  ⚠ PRICING-REVIEW
- **Neighborhoods:**
  - Garden District — *Historic · Grand · Walkable*
  - Uptown — *Leafy · Streetcar · Established*
  - Lakeview — *Suburban · Rebuilt · Quieter*
  - Lower Garden District &amp; Irish Channel — *Walkable · Characterful · Value*

### philadelphia
- **Median Home stat:** $275K — Citywide · far less than NYC/Boston/DC
- **Neighborhoods:**
  - Rittenhouse Square — *Walkable · Sophisticated · Central*
  - Society Hill &amp; Washington Sq West — *Historic · Cobblestoned · Quiet*
  - Chestnut Hill &amp; Mt. Airy — *Village-like · Leafy · Northwest*
  - Fitler Square &amp; Graduate Hospital — *Walkable · Residential · Value*

### pittsburgh
- **Median Home stat:** $425–700K — Target neighborhoods · Range 3  ⚠ HAS RANGE  ⚠ PRICING-REVIEW
- **Neighborhoods:**
  - Shadyside — *Walkable · Upscale · UPMC-adjacent*
  - Squirrel Hill — *Diverse · Walkable · Strong community*
  - Mount Lebanon — *Suburban · Quiet · T-accessible*
  - Fox Chapel — *Estate · Wooded · Premium*

### salt-lake-city
- **Median Home stat:** $590K — Well above U.S. average · condos from ~$465K
- **Neighborhoods:**
  - The Avenues — *Historic · Hillside · Walkable*
  - Sugar House — *Walkable · Vibrant · Mixed-age*
  - The East Bench &amp; Federal Heights — *Premium · Trail-adjacent · Quiet*
  - Holladay &amp; Cottonwood Heights — *Suburban · Canyon-close · Value*

### santa-fe
- **Median Home stat:** $520K — Moderate · Range 3  ⚠ HAS RANGE
- **Neighborhoods:**
  - Eastside / Canyon Road — *Historic · Premium · Gallery-walkable*
  - South Capitol — *Walkable · Established · Mid-priced*
  - Casa Solana / Casa Alegre — *Mid-century · Quiet · Best value*
  - Las Campanas — *Master-planned · Golf · Mountain views*

### sarasota
- **Median Home stat:** $538K — Pricier than most Gulf Coast cities
- **Neighborhoods:**
  - Downtown Sarasota — *Walkable · Premium · Cultural core*
  - St. Armands / Lido Key — *Barrier island · Premium · Beach*
  - Palmer Ranch / South Sarasota — *Suburban · Mid-tier · Master-planned*
  - Venice — *Adjacent city · 20 min south · Value*

### scottsdale
- **Median Home stat:** $875K — High · Range 4 · One of the database's priciest  ⚠ HAS RANGE
- **Neighborhoods:**
  - Old Town Scottsdale — *Walkable · Galleries · Condo + townhome*
  - McCormick Ranch — *Established · Lakes · Mid-tier value*
  - Grayhawk — *Master-planned · Two golf courses · North Scottsdale*
  - DC Ranch / Silverleaf — *Gated · Foothills luxury · Mayo-adjacent*

### st-george
- **Median Home stat:** $525K — Mid-tier · Range 3 · Below Bend, Bozeman, Scottsdale  ⚠ HAS RANGE
- **Neighborhoods:**
  - Downtown / Historic District — *Walkable pockets · Historic · Mid-century homes*
  - Bloomington / Bloomington Hills — *Established master-planned · Golf · Mid-tier*
  - SunRiver — *55+ active adult · Master-planned · Amenities*
  - Coral Canyon / Sienna Hills (Washington) — *Newer master-planned · Single-family · Northeast metro*

### st-louis
- **Median Home stat:** $350–500K — Suburban target · Range 2  ⚠ HAS RANGE  ⚠ PRICING-REVIEW
- **Neighborhoods:**
  - Chesterfield — *Affluent · Suburban · Amenity-rich*
  - Kirkwood / Webster Groves — *Historic · Walkable · Charming*
  - Clayton / Ladue — *Urban · Walkable · Sophisticated*
  - Wildwood / Town &amp; Country — *Quiet · Spacious · Very low crime*

### st-paul
- **Median Home stat:** $425–650K — Retiree neighborhoods · Range 3  ⚠ HAS RANGE  ⚠ PRICING-REVIEW
  - Range also in: Monthly Budget: Range 3 · near national average
- **Neighborhoods:**
  - Summit Hill — *Historic · Premium · Walkable*
  - Macalester-Groveland — *Collegiate · Walkable · Steady*
  - Highland Park — *In-city suburban · Family · Amenities*
  - St. Anthony Park — *Village-y · Leafy · College-adjacent*

### tampa
- **Median Home stat:** $400K — Moderate · Range 3  ⚠ HAS RANGE
- **Neighborhoods:**
  - Hyde Park / South Tampa — *Walkable · Premium · Historic*
  - Westshore / Beach Park — *Suburban · Premium · Near airport*
  - Channelside / Water Street — *Newer urban · Walkable · Condos*
  - Carrollwood — *Mainland · Established · Best value*

### tucson
- **Median Home stat:** $315K — Affordable · Range 2  ⚠ HAS RANGE
- **Neighborhoods:**
  - Catalina Foothills — *Upscale · Mountain views · Spacious*
  - Sam Hughes / West University — *Historic · Walkable · College-adjacent*
  - Civano / Rita Ranch — *Master-planned · Active-adult · East side*
  - Tanque Verde / Eastside — *Suburban · Saguaro-adjacent · Quiet*
