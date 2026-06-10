# RetireMeHere — Comparison Page Build Spec (handoff)

How to build a city-vs-city retirement comparison page, matching the Asheville vs.
Greenville and Sarasota vs. Tampa pages. Paste this into a new chat as the brief.

---

## What a comparison page is for

It's a **front door from Google, not a page in your site's navigation.** It targets
high-intent, decision-stage searches like "Sarasota vs Tampa for retirement" — lower
competition than "best places" listicles, closer to buying intent (good for the moving /
insurance / senior-living affiliate angle), and uniquely doable because RetireMeHere
scores all 100 cities on the same 10 dimensions. That unique, structured data is what
gets cited in AI answers.

**It does NOT go in the "Top Cities For" dropdown.** It lives on search and on links from
the two city profiles.

---

## Before you start

1. **Pull both cities' real numbers from the current database** (`CityDatabase_Jun_9_v14.xlsx`
   or whatever the latest is). Scores never come from the web — see the profile data rule.
   ```python
   import pandas as pd
   df = pd.read_excel(path, sheet_name='City Database', header=1)
   df.columns = [str(c).replace('\n',' ').strip() for c in df.columns]
   ```
   Grab D1–D10, healthcare /10, budget tier, Monthly Est, Median Home, plus
   `PropTax Rate %`, `HO Insur Est $/yr`, `HUM`, `HEAT`, `D4 Resil.`.
2. **Pick a pairing where both cities are already published profiles** (so the reciprocal
   "Compare these" links work). Good pairs: same-state rivals, same-archetype cities, or
   "the famous one vs. the cheaper lookalike."

---

## File & naming convention

- Filename / slug: **`[city]-vs-[city]-retirement.html`** (e.g.,
  `asheville-vs-greenville-retirement.html`), lowercase, hyphenated.
- Lives at the **repo root** (alongside `index.html` and the `top-cities-for-*.html`
  pages), NOT in a `cities/` folder.

---

## How to build it

**Start by cloning the head/CSS/nav/footer from a current published page** (a
`top-cities-for-*.html` landing page works well) so it matches the site exactly, then
replace the body. Keep the GA4 tag (`G-BTL743DSJQ`), nav, and footer.

### Head
- Title: `[City] vs. [City] for Retirement: Cost, Healthcare & [differentiator] | RetireMeHere`
- Canonical + Open Graph + Twitter meta pointing at the new slug.
- **Article + FAQPage schema** (JSON-LD `@graph`), same as profiles.

### Body, in this order

1. **Hero with the verdict up front** (this sentence is the citation bait):
   *"The short version: choose [City A] if [reasons], and [City B] if [reasons]."* Name the
   honest shared catch if there is one (e.g., both Florida cities → hurricane + insurance).

2. **Scored side-by-side table** — the moat. Two city columns, grouped rows:
   - **Cost & money:** typical home value, retiree budget/mo, budget tier, property-tax
     rate, home insurance est.
   - **Our 10-dimension scores:** all ten, shown as `X/10`.
   - **Climate:** winters, summer heat/humidity.
   - Highlight the stronger cell in each row (higher score wins; lower cost wins; leave
     genuine ties unmarked — ties are honest and fine).
   - Caption: "Scored 0–10 against the 100 cities in our database; higher is better."

3. **Tradeoff narrative** (~5 short sections, a few hundred words). Typical arc: what the
   two share, where the money differs, the biggest practical difference, each city's
   signature strength, and the honest shared downside.

4. **Reciprocal profile cards** — two outlined cards (give them distinct brand-color
   outlines, e.g., teal and terra) linking to `/cities/[a]/profile.html` and
   `/cities/[b]/profile.html`, each with a one-line descriptor.

5. **Visible FAQ (5 questions)** backed by the same FAQPage schema. House format:
   1. "Is [City A] or [City B] better for retirement?" (the verdict)
   2. "Which is cheaper, [City A] or [City B]?"
   3. "Which has better healthcare?"
   4. The honest catch question (e.g., "How bad are hurricanes and insurance in…?")
   5. A real differentiator (e.g., "Which has the better airport?")
   Answers cite the actual scores and figures.

6. **Quiz CTA + footer** (kept from the cloned shell).

---

## Writing standards

- **No em dashes** anywhere in the copy (use commas, colons, parentheses, periods).
- Scores cited with referents; honest about shared downsides; no unqualified superlatives.
- Plain language. Specific, attributable facts — those are what get quoted.

---

## Deploy checklist

1. Upload `[city]-vs-[city]-retirement.html` to the **repo root**.
2. Add its URL to **`sitemap.xml`** (`changefreq monthly`, `priority 0.8`).
3. Add a reciprocal link from **both** city profiles' "Compare these" blocks pointing to
   the new comparison page. (This internal link is most of the SEO value and is what makes
   it reachable from inside the site.)
4. In Search Console, **Request Indexing** for the new URL.
5. Do **not** add it to the "Top Cities For" dropdown.

> Future idea (once there are 5–6 comparisons): a single "Compare Cities" hub page that
> lists them all, with its own nav link, so visitors can browse them. Not needed yet.
