#!/usr/bin/env python3
"""
RetireMeHere site validator.

Checks every live page against the canonical City Database and reports drift.
Exit code 0 = clean, 1 = failures found.

Usage:
    python3 tools/validate.py                       # check the LIVE site on GitHub
    python3 tools/validate.py --local .             # check your working copy before pushing
    python3 tools/validate.py --db path/to/db.xlsx  # override the database
    python3 tools/validate.py --only figures        # run one check group
    python3 tools/validate.py --quiet               # failures only, no PASS lines

Check groups:
    figures      CITIES array + CITY_ENRICHMENT modal strings vs DB
    profiles     profile pages: monthly + citywide home value vs DB
    routing      PUBLISHED_PROFILES <-> profile files <-> sitemap parity
    cards        landing pages: stale "coming soon" + card figures vs DB
    superlatives every affordability superlative on the site, checked against the DB
    emdash       em-dash policy (profiles + comparison pages)
    affiliate    affiliate codes: duplicates, missing brands, multiple codes per page
    db           database hygiene

Why this exists: every figure on this site is a string that either matches a DB cell
or does not. That is machine-checkable. Before this script existed, it was not being
checked, and drift accumulated silently across 100 cities and 80 pages.
"""

import argparse
import json
import os
import re
import sys
import urllib.request

RAW = "https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main"
# The database already lives in the repo, in docs/. That is the canonical copy the
# validator reads. Update this constant when you bump the version, in the same commit
# that adds the new xlsx.
DEFAULT_DB = "docs/CityDatabase_Jul_06_v16_1_stpaul-corrected.xlsx"

# Tolerated deviation on home-value prose before we call it stale.
HOME_TOLERANCE = 0.03

# The em-dash rule applies here. Guides and landing pages are grandfathered;
# see PROFILE-FORMATTING.md. Flip GUIDES_TOO to True if that decision changes.
GUIDES_TOO = False

DIMS = [
    ("D1", "D1 Airport"), ("D2", "D2 Budget"), ("D3", "D3 Health"),
    ("D4", "D4 Resil."), ("D5", "D5 Tax"), ("D6", "D6 Walk"),
    ("D7", "D7 Outdoor"), ("D8", "D8 Wellness"), ("D9", "D9 Safety"),
    ("D10", "D10 Comm."),
]

RANGE_RE = re.compile(r"(\$\d{1,2},\d{3})\s*(?:–|—|to|-)\s*(\$\d{1,2},\d{3})")
MONEY_RE = re.compile(r"\$\d{3}K|\$\d{3},\d{3}|\$\d(?:\.\d{1,2})?M")


# ---------------------------------------------------------------- infrastructure

class Report:
    def __init__(self, quiet=False):
        self.fails = []
        self.warns = []
        self.quiet = quiet

    def fail(self, group, msg):
        self.fails.append((group, msg))

    def warn(self, group, msg):
        self.warns.append((group, msg))

    def render(self):
        by_group = {}
        for g, m in self.fails:
            by_group.setdefault(g, []).append(("FAIL", m))
        for g, m in self.warns:
            by_group.setdefault(g, []).append(("WARN", m))

        for group in sorted(by_group):
            print(f"\n{'=' * 72}\n{group.upper()}\n{'=' * 72}")
            for level, msg in by_group[group]:
                print(f"  [{level}] {msg}")

        print(f"\n{'=' * 72}")
        print(f"  {len(self.fails)} failures, {len(self.warns)} warnings")
        print(f"{'=' * 72}")
        return 1 if self.fails else 0


