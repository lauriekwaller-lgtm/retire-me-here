#!/usr/bin/env python3
"""
Planted-error test for check_afford_data in validate.py.

    python3 tools/test_afford_data.py            # against this checkout
    python3 tools/test_afford_data.py --repo ..  # against another checkout

No check ships without one of these.

where-can-i-afford-to-retire.html carries a second copy of six database columns
for every city, because it computes a personalised monthly cost from an equity
figure the reader types and BUDGET-METHODOLOGY.md section 14.4 forbids storing
precomputed figures. A second copy of the database is the exact drift this
validator exists for, so the check has to be worth trusting.

The assertions map to the ways this page can be wrong, and the last two are the
ones worth having:

    1. the control run is clean, so the check is not merely failing at everything
    2. a changed Median Home fails, the plain cell drift
    3. a changed dimension score fails, since the scores drive the ranking and
       nothing else on the site would ever look at this copy of them
    4. a city deleted from the array fails as an OMISSION. This is the one that
       would otherwise ship: every remaining row is internally perfect, the page
       renders, the arithmetic is right, and one city has simply become invisible
       to every reader of the tool. Same shape as the roster gap that put four
       wrong cities on the budget page in July while the gate read clean.
    5. a city added to the array that is not in the database fails
    6. a changed mortgage rate fails. Cells and roster can both be perfect while
       every figure on the page is wrong, and a rate is the likeliest constant to
       be edited by hand between quarterly PMMS checks.
    7. a changed per-state multiplier fails, naming the state. Section 6 is
       transcribed in two places now and they can disagree.
    8. a DELETED per-state multiplier fails rather than defaulting. In the page's
       JavaScript a missing key yields NaN, every city in that state silently
       fails the budget comparison, and the results list just gets shorter.
    9. an emptied array fails LOUDLY rather than comparing zero cities and
       reporting clean. This codebase keeps rediscovering that failure mode.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PAGE = "where-can-i-afford-to-retire.html"


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-afford-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the figures group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "figures"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def edit(tmp, rel, old, new, count=1):
    """Rewrite a staged file, asserting the anchor was actually there."""
    path = os.path.join(tmp, rel)
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    if body.count(old) != count:
        raise SystemExit(f"harness anchor error: {old!r} appears "
                         f"{body.count(old)} times in {rel}, expected {count}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body.replace(old, new))


ROW = re.compile(r'\{n:"((?:[^"\\]|\\.)*)",s:"([A-Z]{2})",h:(\d+),t:([\d.]+),i:(\d+),'
                 r'w:(\d+),x:(\d+),d:\[(\d+(?:,\d+){9})\]\}')


def a_row(repo):
    """The first AFFORD_CITIES row, as (full text, name, state), to plant against."""
    with open(os.path.join(repo, PAGE), encoding="utf-8") as fh:
        body = fh.read()
    m = ROW.search(body)
    if not m:
        raise SystemExit(f"harness setup error: no AFFORD_CITIES row found in {PAGE}")
    return m.group(0), m.group(1), m.group(2)


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: affordability page data vs the database\n")

    row, city, state = a_row(repo)

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a checkout whose page matches the database passes",
          code == 0 and not base, f"{len(base)} failure(s)")

    # ------------------------------------------------- 2. a drifted home value
    tmp = stage(repo)
    m = ROW.match(row)
    bumped = row.replace(f",h:{m.group(3)},", f",h:{int(m.group(3)) + 25000},")
    edit(tmp, PAGE, row, bumped)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a Median Home that disagrees with the database fails",
          code == 1 and any(city in f and "Median Home" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------------------- 3. a drifted score
    tmp = stage(repo)
    dims = m.group(8).split(",")
    twisted = row.replace(f",d:[{m.group(8)}]",
                          ",d:[" + ",".join([str((int(dims[0]) % 10) + 1)] + dims[1:]) + "]")
    edit(tmp, PAGE, row, twisted)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a dimension score that disagrees with the database fails",
          code == 1 and any(city in f and "D1" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------- 4. a city gone missing
    tmp = stage(repo)
    edit(tmp, PAGE, row + ",\n", "")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a city in the database with no row on the page fails (the omission)",
          code == 1 and any(city in f and "no AFFORD_CITIES row" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------------------------------- 5. an invented city
    tmp = stage(repo)
    invented = row.replace(f'n:"{city}"', 'n:"Nowhere"', 1)
    edit(tmp, PAGE, row, row + ",\n" + invented)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a city on the page that is not in the database fails",
          code == 1 and any("Nowhere" in f and "not in the database" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------- 6. a drifted mortgage rate
    tmp = stage(repo)
    edit(tmp, PAGE, "var PMMS_RATE   = 0.0652;", "var PMMS_RATE   = 0.0715;")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a mortgage rate that disagrees with the methodology fails",
          code == 1 and any("PMMS_RATE" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------ 7. a drifted state multiplier
    tmp = stage(repo)
    edit(tmp, PAGE, "  TX:0.96,", "  TX:1.06,")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a per-state cost-of-living multiplier that disagrees with section 6 fails",
          code == 1 and any("COL_MOD[TX]" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------- 8. a DELETED state multiplier
    tmp = stage(repo)
    edit(tmp, PAGE, "  TX:0.96,\n", "")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a missing state multiplier fails rather than computing NaN silently",
          code == 1 and any("missing TX" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------- 9. nothing to check must fail, not read clean
    tmp = stage(repo)
    path = os.path.join(tmp, PAGE)
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    body = re.sub(r"const AFFORD_CITIES = \[.*?\n\];",
                  "const AFFORD_CITIES = [\n];", body, flags=re.S)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("an emptied array fails loudly rather than checking nothing",
          code == 1 and any("parsed to zero rows" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
