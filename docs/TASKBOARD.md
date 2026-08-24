# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** August 23, 2026 (second entry), nav unified on the 46 component pages

**SHIPPED, August 23 2026. Nav parity, BATCH A. BATCH B boarded below.**

*What was found.* Scoping the orphan-page work turned up EIGHT distinct navs
across one hundred pages. Not eight designs, eight accidents: the nav was never
a component, so every page froze whatever the menu looked like on the day it was
built, and each new tool page was added to whichever nav was in front of whoever
added it. `where-can-i-afford-to-retire.html` was in the menu on two pages out
of ninety-eight. `visit-before-you-decide.html` on one. Every guide page was
missing Compare Cities. All eight topic links, by contrast, were everywhere,
which is why nothing ever looked obviously broken.

*Two nav families, not eight variants.* Forty-six pages carry the dropdown
component. Fifty-two carry a three-link stub with none of the machinery behind
it: no `.nav-dropdown` CSS, no `.nav-dropdown-item`, no `.nav-chev`, no
`.header-quiz-btn`, and no `toggleTopCitiesDropdown` anywhere on the page. Two
pages, `privacy.html` and `scouting-trip-workbook.html`, have no header at all
and are outside the sitemap.

*Why index.html is exempt and always will be.* Its nav calls
`openCitySearch()`, `startQuiz()` and `showScreen('screen-explore')`, which
exist only on that page because it is the quiz app. Stamping the shared block
there kills every item; copying its block anywhere else kills every item there.
Two navs is forced by the architecture. Their MENUS agreeing is not, so
`check_nav_parity` holds index.html to the same destinations while letting its
markup differ.

*What shipped.* `tools/nav_canonical.html` is now the nav.
`tools/build_nav.py` stamps it onto all forty-five non-homepage component pages,
root-absolute so the same block will work unchanged at `cities/<slug>/` depth
when BATCH B lands. `check_nav_parity` compares line for line, not as a set of
links: set equality would have passed all eight variants the moment their link
lists converged. Twelve plants in `tools/test_nav_parity.py`.

*Resolved by this batch.* The open board item "nav entry decision for
`visit-before-you-decide.html`, requires partner input before shipping" is
closed. Plan a Visit is in the canonical nav on all forty-six component pages,
approved as part of the item list.

*Item list, as approved.* Find a City, Top Cities For… (dropdown, eight topics
plus More topics), What Can I Afford?, Compare Cities, Plan a Visit, Find My
Match. `pick-and-compare.html` deliberately NOT in the top bar: the hub and the
tool are two different products with near-identical names, and two "Compare"
entries in one menu confuse more than they help. It wants a home on the Compare
hub instead, which is a separate job.

**QUEUED. BATCH B. The fifty-two pages with no nav component.**

Fifty-one city profiles plus `visit-before-you-decide.html`. Needs the CSS
block, the `toggleTopCitiesDropdown` function and the canonical markup shipped
to each file. Root-absolute hrefs are already in the canonical block, so profile
depth is handled. This VISIBLY CHANGES the header on every city profile, which
is partner-reviewable: build one profile, review it rendered, then batch the
rest. `NAV_STUB_EXPECTED = 52` in validate.py is the debt counter and drops to 0
when this lands; the check already FAILS if it ever rises.

*Why it matters beyond tidiness.* Profiles are the deepest content on the site
and currently hand a crawler three links, all to the homepage. Internal links
are how rank moves, and profiles are exactly where the not-indexed pages are.

**Last updated (previous):** August 23, 2026, sitemap lastmod derived from git

**SHIPPED, August 23 2026. Sitemap freshness, made derived. OPS + BATCH.**

*What prompted it.* Search Console showed indexed pages sliding, ninety to
eighty-eight to eighty-six over three weeks, with twelve URLs in "Crawled -
currently not indexed". Ten were readable. One was `/?city=Lexington&state=KY`,
a homepage query-string duplicate that the August 9 canonical already handles
and that will migrate to "Alternate page with proper canonical tag" on its own.
The other nine were real pages.

*The finding, and it is a negative one worth keeping.* Nothing distinguishes
those nine. Inbound internal links ran four to twenty against an indexed median
of eleven; word counts 2,321 to 2,711 against an indexed median of 2,558;
non-boilerplate text share 92-93% against an indexed range of 90-95%; every
title and meta description on the site already unique. Philadelphia had twenty
inbound links, 2,711 words, 93% unique text, and was not indexed. Lexington had
the worst unique-text ratio on the site and was. There is no page-level defect
to fix, so no profile was rewritten and none should be.

*What WAS wrong.* The sitemap. Ninety-seven of ninety-eight URLs carried a
`<lastmod>` older than the file's last commit, by up to 101 days, and
`cities/chattanooga/profile.html` carried no `<lastmod>` element at all. Every
profile had been rewritten by the August 22 pillar-link batch while the file
still said May 11 for Scottsdale, May 20 for Salt Lake City, May 21 for
Philadelphia. Three of the pages Google had not revisited since June were among
them. The one field built to say "come back" was saying the opposite.

*What shipped.* `tools/build_sitemap.py` derives every date from git; the
`<loc>` list is still read from the existing sitemap and preserved exactly, so
page membership stays an editorial decision and only the date is automated.
`<changefreq>` and `<priority>` dropped on rewrite: Google has ignored both for
years and they were 196 lines of hand-maintained fiction sitting beside the
hand-maintained dates that actually broke. `check_sitemap_lastmod` and
`tools/test_sitemap_lastmod.py` hold it, in a `sitemap` group of their own.

*Honest grading, boarded before the result is known.* This removes the reason
Google is not RECRAWLING the stale pages. It does not make them INDEXABLE; that
is site authority and no code change touches it. Expect it to help the pages
whose dates were lying and do nothing for the rest. Read it in the October
Search Console pass, not before, and grade on recrawl dates moving first,
indexed count second.

**Last updated (previous):** August 22, 2026, GA4 verification closed

**VERIFIED IN A BROWSER, August 22 2026. The Aug 21 and Aug 22 entries below
both close with a NOT VERIFIED caveat. Both are now discharged and the caveats
should be read as historical.**

Both events were fired from production and observed arriving in GA4 Realtime:
`affiliate_click` from a profile visit block, and `signup_submit` from a real
signup on the quiz results screen. `form_start` was observed alongside it.

*What that settles, and it is the load-bearing one.* The Aug 21 entry recorded
our own listener logic as proven and MailerLite's native submit emission as
ASSUMED, and named that assumption as the single thing that could not be
checked outside a browser. It holds. MailerLite's embed emits a submit event
our delegated listener catches. There is no fallback to build, no
`MutationObserver` to board, and the enhanced-measurement `form_submit` signal
is a redundant cross-check rather than a contingency.

*Operator steps completed.* `affiliate_click` and `signup_submit` are both
marked as key events. `quiz_complete` was already marked and is the denominator
for the capture rate.

*Still open, and deliberately deferred.* Custom dimensions for `merchant`,
`surface` and `city_slug` are NOT yet registered. Until they are, both events
report as totals and every breakdown reads `(not set)`. That is acceptable at
current volume, where there is nothing to break down, but it must be done
before the October read or the surface labels that justified building
`signup_submit` the way it was built will be unreadable.

*GA4 default to clean up.* GA4 stars `purchase` as a key event automatically on
every property. There is no ecommerce on this site, so it will never fire and
will sit in reporting as a permanent zero. Unmark it.

*A UI correction worth recording, because it cost a session's worth of
confusion.* GA4 removed the Conversions report and did not replace it with a
Key events equivalent. Key event counts are read from Reports > Engagement >
Events, and the genuinely useful view is Reports > Acquisition > Traffic
acquisition, which carries key-event columns per source and is what will answer
whether Pinterest traffic converts better than search. Section 4 of
`docs/GA4-EVENT-REFERENCE.md` describes an admin path that no longer exists and
an ordering that does not work: a brand new event CANNOT be marked as a key
event before it has fired, because the star is the only mechanism and it only
appears next to events GA4 has received. The order is fire it, then star it.
That doc is otherwise current; sections 1, 2 and 5 are the October reading
material.

**Last updated (previous):** August 22, 2026, tool-page affiliate inventory
(51 profiles live, 24 comparison pages live. The affordability calculator and
pick-and-compare now carry affiliate links attached to results, and every code
on the site is tied to docs/AFFILIATE-CODES.csv by the gate.)

**SHIPPED, August 22 2026. Tool-page affiliate inventory, 6 files.**

*The gap.* The Aug 21 session made affiliate clicks measurable and would have
reported zero from the tool pages forever, because no tool page carried a link.
Someone who has just learned that Pensacola fits their budget is closer to
booking a scouting trip than someone who has read a profile, and was handed
nothing.

*What shipped.* A generated code map, `RMH_AFF`, byte-identical on the
affordability calculator and pick-and-compare, keyed on city AND state and
generated from `docs/AFFILIATE-CODES.csv`. Both merchants offered on every
result, in the result, after the answer. Never in the page frame and never in
front of the answer. `RMH-ANALYTICS-V1` added to both pages in the same commit,
byte-identical to the copy on the 51 profiles and index, so the links emit
`affiliate_click` rather than earning silently. Both pages also gained an
affiliate disclosure, which neither had.

*The validator work, done first so the placement landed covered.*
`check_affiliate` was NOT empty, and its docstring argued that a spreadsheet of
codes should never exist because it would be a stale copy of the HTML. That was
right while every link sat on a profile and stopped being right when the tool
pages needed codes for cities that have no profile: 99 cities carry codes and 51
have profiles. The stale-copy objection was answered rather than ignored, by
tying the table to every page on every run. It now enforces unique slugs, unique
codes per brand, both codes on every row, the roster against the database in
both directions, every code on every profile against its row, and the inlined
maps against the table cell by cell. New harness `tools/test_affiliate.py`,
fifteen planted defects, fifteen caught.

*THREE FINDINGS, from grepping rather than inheriting.*
1. `visit-before-you-decide.html` had never been checked by anything: the old
   check only ever looped city profiles. It carries three affiliate links.
2. That page is using **Bend's Expedia code** as its generic code, so every
   generic-page Expedia click is booked to Bend's per-city reporting. Its Vrbo
   code and its Hotels.com code appear in no row of the table. All three are now
   declared by value in `GENERIC_AFF_CODES`, so the gate reads the known state as
   clean and a SECOND city code on a generic page still fails.
   **CORRECTED Aug 22, later the same day: the Vrbo code was NOT clean.**
   `DGMzUEy` appears in no row of the table and was declared generic on that
   basis, but following the link showed it landing on Bend as well. Absence from
   the table means the code belongs to no BUILT city, which is equally true of a
   city code nobody ever recorded. Two of the three links on the generic pillar
   pointed at Bend, not one. Fixed below.
3. None of the four tool pages carried an affiliate disclosure of any kind.

*Verified.* Fresh clone, `python3 tools/validate.py --local .` at 0 failures 0
warnings. Beyond the gate, both tools were driven end to end under jsdom across
23 cases: the calculator still renders and still re-renders when the budget
moves, pick-and-compare still builds a comparison in BOTH the wide table and the
stacked mobile view, every card links its own city's codes, and the two
Wilmingtons resolve to different codes.

**DECIDED, August 22 2026: the tax tool gets NO affiliate links.** Two reasons,
and the second is the real one. Its results are STATES while affiliate codes are
CITIES, so any link there has to pick a city to represent a state and D5 ties
constantly within a state, which makes the pick arbitrary. More decisively, the
page has exactly ONE inbound link on the whole site, from the affordability
calculator, so it sits two hops deep with no nav entry. Inventory on a page
nobody can reach earns nothing. Revisit if and when it gets routing.

**DECIDED, August 22 2026: `compare-retirement-cities.html` gets NO affiliate
links.** Navigational hub, no city data, no result state, so there is no moment
of intent to attach an offer to.

**P1, CLOSED August 22 2026. All 51 profiles now link to the pillar.** The
entry below is kept for the finding. What shipped, and the reasoning, is here.

*Placement, decided rather than defaulted.* The link sits AFTER the affiliate
block and after the disclosure, as a 15px teal text link, not a button. The
profile already carries that city's Expedia and Vrbo links a few lines above.
This was a second path added beside a converting one, not a fix for a dead end,
so it was sized to serve the reader who is not ready to book without stepping in
front of the reader who is. Below the disclosure for a second reason: the
disclosure reads "if you book through these links" and the pillar link is not a
booking link, so it stays outside that sentence's scope.

*What can be graded, and what cannot.* A before-and-after read on per-city
affiliate clicks is NOT available. `affiliate_click` shipped Aug 21 and holds
operator test clicks only, so there is no baseline and there will not be a
useful one before this ships. What IS readable, in October, is the ratio on the
same surface over the same period: `pillar_click` against `affiliate_click`,
both carrying `surface` = city slug. That says whether anyone uses the link. It
does not say what it displaced, and no entry should claim otherwise.

*The gain that starts from a real zero.* The pillar page's three affiliate links
previously received traffic from `index.html` only. Any `affiliate_click` with
`surface: visit-before-you-decide` after this ships is attributable to this
change.

*New event.* `pillar_click`, added to the RMH-ANALYTICS-V1 block on all 51
profiles. It reuses `surface` and `city_slug` and needs no new GA4 custom
dimension. Anchored on `data-rmh-pillar`, not on the href, so a future nav entry
pointing at the same page does not silently fold into this number.

*The finding that came out of shipping it, and it is the more useful half.* The
link was planted first and the gate was run against a deliberate typo in the
href on one profile. It passed at 0 failures, 0 warnings. Nothing on the site
defended this link: not an affiliate link, so `check_affiliate` skips it, not a
canonical, not a sitemap entry, and tag balance sees a well-formed anchor either
way. A single fat-fingered character would have restored the exact orphaning
this entry exists to close, silently, with a clean gate. `check_pillar_links`
and `tools/test_pillar_links.py` were written before hand-off. The check asserts
51 profiles read and fails loudly at zero.

*A second-order catch worth recording.* The first draft of that check tested the
whole file for `data-rmh-pillar` and passed even with the attribute stripped off
the anchor, because the analytics block contains the selector
`a[data-rmh-pillar]`. The harness caught it. The check now inspects the anchor
tag. This is the standing argument for planted-error harnesses: the check was
wrong in a way that would have read as working forever.

**P1, ORIGINAL TEXT, superseded August 22 2026: the pillar page is orphaned.**
All 51 profiles end with a "Visit Before You Decide" section and NOT
ONE of them links to `visit-before-you-decide.html`. The section class matches
the page name, which is why this reads as linked until you grep for an href. The
page carries three affiliate links, already has the analytics block, and is
reachable only from `index.html`. This is a one-line-per-profile fix and it is
worth more than anything shipped this session. Belongs to the routing session.

**P2, OPEN, new: the tools have no nav entry.** The header nav offers Home, Find
a City, Top Cities For, and Find My Match. The affordability calculator, the tax
tool, and pick-and-compare are not in it. The tax tool decision above is
downstream of this.

**CLOSED Aug 22 2026: the generic pillar's affiliate links now point at generic
destinations.** Was P2 OPEN, scoped as one borrowed Expedia code. It was two:
the Vrbo code was landing on Bend as well, which the table lookup could not see
and only a click revealed. All three links on `visit-before-you-decide.html`
were swapped to purpose-generated non-city codes and the old set was retired
from `GENERIC_AFF_CODES`, so `jkBLWmX` is no longer exempt and now fails by name
if it ever reappears on a non-city page.

*Why this was worth doing beyond attribution.* The attribution problem was real,
Bend's affiliate numbers would have been inflated by generic-page traffic in the
October read. But the reader-facing problem was larger and had not been named:
someone on the scouting-trip pillar has not chosen a city, and was being sent to
Bend hotel results regardless. That is a broken destination, not a mislabelled
click, and it had been live long enough that no conversion number from that page
is trustworthy before Aug 22.

*The standing rule this earned.* An entry in `GENERIC_AFF_CODES` silences a
check, so it is a claim about a DESTINATION and can only be established by
following the link. A lookup miss establishes nothing. The set now carries that
rule in a comment, because the previous entry was added on a lookup miss and was
wrong.

**SHIPPED, August 21 2026. Key events, 53 files.**

*What was dark.* Affiliate clicks, the revenue path, fired nothing from any of
the 52 pages carrying a link. The 51 profiles fired no GA4 event of any kind.
A successful signup on the results screen produced no event whatsoever, because
`report_signup` only ever fired on the Netlify fallback path that a real
MailerLite submit never touches. Not a wrong number: no number.

*Two events, two delegated listeners, one identical block on 53 pages.*
`affiliate_click` carries merchant and page slug; `signup_submit` carries which
of the three form homes the node was in at the moment of submit. Both delegate
from `document` in the CAPTURE phase. Capture is doing real work here, not
decoration: it means a downstream `stopPropagation` cannot silence either
event, and delegation from document means the listener survives the MailerLite
node being reparented between the vault, the results band and the modal, which
is the exact hazard the Aug 20 mechanism created. Merchant is read off the
href rather than hardcoded, and the page slug off `location.pathname`, so the
block is byte-identical everywhere and a new profile inherits instrumentation
without anyone remembering to wire it.

*Dead plumbing swept repo-wide, not region-wide.* `submitProfileCapture`
deleted: zero call sites, and it called `openSignupModal('value')`, a key that
stopped existing at the Aug 19 consolidation, so it would have returned
silently even if reached. With it went the orphaned `quiz-results` Netlify stub
it was the only poster to, six `.rsp-` CSS rules with zero usages anywhere in
markup or JS, and a DUPLICATE `report-signup` stub that had been registered
twice. One `report-signup` stub is KEPT deliberately: `submitSignupModal` is a
real fallback for the case where the MailerLite wrapper node is missing, that
fallback is not being retired, so the stub stays.

*Names now match what they measure.* `report_request` fired when the signup
modal OPENED, so it is now `signup_modal_open`. `report_signup` fires only on
the Netlify fallback, so it is now `signup_submit_fallback` and no longer
impersonates the real signal. `profile_capture` went with its dead function.
JUDGMENT CALL: renaming breaks GA4 continuity under the old names. Accepted
because both had near-zero honest volume and the old data stays queryable.

*THE FINDING, and it is the useful part of this session.* MailerLite's
JavaScript-snippet embed renders a real `<form>` into our DOM rather than an
iframe, which is why a delegated `submit` listener works at all. That is a
markedly better hook than the `MutationObserver` on success markup the brief
anticipated as a last resort: an observer is coupled to MailerLite's rendered
success state and breaks silently when they restyle it, whereas a submit
listener is coupled only to there being a form. The observer was NOT needed and
was NOT shipped. Second finding: GA4 enhanced measurement captures `form_start`
and `form_submit` on this embed with no code at all, which is worth switching
on as an independent second signal, but it cannot distinguish the results band
from the city-detail modal because both are the same form on the same URL. Ours
can. That is the reason to have both.

*What `signup_submit` does and does not mean.* It counts an attempted submit,
which is what the name says. It does not count a confirmed subscriber, and it
should not: MailerLite already counts those exactly. The board's grading ratio
needs a denominator GA4 alone can supply and a numerator MailerLite already
holds, so the hard half of this problem was never ours to solve.

**OPERATOR ACTION REQUIRED, GA4 admin, not in the repo. The code is inert until
this is done.**
1. Admin > Events, mark `affiliate_click` and `signup_submit` as key events.
   Firing an event is not the same as GA4 reporting it as a conversion.
2. Admin > Custom definitions, register `merchant`, `surface` and `city_slug`
   as custom dimensions (event-scoped). Without this the events arrive but
   every breakdown reads "(not set)".
3. Admin > Data streams > Enhanced measurement, confirm Form interactions is
   ON, for the independent second signal above.
4. Then verify in DebugView, on production: click an affiliate link on any
   profile, and complete one real signup from the results band. This is the
   ONLY real verification available. The validator cannot see analytics and
   neither can jsdom.

**NOT VERIFIED, and this is the honest limit.** Everything above about our own
listener logic was exercised under jsdom across 33 cases including the
reparenting case, and the test discriminates: five planted defects, five
caught. But jsdom stands in a hand-built form node, because universal.js does
not run there. So it is PROVEN that our listener fires correctly on a real form
element in each of the three homes, and it is UNPROVEN that MailerLite emits a
native submit event on that element in a browser. If step 4 above shows
`affiliate_click` arriving but `signup_submit` never arriving, that is the
assumption that failed, and the fallback is the enhanced-measurement
`form_submit` signal rather than an observer.

**P2, OPEN, new: the tool pages carry no affiliate inventory at all.** The tax
tool and the affordability calculator are described on this board as the
highest-intent inventory on the site and neither has a single affiliate link on
it. The instrumentation now shipped will faithfully report zero from both,
forever, until that changes. Not this session, but it is now measurable the day
it does.

**P2, OPEN, restated with a second instance: the capture path still has no
regression coverage in the repo.** Boarded Aug 20 after the node-lifetime test
could not ship. This session wrote a second node test, for the events, that
also cannot ship for the same reason. Two tests now live outside the repo. The
decision is unchanged and is now more expensive to keep deferring: add a node
harness group to the gate, or accept that this path is hand-tested forever.

**SHIPPED, August 20 2026, later entries.**

*Form spacing, 52 files, index.html plus all 51 profiles.* The MailerLite form
rendered flattened on our pages: bullets hanging outside the text column, copy
below the list sitting flush against it. Cause was ours, not MailerLite's. Both
index.html and every profile open with a global reset, `* { margin: 0; padding:
0; }`, which reaches inside the embed and strips the ul's left padding and every
list and paragraph margin. The builder preview looks correct because the reset
is not there, which is why this read as a MailerLite problem. Fixed by restoring
padding and vertical rhythm scoped to `.ml-form-wrap`, so nothing outside the
form is reachable. Verified in a browser by the operator.

*LESSON, worth keeping.* A third-party embed inherits our global reset. Anything
we style with a universal selector styles their markup too, and their preview
cannot see it. Next time an embed looks wrong, check our reset before editing
theirs.

*PROCESS FAILURE on that commit: it shipped without a board or log entry.* The
standing rule is that TASKBOARD.md and SITE-OPERATIONS-LOG.md travel in the same
commit as the code. This one did not, because the fix was treated as a quick
follow-up to the capture band rather than as a change in its own right. The
record is reconstructed in the timing-copy commit that follows, one commit late.
Noted rather than quietly backfilled: a rule that bends for small changes is not
a rule, and "small" is exactly when it will bend.

*Timing copy, index.html.* A real signup on August 20 arrived well outside the
promised window. Nothing was broken: free-plan automations queue and delivery
time is not ours to control, so the promise was the defect. Five strings in the
modal path rewritten, "Free: Delivered Instantly" twice among them. "Check your
inbox in a few minutes" left alone, already honest. The results band makes no
timing claim; that went out with the rebuild. Profile capture copy never made
one.

*Operator action, MailerLite side, not in the repo.* The form's own line still
reads "within a minute". Change it in the builder to a few minutes. It is the
sentence a reader actually looks at while waiting, so it matters more than any
of the five above.

**SHIPPED, August 20 2026.**

*One commit, 53 files.* index.html plus all 51 profiles, plus this board and the
ops log.

*The results-screen band, P1 closed.* The offer was a single full-width
.report-row inheriting styling built for a list of five, which at desktop width
read as a beige footer strip, and the email field sat behind a modal click. It
is now a centred, width-constrained band on the deep teal ground, matching the
profile capture treatment: gold eyebrow, the same headline the profiles carry,
the five report names, then the MailerLite field inline. The preview modal
survives as a small underlined link below the field, for readers who want to
know what arrives before they hand over an address.

*The mechanism, as boarded.* returnMlForms now asks mlFormHome() where the node
belongs: the results-screen slot when it has been rendered, the hidden vault
otherwise. Two functions, no new machinery, and the vault path is untouched on
first load and on every page where the results screen has never rendered. One
hazard was found while building and is guarded. MailerLite renders each embed
once per page load, and the form node now lives INSIDE the container that
renderReportIcons rewrites. If the node is looked up after the rewrite it is
already orphaned and the field is gone for the rest of the session, which a quiz
retake would trigger. renderReportIcons therefore takes the reference and parks
the node in the vault before touching innerHTML, then moves it into the fresh
slot. Confirmed both directions in a jsdom run: the shipped order survives a
retake, a planted lookup-after-rewrite variant destroys the node.

*City detail screens.* Modal kept, card restyled. Centred, width-constrained,
white on a terra hairline border, buttons side by side and centred. It no longer
reads as a footer.

*The name line, P2 closed.* The August 19 wrap fix bound each icon to its name
but the line still centre-wrapped ragged, because the middot separators
stranded at line ends. The line is now a centred flex row with a gap, on
index.html and on all 51 profiles, so each wrapped line centres as a unit. The
separators are gone: a middot cannot strand if it does not exist, and a
pseudo-element separator would have landed at the start of a wrapped line
instead, which is worse. JUDGMENT CALL, easy to reverse if the spaced list
reads as too loose at desktop width.

*Dead code, partially cleared.* showReportSignup, showReportSignupResults,
submitReport and submitReportResults deleted after confirming zero call sites
repo-wide (the earlier greps double-counted: each name is a substring of its
Results twin). The three unregistered Netlify form stubs and the .rsp-* CSS
were left in place, because submitSignupModal still posts form-name
report-signup on the fallback path and that stub is the only remaining record of
the intent. Clearing them belongs with wiring the key events, not here.

**P2, OPEN, new: the capture path has no regression coverage in the repo.** The
jsdom test written for this session caught the node-lifetime hazard and proves
the modal-borrow-and-return case, but it needs node and jsdom and the toolchain
is python. Decide once: either add a node harness group to the gate, or accept
that the capture path is browser-tested by hand at each change. Do not leave it
implicit, because this is the second time in a week that a defect sat in a
surface no check reads.

**NOT VERIFIED IN A BROWSER.** The validator gate passes and cannot see any of
this. Test after deploy, in this
order, because the third case is the one the change exists for:
1. Finish a quiz. The email field appears inline in the teal band.
2. Open a city detail from the results. The modal still loads the form.
3. Close it, go back to results. The field is still there.
4. Retake the quiz. The field is still there.
If step 3 or 4 shows an empty white box, the node was destroyed rather than
parked; revert the commit rather than patching forward.

**SHIPPED, August 19 2026.**

