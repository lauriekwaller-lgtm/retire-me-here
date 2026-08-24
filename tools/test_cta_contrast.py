#!/usr/bin/env python3
"""
Planted-error test for check_cta_contrast in validate.py.

    python3 tools/test_cta_contrast.py            # against this checkout
    python3 tools/test_cta_contrast.py --repo ..

No check ships without one of these. This one carries more weight than most,
because the check replaces a judgment I made wrong three times in a row on
August 23 2026 -- twice reporting 46 broken pages, with a page list, when the
true answer was the single page Laurie had already told me about.

The plants are therefore chosen to be the specific mistakes I made, not
generic ones:

    1. the control run is clean
    2. a page whose CTA loses to `.header-nav a` FAILS. This is the real defect,
       on the real page
    3. the failure names the page, both colours, the ratio and the winning
       selector, because "some button is wrong" is what I said twice
    4. !important on the losing rule RESCUES the page. My first attempt ignored
       !important entirely and called 45 healthy pages broken; if this plant
       does not pass, the check has that bug
    5. a MULTI-SELECTOR GROUP with comments in it is matched. My second attempt
       matched four hard-coded selector strings, never saw the six-selector
       group that wins on 45 pages, and blamed the wrong rule. This is the exact
       shape of the real stylesheet
    6. HOVER is checked separately from resting. Six pages had a fine resting
       state and a 1.49:1 hover, and a check that looked only at rest would call
       all six clean
    7. specificity, not source order, decides between two rules with no
       !important -- a later, weaker rule must not win
    8. an undefined var() is UNRESOLVED, never assumed readable
    9. unresolvable pages are counted against a budget and a rise FAILS, so the
       check cannot go quiet by ceasing to understand the markup
   10. a borderline ratio just under 4.5 fails and just over passes, so the
       threshold is real rather than decorative
   11. a missing tools/css_cascade.py fails loudly
   12. an empty sitemap fails rather than checking zero buttons

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PAGE = "top-cities-for-hikers.html"

WEAK = """
<style>
.header-nav a { color: #5C5852; }
.header-quiz-btn { background-color: #2A5E5A; color: #FFFFFF; }
</style>
"""


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="rmh-cta-")
    dest = os.path.join(tmp, "repo")
    shutil.copytree(repo, dest,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc",
                                                  "*.jpg", "*.jpeg", "*.png",
                                                  "*.webp", "*.pdf", "*.ico"))
    return dest


def run(tmp):
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "cta"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def strip_hardening(html):
    """
    Remove every existing CTA rule so a plant is the only thing in play.

    Confined to <style> blocks. An earlier version ran the regexes over the
    whole file, and `[^{}]*header-quiz-btn[^{}]*\{[^}]*\}` happily matched from
    the nav markup in the body across to a brace in a later <script>, deleting
    the CTA anchor itself. The page then had no CTA, the check skipped it, and
    five negative plants reported no failure -- looking exactly like a check
    that could not detect anything. Strip CSS from CSS only.
    """
    def scrub(m):
        css = m.group(1)
        css = re.sub(r"[^{}]*header-quiz-btn[^{}]*\{[^}]*\}", "", css)
        css = re.sub(r"\.header-nav\s+a(:hover)?\s*\{[^}]*\}", "", css)
        return "<style>" + css + "</style>"
    return re.sub(r"<style[^>]*>(.*?)</style>", scrub, html, flags=re.S | re.I)


def plant_css(tmp, css, rel=PAGE):
    path = os.path.join(tmp, rel)
    with open(path, encoding="utf-8") as fh:
        html = strip_hardening(fh.read())
    idx = html.rfind("</head>")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html[:idx] + css + html[idx:])


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    print("planted-error test: header CTA contrast\n")

    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a site whose buttons all meet 4.5:1 passes",
          code == 0 and not base, f"{len(base)} failure(s)")

    def plant(css=None, fn=None):
        t = stage(repo)
        if fn:
            fn(t)
        else:
            plant_css(t, css)
        c, f = run(t)
        shutil.rmtree(os.path.dirname(t))
        return c, f - base

    # ------------------------------------------------ 2 + 3. the real defect
    code, added = plant(WEAK)
    hit = [f for f in added if PAGE in f and "resting" in f]
    check("a CTA losing to '.header-nav a' fails (the real defect)",
          code == 1 and bool(hit), f"{len(added)} new failure(s)")
    check("the failure names page, colours, ratio and winning selector",
          bool(hit) and "#5C5852" in hit[0] and "#2A5E5A" in hit[0]
          and "1.04:1" in hit[0] and ".header-nav a" in hit[0],
          hit[0][:100] if hit else "no matching failure")

    # -------------------------------- 4. !important rescues (my first error)
    code, added = plant("""
<style>
.header-nav a { color: #5C5852; }
.header-quiz-btn { background-color: #2A5E5A !important; color: #FFFFFF !important; }
.header-quiz-btn:hover { background-color: #3d7a75 !important; color: #FFFFFF !important; }
</style>
""")
    check("!important on the weaker selector rescues the page",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ------------------------ 5. multi-selector group (my second error)
    code, added = plant("""
<style>
.header-nav a { color: #5C5852; }
.header-nav a:hover { color: #2A5E5A; }
/* ==== QUIZ BUTTON (bulletproof) ==== */
/* Belt and suspenders */
a.header-quiz-btn,
a.header-quiz-btn:link,
a.header-quiz-btn:visited,
button.header-quiz-btn,
.header-quiz-btn { background-color: #2A5E5A !important; color: #FFFFFF !important; }
a.header-quiz-btn:hover,
.header-quiz-btn:hover { background-color: #3d7a75 !important; color: #FFFFFF !important; }
</style>
""")
    check("a commented multi-selector group is matched, not missed",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ------------------------------------------------ 6. hover checked apart
    code, added = plant("""
<style>
.header-nav a { color: #5C5852; }
.header-nav a:hover { color: #2A5E5A; }
a.header-quiz-btn, .header-quiz-btn { background-color: #2A5E5A !important; color: #FFFFFF !important; }
.header-quiz-btn:hover { background-color: #3d7a75 !important; }
</style>
""")
    hov = [f for f in added if PAGE in f and "hover" in f]
    check("a fine resting state with a broken hover still fails",
          code == 1 and bool(hov) and not any("resting" in f for f in added),
          hov[0][:90] if hov else f"{len(added)} new failure(s)")

    # ------------------------------------- 7. specificity beats source order
    code, added = plant("""
<style>
.header-nav a.header-quiz-btn { background-color: #2A5E5A; color: #FFFFFF; }
.header-nav a.header-quiz-btn:hover { background-color: #3d7a75; color: #FFFFFF; }
.header-quiz-btn { color: #5C5852; }
</style>
""")
    check("a later but weaker rule does not win over a stronger earlier one",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ---------------------------------------------- 8 + 9. unresolvable page
    code, added = plant("""
<style>
.header-nav a { color: #5C5852; }
.header-quiz-btn { background-color: #2A5E5A !important; color: var(--nope) !important; }
</style>
""")
    check("an undefined var() counts as unresolved and fails the budget",
          code == 1 and any("could not be resolved" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------- 10. the threshold bites
    code, added = plant("""
<style>
.header-quiz-btn, a.header-quiz-btn { background-color: #2A5E5A !important; color: #9FB8B5 !important; }
.header-quiz-btn:hover, a.header-quiz-btn:hover { background-color: #3d7a75 !important; color: #FFFFFF !important; }
</style>
""")
    check("a ratio just below 4.5:1 fails",
          code == 1 and any(PAGE in f for f in added),
          f"{len(added)} new failure(s)")

    code, added = plant("""
<style>
.header-quiz-btn, a.header-quiz-btn { background-color: #2A5E5A !important; color: #D6E4E2 !important; }
.header-quiz-btn:hover, a.header-quiz-btn:hover { background-color: #3d7a75 !important; color: #FFFFFF !important; }
</style>
""")
    check("a ratio just above 4.5:1 passes",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ---------------------------------------------- 11. the resolver missing
    def no_resolver(t):
        os.remove(os.path.join(t, "tools", "css_cascade.py"))
    code, added = plant(fn=no_resolver)
    check("a missing tools/css_cascade.py fails loudly",
          code == 1 and bool(added), f"{len(added)} new failure(s)")

    # ------------------------------------------------- 12. nothing to check
    def blank_sitemap(t):
        with open(os.path.join(t, "sitemap.xml"), "w", encoding="utf-8") as fh:
            fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset></urlset>\n')
    code, added = plant(fn=blank_sitemap)
    check("an empty sitemap fails rather than checking zero buttons",
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