def fetch(path, local=None):
    """Read a site file, from a local checkout if given, else from live GitHub."""
    if local:
        full = os.path.join(local, path)
        if not os.path.exists(full):
            return None
        with open(full, encoding="utf-8") as fh:
            return fh.read()
    try:
        with urllib.request.urlopen(f"{RAW}/{path}", timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


def money_to_int(tok):
    """
    Parse a single money token. Returns None on anything ambiguous.

    Deliberately strict. An earlier version stripped punctuation and glued the
    digits together, so the range "$430,000-$960,000" silently became the integer
    430000960000 and every downstream comparison for that city ran against garbage.
    A parser that cannot fail is a parser that lies.
    """
    tok = tok.strip().replace(" ", "")
    if len(re.findall(r"\$", tok)) > 1 or re.search(r"[–—]", tok):
        return None                      # a range, not a single figure
    num = re.sub(r"[^0-9.]", "", tok)
    if not num or num.count(".") > 1:
        return None
    val = float(num)
    if tok.endswith("K"):
        val *= 1_000
    elif tok.endswith("M"):
        val *= 1_000_000
    return int(val)


def load_db(path):
    """Load the City Database. Accepts .csv or .xlsx."""
    if path.endswith(".xlsx"):
        import pandas as pd
        df = pd.read_excel(path, sheet_name="City Database", header=1)
    else:
        import pandas as pd
        df = pd.read_csv(path)
    df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]

    # Keyed by BOTH "City" and "City_ST". Wilmington NC and Wilmington DE are both
    # in the database, so a city-name-only key silently drops one of them. Anything
    # that knows the state should look up "City_ST" first.
    db = {}
    names = {}
    for _, r in df.iterrows():
        city = str(r["City"]).strip()
        state = str(r["ST"]).strip()
        raw_home = str(r["Median Home"]).strip()
        home = money_to_int(raw_home if raw_home.startswith("$") else f"${raw_home}")
        row = {
            "city": city,
            "state": state,
            "monthly": str(r["Monthly Est"]).strip(),
            "home": home,             # None if the DB cell is malformed; see check_db
            "home_raw": raw_home,
            "range": int(r["Budget Range"]),
            "scores": {k: int(r[col]) for k, col in DIMS},
        }
        db[f"{city}_{state}"] = row
        names.setdefault(city, []).append(row)

    for city, rows in names.items():
        if len(rows) == 1:
            db[city] = rows[0]          # unambiguous, name-only lookup is safe
        else:
            db[city] = None             # ambiguous: force callers to supply state
    return db


def db_get(db, city, state=None):
    """Look up a city. Returns None if the name is ambiguous and no state is given."""
    if state:
        row = db.get(f"{city}_{state}")
        if row:
            return row
    return db.get(city)


def db_cities(db):
    """Every real row, once."""
    return [v for k, v in db.items() if v is not None and "_" in k]


def home_forms(value):
    """Every acceptable rendering of a home value."""
    forms = {f"${value:,}", f"${round(value / 1000)}K"}
    if value >= 1_000_000:
        forms.add(f"${value / 1e6:.2f}M")
        forms.add(f"${value / 1e6:.1f}M")
    return forms


