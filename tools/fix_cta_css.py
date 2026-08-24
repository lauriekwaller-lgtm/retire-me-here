#!/usr/bin/env python3
"""
Give the hardened header-CTA rule to any page whose CTA fails contrast.

    python3 tools/fix_cta_css.py            # patch the pages that need it
    python3 tools/fix_cta_css.py --check    # report, write nothing
    python3 tools/fix_cta_css.py --repo ..

Forty-five pages already carry this rule. Someone added it by hand, page by
page, and the comment on it says "bulletproof" -- which it is, on the pages that
got it. visit-before-you-decide.html never did, so `.header-nav a` wins there
and the button renders #5C5852 on #2A5E5A at 1.04:1. Six pages got the resting
rule but not the :hover one, so hovering paints teal text on a teal-mid
background at 1.49:1.

Same shape as every other defect this repo has turned up lately: a correct fix
applied by hand, to most places, with nothing checking that it landed
everywhere.

APPENDS rather than rewrites, deliberately. The existing rules are written six
different ways across the site -- minified, spread, with and without the Safari
fallback, with and without border-color -- and matching all six to replace them
is exactly the kind of by-hand pattern-matching that produced two wrong answers
before this script existed. The appended rule carries !important and a higher
specificity than anything above it, so it wins without needing to find what it
is beating.

Idempotent via the marker; re-running is a no-op.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from css_cascade import cta_contrast   # noqa: E402

MARKER = "RMH-CTA-CONTRAST-V1"
MIN_RATIO = 4.5

BLOCK = """
/* ============ """ + MARKER + """ ============ */
/* The header CTA is an <a> inside .header-nav, so `.header-nav a { color }`
   (0-1-1) outranks a bare `.header-quiz-btn { color }` (0-1-0). Both the
   resting and hover states need to win on their own; the hover one was the
   half that got missed. Hex, not var(), so an undefined variable cannot
   silently drop this back to the inherited colour. */
a.header-quiz-btn,
a.header-quiz-btn:link,
a.header-quiz-btn:visited,
a.header-quiz-btn:active,
button.header-quiz-btn,
.header-quiz-btn {
  background-color: #2A5E5A !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  text-decoration: none !important;
}
a.header-quiz-btn:hover,
a.header-quiz-btn:focus,
button.header-quiz-btn:hover,
.header-quiz-btn:hover {
  background-color: #3d7a75 !important;
  border-color: #3d7a75 !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
}
"""


def needs_fix(html):
    """[(state, ratio)] for each state below MIN_RATIO."""
    out = []
    for hover in (False, True):
        got = cta_contrast(html, hover=hover)
        if got and got[0] < MIN_RATIO:
            out.append(("hover" if hover else "resting", got[0]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.repo)

    pages = sorted(f for f in os.listdir(root) if f.endswith(".html"))
    if not pages:
        print("no pages found", file=sys.stderr)
        return 2

    todo = []
    for rel in pages:
        path = os.path.join(root, rel)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        if MARKER in html:
            continue
        bad = needs_fix(html)
        if not bad:
            continue
        todo.append((rel, bad))
        if args.check:
            continue
        idx = html.rfind("</style>")
        if idx == -1:
            print(f"  {rel} has no </style> to append to", file=sys.stderr)
            return 2
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html[:idx] + BLOCK + html[idx:])

    if not todo:
        print("every header CTA already meets contrast; nothing to do")
        return 0
    verb = "need" if args.check else "patched"
    print(f"{len(todo)} page(s) {verb}:")
    for rel, bad in todo:
        detail = ", ".join(f"{state} {ratio:.2f}:1" for state, ratio in bad)
        print(f"  {rel}  ({detail})")
    return 1 if args.check else 0


if __name__ == "__main__":
    sys.exit(main())
