#!/usr/bin/env python3
"""
Planted-error test for check_comparison_prose_scores.

    python3 tools/test_comparison_prose_scores.py
    python3 tools/test_comparison_prose_scores.py --repo ..

No check ships without one of these.

This check exists because eleven live contradictions between a comparison page's
prose and its own table were found in four days, every one on D2, while
check_comparison_scores read those same rows and passed. A checked number
restated in prose is an unchecked number.

The assertions are shaped by how the check can fail, which is mostly by matching
too much:

    1. a wrong score in the "KEYWORD scores N to M" shape fails
    2. a wrong score in the parenthetical "KEYWORD (N vs. M)" shape fails
    3. a wrong score in the "KEYWORD at N of 10 against M" shape fails
    4. a CORRECT restatement in each shape passes, so the check is not merely
       failing at everything with a number in it
    5. "budget tier 3 of 5" does NOT fail, though 3 and 5 are rarely the D2 row.
       The tier field is 1-5 and the dimension is 1-10; conflating them would
       fire on nearly every page.
    6. a number pair belonging to a NEIGHBOURING dimension does not bind to this
       one. This is the assertion that matters most. A first cut of the check
       used a proximity window and flagged 219 claims across 20 pages, nearly all
       of them the next dimension in a list like "taxes (8 of 10 vs. 5),
       healthcare (8 vs. 7)". Adjacency is the whole design.
    7. deleting every dimension row fails LOUDLY rather than reading zero rows
       and reporting clean.
    8. the control run is clean.

Targets are DERIVED at run time, never named, for the reason recorded twice in
test_comparison_cost_rows: a harness pinned to a page breaks when a batch edits
that page, and it breaks on the gate.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _validate(repo):
    sys.path.insert(0, os.path.join(repo, "tools"))
    import validate as V                                      # noqa: E402
    return V


def pages(repo):
    hub = open(os.path.join(repo, "compare-retirement-cities.html"),
               encoding="utf-8").read()
    return sorted(set(re.findall(
        r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)))


def row(repo, page, key):
    html = open(os.path.join(repo, page), encoding="utf-8").read()
    m = re.search(
        rf'<td class="metric">{key}(?![0-9])[^<]*</td>\s*'
        rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>\s*'
        rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>',
        html, re.S)
    return (int(m.group(1)), int(m.group(2))) if m else None


def pick(repo, want_gap=True):
    """
    A (page, key, word, a, b) whose two scores DIFFER, so a planted wrong number
    is unambiguous, and whose dimension word is one the check knows.
    """
    V = _validate(repo)
    for page in pages(repo):
        for key, words in V.PROSE_DIMS:
            got = row(repo, page, key)
            if not got:
                continue
            a, b = got
            if (a != b) == want_gap and 1 < a < 10 and 1 < b < 10:
                word = {"D1": "airport access", "D2": "budget",
                        "D3": "healthcare", "D4": "climate resilience",
                        "D5": "taxes", "D6": "walkability",
                        "D7": "outdoor recreation", "D8": "active wellness",
                        "D9": "safety", "D10": "community"}[key]
                return page, key, word, a, b
    sys.exit("no comparison row has the shape this harness needs. Re-derive it.")


def inject(repo, page, sentence):
    """Drop a sentence into the page's first tradeoff paragraph."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<p class="tradeoff-p">', s)
    if not m:
        m = re.search(r"<p[^>]*>", s)
    if not m:
        raise AssertionError(f"no paragraph to inject into on {page}")
    open(path, "w", encoding="utf-8").write(
        s[:m.end()] + " " + sentence + " " + s[m.end():])


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="prosescores-")
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


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_prose_scores")

    page, key, word, a, b = pick(repo)
    wrong = 1 if a != 1 and b != 1 else 10          # a score neither city holds

    # 8. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1-3. the three shapes, each with a wrong number
    for label, sentence in (
        ("scores N to M", f"{word} scores {wrong} to {b}."),
        ("parenthetical (N vs. M)", f"{word} ({wrong} vs. {b})."),
        ("at N of 10 against M", f"{word} at {wrong} of 10 against {b}."),
    ):
        tmp, r = stage(repo)
        inject(r, page, sentence)
        out = run(r)
        check(f"a wrong score in the \"{label}\" shape fails",
              "restated in prose" in out and key in out)
        shutil.rmtree(tmp)

    # 4. the same three shapes with the RIGHT numbers must pass
    tmp, r = stage(repo)
    for sentence in (f"{word} scores {a} to {b}.",
                     f"{word} ({a} vs. {b}).",
                     f"{word} at {a} of 10 against {b}."):
        inject(r, page, sentence)
    out = run(r)
    check("correct restatements pass in all three shapes", "0 failures" in out)
    shutil.rmtree(tmp)

    # 5. the 1-5 budget tier field must not be read as a 1-10 score
    tmp, r = stage(repo)
    inject(r, page, "It sits at budget tier 3 of 5 against 1.")
    out = run(r)
    check("\"budget tier 3 of 5\" is not read as a D2 score",
          "0 failures" in out)
    shutil.rmtree(tmp)

    # 6. a neighbouring dimension's pair must not bind to this one
    other = "safety" if word != "safety" else "walkability"
    okey = "D9" if word != "safety" else "D6"
    og = row(repo, page, okey)
    tmp, r = stage(repo)
    inject(r, page, f"{word} ({a} vs. {b}), {other} ({og[0]} vs. {og[1]}).")
    out = run(r)
    check("a neighbouring dimension's numbers do not bind to this one",
          "0 failures" in out)
    shutil.rmtree(tmp)

    # 7. no rows at all must fail loudly
    tmp, r = stage(repo)
    path = os.path.join(r, "compare-retirement-cities.html")
    s = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(
        re.sub(r"[a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html", "gone.html", s))
    out = run(r)
    check("reading zero comparison pages fails loudly",
          "verified nothing" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
