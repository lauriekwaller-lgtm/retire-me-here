# RetireMeHere City Profile — Template Specification

**Use this doc as context when starting a new chat to build a city profile.** Paste the relevant sections at the top of the conversation along with the latest template HTML and city photos.

---

## How to use this in a new chat

Open with something like:

> "I'm building city profile pages for retiremehere.com using a template we developed. Attached are:
> 1. The latest template (Pittsburgh or Boulder profile HTML)
> 2. Three photos for [CITY NAME], [STATE] (hero, lifestyle, detail)
> 3. The city database spreadsheet
>
> Build the profile following the template architecture exactly — same sections, same styling, same photo flow. Verify city data from the database. Match the design decisions captured in the template specification I'm pasting below."

Then paste **Sections 2 through 6** of this doc.

---

## 1. Project Background

**Site:** retiremehere.com — a quiz-based retirement city matching tool
**Operator:** Solo developer (Laurie)
**Database:** ~100 U.S. cities scored across 9 dimensions, hosted in Google Sheets
**Architecture:** Single-file HTML for the homepage + landing pages + individual city profiles
**Deployment:** GitHub → Netlify auto-deploy

**Existing landing pages (7):** Active Retirees, Arts Lovers, Foodies, Healthcare, Hikers, LGBTQ+ Retirees, Sports Fans

**Two completed city profiles serve as templates:**
- `boulder-co-profile.html` (verified by 4-year resident)
- `pittsburgh-pa-profile.html` (built but contact verification pending at time of writing)

---

## 2. Brand Identity

### Typography

- **Body / sans-serif:** DM Sans (400, 500, 700) — used for body copy, labels, navigation, UI elements
- **Display / serif:** Fraunces (300, 400, 500 — italic and roman) — used for headlines, city names, pull-quotes, fast-fact numbers
- **Brand wordmark:** Libre Franklin (700, 800) — used only for "RETIREMEHERE" logo

### Color Palette (CSS Variables)

```css
--teal: #2A5E5A;        /* Primary brand */
--teal-mid: #3d7a75;    /* Secondary */
--teal-deep: #1f4744;   /* Strong/dark CTAs */
--terra: #C4724A;       /* Accent — eyebrows, highlights */
--terra-soft: #E89F75;  /* Soft accent */
--sand: #F7F3ED;        /* Section background */
--cream: #FBF7F1;       /* Section background */
--paper: #FFFCF5;       /* Body background */
--dark: #1C1A18;        /* Text primary, dark sections */
--mid: #5C5852;         /* Text secondary */
--light: #8B867E;       /* Text tertiary */
--gold: #D4A84B;        /* Accent — pull-quotes, premium feel */
--line: #ECE6DC;        /* Borders, dividers */
```

### Brand wordmark

```html
<span class="retire">RETIREME</span><span class="here">HERE</span>
```
- "RETIREME" in teal `var(--teal)`
- "HERE" in terra cotta `var(--terra)`
- Letter-spacing 0.18em, weight 800

---

## 3. Page Architecture (City Profile)

Sections in order — DO NOT REORDER:

1. **Sticky Header** — Wordmark left, nav + CTA right
2. **Hero** (70vh, full-bleed photo) — Eyebrow, city name, state, tagline, photo credit
3. **Stats Bar** — 4 cells overlapping the bottom of the hero (-56px margin-top)
4. **Is [City] for you?** — Two-column "love it / skip it" with intro paragraph
5. **Character of the Place** — Long-form prose (left column) + pull-quote AND fast-facts card (right column)
6. **Detail Photo Break** — Dark full-width section, photo left + atmospheric quote right
7. **Sample Week** — 8 day-cards in 4-column grid (Mon-Sun + "Anytime"), sand background
8. **Lifestyle Photo Banner** — Full-bleed (56vh), eyebrow + italic title overlay
9. **Neighborhoods** — 4 cards with vibe tags, descriptions, median home prices
10. **Healthcare Deep-Dive** — Dark callout card with hospital name, detail, score
11. **Appears On Lists** — 3 cross-link cards to relevant landing pages (NO rank numbers)
12. **Quiz CTA** — Teal section with gold button
13. **Footer** — Photo credits + sources

---

