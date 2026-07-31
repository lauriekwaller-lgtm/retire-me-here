#!/usr/bin/env python3
"""
Planted-error test for check_hardcoded_counts.

    python3 tools/test_hardcoded_counts.py
    python3 tools/test_hardcoded_counts.py --repo ..

The check predates this harness and had no test, which is a large part of why it
sat shipped and passing while 23 violations of its own rule were live. It was
blind three separate ways at once, and each of those three is an assertion here.

    1. the SPELLING: "100-city database", the adjectival form. The original
       pattern matched "100 cities" only, and every one of the 23 live instances
       used the hyphen.
    2. the PAGE SET: a violation planted on pick-and-compare.html fails. The
       check read index, the profiles, and the comparison pages linked from the
       hub, which silently excluded the hub itself, the picker and the quiz.
       Twelve of the 23 were on exactly those three pages.
    3. the SURFACE: a violation planted in a <meta ... content="..."> attribute
       fails. visible_text() strips whole tags and script_strings() only reads
       <script>, so nothing on the site had ever read a description attribute.
       Four of the 23 lived there.
    4. the original spelling still fails, so widening the pattern did not lose
       what it already caught.
    5. a violation on a city profile still fails, same reason.
    6. "99-city" fails too. Correct today, wrong on the next city added; the
       policy is no number, not the right number.
    7. reading no pages fails loudly rather than reporting clean.
    8. the control run is clean.

Targets are derived, not named, except pick-and-compare.html and the profile,
which ARE the thing being asserted about coverage and so cannot be derived
without asserting nothing.

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
    tmp = tempfile.mkdtemp(prefix="counts-")
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


def a_profile(repo):
    base = os.path.join(repo, "cities")
    for slug in sorted(os.listdir(base)):
        p = os.path.join("cities", slug, "profile.html")
        if os.path.exists(os.path.join(repo, p)):
            return p
    sys.exit("no city profile found. Re-derive this harness.")


def a_comparison(repo):
    hub = open(os.path.join(repo, "compare-retirement-cities.html"),
               encoding="utf-8").read()
    found = sorted(set(re.findall(
        r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)))
    if not found:
        sys.exit("no comparison pages on the hub. Re-derive this harness.")
    return found[0]


def inject_body(repo, page, text):
    """Put a phrase into visible copy."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<p[^>]*>", s)
    if not m:
        raise AssertionError(f"no paragraph on {page}")
    open(path, "w", encoding="utf-8").write(
        s[:m.end()] + " " + text + " " + s[m.end():])


def inject_meta(repo, page, text):
    """Put a phrase into a meta description attribute."""
    path = os.path.join(repo, page)
    s = open(path, encoding="utf-8").read()
    m = re.search(r'(<meta[^>]*name="description"[^>]*content=")', s)
    if not m:
        m = re.search(r'(<meta[^>]*property="og:description"[^>]*content=")', s)
    if not m:
        raise AssertionError(f"no description meta tag on {page}")
    open(path, "w", encoding="utf-8").write(
        s[:m.end()] + text + " " + s[m.end():])


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_hardcoded_counts")
    profile = a_profile(repo)
    comparison = a_comparison(repo)

    # 8. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1. the hyphenated spelling
    tmp, r = stage(repo)
    inject_body(r, comparison, "Scored across our 100-city database.")
    out = run(r)
    check("the adjectival \"100-city\" fails", "100-city" in out)
    shutil.rmtree(tmp)

    # 4. the original spelling
    tmp, r = stage(repo)
    inject_body(r, comparison, "Scored across 100 cities.")
    out = run(r)
    check("the original \"100 cities\" still fails", "100 cities" in out)
    shutil.rmtree(tmp)

    # 6. a count that is correct today
    tmp, r = stage(repo)
    inject_body(r, comparison, "Scored across our 99-city database.")
    out = run(r)
    check("\"99-city\" fails even though it is correct today", "99-city" in out)
    shutil.rmtree(tmp)

    # 2. the page set: the picker was never read
    tmp, r = stage(repo)
    inject_body(r, "pick-and-compare.html", "Drawn from our 100-city database.")
    out = run(r)
    check("a count on pick-and-compare.html fails",
          "pick-and-compare.html" in out and "100-city" in out)
    shutil.rmtree(tmp)

    # 2b. and neither was the hub itself
    tmp, r = stage(repo)
    inject_body(r, "compare-retirement-cities.html",
                "Drawn from our 100-city database.")
    out = run(r)
    check("a count on the comparison hub itself fails",
          "compare-retirement-cities.html" in out)
    shutil.rmtree(tmp)

    # 3. the surface: meta description attributes were never read
    tmp, r = stage(repo)
    inject_meta(r, comparison, "Our 100-city database.")
    out = run(r)
    check("a count in a meta description attribute fails", "100-city" in out)
    shutil.rmtree(tmp)

    # 5. profiles
    tmp, r = stage(repo)
    inject_body(r, profile, "One of our 100-city database entries.")
    out = run(r)
    check("a count on a city profile fails", profile in out)
    shutil.rmtree(tmp)

    # 7. reading nothing must fail loudly
    tmp, r = stage(repo)
    path = os.path.join(r, "tools", "validate.py")
    s = open(path, encoding="utf-8").read()
    s = s.replace('    pages = {"index.html": idx}\n'
                  '    for slug in slug_to_city:\n'
                  '        h = fetch(f"cities/{slug}/profile.html", local)\n'
                  '        if h:\n'
                  '            pages[f"cities/{slug}/profile.html"] = h\n',
                  '    pages = {}\n'
                  '    slug_to_city = {}\n', 1)
    s = s.replace('    standalone = ["compare-retirement-cities.html", "pick-and-compare.html",\n'
                  '                  "where-should-i-retire-quiz.html"]\n',
                  '    standalone = []\n', 1)
    s = s.replace('    hub = fetch("compare-retirement-cities.html", local) or ""\n'
                  '    # The hub, the picker and the quiz are the three highest-traffic pages that\n'
                  '    # make this claim, and none of them was being read.\n',
                  '    hub = ""\n', 1)
    open(path, "w", encoding="utf-8").write(s)
    out = run(r)
    check("reading fewer than two pages fails loudly",
          "counted nothing rather than finding nothing" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
