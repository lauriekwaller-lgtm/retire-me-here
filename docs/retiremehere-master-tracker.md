# RetireMeHere — Master Project Tracker

**Owner:** Laurie Waller
**Last updated:** May 10, 2026 (multiple updates today)
**Purpose:** Single source of truth for all open items, processes, and reference docs across the RetireMeHere project. Save this somewhere durable (Google Drive, GitHub `/docs` folder, or your project repo).

---

## How to use this document

This is your project home base. When you start a new chat or come back to the project after time away, **start here.** Everything else flows from this document.

**Update this doc when:**
- You complete an item (move it to "Completed")
- A new item comes up
- You start a new chat for a specific work session

**Reference this doc when:**
- Starting a new chat — paste relevant sections as context
- Deciding what to work on next
- Answering "what's the status of X?"

---

## 📍 SECTION 1 — Current Status

### What's live on retiremehere.com (as of May 4, 2026)
- ✅ Homepage (`index.html`) — quiz, matching engine, results page
- ✅ 7 landing pages (Active Retirees, Arts Lovers, Foodies, Healthcare, Hikers, LGBTQ+, Sports Fans)
- ✅ Sitemap submitted to Google Search Console
- ✅ MailerLite forms (5 free reports)
- ✅ Google Analytics tracking (`G-BTL743DSJQ`)

### What's built but NOT yet live
- 🟡 **Boulder city profile** — verified by 4-year resident, ready to deploy
- 🟡 **Pittsburgh city profile** — built, awaiting contact verification

### Database stats
- **100 cities** scored across 9 dimensions
- **22 cities** with personal contacts available for verification
- **Storage:** Google Sheets (migrated from Excel May 2026)

---

## 📍 SECTION 2 — Open Items (Action Required)

### THIS WEEK
- [ ] **Save key documentation to durable storage** (Google Drive `/RetireMeHere/Docs` or GitHub `/docs` folder)
  - This master tracker
  - `city-profile-template-spec.md`
  - `RetireMeHere-Implementation-Plan.md` (v1.1 from April 29, 2026)
  - `pinterest-pin-briefs.md`
  - `foodie-cities-scoring-analysis.md`
  - `active-retirees-cities-scoring-analysis.md` (consolidated May 10, 2026 — supersedes 4 fitness-culture-*.md drafts)
- [ ] **Send Pittsburgh ZIP to your Pittsburgh contact** for verification
- [ ] **Find a Boulder verifier contact** (still searching)
- [ ] **Verify D4 phantom dimension was fully removed** from database spreadsheet (see Section 5)
- [ ] **Document missing landing-page selection criteria** (see new section below)

### LANDING PAGE METHODOLOGY DOCS — GAP TRACKER

Two landing pages have written selection-criteria documents. Five do not. This means decisions about who's on/off each list are not defensible from a rubric — each "why isn't X on this list?" question becomes a fresh argument instead of a lookup.

| Landing Page | Methodology Doc | Status |
|---|---|---|
| Foodies | `foodie-cities-scoring-analysis.md` | ✅ Done |
| Active Retirees | `active-retirees-cities-scoring-analysis.md` | ✅ Done (consolidated May 10, 2026) |
| Hikers | (none) | 🟡 In progress — being built in current conversation about St. George |
| Arts Lovers | (none) | ❌ Missing |
| Sports Fans | (none) | ❌ Missing |
| LGBTQ+ Retirees | (none) | ❌ Missing — highest priority due to editorial sensitivity |
| Healthcare | (none) | ❌ Missing — partly covered by D3 scoring rubric, but no list-specific doc |

**Two approaches for closing the gap:**
- **Option A — Reverse-engineer:** Analyze the cities currently on each list, find the pattern, document the rubric to match. Fast but retrofits.
- **Option B — Build properly:** Decide criteria first, then audit the current list against it. May require adding/removing cities.

**Suggested order to tackle remaining 4:**
1. **LGBTQ+ Retirees** — most editorially sensitive, highest defensibility need
2. **Sports Fans** — currently in flux (Scottsdale just added), good time to lock in criteria
3. **Arts Lovers** — well-defined category, probably easier
4. **Healthcare** — mostly defensible via D3 already; document as supplementary

