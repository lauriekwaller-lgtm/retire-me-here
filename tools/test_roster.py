#!/usr/bin/env python3
"""
Planted-error test for check_roster in validate.py.

    python3 tools/test_roster.py            # against this checkout
    python3 tools/test_roster.py --repo ..  # against another checkout

No check ships without one of these. This one exists because the fault it guards was
not a wrong number anywhere. On July 27 2026 the budget page carried Beaufort,
Pensacola, Rio Rancho and Sioux Falls after all four left Budget Range 1 in the ZHVI
rebase, and was missing San Antonio after it dropped in. Five cities wrong, and the
gate ran over that exact page and printed 0 failures, because check_cards only asks
per-card questions: does this card's money match the DB, and is it marked "coming soon"
while its profile is live. Every card passed both. Nothing asked which cities belonged.

So the assertions here are about SHAPE, not about one direction of error:

    1. a city on the page that is not in the tier fails
    2. a city in the tier with no card fails
    3. BOTH directions fail in the same run, because a roster that has drifted usually
       has drifted both ways at once, and a check that only catches extras would have
       reported this fault as four problems instead of five
    4. a duplicated card fails, since set-comparison alone silently tolerates it
    5. markup that no longer yields cards fails LOUDLY instead of comparing nothing.
       This is the failure mode the codebase keeps rediscovering: a check that reads
       zero and calls it clean. best-places-to-retire-in-florida.html has no city cards
       at all today, which is exactly why it is not in DB_ROSTERS.
    6. a renamed page fails, rather than silently retiring its own coverage
    7. the control run is clean, so the check is not merely failing at everything

Exit 0 = all tests pass.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PAGE = "best-places-to-retire-on-a-budget.html"

# A city that is in Budget Range 1 and has a card, used as the deletion target.
IN_TIER = ("Casper", "WY")
# A city that is NOT in Budget Range 1, used as the insertion target.
OUT_OF_TIER = ("Pensacola", "FL")


def stage(repo):
    """A throwaway copy of the checkout. The real files are never written to."""
    tmp = tempfile.mkdtemp(prefix="rmh-roster-")
    shutil.copytree(repo, os.path.join(tmp, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return os.path.join(tmp, "repo")


def run(tmp):
    """Run the cards group. Returns (exit_code, {failure lines})."""
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--local", ".", "--only", "cards"],
        cwd=tmp, capture_output=True, text=True)
    fails = {ln.split("[FAIL]", 1)[1].strip()
             for ln in proc.stdout.splitlines() if "[FAIL]" in ln}
    return proc.returncode, fails


def read(tmp, path):
    with open(os.path.join(tmp, path), encoding="utf-8") as fh:
        return fh.read()


def write(tmp, path, text):
    with open(os.path.join(tmp, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def card_of(html, city, state):
    """The full markup of one card, so a test can delete or clone it verbatim."""
    for m in re.finditer(r'<(a|div) class="city-card', html):
        tag = m.group(1)
        depth, i = 0, m.start()
        step = re.compile(rf"</?{tag}\b", re.I)
        while True:
            t = step.search(html, i)
            if not t:
                return None
            depth += -1 if t.group(0).startswith("</") else 1
            i = t.end()
            if depth == 0:
                block = html[m.start():i]
                break
        if (f'city-name">{city}<span class="state-code">{state}</span>') in block:
            return block
    return None


def drop_card(tmp, city, state):
    html = read(tmp, PAGE)
    block = card_of(html, city, state)
    if block is None:
        raise AssertionError(
            f"harness cannot find a {city}, {state} card in {PAGE}. The roster or the "
            f"markup has changed; update the anchors in this test rather than "
            f"loosening the assertions.")
    write(tmp, PAGE, html.replace(block, "", 1))


def add_card(tmp, city, state, monthly="$5,000–$6,200/mo · Planted"):
    """Clone an existing card's shape so the plant is markup-identical to a real one."""
    html = read(tmp, PAGE)
    model = card_of(html, *IN_TIER)
    if model is None:
        raise AssertionError(f"harness cannot find the {IN_TIER} model card in {PAGE}")
    planted = (model
               .replace(f'{IN_TIER[0]}<span class="state-code">{IN_TIER[1]}</span>',
                        f'{city}<span class="state-code">{state}</span>')
               .replace(re.search(r'city-teams">([^<]*)</div>', model).group(1),
                        monthly))
    write(tmp, PAGE, html.replace(model, model + "\n\n" + planted, 1))


RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    print("planted-error test: landing-page roster membership\n")

    # ---------------------------------------------------------------- control
    tmp = stage(repo)
    base_code, base = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    print(f"  control run: exit {base_code}, {len(base)} failures\n")
    check("control run is clean: the roster matches Budget Range 1 today",
          base_code == 0 and not base,
          f"{len(base)} failure(s): {sorted(base)[:2]}")

    # ------------------------------------------- 1. a city outside the tier is caught
    tmp = stage(repo)
    add_card(tmp, *OUT_OF_TIER)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a city on the page but outside the tier is caught",
          code == 1 and any(f"{OUT_OF_TIER[0]}, {OUT_OF_TIER[1]}" in f
                            and "not in Budget Range 1" in f for f in added),
          f"{len(added)} new failure(s)")

    # --------------------------------------------- 2. a missing tier city is caught
    tmp = stage(repo)
    drop_card(tmp, *IN_TIER)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a city in the tier with no card is caught",
          code == 1 and any(f"{IN_TIER[0]}, {IN_TIER[1]}" in f
                            and "no card" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------- 3. both directions are caught in the SAME run
    # This is the shape of the real fault: four extras and one omission at once.
    tmp = stage(repo)
    add_card(tmp, *OUT_OF_TIER)          # clone first: the model card is IN_TIER's
    drop_card(tmp, *IN_TIER)
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    both = (any(f"{IN_TIER[0]}, {IN_TIER[1]}" in f and "no card" in f for f in added)
            and any(f"{OUT_OF_TIER[0]}, {OUT_OF_TIER[1]}" in f
                    and "not in Budget Range 1" in f for f in added))
    check("an extra AND an omission both fail in one run",
          code == 1 and both, f"{len(added)} new failure(s)")

    # ------------------------------------------------- 4. a duplicated card is caught
    tmp = stage(repo)
    add_card(tmp, *IN_TIER, monthly="$4,800–$5,900/mo · Planted duplicate")
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a duplicated card is caught",
          code == 1 and any(f"{IN_TIER[0]}, {IN_TIER[1]}" in f
                            and "more than once" in f for f in added),
          f"{len(added)} new failure(s)")

    # -------------------------------- 5. markup yielding no cards fails loudly
    # The silent no-op: read zero, report clean. If this ever passes quietly, the
    # check has stopped checking and nothing on the gate would say so.
    tmp = stage(repo)
    write(tmp, PAGE, read(tmp, PAGE).replace('class="city-card', 'class="cityCard'))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("card markup that yields nothing fails loudly, not silently",
          code == 1 and any("never compared" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------- 6. a renamed page is caught
    tmp = stage(repo)
    os.rename(os.path.join(tmp, PAGE),
              os.path.join(tmp, "best-places-to-retire-on-a-budget-2026.html"))
    code, fails = run(tmp)
    shutil.rmtree(os.path.dirname(tmp))
    added = fails - base
    check("a renamed page fails rather than retiring its own coverage",
          code == 1 and any("matched no file" in f for f in added),
          f"{len(added)} new failure(s)")

    # ------------------------------------------------------------------ verdict
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n  {len(RESULTS) - len(bad)}/{len(RESULTS)} passed")
    if bad:
        print("  failed: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
