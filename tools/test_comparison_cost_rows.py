#!/usr/bin/env python3
"""
Planted-error test for check_comparison_cost_rows and the dimension-label fix.

    python3 tools/test_comparison_cost_rows.py
    python3 tools/test_comparison_cost_rows.py --repo ..

No check ships without one of these.

This one exists because the fault was not a wrong number in a checked place. On
2026-07-30 an audit of all twenty comparison pages found 69 figures disagreeing
with the database, and the gate had been printing 0 failures over every one of
them. Every mismatch sat in Typical home value, Estimated retiree budget or
Budget tier. NOT ONE was in D1-D10, because check_comparison_scores reads those
rows and had kept them correct across all twenty pages.

So the assertions are about COVERAGE and about the RATCHET, not about one
direction of error:

    1. a wrong home value on a clean page fails
    2. a wrong monthly estimate on a clean page fails
    3. a wrong budget tier on a clean page fails
    4. FIXING a mismatch on a quarantined page fails, demanding the baseline be
       lowered. A quarantine list that outlives its fixes is an exemption, and
       this is the assertion that stops COST_ROW_BASELINE becoming permanent.
    5. ADDING a mismatch to a quarantined page fails, so quarantine is not a
       licence to keep breaking that page
    6. deleting the cost rows entirely fails LOUDLY rather than reading zero
       rows and reporting clean. This is the failure mode this codebase keeps
       rediscovering.
    7. a planted D8 error fails. D4, D8 and D10 were skipped on every page for
       the whole life of check_comparison_scores because it matched on the DIMS
       label as a prefix and "D8 Wellness" is not a prefix of "D8 Active
       wellness". This assertion guards the fix.
    8. the control run is clean, so the check is not merely failing at
       everything.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# A page with zero cost mismatches, used for the "clean page breaks" assertions.
# Safe to name: it is not in COST_ROW_BASELINE and nothing in the repair plan
# puts it there. Asserted below anyway.
CLEAN_PAGE = "st-augustine-vs-pensacola-retirement.html"

# The quarantined page used by the ratchet assertions is DERIVED, never named.
# It used to be a literal, `asheville-vs-greenville`, alongside a literal
# `$464,000` as its correct home value. Tier 3 of the cost-figure repair took
# that page out of quarantine and this harness failed on the gate, which is the
# worst place to discover that a test is pinned to the thing it is watching.
# Every tier batch would have done it again. Derived from COST_ROW_BASELINE and
# the database at run time, the tiers can land without touching this file.


def _rows(repo, page, db_by_slug):
    """[(label, which, shown, truth, ok)] for every cost cell on a page."""
    sys.path.insert(0, os.path.join(repo, "tools"))
    import validate as V                                    # noqa: E402
    html = open(os.path.join(repo, page), encoding="utf-8").read()
    a_slug, b_slug = page.replace("-retirement.html", "").split("-vs-")
    a, b = db_by_slug.get(a_slug), db_by_slug.get(b_slug)
    out = []
    for labels in (V.HOME_LABELS, (V.MONTHLY_LABEL,), (V.TIER_LABEL,)):
        for lab in labels:
            cells = V._cost_row(html, lab)
            if cells:
                break
        if not cells:
            continue
        for which, (shown, row) in enumerate(((cells[0], a), (cells[1], b))):
            if row is None:
                continue
            if lab in V.HOME_LABELS:
                truth = str(row.get("home_raw", "")).strip()
                ok = re.sub(r"[^$0-9,]", "", shown) == truth
            elif lab == V.MONTHLY_LABEL:
                truth = str(row.get("monthly", "")).strip()
                ok = V._dashes(shown) == V._dashes(truth)
            else:
                truth = f"{row.get('range')} of 5"
                ok = re.sub(r"[^0-9]", "", shown.split("of")[0]) == str(row.get("range"))
            out.append((lab, which, shown, truth, ok))
    return out


def _wrong_value(label, truth):
    """A value guaranteed to disagree with the database, for the given row."""
    if label.startswith("Typical home value"):
        return "$1"
    if label.startswith("Estimated retiree budget"):
        return "$1\u2013$2/mo"
    return "5 of 5" if not truth.startswith("5") else "1 of 5"


def pick_dirty(repo):
    """
    A quarantined page carrying BOTH a wrong cell and a right one.

    The wrong one is set correct, which must demand the baseline be lowered.
    The right one is broken, which must fail as new drift. A page with only one
    kind cannot carry both assertions.
    """
    sys.path.insert(0, os.path.join(repo, "tools"))
    import validate as V                                    # noqa: E402
    db = V.load_db(os.path.join(repo, V.DEFAULT_DB))
    by_slug = {}
    for key, row in db.items():
        if row is None or "_" not in key:
            continue
        name = str(row.get("city", ""))
        by_slug[name.lower().replace(" ", "-").replace(".", "")] = row

    if CLEAN_PAGE in V.COST_ROW_BASELINE:
        sys.exit(f"{CLEAN_PAGE} is quarantined; it cannot carry the clean-page "
                 f"assertions. Re-derive this harness.")

    for page in sorted(V.COST_ROW_BASELINE):
        rows = _rows(repo, page, by_slug)
        bad = [r for r in rows if not r[4]]
        good = [r for r in rows if r[4]]
        if bad and good:
            fix = bad[0]
            brk = good[0]
            return (page,
                    (fix[0], fix[1], fix[3]),
                    (brk[0], brk[1], _wrong_value(brk[0], brk[3])))
    sys.exit("no quarantined page carries both a wrong cell and a right one; "
             "the ratchet assertions cannot be planted. Re-derive this harness.")


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="costrow-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    # --only superlatives keeps this to the group that RUNS the comparison checks (they report to a
    # group named "comparison" but execute under "superlatives"), and RMH_IN_HARNESS
    # stops validate.py re-running the harnesses (including this one) from
    # inside a harness. Without both, each assertion re-runs the whole suite.
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".",
         "--only", "superlatives"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def edit(repo, page, old, new):
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    if old not in s:
        raise AssertionError(f"anchor not found in {page}: {old[:70]!r}")
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))


def cell(repo, page, label, which, replacement):
    """Rewrite one value cell of a metric row. which = 0 or 1."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(
        r'<td class="metric">' + re.escape(label) + r"</td>\s*"
        r'<td class="value[^"]*">([^<]*)</td>\s*'
        r'<td class="value[^"]*">([^<]*)</td>',
        s, re.S)
    if not m:
        raise AssertionError(f"no {label!r} row in {page}")
    span = m.span(which + 1)
    open(path, "w", encoding="utf-8").write(s[:span[0]] + replacement + s[span[1]:])


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_cost_rows")

    # 8. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1. wrong home value on a clean page
    tmp, r = stage(repo)
    cell(r, CLEAN_PAGE, "Typical home value", 0, "$999,000")
    out = run(r)
    check("wrong home value on a clean page fails",
          "typical home" in out and "999,000" in out)
    shutil.rmtree(tmp)

    # 2. wrong monthly estimate
    tmp, r = stage(repo)
    cell(r, CLEAN_PAGE, "Estimated retiree budget", 1, "$1,000\u2013$2,000/mo")
    out = run(r)
    check("wrong retiree budget on a clean page fails", "retiree budget" in out)
    shutil.rmtree(tmp)

    # 3. wrong budget tier
    tmp, r = stage(repo)
    cell(r, CLEAN_PAGE, "Budget tier (1 = least expensive)", 0, "5 of 5")
    out = run(r)
    check("wrong budget tier on a clean page fails", "budget tier" in out)
    shutil.rmtree(tmp)

    # 4. the ratchet: fixing a quarantined page must demand a lower baseline
    dirty_page, (fix_lab, fix_which, fix_val), (brk_lab, brk_which, brk_val) = \
        pick_dirty(repo)
    tmp, r = stage(repo)
    cell(r, dirty_page, fix_lab, fix_which, fix_val)          # correct value
    out = run(r)
    check("fixing a quarantined page fails until the baseline is lowered",
          "Lower COST_ROW_BASELINE" in out)
    shutil.rmtree(tmp)

    # 5. quarantine is not a licence to break the page further
    tmp, r = stage(repo)
    cell(r, dirty_page, brk_lab, brk_which, brk_val)
    out = run(r)
    check("adding a mismatch to a quarantined page fails",
          "got WORSE" in out)
    shutil.rmtree(tmp)

    # 6. no rows at all must fail loudly, never read zero and report clean
    tmp, r = stage(repo)
    path = os.path.join(r, CLEAN_PAGE)
    s = open(path, encoding="utf-8").read()
    for lab in ("Typical home value", "Estimated retiree budget",
                "Budget tier (1 = least expensive)"):
        s = re.sub(
            r'<tr>\s*<td class="metric">' + re.escape(lab) + r"</td>.*?</tr>",
            "", s, count=1, flags=re.S)
    open(path, "w", encoding="utf-8").write(s)
    out = run(r)
    check("deleting every cost row fails loudly", "no cost rows found" in out)
    shutil.rmtree(tmp)

    # 7. D8 is now actually read
    tmp, r = stage(repo)
    cell(r, CLEAN_PAGE, "D8 Active wellness", 0, "1/10")
    out = run(r)
    check("a planted D8 error fails (guards the label fix)",
          "D8" in out and "1/10" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