*MailerLite, operator side, no repo change.* Restructured from six automations
to two, which is under the free-plan cap of three and closes the upgrade
question. The Visit workbook keeps its own automation. The five themed reports
now share one joint delivery on the former Active Frontier automation and form
(g4M1M8), which is why no form IDs changed on the site. Verified live: a fresh
test subscriber receives the joint email. Per-link click reporting replaces the
five-form picker as the interest signal, which is revealed preference at the
point of reading rather than a choice made before the reader knows what is
inside. Form copy rewritten to "Deep Dive Reports", with the five lenses as a
bulleted list and a single-email promise ("the reports will arrive in one
message within a minute").

*Commit 1, consolidation, 52 files.* Five chips and five embeds collapsed to one
visible form on all 51 profiles. index.html: renderReportIcons rewritten to a
single stated offer, REPORT_MODAL_DATA collapsed to one deepdive entry, four
dead embeds removed, both lead-in strings corrected, toggleMoreReports and
getRecommendedReports deleted as unreferenced. This was urgent rather than
cosmetic: four of the five pills pointed at forms whose automations had just
been paused, so every page was offering four routes to silence.

*Commit 2, layout, 52 files.* The site-side explanation paragraph removed from
the capture band, since the MailerLite form immediately below carries its own
description and the band was explaining the reports twice. Report names now
lead. Data Sources moved below the reports block in BOTH detail renderers, the
editorial and the legacy.

*Commit 3, wrap fix, 52 files.* Each icon and report name is now one
non-breaking unit, so a name no longer starts a line with its icon stranded at
the end of the previous one.

**CORRECTION: the P1 boarded earlier today was wrong.** It said email capture
was absent from index.html. It is not, and never was. index.html has a working
capture: renderReportIcons draws report rows on the quiz results screen and on
every city detail screen, openReportModal and openSignupModal drive preview and
signup modals, and returnMlForms moves the rendered MailerLite node between the
modal and a hidden vault (id mlFormVault). All of it has live call sites and all
of it works. What misled the session was dead plumbing sitting beside the
working system: showReportSignup, showReportSignupResults, submitReport and
submitReportResults, all with zero call sites, plus three form stubs commented
"Hidden Netlify form registration" that carry no data-netlify attribute and were
therefore never registered with Netlify either.

**This is the THIRD instance of the same error in one week,** and the pattern is
now the finding rather than any individual mistake. Cross-city figures were
asserted to be skipped by a check that never reached them. Email capture was
asserted to be silently discarding submissions from a UI that does not render.
Delivery was asserted to be broken when six subscribers show sent, opened and
clicked. In every case the mistake was reading code and asserting runtime
behaviour without checking whether that code is reachable. The operator's own
testing corrected all three. Working rule for future sessions, stated here so it
survives: presence of plumbing is not evidence of a live feature. Check call
sites and element ids before describing behaviour, and treat any assertion about
runtime that has not been verified in a browser as unverified.

**What is actually true about capture placement, corrected.** Capture exists on
all 51 profiles and on index.html. The remaining problem is presentation, not
absence. On the quiz results screen the offer renders as a single full-width row
inheriting .report-row styling designed for a list of five, which at desktop
width reads as a beige footer strip rather than an offer, and the email field
sits behind a modal click at the highest-intent moment on the site. Six signups
since April is a presentation outcome.

**P1, CLOSED August 20: the results-screen offer does not look like an offer.** Rebuild it
as a centred, width-constrained band matching the profile treatment, with the
email field inline rather than behind the modal. The inline field is achievable
without new machinery: returnMlForms currently returns the node to mlFormVault,
so give it a results-screen home slot to prefer, falling back to the vault when
that slot is absent. Defensive, two lines. City detail screens keep the modal
but need the same restyle so the card stops reading as a footer. RISK: this
touches the only working capture path on index.html and cannot be verified
without a browser. Test after: finish a quiz and confirm the field appears; open
a city detail and confirm its modal still loads the form; return to results and
confirm the field is still there. The third case is the one the change exists
for.

**P2, CLOSED August 20: the report-name line centres badly on narrow screens.** The wrap fix
shipped today only stopped names splitting from their icons. The line still
centre-wraps into a ragged three-then-two shape. Fix with flex, a gap and
justify-content:center so each line centres as a unit, or stack on mobile.

**P2, OPEN: deep-dive-reports.html plus a nav tab.** Operator proposal, endorsed.
One page: the five reports, a short line each, the form, no picker. Nav item on
all 52 pages in second or third position, never first, since the quiz stays the
lead. Value beyond navigation: it is a real Pinterest destination during travel,
and a canonical target for the #deep-dive-reports anchors already on 51
profiles. Scope it as a proper build, not a tweak: sitemap, canonical, JSON-LD,
nav across 52 files, validator coverage. No star badge; use the existing gold
accent.

**P2, PARTIALLY DONE August 20: dead capture code on index.html.** Four functions deleted; the three Netlify stubs and the .rsp-* CSS remain, deliberately, until key events are wired. The four zero-call-site functions
and the three unregistered Netlify stubs described above. Delete them when the
results-screen rebuild ships, since that work is in the same code. Cost so far:
one session, three wrong diagnoses.

**Still open from earlier entries, unchanged:** the twelve stale cross-city
figures and the three-layer validator extension; key events for signup and
affiliate click, which remain unwired so nothing shipped today is gradeable; and
the profile-to-tools routing, still the largest lever at current scale, with two
hundred and two users reaching a profile against six reaching a tool.

**Operator constraint, for planning.** Laptop available roughly ten days from
August 19, then travel with an iPad and phone only. Travel work is pins and
possibly Reddit. Anything requiring a repo commit needs to happen before then.
Hold Reddit until the capture presentation work ships, since sending hard-won
traffic at the current results-screen card wastes it.

**Last updated:** August 19, 2026, OPS: quiz demand read, funnel read, email
capture restructure
(51 profiles live, 24 comparison pages live. No site change. The growth pick
opened on Aug 18 is now made: the funnel converts until the point where money
or an email could happen, and email capture is absent from the two pages
carrying most of the traffic.)

**THE READ, August 19 2026. Two exports, one conclusion.**

*Search Console, quiz page, three months to Aug 17.* Two hundred and
seventy-one clicks on one thousand five hundred and seventy-six impressions,
position 4.7. One hundred and twenty-eight clicks are attributed to named
queries and the rest sit in the anonymised tail, which converts BETTER than the
head, nineteen percent against fifteen. Of the named ones, "where should i
retire quiz" alone takes seventy-two, and the top five take ninety-three
percent. Eleven queries drew a click and every one is a variant of the same
phrase. Fifteen of eighteen queries contain the word "quiz". ZERO branded
queries: nobody searches the site name, so every click is discovery and there
is no brand demand to fall back on.

*The trend is the finding that reframes the concentration.* Zero impressions
until mid-June. Weekly clicks since: thirteen, thirteen, fourteen, thirty-eight,
sixty-one, thirty-two, forty-four, forty-nine. Click-through went nine and a
half percent in the middle third of the window to twenty-one percent in the
last. This is an eight-week-old ranking still climbing, not a mature asset on a
plateau, so the sixty-four percent click concentration is what "exactly one
thing has matured" looks like rather than a structural fragility. The first
impressions predate the June 21 quiz subtitle change, so this is ordinary
maturation and there is nothing to reverse-engineer.

*GA4, twenty-eight days to Aug 18, three hundred and sixty active users.* The
handoff works. The ranking page bounces at 4.9 percent. Two hundred and two
users of three hundred and sixty, fifty-six percent, reached a city profile.
Average engagement is four minutes fifty. The Aug 15 thesis is confirmed by
behaviour: fifty profiles pulled two hundred and two users while earning almost
no search traffic of their own, which is what conversion inventory looks like.
Acquisition is google organic two hundred and fifty-one users of three hundred
and sixty; Pinterest delivered about eleven users across fifty sessions, which
is worth calibrating against how this board has treated that channel.

*Where it breaks.* The state tax tool and the affordability calculator, which
carry the financial-advisor affiliate inventory, drew SIX users between them.
Traffic flows Google to quiz to profile and stops. No key events are configured,
so signups and affiliate clicks are unmeasured and no change made now can be
graded.

**P1, CLOSED August 22 2026. Read the correction before the entry below: both
halves are resolved and neither resolved the way this entry expected.** The
entry as written names two pages and is stale on both. It is kept for the
reasoning, which still holds, and for the six-signup baseline.

*`index.html`, closed August 20.* The results screen now carries the MailerLite
field inline, on the deep teal band, at the moment the matches are revealed.
This entry's claim that index.html "has no rendered capture at all" has been
false since that commit.

*`where-should-i-retire-quiz.html`, closed August 22 as NOT APPLICABLE, and this
is the part worth reading.* This entry counts it as a page missing capture. It
is not a destination. It is a search landing page built to rank and hand the
reader off to the quiz, and it carries two CTAs that both go there. Capture does
not belong on it: a reader who arrives, reads a headline and clicks through has
been given nothing yet, and an email ask at that moment is a toll in front of
the value rather than an offer after it. That is the standing board instruction,
DO NOT GATE ANYTHING, and it applies here even though the surface looks like an
opportunity. The offer reaches these same people two clicks later on the results
screen, where it already exists.

*The number that will be misread, flagged now so it is not acted on.* GA4 shows
this page at roughly 4 seconds average engagement against 4m 56s for
`index.html`. Four seconds looks like a bounce and IS NOT one. It is a doorway
page performing its function: land, orient, click through. Do not rewrite,
consolidate, or "fix" this page on the strength of that figure.

*What it actually needs, and it is small.* The handoff is unmeasured. 218 views
and 190 users in the window, and nothing records what fraction take either CTA
to the quiz versus leaving. One click event on both CTAs makes 4 seconds
readable: a high click-through means the page works, a low one means the handoff
leaks. The page also has no `RMH-ANALYTICS-V1` block, which matters here not for
signups but because that block is where any click instrumentation on the page
would live. Belongs to the routing session, which is about exactly this.

**P1, ORIGINAL TEXT, superseded August 22 2026: email capture is absent from the
two pages that carry the traffic.**
Six signups since April. The cause is placement, not demand and not a defect.
Capture exists ONLY on the fifty-one city profiles, near the bottom, behind a
five-chip picker that requires choosing a guide before a field appears.
index.html, the quiz engine, two hundred and sixty-three users in twenty-eight
days, has no rendered capture at all. The quiz landing page, one hundred and
ninety-eight users, has none either. The offer has never once appeared at the
moment of intent, so the six-signup number is not yet evidence that the guides
are unenticing and must not be read as such.

**THE MAILERLITE CONSTRAINT, and why delivery stopped.** MailerLite changed the
free plan on June 16 2026: two hundred and fifty subscribers, two thousand five
hundred monthly emails, and caps of three automations, three forms, one landing
page. Enforcement began August 13 2026. The account carries six automations, the
five themed guides plus the Visit workbook, against a cap of three. Confirmed
live on Aug 19: the six real subscribers all show emails sent, opened and
clicked, and a fresh test subscriber shows zero emails sent. The stack is
HEALTHY. Delivery stopped because the account is over the feature cap, and a
paused automation cannot be reactivated without upgrading. Nothing about this is
a code defect and no repo change fixes it.

**DECISION, operator, Aug 19 2026: restructure to two automations, do not
upgrade.** Twelve dollars a month to run six delivery pipes for six subscribers
inverts the infrastructure against the audience. Keep the Visit workbook on its
own automation, since it serves a different moment (visit planning, post-
shortlist) and is the strongest fit for a reader who just finished the quiz.
Collapse the five themed guides into ONE joint automation delivering all five as
links. Two automations against a cap of three, one slot spare, pricing question
closed. The interest signal survives and improves: per-link click reporting
tells us which of the five people actually want, which is revealed preference at
the moment of reading rather than a choice made before anyone knows what is
inside. Free-tier caveat to confirm in the dashboard, not from a chat: whether a
segment can be built directly from a link click or only viewed in the report.
Multi-trigger automations are not on the free plan, so every form must assign
the same group per automation for the single trigger to catch it.

**Sequence is one-way and matters.** Get under the cap BEFORE editing, because a
restricted account cannot create or edit automations. Pause four, restructure
the survivors, retest with a genuinely fresh address, confirm delivery, and only
then build anything on the site. Any capture built before delivery is confirmed
collects addresses and sends silence, which is worse than having no capture,
because those are people who raised their hand.

**THE WORK ORDER, ten laptop days from Aug 19 2026, then travel.**
Dashboard first, no laptop needed: restructure to two automations, retest,
confirm delivery. Then, in order:
1. One offer on the quiz RESULTS screen, ungated, single field, no chip picker.
   Highest-intent moment on the site and currently the emptiest.
2. The same single offer on the quiz landing page, one hundred and ninety-eight
   users and zero asks.
3. Simplify the profile capture from five chips to one offer pointing at the
   joint guides group.
4. Wire the key events, signup and affiliate click, so the next change is
   gradeable.
5. Profile-to-tools routing with the remaining days: two hundred and two users
   reach a profile, six reach a tool.
Do NOT spend laptop days on pins. Pins are the one item on this list that works
from an iPad, and they are the correct travel activity. Calibrate expectations
to the eleven users they delivered in twenty-eight days. Hold Reddit until
delivery is confirmed.

**DO NOT GATE THE RESULTS.** Operator instinct, endorsed on the data: fifty-six
percent of users reach a profile and that flow is the healthiest metric the site
has. A gate trades the best behavioural number for a handful of emails on a
funnel still growing. Capture goes AFTER value is delivered, as an enhancement,
never as a toll.

**Realistic scale, so nothing is over-invested.** At three hundred and sixty
users a month a good capture rate returns seven to ten signups a month against
the current one and a half. That is a five-fold gain on a small number. Email is
an owned asset and a slow one; it will not pay this year. The routing work is
the larger lever at this scale.

**P2, OPEN: dead capture code on index.html.** The page carries orphaned
plumbing for a capture that does not exist: functions showReportSignup,
showReportSignupResults, submitReport and submitReportResults, the CSS for
report-icon-btn, and three hidden form stubs commented "Hidden Netlify form
registration". NONE of the referenced element ids exist as markup, and no form
carries the data-netlify attribute that Netlify requires to register a form at
deploy time, so the stubs were never live either. If those functions were ever
called they would throw on a null element. Delete when the real capture ships.
Recorded because this code cost a session two wrong diagnoses in one hour: first
that the quiz was silently discarding submissions, then that delivery was
broken. Code that looks like a shipped feature and is not is a trap, and this
board's own principle covers it: the defects that survive longest live in
surfaces nothing reads.

**Corrections on the record, August 19 2026.** Two assertions made in session and
disproved by the operator, both from inferring live behaviour out of code without
checking reachability. (1) "Every visitor who typed an email into the quiz result
screen was told check your inbox and lost" was FALSE; the UI does not render and
nobody was ever offered a form there. (2) "Delivery is broken" was FALSE; the six
real subscribers show sent, opened and clicked. The operator's test signup and
her reading of her own dashboard corrected both. The general lesson, worth more
than either: presence of plumbing is not evidence of a live feature, and the same
error appears twice in the same week in the cross-city figure work.

**Last updated:** August 18, 2026 (third entry), board hygiene: supersession
marker, highlight-figure audit, growth queue empty
(51 profiles live, 24 comparison pages live. No code, no site change. Three
board jobs: the Aug 3 growth-cycle section is now marked superseded in place,
the cross-city figure audit is written down, and the growth queue is recorded
as empty.)

**P2, OPEN: stale cross-city price figures in the two string layers no check
reads.** Opened by the tampa-vs-naples session, August 18 2026. Home values are
copied into three places on index.html: the `highlight` field, the `pros` and
`cons` arrays, and the CITY_ENRICHMENT D1-D10 score notes. `check_highlight_homes`
reads the first and nothing reads the other two. All three render, so this is a
reader-visible defect and clears the growth-cycle rule against machine-only
checks.

Twelve stale cross-city claims found by hand audit against the database, all
live before this session, worst first: Paducah says Memphis is $195K against a
database $147,000; Frisco says San Antonio is $320K against $251,000; Casper
says Boise is $314K against $508,000; Naples says Fort Myers is $372K against
$310,000; Corpus Christi says Fort Myers is $372K against $310,000; Naples says
Sarasota is $462K against $413,000; Paducah says Tulsa is $194K against
$223,000; Frisco says Georgetown is $457K against $428,000; Missoula says
Durango is $704K against $768,000; Missoula says Bozeman is $740K against
$734,000; Corpus Christi says Pensacola is $264K in two separate fields against
$269,000; and New Orleans states its own citywide median as $250K in a score
note against $248,000.

Two are worse than a stale number. Paducah's reads that its $192K home is under
Tulsa at $194K and Memphis at $195K; Memphis is actually $147,000, so the
comparison points the wrong way, which is the check-the-sign-of-the-gap rule
failing in prose. Casper's reads "$314K typical home value, below Boise
($314K)": the parenthetical repeats Casper's own figure rather than Boise's.

**This is the same drift, one layer down.** The July 23 2026 entry further down
this board repaired sixteen drifted figures in the database Highlight column and
names "Memphis $170K/$195K" and "San Antonio $260K/$320K" among them. Those are
the same numbers still sitting in the pros arrays and score notes today. The
repair moved the layer that had a check and left the two that did not.

**Correction on the record, because the first diagnosis was wrong.** The Tampa
entry that started this said Naples "matches it at $585K" against $549,000, and
that was first written up as `cross_city()` skipping the figure. It is not:
HL_HOME_FIG only matches a figure anchored to a home-value noun, so a bare
"$585K" is never a candidate and the cross-city gate is never reached. Measured
across all one hundred and ninety-eight highlight strings, that gate is
currently inert: zero anchored figures are being skipped for naming another
city.

**Fix spec, for the next debt day, in this order.** Extend the check first, let
the check produce the list, then repair all layers for a city in one pass. Do
not repair from the twelve above; it is a hand audit and the check will find
more. Three parts, none of which ships without a planted-error harness:
(a) widen HL_NOUN to catch a bare "citywide median $X", which is what hid the
New Orleans and Tulsa figures and which is not a cross-city case at all;
(b) read all three string layers, not just `highlight`;
(c) resolve a cross-city figure against the NAMED city's row instead of skipping
it, keyed on (City, ST).

The (City, ST) key is not optional. Wilmington DE's score note reads "Greenville
(~$1.085M)", meaning the Delaware neighborhood, not Greenville SC. A name-keyed
pass will silently "correct" a correct figure to $333,000. This is the second
time the two-Wilmington shape has produced a trap; the first closed the slug
resolution P1 on August 17.

**Two figures currently disagree with themselves,** created by this session and
not pre-existing: Corpus Christi's highlight now reads $269K for Pensacola while
its pros array and score note still read $264K, and New Orleans' highlight reads
$248K while its score note reads $250K. Repairing one layer without its siblings
is the containment rule failing. They ride along in the batch above rather than
getting a hotfix.

**OPEN, August 18 2026: the growth queue has no named item in it.** The Aug 17
Search Console read produced exactly one missing-page finding, tampa-vs-naples,
and it shipped this session. Nothing else is boarded as the next growth job, so
the next session is an OPS pick rather than a build, and it should start from
the Search Console read in SITE-OPERATIONS-LOG section 7 rather than from this
board. The strongest unworked finding there: the quiz page earns sixty-four
percent of every click the site gets, at position 4.8 and a 16.9 percent
click-through rate. That is a concentration finding and it has never been
worked. Whether the right response is to defend it, widen it, or route from it
is the question to answer before building anything else.

**Last updated:** August 18, 2026 (second entry), tampa-vs-naples comparison page
(51 profiles live, 24 comparison pages live. The one true missing-page finding
in the Aug 17 Search Console export is now built: "tampa vs naples for
retirees", forty-four impressions at position thirty-five with no page behind
it. Title carries "for Retirees" rather than "for Retirement", the first page
on the site to do so, deliberately, as a free test on a query with no ranking
to protect. Reciprocal CTAs added on both profiles; hub card and ItemList
position twenty-four added.)

**SHIPPED, August 18 2026: three garbled strings and five stale price figures.**
The garbled ones are remnants of the superlative scrub, all rendering to
readers: "with our databSt. Pete's Walk Score" in the tampa-vs-st-petersburg
tradeoff block, "and os Walk Score" in that page's FAQ answer (both anchors,
visible copy and FAQPage schema), and "$549Konthly costs" in the Naples cons
array in index.html.

**P2, OPEN: check_highlight_homes reads only self-labelled home figures.**
Found while repairing the fifth defect above and worth stating precisely,
because the first diagnosis was wrong. Tampa's highlight said Naples "matches
it at $585K" against a database $549,000. The initial reading was that
cross_city() had skipped it. It had not: HL_HOME_FIG requires a figure
anchored to a home-value noun ("typical home value", "median home"), and a
bare "$585K" is never a candidate at all, so the cross-city gate is never
reached. That gate is currently inert; across all one hundred and
ninety-eight highlight strings, zero anchored figures are being skipped for
naming another city.

The measured hole: thirty-two dollar figures in highlight strings are read by
neither highlight pattern. Most are correctly out of scope (neighborhood
ranges, a museum construction cost, an estate-tax threshold). Five were price
claims and all five disagreed with the database. Tampa on Naples, $585K
against $549,000. Chattanooga on Asheville, $462K against $464,000. Corpus
Christi on Pensacola, $264K against $269,000. New Orleans on its own citywide
median, $250K against $248,000. Tulsa on its own citywide median, $194K
against $223,000, which is the largest miss and which the Tulsa profile
already had right in its rendered copy. All five repaired in this commit, on
both mirrored surfaces.

The last two are the finding worth keeping: they are not cross-city at all.
"Citywide median $194K" says median without saying home, so the anchor never
matches. The fix is two changes to the check, and neither ships without a
planted-error harness: extend HL_NOUN to catch a bare "citywide median $X",
and resolve a cross-city figure against the NAMED city's row instead of
skipping it. Keyed on (City, ST), because a name-only lookup is how the two
Wilmingtons collided before.

**Last updated:** August 18, 2026, for-retirees vocabulary pass
(51 profiles live, 23 comparison pages live. Descriptions and one subheading
per comparison page now carry "for retirees", the phrase both of the largest
comparison queries use and no page used. Titles untouched by design.)

**Last updated:** August 17, 2026, matchup pills + Search Console read; Wave 2/3 suspended
(51 profiles live, 23 comparison pages live. The font sweep injected CSS into
the quiz script and killed it; fixed, and the gate now parses every inline
script with node so page JavaScript can never silently break again. Favicon
moved off the teardrop to a Work Sans R in the teal tile: the teardrop read as
a balloon at tab size, and a letter that matches the name a reader just typed
is the one thing a favicon is reliably good at.)

**IN FLIGHT, schema shipped Aug 11 2026: a tax filtering tool.** Strongest remaining tool
candidate. State-level scope, so roughly thirty-nine rows rather than ninety-nine, and the
queries are question-shaped, which is the shape the quiz page already ranks for.

**The finding that decides whether it can be built at all: D5 will not drive it.** D5 is a single
composite blending five things, tax on Social Security, tax on pensions and IRAs, overall income
rate, property tax and sales tax. That is right for the quiz, which weighs tradeoffs, and wrong
for a filter, because it will not run backwards. Montana and Oregon sit one band apart, but
Montana taxes Social Security and Oregon exempts it, and neither score says which. A reader
searching for states that do not tax Social Security needs a yes or no, and no composite can
produce one.

So this is a data-structuring job before it is a build job. The facts already exist in the repo
as prose: `docs/D5-TAX-METHODOLOGY.md` section six carries per-state anchors with exactly the
detail a filter needs. Turning that into discrete state-level fields is the work.

Both operator decisions are made and shipped. The fields live as a State Tax Facts sheet
inside the CityDatabase (v18), one row per live state, thirty-nine rows, keyed on ST, with
closed enum vocabularies and the PropTax mirror populated from the City Database sheet.
Populating the remaining columns is a data addition, not a scoring change, gated by a one-time
D5-versus-facts reconciliation before the tool launches; any D5 that moves in that pass is a
scoring change and goes through the normal process. No front-loading of states without cities:
the validator now forces the facts row for a new state into the same commit as its first city.

Population pass shipped Aug 11 2026 (v19): all thirty-nine states populated across every
column, Tax Year stamped 2026, sources on every row; the completeness check shipped in the
same commit and the blank-enum tolerance is retired. The D5 reconciliation ran against the
populated facts: no score is flat-out wrong, and the tolerated one-point spreads stand as
documented. The Pennsylvania tension is resolved: operator approved Aug 11 2026, Pennsylvania unified at
seven, Philadelphia moved from six with Pittsburgh unchanged, anchored to Iowa at eight minus
the inheritance tax. Rationale recorded in `D5-TAX-METHODOLOGY.md` section eight. Every
surface carrying the score moved in the same commit: the database, the quiz city array, the
pick-and-compare array, and the affordability calculator array.

Methodology shipped to v1.1: scoring a new state now means filling its facts row and
reading the sheet. The tool build shipped Aug 11 2026, fourth session:
`states-that-dont-tax-retirement-income.html`, five checkbox filters and two sliders over
the facts sheet, state cards with the note prose and city chips linking through the
standard `index.html?city=` route. Filter state reads from and writes to the URL
query string, so any combination deep-links (for example `?ret=1&inherit=1`), which
makes the one page a landing page per Pinterest pin; the canonical tag keeps all
variants one page for search. The page embeds TAXFACTS and TAXCITIES as generated
JSON; `check_taxtool_data` (figures group) compares every field, note, and city D5 to the
workbook on every run, with a seven-plant harness at `tools/test_taxtool.py`. Cross-linked
both ways with the affordability calculator; sitemap entry added. This closes the tax
thread that opened with the D5 scoping session.

New hygiene item, priority P2, found during the reconciliation: the Scores by Dimension
sheet in the CityDatabase is a stale second copy of the canonical scores. It carries
eighty-nine rows against ninety-nine cities, and spot checks show drifted values (for
example Philadelphia D2 reads five there against nine in the City Database). No validator
check reads it and no page renders from it. Decide: delete the sheet, or bring it under
validation. Left untouched in v19.1 rather than cosmetically patching one cell of a sheet
that is wrong elsewhere.

Side benefit worth weighing: SCORING-RUBRIC.md flags that tax figures in profile `scoreNotes`
carry year stamps that nothing in the toolchain ages, and Arkansas was already found described
as a flat rate when it is graduated. Structured tax fields would give the validator something to
check that prose against.

**CLOSED, August 10 2026: the last body quiz CTA still pointing at `index.html`.**

`pick-and-compare.html` was missed by the batch earlier the same day, which keyed on
`class="quiz-cta-btn"` while that page uses `class="cta-btn"` for the same button. It
was the only page on the site carrying a header quiz button and no link at all to
`where-should-i-retire-quiz.html`. Found by diffing the two sets, forty-three against
forty-two, rather than by re-reading the batch. Its CTA copy also said three minutes
where the rest of the site says two; corrected in the same edit.

**The header buttons stay pointed at `index.html`, decided rather than deferred.** All
forty-three of them. Forty-two of those pages already reach the landing page through
their body CTA, and a second link from the same page to the same destination buys
little, so repointing the headers would have added friction across the whole site to
gain new link equity from one page. Someone clicking a header button labelled Quiz
wants to take it, not read about it. Revisit only if the landing page stops ranking.

**SHIPPED, August 10 2026 (second session): `where-can-i-afford-to-retire.html`.**

The first tool on the site that takes a figure from the reader about their own money.
Three inputs, cash down, monthly budget, and buying or renting. Affordability filters,
the dimension scores rank. Implements BUDGET-METHODOLOGY.md section 14, added the
same day: one term of the section 3 formula varies, principal and interest is amortised
on typical home value minus equity instead of on eighty percent of it, and property tax
and homeowners insurance are retained in full because they attach to the house and not
to the loan.

Section 14.2 forbids ranking on the equity-adjusted figure, because removing the
mortgage strips out most of the cost variance between cities and a cost ranking at high
equity inverts. Cost filters and never sorts. The page says so in prose, and the reason
is written into the script comment so the next editor does not helpfully add a sort.

`check_afford_data` plus `tools/test_afford_data.py` ship with it. The page holds its
own copy of six database columns for all ninety-nine cities, which is a second copy of
the database and therefore exactly the drift this validator exists for. The check
asserts roster, then every cell, then that the page's own inputs rebuild the published
`Monthly Est` string and `Budget Range` integer through the formula. That last assertion
is the `Monthly Est == f(Median Home)` gate BUDGET-METHODOLOGY.md section 9 has been
asking for; it now runs on every deploy.

