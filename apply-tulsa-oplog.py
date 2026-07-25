#!/usr/bin/env python3
"""
apply-tulsa-oplog.py  --  RetireMeHere: Tulsa ops-log entry + build hand-off standard.

Run from the repo root, after `git pull`:

    git pull
    python3 apply-tulsa-oplog.py
    python3 tools/validate.py --local .
    git status
    git add -A
    git commit -m "Ops log: Tulsa profile 46; cheatsheet v1.1 build hand-off standard"
    git push
    rm apply-tulsa-oplog.py

Edits two files, no whole-file copies:
  1. docs/SITE-OPERATIONS-LOG.md   new change-log entry, inserted above the Roanoke entry
  2. docs/DEPLOY-CHEATSHEET.md     new section 4, old 4 through 8 renumbered 5 through 9,
                                   full-deploy block gains the apply-script step, v1.0 -> v1.1

Idempotent. Refuses to write anything at all if any anchor has moved.
Delete after use; it is not meant to be committed.
"""

import os
import sys

OPS_ANCHOR = "### 2026-07-24 - Roanoke, VA profile; four stale index.html figures fixed en route"

OPS_ENTRY = '### 2026-07-24 (second push) - Tulsa, OK profile; a closed museum caught pre-publish; build hand-off format standardized\n\n**Shipped.** `cities/tulsa/profile.html`, profile 46, plus hero/detail/lifestyle photos. Built from a\nlive pull of the canonical `cities/st-louis/profile.html`. All dimension scores, `Monthly Est`, and\n`Median Home` read from `docs/CityDatabase_Jul_23_v16_6_nohighlight.xlsx` row 96 (D1 7 / D2 9 / D3 8 /\nD5 7 / D6 5 / D7 5 / D8 6 / D9 7 / D10 8, D4 Resil 4, Range 1, $4,200-$5,300/mo, $194,000). Research\nused only for supporting color: Saint Francis and Ascension St. John credentials, Gilcrease\nconstruction status, Route 66 centennial dates, Oklahoma retirement-tax rules.\n\n**Emphasis brief.** One pillar at 9 (D2 Budget) with D3 Health and D10 Community both at 8 and\nD1/D5/D9 at 7. MULTI-STRENGTH, not MULTI-PILLAR, so the hero leads with value and the\nculture-plus-healthcare cluster carries real weight in the character section rather than fading behind\nthe price story. The hard-flagged counterweight is D4 Resilience at 4, Tornado Alley, which leads the\n"Skip if" column alongside summer heat (`Climate Hot Sum` 3, HEAT 8).\n\n**Bug caught pre-publish: a museum that has been closed for five years.** The first draft listed\nGilcrease Museum among Tulsa\'s open institutions, which is what `top-cities-for-arts-lovers.html` shows\non its Tulsa card and what `docs/arts-lovers-cities-scoring-analysis.md` lists in the Tier 2 rationale.\nGilcrease has been closed since 2021. Its replacement building now opens spring 2027, a year later\nthan planned and roughly 70% over budget at $140.9M total. Corrected before publish: the profile\ntreats it as under construction with a dated reopening. **Consequence: a landing-page card and a\nscoring-analysis doc record why a city earned a tier, not whether each named institution is currently\nopen.** Institution status is a live fact and needs checking at build time, the same lesson as the\nJuly 19 San Antonio UNESCO claim, one level further out.\n\n**NRC callout added off-list.** Citywide `Median Home` $194,000 against retiree-target neighborhoods\nat $300K-$500K, with the Maple Ridge mansion blocks past seven figures. MEDIAN-HOME-METHODOLOGY.md\nv1.2 treats the Neighborhood Reality Check as a universal editorial mechanism rather than a fixed\nlist, so the callout was added and approved. Tulsa is the twelfth NRC city. `PROFILE-FORMATTING.md`\nstill says ten and is now two behind, San Antonio having made eleven on July 19.\n\n**Superlative handling: copy tightened before the ledger, not instead of it.** The Saint Francis bed\ncount fired three UNREVIEWED warnings for one fact, across the health card, a fit bullet, and the\nJSON-LD FAQ. Rather than ledger the same claim three times, the vague hedge "among the largest in the\ncountry" was replaced with the sourced figure "the 11th largest in the nation", and the redundant\nthird mention was cut from the fit bullet. Two ledger rows remain, both TRUE, evidenced to Saint\nFrancis Health System and the Premier 15 Top Health Systems 2025 study. **The ledger is for claims\nthat cannot be improved, not for claims that have not been edited yet.**\n\n**Affiliate codes live.** Expedia `TtKUzzx`, Vrbo `W5AR3HO`, from the operator\'s\n`visit-block-affiliate-codes.numbers`, both with `rel="sponsored nofollow"`. Note the sheet has blank\nState cells on its last four rows (Tulsa, Virginia Beach, Iowa City, Carmel); the codes themselves are\nin the correct columns, verified by cross-checking the St. Louis row against the live St. Louis\nprofile.\n\n**Build hand-off format standardized.** The operator flagged that consecutive build chats deliver\ntheir files in different shapes, which is true and was costing a rename step or a wrong-folder drop\neach time. Reviewing `roanoke-deploy.zip` against this build: that zip carried whole copies of\n`index.html` (674K), `sitemap.xml`, `best-places-to-retire-on-a-budget.html`, `TASKBOARD.md`,\n`SUPERLATIVE-LEDGER.md`, and `SITE-OPERATIONS-LOG.md`, against section 4a. All six happened to be\nbyte-identical to live main, so nothing was reverted, but that is the empty-window case rather than a\nsafe method. The July 14 Knoxville near-miss is the same pattern caught only because the reverted\ncontent was itself a hard-FAIL class; a whole-file zip that reverts a corrected photo credit or a\nreciprocal link ships silently. Tulsa shipped instead as a new-files-only bundle plus an idempotent\npatch script (`apply-tulsa.py`) holding every edit to an existing file, each guarded by an exact\nanchor match that refuses to write if the file has drifted. Standard now recorded in\nDEPLOY-CHEATSHEET.md section 4. **New files arrive in a zip already in their final repo paths; every\nexisting file is edited by script, never shipped as a copy.**\n\n**Found, boarded, NOT fixed here.** `top-cities-for-arts-lovers.html` lists Gilcrease on the Tulsa\ncard as an open institution. `index.html` enrichment gives Tulsa `PropTax` 0.77% against the DB 0.79%.\n`PROFILE-FORMATTING.md` NRC list is two cities behind. Tulsa\'s detail photo is a placeholder pending a\nbetter vertical. Tulsa\'s `pick-and-compare.html` D2 of 7 against the DB 9 is one of the 72 stale D2\nscores already boarded on July 23, not a new finding.\n\n**Landing pages.** `top-cities-for-arts-lovers.html` already carried a live Tulsa card.\n`best-places-to-retire-on-a-budget.html` carried Tulsa as a `coming-soon` div, promoted to a live\nlink. No other landing page needed editing.\n\n**Gate.** `python3 tools/validate.py --local .` reads PRE-DEPLOY GATE, 0 failures, 0 warnings,\nverified end to end on a fresh `--depth 1` clone with the patch script applied before hand-off, not\nonly on the build machine. Bare post-deploy run confirmed 0 failures, 0 warnings after the push.\n\n**Files changed.** `cities/tulsa/profile.html` (new), three photos (new), one `PUBLISHED_PROFILES`\nline in `index.html`, one url block in `sitemap.xml`, one card in\n`best-places-to-retire-on-a-budget.html`, `SUPERLATIVE-LEDGER.md`, `TASKBOARD.md`,\n`SITE-OPERATIONS-LOG.md`, `DEPLOY-CHEATSHEET.md`.\n\n'

