#!/usr/bin/env python3
"""
Planted-error test for check_comparison_cta_reciprocity.

    python3 tools/test_comparison_cta_reciprocity.py
    python3 tools/test_comparison_cta_reciprocity.py --repo ..

No check ships without one of these.

The check asserts an EDGE, not a value, which makes it a different shape of test
from the rest of this directory. Everything else here plants a wrong number in a
page and reads the complaint. There is no number to corrupt in a hyperlink: it is
either there in the one form the site uses, or it is not, and the interesting
failures are all the ways markup can look like a link and not be one.

    1. removing one profile's CTA fails, and names that profile
    2. removing the OTHER profile's CTA fails too. The two ends are read
       independently, which is the whole point: nashville-vs-memphis sat linked
       from one side and not the other for four days and read as done from
       whichever end you opened.
    3. a DIFFERENT and perfectly valid comparison CTA does not satisfy the
       missing one, and does not raise a dead-link failure on its way past
    4. a relative href does not count. It resolves for a reader; one absolute
       form site-wide is what makes this greppable at all
    5. data-href="/page" does not count. A bare substring test for href="/page"
       is satisfied by that string, so the check would pass on markup that links
       nothing. This assertion exists because the first draft had that bug
    6. a profile linking a comparison page that does not exist fails. This is
       the rename case, and nothing else on the gate reads it
    7. an empty hub fails rather than reporting a clean zero
    8. the control run is clean

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
    tmp = tempfile.mkdtemp(prefix="cta-recip-")
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


def a_pair(repo):
    """
    First hub-listed page whose two profiles each link it exactly once, with a
    second page available to swap in. Derived at runtime, never named: these
    batches keep retiring whichever page a harness hardcodes.
    """
    hub = open(os.path.join(repo, "compare-retirement-cities.html"),
               encoding="utf-8").read()
    found = sorted(set(re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)))
    if len(found) < 2:
        sys.exit("fewer than two comparison pages on the hub. Re-derive this "
                 "harness.")
    for a, b in found:
        page = f"{a}-vs-{b}-retirement.html"
        paths = [os.path.join(repo, "cities", s, "profile.html") for s in (a, b)]
        if not all(os.path.exists(p) for p in paths):
            continue
        counts = [open(p, encoding="utf-8").read().count(f'href="/{page}"')
                  for p in paths]
        if counts == [1, 1]:
            spare = next(f"{x}-vs-{y}-retirement.html" for x, y in found
                         if f"{x}-vs-{y}-retirement.html" != page)
            return a, b, page, spare
    sys.exit("no comparison page is linked exactly once from each of its two "
             "profiles. Re-derive this harness.")


def edit(repo, rel, pattern, replacement, expect=1):
    path = os.path.join(repo, rel)
    s = open(path, encoding="utf-8").read()
    out, n = re.subn(pattern, replacement, s)
    if n != expect:
        raise AssertionError(
            f"{rel}: pattern {pattern!r} matched {n} times, expected {expect}")
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

    print("test_comparison_cta_reciprocity")
    a, b, page, spare = a_pair(repo)
    prof_a = f"cities/{a}/profile.html"
    prof_b = f"cities/{b}/profile.html"
    HREF = re.escape(f'href="/{page}"')

    # 8. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 1. one side missing
    tmp, r = stage(repo)
    edit(r, prof_a, HREF, 'href="/"')
    out = run(r)
    check("a profile with no CTA to the page that compares it fails",
          f"{prof_a} carries no CTA to /{page}" in out)
    shutil.rmtree(tmp)

    # 2. the other side missing
    tmp, r = stage(repo)
    edit(r, prof_b, HREF, 'href="/"')
    out = run(r)
    check("the second profile is read independently of the first",
          f"{prof_b} carries no CTA to /{page}" in out)
    shutil.rmtree(tmp)

    # 3. a different, valid comparison CTA does not stand in
    tmp, r = stage(repo)
    edit(r, prof_a, HREF, f'href="/{spare}"')
    out = run(r)
    check("an unrelated comparison CTA does not satisfy the missing one",
          f"{prof_a} carries no CTA to /{page}" in out)
    check("swapping in a page that exists raises no dead-link failure",
          f"links /{spare}, which does not exist" not in out)
    shutil.rmtree(tmp)

    # 4. relative href
    tmp, r = stage(repo)
    edit(r, prof_a, HREF, f'href="{page}"')
    out = run(r)
    check("a relative href does not count as a CTA",
          f"{prof_a} carries no CTA to /{page}" in out)
    shutil.rmtree(tmp)

    # 5. the substring trap
    tmp, r = stage(repo)
    edit(r, prof_a, HREF, f'data-href="/{page}"')
    out = run(r)
    check("data-href carrying the same string does not count as a CTA",
          f"{prof_a} carries no CTA to /{page}" in out)
    shutil.rmtree(tmp)

    # 6. a link to a page that does not exist
    tmp, r = stage(repo)
    edit(r, prof_a, HREF, f'href="/{a}-vs-nowhere-retirement.html"')
    out = run(r)
    check("a CTA to a comparison page that does not exist fails",
          f"links /{a}-vs-nowhere-retirement.html, which does not exist" in out)
    shutil.rmtree(tmp)

    # 7. silent no-op guard
    tmp, r = stage(repo)
    hub = os.path.join(r, "compare-retirement-cities.html")
    s = open(hub, encoding="utf-8").read()
    s = re.sub(r"[a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html", "matchup.html", s)
    open(hub, "w", encoding="utf-8").write(s)
    out = run(r)
    check("an empty hub fails rather than reporting a clean zero",
          "check_comparison_cta_reciprocity verified nothing" in out)
    shutil.rmtree(tmp)

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


if __name__ == "__main__":
    main()
