#!/usr/bin/env python3
"""
Planted-error test for check_stray_artifacts in validate.py.

    python3 tools/test_stray_artifacts.py            # against this checkout
    python3 tools/test_stray_artifacts.py --repo ..  # against another checkout

No check ships without one of these. This one exists because of a failure that has
nothing to do with the content of any file and everything to do with its NAME.

DEPLOY-CHEATSHEET.md section 4 says a build chat delivers a zip of new files already
at their final repo paths, plus apply-<city>.py for edits to existing files. Between
July 25 and July 28 2026 a build chat delivered the older shape instead, three times
running: loose `casper-profile.html` and `casper-hero.jpg` files to be renamed by
hand at deploy time. Nothing caught it. The gate read 0/0 every time, because every
check it runs reads the CONTENT of files it already knows the paths of, and a
profile that is sitting at the repo root under the wrong name is not a file the
validator has any reason to open.

The ways that ships wrong are all quiet:

  - photos renamed by hand at 11pm, one of the three missed, and the profile goes
    live with a broken image nobody sees until a reader does
  - the loose copy left at the root alongside the correct one, so `-PROFILE.html`
    strays sit live and unscanned (this is exactly how a scottsdale-vs-santa-fe
    stray carried four banned superlatives past the superlative check)
  - a bundle zip committed because `rm` came after `git add`

So the assertions are about SHAPE, in both directions:

    1. the control run is clean, so the check is not merely failing at everything
    2. a `<city>-profile.html` at the repo root fails
    3. a `<city>-hero.jpg` at the repo root fails
    4. a zip at the repo root fails
    5. a city-prefixed photo INSIDE cities/<slug>/ fails, since the rename-by-hand
       shape leaves debris there too
    6. a MISSING photo in cities/<slug>/ fails, because the broken-image case is
       the one that actually reaches a reader
    7. a cities/ directory that yields nothing fails LOUDLY rather than comparing
       an empty set and reporting clean. This is the failure mode this codebase
       keeps rediscovering: a check that reads zero and calls it a pass.

Exit 0 = all tests pass.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SLUG = "st-louis"          # any published city; used as the plant target


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-stray-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the layout group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "layout"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def touch(tmp, rel, body=b"x"):
    path = os.path.join(tmp, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(body)


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: hand-off shape and stray build artifacts\n")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a correctly shaped checkout passes", code == 0 and not base,
          f"{len(base)} failure(s)")

    # ------------------------------------- 2. a loose profile at the repo root
    tmp = stage(repo)
    touch(tmp, "casper-profile.html", b"<html></html>")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a <city>-profile.html at the repo root fails",
          code == 1 and any("casper-profile.html" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------- 3. a loose photo at the repo root
    tmp = stage(repo)
    touch(tmp, "casper-hero.jpg")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a <city>-hero.jpg at the repo root fails",
          code == 1 and any("casper-hero.jpg" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------------------------- 4. a bundle zip at the root
    tmp = stage(repo)
    touch(tmp, "casper-bundle.zip")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a zip left at the repo root fails before it can be committed",
          code == 1 and any("casper-bundle.zip" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------- 5. rename debris inside the city directory
    tmp = stage(repo)
    touch(tmp, f"cities/{SLUG}/{SLUG}-hero.jpg")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a city-prefixed photo inside cities/<slug>/ fails",
          code == 1 and any(f"{SLUG}-hero.jpg" in f for f in added),
          f"{len(added)} new failure(s)")

    # ----------------------------------------- 6. a missing photo is the worst case
    tmp = stage(repo)
    os.remove(os.path.join(tmp, "cities", SLUG, "hero.jpg"))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a missing hero.jpg fails rather than shipping a broken image",
          code == 1 and any("hero.jpg" in f and SLUG in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------- 7. nothing to compare must fail, not read clean
    tmp = stage(repo)
    os.rename(os.path.join(tmp, "cities"), os.path.join(tmp, "cities-old"))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a cities/ directory that yields nothing fails loudly, not silently",
          code == 1 and any("nothing was checked" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
