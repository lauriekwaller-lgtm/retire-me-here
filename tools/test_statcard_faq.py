#!/usr/bin/env python3
"""
Planted-error test for check_statcard_faq in validate.py.

    python3 tools/test_statcard_faq.py            # against this checkout
    python3 tools/test_statcard_faq.py --repo ..  # against another checkout

No check ships without one of these. This one guards three profile surfaces that were
unread until 2026-07-28, when a draft of the check found 44 wrong figures behind a gate
reading 0 failures, 0 warnings: the abbreviated monthly stat card, the two variable
score slots, and every home figure in profile prose and the JSON-LD FAQ.

Half of these assertions plant an ERROR and demand a failure. The other half plant
something that LOOKS like an error and demand silence, because on this surface the
false positives are the hard part and every one of them cost a wrong answer while the
check was being sized:

    1.  a drifted abbreviated monthly fails
    2.  a CORRECT monthly written with &ndash; does NOT fail (entity normalisation;
        Savannah is correct and only looks wrong to a byte comparison)
    3.  a drifted score slot fails
    4.  a score under a label that maps to no dimension fails, rather than being
        skipped, or the next new label is silently unwatched
    5.  free text under a mapped label does NOT fail ("Healthcare: Barnes-Jewish" is
        thirty slots on this site, and keying on the label alone fails all of them)
    6.  a drifted home figure in the JSON-LD FAQ fails
    7.  a drifted home figure separated from its noun by a HEDGE fails. PROSCONS_HOME
        requires adjacency; profile voice is "the typical home value in Columbus is
        around $251,000" and reusing that matcher covered 13 of about 45 figures
    8.  a wrong figure carrying a trailing comma, with an innocent excuse word later in
        the sentence, still fails. This is the exact shape St. Louis hid behind: a money
        class ending [\\d.,]+ swallows the comma and drags the guard a clause forward
    9.  a wrong OWN figure followed in the same sentence by another city's figure still
        fails, so the other-place guard cannot reach forward and excuse real drift
    10. another city's home figure, named before it, does NOT fail
    11. a wrong figure inside a hood-card does NOT fail: neighborhood medians are
        supposed to differ from the citywide number
    12. a wrong figure in a method-callout fails even with NO home-value noun present,
        and 12b the same for the Neighborhood Reality Check, which is an <aside> and was
        skipped in silence by a div-only region walk
    13. a range does NOT fail, because a range is the Neighborhood Reality Check pattern
    14. stats-bar markup that yields no slots fails loudly on that profile
    15. the same markup change across every profile trips the global zero guard, rather
        than reporting a clean run over nothing
    16. the control run is clean, so the check is not merely failing at everything

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Chosen because their markup is the common shape, not because they are special. If a
# rebuild moves any of these the harness raises rather than quietly testing nothing.
MONTHLY_CITY = "columbus"
SCORE_CITY = "columbus"
LD_CITY = "tucson"
PROSE_CITY = "madison"
CALLOUT_CITY = "st-louis"
NRC_CITY = "columbus"
HOOD_CITY = "pittsburgh"

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-statcard-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc",
                                                  "*.jpg", "*.jpeg", "*.png", "*.webp"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the profiles group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "profiles"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def path_of(slug):
    return os.path.join("cities", slug, "profile.html")


def read(tmp, path):
    with open(os.path.join(tmp, path), encoding="utf-8") as fh:
        return fh.read()


def write(tmp, path, text):
    with open(os.path.join(tmp, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def sub_once(tmp, slug, old, new, what):
    """Replace exactly once, or raise. A plant that did not land tests nothing."""
    path = path_of(slug)
    html = read(tmp, path)
    n = html.count(old)
    if n != 1:
        raise AssertionError(
            f"harness cannot plant {what}: expected exactly one occurrence of "
            f"{old[:60]!r} in {path}, found {n}. The markup has changed; update the "
            f"anchors in this test rather than loosening the assertions.")
    write(tmp, path, html.replace(old, new, 1))


def stat_value(tmp, slug, label):
    """The raw inner HTML of the stat-value under `label`, plus its whole block."""
    html = read(tmp, path_of(slug))
    m = re.search(r'<div class="stat-label">\s*' + re.escape(label) +
                  r'\s*</div>\s*<div class="stat-value">(.*?)</div>', html, re.S)
    if not m:
        raise AssertionError(
            f"harness cannot find a {label!r} stat card in {path_of(slug)}. The "
            f"stats-bar markup has changed; update this test.")
    return m.group(0), m.group(1)


def first_sentence_anchor(tmp, slug, needle):
    html = read(tmp, path_of(slug))
    if html.count(needle) != 1:
        raise AssertionError(
            f"harness anchor {needle[:50]!r} is not unique in {path_of(slug)} "
            f"({html.count(needle)} occurrences). Update this test.")
    return needle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    repo = ap.parse_args().repo

    # ------------------------------------------------------- 16. control is clean
    tmp = stage(repo)
    base_code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    check("control run is clean", base_code == 0 and not base,
          f"{len(base)} failure(s)")

    # ------------------------------------------- 1. drifted abbreviated monthly
    tmp = stage(repo)
    block, inner = stat_value(tmp, MONTHLY_CITY, "Monthly Budget")
    digits = re.search(r"\$[\d.]+", inner).group(0)
    bumped = "$" + str(round(float(digits[1:]) + 1.1, 1))
    sub_once(tmp, MONTHLY_CITY, block, block.replace(digits, bumped, 1),
             "a drifted abbreviated monthly")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a drifted abbreviated monthly fails",
          code == 1 and any("stat card monthly" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------- 2. a CORRECT monthly written with an entity
    tmp = stage(repo)
    block, inner = stat_value(tmp, MONTHLY_CITY, "Monthly Budget")
    sub_once(tmp, MONTHLY_CITY, block, block.replace("\u2013", "&ndash;"),
             "an entity-encoded but correct monthly")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a correct monthly written with &ndash; does not fail",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ------------------------------------------------------ 3. drifted score slot
    tmp = stage(repo)
    block, inner = stat_value(tmp, SCORE_CITY, "Healthcare")
    hit = re.search(r"(\d{1,2})(<span[^>]*>/10)", inner)
    if not hit:
        raise AssertionError(f"{SCORE_CITY} Healthcare slot is not an N/10 score")
    wrong = ("1" if hit.group(1) != "1" else "2") + hit.group(2)
    sub_once(tmp, SCORE_CITY, block, block.replace(hit.group(0), wrong, 1),
             "a drifted score slot")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a drifted score slot fails",
          code == 1 and any("DB D3 is" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------------------------- 4. a score under an unmapped label
    tmp = stage(repo)
    block, _ = stat_value(tmp, SCORE_CITY, "Healthcare")
    sub_once(tmp, SCORE_CITY, block,
             block.replace(">Healthcare<", ">Hospital Depth<", 1),
             "a score under an unmapped label")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a score under an unmapped label fails rather than being skipped",
          code == 1 and any("maps to no dimension" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------ 5. free text under a mapped label
    tmp = stage(repo)
    block, inner = stat_value(tmp, SCORE_CITY, "Healthcare")
    sub_once(tmp, SCORE_CITY, block,
             block.replace(inner, "Wexner", 1),
             "free text under a mapped label")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("free text under a mapped label does not fail",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ---------------------------------------------- 6. drifted JSON-LD home figure
    tmp = stage(repo)
    html = read(tmp, path_of(LD_CITY))
    m = re.search(r"(typical home value is around \$)(\d{3},\d{3})", html)
    if not m:
        raise AssertionError(f"{LD_CITY} JSON-LD does not carry the expected home phrase")
    sub_once(tmp, LD_CITY, m.group(0), m.group(1) + "999,000",
             "a drifted JSON-LD home figure")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a drifted home figure in the JSON-LD FAQ fails",
          code == 1 and any("JSON-LD states a home value" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------------- 7. a hedge between the noun and the figure
    tmp = stage(repo)
    anchor = first_sentence_anchor(
        tmp, PROSE_CITY, "A typical home value around $435K")
    sub_once(tmp, PROSE_CITY, anchor,
             "The typical home value in Madison is around $911,000",
             "a hedged home figure")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a home figure separated from its noun by a hedge fails",
          code == 1 and any("$911,000" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------- 8. trailing comma plus an innocent excuse word after
    tmp = stage(repo)
    anchor = first_sentence_anchor(
        tmp, PROSE_CITY, "A typical home value around $435K")
    sub_once(tmp, PROSE_CITY, anchor,
             "The typical home value is around $911,000, though the suburbs vary",
             "a wrong figure with a trailing comma")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a wrong figure with a trailing comma is not excused by a later clause",
          code == 1 and any("$911,000" in f for f in added),
          f"{len(added)} new failure(s)")

    # ----------------- 9. the other-place guard must not reach FORWARD and excuse
    tmp = stage(repo)
    anchor = first_sentence_anchor(
        tmp, PROSE_CITY, "A typical home value around $435K")
    sub_once(tmp, PROSE_CITY, anchor,
             "The typical home value is around $911,000 above Tampa's $380,000",
             "a wrong own figure trailed by another city")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("the other-place guard does not reach forward to excuse real drift",
          code == 1 and any("$911,000" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------- 10. another city's figure, named before it
    tmp = stage(repo)
    anchor = first_sentence_anchor(
        tmp, PROSE_CITY, "A typical home value around $435K")
    sub_once(tmp, PROSE_CITY, anchor,
             "A typical home value around $435K. Naples' median home value is $549K",
             "a cross-city home figure")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("another city's home figure, named before it, does not fail",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # --------------------------------------------- 11. a hood-card is out of scope
    tmp = stage(repo)
    html = read(tmp, path_of(HOOD_CITY))
    m = re.search(r"<strong>Median home: around \$\d+K\.</strong>", html)
    if not m:
        raise AssertionError(
            f"{HOOD_CITY} no longer carries a single-figure hood-card median. Pick "
            f"another city rather than dropping this assertion.")
    sub_once(tmp, HOOD_CITY, m.group(0),
             "<strong>Median home: around $999K.</strong>",
             "a wrong hood-card median")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a wrong figure inside a hood-card does not fail",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # ------------------------------ 12. the method-callout region rule, no noun at all
    #
    # The figure this plants carries NO home-value noun: the sentence says "the
    # city-limits figure". That is the point. Three real faults on this site had exactly
    # that shape, including Tulsa's NRC still built on a figure the rebase moved 14.9%,
    # and a noun-anchored matcher reaches none of them.
    tmp = stage(repo)
    html = read(tmp, path_of(CALLOUT_CITY))
    m = re.search(r"the city-limits figure \(~\$\d+K\)", html)
    if not m:
        raise AssertionError(
            f"{CALLOUT_CITY} method-callout no longer opens on a bare figure. Update "
            f"this test rather than dropping it.")
    sub_once(tmp, CALLOUT_CITY, m.group(0), "the city-limits figure (~$999K)",
             "a wrong method-callout figure")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a wrong figure in a method-callout fails with no noun present",
          code == 1 and any("method-callout opens on" in f for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------- 12b. the same rule on the Neighborhood Reality Check
    #
    # Separate assertion because the NRC is an <aside>, not a <div>. A div-only region
    # walk skipped it in silence, and that alone would have left Tulsa's NRC unread.
    tmp = stage(repo)
    html = read(tmp, path_of(NRC_CITY))
    m = re.search(r"The \$\d+K citywide median", html)
    if not m:
        raise AssertionError(
            f"{NRC_CITY} no longer opens its NRC on the citywide figure. Pick another "
            f"NRC city rather than dropping this assertion.")
    sub_once(tmp, NRC_CITY, m.group(0), "The $999K citywide median",
             "a wrong NRC opening figure")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a wrong opening figure in the NRC <aside> fails",
          code == 1 and any("reality-check opens on" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------- 13. a range is not a claim
    tmp = stage(repo)
    anchor = first_sentence_anchor(
        tmp, PROSE_CITY, "A typical home value around $435K")
    sub_once(tmp, PROSE_CITY, anchor,
             "A typical home value around $400K\u2013$900K",
             "a home-value range")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a home-value range does not fail",
          code == 0 and not added, f"{len(added)} new failure(s)")

    # --------------------------- 14. stats-bar markup that yields nothing, one page
    tmp = stage(repo)
    html = read(tmp, path_of(MONTHLY_CITY))
    write(tmp, path_of(MONTHLY_CITY), html.replace('<div class="stat">',
                                                   '<div class="statistic">'))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("stats-bar markup that yields no slots fails loudly on that profile",
          code == 1 and any("stat slots, expected 4" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------ 15. the same change everywhere trips the global guard
    tmp = stage(repo)
    for slug in os.listdir(os.path.join(tmp, "cities")):
        p = path_of(slug)
        if os.path.exists(os.path.join(tmp, p)):
            write(tmp, p, read(tmp, p).replace('<div class="stat">',
                                               '<div class="statistic">'))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("stats-bar markup gone site-wide trips the zero-slot guard",
          code == 1 and any("found zero" in f and "score slots" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------- verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
