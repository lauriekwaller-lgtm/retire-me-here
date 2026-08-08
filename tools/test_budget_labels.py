#!/usr/bin/env python3
"""
Planted-error test for check_budget_labels.

    python3 tools/test_budget_labels.py
    python3 tools/test_budget_labels.py --repo ..

The check it guards was written after the 2026-08-07 P0, in which renderBudget()
rendered the quiz budget question from a local BUDGET_LABELS array whose middle
three entries were byte-identical. Three buttons a reader could not tell apart,
each setting a different quizState.budget and returning a different result set,
on step three of four of the primary conversion path. It sat live while the gate
read 0 failures 0 warnings in every session, because nothing in the toolchain had
ever read a quiz option label.

A check written to close that hole is worth nothing unless it can be shown to
FAIL. Each assertion below plants one defect and requires the gate to catch it.

     1. the control run is clean.
     2. TWO IDENTICAL LABELS fail. This is the original defect, reproduced
        exactly: it is the one shape the check exists for.
     3. A MISSING BAND fails. Four options where the engine indexes five.
     4. AN OVERLAPPING EDGE fails. A reader in the overlap has two correct
        answers that return different result sets.
     5. A GAP BETWEEN EDGES fails, the same defect in reverse: a reader in the
        gap has no correct answer.
     6. A CAPPED TOP BAND fails. It silently excludes everyone above it.
     7. A LABEL DISAGREEING WITH ITS EDGES fails, while the deliberate one-dollar
        rounding seam at every boundary stays legal in the control run. Both
        halves matter: a check that rejects the rounding would fire on correct
        data on day one, and a check loosened enough to accept it must still
        reject a genuinely wrong figure.
     8. LOW-END BANDS fail. This is the policy assertion. The bands are derived
        from the MIDPOINT of each range's Monthly Est span; the low end is the
        cheapest month a city ever has, and the candidate filter already grants
        one range of stretch, so low-end labels would stack a second on top. The
        exact set proposed on the board before that argument was made is planted
        here and must be rejected. If the policy is ever reversed, this test
        fails and the reversal has to be made deliberately.
     9. A SECOND COPY of the band set fails. Two copies is the precise condition
        that produced the original defect.
    10. renderBudget() NO LONGER READING BUDGET_BANDS fails: the defect returning
        under a new name.
    11. DELETING BUDGET_BANDS ENTIRELY fails LOUDLY rather than reporting clean.
        Zero matches must never be a pass; that is the silent-no-op shape this
        validator exists to refuse, and it is how the original defect survived.

Nothing here is hardcoded to a band figure it does not have to be: the planted
values are derived from the live constant so this file does not need editing the
next time the bands legitimately move.

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
    tmp = tempfile.mkdtemp(prefix="budget-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".",
         "--only", "superlatives"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def read_index(repo):
    return open(os.path.join(repo, "index.html"), encoding="utf-8").read()


def write_index(repo, s):
    open(os.path.join(repo, "index.html"), "w", encoding="utf-8").write(s)


def bands_block(repo):
    """The BUDGET_BANDS literal, verbatim, so plants are derived not hardcoded."""
    s = read_index(repo)
    m = re.search(r"const BUDGET_BANDS = \[.*?\];", s, re.S)
    if not m:
        sys.exit("BUDGET_BANDS not found in index.html. Re-derive this harness.")
    return m.group(0)


def band_lines(block):
    return [l for l in block.splitlines() if re.search(r"range:\s*\d", l)]


def replace_block(repo, new_block):
    s = read_index(repo)
    old = re.search(r"const BUDGET_BANDS = \[.*?\];", s, re.S).group(0)
    write_index(repo, s.replace(old, new_block, 1))


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_budget_labels")
    block = bands_block(repo)
    lines = band_lines(block)
    if len(lines) != 5:
        sys.exit(f"expected 5 band lines, found {len(lines)}. Re-derive this harness.")

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. the original defect: two identical labels
    tmp, r = stage(repo)
    lab3 = re.search(r"label:\s*'([^']*)'", lines[2]).group(1)
    lab2 = re.search(r"label:\s*'([^']*)'", lines[1]).group(1)
    replace_block(r, block.replace(lines[2], lines[2].replace(lab3, lab2), 1))
    out = run(r)
    check("two identical labels fail", "duplicate labels" in out)
    shutil.rmtree(tmp)

    # 3. a missing band
    tmp, r = stage(repo)
    replace_block(r, block.replace(lines[3] + "\n", "", 1))
    out = run(r)
    check("four bands instead of five fails", "expected 5" in out)
    shutil.rmtree(tmp)

    # 4. overlapping edges
    tmp, r = stage(repo)
    mx = int(re.search(r"max:\s*(\d+)", lines[1]).group(1))
    replace_block(r, block.replace(
        lines[1], re.sub(r"max:\s*\d+", f"max: {mx + 200}", lines[1]), 1))
    out = run(r)
    check("an overlapping band edge fails", "not contiguous" in out)
    shutil.rmtree(tmp)

    # 5. a gap between edges
    tmp, r = stage(repo)
    replace_block(r, block.replace(
        lines[1], re.sub(r"max:\s*\d+", f"max: {mx - 200}", lines[1]), 1))
    out = run(r)
    check("a gap between band edges fails", "not contiguous" in out)
    shutil.rmtree(tmp)

    # 6. a capped top band
    tmp, r = stage(repo)
    replace_block(r, block.replace(
        lines[4], lines[4].replace("max: null", "max: 20000"), 1))
    out = run(r)
    check("a capped top band fails", "open-ended" in out)
    shutil.rmtree(tmp)

    # 7. a label that disagrees with its edges
    tmp, r = stage(repo)
    lab4 = re.search(r"label:\s*'([^']*)'", lines[3]).group(1)
    figs = re.findall(r"\$[\d,]+", lab4)
    bad = lab4.replace(figs[1], "$8,400")
    replace_block(r, block.replace(lines[3], lines[3].replace(lab4, bad), 1))
    out = run(r)
    check("a label figure that contradicts the edges fails",
          "must name" in out or "label closes at" in out)
    shutil.rmtree(tmp)

    # 8. the policy assertion: low-end derivation is rejected
    tmp, r = stage(repo)
    low = """const BUDGET_BANDS = [
  { range: 1, label: 'Under $5,000',  min: 0,    max: 4999 },
  { range: 2, label: '$5,000–$5,900', min: 5000, max: 5899 },
  { range: 3, label: '$5,900–$6,900', min: 5900, max: 6899 },
  { range: 4, label: '$6,900–$8,900', min: 6900, max: 8899 },
  { range: 5, label: '$8,900+',       min: 8900, max: null },
];"""
    replace_block(r, low)
    out = run(r)
    check("low-end derived bands fail against the database",
          "no longer sits between" in out)
    shutil.rmtree(tmp)

    # 9. a second copy of the band set
    tmp, r = stage(repo)
    s = read_index(r)
    dupe = "\nconst BUDGET_LABELS_LEGACY = [\n" + "\n".join(lines) + "\n];\n"
    s = s.replace(block, block + dupe, 1)
    write_index(r, s)
    out = run(r)
    check("a second copy of the band set fails", "appears 2 times" in out)
    shutil.rmtree(tmp)

    # 10. renderBudget no longer reads the constant
    tmp, r = stage(repo)
    s = read_index(r)
    s = s.replace("  BUDGET_BANDS.forEach(opt => {",
                  "  [].forEach(opt => {", 1)
    write_index(r, s)
    out = run(r)
    check("renderBudget() not referencing BUDGET_BANDS fails",
          "does not reference BUDGET_BANDS" in out)
    shutil.rmtree(tmp)

    # 11. deleting it entirely must fail loudly, not report clean
    tmp, r = stage(repo)
    s = read_index(r).replace(block, "", 1)
    write_index(r, s)
    out = run(r)
    check("deleting BUDGET_BANDS fails loudly rather than passing",
          "BUDGET_BANDS not found" in out and "0 failures" not in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
