# RETIREMEHERE TASKBOARD

**Purpose:** single source of truth for what is in flight, what is next, and what is parked.
Chats are disposable; this doc is not. Read it at the start of a work session, update it at the end.
When a job moves, edit the line here (or ask Claude to). If it is not on this board, it is not tracked.

**Last updated:** July 9, 2026 (deploy queue cleared; St. Paul done; all 27 Visit-block codes in hand)

---

## How to run chats

One job type per chat. Name chats so they are findable:

| Chat name pattern | For | Lifespan |
|---|---|---|
| `BUILD - <City>` | one city profile, end to end (DB -> brief -> build -> photos -> deploy pkg) | dies when the city ships |
| `COMPARE - <A> vs <B>` | one comparison page | dies when it ships |
| `BATCH - <job>` | repo-wide scripted operations (retrofits, sweeps) | dies when the batch is pushed |
| `OPS - planning & tracking` | this board, decisions, methodology Qs, small one-off fixes | permanent home base |

Rules of thumb:
- A NEW city's Visit block + affiliate codes belong IN that city's `BUILD` chat. That is part of the build, not a separate job.
- RETROFITTING existing profiles (Visit blocks, template changes, closer variety) is a `BATCH` job, never woven into a single city build.
- If a chat shows a "conversation compacted" note, finish the current step, update this board, and start a fresh chat.

---

## ACTIVE - city profile builds

- **Knoxville** - DEPLOYED (profile, photos, index.html, sitemap.xml all pushed). Only remaining: reciprocal landing-page cards (see Parked).
- **Next in queue** (order set by comparison strategy): Fort Collins -> Prescott -> San Antonio.

Live profiles: 38 (37 + Knoxville).

---

## ACTIVE - comparison pages

Live: 14. Unlocked and ready to build now (both cities live):
- **Knoxville vs Chattanooga** (next up)
- Knoxville vs Nashville
- Knoxville vs Asheville

Unlocks pending a build:
- Fort Collins vs Boulder (needs Fort Collins)
- Arizona three-way cluster (needs Prescott)
- Fort Worth vs San Antonio (needs San Antonio)

---

## ACTIVE - batch / site-wide operations

**Do these in this order.** The mechanical retrofit is unblocked and pure-script; the Visit-block rollout is gated on codes and needs bespoke per-city copy.


- **v1.3 template retrofit** - apply to the 36 existing profiles: dark-mode hardening, Deep Dive block relocation, plain-quiz wording, comment em-dash cleanup. Visit chip + `'visit'` id only where a Visit block already exists (~12). Idempotent script + `--dry-run`. NOT STARTED.
- **Visit-block + affiliate rollout** - UNGATED. All codes are now in hand: 27 cities, both Expedia + Vrbo, saved as `visit-affiliate-codes.csv` (add to project knowledge). This is NOT a mechanical script: each block needs 2 bespoke paragraphs (city hook; neighborhoods + hospital + rotating closer) pulled from that city's live profile, plus its 2 codes + Visit chip + `'visit'` id. Best run in WAVES (~6-9 cities per BATCH chat) with review, not one giant pass. Two flags: (a) St. Louis is in the code list but is also the canonical clone source - decide whether it gets a live Visit block, and if so make the skill REPLACE rather than ADD so clones do not double-insert; (b) Wilmington DE is NOT in the code list - confirm whether it needs one.
- **Closer-variety sweep** - the ~12 existing Visit-block profiles all end on "highlight reel." Reassign varied closers from the skill's rotating set. Fold into the v1.3 retrofit script.

---

## DEPLOY QUEUE (built, awaiting push to GitHub)

(empty - all July 9 items deployed)

---

## PARKED / BACKLOG

- Reciprocal landing-page cards for Knoxville (Budget, Hikers, Sports Fans list pages)
- Site-wide bolding pass (PROFILE-FORMATTING item 6, judgment-based, not batchable)
- Booking.com affiliate (Awin) - applied; deploy deferred until Expedia fully verified
- Pinterest save-rate optimization (ongoing; cadence + pin copy)

---

## RECENTLY SHIPPED (rolling, trim as it grows)

- Jul 9, 2026: Knoxville deployed; v1.3 canonical + docs deployed; St. Paul DB fix done and current DB uploaded to repo
- Jul 9, 2026: v1.3 template + docs rollout authored (canonical, PROFILE-FORMATTING, skill); Visit closer made a rotating set
- Jul 9, 2026: Knoxville profile completed (photos, dark-mode, Deep Dive placement, quiz wording, affiliate codes)
