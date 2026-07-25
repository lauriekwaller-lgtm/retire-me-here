# PROFILE FORMATTING

**Version:** 1.6
**Adopted:** June 21, 2026 (v1.0); em-dash policy added June 24, 2026 (v1.1); NRC list expanded to 10 cities and sweep completed June 29, 2026 (v1.2); forced-dark hardening, Visit-chip default, Deep Dive block placement, and plain-quiz language added July 9, 2026 (v1.3); Visit-block voice standard, Visit-block two-anchor bolding rule, and rollout-complete status added July 10, 2026 (v1.4); guide-page em-dash sweep completed and enforcement extended to guides July 14, 2026 (v1.5); NRC fixed list removed in favour of the live-repo enumeration July 25, 2026 (v1.6)
**Supersedes:** `BOLDING-CONVENTION.md` v2.1
**Canonical reference:** `cities/st-louis/profile.html`

This document captures the settled formatting standard for all city profile pages. It covers (1) the six mechanical format changes applied to every profile, (2) the bolding rules as actually practiced, (3) the em-dash policy, (4) the Neighborhood Reality Check callout structure for NRC cities, and (5) the template structure standards (Visit block and its voice, Visit chip, Deep Dive placement, quiz language).

When in doubt, open the St. Louis profile and match its structure.

---

## The six format changes

Every new profile and every legacy cleanup pass applies these six changes. The first five are mechanical (find-and-replace); the sixth is judgment-based (per the bolding rules below).

### 1. Light-mode lock + forced-dark hardening

Add to `<head>` after the viewport meta:
```html
<meta name="color-scheme" content="light">
```

Add to the existing `html` CSS rule:
```css
html { scroll-behavior: smooth; color-scheme: light; }
```

The two declarations above stop iOS Safari and desktop Chrome from inverting the warm-cream palette. They do **not** stop Android Chrome's "force dark for web contents" flag, Samsung Internet dark mode, or in-app webviews (Facebook, Instagram, Gmail), which run their own algorithmic darkening and ignore `color-scheme`. To defend against those, add the forced-dark hardening block at the very end of the inline `<style>`, immediately before `</style>` (right after the `END STICKY CHIP NAV CSS` marker). The block is a single `@media (prefers-color-scheme: dark)` rule that re-pins light surfaces (cream/white cards) to light with dark text and dark-by-design surfaces (hero, detail break, health card, CTA, email capture, footer) to their intended dark backgrounds with light text, then restores the accent colors the blanket rules would otherwise flatten. It is baked into the canonical `cities/st-louis/profile.html`, so clones inherit it automatically; copy it verbatim from there if a legacy profile needs it.

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

## Template structure standards

Structural defaults baked into the canonical `cities/st-louis/profile.html` (and, where noted, applied at build time). New profiles inherit them by cloning the canonical. Added v1.3.

### Visit block and Visit chip

Every new profile carries a **Visit Before You Decide** block (affiliate slot) and a matching **Visit** nav chip. The block is added at build time from the canonical Visit markup. When adding it:

- Place the Visit block in the lower cluster, after the Deep Dive Reports block and immediately before the Quiz CTA.
- Add `<button class="nav-chip" data-target="visit">Visit</button>` in the **last** position of the sticky nav (after "Compare cities").
- Add `'visit'` to the scroll-spy `ids` array so the chip highlights on scroll. A chip missing from the ids array is the half-wired bug; a chip with no Visit block points at nothing.

Affiliate links use per-city Expedia and Vrbo codes (never shared) with `rel="sponsored nofollow"`. Leave `EXPEDIA_CODE_TK` / `VRBO_CODE_TK` placeholders until the codes are generated in Creator Hub.

Rollout status: as of July 10, 2026, all 41 published profiles carry a Visit block, per-city Expedia/Vrbo codes, and the Visit chip. The rollout is complete; new builds get all three by default.

### Visit block voice