def visible_text(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", html))


def js_object_slice(html, const_name):
    """Return the source text of `const NAME = { ... }` or `= [ ... ]`."""
    m = re.search(rf"const {const_name}\s*=\s*[\{{\[]", html)
    if not m:
        return ""
    open_ch = html[m.end() - 1]
    close_ch = "}" if open_ch == "{" else "]"
    depth = 0
    for i in range(m.end() - 1, len(html)):
        if html[i] == open_ch:
            depth += 1
        elif html[i] == close_ch:
            depth -= 1
            if depth == 0:
                return html[m.end() - 1:i + 1]
    return ""


# ---------------------------------------------------------------- checks

def check_figures(rep, db, idx):
    """CITIES array and CITY_ENRICHMENT modal strings vs the DB."""
    cities_src = js_object_slice(idx, "CITIES")
    if not cities_src:
        rep.fail("figures", "could not locate the CITIES array in index.html")
        return

    seen = 0
    for obj in re.split(r"\n  \{", cities_src)[1:]:
        nm = re.search(r'name:\s*"([^"]+)",\s*state:\s*"([^"]+)"', obj)
        if not nm:
            continue
        city, state = nm.group(1), nm.group(2)
        seen += 1
        row = db_get(db, city, state)
        if not row:
            rep.fail("figures", f"CITIES: {city}, {state} is not in the database")
            continue

        def field(pat):
            m = re.search(pat, obj)
            return m.group(1) if m else None

        checks = [
            ("monthlyEst", field(r'monthlyEst:\s*"([^"]+)"'), row["monthly"]),
            ("budgetRange", field(r"budgetRange:\s*(\d)"), str(row["range"])),
        ]
        if row["home"] is not None:
            checks.append(
                ("medianHome", field(r'medianHome:\s*"([^"]+)"'), f"${row['home']:,}"))
        for label, got, want in checks:
            if got != want:
                rep.fail("figures",
                         f"CITIES {city}, {state}: {label} is {got!r}, DB says {want!r}")

        sc = re.search(r"scores:\s*\{([^}]+)\}", obj)
        if sc:
            got = {k: int(v) for k, v in re.findall(r"(D\d+):(\d+)", sc.group(1))}
            for key, _ in DIMS:
                if got.get(key) != row["scores"][key]:
                    rep.fail("figures",
                             f"CITIES {city}, {state}: {key} is {got.get(key)}, "
                             f"DB says {row['scores'][key]}")

    if seen != len(db_cities(db)):
        rep.warn("figures",
                 f"CITIES array has {seen} cities, database has {len(db_cities(db))}")

    # CITY_ENRICHMENT modal prose. Lookup is [name_ST] || [name], so both key
    # formats are valid; the _ST form exists to disambiguate Wilmington NC/DE.
    enrich = js_object_slice(idx, "CITY_ENRICHMENT")
    keys = [(m.start(), m.group(1)) for m in re.finditer(r"\n\s*\"([^\"]+)\"\s*:\s*\{", enrich)]

    for pos, note in [(m.start(), m.group(1))
                      for m in re.finditer(r'D2: "((?:[^"\\]|\\.)*)"', enrich)]:
        owners = [k for p, k in keys if p < pos]
        if not owners:
            continue
        key = owners[-1]
        st = key.rsplit("_", 1)[1] if re.search(r"_[A-Z]{2}$", key) else None
        city = re.sub(r"_[A-Z]{2}$", "", key).strip()
        row = db_get(db, city, st)
        if not row:
            rep.warn("figures",
                     f"CITY_ENRICHMENT key {key!r}: no DB row, or the city name is "
                     f"ambiguous and the key lacks a state suffix")
            continue

        lo, hi = re.findall(r"\$[\d,]+", row["monthly"])
        for a, b in RANGE_RE.findall(note):
            if (a, b) != (lo, hi):
                rep.fail("figures",
                         f"CITY_ENRICHMENT {city}: modal monthly {a}–{b}, "
                         f"DB says {lo}–{hi}")

        if row["home"] is None:
            continue                     # malformed DB cell; check_db reports it
        ok = home_forms(row["home"])
        first = MONEY_RE.search(note)
        if first and first.group(0) not in ok:
            val = money_to_int(first.group(0))
            if val and abs(val - row["home"]) / row["home"] > HOME_TOLERANCE:
                rep.fail("figures",
                         f"CITY_ENRICHMENT {city}: modal home {first.group(0)}, "
                         f"DB says ${round(row['home'] / 1000)}K")


def check_tiers(rep, db, idx):
    """
    Budget-tier labels written into the modal prose ("Range 2") vs the DB's Budget
    Range. These drift whenever the tier boundaries move, and nothing else catches it.
    Twenty-three were stale on July 12, 2026, some by two full tiers.
    """
    enrich = js_object_slice(idx, "CITY_ENRICHMENT")
    keys = [(m.start(), m.group(1))
            for m in re.finditer(r'\n\s*"([^"]+)"\s*:\s*\{', enrich)]
    for m in re.finditer(r'D2: "((?:[^"\\]|\\.)*)"', enrich):
        owners = [k for p, k in keys if p < m.start()]
        if not owners:
            continue
        key = owners[-1]
        st = key.rsplit("_", 1)[1] if re.search(r"_[A-Z]{2}$", key) else None
        row = db_get(db, re.sub(r"_[A-Z]{2}$", "", key), st)
        if not row:
            continue
        for tier in re.findall(r"\bRange\s*([1-5])\b", m.group(1), re.I):
            if int(tier) != row["range"]:
                rep.fail("figures",
                         f"CITY_ENRICHMENT {key}: modal says Range {tier}, "
                         f"DB Budget Range is {row['range']}")


def check_routing(rep, db, idx, sitemap, local):
    """PUBLISHED_PROFILES <-> profile files <-> sitemap must agree, all directions."""
    m = re.search(r"PUBLISHED_PROFILES\s*=\s*\{(.*?)\n\s*\}", idx, re.S)
    if not m:
        rep.fail("routing", "could not locate PUBLISHED_PROFILES in index.html")
        return {}

    pub = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]", m.group(1)))
    slugs = {v.split("/")[1] for v in pub.values() if "/" in v}
    sm_slugs = set(re.findall(r"cities/([a-z0-9-]+)/", sitemap))

    for slug in sorted(slugs):
        if fetch(f"cities/{slug}/profile.html", local) is None:
            rep.fail("routing",
                     f"PUBLISHED_PROFILES points to cities/{slug}/profile.html, "
                     f"which does not exist")
        if slug not in sm_slugs:
            rep.fail("routing", f"cities/{slug}/ is live but missing from sitemap.xml")

    for slug in sorted(sm_slugs - slugs):
        rep.fail("routing",
                 f"sitemap lists cities/{slug}/ but it is not in PUBLISHED_PROFILES")

    for key in pub:
        if key not in db:
            rep.fail("routing", f"PUBLISHED_PROFILES key {key!r} has no DB row")

    return {v.split("/")[1]: tuple(k.rsplit("_", 1))
            for k, v in pub.items() if "/" in v}


