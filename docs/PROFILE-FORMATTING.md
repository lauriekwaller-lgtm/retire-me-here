# PROFILE FORMATTING

**Version:** 1.0
**Adopted:** June 21, 2026
**Supersedes:** `BOLDING-CONVENTION.md` v2.1
**Canonical reference:** `cities/st-louis/profile.html`

This document captures the settled formatting standard for all city profile pages. It covers (1) the six mechanical format changes applied to every profile, (2) the bolding rules as actually practiced, and (3) the Neighborhood Reality Check callout structure for the eight NRC cities.

When in doubt, open the St. Louis profile and match its structure.

---

## The six format changes

Every new profile and every legacy cleanup pass applies these six changes. The first five are mechanical (find-and-replace); the sixth is judgment-based (per the bolding rules below).

### 1. Light-mode lock

Add to `<head>` after the viewport meta:
```html
<meta name="color-scheme" content="light">
```

Add to the existing `html` CSS rule:
```css
html { scroll-behavior: smooth; color-scheme: light; }
```

Prevents iOS Safari and Chrome from applying forced dark transformations to the warm-cream design palette.

### 2. Cost-strip alignment

Change `.cost-strip` CSS from centered to left-aligned:
```css
.cost-strip {
  /* ... */
  justify-content: flex-start;  /* was: center */
  text-align: left;             /* was: center */
}
```

### 3. Cost-strip bolding — label-only

Flip the bolding direction on the Property tax and Home insurance lines:
```html
<!-- Before -->
<span class="cost-item">Property tax: <strong>0.89%</strong> effective (...)</span>

<!-- After -->
<span class="cost-item"><strong>Property tax:</strong> 0.89% effective (...)</span>
```

State-average disclosures use label-only bolding. The label is the wayfinding cue; the value is reference data.

### 4. Hood-card hover wrap

Wrap the `.hood-card:hover` rule in a hover-capable media query:
```css
@media (hover: hover) {
  .hood-card:hover {
    border-color: var(--teal);
    box-shadow: 0 8px 24px rgba(28,26,24,0.06);
  }
}
```

Prevents the hover border state from sticking after a tap on touch devices (which was producing the inconsistent darker-border anomaly on individual cards).

### 5. Composite-week intro paragraph — delete

Delete the `<p class="week-intro">…</p>` paragraph under the "A week in [city], roughly" section title. The section title plus day cards carry the narrative without the setup paragraph.

### 6. Bolding pass

See the bolding rules below.

---

## Bolding rules

Bolding serves the scanner — a reader who skims on iPad before deciding whether to read deeply. The rule is functional, not stylistic: bold only what a scanner actually needs to find. When in doubt, leave the bold off.

### What stays bolded (existing patterns that work)

- **Reality Check callout** — neighborhood names and the price range inside the callout. The callout is its own scoped context.
- **Fit-section bullet lead-ins** — the label-style topic phrase at the start of each "Yes if / No if" bullet ("Healthcare matters more than weather.", "You won't go suburban.", etc.).
- **Hood-card median/range sentences** — whole-clause information bolds ("Median: ~$538K, with the largest historic homes well above.").
- **Hood-card sub-area anchors** — proper nouns named within the hood-card body (Ladue, Frontenac, Wildwood, Oakville).
- **Hoods-intro disclaimer** — "Pricing reflects May 2026 estimates and varies by municipality, block, and lot."
- **Method-callout label** — "Reading the numbers here:".
- **Cost-strip labels** — Property tax:, Home insurance: (label-only per #3 above).
- **Health-card named designations** — "Honor Roll" or similar named credentials, when they appear in the health-detail prose.

### What gets stripped during a bolding pass

- **Anchor bolds for proper nouns covered elsewhere.** If a neighborhood gets its own hood card, or appears in the Reality Check callout, or sits in a fast-facts aside, or headlines a day-card, don't bold its body-prose appearance. The card / callout / fast-fact IS the anchor.
- **Names in passing illustrative lists.** Lists like "the retirees who land here happily go suburban — Chesterfield, Kirkwood, Webster Groves, Clayton — where the math is different" are illustration, not anchor territory. Don't bold the items.
- **Partial-clause fact bolds.** Don't bold fragments like "the largest city in Ohio" or "$253K citywide typical home value" or "more than 200 working fountains" inside otherwise plain sentences. Either the fact warrants a complete-clause information bold (rare) or it doesn't earn a bold.
- **Sub-institution names in health-detail prose.** The health-card already gives the primary institution prominent styling. Don't add inline bolds for sub-units (e.g., "Mid-America Heart Institute" within Saint Luke's detail).

