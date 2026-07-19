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
import pathlib
import re
import sys
import urllib.request

RAW = "https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main"
# The database already lives in the repo, in docs/. That is the canonical copy the
# validator reads. Update this constant when you bump the version, in the same commit
# that adds the new xlsx.
DEFAULT_DB = "docs/CityDatabase_Jul_13_v16_4_climate.xlsx"

# Tolerated deviation on home-value prose before we call it stale.
HOME_TOLERANCE = 0.03

# Tolerated within-state spread on D5 Tax. D5 is a state-level score (see
# docs/D5-TAX-METHODOLOGY.md); 1 point of slack covers real local sales-tax and
# millage differences the database does not yet record. 2+ is always an error.
D5_MAX_SPREAD = 1

# The em-dash rule applies to the five guide pages too, as of the July 14 2026 sweep.
#
# This flag used to be False, with a comment saying guides were "grandfathered; see
# PROFILE-FORMATTING.md". That document grandfathers nothing. Its scope is profiles, and
# its sweep status covers "all 38 published profiles" -- it never spoke to the guides
# either way. So the flag was not recording a decision. It was recording an unfinished
# job, in the grammar of a decision, and it hid 231 rendered em-dashes across the five
# guides for as long as it stayed False.
GUIDES_TOO = True

DIMS = [
    ("D1", "D1 Airport"), ("D2", "D2 Budget"), ("D3", "D3 Health"),
    ("D4", "D4 Resil."), ("D5", "D5 Tax"), ("D6", "D6 Walk"),
    ("D7", "D7 Outdoor"), ("D8", "D8 Wellness"), ("D9", "D9 Safety"),
    ("D10", "D10 Comm."),
]

RANGE_RE = re.compile(r"(\$\d{1,2},\d{3})\s*(?:–|—|to|-)\s*(\$\d{1,2},\d{3})")
MONEY_RE = re.compile(r"\$\d{3}K|\$\d{3},\d{3}|\$\d(?:\.\d{1,2})?M")

# The citywide home figure is stated in exactly one place on a profile: the stat card.
# <div class="stat-label">Typical Home Value</div><div class="stat-value">$726<span…>K…
STAT_HOME = re.compile(
    r'<div class="stat-label">\s*(?:Typical Home Value|Median Home[^<]*)\s*</div>\s*'
    r'<div class="stat-value">(.*?)</div>', re.S | re.I)

# "under $400K", "below $1M" — a bound, not a figure. Must sit in the same clause as
# a home word, or it would swallow monthly-budget claims.
HOME_BOUND = re.compile(
    r"(?:home|house|housing|median)[^.!?;]{0,60}?"
    r"\b(?:under|below|less than)\s+(\$[\d.,]+[KM]?)", re.I)


# A home-value figure stated inside a pros/cons bullet, tied to the DB Median Home.
# Two shapes: word-then-figure ("typical home value $585,000", "median home $465K")
# and figure-then-word ("$465K median", "$530K typical home value").
#
# The noun is restricted to home value / median home, NEVER a bare "median": the
# pros/cons carry "median bill $5,026" (property-tax bill) and "monthly costs $10K+",
# which are not home values and must not match. The token is range-aware so a range
# self-rejects through money_to_int (returns None) instead of the regex grabbing only
# the low end. And it is anchored tight so it cannot cross a comma into the next
# clause: the Frisco con "home value $663K, above Georgetown at $457K" yields $663K
# only, never the comparison city's figure.
_FIG = r"~?(\$[\d.,]+[KM]?(?:\s*[\u2013\u2014-]\s*\$?[\d.,]+[KM]?)?)"
PROSCONS_HOME = re.compile(
    r"(?:typical\s+)?home\s+value\s*" + _FIG +
    r"|median\s+home(?:\s+(?:value|price|sale))?\s*" + _FIG +
    r"|" + _FIG + r"\s+(?:median|typical\s+home\s+value)\b", re.I)


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


def _read_xlsx(path, sheet_name):
    """
    Read one sheet of an .xlsx with the standard library only.

    An .xlsx is a zip of XML. Reading it needs no pandas and no openpyxl, and that
    matters: Codespaces rebuilds periodically and pip-installed packages vanish with
    it. A validator that cannot run is a validator that is not run. Zero dependencies
    means this works on any machine with Python, forever, with no setup step.
    """
    import zipfile
    import xml.etree.ElementTree as ET

    NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}

        sheet_path = None
        for sh in wb.iter(NS + "sheet"):
            if sh.get("name") == sheet_name:
                # Excel writes the rel target as "worksheets/sheet1.xml"; openpyxl and
                # pandas write "/xl/worksheets/sheet1.xml". The old code checked for the
                # "xl/" prefix BEFORE stripping the leading slash, so the openpyxl form
                # became "xl/xl/worksheets/sheet1.xml" and the validator died the first
                # time the database was saved from Python. Strip, then prefix.
                t = target[sh.get(REL + "id")].lstrip("/")
                sheet_path = t if t.startswith("xl/") else "xl/" + t
                break
        if sheet_path is None:
            names = [sh.get("name") for sh in wb.iter(NS + "sheet")]
            raise KeyError(f"sheet {sheet_name!r} not found; sheets are {names}")

        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sst.iter(NS + "si"):
                shared.append("".join(t.text or "" for t in si.iter(NS + "t")))

        sheet = ET.fromstring(z.read(sheet_path))

    def col_index(ref):
        letters = "".join(ch for ch in ref if ch.isalpha())
        n = 0
        for ch in letters:
            n = n * 26 + (ord(ch.upper()) - 64)
        return n - 1

    rows = []
    for row in sheet.iter(NS + "row"):
        cells = {}
        for c in row.iter(NS + "c"):
            # inlineStr cells carry <is><t>, NOT <v>. This check must come FIRST:
            # the <v> lookup below returns None for them, and an early `continue`
            # would skip every inline string in the file. Excel writes sharedStrings
            # so this never bit us; openpyxl writes inlineStr, which blanks the sheet.
            if c.get("t") == "inlineStr":
                cells[col_index(c.get("r"))] = "".join(
                    t.text or "" for t in c.iter(NS + "t"))
                continue
            v = c.find(NS + "v")
            if v is None or v.text is None:
                continue
            if c.get("t") == "s":
                val = shared[int(v.text)]
            else:
                txt = v.text
                try:
                    f = float(txt)
                    val = int(f) if f == int(f) else f
                except ValueError:
                    val = txt
            cells[col_index(c.get("r"))] = val
        rows.append(cells)
    return rows


