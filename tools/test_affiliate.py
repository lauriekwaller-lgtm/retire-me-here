#!/usr/bin/env python3
"""
Planted-error test for check_affiliate.

    python3 tools/test_affiliate.py
    python3 tools/test_affiliate.py --repo ..

docs/AFFILIATE-CODES.csv became the affiliate record on Aug 21 2026, because the
tool pages need a code at render time for cities that have no profile: 99 cities
carry codes and only 51 have a profile, so the profiles can no longer be the whole
record. A separate table is a stale copy of the HTML unless something ties the two
together on every run, which is what check_affiliate does and what this file proves
it actually does.

A duplicated or drifted code is the dangerous failure here. It does not error and
it does not look broken. It quietly books one city's commission to another, and
nobody catches that by eye. Each assertion below plants one defect in a staged copy
and requires the gate to name it:

    1.  the control run is clean.
    2.  A DRIFTED PROFILE CODE fails: the profile and the table disagree.
    3.  A SHARED CODE fails: two cities carrying one Expedia code.
    4.  A DUPLICATE SLUG fails: two rows addressing one profile directory.
    5.  A BLANK CODE fails: a link that earns nothing.
    6.  A CITY MISSING FROM THE TABLE fails the roster.
    7.  A CITY IN THE TABLE BUT NOT THE DATABASE fails the roster the other way,
        which is the shape a wrong state abbreviation takes.
    8.  AN UNKNOWN CODE on a non-city page fails: a typo, or a code nobody recorded.
    9.  A CITY CODE ON A GENERIC PAGE fails unless it is declared deliberately.
        This is the misattribution case, and it is silent by nature.
    10. AN EMPTIED TABLE fails LOUDLY rather than checking zero codes and
        reporting clean.
    11. A CHANGED LINK FORMAT fails loudly rather than finding zero links and
        reporting clean.
    12. A DRIFTED INLINED CODE on a tool page fails. The tool pages carry a
        generated copy of the table so results can be linked at render time, and
        that copy is only tolerable because this catches it drifting.
    13. A CITY MISSING FROM AN INLINED MAP fails: that city renders with no link,
        which is invisible from the page.
    14. A REMOVED MAP fails loudly rather than checking nothing.
    15. AN EMPTIED MAP fails loudly rather than reporting clean while every result
        on the page renders linkless.

Exit 0 = all tests pass.
"""

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile

CSV_PATH = "docs/AFFILIATE-CODES.csv"
GENERIC_PAGE = "visit-before-you-decide.html"
MAP_PAGE = "where-can-i-afford-to-retire.html"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="affiliate-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "affiliate"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, s):
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def plant(repo, rel, old, new, count=1):
    path = os.path.join(repo, rel)
    s = read(path)
    if s.count(old) < count:
        sys.exit(f"plant target not found in {rel}: {old[:60]!r}. "
                 f"The file's byte format changed; re-derive this harness.")
    write(path, s.replace(old, new, count))


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_affiliate")

    # Derive every plant target from the live table. Nothing here is hardcoded, so
    # the harness follows the data instead of rotting against it.
    rows = list(csv.DictReader(read(os.path.join(repo, CSV_PATH)).splitlines()))
    profiled = [r for r in rows
                if os.path.exists(os.path.join(repo, "cities", r["slug"], "profile.html"))]
    if len(profiled) < 2:
        sys.exit("fewer than two profiled cities in the table; re-derive this harness.")
    a, b = profiled[0], profiled[1]
    a_line = ",".join(a[c] for c in ("city", "state", "slug",
                                     "expedia_code", "vrbo_code", "source"))

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. a drifted profile code
    tmp, r = stage(repo)
    plant(r, f"cities/{a['slug']}/profile.html",
          f"expedia.com/affiliate/{a['expedia_code']}",
          "expedia.com/affiliate/Zq9Zq9Z")
    out = run(r)
    check("a profile code that disagrees with the table fails",
          "does not match" in out and a["slug"] in out)
    shutil.rmtree(tmp)

    # 3. two cities sharing one Expedia code
    tmp, r = stage(repo)
    plant(r, CSV_PATH, f",{b['expedia_code']},", f",{a['expedia_code']},")
    out = run(r)
    check("two cities sharing an Expedia code fails", "is on both" in out)
    shutil.rmtree(tmp)

    # 4. a duplicate slug
    tmp, r = stage(repo)
    plant(r, CSV_PATH, f",{b['slug']},", f",{a['slug']},")
    out = run(r)
    check("a duplicate slug fails", "must be unique" in out)
    shutil.rmtree(tmp)

    # 5. a blank code
    tmp, r = stage(repo)
    plant(r, CSV_PATH, f",{a['expedia_code']},", ",,")
    out = run(r)
    check("a blank code fails", "has no expedia code" in out)
    shutil.rmtree(tmp)

    # 6. a city missing from the table
    tmp, r = stage(repo)
    plant(r, CSV_PATH, a_line + "\n", "")
    out = run(r)
    check("a database city with no row fails",
          "has no row in" in out and a["city"] in out)
    shutil.rmtree(tmp)

    # 7. a table row that is not a database city, which is what a wrong state
    #    abbreviation looks like from here
    tmp, r = stage(repo)
    plant(r, CSV_PATH, f"{a['city']},{a['state']},", f"{a['city']},ZZ,")
    out = run(r)
    check("a table row that is not a database city fails",
          "but not in the database" in out)
    shutil.rmtree(tmp)

    # 8. an unknown code on a non-city page
    tmp, r = stage(repo)
    page = read(os.path.join(r, GENERIC_PAGE))
    m = re.search(r"vrbo\.com/affiliate/([A-Za-z0-9]+)", page)
    if not m:
        sys.exit(f"no Vrbo link on {GENERIC_PAGE}; re-derive this harness.")
    plant(r, GENERIC_PAGE, f"vrbo.com/affiliate/{m.group(1)}",
          "vrbo.com/affiliate/Qx7Qx7Q")
    out = run(r)
    check("an unrecorded code on a generic page fails", "is in no row of" in out)
    shutil.rmtree(tmp)

    # 9. a city's code on a generic page, undeclared
    tmp, r = stage(repo)
    plant(r, GENERIC_PAGE, f"vrbo.com/affiliate/{m.group(1)}",
          f"vrbo.com/affiliate/{a['vrbo_code']}")
    out = run(r)
    check("a city code on a generic page fails as misattribution",
          "is not a city page but carries" in out)
    shutil.rmtree(tmp)

    # 10. an emptied table
    tmp, r = stage(repo)
    header = read(os.path.join(r, CSV_PATH)).splitlines()[0]
    write(os.path.join(r, CSV_PATH), header + "\n")
    out = run(r)
    check("an emptied table fails loudly rather than passing",
          "parsed to zero rows" in out)
    shutil.rmtree(tmp)

    # 11. a changed link format, site-wide
    tmp, r = stage(repo)
    for base, _, files in os.walk(r):
        for fn in files:
            if fn.endswith(".html"):
                p = os.path.join(base, fn)
                s = read(p)
                if "/affiliate/" in s:
                    write(p, s.replace("/affiliate/", "/partner-link/"))
    out = run(r)
    check("a changed link format fails loudly rather than finding nothing",
          "not one affiliate link was found" in out)
    shutil.rmtree(tmp)

    # 12 to 15: the inlined maps on the tool pages
    tmp, r = stage(repo)
    page = read(os.path.join(r, MAP_PAGE))
    mm = re.search(r'var RMH_AFF = (\{.*?\}); /\*END_RMH_AFF\*/', page, re.S)
    if not mm:
        sys.exit(f"no RMH_AFF map on {MAP_PAGE}; re-derive this harness.")
    shutil.rmtree(tmp)
    key = f'"{a["city"]}|{a["state"]}":["{a["expedia_code"]}","{a["vrbo_code"]}"]'

    # 12. a drifted code inside the map
    tmp, r = stage(repo)
    plant(r, MAP_PAGE, key,
          f'"{a["city"]}|{a["state"]}":["Wr0ngC0","{a["vrbo_code"]}"]')
    out = run(r)
    check("a drifted code in an inlined map fails",
          "booking commission to the wrong code" in out)
    shutil.rmtree(tmp)

    # 13. a city dropped from the map
    tmp, r = stage(repo)
    plant(r, MAP_PAGE, key + ",", "")
    out = run(r)
    check("a city missing from an inlined map fails",
          "renders with no affiliate link" in out and a["city"] in out)
    shutil.rmtree(tmp)

    # 14. the map removed outright
    tmp, r = stage(repo)
    plant(r, MAP_PAGE, "var RMH_AFF = ", "var RMH_AFF_DISABLED = ")
    out = run(r)
    check("a removed map fails loudly rather than checking nothing",
          "carries no RMH_AFF map" in out)
    shutil.rmtree(tmp)

    # 15. the map emptied
    tmp, r = stage(repo)
    path = os.path.join(r, MAP_PAGE)
    s2 = re.sub(r"var RMH_AFF = \{.*?\}; /\*END_RMH_AFF\*/",
                "var RMH_AFF = {}; /*END_RMH_AFF*/", read(path), count=1, flags=re.S)
    write(path, s2)
    out = run(r)
    check("an emptied map fails loudly rather than reporting clean",
          "parsed to zero cities" in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
