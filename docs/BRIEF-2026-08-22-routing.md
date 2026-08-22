# NEXT SESSION BRIEF: ROUTING
**Written:** August 22, 2026
**Suggested repo location:** `docs/BRIEF-2026-08-22-routing.md`
**Session type:** BATCH (routing and one nav decision. No city builds, no
comparison builds. `deep-dive-reports.html` is boarded and is NOT this session.)

---

## Read first

1. This brief.
2. `docs/TASKBOARD.md` top section, entries dated Aug 21 and Aug 22. There are
   FOUR Aug 22 entries; read all of them.
3. `docs/SITE-OPERATIONS-LOG.md` section 7, all four `2026-08-22` entries.
4. `docs/GA4-EVENT-REFERENCE.md` sections 1 and 2.

Pull everything live from the repo. Do not read a cached or project-knowledge
copy of any file that exists in the repo. Re-derive baselines from live main
before building anything. Size scope by grepping, not by the numbers on this
page.

---

## Why this session exists

Three pages exist that people cannot get to.

The board's P1 is that all 51 profiles end with a "Visit Before You Decide"
section and NOT ONE links to `visit-before-you-decide.html`. The section class
matches the page name, which is why it reads as linked until you grep for an
href. Verified again Aug 22: 51 profiles carry the section, 0 link to the page.

The tools are in the same position. The header nav offers Home, Find a City, Top
Cities For, and Find My Match. The affordability calculator, the tax tool, and
pick-and-compare are not in it.

And `where-should-i-retire-quiz.html` routes people onward through two CTAs
that nothing measures.

All three are the same job: people cannot reach a page, or we cannot tell
whether they did.

---

## What is actually true, verified Aug 22

Verified by grep against live main. Re-verify; do not inherit.

- 51 profiles carry a `<section id="visit" class="visit-before-you-decide">`.
- 0 of them link to `visit-before-you-decide.html`.
- Each visit section already carries that city's Expedia link and Vrbo link,
  inline in the prose, plus a disclosure paragraph.
- `visit-before-you-decide.html` carries three affiliate links, all repointed to
  non-city generic codes on Aug 22, and is reachable only from `index.html`.
- `where-should-i-retire-quiz.html` has the GA4 tag but NO `RMH-ANALYTICS-V1`
  block, no affiliate links, no capture, and two CTAs into the quiz.

**One markup irregularity that will break a naive anchor count.** 50 of the 51
visit sections close identically. `cities/asheville/profile.html` closes with a
trailing space after `</section>`. Any apply script anchoring on the closing
markup must handle both or it will report 50 and refuse to write, which is the
correct behaviour but will read as a mystery. Anchor on something stable and
assert 51.

---

## The judgment call, decide it before writing code

**The pillar link is not being added to a page with no route to booking.** The
profile already carries that city's Expedia and Vrbo links, in the same section,
a few lines above where the pillar link would go. This is a second path added
beside a converting one, not a fix for a dead end.

That could go two ways and the session has to choose:

- A reader ready to price a trip for that city should click that city's Expedia
  link, not detour to a general how-to page. A prominent pillar link could take
  clicks from the higher-intent action sitting beside it.
- A reader who is not ready to book, who wants to know how to run a scouting
  trip at all, currently leaves. For that person the pillar is the right
  destination and the affiliate links are premature.

**The recommended resolution, to be adopted or overridden deliberately:** put
the pillar link AFTER the affiliate block and the disclosure, framed as the
how-to rather than the where-to-book, sized as a secondary text link rather than
a button. That serves the not-yet-ready reader without stepping in front of the
ready one, and keeps the cost small if it does siphon.

**Do NOT promise that this will be graded, because it cannot be.**
`affiliate_click` shipped Aug 21 and holds nothing but operator test clicks.
There is no baseline to compare against and there will not be a useful one
before this ships. A before-and-after read on per-city affiliate clicks is NOT
available. What IS available, later, is the ratio on the same page over the same
period: profile affiliate clicks versus profile pillar clicks. That says whether
anyone uses the pillar link, not what it displaced. Write the board entry to
claim only that.

