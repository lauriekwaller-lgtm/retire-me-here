# NEXT SESSION BRIEF: AFFILIATE INVENTORY ON THE TOOL PAGES
**Written:** August 22, 2026
**Suggested repo location:** `docs/BRIEF-2026-08-22-tool-page-affiliates.md`
**Session type:** BATCH (affiliate placement and one validator check. No city
builds, no comparison builds, no new pages. `deep-dive-reports.html` is boarded
and is NOT this session.)

---

## Read first

1. This brief.
2. `docs/TASKBOARD.md` top section, entries dated Aug 21, 2026.
3. `docs/SITE-OPERATIONS-LOG.md` section 7, entry `2026-08-21`.
4. `docs/GA4-EVENT-REFERENCE.md`, sections 1 and 6.
5. `docs/AFFILIATE-CODES.csv`, the new source of truth for affiliate codes.

Pull everything live from the repo. Do not read a cached or project-knowledge
copy of any file that exists in the repo. Re-derive baselines from live main
before building anything. Size scope by grepping, not by the numbers on this
page: this brief was written on Aug 22 and the counts below will drift.

---

## Why this session exists

The Aug 21 session made affiliate clicks measurable. It did not make them
possible everywhere they should be.

The board describes the tax tool and the affordability calculator as the
highest-intent affiliate inventory on the site. Neither carries a single
affiliate link. Someone who has just run the numbers and learned that Pensacola
fits their budget is closer to booking a scouting trip than someone who has
read a profile, and right now that person is handed nothing.

The instrumentation shipped Aug 21 will faithfully report zero from both pages,
forever, until this changes. That is the gap.

**Do not treat this as a traffic-routing session.** Profile-to-tools routing is
the board's largest lever and is the natural session AFTER this one. Sending
more people to the tools before the tools monetise is sending them to a dead
end. Order matters here: inventory first, routing second.

---

## What is actually true, verified Aug 22

Verified by grep against live main. Re-verify; do not inherit.

**The four tool pages, and they are not equivalent:**

| Page | Lines | Analytics block | Affiliate links | City data |
|---|---|---|---|---|
| `where-can-i-afford-to-retire.html` | 1203 | **NO** | none | `AFFORD_CITIES` array |
| `states-that-dont-tax-retirement-income.html` | 770 | **NO** | none | `TAXCITIES` object |
| `pick-and-compare.html` | 1546 | **NO** | none | 5 data refs |
| `compare-retirement-cities.html` | 1140 | **NO** | none | none, navigational |

**The dependency that is easy to miss and will silently waste the session.**
The `RMH-ANALYTICS-V1` block shipped Aug 21 went onto `index.html`, the 51
profiles, and `visit-before-you-decide.html`. It did **NOT** go onto any tool
page, because at the time no tool page had an affiliate link to track. Adding
affiliate links to a tool page without also adding that block produces links
that earn commission but emit no `affiliate_click` event. The whole point of
sequencing this session after the instrumentation was to be able to grade it.
**Add the block to every tool page that gets a link, in the same commit.**

The block is generic by design: merchant is read off the href and the page slug
off `location.pathname`, so it needs no per-page customisation. Copy it
byte-identical. A jsdom test written Aug 21 asserts the profile and index
copies are identical; extend that idea rather than hand-editing a variant.

**City data on the tool pages is inline JS and carries name plus state:**

- `AFFORD_CITIES` is an array of objects shaped `{n:"Fairhope", s:"AL", ...}`.
- `TAXCITIES` is an object keyed by state, values are arrays of `{d5:7,
  n:"Fairhope"}`.

Neither carries a slug and neither carries an affiliate code. That is the
central build question below.

**`docs/AFFILIATE-CODES.csv` is new as of Aug 21 and is now the source of
truth.** 99 rows, one per database city, columns `city, state, slug,
expedia_code, vrbo_code, source`. All 99 have both codes. It was built by
extracting codes from the 51 live profiles (authoritative) and merging the
operator's codes file for the rest, then reconciled: zero mismatches against
live profiles, no duplicate codes, unique slugs. The two Wilmingtons are
`wilmington-de` and `wilmington-nc` and have genuinely different codes; keying
on city name alone silently collides them, which happened once during the
build. **Key on city AND state, always.**

---

## The build question, decide it before writing code

The tool pages render results dynamically through `innerHTML` (6 writes on the
afford page, 2 on the tax tool, 7 on pick-and-compare). A link attached to a
result has to be produced at render time, which means the page needs access to
a city's affiliate code in the browser.

Three approaches. Pick one deliberately and state the reasoning:

1. **Inline a code map into each tool page**, generated from
   `AFFILIATE-CODES.csv` by an apply script. Simple, no fetch, no runtime
   dependency. Cost: the codes are then duplicated in three more files and can
   drift from the CSV. Mitigated entirely by the validator check below, which
   is being built this session anyway.
