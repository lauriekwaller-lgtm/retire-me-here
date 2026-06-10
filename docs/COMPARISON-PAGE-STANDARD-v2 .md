# Comparison Page Standard — v2 addendum (June 2026)

Append to HANDOFF-comparison-pages.md. Decisions from the Scottsdale vs. Tucson
A/B review. The Scottsdale vs. Tucson FINAL file is the reference build.

## Page architecture (locked)

1. Hero: eyebrow "City Comparison" · H1 "[A] vs. [B] for retirement." with both
   city names in accent color · one-line context tagline under the H1 (what makes
   this pairing interesting, e.g. "110 miles apart, nearly identical weather,
   very different price tags").
2. Verdict box directly under the hero: bordered card, teal left accent, labeled
   "The short version". This is the citation bait; it must name when to choose
   each city AND the honest shared catch.
3. Scored table with three section rows (Cost & money / Our 10-dimension scores /
   Climate), terra section-row headers, stacked City + STATE column headers.
4. Tradeoff narrative, 5 H3 blocks: What they share · Where the money differs ·
   The biggest practical difference · Each city's signature strength · The honest
   shared downside.
5. "Read the full profile" section with two outlined profile cards (teal + terra).
6. "More city matchups" pill links to ALL other live comparison pages (update
   every existing comparison page when a new one ships — this keeps the
   comparison cluster interlinked until the hub page exists).
7. Visible FAQ (5 Qs) + quiz CTA + footer.

## Table rules

- Winner cell = shaded (teal-lt, bold) AND a real " ✓" text character in the cell.
  CSS ::after checkmarks are invisible to scrapers and AI answer engines; the
  literal character travels with the text.
- Caption must include: scoring sentence, checkmark/tie explanation, and a
  data-freshness line: "Data: RetireMeHere city database, [Month Year]." Update
  the month whenever scores are refreshed from a new DB version.
- Budget tier label is "(1 = least expensive)" and values read "X of 5". There
  are FIVE tiers. Never write "of 4".
- Do NOT include the "Mild year-round" climate score as a row. It is a quiz
  preference-match field; on a page that also shows heat severity 10/10 it reads
  as a contradiction and damages credibility. Use a "Winters" row with a short
  plain description instead.
- Don't mark a winner on 1-point gaps that are practically identical (e.g.
  humidity 1 vs. 2 between two deserts). Add short context instead
  ("1/10, very dry"). A winner mark on heat 9 vs. 10 is fine WITH context
  ("softened by elevation") because readers genuinely feel that difference.
- Inline context in climate cells is encouraged ("on par with Phoenix",
  "softened by elevation"). It is what gets quoted.

## FAQ rules

- Every question contains both city names ("Which has better healthcare,
  Scottsdale or Tucson?"). Bare questions ("Which has better healthcare?") match
  fewer People Also Ask queries.
- FAQPage schema text must be synced verbatim from the visible FAQ. Build the
  visible FAQ first, then generate schema from it, never the reverse.

## Schema rules

- Article node: headline, description, url, datePublished, dateModified,
  mainEntityOfPage, publisher, AND about: two City entities each with
  containedInPlace State. (Dates were missing in one draft; City entities in the
  other. Both are required.)

## Fact standards for the "color" claims

- Specific verified numbers beat vague claims for AI citation (e.g. "PHX:
  nonstop to more than 130 domestic destinations plus international routes" and
  "TUS: 19 nonstop destinations, all domestic" are both verified against the
  airports' own published figures, June 2026). Verify route counts, hospital
  rankings, and drive times before publishing; if unverifiable, soften to
  qualitative language rather than guessing.
- Drive times: use realistic figures (Tucson to Sky Harbor is about 1 hour 45
  minutes, not "90 minutes").
- Hospital proximity: prefer verifiable geography ("just over the city's
  northern border") over unverified drive times ("15 minutes away").

## Bold text in narrative blocks

- Selective <strong> only, on three things: dollar values (the two home values),
  anchor institution names (the hospitals), and each city's headline dimension
  score in the signature-strength section. In the FAQ, bold only the
  direct-answer lead ("Tucson, dramatically.").
- Never bold whole sentences or adjectives; that reads as AI-styled copy.
- Bold renders in the dark body color (--dark), weight 700, not teal. Colored
  bold reads as "colored" rather than "emphasized" at body sizes.
- FAQPage schema text stays plain: strip tags when generating schema from the
  visible FAQ.

## Photos (now standard, June 2026 update)

Both cities in a pairing are always published profiles, so hero photos already
exist at cities/<slug>/hero.jpg. Use them two ways, no new assets needed:

1. og:image + twitter:image in the head, absolute URL, pointing at one city's
   hero (lead city of the pairing). Upgrade later to a branded vs-card from Pin
   Studio when one exists.
2. Lazy-loaded thumbnails at the top of the two profile cards
   (class profile-card-img, full-bleed via negative margins, height 160px,
   object-fit cover, loading="lazy", width/height attributes set to prevent
   layout shift).

Do NOT add a photo hero or gallery above the table. The verdict box and scored
table are the SEO payload and must stay high on the page; photos above them
slow load and push the moat below the fold.

## Known-good copy patterns worth reusing

- "You are not choosing between two climates or two tax codes. You are choosing
  between two price points and two personalities." (frame for same-state pairs)
- Equity framing: "A retiree who sells a home in a mid-priced market can often
  buy in [cheaper city] with cash left over; in [pricier city], the same equity
  may only be a down payment."
- Lifestyle litmus: "If your ideal week includes X and Y, [A] fits. If it
  includes P, Q, and R, [B] fits."

## Future (not yet)

- Branded vs-card share image (Pin Studio template) to replace the single-city
  hero currently used as og:image.
- Comparison hub page once there are 5–6 matchups (already in the original spec).