**The gain that CAN be seen** is on the pillar page itself. Its three affiliate
links currently receive traffic from `index.html` only. That starts from a real
zero, so any `affiliate_click` arriving from
`surface: visit-before-you-decide` after this ships is attributable to this
change.

---

## Scope, in the order I would work it

### 1. Pillar links on the 51 profiles (do this first)

Highest value on the board, mechanical, no design conversation, no third-party
unknowns. One line per profile, placed per the decision above.

The profiles already carry `RMH-ANALYTICS-V1`, so a click on the new link is
NOT an affiliate click and will not fire `affiliate_click`. If the session wants
the profile-to-pillar click measured, that needs its own event. Decide it rather
than assuming the existing block covers it.

### 2. The two CTAs on `where-should-i-retire-quiz.html`

Smallest item. The page is a search landing page whose job is to hand readers to
the quiz; see the Aug 22 fourth board entry. It needs the `RMH-ANALYTICS-V1`
block (currently absent) and a click event on both CTAs, so the handoff becomes
readable.

**Do NOT add email capture to this page.** It is boarded as closed and NOT
APPLICABLE. A reader four seconds in has been given nothing, and an ask there is
a toll in front of value. **Do NOT read its 4 second average engagement as a
bounce.** It is a doorway page working as designed. Both traps are written up on
the board; this brief repeats them because they are the two ways this page gets
"fixed" wrongly.

### 3. The nav entry, and it needs a decision, not a build

The header carries four items. Adding three tools makes seven, which is a lot on
mobile. **This is a visual decision and the operator's partner weighs in on
those.** Do not ship a seven-item nav on the assumption that more entries are
better.

Options worth putting to the operator rather than choosing unilaterally: a
single "Tools" entry that opens a small menu or lands on a tools index; folding
the tools under the existing "Find a City"; or promoting only the strongest one
and leaving the other two to in-page links. The board notes the tax tool has
exactly one inbound link on the whole site, from the affordability calculator,
which is the strongest argument that this is a nav problem rather than a page
problem.

If the decision is not settled during the session, ship items 1 and 2 and board
the nav shape as a decision pending. Do not stall the session on it.

### 4. Board and log

Same commit. Standing rule.

---

## Explicitly out of scope

- `deep-dive-reports.html` and the nav tab. Boarded P2, endorsed. Better built
  with October capture data than guessed at now.
- Any new affiliate partner or category. Boarded to be revisited after October
  with `affiliate_click` data in hand.
- The twelve stale cross-city figures and the three-layer validator extension.
- Any new city profile or comparison page.
- GA4 custom dimensions. Operator-side, on the board, needed before October.

---

## Constraints

**Laptop days.** Roughly seven left from Aug 22, then travel with an iPad and
phone only. This session needs a laptop.

**Do not gate anything.** Standing board instruction. Nothing in this session
may put a step in front of something a visitor can currently reach.

**Nothing may break.** The visit section on the profiles is live, converting
inventory. A malformed edit across 51 files is worse than no pillar link.

---

## Definition of done

- All 51 profiles link to `visit-before-you-decide.html`, placed per a decision
  recorded on the board with its reasoning.
- `where-should-i-retire-quiz.html` carries `RMH-ANALYTICS-V1` and a click event
  on both CTAs.
- A nav decision, either shipped or boarded as pending with options named.
- `python3 tools/validate.py --local .` at 0 failures, 0 warnings on a fresh
  clone.
- Apply script idempotent on second run, anchor counts asserted before write,
  and the Asheville trailing-space case handled.
- Board and log updated in the same commit, claiming only what is measurable.

---

## The standing rule this project keeps relearning

Two entries went stale on Aug 22 by being true when written and quietly false
after something downstream shipped: the NOT VERIFIED caveats on the key-events
work, and a P1 asserting `index.html` had no capture months after it got some.
The board is long enough that old sections do not get reread. When this session
closes an item, check whether it also falsifies an older entry, and correct that
entry in the same commit.

The second rule, earned repeatedly: **grep, do not inherit.** Every brief so far
has been wrong about at least one count.
