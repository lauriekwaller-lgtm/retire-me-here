#!/usr/bin/env python3
"""
apply-tulsa.py  --  RetireMeHere: ship the Tulsa, OK profile.

Run from the repo root in Codespaces, AFTER `git pull`, and AFTER dropping
cities/tulsa/profile.html and the three photos into place:

    git pull
    mkdir -p cities/tulsa
    # copy tulsa-profile.html  -> cities/tulsa/profile.html
    # copy tulsa-hero.jpg      -> cities/tulsa/hero.jpg
    # copy tulsa-detail.jpg    -> cities/tulsa/detail.jpg
    # copy tulsa-lifestyle.jpg -> cities/tulsa/lifestyle.jpg
    python3 apply-tulsa.py
    python3 tools/validate.py --local .

Edits five existing files with minimum diffs:
  1. index.html                              PUBLISHED_PROFILES entry
  2. sitemap.xml                             url block
  3. best-places-to-retire-on-a-budget.html  coming-soon div -> live card
  4. docs/SUPERLATIVE-LEDGER.md              two Saint Francis rows
  5. docs/TASKBOARD.md                       counts 45 -> 46, queue, follow-ups

Idempotent: re-running is a no-op. Exits non-zero and changes nothing if any
anchor has moved, so a drifted file fails loudly instead of silently.
Delete this script after use; it is not meant to be committed.
"""

import os
import sys

EDITS = []


def edit(path, old, new, done_marker):
    EDITS.append((path, old, new, done_marker))


# ---------------------------------------------------------------- 1. index.html
edit(
    "index.html",
    "    'Roanoke_VA': 'cities/roanoke/profile.html'\n  };",
    "    'Roanoke_VA': 'cities/roanoke/profile.html',\n"
    "    'Tulsa_OK': 'cities/tulsa/profile.html'\n  };",
    "'Tulsa_OK': 'cities/tulsa/profile.html'",
)

# ---------------------------------------------------------------- 2. sitemap.xml
SITEMAP_ANCHOR = """    <loc>https://retiremehere.com/cities/roanoke/profile.html</loc>
    <lastmod>2026-07-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
edit(
    "sitemap.xml",
    SITEMAP_ANCHOR,
    SITEMAP_ANCHOR + """
  <url>
    <loc>https://retiremehere.com/cities/tulsa/profile.html</loc>
    <lastmod>2026-07-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
""",
    "cities/tulsa/profile.html</loc>",
)

# ------------------------------------------- 3. budget landing page: card goes live
edit(
    "best-places-to-retire-on-a-budget.html",
    """        <div class="city-card coming-soon" title="Profile coming soon">
          <div class="city-rank">31</div>
          <div class="city-info">
            <div class="city-name">Tulsa<span class="state-code">OK</span></div>
            <div class="city-teams">$4,200\u2013$5,300/mo \u00b7 Major Metro / Cultural / Plains</div>
          </div>
          <span class="city-soon">Coming soon</span>
        </div>""",
    """        <a class="city-card" href="index.html?city=Tulsa&state=OK">
          <div class="city-rank">31</div>
          <div class="city-info">
            <div class="city-name">Tulsa<span class="state-code">OK</span></div>
            <div class="city-teams">$4,200\u2013$5,300/mo \u00b7 Major Metro / Cultural / Plains</div>
          </div>
          <span class="city-arrow">\u2192</span>
        </a>""",
    'href="index.html?city=Tulsa&state=OK"',
)

# --------------------------------------------------- 4. superlative ledger rows
LEDGER_ANCHOR = (
    "| cities/st-petersburg/profile.html | largest farmers markets in the Southeast, "
    "in season from fall through | TRUE | Outside-world claim, hedged or sourced. "
    "Not scoped to our dataset; cannot rot when a city is added. |\n"
)
edit(
    "docs/SUPERLATIVE-LEDGER.md",
    LEDGER_ANCHOR,
    LEDGER_ANCHOR
    + "| cities/tulsa/profile.html | largest hospital in Oklahoma and the 11th largest in the "
      "nation, anchored by a 168-bed heart | TRUE | Saint Francis Hospital, 1,112 beds: largest in "
      "Oklahoma and 11th largest in the US, per Saint Francis Health System and the Premier 15 Top "
      "Health Systems 2025 study. Outside-world fact, static. |\n"
      "| cities/tulsa/profile.html | largest hospital in the state | TRUE | Same Saint Francis "
      "claim, in the JSON-LD FAQ answer. 1,112 beds, largest in Oklahoma. |\n",
    "| cities/tulsa/profile.html |",
)

# ------------------------------------------------------------------ 5. taskboard
edit(
    "docs/TASKBOARD.md",
    """**Last updated:** July 24, 2026 (Roanoke, VA profile shipped, profile 45; four stale Roanoke
index.html figures fixed en route: $280K->$251K, hospital 16->15, D1 routes refreshed, D7
"Range 2"->"Range 1"; Carvins Cove second-largest-municipal-park claim retired to the ledger)

