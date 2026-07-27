#!/usr/bin/env python3
"""
Planted-error test for the highlight home-figure check in validate.py.

    python3 tools/test_highlight_homes.py            # against this checkout
    python3 tools/test_highlight_homes.py --repo ..  # against another checkout

No check ships without one of these. A validator check is only worth the line it
occupies if it has been watched to fail on a real error, and the way that goes wrong
is subtle: a regex that matches nothing reports a clean run forever and looks exactly
like a site with no bugs.

The planted error is the one that actually shipped. Wilmington DE's highlight read
$215K while the database said something else, and it read that way on the live site
until this check was written. Nothing synthetic here.

Every home figure below is READ FROM THE DATABASE at runtime. They were hardcoded
until July 27 2026, when the annual ZHVI rebase moved Wilmington DE from $321,000 to
$336,000 and this file began crashing on an assert at the first test. Nothing ran it,
so nothing said so, and it sat broken on main through a clean 0/0 gate. Both halves of
that are fixed together: the figures are derived, and the harness is wired into the
gate as the `harness` check group. A fixture that names a constant the annual refresh
moves is a fixture with an expiry date on it.

Test 3 is the one that matters most. The database holds Wilmington DE AND Wilmington
NC. On July 21 a name-only lookup graded one against the other's figure and put
$418,000 on the board as a bug that did not exist. Any check that keys on city name
alone reproduces that. Test 3 plants NC's own correct figure and asserts silence,
then plants DE's figure into NC's string and asserts a failure -- the two halves are
only both true if the lookup is keyed on (City, ST).

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate  # noqa: E402  -- same directory, imported only to read the database

NEEDED = ["index.html", "pick-and-compare.html", "sitemap.xml", "docs", "tools"]


def db_homes(repo, wanted):
    """
    Median Home for each (City, ST), read through validate.py's own loader.

    Deliberately not a second xlsx parser. If the database moves or its columns are
    renamed, this harness must break in the same place and the same way the validator
    does, rather than grading the site against a stale copy of the truth.
    """
    db = validate.load_db(os.path.join(repo, validate.DEFAULT_DB))
    out = {}
    for city, state in wanted:
        row = validate.db_get(db, city, state)
        if not row or row.get("home") is None:
            raise AssertionError(
                f"{city}, {state} has no Median Home in {validate.DEFAULT_DB}. This "
                f"harness plants against real rows; pick a different fixture city "
                f"rather than hardcoding a figure back in.")
        out[(city, state)] = row["home"]
    return out


def K(value):
    """The $NNNK rendering, the one the highlight strings use."""
    return "$%dK" % round(value / 1000)


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-planted-")
    for item in NEEDED:
        src = os.path.join(repo, item)
        dst = os.path.join(tmp, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return tmp


def run(tmp):
    """Run the figures group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "figures"],
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
            f"{old!r}, found {text.count(old)}. The copy has changed; update the "
            f"anchor in this test rather than loosening it.")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))


# The highlight string for one city, on one surface. Anchored on name+state so it
# cannot land on the wrong Wilmington.
def highlight_of(tmp, path, city, state):
    with open(os.path.join(tmp, path), encoding="utf-8") as fh:
        text = fh.read()
    if path == "index.html":
        pat = (r'name:\s*"%s",\s*state:\s*"%s".*?highlight:\s*"((?:[^"\\]|\\.)*)"'
               % (re.escape(city), re.escape(state)))
    else:
        pat = (r'"city":\s*"%s",\s*"state":\s*"%s".*?"highlight":\s*"((?:[^"\\]|\\.)*)"'
               % (re.escape(city), re.escape(state)))
    m = re.search(pat, text, re.S)
    if not m:
        raise AssertionError(f"could not find the highlight for {city}, {state} in {path}")
    return m.group(1)


# Planting into ONE surface desyncs it from the other, and check_highlight_surfaces
# reports that. It is a real failure and a correct one, so it is partitioned off rather
# than filtered away: every assertion below says what it expects from each check.
DRIFT = "highlight differs between surfaces"