The page was added to all four hand-maintained target lists in the same commit:
`check_emdash`, `check_superlatives`, `check_hardcoded_counts`, `check_tag_balance`.
Each of those has previously shipped clean over a page it was not reading.

**The rank excludes D2 Budget.** Nine dimensions, not ten. Cost is already the filter,
so including D2 in the ordering would let price decide the outcome twice, and it does
the most damage to exactly the reader this page is for: someone arriving with a large
cash-down figure gets pushed toward cheap-housing cities on account of a mortgage
payment they are not making. `RANK_SKIP` names the excluded index rather than hiding
it in a loop bound. Scores render out of 90.

**Section 5 of BUDGET-METHODOLOGY.md gained an order-of-operations clause** in this
commit. The utilities line never said whether the climate adjustment lands before or
after the state multiplier, and the two readings disagree on six cities. The order was
recovered from the database while building this page, which is one recovery more than
it should have needed. Now written down, and asserted.

**One thing left open.** The renting option uses the published mortgaged figure and
ignores the cash input, per section 14.3, because the database has no rent column and
inventing one would break the data-source rule. Stated plainly on the page in three
places. A real rent basis needs its own data source and is a separate job.

**SHIPPED, August 10 2026: five commits, all driven by Search Console and GA4 rather than
by the build queue.**

`458c378` canonical on index.html and privacy.html, `check_canonicals` plus planted-error
harness, dead affiliate-policy link and sitemap entry removed.
`dcc5317` guide title tags front-loaded.
Results screen: recommended reports sorted to top, remainder collapsed, restart bar moved
below the offer.
Quiz CTA on forty-one pages repointed to `where-should-i-retire-quiz.html`; two hardcoded
city counts removed from that page.

**The finding that reframed the session.** Search Console: 340 clicks across ninety days,
235 of them in the last twenty-eight. Daily search clicks went from roughly 1.7 to 8.4, a
fivefold rise, while impressions only doubled. The site is not flat; a ninety-day average
was hiding a steep recent climb. `where-should-i-retire-quiz.html` accounts for 134 of the
gained clicks on its own, at position 5.07 for "where should i retire", and its top query
gained only 39 of those, so the rest arrived through a long tail of the same question.

**The orphan.** A grep of all ninety-seven pages found exactly one reference to
`where-should-i-retire-quiz.html` in the repo: its own canonical URL. No page linked to it.
Google reached it through sitemap.xml alone. Every quiz CTA on the site pointed at
`index.html`, which competes for the same intent and sits at position 16.8. Internal equity
was flowing to the weaker of the two pages. Forty-one CTAs now point at the stronger one.

**What the numbers actually say about page types.** Themed and landing pages earn about
2.6 search clicks per page per month, comparison pages about 1.4, city profile pages 0.20.
GA4 caps profile views at 112 a month via `breakdown_click` and the real figure is nearer
sixty, so profiles are not search assets and are barely internal ones either. Building more
of them to attract search traffic is answered: do not.

**Funnel, twenty-eight days.** 341 users, 216 quiz starts, 193 completions (89% of starters,
which is excellent and should not be touched), 64 clicks into a city, 6 report requests.
The drop is entirely after the results screen.

**Channel mix, twenty-eight days.** Organic Search 372 sessions (70%), Direct 103, Organic
Social 43, Unassigned 24, AI Assistant 11 at a 73% engagement rate, the highest of any
channel. Pinterest is a minority channel; the assumption that it was carrying the site was
wrong. Internal traffic filter confirmed Active, so these are clean.

**WATCH, four to six weeks.** `quiz_start` for regression from the CTA reroute (the path to
the quiz is now one click longer from forty-one pages; this is the first change to reverse
if starts fall). `reports_expand` against `report_request` to separate a placement problem
from an offer problem. Position on "where should i retire" for movement off 5.07.

**PARKED.** Landing-page typography and visual treatment, operator-flagged as long-standing
dissatisfaction, deliberately not addressed in a session about measurement.

**OPEN.** `affiliate-policy.html` was never written; the sitemap entry and the
`visit-before-you-decide.html` link to it were removed rather than the page created. The
disclosure paragraph on that page is complete and carries the substance. Decide whether a
standalone policy page is wanted.

**Last updated:** August 8, 2026, fayetteville-vs-bentonville shipped
(COMPARE; 51 profiles live, 23 comparison pages live. New page, hub card and schema entry,
reciprocal CTAs on both profiles, sitemap. No DB change, no score change.)

**SHIPPED, August 8 2026: fayetteville-vs-bentonville-retirement.html.**

The tightest pairing on the site so far. One dimension of ten clears the two-point bar, D2 budget
at 8 against 6. Six dimensions are dead level, and D1, D5, D7, D8 and D10 are identical figures,
not merely close. Both cities are served by XNA, both carry a 0.56% effective property tax rate,
both carry the same $3,733 insurance estimate, and Jan mean, annual snowfall and annual sun are
identical at 36F, 11in and 60%. Four checkmarks ship on the whole table: three cost rows and D2,
all to Fayetteville. The climate block ships entirely unmarked.

**The five-versus-three question was raised and dropped rather than answered.** The COMPARE brief
proposed overriding COMPARISON-PAGE-STANDARD-v2's five-block narrative down to three, on the
grounds that six tied dimensions leave nothing to trade off. That rests on reading item 4 as five
tradeoffs. It is not: it is a fixed arc, and two of its five blocks, "What they share" and "The
honest shared downside", are about similarity and get STRONGER as the pairing tightens. Burlington
vs. Portland ME ships those headings verbatim. No override was taken and the standard is unchanged.

**Two findings boarded, not fixed here.** See P1 and P2 below.

**Last updated:** August 8, 2026, Saratoga Springs NY profile shipped
(BUILD; fifty-one profiles live, twenty-two comparison pages live. Three stale "Perfect 10 community" claims
corrected in the same commit.)

**CLOSED, August 17 2026 (BATCH): the slug-resolution P1.** Both checks now resolve every
comparison slug through PUBLISHED_PROFILES into a `(City, ST)` database key via a shared
`_comparison_row()` helper, and every miss FAILS loudly instead of skipping. The landmine fired
exactly as sized below: the moment `portland-me` resolved, the gate threw the two predicted
`&ndash;` budget-cell failures on `burlington-vs-portland-me`, fixed to literal en dash in the
same commit (its caption entity converted too, matching every sibling page).
`tools/test_comparison_slugs.py` ships alongside, 5 plants: control, wrong score on the
state-suffixed page, wrong cost cell on it, unresolvable slug fails loudly, and a slug rebound
to Wilmington DE fails, which is the wrong-city landmine made executable. Gate 0/0.
The original sizing, kept for the record:

**P1 (measured August 8, COMPARE fayetteville-vs-bentonville): the slug-resolution item now has a
size, a second failure mode, and a landmine behind it.**

*Size.* Of the 23 pages the hub lists, exactly one is silently skipped by both
`check_comparison_scores` and `check_comparison_cost_rows`: `burlington-vs-portland-me`, because
`portland-me` does not resolve. Every other page genuinely runs. That is a smaller blast radius
than the open item implied, and it is worth having the number rather than the fear.

*Second failure mode, worse than skipping.* The lookup is built as
`name.lower().replace(" ","-").replace(".","")` with no state suffix, so Wilmington DE and
Wilmington NC both key to `wilmington` and the dict keeps whichever row is built last. A future
wilmington comparison page would not be skipped; it would be validated against the WRONG city's
figures and pass. Keying on City plus ST closes both this and the skip.

*The landmine.* Fixing the slug resolution will not be a no-op. The moment `portland-me` resolves,
`burlington-vs-portland-me` starts being checked for the first time, and its two
`Estimated retiree budget` cells fail immediately: they carry `&ndash;` where `_dashes()` only
normalises literal en dash, em dash and hyphen, so the entity never matches the DB string. Expect
two cost-row failures the same commit the slug fix lands. Fix them together or the gate will look
like the slug fix broke something.

*Knock-on for anyone templating.* `burlington-vs-portland-me` is the most recent page and the
natural reference build, but it is also the one page these checks have never read. It is not a safe
source for cell-level conventions. Comparison tables need the literal en dash and the literal tick
character; entity forms pass unnoticed only on a page nothing is checking. Confirmed August 8:
Fayetteville and Bentonville both resolve, so both checks genuinely ran on the new page, which is
how the entity problem was caught at all.

**P2 (raised August 8, COMPARE fayetteville-vs-bentonville): Climate preference fields disagree
across one metro.** Fayetteville and Bentonville sit thirty minutes apart and carry identical
`Jan Mean F` (36), `Ann Snow in` (11), `Ann Sun %` (60), `HUM` (7) and `HEAT` (7). Their quiz
preference-match fields do not agree: `Climate Hot Sum` 6 against 3, `Climate Warm W` 5 against 4,
`Climate Dryness M` 4 against 6. A three-point spread on hot-summer fit between two cities with the
same heat severity is not defensible. Across the DB `Climate Hot Sum` tracks inversely with `HEAT`
(Burlington HEAT 4 / Hot Sum 9; Portland HEAT 3 / Hot Sum 8), which puts Bentonville's 3 at HEAT 7
as the likely bad cell rather than Fayetteville's 6. This does not touch any rendered page, since
the standard bars preference-match rows from comparison tables, but it does change quiz matching: a
reader asking for hot summers gets one of these two cities and not the other, on what looks like a
data error. Do not correct a single cell in isolation; audit `Climate Hot Sum` against `HEAT`
across all 99 rows and fix the class.

**SHIPPED, August 8 2026: Saratoga Springs, NY (Wave 1).**

Fourth-range city, and the first profile built on a dimension vector with no pillar at all.
Nothing scores 9 or 10. Four dimensions tie at eight (walkability, safety, community,
resilience), outdoor supports at seven, and two hard flags bind: tax at two and budget at
four. The hero tagline and opening character paragraph carry the cluster rather than leading
with the arts, which is the emphasis the ranked brief exists to force.

**Three stale claims corrected, found during the brief step.** Live `index.html` asserted
"Perfect 10 community" in both the `highlight` string and `pros[0]`, `pick-and-compare.html`
carried the same highlight, and the `culture_walkable` pairings block carried `s1: 10`.
The database says D10 Comm. is eight. Separately `value-navigator.html` badged Saratoga as
Range three against a database Budget Range of four, while Frisco on the same page at the
same monthly figures badged Range four correctly. None of the four trips any existing check.
`pros[2]` also carried "Most walkable small city in Upstate NY", an outside-world superlative
with no citation behind it, replaced with the walkability score.

**Boarded, not fixed: the Saratoga home-value gap.** The database carries Median Home at
$663,000. The live Zillow ZHVI page for Saratoga Springs read $618,681 at the end of June
2026, a gap of about seven per cent. The data-source rule says the profile displays the
database figure and it does, in every one of the five places the profile names a home value.
Flagged for the next database pass rather than reconciled here, on the Burlington snowfall
precedent: a build chat is the wrong place to overwrite a database cell.

**No Neighborhood Reality Check.** The callout test is whether the citywide figure understates
the retiree-target budget. Here it overstates the cheap end and understates only the east
side, and the outer towns run below it, so the method callout in the neighborhoods section
carries that spread instead. The `.reality-check` CSS was stripped from the clone so the
profile does not register in the NRC roster grep.

**Before that:** August 8, 2026, budget-label P0 fixed, push one of two
(OPS; 50 profiles live, 22 comparison pages live. `index.html` only. The quiz budget question
now renders five distinct ascending bands from one constant. The guard is not yet written;
until push two ships, nothing in the toolchain reads quiz option labels.)

**SHIPPED, August 8 2026: the quiz budget question renders five distinct bands.**

`BUDGET_BANDS` is now a module-level constant in `index.html`, referenced by `renderBudget()`
and by the results prose. `BUDGET_OPTIONS` is deleted. The local `BUDGET_LABELS` array inside
`renderBudget()` is deleted. One array, two consumers.

**Bands shipped, and why midpoint rather than low end.** The fix spec below called for deriving
labels from the DB `Budget Range` LOW-END bands (`under $5,000`, `$5,000-5,899`, `$5,900-6,899`,
`$6,900-8,899`, `$8,900+`). That was the wrong statistic and was overridden. `Monthly Est` is a
range; its low end is the cheapest month a city ever has. The candidate filter already grants a
deliberate one-range stretch (`budgetRange <= quizState.budget + 1`, commented as such), so
deriving the labels from the low end stacks a second undocumented stretch on top of it. Worked
example: a reader stating $6,200 would select Range three under low-end labels, admitting all
twelve Range four cities, including Boulder at $8,000-$10,000 per month. Boulder's cheapest month
is twenty-nine per cent over that reader's stated budget and its typical month is forty-five per
cent over.

The set actually shipped is the MIDPOINT of each range's `Monthly Est` span, rounded at the seams:
`Under $5,500`, `$5,500-$6,500`, `$6,500-$7,500`, `$7,500-$9,000`, `$9,000+`. Midpoints by range
are R1 $4,300-5,550, R2 $5,600-6,550, R3 $6,600-7,400, R4 $7,750-9,000, R5 $9,950+.

**Labels rounded, August 8 2026 second push.** The displayed labels were rounded to clean hundreds.
A column of figures ending in 499 and 999 is harder to read at a glance than one ending in round
hundreds, and this is the single highest-leverage question in the quiz. The numeric `min`/`max`
edges on `BUDGET_BANDS` are unchanged and stay exact and non-overlapping, so the assignment math is
untouched and only the display copy moved. The two now disagree by one dollar at each seam, which
means a reader stating exactly $6,500 sees that figure named in two bands. Deliberate: at the
boundary the two bands admit result sets that differ by one range and the reader is better placed
than we are to pick. Consequence for push two: `check_budget_labels` must assert each label's upper
figure against the NEXT band's `min`, not against its own `max`, or the rounding reads as an error.

A finding that corrects item ONE below: the results-prose `budgetLabels` set was NOT approximate.
It is the midpoint bands, derived correctly, rounded at the seams. It was right and it was the
copy nobody rendered. The quiz array was the wrong one.

**Reconciliation checked while fixing.** All ninety-nine rows of the `CITIES` array in
`index.html` were compared to v17 on both `budgetRange` and `monthlyEst`. Zero mismatches. The
labels were the only thing wrong; no data repair rode along.

**CLOSED, August 8 2026, push two of two: `check_budget_labels` shipped with its harness.**
The P0 is now fully closed: the labels were fixed in push one and are guarded from push two.

The check makes five assertions, all FAIL rather than warn: BUDGET_BANDS exists and parses;
exactly five bands, numbered one to five in order, with five distinct labels; the numeric edges
ascend, do not overlap and leave no gap, with the top band open-ended; each label's upper figure
names the NEXT band's floor rather than its own max, which is what makes the deliberate rounding
seam legal while a genuinely wrong figure still fails; and the boundaries still sit where the
database puts them, recomputed at run time from Monthly Est rather than hardcoded. It also refuses
a second copy of the band set under any name, and refuses a renderBudget() that no longer reads
the constant. Missing BUDGET_BANDS entirely is a loud failure, never a quiet pass.

`tools/test_budget_labels.py` plants eleven defects and requires the gate to catch each one,
including the original defect reproduced exactly.

**Two findings worth keeping.**

ONE. The harness caught a hole in the check on its first run, before either shipped. The
"renderBudget still reads the constant" assertion was matching the constant's name inside a
COMMENT, so gutting the code beneath it still passed. A check written specifically to close a
silent-pass hole shipped with a smaller silent-pass hole inside it, and only the planted-error
harness found it. This is the strongest evidence yet for the no-check-without-a-harness rule:
the rule is not about catching careless checks, it is that a check cannot test itself.

TWO. The database assertion encodes a POLICY, not just a threshold, and does so deliberately. The
bands derive from the MIDPOINT of each range's Monthly Est span. The low-end derivation originally
specified in this fix spec is planted in the harness as a defect and must be rejected, because the
candidate filter already grants one range of stretch and low-end labels would stack a second on
top. If that decision is ever reversed, the gate fails until someone changes the check on purpose.
A reversal cannot happen by quietly editing five strings.

**Growth-versus-debt split resumes.** The suspension is lifted. Next build: Fayetteville AR is
shipped, so Saratoga Springs NY, then the fayetteville-vs-bentonville comparison.

**CLOSED, August 8 2026: `scoring_rubric_v3_2` converted to markdown and committed.** Now
`docs/SCORING-RUBRIC.md` at v3.3. Budget ranges reconciled to the shipped `BUDGET_BANDS`, which
closes item four of the P0 fix spec. The `.docx` in project knowledge is superseded and should be
DELETED, not kept: leaving it is the two-copies condition 4a exists to prevent, and it is the exact
shape that produced the St. Paul divergence.

FOUND WHILE CONVERTING, P1, OPS: **the rubric documented nine of the ten dimensions the site
scores.** v3.2 stated that D4 had been retired and carried no D4 section at all. D4 is live: it is
`D4 Resil.` in the database, scored one to nine on all ninety-nine cities, it appears in the
`DIMENSIONS` array in `index.html` as "Climate Resilience & Insurance" where the reader can set it
as a priority, and it takes a full priority weight in the match calculation like every other
dimension. The retirement was real but applied to the OLD D4, a daily-cost sub-score folded into
D2; the slot was later reused for resilience and the rubric never caught up. Section restored in
v3.3. This is the same defect class as the budget labels: a governing document describing a surface
nobody re-opened after the code moved underneath it.

FOUND WHILE CONVERTING, P2, OPS: **D4 is the only dimension with no published band anchors.** There
is no table saying what separates a seven from a five. Ninety-nine scores exist with individual
rationales in `D4-resilience-scores-all-100.md`, but a new city cannot be scored against a written
standard, and two people scoring the same city would not reliably agree. Write the anchors FROM the
existing ninety-nine rationales rather than inventing them, then add them to the D4 section.

FOUND WHILE CONVERTING, P2, OPS: **the budget alignment bonus table in the rubric does not describe
the implementation.** The rubric gives a symmetric table keyed on absolute difference (0 = +6,
1 = +4, 2 = +2). `index.html` implements an ASYMMETRIC bonus that rewards being under budget and
penalises being over: one under scores five, one over scores two. The implementation is what
readers get. Decide which is correct and make the other match; flagged inline in the rubric so
neither is assumed authoritative meanwhile.

FOUND WHILE CONVERTING, P3, OPS: **dimension names differ between the rubric and the quiz.** D6 is
"Walkability" in the rubric and "Walkability & Transit" in `DIMENSIONS`; D8 is "Active Wellness" and
"Sports & Fitness". Cosmetic, but it means a search for either name finds only half the surfaces.

FOUND WHILE CONVERTING, P3, OPS: **the eight-city retiree-target-neighborhood list in the rubric is
not the same list as the Neighborhood Reality Check roster** in `MEDIAN-HOME-METHODOLOGY.md`, and
neither document says how they relate. One is scoring methodology and one is an editorial callout;
they overlap without being identical. Relates to the open P3 on the NRC roster count. State the
relationship explicitly in both docs.

**Superseded item, retained for the record. P1: `scoring_rubric_v3_2` is not in the repo.**
Found while fixing. `docs/` holds no scoring rubric under any filename; the only copy is a `.docx`
in project knowledge. That is a section 4a breach of the same shape as the
`MEDIAN-HOME-AUDIT-REFERENCE` gap already recorded in `SITE-OPERATIONS-LOG` section 4: a governing
document living outside `docs/`, with no version history, in the one place 4a forbids. Its budget
ranges are also now wrong in a second way: they read Range one under $3,500 per month, which is an
empty set against a database whose cheapest city starts at $3,800, and they now disagree with the
shipped bands as well. Convert it to markdown, commit it to `docs/`, reconcile the ranges to the
five bands above, and delete the outside copy. Do not reconcile the `.docx` in place; that
perpetuates the breach.

**Original item, retained for the record. P0, LIVE, CONVERSION PATH: the quiz budget question
shows three identical options.**

`renderBudget()` in `index.html` (currently near line 6751) builds Step three of four from a
local `BUDGET_LABELS` array whose middle three entries are byte-identical:

```
Under $5,500 / month        -> range 1
$8,900-$11,000 / month      -> range 2
$8,900-$11,000 / month      -> range 3
$8,900-$11,000 / month      -> range 4
$9,000+ / month             -> range 5
```

A reader is asked the single highest-leverage question in the quiz and handed three buttons
they cannot tell apart. Each sets a different `quizState.budget`, and that value drives a hard
candidate filter (`budgetRange <= quizState.budget + 1`), the alignment bonus, and the
over-budget penalty. Three indistinguishable buttons therefore return three different result
sets. This is the primary conversion path and it has been wrong for an unknown length of time.

Three findings that go with it:

ONE. The correct band set already exists in the same file, about twenty lines below, as
`budgetLabels` in the results prose: `under $5,500`, `$5,500-6,499`, `$6,500-7,499`,
`$7,500-8,999`, `$9,000+`. Distinct, ascending, non-overlapping. So the quiz array was never
filled past its first and last slots, and the paste source was one `$8,900-$11,000` line.

TWO. `BUDGET_OPTIONS`, near line 6352, is dead code carrying the same defect plus a stray
`Range 5:` prefix on all five labels. It is referenced nowhere. DELETE it rather than fixing
it, or someone repairs it later and it still does nothing.

THREE. Neither label set is derived from the database. Read off `CityDatabase_Jul_27_v17`,
the real low-end bands are: Range one $3,800 to $4,900, Range two $5,000 to $5,800, Range
three $5,900 to $6,600, Range four $6,900 to $8,000, Range five $8,900 and up. The results
prose set is directionally right and internally consistent; it is still approximate.

**Fix spec, one BATCH:**

1. Derive one label set from the DB low-end bands: `under $5,000`, `$5,000-5,899`,
   `$5,900-6,899`, `$6,900-8,899`, `$8,900+`.
2. Write it ONCE as a module-level constant and reference it from both `renderBudget()` and
   the results prose. Two surfaces holding two copies is what produced this; a fix that leaves
   two copies has fixed nothing.
3. Delete `BUDGET_OPTIONS` entirely.
4. Reconcile `scoring_rubric_v3_2` to the same bands. Its current text puts Range one at under
   $3,500/mo, which is an empty set: no city in the database is under $3,800.
5. New validator check `check_budget_labels`, with a planted-error harness before it ships,
   per the no-silent-no-op rule. It must assert, and FAIL rather than warn, that: the label set
   is exactly five entries; all five strings are distinct; the bands ascend and do not overlap;
   the thresholds match the DB `Budget Range` low-end bands; and exactly one label array exists
   in `index.html`. Zero matches must be a failure, not a pass.

**Why this was graded P2 first, recorded so the mistake is not repeated.** It was boarded as
documentation drift between the rubric and the DB field, which is real and is item four above.
The rubric was read; the rendered quiz was not. A doc-versus-data disagreement and a live
broken control surface look identical from the spreadsheet, and only one of them costs
conversions. The lesson generalises past this item: when a doc and the data disagree about a
field, check what the USER sees that field through before grading the severity.

**Priority consequence:** this outranks everything currently on the board, including the Wave
one and Wave two profile queue. New profiles feed a quiz whose budget filter is not doing what
the reader asked for, so profile volume is currently being poured into a broken funnel. The
growth-versus-debt split is suspended until this ships.

**Before that:** August 7, 2026, Fayetteville AR profile shipped
(BUILD; 50 profiles live, 22 comparison pages live. First build with no pillar: nothing in the
row reaches nine, so the hero and opening paragraph lead the four-way cluster at eight
(affordability, healthcare, outdoor, community) rather than picking a favourite. Recorded as a
SKILL GAP: `retiremehere-city-profile` tunes for MULTI-PILLAR at nine-plus and a MULTI-STRENGTH
advisory that assumes a standout exists, and has no case for a flat cluster. Budget card on
`best-places-to-retire-on-a-budget` promoted from coming-soon to live. Lists section ships with a
single card under `lists-grid`, matching the deployed Prescott pattern; Fayetteville is on no
other landing list.

FOUND WHILE BUILDING, P1, OPS: four instances of Lake Leatherwood in `index.html` Fayetteville
copy, one of them reading "Lake Leatherwood trails in city". Lake Leatherwood City Park is in
Eureka Springs, about forty-five minutes northeast. Fixed in this ship (pros, D6, D7, D8). The
class of defect is a regional asset absorbed into a city's own copy; the same shape is worth a
sweep across every profile that borrows from a nearby town.

FOUND WHILE BUILDING, P1, OPS: `index.html` Fayetteville D5 read "Arkansas income tax 4.4% flat".
Wrong twice: the rate is graduated, not flat, and 4.4% was the 2025 figure. The 2026 top rate is
3.9%. Fixed. Tax scoreNotes across all profiles carry a year-stamped figure and nothing in the
toolchain ages them; worth a dated sweep.

~~FOUND WHILE BUILDING, P2, OPS: the DB `Budget Range` field has drifted from the v3.2 rubric
definition.~~ **RAISED TO P0 and superseded, August 7 2026, second push.** The grade was wrong.
This is not doc drift; the same disagreement is live in the quiz budget question as three
identical options on the conversion path. Full item and fix spec at the head of this board.
The doc-reconciliation half survives as item four of that spec.

FOUND WHILE BUILDING, P3, OPS: the live NRC roster greps to thirteen cities. The board and
`PROFILE-FORMATTING` history both record ten. The live enumeration is authoritative; the prose
that says ten should be struck.)

**Before that:** August 7, 2026, comparison cross-link rule retired and board hygiene
boarded (OPS; 49 profiles live, 22 comparison pages live, no site change.
`COMPARISON-PAGE-STANDARD-v2` item 6 required every new comparison page to link to ALL other live
pages and to update all of them on every ship. It had already expired on its own terms: its
sunset clause was "until the hub page exists", the hub exists, lists every matchup and is linked
from all 22 pages. It had also never been followed. Measured across all 22: 1 to 4 outbound links
per page, none ever at 21. Replaced with the curated 2-to-4 pattern already in practice, with the
retired text kept inline so it is not reinvented. Three items boarded below, one of them a
priority RAISE on an item that was already open and that I nearly double-boarded by not grepping
this board first.)

**Before that:** August 6, 2026 (second push), `burlington-vs-portland-me` shipped
(COMPARE; 49 profiles live, 22 comparison pages live. The pairing splits two marks each,
which is the honest result rather than a convenient one. Three judgment calls, all noted in
the ops log entry: the two headline cost rows ship UNMARKED because they point in opposite
directions and the monthly ranges overlap almost entirely, so a mark on either would assert
a cost verdict the property-tax row contradicts on the same page; the climate figure rows
ship unmarked for the same reason in reverse, since every winter figure favours Portland and
marking all three would read as a sweep on gaps of four degrees and eight inches; and the
page stays off the Climate Warm W scores entirely, because W has Portland at two against
Burlington's three while Portland is warmer, drier of snow and sunnier on the figures printed
in the same table.

FOUND WHILE BUILDING, P1, OPS: `check_comparison_scores` and `check_comparison_cost_rows`
resolve a page's cities by lowercasing the DB city name, so `portland-me` does not resolve
to the Portland row and BOTH checks skip this entire page at their `if not a or not b:
continue` guard, including the Burlington cells beside it. That is the silent-no-op shape
this validator exists to refuse: neither check reports anything, and both count as clean.
`check_comparison_checkmarks` is unaffected because it reads only the table.
Every figure on the page was verified against the database by hand instead.)

