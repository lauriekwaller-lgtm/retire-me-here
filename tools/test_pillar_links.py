#!/usr/bin/env python3
"""
Planted-error test for check_pillar_links in validate.py.

    python3 tools/test_pillar_links.py            # against this checkout
    python3 tools/test_pillar_links.py --repo ..  # against another checkout

No check ships without one of these. This one exists because of the August 22
2026 routing session, and specifically because of what happened when the link
was planted BEFORE the check was written: a typo in the href on one of the 51
profiles ran the full gate at 0 failures, 0 warnings. The site would have
shipped a dead link to the very page the session existed to make reachable.

The pillar link is not defended by anything else. It is not an affiliate link,
so check_affiliate ignores it. It is not a canonical, not a sitemap entry, not
a score, not a figure. Tag balance sees a well-formed anchor and moves on. The
one thing that would have caught it, an internal-link-target check, does not
exist. So this check is the only thing standing between a fat-fingered href and
a silently orphaned pillar page, which is the exact condition the session was
convened to fix.

The assertions are the ways this goes wrong:

    1. the control run is clean, so the check is not merely failing at everything
    2. a profile missing the link entirely fails, and names the slug
    3. a typo'd href fails, which is the defect that actually got through
    4. an href to the extensionless form fails, since the site links to root
       pages as /foo.html everywhere and a lone /foo would be a new convention
       nothing else follows
    5. a profile carrying the link but NOT the data-rmh-pillar hook fails,
       because the click would be invisible and the entry would read as
       measured when it is not
    6. the pillar page itself going missing fails LOUDLY, rather than 51
       profiles cheerfully pointing at nothing
    7. zero profiles found fails LOUDLY rather than checking nothing and
       reporting clean. This is the failure mode this codebase keeps
       rediscovering: a check that reads nothing and calls it a pass.

Exit 0 = all tests pass.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SLUG = "santa-fe"
PROFILE = f"cities/{SLUG}/profile.html"
GOOD = '<a href="/visit-before-you-decide.html" data-rmh-pillar="1"'


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-pillar-")
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


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: pillar link on every profile\n")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a checkout with all 51 pillar links passes", code == 0 and not base,
          f"{len(base)} failure(s)")

    # -------------------------------------------------- 2. link deleted outright
    tmp = stage(repo)
    edit(tmp, PROFILE, GOOD, '<a href="#" ')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a profile with no pillar link fails, by slug",
          code == 1 and any(SLUG in f and "pillar" in f.lower() for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------- 3. typo'd href: the real defect
    tmp = stage(repo)
    edit(tmp, PROFILE, GOOD,
         '<a href="/visit-before-you-decide.htm" data-rmh-pillar="1"')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a typo'd pillar href fails (the defect that got through Aug 22)",
          code == 1 and any(SLUG in f and "pillar" in f.lower() for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------ 4. extensionless variant
    tmp = stage(repo)
    edit(tmp, PROFILE, GOOD,
         '<a href="/visit-before-you-decide" data-rmh-pillar="1"')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("an extensionless pillar href fails",
          code == 1 and any(SLUG in f and "pillar" in f.lower() for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------- 5. link present, hook missing
    tmp = stage(repo)
    edit(tmp, PROFILE, GOOD, '<a href="/visit-before-you-decide.html" ')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a pillar link with no data-rmh-pillar hook fails",
          code == 1 and any(SLUG in f and "data-rmh-pillar" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------ 6. destination page missing
    tmp = stage(repo)
    os.remove(os.path.join(tmp, "visit-before-you-decide.html"))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("the pillar page going missing fails loudly",
          code == 1 and any("visit-before-you-decide.html" in f
                            and "does not exist" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------- 7. nothing to check must fail, not read clean
    tmp = stage(repo)
    for slug in os.listdir(os.path.join(tmp, "cities")):
        p = os.path.join(tmp, "cities", slug, "profile.html")
        if os.path.exists(p):
            os.remove(p)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("zero readable profiles fails loudly rather than checking nothing",
          code == 1 and any("no profile" in f.lower() or "0 profiles" in f
                            for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