def check_profiles(rep, db, slug_to_city, local):
    """Profile pages: monthly ranges and citywide home-value claims vs DB."""
    citywide = re.compile(
        r"(typical home value|median home is|home value is|citywide median|typical home of)",
        re.I)

    for slug, (city, state) in sorted(slug_to_city.items()):
        html = fetch(f"cities/{slug}/profile.html", local)
        if html is None:
            continue
        row = db_get(db, city, state)
        if not row:
            continue
        lo, hi = re.findall(r"\$[\d,]+", row["monthly"])
        flat = re.sub(r"\s+", " ", html)
        text = visible_text(html)

        for m in RANGE_RE.finditer(flat):
            a, b = m.group(1), m.group(2)
            if (a, b) == (lo, hi):
                continue
            ctx = re.sub(r"<[^>]*>", "", flat[max(0, m.start() - 90):m.end() + 20])
            if re.search(r"month|budget", ctx, re.I):
                rep.fail("profiles",
                         f"{city}: monthly {a}–{b}, DB says {lo}–{hi}  "
                         f"(...{ctx.strip()[-70:]})")

        if row["home"] is None:
            continue                     # malformed DB cell; check_db reports it
        ok = home_forms(row["home"])
        for m in citywide.finditer(text):
            seg = text[m.start():m.start() + 70]
            fig = MONEY_RE.search(seg)
            if not fig or fig.group(0) in ok:
                continue
            # A neighborhood range like "$475K–$650K" is legitimate; skip those.
            if re.search(r"\$[\d.]+[KM]?\s*[–—-]\s*\$", seg):
                continue
            val = money_to_int(fig.group(0))
            if val and abs(val - row["home"]) / row["home"] > HOME_TOLERANCE:
                rep.fail("profiles",
                         f"{city}: citywide home {fig.group(0)}, "
                         f"DB says ${round(row['home'] / 1000):,}K  "
                         f"(\"{seg.strip()[:60]}\")")


def check_cards(rep, db, idx, local):
    """Landing pages: stale coming-soon cards, and card figures vs DB."""
    m = re.search(r"PUBLISHED_PROFILES\s*=\s*\{(.*?)\n\s*\}", idx, re.S)
    pub = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]", m.group(1)))
    live = {tuple(k.rsplit("_", 1)) for k in pub}

    pages = [
        "best-places-to-retire-on-a-budget.html",
        "best-places-to-retire-in-florida.html",
        "best-places-to-retire-in-the-midwest.html",
        "best-places-to-retire-avoid-natural-disasters.html",
        "value-navigator.html", "active-frontier.html", "wellness-blueprint.html",
        "globetrotter-guide.html", "urban-walkabout.html",
        "top-cities-for-active-retirees.html", "top-cities-for-arts-lovers.html",
        "top-cities-for-foodies.html", "top-cities-for-healthcare.html",
        "top-cities-for-hikers.html", "top-cities-for-lgbtq-retirees.html",
        "top-cities-for-sports-fans.html",
    ]

    for page in pages:
        html = fetch(page, local)
        if html is None:
            rep.warn("cards", f"{page}: could not fetch")
            continue

        for block in re.split(r'(?=<(?:a|div) class="city-card)', html):
            nm = re.search(r'city-(?:name|featured-name)">([^<]+)', block)
            if not nm:
                continue
            city = nm.group(1).strip()
            st = re.search(r'state-code">([^<]+)', block)
            st = st.group(1).strip() if st else None

            head = block.split(">", 1)[0]
            if "coming-soon" in head and st and (city, st) in live:
                rep.fail("cards",
                         f'{page}: {city}, {st} shows "Coming soon" but its '
                         f"profile is live")

            row = db_get(db, city, st)
            if not row:
                continue
            lo, hi = re.findall(r"\$[\d,]+", row["monthly"])
            for a, b in RANGE_RE.findall(block):
                if (a, b) != (lo, hi):
                    rep.fail("cards",
                             f"{page}: {city} card monthly {a}–{b}, "
                             f"DB says {lo}–{hi}")


