# Deploy Cheatsheet

**Purpose:** The Codespaces deploy loop, written to be followed without help.
**Audience:** The operator, at 11pm, having not deployed in three weeks.
**Owner:** Laurie Waller
**Created:** July 14, 2026

Companion to SITE-OPERATIONS-LOG.md. The SOPs in section 6 of that document tell you *what* to change
for each kind of job. This document tells you *how to get the change onto the live site* once you have
made it. The mechanics below are identical for every job.

---

## 1. The only mental model you need

Git has three places your file can be. A deploy walks it through all three.

| Place | What it means | How the file gets there |
|---|---|---|
| **Working directory** | The file on disk in Codespaces. | You drag it in, or edit it. |
| **Staging area** | "These are the changes I mean to save." | `git add` |
| **Commit** | A permanent, named snapshot with your message on it. | `git commit` |

Then `git push` sends your commits up to GitHub. Netlify watches GitHub and deploys automatically.

**The step everyone skips is `git add`.** Dropping a file into Codespaces does not tell Git anything.
Git sees a changed file sitting there and waits for you to say whether you meant it. Until you `add`
and `commit`, there is nothing for `push` to send, which is why it feels like nothing happened.

**`git status` tells you which of the three places you are in.** It is free, it changes nothing, and
it is written in plain English. Run it constantly. It is the single habit that ends the need to ask
anyone how this works.

---

## 2. The loop: one file or a few files

This is the everyday case. Editing a doc, fixing one profile, updating the sitemap.

```bash
git pull                                  # 1. get current with GitHub, always first
                                          # 2. drag your file into the right folder
git status                                # 3. confirm Git sees exactly what you expect
python3 tools/validate.py --local .       # 4. the gate. exit 1 means stop.
git add docs/SITE-OPERATIONS-LOG.md       # 5. name the files you meant to change
git commit -m "Ops log: enumeration rule and session start gate"
git push                                  # 6. ship. Netlify takes it from here.
```

Netlify deploys on its own. Watch the deploy log, then check the live page in an incognito window so
you are not looking at your own browser cache.

---

## 3. The loop: a batch of files from a zip

For bulk profile edits. Same bones, one extra step. Full version is SOP-5 in the ops log.

```bash
git pull
                                          # drag the bundle zip into the file panel
unzip -o bundle.zip                       # -o overwrites in place, no prompts
rm bundle.zip                             # do not commit the zip
git status                                # does the changed-file count match what you expect?
git diff cities/savannah/profile.html | head -30    # spot-check one diff
python3 tools/validate.py --local .
git add cities/
git commit -m "Batch: Visit blocks across 12 profiles"
git push
```

The `git status` count check is the whole point of doing it this way. If you expected 12 changed files
and Git says 47, something in the zip was built wrong. Find out before you commit, not after.

---

## 4. What a build chat hands you, and what you do with it

Every build chat delivers the same two things in the same shape. If a chat gives you something else,
it is the chat that is wrong, not you.

**A zip, containing only files that do not exist in the repo yet**, already in their final paths:

```
cities/tulsa/profile.html
cities/tulsa/hero.jpg
cities/tulsa/detail.jpg
cities/tulsa/lifestyle.jpg
docs/DEPLOY-tulsa.md
apply-tulsa.py
```

Final paths and final names. No `tulsa-hero.jpg` to rename by hand, no folder to create. Unzip at the
repo root and everything lands where it belongs.

**A patch script, `apply-<city>.py`, holding every edit to a file that already exists.** Typically
`index.html`, `sitemap.xml`, a landing page, `TASKBOARD.md`, `SUPERLATIVE-LEDGER.md`. It runs from the
repo root, it is idempotent, and it refuses to write anything at all if any anchor text has moved.

Then the deploy is the same sequence for every city:

```bash
git pull                                  # first, always
unzip -o tulsa-bundle.zip                 # new files land in final paths
rm tulsa-bundle.zip
python3 apply-tulsa.py                    # edits the existing files
python3 tools/validate.py --local .       # the gate. 0 failures or stop.
rm apply-tulsa.py                         # BEFORE git add, or it gets committed
git status                                # does the count match what you expect?
git add -A && git commit -m "Tulsa OK profile (46); budget card live; ledger + taskboard"
git push
```

### Why the existing files are not in the zip

Because of section 4a, and because of what happened on July 14. A build chat pulls `index.html` at the
start of a session and hands it back an hour later. Anything that landed in between is silently
reverted when you unzip the older copy over your pulled tree.

The July 14 Knoxville deploy did exactly that and reintroduced five dataset-scoped superlatives that
had been cleaned from live `index.html` in the interim. The gate caught it, with 5 errors, **but only
because those five were a hard-FAIL class.** A whole-file zip that reverts a corrected photo credit, a
rewritten blurb, or a reciprocal link reverts it silently and ships. The validator has no idea it was
ever different.