## 4. Photo Flow (Critical Design Lesson)

**Rule:** Never stack two photo sections back-to-back. The pattern is:

```
Hero (photo) → Stats → Text → Text → Detail Break (photo) → Text → Lifestyle Banner (photo) → Text → Text
```

- **Hero** = the iconic postcard shot of the city
- **Lifestyle** = scene with people / energy / daily life
- **Detail** = closer, atmospheric, often portrait orientation OK

### Photo Specs
- **Resize to 1600px wide max** before deploying (Mac Preview → Tools → Adjust Size)
- **Filename convention:** `[city-state]-[shottype].jpg`
  - Examples: `boulder-co-hero.jpg`, `pittsburgh-pa-lifestyle.jpg`
- **Source:** Unsplash, Pexels, Wikimedia Commons preferred for early-stage
- **License attribution:** Credit photographer + source in HTML photo credit overlay AND in footer

### Photo Credit Position (Standardized)
- **Hero photo credit:** Bottom-right of hero, raised to `bottom: 92px` to clear stats bar overlap. Has dark blur pill background.
- **Lifestyle photo credit:** Bottom-right of banner
- **Detail photo credit:** Bottom-right of detail photo half

---

## 5. Content Guidelines

### Voice & Tone
- **Editorial, magazine-style** — like Travel + Leisure or NYT Real Estate, NOT like Forbes "10 Best" listicles
- **Honest, even when critical** — talking openly about wildfire risk, expensive housing, weather downsides differentiates RetireMeHere
- **Specific over general** — "Mt. Sanitas, 3.1 miles round-trip" beats "great hiking nearby"
- **Use real data from the database** — pros, cons, healthcare facts, scores

### Section-by-Section Content Rules

**Hero tagline:** One sentence, italic, captures the city's defining quality in evocative language.
- Boulder: *"Where the Front Range begins, retirement keeps moving, and the Flatirons are always watching over the day."*
- Pittsburgh: *"Three rivers, hundreds of bridges, world-class hospitals, and a value-to-substance ratio that retirees figure out before everyone else does."*

**Stats bar (4 cells):**
1. Median Home (target neighborhoods, not citywide)
2. Monthly Budget
3. Weather (key descriptor + elevation/sun days)
4. Healthcare (hospital name)

**Is [City] for you? — 4 pros, 4 cons each, with bold lead phrases.** Real tradeoffs, not fluff.

**Character section:**
- ~3 paragraphs of editorial prose with drop cap on first letter
- One sentence in bold per paragraph for visual rhythm
- Pull-quote on right side WITH attribution like "— On [topic]" (NOT fake person quotes)
- Fast-facts card below pull-quote: 3 distinctive numbers per city

**Detail break quote:** Single observation about the city's defining quality, attributed thematically (e.g., "— On Pittsburgh's value proposition")

**Sample week:** 7 days + "Anytime" card. Each card has:
- Day name
- Time
- Activity
- Where/what (1-2 sentences)
- **Honest framing in intro:** "A composite week of what an active retiree's days could look like — drawn from neighborhood patterns..." (NEVER claim "interviews" unless real interviews happened)

**Neighborhoods:** 4 cards, each with:
- Name
- Vibe tags (3 short descriptors separated by ·)
- Description (2-3 sentences)
- Bold median home price range

**Healthcare card:** Single big dark card. Hospital name, what's notable, healthcare score from database.

**Appears On lists:** 3 cards, NO rank numbers (just landing page name + tier/score subtitle).

**Footer:** Photo credits with photographer names + Unsplash/Pexels source. Sources line listing data origins.

### What NEVER appears on a city profile page

- ❌ **Scores grid** — users who took the quiz already trust the match; scores are clutter
- ❌ **Rank numbers on "Appears on" cards** — meaning is unclear ("Boulder is #3 at... what?")
- ❌ **Sticky pull-quote** — gets in the way during scroll
- ❌ **Fake retiree quotes** — only use thematic attributions until real contacts are interviewed
- ❌ **Two photo sections back-to-back** — always interleave with text

---

## 6. Critical Link Patterns

**Use absolute paths for cross-page links.** When a city profile links to landing pages (Active Retirees, Hikers, etc.) or back to the homepage, use paths starting with `/` — NOT relative paths like `../` or `../../`.