def load_db(path):
    """Load the City Database. Header is on row 2; data starts on row 3."""
    rows = _read_xlsx(path, "City Database")
    if len(rows) < 3:
        raise ValueError(f"{path}: expected a header on row 2 and data below it")

    header = {i: str(v).replace("\n", " ").strip()
              for i, v in rows[1].items() if str(v).strip()}
    col = {name: i for i, name in header.items()}

    required = ["City", "ST", "Monthly Est", "Median Home", "Budget Range"] + \
               [c for _, c in DIMS]
    missing = [c for c in required if c not in col]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")

    # Keyed by BOTH "City" and "City_ST". Wilmington NC and Wilmington DE are both in
    # the database, so a city-name-only key silently drops one of them.
    db = {}
    names = {}
    for r in rows[2:]:
        city = str(r.get(col["City"], "")).strip()
        if not city:
            continue
        state = str(r.get(col["ST"], "")).strip()
        raw_home = str(r.get(col["Median Home"], "")).strip()
        row = {
            "city": city,
            "state": state,
            "monthly": str(r.get(col["Monthly Est"], "")).strip(),
            "home": money_to_int(raw_home if raw_home.startswith("$") else f"${raw_home}"),
            "home_raw": raw_home,
            "range": int(r[col["Budget Range"]]),
            "scores": {k: int(r[col[c]]) for k, c in DIMS},
        }
        db[f"{city}_{state}"] = row
        names.setdefault(city, []).append(row)

    for city, rs in names.items():
        db[city] = rs[0] if len(rs) == 1 else None
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


BLOCK_TAGS = ("div|p|h[1-6]|li|ul|ol|table|thead|tbody|tr|td|th|section|article|"
              "header|footer|nav|aside|main|blockquote|figure|figcaption|br|hr|form|label")


def visible_text(html):
    """
    Rendered text, with BLOCK boundaries preserved.

    Every tag used to become a single space, which quietly fused text from separate
    block elements into one running clause. That manufactured phrases that appear
    nowhere on the page. Real example, from cities/prescott/profile.html:

        <div class="eyebrow">Prescott also appears on</div>
        <h2 class="section-title">The list where Prescott earns its place.</h2>

    collapsed to "...appears on The list where..." and tripped the superlative ban on
    "on ... list" -- a phrase no reader ever sees. The same seam can hide a real
    violation just as easily as invent a fake one.

    So: block-level tags become a hard boundary, inline tags (span, strong, a, em ...)
    stay a space, because a banned phrase legitimately runs through <strong> mid-clause.
    """
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    # block boundaries first: a period stops a clause dead
    html = re.sub(r"</?(?:%s)\b[^>]*>" % BLOCK_TAGS, " . ", html, flags=re.I)
    # everything else (inline) is just a space
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

        # pros/cons bullets hard-code home figures that nothing checked against the
        # DB. That is how a stale "$327K" survived a Knoxville refresh while the
        # medianHome field four lines up was already correct. Read every home-value
        # figure in the pros/cons prose and hold it to the same DB Median Home.
        if row["home"] is not None:
            prose = " ".join(re.findall(r'(?:pros|cons):\s*\[([^\]]*)\]', obj))
            for m in PROSCONS_HOME.finditer(prose):
                tok = next(g for g in m.groups() if g)
                # "$250K citywide but retirees target ..." — an explicitly citywide
                # figure is a deliberate second number for a high-variance city, whose
                # DB Median Home carries the retiree-target figure by design. Skip it.
                if re.match(r"\s*citywide", prose[m.end():m.end() + 12], re.I):
                    continue
                val = money_to_int(tok)
                if val is None:                     # a range or unparseable: skip
                    continue
                if abs(val - row["home"]) / row["home"] > HOME_TOLERANCE:
                    # PROMOTED WARN -> FAIL, Jul 18 2026. It shipped WARN on Jul 15
                    # only because the first run surfaced 34 stranded figures from the
                    # Jul-13 DB refresh and they had to be reconciled without
                    # red-lighting the gate. That reconciliation is done and both
                    # `--local .` and the live bare run read 0 pros/cons warnings, so
                    # the check now gates a deploy like every other figures check.
                    rep.fail("figures",
                             f"CITIES {city}, {state}: pros/cons state a home value "
                             f"{tok}, DB Median Home is ${round(row['home'] / 1000)}K")

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


def published_profiles(idx):
    """The single parse of PUBLISHED_PROFILES. Returns {slug: (City, ST)}."""
    m = re.search(r"PUBLISHED_PROFILES\s*=\s*\{(.*?)\n\s*\}", idx, re.S)
    if not m:
        return {}
    pub = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]", m.group(1)))
    out = {}
    for key, path in pub.items():
        if "/" not in path:
            continue
        city, _, state = key.rpartition("_")
        out[path.split("/")[1]] = (city.strip(), state.strip())
    return out


def check_routing(rep, db, idx, sitemap, local, slug_to_city):
    """PUBLISHED_PROFILES <-> profile files <-> sitemap must agree, all directions."""
    m = re.search(r"PUBLISHED_PROFILES\s*=\s*\{(.*?)\n\s*\}", idx, re.S)
    pub = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]", m.group(1)))
    slugs = set(slug_to_city)
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


