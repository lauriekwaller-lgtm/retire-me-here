# RetireMeHere — Profile Template Conventions (post-cleanup)

These are the design conventions settled after the May 2026 "de-tell" pass across
all 27 city profiles. The goal: keep the editorial, content-forward look while
removing the design patterns that read as AI-generated and that made profiles
feel repetitive across cities. Apply these to Sarasota's successors and any
future city so the patterns never creep back.

## What we removed, and why

1. **No pull-quote in the character section.**
   The old `<aside class="pullquote">` re-stated a sentence that already appeared
   in the adjacent body text, under a big decorative quote mark with a fake
   attribution ("— On [city]'s preservation"). That non-attribution was the
   single strongest "AI-generated editorial" signal, and the repetition was the
   literal source of the "repetitive" feedback. The character section's aside
   now holds ONLY the `fast-facts` card (real data: founding year, a key date,
   a healthcare fact). Data is a credibility anchor; a repeated quote is not.

2. **Detail-photo break is a CAPTION, not a quote.**
   The old version had a 90px decorative quote mark + an italic "quote" + a fake
   "— On the historic peninsula" attribution. It's now a small uppercase label
   (`detail-eyebrow`) above an upright descriptive caption (`detail-quote`,
   font-style: normal). It reads as a photo caption written by a person, not a
   fabricated pull-quote.

3. **Dropcap is upright and dark, not italic terra-cotta.**
   Kept the dropcap (it's nice), but `font-style: normal; font-weight: 500;
   color: var(--dark)`. The italic-colored version paired with a pull-quote was
   squarely in the generated-editorial cluster.

## Heading emphasis rule (the important judgment call)

The `<em>` inside `.section-title` renders italic + teal. The OLD template put it
on ALL SIX content headings in every city, plus the CTA. Having every heading do
the same italic move — in the same positions — across 27 cities was itself a
template signature and a big part of why the site felt repetitive.

**New rule — emphasis is earned, not automatic. Keep `<em>` only on:**

- **The Fit heading** — "Is [City] *for you*?" The emphasis is the question's point.
- **The Character heading** — the city's DISTINCT editorial hook. This is the one
  that should differ most city to city: "the small town that *got rich*"
  (Bentonville), "a city that *taxes itself* to stay this way" (Boulder),
  "a town built on *Jefferson's idea*" (Charlottesville). This is where voice lives.
- **The CTA** — "[City] might fit. *Or it might not.*" Real rhetorical rhythm.
- **A healthcare heading ONLY if it carries a genuine honest-tradeoff beat** —
  e.g. "...and an *honest caveat*" (Bentonville), "...a *2 a.m. drive to ABQ*"
  (Santa Fe), "...with academic backup *an hour north*" (Bloomington). These show
  a human weighing a real downside, which is on-brand.

**Always make these PLAIN (no `<em>`):**

- "A week in [City], roughly." (the "roughly" italic was a cute tic)
- "Four [City]s, depending on you." (mechanical)
- "[N] lists where [City] earned its place." (mechanical)
- Flat-label healthcare headings with no tradeoff: "medical capital,"
  "regional anchor," "medical powerhouse," "medical city." A bare label isn't
  an emphasis, it's a fact — set it plain.

Net result per city: usually 3 emphasized headings (Fit + Character + CTA),
sometimes 4 when the healthcare line has a real beat. Never 6.

## What we deliberately KEPT (these are credibility anchors — do not remove)

- Photo credits (hero, detail, lifestyle) and the footer source citations.
- City-specific factual detail: named neighborhoods with pricing, opening dates,
  flood-risk honesty, real hospital names and rankings.
- The stats bar, sample-week grid, neighborhoods grid, healthcare card — these
  are content-justified and the real data inside them is what separates a
  researched profile from AI slop.

## Quick checklist for a NEW city profile

- [ ] No `<aside class="pullquote">` anywhere. Aside-stack holds fast-facts only.
- [ ] Detail-photo break uses `detail-eyebrow` label + upright `detail-quote`
      caption. No decorative quote mark, no "— On the..." attribution.
- [ ] Dropcap is upright/dark (font-style: normal, color: var(--dark)).
- [ ] Headings: emphasis only on Fit, Character hook, CTA, and (optionally) a
      healthcare line with a real tradeoff. Everything else plain.
- [ ] Make the Character hook genuinely specific to THIS city — that's the line
      doing the editorial work now that the pull-quote is gone.
