#!/usr/bin/env python3
"""
Planted-error test for check_comparison_vintage.

    python3 tools/test_comparison_vintage.py
    python3 tools/test_comparison_vintage.py --repo ..

No check ships without one of these.

COMPARISON-PAGE-STANDARD-v2 has always required the caption month to move when
figures are refreshed from a new database version. That rule was prose in a doc
and was missed BY HAND TWICE, on the Tier 3 cost-figure batch and again on Tier 2
batch A, which shipped three pages carrying refreshed July figures under a June
2026 caption with dateModified values up to seven weeks stale.

    1. a caption month older than DB_VERSION_DATE fails
    2. a caption YEAR older than DB_VERSION_DATE fails, even when the month is
       later in the year. December 2025 is not newer than July 2026, and a
       month-only comparison would say it was.
    3. a dateModified older than DB_VERSION_DATE fails
    4. the caption and dateModified are checked INDEPENDENTLY: fixing one while
       leaving the other stale still fails. This is the exact shape of the Tier 2
       batch A miss, where one page had a July caption and a stale dateModified.
    5. a missing caption fails, rather than passing because there was nothing to
       read
    6. a missing dateModified fails
    7. DB_VERSION_DATE disagreeing with the DEFAULT_DB filename fails. The
       constant is the floor for every page's vintage, so it drifting silently
       would move that floor without anyone deciding to.
    8. a caption NEWER than the database passes. Vintage moving ahead of the DB
       is legitimate, and a check that demanded exact equality would fire every
       time a page was edited between database versions.
    9. the control run is clean.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="vintage-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo, groups=("superlatives",)):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    cmd = [sys.executable, "tools/validate.py", "--local", "."]
    for g in groups:
        cmd += ["--only", g]
    p = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def a_page(repo):
    """First comparison page the hub links. Derived, never named."""
    hub = open(os.path.join(repo, "compare-retirement-cities.html"),
               encoding="utf-8").read()
    found = sorted(set(re.findall(
        r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)))
    if not found:
        sys.exit("no comparison pages on the hub. Re-derive this harness.")
    return found[0]


def edit(repo, page, pattern, replacement, expect=1):
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    out, n = re.subn(pattern, replacement, s)
    if n != expect:
        raise AssertionError(
            f"{page}: pattern {pattern!r} matched {n} times, expected {expect}")
    open(path, "w", encoding="utf-8").write(out)


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_vintage")
    page = a_page(repo)

    CAP = r"city database, \w+ \d{4}"
    DM = r'"dateModified": "\d{4}-\d{2}-\d{2}"'

    # 9. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1. stale caption month
    tmp, r = stage(repo)
    edit(r, page, CAP, "city database, January 2026")
    out = run(r)
    check("a caption month older than the database fails",
          "caption says the data is from January 2026" in out)
    shutil.rmtree(tmp)

    # 2. stale caption YEAR with a later month
    tmp, r = stage(repo)
    edit(r, page, CAP, "city database, December 2025")
    out = run(r)
    check("a caption from a previous year fails even with a later month",
          "December 2025" in out)
    shutil.rmtree(tmp)

    # 3. stale dateModified
    tmp, r = stage(repo)
    edit(r, page, DM, '"dateModified": "2026-01-05"')
    out = run(r)
    check("a dateModified older than the database fails",
          "2026-01-05 predates" in out)
    shutil.rmtree(tmp)

    # 4. one fixed, one stale, still fails
    tmp, r = stage(repo)
    edit(r, page, CAP, "city database, December 2026")
    edit(r, page, DM, '"dateModified": "2026-02-02"')
    out = run(r)
    check("a fresh caption does not excuse a stale dateModified",
          "2026-02-02 predates" in out)
    shutil.rmtree(tmp)

    # 5. missing caption
    tmp, r = stage(repo)
    edit(r, page, CAP, "figures compiled recently")
    out = run(r)
    check("a missing caption fails", "no \"Data: RetireMeHere" in out)
    shutil.rmtree(tmp)

    # 6. missing dateModified
    tmp, r = stage(repo)
    edit(r, page, DM, '"dateCreated": "2026-07-31"')
    out = run(r)
    check("a missing dateModified fails", "no schema dateModified" in out)
    shutil.rmtree(tmp)

    # 7. the constant must agree with the filename it describes
    tmp, r = stage(repo)
    path = os.path.join(r, "tools", "validate.py")
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"DB_VERSION_DATE = date\(\d+, \d+, \d+\)",
               "DB_VERSION_DATE = date(2026, 3, 3)", s, count=1)
    open(path, "w", encoding="utf-8").write(s)
    out = run(r, groups=("docs",))
    check("DB_VERSION_DATE disagreeing with DEFAULT_DB fails",
          "DB_VERSION_DATE disagrees" in out)
    shutil.rmtree(tmp)

    # 8. a vintage AHEAD of the database is fine
    tmp, r = stage(repo)
    edit(r, page, CAP, "city database, November 2026")
    edit(r, page, DM, '"dateModified": "2026-11-30"')
    out = run(r)
    check("a caption newer than the database passes", "0 failures" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