def check_profiles(rep, db, slug_to_city, local):
    """Profile pages: monthly ranges and the citywide home stat card vs DB."""
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

        # The stat card is the ONLY place a profile states the citywide figure.
        # The old check scanned the whole page for phrases like "median home is",
        # which swept up things that are supposed to differ from the citywide number:
        # neighborhood medians, "condos from ~$X", and deliberate historical
        # comparisons. Those are not drift. Read the stat card and nothing else.
        sm = STAT_HOME.search(html)
        if not sm:
            rep.warn("profiles", f"{city}: no 'Typical Home Value' stat card found")
        else:
            shown = re.sub(r"\s+", "", re.sub(r"<[^>]*>", "", sm.group(1)))
            if shown not in ok:
                val = money_to_int(shown)
                if val is None:
                    rep.fail("profiles",
                             f"{city}: stat card home {shown!r} is unparseable")
                elif abs(val - row["home"]) / row["home"] > HOME_TOLERANCE:
                    rep.fail("profiles",
                             f"{city}: stat card home {shown}, "
                             f"DB says ${round(row['home'] / 1000):,}K")

        # "under $400K" is a claim about a BOUND, not a figure, so it is satisfied by
        # any DB value below the bound. Only fails when the DB actually exceeds it.
        for m in HOME_BOUND.finditer(text):
            bound = money_to_int(m.group(1))
            if bound and row["home"] >= bound:
                rep.fail("profiles",
                         f"{city}: claims a home value {m.group(0).strip()!r}, but "
                         f"DB says ${round(row['home'] / 1000):,}K, which is not below it")


def card_blocks(html):
    """
    Yield each city card bounded at its OWN closing tag.

    The old version did re.split(lookahead for the next card-open), so a block ran
    from one card to the start of the next, and the LAST card in a section swallowed
    every paragraph after it. On value-navigator that trailing prose contained nine
    money ranges, all of which were then attributed to Chattanooga and reported as
    card drift. Nine failures, zero bugs. Walk the tag depth and stop at the real end.
    """
    for m in re.finditer(r'<(a|div) class="city-(?:card|featured)', html):
        tag = m.group(1)
        depth, i = 0, m.start()
        step = re.compile(rf"</?{tag}\b", re.I)
        while True:
            t = step.search(html, i)
            if not t:
                yield html[m.start():]           # unbalanced; caller still sees it
                break
            depth += -1 if t.group(0).startswith("</") else 1
            i = t.end()
            if depth == 0:
                yield html[m.start():i + len(tag) + 1]
                break


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

        for block in card_blocks(html):
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
# PHRASE BAN (adopted July 12, 2026, replacing the two-half semantic check).
#
# The old check required BOTH a ranking word AND a scope phrase in the same clause.
# The scope half was airtight. The ranking half was a closed list of seventeen words,
# and English is not a closed list. Everything that leaked, leaked through the ranking
# half, never the scope half:
#
#   "one of the LOWER safety scores in our coverage"        (comparative, not "lowest")
#   "the GENTLEST hurricane ledger of any Florida city we cover"   (not in the list)
#   "NO OTHER Florida city in our coverage matches"         (not in the list)
#
# All three are dataset-scoped claims. All three rot the day city 100 lands. All three
# passed clean. Extending the word list only moves the leak; the next escape is
# "second to none in our coverage".
#
# So: drop the ranking half entirely and ban the SCOPE PHRASE on its own. A claim rots
# if and only if it points at the moving dataset, which makes the scope phrase both
# necessary and sufficient for the failure mode. The ranking word was only ever a proxy
# for "is this a claim?", and the proxy is what failed.
#
# This does fire on non-claims ("the 99 cities we cover"). That is accepted, not
# tolerated: "we cover" is insider voice. The reader does not know what we cover and has
# no reason to care. Reword to "the 99 cities on RetireMeHere" and the sentence improves.
#
# Anchor real claims to a NUMBER or a NAMED city, never to a rank:
#   BAD:  "the most affordable Gulf Coast entry we cover"
#   GOOD: "at $372K, well below Sarasota ($462K) and Naples ($585K)"
# Numbers stay true when the database grows. Ranks do not.
#
# Deliberately NOT banned: "of any city in the state", "in the country", "in Florida".
# Those scope to the outside world, not to us. They cannot rot when we add a city; they
# are handled by the WARN tier below, which asks a human to check them for truth.
BANNED_SUPERLATIVE = re.compile(
    # (a) a preposition pointing at our own corpus. The modifier slot is now a
    #     REPEATING group plus one free adjective, because the fixed (the|our|this)
    #     was itself a closed list and two things walked straight through it:
    #       "among most affordable in ENTIRE database"      (index.html, live)
    #       "perfect 10s in our MIDWEST coverage"           (midwest page, live)
    #     The nouns stay narrow on purpose. "scorecard" and "board" are NOT here:
    #     "the widest gap on the scorecard" points at the two-city table the reader
    #     is looking at. It is bounded, visible, and static. It cannot rot when city
    #     100 lands, so it is not this policy's business, and banning it would have
    #     condemned ~30 clean sentences plus every "similar scores across the board".
    r"\b(?:in|on|of|across|from|among|throughout|against|within)\s+"
    # The free word is only allowed AFTER a real determiner. "in our FLORIDA coverage"
    # and "in ENTIRE database" match; "high on YOUR list" and "in result list" do not,
    # because "your"/"result" are not determiners and the noun must then follow directly.
    # Bare "in database" still matches, as before.
    r"(?:(?:the|our|this|these|entire|whole|full|all)\s+(?:\w+\s+)?)?"
    r"(?:database|dataset|coverage|site|list)\b"
    # (b) first-person verbs of curation. "compare" and "profile" were missing:
    #       "the highest of any pairing WE HAVE COMPARED"   (madison-vs-ann-arbor)
    #       "more than almost any city WE PROFILE"          (new-orleans)
    r"|\bwe(?:'ve| have)?\s+(?:cover|covered|score|scored|rank|ranked|track|tracked|"
    r"publish|published|list|listed|include|included|compare|compared|feature|featured|"
    r"profile|profiled|review|reviewed|select|selected|analyze|analyzed)\b"
    # (c) "of any city we ...", and the generalised noun: "of any PAIRING here",
    #     "of any ARIZONA CITY here", "of any FLORIDA CITY here" all leaked past a
    #     hardcoded "city".
    r"|\bof any \w+(?:\s+\w+)?\s+(?:we|here)\b"
    # (d) A VERB pointing at the corpus, with no preposition in front to catch it in (a):
    #       "Three cities TOP the database"
    #       "One of the safer additions TO the database"
    #       "our database NOTES NCH as the #1-rated hospital in Florida"
    #     The last shape is the worst of the three. It launders an OUTSIDE fact through our
    #     own spreadsheet: US News rates NCH, not us. It tells the reader to trust a document
    #     they cannot open, and it rots if the score ever moves. State the fact, drop the
    #     attribution. 46 of these were live on July 14 2026.
    r"|\b(?:our|the)\s+(?:city\s+)?(?:database|dataset)\b"
    # (e) the same rot wearing a noun the list did not have: "the gentlest in our FLORIDA SET".
    r"|\bour\s+\w+\s+set\b",
    re.I)