# Superlatives scoped to our own dataset are BANNED (policy adopted July 12, 2026).
# A claim like "the most affordable city we cover" is a claim about a private, moving
# object the reader cannot see. The moment a city is added to the database, every such
# claim silently becomes a potential lie, and nothing tells you. Fort Myers and
# Pensacola both got wrong exactly this way.
#
# Anchor claims to a NUMBER or a NAMED comparison, never to a rank:
#   BAD:  "the most affordable Gulf Coast entry we cover"
#   GOOD: "at $372K, well below Sarasota ($462K) and Naples ($585K)"
# Numbers stay true when the database grows. Ranks do not.
# A ranking word followed, IN THE SAME CLAUSE, by a scope pointing at our own dataset.
# Both halves are required and no sentence boundary may sit between them, or this fires
# on harmless things like "Top Cities for Healthcare" and "Community 9 of 10 in our
# database", which are not superlatives.
BANNED_SUPERLATIVE = re.compile(
    r"\b(most|least|cheapest|priciest|highest|lowest|largest|smallest|widest|"
    r"narrowest|strongest|weakest|worst|only)\b"
    r"(?!\s+(?:of the (?:metro|city|state)|of both))"     # "most of the metro" is not a claim
    r"[^.!?;<]{0,55}?"                                     # same clause only
    r"\b(in (?:the|our) database"
    r"|(?:that |cities )?we cover"
    r"|in our coverage"
    r"|we(?:'ve| have) published"
    r"|of any city we\b"
    r"|of any city (?:in|on) (?:the|our)\b"
    r"|on this site)\b", re.I)