Examples:
- ✅ Correct: `<a href="/top-cities-for-foodies.html">`
- ❌ Wrong: `<a href="../top-cities-for-foodies.html">` (only works one level deep)
- ❌ Wrong: `<a href="../../top-cities-for-foodies.html">` (depends on folder depth)

**Why:** City profiles live at `cities/[city-slug]/profile.html` (two levels deep). Absolute paths starting with `/` work from anywhere. Relative paths break when folder depth changes.

**Photo references** (within a profile.html file) DO use relative paths because photos live in the same folder as the HTML:
- ✅ Correct: `url('hero.jpg')`
- ❌ Wrong: `url('/cities/boulder/hero.jpg')` (works but ties to a specific city — bad for templating)

**Canonical URL** in the `<head>`:
- Should match actual deployed URL: `https://retiremehere.com/cities/[city-slug]/profile.html`
- Common mistake: leaving the previous city's canonical URL when cloning the template

---

## 7. Critical CSS Patterns

### CSS Specificity Gotcha
The header CTA button needs the selector `.header-nav a.header-cta` (NOT just `.header-cta`) because the parent rule `.header-nav a` has higher specificity (0,1,1) than `.header-cta` alone (0,1,0). Without this fix, the CTA text renders as dark gray on dark teal — invisible.

### Section padding
- **Default `.section` padding:** 64px top/bottom
- **Sections bordering the photo break (Character, Week):** 48px on the photo-break-facing side
- **Healthcare section explicit override:** `padding-bottom: 64px`
- **Mobile:** Reduce to 56px

### Hero spacing
- `padding: 0 48px 88px` on `.hero-content` — 88px bottom keeps content above stats bar overlap
- Hero name: `margin-bottom: 4px`
- Hero state: `margin-bottom: 16px`
- (Tighter than default to keep tagline visible above stats bar)

### Text-wrap balance
Apply to `.hero-name`, `.hero-tagline`, `.section-title`, `.lifestyle-banner-title`, `.cta-h2` — prevents orphaned words on hero headlines.

### Mobile breakpoint
`@media (max-width: 880px)` — stacks 2-column layouts, reduces padding, simplifies nav.

---

## 7. Workflow Checklist for Each New City

When building a city profile from scratch:

1. **Pull real data from the database** — scores, prices, monthly budget, healthcare ranking, character, highlight prose
2. **Verify data freshness** — run searches for hospital rankings, AARP lists, current data points if more than 6 months old
3. **Get 3 photos** — hero (postcard), lifestyle (people/energy), detail (atmospheric/portrait OK)
4. **Resize photos to 1600px wide, rename to `[city-state]-[shottype].jpg`**
5. **Clone the latest template HTML** (most recent verified version)
6. **Update meta:** title, description, canonical URL
7. **Update photo references in CSS** (3 references for hero/lifestyle/detail backgrounds)
8. **Update content section by section:**
   - Hero (city name, state, tagline, photo credit)
   - Stats bar (4 cells with real data)
   - Is This For You (4 pros, 4 cons)
   - Character (3-paragraph prose, drop cap, pull-quote, fast-facts card with 3 numbers)
   - Detail break (atmospheric quote + thematic attribution)
   - Sample week (8 day-cards with real activities)
   - Lifestyle banner (eyebrow + italic title)
   - Neighborhoods (4 cards with prices)
   - Healthcare card (hospital name, ranking, score)
   - Appears On (3 cross-links, no rank numbers)
   - Quiz CTA ("[City] might fit. Or it might not.")
   - Footer (photo credits, sources)
