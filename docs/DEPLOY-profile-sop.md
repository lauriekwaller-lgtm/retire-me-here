# DEPLOY: profile build SOP into the repo, skill cut to a stub

**Built:** August 26, 2026
**Depends on:** `apply-nc-tax-and-docs.py` must be deployed FIRST
**Gate:** 0 failures, 0 warnings on a fresh clone with both bundles applied

Docs only. No code, no site change, no profile.

---

## 1. Order, and what happens if you get it wrong

This bundle anchors on the board and ops-log entries the NC tax commit writes. Run it
first and it aborts, writes nothing, and tells you why. Verified: run out of order it
exits 1 with three named missing anchors and the line "Deploy that first; this script
depends on it."

```bash
# after the NC tax commit is pushed
git pull
unzip -o profile-sop-bundle.zip
rm profile-sop-bundle.zip
python3 apply-profile-sop.py --check
python3 apply-profile-sop.py
python3 tools/validate.py --local .
rm apply-profile-sop.py
git status --short --untracked-files=all
git add -A && git commit -m "docs/PROFILE-BUILD-SOP.md: profile build SOP consolidated into the repo; skill reduced to a stub; entry-point pointers on three docs"
git push
```

Expect **2 untracked** (`docs/PROFILE-BUILD-SOP.md`, `.claude/skills/retiremehere-city-profile/SKILL.md`)
plus this doc, and **5 modified**.

**THEN, and only then, paste the stub into the skill editor.** The stub points at a
doc that has to already be on `main`. Paste it before pushing and the next build
follows a pointer to a 404. The text to paste is
`.claude/skills/retiremehere-city-profile/SKILL.md` from this bundle.

---

## 2. What was actually decided, and why

**The skill was not moved into the repo, because it cannot be.** App skills load from
Claude's skill storage, not from a GitHub path. The repo cannot be the loader for the
copy you use in these sessions.

**So the content moved instead, and the skill became a pointer.** `SKILL.md` goes
from 258 lines to about 30 and owns nothing: no DB filename, no pixel dimensions, no
`/10` rule, no delegation table, no thresholds. It still rots, but there is nothing
in it left to rot.

That is the whole fix. Every profile defect this month traced to a restated fact
going stale in a copy outside the repo:

| Defect | What it cost |
| --- | --- |
| Superseded hand-off shape | three builds shipped in the wrong shape |
| DB filename two versions stale | a build would have read the wrong spreadsheet |
| Flat "never display a /10" | scores stripped from the Raleigh FAQ, against the canonical |
| A `Highlight` column that does not exist | a build step pointed at nothing |

None was a misunderstanding of a rule. All four were convenience copies.

**A copy of the stub is committed** at `.claude/skills/retiremehere-city-profile/SKILL.md`.
Claude Code loads project skills from `.claude/skills/` in the start directory and in
every parent up to the repo root, so a Claude Code session started anywhere in the
Codespace picks it up from the repo, version-controlled and diffable. Costs nothing
if you never use Claude Code. No `.claude/` directory existed before this commit, so
nothing was overwritten.

---

## 3. What `docs/PROFILE-BUILD-SOP.md` owns

Only what nothing else owned:

- The brief: pillar and support thresholds, hard flags, MULTI-PILLAR and
  MULTI-STRENGTH, the tuning constants
- **The per-surface score-display table.** No on the stats bar and in body prose, Yes
  on the healthcare card and in FAQ answers. This is the P3 that has been reopened on
  every build since June, now written down once with the reasoning
- Photo specs, the sourcing standard, and "write the caption to the photo"
- The live-canonical rule and the known stale-template regressions
- Build order, and the file list a new profile changes
- Apply-script discipline, including the insertion-shaped idempotence trap

It delegates ten subjects by name, and flags two docs that look like owners and are
not: `city-profile-template-spec.md` (nine dimensions, a pull-quote
`PROFILE_CONVENTIONS.md` removed) and `DEPLOY-CHECKLIST.md` (a May snapshot).

It also carries the two habits this month taught, in section 8: count causes rather
than failure lines, and grepping one string is not enumerating a subject.

---

## 4. Edits to existing files

| File | Edit |
| --- | --- |
| `docs/CITATION-RECIPE-city-profiles.md` | photo bullet now delegates to the SOP instead of carrying a third copy of the specs |
| `docs/PROFILE_CONVENTIONS.md` | entry-point pointer at the top |
| `docs/PROFILE-FORMATTING.md` | entry-point pointer at the top |
| `docs/TASKBOARD.md` | eleventh entry |
| `docs/SITE-OPERATIONS-LOG.md` | change-log entry |

The two pointers exist so a build that lands on a subject doc first gets routed to
the SOP rather than treating one subject as the whole procedure. That is the exact
mistake the August 25 build made with `PROFILE_CONVENTIONS.md`, in reverse.

---

## 5. Dropped on purpose

A validator check failing the gate if the skill file restates repo facts. Offered
earlier, then withdrawn: a 30-line stub that owns nothing has nothing to restate, so
the check would guard an empty room, and the planted-error harness would cost more
than the defect it prevents. Reopen only if the stub starts growing.