def check_superlatives(rep, db, idx, slug_to_city, local):
    """
    Two things at once.

    FAIL: any superlative scoped to our own dataset. This is a policy violation, and
    unlike scope-correctness it is mechanically decidable, so it is a hard failure.

    WARN: database-wide affordability claims, printed next to the DB's real answer,
    for a human to judge. Also surfaces claims about the outside world ("largest art
    market in the country"), which no spreadsheet can settle.
    """
    rows = [r for r in db_cities(db) if r["home"] is not None]
    ranked = sorted(rows, key=lambda r: r["home"])
    cheapest, priciest = ranked[0], ranked[-1]

    by_monthly = sorted(
        rows, key=lambda r: money_to_int(re.findall(r"\$[\d,]+", r["monthly"])[0]))
    cheapest_m, priciest_m = by_monthly[0], by_monthly[-1]

    # A superlative only needs checking when it claims a SCOPE: the database, our
    # coverage, a region, a state. "Best value" as a neighborhood-card tag and
    # "most affordable tier" as a Range-1 label are not claims about anything.
    claim = re.compile(
        r"(most affordable|least affordable|cheapest|most expensive|lowest[- ]cost"
        r"|least expensive|best value|widest|largest|highest)"
        r"(?! tier)"
        r"[^.<\"]{0,80}?"
        r"(in the database|we cover|in our coverage|of any|of all|anywhere|"
        r"in the (?:US|country|nation|Southeast|Midwest|Northeast|South|West)|"
        r"in Florida|in Texas|in the state)"
        r"[^.<\"]{0,30}", re.I)

    pages = {"index.html": idx}
    for slug in slug_to_city:
        html = fetch(f"cities/{slug}/profile.html", local)
        if html:
            pages[f"cities/{slug}/profile.html"] = html

    # The CITY_ENRICHMENT strings live inside <script>, so visible_text() strips them.
    # They render into the quiz results modal, which a reader absolutely does see. On
    # July 12, 2026 this blind spot was hiding 27 banned superlatives, four of them
    # flatly false ("Naples: most expensive city in the database" — Naples is $585K,
    # Carmel is $2.28M). Scan the data strings as their own surface.
    enrich = js_object_slice(idx, "CITY_ENRICHMENT")
    for m in BANNED_SUPERLATIVE.finditer(enrich):
        rep.fail("superlatives",
                 f'index.html CITY_ENRICHMENT: "{m.group(0).strip()}" — superlative '
                 f"scoped to our own dataset, and it renders in the quiz modal.")

    # --- FAIL: dataset-scoped superlatives (policy) ---
    banned = {}
    for page, html in pages.items():
        for m in BANNED_SUPERLATIVE.finditer(visible_text(html)):
            phrase = re.sub(r"\s+", " ", m.group(0)).strip()
            banned.setdefault((page, phrase), 0)
            banned[(page, phrase)] += 1

    for (page, phrase), n in sorted(banned.items()):
        times = f" (x{n})" if n > 1 else ""
        rep.fail("superlatives",
                 f'{page}: "{phrase}"{times} — superlative scoped to our own '
                 f"dataset. Anchor to a figure or a named city instead.")

    # --- WARN: everything else sweeping, for human eyes ---
    hits = {}
    for page, html in pages.items():
        for m in claim.finditer(visible_text(html)):
            txt = re.sub(r"\s+", " ", m.group(0)).strip()
            hits.setdefault((page, txt), 0)
            hits[(page, txt)] += 1

    for (page, txt), n in sorted(hits.items()):
        times = f" (x{n})" if n > 1 else ""
        rep.warn("superlatives", f"{page}: \"{txt}\"{times}")

    rep.warn("superlatives",
             f"DB truth: cheapest home = {cheapest['city']}, {cheapest['state']} "
             f"(${cheapest['home']:,}); priciest = {priciest['city']}, "
             f"{priciest['state']} (${priciest['home']:,})")
    rep.warn("superlatives",
             f"DB truth: lowest monthly = {cheapest_m['city']}, {cheapest_m['state']} "
             f"({cheapest_m['monthly']}); highest = {priciest_m['city']}, "
             f"{priciest_m['state']} ({priciest_m['monthly']})")
    rep.warn("superlatives",
             "Every line above is a claim about the whole database. Confirm each "
             "against the two DB truth lines, or scope it explicitly.")


def check_emdash(rep, idx, sitemap, slug_to_city, local):
    """Em-dash policy: profiles and comparison pages. Guides are grandfathered."""
    targets = [f"cities/{s}/profile.html" for s in slug_to_city]
    targets += re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", sitemap)
    if GUIDES_TOO:
        targets += ["value-navigator.html", "active-frontier.html",
                    "wellness-blueprint.html", "globetrotter-guide.html",
                    "urban-walkabout.html"]

    for page in sorted(set(targets)):
        html = fetch(page, local)
        if html is None:
            continue
        n = visible_text(html).count("\u2014")
        if n:
            rep.fail("emdash", f"{page}: {n} em-dash(es) in rendered text")


def check_affiliate(rep, slug_to_city, local):
    """
    Affiliate codes, read from the profiles themselves.

    The profiles ARE the record. There is no spreadsheet, deliberately: a separate
    list of codes is a stale copy of data that lives in the HTML, and a half-current
    reference is worse than none, because eventually someone trusts it.

    A duplicated code is the dangerous failure. It does not error and it does not look
    broken. It just quietly sends a Savannah reader to Charleston's hotel page. Nobody
    catches that by eye.
    """
    LINK = re.compile(
        r"https?://(?:www\.)?(expedia|hotels|vrbo)\.com/affiliate/([A-Za-z0-9]+)", re.I)
    BRANDS = {"expedia", "vrbo"}

    seen = {}          # (brand, code) -> slug
    for slug in sorted(slug_to_city):
        html = fetch(f"cities/{slug}/profile.html", local)
        if html is None:
            continue
        found = {}
        for brand, code in LINK.findall(html):
            brand = brand.lower()
            found.setdefault(brand, set()).add(code)
            owner = seen.get((brand, code))
            if owner and owner != slug:
                rep.fail("affiliate",
                         f"{slug}: {brand} code {code} is ALSO used by {owner}. "
                         f"A duplicated code sends readers to the wrong city and "
                         f"fails silently.")
            seen.setdefault((brand, code), slug)

        for brand in sorted(BRANDS - set(found)):
            rep.fail("affiliate", f"{slug}: no {brand} affiliate link on the profile")
        for brand, cs in sorted(found.items()):
            if len(cs) > 1:
                rep.fail("affiliate",
                         f"{slug}: {len(cs)} different {brand} codes on one profile "
                         f"({', '.join(sorted(cs))}). Only one is being credited.")


