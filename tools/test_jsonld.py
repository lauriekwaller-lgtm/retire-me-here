#!/usr/bin/env python3
"""
Planted-error test for check_jsonld in validate.py.

    python3 tools/test_jsonld.py            # against this checkout
    python3 tools/test_jsonld.py --repo ..  # against another checkout

No check ships without one of these. This one exists because of the August 14 2026
Search Console notice, "Unparsable structured data ... Parsing error: Missing ','
or ']' in array declaration", on states-that-dont-tax-retirement-income.html. The
FAQPage node inside @graph had shipped without its opening brace, so its keys sat
loose in the array and a spare "]" closed the hole further down.

The reason it survived a clean gate run is the whole point of the check. Nothing
renders JSON-LD, so the page looked correct in every browser, and the validator was
reading the same file for figures, superlatives and tag balance without ever asking
whether the one machine-readable block on the page was machine-readable.

The assertions cover the ways this goes wrong, plus the shape failure that hides
all of them:

    1. the control run is clean, so the check is not merely failing at everything
    2. a node in @graph missing its opening brace fails, on the exact page it
       shipped on, with the exact defect
    3. a trailing comma before a closing brace fails, the commonest hand-edit slip
    4. a spare closing bracket fails, the other half of what actually shipped
    5. the same defect planted in a city profile fails, proving coverage is a glob
       and not a hand-maintained target list that a new page can fall off
    6. a checkout with no JSON-LD anywhere fails LOUDLY rather than parsing zero
       blocks and reporting clean. This is the failure mode this codebase keeps
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

PAGE = "states-that-dont-tax-retirement-income.html"   # where it actually shipped
PROFILE = "cities/st-louis/profile.html"               # the canonical profile

BLOCK = re.compile(
    r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-jsonld-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the tags group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "tags"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def mangle(tmp, rel, fn):
    """Rewrite the inner text of the first JSON-LD block through fn."""
    path = os.path.join(tmp, rel)
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    m = BLOCK.search(body)
    if not m:
        raise SystemExit(f"harness setup error: {rel} has no JSON-LD to plant against")
    broken = fn(m.group(2))
    if broken == m.group(2):
        raise SystemExit(f"harness setup error: the plant changed nothing in {rel}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body[:m.start(2)] + broken + body[m.end(2):])


def drop_graph_brace(block):
    """Delete the opening brace of the first node in @graph. The shipped defect."""
    i = block.index('"@graph"')
    j = block.index("{", i)
    return block[:j] + block[j + 1:]


def trailing_comma(block):
    """A comma before the final closing brace."""
    j = block.rstrip().rindex("}")
    return block[:j] + ",\n" + block[j:]


def spare_bracket(block):
    """One closing bracket too many, the other half of what shipped."""
    j = block.rstrip().rindex("}")
    return block[:j] + "]\n" + block[j:]


def strip_all_jsonld(tmp):
    """Remove every JSON-LD block in the staged checkout."""
    for base, _dirs, files in os.walk(tmp):
        if ".git" in base:
            continue
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(base, name)
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            stripped = BLOCK.sub("", body)
            if stripped != body:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(stripped)


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: JSON-LD parses\n")

    for rel in (PAGE, PROFILE):
        if not os.path.exists(os.path.join(repo, rel)):
            raise SystemExit(f"harness setup error: {rel} is missing from the checkout")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("a checkout with valid JSON-LD passes", code == 0 and not base,
          f"{len(base)} failure(s)")

    # ------------------------------------------- 2. the defect that shipped
    tmp = stage(repo)
    mangle(tmp, PAGE, drop_graph_brace)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a @graph node missing its opening brace fails (the defect that shipped)",
          code == 1 and any(PAGE in f and "does not parse" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------------------- 3. trailing comma
    tmp = stage(repo)
    mangle(tmp, PAGE, trailing_comma)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a trailing comma before a closing brace fails",
          code == 1 and any(PAGE in f and "does not parse" in f for f in added),
          f"{len(added)} new failure(s)")

    # ---------------------------------------------------- 4. spare bracket
    tmp = stage(repo)
    mangle(tmp, PAGE, spare_bracket)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a spare closing bracket fails",
          code == 1 and any(PAGE in f and "does not parse" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------- 5. coverage is a glob, not a list
    tmp = stage(repo)
    mangle(tmp, PROFILE, drop_graph_brace)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("the same defect in a city profile fails (coverage is not a target list)",
          code == 1 and any(PROFILE in f and "does not parse" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------- 6. nothing to check must fail, not read clean
    tmp = stage(repo)
    strip_all_jsonld(tmp)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a checkout with no JSON-LD fails loudly rather than checking nothing",
          code == 1 and any("no JSON-LD blocks found" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
