#!/usr/bin/env python3
"""
Planted-error test for check_js_parse.

    python3 tools/test_js_parse.py
    python3 tools/test_js_parse.py --repo ..

check_js_parse exists because of August 15, 2026: a sitewide CSS sweep
injected one declaration into a JavaScript function body, the resulting
syntax error killed the quiz engine's whole script, and both quiz buttons
shipped dead through a gate in which nothing parsed JavaScript. The check
node-parses every inline script on every page. Each assertion below plants
one defect in a staged copy and requires the gate to catch it:

    1. the control run is clean.
    2. THE ORIGINAL INJURY fails: a CSS declaration inside a JS function
       body, planted exactly as the sweep planted it.
    3. AN ORDINARY SYNTAX ERROR fails: an unclosed brace in a page script.
    4. JSON-LD STAYS EXEMPT: a script of type application/ld+json is not
       parsed as JavaScript (check_jsonld owns those), so planting JSON
       there must NOT fail this check.

Exit 0 = all tests pass.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

TARGET = "index.html"


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="jsparse-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "tags"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def plant(repo, addition):
    path = os.path.join(repo, TARGET)
    with open(path, encoding="utf-8") as f:
        s = f.read()
    marker = "</body>"
    if marker not in s:
        sys.exit(f"{TARGET} has no </body>; re-derive this harness.")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s.replace(marker, addition + "\n" + marker, 1))


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_js_parse")

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. the original injury: CSS inside a function body
    tmp, r = stage(repo)
    plant(r, "<script>function hurt(x) { text-wrap: balance;\n  return x; }</script>")
    out = run(r)
    check("CSS injected into a JS function body fails",
          "does not parse as JavaScript" in out)
    shutil.rmtree(tmp)

    # 3. an ordinary syntax error
    tmp, r = stage(repo)
    plant(r, "<script>function open(x) { if (x) { return 1; }</script>")
    out = run(r)
    check("an unclosed brace in a page script fails",
          "does not parse as JavaScript" in out)
    shutil.rmtree(tmp)

    # 4. JSON-LD is not JavaScript and stays exempt
    tmp, r = stage(repo)
    plant(r, '<script type="application/ld+json">{"@context": "https://schema.org"}</script>')
    out = run(r)
    check("JSON-LD blocks are exempt from JS parsing", "0 failures" in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
