#!/usr/bin/env python3
"""
Raise the nav collapse threshold above the band where six items do not fit.

    python3 tools/fix_nav_breakpoint.py            # write
    python3 tools/fix_nav_breakpoint.py --check    # report, write nothing

THE DEFECT. BATCH A replaced a 3-item nav with a 6-item one on 46 pages and
BATCH B carried the same block to a profile. Nobody moved the breakpoint. The
menu needs roughly 950px; the pages collapse to mobile at 760 (42 pages), 720
(3), 768 (1) and 880 (the profile). Between the collapse point and ~960px there
is not room for six items, the flex line squeezes, and the text wraps INSIDE
each link: "Find a / City", "Top Cities / For...", "What Can I / Afford?" on two
lines, with the wordmark colliding with the first item. Reported from a photo of
a real window, not caught by the gate, because both my checks and the harnesses
compared markup and colour and never a layout width.

WHY NOT JUST EDIT THE EXISTING @media. Because those blocks are not about the
nav. The 760px block on a topic page also carries hero sizing, section padding
and grid changes. Raising 760 to 1000 would drag all of that up with it and
restyle the whole page between 760 and 1000. So this appends a NEW block that
carries the nav swap and nothing else, and leaves every existing block alone.
Below the old threshold both blocks agree, so there is no conflict.

TWO PARTS, because the breakpoint alone is a number that could drift again:

  1. the swap moves to 1000px, with headroom over the ~950 the menu needs
  2. `white-space: nowrap` on the items, so if a longer label is ever added and
     the true requirement creeps past 1000, it degrades to slight crowding
     instead of the two-line collision in the photo. The wrap is the ugly part,
     and it is preventable independently of getting the number right.

Component pages swap the nav for the hamburger. Profiles have no hamburger, so
they keep the existing behaviour of showing the CTA alone.
"""

import argparse
import os
import re
import sys

MARKER = "RMH-NAV-BREAKPOINT"
BREAKPOINT = 1000

NOWRAP = """
/* %s -- see tools/fix_nav_breakpoint.py
   Six nav items need ~950px. Anything narrower squeezed the flex line and
   wrapped the text inside each link onto two lines. nowrap makes a near miss
   degrade to crowding rather than collision. */
.header-nav a, .header-nav .nav-dropdown-trigger { white-space: nowrap; }
""" % MARKER

SWAP_MOBILE = """@media (max-width: %dpx) {
  /* %s. Nav only. The page's own mobile block, at its original width, still
     owns hero/padding/grid; this deliberately does not touch it. */
  .header-nav { display: none; }
  .header-mobile-menu { display: flex; }
}
""" % (BREAKPOINT, MARKER)

SWAP_PROFILE = """@media (max-width: %dpx) {
  /* %s. Profiles have no hamburger, so this keeps the pre-existing
     behaviour -- the CTA alone -- and simply starts it higher up. */
  .header-nav a:not(.header-quiz-btn) { display: none; }
  .header-nav .nav-dropdown { display: none; }
}
""" % (BREAKPOINT, MARKER)


def targets(root):
    out = []
    for dirpath, _, names in os.walk(root):
        # tools/ holds nav_canonical.html, which is the nav MARKUP fragment and
        # carries no stylesheet. It is not a page and must not be stamped.
        if any(s in dirpath for s in (".git", "node_modules", "tools")):
            continue
        for n in names:
            if not n.endswith(".html"):
                continue
            p = os.path.join(dirpath, n)
            html = open(p, encoding="utf-8").read()
            if "nav-dropdown" in html and "header-nav" in html:
                out.append((os.path.relpath(p, root), html))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.repo)

    pages = targets(root)
    if not pages:
        print("no pages with the nav component were found; nothing was read",
              file=sys.stderr)
        return 2

    done, todo, problems = [], [], []
    for rel, html in pages:
        if MARKER in html:
            done.append(rel)
            continue
        if html.count("</style>") < 1:
            problems.append(f"{rel}: no </style> to append to")
            continue
        todo.append(rel)

    if problems:
        for p in problems:
            print(f"  ABORT {p}", file=sys.stderr)
        return 2

    print(f"{len(pages)} pages carry the nav component: "
          f"{len(todo)} to fix, {len(done)} already done")

    if args.check:
        for rel in todo:
            print(f"  would fix {rel}")
        return 1 if todo else 0

    for rel in todo:
        path = os.path.join(root, rel)
        html = open(path, encoding="utf-8").read()
        block = SWAP_MOBILE if "header-mobile-menu" in html else SWAP_PROFILE
        addition = NOWRAP + "\n" + block
        i = html.rindex("</style>")
        html = html[:i] + addition + html[i:]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"  fixed {rel} ({'hamburger' if 'header-mobile-menu' in block else 'CTA-only'})")

    print(f"\n{len(todo)} page(s) rewritten at max-width: {BREAKPOINT}px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