9. **Verify NO leftover content from template city** (search for previous city's name)
10. **Get verification from local contact when possible** before publishing

---

## 8. Friends-and-Family Contact List (Cities Where Verification Available)

Already organized by landing page coverage value:

🥇 **Madison, WI** — 6 of 7 landing pages
🥈 **Pittsburgh, PA** — 5 of 7 landing pages (mockup built, awaiting verification)
🥉 **Alexandria, VA** — 3 of 7 landing pages (Laurie lives there)

Other contact-list cities:
Bloomington, Lexington, Tucson, Sun Valley, Park City, Fort Collins, Carlsbad, Virginia Beach, Scottsdale, Bozeman, Fort Worth, Bend, Flagstaff, Vail, Miami, Iowa City, Sedona, Salt Lake City, Kansas City

---

## 9. Deployment

**URL structure:** `retiremehere.com/cities/[city-name]/profile.html`
- Each city gets its own subfolder under `/cities/`
- Folder name uses just the city slug (e.g., `boulder`, `pittsburgh`, `madison`) — no state suffix needed since folders are isolated namespaces
- Photos go in the same per-city subfolder as `profile.html`
- Photo filenames are simple within each folder: `hero.jpg`, `lifestyle.jpg`, `detail.jpg`

**Folder structure example:**
```
cities/
├── boulder/
│   ├── profile.html
│   ├── hero.jpg
│   ├── lifestyle.jpg
│   └── detail.jpg
├── pittsburgh/
│   ├── profile.html
│   ├── hero.jpg
│   ├── lifestyle.jpg
│   └── detail.jpg
```

**HTML photo references** stay simple because they're relative to the same folder:
- `url('hero.jpg')` not `url('cities/boulder/hero.jpg')`

**Per-city deploy steps:**
1. Create `cities/[city-slug]/` folder in GitHub
2. Upload `profile.html` + 3 JPGs (hero, lifestyle, detail) into the city's subfolder
3. Add new URL to `sitemap.xml`: `https://retiremehere.com/cities/[city-slug]/profile.html`
4. Update `PUBLISHED_PROFILES` in `index.html`: `'CityName_ST': 'cities/[city-slug]/profile.html'`
5. Update relevant landing pages so the city's name links to the new profile
6. Netlify auto-deploys in ~30 seconds

---

## 10. Known Open Items / Future Improvements

- Once 5+ city profiles exist: consider data-driven JSON architecture so updates are centralized
- Real local quotes from verified contacts replace thematic attributions over time
- Mini-quiz CTA at top of profile pages (alternative to "Find My Match" button)
- Schema.org structured data for better SEO once SEO becomes a priority
- Pinterest pin generation per city profile

---

## 11. Scoring System — Known Issues & Decisions

The matching engine uses 9 active dimensions: D1 (Airport), D3 (Healthcare), DC (Weather), D5 (Tax), D6 (Walkability), D7 (Outdoor), D8 (Sports/Fitness), D9 (Safety), D10 (Community).

### Resolved decisions (do not revisit without new info)
- **D2 (Cost of Living)** removed from user priorities grid; budget step + bonus handle affordability
- **D4** was a phantom dimension; decision: remove entirely. Verify cleanup completion in master tracker.
- **"Value for Money" as user-weighted dimension** — rejected. Wouldn't differentiate users.
- **"Not Important" weight = 0** — dimensions marked "Not Important" are skipped in scoring loop
- **+6 budget bonus** — kept as primary affordability mechanism
- **Climate → Weather** — wording change in user-facing UI (May 2026)

### Deferred to "Phase 2"
- **Relative D2 scoring** — make D2 score relative to user's budget range instead of absolute. Deferred until traffic justifies. Trigger to revisit: meaningful traffic + user feedback that results feel off for high-budget users.

### Future enhancements tracked in `RetireMeHere-Implementation-Plan.md`
- Household size question (solo vs. couple)
- D8 sub-component restructure (golf, pickleball, gyms, rec)
- Spectator sports as Community input
- Biking as Walkability input
- Manual data spot-check on Sports & Fitness scoring
- "Adjust Priorities" jump-back button on empty results
- **FE-6:** Neighborhood-level walkability nuance — D6 collapses neighborhood variation
- **FE-7:** Broader dimension-scoring audit — periodic gut-check on Healthcare, Safety, etc.

### Special scoring mechanics worth knowing
- **Budget filter:** hard filter `budgetRange <= quizState.budget + 2` eliminates cities above range
- **Budget bonus:** up to +6 points for perfect budget alignment
- **Four Seasons climate:** special handling so cities with brutal winters (Bozeman, Park City) score well when user wants Four Seasons

For full status, refer to `retiremehere-master-tracker.md` Section 4.

---

*Last updated: May 2026. Based on the template architecture finalized for Boulder, CO and Pittsburgh, PA.*
