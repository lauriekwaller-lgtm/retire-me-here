#!/usr/bin/env python3
"""
Planted-error test for check_taxfacts.

    python3 tools/test_taxfacts.py
    python3 tools/test_taxfacts.py --repo ..

The check it guards holds the State Tax Facts sheet (DB v18) to three promises:
two-way coverage against the City Database's state roster, closed enum
vocabularies, and a PropTax mirror that may not drift from the City Database
column. A check written to close those holes is worth nothing unless it can be
shown to FAIL, so each assertion below plants one defect and requires the gate
to catch it.

    1. the control run is clean.
    2. A RENAMED STATE KEY fails TWICE: the real state now has no facts row,
       and the fake state is an orphan. One plant, both directions of the
       coverage promise.
    3. A DRIFTED PROPTAX MIRROR fails. The exact duplication this check exists
       to police: the same figure in two sheets, silently diverging.
    4. FREE TEXT IN AN ENUM COLUMN fails. "sometimes exempt" is a sentence,
       not a filter value; a filter built on it silently drops the row.
    5. AN EMPTIED SHEET fails LOUDLY rather than reporting clean. Zero matches
       must never be a pass; that is the silent-no-op shape the validator
       exists to refuse.
    6. A DELETED SHEET fails LOUDLY, same reason, different failure path (the
       sheet lookup itself, not the row scan).
    7. A BLANKED ENUM CELL fails. The population pass (v19) retired the
       blank tolerance; this assertion keeps it retired.
    8. A REMOVED TAX YEAR CELL fails: the same retirement, numeric side.

All plants are made with the standard library only, by rewriting worksheet XML
inside the xlsx zip. The facts sheet is written as inlineStr cells precisely so
this file can manipulate it without openpyxl, which vanishes every time
Codespaces rebuilds.

Nothing here hardcodes a state or a rate it does not have to: plants are
derived from whatever the live sheet carries, so this file does not need
editing when the sheet's contents legitimately move.

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

DB_GLOB_PREFIX = "CityDatabase_"
SHEET_MARKER = "Income Tax Type"          # only the facts sheet contains this


def stage(repo):
    tmp = tempfile.mkdtemp(prefix="taxfacts-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "node_modules"))
    return tmp, dst


def run(repo):
    env = dict(os.environ, RMH_IN_HARNESS="1")
    p = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "db"],
        cwd=repo, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


def db_path(repo):
    docs = os.path.join(repo, "docs")
    dbs = [f for f in os.listdir(docs)
           if f.startswith(DB_GLOB_PREFIX) and f.endswith(".xlsx")]
    if len(dbs) != 1:
        sys.exit(f"expected exactly one CityDatabase in docs/, found {dbs}. "
                 f"Re-derive this harness.")
    return os.path.join(docs, dbs[0])


def facts_part(path):
    """Locate the facts worksheet part inside the xlsx by its header marker."""
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                if SHEET_MARKER in z.read(name).decode("utf-8", "replace"):
                    return name
    sys.exit("no worksheet part contains the State Tax Facts header. "
             "Re-derive this harness.")


def rewrite_zip(path, edits):
    """Rewrite the xlsx with `edits` = {part_name: transform(text) -> text}."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        payload = {n: z.read(n) for n in names}
    for part, fn in edits.items():
        payload[part] = fn(payload[part].decode("utf-8")).encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, payload[n])


RESULTS = []


