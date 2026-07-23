#!/usr/bin/env python3
"""
Planted-error test for the em-dash check in validate.py.

    python3 tools/test_emdash_forms.py            # against this checkout
    python3 tools/test_emdash_forms.py --repo ..  # against another checkout

No check ships without one of these. This one exists because check_emdash has now
read ZERO while em dashes were live on the site three separate times, each time for a
different reason, and each time the previous fix looked complete:

    1. visible_text() strips <script>, so 1,092 in index.html's city strings were
       invisible to it.
    2. index.html was not in the target list at all, so 311 more were never scanned.
    3. the check counted the literal character. pick-and-compare.html stores its
       strings as JSON, where an em dash is the six characters \\u2014, so 63 sat
       inside the check's own target list and read zero. 22 more sat in the JSON-LD
       of four profiles.

The through-line is a check written against one spelling on one surface. So this test
does not assert "the escape form is caught". It asserts the SHAPE: every rendering is
caught on every scanned surface, every deliberate exclusion stays silent, and the
fourth way to read zero -- a target list that has drifted off the filenames -- fails
loudly instead of scanning nothing.

Tests 4, 5 and 6 are the ones that matter. Counting escape forms is only shippable
because script_strings() returns literals of 25+ characters, which keeps the
'\\u2014' UI placeholder out, and because regex character classes that match em
dashes on purpose are removed first. Lose either and the check produces permanent
failures on code, which is how a gate stops being read.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# A clean profile: no em-dash renderings on either scanned surface, a JSON-LD block to
# plant an escaped one into, and a <style> block to prove the exclusion holds.
CLEAN_PROFILE = "cities/tucson/profile.html"
CLEAN_PAGE = "top-cities-for-foodies.html"


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-emdash-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the emdash group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "emdash"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def edit(tmp, path, old, new):
    full = os.path.join(tmp, path)
    with open(full, encoding="utf-8") as fh:
        text = fh.read()
    if text.count(old) != 1:
        raise AssertionError(
            f"harness cannot plant into {path}: expected exactly one occurrence of "
            f"{old!r}, found {text.count(old)}. The file has changed; update the "
            f"anchor in this test rather than loosening it.")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))


def plant_in_style(tmp, path, snippet):
    """Insert a snippet just before the first </style>."""
    full = os.path.join(tmp, path)
    with open(full, encoding="utf-8") as fh:
        text = fh.read()
    i = text.index("</style>")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text[:i] + snippet + text[i:])


def plant_in_script(tmp, path, snippet):
    """Append a snippet inside the JSON-LD script block, as sibling code would sit."""
    full = os.path.join(tmp, path)
    with open(full, encoding="utf-8") as fh:
        text = fh.read()
    i = text.index("</script>")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text[:i] + snippet + text[i:])


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def new_fails(base, fails):
    return fails - base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: em-dash renderings\n")

    # ---------------------------------------------------------------- control
    # The baseline is whatever this checkout currently reports. The test asserts on
    # what the plant ADDS, so it is correct before and after the conversion push.
    tmp = stage(repo)
    base_code, base = run(tmp)
    for p in (CLEAN_PROFILE, CLEAN_PAGE):
        dirty = [f for f in base if f.startswith(p)]
        if dirty:
            raise AssertionError(
                f"{p} is no longer a clean planting surface: {dirty}. Pick another "
                f"file rather than loosening the assertions below.")
    shutil.rmtree(os.path.dirname(tmp))
    print(f"  control run: exit {base_code}, {len(base)} failures\n")

    # --------------------------------------- 1. escaped em dash in prose is caught
    # The error that shipped: 85 of these, live, while the gate read 0.
    tmp = stage(repo)
    edit(tmp, CLEAN_PROFILE,
         '"headline": "Tucson, Arizona: A Retirement City Profile"',
         '"headline": "Tucson, Arizona \\u2014 A Retirement City Profile"')
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("escaped \\u2014 in a JSON-LD string is caught",
          code == 1 and any(CLEAN_PROFILE in f and "escaped" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------- 2. literal em dash in prose is caught
    tmp = stage(repo)
    edit(tmp, CLEAN_PROFILE, "<h1", "<p>Tucson \u2014 a planted em dash.</p><h1")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("literal em dash in rendered text is caught",
          code == 1 and any(CLEAN_PROFILE in f and "rendered text" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------ 3. HTML entity forms are caught
    for entity in ("&mdash;", "&#8212;", "&#x2014;"):
        tmp = stage(repo)
        edit(tmp, CLEAN_PROFILE, "<h1", f"<p>Tucson {entity} planted.</p><h1")
        code, fails = run(tmp)
        shutil.rmtree(os.path.dirname(tmp))
        added = new_fails(base, fails)
        check(f"{entity} in rendered text is caught",
              code == 1 and any(CLEAN_PROFILE in f for f in added),
              f"{len(added)} new failure(s)")

    # ------------------------------------------ 4. <style> em dash stays silent
    # Deliberate exclusion. CSS content strings are not copy.
    tmp = stage(repo)
    plant_in_style(tmp, CLEAN_PROFILE,
                   "\n.planted::after{content:'\u2014';}\n"
                   ".planted2::before{content:'\\u2014';}\n")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("em dash inside <style> stays silent",
          not added, f"{len(added)} unexpected new failure(s): {sorted(added)[:1]}")

    # -------------------------------------- 5. the short UI placeholder is silent
    # Both spellings. This is the whole reason the escape form can be counted at all:
    # script_strings() returns literals of 25+ chars, so a placeholder short enough to
    # BE a placeholder never reaches the check. A raw-text scan fires on every one.
    tmp = stage(repo)
    plant_in_script(tmp, CLEAN_PROFILE,
                    "\n</script>\n<script>\n"
                    "const a = city.monthlyEst || '\\u2014';\n"
                    "const b = city.medianHome || '\u2014';\n"
                    "const c = { empty: \"\\u2014\" };\n")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("short '\\u2014' UI placeholder stays silent",
          not added, f"{len(added)} unexpected new failure(s): {sorted(added)[:1]}")

    # ------------------------------------ 6. regex character classes stay silent
    # /[\u2013\u2014\-]/ is code doing the right thing. Two of these are live in
    # pick-and-compare.html. Counting them puts permanent failures on the gate.
    tmp = stage(repo)
    plant_in_script(tmp, CLEAN_PROFILE,
                    "\n</script>\n<script>\n"
                    "const isRange = v && /[\\u2013\\u2014\\-].*\\$/.test(v);\n"
                    "const alsoRange = v && /[\u2013\u2014-]/.test(v);\n")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("regex character class stays silent",
          not added, f"{len(added)} unexpected new failure(s): {sorted(added)[:1]}")

    # ------------- 7. a character class does not shield a real em dash beside it
    # The exclusion must be narrow. Same line, one class and one piece of prose.
    tmp = stage(repo)
    plant_in_script(tmp, CLEAN_PROFILE,
                    "\n</script>\n<script>\n"
                    "const isRange = v && /[\\u2013\\u2014\\-]/.test(v);\n"
                    "const label = 'Median home value \\u2014 citywide, not neighborhood';\n")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("prose em dash beside a character class is still caught",
          code == 1 and any(CLEAN_PROFILE in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------- 8. a target that matches no file fails loudly
    # The fourth way to read zero. Before this, fetch() returned None and the page was
    # skipped in silence, so renaming a landing page retired its em-dash coverage
    # without a word.
    tmp = stage(repo)
    os.rename(os.path.join(tmp, CLEAN_PAGE),
              os.path.join(tmp, "top-cities-for-foodies-2026.html"))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = new_fails(base, fails)
    check("a named target that matches no file fails loudly",
          code == 1 and any("matched no file" in f and CLEAN_PAGE in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
