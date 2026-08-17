#!/usr/bin/env python3
"""
Planted-error test for _comparison_row, the slug resolver behind
check_comparison_scores and check_comparison_cost_rows.

    python3 tools/test_comparison_slugs.py
    python3 tools/test_comparison_slugs.py --repo ..

No check ships without one of these.

This one exists because both table checks were shipped with a lookup keyed on
the lowercased city NAME and no state. Two silent defects, measured 2026-08-08:

    burlington-vs-portland-me-retirement.html was never checked by either
    function, from the day it shipped. "Portland" keys to "portland", the page
    says "portland-me", the lookup missed, and `if not a or not b: continue`
    read nothing and called it clean. The proof arrived the moment the fix
    landed: the page's budget cells carried `&ndash;` entities that had never
    been compared to the database, and failed on the fix's first run.

    Wilmington DE and Wilmington NC both keyed to "wilmington" and the dict
    kept whichever row built last, so a future Wilmington page would have
    validated against the WRONG CITY's figures and PASSED.

The fix resolves slugs through PUBLISHED_PROFILES into (City, ST) db keys and
fails loudly on every miss. The assertions cover both original defects and the
loud-miss contract:

    1. the control run is clean, so the resolver is not merely failing at
       everything
    2. a wrong D-score planted on the state-suffixed page FAILS. This is the
       silent-skip defect: under the old lookup this plant passed the gate.
    3. a wrong home value planted on the state-suffixed page FAILS, same
       defect, cost-rows side.
    4. a comparison slug with no PUBLISHED_PROFILES entry FAILS LOUDLY rather
       than skipping. An unresolvable page is uncovered work, and reading
       nothing while reporting clean is the fault this whole file family
       exists to stop.
    5. a slug rebound to a DIFFERENT city's (City, ST) FAILS, because the page
       figures no longer match the resolved row. This is the Wilmington
       collision made executable: wrong-city resolution must never pass.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The page whose slug carries a state suffix. It is the page the old lookup
# never resolved, which makes it the right host for the planted errors: every
# plant below passed the old code and must fail the new.
PAGE = "burlington-vs-portland-me-retirement.html"

# The PUBLISHED_PROFILES entry behind that page's second slug, verbatim as it
# appears in index.html. Both rebinding assertions edit this line in a staged
# copy; the anchor check in edit() fails the harness if the line moves.
PM_ENTRY = "'Portland_ME': 'cities/portland-me/profile.html'"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="cslug-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    # --only superlatives is the group that RUNS the comparison checks (they
    # report to "comparison" but execute under "superlatives"), and
    # RMH_IN_HARNESS stops validate.py re-running the harnesses (including
    # this one) from inside a harness.
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".",
         "--only", "superlatives"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def edit(repo, relpath, old, new):
    path = os.path.join(repo, relpath)
    s = open(path, encoding="utf-8").read()
    if old not in s:
        raise AssertionError(f"anchor not found in {relpath}: {old[:70]!r}")
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))


def score_cell(repo, page, dim):
    """Rewrite the first value cell of a dimension row to a wrong score."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(
        rf'(<td class="metric">{dim}(?![0-9])[^<]*</td>\s*'
        rf'<td class="value[^"]*">)(\d{{1,2}})(/10[^<]*</td>)',
        s, re.S)
    if not m:
        raise AssertionError(f"no {dim} row in {page}")
    wrong = "1" if m.group(2) != "1" else "9"
    open(path, "w", encoding="utf-8").write(
        s[:m.start(2)] + wrong + s[m.end(2):])


def cost_cell(repo, page, label, replacement):
    """Rewrite the first value cell of a cost row."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(
        r'<td class="metric">' + re.escape(label) + r"</td>\s*"
        r'<td class="value[^"]*">([^<]*)</td>',
        s, re.S)
    if not m:
        raise AssertionError(f"no {label!r} row in {page}")
    span = m.span(1)
    open(path, "w", encoding="utf-8").write(
        s[:span[0]] + replacement + s[span[1]:])


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_slugs")

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. the silent-skip defect, scores side: a wrong score on the
    #    state-suffixed page must fail. Under the old lookup it passed.
    tmp, r = stage(repo)
    score_cell(r, PAGE, "D1")
    out = run(r)
    check("wrong score on the state-suffixed page fails",
          PAGE in out and "DB says" in out)
    shutil.rmtree(tmp)

    # 3. same defect, cost-rows side.
    tmp, r = stage(repo)
    cost_cell(r, PAGE, "Typical home value", "$999,000")
    out = run(r)
    check("wrong home value on the state-suffixed page fails",
          PAGE in out and "999,000" in out)
    shutil.rmtree(tmp)

    # 4. an unresolvable slug fails loudly, never skips. Point the profile
    #    path somewhere else so the slug 'portland-me' has no entry.
    tmp, r = stage(repo)
    edit(r, "index.html", PM_ENTRY,
         "'Portland_ME': 'cities/portland-me-zz/profile.html'")
    out = run(r)
    check("a slug missing from PUBLISHED_PROFILES fails loudly",
          PAGE in out and "not in PUBLISHED_PROFILES" in out)
    shutil.rmtree(tmp)

    # 5. the collision defect: rebind the slug to a different city's
    #    (City, ST) and the page must fail, because its figures no longer
    #    match the resolved row. Wrong-city validation passing is the exact
    #    Wilmington landmine the tuple keying exists to defuse.
    tmp, r = stage(repo)
    edit(r, "index.html", PM_ENTRY,
         "'Wilmington_DE': 'cities/portland-me/profile.html'")
    out = run(r)
    check("a slug rebound to the wrong city fails",
          PAGE in out and "DB says" in out)
    shutil.rmtree(tmp)

    failed = [n for n, ok in RESULTS if not ok]
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} passed"
          + (f", failed: {failed[0]}" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