# WHY THIS SHAPE, AND WHY IT GOT WIDER (2026-07-13, second pass)
#
# The first phrase ban replaced a closed list of RANKING words with what I called an
# airtight scope check. It was not airtight. It was a closed list of SCOPE strings --
# the same mistake, moved one clause to the right. It matched "in the database" and
# "in our database" but not bare "in database", and not "we score" / "we rank" /
# "we track". Twenty-one bare "in database" and fifteen "we score" were live and
# invisible, and inside them sat three separate cities each claiming to be the "Most
# expensive city in database" (Naples $549K, Carlsbad $1.36M, Jackson Hole $1.93M).
# None of them is. Carmel-by-the-Sea is, at $2,281,000. All three figures were stale too.
#
# So this version bans the STRUCTURE, not the strings: a preposition aimed at our corpus,
# or a first-person verb of curation. Those are the only two ways to point a claim at
# our own moving dataset, and both are now closed.
#
# Anchor real claims to a NUMBER or a NAMED city, never to a rank:
#   BAD:  "the most expensive city in database"
#   GOOD: "at $585,000, well below Carmel-by-the-Sea's $2.28M"
# Numbers stay true when the database grows. Ranks do not.
#
# Deliberately NOT banned: "in the country", "in Florida", "of any city in the state".
# Those scope to the outside world and cannot rot when we add a city; the WARN tier
# below asks a human to check them for truth.


def script_strings(html):
    """
    Prose that lives inside <script> as data, then renders to the reader through JS.

    visible_text() strips <script> wholesale, so every such string is invisible to a
    text scan. That blind spot hid 27 banned superlatives in index.html's
    CITY_ENRICHMENT (four flatly false) and 13 more in pick-and-compare.html. Special-
    casing one constant at a time loses; scan every string literal in every script and
    the whole class is closed.

    Only literals long enough to be prose. Short ones are selectors, keys, and classes.
    """
    out = []
    for block in re.findall(r"<script[^>]*>(.*?)</script>", html, re.S):
        for q in re.findall(r"'((?:[^'\\]|\\.){25,})'"
                            r'|"((?:[^"\\]|\\.){25,})"'
                            r"|`((?:[^`\\]|\\.){25,})`", block):
            out.append(next(s for s in q if s))
    return " ... ".join(out)



def check_hardcoded_counts(rep, db, idx, slug_to_city, local):
    """
    A hardcoded city count is a claim that rots. Same disease as a self-scoped
    superlative, different symptom.

    On July 13 2026 the site was simultaneously telling readers "100 cities" (37x),
    "100+ cities" (17x), "100 US cities" (5x), "99 cities" (4x) and "92 cities" (1x).
    The database had 99. The most common claim was wrong; "100+" was flatly false;
    and the "92" was a fossil from whenever that was briefly true.

    Policy: no number. "every city on RetireMeHere". Nothing to drift, nothing to
    maintain, correct forever.
    """
    pat = re.compile(r"\b(?:9[0-9]|1[0-9]{2})\+? (?:scored |ranked |US |U\.S\. )?cities\b", re.I)
    pages = {"index.html": idx}
    for slug in slug_to_city:
        h = fetch(f"cities/{slug}/profile.html", local)
        if h:
            pages[f"cities/{slug}/profile.html"] = h
    hub = fetch("compare-retirement-cities.html", local) or ""
    for page in sorted(set(re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub))):
        h = fetch(page, local)
        if h:
            pages[page] = h
    for page, html in pages.items():
        for surface in (visible_text(html), script_strings(html)):
            for m in pat.finditer(re.sub(r"\s+", " ", surface)):
                rep.fail("counts",
                         f'{page}: "{m.group(0)}" — hardcoded city count. It drifts every '
                         f'time the database grows. Use count-free language.')


def check_numeric_cells(rep, db, idx, slug_to_city, local):
    """
    A range is not a number.

    Wilmington DE carried "$430,000-$960,000" in Median Home. Nothing errored. Every
    consumer just silently picked a different point on it: the June budget audit read
    the low end, a later edit recomputed Monthly Est off the midpoint, validate.py's
    parser read the low end, and the actual citywide ZHVI ($321,158) sat below all
    three. Four numbers, four systems, zero complaints.

    St. Paul carried a bare int (297000, no dollar sign) and the parser returned None,
    so it was silently dropped from every home-value check instead.

    Both failure modes are silent by construction. Fail loudly on either.
    """
    for key, row in db.items():
        if row is None or "_" not in key:
            continue
        raw = str(row.get("home_raw", "")).strip()
        if not raw or raw.lower() == "nan":
            continue
        if re.search(r"[-\u2013\u2014]", raw[1:]):
            rep.fail("db", f'{key}: Median Home is a RANGE ("{raw}"). A range is not a '
                           f'number; every consumer picks a different point on it.')
        elif not raw.startswith("$"):
            rep.fail("db", f'{key}: Median Home ("{raw}") has no $ and will not parse. '
                           f'It is silently dropped from every price check.')