Each is ~30 minutes of focused conversation. Don't try to do all four in one session.

### WHEN YOU PUBLISH BOULDER (first city profile)
- [ ] Decide URL structure — recommended: `retiremehere.com/cities/boulder-co.html`
- [ ] Create `cities/` folder in GitHub repo
- [ ] Upload Boulder HTML + 3 photos to `/cities/` folder
- [ ] Add Boulder URL to `sitemap.xml`
- [ ] Update relevant landing pages (Active Retirees, Hikers, Arts Lovers) to make "Boulder" clickable, linking to the new profile
- [ ] Re-ping Google Search Console with updated sitemap
- [ ] Repeat process for Pittsburgh once verified

### ANYTIME, NO RUSH
- [ ] **Pinterest pins** — 18 pin briefs ready in `pinterest-pin-briefs.md`. Design in Canva.
- [ ] **Domain forwarding** for `destinationretired.com` and `wheretoretireus.com` → retiremehere.com
- [ ] **MailerLite sender email** update to `hello@retiremehere.com`; verify sending domain

### NEXT CITY PROFILES (priority order)
- [ ] **Scottsdale, AZ** — building tomorrow. While building, also add Scottsdale to `top-cities-for-sports-fans.html` in the "Strong Sports Cities" tier. Editorial reasoning: Cactus League spring training (15+ MLB teams within 30 min radius), all 4 Phoenix-area pro teams accessible (Cardinals, Diamondbacks, Suns, Mercury), plus WM Phoenix Open at TPC Scottsdale. Justified by existing precedent — Fort Worth lists Dallas-area teams, St. Paul lists Minneapolis teams, both via metro proximity. Suggested team listing: *"Cactus League spring training · Cardinals · Diamondbacks · Suns · WM Phoenix Open"*.
- [ ] **Madison, WI** — 6 of 7 landing pages (highest cross-page payoff)
- [ ] **Alexandria, VA** — local knowledge, low research lift
- [ ] **Top 5 photo cities to continue:** Asheville, Charleston, Santa Fe, Bend (after Boulder photos in hand)

### NEW CITIES TO ADD TO DATABASE (candidates from prior chats — not yet scored)
These cities were identified as future additions in earlier chats but never scored or added to the database. Decide if/when to research and add:

- [ ] Bentonville, AR — Walmart HQ, growing arts scene (Crystal Bridges)
- [ ] Eureka Springs, AR — small artsy mountain town
- [ ] Cheyenne, WY — Mountain West, conservative-leaning option
- [ ] Iowa City, IA — University of Iowa Hospitals (world-class healthcare)
- [ ] Vancouver, WA — Portland-adjacent, no income tax (across river from OR)
- [ ] La Crosse, WI — Upper Midwest, river town
- [ ] Appleton, WI — affordable small Wisconsin city
- [ ] Eau Claire, WI — college town, growing arts scene
- [ ] Wichita, KS — Plains States representation
- [ ] Rapid City, SD — Mountain West / Black Hills, distinctive setting
- [ ] Winchester, VA — Shenandoah Valley, affordable Mid-Atlantic
- [ ] Providence, RI — New England, was discussed as a potential 101st city
- [ ] Hot Springs Village, AR — golf-heavy retirement community (was on earlier list)
- [ ] Saratoga Springs, NY — historic, arts, horse racing, was on earlier list

**Workflow when adding a city:** Score on 9 dimensions, add to database (Google Sheet + index.html), check which landing pages it could qualify for, add to those landing pages too. Profile page comes later as a separate workflow once verified by contact.

---

## 📍 SECTION 3 — Implementation Plan (from v1.1 doc, April 29, 2026)

This is a separate, detailed document: **`RetireMeHere-Implementation-Plan.md`** (v1.1)

If you don't have it saved durably, find it in past chat outputs and save now. Key sections:

### Phases
- Phase 1: Core fixes (D6 walkability reframing, etc.)
- Phase 2: Quiz language updates
- Phase 3: Tradeoff message updates
- Phase 4: Edge case handling
- Phase 5: Documentation

**Estimated total time:** 6-10 hours, spread across multiple sessions

