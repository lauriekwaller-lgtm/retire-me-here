#!/usr/bin/env python3
"""
Planted-error test for check_comparison_cta_cost_debt.

    python3 tools/test_comparison_cta_debt.py
    python3 tools/test_comparison_cta_debt.py --repo ..

No check ships without one of these.

This one exists because two repairs are in flight against each other. The
orphaned-CTA item wants CTA blocks added to roughly eleven profiles; the
cost-row item has 69 stale figures quarantined across eighteen comparison
pages. Wiring the first while the second is open sends readers straight into
known-bad money, and neither item's own check can see it: COST_ROW_BASELINE
reads the comparison page, and nothing reads a profile's outbound links.

NOTHING IN THIS FILE IS HARDCODED TO A BASELINE VALUE. The first cut named the
pages and spelled the expected counts as literals, which meant every tier batch
would have broken the harness the moment it lowered a number, and the harness
breaks LOUDLY on the gate. A test that has to be re-cut on every commit it is
watching gets re-cut carelessly. Everything below is derived at run time from
COST_ROW_BASELINE and CTA_COST_DEBT_BASELINE, so the tiers can land without
touching this file at all. The sibling harness
tools/test_comparison_cost_rows.py was pinned this way and did break on Tier 3.

The assertions are about the EDGE COUNT and the RATCHET, and two of them exist
only to pin down what is being counted, because the plausible wrong
implementations both pass a naive test:

    1. the control run is clean, so the check is not merely failing at
       everything
    2. a NEW CTA to a quarantined page fails. This is the whole purpose.
    3. a SECOND CTA to an ALREADY-linked quarantined page fails. Counting
       distinct pages instead of links would pass assertion 2 and miss this,
       and a profile can carry more than one link to the same page.
    4. a RELATIVE href to a quarantined page is counted. Every CTA on the site
       today is written with a leading slash; a matcher that requires one reads
       clean the first time someone writes it the other way.
    5. REMOVING a CTA to a quarantined page fails, demanding the constant be
       lowered. Same argument as COST_ROW_BASELINE: a ratchet that outlives its
       fixes is a number nobody trusts.
    6. adding a CTA to a page NOT in the baseline does NOT fail. The check
       gates debt, not linking; the orphan repair must stay possible on the
       unquarantined pages while this is open.
    7. removing a CTA to a page NOT in the baseline does NOT fail, for the same
       reason from the other direction.

Exit 0 = all tests pass.
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

HREF = re.compile(r'href="/?([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)"')


def load_constants(repo):
    sys.path.insert(0, os.path.join(repo, "tools"))
    import validate                                       # noqa: E402
    return validate.COST_ROW_BASELINE, validate.CTA_COST_DEBT_BASELINE


def profile_links(repo):
    """[(profile_path_relative, comparison_page)] across every profile."""
    out = []
    for path in sorted(glob.glob(os.path.join(repo, "cities", "*", "profile.html"))):
        rel = os.path.relpath(path, repo)
        for page in HREF.findall(open(path, encoding="utf-8").read()):
            out.append((rel, page))
    return out


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="ctadebt-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    # --only superlatives is the group the comparison checks execute under
    # (they report to a group named "comparison"). RMH_IN_HARNESS stops
    # validate.py re-running the harnesses, including this one, from inside a
    # harness.
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".",
         "--only", "superlatives"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def plant(repo, rel, href):
    """Append an anchor to a profile, just inside </body>."""
    path = os.path.join(repo, rel)
    s = open(path, encoding="utf-8").read()
    if "</body>" not in s:
        raise AssertionError(f"no </body> in {rel}")
    open(path, "w", encoding="utf-8").write(
        s.replace("</body>", f'<a href="{href}">planted</a>\n</body>', 1))


def unplant(repo, rel, page):
    """Repoint one CTA at the hub, which is not a comparison page."""
    path = os.path.join(repo, rel)
    s = open(path, encoding="utf-8").read()
    m = re.search(r'href="/?' + re.escape(page) + r'"', s)
    if not m:
        raise AssertionError(f"no link to {page} in {rel}")
    open(path, "w", encoding="utf-8").write(
        s[:m.start()] + 'href="/compare-retirement-cities.html"' + s[m.end():])


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def report():
    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        for n in bad:
            print(f"  failed: {n}")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_comparison_cta_debt")

    quarantined, base = load_constants(repo)
    links = profile_links(repo)

    if not quarantined:
        # The dict is empty, so the check exists only to demand its own
        # deletion. Assert that and stop; there is no debt left to plant.
        tmp, r = stage(repo)
        out = run(r)
        check("with an empty COST_ROW_BASELINE the check demands its own deletion",
              base == 0 or "Delete CTA_COST_DEBT_BASELINE" in out)
        shutil.rmtree(tmp)
        report()
        return

    # A profile that links to a page still in quarantine, and one that links to
    # a page that is not. Both derived, never named.
    dirty = next(((rel, pg) for rel, pg in links if pg in quarantined), None)
    clean = next(((rel, pg) for rel, pg in links if pg not in quarantined), None)
    if not dirty:
        sys.exit("no profile links to a quarantined page; cannot plant "
                 "assertions 3 and 5. Re-derive this harness.")
    if not clean:
        sys.exit("every profile CTA points at a quarantined page; cannot plant "
                 "assertions 6 and 7. Re-derive this harness.")
    dirty_rel, dirty_page = dirty
    clean_rel, clean_page = clean

    # A profile carrying no CTA at all, so a plant there is unambiguously an
    # addition rather than a swap.
    linked = {rel for rel, _ in links}
    empty_rel = next(
        (os.path.relpath(p, repo)
         for p in sorted(glob.glob(os.path.join(repo, "cities", "*", "profile.html")))
         if os.path.relpath(p, repo) not in linked), None)
    if not empty_rel:
        sys.exit("every profile carries a CTA; cannot plant assertions 2, 4, 6.")

    not_quarantined = clean_page
    up, down = f"{base + 1} profile CTA links", f"to {base - 1} in this same commit"

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. a new CTA to a quarantined page
    tmp, r = stage(repo)
    plant(r, empty_rel, f"/{dirty_page}")
    out = run(r)
    check("a new CTA to a quarantined page fails", up in out)
    shutil.rmtree(tmp)

    # 3. links are counted, not pages
    tmp, r = stage(repo)
    plant(r, dirty_rel, f"/{dirty_page}")
    out = run(r)
    check("a second CTA to an already-linked quarantined page fails", up in out)
    shutil.rmtree(tmp)

    # 4. the matcher does not depend on the leading slash
    tmp, r = stage(repo)
    plant(r, empty_rel, dirty_page)
    out = run(r)
    check("a relative href to a quarantined page is counted", up in out)
    shutil.rmtree(tmp)

    # 5. the ratchet's other direction
    tmp, r = stage(repo)
    unplant(r, dirty_rel, dirty_page)
    out = run(r)
    check("removing a CTA to a quarantined page demands a lower baseline",
          "Lower CTA_COST_DEBT_BASELINE" in out and down in out)
    shutil.rmtree(tmp)

    # 6. the orphan repair stays possible on the unquarantined pages
    tmp, r = stage(repo)
    plant(r, empty_rel, f"/{not_quarantined}")
    out = run(r)
    check("adding a CTA to a page not in the baseline does not fail",
          "0 failures" in out)
    shutil.rmtree(tmp)

    # 7. and so does removing one
    tmp, r = stage(repo)
    unplant(r, clean_rel, clean_page)
    out = run(r)
    check("removing a CTA to a page not in the baseline does not fail",
          "0 failures" in out)
    shutil.rmtree(tmp)

    report()


if __name__ == "__main__":
    main()