def check(name, condition):
    RESULTS.append((name, condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("test_taxfacts")

    live_db = db_path(repo)
    part = facts_part(live_db)
    with zipfile.ZipFile(live_db) as z:
        sheet_xml = z.read(part).decode("utf-8")

    # Derive a state key and its row from the live sheet, no hardcoding. The
    # first data row is row 3; its A cell is an inlineStr two-letter key.
    m = re.search(r'<row r="3"><c r="A3" t="inlineStr"><is><t>([A-Z]{2})</t>',
                  sheet_xml)
    if not m:
        sys.exit("cannot find the first data row's ST cell. The sheet's byte "
                 "format changed; re-derive this harness.")
    st = m.group(1)
    vm = re.search(r'<row r="3">.*?<c r="H3"><v>([0-9.]+)</v>', sheet_xml)
    if not vm:
        sys.exit(f"cannot find {st}'s PropTax cell in row 3. Re-derive this "
                 f"harness.")
    rate = vm.group(1)

    # 1. control
    tmp, r = stage(repo)
    out = run(r)
    check("control run is clean", "0 failures" in out)
    shutil.rmtree(tmp)

    # 2. one renamed key, both coverage directions
    tmp, r = stage(repo)
    rewrite_zip(db_path(r), {part: lambda s: s.replace(
        f"<t>{st}</t>", "<t>ZZ</t>", 1)})
    out = run(r)
    check("a state with a city but no facts row fails",
          "has no row in State Tax Facts" in out)
    check("a facts row for a state with no city fails",
          "has no city in the database" in out
          and "Speculative rows are refused" in out)
    shutil.rmtree(tmp)

    # 3. a drifted PropTax mirror
    tmp, r = stage(repo)
    rewrite_zip(db_path(r), {part: lambda s: s.replace(
        f'<c r="H3"><v>{rate}</v></c>', '<c r="H3"><v>9.99</v></c>', 1)})
    out = run(r)
    check("a PropTax mirror that drifts from the City Database fails",
          "disagrees with the City" in out)
    shutil.rmtree(tmp)

    # 4. free text in an enum column
    tmp, r = stage(repo)
    rewrite_zip(db_path(r), {part: lambda s: s.replace(
        f'<c r="H3"><v>{rate}</v></c>',
        f'<c r="D3" t="inlineStr"><is><t>sometimes exempt</t></is></c>'
        f'<c r="H3"><v>{rate}</v></c>', 1)})
    out = run(r)
    check("free text in an enum column fails",
          "not a recognized value" in out)
    shutil.rmtree(tmp)

    # 5. an emptied sheet: zero rows must fail loudly, never pass
    tmp, r = stage(repo)
    rewrite_zip(db_path(r), {part: lambda s: re.sub(
        r'<row r="(?:[3-9]|\d\d+)">.*?</row>', "", s)})
    out = run(r)
    check("an emptied sheet fails loudly rather than passing",
          "read zero state rows" in out)
    shutil.rmtree(tmp)

    # 6. a deleted sheet: the lookup itself must fail, not crash, not pass
    tmp, r = stage(repo)
    rewrite_zip(db_path(r), {"xl/workbook.xml": lambda s: re.sub(
        r'<sheet name="State Tax Facts"[^/]*/>', "", s)})
    out = run(r)
    check("a deleted sheet fails loudly rather than passing",
          "sheet is missing" in out)
    shutil.rmtree(tmp)

    # 7. a blanked enum cell: the blank tolerance stays retired
    tmp, r = stage(repo)
    d3 = re.search(r'<c r="D3"[^>]*>.*?</c>', sheet_xml).group(0)
    rewrite_zip(db_path(r), {part: lambda s: s.replace(d3, "", 1)})
    out = run(r)
    check("a blanked enum cell fails", "is blank" in out)
    shutil.rmtree(tmp)

    # 8. a removed Tax Year cell: numeric completeness holds too
    tmp, r = stage(repo)
    k3 = re.search(r'<c r="K3"[^>]*>.*?</c>', sheet_xml).group(0)
    rewrite_zip(db_path(r), {part: lambda s: s.replace(k3, "", 1)})
    out = run(r)
    check("a removed Tax Year cell fails", "Tax Year is blank" in out)
    shutil.rmtree(tmp)

    passed = sum(1 for _, ok in RESULTS if ok)
    print(f"{passed}/{len(RESULTS)} passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