A patch script cannot do this. It changes one line and fails loudly if the surrounding text is not
what it expected.

**So: if a chat hands you a zip with `index.html` in it, do not unzip it.** Ask for a patch script
instead. This is not a preference. It is the rule in section 4a with the mechanics attached.

### Images, and anything else a script cannot diff

A patch script can edit HTML and markdown. It cannot edit a JPEG. Photos and other binaries are
always dragged, never patched.

**Drag them to the repo root, then move them with one line.** Never into a nested folder, never
hand-renamed first:

```bash
mv tulsa-detail.jpg cities/tulsa/detail.jpg
```

Dropping a file into the Explorer puts it wherever you release the mouse, and the root is the
easiest place to hit by accident. A hand-rename plus an aimed drag is two chances to go wrong with
no error message either way. One `mv` line does both and complains if the path is wrong. This has
already gone wrong once: on July 24 a replacement Tulsa photo landed at the root while
`profile.html` was correctly updated, so the live page credited one image and displayed another.

`.gitignore` also carries `apply-*.py` now, so a one-time script cannot reach a commit whatever
order you run things in.

---

## 5. Which validator command, and why it matters

```bash
python3 tools/validate.py --local .       # PRE-deploy. Reads the files on your disk.
python3 tools/validate.py                 # POST-deploy. Reads live GitHub. Confirmation only.
```

Before you push, you care about the code you are *about to ship*, which is on your disk. That is
`--local .`

The bare command reads what is already live, meaning what you shipped *last* time. Running that one
before a deploy validates the old site and then ships the new one unchecked. It will pass, and it will
have told you nothing.

**Exit code 1 means do not deploy.** Not "do not deploy unless it looks like a false positive." If you
believe a failure is wrong, that is a bug in the validator, and the fix goes in the validator.

---

## 6. Commit messages

You are the only person who will ever read these, which is exactly why they matter. In six months, the
change log and the commit history are the only record of why the site is the way it is.

Write what changed and where.

- Good: `Savannah profile: NRC callout, Visit block, affiliate codes`
- Good: `Ops log: ban repo snapshots, add enumeration rule`
- Useless: `update`, `fixes`, `wip`, `asdf`

---

## 7. When it goes wrong

**"nothing to commit, working tree clean"** right after you dropped a file in.
The file is not where you think it is. Run `git status`. If Git cannot see it, you dropped it in the
wrong folder, or you dropped it outside the repo entirely.

**"Updates were rejected because the remote contains work that you do not have."**
Something reached GitHub since your last pull. Usually you, from another tab or the GitHub web editor.
Fix: `git pull`, then `git push` again.

**You staged a file you did not mean to.**
`git restore --staged path/to/file` takes it back out of staging. The file on disk is untouched.

**You want to throw away your edits to a file and start over.**
`git restore path/to/file` resets it to the last commit. This deletes your changes and cannot be
undone. Be sure.

**You committed but forgot to push.**
Nothing is live. `git push`. The commit was only ever on your machine.

**Netlify did not deploy.**
Confirm the push actually landed: refresh the repo on github.com and look for your commit. No commit
on GitHub means Netlify never saw anything, and the problem is upstream of Netlify.

---

## 8. Rules that live above this document

These are from SITE-OPERATIONS-LOG.md sections 4a through 4c and are repeated here because they are
easy to violate during a deploy.

**Pull before you act.** `git pull` first, every time. This is the same discipline as 4c: get current
before you touch anything.

**Never edit a governing doc in two places at once.** Pick the repo copy or your local copy, not both.
Reconciling two divergent versions of a canonical document by hand is how the record gets corrupted.

**A file sitting in front of you is not evidence that it is current.** Not a downloaded copy, not a
snapshot, not something a chat handed you an hour ago. If it exists in the repo, pull it fresh.

**Update the sitemap when you add a city.** Step 5 of SOP-1. A missed step 5 does not break the site,
which is what makes it dangerous: it silently makes a live city invisible to anything that reads the
sitemap.

---

## 9. Full deploy, start to finish

The whole thing, in the order you actually do it.

```bash
git pull                                  # 1. get current
                                          # 2. make your change (drop file, unzip, or edit)
python3 apply-<city>.py                   # 3. edits to existing files, if the build sent one
git status                                # 4. does Git see what you expect, and nothing else?
python3 tools/validate.py --local .       # 5. exit 0 or stop
git add <the files you meant>             # 6. stage deliberately
git commit -m "<what changed and where>"  # 7. snapshot it
git push                                  # 8. ship
                                          # 9. watch the Netlify deploy log
                                          # 10. verify live in an incognito window
python3 tools/validate.py                 # 11. optional: confirm against live
                                          # 12. log it in ops log section 7
```

Steps 4 and 5 are the two you will be tempted to skip. They are the two that pay for themselves.

---

*RetireMeHere.com · DEPLOY-CHEATSHEET.md v1.2 · July 24, 2026*