def split(new):
    """(home-figure failures, surface-drift failures)."""
    drift = {f for f in new if DRIFT in f}
    return new - drift, drift


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: highlight home figures\n")

    homes = db_homes(repo, [("Wilmington", "DE"), ("Wilmington", "NC"),
                            ("Naples", "FL")])
    DE = homes[("Wilmington", "DE")]
    NC = homes[("Wilmington", "NC")]
    NAPLES = homes[("Naples", "FL")]
    WRONG = "$215K"          # the figure that actually shipped on Wilmington DE

    # The fixtures below are only meaningful if the planted figures really are wrong
    # and really do differ from each other. Assert it rather than assume it, because a
    # future refresh that collides them would turn several tests green by accident.
    assert K(DE) != WRONG, "the planted wrong figure now equals Wilmington DE's DB value"
    assert K(DE) != K(NC), "the two Wilmingtons now share a figure; test 3 is void"
    print(f"  database: Wilmington DE {K(DE)}, Wilmington NC {K(NC)}, "
          f"Naples {K(NAPLES)}\n")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    base_code, base_fails = run(tmp)
    shutil.rmtree(tmp)
    print(f"  control run: exit {base_code}, {len(base_fails)} failures\n")

    # ------------------------------------------------- 1. the error that shipped
    # Wilmington DE: highlight $215K against its DB Median Home.
    tmp = stage(repo)
    hl = highlight_of(tmp, "index.html", "Wilmington", "DE")
    assert K(DE) in hl, f"Wilmington DE's highlight no longer states {K(DE)}"
    edit(tmp, "index.html", hl, hl.replace(K(DE), WRONG))
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    new = fails - base_fails
    home, drift = split(new)
    check("planted $215K on Wilmington DE is caught",
          len(home) == 1 and "Wilmington, DE" in next(iter(home))
          and "$215K" in next(iter(home)) and len(drift) == 1,
          f"exit {code}, new failures: {sorted(new) or 'none'}")
    check("planted error gates the deploy (exit 1)", code == 1, f"exit {code}")

    # ---------------------------------------------- 2. the same error, other surface
    tmp = stage(repo)
    hl = highlight_of(tmp, "pick-and-compare.html", "Wilmington", "DE")
    edit(tmp, "pick-and-compare.html", hl, hl.replace(K(DE), WRONG))
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    new = fails - base_fails
    home, drift = split(new)
    check("pick-and-compare.html is parsed and checked too",
          len(home) == 1 and "pick-and-compare.html" in next(iter(home))
          and len(drift) == 1,
          f"new failures: {sorted(new) or 'none'}")

    # ------------------------------------------- 3. the two-Wilmingtons key guard
    # NC's own correct figure must be silent; DE's figure in NC's string must fail.
    # Both halves pass only if the lookup is keyed on (City, ST).
    tmp = stage(repo)
    hl = highlight_of(tmp, "index.html", "Wilmington", "NC")
    edit(tmp, "index.html", hl, f"A {K(NC)} typical home value. " + hl)
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    home, _ = split(fails - base_fails)
    check(f"Wilmington NC graded against NC's {K(NC)}, not DE's {K(DE)}",
          not home, f"new failures: {sorted(home) or 'none'}")

    tmp = stage(repo)
    hl = highlight_of(tmp, "index.html", "Wilmington", "NC")
    edit(tmp, "index.html", hl, f"A {K(DE)} typical home value. " + hl)
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    new = fails - base_fails
    home, _ = split(new)
    check("Wilmington NC carrying DE's figure is caught",
          len(home) == 1 and "Wilmington, NC" in next(iter(home)),
          f"new failures: {sorted(new) or 'none'}")

    # ------------------------------------------------------ 4. scope: no false fires
    # Every shape below is legitimate copy that a naive "any $ figure" check would
    # red-light. They are planted into one city's string and must produce silence.
    legit = [
        ("NRC neighborhood range",
         f" Citywide median home {K(DE)} but retirees target Greenville, Hockessin "
         "($400K\\u2013$1.1M)."),
        # JUDGMENT CALL, Jul 27 2026: this fixture used to read "Naples matches it at
        # $585K", which carries no home-value noun and so matched neither HL_HOME_FIG
        # nor HL_HOME_BOUND. It passed by matching nothing, which is the exact failure
        # this harness exists to catch, and it never once exercised the cross_city()
        # veto it is named for. Reworded to the sentence validate.py's own HL_* comment
        # says the veto is there for, and pointed at Naples' real figure.
        ("cross-city reference", f" Naples' median home is {K(NAPLES)}."),
        ("figure that is not a home value", " The $465M Gathering Place anchors downtown."),
        ("tax threshold", " A $132K joint retirement income deduction."),
        ("monthly budget range", " Budget $4,700\\u2013$5,800/mo."),
        ("a true bound", f" Affordable homes under {K(DE + 100_000)}."),
    ]
    for label, snippet in legit:
        tmp = stage(repo)
        hl = highlight_of(tmp, "index.html", "Wilmington", "DE")
        edit(tmp, "index.html", hl, hl + snippet)
        code, fails = run(tmp)
        shutil.rmtree(tmp)
        home, _ = split(fails - base_fails)
        check(f"no false fire: {label}",
              not home, f"{sorted(home) or 'silent'}")

    # ------------------------------------------------ 5. scope: real errors still caught
    # The mirror image. Each of these is false against Wilmington DE's DB figure.
    wrong = [
        ("stale figure off by one thousand",
         f" Typical home value ${round(DE / 1000) + 1}K."),
        ("a bound that does not hold", f" Median homes under {K(DE - 50_000)}."),
        ("wrong figure in full dollars", f" Median home ${DE - 100_000:,}."),
    ]
    for label, snippet in wrong:
        tmp = stage(repo)
        hl = highlight_of(tmp, "index.html", "Wilmington", "DE")
        edit(tmp, "index.html", hl, hl + snippet)
        code, fails = run(tmp)
        shutil.rmtree(tmp)
        home, _ = split(fails - base_fails)
        check(f"caught: {label}",
              len(home) == 1, f"{sorted(home) or 'SILENT'}")

    # ------------------------------------------------------------ 6. no silent no-op
    # If the CITIES array is renamed or reshaped, the check must say so rather than
    # scan zero strings and report a clean site.
    tmp = stage(repo)
    with open(os.path.join(tmp, "pick-and-compare.html"), encoding="utf-8") as fh:
        text = fh.read()
    with open(os.path.join(tmp, "pick-and-compare.html"), "w", encoding="utf-8") as fh:
        fh.write(text.replace("const CITIES = ", "const CITY_LIST = ", 1))
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    check("a missing CITIES array fails loudly, not silently",
          any("could not locate CITIES in pick-and-compare" in f
              for f in fails - base_fails),
          f"{sorted(fails - base_fails) or 'SILENT'}")

    # --------------------------------------------- 7. the two surfaces must agree
    # The same highlight lives in index.html and pick-and-compare.html. It used to
    # live in a database column too, and all three drifted apart unwatched: 65 rows,
    # 16 rows, 67 rows. The column is gone; these two both render, so they get gated.
    tmp = stage(repo)
    hl = highlight_of(tmp, "pick-and-compare.html", "Wilmington", "DE")
    edit(tmp, "pick-and-compare.html", hl, hl + " One extra sentence.")
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    check("caught: highlight differs between the two surfaces",
          any("highlight differs between surfaces" in f for f in fails - base_fails),
          f"{sorted(fails - base_fails) or 'SILENT'}")

    # A whole city present on one surface and not the other.
    tmp = stage(repo)
    with open(os.path.join(tmp, "index.html"), encoding="utf-8") as fh:
        text = fh.read()
    hl = highlight_of(tmp, "index.html", "Wilmington", "DE")
    with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(text.replace('highlight: "%s"' % hl, 'blurb: "%s"' % hl, 1))
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    check("caught: a city with a highlight on only one surface",
          any("no highlight in index.html" in f for f in fails - base_fails),
          f"{sorted(fails - base_fails) or 'SILENT'}")

    # And the no-op guard again, on the other extractor. Renaming the field on every
    # city must fail loudly, not quietly compare an empty set to an empty set.
    tmp = stage(repo)
    with open(os.path.join(tmp, "index.html"), encoding="utf-8") as fh:
        text = fh.read()
    with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(text.replace("highlight: \"", "blurb: \""))
    code, fails = run(tmp)
    shutil.rmtree(tmp)
    check("a reshaped index.html highlight field fails loudly, not silently",
          any("scanning nothing" in f for f in fails - base_fails),
          f"{sorted(fails - base_fails) or 'SILENT'}")

    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
