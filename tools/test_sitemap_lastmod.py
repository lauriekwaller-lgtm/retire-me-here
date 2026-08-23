#!/usr/bin/env python3
"""
Planted-error test for check_sitemap_lastmod in validate.py.

    python3 tools/test_sitemap_lastmod.py            # against this checkout
    python3 tools/test_sitemap_lastmod.py --repo ..  # against another checkout

No check ships without one of these. This one exists because of the August 23
2026 Search Console read, where seven of the nine pages Google had declined to
index were being described by the sitemap as untouched since May or June while
the August 22 pillar-link batch had rewritten every one of them.

WHY THIS HARNESS BUILDS ITS OWN GIT HISTORY, which is the one thing that makes
it different from every other harness in this directory. The others stage a copy
of the checkout with `.git` excluded and run `--only <group>` against it. This
check reads git, so a staged copy with no history would fail every assertion for
the wrong reason and prove nothing. So each stage runs `git init` and commits
with GIT_COMMITTER_DATE pinned to a fixed day. Every date in play is then a
value this file chose, which is what makes the staleness assertions mean
something: "fails when 30 days stale" is a real claim only if the harness knows
the commit was 30 days ago.

That also decided where the check lives. It cannot go in the `routing` group:
test_canonicals.py and test_pillar_links.py both stage without `.git` and run
`--only routing`, so a git-reading check in that group would fail both of them
on a clean tree. Hence a `sitemap` group of its own.

The assertions are the ways the August 23 defect could recur, plus the shape
failures that would hide it:

    1. the control run is clean, so the check is not merely failing at everything
    2. a stale date fails, and this is the defect that shipped: the file on disk
       has moved on and the sitemap still describes the old version
    3. the failure NAMES the page and both dates. A stale-sitemap failure that
       does not say which page or how stale sends you back to the sitemap to
       diff 98 entries by eye, which is how it went unnoticed for three months
    4. a MISSING <lastmod> fails, which is the chattanooga defect found in the
       same read, and it fails distinctly from the stale case
    5. two <lastmod> elements on one entry fails, since "we set it twice" reads
       as defended when which value a crawler honours is undefined
    6. a non-date, and a real-looking date that is not a real day, both fail
    7. a FUTURE date fails. This is the plausible bad fix: someone stamps every
       entry with a date ahead of the batch to force a recrawl, and the file
       becomes a page-by-page assertion nobody can have made
    8. a date that is FRESHER than git but not in the future passes, because the
       tolerance exists for the commit-day boundary and a check that failed here
       would fail on any deploy that straddled midnight
    9. a sitemap entry with no file on disk fails
   10. a tree with no .git FAILS rather than skipping clean, which is the
       failure mode this codebase keeps rediscovering
   11. an empty sitemap fails loudly rather than checking zero entries

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta

# Any sitemapped page will do; these two are stable and are not the homepage,
# whose <loc> is the bare root and therefore its own parsing case.
PAGE = "top-cities-for-hikers.html"
OTHER = "top-cities-for-foodies.html"

COMMIT_DAY = "2026-08-20"


def stage(repo, with_git=True):
    """
    A throwaway copy with a git history this file controls. The real checkout is
    never written to and its history is never read.
    """
    tmp = tempfile.mkdtemp(prefix="rmh-sitemap-")
    dest = os.path.join(tmp, "repo")
    # Binaries are excluded, unlike the other harnesses, purely for speed: this
    # file stages eleven times and git-hashes every staged file on each, and the
    # 153 profile photos are ~150MB that no sitemap check will ever open. Nothing
    # in the sitemap is an image, so their absence cannot change a result.
    shutil.copytree(repo, dest,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc",
                                                  "*.jpg", "*.jpeg", "*.png",
                                                  "*.webp", "*.pdf", "*.ico"))
    if with_git:
        env = dict(os.environ)
        env.update({
            "GIT_AUTHOR_NAME": "harness", "GIT_AUTHOR_EMAIL": "harness@local",
            "GIT_COMMITTER_NAME": "harness", "GIT_COMMITTER_EMAIL": "harness@local",
            "GIT_AUTHOR_DATE": f"{COMMIT_DAY}T12:00:00",
            "GIT_COMMITTER_DATE": f"{COMMIT_DAY}T12:00:00",
        })
        for args in (["init", "-q"], ["add", "-A"],
                     ["commit", "-q", "-m", "harness baseline"]):
            proc = subprocess.run(["git", "-C", dest] + args,
                                  capture_output=True, text=True, env=env)
            if proc.returncode != 0:
                raise SystemExit(f"harness setup error: git {args[0]} failed: "
                                 f"{proc.stderr.strip()}")
    return dest


def run(tmp):
    """Run the sitemap group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "sitemap"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def write_sitemap(tmp, rows):
    body = ['<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n']
    for loc, inner in rows:
        body.append(f"\n  <url>\n    <loc>{loc}</loc>\n{inner}  </url>\n")
    body.append("\n</urlset>\n")
    with open(os.path.join(tmp, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("".join(body))


def baseline_rows(tmp):
    """Every sitemap entry, rewritten to the harness's own commit day."""
    with open(os.path.join(tmp, "sitemap.xml"), encoding="utf-8") as fh:
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", fh.read())
    if not locs:
        raise SystemExit("harness setup error: no <loc> entries to plant against")
    return [(loc, f"    <lastmod>{COMMIT_DAY}</lastmod>\n") for loc in locs]


def loc_for(rows, page):
    for loc, _ in rows:
        if loc.endswith("/" + page):
            return loc
    raise SystemExit(f"harness setup error: {page} is not in the sitemap")


def replace(rows, loc, inner):
    return [(l, inner if l == loc else i) for l, i in rows]


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: sitemap <lastmod> integrity\n")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    rows = baseline_rows(tmp)
    page_loc = loc_for(rows, PAGE)
    other_loc = loc_for(rows, OTHER)
    write_sitemap(tmp, rows)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a sitemap whose dates match git passes", code == 0 and not base,
          f"{len(base)} failure(s)")

    def plant(inner, loc=None, rewrite=None, with_git=True):
        """Stage, apply one plant, run, tear down. Returns new failures + code."""
        t = stage(repo, with_git=with_git)
        if rewrite is not None:
            rewrite(t)
        else:
            write_sitemap(t, replace(baseline_rows(t), loc or page_loc, inner))
        c, f = run(t)
        shutil.rmtree(os.path.dirname(t))
        return c, f - base

    # ------------------------------------------------- 2 + 3. the stale defect
    stale_day = (date.fromisoformat(COMMIT_DAY) - timedelta(days=101)).isoformat()
    code, added = plant(f"    <lastmod>{stale_day}</lastmod>\n")
    hit = [f for f in added if PAGE in f and "last changed" in f]
    check("a stale <lastmod> fails (the May-date defect that shipped)",
          code == 1 and bool(hit), f"{len(added)} new failure(s)")
    check("the stale failure names the page, the claimed date and the real one",
          bool(hit) and stale_day in hit[0] and COMMIT_DAY in hit[0]
          and "101 days" in hit[0],
          hit[0][:96] if hit else "no matching failure")

    # ------------------------------------------------ 4. no <lastmod> at all
    code, added = plant("")
    check("an entry with no <lastmod> fails (the chattanooga defect)",
          code == 1 and any(PAGE in f and "0 <lastmod>" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------------------- 5. two <lastmod>
    code, added = plant(f"    <lastmod>{COMMIT_DAY}</lastmod>\n"
                        f"    <lastmod>{stale_day}</lastmod>\n")
    check("two <lastmod> elements on one entry fails",
          code == 1 and any(PAGE in f and "2 <lastmod>" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------- 6. malformed and unreal dates
    code, added = plant("    <lastmod>August 2026</lastmod>\n")
    check("a non-ISO <lastmod> fails",
          code == 1 and any(PAGE in f and "not an ISO" in f for f in added),
          f"{len(added)} new failure(s)")

    code, added = plant("    <lastmod>2026-02-31</lastmod>\n")
    check("an ISO-shaped date that is not a real day fails",
          code == 1 and any(PAGE in f and "not a real calendar date" in f
                            for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------------------------------------- 7. future date
    ahead = (date.today() + timedelta(days=30)).isoformat()
    code, added = plant(f"    <lastmod>{ahead}</lastmod>\n")
    check("a future <lastmod> fails (the plausible bad fix)",
          code == 1 and any(PAGE in f and "in the future" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------- 8. fresher than git, inside tolerance, is fine
    fresh = (date.fromisoformat(COMMIT_DAY) + timedelta(days=1)).isoformat()
    code, added = plant(f"    <lastmod>{fresh}</lastmod>\n")
    check("a date one day fresher than git still passes (commit-day boundary)",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # --------------------------------------------- 9. entry with no file
    ghost = other_loc.replace(OTHER, "top-cities-for-nobody.html")
    t = stage(repo)
    r = baseline_rows(t)
    r.append((ghost, f"    <lastmod>{COMMIT_DAY}</lastmod>\n"))
    write_sitemap(t, r)
    code, fails = run(t)
    shutil.rmtree(os.path.dirname(t))
    added = fails - base
    check("a sitemap entry with no file on disk fails",
          code == 1 and any("could not be read" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------- 10. no git must fail, not read clean
    code, added = plant(f"    <lastmod>{COMMIT_DAY}</lastmod>\n", with_git=False)
    check("a tree with no .git fails loudly rather than skipping clean",
          code == 1 and any("not a git checkout" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------- 11. nothing to check must fail, not pass
    def blank(t):
        with open(os.path.join(t, "sitemap.xml"), "w", encoding="utf-8") as fh:
            fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset></urlset>\n')
    code, added = plant(None, rewrite=blank)
    check("an empty sitemap fails loudly rather than checking nothing",
          code == 1 and any("no <url> blocks" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