The Visit block is written to a fixed voice standard, established when the block rolled out across all 41 profiles. The block sells the visit, not the city: the reader is already on the profile and already interested, so the job is to convert that interest into a scouting trip, and the honest, diligence-first framing is what actually motivates a retiree to go. Match the deployed blocks; the canonical example is `cities/st-louis/profile.html`.

Five short paragraphs, in order:

1. **Hook.** Open with the single most concrete, specific, appealing thing about the city: a named credential, a ranking, a signature fact, or a vivid scene, never a generic adjective. Lead with the positive. If the city has a real tradeoff (heat, winters, cost, crime, remoteness), weave it into the second or third sentence, not the opener. Do not open with a template ("A visit is how you..."); every hook opens differently from every other block.
2. **Neighborhoods + hospital + closer.** Vary the opener (no stock "Base yourself where retirees actually land"). Name the retiree-target neighborhoods (from the profile's own hood cards) and the hospital (from its healthcare section), then send the reader out to test it. End on the canonical closer, verbatim: **"Test the daily routine, not the highlight reel."** This closer is the site's signature sign-off, used on every block; it does not rotate.
3. **Expedia link.** "Search [City] hotels on Expedia" with the arrow, `rel="sponsored nofollow"`.
4. **Vrbo lead + link.** A one-line, city-specific rental lead (vary the opener across cities), then "Browse [City] rentals on Vrbo" with the arrow, `rel="sponsored nofollow"`.
5. **Disclaimer.** The standard FTC line, including the Costco Travel / AAA / price-three-ways note. Italic, verbatim.

Tone test: the set reads confident, not cautionary. Across a run of blocks the hooks lead with the positive and the tradeoffs feel woven in, never front-loaded as a warning per block. Scaffolding must not repeat block to block: unique hook openers, unique neighborhood-paragraph openers, varied rental-line openers. The one intentional refrain is the closer.

NRC cities in the Visit block: for the ten NRC cities, use retiree-target neighborhoods in paragraph 2 (not the citywide median) and make the citywide-versus-neighborhood point, but phrase it freshly each time. Do not repeat a stock line ("the citywide median averages in areas retirees would not target") across cities.

### Deep Dive Reports block placement

The email-capture "Free Deep Dive Reports" block sits in the **lower conversion cluster**, not near the top. Canonical order:

Plan Your Move -> Appears on Lists -> Related Cities -> **Deep Dive Reports** -> Visit -> Quiz CTA

Placing it after Related Cities (rather than right after the stats bar) means readers get the full city narrative before any email ask, and the "Step 3: Get the Deep Dive reports" card in Plan Your Move becomes a genuine jump-link down to the form instead of pointing at an adjacent block. The `#deep-dive-reports` anchor and the services-card link both resolve to the relocated block.

### Quiz language: no question count

Quiz copy uses plain **"the quiz"** with no number. Do not write "5-question quiz" or "7-question quiz." The quiz weighs more than seven considerations, the stated count has drifted across pages, and a fixed number dates the copy. Applies to the Plan Your Move services card ("Take the quiz") and the Quiz CTA tagline.

---

## Bolding rules

Bolding serves the scanner, a reader who skims on iPad before deciding whether to read deeply. The rule is functional, not stylistic: bold only what a scanner actually needs to find. When in doubt, leave the bold off.

### What stays bolded (existing patterns that work)

- **Reality Check callout**: neighborhood names and the price range inside the callout. The callout is its own scoped context.
- **Fit-section bullet lead-ins**: the label-style topic phrase at the start of each "Yes if / No if" bullet ("Healthcare matters more than weather.", "You won't go suburban.", etc.).
- **Hood-card median/range sentences**: whole-clause information bolds ("Median: ~$538K, with the largest historic homes well above.").
- **Hood-card sub-area anchors**: proper nouns named within the hood-card body (Ladue, Frontenac, Wildwood, Oakville).
- **Hoods-intro disclaimer**: "Pricing reflects May 2026 estimates and varies by municipality, block, and lot."
- **Method-callout label**: "Reading the numbers here:".
- **Cost-strip labels**: Property tax:, Home insurance: (label-only per #3 above).
- **Health-card named designations**: "Honor Roll" or similar named credentials, when they appear in the health-detail prose.
- **Visit block, two anchors**: one credential or standout fact in the hook, and the neighborhood names in paragraph 2, and nothing else. Never bold the tradeoff/caveat, the Expedia or Vrbo lines, or the disclaimer; bolding a caveat undoes the block's confident tone. Roughly four to five bolds per block (one hook anchor plus three to four neighborhoods). This is the Visit-block application of the item-6 pass.

### What gets stripped during a bolding pass

- **Anchor bolds for proper nouns covered elsewhere.** If a neighborhood gets its own hood card, or appears in the Reality Check callout, or sits in a fast-facts aside, or headlines a day-card, don't bold its body-prose appearance. The card / callout / fast-fact IS the anchor.
- **Names in passing illustrative lists.** Lists like "the retirees who land here happily go suburban, Chesterfield, Kirkwood, Webster Groves, Clayton, where the math is different" are illustration, not anchor territory. Don't bold the items.
- **Partial-clause fact bolds.** Don't bold fragments like "the largest city in Ohio" or "$253K citywide typical home value" or "more than 200 working fountains" inside otherwise plain sentences. Either the fact warrants a complete-clause information bold (rare) or it doesn't earn a bold.
- **Sub-institution names in health-detail prose.** The health-card already gives the primary institution prominent styling. Don't add inline bolds for sub-units (e.g., "Mid-America Heart Institute" within Saint Luke's detail).

### What gets added during a bolding pass

In the **character section** body prose (the "About this city" overview after the hero), add **1-2 topic-sentence whole-clause bolds** that capture a unifying insight, the sentence a reader would want to remember after closing the page.

Examples from canonical profiles:

- **St. Louis**: *"The metro is structured by an emphatic City-County divide."* (topic-sentence) and *"What unites all of them is Forest Park"* (connective tissue between paragraphs)
- **Columbus**: *"What that steady growth bought, over time, was a real city's worth of culture without a big city's price tag."* and *"And running underneath everything is the medical engine."*
- **Pittsburgh**: *"The healthcare story is what brings most retirees here."* and *"What's surprising is the math."*
- **Philadelphia**: *"But Philadelphia's defining trait, for a retiree, is its contradictions."* and *"That combination, affordable, walkable, cultured, medically deep, is what makes Philadelphia quietly one of the best urban retirement values in the country."*

Don't force two. If a profile only has one clear unifying insight, one bold is better than a weak second. (Kansas City has only one, the P3 closer "The whole package is what a major coastal metro costs minus the coast.")

Don't add character-section bolds in the first paragraph if it carries a dropcap. The dropcap is the visual entry; competing with it adds noise.

### What never gets bolded

- Adjectives or subjective descriptors on their own: "walkable," "vibrant," "affordable," "underrated"
- Verbs or process language
- Generic nouns when not used as proper names: downtown, the river, the airport, the hospital
- Anything inside a pull quote, blockquote, or callout other than the Reality Check
- Anything inside a day-card body (the day-activity headline is the card's anchor)
- The hero tagline (the hero is the visual emphasis)

---

## Em-dash policy

**Zero em-dashes in body prose, meta tags, JSON-LD, and visible UI text.** Em-dashes (`—` literal or `&mdash;` entity) read as an AI-generated writing signal and undercut the editorial voice. They are not permitted in any rendered content, including but not limited to: hero taglines, fit-section bullets, character paragraphs, fast-facts, day cards, hood-card descriptions, healthcare detail, lifestyle banners, related-city blurbs, CTA copy, footer credits, page titles, meta descriptions, Open Graph tags, and JSON-LD `headline` / `description` / FAQ answers.

### Replacement choices

The right substitute depends on what the em-dash was doing. In order of preference:

- **Period + new sentence** when the clauses are independent and stand on their own. *"Strong regional anchor for a city its size. Portland is the backup for complex specialty care."*
- **Comma** for parenthetical or apposition where the rhythm is light. *"a National Historic District, walkable to Pack Square in 10 minutes"*
- **Colon** when the em-dash was introducing examples, a definition, or amplification. *"Mission is the regional anchor: a Level II trauma center, the largest hospital in western North Carolina"*
- **Parentheses** for wrapped clauses that genuinely interrupt the sentence. *"The Old Mill District (once a lumber mill complex) is now a riverside walking grid."*
- **Semicolon** is acceptable but used sparingly; prefer a period when the clauses can break cleanly.

### Structural label-and-amplification patterns take colon

Elements whose function is "label + amplification" (a short noun phrase followed by an explainer) take a colon when the em-dash would sit between them. This applies to:

- `<span class="cost-qualifier">` (e.g., *"State averages: local rates and exemptions vary"*)
- `<div class="stat-sub">` (e.g., *"UVA Health: Virginia's #1 hospital"*)
- `<div class="section-eyebrow">` and `<div class="section-title">`
- `<div class="fast-fact-desc">`, `<div class="list-card-tier">`, `<div class="day-activity">`
- `<div class="hero-tagline">` when it contains a single em-dash (paired em-dashes in hero-tagline are handled as parentheticals, comma-comma)

Page title pattern `City, State — A Retirement City Profile` takes a colon in `<title>`, JSON-LD `headline`, and og:title meta.

### What about en-dashes and hyphens?

- **En-dashes (`–` / `&ndash;`)** are fine for numeric and date ranges (*"$420K&ndash;$575K"*, *"2025&ndash;26"*) and stay.
- **Hyphens (`-`)** in compound modifiers (*"NCI-designated"*, *"retiree-target"*) stay.

### CSS and HTML comments

Comments inside `<style>` blocks and `<!-- ... -->` HTML comments are non-rendered and don't violate the policy in practice. New profiles should still use `--` instead of `—` inside comments for consistency, but legacy comments carrying em-dashes are cosmetic only and do not require sweeping unless touched.

### Day-time placeholder

Day cards with "Anytime" timing use `<div class="day-time">–</div>` (en-dash) as the placeholder. The en-dash reads cleanly as a "no specific time" typographic marker and matches the intent of the "Anytime" day-name. Legacy profiles used em-dash; the June 28-29 sweep converted all day-time em-dashes to en-dashes. New profiles should follow the same convention.

### Sweep status

The policy is enforced going forward. Retroactive sweep is complete.

- **Swept (zero em-dashes in rendered content):** all 38 published profiles as of June 29, 2026.
- **Swept (guides):** all five guide pages as of July 14, 2026: `value-navigator`, `active-frontier`, `wellness-blueprint`, `globetrotter-guide`, `urban-walkabout`. 231 rendered em-dashes replaced per the substitution rules above.
- **Enforcement:** the guides are now inside the validator's em-dash check (`GUIDES_TOO = True` in `tools/validate.py`). Before July 14, 2026 that flag was `False` with a comment claiming the guides were "grandfathered; see PROFILE-FORMATTING.md". This document never said that. Its scope is profiles. The flag was recording an unfinished job in the grammar of a decision, and the em-dash rule now applies to every rendered surface on the site with no exemptions.
- **Legacy comments preserved:** 207 em-dashes inside `<style>` and `<!-- ... -->` blocks retained (non-rendered).

Touch any profile during future edits and confirm no em-dash reintroduction via the QA checklist.

---

## Neighborhood Reality Check callout

A Neighborhood Reality Check callout sits above the fold on any profile where the citywide ZHVI figure would understate the realistic budget for retiree-target neighborhoods. It is a universal editorial mechanism, not a property of a fixed roster of cities. Any profile may carry one, and the call is made at build time.

`MEDIAN-HOME-METHODOLOGY.md` v1.2 section 4 is the governing test for **when** a callout is warranted. This document governs only its **structure and placement**.

**Do not maintain a list of NRC cities in this document.** Versions 1.2 through 1.5 enumerated ten. That list was stale within a month, ran seven cities behind by late July, and named Wilmington DE, which has no profile and therefore never carried a callout at all. The enumeration of record is the live repo:

```bash
grep -l 'reality-check-eyebrow' cities/*/profile.html
```

That returned 17 profiles on July 25, 2026.

### Structure

The callout sits between the stats-bar (if present) and the cost-strip:

```html
<!-- NEIGHBORHOOD REALITY CHECK — per MEDIAN-HOME-METHODOLOGY.md v1.2 -->
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
> The $235K citywide median reflects significant variation across St. Louis. The neighborhoods retirees typically target in the city, **Tower Grove South**, **Central West End**, **Soulard**, **Lafayette Square**, run roughly **$420K–$575K**. Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice.

**Kansas City:**
> The $253K citywide median is the Kansas City, Missouri figure. Retiree-target neighborhoods, **the Plaza**, **Brookside**, **Waldo**, and the Kansas suburbs (**Mission Hills**, **Leawood**, **Overland Park**), run **$300K–$900K**, with premier Kansas enclaves into seven figures. Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice.

**St. Paul:**
> The $297K citywide median is the St. Paul figure. Retiree-target neighborhoods, **Highland Park**, **Macalester-Groveland**, **Summit Hill**, and **St. Anthony Park**, run **$415K–$550K**. Use the citywide figure as a starting reference; the realistic budget depends on neighborhood choice.

---

## QA checklist for any profile being touched

- [ ] `<meta name="color-scheme" content="light">` in `<head>`
- [ ] `html { ... color-scheme: light; }` in CSS
- [ ] Forced-dark hardening `@media (prefers-color-scheme: dark)` block present just before `</style>`
- [ ] `.cost-strip` CSS uses `flex-start` and `left`
- [ ] Property tax / Home insurance lines bold the labels, not the values
- [ ] `.hood-card:hover` is wrapped in `@media (hover: hover) { ... }`
- [ ] No `<p class="week-intro">…</p>` in the week-section
- [ ] Visit block present, with matching Visit chip in the last nav position and `'visit'` in the scroll-spy ids array
- [ ] Visit block follows the voice standard: unique concrete hook (positive-led, tradeoff woven not front-loaded), varied neighborhood and rental openers, canonical closer verbatim
- [ ] Visit block bolding: one hook anchor plus neighborhood names only; nothing bolded on the caveat, the Expedia/Vrbo lines, or the disclaimer
- [ ] Deep Dive Reports block in the lower cluster (after Related Cities), not after the stats bar
- [ ] Quiz copy says "the quiz" with no question count
- [ ] No anchor bolds for proper nouns covered in callouts, hood cards, fast-facts, or day-card headlines
- [ ] No partial-clause fact bolds in body prose
- [ ] Character section has 1-2 topic-sentence whole-clause bolds (or 1 if no clear second insight)
- [ ] NRC callout present (if city is one of the 10 NRC cities)
- [ ] **Zero em-dashes** (`—` or `&mdash;`) in body prose, meta tags, JSON-LD, or visible UI. Period / comma / colon / parentheses depending on context. Day-time "Anytime" placeholders use en-dash `–`, not em-dash. See Em-dash policy section.
- [ ] Strong tag balance: `<strong>` count equals `</strong>` count

---

## Working principle

When something feels uncertain, the answer is in the St. Louis profile. If St. Louis doesn't have an example of the case in question, lean toward fewer bolds rather than more. The risk of over-application is much higher than the risk of under-application.