CS_SECTION = '---\n\n## 4. What a build chat hands you, and what you do with it\n\nEvery build chat delivers the same two things in the same shape. If a chat gives you something else,\nit is the chat that is wrong, not you.\n\n**A zip, containing only files that do not exist in the repo yet**, already in their final paths:\n\n```\ncities/tulsa/profile.html\ncities/tulsa/hero.jpg\ncities/tulsa/detail.jpg\ncities/tulsa/lifestyle.jpg\ndocs/DEPLOY-tulsa.md\napply-tulsa.py\n```\n\nFinal paths and final names. No `tulsa-hero.jpg` to rename by hand, no folder to create. Unzip at the\nrepo root and everything lands where it belongs.\n\n**A patch script, `apply-<city>.py`, holding every edit to a file that already exists.** Typically\n`index.html`, `sitemap.xml`, a landing page, `TASKBOARD.md`, `SUPERLATIVE-LEDGER.md`. It runs from the\nrepo root, it is idempotent, and it refuses to write anything at all if any anchor text has moved.\n\nThen the deploy is the same eight lines for every city:\n\n```bash\ngit pull                                  # first, always\nunzip -o tulsa-bundle.zip                 # new files land in final paths\nrm tulsa-bundle.zip\npython3 apply-tulsa.py                    # edits the existing files\npython3 tools/validate.py --local .       # the gate. 0 failures or stop.\ngit status                                # does the count match what you expect?\ngit add -A && git commit -m "Tulsa OK profile (46); budget card live; ledger + taskboard"\ngit push\nrm apply-tulsa.py                         # one-time script, never committed\n```\n\n### Why the existing files are not in the zip\n\nBecause of section 4a, and because of what happened on July 14. A build chat pulls `index.html` at the\nstart of a session and hands it back an hour later. Anything that landed in between is silently\nreverted when you unzip the older copy over your pulled tree.\n\nThe July 14 Knoxville deploy did exactly that and reintroduced five dataset-scoped superlatives that\nhad been cleaned from live `index.html` in the interim. The gate caught it, with 5 errors, **but only\nbecause those five were a hard-FAIL class.** A whole-file zip that reverts a corrected photo credit, a\nrewritten blurb, or a reciprocal link reverts it silently and ships. The validator has no idea it was\never different.\n\nA patch script cannot do this. It changes one line and fails loudly if the surrounding text is not\nwhat it expected.\n\n**So: if a chat hands you a zip with `index.html` in it, do not unzip it.** Ask for a patch script\ninstead. This is not a preference. It is the rule in section 4a with the mechanics attached.\n\n---\n\n'