def check_db(rep, db_path):
    """Database hygiene."""
    import pandas as pd
    if db_path.endswith(".xlsx"):
        df = pd.read_excel(db_path, sheet_name="City Database", header=1)
    else:
        df = pd.read_csv(db_path)
    df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]

    for _, r in df.iterrows():
        raw = str(r["Median Home"]).strip()
        figs = re.findall(r"\$[\d,]+", raw)
        if len(figs) > 1 or re.search(r"[–—]", raw):
            rep.fail("db",
                     f"{r['City']}, {r['ST']}: Median Home is {raw!r}, a RANGE. "
                     f"MEDIAN-HOME-METHODOLOGY.md v1.2 requires a single citywide "
                     f"ZHVI figure for all 99 cities. Replace with one number and "
                     f"move the spread into a Neighborhood Reality Check note.")
        elif not raw.startswith("$"):
            rep.fail("db",
                     f"{r['City']}, {r['ST']}: Median Home is {raw!r}, not a "
                     f"'$N,NNN' string like the other rows. Scripts that string-match "
                     f"this column will silently skip or mis-parse it.")

    dupes = df[df.duplicated(subset=["City", "ST"], keep=False)]
    for _, r in dupes.iterrows():
        rep.fail("db", f"duplicate DB row: {r['City']}, {r['ST']}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Validate RetireMeHere against the City Database.")
    ap.add_argument("--db", default=DEFAULT_DB, help=f"database path (default: {DEFAULT_DB})")
    ap.add_argument("--local", help="validate a local checkout instead of live GitHub")
    ap.add_argument("--only", action="append",
                    choices=["figures", "profiles", "routing", "cards",
                             "superlatives", "emdash", "affiliate", "db"],
                    help="run only these check groups (repeatable)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        print(f"Database not found at {args.db}.", file=sys.stderr)
        print("The validator reads the xlsx in docs/. If you have bumped the "
              "database version, update DEFAULT_DB at the top of this file, "
              "or pass --db.", file=sys.stderr)
        return 2

    groups = set(args.only) if args.only else {
        "figures", "profiles", "routing", "cards", "superlatives", "emdash",
        "affiliate", "db"}

    source = args.local or "live GitHub"
    print(f"RetireMeHere validator")
    print(f"  source:   {source}")
    print(f"  database: {args.db}")

    db = load_db(args.db)
    print(f"  cities:   {len(db_cities(db))}")

    idx = fetch("index.html", args.local)
    sitemap = fetch("sitemap.xml", args.local)
    if idx is None or sitemap is None:
        print("Could not read index.html or sitemap.xml.", file=sys.stderr)
        return 2

    rep = Report(quiet=args.quiet)

    slug_to_city = check_routing(rep, db, idx, sitemap, args.local) \
        if "routing" in groups else {}
    if not slug_to_city:
        # other checks still need the slug map
        m = re.search(r"PUBLISHED_PROFILES\s*=\s*\{(.*?)\n\s*\}", idx, re.S)
        pub = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]",
                              m.group(1))) if m else {}
        slug_to_city = {v.split("/")[1]: k.rsplit("_", 1)[0].strip()
                        for k, v in pub.items() if "/" in v}

    if "figures" in groups:
        check_figures(rep, db, idx)
        check_tiers(rep, db, idx)
    if "profiles" in groups:
        check_profiles(rep, db, slug_to_city, args.local)
    if "cards" in groups:
        check_cards(rep, db, idx, args.local)
    if "superlatives" in groups:
        check_superlatives(rep, db, idx, slug_to_city, args.local)
    if "emdash" in groups:
        check_emdash(rep, idx, sitemap, slug_to_city, args.local)
    if "affiliate" in groups:
        check_affiliate(rep, slug_to_city, args.local)
    if "db" in groups:
        check_db(rep, args.db)

    return rep.render()


if __name__ == "__main__":
    sys.exit(main())
