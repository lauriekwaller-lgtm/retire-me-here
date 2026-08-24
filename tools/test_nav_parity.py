#!/usr/bin/env python3
"""
Planted-error test for check_nav_parity in validate.py.

    python3 tools/test_nav_parity.py            # against this checkout
    python3 tools/test_nav_parity.py --repo ..  # against another checkout

No check ships without one of these. This one exists because the defect it
guards against was invisible for months: the site had EIGHT distinct navs across
100 pages and every single page looked fine on its own. Nothing compared them,
so nothing was wrong anywhere in particular.

The plants are the ways the ninth variant could arrive, plus the ways this check
could look like it was working when it was not:

    1. the control run is clean, so the check is not merely failing at everything
    2. a page missing a nav item fails, which is the defect that shipped:
       where-can-i-afford-to-retire.html was in the menu on 2 pages out of 98
    3. the failure NAMES the page and the offending line. "Some nav is wrong"
       across 98 pages is how this went unnoticed in the first place
    4. an EXTRA item fails too, not just a missing one. A page quietly growing a
       link the rest of the site does not have is the same defect running the
       other way, and a contains-all-canonical-links check would pass it
    5. REORDERED lines fail. Set equality would call a reshuffled menu identical,
       and the eight real variants would have passed such a check the moment
       their link lists converged
    6. changing a LABEL fails while the href stays put, because the nav is
       compared as markup and not as a list of destinations
    7. index.html's exemption is real but narrow: it passes with its own markup,
       and FAILS when its destinations drift from everyone else's. An exemption
       that accepted anything would be a hole exactly where the homepage is
    8. a 53rd component-less page FAILS, since that is the ninth variant being
       born. This is the one that actually stops the recurrence
    9. removing a page's component (52 -> 53 stubs) is caught by the same count
   10. a MISSING tools/nav_canonical.html fails loudly. A check whose reference
       file has been deleted must not quietly compare every page to nothing
   11. an EMPTY canonical fails loudly, for the same reason: a <nav> with no
       links would let all 46 pages pass while asserting nothing
   12. a sitemap with no pages fails rather than checking zero navs

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _nav_stub_expected():
    """Read NAV_STUB_EXPECTED out of validate.py, by text.

    Deliberately not `import validate`: that module runs a real gate on import
    in some paths, and the harness must stay cheap and side-effect free.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate.py")
    with open(path, encoding="utf-8") as fh:
        m = re.search(r"^NAV_STUB_EXPECTED\s*=\s*(\d+)", fh.read(), re.M)
    if not m:
        raise SystemExit("NAV_STUB_EXPECTED not found in validate.py; the "
                         "harness cannot assert against a number it cannot read")
    return int(m.group(1))

# Two ordinary component pages. Neither is index.html, whose exemption is its
# own case, and neither is a city profile, which has no component at all.
PAGE = "wellness-blueprint.html"
OTHER = "top-cities-for-hikers.html"

NAV_RE = re.compile(r"<nav\b.*?</nav>", re.S | re.I)


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="rmh-nav-")
    dest = os.path.join(tmp, "repo")
    # Images excluded for speed only: this file stages twelve times and no nav
    # check will ever open a JPEG.
    shutil.copytree(repo, dest,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc",
                                                  "*.jpg", "*.jpeg", "*.png",
                                                  "*.webp", "*.pdf", "*.ico"))
    return dest


def run(tmp):
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "nav"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def read(tmp, rel):
    with open(os.path.join(tmp, rel), encoding="utf-8") as fh:
        return fh.read()


def write(tmp, rel, body):
    with open(os.path.join(tmp, rel), "w", encoding="utf-8") as fh:
        fh.write(body)


