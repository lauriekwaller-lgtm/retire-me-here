#!/usr/bin/env python3
"""
Stamp tools/nav_canonical.html onto every page that carries the nav component.

    python3 tools/build_nav.py            # rewrite the navs in place
    python3 tools/build_nav.py --check    # report drift, write nothing
    python3 tools/build_nav.py --repo ..  # operate on another checkout

Same shape as tools/build_sitemap.py, for the same reason: the thing that broke
was hand-maintenance. The site had eight distinct navs across 100 pages because
the nav was never a component -- each page kept whatever the menu looked like on
the day it was built, and every new tool page got added to whichever nav was in
front of whoever added it. where-can-i-afford-to-retire.html ended up in the menu
on 2 pages out of 98.

WHAT IT DOES NOT TOUCH, deliberately:

  index.html. Its nav calls openCitySearch(), startQuiz() and
  showScreen('screen-explore'), which exist only on that page because it is the
  quiz app. Stamping the canonical block there would kill every item. Its nav
  stays hand-written; check_nav_parity holds it to the same destinations.

  The 52 pages with no component -- the 51 city profiles and
  visit-before-you-decide.html. They have no .nav-dropdown CSS and no
  toggleTopCitiesDropdown JS, so pasting the block in would render a broken
  menu that does not open. Giving them the nav means shipping CSS and JS too,
  and it visibly changes the top of every profile. That is BATCH B and it wants
  a rendered page reviewed first. This script skips them and says how many.

Exit codes: 0 clean (or written), 1 drift found under --check, 2 setup problem.
"""

import argparse
import os
import re
import sys

SITE = "https://retiremehere.com"
CANONICAL = os.path.join("tools", "nav_canonical.html")
EXEMPT = {"index.html"}

NAV_RE = re.compile(r"<nav\b.*?</nav>", re.S | re.I)


def read_canonical(root):
    path = os.path.join(root, CANONICAL)
    if not os.path.exists(path):
        raise SystemExit(f"{CANONICAL} is missing; there is nothing to stamp")
    with open(path, encoding="utf-8") as fh:
        m = NAV_RE.search(fh.read())
    if not m:
        raise SystemExit(f"{CANONICAL} contains no <nav> element")
    return m.group(0)


def sitemap_pages(root):
    with open(os.path.join(root, "sitemap.xml"), encoding="utf-8") as fh:
        body = fh.read()
    pages = []
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body):
        rest = loc[len(SITE):].lstrip("/") if loc.startswith(SITE) else ""
        pages.append(rest if rest else "index.html")
    if not pages:
        raise SystemExit("sitemap.xml yielded no pages")
    return sorted(set(pages))


def indent_like(nav, original):
    """Reproduce the original block's leading whitespace so diffs stay small."""
    lead = re.match(r"[ \t]*", original.splitlines()[0]).group(0)
    if not lead:
        return nav
    return "\n".join(lead + ln if ln.strip() else ln for ln in nav.splitlines())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.repo)

    canon = read_canonical(root)
    canon_key = tuple(ln.strip() for ln in canon.splitlines() if ln.strip())

    changed, stubs, exempt, already = [], 0, 0, 0
    for rel in sitemap_pages(root):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            print(f"  {rel} is in the sitemap but not on disk", file=sys.stderr)
            return 2
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        m = NAV_RE.search(html)
        if not m:
            continue
        nav = m.group(0)
        if "nav-dropdown" not in nav:
            stubs += 1
            continue
        if rel in EXEMPT:
            exempt += 1
            continue
        if tuple(ln.strip() for ln in nav.splitlines() if ln.strip()) == canon_key:
            already += 1
            continue
        changed.append(rel)
        if not args.check:
            new = html[:m.start()] + indent_like(canon, nav) + html[m.end():]
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)

    tail = (f"{already} already canonical, {exempt} exempt (index.html), "
            f"{stubs} without the component (BATCH B)")
    if args.check:
        if not changed:
            print(f"every nav is canonical: {tail}")
            return 0
        print(f"{len(changed)} nav(s) differ from {CANONICAL}: {tail}")
        for rel in changed:
            print(f"  {rel}")
        return 1

    print(f"{len(changed)} nav(s) rewritten: {tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