def check_comparison_scores(rep, db, idx, slug_to_city, local):
    """
    Comparison pages hardcode every D1-D10 score in a table. Nothing checked them.

    On 2026-07-13 the D2 column was rebuilt in the database and propagated into
    index.html. The validator went green. Sixteen of nineteen comparison pages were
    still showing the OLD D2, live, because no check ever read them. The tool said the
    site was consistent while a third of the score tables on it were wrong.

    A hardcoded score in prose or a table is a copy of the truth, and every copy drifts.
    Check them all, on every dimension, not just the one that happened to change.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pages = sorted(set(re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)))

    by_slug = {}
    for key, row in db.items():
        if row is None or "_" not in key:
            continue
        name = str(row.get("city", ""))
        by_slug[name.lower().replace(" ", "-").replace(".", "")] = row

    for a_slug, b_slug in pages:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        html = fetch(page, local)
        if not html:
            continue
        a, b = by_slug.get(a_slug), by_slug.get(b_slug)
        if not a or not b:
            continue
        for dim_key, dim_label in DIMS:
            m = re.search(
                rf'<td class="metric">{re.escape(dim_label)}[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>',
                html, re.S)
            if not m:
                continue
            shown_a, shown_b = int(m.group(1)), int(m.group(2))
            for who, shown, row in ((a_slug, shown_a, a), (b_slug, shown_b, b)):
                # Scores are NESTED under row["scores"], not on the row. The first cut
                # of this check used row.get(dim_key), which returned None for every
                # city, and the `is not None` guard below then skipped all of them --
                # so it reported zero failures on a site with sixteen broken pages.
                # A check that cannot fail is worse than no check. If a score is
                # missing, say so; never skip quietly.
                truth = row.get("scores", {}).get(dim_key)
                if truth is None:
                    rep.fail("comparison",
                             f"{page}: {who} has no {dim_key} in the DB.")
                elif shown != truth:
                    rep.fail("comparison",
                             f"{page}: {who} {dim_label} shows {shown}/10, "
                             f"DB says {truth}/10.")


def check_dead_dimension_guards(rep, db, idx, slug_to_city, local):
    """
    A guard on a dimension key that is not in DIMENSIONS can never fire.

    index.html carried `if (dim.key === 'D2' ...)` inside a `DIMENSIONS.forEach(dim =>`
    loop from the site's very first commit (2026-03-29). D2 has never been in
    DIMENSIONS, in any of 926 commits. The guard never executed once. It was written
    for a design where affordability was a weighted dimension; that design was dropped,
    the code was not. BUDGET-METHODOLOGY then documented the bonus as live, because
    someone read the line and reasonably assumed it ran.

    Dead code that looks alive is worse than no code: it teaches the next reader
    something false about how the product works.
    """
    m = re.search(r"const DIMENSIONS = \[(.*?)\];", idx, re.S)
    if not m:
        rep.fail("engine", "index.html: DIMENSIONS array not found.")
        return
    keys = set(re.findall(r"key:\s*'([^']+)'", m.group(1)))
    for guard in set(re.findall(r"dim\.key === '([^']+)'", idx)):
        if guard not in keys:
            rep.fail("engine",
                     f"index.html: guard `dim.key === '{guard}'` is unreachable. "
                     f"'{guard}' is not in DIMENSIONS ({', '.join(sorted(keys))}). "
                     f"Delete it or add the dimension.")

def check_tag_balance(rep, db, idx, sitemap, slug_to_city, local):
    """
    Unclosed / orphaned inline tags.

    Added 2026-07-13 after finding a stray </strong> live in value-navigator.html:

        Typical home value <strong>$185K</strong> , under Tulsa at $194K
        and Memphis at $195K</strong> · UNESCO Creative City

    An earlier edit deleted the opening tag and left the closer behind. Browsers
    swallow it silently, so it rendered "fine" and nothing caught it. Cheap to check,
    so check it.

    Only inline tags with mandatory closers. <p> and <li> are legally left open in
    HTML, and <br>/<img> are void, so they are not counted.
    """
    TAGS = ("strong", "em", "b", "i", "span", "a")

    targets = ["index.html", "pick-and-compare.html", "compare-retirement-cities.html",
               "visit-before-you-decide.html"]
    targets += [f"cities/{s}/profile.html" for s in slug_to_city]
    targets += re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", sitemap)
    targets += ["value-navigator.html", "active-frontier.html", "wellness-blueprint.html",
                "globetrotter-guide.html", "urban-walkabout.html"]

    for page in sorted(set(targets)):
        html = idx if page == "index.html" else fetch(page, local)
        if html is None:
            continue
        body = re.sub(r"<(script|style)\b.*?</\1>", "", html, flags=re.S | re.I)
        for tag in TAGS:
            opens = len(re.findall(r"<%s\b[^>]*>" % tag, body, re.I))
            closes = len(re.findall(r"</%s\s*>" % tag, body, re.I))
            if opens != closes:
                rep.fail("tags",
                         f"{page}: <{tag}> unbalanced, {opens} open vs {closes} close "
                         f"({opens - closes:+d})")


def load_ledger(local):
    """
    docs/SUPERLATIVE-LEDGER.md. One reviewed claim per row:

        | page | phrase | verdict | evidence |

    Only rows whose verdict is TRUE are honoured. A row is an assertion by a human
    that this claim is true about the OUTSIDE WORLD and therefore cannot rot when a
    city is added. Claims about our own dataset never belong here; they are a FAIL.
    """
    raw = fetch("docs/SUPERLATIVE-LEDGER.md", local) or ""
    out = set()
    for line in raw.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in ("page", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[2].upper().startswith("TRUE"):
            out.add((cells[0], cells[1].lower()))
    return out


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

    # Every page a reader can actually reach. The old scan covered index.html and the
    # city profiles only, which is why pick-and-compare.html sat at 14 banned phrases
    # and never once appeared in a FAIL.
    #
    # It was then widened to a HAND-MAINTAINED LIST, which is its own trap: a list of
    # pages someone remembered to add. privacy.html was never on it. Neither was a
    # stray scottsdale-vs-santa-fe-PROFILE.html (note the suffix -- the hub regex only
    # matches -retirement.html), which sat live on Netlify carrying four banned
    # superlatives and passed this gate clean, because the gate never looked at it.
    #
    # So: in local mode, discover from DISK. Anything that deploys is something a
    # reader can reach, and anything a reader can reach gets scanned. The filesystem is
    # the only list that cannot drift from what actually ships.
    pages = {}
    if local:
        root = pathlib.Path(local)
        found = sorted(root.glob("*.html")) + sorted(root.glob("cities/*/profile.html"))
        for p in found:
            rel = str(p.relative_to(root))
            html = fetch(rel, local)
            if html:
                pages[rel] = html
    else:
        # Remote mode cannot glob, so fall back to the known surfaces. This is the
        # post-deploy confirmation run, not the gate.
        pages = {"index.html": idx}
        for slug in slug_to_city:
            html = fetch(f"cities/{slug}/profile.html", local)
            if html:
                pages[f"cities/{slug}/profile.html"] = html

        hub = fetch("compare-retirement-cities.html", local) or ""
        others = sorted(set(
            re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)
        )) + [
            "compare-retirement-cities.html", "pick-and-compare.html",
            "where-should-i-retire-quiz.html", "visit-before-you-decide.html",
            "best-places-to-retire-on-a-budget.html",
            "best-places-to-retire-in-florida.html",
            "best-places-to-retire-in-the-midwest.html",
            "best-places-to-retire-avoid-natural-disasters.html",
            "top-cities-for-active-retirees.html", "top-cities-for-arts-lovers.html",
            "top-cities-for-foodies.html", "top-cities-for-healthcare.html",
            "top-cities-for-hikers.html", "top-cities-for-lgbtq-retirees.html",
            "top-cities-for-sports-fans.html",
            "value-navigator.html", "active-frontier.html", "wellness-blueprint.html",
            "globetrotter-guide.html", "urban-walkabout.html",
        ]
        for page in others:
            html = fetch(page, local)
            if html:
                pages[page] = html

    # --- FAIL: dataset-scoped phrasing (policy) ---
    # Two surfaces per page: rendered HTML, and prose held in JS string literals that
    # renders through the quiz modal, the compare tool, and friends. Report the
    # surrounding clause, not the bare phrase; "we cover" alone tells you nothing about
    # where to edit.
    banned = {}
    for page, html in pages.items():
        surfaces = [("", visible_text(html)), (" [in JS]", script_strings(html))]
        for tag, raw in surfaces:
            text = re.sub(r"\s+", " ", raw)
            for m in BANNED_SUPERLATIVE.finditer(text):
                a, b = max(0, m.start() - 60), min(len(text), m.end() + 25)
                ctx = text[a:b].strip()
                if a > 0:
                    ctx = "..." + ctx
                key = (page + tag, ctx)
                banned[key] = banned.get(key, 0) + 1

    for (page, ctx), n in sorted(banned.items()):
        times = f" (x{n})" if n > 1 else ""
        rep.fail("superlatives",
                 f'{page}: "{ctx}"{times} — scoped to our own dataset. '
                 f"Anchor to a figure or a named city instead.")

    # --- WARN: everything else sweeping, for human eyes ---
    #
    # TWO SURFACES, not one. This scan read visible_text() only, and the FAIL scan
    # above has read BOTH surfaces since July 12. That asymmetry is not academic:
    # every city card, quiz-modal highlight, and D2 blurb lives in a JS string
    # literal, which is where "Best value city in the Southeast" (Chattanooga) and
    # "Best value in FL" (Tampa) sat unreviewed while the rendered-HTML copies of
    # the same claims warned every run. Same blind spot, third time. It is closed.
    hits = {}
    for page, html in pages.items():
        for tag, raw in ((" ", visible_text(html)), (" [in JS]", script_strings(html))):
            text = re.sub(r"\s+", " ", raw)
            for m in claim.finditer(text):
                txt = re.sub(r"\s+", " ", m.group(0)).strip()
                key = (page + ("" if tag == " " else tag), txt)
                hits[key] = hits.get(key, 0) + 1

    # A claim about the outside world ("largest stadium in the country") cannot be
    # settled by a spreadsheet and cannot be rewritten away -- it is true, it is
    # load-bearing, and it should stay. But an unclearable warning is worse than no
    # warning: 39 permanent lines is a wall nobody reads, and a wall nobody reads is
    # where the next false claim hides. So a claim can be RETIRED from this queue by
    # recording it, with its evidence, in docs/SUPERLATIVE-LEDGER.md. Ledgered claims
    # go quiet. Anything not ledgered is, by definition, unreviewed, and shouts.
    #
    # The ledger is checked in both directions. An entry that no longer matches any
    # live page is reported as stale, so the ledger cannot quietly outlive the copy it
    # vouches for -- which is the exact rot this whole policy exists to prevent.
    ledger = load_ledger(local)
    unreviewed, seen = [], set()
    for (page, txt), n in sorted(hits.items()):
        key = (page.replace(" [in JS]", "").strip(), txt.lower())
        if key in ledger:
            seen.add(key)
            continue
        times = f" (x{n})" if n > 1 else ""
        unreviewed.append(f"{page.strip()}: \"{txt}\"{times}")

    for line in unreviewed:
        rep.warn("superlatives", f"UNREVIEWED {line}")

    for key in sorted(set(ledger) - seen):
        rep.warn("superlatives",
                 f"STALE LEDGER {key[0]}: \"{key[1]}\" is vouched for in "
                 f"SUPERLATIVE-LEDGER.md but no longer appears on the page. "
                 f"Delete the entry.")

    if not unreviewed:
        return

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
    """
    Em-dash policy: zero in rendered content. Guides stay grandfathered.

    This check used to scan visible_text() only, and only city profiles and comparison
    pages. Both gaps mattered:

      * visible_text() strips <script>, so the 1,092 em-dashes sitting in index.html's
        city pros/cons/highlight strings were invisible -- and they render, in the city
        cards and the quiz modal. Same blind spot that hid the superlatives twice.
      * index.html was never a target at all, so its 311 plain-HTML em-dashes were
        never counted either.

    On 2026-07-13 the check reported ZERO while 1,403 em-dashes were live on the home
    page. Scan both surfaces, and scan index.html.

    Not converted, deliberately: em-dashes inside <style>, and the '\u2014' UI
    placeholder used as a fallback when a value is missing (city.monthlyEst || '\u2014').
    Those are not prose. script_strings() only returns literals of 25+ chars, so the
    placeholder never reaches this check.
    """
    targets = [f"cities/{s}/profile.html" for s in slug_to_city]
    targets += re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", sitemap)
    targets += [
        "best-places-to-retire-on-a-budget.html",
        "best-places-to-retire-in-florida.html",
        "best-places-to-retire-in-the-midwest.html",
        "best-places-to-retire-avoid-natural-disasters.html",
        "top-cities-for-active-retirees.html", "top-cities-for-arts-lovers.html",
        "top-cities-for-foodies.html", "top-cities-for-healthcare.html",
        "top-cities-for-hikers.html", "top-cities-for-lgbtq-retirees.html",
        "top-cities-for-sports-fans.html",
        "pick-and-compare.html", "compare-retirement-cities.html",
    ]
    if GUIDES_TOO:
        targets += ["value-navigator.html", "active-frontier.html",
                    "wellness-blueprint.html", "globetrotter-guide.html",
                    "urban-walkabout.html"]

    pages = {"index.html": idx}
    for page in sorted(set(targets)):
        html = fetch(page, local)
        if html is not None:
            pages[page] = html

    for page, html in sorted(pages.items()):
        rendered = visible_text(html).count("\u2014")
        in_js = script_strings(html).count("\u2014")
        if rendered:
            rep.fail("emdash", f"{page}: {rendered} em-dash(es) in rendered text")
        if in_js:
            rep.fail("emdash", f"{page}: {in_js} em-dash(es) in JS strings "
                               f"(these render to the reader through the cards and modal)")


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


# ---------------------------------------------------------------------------
# Docs currency
# ---------------------------------------------------------------------------
# The governing docs go stale for a boring reason: they go stale WHILE the work
# is being done, and the person doing the work is the same person who would have
# to notice. Discipline does not fix that. A tool that is already being run at
# the exact moment of the deploy does.
#
# These are WARNINGS, not failures. A stale taskboard must never block a deploy.
# It should nag, at the one moment you are guaranteed to be looking.

DOC_MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
              "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}


def _doc_date(text):
    """Pull a date out of 'July 13, 2026' or 'Jul_13' or '2026-07-13'. None if absent."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return tuple(int(g) for g in m.groups())
    m = re.search(r"([A-Za-z]{3})[a-z]*[_ ](\d{1,2}),?[_ ]?(\d{4})?", text)
    if m and m.group(1)[:3].lower() in DOC_MONTHS:
        year = int(m.group(3)) if m.group(3) else 2026
        return (year, DOC_MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
    return None


def check_docs(rep, db_path, idx, sitemap, slug_to_city, local):
    """Are TASKBOARD.md and SITE-OPERATIONS-LOG.md current with the live repo?"""
    board = fetch("docs/TASKBOARD.md", local)
    log = fetch("docs/SITE-OPERATIONS-LOG.md", local)

    if board is None:
        rep.warn("docs", "docs/TASKBOARD.md not found; nothing tracked")
        return
    if log is None:
        rep.warn("docs", "docs/SITE-OPERATIONS-LOG.md not found")
        return

    # --- 1. counts the board asserts vs counts actually live -----------------
    live_profiles = len(slug_to_city)
    live_compares = len(set(re.findall(r"[a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html", sitemap)))

    m = re.search(r"(\d+)\s+profiles", board)
    if m and int(m.group(1)) != live_profiles:
        rep.warn("docs",
                 f"TASKBOARD.md asserts {m.group(1)} profiles; {live_profiles} are live. "
                 f"The board is behind the work.")
    elif not m:
        rep.warn("docs", "TASKBOARD.md states no profile count; add one so it can be checked")

    m = re.search(r"(\d+)\s+comparison pages", board)
    if m and int(m.group(1)) != live_compares:
        rep.warn("docs",
                 f"TASKBOARD.md asserts {m.group(1)} comparison pages; "
                 f"{live_compares} are live.")

    # --- 2. the DB the validator reads vs the DB the log registers -----------
    db_name = os.path.basename(db_path)
    if db_name not in log:
        rep.warn("docs",
                 f"SITE-OPERATIONS-LOG.md never mentions {db_name}, the database this "
                 f"validator is reading. The file registry in section 4 is stale.")

    # --- 3. is there a log entry for the current database? -------------------
    db_date = _doc_date(db_name)
    entries = re.findall(r"^### (\d{4}-\d{2}-\d{2})", log, re.M)
    newest_log = _doc_date(entries[0]) if entries else None
    if db_date and newest_log and newest_log < db_date:
        rep.warn("docs",
                 f"newest change-log entry is {entries[0]}, but the live database is "
                 f"{db_name}. A database version shipped without being logged.")

    # --- 4. is the board older than the log? --------------------------------
    m = re.search(r"\*\*Last updated:\*\*\s*([^\n(]+)", board)
    board_date = _doc_date(m.group(1)) if m else None
    if board_date is None:
        rep.warn("docs", "TASKBOARD.md has no parseable '**Last updated:**' date")
    elif newest_log and board_date < newest_log:
        rep.warn("docs",
                 f"TASKBOARD.md last updated {board_date[0]}-{board_date[1]:02d}-"
                 f"{board_date[2]:02d}, but SITE-OPERATIONS-LOG.md has an entry dated "
                 f"{entries[0]}. Work shipped that the board does not know about.")

    # --- 5. exactly one database in docs/ (local only; cannot list on GitHub) -
    if local:
        docs_dir = os.path.join(local, "docs")
        if os.path.isdir(docs_dir):
            dbs = [f for f in os.listdir(docs_dir)
                   if f.startswith("CityDatabase_") and f.endswith(".xlsx")]
            if len(dbs) > 1:
                rep.fail("docs",
                         f"{len(dbs)} CityDatabase files in docs/: {sorted(dbs)}. "
                         f"Leaving more than one invites a future session to read the "
                         f"wrong one. Delete the superseded file.")
            elif dbs and dbs[0] != db_name:
                rep.fail("docs",
                         f"DEFAULT_DB points at {db_name}, but docs/ contains "
                         f"{dbs[0]}. One of the two is wrong.")


def check_db(rep, db_path):
    """Database hygiene. Standard library only, same as load_db."""
    rows = _read_xlsx(db_path, "City Database")
    header = {i: str(v).replace("\n", " ").strip()
              for i, v in rows[1].items() if str(v).strip()}
    col = {name: i for i, name in header.items()}

    seen = set()
    d5_by_state = {}
    for r in rows[2:]:
        city = str(r.get(col["City"], "")).strip()
        if not city:
            continue
        state = str(r.get(col["ST"], "")).strip()
        raw = str(r.get(col["Median Home"], "")).strip()

        try:
            d5_by_state.setdefault(state, []).append(
                (city, int(float(r.get(col["D5 Tax"])))))
        except (TypeError, ValueError):
            rep.fail("db", f"{city}, {state}: D5 Tax is not a number")

        figs = re.findall(r"\$[\d,]+", raw)
        if len(figs) > 1 or re.search(r"[–—]", raw):
            rep.fail("db",
                     f"{city}, {state}: Median Home is {raw!r}, a RANGE. "
                     f"MEDIAN-HOME-METHODOLOGY.md v1.2 requires a single citywide "
                     f"ZHVI figure for all cities. Replace with one number and move "
                     f"the spread into a Neighborhood Reality Check note.")
        elif not raw.startswith("$"):
            rep.fail("db",
                     f"{city}, {state}: Median Home is {raw!r}, not a '$N,NNN' string "
                     f"like the other rows. Scripts that string-match this column will "
                     f"silently skip or mis-parse it.")

        if (city, state) in seen:
            rep.fail("db", f"duplicate DB row: {city}, {state}")
        seen.add((city, state))

    # ---- D5 is a STATE-level score. See docs/D5-TAX-METHODOLOGY.md.
    #
    # Every input D5 measures (income tax on SS, on pension/IRA/401k, the overall
    # rate, property tax, sales tax) is set at the state line or above. The rubric's
    # neighborhood carve-out (Universal Methodology) is scoped to D2, D6 and D9 and
    # does NOT reach D5. And the database holds no per-city tax input at all:
    # PropTax Rate % carries exactly one value per state, for all 39 states.
    #
    # So a within-state D5 spread is not a judgment call, it is unsourced. Oregon had
    # Bend at 6 and Eugene at 3 while Bend's own cons list said Oregon taxes are "worst
    # for retirees in the Pacific Northwest". Fort Collins vs Boulder shipped a whole
    # paragraph explaining a 2-point gap "that reflects local tax burden" on a page
    # that also stated both cities pay an identical property rate.
    #
    # A 1-point spread is tolerated: local sales-tax and millage differences are real
    # even if the DB does not currently record them. 2+ is always a mistake.
    for state, entries in sorted(d5_by_state.items()):
        scores = [s for _, s in entries]
        spread = max(scores) - min(scores)
        if spread > D5_MAX_SPREAD:
            detail = ", ".join(f"{c} {s}" for c, s in sorted(entries, key=lambda e: e[1]))
            rep.fail("db",
                     f"{state}: D5 Tax spans {min(scores)}–{max(scores)} "
                     f"({detail}). D5 is a state-level score; a spread of "
                     f"{spread} points has no source in the database. "
                     f"See docs/D5-TAX-METHODOLOGY.md.")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Validate RetireMeHere against the City Database.")
    ap.add_argument("--db", default=DEFAULT_DB, help=f"database path (default: {DEFAULT_DB})")
    ap.add_argument("--local", help="validate a local checkout instead of live GitHub")
    ap.add_argument("--only", action="append",
                    choices=["figures", "profiles", "routing", "cards",
                             "superlatives", "emdash", "tags", "affiliate", "db",
                             "docs"],
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
        "tags", "affiliate", "db", "docs"}

    source = args.local or "live GitHub"
    print(f"RetireMeHere validator")
    # One command, two entirely different jobs, and until now nothing on screen said which
    # one you got. Run it bare before pushing and it grades the OLD live site with the NEW
    # rules, then reports failures you already fixed. It did exactly that on July 14 2026.
    if args.local:
        print(f"  mode:     PRE-DEPLOY GATE -- reading the files on this machine")
    else:
        print(f"  mode:     POST-DEPLOY CHECK -- reading the LIVE files from GitHub,")
        print(f"            not your working copy. If you have not pushed, this is")
        print(f"            grading the OLD site. The gate is: --local .")
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

    # The slug map is needed by several checks, so build it exactly once, in exactly
    # one format: {slug: (City, ST)}. It used to be rebuilt in a second place when the
    # routing group was skipped, in the OLD string format, which made check_profiles
    # silently iterate over nothing and report a clean zero. A checking tool that
    # quietly reports success when it has not checked anything is worse than no tool.
    slug_to_city = published_profiles(idx)
    if not slug_to_city:
        print("Could not parse PUBLISHED_PROFILES from index.html.", file=sys.stderr)
        return 2

    if "routing" in groups:
        check_routing(rep, db, idx, sitemap, args.local, slug_to_city)

    if "figures" in groups:
        check_figures(rep, db, idx)
        check_tiers(rep, db, idx)
    if "profiles" in groups:
        if not slug_to_city:
            rep.fail("profiles", "no published profiles found; nothing was checked")
        check_profiles(rep, db, slug_to_city, args.local)
    if "cards" in groups:
        check_cards(rep, db, idx, args.local)
    if "superlatives" in groups:
        check_superlatives(rep, db, idx, slug_to_city, args.local)
        check_dead_dimension_guards(rep, db, idx, slug_to_city, args.local)
        check_comparison_scores(rep, db, idx, slug_to_city, args.local)
        check_hardcoded_counts(rep, db, idx, slug_to_city, args.local)
        check_numeric_cells(rep, db, idx, slug_to_city, args.local)
    if "emdash" in groups:
        check_emdash(rep, idx, sitemap, slug_to_city, args.local)
    if "tags" in groups:
        check_tag_balance(rep, db, idx, sitemap, slug_to_city, args.local)
    if "affiliate" in groups:
        check_affiliate(rep, slug_to_city, args.local)
    if "db" in groups:
        check_db(rep, args.db)
    if "docs" in groups:
        check_docs(rep, args.db, idx, sitemap, slug_to_city, args.local)

    return rep.render()


if __name__ == "__main__":
    sys.exit(main())