**Before that:** August 6, 2026, Burlington VT shipped as profile 49 (BUILD; 49 profiles
live. First Wave 1 city of the growth cycle. Emphasis brief ran MULTI-STRENGTH, not MULTI-PILLAR:
one pillar at D7 Outdoor 9 with a cluster at D3 Health 8 and D10 Community 8, so the hero leads
with the outdoor pillar and the character section carries the cluster. Three judgment calls,
each noted in the ops log entry: no Neighborhood Reality Check, because the retiree-target towns
bracket the citywide figure rather than sitting above it; stat slot four went to healthcare over
arts on a tie at eight; and three Burlington figures in `index.html` were corrected against the
database on the way through, property tax at three surfaces and the D2 median at one. No landing
page needed touching: all seven Burlington cards were already live links, not coming-soon.
`check_figures` caught the property-tax fix mid-build: `pick-and-compare.html` keeps its own copy
of every highlight string, so a one-surface correction is a hard failure, correctly.)

**Before that:** August 3, 2026, `knoxville-vs-asheville` shipped and the three-week growth
cycle is finally on the board (COMPARE; 21 comparison pages live. The page ships WIRED: CTA blocks
on both profiles in the same commit, which is what `check_comparison_cta_reciprocity` now requires
and is the whole point of having built it yesterday. The cycle plan itself ran its entire first
week untracked because it was drafted in a chat and never boarded, which is the same failure that
lost the Wave 1 batch, so it is reconstructed in full below rather than summarised. Also corrected
on the way: the board's own live-profile count, and a hardcoded city count on the hub that
`check_hardcoded_counts` cannot see because its pattern needs the word "cities" to follow the
digits.)

**Before that:** August 3, 2026, THE ORPHANED COMPARISON PAGES ARE WIRED (BATCH; fifteen
missing CTA edges added across twelve profiles, closing the eight-page P1, and
`check_comparison_cta_reciprocity` shipped with an eight-assertion harness so the edge cannot
rot again. First ship of the three-week growth cycle: this is the 80% growth side, not debt,
because comparison pages carry the site's best engagement and 40% of them were unreachable
from the two pages whose readers want them.)

**Before that:** July 31, 2026, three prose-only conventions closed and gated (OPS;
23 hardcoded city counts across 11 files, a matchup count wrong by one on the hub, two
more D2 prose-score errors taking that run to eleven, and 23 stale data-vintage values;
`check_comparison_prose_scores` and `check_comparison_vintage` shipped,
`check_hardcoded_counts` rewritten after being blind three separate ways).