def edit_nav(tmp, rel, fn):
    """Replace rel's <nav> with fn(nav)."""
    html = read(tmp, rel)
    m = NAV_RE.search(html)
    if not m:
        raise SystemExit(f"harness setup error: {rel} has no <nav>")
    write(tmp, rel, html[:m.start()] + fn(m.group(0)) + html[m.end():])


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: nav parity\n")

    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a site whose navs all match the canonical passes",
          code == 0 and not base, f"{len(base)} failure(s)")

    def plant(fn):
        t = stage(repo)
        fn(t)
        c, f = run(t)
        shutil.rmtree(os.path.dirname(t))
        return c, f - base

    # ------------------------------------------------ 2 + 3. a missing item
    def drop_item(t):
        edit_nav(t, PAGE, lambda n: re.sub(
            r'\n[^\n]*href="/where-can-i-afford-to-retire\.html"[^\n]*', "", n))
    code, added = plant(drop_item)
    hit = [f for f in added if PAGE in f and "missing" in f]
    check("a nav missing a canonical item fails (the defect that shipped)",
          code == 1 and bool(hit), f"{len(added)} new failure(s)")
    check("the failure names the page and the missing line",
          bool(hit) and "where-can-i-afford" in hit[0],
          hit[0][:96] if hit else "no matching failure")

    # ---------------------------------------------------- 4. an extra item
    def add_item(t):
        edit_nav(t, PAGE, lambda n: n.replace(
            "</nav>", '<a href="/secret-page.html">Secret</a>\n</nav>'))
    code, added = plant(add_item)
    check("a nav with an item nobody else has fails",
          code == 1 and any(PAGE in f and "not in" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------ 5. reordering
    def reorder(t):
        def swap(n):
            a = '<a href="/compare-retirement-cities.html">Compare Cities</a>'
            b = '<a href="/visit-before-you-decide.html">Plan a Visit</a>'
            return n.replace(a + "\n" + b, b + "\n" + a)
        edit_nav(t, PAGE, swap)
    code, added = plant(reorder)
    check("reordered nav lines fail (set equality would pass this)",
          code == 1 and any(PAGE in f and "different order" in f for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------------------------------- 6. label-only change
    def relabel(t):
        edit_nav(t, PAGE, lambda n: n.replace(
            ">Plan a Visit<", ">Visit First<"))
    code, added = plant(relabel)
    check("a changed label fails even though the href is unchanged",
          code == 1 and any(PAGE in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------- 7. the index.html exemption
    def index_drift(t):
        edit_nav(t, "index.html", lambda n: re.sub(
            r'\n[^\n]*href="/visit-before-you-decide\.html"[^\n]*', "", n))
    code, added = plant(index_drift)
    check("index.html fails when ITS destinations drift, exemption or not",
          code == 1 and any("index.html" in f and "visit-before-you-decide" in f
                            for f in added),
          f"{len(added)} new failure(s)")

    def index_untouched(t):
        pass
    code, added = plant(index_untouched)
    check("index.html passes with its own JS-driven markup",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ------------------------------------------ 8 + 9. a 53rd stub page
    def new_stub(t):
        edit_nav(t, OTHER, lambda n: '<nav class="header-nav">\n'
                                     '<a href="/">Home</a>\n</nav>')
    code, added = plant(new_stub)
    # The expected count is read from validate.py rather than written here as a
    # literal. It was "up from the 52" until BATCH B shipped its first profile
    # and the counter ratcheted to 51, at which point this plant still detected
    # the defect correctly but failed on the wording. A debt counter that is
    # designed to move cannot be asserted against a frozen number, and it goes
    # to 0 when BATCH B finishes.
    expected = _nav_stub_expected()
    check(f"one more component-less page than the expected {expected} fails "
          f"(the ninth variant)",
          code == 1 and any(f"up from the {expected}" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------- 10 + 11. the canonical reference
    def no_canon(t):
        os.remove(os.path.join(t, "tools", "nav_canonical.html"))
    code, added = plant(no_canon)
    check("a missing tools/nav_canonical.html fails loudly",
          code == 1 and any("is missing" in f for f in added),
          f"{len(added)} new failure(s)")

    def empty_canon(t):
        write(t, "tools/nav_canonical.html",
              '<nav class="header-nav">\n<a href="/">Home</a>\n</nav>\n')
    code, added = plant(empty_canon)
    check("a canonical with almost no links fails rather than passing everything",
          code == 1 and any("not a site nav" in f for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------------------------------- 12. nothing to check
    def blank_sitemap(t):
        write(t, "sitemap.xml",
              '<?xml version="1.0" encoding="UTF-8"?>\n<urlset></urlset>\n')
    code, added = plant(blank_sitemap)
    check("an empty sitemap fails rather than checking zero navs",
          code == 1 and any("no pages" in f or "read nothing" in f
                            for f in added),
          f"{len(added)} new failure(s)")

    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
