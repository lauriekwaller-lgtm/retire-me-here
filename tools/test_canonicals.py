#!/usr/bin/env python3
"""
Planted-error test for check_canonicals in validate.py.

    python3 tools/test_canonicals.py            # against this checkout
    python3 tools/test_canonicals.py --repo ..  # against another checkout

No check ships without one of these. This one exists because of the August 9 2026
Search Console read, which found the same HTML being served at up to a hundred
distinct URLs with nothing declaring which was real.

The landing pages were fine, and that is the interesting part. Every root-level
page carried a self-referencing canonical, so when Netlify served both /foo and
/foo.html, Google consolidated them and the duplicate forms never got above a
handful of impressions. The defence worked. It just was not written down anywhere
or enforced, so index.html shipped without one and nobody noticed for months,
while the site linked to it as index.html?city=NAME&state=ST in 471 places.

So the assertions are about the two ways this goes wrong, absence and
disagreement, plus the shape failure that would hide both:

    1. the control run is clean, so the check is not merely failing at everything
    2. a page with NO canonical fails
    3. index.html with no canonical fails specifically, since that is the exact
       defect that shipped, and the homepage is reached through more alias URLs
       than any other page on the site
    4. two canonicals on one page fails, because which one Google honours is
       undefined and "we set it twice" reads like it is defended when it is not
    5. a canonical pointing at the EXTENSIONLESS form fails, since that is the
       plausible half-fix: someone tidies one page to /foo while the sitemap and
       every internal link still say /foo.html, and the page now argues against
       its own sitemap entry
    6. a canonical pointing at a different real page on the site fails, the
       copy-paste error a new landing page would ship with
    7. an empty sitemap fails LOUDLY rather than checking zero pages and
       reporting clean. This is the failure mode this codebase keeps
       rediscovering: a check that reads nothing and calls it a pass.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PAGE = "top-cities-for-hikers.html"     # any sitemapped landing page
OTHER = "top-cities-for-foodies.html"   # a second one, for the wrong-target plant


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-canon-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the routing group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "routing"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def edit(tmp, rel, old, new, count=1):
    """Rewrite a staged file, asserting the anchor was actually there."""
    path = os.path.join(tmp, rel)
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    if body.count(old) != count:
        raise SystemExit(f"harness anchor error: {old!r} appears "
                         f"{body.count(old)} times in {rel}, expected {count}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body.replace(old, new))


def canonical_of(repo, rel):
    with open(os.path.join(repo, rel), encoding="utf-8") as fh:
        m = re.search(r'<link\s+rel="canonical"\s+href="[^"]*">', fh.read())
    if not m:
        raise SystemExit(f"harness setup error: {rel} has no canonical to plant against")
    return m.group(0)


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: canonical tag integrity\n")

    tag = canonical_of(repo, PAGE)
    idx_tag = canonical_of(repo, "index.html")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a checkout with correct canonicals passes", code == 0 and not base,
          f"{len(base)} failure(s)")

    # ------------------------------------------- 2. a landing page with none
    tmp = stage(repo)
    edit(tmp, PAGE, tag, "")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a page with no canonical fails",
          code == 1 and any(PAGE in f and "no rel" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------- 3. index.html with none
    tmp = stage(repo)
    edit(tmp, "index.html", idx_tag, "")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("index.html with no canonical fails (the defect that shipped)",
          code == 1 and any("index.html" in f and "no rel" in f for f in added),
          f"{len(added)} new failure(s)")

    # ----------------------------------------------------- 4. two canonicals
    tmp = stage(repo)
    edit(tmp, PAGE, tag, tag + "\n" + tag)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("two canonical tags on one page fails",
          code == 1 and any(PAGE in f and "2 canonical" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------- 5. canonical to extensionless form
    tmp = stage(repo)
    edit(tmp, PAGE, tag, tag.replace(".html", ""))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a canonical pointing at the extensionless form fails",
          code == 1 and any(PAGE in f and "disagree" in f for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------------------- 6. canonical to a different page
    tmp = stage(repo)
    edit(tmp, PAGE, tag, canonical_of(repo, OTHER))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a canonical pointing at another page on the site fails",
          code == 1 and any(PAGE in f and "disagree" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------- 7. nothing to check must fail, not read clean
    tmp = stage(repo)
    with open(os.path.join(tmp, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset></urlset>\n')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("an empty sitemap fails loudly rather than checking nothing",
          code == 1 and any("no <loc>" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