### Deferred to "Future Enhancement Cycle" (FE)
1. **Household size question** (solo vs. couple) — would require new quiz step + budget recalibration
2. **D8 sub-component restructure** — splitting Sports & Fitness into named sub-scores (golf, pickleball, gyms, rec)
3. **Spectator sports as Community & Social Life input** — would require re-scoring all cities
4. **Biking as a Walkability & Transit input** — needs data audit
5. **Manual data spot-check on Sports & Fitness scoring**
6. **"Adjust Priorities" jump-back button** on empty-state results
7. **Neighborhood-level walkability nuance (FE-6)** — D6 collapses neighborhood variation into one number
8. **Broader dimension-scoring audit (FE-7)** — periodic gut-check on Healthcare, Safety, etc.

---

## 📍 SECTION 4 — Scoring System: Known Issues & Decisions

### Active dimensions (9 total — what the matching engine actually uses)
| Key | Dimension | Notes |
|-----|-----------|-------|
| D1 | Airport Access | |
| D3 | Healthcare Quality | |
| DC | Weather Preference | (was "Climate" — renamed for user clarity) |
| D5 | Tax Friendliness | |
| D6 | Walkability & Transit | Reframed as "car-free OR car-light" April 2026 |
| D7 | Outdoor Recreation | |
| D8 | Sports & Fitness | Sub-component restructure deferred |
| D9 | Safety | |
| D10 | Community & Culture | |

### Resolved decisions
- ✅ **"Not Important" weight = 0** — dimensions marked "Not Important" are now skipped entirely in scoring loop (April 17, 2026)
- ✅ **D2 removed from priorities grid** — Budget/Affordability no longer user-weighted; budget step + bonus handle affordability (April 8, 2026)
- ✅ **+6 budget bonus kept as-is** — primary affordability mechanism
- ✅ **D4 (phantom dimension) — decision: remove from system** — verify completion in Section 5 below
- ✅ **"Value for Money" rejected as separate dimension** — wouldn't differentiate (everyone wants value)
- ✅ **Climate → Weather wording change** in user-facing UI (May 2026)
- ✅ **Region step language updated** to surface family/community considerations (May 2026)

### Deferred to Phase 2 (when traffic justifies)
- ⏳ **Relative D2 scoring** — make D2 score relative to user's budget range instead of absolute
  - Rationale for deferral: low traffic, +6 budget bonus is doing the work for now
  - Trigger to revisit: meaningful traffic + user feedback that results feel off for high-budget users

### Open scoring concerns to monitor
- **D4 cleanup status** — verify D4 is fully removed from:
  - [ ] Database spreadsheet (column)
  - [ ] City objects in `index.html` (any `D4: X` entries in scores)
  - [ ] Scoring rubric document (v3.2)
- **D6 calibration** — recent reframing as "car-free OR car-light" may have left some scores too generous; periodic audit warranted
- **Healthcare/Safety scoring** — broader audit recommended to ensure threshold scores actually deliver what dimension promises

### Special scoring mechanics (not in dimension array)
- **Budget filter** — hard filter: `budgetRange <= quizState.budget + 2` eliminates expensive cities
- **Budget bonus** — up to +6 points for perfect budget alignment (primary affordability mechanism)
- **Four Seasons climate logic** — special handling so cities with brutal winters (Bozeman, Park City) aren't penalized for being "too winter-y" when user wants Four Seasons

---

## 📍 SECTION 5 — D4 Verification Checklist

D4 was a "phantom dimension" — data existed in city scores but matching engine never used it. Decision was to remove entirely. **Verify completion:**

```
Run these checks before considering D4 cleanup done:
```

- [ ] Open Google Sheets database → confirm no D4 column exists in City Database tab
- [ ] Open `index.html` → search for `D4` → confirm no `D4: X` entries in any city scores object
- [ ] Open scoring rubric doc → confirm D4 is absent or marked deprecated
- [ ] Confirm city detail pages don't reference D4 score in any UI

If any leftover D4 references exist, decide:
- **Option A:** Remove entirely (recommended — clean slate)
- **Option B:** Keep as `internalNotes.dailyCostScore` (invisible to users, available for editorial reference)

---

## 📍 SECTION 6 — City Profile Build Process

Every new city profile follows this workflow:

