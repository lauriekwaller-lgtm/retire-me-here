#!/usr/bin/env python3
"""
Planted-error test for check_typography.

    python3 tools/test_typography.py
    python3 tools/test_typography.py --repo ..

The August 2026 font sweep retired Playfair Display, Fraunces, and every
font-weight 300, and collapsed all Google Fonts requests to one canonical
link. check_typography holds that in place, because new pages are cloned from
existing ones and a single stale template would quietly reintroduce all of it.
Each assertion plants one defect in a staged copy and requires the gate to
catch it, plus one plant that must NOT be caught:

    1. the control run is clean.
    2. A DECLARED RETIRED FAMILY fails: font-family: 'Playfair Display' in a
       style block.
    3. A THIN WEIGHT fails: font-weight: 300 anywhere.
    4. A RETIRED FAMILY IN A FONTS LINK fails: family=Fraunces requested from
       Google Fonts.
    5. A NON-CANONICAL FAMILY fails: a Google Fonts request for a family that
       is neither Libre Franklin nor DM Sans.
    6. PROSE STAYS LEGAL: the words "Playfair Park" in visible copy (a real
       Alexandria pickleball spot) must NOT fail. The check bans font
       references, not vocabulary; this plant is the regression test for the
       false positive found while building the sweep.

Exit 0 = all tests pass.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

TARGET = "index.html"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="typog-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "layout"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def plant(repo, addition):
    path = os.path.join(repo, TARGET)
    with open(path, encoding="utf-8") as f:
        s = f.read()
    marker = "</body>"
    if marker not in s:
        sys.exit(f"{TARGET} has no </body>; re-derive this harness.")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s.replace(marker, addition + "\n" + marker, 1))


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_typography")

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. a declared retired family
    tmp, r = stage(repo)
    plant(r, "<div style=\"font-family: 'Playfair Display', serif;\">x</div>")
    out = run(r)
    check("a declared retired family fails", "retired font family" in out)
    shutil.rmtree(tmp)

    # 3. a thin weight
    tmp, r = stage(repo)
    plant(r, "<style>.rogue { font-weight: 300; }</style>")
    out = run(r)
    check("a font-weight 300 rule fails", "font-weight 300" in out)
    shutil.rmtree(tmp)

    # 4. a retired family requested from Google Fonts
    tmp, r = stage(repo)
    plant(r, '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600&display=swap" rel="stylesheet">')
    out = run(r)
    check("a retired family in a fonts link fails",
          "retired font family" in out or "non-canonical" in out)
    shutil.rmtree(tmp)

    # 5. a non-canonical family requested from Google Fonts
    tmp, r = stage(repo)
    plant(r, '<link href="https://fonts.googleapis.com/css2?family=Lobster&display=swap" rel="stylesheet">')
    out = run(r)
    check("a non-canonical fonts request fails", "non-canonical" in out)
    shutil.rmtree(tmp)

    # 6. prose containing a retired font's name must NOT fail
    tmp, r = stage(repo)
    plant(r, "<p>Close to Playfair Park (8 outdoor pickleball courts).</p>")
    out = run(r)
    check("prose mentioning Playfair Park stays legal", "0 failures" in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