**Verified live at last update:** 45 profiles, 20 comparison pages, 5 guides, 7 landing pages.
All 45 profiles carry a Visit block (Roanoke's uses placeholder affiliate codes pending Creator Hub).""",
    """**Last updated:** July 24, 2026 (Tulsa, OK profile shipped, profile 46; Tulsa card on
best-places-to-retire-on-a-budget.html promoted from coming-soon to a live link; two Saint Francis
"largest hospital" claims retired to the ledger. Earlier the same day: Roanoke, VA shipped as profile
45, with four stale Roanoke index.html figures fixed en route: $280K->$251K, hospital 16->15, D1
routes refreshed, D7 "Range 2"->"Range 1"; Carvins Cove second-largest-municipal-park claim retired)

**Verified live at last update:** 46 profiles, 20 comparison pages, 5 guides, 7 landing pages.
All 46 profiles carry a Visit block with per-city Expedia and Vrbo codes (Roanoke's are still
placeholders pending Creator Hub; Tulsa's are live).""",
    "Tulsa, OK profile shipped, profile 46",
)

edit(
    "docs/TASKBOARD.md",
    """- **Next in queue:** Roanoke, then Tulsa.
- Live profiles: 44. San Antonio shipped Jul 19; Fort Collins, Prescott, Knoxville and Savannah
  shipped earlier in the same window.
- San Antonio carries a Neighborhood Reality Check callout, making it the 11th NRC city.
  `PROFILE-FORMATTING.md` still lists ten and needs updating.""",
    """- **Next in queue:** open. Roanoke and Tulsa both shipped Jul 24.
- Live profiles: 46. Tulsa shipped Jul 24; Roanoke the same day; San Antonio Jul 19; Fort Collins,
  Prescott, Knoxville and Savannah shipped earlier in the same window.
- San Antonio carries a Neighborhood Reality Check callout, making it the 11th NRC city, and Tulsa
  makes it 12 (citywide $194K against retiree-target $300K-$500K, the exact gap the note exists for).
  `PROFILE-FORMATTING.md` still lists ten and is now two behind.
- **Tulsa follow-ups (not blocking the push):**
  - `pick-and-compare.html` carries Tulsa at `d2:7`; DB and `index.html` both say **D2 = 9**. Stale.
  - `index.html` enrichment gives Tulsa property tax 0.77%; DB says 0.79. Profile uses the DB.
  - `top-cities-for-arts-lovers.html` lists Gilcrease Museum on the Tulsa card as a live asset. It
    has been closed since 2021 and now reopens spring 2027, a year late and ~70% over budget.
  - Detail photo is a placeholder (ORU Prayer Tower); swap for Art Deco downtown, Cain's, or Route 66.""",
    "**Tulsa follow-ups (not blocking the push):**",
)


def main():
    if not os.path.isfile("index.html") or not os.path.isdir("cities"):
        sys.exit("Run this from the repo root (index.html and cities/ must be here).")

    planned, skipped, missing = [], [], []
    cache = {}

    for path, old, new, marker in EDITS:
        if not os.path.isfile(path):
            missing.append(f"{path}: file not found")
            continue
        if path not in cache:
            cache[path] = open(path, encoding="utf-8").read()
        text = cache[path]
        if marker in text:
            skipped.append(f"{path}: already applied ({marker[:48]}...)")
            continue
        n = text.count(old)
        if n != 1:
            missing.append(f"{path}: anchor found {n} times, expected 1. File has drifted.")
            continue
        cache[path] = text.replace(old, new, 1)
        planned.append(f"{path}: patched")

    if missing:
        print("STOPPED. Nothing written.\n")
        for m in missing:
            print("  [FAIL]", m)
        print("\nRe-pull main, or hand the drifted file back for a fresh diff.")
        sys.exit(1)

    for path in {p for p, *_ in EDITS}:
        if path in cache:
            open(path, "w", encoding="utf-8").write(cache[path])

    for line in planned:
        print("  [OK]  ", line)
    for line in skipped:
        print("  [SKIP]", line)

    print("\nProfile file and photos are NOT handled here. Confirm they are in place:")
    for f in ("cities/tulsa/profile.html", "cities/tulsa/hero.jpg",
              "cities/tulsa/detail.jpg", "cities/tulsa/lifestyle.jpg"):
        print(f"  {'present' if os.path.isfile(f) else 'MISSING'}  {f}")

    print("\nNext: python3 tools/validate.py --local .   (expect 0 failures, 0 warnings)")


if __name__ == "__main__":
    main()