### Step 1: Pre-build checklist
- [ ] City exists in database with all 9 dimension scores
- [ ] City has rich `Highlight` text in database
- [ ] 3 photos sourced (hero/lifestyle/detail) — landscape preferred for hero
- [ ] Photos resized to 1600px wide, renamed `[city-state]-[shottype].jpg`
- [ ] Local contact identified (ideal) for content verification

### Step 2: Build
- Use `pittsburgh-pa-profile.html` or `boulder-co-profile.html` as template
- Follow `city-profile-template-spec.md` for design decisions
- Replace ALL city-specific content (search for previous city's name to verify)

### Step 3: Verify
- [ ] Send ZIP (HTML + 3 JPGs) to local contact for fact-checking
- [ ] Incorporate feedback before publishing

### Step 4: Publish

The full deployment requires uploads to **5 places** in your repo. Use this checklist for every new city:

#### Files to create/upload (in `cities/[city-slug]/`)
- [ ] `profile.html` (the city profile HTML)
- [ ] `hero.jpg`
- [ ] `lifestyle.jpg`
- [ ] `detail.jpg`

#### Files to update at repo root
- [ ] **`index.html`** — Add city to `PUBLISHED_PROFILES` object (e.g., `'Madison_WI': 'cities/madison/profile.html'`)
- [ ] **`sitemap.xml`** — Add new `<url>` entry pointing to `https://retiremehere.com/cities/[city-slug]/profile.html`
- [ ] **Each relevant landing page HTML** — Update the city card's `<a href>` to point to the new profile. Identify which landing pages by checking which lists the city appears on.

#### External steps
- [ ] **Google Search Console** — resubmit sitemap at search.google.com/search-console → Sitemaps section (optional but recommended)
- [ ] **Netlify deploy verification** — wait ~30 seconds, then test the URL

#### Suggested commit rhythm
- **Commit 1:** Upload 4 files to `cities/[city-slug]/` folder
- **Commit 2:** Upload root file updates (`index.html`, `sitemap.xml`, all affected landing pages) together

### Step 5: Promote
- [ ] Generate Pinterest pins for the city (use existing 18 briefs as template)
- [ ] Add to any relevant city-specific email outreach

---

## 📍 SECTION 7 — Photo Collection Workflow

### Quick reference
- **Sources:** Unsplash, Pexels, Wikimedia Commons (in order of preference)
- **Filename convention:** `[city-state]-[shottype]--[photographer]-[source].jpg` (during collection); rename to `[city-state]-[shottype].jpg` for final use
- **Resize:** 1600px wide max, Mac Preview → Tools → Adjust Size

### iPad → Mac workflow
1. **On iPad** (browsing): Find photos, save URLs to Apple Notes ("Photos to process")
2. **On Mac** (processing): Open queue, batch download → resize → rename → file to city folder
3. Skip the spreadsheet — filename-as-attribution is sufficient

### Top 5 photo priority
1. ✅ Boulder, CO (done)
2. ✅ Pittsburgh, PA (done)
3. Asheville, NC (4 landing pages)
4. Charleston, SC (Foodies Tier 1)
5. Santa Fe, NM (Foodies + Arts Lovers)
6. Bend, OR (Active Retirees + Hikers)

---

## 📍 SECTION 8 — Contact List for Verification

22 cities where Laurie has personal contacts (May 2026):

### Strategic priority (by landing page coverage)
🥇 **Madison, WI** — 6 of 7 landing pages
🥈 **Pittsburgh, PA** — 5 of 7 landing pages (mockup built, contact verification pending)
🥉 **Alexandria, VA** — 3 of 7 landing pages (Laurie lives there)

### Other contacts available
Bloomington, Lexington, Tucson, Sun Valley, Park City, Fort Collins, Carlsbad, Virginia Beach, Scottsdale, Bozeman, Fort Worth, Bend, Flagstaff, Vail, Miami, Iowa City, Sedona, Salt Lake City, Kansas City

---

## 📍 SECTION 9 — Document Reference Library

### Core project docs (save durably!)
| Document | Purpose | Status |
|----------|---------|--------|
| **This master tracker** | Single source of truth for everything | Save NOW |
| `city-profile-template-spec.md` | Template specification for new city profiles | Created May 4, 2026 |
| `RetireMeHere-Implementation-Plan.md` v1.1 | Phased implementation roadmap with deferred items | Last updated April 29, 2026 |
| `pinterest-pin-briefs.md` | 18 Pinterest pin design briefs ready for Canva | Ready |
| `foodie-cities-scoring-analysis.md` | Methodology for foodie cities landing page | Reference |
| Scoring rubric (v3.1 or v3.2) | Dimension scoring methodology | Confirm latest version |

### Working files (live)
- `index.html` — main site (quiz, matching, all city data)
- `top-cities-for-*.html` × 7 — landing pages
- `sitemap.xml`, `robots.txt`
- `boulder-co-profile.html` + 3 JPGs — first city profile (ready to deploy)
- `pittsburgh-pa-profile.html` + 3 JPGs — second city profile (verification pending)

### Database
- **Live database:** Google Sheets — "RetireMeHere City Database"
- **Tabs:** City Database, Scores by Dimension, Budget Tiers, New Cities to Add

### Brand assets
- **Domain (active):** retiremehere.com
- **Domains (to forward):** destinationretired.com, wheretoretireus.com
- **Email:** laurie@retiremehere.com (Google Workspace) + hello@, info@ aliases
- **MailerLite Account ID:** 2238788
- **Form IDs:** Globetrotter (fwB9NA), Wellness (f03tJB), Value (W6rMh2), Urban Walkabout (dJJ40D), Active Frontier (g4M1M8)
- **Google Analytics:** G-BTL743DSJQ

---

## 📍 SECTION 10 — Strategic Roadmap

### Architecture trigger points
- **Now (100 cities, 7 landing pages):** Single-file HTML works fine
- **City profile URL structure:** `retiremehere.com/cities/[city-slug]/profile.html` — each city in its own subfolder. Photos use simple names (`hero.jpg`, `lifestyle.jpg`, `detail.jpg`) within the folder.
- **At 150-200 cities OR 12+ landing pages:** Consider data-driven JSON architecture
- **At 250+ cities:** Move database from Google Sheets → Airtable
- **When adding user accounts/saved searches:** Move database to Supabase/Postgres

### Quarterly content cadence (recommended)
- Add cities to database whenever
- Refresh landing pages quarterly (1-2 hour focused session)
- Build city profiles incrementally as photos + contacts allow

### Marketing channels (in development)
- ✅ SEO via landing pages (sitemap submitted)
- 🟡 Pinterest (18 pins ready, awaiting Canva execution)
- 🟡 Facebook retire groups (link sharing strategy)
- ⏳ Email outreach to past quiz takers (when traffic justifies)

---

## 📍 SECTION 11 — Anti-Drift Reminders

Things that will be tempting to forget but matter:

1. **Don't write fake retiree quotes.** Use thematic attributions ("— On Pittsburgh's value proposition") until real interviews happen.
2. **Don't claim "interviews" in sample week intros** unless interviews actually happened.
3. **Always interleave photos and text** — never two photo sections back-to-back.
4. **Don't include rank numbers on "Appears on" cards** — meaning is unclear.
5. **Don't include a scores grid on city profiles** — users who took the quiz already trust the match.
6. **Photo credits go in same position on every photo** — bottom-right, raised above any overlapping element.
7. **Resize photos to 1600px wide BEFORE deploying** — don't ship 5MB hero images.
8. **CSS specificity gotcha:** `.header-cta` button needs `.header-nav a.header-cta` selector, NOT just `.header-cta`, to override parent rule color.

---

## 📍 SECTION 12 — Things Explicitly NOT Being Done (and Why)

These came up, were considered, were rejected. Don't re-litigate without new info:

- ❌ **"Value for Money" as a user-weighted dimension** — would not differentiate (everyone wants value)
- ❌ **Adding Providence as 101st city for subtitle math** — subtitle no longer mentions a number, so no value
- ❌ **Sticky pull-quote in Character section** — gets in way during scroll
- ❌ **Photo tracking spreadsheet** — overbuilt; filename-as-attribution is sufficient
- ❌ **Tourism press kits for Boulder/Bend** — registration-gated, slow; Unsplash is faster for now
- ❌ **Centering all body content** — magazine convention is centered hero + left-aligned body for readability

---

*This is a living document. Update it when status changes. When in doubt, this doc is the truth.*
