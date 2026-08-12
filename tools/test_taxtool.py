#!/usr/bin/env python3
"""
Planted-error test for check_taxtool_data.

    python3 tools/test_taxtool.py
    python3 tools/test_taxtool.py --repo ..

states-that-dont-tax-retirement-income.html carries two embedded copies of
database content: TAXFACTS (the State Tax Facts sheet) and TAXCITIES (the city
roster with each city's D5). Embedded copies are the drift this validator
exists for, so check_taxtool_data compares both, field by field, against the
workbook on every run. Each assertion below plants one defect in a staged copy
of the PAGE (the workbook is left alone: the taxfacts harness owns that side)
and requires the gate to catch it:

    1. the control run is clean.
    2. A DRIFTED FACT fails: one state's top rate changed on the page only.
    3. A REMOVED STATE fails the roster in both directions when renamed to a
       fake key: the real state is missing, the fake one is an orphan.
    4. A DRIFTED CITY D5 fails: the exact stale-score failure the Philadelphia
       correction showed every embedded array is capable of.
    5. A REMOVED CITY fails the city roster.
    6. A DRIFTED NOTE fails. Prose restating checked data is itself data:
       a note claiming an exemption the sheet no longer records is a lie the
       reader cannot detect.
    7. AN EMPTIED TAXFACTS ARRAY fails LOUDLY rather than comparing zero
       states and reporting clean.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PAGE = "states-that-dont-tax-retirement-income.html"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="taxtool-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "figures"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def plant(repo, old, new, count=1):
    path = os.path.join(repo, PAGE)
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if s.count(old) < count:
        sys.exit(f"plant target not found in {PAGE}: {old[:60]!r}. "
                 f"The page's byte format changed; re-derive this harness.")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s.replace(old, new, count))


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_taxtool")

    with open(os.path.join(repo, PAGE), encoding="utf-8") as f:
        html = f.read()
    facts = re.search(r'const TAXFACTS = (\[.*?\]); /\*END_TAXFACTS\*/',
                      html, re.S).group(1)
    # derive plant targets from the live page, no hardcoding
    m = re.search(r'\{"st":"([A-Z]{2})","name":"[^"]+","itype":"[^"]+",'
                  r'"top":([0-9.]+)', facts)
    st, top = m.group(1), m.group(2)
    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. a drifted fact
    tmp, r = stage(repo)
    plant(r, f'"top":{top}', f'"top":{float(top) + 1.11:g}')
    out = run(r)
    check("a drifted fact on the page fails", "disagrees with the State Tax Facts" in out)
    shutil.rmtree(tmp)

    # 3. a renamed state key: missing and orphan at once
    tmp, r = stage(repo)
    plant(r, f'"st":"{st}"', '"st":"ZZ"')
    out = run(r)
    check("a state missing from the page fails", "is not on the page" in out)
    check("a state on the page but not in the sheet fails", "not in the State Tax Facts sheet" in out)
    shutil.rmtree(tmp)

    # 4. a drifted city D5
    tmp, r = stage(repo)
    d5m = re.search(r'\{("d5":(\d+),"n":"[^"]+")\},', html)
    inner, val = d5m.group(1), d5m.group(2)
    plant(r, "{" + inner + "}", "{" + inner.replace(f'"d5":{val}', f'"d5":{int(val) + 1}', 1) + "}")
    out = run(r)
    check("a drifted city D5 fails", "D5 as" in out and "database says" in out)
    shutil.rmtree(tmp)

    # 5. a removed city
    tmp, r = stage(repo)
    plant(r, "{" + inner + "},", "")
    out = run(r)
    check("a city missing from the page fails", "is missing from the page" in out)
    shutil.rmtree(tmp)

    # 6. a drifted note
    tmp, r = stage(repo)
    note = re.search(r'"note":"([^"]{20,})"', facts).group(1)
    plant(r, f'"note":"{note}"', f'"note":"{note} and always has been"')
    out = run(r)
    check("a drifted note fails", "note for" in out and "does not match" in out)
    shutil.rmtree(tmp)

    # 7. an emptied TAXFACTS array
    tmp, r = stage(repo)
    path = os.path.join(r, PAGE)
    with open(path, encoding="utf-8") as f:
        s = f.read()
    s2 = re.sub(r"const TAXFACTS = \[.*?\]; /\*END_TAXFACTS\*/",
                "const TAXFACTS = []; /*END_TAXFACTS*/", s, count=1, flags=re.S)
    if s2 == s:
        sys.exit("plant 7 found nothing to empty; re-derive this harness.")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s2)
    out = run(r)
    check("an emptied TAXFACTS array fails loudly rather than passing",
          "parsed to zero states" in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
