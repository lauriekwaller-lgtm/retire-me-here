# RetireMeHere — City Profile Citation Recipe

A working playbook for building city profiles that get cited in Google's AI Overviews
(the way the Bentonville profile did). Paste this into a new chat as the brief.

---

## Why this matters

In 2026, roughly half of Google searches show an AI-generated answer box, and it
heavily favors informational queries like "[city] for retirement." Ranking #1 the old
way matters less; being **cited inside the AI answer** is the new win — and cited
sources get *more* clicks than the top blue link. The good news: unique, specific data
earns those citations even for a smaller site. That's exactly why Bentonville worked.

---

## The 4 things that make a profile citable

1. **It answers the literal question.** Title is "[City], [State] — A Retirement City
   Profile," and the FAQ asks "Is [City] a good place to retire?" in those words. Tight
   match between the search and what the page is *about* is the single biggest factor.

2. **Schema tells Google what it is.** Article + FAQPage structured data (JSON-LD) spells
   out, machine-readably, that this is a retirement profile with these questions answered.

3. **It has specific, attributable facts to quote.** AI answers lift concrete facts, not
   vague prose. "Seven lakes, six golf courses," "Sarasota Memorial holds a 5-star CMS
   rating," "Healthcare scores 10/10." Vague description ("a charming town") never gets
   quoted. **This is the real edge — lead with specifics and scores.**

4. **It's indexed and focused.** Entirely about one city for retirement, live, crawled,
   and internally linked so Google prioritizes it.

---

## Hard rule: scores come from the database, never the web

All dimension scores (D1–D10), the healthcare /10 grade, budget tier, Monthly Est, and
Median Home **must** be read from the current CityDatabase spreadsheet before writing a
word. Web research is only for *supporting color* (hospital names/rankings, beach names,
airport routes) — never for scores. If the database isn't provided, stop and ask for it.

**Current database:** `CityDatabase_Jun_9_v14.xlsx` (this filename increments over time —
always use the latest one provided, and confirm it at the start).

How to read it (Python):
```python
import pandas as pd
df = pd.read_excel(path, sheet_name='City Database', header=1)
df.columns = [str(c).replace('\n',' ').strip() for c in df.columns]   # headers have newlines
# match on (City, ST) as stripped strings
```
Useful extra columns already in the DB: `PropTax Rate %`, `HO Insur Est $/yr`, `HUM`,
`HEAT`, `D4 Resil.` (disaster resilience), plus a `Highlight` field with quotable facts.

---

## Required structure of a current profile

Match the standard set by the recent profiles (e.g., Santa Fe, Sarasota, Bentonville).
A current profile has, in the `<head>`:

- **GA4 tag** — measurement ID `G-BTL743DSJQ` (and the `report_request` event on the
  guide forms so report sign-ups are tracked). *Without GA4 you can't measure the page —
  this is mandatory.*
- **Open Graph / social meta** (og:type/title/description/url/site_name, twitter:card).
- **Article + FAQPage schema** in one JSON-LD `@graph`.

In the body (keep all of these — older profiles that lack them are the ones to upgrade):
- Hero, stats bar, the "Is [City] for you?" narrative section
- **Deep Dive email capture** section (the 5 MailerLite guide forms)
- Character / "a week in" / neighborhoods / healthcare narrative
- **Services section** (moving / senior-living / insurance affiliate hooks)
- **"Compare these" related-cities block** (links to other profiles + any comparison pages)

### The FAQ (4-question house format)

Keep the FAQ in the schema, fact-led, citing scores. The four questions:

1. "Is [City], [State] a good place to retire?"
2. "How much does it cost to retire in [City], [State]?"
3. "What is healthcare like in [City] for retirees?"
4. "What are the downsides of retiring in [City]?"

Answers should name real numbers ("scores 8 of 10," "$3,500 to $4,800 a month") and be
honest about the downsides.

---

## Writing standards

- **Lead with specific, attributable facts and scores.** The more concrete and unique,
  the more citable. This is the whole game.
- **Scores woven in with referents, not a bare scorecard.** "Healthcare scores a perfect
  10, the only city in our database to do so" beats a clinical grid. (No raw scorecard —
  that was a rejected idea.)
- **Honest labeling.** Scores are RetireMeHere's own assessment, never claimed as a
  federal index or third-party ranking.
- **No unqualified superlatives.** "Lowest of any city we scored," not "the safest in
  America."
- **No em dashes** (they read as AI-generated). Use commas, colons, parentheses, periods.
- **Plain language.** Short, concrete, no jargon.
- **Neighborhood-basis cities** (e.g., St. Louis, Memphis, Philadelphia, Pittsburgh,
  San Antonio, Wilmington DE, Indianapolis) legitimately use retiree-target neighborhood
  figures — handle home values honestly (citywide median vs. the suburbs retirees buy in).

---

## Build & file conventions

- **Photos:** hero 1600×899, detail 1600×2133 (portrait), lifestyle 1280×1280 (square);
  vet for licensing and editorial fit. Hand off with city-prefixed names
  (e.g., `bentonville-hero.jpg`); they get renamed to `hero/detail/lifestyle.jpg` inside
  `cities/<slug>/` at deploy.
- **Hand off the profile as** `<city>-profile.html`; renamed to `profile.html` in
  `cities/<slug>/` at deploy.
- **Slug** = lowercase, spaces → hyphens (`St. Paul` → `st-paul`, `Ann Arbor` → `ann-arbor`).

---

## Deploy checklist

1. Read scores from the database first.
2. Build the profile to the structure above (GA4 + OG + schema + FAQ + all body sections).
3. Add the city to `PUBLISHED_PROFILES` in `index.html` (key = `cityName_state`).
4. Add the profile URL to `sitemap.xml`.
5. Add reciprocal links (from related profiles / comparison pages).

---

## Getting it cited (after deploy)

- Confirm GA4 is on the page (analytics = measurement).
- In Google Search Console, make sure `sitemap.xml` is submitted (once), then use
  **URL Inspection → Request Indexing** on the new profile. There's a daily quota; one
  request per URL is enough.
- **Internal-link the page** from a stronger page (related profiles, comparison pages).
  Orphan pages sit "discovered, not indexed"; links are the fix.
- Expect days-to-weeks to index, and unevenness — some profiles get cited, some won't,
  and it builds over months. The pattern is proven; volume + time does the rest.