### What gets added during a bolding pass

In the **character section** body prose (the "About this city" overview after the hero), add **1–2 topic-sentence whole-clause bolds** that capture a unifying insight — the sentence a reader would want to remember after closing the page.

Examples from canonical profiles:

- **St. Louis** — *"The metro is structured by an emphatic City–County divide."* (topic-sentence) and *"What unites all of them is Forest Park"* (connective tissue between paragraphs)
- **Columbus** — *"What that steady growth bought, over time, was a real city's worth of culture without a big city's price tag."* and *"And running underneath everything is the medical engine."*
- **Pittsburgh** — *"The healthcare story is what brings most retirees here."* and *"What's surprising is the math."*
- **Philadelphia** — *"But Philadelphia's defining trait, for a retiree, is its contradictions."* and *"That combination — affordable, walkable, cultured, medically deep — is what makes Philadelphia quietly one of the best urban retirement values in the country."*

Don't force two. If a profile only has one clear unifying insight, one bold is better than a weak second. (Kansas City has only one — the P3 closer "The whole package is what a major coastal metro costs minus the coast.")

Don't add character-section bolds in the first paragraph if it carries a dropcap. The dropcap is the visual entry; competing with it adds noise.

### What never gets bolded

- Adjectives or subjective descriptors on their own — "walkable," "vibrant," "affordable," "underrated"
- Verbs or process language
- Generic nouns when not used as proper names — downtown, the river, the airport, the hospital
- Anything inside a pull quote, blockquote, or callout other than the Reality Check
- Anything inside a day-card body (the day-activity headline is the card's anchor)
- The hero tagline (the hero is the visual emphasis)

---

## Neighborhood Reality Check callout

The eight NRC cities require an above-fold Reality Check callout under the Median Honesty Rule:

- Memphis
- Philadelphia
- Pittsburgh
- St. Louis
- New Orleans
- Columbus
- Kansas City
- Tampa

These are cities where the citywide ZHVI median significantly understates what retirees actually pay because retiree-target neighborhoods run substantially higher.

### Structure

The callout sits between the stats-bar (if present) and the cost-strip:

```html
<!-- NEIGHBORHOOD REALITY CHECK — per Median Honesty Rule, MEDIAN-HOME-METHODOLOGY.md v1.1 -->
<aside class="reality-check">
  <div class="reality-check-eyebrow">Neighborhood Reality Check</div>
  <p class="reality-check-body">
    [content]
  </p>
</aside>
```

CSS is in the batch additions section of each profile's inline `<style>` block (copy from any existing NRC city profile).

### Content formula

1. State the citywide median figure and what it represents.
2. Name the retiree-target neighborhoods (bolded).
3. Give the realistic range (bolded).
4. Optional: note premier-tier outliers ("with estate enclaves higher", "into seven figures", etc.).
5. Close with: "Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice."

### Examples

**St. Louis:**
> The $235K citywide median reflects significant variation across St. Louis. The neighborhoods retirees typically target in the city — **Tower Grove South**, **Central West End**, **Soulard**, **Lafayette Square** — run roughly **$420K–$575K**. Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice.

**Kansas City:**
> The $253K citywide median is the Kansas City, Missouri figure. Retiree-target neighborhoods — **the Plaza**, **Brookside**, **Waldo**, and the Kansas suburbs (**Mission Hills**, **Leawood**, **Overland Park**) — run **$300K–$900K**, with premier Kansas enclaves into seven figures. Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice.

---

## QA checklist for any profile being touched

- [ ] `<meta name="color-scheme" content="light">` in `<head>`
- [ ] `html { ... color-scheme: light; }` in CSS
- [ ] `.cost-strip` CSS uses `flex-start` and `left`
- [ ] Property tax / Home insurance lines bold the labels, not the values
- [ ] `.hood-card:hover` is wrapped in `@media (hover: hover) { ... }`
- [ ] No `<p class="week-intro">…</p>` in the week-section
- [ ] No anchor bolds for proper nouns covered in callouts, hood cards, fast-facts, or day-card headlines
- [ ] No partial-clause fact bolds in body prose
- [ ] Character section has 1–2 topic-sentence whole-clause bolds (or 1 if no clear second insight)
- [ ] NRC callout present (if city is one of the 8 NRC cities)
- [ ] No em-dashes outside of the established convention spots
- [ ] Strong tag balance: `<strong>` count equals `</strong>` count

---

## Working principle

When something feels uncertain, the answer is in the St. Louis profile. If St. Louis doesn't have an example of the case in question, lean toward fewer bolds rather than more. The risk of over-application is much higher than the risk of under-application.
