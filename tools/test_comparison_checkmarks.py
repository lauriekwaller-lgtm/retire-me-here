#!/usr/bin/env python3
"""
Planted-error test for check_comparison_checkmarks.

    python3 tools/test_comparison_checkmarks.py
    python3 tools/test_comparison_checkmarks.py --repo ..

No check ships without one of these.

This one exists because the numbers were never the problem. On 2026-07-31 every
one of the 200 dimension cells across the twenty comparison pages agreed with
the database, and check_comparison_scores had kept them that way. What had
drifted was the CHECKMARK on top of the number: eight pages marked one-point
gaps, twelve did not, and nothing read a mark at all. A page can be
arithmetically perfect and still tell a reader something the site does not mean.

So the assertions are about the mark, in both directions and on both cells:

    1. marking a single-point gap fails
    2. removing the mark from a two-point gap fails, so the rule is not merely
       "do not over-mark"
    3. moving a mark onto the LOWER score fails
    4. marking both cities fails
    5. shading with no tick character fails
    6. a tick character with no shading fails. Five and six are separate
       assertions because the standard requires both and they break separately:
       the shading is for the reader, the character is for the scrapers.
    7. deleting every dimension row fails LOUDLY rather than reading zero rows
       and reporting clean. This is the failure mode this codebase keeps
       rediscovering.
    8. the control run is clean, so the check is not merely failing at
       everything.

Every planted target is DERIVED from the live pages at run time, never named.
The cost-row harness was pinned to a literal page and a literal figure, and the
batch that repaired that page broke the harness on the gate, which is the worst
place to find out a test is attached to the thing it watches. Nothing here
knows which page it is editing.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROW = (r'<td class="metric">({key}(?![0-9])[^<]*)</td>\s*'
       r'<td class="value([^"]*)">(\d{{1,2}})/10([^<]*)</td>\s*'
       r'<td class="value([^"]*)">(\d{{1,2}})/10([^<]*)</td>')


def _pages(repo):
    hub = open(os.path.join(repo, "compare-retirement-cities.html"),
               encoding="utf-8").read()
    return sorted({f"{a}-vs-{b}-retirement.html" for a, b in re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)})


def _dims(repo):
    sys.path.insert(0, os.path.join(repo, "tools"))
    import validate as V                                      # noqa: E402
    return [k for k, _ in V.DIMS], V.CHECKMARK_MIN_GAP


def _row(html, key):
    """(whole match, gap, [(cell_index, marked, score)]) for one dimension row."""
    m = re.search(ROW.format(key=key), html, re.S)
    if not m:
        return None
    a, b = int(m.group(3)), int(m.group(6))
    cells = [(0, "winner" in m.group(2) or "\u2713" in m.group(4), a),
             (1, "winner" in m.group(5) or "\u2713" in m.group(7), b)]
    return m, abs(a - b), cells


def find(repo, want):
    """
    First (page, key) whose dimension row satisfies want(gap, cells).

    Returns the page and key only. The caller re-reads the staged copy, so a
    match found here is never carried across the copy boundary.
    """
    keys, _ = _dims(repo)
    for page in _pages(repo):
        path = os.path.join(repo, page)
        if not os.path.exists(path):
            continue
        html = open(path, encoding="utf-8").read()
        for key in keys:
            got = _row(html, key)
            if got and want(got[1], got[2]):
                return page, key
    sys.exit("no comparison row matches the shape this harness needs to plant "
             "an error. Re-derive this harness.")


def rewrite(repo, page, key, fn):
    """Rewrite both value cells of a dimension row via fn(cls, score, tail)."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(ROW.format(key=key), s, re.S)
    if not m:
        raise AssertionError(f"no {key} row in {page}")
    a = fn(m.group(2), m.group(3), m.group(4), 0)
    b = fn(m.group(5), m.group(6), m.group(7), 1)
    new = (f'<td class="metric">{m.group(1)}</td>\n'
           f'          <td class="value{a[0]}">{m.group(3)}/10{a[1]}</td>\n'
           f'          <td class="value{b[0]}">{m.group(6)}/10{b[1]}</td>')
    open(path, "w", encoding="utf-8").write(s[:m.start()] + new + s[m.end():])


def plain(cls, score, tail, which):
    return "", ""


def marked(which_cell):
    def fn(cls, score, tail, which):
        return (" winner", " \u2713") if which == which_cell else ("", "")
    return fn


def half(shaded_only, which_cell):
    def fn(cls, score, tail, which):
        if which != which_cell:
            return "", ""
        return (" winner", "") if shaded_only else ("", " \u2713")
    return fn


def both(cls, score, tail, which):
    return " winner", " \u2713"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="checkmarks-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    # --only superlatives is the group the comparison checks execute under; they
    # report to a group named "comparison". RMH_IN_HARNESS stops validate.py
    # re-running the harnesses from inside a harness.
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".",
         "--only", "superlatives"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_checkmarks")

    _, min_gap = _dims(repo)

    # A near-tie that is currently unmarked, and a real gap that is currently
    # marked. Both are derived, so any page may play either part.
    near_page, near_key = find(
        repo, lambda gap, cells: gap == min_gap - 1
        and not any(c[1] for c in cells))
    wide_page, wide_key = find(
        repo, lambda gap, cells: gap >= min_gap and any(c[1] for c in cells))

    # 8. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1. marking a near-tie
    tmp, r = stage(repo)
    rewrite(r, near_page, near_key, marked(0))
    out = run(r)
    check("marking a single-point gap fails",
          near_key in out and "near-ties" in out)
    shutil.rmtree(tmp)

    # 2. unmarking a real gap
    tmp, r = stage(repo)
    rewrite(r, wide_page, wide_key, plain)
    out = run(r)
    check("removing the mark from a two-point gap fails",
          wide_key in out and "neither cell" in out)
    shutil.rmtree(tmp)

    # 3. the mark on the weaker city
    tmp, r = stage(repo)
    html = open(os.path.join(r, wide_page), encoding="utf-8").read()
    _, _, cells = _row(html, wide_key)
    lo = 0 if cells[0][2] < cells[1][2] else 1
    rewrite(r, wide_page, wide_key, marked(lo))
    out = run(r)
    check("a mark on the lower score fails", "WEAKER" in out)
    shutil.rmtree(tmp)

    # 4. both cities marked
    tmp, r = stage(repo)
    rewrite(r, wide_page, wide_key, both)
    out = run(r)
    check("marking both cities fails", "BOTH" in out)
    shutil.rmtree(tmp)

    # 5 and 6. half a mark, each way round
    hi = 1 - lo
    tmp, r = stage(repo)
    rewrite(r, wide_page, wide_key, half(True, hi))
    out = run(r)
    check("shading with no tick character fails", "carries no tick" in out)
    shutil.rmtree(tmp)

    tmp, r = stage(repo)
    rewrite(r, wide_page, wide_key, half(False, hi))
    out = run(r)
    check("a tick character with no shading fails", "not shaded" in out)
    shutil.rmtree(tmp)

    # 7. no rows at all must fail loudly, never read zero and report clean
    tmp, r = stage(repo)
    path = os.path.join(r, near_page)
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'<tr>\s*<td class="metric">D\d+[^<]*</td>.*?</tr>', "", s,
               flags=re.S)
    open(path, "w", encoding="utf-8").write(s)
    out = run(r)
    check("deleting every dimension row fails loudly",
          "not one D1-D10 row was readable" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