CS_OLD_FULL = 'git status                                # 3. does Git see what you expect, and nothing else?\npython3 tools/validate.py --local .       # 4. exit 0 or stop\ngit add <the files you meant>             # 5. stage deliberately\ngit commit -m "<what changed and where>"  # 6. snapshot it\ngit push                                  # 7. ship\n                                          # 8. watch the Netlify deploy log\n                                          # 9. verify live in an incognito window\npython3 tools/validate.py                 # 10. optional: confirm against live\n                                          # 11. log it in ops log section 7'

CS_NEW_FULL = 'python3 apply-<city>.py                   # 3. edits to existing files, if the build sent one\ngit status                                # 4. does Git see what you expect, and nothing else?\npython3 tools/validate.py --local .       # 5. exit 0 or stop\ngit add <the files you meant>             # 6. stage deliberately\ngit commit -m "<what changed and where>"  # 7. snapshot it\ngit push                                  # 8. ship\n                                          # 9. watch the Netlify deploy log\n                                          # 10. verify live in an incognito window\npython3 tools/validate.py                 # 11. optional: confirm against live\n                                          # 12. log it in ops log section 7'

OPS = "docs/SITE-OPERATIONS-LOG.md"
CS = "docs/DEPLOY-CHEATSHEET.md"

EDITS = [
    (OPS, OPS_ANCHOR, OPS_ENTRY + OPS_ANCHOR,
     "### 2026-07-24 (second push) - Tulsa, OK profile"),

    (CS, "---\n\n## 4. Which validator command, and why it matters",
     CS_SECTION + "## 5. Which validator command, and why it matters",
     "## 4. What a build chat hands you"),

    # renumber from the bottom up so no heading is rewritten twice
    (CS, "## 8. Full deploy, start to finish", "## 9. Full deploy, start to finish",
     "## 9. Full deploy, start to finish"),
    (CS, "## 7. Rules that live above this document", "## 8. Rules that live above this document",
     "## 8. Rules that live above this document"),
    (CS, "## 6. When it goes wrong", "## 7. When it goes wrong", "## 7. When it goes wrong"),
    (CS, "## 5. Commit messages", "## 6. Commit messages", "## 6. Commit messages"),

    (CS, CS_OLD_FULL, CS_NEW_FULL, "# 12. log it in ops log section 7"),
    (CS, "Steps 3 and 4 are the two you will be tempted to skip.",
     "Steps 4 and 5 are the two you will be tempted to skip.",
     "Steps 4 and 5 are the two you will be tempted to skip."),
    (CS, "DEPLOY-CHEATSHEET.md v1.0 \u00b7 July 14, 2026",
     "DEPLOY-CHEATSHEET.md v1.1 \u00b7 July 24, 2026",
     "DEPLOY-CHEATSHEET.md v1.1"),
]


def main():
    if not os.path.isfile("index.html") or not os.path.isdir("docs"):
        sys.exit("Run this from the repo root (index.html and docs/ must be here).")

    planned, skipped, missing, cache = [], [], [], {}

    for path, old, new, marker in EDITS:
        if not os.path.isfile(path):
            missing.append(path + ": file not found")
            continue
        if path not in cache:
            cache[path] = open(path, encoding="utf-8").read()
        text = cache[path]
        if marker in text:
            skipped.append(path + ": already applied (" + marker[:46] + "...)")
            continue
        n = text.count(old)
        if n != 1:
            missing.append(path + ": anchor found " + str(n) + " times, expected 1. "
                           "File has drifted. Anchor: " + repr(old[:60]))
            continue
        cache[path] = text.replace(old, new, 1)
        planned.append(path + ": patched")

    if missing:
        print("STOPPED. Nothing written.\n")
        for m in missing:
            print("  [FAIL]", m)
        print("\nRe-pull main, or hand the drifted file back for a fresh diff.")
        sys.exit(1)

    for path in {p for p, *_ in EDITS}:
        open(path, "w", encoding="utf-8").write(cache[path])

    for line in planned:
        print("  [OK]  ", line)
    for line in skipped:
        print("  [SKIP]", line)

    print("\nNext: python3 tools/validate.py --local .   (expect 0 failures, 0 warnings)")


if __name__ == "__main__":
    main()