2. **Extend the existing arrays** with a code field rather than adding a
   parallel map. Fewer moving parts, but a larger diff into hand-maintained
   data structures and a higher chance of breaking the tools.
3. **Fetch the CSV at runtime.** Cleanest single source, but adds a network
   dependency to a tool that currently works offline-ish and fails in a way the
   visitor sees. Not recommended.

Option 1 is the likely answer. Do not adopt it by default without checking the
diff size on option 2 first.

**Whichever is chosen, the visitor-facing placement question is separate and
matters more.** A link attached to a result the visitor just earned is
high-intent. A link bolted to the page frame is banner blindness. The board's
standing rule is that capture goes after value is delivered, never as a toll,
and the same logic applies to affiliate placement: the link belongs in or
beside the result, after the answer, not above it.

**`compare-retirement-cities.html` should probably get nothing.** It is a
navigational hub with no city data and no result state, so there is no moment
of intent to attach to. Confirm by reading it, then board the decision either
way rather than leaving it ambiguous.

---

## Scope, in the order I would work it

### 1. The validator check (do this first)

Build it before the placement work, so the placement work is covered the moment
it lands rather than retrofitted.

`tools/validate.py` already has a `check_affiliate`. **Read it first and find
out what it already covers** before adding anything; do not assume it is empty
and do not duplicate its logic.

What the check needs to enforce, whether by extension or a new check:

- every affiliate code on any page matches the row for that city in
  `docs/AFFILIATE-CODES.csv`;
- no two cities share an Expedia code or a Vrbo code;
- every city in the database has a row in the CSV, and every row has both
  codes;
- slugs in the CSV are unique.

Standing rules: no new validator check ships without a planted-error harness,
and every check must fail loudly on zero matches. The silent no-op is the known
failure mode on this project and a check that passes because it matched nothing
is worse than no check.

### 2. Affiliate placement on the afford calculator

Highest intent of the four. The visitor has entered a budget and received a
list of cities they can afford. Attach the link to the city result.

### 3. Affiliate placement on the tax tool

Same pattern, second highest intent.

### 4. Pick-and-compare

Two named cities, so two link pairs. Lowest of the three but still real intent.

### 5. The analytics block on every page touched

Same commit. See the dependency note above.

### 6. Board and log

Same commit. Standing rule.

---

## Explicitly out of scope

- `deep-dive-reports.html` and the nav tab. Boarded P2, endorsed, and a proper
  build. Better built with October capture data in hand than guessed at now.
- Profile-to-tools routing. The natural session after this one.
- The twelve stale cross-city figures and the three-layer validator extension.
- The St. Paul DB cell and the `index.html` D2 monthly budget audit.
- Any new city profile or comparison page.
- GA4 admin work. Operator-side, tracked on the board.

---

## Constraints

**Laptop days.** Roughly seven left from Aug 22, then travel with an iPad and
phone only. This session needs a laptop. Scope it to finish rather than to be
comprehensive.

**Do not gate anything.** Standing board instruction. Affiliate links are
offered after the answer, never in front of it. Nothing in this session may
make a visitor complete a step to see a result they can currently see.

**Nothing a visitor sees may break.** The tools are working features with real
usage. A broken calculator is worse than a calculator with no affiliate link.
Verify the tools still function after the edit, not just that the page parses.

**Realistic scale.** At roughly 360 users a month this will not move revenue
this year. It creates inventory on the two surfaces where intent is highest,
and it makes the routing session that follows worth running.

---

## Definition of done

- Affiliate links live on the afford calculator, the tax tool, and
  pick-and-compare, attached to results rather than to the page frame.
- A boarded decision on `compare-retirement-cities.html`, either way.
- `RMH-ANALYTICS-V1` present on every page that gained a link, byte-identical
  to the copy on the profiles.
- A validator check tying every affiliate code on the site to
  `docs/AFFILIATE-CODES.csv`, with a planted-error harness proving it fails
  when a code is wrong and when two cities share one.
- Each tool still works: run each one end to end in a browser, not just a
  parse.
- `python3 tools/validate.py --local .` at 0 failures, 0 warnings on a fresh
  clone.
- Apply script idempotent on second run, anchor counts asserted before write.
- Board and log updated in the same commit.

---

## The standing rule this project keeps relearning

Presence of plumbing is not evidence of a live feature. The Aug 21 session
found an event named `report_signup` that did not fire on signups, and a
capture function with zero call sites. This session's version of that trap is
assuming a link earns commission because it is on the page: check the code
against the CSV, check the analytics block is present, and treat any assertion
about runtime that has not been verified in a browser as unverified.

The second rule, earned on Aug 21 and Aug 22 both: **grep, do not inherit.**
The last brief was wrong about where GA4 events lived and wrong about the
affiliate merchant count, and the operator's codes file was missing 19 codes
that had been live on profiles all along. Both were caught by re-deriving from
live main. Neither would have been caught by trusting the page.