**Before that:** July 31, 2026, the COMPARISON COST-FIGURE REPAIR IS COMPLETE
(BATCH; Tier 2 batch B closed naples-vs-fort-myers, naples-vs-sarasota and
nashville-vs-memphis; COST_ROW_BASELINE emptied and the CTA cost-debt ratchet,
check and harness deleted; four more live D2 prose errors, a monthly gap that was
never right, and batch A's missed caption-vintage bump all corrected).

**Before that:** July 31, 2026, TIER 2 BATCH A of the comparison cost-figure repair shipped
(BATCH; sarasota-vs-tampa, knoxville-vs-nashville, knoxville-vs-chattanooga; 12 cells over 82 surfaces;
COST_ROW_BASELINE 24 to 12, CTA_COST_DEBT_BASELINE 7 to 5; two live D2 prose errors and four
dataset-scoped claims corrected on the way).

**Before that:** July 31, 2026, the CHECKMARK RULE settled at two points on dimension rows,
written into COMPARISON-PAGE-STANDARD-v2 and gated by `check_comparison_checkmarks` (BATCH; 22
marks off eight pages, one on, five captions and five sub-heads onto the current template, one
wrong prose score corrected on `santa-fe-vs-tucson`).

**Before that:** July 31, 2026, `bloomington-vs-lexington` rewritten and TIER 1 IS CLOSED (BATCH,
page 4 of 4. This is the one page where the gap NARROWS, $37,000 to $16,000, with the monthly
spread halving from $200 to $100, so the board was right that the "meaningfully cheaper" spine
could not stand. The real find is older than the rebase: the page counts the same money twice, in
tradeoff #2 and again in FAQ 3, presenting the monthly saving and the insurance saving as separate
advantages that add up to a lower all-in cost. BUDGET-METHODOLOGY.md section 4 puts homeowners
insurance INSIDE the monthly estimate, so Bloomington's $1,155 a year on insurance is already most
of the $1,200 a year its monthly figure shows. A thin margin was being presented as decisive.
Baseline 27 to 24 over six pages, CTA debt 9 to 7. Also: the checkmark rule is now MEASURED across
all twenty pages, and the Madison edit from earlier today went the wrong way. See the P1.)

**Before that:** July 31, 2026, `madison-vs-ann-arbor` rewritten (BATCH, Tier 1 page 3 of 4. The
gap widens $76,000 to $106,000 and Ann Arbor crosses into budget tier 3 while Madison stays at 2,
which kills two of the five items on tradeoff #2's list of what the cities SHARE, plus the same
claim in FAQ 2 in visible copy and in schema. Direction does not invert here, Madison was and stays
the cheaper city, so the spine held and four sentences went. The find worth keeping is a checkmark
defect that predates the rebase: this page declares "checkmarks mark the stronger city in each row"
twice, with no two-point threshold, and then leaves D2 unmarked at Madison 6 against Ann Arbor 5.
Marked now, along with the monthly row and the tier row that stopped being a tie. Baseline 32 to 27
over seven pages, CTA debt 11 to 9.)

**Before that:** July 31, 2026, `san-antonio-vs-fort-worth` rewritten (BATCH, Tier 1 page 2 of 4.
The board sized this one as "gap +145% AND San Antonio drops tier 2 to 1". Both true, and both
undersold it: the SIGN INVERTS. The page had San Antonio $20,000 more expensive than Fort Worth;
under v17 it is $49,000 cheaper and a full budget tier lower. Every sentence ordering the two on
price was backwards rather than stale. A second live error came out of the same read and has
nothing to do with cost rows: FAQ 1 claimed five exact dimension ties including budget, while the
page's own D2 row twelve lines above says 8 against 7. Four tie, and San Antonio wins budget. The
neighborhood-band argument survived untouched, every figure in it re-checked against both
profiles, so the page's CONCLUSION stands and only its premise was wrong. Baseline 35 to 32 over
eight pages.)

**Before that:** July 30, 2026, `st-louis-vs-kansas-city` rewritten (BATCH, step 3 of 3 and the
first Tier 1 page. The page was built on the two cities costing the same. Under v17 they do not:
the citywide gap is $65,000 where the page asserted $15,000, and the monthly estimates are $500
apart where it said $200. Tradeoff #2 was HEADLINED on "structurally identical", so the swap was
never available. The neighborhood argument survived and got sharper: St. Louis' retiree
neighborhoods run $420K to $575K against a $192,000 citywide figure, two to three times the
median, so the citywide gap favors St. Louis and the neighborhood FLOORS do not. Baseline 39 to
35 over nine pages. CTA debt unchanged at 11, because no profile links to this page, which is
itself the orphaned-comparison-page P1.)

**Before that:** July 30, 2026, Tier 3 of the comparison cost-figure repair shipped (BATCH, step
2 of 3. Eight pages, 30 quarantined table mismatches to zero, both ratchets lowered in the same
commit: COST_ROW_BASELINE 69 to 39 across ten remaining pages, CTA_COST_DEBT_BASELINE 21 to 11.
The finding is the SIZE. The board called Tier 3 mechanical at 30 figures, meaning the 30 table
cells the check counts; the actual edit was 184, because every table figure has three to fourteen
copies of itself in prose, in the FAQ, in the FAQPage schema and in the `og:description` meta, and
NONE of those copies is read by anything. `fort-collins-vs-boulder` alone carries the same gap
figure fourteen times. The check counts what it can see, and what it can see was 16% of the
defect. Three edits were not mechanical at all and are written up in the closed entry.)

**Before that:** July 30, 2026, the CTA cost-debt gate shipped (OPS, step 1 of 3 in the cost-row
repair. Two open items pull against each other: the orphaned-CTA P1 wants CTA blocks added to
roughly eleven profiles, and the cost-row P0 has 69 stale figures quarantined across eighteen
comparison pages. Wiring the first while the second is open sends readers into money the validator
already knows is wrong, and NEITHER item's check can see it happening, because one reads the
comparison page and the other reads nothing on the profile at all. The new check counts the EDGES
between them, 21 today, and ratchets both ways like the baseline it rides on. Nothing was found
wrong: this is a gate on a repair in flight, not a fix.)

**Before that:** July 30, 2026, comparison cost-row coverage shipped (OPS. The gate could not
see Typical home value, Estimated retiree budget or Budget tier on any of the 20 comparison pages,
and 18 of them had drifted, 69 figures. Not one D1-D10 score was wrong anywhere, which is the
finding: the rows under a check held, the rows beside them did not. Also fixed dimension-label
matching, which had silently skipped D4, D8 and D10 on every page since the check shipped. The 69
are quarantined in a two-way ratchet and repaired in tiers, see the P0. Note this lands on top of
the same-day lists-heading batch from a parallel session; that batch boarded a
`check_lists_heading_count`, which is the same defect class as this one, a page asserting something
about itself that nothing reads.)

**Before that:** July 30, 2026, lists-section heading counts corrected on six profiles and the
dead Memphis comparison CTA wired to its live page (BATCH. Both defects are the same shape: a page
asserting something about itself that nothing in the toolchain reads. The heading spells a card
count in words; the CTA said "Coming soon" about a page that has been live for weeks and was
edited earlier the same day. `st-louis` is the CANONICAL, which is how the heading defect reached
five other profiles. The wider finding is boarded: 8 of 20 live comparison pages have no CTA link
from either of the two city profiles they compare.)

**Before that:** July 30, 2026, summer-comfort values corrected, Memphis 8 to 4 and
St. Petersburg 7 to 4, and the last two comparison pages relabelled (BATCH. Both checkmarks came
off without being moved, because the gaps were never real. The finding worth keeping:
`Climate Hot Sum` is an ORPHAN COLUMN. The matching engine never reads it, the rubric documents a
weight the code does not implement, and both city profiles had been quietly contradicting it for
months. No quiz result was ever affected. An earlier read of this session claimed otherwise, from
the rubric doc rather than the code.)

**Before that:** July 30, 2026, summer-polarity label cleared on 6 of 8 pages (BATCH. The two
held back are the story: `nashville-vs-memphis` and `tampa-vs-st-petersburg` sit on DB
`Climate Hot Sum` values that contradict every other climate column for the same city, and that
column carries 0.35 weight in the Mild Year-Round match score, so it is a QUIZ defect, not a
display one. Both escalated to P1 pending a scoring decision. Also closed the Jul 30 ranking-CTA
sweep, 15 files, which had shipped with no board entry.)

**Before that:** July 30, 2026, st-augustine vs pensacola dead tier gap closed (BATCH. Both
cities are Range 2 under v17, so the page's organising claim of a tier gap was false on five
surfaces including the headline of tradeoff #1, which was rewritten rather than patched. Twenty
stale v16 figures swapped. A duplicate `Budget dimension score` row in the Cost & money block was
reading 5/10 against a correct 6/10 in the D-score rows on the same page, and is deleted: it is
the unchecked copy of a checked number. Boarded P2 summer-row polarity taken in the same pass, plus two items
that should never have been boarded separately: FAQ 4's "#4 spot on our Top Cities for Healthcare
list", which describes a ranking that does not exist, and a second dead tier gap on
`cities/pensacola/profile.html`. Two new items boarded, both about checks that cannot see the
surface they should be reading. Gate clean at 0/0.)

**Before that:** July 29, 2026, D2 band-mover review closed, no change (BATCH, board only. The
last open piece of the ZHVI rebase, step 5. Charlottesville, Ann Arbor and Columbus all crossed a
D2 median-home band when the figures were rebased. Reviewed against rubric step 4, cross-check
against similar cities rather than the band table, since the rubric states D2 is affordability
RELATIVE TO THE DATABASE AVERAGE. Every city in the DB between $495,000 and $571,000 scores D2 5
or 6 without exception, so Charlottesville at 6 sits with St. George at $521K and Ann Arbor at 5
sits with Pinehurst at $542K. No scores changed. The review's real output is a documentation
defect, now logged as divergence (7) on the Rubric v3.3 item: the rubric publishes $525-$750K as a
3-4 band and the database has never once scored that range below 5, which will mis-score the next
city anyone adds from the rubric alone.)

**Then:** July 29, 2026, stat-card labels unhidden site-wide (BATCH. Every profile was
rendering its stats bar with the label row invisible, so readers saw `9/10` with nothing saying
what was scored. Not a Bozeman bug and not new: it is in the St. Louis canonical, so all 48
profiles inherited it. The stats bar's negative top margin was written to pull the card up over
the HERO; the sticky section-nav was later inserted between them, so the pull-up lands on the nav
instead, and the nav wins on z-index 50 against 3. The hidden band is exactly the label row at
both widths, which is why the 2x2 mobile grid shows row 2's labels and not row 1's. Pull-up
reduced below the top padding at both widths, 8px clearance, 96 edits across 48 files. Found by
reading a live page, not by any check.)

**Earlier:** July 29, 2026, Portland ME shipped as profile 48 (BUILD. Built from the live
St. Louis canonical against CityDatabase_Jul_27_v17. Emphasis brief: three pillars, D3 Health 9,
D6 Walk 9 and D10 Community 9, so the MULTI-PILLAR rule applies and all three land in the hero
tagline and the opening character paragraph rather than one leading. Support at D1 Airport 8 and
D7 Outdoor 7. Hard-flagged D9 Safety 4 and D5 Tax 4 both sit in the No-if column, property crime
first: CrimeGrade has Portland at the 28th percentile OVERALL on a property crime rate about 40%
above national, while violent crime sits BELOW national at the 84th percentile, and writing only
the first half would have been the dishonest version of a 4. No NRC callout and no `.reality-check`
markup: under MEDIAN-HOME-METHODOLOGY.md v1.2 section 4 a note is warranted where retiree-target
neighborhoods run materially ABOVE the citywide figure, and Portland is the opposite case, with the
West End at roughly $554K against a citywide $571,000. The method-callout carries that point
instead and opens on the DB figure. Stat slots 3 and 4 use concrete proof, `Level I` and a Walk
Score band, not a bare N/10; the abbreviated monthly was derived through `monthly_abbrev` rather
than typed. Zero landing-page edits needed: all six Portland cards were already live `city-card`
links, none coming-soon, none carrying a money figure. Two items boarded. Gate clean at 48
profiles.)

**Previously:** July 29, 2026, `bozeman` 2015 anchor sourced and closed (BATCH. The last open
P0 from the rebase. The prose read "The Bozeman of 2015 had typical home values near $734,000.
Today it's near $740,000", which put the v17 figure in the 2015 clause and the superseded v16
figure in today's. No 2015 value had ever been in the file to restore, so it was sourced from the
Zillow ZHVI city series rather than guessed: RegionID 44281, 2015-06-30 = $327,317 against
2026-06-30 = $733,959, which matches DB Median Home to the thousand and confirms the DB's ZHVI
vintage is June 2026. Same series, same month, eleven years apart, so the comparison is
methodology-clean. It also shows "doubled" UNDERSTATES at x2.24, so the three surfaces carrying
that claim now read "more than doubled". Three further stale items on the same page, none boarded:
a `$740K` in the JSON-LD presented as current, a `$734,000with` run-together, and a Budget score of
3 where v17 says 4. The fix then FAILED the gate, which is the more useful half of this
entry: `check_statcard_faq` had no concept of a figure attributed to a past year, so a correct
2015 value under a home-value noun read as a claim about today. Shipped with an OTHER-TIME guard
alongside the existing other-place guard, same window, same backward-only bound, current year
excluded so the "As of 2026," opener stays read. Four new assertions, harness now 21. Gate clean
at 47 profiles.)

**Previously:** July 29, 2026, the v17 argument rewrites shipped (BATCH, editorial. The two
P0 items the July 27 rebase left behind, both the same cause: v17 collapsed a price ordering that
two pages argued from, so both wanted an ARGUMENT rewrite rather than a figure swap.
`best-places-to-retire-in-florida.html` lost its budget ladder entirely, since Pensacola, Fort
Myers and Delray Beach are now all D2=7 and all Range 2; the cheapest-FAQ is rebuilt on what the
$73,000 of spread buys, and the banned "Of the Florida cities scored on RetireMeHere" opener is
re-anchored to named cities and figures. `st-augustine` lost its price bracket, since v17 puts it
above both Sarasota and Tampa; rebuilt on the scale mismatch, a town of 15,000 pricing above two
Gulf Coast metros. The same page's eight-row comparison table was folded in by decision rather
than left to contradict the rewritten FAQ three screens up: six stale home figures and five stale
Budget/D2 scores, none of which any check reads. 18 edits, two files. Two items boarded, both
comparison pages with the same cause. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, `check_statcard_faq` shipped with the 36 figures it reports (OPS.
The profile stat-card, score-slot and prose/FAQ surfaces are now gated. New harness
`tools/test_statcard_faq.py`, 16 assertions, five harnesses in the list. Every figure the check
reports is fixed in the same commit, plus eight cross-city figures it deliberately excuses and three
unanchored ones it cannot see. Four items boarded, two of them P0 editorial. Gate clean at 47
profiles.)

**Previously:** July 28, 2026, P0 figure batch and board triage scale (BATCH + OPS. Thirteen
reader-visible figures corrected across ten profiles, ten abbreviated monthly stat cards off by
$300 to $600 and three home figures each contradicted by their own page. Every open item on this
board now carries a P0-P4 rank; the scale and the two rules that make it hold are the first
section below. The stat-card + FAQ validator check that found all of this did NOT ship: it is
P2, its findings are recorded on its own board item, and the 26 P1 figures it also found are
deliberately still in place as its regression corpus. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, Casper WY profile shipped as profile 47 (BUILD. Built from the
live St. Louis canonical against CityDatabase_Jul_27_v17. Emphasis brief: one pillar, D5 Tax 10,
with a cluster of three 8s (D2 Budget, D7 Outdoor, D9 Safety), so the MULTI-STRENGTH pattern
applies: tax leads, cluster carries the character section. Hard-flagged weaknesses D1 Airport 4
and D6 Walk 3 both sit in the No-if column, airport first. No NRC callout: Paradise Valley
prices within a few thousand dollars of the $314K citywide figure, so a callout would add noise
under MEDIAN-HOME-METHODOLOGY.md v1.2 section 4. Casper card on
best-places-to-retire-on-a-budget.html promoted from coming-soon to a live link; the Value
Navigator, Active Frontier and natural-disasters cards were already live. Two items boarded,
see below. Gate clean at 47 profiles.)

**Previously:** July 28, 2026, validator `layout` group shipped (OPS. New check
`check_stray_artifacts` plus `tools/test_stray_artifacts.py`, 7 planted-error assertions.
It fails on a `<city>-profile.html` or `<city>-hero.jpg` at the repo root, any zip at the
root, rename debris or a missing photo inside `cities/<slug>/`, and a `cities/` directory
that yields nothing. Run it with `--only layout`. Local mode only: it asks what is on disk,
and a bare run cannot list a directory over HTTP, so it is skipped rather than faked in the
post-deploy run. Cause it addresses: every other check reads the CONTENT of a file whose
path it already knows, which left a file with the wrong NAME in the wrong PLACE unwatched.
A build chat delivered the pre-July-14 hand-off shape three times between Jul 25 and Jul 28,
loose `casper-profile.html` and `casper-hero.jpg` to rename by hand, and the gate read 0/0
each time. The skill file was the leak: it lives outside the repo, so section 4a and the
enumeration rule cannot keep it current, and it still specified a shape DEPLOY-CHEATSHEET.md
superseded on Jul 14. Skill rewritten to delegate rather than restate. One item boarded,
see below.)

**Previously:** July 27, 2026, cleanup batch (BATCH: nine stale `Median Home` instances across
five profiles, the tail of the ZHVI rebase, plus board corrections. Salt Lake City `$525,000` and
`$525K` -> `$580K`, Columbus `$235,000` and the visible By the Numbers stat -> `$251K`, Nashville
`$460,000` -> `$437,000`, Kansas City `$250K` -> `$257K` in THREE places (prose, By the Numbers and
the NRC callout), Lexington `$333K` -> `$337K`. Kansas City and Lexington were not in the original
scope: they were surfaced by the post-edit verification scan rather than by hunting, and were folded
in because they are the same stat on the same surface, not a new line of inquiry. Verified before
editing: the monthly figures in the same sentences are all correct against v17, so this was home
value only with no cascade. Post-batch scan across all 46 profiles: zero home-figure disagreements
with v17 on either the JSON-LD or By the Numbers surfaces, and every JSON-LD blob parses.
Also corrected validate.py's usage text, which advertised `no PASS lines` when no check has ever
printed one, boarded since Jul 27 as "fix on the next validator touch" and missed by the last two
validator touches. Board corrections, which were the larger problem: the rebase item still read
NEXT JOB and still blocked Casper, when steps 1-3 had already shipped in v17; the Scottsdale item
still read as open after shipping this morning. Both closed. Nothing else touched, nothing new
investigated. Standing decision as of this session: findings get boarded, not fixed, and the board
is reviewed monthly rather than chased. The site's actual accuracy state after this batch is zero
known reader-visible wrong figures on any profile.)

**Previously:** July 27, 2026, nav batch (BATCH: the budget pillar is now in the site
menu. Added as "Budget-Conscious Retirees" (desktop `index.html`) and "For Budget-Conscious
Retirees" (everywhere else), sorted between Arts Lovers and Foodies, which is the order the
dropdown already followed once you ignore the leading "For". 40 files, 80 rows, 2 per file for
desktop and mobile. Option A of three considered: the item was RENAMED into the "Top Cities
For..." pattern rather than kept as "On a Budget", because every other item completes that
heading and "On a Budget" does not. Decided at the same time NOT to add the other three pillars,
Florida, Midwest and Avoid Natural Disasters: the location lists are thin against a 99-city
database and do not warrant menu placement yet. Also fixed rather than propagated: the budget
page already carried "On a Budget" in its own dropdown, alone among 87 files, sitting between
LGBTQ+ Retirees and Sports Fans, which is alphabetical under no reading. Those 2 rows were
removed and re-inserted correctly, which is the only deletion in the diff. Nothing hardcodes
markup: each file's own Arts Lovers row is cloned and its href and label swapped, so absolute
paths stay absolute on index.html and relative stay relative elsewhere, across all seven nav
variants. Verified: 40 files at exactly 2 rows each, every href resolves from its own directory,
every dropdown still alphabetical, diff is 80 insertions and 2 deletions and nothing else.
Gate 0/0, three harnesses. NOT touched, and this is the real finding: the nav is copy-pasted
into 87 files in SEVEN variants, and the 46 city profiles carry a stripped 3-link nav with no
dropdown at all, so they cannot receive menu items without a nav rework. Boarded below.)

**Previously:** July 27, 2026, budget-roster batch (BATCH: `best-places-to-retire-on-a-budget.html`
rebased on v17. Roster moved from a 31-card set to tier R1's 30. Four came off, Beaufort NC,
Pensacola FL, Rio Rancho NM and Sioux Falls SD, all now R2; three went on, Indianapolis IN and
Wilmington DE as coming-soon cards and San Antonio TX as a live card. Per the boarded Jul 27
decision the methodology prose moved in the SAME commit: the bar stopped describing the low end
of the published range, "starts under about $5,500", which admitted 47 cities and was the sentence
justifying all four departures, and now describes the CENTRAL estimate, "centers at $5,550 or below",
which is the basis the DB and quiz already use. R1 midpoints run $4,300 to $5,550 and R2 opens at
$5,600, so the band is cleanly separable and a reader can check the claim against the midpoints
printed on the cards. Verified before the edit: all 27 surviving cards already carried correct v17
monthly figures, so this was purely a roster and prose fault. Ranks renumbered 1-30, roster
alphabetical, 18 live and 12 coming-soon. Reciprocal link added: San Antonio's profile gained a
budget list card and moved from `lists-grid-four` to `lists-grid` per the 3-card convention.
Pensacola needed no reciprocal removal, its profile carries no list cards at all. Meta descriptions
corrected 31 -> 30, and "ranked by" changed to "measured by" in three places where it contradicted
the page's own "alphabetically, not ranked" one line below. Gate 0/0 on a fresh clone, both
harnesses ran. Shipped in the same commit, because it is the fix for the reason this rotted:
`check_roster` in validate.py, wired into the `cards` group, with `tools/test_roster.py` as its
planted-error test at 7 assertions. `check_cards` only ever asked per-card questions, so the page
could be wrong about WHICH cities belong while every card on it was individually correct, and the
gate confirmed that by passing the stale page at 0 failures. Run the new check against the PRE-batch
page and it reports 7 failures naming exactly the four extras and the three omissions. Also cleared
the boarded Scottsdale fossil: the `Mullett` entry and the `5+ teams` pill, both left over from the
Coyotes' 2024 move to Utah, corrected on the sports page and in the scoring doc to `4 teams`.
Four leagues still clears the Tier 1 bar of "4 or more", so placement did not move. Two new faults
found en route and boarded below, neither shipped: the Florida and Midwest pillars parse to ZERO
cards inside `check_cards`, and the Florida pillar carries a stale comparison passage on three
surfaces whose fix changes an argument rather than a figure.)

**Previously:** July 27, 2026, batch (BATCH: three stale prose home figures corrected
and two unscanned pages brought under the `emdash` check. Philadelphia `$234K` x2 ->
`$237K`, New Orleans `$246K` -> `$248K`, matching v17 and matching the correct figure each
file already carried elsewhere. `privacy.html` and `scouting-trip-workbook.html` added to
the `emdash` named target list and their one em dash each converted. The feared sprawl did
not happen: both pages held exactly one, and a raw scan finds nothing further in either
file, not even in `<style>` or comments. Gate 0/0 on a fresh clone, both harnesses ran.
Three planted-error tests confirm the two new targets are genuinely scanned rather than
silently clean, including the escaped `&mdash;` form. Note what this does NOT close: the
coverage gap that let the three figures live is still open, see the item below.)

**Previously:** July 27, 2026, latest (OPS: VALIDATOR HARNESS REPAIR SHIPPED, commit
`b13edf1`. `tools/test_highlight_homes.py` no longer hardcodes home figures; it reads them from
the DB at runtime through validate.py's own loader, so the next annual ZHVI refresh cannot break
it again. Both harnesses are now a `harness` check group and gate the deploy. Gate 0/0 on a fresh
clone; bare post-deploy run also 0/0 on live main. Two things the board did not have: the harness
hardcoded TEN figures, not nine - Wilmington NC sat at $418,000 against a v17 $423,000, which would
have failed test 3 silently once the crash cleared - and one of the 18 assertions was passing
vacuously, matching nothing at all. Both fixed.)

**Previously:** July 27, 2026, later (OPS: BUDGET-METHODOLOGY.md made independently
reproducible. Exact per-state COL and Medigap multipliers written into section 6 as tables,
recovered from BudgetAuditJun162026.xlsx; section 4 snapshot date corrected to 2026-06-30;
section 5 healthcare range corrected to $924-$1,096; section 9 tier counts corrected to
30/29/19/12/9 and the stale quiz-rollout paragraph replaced. Verified: the formula now
reproduces all 99 rows of v17 exactly, both the Monthly Est string and the Budget Range
integer. Gate 0/0. Board swept: three items below were already dead and one was mislabeled.)

**Previously:** July 27, 2026 (OPS: ZHVI REBASE SHIPPED. `Median Home` rebuilt for all 99 cities
from the 2026-06-30 Zillow column; Monthly Est, Budget Range and D2 recomputed; every derived surface
figure re-derived. Three further faults found and closed en route: Monthly Est did not equal
f(Median Home) for 31 cities, `pick-and-compare.html` disagreed with `index.html` on d2 for 72 cities
(the boarded item, now closed), and seven carve-out fossils still framed cities on the retired
retiree-target-neighborhood basis. Validator 0/0.)

**Previously:** July 26, 2026 (board-only: six-city vintage question RESOLVED against the DB;
`Median Home` found to be a 2020-2026 patchwork never rebased, full audit boarded below; two
TASKBOARD header nits fixed. No content surfaces touched, no scores changed.)

**Previously:** July 25, 2026 (BATCH: Gilcrease Museum corrected on the arts landing card and
in the arts scoring doc; NRC fixed list removed from PROFILE-FORMATTING.md and
MEDIAN-HOME-METHODOLOGY.md, live count is 17 not 10; Tulsa property tax 0.77% -> 0.79% in
index.html; Wilmington DE phantom NRC entry removed. Four items boarded, see below.)

**Previously:** July 24, 2026 (Tulsa, OK profile shipped, profile 46; Tulsa card on
best-places-to-retire-on-a-budget.html promoted from coming-soon to a live link; two Saint Francis
"largest hospital" claims retired to the ledger. Earlier the same day: Roanoke, VA shipped as profile
45, with four stale Roanoke index.html figures fixed en route: $280K->$251K, hospital 16->15, D1
routes refreshed, D7 "Range 2"->"Range 1"; Carvins Cove second-largest-municipal-park claim retired)

**Verified live at last update:** 48 profiles, 20 comparison pages, 5 guides, 11 category pages
(7 `top-cities-for-*` plus 4 `best-places-to-*` pillars; the old "7 landing pages" line counted
only the first set).
All 48 profiles carry a Visit block with per-city Expedia and Vrbo codes (Roanoke's are still
placeholders pending Creator Hub; Tulsa's, Casper's and Portland ME's are live).
Validator: **0 failures, 0 warnings** on `--local .`, confirmed on a fresh clone at commit
`b13edf1` (Jul 27 harness push). The bare (live GitHub) post-deploy run was also made at that
commit and also reads 0/0, so the outstanding bare run from the Jul 25 push is closed.
The validator now ALSO carries a pros/cons home-figure check (folded into the `figures` group).
As of Jul 18 it ships **FAIL**, not WARN: the Jul-15 34-figure reconciliation held, both `--local .`
and the live bare run read 0 pros/cons warnings, so drift now blocks the gate like every other
figures check. Planted-error tested (Knoxville `$327K` against DB `$368,000`: 1 failure, exit 1).
As of Jul 23 the `figures` group ALSO covers home figures in `highlight` PROSE, on both
`index.html` and `pick-and-compare.html`. Also **FAIL**. Planted-error tested by
`tools/test_highlight_homes.py` (now **18 assertions**, run it after any edit to the `HL_*` patterns).
Exact match, no tolerance band: a figure in thousands must equal `round(DB/1000)`.
As of Jul 23 the `figures` group ALSO carries `check_highlight_surfaces`, which fails when a city's
highlight differs between `index.html` and `pick-and-compare.html` byte for byte. Three of the 18
assertions cover it. And the `emdash` group counts every RENDERING of the character rather than one
spelling, with its own planted-error test, `tools/test_emdash_forms.py` (**10 assertions**).
As of Jul 27 BOTH test files run automatically as the `harness` check group, so the gate covers
them and you no longer have to remember. A gate run prints two extra lines:

    harness:  tools/test_highlight_homes.py 18/18 passed
    harness:  tools/test_emdash_forms.py 10/10 passed

If either line is absent from a gate run, the group did not execute; that is itself the failure.
Three ways the group fails, all planted-error tested: a failing assertion (named individually on
the gate, plus `17/18 passed`), a harness file that has been deleted, and a harness that exits 0
having run nothing.

---

## How to run chats

One job type per chat. Name chats so they are findable:

| Chat name pattern | For | Lifespan |
|---|---|---|
| `BUILD - <City>` | one city profile, end to end | dies when the city ships |
| `COMPARE - <A> vs <B>` | one comparison page | dies when it ships |
| `BATCH - <job>` | repo-wide scripted operations (retrofits, sweeps) | dies when the batch is pushed |
| `OPS - planning & tracking` | this board, decisions, methodology Qs, small one-off fixes | permanent home base |

Rules of thumb:
- A NEW city's Visit block + affiliate codes belong IN that city's `BUILD` chat.
- RETROFITTING existing profiles is a `BATCH` job, never woven into a single city build.
- If a chat shows a "conversation compacted" note, finish the current step, update this board, start fresh.

**Before every deploy:** `python3 tools/validate.py --local .`  <- THIS IS THE GATE
**After every deploy (optional receipt):** `python3 tools/validate.py`

These read different things. `--local .` reads your working checkout: the code you are about to push.
Bare reads live GitHub: the code already deployed. A bare run BEFORE a push grades the OLD site with
your NEW rules and reports failures you have already fixed. This misfired twice on July 14, 2026.

As of July 14 the validator PRINTS WHICH ONE IT IS DOING at the top of every run:

    mode:     PRE-DEPLOY GATE -- reading the files on this machine
    mode:     POST-DEPLOY CHECK -- reading the LIVE files from GitHub, not your working copy

If the header says POST-DEPLOY, the numbers describe the live site, not your work. Read the header
before you read the failure count.

Standard deploy block:

    git pull
    (drag zip into repo root)
    unzip -o <bundle>.zip
    rm <bundle>.zip
    python3 tools/validate.py --local .     # must read PRE-DEPLOY GATE and 0 failures
    git add -A                              # -A, not `git add .` -- catches docs/ and tools/
    git commit -m "..."
    git push

---

## HOW TO RANK ANYTHING ON THIS BOARD (adopted July 28, 2026)

Every open item below carries a rank. An item without one is not tracked, because a board on
which everything looks equally urgent gets read as a pile rather than a queue.

Rank on one question: who is harmed, and how fast.

| Rank | Test | What it means for the schedule |
|---|---|---|
| **P0** | A reader sees a wrong number that could change a decision, or a page is broken | Fix in the chat that finds it |
| **P1** | Wrong, but a reader cannot see it or would not act on it: machine-only surfaces, rounding, low-traffic pages, dated triggers not yet due | Batch. Monthly, or the next time you are in the file |
| **P2** | Nothing is wrong today; nothing prevents it going wrong tomorrow. Every validator check lives here | Its own scheduled OPS chat |
| **P3** | Structural debt. The nav in 87 files, the rubric living outside the repo | Only when it blocks something you actually want to do |
| **P4** | Cosmetic, wording, doc version numbers, enumeration accuracy | Only while already in the file. Never its own job |

Two rules make the scale hold:

1. **No board line without a rank.** A chat that cannot rank a finding does not board it.
2. **Only P0 may interrupt a city profile build.** With 52 cities left to score into profiles,
   builds are the default work and findings are the interruption, never the other way round.

Ranks are cheap to change and are a judgment, not a measurement. Move one the moment it reads
wrong; do not open a discussion about the scale to do it.

One exception, and only one: **queue entries carry no rank.** `Next in queue`, the comparison-page
queue and the per-city follow-up lists are the WORK, not findings about the work. Four such bullets
are unranked today and that is correct, not an oversight.

Why this exists, recorded so the reasoning does not have to be reconstructed: on July 28 an OPS
chat scoped to a single validator check turned up 44 wrong figures across 36 profiles. Ten moved
a headline monthly budget by $300 to $600. Twenty moved it by $100. Before today those two
classes read identically on this board, and the effect was that the $100 ones felt as blocking
as the $600 ones. Nothing was wrong with the finding. What was missing was the rank.

---

## SUPERSEDED IN PART, August 17 2026 - three-week growth cycle (boarded August 3, 2026)

> **READ THIS BEFORE ACTING ON ANYTHING BELOW.** The Wave 2 and Wave 3 profile
> lists in this section are SUSPENDED. They were called off in a chat on
> August 15 2026 and boarded on August 17 as a STRATEGY SUPERSESSION; search
> this board for "STRATEGY SUPERSESSION" for the full entry. Profiles are
> conversion inventory, not acquisition pages. Build a profile when demand
> names it, not on a schedule.
>
> What still stands from this section: the 80/20 growth-to-debt split, the
> one-debt-day-per-week hard cap, the reader-visible test for new validator
> checks, and grading on leading indicators. "Growth" in those rules now means
> comparison pages, tools and pins.
>
> This marker exists because the section below reads as current and sits above
> the decision that replaced it. As of August 18 2026 it had misled FOUR
> sessions into recommending profile builds that were already called off, the
> most recent being the session that shipped tampa-vs-naples. A superseded plan
> that is not marked superseded outranks the decision that superseded it, every
> time, because it is what a reader hits first.


Unranked. This is the work, not a finding about the work: same exception the build queue and the
comparison queue carry.

Drafted at the end of the CTA-reciprocity session and never committed, so it governed its entire
first week while being untracked. Reconstructed here from that session. This is the second time in
three weeks: the Wave 1 batch of Fayetteville AR, Saratoga Springs NY and La Crosse WI was carried
in a chat for the same reason. A plan that lives in a chat is a plan that dies with the chat.

**The split: 80% growth, 20% debt.** The binding constraint on this site is DEMAND, not
correctness. Internal quality work is invisible to a search engine. Profile volume and comparison
pages are the two levers that move impressions, so they take four days in five and the debt queue
takes one.

**Three rules, for the whole cycle:**

1. **One debt day per week, hard-capped.** Not "about a day". When the day ends, the remaining P1s
   and P2s roll to next week untouched. The cap exists because debt work is more legible than
   growth work and will eat the cycle if allowed to argue for itself.
2. **No new validator check unless the defect it catches is reader-visible.** Every check written
   in the last fortnight was justified and the queue is still growing faster than it drains. A
   machine-only surface is a P2 by this board's own scale and does not earn a check during a
   growth cycle.
3. **Graded on leading indicators, not clicks.** Pages indexed, impressions, average position.
   There is a six to twelve week lag between publishing and clicks, so grading this cycle on
   clicks grades week one's work against week minus six's traffic and concludes, wrongly, that the
   cycle failed.

**Week-1 indexing gate: PASSED.** Seventy-nine pages indexed, zero in discovered-not-indexed. The
gate existed so Wave 3 would not be built into a crawl problem. There is no crawl problem. Wave 3
proceeds.

**Build order:**
- **Wave 1 (in flight):** Fayetteville AR, Saratoga Springs NY, La Crosse WI.
  Burlington VT shipped August 6 as profile 49 and is closed below.
  Burlington ran AHEAD of Fayetteville. Fayetteville scores four points higher, 71 to 67, so this
  inverts score order on purpose: it is the order the builds are actually happening in, and the
  board records the real order, not the intended one. Portland ME was on the original wave list
  and is not on this one because it shipped July 29, ahead of the cycle.
- **Wave 2:** Raleigh NC, Boise ID, Colorado Springs CO, Sedona AZ, Flagstaff AZ.
- **Wave 3:** Park City UT, Jackson Hole WY and the rest. Unblocked by the gate above.

**Why Traverse City MI is not on any wave.** At 73 it is the highest-scoring unbuilt city, two
points clear of Fayetteville AR at 71, and it is still unscheduled because it has no live pairing
partner: it ships one profile and unlocks zero comparison pages, which is the wrong shape for a
cycle whose second lever is comparisons.

---

## BOARDED - opened August 6, 2026 (board hygiene + comparison standard)

**[P2] This board is 40% closed-work archive and should be split.** Measured August 7, 2026:
220,557 characters, 2,848 lines, of which 87,628 characters across 27 `## CLOSED` sections are
completed work. It grew by 6,340 characters in a single day. The board's own purpose statement is "what is in flight, what is next, and what
is parked", and none of those three describes a closed item. Move the `## CLOSED` sections to
`docs/TASKBOARD-ARCHIVE.md` and leave the live board holding only open work.

The reason this is safe: every shipped item is currently recorded THREE times. Once in the
Last-updated ladder at the top of this board, once in a full `## CLOSED` section further down,
and once in section 7 of `SITE-OPERATIONS-LOG.md`. The Burlington build wrote all three and the
CLOSED section and the ops-log entry were close to duplicates. The `## CLOSED` copy is the
redundant one and the largest; the ladder stays as the scannable recent history and the ops log
stays as the permanent narrative record. `check_docs` reads only `TASKBOARD.md`, so the archive
file is invisible to the gate and no validator change is needed.

What this does NOT fix: the count anchor above. Roughly a third of the 27 historical profile
counts sit in the front-matter ladder, above the first `## CLOSED` heading, which is exactly
where the current first match lives. Do not ship the split believing it closed the P2 above.

**[P4] One comparison page sits below the new link floor.** `COMPARISON-PAGE-STANDARD-v2` item 6
now sets two related matchups as the minimum. `bloomington-vs-lexington-retirement.html` carries
one. Fix while already in that file; do not make it a job. Nothing gates this, which is why it
needs writing down. Re-count by grepping before acting, never from this entry.

---

## OPEN P2 - Burlington snowfall figure, DB vs live copy (opened August 6, 2026)

`CityDatabase_Jul_27_v17.xlsx` gives Burlington `Ann Snow in` = 70. The `index.html` cons bullet
says approximately 80 inches, and NOAA's 1991-2020 normal for Burlington is about 81. One of the
two is wrong and the DB is the likelier candidate. Check the cell against the NOAA normal, correct
whichever is wrong, and sweep the profile and `index.html` together so the two surfaces agree.
Low priority: both figures land a reader in the same place, which is why it can wait, and also why
it would otherwise never get found.

---

## BOARDED - opened by the knoxville-vs-asheville build (Aug 3)

**[P4] Two climate-row conventions are live across the comparison pages.**
COMPARISON-PAGE-STANDARD-v2 describes Winters / Summer heat severity (10 = worst) / Summer humidity
(10 = worst), and explicitly rules out showing a "Mild year-round" style score row. At least
`knoxville-vs-chattanooga` and `knoxville-vs-nashville` still carry the older four-row form with
"Warm winters", "Summer comfort", "Humidity" and "Extreme heat exposure". Nothing reads climate
rows, so this is invisible to the gate and to readers who only see one page. Fix while already in
those files; do not make it a job. Count the real spread by grepping first, never from this entry.

**[P2, RAISED from P4 on August 7, 2026] `check_docs` reads a line-wrapped number as its
profile-count anchor.** Raised because the Burlington build had to work around it by hand:
the fix was to place "49 profiles" in the new head paragraph so it would shadow the July 29
sentence. That works, and it is a workaround that every future build must remember to repeat,
which is exactly the shape of thing that gets forgotten once. The real fix is an explicit
labelled field, `**Live profiles:** 49`, near the top of this board, with `check_docs` reading
that field rather than the first loose regex match anywhere in the file. Under the harness rule
that check change ships with a planted-error harness: one fixture where the field disagrees with
reality, one where the field is missing entirely, so the check cannot silently no-op. There are
currently 31 digit-formatted profile counts in this file, ranging from 4 to 49. The check is
reading the first of 27 landmines and passing by coincidence. Original entry follows.

The first
`(\d+)\s+profiles` match in this board is not the "Live profiles:" line. It is a wrapped `48` at
the end of a July 29 sentence about stat-card labels, where the digits and the word land on
different lines. It happens to be correct today. It will silently go stale, and the next session to
write a digit-formatted profile count anywhere above it will shadow it instead. Either give the
check an explicit anchor to read, or keep spelling profile counts out in words above that line.

---

## BOARDED - opened by the stat-card check (Jul 28)

- **[P1] `.site-header` and `.section-nav` are both pinned to `top: 0`.** Found July 29 alongside
  the stat-label fix, same block of CSS. The header carries `z-index: 100` and the nav `z-index:
  50`, so when the nav sticks it slides UNDER the header instead of stacking below it, and the
  chips are clipped along their top edge. Visible in the same screenshot that surfaced the label
  bug. Likely fix is `top: <site-header height>` on `.section-nav` plus a matching
  `scroll-padding-top`, which is currently `64px` and looks too small for the two bars stacked.
  Not touched, because unlike the label bug the arithmetic cannot be settled from the CSS alone:
  the header's height is padding plus content and wants measuring in a browser. All 48 profiles.

- **[P3] Nothing on the site reads rendered geometry.** The stat-label bug lived in the canonical
  template and shipped into 48 profiles, and no check could have caught it, because the markup was
  correct and the pixels were wrong. Open question rather than a task: a check asserting the
  stats-bar pull-up stays smaller than its top padding would have caught this exact bug and
  nothing else, which may not earn its keep. Worth deciding deliberately rather than by default.

- **[P2]** **43 run-together money figures across 40 of 48 profiles.** `$326,000with`,
  `$223,000though`, `$858,000with`. Found Jul 30 while fixing a single instance on
  `cities/pensacola/profile.html`, which turned out to be 1 of 44, not a typo. It is
  template-inherited: 17 sit in the identical stat-card FAQ sentence "As of 2026, the typical home
  value is around $X" and the rest in three close variants. Trailing words are `with` x28,
  `though` x6, `but` x2, `and` x2. The Pensacola one is fixed only because it shared a sentence
  with a false tier claim; the other 43 are untouched deliberately, since fixing 1 of 44 hides the
  pattern. `check_statcard_faq` passes 21/21 and cannot see any of them, which is the more
  interesting half: these are in FAQPage schema, so they are what gets quoted. Fix is one BATCH
  plus a check with a planted-error test.

- **[P0]** **24 stale cost figures left on 6 of 20 comparison pages. Was 69 on 18.**
  Audited Jul 30 across every DB-derived field. All 69 were in Typical home value, Estimated
  retiree budget or Budget tier; zero were in D1-D10. The ZHVI rebase never reached these pages.
  Held by `COST_ROW_BASELINE` in the validator, so the gate stays honest while they are repaired.
  **Tier 3 and Tier 1 are closed (Jul 30 and Jul 31). Everything remaining is Tier 2**, six pages
  at 4 mismatches each. Attack in three tiers, hardest first, lowering the baseline in each commit:
    - **Tier 1, argument rewrites, one page per pass.** ~~`st-louis-vs-kansas-city` (gap
      $15,000 -> $65,000, a 333% change, any "same price" framing is dead)~~ **CLOSED Jul 30**,
      eleven surfaces, not the one the headline suggested;
      ~~`san-antonio-vs-fort-worth` (gap +145% AND San Antonio drops tier 2 -> 1)~~
      **CLOSED Jul 31**, and the sizing missed that the price ordering INVERTS. Check the sign,
      not just the magnitude, on the two remaining Tier 1 pages;
      ~~`madison-vs-ann-arbor` (Ann Arbor rises tier 2 -> 3, gap +39%)~~ **CLOSED Jul 31**, and the
      sizing was accurate for once: direction holds, so only the shared-items list broke;
      ~~`bloomington-vs-lexington` (gap $37,000 -> $16,000, near noise on a $321,000 house, so
      the "meaningfully cheaper" spine of the page probably cannot stand)~~ **CLOSED Jul 31**, and
      the spine could not stand, for a bigger reason than the narrower gap: the page was adding
      the insurance saving to the monthly saving, and insurance is INSIDE the monthly estimate.
    - **TIER 1 IS COMPLETE.** 24 mismatches remain, all Tier 2, all six pages.
    - **Tier 2, figures plus prose reconciliation, 2-3 per batch.** `sarasota-vs-tampa`,
      `knoxville-vs-nashville`, `knoxville-vs-chattanooga` on gap movement of 30-50%; plus
      `naples-vs-fort-myers`, `naples-vs-sarasota`, `nashville-vs-memphis`, which move under 12%
      but cite the gap 8 to 14 times each, so volume puts them here.
    - **Tier 3, mechanical, one script. CLOSED Jul 30**, 8 pages, 184 edits, baseline 69 -> 39.
      Read the closed entry before sizing Tier 1 or Tier 2: the quarantine count is table rows
      only and undercounted the real surface by a factor of six, and the "under 6% gap movement"
      criterion was wrong on two of the eight. Size by grepping the page for the figure, and tier
      by whether the page ARGUES from it.
  ~~OPEN QUESTION before Tier 3: most monthly estimates are off by exactly $100, which smells like
  a `BUDGET-METHODOLOGY.md` recompute rather than drift.~~ **ANSWERED Jul 30, and the answer is
  no.** Across the eight Tier 3 pages the monthly deltas run 0, +$100, +$200 and -$100, in both
  directions, tracking each city's own median-home move. Ordinary rebase drift, not a recompute.
  GATED Jul 30 by `check_comparison_cta_cost_debt`, and the number has fallen with the repair:
  **7 profile CTA links now point into the 6 quarantined pages, down from 21 into 18.** It cannot
  rise while this P0 is open. Do the orphaned-CTA P1 after this one, or do it only on the pages
  that are no longer quarantined, which is now fourteen of twenty rather than two.
  SECOND, and now down to one city: Memphis $195,000 -> $147,000 is an NRC city and
  `nashville-vs-memphis` is still ahead in Tier 2. Check it uses the citywide-plus-callout
  convention before swapping, or a $147,000 figure ends up stranded beside prose about Germantown
  at $280K-$500K. The St. Louis half of this note is done: `st-louis-vs-kansas-city` shipped
  Jul 30 and the convention was already settled on that page.
  THIRD, added Jul 31 after all four Tier 1 pages: **size a page by grepping it, never by its
  baseline number.** The baseline counts three table rows. Tier 3 was 30 by that count and 184 in
  reality; `st-louis-vs-kansas-city` was 4 and eleven load-bearing surfaces. The same figures sit
  in prose, visible FAQ text, FAQPage schema, `og:description` and `twitter:description`, and no
  check reads any of those copies.


  Found Jul 30. Distinct from the D4/D10 item below, which is about the DIMS label prefix. This one
  is about coverage: the check reads `<td class="metric">D<n> ...` rows ONLY, so typical home value,
  estimated retiree budget and budget tier are unchecked on all 19 comparison pages. That is exactly
  how `st-augustine-vs-pensacola` held a `Budget dimension score` of 5/10 twelve lines above a
  `D2 Budget` of 6/10, in the same table, with the gate green. The July 13 D2 rebuild landed on the
  row the check reads and not the row it does not. Worth a hand-audit of the other 18 pages BEFORE
  writing the check, to size how much stale money is sitting in the blind spot. Ship with a
  planted-error test on a cost row, together with the D4/D10 fix below.

- **[P2]** **`check_comparison_scores` cannot see the D4 or D10 rows on any comparison page.**
  Found Jul 29 while rewriting the Pensacola pairing. The check matches
  `<td class="metric">{dim_label}` as a PREFIX, and `DIMS` carries the DB's column names:
  `D4 Resil.` and `D10 Comm.`, both with a trailing period. Comparison pages write the rows out
  in full as `D4 Climate resilience & insurance` and `D10 Community & culture`, neither of which
  starts with the DIMS label, so `re.search` returns None and the `if not m: continue` guard skips
  them silently. Eight dimensions are checked on every comparison page and two are not, and the
  gate reads 0/0 either way. Both rows happened to be correct on this page (2/1 and 7/7 against
  v17), so nothing shipped as a fix here. The same shape as the D2-column incident this check was
  written for: a check that cannot fail on a surface is indistinguishable from a check that passes.
  Fix is to match on the `D<n>` token rather than the DB column name, with a planted-error test on
  a D4 row before it ships.


- **[P2]** **Money with no anchor at all is still unreadable, and it is not hypothetical.** Three
  figures in this batch were found by hand and by hand only, because they sit under no home-value
  noun, in no structured region, and name no city: `st-augustine`'s "At $432,000 this is a pricey
  small town", the same page's "Price: at $432,000", and `carlsbad`'s "At $1,481,000, Carlsbad sits
  among the priciest coastal markets" against a `$1,388,000` DB figure and a `$1.39M` stat card two
  sentences earlier. All three are fixed here; the SHAPE is not closed. Reaching them means grading
  every dollar figure on the page against Median Home, which fires on monthly budgets, property-tax
  bills and neighborhood prices. The cheaper move is probably a PROFILE-FORMATTING rule that a
  citywide figure must carry its noun, enforced on new builds rather than retrofitted.

- **[P4]** **`prescott` was the only profile writing money as "585,000 dollars".** Three occurrences,
  all in the JSON-LD, all invisible to every money pattern on the site, and all three were stale: the
  home figure twice and the monthly top end once (`7,400` against a DB `$7,500`). Normalised to the
  `$` form the other 46 profiles use, which brings them under `RANGE_RE` and the new check rather than
  adding a spelled-out variant to the token. Worth a glance on the next build that a profile has not
  invented a third money style.

---

## ACTIVE - batch / site-wide operations

- **GAP CLOSED Jul 28, 2026.** `check_statcard_faq` now reads profile prose, the JSON-LD FAQ, the
  method-callout and the NRC. The fourth figure this item predicted turned out to be ten. Original
  text below.
  **[P2]** **Three stale home figures in profile PROSE: FIXED Jul 27. The GAP THAT ALLOWED THEM IS STILL
  OPEN.** Philadelphia `$234K` x2 -> `$237K` and New Orleans `$246K` -> `$248K`, both now equal to
  v17 and to the correct figure each file already carried elsewhere. Read the fix narrowly: three
  characters of drift were corrected by hand, and nothing was built that would catch the fourth.
  Profile prose remains outside every figures check. One detail the earlier framing got slightly
  wrong and worth keeping straight, because it changes what a covering check has to match: the
  three were described as visible BOLDED body copy, and two of them are, but Philadelphia's second
  (`that $234K figure is citywide`) sat in plain unbolded prose inside the same `<span>`. A matcher
  keyed to `<strong>` would have found two of three and reported the surface handled. Confirmed
  correct: none of the three was in JSON-LD. Real fix is the profile stat-card + FAQ figure check
  boarded below, which must reach prose, bolded or not.

- **[P4]** **Em-dash target list: two pages added Jul 27, two remain out, both already clean.**
  `privacy.html` and `scouting-trip-workbook.html` are now named targets and their one em dash each
  is converted (the `<title>` moved to the ` | RetireMeHere` form the other 88 titles use; the
  workbook label took a comma). The risk boarded against this job did not materialise: the workbook
  is long, but a raw scan of both files finds exactly one em dash each and nothing else, in any
  region, scanned or not. Nothing to defer.
  What the sweep turned up: only TWO top-level pages are still outside the target list,
  `visit-before-you-decide.html` and `where-should-i-retire-quiz.html`, and both already read zero
  on both surfaces today. Adding them is a two-line edit that converts nothing and closes the
  target-membership axis for the whole top level. Deliberately not done here, because a target
  added is a target that must stay true and this chat was scoped to two characters.
  Also unscanned and out of scope by nature: `scouting-trip-workbook.pdf`, a separate built
  artifact that no HTML check reaches. If it was generated from the HTML it now differs from it by
  one label. Worth a look next time the workbook is regenerated, not before.

- **[P2]** **Superlative rules are now PATTERN-based, not string-based - keep them that way.** The old ban was
  a list of remembered phrases, and every single leak came through the list, never the logic. Six
  distinct shapes were found live on July 14: a modifier the list didn't have (`in ENTIRE database`),
  a region word between modifier and noun (`in our FLORIDA coverage`), a curation verb not on the list
  (`we have COMPARED`), a verb pointing at the corpus with no preposition (`Three cities TOP the
  database`), attribution voice (`our database NOTES NCH as...`), and a different noun (`our Florida
  SET`). All six are now closed structurally. When adding a new one, ban the SHAPE, never the string.
  Counter-check: `high on YOUR list` and `across the board` must NOT fire - the free-word slot is only
  allowed after a real determiner, and page-local objects (the two-city scorecard the reader is looking
  at) are bounded and static, so they cannot rot and are not this policy's business.
  **New leak found Jul 15 (Pensacola):** `Florida's lowest here`, and the bare `[STATE]'s lowest` form,
  scope a rank to the site through the word `here` with no ledger phrase to trip on. Same rot as
  `we cover`, different disguise. Close the SHAPE (a superlative/rank adjacent to a state name, or a rank
  plus site-scoping `here`), surgically enough that an innocent `here` (`the winters are real here too`)
  does not fire.

- **[P2]** **Validator: add a climate check group** - the validator compares `index.html` city FIGURES against
  the DB but has never checked the CLIMATE blocks. They happen to match 99/99, but nothing enforces it,
  and the July 13 rebuild added three fields (`janF`, `snow`, `sun`) that live in `index.html` with no
  guard at all. Add a group asserting (1) all five original climate values match the DB per city,
  (2) `janF`, `snow`, `sun` present and non-null for all 99. Silent drift of exactly this kind produced
  the Boulder bug.

- **CLOSED Jul 28, 2026 (shipped).** ~~**[P2]** **Validator: build the profile stat-card + FAQ figure
  check.**~~ Shipped as `check_statcard_faq` in the `profiles` group, with `tools/test_statcard_faq.py`
  as its planted-error test, 16 assertions, five harnesses now in the list. Proof it works on the real
  fault and not only on plants: run against the PRE-batch tree it reports 36 failures naming every one
  of them, and reports nothing else. All 36 are fixed in the same commit.
  Two things changed from the design boarded on Jul 27, both because the sizing pass was wrong about
  them. First, the method-callout is not a NOUN problem, it is a REGION problem: the first money figure
  in a `method-callout` or a `reality-check` block is the citywide home value, always, verified across
  all 22 such blocks. Three were wrong and NONE of the three is reachable by any home-value noun,
  because Tulsa's two blocks and Prescott's both open on the phrase "the $X figure". Tulsa's NRC
  callout was still built on `$194K` after the rebase moved it 14.9% to `$223K`. Second, the region
  walk must accept `aside` as well as `div`: the NRC is an `<aside>`, a div-only walk skipped it
  silently, and that alone would have left Tulsa's NRC unread.
  Original text below.
  **[P2]** **Validator: build the profile stat-card + FAQ figure check.** The 13 drifted figures are now
  reconciled (see RECENTLY SHIPPED), so this can be built against a clean tree. Three things the
  audit proved the check needs, each of which cost a wrong answer while sizing the job:
  (1) a HEDGE SLOT between the noun and the figure. The existing `PROSCONS_HOME` matcher requires them
  adjacent, but the profile voice is "the typical home value in Columbus IS AROUND $249,000". Reusing
  the pros/cons matcher as-is covers 13 of ~45 home figures and reports a near-clean surface.
  (2) a money token anchored to end on a DIGIT. A class ending `[\d.,]+` swallows the sentence comma
  and drags the other-place guard a clause forward, which is exactly how St. Louis hid behind an
  unrelated "suburbs".
  (3) the other-place guard bounded to the SAME clause, so it still skips Bentonville's Bella Vista
  figure and Tampa's Water Street range without excusing a real citywide drift.
  Also still unguarded: the stat card's ABBREVIATED monthly (`$4.9-6.1K/mo`) - `RANGE_RE` only knows
  the `$4,900-$6,100` long form, so all 43 monthly stat cards are unchecked; and the two variable stat
  slots, which carry real dimension scores under ~20 labels (Healthcare, Outdoor, Walkability,
  Community, Safety, Airport Access, Tax Friendliness, Wellness, Budget Score). Six slot labels are
  non-DB facts (Founded, Elevation, Metro, Coastline, Weather, State Income Tax) and must stay unmapped.
  Planted-error test the whole surface: the audit pass caught 5 of 5 planted errors across both.
  **SIZED Jul 28, and it is bigger than a check.** A draft of all three sub-checks was run across
  the 47 live profiles. Findings, so the next chat does not re-derive them: 35 of 47 abbreviated
  monthly cards disagree with v17; 1 variable slot disagrees (Pensacola Budget Score 8, D2 = 7);
  8 prose home figures disagree out of 157 matched. Ten of the monthly cards and three of the home
  figures shipped as P0 on Jul 28. (CORRECTED: the remainder was 31, not 26, and the shipped check
  reports 36.) The remaining 26 are P1 and are deliberately left in place: they
  are the check's own regression corpus, and hand-fixing them before the guard exists means doing
  it twice.
  Design settled while sizing, so it does not have to be re-argued: the money token must be
  `\$\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?`, which can only end on a digit or K/M and is what
  stops `$314,000, with` swallowing the comma. The hedge slot is a bounded run that crosses no
  comma, no second `$` and no bound word, which is enough for "the typical home value in Salt Lake
  City is around $580,000" at 28 characters. `hood-card` blocks are excluded structurally, which is
  what keeps Bentonville's Bella Vista `~$300K` and Tampa's Water Street range out; note Pittsburgh's
  Brookline card reads `around $246K` and passes today only because it happens to equal the citywide
  figure. `method-callout` is a THIRD sub-surface where a bare "median" is admissible, because that
  box only ever discusses the citywide home figure: 3 matches site-wide, all three were wrong, and
  San Antonio and St. Louis are reachable no other way. The variable-slot rule fires only on a
  `N/10` value, so `Healthcare: Barnes-Jewish` is out of scope, and a `N/10` under an unmapped label
  is a FAIL rather than a skip.

- **[CLOSED Jul 30]** **Two DB summer-comfort values do not survive scrutiny, and they feed the QUIZ, not just
  two pages.** Found Jul 30 while clearing the inverted summer label. `Climate Hot Sum` carries
  0.35 weight in the Mild Year-Round climate score, so this is a matching-engine defect that
  happens to also be visible on two comparison pages.
    - **Memphis = 8.** Memphis is hotter than Nashville on every other column (HEAT 8 vs 7,
      HUM 9 vs 8, Jan 42F vs 39F) and scores THREE POINTS MORE COMFORTABLE. At 8 it is the most
      summer-comfortable city in the entire southern set, ahead of Knoxville 6, St. Louis 7 and
      Kansas City 7, all of which are cooler in July. Memphis is Mississippi Delta. Compare
      New Orleans 2, Miami 2, San Antonio 3, Tampa 4. A defensible value is 3 to 4.
    - **St. Petersburg = 7 against Tampa = 4.** Identical HEAT (7), identical HUM (9), Jan means
      one degree apart, twenty miles apart. St. Pete's peninsula breeze is real but it is not
      three points of it. One of the two is wrong; the pair cannot both be right.
  Both need a scoring decision from Laurie, not a mechanical fix, because the correct value is a
  judgment against the rubric anchors. Everything downstream waits on it: the DB cell, `index.html`,
  the two profiles, the two comparison pages, and the quiz.

- **[CLOSED Jul 30]** **`nashville-vs-memphis` and `tampa-vs-st-petersburg` carried the inverted summer
  label, deliberately.** Held back from the Jul 30 batch. Relabelling them without fixing the DB
  first would convert a currently-buried wrong number into a prominent confident claim: the table
  would assert Memphis has 8 of 10 summer comfort. Worse on `nashville-vs-memphis`, where the PROSE
  is factually RIGHT about reality (it says Memphis "sits in the Mississippi Delta and is
  meaningfully hotter") while citing the numbers through the inverted label, explicitly, in the
  words "hot summers (5 vs. 8, where lower is milder)". Two errors currently cancel and the page
  reads correctly by accident. Fixing either one alone breaks it. Four prose sites need rewriting,
  including the claim that "Nashville wins every climate-comfort row". Both pages also carry a
  checkmark on the wrong city, which is a SYMPTOM of the bad value rather than a separate bug:
  the 2-point rule means only an implausible gap is wide enough to generate a mark in this column.

- **[P3]** **Visible FAQ text and FAQPage schema are out of sync on 6 pages, 7 Q&As.** Audited
  Jul 30 across all 24 pages carrying FAQ schema. Two were fixed in the same pass because this
  batch already opened those files: `nashville-vs-memphis` Q2 (`Franklin/Brentwood` in schema vs
  `Franklin and Brentwood` visible) and `tampa-vs-st-petersburg` Q5 (schema reads "and Tampa Bay
  is among", visible reads "with Tampa Bay among"). Still open: `bend-vs-boulder` Q2,
  `san-antonio-vs-fort-worth` Q2, `scottsdale-vs-santa-fe` Q3 and Q5, `visit-before-you-decide` Q2.
  All seven are wording-level, none change a figure, so this is P3 rather than P2. The check is
  cheap and mechanical: parse the JSON-LD, strip tags from the visible pairs, compare normalised.
  Worth shipping WITH the check rather than as a one-off sweep, since nothing prevents recurrence.

- **[P2]** **A published figure on `nashville-vs-memphis` matches no formula anyone can find.**
  The page cited "a mild-year-round score of 7 vs. 5" in two places. The rubric's documented
  formula (W*0.40 + H*0.35 + M*0.25) gives 6 and 6. The code in `getCityScore` gives 4 and 3.
  Neither is 7 and 5. The clause was CUT on Jul 30 rather than recomputed, because publishing a
  third unsourced number would be worse than publishing none. Two questions behind it: where did
  7 and 5 come from, and do other comparison pages cite a mild-year-round score from the same
  unknown source? Grep before assuming this page is the only one.

- **[P2]** **The rubric documents a climate formula the code does not run.** Second instance of
  rubric-vs-code drift, alongside the D1 filter item already boarded. `scoring_rubric_v3.2`
  publishes Mild Year-Round as (Winter x 0.40) + (Summer comfort x 0.35) + (Humidity x 0.25).
  `getCityScore` implements a worst-of-winter-and-summer model driven by janF, HEAT and HUM, and
  never reads `Climate Hot Sum` at all. Warm & Dry, Four Seasons and Cool/Mountain also differ
  from their documented forms. Either the rubric or the code is the spec; right now neither is,
  and the rubric is the one being used to score new cities by hand. Fold into the Rubric v3.3 item.

- **[P3]** **`Climate Hot Sum` is maintained but unread. Decide whether to keep it.** It is
  published on comparison pages and hand-maintained across 99 rows, and no code path consumes it.
  Either wire it into the climate scoring, in which case the two bad values were a live defect
  waiting to happen, or retire the column and drive the comparison rows off HEAT and HUM, which
  are what the engine and the profiles already use. Leaving it as decorative data guarantees it
  drifts again.

- **[P4]** **Wilmington NC scores 6 on `Climate Hot Sum` with HEAT 7 and HUM 9.** Same twin group
  as the Florida 4s. May be justified by latitude the way Pensacola's 5 is, may not. Cheap to
  settle next time the climate columns are open.

- **[P2]** **Climate rows have no validator coverage of any kind.** Nothing reads them, which is why
  an inverted label survived on eight pages and two bad DB values survived in the quiz. Two checks
  worth having, each with a planted-error test: (1) label-to-column polarity, asserting the rendered
  label agrees with the column's direction, and (2) a DB-side consistency assertion that
  `Climate Hot Sum` does not contradict `HEAT (0-10)` beyond a tolerance. On the second, note the
  crude form (`10 - HEAT`) has a correlation of only -0.693 and flags plausible cities like
  Burlington and Traverse City, so the check needs to be RELATIVE (within-pair, or against
  same-region peers) rather than absolute, or it will cry wolf.

- **[P3]** **Open question from the same audit: is `Climate Hot Sum` calibrated absolutely or on a
  curve?** St. Louis and Kansas City both score 7 with HEAT 8 and 8/7 humidity, and
  `st-louis-vs-kansas-city` describes "hot, humid summers" in prose two paragraphs from a 7 of 10
  comfort score. If the column is graded relative to the database rather than absolutely, that is
  fine and should be written down. If it is meant to be absolute, a cluster of Midwest cities is
  three points high. Not blocking, but it decides whether the check above is even well-defined.

- **[P1]** **Latent label bug on `knoxville-vs-chattanooga`: inverted climate scale.** The summer row is labeled
  "Hot summers (lower = milder)" but populated from `Climate Hot Sum`, which the rubric defines as summer
  COMFORT (10 = comfortable, 1 = extreme heat) - so higher is milder, and the label says the opposite.
  Invisible there because both cities score 6, but the label is wrong. The new `knoxville-vs-nashville`
  page uses the correct "Summer comfort (higher = milder)". Fix the Chattanooga label on its next touch;
  audit other comparison pages for the same inverted wording while at it. Latent, not live-wrong.

- **[P4]** **Visit-block hooks: 4 profiles open on a template.** `asheville`, `bend`, `boulder`, `fort-collins`
  all open the Visit hook with "A scoring sheet can't tell you..." / "A scoring sheet only tells you...".
  PROFILE-FORMATTING.md is explicit that the hook must be "the single most concrete, specific, appealing
  thing about the city... never a generic adjective" and "do not open with a template; every hook opens
  differently from every other block." These four are the last scaffolding repeat in the set: the other
  39 hooks are distinct, and the rental-line openers are 42/43 distinct. Small, precise, judgment-based
  rewrite of four opening sentences. Not batchable.

---

## BOARDED - opened by the layout-check work (Jul 28)

- **[P3]** **Any doc that lives outside the repo is unwatchable.** Section 4a makes the repo
  canonical and the enumeration rule keeps repo docs honest, but `SKILL.md` sits in
  `/mnt/skills/user/` and this project's own instructions sit in project settings. Both
  restated the hand-off shape, both went stale on Jul 14, and neither could be caught by
  anything. The skill is now rewritten to delegate to the repo docs instead of restating
  them. **The project instructions still say the old thing** and should get the same
  treatment: they currently ask for `<city>-profile.html` and city-prefixed photos to
  rename at deploy time. Worth a periodic audit of both against the repo, since no tool
  can do it.

## BOARDED - opened by the Casper build (Jul 28)

- **[P4]** **The NRC roster grep over-counts.** `PROFILE-FORMATTING.md` v1.6 names
  `grep -l 'reality-check-eyebrow' cities/*/profile.html` as the enumeration of record, but that
  matches the CSS selector as well as the markup, so profiles carrying the inherited stylesheet
  and no callout are counted. Knoxville, Roanoke and Prescott are three such today; the grep
  returns 17. Tighten it to `grep -l 'class="reality-check-eyebrow"'` and re-count. Casper was
  built with the unused NRC CSS stripped, so it does not add to the problem.
- **[P1]** **index.html Casper scoreNotes name the hospital "Wyoming Medical Center".** It has been
  Banner Wyoming Medical Center since the Banner Health acquisition. Low urgency: with
  `Casper_WY` now in PUBLISHED_PROFILES the inline detail view never renders. Fold into the
  next BATCH.

## ACTIVE - city profile builds

- **Next in queue:** open. Casper shipped Jul 28.
- Live profiles: 48. Portland ME shipped Jul 29; Casper Jul 28; Tulsa Jul 24; Roanoke the same day; San Antonio Jul 19; Fort Collins,
  Prescott, Knoxville and Savannah shipped earlier in the same window.
- NRC city count: **17 profiles carry a callout**, not 10 and not 12. Both the June count and the
  Jul 24 "San Antonio makes 11, Tulsa makes 12" note were wrong. Closed Jul 25: neither
  `PROFILE-FORMATTING.md` nor `MEDIAN-HOME-METHODOLOGY.md` enumerates NRC cities any more. The
  enumeration of record is `grep -l 'reality-check-eyebrow' cities/*/profile.html`. Do not
  reintroduce a list in either doc.
- **Tulsa follow-ups:**
  - **CLOSED Jul 28, 2026, verified.** ~~`pick-and-compare.html` carries Tulsa at `d2:7`; DB and
    `index.html` both say **D2 = 9**. Stale.~~ The 72-score job carried it: the live blob now reads
    `d2: 9` for Tulsa, and Coeur d'Alene, boarded separately as unreachable by name-keyed checks,
    now reads `$611,000` against a v17 `$611,000`. Both checked against live `main` on Jul 28. The
    SHAPE of the Coeur d'Alene hole is still open and is boarded as P2; only its data is clean.
  - Detail photo resolved Jul 24: Boston Avenue Methodist Church, CPacker at English Wikipedia,
    CC BY 2.0, credited on the image and in the footer with a license link and a cropped note.
  - Gilcrease Museum: CLOSED Jul 25 on both surfaces (landing card and scoring doc), marked as
    reopening spring 2027 rather than deleted, since the collection still earns Tulsa its arts tier.
  - `index.html` Tulsa property tax: CLOSED Jul 25, 0.77% -> 0.79% in both the pros bullet and the
    D5 scoreNote.

---

## ACTIVE - boarded July 27, 2026 (validator blind spots found during the rebase)

- **[P2] `check_docs` reads its profile count from the first regex hit anywhere in the board, so it
  passes by coincidence.** Found Jul 29 while auditing board currency. The check's docstring asks
  whether TASKBOARD and SITE-OPERATIONS-LOG are current with the live repo, and it tests that by
  comparing a profile count. It finds that count with `re.search(r"(\d+)\s+profiles", board)`,
  which takes the FIRST match in the file. Today that resolves to a fragment of narrative prose
  inside a header entry, "so all 48 profiles inherited it", which happens to be right.
  **Why it will break.** The board currently holds twelve `<N> profiles` strings reading
  48, 48, 47, 47, 47, 47, 47, 46, 48, 48, 36, 45. Session notes routinely name historical counts.
  The next entry written above the assertion that says 47 will fail the gate on a correct board.
  Worse in the other direction: the deliberate claim the check exists to guard,
  `**Verified live at last update:** N profiles`, could go stale and still pass because some
  paragraph above it names the right number.
  **Fix.** Anchor to the labelled assertion rather than the first match: read the
  `**Verified live at last update:**` line specifically, so the board has exactly one place that
  has to be true. Needs a planted-error test both ways, a stale assertion must fail and a
  historical count in prose above it must NOT.
  **Same family as two items already on this board:** the `check_comparison_dims` prefix-match on
  `D4 Resil.` / `D10 Comm.`, and the `check_hardcoded_counts` hyphen variant that hides
  "100-city database (v14)". Three instances of one pattern, a check that can pass for the wrong
  reason. Worth reading the other checks for the same shape while in there.

- **[P2] The recency chain has no structural check and silently grew a second `Before that:`.**
  Found Jul 29. The header ladder is Last updated -> Before that -> Earlier -> Previously, and each
  session is meant to demote the one above it. A chat inserted an entry without demoting, so two
  `Before that:` blocks coexisted and nothing noticed. Three assertions would close it: exactly one
  `**Last updated:**`, one `**Before that:**`, one `**Earlier:**`. Stateless, unambiguous, no
  false-positive risk, and cheap enough to fold into `check_docs`.
  **Deliberately NOT proposed: orphan detection.** Catching an item removed from the board with no
  CLOSED entry is the failure that lost the `pensacola-vs-fort-myers` record, but it needs the
  previous board version, which means git working-tree state. The gate runs on fresh clones where
  that state is unreliable, and a check that behaves differently depending on how it was invoked is
  worse than the gap it closes. Left uncaught on purpose.
  **The cause this does not reach.** Board edits are remembered rather than structural: they live
  in whatever apply script gets written that session. Three of five board updates on Jul 29 were
  complete. A `tools/apply-template.py` skeleton with the board block pre-stubbed would make
  omission require deletion rather than recall, which is the only fix that addresses the actual
  failure mode. Not boarded as a task, because it is a convention decision rather than a defect.

- **CLOSED Jul 27, 2026 (shipped).** ~~`best-places-to-retire-on-a-budget.html` roster is stale against v17.~~ Shipped exactly as decided: roster = R1 (30), prose = central estimate, both in one
  commit. Delta as boarded proved correct against v17: off Beaufort/Pensacola/Rio Rancho/Sioux Falls,
  on Indianapolis/San Antonio/Wilmington DE, 31 - 4 + 3 = 30. Original text kept below for the record.
  The page was built off
  tier R1 (under v16.6, R1 was 33 and the page carried 31, missing only Indianapolis and Wilmington;
  nothing on the page was outside R1). R1 is now 30. The page therefore carries FOUR cities that
  left the tier - Pensacola, Beaufort, Rio Rancho, Sioux Falls - and is MISSING San Antonio, which
  dropped into R1 when its Median Home fell from $320,000 to $251,000. Per-city monthly figures on
  the page are all correct against v17; it is the roster that did not move.
  **Delta re-derived against v17 on Jul 27, use these numbers:** page carries 31 cards (18 live,
  13 coming-soon), R1 is 30. Four come OFF - Beaufort (now R2, $5,300 start), **Pensacola (now R2,
  $5,000 start, and this is a LIVE card for a Tier 1 profile, so removing it is an editorial call,
  not a mechanical one)**, Rio Rancho (R2), Sioux Falls (R2). Three go ON - Indianapolis
  ($4,300-$5,400), San Antonio ($4,700-$5,800), Wilmington DE ($4,700-$5,800); note Wilmington NC
  is R2 and must NOT be added. Net 31 - 4 + 3 = 30.
  The prose bar as written ("starts under about $5,500") admits **47** cities in v17, not 46 as
  first boarded. Note which way that cuts: the prose as written currently JUSTIFIES all four cities
  the tier says should come off. So this is not a stale roster against agreed prose; it is two rules
  that were never the same rule. Fix both in one pass or the page contradicts itself either way.
  **Decide before fixing:** the page's methodology block says the bar is "every city whose all-in
  monthly estimate STARTS under about $5,500". That describes the LOW end of the published range,
  not the central estimate the tier uses, and it admits 46 cities in v17 rather than 30. The prose
  and the tier have been describing different rules all along; the page only ever sat close to R1 by
  luck. Pick one basis and restate the prose to match, because a reader can check that claim against
  the numbers printed on the same page. Recommendation: keep R1, say "central estimate".
  **DECIDED Jul 27, 2026: keep R1.** The roster is tier R1 and the prose is restated to describe
  the CENTRAL estimate, not the low end of the published range. Rationale: R1 is the basis the quiz
  and the DB actually use, so the page then agrees with the rest of the site instead of inventing a
  private rule, and 47 cards is a worse page than 30. Consequence to carry into the fix: the
  methodology sentence must stop saying "starts under about $5,500", because that sentence is what
  currently justifies keeping Beaufort, Pensacola, Rio Rancho and Sioux Falls. Roster and prose move
  in the SAME commit; shipping either alone leaves the page contradicting itself.

- **CLOSED Jul 27, 2026 (shipped in the same commit).** ~~`check_cards` does not validate tier
  membership.~~ `check_roster` added, wired into the `cards` group, with `tools/test_roster.py`
  as its planted-error test, 7 assertions. Proof it works on the real fault, not just on plants:
  run against the PRE-batch page it reports 7 failures naming exactly the four extras and the
  three omissions. Only pages whose roster is a DB PREDICATE are in `DB_ROSTERS`, which today is
  the budget page alone. Test 5 is the one that matters longest: markup that yields zero cards
  fails loudly instead of comparing nothing.

- **[P2]** **Two pillar pages have no city cards at all, so `check_cards` reads them and finds nothing.**
  `best-places-to-retire-in-florida.html` and `best-places-to-retire-in-the-midwest.html` are both
  in the `check_cards` target list and both parse to ZERO cards: they use `bestfor-card` markup, not
  `city-card`. The check fetches them, iterates nothing, and passes. This is the silent-no-op shape
  the emdash harness already exists to prevent, sitting in a different check. Note this is NOT the
  same hole as the roster gap just closed: those pages carry no per-city cards to check, so their
  figures live in prose instead, and see the Florida item directly below for what that let through.
  Fix is a decision, not a patch: either bring their money prose under a check, or drop them from the
  `check_cards` list and say in the code why they are exempt. Leaving them listed-but-unread is the
  worst of the three, because the target list currently reads as coverage.


- **[P3]** **The site nav is copy-pasted into 87 files in seven variants, and 46 of them cannot take a menu
  item at all.** Found while adding the budget pillar to the menu. There is no template, no include,
  no build step: every header is a literal copy. The variants differ in path style (absolute on
  `index.html`, relative elsewhere), in class names (`nav-dropdown-item` on 38 pages, bare `<a>` on
  `index.html`), in label form ("Arts Lovers" on index desktop, "For Arts Lovers" on all mobile and
  all other desktop), and in which top-level links are present (`index.html` alone carries "Plan a
  Visit"). Three consequences, in the order they will bite:
    1. The 46 city profiles carry a 3-link nav, Home / Top Cities For... / Find My Match, with NO
       dropdown. They did not get the budget item and cannot get any future one. Roughly half the
       site's pages are therefore permanently one menu behind, and a reader who lands on a profile
       from search sees a different site than one who lands on the homepage.
    2. `visit-before-you-decide.html` has flat links and no dropdown either, a seventh variant of one.
    3. Every future menu change is a 40-file edit that must be scripted, and any hand-edit
       reintroduces drift. The "On a Budget" entry that existed on exactly one page out of 87 is
       what that looks like after one occurrence.
  Nothing validates nav parity today, so none of this fails a gate. The cheap first move is a check
  that asserts every page's dropdown contains the same set of hrefs, which would have caught the
  single-page "On a Budget" the day it shipped. The real fix is one nav partial and a build step,
  which is a bigger call about whether this site stays hand-authored HTML.

- **[P1]** **Florida and Midwest pillar titles both claim "The 8 Best Places" and both render six cards.**
  Noticed while listing the pillars for the menu decision. Not verified further and not fixed: the
  count may be stale, or the pages may deliberately narrate 8 while carding 6. Worth ten minutes
  before either page gets promoted anywhere, since the title tag is what search results show.
  Note `check_hardcoded_counts` does not catch these, for the same reason it missed the "100-city
  database (v14)" string already boarded: the number is fused into prose it does not scan.


- **[P3]** **Rubric v3.3.** `scoring_rubric_v3.2` is wrong in six places, four of which are already resolved
  elsewhere on this board: (1) budget ranges still published as Under $3,500 through $8,000+, when
  both the DB and the quiz use Under $5,500 through $9,000+; (2) the D1 hard-filter ladder, resolved
  Jul 18 as keep-generic-7, pairs with deleting dead `D1_THRESHOLDS` from index.html; (3) D4
  described as retired and folded into D2, when it is live as Climate Resilience & Insurance with 99
  of 99 cities scored and no anchors documented anywhere; (4) the Universal Methodology section still
  scopes D2 to retiree-target neighborhoods, which BUDGET-METHODOLOGY.md section 4 already calls "its
  fossil, struck 2026-07-13"; (5) consequently the D2/D6/D9 grouping must become D6/D9, since D9 IS
  still genuinely neighborhood-scored (Memphis and San Antonio both sit at D9=7 where the rubric's
  own anchor puts their citywide figures at 1-2); (6) the D2 data-source line reads "Zillow/Redfin"
  and should be Zillow ZHVI only.
  Also check while in there: D2's anchor bands key off median-home breakpoints at $250K / $375K /
  $525K / $750K, and 23 D2 scores moved in the rebase. Those bands were calibrated against the old
  patchwork column.
  **Structural question to settle first:** the rubric is the only governing doc NOT in the repo. It
  lives in project knowledge as a .docx. That is a direct conflict with the source-of-truth rule in
  SITE-OPERATIONS-LOG section 4a, and it is the likeliest reason this doc drifted further than any
  other: nothing pulls it, nothing validates it, no commit touches it. Ship v3.3 as markdown in
  `docs/`, not as another .docx.
  **(7) The D2 median-home band table does not describe what the database does.** Added Jul 29
  from the band-mover review. The rubric publishes `$525-$750K` as a 3-4 band; every one of the
  twelve cities the database holds between `$495,000` and `$571,000` scores 5 or 6, none lower.
  The scores are peer-consistent and correct, so this is the table that is wrong, and it is the
  most actively harmful of the seven: the other six are stale descriptions of settled decisions,
  whereas this one will actively mis-score the next city anyone adds from the rubric alone.
  Either restate the bands to match practice or say plainly that the bands are indicative and
  the peer cross-check governs.

- **[P4]** **MEDIAN-HOME-METHODOLOGY.md needs three lines and was deliberately not touched on Jul 27.**
  (1) Section 1 says the figure is "refreshed annually"; the first annual refresh has now actually
  run, so record the date and that it used the 2026-06-30 ZHVI column. (2) Note that the refresh is a
  column swap against a file already in hand, not research; section 6 currently reads like a research
  task ("pull current Zillow ZHVI for all 99 cities") and will mislead the next operator. (3) Section
  6's out-of-cycle triggers should record that this refresh fired OUTSIDE the June cycle and why
  (Memphis 33% off was the credibility trigger in practice); a doc that says "annual" with no record
  of an off-cycle run invites the next operator to wait until June. Separately, section 9 lists
  `/methodology.html` as a surface this methodology touches. It 404s and is not in the sitemap.
  Either build it or strike the line.

- **[P2]** **`check_highlight_surfaces` enforces highlight parity but not SCORE parity.** `pick-and-compare.html`
  carries its own JSON blob (`monthlyEst`, `monthlyMid`, `medianHome`, `medianHomeMid`, `budgetTier`,
  `d2`) and nothing held it to the DB, so d2 drifted on 72 of 99 cities unnoticed. All ten dimensions
  now agree across both surfaces, but nothing stops it recurring. Extend the check to every `dN` field
  plus the four cost fields. Planted-error test required.
- **[P2]** **A city whose name contains non-ASCII is invisible to the surface checks.** Coeur d'Alene is stored
  `Coeur d\u2019Al\u00e8ne` in the pick-and-compare blob, so name-keyed checks skip it. Its record was
  stale at $553K against a DB $611K and the gate read clean. Any check that joins the two surfaces by
  literal name has this hole.
- **CLOSED Jul 28, 2026 (shipped).** ~~**[P2]** **The abbreviated stat-card money form is
  unparsed.**~~ Now parsed and gated by `check_statcard_faq`. Final count on the profile surface was
  35 of 47 wrong, of which 10 shipped as P0 on Jul 28 and the remaining 25 in this commit.
  **[P2]** **The abbreviated stat-card money form is unparsed.** The editorial modal renders
  `value: '$3.5–4.8K<span>/mo</span>'`. The validator reads `$X,XXX–$X,XXX` only, so St. Louis sat at
  $3.5-4.8K against a DB $4,100-$5,200, wrong before the rebase and never flagged. Same hole for the
  `$192<span>K</span>` home form.
  **Measured Jul 28: 35 of 47 live profiles carry a wrong abbreviated monthly.** Not a St. Louis
  quirk. Ten were off by $300 to $600 and shipped as P0 the same day; twenty are off by exactly
  $100 and are P1 pending the check. The rendering convention is one decimal with a trailing `.0`
  dropped, established by the 12 cards that were already correct, and both span variants are live
  (`$5.9-7.3K<span>/mo</span>` and `$5.8-7.3<span>K/mo</span>`), so a comparison has to normalise
  HTML entities before it reads.
- **[P2]** **No vintage check on `Median Home`.** The rebase fixed the values; nothing prevents the column
  ageing into a patchwork again. Add a gate check that flags any DB figure more than N% off the
  current ZHVI CSV, as boarded on July 26. This is the mechanism fix, not the data fix.
- **CLOSED Aug 10, 2026 (shipped).** ~~**A `Monthly Est == f(Median Home)` assertion would have
  caught 31 cities.**~~ Built as assertion three of `check_afford_data`, with
  `tools/test_afford_data.py` as the planted-error harness. It runs the full sections 3 to 6
  formula over every row on every deploy and asserts it rebuilds both the `Monthly Est` string
  and the `Budget Range` integer. Shipped as part of the affordability calculator rather than on
  its own, because that page had to reproduce the formula anyway.

  Building it surfaced one thing the docs could not have told us. Section 5 never said whether
  the state modifier or the climate adjustment is applied first to the utilities line, and the
  two orders disagree on six cities. The order actually used was recovered from the database,
  written into section 5 in the same commit, and is now asserted. So the July 27 claim that
  nothing further was needed from the docs was not quite right: the tables were exact, the
  order of operations was missing.
- **[P1]** **DB title cell is stale on three counts.** Row one of the `City Database` sheet reads
  `RetireMeHere - City Database (June 2026, v3.3 - 100 cities)`. The file is `_Jul_27_v17`, holds
  ninety-nine rows, and v3.3 is the SCORING-RUBRIC version, not the database version. Invisible to
  `check_hardcoded_counts`, which reads HTML and never opens the xlsx.

  Half of this item is now done: the `pick-and-compare.html` half is fixed and the string is gone
  from that file. Re-verified Aug 10, 2026. The database half is a binary edit and needs the
  operator, not an apply script. Worth doing at the next DB touch rather than opening the file
  for it alone.

---

## ACTIVE - boarded July 25, 2026 (BATCH: Gilcrease, NRC list, Tulsa PropTax)

- **CLOSED Jul 27, 2026 (shipped).** ~~`top-cities-for-sports-fans.html` Scottsdale card names a
  franchise that left in 2024.~~ Shipped in the roster commit: `Mullett` dropped from the card and
  the pill changed `5+ teams` -> `4 teams`, and the same fossil corrected in
  `docs/sports-fans-cities-scoring-analysis.md`. Placement checked before editing and did NOT move:
  Tier 1 requires four or more leagues and Cardinals, Diamondbacks, Suns and Mercury is four.
  **The open sub-question is answered: Cactus League does NOT count as a team.** It stays listed on
  the card as a genuine draw but is excluded from the count, which is what makes the pill 4 and not
  5. Original text kept below for the record. The
  card reads `Cardinals · Diamondbacks · Suns · Mullett · Mercury (WNBA) · Cactus League spring
  training` with a `5+ teams` pill. Mullett Arena was the Arizona Coyotes' venue; the NHL board of
  governors approved the sale and relocation to Utah in April 2024 and the Phoenix metro has had no
  NHL team since. The site already knows this, because the Salt Lake City card correctly reads
  `Mammoth`. Fix is two lines, not one, which is why it was boarded rather than shipped Jul 25:
  drop `Mullett ·` from line 584, and change the pill on line 586 from `5+ teams` to `4 teams`
  (Cardinals, Diamondbacks, Suns, Mercury). Decide separately whether Cactus League counts.
- **[P1]** **Memphis card and arts doc will go stale in autumn 2026.** `top-cities-for-arts-lovers.html` and
  `docs/arts-lovers-cities-scoring-analysis.md` both name `Brooks Museum of Art`. It is genuinely
  open in Overton Park today, so nothing was changed. It closes there in autumn 2026 and reopens
  downtown in December 2026 as the **Memphis Art Museum**. Two edits, both dated, both known now.
  Do them at the autumn close, not before.
- **[P4]** **Enrichment-vs-DB property tax is a category mismatch, not a set of bugs.** The Jul 24 board read
  "index.html says 0.77, DB says 0.79, one is wrong". The premise was wrong. `D5-TAX-METHODOLOGY.md`
  section 2 defines `PropTax Rate %` as **one value per state**, and the DB holds exactly one value
  per state across all 39 states. The `index.html` D5 enrichment carries **county or city** rates,
  several of which name their county in the prose (Nueces, Tarrant, Williamson, Escambia). A sweep
  of all 38 property-tax figures in the enrichment found 17 cities where the two disagree by design:
  Ann Arbor, Burlington, Charleston, Charlottesville, Corpus Christi, Delray Beach, Fort Myers,
  Fort Worth, Georgetown, Greenville, Miami, Naples, Pensacola, Provincetown, Sarasota, Tampa,
  Traverse City. None of these is a bug. Tulsa was the one real error only because it is the sole
  Oklahoma city, so there is no city-versus-state distinction to preserve, and 0.77 matched neither
  the state figure nor any sourced Tulsa county rate (which run 0.94% to 1.06%). **Open question,
  not a defect:** neither doc says the enrichment may hold county rates. Either write that down in
  `D5-TAX-METHODOLOGY.md` or add the `Local Tax Adj` column that doc already proposes.
- **[P3]** **Institution-status checks are still manual.** Gilcrease was caught twice by hand. The validator
  cannot know whether a named museum is open. Consider a thin `docs/INSTITUTION-WATCH.md` listing
  every named institution with a known status change and its date, so landing cards get checked on a
  schedule instead of when someone happens to notice.

---

## ACTIVE - comparison pages

Live: 21. Shipped since last board update: Knoxville vs Asheville, San Antonio vs Fort Worth, Knoxville vs Nashville, Fort Collins vs Boulder,
Knoxville vs Chattanooga, Bend vs Boulder, Bloomington vs Lexington, Madison vs Ann Arbor,
Madison vs Columbus, and others.

Unlocked and ready to build now (both cities live):
- **Arizona three-way cluster** (Prescott now live, so this is unblocked)

~~**Knoxville vs Asheville**~~ SHIPPED August 3, 2026. See the CLOSED section above.

Unlocks pending a build:
- (none)

~~**[P1] 8 of 20 live comparison pages have no CTA link from either city profile.**~~ CLOSED
August 3, 2026. Fifteen edges added across twelve profiles. See the CLOSED section below.

~~**[P2] Add `check_comparison_cta_reciprocity` to the validator.**~~ CLOSED August 3, 2026,
shipped in the same commit as the wiring it guards.

**[P3] Add `check_lists_heading_count` to the validator.** Parse the `lists-section` `<h2>`, map
the number word to an integer, compare against the count of `.list-card` anchors in the same
section, fail on mismatch and skip cleanly when the heading carries no number. Would have caught
all six headings closed above. Planted-error test required.

~~**[P3] Stale placeholder comment on `cities/kansas-city/profile.html`.**~~ CLOSED August 3,
2026, folded into the CTA wiring batch as boarded. The block it sat above was a Midwest guide CTA
occupying the head-to-head slot; it is now the real head-to-head, and the Midwest guide keeps its
link from the lists section on the same profile.

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty)

---

## PARKED / BACKLOG

- **[P1]** **Four CityDatabase / index.html data conflicts on San Antonio, surfaced during the Jul 19 build.**
  Not fixed in the build chat because three of them touch shared surfaces, which makes them BATCH work:
    - DB `Highlight` says "Citywide median home $260K" while DB `Median Home` reads `$320,000` and
      `CITY_ENRICHMENT` scoreNotes D2 reads "~$320K". The Highlight string renders on
      `pick-and-compare.html` and the foodies landing card, so the site currently publishes two
      different medians for the same city. Worst of the four.
      **Jul 21: escalated out of PARKED. This is a seven-city cohort bug, not a San Antonio bug.
      See the top of ACTIVE - batch / site-wide operations.**
      **Jul 23: CLOSED by deletion. The DB `Highlight` column no longer exists (v16_6), so there is
      no second median to conflict with. `Median Home` is the only DB home figure now, and both
      rendering surfaces are gated against it and against each other. The `PropTax Rate %` and
      `Budget Range` items below are untouched and still open.**
    - DB `PropTax Rate %` = 1.4 for San Antonio. External sources put Bexar County effective rates at
      1.55% to 1.96%, and index.html cons/scoreNotes already publish ~1.8%. The profile shipped with
      1.8% for internal consistency. The DB field is the thing to fix.
    - DB `Budget Range` = 2, but `Monthly Est` `$5,100-$6,400/mo` puts the midpoint in Range 3.
    - `CITY_ENRICHMENT["San Antonio"].scoreNotes.DW` says "Jan avg 44 F"; DB `Jan Mean F` = 52.
- **[P4]** **San Antonio landing-page placements: Healthcare Tier 2 and Arts Lovers Tier 2.** BATCH scope.
  Neither scoring-analysis doc evaluated the city at all (zero mentions), so these are omissions, not
  rejections. Healthcare Tier 2 is defined as "major university medical center or state flagship";
  San Antonio has University Hospital plus UT Health San Antonio with the Mays Cancer Center holding
  NCI designation, the same credential that places Miami in Tier 2. Arts Tier 2 runs 8.3 to 8.8;
  San Antonio reads 8.3 to 8.5 against Fort Worth at 8.4. Touches five files: the two landing pages,
  the two scoring-analysis docs, and a return trip to `cities/san-antonio/profile.html` to take the
  Lists section from 2 cards to 4.
- **[P4]** **`PROFILE-FORMATTING.md` NRC list is stale at ten cities.** San Antonio is the eleventh.
- **[P2]** **Validator superlative check matches `on this list` literally and fires on within-page lists.**
  Caught `cities/san-antonio/profile.html` ("the most genuinely urban option on this list") on Jul 21,
  where "this list" meant the four neighborhood cards in the same section, not the city dataset. The
  claim does not rot when a city is added, so this is a scoping false positive. Two sibling phrases in
  the same section ("the most expensive of the inner-loop municipalities", "the most house per dollar
  of the retiree-target areas") pass, which confirms the check is keying on the string and not the
  shape. Copy was rewritten rather than the check loosened. If the pattern is scoped later, it needs a
  planted-error test first.
- **[P2]** **`scripts/generate_brief.py` is referenced by the `retiremehere-city-profile` skill but is not in
  the repo** (404 on raw). The Jul 19 brief was computed by hand against the thresholds documented in
  the skill. Either commit the script or amend the skill; as written it points the next build at a
  file that is not there.
- **[P4]** **Landing-page card counters are positional, not ranks.** `top-cities-for-foodies.html` numbers
  restart at 1 per tier and each tier is alphabetical, so the on-page number never has to match the
  scoring-analysis doc's rank. Recorded because it was raised as a discrepancy during the San Antonio
  build and was not one.
- **[P3]** **Rubric doc drift: `scoring_rubric_v3.2` describes a filter the code does not run.** The rubric says
  "D1 is the only dimension with a hard filter threshold" and describes a priority ladder (Must Have 8+,
  Very Important 6+, Somewhat Important 4+). Live code does neither. `MUST_HAVE_THRESHOLD = 7` filters
  EVERY dimension marked Must Have, and D1 is not special. `D1_THRESHOLDS` (index.html ~line 6346) is
  defined and referenced nowhere: dead code. Decision made Jul 18, 2026 after checking the D1 spread
  (99 cities: 44 at 7+, 32 at 8+) and the D1=7 cohort city by city: KEEP generic-7. Raising the floor to
  8 would strand Bozeman, Boise, Tulsa, Pensacola, Sarasota, Spokane, Des Moines, Virginia Beach and
  Georgetown, all of which carry real air access. Restoring the ladder would also make "Very Important"
  silently cut 29 of 99 cities while the quiz only ever warns about Must Have. Resolution: delete
  `D1_THRESHOLDS`, rewrite the rubric to describe generic-7 as shipped. Doc + dead-code only, no
  matching-logic change.
- **[P3]** **`D4` key reuse for Climate Resilience & Insurance.** The dimension occupies the internal key `'D4'`,
  the slot the retired cost-of-living dimension vacated. Functionally harmless; it is a trap for anyone
  cross-referencing the rubric, where D4 means something else. Fix ONLY as its own scoped rename with a
  full grep (DIMENSIONS array, every city score object, `quizState.priorities`, `getCityScore`, the
  filter loop, results render) plus a validator run. Never bolt onto other work. Low value, wide blast
  radius: leaving it is a defensible permanent answer.
- Site-wide bolding pass (PROFILE-FORMATTING item 6, judgment-based, not batchable)
- Booking.com affiliate (Awin) - applied; deploy deferred until Expedia fully verified
- Pinterest save-rate optimization (ongoing; cadence + pin copy)
- `Ann Sun %` provenance: ~30 of 99 values are interpolated from the nearest NOAA station. Fine behind
  the 55% dealbreaker cutoff. Do NOT print these figures on a profile page without verifying that city.
- Weather weighting: picking a weather preference auto-sets `DC` to "Very Important" (weight 3) while
  nine other dimensions sit at 1, so climate is 25% of the match score. This is why Florida leads a
  "Mild Year-Round" search ahead of Santa Barbara. Working as designed, not a bug. Raising weather's
  influence is a product decision and needs testing against every quiz path.

---

## RECENTLY SHIPPED (rolling, trim as it grows)

- Jul 27, 2026 (batch): STALE PROSE FIGURES + EM-DASH TARGET LIST. Six edits in five files
  through one idempotent `apply-batch.py`, marker-gated per edit rather than keyed to the old
  string being gone. Philadelphia `$234K` x2 -> `$237K`, New Orleans `$246K` -> `$248K`.
  `privacy.html` + `scouting-trip-workbook.html` added to `check_emdash`'s named list, one em
  dash converted on each. Gate: `PRE-DEPLOY GATE`, 0 failures / 0 warnings on a fresh clone,
  harnesses 18/18 and 10/10. Planted-error tested three ways, because a passing gate on a newly
  added target proves nothing on its own: a literal em dash planted in `privacy.html` fails, an
  ESCAPED `&mdash;` planted in the workbook fails (so the new targets run through
  `emdash_forms()`, not a literal scan), and a deliberately misspelled target name still trips
  the matched-no-file failure. Control run after each: 0/0.

- Jul 23, 2026 (second push): EM-DASH CHECK REBUILT + DB `Highlight` COLUMN DELETED (**v16_6**).
  `docs/CityDatabase_Jul_23_v16_5_highlights.xlsx` -> **`docs/CityDatabase_Jul_23_v16_6_nohighlight.xlsx`**;
  `DEFAULT_DB` and the SITE-OPERATIONS-LOG "Current:" line updated in the same commit, old file
  deleted before the gate ran.
  `check_emdash` counted ONE SPELLING of the character, so 85 escaped em dashes were live while the
  gate read 0. It now counts every rendering that reaches a reader: the literal character, `\u2014`,
  `&mdash;`, `&#8212;`, `&#x2014;`. Two of the 85 turned out to be regex character classes
  (`/[\u2013\u2014\-].*\$/`, twice in `pick-and-compare.html`), which are code doing the right thing,
  so whitespace-free bracket groups are excluded and named as a third deliberate exclusion alongside
  `<style>` and the short `'\u2014'` UI placeholder. Real count was 83, not 85.
  Converted: 61 on `pick-and-compare.html` and 22 in the JSON-LD of New Orleans, Philadelphia, Salt
  Lake City and St. Louis (4 of those were the `headline` separator, brought into line with the colon
  the other 44 profiles already use).
  The page conversion turned out to be already written. `index.html` was swept Jul 13 and
  `pick-and-compare.html` was missed, so the two surfaces had disagreed on 65 of 99 highlights ever
  since, silently. All 99 were synced from `index.html`, which is newer on every one of the 24 rows
  that differed by more than punctuation (the `median home` -> `typical home value` sweep, the Jul 12
  superlative sweep, and corrected figures for Boulder, Bentonville and New Orleans).
  The DB `Highlight` column is deleted rather than converted. It was a master nothing read: `load_db()`
  never touched it, no tool consumed it, no check validated it, and it disagreed with both surfaces.
  Deleting it also retired, at zero cost, the twelve banned dataset-scoped superlatives sitting in it
  (Fayetteville AR, Carmel-by-the-Sea CA, Santa Barbara CA, Vail CO, Delray Beach FL, Boise ID,
  Paducah KY, Beaufort NC, Johnson City TN, Corpus Christi TX, Jackson Hole WY, Burlington VT), plus
  Chattanooga's unanchored "Best value city in the Southeast", plus two cells that contradicted the
  `Median Home` in their own row (New Orleans $267K vs $250,000, Tulsa $245K vs $194,000).
  NEW CHECK: `check_highlight_surfaces`, in the `figures` group, fails when the same city's highlight
  differs between `index.html` and `pick-and-compare.html`, byte for byte. It is what makes "one
  record" true rather than aspirational, and it would have caught the em-dash gap on the day it opened.
  Tested: `tools/test_emdash_forms.py` NEW, 10/10 (escape form caught; `<style>` silent; short
  placeholder silent in both spellings; regex character class silent; prose beside a character class
  still caught; entity forms caught; a named target matching no file fails loudly).
  `tools/test_highlight_homes.py` extended to 18/18, with three plants for the new check. Its older
  assertions were retightened rather than loosened: a single-surface plant now legitimately trips two
  checks, so each assertion names what it expects from each.
  Column removed as inline strings in `xl/worksheets/sheet1.xml` and rezipped; no openpyxl, no pandas.
  Verified: every other zip part byte-identical, part order preserved, only `Highlight` gone,
  0 data cells changed outside it, `load_db()` output identical old vs new.
  Gate: `python3 tools/validate.py --local .` reads PRE-DEPLOY GATE, **0 failures, 0 warnings**.

- Aug 18, 2026: FOR-RETIREES VOCABULARY PASS shipped (BATCH). The Aug 17 Search Console read
  found the two largest comparison queries both say "for retirees" (tampa vs sarasota, 78
  impressions; tampa vs naples, 44) while zero comparison pages used the phrase in a description
  or subheading. All twenty-three comparison pages edited, titles deliberately untouched: meta
  description's single "for retirement" moved to "for retirees" (the retirement token survives
  in title and slug); the JSON-LD Article description moved with it on the five pages where it
  mirrors the meta byte for byte, and was left alone on the eighteen that carry independent
  schema copy; one subheading per page gained the phrase (newer template: the faq h2 now reads
  "X vs. Y for retirees: the questions people actually ask", the exact query shape; older
  template: "Side by side, scored for retirees."); dateModified bumped to 2026-08-18 on all
  twenty-three since schema and rendered content both moved. og and twitter descriptions
  untouched, judgment call: social surfaces, not ranking surfaces, most already carry distinct
  copy. Grade on impressions and position, not clicks, and not before October, per the
  measurement rule in ops log section 7. NEXT: tampa-vs-naples-retirement, the one true
  missing-page finding, as its own COMPARE session.
- Aug 17, 2026: STRATEGY SUPERSESSION, boarded late. On Aug 15 the operator asked where city
  profiles stood given weak traffic, and the answer given was that profiles are conversion
  inventory rather than acquisition pages, that 51 is enough, and that build energy should move
  to comparison pages, tools and pins. The operator acted on it: the tax tool and the affordability
  calculator both shipped after that conversation. The decision never reached this board. The
  three-week growth cycle boarded Aug 3, with its Wave 2 profile list, sat here looking current for
  two weeks and misled a later session into recommending profile builds that had already been
  called off. That is the third time a plan has lived only in a chat. THE WAVE 2 AND WAVE 3 PROFILE
  LISTS ARE SUSPENDED. They are not cancelled: build a profile when demand names it, not on a
  schedule. Everything else in the Aug 3 cycle stands, including the 80/20 split and the one-debt-
  day cap, with growth now meaning comparison pages, tools and pins.
- Aug 17, 2026 (second push): BATCH SESSION, four queue items resolved. (1) P1 SLUG RESOLUTION
  CLOSED: `check_comparison_scores` / `check_comparison_cost_rows` rewired through a shared
  `_comparison_row()` resolver (PUBLISHED_PROFILES -> (City, ST) -> db), every miss a loud
  failure; `burlington-vs-portland-me` checked for the first time and its two predicted
  `&ndash;` budget cells fixed to literal en dash in the same commit; harness
  `tools/test_comparison_slugs.py` (5 plants) registered. (2) DUPLICATE URL FORMS: two 301
  rules in `netlify.toml`, `/:page -> /:page.html` and `/cities/:slug/profile ->
  profile.html`; root-safe because `/:page` cannot match `/` and neither rule is forced, so
  existing files always win. Live curl checks after deploy: `/` 200, an extensionless
  comparison URL 301, its `.html` form 200. CORRECTED same day, measured live: the non-forced
  rules were shadowed by Netlify's native extensionless serving and never fired; replaced with
  three explicit `force = true` rules for exactly the three split pages, placeholders
  forbidden under force. (3) D2 DRIFT AUDIT: all 99 CITY_ENRICHMENT D2
  prose figures and all 99 `monthlyEst` fields brace-parsed and compared to DB `Monthly Est`;
  ZERO mismatches; the July 9 finding was repaired in the interim and `$4,500-$5,500` no
  longer appears anywhere. Closes the open D2-drift item. (4) ST. PAUL ITEM: stale twice over;
  the Jul 27 rebase already set the single figure `$301,000` (recorded further down this
  board) and the pre-rebase `$297,000` prescription is superseded. No DB change made.
  `urban-walkabout` vocabulary deliberately untouched per its own opportunistic-only rule.
- Aug 17, 2026: MATCHUP PILL PASS shipped, and FIRST FULL SEARCH CONSOLE READ.
  Two pushes. First, link-form conversion: 404 `?city=` links across 63 files converted to direct
  profile hrefs, zero-inbound profiles 12 -> 4. Second, curated matchup pills: 28 added across 19
  comparison pages under COMPARISON-PAGE-STANDARD-v2 item 6, no page over the four-pill ceiling.
  Every comparison page now has at least two peer inbound links; Burlington vs. Portland ME went
  0 -> 3, San Antonio vs. Fort Worth 0 -> 2, Fayetteville vs. Bentonville 0 -> 2, Naples vs. Fort
  Myers 0 -> 3, Sarasota vs. Tampa 3 -> 5. THE P4 BELOW IS CLOSED BY THIS: bloomington-vs-lexington
  now carries four pills, above the item 6 floor.
  The pill pass shipped WITHOUT a board or ops-log entry, against the same-commit rule. This entry
  is the retroactive fix and the reason the rule exists.
  The Search Console read (3 months to Aug 17, 8,974 impressions, 403 clicks) is written up in
  SITE-OPERATIONS-LOG section 7. The four findings that change priorities: the quiz page earns 64%
  of all site clicks at position 4.8; `urban-walkabout.html` draws 947 impressions and 1 click on
  Walk Score vocabulary it never meant to match; comparison pages are held back by POSITION, not by
  missing pages, so new pages are the wrong lever; and Google has indexed both URL forms for three
  pages, splitting them.
- Aug 16, 2026: LINK-FORM CONVERSION shipped. 404 city links across 63 files converted from
  `index.html?city=NAME&state=ST` (JS redirect via PUBLISHED_PROFILES, which crawlers do not
  execute) to direct `cities/<slug>/profile.html` hrefs. 218 links for cities with no profile yet
  were left on the ?city= form deliberately and are listed by the apply script. Effect on internal
  link graph: profiles with zero crawlable inbound links went 12 -> 4, and one-inbound went 22 -> 7.
  The four remaining zero-inbound pages are globetrotter-guide, wellness-blueprint, privacy, and
  scouting-trip-workbook, which are lead-magnet and utility pages rather than profiles. Zero broken
  internal links after conversion; PUBLISHED_PROFILES left in place so old inbound ?city= URLs and
  the quiz flow still resolve. Prompted by three pages sitting at "Discovered, currently not
  indexed" in Search Console; note that those three (Kansas City profile, Knoxville vs. Asheville,
  Knoxville vs. Nashville) already had 3, 5 and 6 inbound links, so this is not a targeted fix for
  them and may not move them. It removes a structural handicap on the 34 under-linked profiles.
- Jul 23, 2026: DB `Highlight` COLUMN RECONCILED. `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` ->
  **`docs/CityDatabase_Jul_23_v16_5_highlights.xlsx`**; `DEFAULT_DB` and the SITE-OPERATIONS-LOG
  "Current:" line updated in the same commit, old file deleted.
  Running the freshly shipped `HL_*` matcher over the column found **16 drifted home figures**, and
  it was a DIFFERENT 16 than the two HTML surfaces carried. The column was a pre-Jul-23 vintage: it
  still held every NRC citywide figure from before that sweep, including **Wilmington DE at $215K
  against a `Median Home` of $321,000** - the exact string used as the planted error in
  `tools/test_highlight_homes.py`, sitting live in the master the whole time. Also stale: Memphis
  $170K/$195K, San Antonio $260K/$320K, Philadelphia $270K/$240K, Pittsburgh $265K/$240K, St. Paul
  $280K/$297K, St. Louis $250K/$235K, Indianapolis $223K/$224K, Miami $430K/$575K, plus the six
  non-NRC cities and Provincetown.
  One extra fix in the same pass: Miami's cell opened "The only city in the database with all four
  major pro sports leagues" - a dataset-scoped superlative, banned since Jul 12, sitting in the
  master where a regen would have pushed it back onto the site. Now "A rare city with all four major
  pro sports leagues," matching both surfaces.
  Edited as inline strings in `xl/worksheets/sheet1.xml` and rezipped; no openpyxl, no pandas.
  Verified: every other zip part byte-identical, the other four sheets row-identical, `load_db()`
  output identical across old and new (so no score, monthly, home value or tier moved), exactly 16
  rows changed, exactly one column touched, and 0 drifted figures on the re-read.

- Jul 23, 2026: HIGHLIGHT HOME-FIGURE CHECK SHIPPED. `check_highlight_homes()` in
  `tools/validate.py`, folded into the `figures` group, **FAIL** not WARN. Holds every home figure in
  `highlight` prose to `Median Home` on both surfaces: `index.html` (JS object literals) and
  `pick-and-compare.html` (single-line JSON under `const CITIES =`), parsed separately because they
  are not the same format. Exact match, **no tolerance band** - a figure in thousands must equal
  `round(DB/1000)`. A band was the whole reason the nine hid: 3% forgives Casper's $275K against
  $273K and does not forgive Des Moines' $217K against $191K, and both are equally false.
  Scope is ANCHORED, not blanket: a figure counts only when attached to a home-value noun. That one
  rule keeps three legitimate shapes silent forever - the NRC neighborhood range, the cross-city
  reference (Tampa naming Naples' figure), and figures that are not homes at all (Tulsa's $465M
  Gathering Place, Traverse City's $132K deduction, Provincetown's $2M estate cliff). A cross-city
  veto sits behind the anchor for the day someone writes "Naples' median home is $585K" inside
  Tampa's string. Bounds are checked as bounds, not equalities.
  **16 failures on the unpatched tree, all real**, all reconciled to the DB in the same push:
  `index.html` 9 (Des Moines, Sioux Falls, Casper, Columbus, Roanoke, Miami, La Crosse, Boulder,
  Provincetown), `pick-and-compare.html` 7 (Des Moines, Columbus, Sioux Falls, Roanoke, Casper,
  La Crosse, Provincetown). Sioux Falls carried TWO DIFFERENT wrong figures, $333K on one surface and
  $285K on the other, against a DB $314,000. Roanoke's was a false BOUND, "median homes under $230K"
  against $251,000. Provincetown's $2.1M was resolved to $924K, which is what its own `D2` modal
  already said, sourced to Boston Globe / Warren Group April 2026 - so the $2.1M was simply wrong and
  the earlier $326K paste is already gone.
  Planted-error tested by `tools/test_highlight_homes.py`, 15 assertions, all passing. The plant is
  the bug that actually shipped: Wilmington DE's highlight at `$215K` against a DB `$321,000`, one
  failure, exit 1. Test 3 is the (City, ST) key guard - Wilmington NC carrying its own $418K must be
  silent AND Wilmington NC carrying DE's $321K must fail, which is only true if the lookup keys on
  state. That is the Jul 21 mistake, now mechanically prevented. Test 6 plants a renamed `CITIES`
  array and asserts the check fails LOUDLY rather than scanning nothing and reporting a clean site.
  Files: `tools/validate.py`, `tools/test_highlight_homes.py` (new), `tools/README.md`, `index.html`,
  `pick-and-compare.html`, this board. Validator 0 failures, 0 warnings, exit 0 on `--local .`.

- Jul 23, 2026: NRC HIGHLIGHT PROSE RECONCILED with `Median Home`. Recorded on this board as seven
  cities; the actual count was **nine** across **two** surfaces - the board omitted New Orleans and
  Tulsa, and the `pick-and-compare.html` surface it flagged had never been swept.
  `index.html`: 9 highlight figures, the Indianapolis $223K/$224K rounding, and the St. Louis
  stat-card `sub`, which read "Citywide $250K" while its own `methodologyNote` two lines below said
  $235,000. `pick-and-compare.html`: the same 9 figures, plus Indianapolis, Wilmington DE and
  St. Paul still holding pre-v1.2 retiree-target values in `medianHome` / `medianHomeMid` /
  `monthlyEst` (two stored as ranges, which v1.2 abolished). `medianHomeMid` drives the comparison
  sort, so Indianapolis had been sorting at $432,000 against a real $224,000 - that one corrupted
  output, not just copy. Also two $100 monthlyEst drifts (Burlington, Nashua). City profiles audited
  clean. Both patches idempotent with abort-on-miss; validator 0/0 exit 0 on `--local .`.
  **CORRECTION to the Jul 21 entry:** it listed Wilmington DE `Median Home` as $418,000, an apparent
  $203,000 gap. $418,000 is **Wilmington NC**. The measurement matched on city name without state.
  True DE figure is $321,000 and the real gap was $106,000. Two Wilmingtons in the DB, and two
  Columbuses - always key on (City, ST).

- Jul 21, 2026: SAN ANTONIO vs FORT WORTH comparison page shipped (page 20). Built from a live pull of
  `st-louis-vs-kansas-city-retirement.html`; all scores, Monthly Est, Median Home, tier, property tax
  and insurance read from `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` rows 73 and 75. Four files:
  the new page, `sitemap.xml`, `compare-retirement-cities.html` (new Texas hub region + ItemList
  position 20), and `cities/fort-worth/profile.html`.
  **Zero checkmarks on the whole table, and that is the finding, not an omission.** All ten dimensions
  are a tie or a one-point gap: five exact ties (D2, D3, D4, D6, D8), San Antonio +1 on D5/D7/D9/D10,
  Fort Worth +1 on D1. Cost rows are $20,000 and $200/mo apart with identical tier, property tax and
  insurance, so the two cost rows were left unmarked as well rather than manufacturing separation
  the data does not support. The D9 row is disclosed in prose as apples-to-oranges: San Antonio is
  scored on retiree-target areas (three of which are independent municipalities with their own police
  departments), Fort Worth citywide.
  Two deviations from the template, both deliberate: the climate row is labelled "Summer comfort
  (higher = milder)" rather than the template's inverted "Hot summers (lower = milder)", so the page
  does not propagate the known `knoxville-vs-chattanooga` label bug (both cities score 3, so it is
  invisible either way); and the caption carries a property-tax variance note because the DB ships the
  Texas state average while the San Antonio profile publishes a Bexar-specific 1.8%.
  `cities/fort-worth/profile.html`: Tulsa removed from the related-cities grid and replaced with San
  Antonio. Tulsa was the only one of the three with no live profile, so the card dead-ended at the
  matcher, and its `related-card-why` text was a verbatim duplicate of Memphis's. Kansas City's
  "The closest overall match" line was also rewritten, since San Antonio now holds that position.
  Deployed by drag-and-drop through the GitHub web UI rather than Codespaces, so `--local .` was not
  run as a pre-deploy gate; structural checks (tag balance, JSON-LD parse, sitemap XML, em-dash count,
  banned-superlative scan) were run on all four files before upload and the bare live validator was
  run after.
- Jul 21, 2026: PRE-EXISTING SUPERLATIVE FAIL CLEARED IN `cities/san-antonio/profile.html`. The bare
  live validator run after the comparison-page deploy returned 1 failure + 1 warning. Neither came
  from the deploy. The failure was the King William hood-card reading "the most genuinely urban option
  on this list", live since the Jul 19 San Antonio ship and never caught because live mode had not
  been run since. Rewritten to "the most genuinely urban of the four retiree-target areas here". The
  warning was this board asserting 19 comparison pages against 20 live, cleared by this update.
  **Process note: the Jul 19 board claims validator 0/0 confirmed on both `--local .` and bare. The
  bare run cannot have covered the San Antonio profile, or it would have failed then.** Worth
  distrusting that line and re-running bare mode before relying on any 0/0 claim on this board.
- Jul 19, 2026: SAN ANTONIO, TX SHIPPED. Profile 44. Built from a live pull of
  `cities/st-louis/profile.html`; all scores, Monthly Est and Median Home read from
  `docs/CityDatabase_Jul_13_v16_4_climate.xlsx` row 75. Carries an NRC callout (11th NRC city), a
  Visit block with live per-city Expedia and Vrbo codes, and the Visit chip wired into the scroll-spy
  ids array. No landing-page edits were needed: existing foodies and urban-walkabout cards already
  routed through `index.html?city=San Antonio&state=TX`, and `CITY_ENRICHMENT` plus the `cities[]`
  object already existed, so `index.html` took a single `PUBLISHED_PROFILES` line. The pre-publish
  rubric check caught a false UNESCO claim in the draft (see ops log).
- Jul 18, 2026: PROFILE FIGURE DRIFT AUDITED AND RECONCILED. 13 fixes across five city profiles. The audit was
  scoped to stat cards + FAQ JSON-LD and found 5 figures in 4 cities; reading each one IN CONTEXT before
  editing showed the scope was wider, and the failure was worse than "a stale schema field": three
  profiles CONTRADICTED THEIR OWN STAT CARD.
    - `columbus` 8 fixes. Stat card read `$235K` while EIGHT other places on the same page read `$249K`:
      meta description, og:description, JSON-LD Article description, two FAQ answers, hero tagline, a
      fit-list bullet, and a fast-fact box. The meta description is what Google shows in results, so
      the stale figure was the most publicly visible number on the page.
    - `st-louis` 2 fixes. FAQ `$250,000` and the "Reading the numbers here" callout `~$250K`; stat card
      already read `$235K`.
    - `tampa` 1 fix. FAQ `$377,000` -> `$400,000`. The Water Street hood-card range `$377K-$800K` is a
      NEIGHBORHOOD figure and was deliberately left alone.
    - `pensacola` 1 fix. Stat card Budget Score `7/10` -> `8/10` (DB D2 = 8).
    - `st-paul` 1 fix. Stat card Monthly Budget `$3.8-5K/mo` -> `$4.7-5.9K/mo`, already contradicted by
      its own FAQ, which read `$4,700 to $5,900`.
  In every case `index.html` and the DB agreed and the PROFILE was the stale side, so nothing in the
  matching engine was affected. Applied with an abort-on-count-mismatch batch. Verified: 0 leftovers of
  the old figures, JSON-LD parses on all five, 0 rendered em-dashes introduced, gate 0 failures /
  0 warnings, and both audit passes re-read zero. LESSON: the audit surface was too narrow. A figure
  that drifts drifts EVERYWHERE it was typed, including meta and og tags that no on-page read catches.

- Jul 18, 2026: PROS/CONS FIGURE CHECK PROMOTED WARN -> FAIL (`tools/validate.py`, one line plus its
  comment). Preconditions re-confirmed first: `--local .` on a fresh clone of main read 0 failures,
  0 warnings, so the Jul-15 reconciliation of 34 stranded figures is holding. Planted-error tested
  three ways: clean tree 0/0, a planted Knoxville `$327K` against DB `$368,000` produces
  `[FAIL] ... figures` and exit 1 (not a warning), revert returns to 0/0.

- Jul 18, 2026: QUIZ DIMENSION DESCRIPTIONS REFRAMED to name the desirable trait (5 of 10, `index.html`
  DIMENSIONS array only). The importance scale asks "how important is this to you?" against four shared
  labels, so a desc naming the neutral topic or the bad end does not parse: "Must Have ... disaster
  exposure" dangles. Fixed: Climate Resilience (`Disaster exposure, insurance cost & availability` ->
  `Low disaster risk, affordable and available insurance`), Airport Access (`Drive time to major hub,
  nonstop routes, airlines` -> `Flying easily from an airport nearby, or a major hub a short drive
  away`), Healthcare (`Hospital ratings...` -> `Top hospital ratings...`), Tax Friendliness (`...property
  tax burden` -> `Low to no tax on Social Security, income, and property`), Safety (`Violent and property
  crime rates by city` -> `Low crime and feeling safe day to day`). The other five already named the good
  version; Weather uses a different pattern. The Airport rewrite is also the RESOLUTION of the Georgetown
  question: Georgetown TX has no field of its own and leans on Austin (AUS) 35 min out, which felt like
  "drive far, then connect" but is not: AUS runs ~87 nonstops incl. direct to JFK/LGA, Boston, Charlotte,
  Atlanta, Miami, DCA/IAD, plus year-round London, Amsterdam, Frankfurt. Chose to name both the
  own-airport and hub-drive cases honestly rather than encode a proximity cap and re-score the
  drive-to-hub cities. Validator 0/0 pre-deploy. Ops-log writeup still to be added.

- Jul 15, 2026: PENSACOLA profile 3-fix correction shipped. (1) Removed a doubled figure in the
  character section (`a typical home of $264,000, a $264,000 median` -> single figure). (2) Fixed a
  stale FAQ monthly buried in the FAQPage JSON-LD (`$3,000` -> `$4,900`; DB `$4,900-$6,100`), invisible
  in prose. (3) Retired `Florida's lowest here` in all 5 spots (meta, og, JSON-LD, stat-sub, character):
  a rank scoped to the site via `here` that goes false the moment a cheaper FL city is added. Replaced
  with `well under Florida's peninsula prices` (panhandle vs peninsula, rot-proof). Verified live: 5x new
  phrase, 0 old rank, 0 stale figure, JSON-LD parses. Ops-log writeup still to be added.

- Jul 15, 2026: PROS/CONS FIGURE-DRIFT CHECK built + 34-CITY RECONCILIATION shipped. The board item
  assumed one stale figure (Knoxville `$327K`, already fixed). The check found 34: a third of the
  CITIES-array pros/cons home figures had drifted from the Jul-13 DB, in both directions (21 high, 13
  low), which reads as accumulated staleness across refreshes rather than one migration. Built into the
  `figures` group, anchored to home-value CONTEXT only, so monthly/bill figures, ranges, explicitly-
  `citywide` figures on high-variance cities, and cross-city comparison figures (`above Georgetown at
  $457K`) do not misfire; 0 false positives across all 99 cities. Shipped WARN, not FAIL, so the 34
  could be reconciled without red-lighting the gate. Reconciled with a two-pass scripted batch (audit
  all, then apply; abort if any anchor is missing or non-unique; re-run-safe), which caught a real
  anchor collision: Santa Barbara's STALE `$1.85M` equalled Jackson Hole's CORRECT `$1.85M`, resolved
  by quoting the anchor to the array literal. Deployed `index.html` (34 fixes) + `tools/validate.py`;
  live bare run reads 0 failures, 0 pros/cons warnings. FOLLOW-UPS now on the ACTIVE board: promote the
  check WARN->FAIL, and extend the same cross-check to profile stat cards + FAQ schemas. Ops-log writeup
  still to be added.

- Jul 15, 2026: WORKING-ENVIRONMENT CLARIFICATION logged in SITE-OPERATIONS-LOG.md (Section 9 +
  change log). Laurie works from a Mac laptop but the repo working tree lives in Codespaces at
  `/workspaces/retire-me-here`; all terminal, git, deploy, and file-management commands run there.
  Operator-facing instructions use bare Codespaces commands and paths, never Mac-local paths or a
  leading `cd`. Docs-only; no site or scoring impact.

- Jul 14, 2026: KNOXVILLE vs NASHVILLE comparison page shipped (page 19). Built from the
  `knoxville-vs-chattanooga` template against COMPARISON-PAGE-STANDARD-v2; scores/figures/tiers from
  `CityDatabase_Jul_13_v16_4_climate.xlsx`. Checkmarks at 2+ point gaps only (D1 Nashville; D7, D9
  Knoxville) plus the three cost rows. Also fixed a stale `index.html` figure: the Knoxville `pros`
  array read `$327K` while its own `medianHome` read `$368,000` (DB agrees $368K); corrected. Deploy
  hit and cleared a real gate failure: a session-start `index.html` copy, packaged whole, reintroduced
  five superlatives that live had been cleaned of in between; rebuilt on a fresh pull as a one-line
  diff. See SITE-OPERATIONS-LOG.md change log for the full note.

- Jul 14, 2026: `.lists-grid-four` UNDEFINED-CLASS BUG FIXED. Four profiles (`st-louis` the CANONICAL,
  `columbus`, `memphis`, `pittsburgh`) carried `class="lists-grid-four"` on the four-card container but
  never defined the rule, and had no base `.lists-grid` on the div to fall back on, so the cards stacked
  full-width instead of forming the centered 2x2. Added a self-contained `.lists-grid-four` rule (display
  grid, `repeat(2, minmax(0,340px))`, centered) to all four, matching the standalone form `st-paul`
  already used. Also added the mobile single-column collapse (`minmax(0,340px)` at max-width 768px) the
  build spec calls for, which no profile was enforcing: on a phone the 2-col grid was squeezing cards to
  ~151px instead of stacking. All 7 profiles that use the class now render identically: desktop 2x2,
  mobile 1-col. `new-orleans` and `philadelphia` were already correct via the two-class combo
  (`lists-grid lists-grid-four`) and needed no change. Nothing in the validator sees CSS, so this class
  of bug does not self-report; caught by audit. Verified with tag-balance; visual behavior reasoned from
  the grid track math, NOT rendered, so eyeball the 2x2 on one rebuilt profile after deploy to be sure.

- Jul 14, 2026: v1.3 TEMPLATE RETROFIT VERIFIED COMPLETE (was "NOT VERIFIED"). Checked against all 43
  profiles, not assumed: forced-dark hardening block 43/43; Visit chip present, in LAST nav position,
  and wired into the scroll-spy ids array 43/43; Deep Dive block correctly placed after Related Cities
  and before Visit 43/43; zero "N-question quiz" copy 43/43. The "comment em-dash cleanup" the old board
  carried as an open v1.3 task was never a deliverable: PROFILE-FORMATTING.md explicitly exempts them
  ("legacy comments carrying em-dashes are cosmetic only and do not require sweeping unless touched").
  219 remain in `<style>`/`<!-- -->` blocks across 36 profiles and are fine there. Rendered em-dashes
  across all 43 profiles: 0.
- Jul 14, 2026: CLOSER-VARIETY SWEEP RETIRED AS OBSOLETE. The item predated v1.4 and had the standard
  backwards. It flagged that the Visit blocks all end on "the highlight reel" as a defect. v1.4 makes
  that closer MANDATORY: "Test the daily routine, not the highlight reel" is the site's signature
  sign-off, "used on every block; it does not rotate." Verified 43/43 carry it verbatim, which is
  compliance, not drift. What the standard DOES require to vary is hooks and openers: 38/43 distinct
  hook openers, 42/43 distinct rental-line openers. The real residual is 4 templated hooks, now its
  own board item.

- Jul 14, 2026: SUPERLATIVE POLICY CLOSED OUT (4 batches). The 41 warnings were the wrong target:
  most were TRUE outside-world facts that should stay. But they formed a wall nobody reads, and false
  claims were hiding in it. Killed: Chattanooga "best value in the Southeast" (8th-cheapest SE city);
  Tampa "best value in Florida" (D2=6, four FL cities beat it, and our own Florida page already said
  Pensacola was cheapest); BOTH FAQPage schema answers wrong (Google can serve those as direct
  answers); St. Augustine claiming FOUR TIMES that "only Naples costs more" when Miami and Sarasota
  both exceed it; three stale D2 scores on comparison pages; "Lee Health #3 on our healthcare list"
  x6 (landing pages are alphabetical, not ranked - that rank never existed). Then 46 instances of
  "our database notes/calls/flags", which launders outside facts (US News rates NCH, not us) through
  a private spreadsheet the reader cannot open. **docs/SUPERLATIVE-LEDGER.md** now retires reviewed
  true claims so the warn queue sits at zero and a NEW claim shouts. See SITE-OPERATIONS-LOG.md
  2026-07-14.
- Jul 14, 2026: GUIDE EM-DASH SWEEP. 231 across all five guides, not the 64 first counted.
  `GUIDES_TOO = True`, planted-error tested. PROFILE-FORMATTING.md -> v1.5. The flag was never a
  decision: its comment claimed the guides were "grandfathered; see PROFILE-FORMATTING.md" and that
  doc grandfathers nothing. It was an unfinished job written in the grammar of a decision, which is
  why it went unquestioned for weeks. Also: all five guides said "Our database has 100." It has 99.
- Jul 14, 2026: VALIDATOR MODE BANNER. One command, two different jobs, nothing on screen saying
  which. Bare runs before a push grade the OLD site with NEW rules and report already-fixed failures;
  this misfired twice in one session. It now prints PRE-DEPLOY GATE or POST-DEPLOY CHECK at the top.

- Jul 13, 2026: Climate engine rebuild. Four compounding faults fixed: the cold dealbreaker was
  calibrated against the wrong scale (Boulder, 33F and 88in of snow, passed a "no freezing winters"
  filter); the `Climate Mild YR` column was actually the dryness score and the grey-winter filter was
  wired to it (removing Naples and Miami while keeping Pittsburgh); `mild` and `warm_dry` were weighted
  averages, so a great summer cancelled a freezing winter; and a `length >= 5` guard was silently
  failing open and discarding the climate filter entirely. Added NOAA 1991-2020 normals to all 99
  cities. DB v16.4. Zero score churn. See SITE-OPERATIONS-LOG.md 2026-07-13.
- Jul 13, 2026: Wilmington DE, Indianapolis and St. Paul median-home corrections confirmed live in both
  DB and index.html. MEDIAN-HOME-LABEL-CONVENTIONS.md deleted. D2 rebuild cleared the suspect
  `$4,500-$5,500` range (the one remaining instance is La Crosse WI's genuine DB value).
- Jul 14, 2026: VALIDATOR BLIND SPOT CLOSED. check_superlatives picked its targets from a
  hand-maintained list of filenames plus a hub regex matching only *-retirement.html. Anything not
  on that list shipped unchecked. privacy.html was never on it. Neither was a stray
  scottsdale-vs-santa-fe-PROFILE.html, which sat live on Netlify with FOUR banned superlatives and
  passed the gate clean. Local mode now discovers pages by globbing the disk: the filesystem is the
  only list that cannot drift from what actually ships. Planted-error tested with a brand-new
  unlinked page. The gate went from a false "0 failures" to a true 6, now cleared to 0.
- Jul 14, 2026: SCOTTSDALE vs SANTA FE deduplicated. Two files existed. The orphan (-profile.html,
  Jul 6) was NEWER and better than the live page (-retirement.html, Jun 22): proper favicon set, and
  a body that names the healthcare drop, the 3-of-10 safety, and wildfire directly. It was a rebuild
  saved under the wrong suffix that never replaced the original. Its body was promoted onto the live
  -retirement.html URL and **the orphan file was deleted with `git rm`**. A zip cannot express a
  deletion, so this step is easy to skip and it is the step that turns the new globbing validator from
  green to 4 failures. D2 scores corrected on the promoted page (Scottsdale 3->4, Santa Fe 6->5, both
  verified against CityDatabase_Jul_13_v16_4_climate.xlsx) and the D2 checkmark dropped, since 4 vs 5
  is a 1-point gap and the table rule is 2+. All dollar figures already matched the DB.
  SECOND PASS: promoting the orphan's body carried in three NEW dataset-scoped claims that the
  validator's literal phrase list does not match: "in the lower third of our 100-city database",
  "which our database records as", and "matched only by Miami and New Orleans among cities to score
  it". All three re-anchored before push. The lesson is below, under the validator item.
- Jul 14, 2026: FAVICON UNIFIED site-wide. 20 pages fixed: 14 carried an inline SVG data-URI, 6
  (privacy.html + Chattanooga, Delray Beach, Pensacola, St. Augustine, St. Petersburg) had none at
  all. All 84 pages now carry the real favicon set exactly once. Verified post-merge: 84/84 pages
  carry `/favicon.ico`, zero pages carry it twice, zero data-URI stragglers remain. Diff-reviewed:
  the batch touched only favicon markup. The 9 asset files were already in the repo root.
- Jul 14, 2026: SAVANNAH, GA profile shipped. No pillar city (nothing scores 9+); built on the
  D2 Budget 8 / D10 Community 8 cluster, with Safety 4 and Resilience 3 stated in the character
  section rather than buried. Carries an NRC callout under MEDIAN-HOME-METHODOLOGY v1.2 (citywide
  $326K vs retiree-target hoods $500K-$790K) despite not being one of the ten legacy NRC cities.
  Savannah is on TWO lists (arts-lovers, budget); it is a documented near-miss on foodies.
  Built with `lists-grid` (2 cards), not `lists-grid-four`: see the undefined-class bug below.
  OPEN: DB scores Savannah D1=5, but SAV runs 38 nonstops on 9 airlines, which the rubric's own
  anchors put at 6-7. Score NOT changed; prose written consistent with a 5. Worth a D1 review.
- Jul 14, 2026: Visit-block rollout COMPLETE. All 43 live profiles carry a Visit block.
- Jul 9, 2026: Knoxville deployed; v1.3 canonical + docs deployed; St. Paul DB fix done.

---

## CLOSED WORK -> docs/TASKBOARD-ARCHIVE.md

27 completed `## CLOSED` sections were moved to
`docs/TASKBOARD-ARCHIVE.md` so this board holds only what is in flight,
what is next, and what is parked -- which is what its purpose statement says.

Nothing was deleted. Every shipped item is still recorded three times: the
Last-updated ladder at the top of this file, the full section in the archive,
and section 7 of `SITE-OPERATIONS-LOG.md`.

`check_docs` reads only `TASKBOARD.md`, so the archive is invisible to the
gate and no validator change was needed. When closing an item from now on,
write the CLOSED section straight into the archive and leave a one-line
entry in the ladder here.
