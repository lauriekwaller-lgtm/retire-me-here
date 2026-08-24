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
    python3 tools/validate.py --quiet               # failures only, hides the harness lines

Check groups:
    figures      CITIES array + CITY_ENRICHMENT modal strings vs DB
    profiles     profile pages: monthly + citywide home value vs DB, plus the
                 abbreviated monthly stat card, the variable score slots, and
                 every home figure in profile prose and the JSON-LD FAQ
    routing      PUBLISHED_PROFILES <-> profile files <-> sitemap parity
    cards        landing pages: stale "coming soon" + card figures vs DB,
                 and roster membership for pages whose roster is a DB predicate
    superlatives every affordability superlative on the site, checked against the DB
    emdash       em-dash policy (profiles + comparison pages)
    affiliate    affiliate codes: duplicates, missing brands, multiple codes per page
    db           database hygiene
    sitemap      every <lastmod> well-formed, and not older than git
    nav          one nav, byte-for-byte, on every page but the homepage
    cta          header button readable, resting and hover
    harness      the planted-error tests in tools/, run against this checkout

Why this exists: every figure on this site is a string that either matches a DB cell
or does not. That is machine-checkable. Before this script existed, it was not being
checked, and drift accumulated silently across 100 cities and 80 pages.
"""

import argparse
import csv
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import urllib.request

from html import unescape as html_unescape

# Used only by the other-time guard in _sc_scan. Wall-clock rather than a constant so
# the guard does not need editing every January; see the comment there for why the
# rollover is safe on the current corpus.
from datetime import date

# check_sitemap_lastmod and tools/build_sitemap.py must agree on what "last
# changed" means, so the definition lives in one module they both import
# rather than being written out twice and drifting.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sitemap_dates import GitUnavailable, effective_dates, is_git_checkout

CURRENT_YEAR = date.today().year

RAW = "https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main"
# The database already lives in the repo, in docs/. That is the canonical copy the
# validator reads. Update this constant when you bump the version, in the same commit
# that adds the new xlsx.
DEFAULT_DB = "docs/CityDatabase_Jul_27_v19.1.xlsx"

# The date in DEFAULT_DB's filename, as a date. check_docs asserts the two agree,
# so this cannot drift from the file it describes; bump both in the same commit.
# It exists because a page's stated data vintage has to be checked against
# SOMETHING, and the filename is the only place the database records its own age.
DB_VERSION_DATE = date(2026, 7, 27)

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

# BUDGET-METHODOLOGY.md section 6, transcribed. Exact values, never ranges: an
# earlier version of that document published them as bands ("low-cost rural states
# 0.88-0.95"), which is not precise enough to recompute a city from and silently
# collapsed real distinctions (OR and CO were both "1.07-1.08" but are 1.08 and 1.07).
#
# These cover the states with a city in the database and nothing else. That is
# deliberate: an unexercised value is an unverified value. A city in a 40th state
# needs both multipliers derived first, per section 6, and check_afford_data fails
# on a state present in one place and absent from the other rather than defaulting.
AFFORD_COL = {
    "AL": 0.88, "AR": 0.88, "OK": 0.88,
    "KY": 0.90, "LA": 0.90,
    "IN": 0.92, "TN": 0.92,
    "IA": 0.93, "MO": 0.93, "SD": 0.93,
    "OH": 0.94, "SC": 0.94,
    "GA": 0.95, "MI": 0.95, "NC": 0.95, "WI": 0.95,
    "TX": 0.96,
    "NM": 0.98, "PA": 0.98,
    "DE": 1.00, "ID": 1.00, "ME": 1.00, "WY": 1.00,
    "FL": 1.02, "MN": 1.02, "MT": 1.02,
    "AZ": 1.03, "UT": 1.03, "VA": 1.03,
    "NH": 1.05, "NV": 1.05, "VT": 1.05,
    "CO": 1.07, "MD": 1.07,
    "OR": 1.08,
    "WA": 1.10,
    "MA": 1.15, "NY": 1.15,
    "CA": 1.20,
}

# A separate scale from AFFORD_COL, and the two do not track each other: TX is 0.96
# on cost of living but 1.05 on Medigap; MN is 1.02 and 0.95.
AFFORD_MEDIGAP = {
    "SD": 0.88,
    "IA": 0.90, "WY": 0.90,
    "AL": 0.92, "AR": 0.92, "KY": 0.92, "OK": 0.92, "TN": 0.92,
    "MN": 0.95, "WI": 0.95,
    "AZ": 1.00, "CO": 1.00, "DE": 1.00, "GA": 1.00, "ID": 1.00, "IN": 1.00,
    "LA": 1.00, "MD": 1.00, "ME": 1.00, "MI": 1.00, "MO": 1.00, "MT": 1.00,
    "NC": 1.00, "NH": 1.00, "NM": 1.00, "NV": 1.00, "OH": 1.00, "OR": 1.00,
    "SC": 1.00, "UT": 1.00, "VA": 1.00, "VT": 1.00, "WA": 1.00,
    "PA": 1.05, "TX": 1.05,
    "FL": 1.15,
    "CA": 1.25, "MA": 1.25,
    "NY": 1.40,
}

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


# ------------------------------------------------------- highlight home figures
#
# The `highlight` string is the one place a home figure is prose, not a field. It
# renders on the card, in the modal, and in the compare table, and until now nothing
# held it to `medianHome` sitting four lines away in the same object. Nine cities had
# drifted: Des Moines said $217K against a DB $191K, La Crosse $285K against $243K,
# Sioux Falls $333K on one surface and $285K on the other against a DB $314K.
#
# Scope is the hard part. Three things in these strings are dollar figures that are
# SUPPOSED to disagree with medianHome, and a naive "every $ figure must match" check
# fires on all of them, forever:
#
#   1. Neighborhood ranges.  "Citywide median home $195K but retirees target
#      Germantown, Collierville ($280K–$500K)."  The range is the point of the
#      sentence. Every NRC city carries one.
#   2. Cross-city references. Tampa's highlight names Naples' figure; Chattanooga
#      names Asheville's; Corpus Christi names Pensacola's. All correct, none ours.
#   3. Figures that are not home values at all. Tulsa's "$465M Gathering Place",
#      Traverse City's "$132K joint retirement income deduction", Provincetown's
#      "$2M estate tax cliff", and every monthly budget range on the site.
#
# So the figure has to be ANCHORED to a home-value noun to be in scope, the same way
# PROSCONS_HOME works. That one rule kills all three classes: the neighborhood range
# sits after "retirees target", not after "median home"; the cross-city figure hangs
# off a city name; and a park's price tag is not a home value. The cross-city veto
# below is belt-and-braces for the day someone writes "Naples' median home is $585K"
# inside Tampa's string, which the anchor alone would not catch.
HL_MONEY = r"\$\s?\d[\d,]*(?:\.\d+)?\s?[KkMm]?"
HL_DASH = r"[\u2013\u2014-]"
# Range-aware on purpose: a range must be captured WHOLE so it self-rejects in
# _hl_money(). Capturing only the low end is how "$800K–$1M median" would have been
# graded as a claim of $800K.
HL_FIG = (r"~?(" + HL_MONEY +
          r"(?:\s*" + HL_DASH + r"\s*\$?\s?\d[\d,]*(?:\.\d+)?\s?[KkMm]?)?)")

HL_NOUN = (r"(?:citywide|typical|median|average)?\s*"
           r"(?:single-family\s+|starter\s+|entry-level\s+)?"
           r"home\s+(?:value|price|sale\s+price)s?"
           r"|(?:citywide|typical|median|average)\s+"
           r"(?:single-family\s+|starter\s+)?homes?")

HL_BOUNDW = r"under|below|less\s+than|over|above|from|starting\s+at|upward\s+of"

# Up to 20 characters of connector between the noun and the figure ("home values
# around $280K", "home value is $585K"), but never across a sentence boundary, never
# across another "$", and never across a bound word: "median homes under $230K" is a
# BOUND claim, handled below, and must not also be read as a claim that the median
# IS $230K, or one error reports twice.
HL_GAP = r"(?:(?!\b(?:" + HL_BOUNDW + r")\b)[^.;!?$]){0,20}?"

HL_HOME_FIG = re.compile(
    r"(?:" + HL_NOUN + r")" + HL_GAP + HL_FIG +
    r"|" + HL_FIG + r"\s+(?:citywide\s+)?(?:" + HL_NOUN + r"|median)\b", re.I)

HL_HOME_BOUND = re.compile(
    r"(?:" + HL_NOUN + r"|homes?)" + HL_GAP +
    r"\b(" + HL_BOUNDW + r")\s+" + HL_FIG, re.I)


def _hl_money(tok):
    """Parse one prose money token. None means 'not a single figure, skip it'."""
    tok = tok.strip().strip(".,;:").replace("~", "")
    if re.search(HL_DASH, tok) or tok.count("$") > 1:
        return None                      # a range
    return money_to_int(tok.replace(" ", ""))


def _hl_agrees(tok, val, home):
    """
    Exact agreement, no tolerance band.

    A band is precisely how the nine drifted figures hid: HOME_TOLERANCE is 3%, and
    $217K against $191K is 13% but $275K against $273K is 0.7%. One got caught by a
    band and one did not, and both are equally wrong. So: a figure written in
    thousands must equal round(DB/1000) exactly. $224K for a $224,000 DB cell passes;
    $223K does not.

    Figures written in millions are held to home_forms(), which is the convention
    already shipped for the modal check: $1.85M is an accepted rendering of
    $1,851,000. That is a rounding convention, not a tolerance, and keeping one
    convention across the validator beats inventing a second one here.
    """
    clean = tok.strip().strip(".,;:").replace(" ", "").upper()
    if clean.endswith("M"):
        return clean in {f"${home / 1e6:.2f}M".upper(),
                         f"${home / 1e6:.1f}M".upper()}
    return round(val / 1000) == round(home / 1000)


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



TAXTOOL_PAGE = "states-that-dont-tax-retirement-income.html"


def check_taxtool_data(rep, db_path, local):
    """
    The state tax filter carries two embedded copies of database content:
    TAXFACTS (the State Tax Facts sheet, one object per state) and TAXCITIES
    (every city with its D5). It has to: the page is static and filters
    client-side. An embedded copy is the drift this validator exists for, so
    every field on the page is compared to its workbook cell on every run.

    Three promises:

      1. ROSTER, both ways, both arrays. Every facts state is on the page and
         every page state is in the sheet; every database city appears under
         its state and no invented city appears anywhere. A state added to the
         sheet and not to the page is invisible to every reader of this tool.
      2. CELLS. Every enum, rate, and note on the page equals its sheet cell.
         Notes are compared as exact strings: the note IS the product here,
         and a note claiming an exemption the sheet no longer records is a lie
         the reader cannot detect.
      3. D5. Each city chip's score equals its City Database cell. The
         Philadelphia correction (v19.1) touched four embedded arrays; this is
         the check that would have caught a missed fifth.

    And the standing rule: a page that cannot be read, or an array that parses
    to nothing, fails loudly rather than comparing zero states and reporting
    clean.
    """
    html = fetch(TAXTOOL_PAGE, local)
    if html is None:
        rep.fail("figures",
                 f"{TAXTOOL_PAGE} could not be read, so its embedded tax data "
                 f"was never compared to the database. If the page was renamed, "
                 f"rename it here too; if it was retired, delete this check "
                 f"deliberately.")
        return

    fm = re.search(r"const TAXFACTS = (\[.*?\]); /\*END_TAXFACTS\*/", html, re.S)
    cm = re.search(r"const TAXCITIES = (\{.*?\}); /\*END_TAXCITIES\*/", html, re.S)
    if not fm or not cm:
        rep.fail("figures",
                 f"{TAXTOOL_PAGE}: the TAXFACTS or TAXCITIES block could not be "
                 f"parsed. Either the arrays are gone or their end markers "
                 f"moved, and either way this check just compared nothing.")
        return
    try:
        page_facts = {f["st"]: f for f in json.loads(fm.group(1))}
        page_cities = json.loads(cm.group(1))
    except (ValueError, KeyError, TypeError):
        rep.fail("figures",
                 f"{TAXTOOL_PAGE}: the embedded arrays are not valid JSON, so "
                 f"nothing was compared and the page's own script is broken "
                 f"for every reader.")
        return
    if not page_facts:
        rep.fail("figures",
                 f"{TAXTOOL_PAGE}: TAXFACTS parsed to zero states. This check "
                 f"verified nothing rather than finding nothing.")
        return

    fr = _read_xlsx(db_path, "State Tax Facts")
    fh = {i: str(v).replace("\n", " ").strip()
          for i, v in fr[1].items() if str(v).strip()}
    fc = {n: i for i, n in fh.items()}
    sheet = {}
    for r in fr[2:]:
        st = str(r.get(fc["ST"], "")).strip()
        if st:
            sheet[st] = r

    for st in sorted(set(sheet) - set(page_facts)):
        rep.fail("figures",
                 f"{TAXTOOL_PAGE}: {st} is in the State Tax Facts sheet but is "
                 f"not on the page. Every reader filtering states will never "
                 f"see it.")
    for st in sorted(set(page_facts) - set(sheet)):
        rep.fail("figures",
                 f"{TAXTOOL_PAGE}: the page carries {st}, which is not in the "
                 f"State Tax Facts sheet. Invented states do not get shown to "
                 f"readers.")

    FIELDS = (("itype", "Income Tax Type", False), ("top", "Top Rate %", True),
              ("ss", "SS Treatment", False),
              ("ret", "Retirement Income Treatment", False),
              ("sales", "Sales Tax Combined %", True),
              ("ptax", "PropTax Rate %", True), ("estate", "Estate Tax", False),
              ("inherit", "Inheritance Tax", False), ("ty", "Tax Year", True))
    for st in sorted(set(sheet) & set(page_facts)):
        pf, row = page_facts[st], sheet[st]
        for key, colname, numeric in FIELDS:
            want, got = row.get(fc[colname]), pf.get(key)
            if numeric:
                try:
                    bad = abs(float(want) - float(got)) > 1e-9
                except (TypeError, ValueError):
                    bad = True
            else:
                bad = str(want).strip() != str(got).strip()
            if bad:
                rep.fail("figures",
                         f"{TAXTOOL_PAGE}: {st} {key} is {got!r}, which "
                         f"disagrees with the State Tax Facts cell {want!r}. "
                         f"The page filters readers on a fact the database "
                         f"does not hold.")
        want_note = str(row.get(fc["Retirement Income Note"], "")).strip()
        if str(pf.get("note", "")).strip() != want_note:
            rep.fail("figures",
                     f"{TAXTOOL_PAGE}: the note for {st} does not match the "
                     f"sheet. Prose restating checked data is itself data; a "
                     f"drifted note is a claim the reader cannot verify.")

    cr = _read_xlsx(db_path, "City Database")
    chh = {i: str(v).replace("\n", " ").strip()
           for i, v in cr[1].items() if str(v).strip()}
    ccc = {n: i for i, n in chh.items()}
    db_cities = {}
    for r in cr[2:]:
        city = str(r.get(ccc["City"], "")).strip()
        if not city:
            continue
        st = str(r.get(ccc["ST"], "")).strip()
        db_cities.setdefault(st, {})[city] = int(float(r[ccc["D5 Tax"]]))

    page_by_state = {st: {c["n"]: c["d5"] for c in lst}
                     for st, lst in page_cities.items()}
    for st in sorted(set(db_cities) | set(page_by_state)):
        want, got = db_cities.get(st, {}), page_by_state.get(st, {})
        for city in sorted(set(want) - set(got)):
            rep.fail("figures",
                     f"{TAXTOOL_PAGE}: {city}, {st} is missing from the page's "
                     f"city list. A city added to the database and not here is "
                     f"invisible to every reader of this tool.")
        for city in sorted(set(got) - set(want)):
            rep.fail("figures",
                     f"{TAXTOOL_PAGE}: the page lists {city}, {st}, which is "
                     f"not in the database.")
        for city in sorted(set(want) & set(got)):
            if want[city] != got[city]:
                rep.fail("figures",
                         f"{TAXTOOL_PAGE}: {city}, {st} shows D5 as "
                         f"{got[city]}, the database says {want[city]}. A "
                         f"stale score on a live surface is exactly the "
                         f"failure the v19.1 correction swept for.")


AFFORD_PAGE = "where-can-i-afford-to-retire.html"

# Every column the page embeds, and the database column it must equal. The page
# recomputes its monthly figures at run time from these inputs, per
# BUDGET-METHODOLOGY.md section 14.4, which forbids storing precomputed figures so
# that a database rebuild propagates without a second update step. That design is
# only safe if the inputs cannot drift, which is what check_afford_data enforces.
AFFORD_FIELDS = {
    "h": ("home", "Median Home"),
    "t": ("proptax", "PropTax Rate %"),
    "i": ("insurance", "HO Insur Est $/yr"),
    "w": ("warm", "Climate Warm W"),
    "x": ("heat", "HEAT (0-10)"),
}

AFFORD_ROW = re.compile(
    r'\{n:"((?:[^"\\]|\\.)*)",s:"([A-Z]{2})",h:(\d+),t:([\d.]+),i:(\d+),'
    r'w:(\d+),x:(\d+),d:\[(\d+(?:,\d+){9})\]\}')

AFFORD_CONSTANTS = (
    ("PMMS_RATE",    r"var PMMS_RATE\s*=\s*([\d.]+)",    0.0652),
    ("DOWN_FRAC",    r"var DOWN_FRAC\s*=\s*([\d.]+)",    0.20),
    ("TERM_MONTHS",  r"var TERM_MONTHS\s*=\s*(\d+)",     360),
    ("PART_B",       r"PART_B\s*=\s*([\d.]+)",           202.90),
    ("PART_D",       r"PART_D\s*=\s*([\d.]+)",           38.99),
    ("MEDIGAP_BASE", r"MEDIGAP_BASE\s*=\s*([\d.]+)",     165),
    ("OOP",          r"OOP\s*=\s*([\d.]+)",              150),
    ("UTIL_BASE",    r"UTIL_BASE\s*=\s*([\d.]+)",        400),
    ("FOOD_BASE",    r"FOOD_BASE\s*=\s*([\d.]+)",        750),
    ("DISC_BASE",    r"DISC_BASE\s*=\s*([\d.]+)",        500),
)


def afford_central(row):
    """
    BUDGET-METHODOLOGY.md sections 3 through 6 in full: the published central
    monthly estimate for a couple aged 65+ buying with 20% down.

    Written out here rather than imported, because there is nowhere to import it
    from. The formula lives in a markdown document and in the page's JavaScript,
    and the point of this function is to be a THIRD, independent statement that
    the other two get checked against.
    """
    home = row["home"]
    col = AFFORD_COL[row["state"]]
    mg = AFFORD_MEDIGAP[row["state"]]

    r = 0.0652 / 12                          # Freddie Mac PMMS, week of 06/11/2026
    pi = (home * 0.80) * r / (1 - (1 + r) ** -360)

    prop_tax = home * (row["proptax"] / 100.0) / 12
    insurance = row["insurance"] / 12.0
    healthcare = 2 * 202.90 + 2 * 38.99 + 2 * 165 * mg + 150

    adj = 0
    heat, warm = row["heat"], row["warm"]
    adj += 80 if heat >= 8 else 40 if heat >= 6 else -20 if heat <= 3 else 0
    adj += 80 if warm <= 3 else 30 if warm <= 5 else -30 if warm >= 9 else 0

    # The multiplier lands on the baseline, THEN the climate adjustment is added.
    # Not the other way round: applying COL to (400 + adj) disagrees with the
    # published Monthly Est on six cities. Section 5 does not say which order, so
    # the database settles it, and this comment is the record of that.
    utilities = 400 * col + adj

    walk = row["scores"]["D6"]
    transport = 400 if walk >= 8 else 550 if walk >= 6 else 650 if walk >= 4 else 700

    return (pi + prop_tax + insurance + healthcare + utilities
            + 750 * col + transport + 500 * col)


def check_afford_data(rep, db_path, local):
    """
    where-can-i-afford-to-retire.html carries its own copy of the city inputs.

    It has to. The page computes a personalised monthly cost from an equity figure
    the reader types, which no precomputed column can answer, and section 14.4 of
    BUDGET-METHODOLOGY.md requires it to derive that at run time from current data.
    So the page holds Median Home, the property tax rate, the insurance estimate,
    two climate fields and all ten dimension scores for every city, in an
    AFFORD_CITIES array.

    A second copy of the database is exactly the drift this validator exists for.
    The July 27 ZHVI rebase moved fourteen cities across a tier boundary; a page
    holding a stale Median Home would have gone on quoting the old mortgage to
    every reader, silently, and the only symptom would have been figures that were
    merely plausible.

    Four assertions, in order of how badly each one fails:

      1. ROSTER. Same cities, same states, no extras, no omissions, no duplicates.
         A city added to the database and not to the page is invisible to every
         reader of this tool, and nothing else on the site would notice.
      2. CELLS. Every embedded field equals its database cell.
      3. ARITHMETIC. The page's inputs, run through the published formula, must
         rebuild the Monthly Est string and the Budget Range integer the database
         publishes. This is the gate section 9 calls for under Reproducibility. It
         catches what 1 and 2 cannot: data that is perfect and CONSTANTS that have
         drifted, which is the failure that produces plausible wrong numbers.
      4. CONSTANTS. The page's rate, baselines and per-state multipliers match the
         ones this file computes with. Assertion 3 would mostly cover this, but it
         fails as a puzzle ("Boise is $80 out") instead of as an answer ("the Idaho
         cost-of-living modifier on the page says 1.02, section 6 says 1.00").

    And, because this codebase keeps rediscovering it: a page that cannot be read,
    or an array that parses to nothing, fails loudly rather than comparing zero
    cities and reporting clean.
    """
    html = fetch(AFFORD_PAGE, local)
    if html is None:
        rep.fail("figures",
                 f"{AFFORD_PAGE} could not be read, so its embedded city data was "
                 f"never compared to the database. If the page was renamed, rename it "
                 f"here too; if it was retired, delete this check deliberately.")
        return

    rows = AFFORD_ROW.findall(html)
    if not rows:
        rep.fail("figures",
                 f"{AFFORD_PAGE}: the AFFORD_CITIES array parsed to zero rows. Either "
                 f"the array is gone or its shape has changed, and either way this "
                 f"check just compared nothing to the database.")
        return

    # ---- 4. constants, read out of the page ------------------------------
    for label, pattern, expected in AFFORD_CONSTANTS:
        m = re.search(pattern, html)
        if not m:
            rep.fail("figures",
                     f"{AFFORD_PAGE}: constant {label} not found, so the formula "
                     f"cannot be checked against BUDGET-METHODOLOGY.md sections 4-5")
        elif abs(float(m.group(1)) - expected) > 1e-9:
            rep.fail("figures",
                     f"{AFFORD_PAGE}: {label} is {m.group(1)}, methodology says "
                     f"{expected}. Every monthly figure on the page is wrong.")

    for var, table, sect in (("COL_MOD", AFFORD_COL, "cost-of-living"),
                             ("MEDIGAP_MOD", AFFORD_MEDIGAP, "Medigap")):
        m = re.search(r"var %s\s*=\s*\{(.*?)\};" % var, html, re.S)
        if not m:
            rep.fail("figures",
                     f"{AFFORD_PAGE}: the {var} table was not found, so the per-state "
                     f"{sect} multipliers were never checked")
            continue
        on_page = {k: float(v)
                   for k, v in re.findall(r"([A-Z]{2}):\s*([\d.]+)", m.group(1))}
        for st in sorted(set(on_page) | set(table)):
            want_v, got_v = table.get(st), on_page.get(st)
            if want_v is None:
                rep.fail("figures", f"{AFFORD_PAGE}: {var} carries {st}, which "
                                    f"BUDGET-METHODOLOGY.md section 6 does not list")
            elif got_v is None:
                rep.fail("figures", f"{AFFORD_PAGE}: {var} is missing {st}. Every {st} "
                                    f"city computes as NaN and drops out of the results "
                                    f"without a word")
            elif abs(want_v - got_v) > 1e-9:
                rep.fail("figures", f"{AFFORD_PAGE}: {var}[{st}] is {got_v}, section 6 "
                                    f"says {want_v}")

    # ---- the database, read for the columns load_db does not carry -------
    raw = _read_xlsx(db_path, "City Database")
    header = {i: str(v).replace("\n", " ").strip()
              for i, v in raw[1].items() if str(v).strip()}
    col = {name: i for i, name in header.items()}
    missing = [c for _, c in AFFORD_FIELDS.values() if c not in col]
    if missing:
        rep.fail("figures",
                 f"{os.path.basename(db_path)}: columns {missing} are missing, and "
                 f"{AFFORD_PAGE} is built out of them")
        return

    want = {}
    for r in raw[2:]:
        city = str(r.get(col["City"], "")).strip()
        if not city:
            continue
        state = str(r.get(col["ST"], "")).strip()
        want[(city, state)] = {
            "state": state,
            "home": money_to_int(str(r.get(col["Median Home"], "")).strip()),
            "proptax": round(float(r[col["PropTax Rate %"]]), 2),
            "insurance": int(r[col["HO Insur Est $/yr"]]),
            "warm": int(r[col["Climate Warm W"]]),
            "heat": int(r[col["HEAT (0-10)"]]),
            "scores": {k: int(r[col[c]]) for k, c in DIMS},
            "monthly": str(r.get(col["Monthly Est"], "")).strip(),
            "range": int(r[col["Budget Range"]]),
        }

    # ---- 1. roster -------------------------------------------------------
    got = {}
    for name, st, home, tax, ins, warm, heat, dims in rows:
        key = (name, st)
        if key in got:
            rep.fail("figures", f"{AFFORD_PAGE}: {name}, {st} appears in "
                                f"AFFORD_CITIES more than once")
        got[key] = {
            "home": int(home), "proptax": float(tax), "insurance": int(ins),
            "warm": int(warm), "heat": int(heat),
            "scores": dict(zip([k for k, _ in DIMS],
                               [int(v) for v in dims.split(",")])),
        }

    for city, st in sorted(set(got) - set(want)):
        rep.fail("figures", f"{AFFORD_PAGE}: {city}, {st} is in AFFORD_CITIES but not "
                            f"in the database")
    for city, st in sorted(set(want) - set(got)):
        rep.fail("figures", f"{AFFORD_PAGE}: {city}, {st} is in the database but has "
                            f"no AFFORD_CITIES row, so no reader of this tool can ever "
                            f"be shown it")

    # ---- 2. cells --------------------------------------------------------
    for city, st in sorted(set(got) & set(want)):
        page, db_row = got[(city, st)], want[(city, st)]
        for field, label in AFFORD_FIELDS.values():
            if abs(float(page[field]) - float(db_row[field])) > 1e-9:
                rep.fail("figures",
                         f"{AFFORD_PAGE}: {city}, {st} {label} is {page[field]}, "
                         f"database says {db_row[field]}")
        for dim, _ in DIMS:
            if page["scores"][dim] != db_row["scores"][dim]:
                rep.fail("figures",
                         f"{AFFORD_PAGE}: {city}, {st} {dim} is {page['scores'][dim]}, "
                         f"database says {db_row['scores'][dim]}")

    # ---- 3. arithmetic ---------------------------------------------------
    checked = 0
    for city, st in sorted(set(got) & set(want)):
        db_row = want[(city, st)]
        central = afford_central(db_row)
        lo = int(round(central * 0.90 / 100.0)) * 100
        hi = int(round(central * 1.12 / 100.0)) * 100
        rebuilt = f"${lo:,}\u2013${hi:,}/mo"
        if rebuilt != db_row["monthly"]:
            rep.fail("figures",
                     f"{city}, {st}: the published formula rebuilds Monthly Est as "
                     f"{rebuilt}, the database says {db_row['monthly']}. One of the two "
                     f"drifted, and {AFFORD_PAGE} quotes readers the formula.")
        tier = (1 if central < 5500 else 2 if central < 6500 else
                3 if central < 7500 else 4 if central < 9000 else 5)
        if tier != db_row["range"]:
            rep.fail("figures",
                     f"{city}, {st}: the formula puts the central estimate at "
                     f"${round(central):,}, which is Budget Range {tier}; the database "
                     f"says {db_row['range']}")
        checked += 1

    if checked == 0:
        rep.fail("figures",
                 f"{AFFORD_PAGE}: not one city was checked. The page and the database "
                 f"have no city in common, which is not a state to report clean from.")


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


def _highlight_rows(idx, pc, rep):
    """
    Every (city, state, highlight, surface) pair on the two surfaces that carry one.

    Two surfaces, two formats, same data. index.html holds JS object literals with
    unquoted keys, which is not JSON and will not parse as JSON. pick-and-compare.html
    holds a single-line JSON array under `const CITIES =`, which will. Parse each the
    way it is actually written rather than forcing one reader to cover both.
    """
    rows = []

    src = js_object_slice(idx, "CITIES")
    if not src:
        rep.fail("figures", "highlight check: could not locate CITIES in index.html")
    for obj in re.split(r"\n  \{", src)[1:]:
        nm = re.search(r'name:\s*"([^"]+)",\s*state:\s*"([^"]+)"', obj)
        hl = re.search(r'highlight:\s*"((?:[^"\\]|\\.)*)"', obj)
        if nm and hl:
            rows.append((nm.group(1), nm.group(2), hl.group(1), "index.html"))

    if pc is None:
        rep.fail("figures", "highlight check: pick-and-compare.html could not be read")
        return rows
    src = js_object_slice(pc, "CITIES")
    if not src:
        rep.fail("figures",
                 "highlight check: could not locate CITIES in pick-and-compare.html")
        return rows
    try:
        data = json.loads(src)
    except ValueError as exc:
        rep.fail("figures", f"highlight check: pick-and-compare.html CITIES is not "
                            f"valid JSON ({exc})")
        return rows
    for r in data:
        if r.get("highlight"):
            rows.append((r.get("city", ""), r.get("state", ""),
                         r["highlight"], "pick-and-compare.html"))
    return rows


def check_highlight_homes(rep, db, idx, local):
    """
    Home figures in `highlight` prose vs the DB Median Home, on both surfaces.

    See the HL_* block above for why the scope is anchored rather than "every dollar
    figure". FAIL, not WARN: unlike a superlative, this is decidable. The string
    either names the DB's number or it names a different one.
    """
    pc = fetch("pick-and-compare.html", local)
    rows = _highlight_rows(idx, pc, rep)
    if not rows:
        rep.fail("figures", "highlight check: no highlight strings found on either "
                            "surface; nothing was checked")
        return

    # Keyed on (City, ST) throughout. The database holds two Wilmingtons, and a
    # name-only key is how Wilmington NC's $418,000 ended up graded against
    # Wilmington DE's string on July 21.
    names = {r["city"] for r in db_cities(db)}

    for city, state, hl, surface in rows:
        row = db_get(db, city, state)
        if not row or row["home"] is None:
            continue                     # unknown city / malformed cell: other checks
        home = row["home"]
        others = [n for n in names if n != city]

        def cross_city(start, end):
            """Is this figure attached to some OTHER city's name?"""
            window = hl[max(0, start - 12):end]
            return any(re.search(r"\b" + re.escape(n) + r"\b", window) for n in others)

        for m in HL_HOME_FIG.finditer(hl):
            tok = next(g for g in m.groups() if g)
            if cross_city(m.start(), m.end()):
                continue
            val = _hl_money(tok)
            if val is None:
                continue                 # a range: the NRC pattern, deliberately ours
            if not _hl_agrees(tok, val, home):
                rep.fail("figures",
                         f"{surface} {city}, {state}: highlight states a home value "
                         f"{tok.strip()}, DB Median Home is ${round(home / 1000)}K")

        # "homes under $260K" is not a claim that the median IS $260K, so it is not
        # held to equality -- but it is still a factual claim, and Roanoke shipped
        # "median homes under $230K" against a DB $251,000. Check that the inequality
        # actually holds, which is the only reading under which the sentence is true.
        for m in HL_HOME_BOUND.finditer(hl):
            op = m.group(1).lower()
            tok = next(g for g in m.groups()[1:] if g)
            val = _hl_money(tok)
            if val is None or cross_city(m.start(), m.end()):
                continue
            below = op in ("under", "below", "less than")
            if (home >= val) if below else (home < val):
                rep.fail("figures",
                         f"{surface} {city}, {state}: highlight says homes {op} "
                         f"{tok.strip()}, DB Median Home is ${round(home / 1000)}K")


def check_highlight_surfaces(rep, idx, local):
    """
    The same highlight sentence, on both surfaces, byte for byte.

    Until 2026-07-23 this string lived in THREE places: index.html, pick-and-compare
    .html, and a `Highlight` column in the database. Nothing read the database copy,
    nothing compared any of them, and by the time anyone looked they disagreed on 65
    of 99 rows, 16 of 99, and 67 of 99 respectively. Two of the database rows quoted a
    home price that contradicted the `Median Home` cell in their own row.

    The column is gone. The two that remain both render, so neither can go, which
    makes them the thing to gate instead. This check is the reason "one record" is
    true rather than aspirational.

    It would also have caught the em-dash gap on the day it opened. The July 13 sweep
    converted index.html and missed pick-and-compare.html, and the two surfaces have
    disagreed on 65 rows ever since, in silence, because no check compared them.

    Byte-for-byte on purpose. "Near enough" is how a terminology sweep half-lands and
    one surface says median home while the other says typical home value.
    """
    pc = fetch("pick-and-compare.html", local)
    if pc is None:
        rep.fail("figures", "highlight surfaces: pick-and-compare.html not found")
        return

    ix = {}
    for m in re.finditer(r'name:\s*"((?:[^"\\]|\\.)*)",\s*state:\s*"([A-Z]{2})",'
                         r'(?:(?!name:\s*")[\s\S])*?highlight:\s*"((?:[^"\\]|\\.)*)"', idx):
        ix[(m.group(1), m.group(2))] = json.loads('"%s"' % m.group(3))

    m = re.search(r"const CITIES\s*=\s*(\[.*?\]);", pc, re.S)
    if not m:
        rep.fail("figures", "highlight surfaces: could not locate CITIES in "
                            "pick-and-compare.html")
        return
    try:
        cities = json.loads(m.group(1))
    except ValueError as exc:
        rep.fail("figures", f"highlight surfaces: CITIES did not parse as JSON ({exc})")
        return

    # An extractor that matches nothing reports a clean run forever.
    if not ix or not cities:
        rep.fail("figures",
                 f"highlight surfaces: read {len(ix)} highlights from index.html and "
                 f"{len(cities)} from pick-and-compare.html. One of the two shapes has "
                 f"changed and the comparison is scanning nothing.")
        return

    pcs = {(c.get("city"), c.get("state")): c.get("highlight", "") for c in cities}
    for key in sorted(set(ix) | set(pcs), key=lambda k: (k[1] or "", k[0] or "")):
        city, state = key
        if key not in ix:
            rep.fail("figures", f"{city}, {state}: on pick-and-compare.html but has no "
                                f"highlight in index.html")
        elif key not in pcs:
            rep.fail("figures", f"{city}, {state}: in index.html but has no highlight "
                                f"on pick-and-compare.html")
        elif ix[key] != pcs[key]:
            a, b = ix[key], pcs[key]
            i = next((n for n, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            rep.fail("figures",
                     f"{city}, {state}: highlight differs between surfaces. "
                     f"index.html: ...{a[max(0, i - 30):i + 40]!r}... "
                     f"pick-and-compare.html: ...{b[max(0, i - 30):i + 40]!r}...")


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


def check_pillar_links(rep, slug_to_city, local):
    """Every profile must link to the scouting-trip pillar, with the click hook.

    Added Aug 22 2026, immediately after the link itself, because a planted typo
    in the href passed the entire gate. Nothing else defends this link: it is
    not an affiliate link, not a canonical, not a sitemap entry, and tag balance
    sees a well-formed anchor either way. A dead href here silently restores the
    exact condition the routing session existed to fix.
    """
    href = "/visit-before-you-decide.html"

    if fetch("visit-before-you-decide.html", local) is None:
        rep.fail("pillar", "visit-before-you-decide.html does not exist, but the "
                           "profiles link to it")

    seen = 0
    for slug in sorted(slug_to_city):
        html = fetch(f"cities/{slug}/profile.html", local)
        if html is None:
            continue
        seen += 1

        # BATCH B, Aug 24 2026. The canonical site nav carries Plan a Visit, so
        # every profile that has the nav component now holds the pillar href
        # TWICE: once as site furniture in the header, once as the measured
        # in-content link. Those are different things and only the second one is
        # what this check is about, so the header nav comes out before counting.
        #
        # Counting them together would have forced one of two bad fixes: allow 2
        # and stop noticing a genuine duplicate in the body, or hang
        # data-rmh-pillar on the nav item and let a furniture click land in
        # pillar_click, which would inflate the conversion on every profile
        # against a denominator that never moved.
        body = re.sub(r'<nav class="header-nav">.*?</nav>', "", html,
                      flags=re.S | re.I)

        n = body.count(f'href="{href}"')
        if n == 0:
            rep.fail("pillar",
                     f"cities/{slug}/profile.html has no pillar link: expected "
                     f'href="{href}". The page is orphaned from this profile.')
            continue
        if n > 1:
            rep.fail("pillar",
                     f"cities/{slug}/profile.html carries {n} pillar links "
                     f"outside the header nav, expected 1")

        # The nav item must stay UNMEASURED, for the reason above.
        nav_m = re.search(r'<nav class="header-nav">.*?</nav>', html,
                          re.S | re.I)
        if nav_m and "data-rmh-pillar" in nav_m.group(0):
            rep.fail("pillar",
                     f"cities/{slug}/profile.html has data-rmh-pillar on the "
                     f"header-nav item. That is site furniture on every page, "
                     f"not a conversion; it would fire pillar_click on every "
                     f"menu click and inflate the metric")

        # The hook must be on the ANCHOR. Testing the whole file is not enough:
        # the analytics block contains the selector a[data-rmh-pillar], so a
        # file-wide substring test passes even with the attribute stripped off
        # the link. The Aug 22 harness caught exactly that in the first draft.
        # Against `body`, not `html`. The header nav's Plan a Visit item comes
        # first in source order, so searching the whole file would find the
        # unmeasured furniture link and report every nav-bearing profile as
        # missing its hook.
        tag = re.search(r'<a\s[^>]*href="' + re.escape(href) + r'"[^>]*>', body)
        if tag and 'data-rmh-pillar' not in tag.group(0):
            rep.fail("pillar",
                     f"cities/{slug}/profile.html links to the pillar but the "
                     f"anchor carries no data-rmh-pillar attribute, so "
                     f"pillar_click cannot fire and the link reads as measured "
                     f"when it is not")

    # The silent-no-op guard. A check that reads nothing must say so.
    if seen == 0:
        rep.fail("pillar", "no profile pages were readable: the pillar-link check "
                           "ran against 0 profiles and would have reported clean")
    elif seen != 51:
        rep.fail("pillar", f"the pillar-link check read {seen} profiles, expected 51")


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


# ------------------------------------------- profile stat card + FAQ figures
#
# check_profiles above reads exactly two things on a profile: the long-form monthly
# range, and the "Typical Home Value" stat card. That left three surfaces on every
# profile unread, and on 2026-07-28 a draft of this check found 44 wrong figures
# sitting behind a gate that read 0 failures, 0 warnings.
#
#   1. The ABBREVIATED monthly, "$4.5-5.6K/mo". RANGE_RE only knows "$4,500-$5,600",
#      so all 47 of these were unchecked. 35 were wrong. Carlsbad is the one to
#      remember: its stat-sub on the very next rendered line already read "Tier 5 -
#      $10,400 to $13,000 a month", so the card contradicted its own subtitle.
#   2. The two VARIABLE stat slots, which carry real dimension scores under about
#      twenty different labels. Pensacola's Budget Score tile read 8 against a D2 of 7.
#   3. HOME FIGURES IN PROSE. The stat card is the only place check_profiles looks, but
#      the same number is restated in the JSON-LD FAQ, in the body, and in the
#      method-callout at the head of Where to live. Eight disagreed with the DB.
#
# Scope is the whole difficulty, exactly as it was for the highlight strings. Three
# things below are dollar figures that are SUPPOSED to differ from Median Home:
# neighborhood card medians, cross-city comparisons, and figures that are not home
# values at all. The rules that kill all three are recorded next to the pattern they
# belong to rather than in one lump, because each was learned separately.

# A money token that can only END on a digit or on K/M. This is not cosmetic. A class
# ending [\d.,]+ matches "$314,000," including the sentence comma, which drags the
# same-clause guard a clause forward, and that is precisely how St. Louis's wrong
# $192,000 hid behind an unrelated later mention of "suburbs".
SC_MONEY = r"\$\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?"
SC_DASH = r"[\u2013\u2014-]"

# Range-aware on purpose, so a range is captured WHOLE and self-rejects in _hl_money()
# rather than being read as a claim of its low end.
SC_FIG = (r"(~?" + SC_MONEY +
          r"(?:\s*" + SC_DASH + r"\s*\$?\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?)?)")

SC_MOD = r"(?:citywide|city-proper|typical|median|average)"

# "citywide median" with no "home" is admitted because it is unambiguous. A BARE
# "median" is not, and never will be: the pros/cons carry "median bill $5,026".
SC_NOUN = (r"(?:" + SC_MOD + r"\s+)?(?:single-family\s+|starter\s+|entry-level\s+)?"
           r"home\s+(?:value|price|sale\s+price)s?"
           r"|" + SC_MOD + r"\s+(?:single-family\s+|starter\s+)?homes?"
           r"|citywide\s+median\b")

SC_BOUNDW = r"under|below|less\s+than|over|above|from|starting\s+at|upward\s+of"

# THE HEDGE SLOT. PROSCONS_HOME requires the noun and the figure to be adjacent, which
# matches pros/cons voice but not profile voice: "the typical home value in Columbus is
# around $251,000" puts 21 characters between them, and "in Salt Lake City is around"
# puts 28. Reusing the pros/cons matcher unchanged covered 13 of about 45 home figures
# and reported a near-clean surface. The slot is bounded rather than free: it crosses no
# sentence punctuation, no comma, no second "$", and no bound word. Excluding the comma
# is what makes it a clause and not a paragraph.
SC_HEDGE = r"(?:(?!\b(?:" + SC_BOUNDW + r")\b)[^.;!?$,]){0,45}?"

# "citywide" is itself an anchor, with or without the word "home" after it. The profile
# voice uses it both ways round: "the citywide $341K number" and "the $194K citywide
# figure". Admitted because on a city profile "citywide" modifies exactly one quantity.
SC_CITYWIDE_NOUN = r"citywide\s+(?:figure|number|median|price|home\s+value|typical\s+home\s+value)"

SC_HOME = re.compile(
    r"(?:" + SC_NOUN + r")" + SC_HEDGE + SC_FIG +
    r"|" + SC_FIG + r"\s+(?:citywide\s+)?(?:" + SC_NOUN + r")" +
    r"|\bcitywide\s+" + SC_FIG +
    r"|" + SC_FIG + r"\s+" + SC_CITYWIDE_NOUN, re.I)

# Two blocks on a profile are STRUCTURED rather than prose, and they carry an invariant
# worth more than any noun pattern: the FIRST money figure in a method-callout or a
# Neighborhood Reality Check is the citywide home figure, always, because both blocks
# exist to state that figure and then contrast it with neighborhood ranges. Verified
# across all 22 such blocks on 2026-07-28.
#
# This is why the rule is a REGION rule and not a noun rule. Three of those blocks were
# wrong, and not one of the three is reachable by any home-value noun: Tulsa's callout
# and NRC both open "the $194K figure", and Prescott's opens "the $585K figure". Tulsa
# had moved 14.9% in the ZHVI rebase and its NRC callout was still built on the old
# number. Loosening the noun far enough to catch "figure" in open prose would also catch
# every unrelated dollar amount on the page; bounding it to these two blocks does not.
SC_REGIONS = ("method-callout", "reality-check")
SC_ANY_MONEY = re.compile(
    r"~?\$\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?"
    r"(?:\s*" + SC_DASH + r"\s*\$?\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[KkMm])?)?")

# Stat slots 1 and 2 are fixed; 3 and 4 are chosen per city. A slot is a SCORE claim
# only when its value is literally "N/10". The same label carries free text elsewhere:
# "Healthcare: Barnes-Jewish", "Airport: 48 nonstops", "Outdoors: Blue Ridge". Keying on
# the label alone would fail all thirty of those.
SC_SLOT = re.compile(
    r'<div class="stat">\s*<div class="stat-label">\s*(.*?)\s*</div>\s*'
    r'<div class="stat-value">(.*?)</div>', re.S)
SC_SCORE = re.compile(r"^(\d{1,2})/10$")

SC_SLOT_DIMS = {
    "healthcare": "D3",
    "airport": "D1", "airport access": "D1", "air access": "D1",
    "budget": "D2", "budget score": "D2",
    "tax friendliness": "D5", "taxes": "D5", "tax": "D5",
    "walkability": "D6", "walkable": "D6",
    "outdoor": "D7", "outdoors": "D7", "the outdoors": "D7",
    "outdoor access": "D7", "outdoor recreation": "D7", "open space": "D7",
    "wellness": "D8", "active wellness": "D8",
    "safety": "D9",
    "community": "D10", "community & culture": "D10", "culture": "D10",
    "arts": "D10", "arts & culture": "D10",
}

# Labels that are facts about the city, not dimension scores. They are listed rather
# than merely absent so that the FAIL below reads as "this label is unmapped" and not
# as "someone forgot Founded". None of them carries an N/10 value today, and if one
# ever does that is a mislabelled score and should fail.
SC_SLOT_NOT_DB = {
    "founded", "elevation", "metro", "coastline", "weather", "state income tax",
    "population", "sunshine", "distance", "airport code",
}


def monthly_abbrev(monthly):
    """'$4,500-$5,600/mo' -> '$4.5-5.6K/mo'. One decimal, trailing .0 dropped.

    Not invented here. It is the convention the 12 correct cards already used on
    2026-07-28, read off the tree rather than chosen: $8,000 renders "$8", not "$8.0",
    and $10,400 renders "$10.4".
    """
    parts = re.findall(r"\$[\d,]+", monthly)
    if len(parts) != 2:
        return None
    out = []
    for tok in parts:
        n = int(tok.replace("$", "").replace(",", ""))
        out.append(("%.1f" % (n / 1000.0)).rstrip("0").rstrip("."))
    return "$%s\u2013%sK/mo" % (out[0], out[1])


def _sc_flat(fragment):
    """Rendered text of a fragment: tags out, entities resolved, whitespace gone.

    Entity handling is load-bearing, not tidiness. Four profiles write the range as
    `&ndash;` and Savannah's card is CORRECT; comparing raw bytes reports it as drift.
    """
    txt = html_unescape(re.sub(r"<[^>]*>", "", fragment))
    return re.sub(r"\s+", "", txt).replace("\u2014", "\u2013").replace("-", "\u2013")


def _sc_div_spans(page, cls):
    """(start, end) of every <div|aside class="cls"> block, bounded at its OWN closing tag.

    Same tag-depth walk as card_blocks(), and for the same reason: a lookahead to the
    next opening tag makes the last block in a section swallow everything after it.
    """
    # div OR aside: the Neighborhood Reality Check is an <aside>, and a div-only walk
    # skipped it silently, which put Tulsa's stale $194K back into the prose surface
    # instead of the region rule that is meant to own it.
    step = re.compile(r"</?(?:div|aside)\b", re.I)
    for m in re.finditer(r'<(?:div|aside) class="%s"' % re.escape(cls), page):
        depth, i = 0, m.start()
        while True:
            t = step.search(page, i)
            if not t:
                yield (m.start(), len(page))
                break
            depth += -1 if t.group(0).startswith("</") else 1
            i = t.end()
            if depth == 0:
                close = page.find(">", i)
                yield (m.start(), len(page) if close == -1 else close + 1)
                break


def _sc_cut(page, classes):
    """Return page with every block of the named classes removed."""
    spans = []
    for cls in classes:
        spans.extend(_sc_div_spans(page, cls))
    out, last = [], 0
    for a, b in sorted(spans):
        if a < last:
            continue                     # nested or overlapping; already dropped
        out.append(page[last:a])
        last = b
    out.append(page[last:])
    return "".join(out)


def _sc_jsonld(page):
    """Every FAQ answer and Article description string, decoded.

    The FAQ on a profile is JSON-LD only; there is no rendered FAQ section. A reader
    never sees these, but Google does, and on Columbus the JSON-LD monthly was RIGHT
    while the stat card two thousand lines below it was wrong.
    """
    out = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            page, re.S):
        for raw in re.findall(r'"(?:text|description)":\s*"((?:[^"\\]|\\.)*)"', block):
            try:
                out.append(json.loads('"%s"' % raw))
            except ValueError:
                out.append(raw)
    return " ".join(out)


def _sc_region_first(rep, city, state, cls, page, home):
    """In a structured callout block, the FIRST money figure IS the citywide claim."""
    for a, b in _sc_div_spans(page, cls):
        text = re.sub(r"\s+", " ", visible_text(page[a:b]))
        m = SC_ANY_MONEY.search(text)
        if not m:
            continue
        val = _hl_money(m.group(0))
        if val is None:
            continue                     # a range opens the block: not a citywide claim
        if not _hl_agrees(m.group(0), val, home):
            rep.fail("profiles",
                     f"{city}, {state}: {cls} opens on {m.group(0).strip()}, but the "
                     f"first figure in that block is the citywide home value and the "
                     f"DB Median Home is ${round(home / 1000):,}K")


def _sc_scan(rep, city, state, where, text, home, others):
    """Report every home figure in `text` that disagrees with `home`."""
    text = re.sub(r"\s+", " ", text)
    for pat in (SC_HOME,):
        for m in pat.finditer(text):
            tok = next(g for g in m.groups() if g)

            # THE OTHER-PLACE GUARD, bounded to the same clause AND to text BEFORE the
            # figure. Both bounds matter and in opposite directions. Unbounded forward,
            # it excuses real drift by finding an unrelated place name later in the
            # sentence. Unbounded backward across a comma, it stops seeing the figure as
            # ours at all: St. Augustine's "the citywide typical home value is around
            # $433,000 above Tampa's $400,000" and Fort Myers' "the median home runs
            # $310,000 against Naples' $585K" are BOTH our own correct figures, and a
            # looser guard would skip them and call the surface clean.
            ls = max([text.rfind(ch, 0, m.start()) for ch in ".;!?,"] + [-1])
            before = text[ls + 1:m.start()]
            if any(re.search(r"\b" + re.escape(o) + r"\b", before) for o in others):
                continue

            # THE OTHER-TIME GUARD, same window and same backward bound as the guard
            # above. A figure attributed to a PAST year is not a claim about today's
            # typical value: Bozeman's "The Bozeman of 2015 had typical home values
            # near $327,000" is correct and disagrees with Median Home by design.
            #
            # The CURRENT year must not excuse, or the commonest opener on this site
            # stops being read. Note the real profiles are protected twice over: in
            # "As of 2026, the typical home value is around $734,000" the year sits
            # behind a comma and is already outside the window, which is why this
            # guard survives a New Year rollover without unwatching 47 profiles.
            #
            # Bounded backward only, exactly like the place guard. "$327,000, back in
            # 2015" is NOT excused, so the house style is year-before-figure.
            # Known and accepted false negative: "Since 2015 the value has risen to
            # $999,000" is excused though it claims today. Reaching it needs tense
            # parsing, which fails in worse ways than this does.
            yrs = [int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", before)]
            if yrs and all(y < CURRENT_YEAR for y in yrs):
                continue

            val = _hl_money(tok)
            if val is None:
                continue                 # a range: neighborhood spread, deliberately ours
            if not _hl_agrees(tok, val, home):
                rep.fail("profiles",
                         f"{city}, {state}: {where} states a home value {tok.strip()}, "
                         f"DB Median Home is ${round(home / 1000):,}K")


def check_statcard_faq(rep, db, slug_to_city, local):
    """
    The three profile surfaces check_profiles does not read.

    Deliberately NOT covered, so that a later reader knows these are decisions and not
    oversights:
      * hood-card blocks. Their "Median home:" figures are NEIGHBORHOOD claims by
        construction. This is what keeps Bentonville's Bella Vista "~$300K" and Tampa's
        Water Street range out. It also removes a trap: Pittsburgh's Brookline card
        reads "around $246K" and would pass today only because it happens to equal the
        citywide figure.
      * stat values that are not N/10. Free text, no DB counterpart.
      * bound claims ("under $400K") and the long-form monthly, both already held by
        HOME_BOUND and RANGE_RE in check_profiles. Checking them twice reports one
        error twice.
      * money with no home-value anchor anywhere outside a method-callout. Loosening
        the noun to reach it is how "median bill $5,026" gets graded as a home price.
    """
    seen_profiles = 0
    seen_slots = 0
    names = {r["city"] for r in db_cities(db)}

    for slug, (city, state) in sorted(slug_to_city.items()):
        page = fetch(f"cities/{slug}/profile.html", local)
        if page is None:
            continue
        row = db_get(db, city, state)
        if not row:
            continue
        seen_profiles += 1

        slots = SC_SLOT.findall(page)
        if len(slots) < 3:
            rep.fail("profiles",
                     f"{city}, {state}: found {len(slots)} stat slots, expected 4. "
                     f"The stats-bar markup has changed and this profile is unchecked.")
            continue

        # ---- slot 2: the abbreviated monthly -------------------------------------
        want = monthly_abbrev(row["monthly"])
        got = _sc_flat(slots[1][1])
        label = _sc_flat(slots[1][0])
        if label.lower() not in ("monthlybudget", "monthlyest", "monthlycost"):
            rep.fail("profiles",
                     f"{city}, {state}: stat slot 2 is labelled {label!r}, not "
                     f"Monthly Budget. The abbreviated monthly is not where it is "
                     f"expected and is therefore unchecked.")
        elif want is None:
            rep.fail("profiles",
                     f"{city}, {state}: DB Monthly Est {row['monthly']!r} is not a "
                     f"two-figure range, so the stat card cannot be derived")
        elif got != want:
            rep.fail("profiles",
                     f"{city}, {state}: stat card monthly {got}, DB says {want} "
                     f"(Monthly Est {row['monthly']})")

        # ---- slots 3+: dimension scores ------------------------------------------
        for i, (raw_label, raw_value) in enumerate(slots[2:], start=3):
            value = _sc_flat(raw_value)
            key = html_unescape(re.sub(r"<[^>]*>", "", raw_label)).strip().lower()
            key = re.sub(r"\s+", " ", key.replace("&", "&"))
            hit = SC_SCORE.match(value)
            if not hit:
                continue                 # free text: a hospital name, a trail mileage
            seen_slots += 1
            dim = SC_SLOT_DIMS.get(key)
            if dim is None:
                rep.fail("profiles",
                         f"{city}, {state}: stat slot {i} shows a score {value} under "
                         f"the label {key!r}, which maps to no dimension. Add it to "
                         f"SC_SLOT_DIMS or the score is unwatched."
                         + (" This label is listed as a non-DB fact."
                            if key in SC_SLOT_NOT_DB else ""))
                continue
            shown = int(hit.group(1))
            if shown != row["scores"][dim]:
                rep.fail("profiles",
                         f"{city}, {state}: stat slot {i} {key!r} shows {shown}/10, "
                         f"DB {dim} is {row['scores'][dim]}")

        # ---- home figures in prose -----------------------------------------------
        if row["home"] is None:
            continue                     # malformed DB cell; check_db reports it
        others = [n for n in names if n != city]

        for cls in SC_REGIONS:
            _sc_region_first(rep, city, state, cls, page, row["home"])

        body = _sc_cut(page, ("hood-card",) + SC_REGIONS)
        _sc_scan(rep, city, state, "profile prose",
                 visible_text(body), row["home"], others)
        _sc_scan(rep, city, state, "JSON-LD",
                 _sc_jsonld(page), row["home"], others)

    # An extractor that matches nothing reports a clean run forever. This is the same
    # guard check_highlight_surfaces carries, and the reason tools/test_roster.py keeps
    # a zero-cards assertion: silence and success look identical from the outside.
    if seen_profiles == 0:
        rep.fail("profiles", "stat-card check: no profiles were read; nothing was checked")
    elif seen_slots == 0:
        rep.fail("profiles",
                 f"stat-card check: read {seen_profiles} profiles and found zero "
                 f"N/10 score slots. The stats-bar markup has changed.")


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


# Roster membership: WHICH cities belong on a page, not whether each card is correct.
#
# check_cards above asks two questions of every card: does the money match the DB, and
# is this marked "coming soon" while the profile is live. Both are per-card questions.
# Neither asks whether the card should be on the page at all.
#
# That gap shipped. On July 27 2026 the budget page was carrying Beaufort, Pensacola,
# Rio Rancho and Sioux Falls after all four left Budget Range 1 in the ZHVI rebase, and
# was missing San Antonio after it dropped in. Five cities wrong. The gate ran against
# that exact page and reported 0 failures, because every individual card was internally
# correct. The page was wrong about its own membership and nothing looked.
#
# Only pages whose roster is a DB PREDICATE belong here. The top-cities-for-* set is
# editorial tiering out of the scoring-analysis docs, not a predicate, so asserting it
# here would be asserting a guess. Those need a hardcoded expected roster instead, which
# is a separate job.
DB_ROSTERS = {
    "best-places-to-retire-on-a-budget.html": (
        "Budget Range 1", lambda row: row["range"] == 1),
}


def check_roster(rep, db, local):
    """Pages whose roster is a DB predicate: fail on extras AND on omissions."""
    for page, (label, predicate) in DB_ROSTERS.items():
        html = fetch(page, local)
        if html is None:
            rep.fail("cards", f"{page}: roster target matched no file. Renaming a page "
                              f"must not silently retire its roster check")
            continue

        on_page = []
        for block in card_blocks(html):
            nm = re.search(r'city-(?:name|featured-name)">([^<]+)', block)
            st = re.search(r'state-code">([^<]+)', block)
            if nm and st:
                on_page.append((nm.group(1).strip(), st.group(1).strip()))

        # The silent no-op. If the markup changes shape, this check finds nothing to
        # compare and would otherwise report a clean pass over an unread page.
        if not on_page:
            rep.fail("cards", f"{page}: no city cards found, so the {label} roster was "
                              f"never compared. The card markup has changed shape")
            continue

        dupes = {c for c in on_page if on_page.count(c) > 1}
        for city, st in sorted(dupes):
            rep.fail("cards", f"{page}: {city}, {st} appears on the page more than once")

        listed = set(on_page)
        expected = {(r["city"], r["state"]) for r in db_cities(db) if predicate(r)}

        for city, st in sorted(listed - expected):
            row = db_get(db, city, st)
            now = f", now Budget Range {row['range']}" if row else ", not in the DB"
            rep.fail("cards", f"{page}: {city}, {st} is on the page but is not in "
                              f"{label}{now}")
        for city, st in sorted(expected - listed):
            rep.fail("cards", f"{page}: {city}, {st} is in {label} but has no card "
                              f"on the page")


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


def meta_content(html):
    """
    Text that reaches readers through meta/og/twitter description attributes.

    visible_text() strips whole tags, so everything inside a `content="..."`
    attribute is invisible to it, and script_strings() only reads <script>. That
    left the description attributes unread by every text-scanning check on the
    site. Four hardcoded city counts lived there undetected, two of them also
    carrying a matchup count that was wrong by one.

    These strings are what Google, Facebook and every AI answer engine quote back
    as the page's summary, so a claim here reaches more readers than most body
    copy does.
    """
    out = []
    for tag in re.findall(r"<meta\b[^>]*>", html, re.I):
        if not re.search(r'(?:name|property)\s*=\s*"[^"]*(?:description|title)"',
                         tag, re.I):
            continue
        m = re.search(r'content\s*=\s*"([^"]*)"', tag, re.I)
        if m:
            out.append(html_unescape(m.group(1)))
    return " ... ".join(out)

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


# Every spelling that reaches a reader as an em dash. The check used to count the
# literal character and nothing else, so pick-and-compare.html -- which stores its
# strings as JSON, where an em dash is written as the six characters \u2014 -- read
# zero while 63 were live. Count the SHAPE, not one spelling of it.
EMDASH_RENDERINGS = [
    ("literal", re.compile("\u2014")),
    ("escaped \\u2014", re.compile(r"\\u2014")),
    ("&mdash;", re.compile(r"&mdash;")),
    ("&#8212;", re.compile(r"&#0*8212;")),
    ("&#x2014;", re.compile(r"&#[xX]0*2014;")),
]

# A bracket group with no whitespace inside it is a regex character class, not prose:
#
#     /[\u2013\u2014\-].*\$/        pick-and-compare.html, twice
#
# script_strings() pairs quotes naively, so the code around that line comes back as if
# it were a string literal. Counting escape forms without removing character classes
# first puts two permanent failures on code that is doing exactly the right thing, and
# a gate with permanent noise in it is a gate nobody reads.
RE_CHAR_CLASS = re.compile(r"\[[^\]\s]{0,40}\]")


def emdash_forms(surface):
    """Em-dash renderings in a surface, keyed by spelling. Character classes excluded."""
    surface = RE_CHAR_CLASS.sub(" ", surface)
    found = {}
    for name, pat in EMDASH_RENDERINGS:
        n = len(pat.findall(surface))
        if n:
            found[name] = n
    return found


# ---- prose scores -------------------------------------------------------

# A dimension named in prose, and the vocabulary each one is actually written
# with on these pages. Deliberately NARROW. "budget" excludes "budget tier",
# which is a 1-5 field and would collide with the 1-10 scale on every page.
PROSE_DIMS = (
    ("D1", r"airport(?: access)?"),
    ("D2", r"budget(?!\s+tier)|affordabilit(?:y|ies)|cost of living|(?<![\w$])cost"),
    ("D3", r"healthcare"),
    ("D4", r"climate resilience|disaster resilience"),
    ("D5", r"tax(?:es|-friendliness| friendliness)?"),
    ("D6", r"walkabilit(?:y|ies)"),
    ("D7", r"outdoor recreation"),
    ("D8", r"active wellness|wellness(?: infrastructure)?"),
    ("D9", r"safety"),
    ("D10", r"community(?:[- ]and[- ]culture)?"),
)

_SEP = r"(?:to|against|vs\.?|versus)"
_CITY = r"(?:[A-Z][\w.]*(?:\s+[A-Z][\w.]*){0,2}(?:'s|')\s*)?"
_NUM = r"(\d{1,2})(?:\s*of\s*10)?"

# Three shapes, all of which bind the pair TIGHTLY to the dimension word. An
# earlier cut used a proximity window instead and flagged 219 claims on 20 pages,
# nearly all of them the neighbouring dimension in a list like "taxes (8 of 10
# vs. 5), healthcare (8 vs. 7), outdoor recreation (9 of 10 vs. 7)". Adjacency is
# what makes this check usable; a window is not.
PROSE_SHAPES = (
    r"{k}\s*(?:dimension\s+)?(?:scores?|scoring)\s+(?:of\s+)?" + _NUM
    + r"\s*" + _SEP + r"\s*" + _CITY + _NUM,
    r"{k}\s*\(\s*(?:a\s+perfect\s+)?" + _NUM
    + r"\s*" + _SEP + r"\s*" + _CITY + _NUM + r"\s*[),]",
    r"{k}\s+at\s+" + _NUM + r"\s*" + _SEP + r"\s*" + _CITY + _NUM,
)


def check_comparison_prose_scores(rep, db, idx, slug_to_city, local):
    """
    A score restated in prose must match the table row it restates.

    ELEVEN live instances of this in four days, and D2 EVERY SINGLE TIME:

      sarasota-vs-tampa       "budget dimension scores 6 to Sarasota's 5"   (x3)
      knoxville-vs-chattanooga "budget scores 9 against 8"
      naples-vs-fort-myers    "7 vs. 3", "6 vs. 5", "7 against Naples' 3"   (x4)
      nashville-vs-memphis    "budget score of 7 against Nashville's 5"
      madison-vs-columbus     "budget score of 7 to Madison's 6"
      scottsdale-vs-tucson    "cost (8 of 10 vs. 3 of 10)"

    naples-vs-fort-myers managed to disagree with itself three different ways on
    one page. Every one of these sat above or below a table row that was correct,
    and check_comparison_scores read the row and passed, because a checked number
    restated in prose is an UNCHECKED number. The July 13 D2 rebuild edited table
    rows and nothing else, which is why the whole run is D2.

    The assertion is set equality, not ordered: {prose} == {table}. Ordered would
    additionally catch a swap ("Tucson 8 to Santa Fe 5" when it is Santa Fe that
    scores 8), but naming which city owns which number means resolving city names
    in free prose, and a check that is wrong occasionally is worse than one that
    is narrow. Set equality caught all eleven.

    Scope is the comparison pages, where a table exists to check prose against.
    Profiles have no such table; their scores are checked at the source.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pages = sorted(set(re.findall(
        r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)))
    if not pages:
        rep.fail("comparison",
                 "no comparison pages found on compare-retirement-cities.html; "
                 "check_comparison_prose_scores verified nothing.")
        return

    read = 0
    for page in pages:
        html = fetch(page, local)
        if not html:
            continue
        read += 1
        prose = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(
            r"<style.*?</style>", " ", html, flags=re.S)))

        for key, words in PROSE_DIMS:
            m = re.search(
                rf'<td class="metric">{key}(?![0-9])[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>',
                html, re.S)
            if not m:
                continue
            table = {int(m.group(1)), int(m.group(2))}

            for shape in PROSE_SHAPES:
                pat = shape.replace("{k}", "(?:" + words + ")")
                for pm in re.finditer(pat, prose, re.I):
                    said = {int(pm.group(1)), int(pm.group(2))}
                    if said != table:
                        quote = re.sub(r"\s+", " ", pm.group(0)).strip()
                        rep.fail("comparison",
                                 f"{page}: prose says \"{quote}\" but the "
                                 f"{key} row reads "
                                 f"{m.group(1)}/10 and {m.group(2)}/10. A score "
                                 f"restated in prose is not checked by the row "
                                 f"it restates.")

    if not read:
        rep.fail("comparison",
                 "check_comparison_prose_scores read zero comparison pages. It "
                 "verified nothing rather than finding nothing.")


# ---- data vintage -------------------------------------------------------

CAPTION_VINTAGE = re.compile(r"city database,\s*(\w+)\s+(\d{4})")
DATE_MODIFIED = re.compile(r'"dateModified"\s*:\s*"(\d{4})-(\d{2})-(\d{2})"')
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def check_comparison_vintage(rep, db, idx, slug_to_city, local):
    """
    A page's stated data vintage must not predate the database it was read from.

    COMPARISON-PAGE-STANDARD-v2 says to update the caption month "whenever scores
    are refreshed from a new DB version". That rule lived only as prose in a doc,
    and was missed BY HAND TWICE: on the Tier 3 cost-figure batch and again on
    Tier 2 batch A, where three pages shipped refreshed July figures still
    captioned June 2026, with dateModified values up to seven weeks stale.

    Every comparison page's cost rows are asserted against the CURRENT database by
    check_comparison_cost_rows, and that check passes. So every page's figures
    are, by construction, verified against DB_VERSION_DATE. A caption claiming an
    older vintage is therefore understating the data, and a stale dateModified
    tells Google the page is older than it is.

    Both surfaces are checked because they drift independently: the caption is
    visible copy and dateModified is schema, and Tier 2 batch A managed to leave
    one right and the other wrong on the same page.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pages = sorted(set(re.findall(
        r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub)))
    if not pages:
        rep.fail("comparison",
                 "no comparison pages found on compare-retirement-cities.html; "
                 "check_comparison_vintage verified nothing.")
        return

    floor = f"{DB_VERSION_DATE.year:04d}-{DB_VERSION_DATE.month:02d}"
    read = 0
    for page in pages:
        html = fetch(page, local)
        if not html:
            continue
        read += 1

        cap = CAPTION_VINTAGE.search(html)
        if not cap:
            rep.fail("comparison",
                     f"{page}: no \"Data: RetireMeHere city database, "
                     f"[Month Year]\" caption found. The standard requires one, "
                     f"and a missing caption reads as no vintage at all.")
        else:
            month, year = cap.group(1), int(cap.group(2))
            if month not in MONTHS:
                rep.fail("comparison",
                         f"{page}: caption vintage month \"{month}\" is not a "
                         f"month name.")
            elif f"{year:04d}-{MONTHS.index(month) + 1:02d}" < floor:
                rep.fail("comparison",
                         f"{page}: caption says the data is from {month} {year}, "
                         f"but its figures are checked against "
                         f"{os.path.basename(DEFAULT_DB)} "
                         f"({DB_VERSION_DATE.isoformat()}). Bump the caption "
                         f"month when figures are refreshed.")

        dm = DATE_MODIFIED.search(html)
        if not dm:
            rep.fail("comparison",
                     f"{page}: no schema dateModified found. "
                     f"COMPARISON-PAGE-STANDARD-v2 requires it on the Article "
                     f"node.")
        elif "-".join(dm.groups()) < DB_VERSION_DATE.isoformat():
            rep.fail("comparison",
                     f"{page}: dateModified {'-'.join(dm.groups())} predates "
                     f"{os.path.basename(DEFAULT_DB)} "
                     f"({DB_VERSION_DATE.isoformat()}), so the page claims to be "
                     f"older than the figures it carries.")

    if not read:
        rep.fail("comparison",
                 "check_comparison_vintage read zero comparison pages. It "
                 "verified nothing rather than finding nothing.")


def check_comparison_cta_reciprocity(rep, db, idx, slug_to_city, local):
    """
    A comparison page ships without any step that returns to the two profiles.

    Eight of the twenty live pages were built, indexed, listed in sitemap.xml and
    reachable from nowhere a reader actually starts. Every figure ON those pages
    sat under three separate checks the whole time. Nothing read the EDGE, so it
    accumulated for months, and the half-wired state is the one that hides best:
    nashville-vs-memphis was linked from Memphis and not from Nashville between
    July 30 and today, which reads as done from either end you happen to open.

    Two directions, asserted independently:

      1. every page the hub lists is linked from BOTH profiles it names. The two
         city slugs come out of the filename, which is why the -vs- convention is
         worth keeping literal.
      2. every comparison href on a profile points at a page that exists. That is
         the case a rename creates, it leaves a dead CTA on a live profile, and no
         other check on this gate would see it.

    The link form asserted is the absolute href every CTA on the site already
    uses. A relative href resolves fine for a reader and still fails here on
    purpose: one form site-wide is what makes the edge greppable at all. The
    leading boundary in the pattern is not decoration either. A bare substring
    test for href="/page" is satisfied by data-href="/page", so the check would
    pass on markup that links nothing.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pairs = sorted(set(re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)))

    if not pairs:
        rep.fail("comparison",
                 "no comparison pages found on compare-retirement-cities.html; "
                 "check_comparison_cta_reciprocity verified nothing.")
        return

    profiles = {}
    for slug in sorted(slug_to_city):
        html = fetch(f"cities/{slug}/profile.html", local)
        if html is not None:
            profiles[slug] = html

    if not profiles:
        rep.fail("comparison",
                 "no city profiles could be read; "
                 "check_comparison_cta_reciprocity verified nothing.")
        return

    def links(html, page):
        return re.search(r'(?<![-\w])href="/' + re.escape(page) + r'"', html)

    edges = 0
    for a_slug, b_slug in pairs:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        for slug in (a_slug, b_slug):
            if slug not in profiles:
                rep.fail("comparison",
                         f"{page} compares {slug}, and there is no published "
                         f"profile at cities/{slug}/profile.html to link back "
                         f"from. Either the page names a city that is not built "
                         f"or the profile is missing from PUBLISHED_PROFILES.")
                continue
            edges += 1
            if not links(profiles[slug], page):
                rep.fail("comparison",
                         f"cities/{slug}/profile.html carries no CTA to /{page}, "
                         f"the page that compares it. The reader who wants that "
                         f"matchup is standing on this profile and cannot get "
                         f"there.")

    if not edges:
        rep.fail("comparison",
                 "check_comparison_cta_reciprocity matched no profile and page "
                 "pairs; it verified nothing.")

    # Direction 2. Deduped first: the same page is linked from two profiles by
    # design, and in a bare run every one of these is an HTTP round trip.
    outbound = {}
    for slug in sorted(profiles):
        for href in re.findall(
                r'(?<![-\w])href="/([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)"',
                profiles[slug]):
            outbound.setdefault(href, []).append(slug)

    for href in sorted(outbound):
        if fetch(href, local) is None:
            for slug in outbound[href]:
                rep.fail("comparison",
                         f"cities/{slug}/profile.html links /{href}, which does "
                         f"not exist. A renamed or deleted comparison page "
                         f"leaves a dead CTA on a live profile.")


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

    THREE blind spots, all closed 2026-07-31, all found by hand rather than by
    this check, which is the reason the count survived here for six weeks after
    the July 13 sweep:

      1. THE HYPHEN. "100-city database" is the adjectival form and the old
         pattern only matched "100 cities". 23 live instances.
      2. THE PAGE SET. It read index.html, the profiles, and the comparison pages
         linked from the hub, which silently excluded the hub ITSELF,
         pick-and-compare.html and where-should-i-retire-quiz.html. Twelve of the
         23 were on exactly those three pages.
      3. THE META ATTRIBUTE. visible_text() strips whole tags, so
         `<meta name="description" content="... 100-city ...">` was invisible to
         both surfaces. Four of the 23 lived there, including two that were also
         wrong about the matchup count.

    The lesson worth keeping: this check was written, shipped, and passing while
    23 violations of the exact rule it enforces were live. A check that reads the
    wrong pages reports clean for the same reason a check that reads no pages
    does.
    """
    pat = re.compile(
        r"\b(?:9[0-9]|1[0-9]{2})\+?[- ](?:scored |ranked |US |U\.S\. )?cit(?:y|ies)\b",
        re.I)

    pages = {"index.html": idx}
    for slug in slug_to_city:
        h = fetch(f"cities/{slug}/profile.html", local)
        if h:
            pages[f"cities/{slug}/profile.html"] = h
    hub = fetch("compare-retirement-cities.html", local) or ""
    # The hub, the picker and the quiz are the three highest-traffic pages that
    # make this claim, and none of them was being read.
    standalone = ["compare-retirement-cities.html", "pick-and-compare.html",
                  "where-should-i-retire-quiz.html",
                  "where-can-i-afford-to-retire.html"]
    for page in sorted(set(re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", hub))
                       ) + standalone:
        h = fetch(page, local)
        if h:
            pages[page] = h

    if len(pages) < 2:
        rep.fail("counts",
                 "check_hardcoded_counts read fewer than two pages. It counted "
                 "nothing rather than finding nothing.")
        return

    for page, html in sorted(pages.items()):
        for surface in (visible_text(html), script_strings(html),
                        meta_content(html)):
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


def _comparison_row(rep, db, slug_to_city, page, slug):
    """
    Resolve one comparison-page slug to its City Database row, loudly.

    Until 2026-08-17 the two table checks below each built their own lookup from
    the lowercased city NAME with no state. Two defects, both silent:

      1. A state-suffixed slug never resolved. burlington-vs-portland-me was on
         the hub from the day it shipped and neither check had ever read it,
         because "Portland" keys to "portland" while the page says "portland-me".
         The page fell straight through `if not a or not b: continue`.
      2. Same-name cities collided. Wilmington DE and Wilmington NC both keyed
         to "wilmington" and the dict kept whichever row built last, so a future
         Wilmington page would have validated against the WRONG CITY's figures
         and passed.

    PUBLISHED_PROFILES is the one map that already knows slug -> (City, ST), and
    check_routing keeps it honest against the profile files and the sitemap.
    Resolve through it, keyed into the db by the (City, ST) tuple form, matching
    the pattern the rest of the toolchain uses. Every miss is a FAILURE: a page
    this function cannot resolve is a page the caller is not covering, and an
    uncovered page reported as clean is the defect both callers were shipped
    with.
    """
    if slug not in slug_to_city:
        rep.fail("comparison",
                 f"{page}: slug {slug!r} is not in PUBLISHED_PROFILES, so this "
                 f"page cannot be resolved to a city and its table is NOT being "
                 f"checked. An unresolvable slug is uncovered work, never a "
                 f"quiet skip.")
        return None
    city, state = slug_to_city[slug]
    row = db.get(f"{city}_{state}")
    if not row:
        rep.fail("comparison",
                 f"{page}: {city}, {state} (slug {slug!r}) has no City Database "
                 f"row, so its half of the table is unverifiable.")
        return None
    return row


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

    for a_slug, b_slug in pages:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        html = fetch(page, local)
        if not html:
            continue
        a = _comparison_row(rep, db, slug_to_city, page, a_slug)
        b = _comparison_row(rep, db, slug_to_city, page, b_slug)
        if not a or not b:
            continue    # _comparison_row already failed loudly
        for dim_key, dim_label in DIMS:
            # Match the D-NUMBER, not the DIMS label. The label is the database
            # column name and the page uses a reader-facing one: "D4 Resil." vs
            # "D4 Climate resilience & insurance", "D8 Wellness" vs "D8 Active
            # wellness", "D10 Comm." vs "D10 Community & culture". Prefix
            # matching on the label silently skipped those three on all twenty
            # pages from the day this check shipped. (?![0-9]) stops D1 from
            # swallowing D10.
            m = re.search(
                rf'<td class="metric">{dim_key}(?![0-9])[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>\s*'
                rf'<td class="value[^"]*">(\d{{1,2}})/10[^<]*</td>',
                html, re.S)
            if not m:
                # Never `continue` here. A row that cannot be found is the exact
                # failure this check was written after: reading nothing and
                # calling it clean.
                rep.fail("comparison",
                         f"{page}: no {dim_key} row found. The check cannot "
                         f"verify a dimension it cannot locate.")
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



# A checkmark is an EDITORIAL claim, not an arithmetic one. It says the gap is big
# enough for a retiree to plan around, not that one number is larger. Two points on
# a ten-point dimension is where that becomes true, and it is what most of the site
# was already doing: measured on 2026-07-31, twelve of twenty pages left every
# one-point gap unmarked, four marked them, three were internally inconsistent, and
# one (madison-vs-ann-arbor) had been edited the wrong way that morning.
#
# The rule is written in COMPARISON-PAGE-STANDARD-v2, under Table rules. Change it
# there first; this constant only enforces it.
CHECKMARK_MIN_GAP = 2


def check_comparison_checkmarks(rep, db, idx, slug_to_city, local):
    """
    Nothing read a checkmark until 2026-07-31, and two rules were in circulation.

    check_comparison_scores keeps the NUMBERS in these tables correct, and it has:
    all 200 dimension cells across the twenty pages agreed with the database on the
    day this check was written. What drifted was the layer on top of the numbers.
    Five pages never got the caption update that the other fifteen got, so they kept
    saying "ties are left unmarked" while the rest said "ties and near-ties", and
    their tables followed their own captions. A page can be arithmetically perfect
    and still tell the reader something the site does not mean.

    Scope is DIMENSION rows only, D1-D10, where a gap is a difference of scores on a
    shared 1-10 scale and higher is always better. Deliberately NOT the cost rows
    (dollar figures have no score gap; check_comparison_cost_rows owns those values)
    and NOT the climate rows, which keep the older context rule in the standard: a
    mark on heat 9 vs. 10 is allowed WITH an inline explanation, because readers
    genuinely feel that one. Both exclusions are stated in the standard, not
    invented here.

    Four things are asserted on every dimension row:

      1. a marked row has a gap of CHECKMARK_MIN_GAP or more
      2. a row with a gap that large is marked
      3. the mark sits on the HIGHER score, never the lower one
      4. shading and the literal tick character always travel together, on exactly
         one cell. The standard requires both because CSS-only checkmarks are
         invisible to scrapers and answer engines, and a cell carrying one without
         the other is half a mark.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pages = sorted(set(re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)))

    if not pages:
        # Same lesson as everywhere else in this file: reading nothing is a failure,
        # not a pass.
        rep.fail("comparison",
                 "no comparison pages found on compare-retirement-cities.html; "
                 "check_comparison_checkmarks verified nothing.")
        return

    for a_slug, b_slug in pages:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        html = fetch(page, local)
        if not html:
            continue

        seen = 0
        for dim_key, dim_label in DIMS:
            m = re.search(
                rf'<td class="metric">{dim_key}(?![0-9])[^<]*</td>\s*'
                rf'<td class="value([^"]*)">(\d{{1,2}})/10([^<]*)</td>\s*'
                rf'<td class="value([^"]*)">(\d{{1,2}})/10([^<]*)</td>',
                html, re.S)
            if not m:
                rep.fail("comparison",
                         f"{page}: no {dim_key} row found, so its checkmark was "
                         f"not verified.")
                continue
            seen += 1

            cells = ((a_slug, m.group(1), int(m.group(2)), m.group(3)),
                     (b_slug, m.group(4), int(m.group(5)), m.group(6)))
            gap = abs(cells[0][2] - cells[1][2])
            marked = []

            for who, cls, score, tail in cells:
                shaded = "winner" in cls
                ticked = "\u2713" in tail
                if shaded != ticked:
                    half = ("shaded but carries no tick character" if shaded
                            else "ticked but not shaded")
                    rep.fail("comparison",
                             f"{page}: {dim_key} {who} cell is {half}. The "
                             f"standard requires both: the shading is for the "
                             f"reader, the character is for the scrapers.")
                if shaded or ticked:
                    marked.append((who, score))

            if len(marked) == 2:
                rep.fail("comparison",
                         f"{page}: {dim_key} marks BOTH cities. A checkmark names "
                         f"one stronger city; two marks name none.")
                continue
            if not marked:
                if gap >= CHECKMARK_MIN_GAP:
                    hi = max(cells, key=lambda c: c[2])
                    rep.fail("comparison",
                             f"{page}: {dim_key} is {cells[0][2]} against "
                             f"{cells[1][2]}, a {gap}-point gap, and neither cell "
                             f"is marked. At {CHECKMARK_MIN_GAP} points or more "
                             f"the stronger city ({hi[0]}) takes the mark.")
                continue

            who, score = marked[0]
            other = cells[1][2] if who == cells[0][0] else cells[0][2]
            if gap < CHECKMARK_MIN_GAP:
                shape = "a tie" if gap == 0 else f"a {gap}-point gap"
                rep.fail("comparison",
                         f"{page}: {dim_key} marks {who} on {shape} "
                         f"({cells[0][2]} against {cells[1][2]}). Ties and "
                         f"single-point gaps are left unmarked as near-ties; "
                         f"the caption on this page says so.")
            elif score < other:
                rep.fail("comparison",
                         f"{page}: {dim_key} marks {who} at {score}/10 against "
                         f"{other}/10. The mark is on the WEAKER city.")

        if seen == 0:
            rep.fail("comparison",
                     f"{page}: not one D1-D10 row was readable. The checkmark "
                     f"check read zero rows here and would otherwise report clean.")


# Pages whose cost rows are known stale as of 2026-07-30, with their exact
# mismatch counts. A RATCHET, not an exemption: see check_comparison_cost_rows.
# Lower each number as batches land. Delete the entry at zero. Delete this dict
# when it is empty.
# EMPTIED 2026-07-31. The comparison cost-figure repair is complete: all twenty
# pages now agree with the database on every cost row, so there is nothing left
# to quarantine. check_comparison_cost_rows stays and is now a plain assertion
# rather than a ratchet, which is the point it was built to reach.
#
# What the ratchet was for, in case one is ever needed again: it let a known-bad
# figure stay published while the repair was staged over several batches, without
# letting a NEW bad figure in beside it. It failed in both directions, so a page
# leaving quarantine forced the constant down in the same commit and the number
# never drifted from reality.
COST_ROW_BASELINE = {}

# Two labels for the same row. The three-page variant says "(citywide)".
HOME_LABELS = ("Typical home value (citywide)", "Typical home value")
MONTHLY_LABEL = "Estimated retiree budget"
TIER_LABEL = "Budget tier (1 = least expensive)"


def _cost_row(html, label):
    """Both value cells of a metric row, checkmark and whitespace stripped."""
    m = re.search(
        r'<td class="metric">' + re.escape(label) + r"</td>\s*"
        r'<td class="value[^"]*">([^<]*)</td>\s*'
        r'<td class="value[^"]*">([^<]*)</td>',
        html, re.S)
    if not m:
        return None
    return [re.sub(r"\s*\u2713", "", v).strip() for v in m.groups()]


def _dashes(s):
    """En dash, em dash and hyphen are the same separator for comparison."""
    return re.sub(r"[\u2013\u2014-]", "-", s.replace(" ", ""))


def check_comparison_cost_rows(rep, db, idx, slug_to_city, local):
    """
    The money rows on comparison pages were read by nothing.

    On 2026-07-30 an audit of all twenty pages found 69 mismatches against the
    database. Every one was in Typical home value, Estimated retiree budget or
    Budget tier. NOT ONE was in D1-D10, because check_comparison_scores reads
    those. Fort Myers was showing $372,000 against a database figure of
    $310,000; San Antonio was a full budget tier out.

    That is the whole lesson: the rows under a check held across twenty pages,
    and the rows beside them drifted on eighteen. Coverage is not a property of
    a page, it is a property of each field on it.

    The baseline quarantines the known-bad pages so the gate can stay at 0/0
    while they are repaired in batches. It fails in BOTH directions. A count
    going up is new drift. A count going DOWN means a fix landed and the
    baseline is now lying about the state of the site, which is how a
    quarantine list quietly becomes a permanent exemption.
    """
    hub = fetch("compare-retirement-cities.html", local) or ""
    pages = sorted(set(re.findall(
        r"([a-z0-9-]+)-vs-([a-z0-9-]+)-retirement\.html", hub)))

    seen = set()
    for a_slug, b_slug in pages:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        html = fetch(page, local)
        if not html:
            continue
        seen.add(page)
        a = _comparison_row(rep, db, slug_to_city, page, a_slug)
        b = _comparison_row(rep, db, slug_to_city, page, b_slug)
        if not a or not b:
            continue    # _comparison_row already failed loudly

        found = []
        for labels in (HOME_LABELS, (MONTHLY_LABEL,), (TIER_LABEL,)):
            for lab in labels:
                r = _cost_row(html, lab)
                if r:
                    found.append((lab, r))
                    break

        if not found:
            rep.fail("comparison",
                     f"{page}: no cost rows found at all. Reading zero rows and "
                     f"reporting clean is the fault this check exists to stop.")
            continue

        bad = []
        for lab, cells in found:
            for who, shown, row in ((a_slug, cells[0], a), (b_slug, cells[1], b)):
                if lab in HOME_LABELS:
                    truth = row.get("home_raw", "")
                    if re.sub(r"[^$0-9,]", "", shown) != str(truth).strip():
                        bad.append(f"{who} typical home shows {shown!r}, "
                                   f"DB says {truth!r}")
                elif lab == MONTHLY_LABEL:
                    truth = str(row.get("monthly", "")).strip()
                    if _dashes(shown) != _dashes(truth):
                        bad.append(f"{who} retiree budget shows {shown!r}, "
                                   f"DB says {truth!r}")
                else:
                    truth = row.get("range")
                    digits = re.sub(r"[^0-9]", "", shown.split("of")[0])
                    if digits != str(truth):
                        bad.append(f"{who} budget tier shows {shown!r}, "
                                   f"DB says {truth} of 5")

        expected = COST_ROW_BASELINE.get(page, 0)
        if len(bad) > expected:
            for msg in bad:
                rep.fail("comparison", f"{page}: {msg}")
            if expected:
                rep.fail("comparison",
                         f"{page}: {len(bad)} cost mismatches against a baseline "
                         f"of {expected}. This page got WORSE.")
        elif len(bad) < expected:
            rep.fail("comparison",
                     f"{page}: {len(bad)} cost mismatches, baseline says "
                     f"{expected}. A fix landed. Lower COST_ROW_BASELINE to "
                     f"{len(bad)} in this same commit, or delete the entry if "
                     f"it is now 0. A stale baseline is an exemption.")

    for page in COST_ROW_BASELINE:
        if page not in seen:
            rep.fail("comparison",
                     f"COST_ROW_BASELINE names {page}, which the hub does not "
                     f"link. A renamed page must not retire its own coverage.")


def check_budget_labels(rep, db, idx):
    """
    The quiz budget question, which is the highest-leverage control on the site.

    On 2026-08-07 this rendered from a local BUDGET_LABELS array inside
    renderBudget() whose middle three entries were byte-identical strings. Three
    buttons a reader could not tell apart, each setting a different
    quizState.budget, each driving a different hard candidate filter. It sat live
    for an unknown length of time and the gate read 0 failures 0 warnings through
    every session, because nothing in the toolchain had ever read a quiz option
    label. That is the hole this check closes.

    Five assertions, all FAIL rather than warn:

      1. BUDGET_BANDS exists and parses. Not finding it is a FAILURE, never a
         quiet pass: zero matches is the silent-no-op shape this validator exists
         to refuse.
      2. Exactly five bands, numbered 1..5 in order, five DISTINCT labels.
      3. The numeric edges ascend, do not overlap, and leave no gap; the top band
         is open-ended.
      4. Each label's upper figure equals the NEXT band's `min`, not its own
         `max`. The labels are rounded to clean hundreds while the edges are
         exact, so they disagree by one dollar at every seam ON PURPOSE. Asserted
         this way the rounding is legal and a genuinely mis-set band still fails.
         Asserted the obvious way this fires on correct data, and a check that
         fires on its own correct input gets loosened rather than fixed.
      5. The boundaries are still where the DATABASE puts them, recomputed here
         at run time from Monthly Est. A check holding its own hardcoded copy of
         the five strings would be a fourth copy of the thing that broke, and it
         would pass forever while the database moved underneath it.

    Plus: no second copy. Each label string must appear exactly once in
    index.html, and the three retired identifiers must not come back. Two copies
    of the band set is the precise condition that produced the original defect,
    so a fix that permits a second copy has fixed nothing.

    On assertion 5, and it is a policy decision made executable. The bands are
    derived from the MIDPOINT of each range's Monthly Est span, not its low end.
    The low end is the cheapest month a city ever has, and the candidate filter
    already grants one range of deliberate stretch (budgetRange <= budget + 1),
    so low-end labels would stack a second undocumented stretch on the first. The
    boundary-versus-median test below FAILS on a low-end derivation, by design.
    If that policy is ever reversed the reversal has to be made here, deliberately
    and in writing, rather than by quietly editing five strings.

    The test is against the MEDIAN midpoint of each range rather than per-city
    containment. Five of ninety-nine cities straddle a boundary (Fayetteville,
    Knoxville, St. George, Charlottesville, Boulder all sit within $50 of one),
    because Budget Range is not a pure function of the midpoint. Per-city
    containment would therefore fail on correct data on day one. Medians move
    slowly and separate cleanly.
    """
    m = re.search(r"const BUDGET_BANDS = \[(.*?)\];", idx, re.S)
    if not m:
        rep.fail("engine",
                 "index.html: BUDGET_BANDS not found. The quiz budget question is "
                 "the primary conversion path and nothing else on this site reads "
                 "its labels. Finding nothing here is a failure, not a pass.")
        return

    bands = []
    for line in m.group(1).splitlines():
        e = re.search(r"range:\s*(\d+)\s*,\s*label:\s*'([^']*)'\s*,\s*"
                      r"min:\s*(\d+)\s*,\s*max:\s*(\d+|null)", line)
        if e:
            bands.append({"range": int(e.group(1)), "label": e.group(2),
                          "min": int(e.group(3)),
                          "max": None if e.group(4) == "null" else int(e.group(4))})

    if len(bands) != 5:
        rep.fail("engine",
                 f"index.html: BUDGET_BANDS parsed {len(bands)} bands, expected 5. "
                 f"Either a band is missing or an entry no longer matches the "
                 f"expected shape and is being skipped silently.")
        return

    # --- 2. numbering and distinctness -------------------------------------
    if [b["range"] for b in bands] != [1, 2, 3, 4, 5]:
        rep.fail("engine",
                 f"index.html: BUDGET_BANDS ranges are "
                 f"{[b['range'] for b in bands]}, expected 1 through 5 in order. "
                 f"quizState.budget indexes this array positionally.")

    labels = [b["label"] for b in bands]
    if len(set(labels)) != 5:
        dupes = sorted({l for l in labels if labels.count(l) > 1})
        rep.fail("engine",
                 f"index.html: BUDGET_BANDS has duplicate labels: "
                 f"{', '.join(repr(d) for d in dupes)}. Each button sets a "
                 f"different quizState.budget and returns a different result set, "
                 f"so identical labels ask the reader to choose blind. This is the "
                 f"exact defect of 2026-08-07.")

    # --- 3. edges ascend, contiguous, top open -----------------------------
    for i, b in enumerate(bands[:-1]):
        nxt = bands[i + 1]
        if b["max"] is None:
            rep.fail("engine",
                     f"index.html: BUDGET_BANDS range {b['range']} has an "
                     f"open-ended max but is not the last band.")
            continue
        if b["max"] < b["min"]:
            rep.fail("engine",
                     f"index.html: BUDGET_BANDS range {b['range']} has max "
                     f"{b['max']} below min {b['min']}.")
        if b["max"] + 1 != nxt["min"]:
            rep.fail("engine",
                     f"index.html: BUDGET_BANDS ranges {b['range']} and "
                     f"{nxt['range']} are not contiguous: max {b['max']} then min "
                     f"{nxt['min']}. A reader whose budget falls in the gap, or in "
                     f"the overlap, has no correct answer.")
    if bands[-1]["max"] is not None:
        rep.fail("engine",
                 "index.html: BUDGET_BANDS top band must be open-ended (max: null). "
                 "A capped top band silently excludes anyone above it.")

    # --- 4. labels agree with the edges, allowing the rounding convention ---
    def figures(s):
        return [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", s)]

    for i, b in enumerate(bands):
        f = figures(b["label"])
        if not f:
            rep.fail("engine",
                     f"index.html: BUDGET_BANDS range {b['range']} label "
                     f"{b['label']!r} carries no dollar figure.")
            continue
        if i == 0:
            if len(f) != 1 or f[0] != bands[1]["min"]:
                rep.fail("engine",
                         f"index.html: BUDGET_BANDS band 1 label {b['label']!r} "
                         f"should name {bands[1]['min']}, the floor of band 2.")
        elif i == len(bands) - 1:
            if len(f) != 1 or f[0] != b["min"]:
                rep.fail("engine",
                         f"index.html: BUDGET_BANDS band 5 label {b['label']!r} "
                         f"should name its own floor, {b['min']}.")
        else:
            if len(f) != 2:
                rep.fail("engine",
                         f"index.html: BUDGET_BANDS range {b['range']} label "
                         f"{b['label']!r} should name two figures.")
                continue
            if f[0] != b["min"]:
                rep.fail("engine",
                         f"index.html: BUDGET_BANDS range {b['range']} label opens "
                         f"at {f[0]} but the band opens at {b['min']}.")
            if f[1] != bands[i + 1]["min"]:
                rep.fail("engine",
                         f"index.html: BUDGET_BANDS range {b['range']} label closes "
                         f"at {f[1]}; it must name {bands[i + 1]['min']}, the floor "
                         f"of the next band. Labels round to clean hundreds while "
                         f"the edges stay exact, so the label names the next floor, "
                         f"not this band's max ({b['max']}).")

    # --- 5. the boundaries are still where the database puts them ----------
    mids = {}
    for row in db_cities(db):
        found = re.findall(r"[\d,]+", str(row.get("monthly", "")))
        if len(found) < 2:
            continue
        lo = int(found[0].replace(",", ""))
        hi = int(found[-1].replace(",", ""))
        mids.setdefault(int(row["range"]), []).append((lo + hi) / 2.0)

    if len(mids) != 5:
        rep.fail("engine",
                 f"index.html/database: Monthly Est midpoints resolved for "
                 f"{len(mids)} budget ranges, expected 5. The band check cannot "
                 f"run against the data and is not reporting clean.")
        return

    medians = {r: statistics.median(v) for r, v in mids.items()}
    for i in range(4):
        boundary = bands[i + 1]["min"]
        lower, upper = medians[i + 1], medians[i + 2]
        if not (lower < boundary < upper):
            rep.fail("engine",
                     f"index.html: the boundary at ${boundary:,} between quiz "
                     f"ranges {i + 1} and {i + 2} no longer sits between what the "
                     f"database says those cities cost. Median Monthly Est midpoint "
                     f"is ${lower:,.0f} for range {i + 1} and ${upper:,.0f} for "
                     f"range {i + 2}. Bands are derived from the MIDPOINT of each "
                     f"range, not its low end: the candidate filter already grants "
                     f"one range of stretch and low-end labels would stack a second "
                     f"on top. If that policy is being reversed, change it here.")

    # --- no second copy ----------------------------------------------------
    for dead in ("BUDGET_LABELS", "BUDGET_OPTIONS", "budgetLabels"):
        if dead in idx:
            rep.fail("engine",
                     f"index.html: `{dead}` is back. The band set lives once, as "
                     f"BUDGET_BANDS. Two copies is what produced the 2026-08-07 "
                     f"defect; one of them was never filled in past its first and "
                     f"last slots and nobody rendered the other.")

    if idx.count("const BUDGET_BANDS = [") != 1:
        rep.fail("engine",
                 f"index.html: found {idx.count('const BUDGET_BANDS = [')} "
                 f"BUDGET_BANDS declarations, expected exactly 1.")

    for b in bands:
        if idx.count(b["label"]) != 1:
            rep.fail("engine",
                     f"index.html: the label {b['label']!r} appears "
                     f"{idx.count(b['label'])} times. Each band string must exist "
                     f"exactly once; a second occurrence is a second copy of the "
                     f"band set by another name.")

    # --- both consumers actually read it -----------------------------------
    rb = re.search(r"function renderBudget\(container\)\s*\{(.*?)\n\}", idx, re.S)
    if not rb:
        rep.fail("engine", "index.html: renderBudget() not found.")
        return
    # Comments are stripped before the membership test. Without this, a `//` line
    # merely MENTIONING the constant satisfies the check while the code below it
    # builds the buttons from something else. The harness caught exactly that on
    # this check's first run, which is the argument for planted-error harnesses
    # in one sentence: the check was written to close a silent-pass hole and
    # shipped with a smaller one inside it.
    body = re.sub(r"//[^\n]*", "", rb.group(1))
    if "BUDGET_BANDS" not in body:
        rep.fail("engine",
                 "index.html: renderBudget() does not reference BUDGET_BANDS. The "
                 "quiz buttons are being built from something else, which is the "
                 "original defect returning under a new name.")


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
               "visit-before-you-decide.html", "where-can-i-afford-to-retire.html"]
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


JSONLD_BLOCK = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)


def check_js_parse(rep, local):
    """
    Every inline script on every page must parse as JavaScript.

    This check exists because on August 15, 2026 the quiz shipped dead: a
    sitewide CSS sweep matched blocks by braces, one match landed inside a
    JS function body, the injected declaration was a syntax error, the error
    killed the whole script, and the quiz engine lived in that script. Three
    layers of gating passed it, because check_tag_balance strips script
    bodies by design, check_jsonld reads only ld+json, and nothing parsed
    JavaScript. Now something does: node --check on every inline script,
    JSON-LD excluded.

    node is required, and its absence is a FAILURE, not a skip: a gate that
    silently stops verifying JS is the exact hole this check fills.
    """
    if not local:
        return
    import os as _os
    import re as _re
    import shutil as _shutil
    import subprocess as _sp
    import tempfile as _tf
    if not _shutil.which("node"):
        rep.fail("tags",
                 "check_js_parse needs node and node was not found, so no "
                 "JavaScript was verified. Install node or run the gate in "
                 "Codespaces; do not ship unverified scripts.")
        return
    scanned = 0
    for root, dirs, files in _os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = _os.path.join(root, fn)
            try:
                s = open(path, encoding="utf-8").read()
            except OSError:
                continue
            for m in _re.finditer(
                    r"<script(?![^>]*src)(?![^>]*ld\+json)[^>]*>(.*?)</script>",
                    s, _re.S):
                body = m.group(1)
                if not body.strip():
                    continue
                scanned += 1
                with _tf.NamedTemporaryFile("w", suffix=".js",
                                            delete=False) as f:
                    f.write(body)
                    p = f.name
                r = _sp.run(["node", "--check", p],
                            capture_output=True, text=True)
                _os.unlink(p)
                if r.returncode != 0:
                    first = (r.stderr.strip().splitlines() or ["?"])[0]
                    rep.fail("tags",
                             f"{path}: an inline script does not parse as "
                             f"JavaScript ({first}). One syntax error kills "
                             f"every function in the script, including the "
                             f"ones the page's buttons call.")
    if scanned < 50:
        rep.fail("tags",
                 f"check_js_parse parsed only {scanned} scripts. It verified "
                 f"nothing rather than finding nothing.")


def check_jsonld(rep, local):
    """
    Every JSON-LD block in the checkout must parse as JSON.

    Added 2026-08-14 after Search Console reported one Unparsable structured data
    issue: "Parsing error: Missing ',' or ']' in array declaration" on
    states-that-dont-tax-retirement-income.html. The FAQPage node inside @graph had
    lost its opening brace, so its "@type" and "mainEntity" keys sat loose in the
    array, and a spare "]" closed the hole further down. Browsers never read
    JSON-LD, so the page rendered perfectly and looked fine for three days. The
    cost is not cosmetic: Google drops an unparsable block whole, so the FAQ rich
    result never had a chance to appear.

    A whole-checkout glob, not a named target list, because the page this shipped
    on is not on any list a hand-maintained enumeration would have carried. A block
    that parses but is semantically wrong is out of scope; this catches the class
    Search Console calls critical, the block it cannot read at all.

    LOCAL MODE ONLY: the pre-deploy gate is the moment to catch it, and globbing
    the live site would cost one fetch per page.
    """
    if not local:
        return                           # see LOCAL MODE ONLY above

    root = pathlib.Path(local)
    seen = 0

    for path in sorted(root.rglob("*.html")):
        if any(part in (".git", "node_modules", "__pycache__") for part in path.parts):
            continue
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        for n, m in enumerate(JSONLD_BLOCK.finditer(body), 1):
            seen += 1
            try:
                json.loads(m.group(1))
            except ValueError as exc:
                rep.fail("tags",
                         f"{rel}: JSON-LD block {n} does not parse, {exc}. Google "
                         f"drops an unparsable block whole, so every rich result on "
                         f"the page is lost. Look for a missing brace, bracket or "
                         f"comma.")

    if seen == 0:
        rep.fail("tags",
                 "no JSON-LD blocks found anywhere in the checkout; nothing was "
                 "checked. Either the site has lost its structured data or this "
                 "check is looking in the wrong place.")


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
            "where-can-i-afford-to-retire.html",
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

    Then it happened a THIRD time, same family, different axis. The check counted one
    spelling of the character. pick-and-compare.html stores its city strings as JSON,
    where an em dash is the six characters \u2014, so 63 of them sat in the check's own
    target list and read zero, and 22 more sat in the JSON-LD of four profiles. Twice
    is a coincidence; three times is the check being written against a spelling instead
    of a shape. emdash_forms() counts every rendering: the literal character, \u2014,
    &mdash;, &#8212;, &#x2014;.

    Not converted, deliberately, and each exclusion is load-bearing:
      * em-dashes inside <style> and <script> code. visible_text() drops both.
      * the UI placeholder used when a value is missing (city.monthlyEst || '\u2014').
        script_strings() only returns literals of 25+ chars, so a placeholder short
        enough to BE a placeholder never reaches this check. That protection is what
        makes counting escape forms shippable at all -- a raw-text scan for \u2014
        fires on every placeholder in the file.
      * regex character classes that match em dashes on purpose. See RE_CHAR_CLASS.

    A target that matches no file is the fourth way this check can read zero, so a
    named target that does not resolve is a failure, not a skip.
    """
    named = [
        "best-places-to-retire-on-a-budget.html",
        "best-places-to-retire-in-florida.html",
        "best-places-to-retire-in-the-midwest.html",
        "best-places-to-retire-avoid-natural-disasters.html",
        "top-cities-for-active-retirees.html", "top-cities-for-arts-lovers.html",
        "top-cities-for-foodies.html", "top-cities-for-healthcare.html",
        "top-cities-for-hikers.html", "top-cities-for-lgbtq-retirees.html",
        "top-cities-for-sports-fans.html",
        "pick-and-compare.html", "compare-retirement-cities.html",
        # Added 2026-07-27. Neither page had ever been scanned. That is the
        # fourth axis of this same blind spot, and the only one that is not
        # about HOW the check reads: surface, spelling, unresolved target --
        # and now plain TARGET MEMBERSHIP. Each carried exactly one live em
        # dash on the day it was added.
        "privacy.html", "scouting-trip-workbook.html",
        # Added with the page itself, 2026-08-10.
        "where-can-i-afford-to-retire.html",
    ]
    if GUIDES_TOO:
        named += ["value-navigator.html", "active-frontier.html",
                  "wellness-blueprint.html", "globetrotter-guide.html",
                  "urban-walkabout.html"]

    derived = [f"cities/{s}/profile.html" for s in slug_to_city]
    derived += re.findall(r"([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)", sitemap)

    pages = {"index.html": idx}
    missing = []
    for page in sorted(set(named + derived)):
        html = fetch(page, local)
        if html is None:
            missing.append(page)
        else:
            pages[page] = html

    if missing:
        rep.fail("emdash",
                 f"{len(missing)} target(s) matched no file and were scanned for "
                 f"nothing: {', '.join(missing)}. A target list that has drifted off "
                 f"the filenames reports a clean run forever. Fix the path or drop "
                 f"the entry deliberately.")

    for page, html in sorted(pages.items()):
        for surface, where in ((visible_text(html), "rendered text"),
                               (script_strings(html), "script strings")):
            found = emdash_forms(surface)
            if not found:
                continue
            total = sum(found.values())
            spellings = ", ".join(f"{k} x{v}" for k, v in sorted(found.items()))
            note = ("" if where == "rendered text" else
                    " (these reach the reader through the cards, the modal, and "
                    "the JSON-LD that search results are built from)")
            rep.fail("emdash",
                     f"{page}: {total} em-dash(es) in {where} [{spellings}]{note}")


AFF_CSV = "docs/AFFILIATE-CODES.csv"

AFF_LINK = re.compile(
    r"https?://(?:www\.)?(expedia|hotels|vrbo)\.com/affiliate/([A-Za-z0-9]+)", re.I)

AFF_COL = {"expedia": "expedia_code", "vrbo": "vrbo_code"}

AFF_REQUIRED_COLS = ("city", "state", "slug", "expedia_code", "vrbo_code", "source")

# Codes that deliberately sit on a page that is not about one city. Declared BY
# VALUE rather than by exempting the page, so that a typo or an unrecorded code on
# that same page still fails.
#
# The Expedia entry is Bend, OR's code, doing duty as the generic code on
# visit-before-you-decide.html. It earns, but every generic-page Expedia click is
# booked to Bend's per-city reporting. Boarded Aug 22 2026: either get a non-city
# code from Partnerize or accept the attribution. Listed here so the gate reads the
# known state as clean, and so a SECOND city code on a generic page still fails.
#
# The CSV has no hotels column because exactly one Hotels.com link exists on the
# site. If a second appears, give hotels a column instead of growing this set.
# Codes that are deliberately NOT city-specific, for pages where the reader has
# not chosen a city. Every entry here silences a check that would otherwise fail,
# so an entry is a claim, and the claim is about a DESTINATION, not about a string.
#
# The only way to establish that a code is generic is to follow the link. Absence
# from AFFILIATE-CODES.csv proves nothing: it means the code belongs to no BUILT
# city, which is also true of a city code that was never written into the CSV.
# That is exactly how the previous vrbo entry earned its place here while pointing
# at Bend. Do not add an entry on a lookup miss. Click it, then add it.
#
# All three below generated Aug 22 2026 against non-city destinations and verified
# by following each link.
GENERIC_AFF_CODES = {
    ("expedia", "lDLnJER"),
    ("vrbo", "osjcVrF"),
    ("hotels", "LPNJzOw"),
}

# Pages carrying a GENERATED copy of the code table, inlined so results can be linked
# at render time. A second copy of the codes is only tolerable because the check below
# compares it to the CSV on every run; without that this list is the drift.
AFF_MAP_PAGES = ("where-can-i-afford-to-retire.html", "pick-and-compare.html")

AFF_MAP_RE = re.compile(r"var RMH_AFF = (\{.*?\}); /\*END_RMH_AFF\*/", re.S)

# Remote mode cannot glob. The gate is --local, which reads from disk; this list is
# only for the post-deploy receipt.
AFF_REMOTE_PAGES = ("visit-before-you-decide.html",
                    "where-can-i-afford-to-retire.html",
                    "states-that-dont-tax-retirement-income.html",
                    "pick-and-compare.html",
                    "compare-retirement-cities.html")


def load_affiliate_table(rep, local):
    """
    docs/AFFILIATE-CODES.csv, the affiliate code table.

    Returns {(City, ST): row}, or None if the file cannot be trusted. None means
    STOP, not "nothing to check": every caller returns rather than iterating an
    empty dict, because a check that compares zero codes and reports clean is the
    exact failure this file exists to prevent.

    Keyed on city AND state. Wilmington DE and Wilmington NC are both in the
    database and carry genuinely different codes, so a name-only key silently
    collides them and books one city's commission to the other.
    """
    raw = fetch(AFF_CSV, local)
    if raw is None:
        rep.fail("affiliate",
                 f"{AFF_CSV} could not be read, so not one affiliate code on the "
                 f"site was checked against anything. If it moved, update AFF_CSV; "
                 f"if it was retired, delete this check deliberately.")
        return None

    rows = list(csv.DictReader(raw.lstrip("\ufeff").splitlines()))
    if not rows:
        rep.fail("affiliate",
                 f"{AFF_CSV} parsed to zero rows. The table is empty or its format "
                 f"changed, and every affiliate assertion below would have passed "
                 f"by checking nothing.")
        return None

    missing_cols = [c for c in AFF_REQUIRED_COLS if c not in (rows[0].keys() or {})]
    if missing_cols:
        rep.fail("affiliate",
                 f"{AFF_CSV} is missing column(s) {missing_cols}. Expected "
                 f"{list(AFF_REQUIRED_COLS)}.")
        return None

    table = {}
    seen_slug, seen_code = {}, {}
    for i, r in enumerate(rows, start=2):          # row 1 is the header
        r = {k: (v or "").strip() for k, v in r.items()}
        city, state, slug = r["city"], r["state"], r["slug"]

        if not city or not state:
            rep.fail("affiliate", f"{AFF_CSV} line {i}: blank city or state. "
                                  f"Every row must key on both.")
            continue

        key = (city, state)
        if key in table:
            rep.fail("affiliate", f"{AFF_CSV} line {i}: {city}, {state} appears "
                                  f"twice. One of the two rows is being ignored, "
                                  f"and nothing says which.")
            continue

        for brand, col in sorted(AFF_COL.items()):
            code = r[col]
            if not code:
                rep.fail("affiliate", f"{AFF_CSV} line {i}: {city}, {state} has no "
                                      f"{brand} code. A blank code is a link that "
                                      f"earns nothing.")
                continue
            owner = seen_code.get((brand, code))
            if owner and owner != key:
                rep.fail("affiliate",
                         f"{AFF_CSV}: {brand} code {code} is on both "
                         f"{owner[0]}, {owner[1]} and {city}, {state}. A shared "
                         f"code books one city's commission to the other and "
                         f"fails silently.")
            seen_code.setdefault((brand, code), key)

        if not slug:
            rep.fail("affiliate", f"{AFF_CSV} line {i}: {city}, {state} has no slug.")
        else:
            prior = seen_slug.get(slug)
            if prior:
                rep.fail("affiliate",
                         f"{AFF_CSV}: slug {slug!r} is on both {prior[0]}, "
                         f"{prior[1]} and {city}, {state}. Slugs address profile "
                         f"directories and must be unique.")
            seen_slug.setdefault(slug, key)

        table[key] = r

    return table


def check_affiliate(rep, db, slug_to_city, local):
    """
    Affiliate codes, anchored to docs/AFFILIATE-CODES.csv.

    HISTORY, because this docstring used to say the opposite. Until August 2026 the
    profiles WERE the record and there was deliberately no spreadsheet, on the
    argument that a separate list is a stale copy of data that lives in the HTML.
    That argument was sound while every affiliate link sat on a city profile. It
    stopped being sound when the tool pages needed codes at RENDER time, from cities
    that have no profile: 99 cities carry codes, only 51 have a profile, so the
    profiles can no longer be the whole record. The CSV became the record on Aug 21.
    The stale-copy objection was never wrong, it was simply answered a different way:
    by this check, which ties every code on every page back to the table on every run.

    A duplicated code is still the dangerous failure. It does not error and it does
    not look broken. It just quietly sends a Savannah reader to Charleston's hotel
    page, and nobody catches that by eye.

    Four assertions, in order of how badly each one fails:

      1. TABLE INTEGRITY. Unique slugs, unique codes per brand, both codes on every
         row, no duplicate city+state. Handled in load_affiliate_table above.
      2. ROSTER. Every database city has a row and every row is a database city. A
         city added to the database and not here has no code the day it gets a
         profile, and the profile check below is what would catch it, late.
      3. CITY SURFACES. Every code on cities/<slug>/profile.html equals that city's
         row. Both brands present, one code each.
      4. GENERIC SURFACES. A page that is not about one city may only carry a code
         named in GENERIC_AFF_CODES. Declared by value rather than by exempting the
         page, so a typo on that same page still fails.
    """
    table = load_affiliate_table(rep, local)
    if table is None:
        return

    # --- 2. roster, both directions -------------------------------------------
    db_keys = {(c["city"], c["state"]) for c in db_cities(db)}
    for key in sorted(db_keys - set(table)):
        rep.fail("affiliate",
                 f"{key[0]}, {key[1]} is in the database but has no row in "
                 f"{AFF_CSV}. It has no affiliate code, so it will earn nothing "
                 f"the day it gets a profile.")
    for key in sorted(set(table) - db_keys):
        rep.fail("affiliate",
                 f"{key[0]}, {key[1]} is in {AFF_CSV} but not in the database. "
                 f"Either the city was renamed and the table was not, or the "
                 f"state abbreviation is wrong.")

    # --- 3 and 4. every affiliate URL that ships ------------------------------
    pages = {}
    if local:
        root = pathlib.Path(local)
        for p in sorted(root.glob("*.html")) + sorted(root.glob("cities/*/profile.html")):
            rel = str(p.relative_to(root))
            html = fetch(rel, local)
            if html:
                pages[rel] = html
    else:
        for slug in slug_to_city:
            html = fetch(f"cities/{slug}/profile.html", local)
            if html:
                pages[f"cities/{slug}/profile.html"] = html
        for page in AFF_REMOTE_PAGES:
            html = fetch(page, local)
            if html:
                pages[page] = html

    if not pages:
        rep.fail("affiliate",
                 "no pages could be read, so no affiliate link on the site was "
                 "checked. This check reported clean without looking at anything.")
        return

    by_slug = {r["slug"]: k for k, r in table.items()}
    links_seen = 0

    for page, html in sorted(pages.items()):
        found = [(b.lower(), c) for b, c in AFF_LINK.findall(html)]
        links_seen += len(found)
        m = re.match(r"cities/([^/]+)/profile\.html$", page)

        if m:
            slug = m.group(1)
            key = by_slug.get(slug)
            if key is None:
                rep.fail("affiliate",
                         f"{page}: slug {slug!r} has no row in {AFF_CSV}, so its "
                         f"codes cannot be checked against anything.")
                continue
            row = table[key]
            per_brand = {}
            for brand, code in found:
                per_brand.setdefault(brand, set()).add(code)
            for brand, col in sorted(AFF_COL.items()):
                got = per_brand.get(brand, set())
                want = row[col]
                if not got:
                    rep.fail("affiliate", f"{page}: no {brand} affiliate link")
                elif got != {want}:
                    rep.fail("affiliate",
                             f"{page}: {brand} code {sorted(got)} does not match "
                             f"{AFF_CSV}, which says {want} for {key[0]}, {key[1]}.")
            for brand in sorted(set(per_brand) - set(AFF_COL)):
                for code in sorted(per_brand[brand]):
                    if (brand, code) not in GENERIC_AFF_CODES:
                        rep.fail("affiliate",
                                 f"{page}: {brand} code {code} is not in "
                                 f"{AFF_CSV} and is not a declared generic code.")
        else:
            for brand, code in found:
                if (brand, code) in GENERIC_AFF_CODES:
                    continue
                owner = None
                for k, r in table.items():
                    col = AFF_COL.get(brand)
                    if col and r[col] == code:
                        owner = k
                        break
                if owner:
                    rep.fail("affiliate",
                             f"{page} is not a city page but carries {owner[0]}'s "
                             f"{brand} code {code}. Every click here is booked to "
                             f"{owner[0]}, {owner[1]}. Either declare it in "
                             f"GENERIC_AFF_CODES deliberately or get a non-city "
                             f"code for this page.")
                else:
                    rep.fail("affiliate",
                             f"{page}: {brand} code {code} is in no row of "
                             f"{AFF_CSV} and is not a declared generic code. It is "
                             f"a typo, or a code nobody recorded.")

    # --- 5. the inlined code maps on the tool pages -------------------------
    for page in AFF_MAP_PAGES:
        html = pages.get(page) or fetch(page, local)
        if html is None:
            rep.fail("affiliate",
                     f"{page} could not be read, so its inlined code map was never "
                     f"compared to {AFF_CSV}.")
            continue
        m = AFF_MAP_RE.search(html)
        if not m:
            rep.fail("affiliate",
                     f"{page} carries no RMH_AFF map. Either the block was dropped, "
                     f"or its format changed and this check is now watching nothing.")
            continue
        try:
            inlined = json.loads(m.group(1))
        except ValueError as err:
            rep.fail("affiliate", f"{page}: RMH_AFF did not parse as JSON ({err}).")
            continue
        if not inlined:
            rep.fail("affiliate",
                     f"{page}: RMH_AFF parsed to zero cities. Every result on the "
                     f"page renders with no link, silently.")
            continue

        want = {f"{c}|{st}": [table[(c, st)]["expedia_code"],
                              table[(c, st)]["vrbo_code"]] for (c, st) in table}
        for key in sorted(set(want) - set(inlined)):
            rep.fail("affiliate",
                     f"{page}: {key.replace('|', ', ')} is in {AFF_CSV} but not in "
                     f"RMH_AFF, so that city renders with no affiliate link.")
        for key in sorted(set(inlined) - set(want)):
            rep.fail("affiliate",
                     f"{page}: RMH_AFF has {key.replace('|', ', ')}, which is in no "
                     f"row of {AFF_CSV}.")
        for key in sorted(set(want) & set(inlined)):
            if list(inlined[key]) != want[key]:
                rep.fail("affiliate",
                         f"{page}: RMH_AFF gives {key.replace('|', ', ')} "
                         f"{list(inlined[key])}, {AFF_CSV} says {want[key]}. The "
                         f"page is booking commission to the wrong code.")

    if links_seen == 0:
        rep.fail("affiliate",
                 f"{len(pages)} pages were read and not one affiliate link was "
                 f"found. The link format changed and this check is now watching "
                 f"nothing.")

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

    stamp = re.search(r"CityDatabase_([A-Za-z]{3})_(\d{1,2})_", db_name)
    if not stamp:
        rep.fail("docs",
                 f"cannot read a date out of {db_name}. DB_VERSION_DATE has "
                 f"nothing to check itself against, and every comparison page's "
                 f"data vintage is measured from it.")
    else:
        mon = ["jan", "feb", "mar", "apr", "may", "jun",
               "jul", "aug", "sep", "oct", "nov", "dec"].index(
                   stamp.group(1).lower()) + 1
        if (DB_VERSION_DATE.month, DB_VERSION_DATE.day) != (mon, int(stamp.group(2))):
            rep.fail("docs",
                     f"DB_VERSION_DATE disagrees with DEFAULT_DB: the constant "
                     f"says {DB_VERSION_DATE.isoformat()}, the filename says "
                     f"{stamp.group(1)} {stamp.group(2)}. Bump both together.")


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


# Enum vocabularies for the State Tax Facts sheet. Closed sets, deliberately:
# the sheet exists so a filter can run on these columns, and a filter cannot run
# on "mostly exempt" or "exempt over 65". Nuance goes in the Note column; the
# enum column carries one word a reader's yes-or-no question maps onto.
TAXFACTS_ENUMS = {
    "Income Tax Type": ("None", "Flat", "Graduated"),
    "SS Treatment": ("Exempt", "Partial", "Taxed"),
    "Retirement Income Treatment": ("Exempt", "Partial", "Taxed"),
    "Estate Tax": ("Yes", "No"),
    "Inheritance Tax": ("Yes", "No"),
}
TAXFACTS_NUMERIC = ("Top Rate %", "Sales Tax Combined %",
                    "PropTax Rate %", "Tax Year")


def check_taxfacts(rep, db_path):
    """
    The State Tax Facts sheet: one row per live state, no more, no less.

    D5 is a composite and cannot drive discrete filters (see
    docs/D5-TAX-METHODOLOGY.md), so the facts behind it live in their own sheet,
    keyed on ST. This check holds that sheet to three promises:

    1. COVERAGE, both ways. Every state with a city in the City Database has
       exactly one facts row, and no facts row names a state without a city.
       Strict in both directions on purpose: rows nothing reads are where this
       site's worst defects have hidden, so speculative rows are refused, and
       the row for a new state is forced into the same commit as its first city.
    2. ENUMS are closed and COMPLETE. Every fact column carries a listed
       value: blank stopped being legal when the population pass shipped
       (v19), because a blank cell in a filter column is a row the tool
       silently drops. Free text never passes for the same reason, and
       every row carries its Note and Source, so no enum is a claim with
       no reason written down.
    3. THE PROPTAX MIRROR. PropTax Rate % lives in both sheets because existing
       consumers read the City Database column. The facts sheet owns the value;
       this check fails the moment the two copies disagree, so the duplication
       can never drift silently.
    """
    try:
        rows = _read_xlsx(db_path, "State Tax Facts")
    except KeyError:
        rep.fail("db",
                 "the State Tax Facts sheet is missing from "
                 f"{os.path.basename(db_path)}. The tax-facts checks verified "
                 "nothing; the schema shipped with DB v18 and should not have "
                 "gone away.")
        return

    header = {i: str(v).replace("\n", " ").strip()
              for i, v in rows[1].items() if str(v).strip()}
    col = {name: i for i, name in header.items()}
    missing_cols = [c for c in ("ST", "PropTax Rate %",
                                "Retirement Income Note", "Source")
                    + tuple(TAXFACTS_ENUMS) + TAXFACTS_NUMERIC
                    if c not in col]
    if missing_cols:
        rep.fail("db",
                 f"State Tax Facts is missing columns {missing_cols}. "
                 f"The schema changed out from under this check.")
        return

    # Canonical per-state PropTax from the City Database sheet, and the state
    # roster the coverage promise is measured against.
    db_rows = _read_xlsx(db_path, "City Database")
    db_header = {i: str(v).replace("\n", " ").strip()
                 for i, v in db_rows[1].items() if str(v).strip()}
    db_col = {name: i for i, name in db_header.items()}
    db_ptax = {}
    for r in db_rows[2:]:
        if not str(r.get(db_col["City"], "")).strip():
            continue
        st = str(r.get(db_col["ST"], "")).strip()
        db_ptax[st] = r.get(db_col["PropTax Rate %"])

    facts_states = {}
    for r in rows[2:]:
        if not r:
            continue
        st = str(r.get(col["ST"], "")).strip()
        if not st:
            rep.fail("db", "State Tax Facts: a data row has a blank ST cell "
                           "but is not empty. Every row must be keyed.")
            continue
        if st in facts_states:
            rep.fail("db", f"duplicate State Tax Facts row for {st}")
        facts_states[st] = r

        for name, allowed in TAXFACTS_ENUMS.items():
            v = str(r.get(col[name], "")).strip()
            if not v:
                rep.fail("db",
                         f"State Tax Facts, {st}: {name} is blank. The "
                         f"population pass shipped in v19; a blank "
                         f"filter column is a row the tool silently "
                         f"drops.")
            elif v not in allowed:
                rep.fail("db",
                         f"State Tax Facts, {st}: {name} is {v!r}, which is "
                         f"not a recognized value. Allowed: "
                         f"{'/'.join(allowed)}. Nuance belongs in the "
                         f"Note column.")

        for name in TAXFACTS_NUMERIC:
            v = r.get(col[name])
            if v is None or str(v).strip() == "":
                rep.fail("db",
                         f"State Tax Facts, {st}: {name} is blank. The "
                         f"population pass shipped in v19 and every "
                         f"numeric column carries a figure.")
                continue
            try:
                float(v)
            except (TypeError, ValueError):
                rep.fail("db",
                         f"State Tax Facts, {st}: {name} is {v!r}, not a "
                         f"number. Scripts reading this column will silently "
                         f"skip it.")

        for name in ("Retirement Income Note", "Source"):
            v = str(r.get(col[name], "")).strip()
            if not v:
                rep.fail("db",
                         f"State Tax Facts, {st}: {name} is blank. "
                         f"Every row records its mechanism and its "
                         f"source; a bare enum is a claim with no "
                         f"reason written down.")

        ty = r.get(col["Tax Year"])
        try:
            if not (2025 <= int(float(ty)) <= CURRENT_YEAR):
                rep.fail("db",
                         f"State Tax Facts, {st}: Tax Year is {ty}, "
                         f"outside 2025..{CURRENT_YEAR}. A vintage "
                         f"from the future is a typo; one before "
                         f"2025 predates the sheet.")
        except (TypeError, ValueError):
            pass  # already failed as non-numeric above

        mirror = r.get(col["PropTax Rate %"])
        canon = db_ptax.get(st)
        if st in db_ptax:
            if mirror is None or str(mirror).strip() == "":
                rep.fail("db",
                         f"State Tax Facts, {st}: PropTax Rate % is blank but "
                         f"the City Database carries {canon}. The mirror is "
                         f"the one populated column and may not regress.")
            else:
                try:
                    drift = abs(float(mirror) - float(canon)) > 1e-9
                except (TypeError, ValueError):
                    drift = True
                if drift:
                    rep.fail("db",
                             f"State Tax Facts, {st}: PropTax Rate % is "
                             f"{mirror}, which disagrees with the City "
                             f"Database value {canon}. The facts sheet owns "
                             f"this figure; fix whichever copy is wrong and "
                             f"keep them identical.")

    if not facts_states:
        rep.fail("db",
                 "check_taxfacts read zero state rows from State Tax Facts. "
                 "It verified nothing rather than finding nothing.")
        return

    for st in sorted(set(db_ptax) - set(facts_states)):
        rep.fail("db",
                 f"{st} has a city in the database but has no row in State "
                 f"Tax Facts. The facts row for a new state ships in the same "
                 f"commit as its first city.")
    for st in sorted(set(facts_states) - set(db_ptax)):
        rep.fail("db",
                 f"State Tax Facts has a row for {st}, but {st} has no city "
                 f"in the database. Speculative rows are refused: a row "
                 f"nothing reads is where defects hide. Add it with the "
                 f"state's first city.")


# ---------------------------------------------------------------- main

# ------------------------------------------------------------------- harnesses
#
# The planted-error harnesses check the CHECKER. Each plants an error that really
# shipped, runs the relevant group against a throwaway copy, and asserts it is caught.
# House rule is that no check ships without one.
#
# They were run by hand or not at all, and on July 27 2026 the cost of that showed up:
# test_highlight_homes.py had been crashing on main since the ZHVI rebase, through a
# clean 0/0 gate, with eighteen assertions dead and nothing on screen saying so. A test
# suite nothing executes is not a test suite. So they are a check group now, and they
# gate the deploy like every other group.
# ---------------------------------------------------------------------------
# Hand-off shape
# ---------------------------------------------------------------------------
# Every other check in this file reads the CONTENT of a file whose path it already
# knows. That leaves one whole class of fault unwatched: a file with the wrong NAME,
# in the wrong PLACE, which no check has any reason to open.
#
# DEPLOY-CHEATSHEET.md section 4 says a build chat delivers a zip of new files already
# at their final repo paths, plus apply-<city>.py for edits to existing files. Between
# July 25 and July 28 2026 a build chat delivered the older shape three times running:
# loose `casper-profile.html` and `casper-hero.jpg` to be renamed by hand at deploy
# time. The gate read 0/0 each time and was right to, by its own lights.
#
# The ways that ships wrong are all quiet: three photos renamed by hand at 11pm with
# one missed, so the profile goes live with a broken image; the loose copy left at the
# root next to the correct one, so a stray `-PROFILE.html` sits live and unscanned,
# which is exactly how a scottsdale-vs-santa-fe stray carried four banned superlatives
# past check_superlatives; or a bundle zip committed because `rm` came after `git add`.
#
# LOCAL MODE ONLY. This asks what is ON DISK, and a bare run cannot list a directory
# over HTTP. It is skipped rather than faked in the post-deploy run.
STRAY_ROOT = re.compile(
    r"-(profile\.html|hero|detail|lifestyle)(\.(jpe?g|png|webp|html))?$", re.I)

# Every one of the 46 city folders held exactly these four files on July 28 2026.
# The uniformity is the point: anything else in there is debris from a rename.
CITY_FILES = {"profile.html", "hero.jpg", "detail.jpg", "lifestyle.jpg"}


SITE = "https://retiremehere.com"


def check_canonicals(rep, sitemap, local):
    """
    Every page in the sitemap must carry exactly one self-referencing canonical.

    This check exists because of what Search Console showed on August 9 2026. The
    site serves the same HTML at more than one URL in two separate ways, and only
    one of them was defended:

      1. Netlify serves foo.html at BOTH /foo and /foo.html. Eleven pages were
         indexed under both forms. That one was already survivable: every root
         page carried a canonical pointing at the .html form, so the duplicates
         stayed at a handful of impressions each.

      2. index.html carried NO canonical at all, and the site links to it as
         `index.html?city=NAME&state=ST` in 471 places across 98 distinct query
         strings, plus bare `index.html` 300 times and `/` 256 times. Every one
         of those is a separate indexable URL serving byte-identical homepage
         HTML. Two were already in the index (?city=Flagstaff, ?city=Sedona).

    The difference between (1) and (2) is only that somebody remembered the
    canonical on the landing pages and did not on the homepage. Nothing checked.
    So this check reads the page list from sitemap.xml rather than from a glob:
    the sitemap is the list of URLs we are asking Google to index, so a page that
    is in the sitemap and disagrees with itself about its own address is exactly
    the defect worth failing on, and a page missing from the sitemap is caught by
    check_routing already.

    Asserted, per sitemap entry:
      - the file is readable
      - it contains exactly one rel="canonical" (two is worse than none: it is
        undefined which one Google honours)
      - the canonical href equals the sitemap <loc> for that page, character for
        character, including the trailing-slash form of the homepage

    And, loudly, that the sitemap yielded a page list at all. A canonical check
    that parses zero <loc> elements and reports clean is the failure mode this
    codebase keeps rediscovering.
    """
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap)
    if not locs:
        rep.fail("canonicals", "sitemap.xml yielded no <loc> entries, so no page "
                               "was checked; the sitemap is unreadable or its "
                               "shape has changed")
        return

    checked = 0
    for loc in locs:
        if not loc.startswith(SITE):
            rep.fail("canonicals", f"sitemap entry {loc} is not on {SITE}")
            continue

        rest = loc[len(SITE):].lstrip("/")
        path = rest if rest else "index.html"

        html = fetch(path, local)
        if html is None:
            rep.fail("canonicals", f"{path} is in the sitemap but could not be read")
            continue

        found = re.findall(r'<link\s+rel="canonical"\s+href="([^"]*)"', html)
        if not found:
            rep.fail("canonicals",
                     f'{path} has no rel="canonical". It is reachable at more '
                     f"than one URL (Netlify serves /{rest} and /{rest}.html; "
                     f"index.html additionally answers every ?city= query string) "
                     f"and nothing tells Google which address is the real one")
            continue
        if len(found) > 1:
            rep.fail("canonicals",
                     f"{path} has {len(found)} canonical tags "
                     f"({', '.join(found)}); which one is honoured is undefined")
            continue
        if found[0] != loc:
            rep.fail("canonicals",
                     f"{path} canonical is {found[0]} but its sitemap entry is "
                     f"{loc}; the page and the sitemap disagree about its address")
            continue

        checked += 1

    if checked == 0:
        rep.fail("canonicals", f"{len(locs)} sitemap entries, none of them checked "
                               f"clean; the check read nothing it understood")



SITEMAP_STALE_TOLERANCE_DAYS = 1

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_sitemap_lastmod(rep, sitemap, local):
    """
    Every sitemap entry carries one well-formed <lastmod>, and it agrees with git.

    The August 23 2026 Search Console read found nine real pages parked in
    "Crawled - currently not indexed" with no page-level defect between them:
    inbound internal links 4 to 20 against an indexed median of 11, word counts
    2,321 to 2,711 against an indexed median of 2,558, non-boilerplate text
    share 92-93% against an indexed range of 90-95%, and every title and meta
    description on the site already unique. Philadelphia had 20 inbound links,
    2,711 words and 93% unique text and was not indexed; Lexington had the worst
    unique-text ratio on the site and was.

    What was wrong was the sitemap. All 51 profiles had been edited by the
    August 22 pillar-link batch, and the file still reported May 11 for
    Scottsdale, May 20 for Salt Lake City, May 21 for Philadelphia, June 11 for
    Delray Beach, June 12 for Pensacola, June 21 for Kansas City and June 23 for
    St. Paul. The newest date anywhere in it was August 18, on one URL, and
    cities/chattanooga/profile.html had no <lastmod> at all. Three of the pages
    Google had not revisited since June were among the ones whose dates said
    May. A crawler scheduling revisits off those dates has been told, in the one
    field built to say otherwise, that nothing has changed.

    Fixing 98 dates by hand today would have them rotten again by October, the
    same way the profile counts and the affiliate codes and the D2 budget
    figures each rotted once. So tools/build_sitemap.py derives them from git
    and this check refuses the commit when the two disagree.

    Asserted on every entry, in both modes:
      - exactly one <loc> and exactly one <lastmod> per <url> block
      - the date is ISO yyyy-mm-dd and is not in the future
      - the <loc> resolves to a file that can actually be read

    And, only under --local, where there is a git history to read:
      - no entry is more than a day older than that file's last commit, with
        uncommitted work counting as today because the gate runs before `git add`

    The freshness half is deliberately not attempted in the bare post-deploy
    run, which reads live GitHub while git would be answering about the working
    copy: two different trees, and an answer about the wrong one is worse than
    no answer. It says so on screen rather than skipping quietly, and under
    --local a tree with no .git is a FAILURE, never a skip. A check that reads
    nothing and reports clean is the exact defect this file keeps rediscovering.
    """
    blocks = re.findall(r"<url>(.*?)</url>", sitemap, re.S)
    if not blocks:
        rep.fail("sitemap", "sitemap.xml yielded no <url> blocks, so no date was "
                            "checked; the sitemap is unreadable or its shape has "
                            "changed")
        return

    today = date.today()
    entries = []          # [(rel, loc, lastmod)] for the ones that parsed
    for block in blocks:
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", block)
        if len(locs) != 1:
            rep.fail("sitemap", f"a <url> block has {len(locs)} <loc> elements; "
                                f"expected exactly one")
            continue
        loc = locs[0]

        if not loc.startswith(SITE):
            rep.fail("sitemap", f"sitemap entry {loc} is not on {SITE}")
            continue
        rest = loc[len(SITE):].lstrip("/")
        rel = rest if rest else "index.html"

        stamps = re.findall(r"<lastmod>\s*([^<]*?)\s*</lastmod>", block)
        # [^<]*? not [^<\s]*: a date with a space in it ("August 2026") is
        # MALFORMED, not absent, and the harness caught this check reporting
        # it as "0 <lastmod> elements" -- sending you to look for a tag that
        # is sitting right there.
        if len(stamps) != 1:
            rep.fail("sitemap",
                     f"{rel} has {len(stamps)} <lastmod> elements. Without exactly "
                     f"one, the crawler has no revisit signal for this page and "
                     f"tools/build_sitemap.py cannot round-trip the file")
            continue
        stamp = stamps[0]

        if not ISO_DATE.match(stamp):
            rep.fail("sitemap", f"{rel} has <lastmod>{stamp}</lastmod>, which is "
                                f"not an ISO yyyy-mm-dd date")
            continue
        try:
            when = date.fromisoformat(stamp)
        except ValueError:
            rep.fail("sitemap", f"{rel} has <lastmod>{stamp}</lastmod>, which is "
                                f"not a real calendar date")
            continue

        if when > today:
            rep.fail("sitemap", f"{rel} claims <lastmod>{stamp}</lastmod>, which is "
                                f"in the future; a date nobody can have edited on "
                                f"is not a freshness signal")
            continue

        if fetch(rel, local) is None:
            rep.fail("sitemap", f"{rel} is in the sitemap but could not be read")
            continue

        entries.append((rel, loc, when))

    if not entries:
        rep.fail("sitemap", f"{len(blocks)} sitemap entries, none of them checked "
                            f"clean; the check read nothing it understood")
        return

    if not local:
        print(f"  sitemap:  {len(entries)} <lastmod> dates well-formed. Freshness "
              f"vs git is a --local check only; the gate is --local .")
        return

    if not is_git_checkout(local):
        rep.fail("sitemap", f"{local} is not a git checkout, so no <lastmod> could "
                            f"be checked against anything. Run the gate on a real "
                            f"clone; an unzipped tarball cannot prove its own dates")
        return

    try:
        dates = effective_dates(local, today=today)
    except GitUnavailable as exc:
        rep.fail("sitemap", f"git history is unreadable ({exc}), so no <lastmod> "
                            f"could be checked")
        return

    for rel, loc, when in entries:
        actual = dates.get(rel)
        if actual is None:
            rep.fail("sitemap", f"{rel} is in the sitemap and on disk but git has "
                                f"never seen it, so its <lastmod> is unverifiable")
            continue
        real = date.fromisoformat(actual)
        stale = (real - when).days
        if stale > SITEMAP_STALE_TOLERANCE_DAYS:
            rep.fail("sitemap",
                     f"{rel} says <lastmod>{when.isoformat()}</lastmod> but last "
                     f"changed {actual}, {stale} days later. Run "
                     f"python3 tools/build_sitemap.py")



NAV_CANONICAL = "tools/nav_canonical.html"

# The 52 pages that do not carry the nav component at all: 51 city profiles plus
# visit-before-you-decide.html. They are not a nav variant, they are a different
# thing -- no .nav-dropdown CSS, no .nav-dropdown-item, no .nav-chev, no
# .header-quiz-btn, and no toggleTopCitiesDropdown JS anywhere on the page. Their
# entire header is three links that all go to the homepage.
#
# Fixing them means shipping a CSS block and a JS function to each file, and it
# visibly changes the top of every city profile, which is partner-reviewable
# work. So it is BATCH B, and this number is the debt, written down.
#
# The comparison is > not ==, on purpose. Lowering it is BATCH B doing its job
# and must not fail the gate. RAISING it means a 53rd page was built without the
# nav, which is the ninth variant appearing, which is the entire thing this
# check exists to stop.
NAV_STUB_EXPECTED = 51


def _nav_lines(nav):
    """Indentation-insensitive comparison key: stripped, non-blank lines."""
    return tuple(ln.strip() for ln in nav.splitlines() if ln.strip())


def _nav_targets(nav):
    """Every page the nav points at, normalised across href styles.

    index.html writes /top-cities-for-foodies.html where the rest write
    top-cities-for-foodies.html, and the homepage is variously "/", "index.html"
    and "/#screen-explore". Comparing raw hrefs would call those different navs
    when they are the same menu.
    """
    out = set()
    for href in re.findall(r'href="([^"]+)"', nav):
        base = href.lstrip("/").split("#")[0].split("?")[0]
        if not base or base == "index.html":
            continue
        out.add(base)
    return out


def check_nav_parity(rep, sitemap, local):
    """
    One nav, byte-for-byte, on every page that is not the homepage.

    Found August 23 2026 while scoping the orphan-page work. The site had EIGHT
    distinct navs across 100 pages. Not eight designs -- eight accidents: the nav
    was never a component, so each page froze whatever the menu looked like the
    day it was built, and each new tool page was added to whichever nav happened
    to be in front of whoever added it. where-can-i-afford-to-retire.html was in
    the menu on 2 pages out of 98. visit-before-you-decide.html was in it on 1.
    Every guide page was missing Compare Cities entirely.

    That is also an indexing problem and not only a navigation one. Internal
    links are how rank moves between pages, and nine real pages were sitting in
    "Crawled - currently not indexed" while the menu that should have been
    pointing at them pointed at eight different things.

    So: tools/nav_canonical.html is the nav, and every page carrying the
    component must match it exactly. Not "contains the right links" -- matches.
    A set-equality check would have passed all eight variants the moment their
    link lists converged, and the ninth would have arrived anyway.

    index.html is the one exemption, and it is a real one rather than a
    convenience. Its nav calls openCitySearch(), startQuiz() and
    showScreen('screen-explore'), functions that exist only on that page because
    it is the quiz app. Copy the canonical block onto it and every item dies;
    copy its block anywhere else and every item dies there instead. Two navs is
    forced by the architecture. What is NOT forced is their menus disagreeing,
    so index.html is held to the same set of destinations even though its markup
    differs.

    Asserted:
      - the canonical file exists and parses as a <nav> (no canonical, no check)
      - every component page's nav matches it line for line
      - index.html reaches exactly the same set of destinations
      - the count of pages with no component has not grown past NAV_STUB_EXPECTED
    """
    canon_raw = fetch(NAV_CANONICAL, local)
    if canon_raw is None:
        rep.fail("nav", f"{NAV_CANONICAL} is missing, so no nav was compared "
                        f"against anything")
        return
    m = re.search(r"<nav\b.*?</nav>", canon_raw, re.S | re.I)
    if not m:
        rep.fail("nav", f"{NAV_CANONICAL} contains no <nav> element, so no nav "
                        f"was compared against anything")
        return
    canon = m.group(0)
    canon_lines = _nav_lines(canon)
    canon_targets = _nav_targets(canon)
    if len(canon_targets) < 5:
        rep.fail("nav", f"{NAV_CANONICAL} points at only {len(canon_targets)} "
                        f"page(s); that is not a site nav and every page would "
                        f"pass against it")
        return

    # Page list from sitemap.xml, the same source check_canonicals uses. It is
    # also exactly right here: the 98 sitemap URLs are precisely the 98 pages
    # that carry a <nav>. The only two HTML files outside it, privacy.html and
    # scouting-trip-workbook.html, have no header at all.
    pages = []
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap):
        rest = loc[len(SITE):].lstrip("/") if loc.startswith(SITE) else ""
        pages.append(rest if rest else "index.html")
    pages = sorted(set(pages))
    if not pages:
        rep.fail("nav", "sitemap.xml yielded no pages, so no nav was checked")
        return

    checked = stubs = 0
    for page in pages:
        html = fetch(page, local)
        if html is None:
            continue
        found = re.search(r"<nav\b.*?</nav>", html, re.S | re.I)
        if not found:
            continue
        nav = found.group(0)

        if "nav-dropdown" not in nav:
            stubs += 1
            continue

        if page == "index.html":
            # Markup differs by necessity; the menu must not.
            missing = canon_targets - _nav_targets(nav)
            extra = _nav_targets(nav) - canon_targets
            if missing:
                rep.fail("nav", f"index.html nav is missing {sorted(missing)}, "
                                f"which the rest of the site links to")
            if extra:
                rep.fail("nav", f"index.html nav links to {sorted(extra)}, which "
                                f"no other page's nav does")
            checked += 1
            continue

        checked += 1
        got = _nav_lines(nav)
        if got == canon_lines:
            continue

        want = set(canon_lines)
        have = set(got)
        gone = [ln for ln in canon_lines if ln not in have]
        added = [ln for ln in got if ln not in want]
        if gone:
            rep.fail("nav", f"{page} nav is missing {len(gone)} canonical "
                            f"line(s), first: {gone[0][:88]!r}. Run "
                            f"tools/build_nav.py")
        if added:
            rep.fail("nav", f"{page} nav has {len(added)} line(s) not in "
                            f"{NAV_CANONICAL}, first: {added[0][:88]!r}. Run "
                            f"tools/build_nav.py")
        if not gone and not added:
            rep.fail("nav", f"{page} nav has the canonical lines in a different "
                            f"order. Run tools/build_nav.py")

    if checked == 0:
        rep.fail("nav", f"{len(pages)} pages scanned and not one nav was "
                        f"compared; the check read nothing")
        return

    if stubs > NAV_STUB_EXPECTED:
        rep.fail("nav", f"{stubs} pages carry a nav with no dropdown component, "
                        f"up from the {NAV_STUB_EXPECTED} on the board. A new "
                        f"page was built without the site nav; give it the block "
                        f"in {NAV_CANONICAL}")
    elif stubs < NAV_STUB_EXPECTED:
        print(f"  nav:      {checked} navs match {NAV_CANONICAL}. "
              f"{stubs} component-less pages remain, down from "
              f"{NAV_STUB_EXPECTED} -- lower NAV_STUB_EXPECTED to {stubs}")
    else:
        print(f"  nav:      {checked} navs match {NAV_CANONICAL}. "
              f"{stubs} component-less pages remain (BATCH B)")



CTA_MIN_RATIO = 4.5

# index.html builds its CTA as <button>, not <a>, so `.header-nav a` never
# applies to it and cta_contrast() correctly returns None. That is the ONLY page
# expected to be unresolvable. Anything else coming back None is a page whose
# colours could not be worked out, which is not the same as a page that passes,
# and is reported rather than skipped.
CTA_UNRESOLVED_EXPECTED = 1


def check_cta_contrast(rep, sitemap, local):
    """
    The Find My Match button must be readable, resting and on hover.

    Laurie reported on August 23 2026 that the CTA on visit-before-you-decide
    looked terracotta rather than cream and could not be read. It renders
    #5C5852 on #2A5E5A: a contrast ratio of 1.04:1, where WCAG AA wants 4.5:1.
    The button is an <a> inside .header-nav, so `.header-nav a { color: var(--mid) }`
    at specificity 0-1-1 outranks a bare `.header-quiz-btn { color: var(--white) }`
    at 0-1-0, and the nav-link colour wins.

    Forty-five other pages were fine, because each carries a hand-added rule
    whose own comment calls it "bulletproof" -- explicit hex, !important, every
    link state, a -webkit-text-fill-color fallback. One page never got it. Six
    more got the resting half and not the :hover half, so hovering paints
    var(--teal) text on a #3d7a75 background at 1.49:1.

    THIS CHECK IS ARITHMETIC BECAUSE I COULD NOT DO IT BY EYE. Asked how many
    pages were affected, I answered 46 twice, confidently, with a page list
    attached, and the true answer was one -- the single page Laurie had already
    named. The first attempt ignored !important. The second handled !important
    but matched selectors against four hard-coded strings, so it never saw the
    six-selector group that actually wins, and misattributed the win a second
    time. Four things interact here -- !important, selector groups, specificity,
    var() indirection -- and getting any one wrong flips the answer. So the
    cascade is resolved in code, in tools/css_cascade.py, under test.

    Asserted, per page, on both the resting and hover states:
      - the winning colour and background resolve to real values
      - their contrast ratio is at least 4.5:1

    A page whose CTA cannot be resolved is counted, not skipped, and the count
    is held at CTA_UNRESOLVED_EXPECTED. Silence about a page it could not read
    is how a check like this reports clean while the site is broken.
    """
    try:
        from css_cascade import cta_contrast
    except ImportError as exc:
        rep.fail("cta", f"tools/css_cascade.py could not be imported ({exc}), so "
                        f"no button contrast was checked")
        return

    pages = []
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap):
        rest = loc[len(SITE):].lstrip("/") if loc.startswith(SITE) else ""
        pages.append(rest if rest else "index.html")
    pages = sorted(set(pages))
    if not pages:
        rep.fail("cta", "sitemap.xml yielded no pages, so no button was checked")
        return

    checked = unresolved = 0
    no_cta = []
    for page in pages:
        html = fetch(page, local)
        if html is None:
            continue
        nav = re.search(r"<nav\b.*?</nav>", html, re.S | re.I)
        if not nav or "header-quiz-btn" not in nav.group(0):
            no_cta.append(page)
            continue

        page_ok = True
        for hover in (False, True):
            got = cta_contrast(html, hover=hover)
            state = "hover" if hover else "resting"
            if got is None:
                if page_ok:
                    unresolved += 1
                    page_ok = False
                continue
            ratio, fg, bg, sel = got
            if ratio < CTA_MIN_RATIO:
                rep.fail("cta", f"{page} Find My Match button is unreadable "
                                f"({state}): {fg} on {bg} is {ratio:.2f}:1, "
                                f"below {CTA_MIN_RATIO}:1. The winning rule is "
                                f"'{sel}'. Run python3 tools/fix_cta_css.py")
        if page_ok:
            checked += 1

    if checked == 0:
        rep.fail("cta", f"{len(pages)} pages scanned and not one button contrast "
                        f"was computed; the check read nothing")
        return

    if unresolved > CTA_UNRESOLVED_EXPECTED:
        rep.fail("cta", f"{unresolved} pages have a CTA whose colours could not be "
                        f"resolved, up from the {CTA_UNRESOLVED_EXPECTED} on the "
                        f"board. An unreadable page is not a passing page; check "
                        f"tools/css_cascade.py against the new markup")
    else:
        print(f"  cta:      {checked} buttons at or above {CTA_MIN_RATIO}:1 "
              f"resting and hover. {len(no_cta)} pages have no header CTA")


RETIRED_FONTS = ("Playfair", "Fraunces")
CANON_FONTS_LINK_FAMILIES = ("Libre+Franklin", "DM+Sans")


def check_typography(rep, local):
    """
    The August 2026 font sweep, held in place.

    System B is the site's type system: bold Libre Franklin display over DM
    Sans body, nothing else, no thin weights. This check exists because new
    pages are built by cloning existing ones, so a single stale template would
    quietly reintroduce the retired fonts on every page built from it. Three
    rules, each a gate failure:

      1. No page references Playfair Display or Fraunces, anywhere, including
         Google Fonts requests. They are retired, not discouraged.
      2. No font-weight 300. Thin type on the sand background was the site's
         biggest readability cost for a retiree audience; the sweep mapped
         display rules to 800 and body rules to 400.
      3. Every Google Fonts css2 request is the canonical two-family link.
         Eight variants existed before the sweep; one exists after.

    And the standing rule: this check counts what it scanned, and fewer than
    fifty pages is itself a failure, because a scan of nothing must never
    report clean.
    """
    if not local:
        return
    import os as _os
    import re as _re
    scanned = 0
    for root, dirs, files in _os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = _os.path.join(root, fn)
            try:
                s = open(path, encoding="utf-8").read()
            except OSError:
                continue
            scanned += 1
            if _re.search("font-family[^;{}]*(?:Playfair|Fraunces)"
                          "|Playfair\\+Display|family=Fraunces|Fraunces:ital", s):
                rep.fail("layout",
                         f"{path} loads or declares a retired font family "
                         f"(Playfair Display or Fraunces). "
                         f"If this page was cloned from an old template, "
                         f"re-clone from a current one; the type system is "
                         f"bold Libre Franklin over DM Sans, nothing else.")
            if _re.search(r"font-weight:\s*300", s):
                rep.fail("layout",
                         f"{path} carries a font-weight 300 rule. Thin weights "
                         f"are retired: display rules are 800, body rules 400.")
            for m in _re.finditer(r"https://fonts\.googleapis\.com/css2\?[^\"\']*", s):
                link = m.group(0)
                fams = _re.findall(r"family=([A-Za-z+]+)", link)
                bad = [f for f in fams if f not in CANON_FONTS_LINK_FAMILIES]
                if bad:
                    rep.fail("layout",
                             f"{path} requests non-canonical font families "
                             f"{bad} from Google Fonts. The canonical link "
                             f"loads Libre Franklin and DM Sans only.")
    if scanned < 50:
        rep.fail("layout",
                 f"check_typography scanned only {scanned} pages. It verified "
                 f"nothing rather than finding nothing.")


def check_stray_artifacts(rep, local):
    """Repo-root strays and city-folder debris: the wrong-shape hand-off, caught."""
    if not local:
        return                           # see LOCAL MODE ONLY above

    root = pathlib.Path(local)

    for p in sorted(root.iterdir()):
        if not p.is_file():
            continue
        name = p.name
        if name.lower().endswith(".zip"):
            rep.fail("layout",
                     f"{name}: a zip at the repo root. Delete it before `git add`, or "
                     f"it gets committed. See DEPLOY-CHEATSHEET.md section 4.")
        elif STRAY_ROOT.search(name):
            rep.fail("layout",
                     f"{name}: a build artifact at the repo root. Files ship at their "
                     f"FINAL paths and names (cities/<slug>/hero.jpg), never as "
                     f"<city>-hero.jpg to rename by hand. See DEPLOY-CHEATSHEET.md "
                     f"section 4.")

    cities = root / "cities"
    if not cities.is_dir():
        rep.fail("layout", "cities/ is missing entirely; nothing was checked")
        return

    slugs = [d for d in sorted(cities.iterdir()) if d.is_dir()]
    if not slugs:
        rep.fail("layout", "cities/ contains no city folders; nothing was checked")
        return

    for d in slugs:
        names = {f.name for f in d.iterdir()
                 if f.is_file() and not f.name.startswith(".")}
        for missing in sorted(CITY_FILES - names):
            rep.fail("layout",
                     f"cities/{d.name}/{missing} is missing. A profile without all "
                     f"three photos ships a broken image to a reader.")
        for extra in sorted(names - CITY_FILES):
            rep.fail("layout",
                     f"cities/{d.name}/{extra} is not one of the four expected files "
                     f"({', '.join(sorted(CITY_FILES))}). Rename debris, or a file "
                     f"that belongs somewhere else.")


HARNESSES = ("tools/test_afford_data.py",
             "tools/test_budget_labels.py",
             "tools/test_comparison_cost_rows.py",
             "tools/test_comparison_slugs.py",
             "tools/test_comparison_checkmarks.py",
             "tools/test_comparison_cta_reciprocity.py",
             "tools/test_comparison_prose_scores.py",
             "tools/test_comparison_vintage.py",
             "tools/test_hardcoded_counts.py",
             "tools/test_highlight_homes.py", "tools/test_emdash_forms.py",
             "tools/test_roster.py", "tools/test_stray_artifacts.py",
             "tools/test_statcard_faq.py",
             "tools/test_canonicals.py",
             "tools/test_taxfacts.py",
             "tools/test_taxtool.py",
             "tools/test_jsonld.py",
             "tools/test_typography.py",
             "tools/test_js_parse.py",
             "tools/test_affiliate.py",
             "tools/test_pillar_links.py",
             "tools/test_sitemap_lastmod.py",
             "tools/test_nav_parity.py",
             "tools/test_cta_contrast.py")

# Each harness runs THIS script on a staged copy, so the group would recurse without a
# stop. Two of them: the harnesses invoke --only figures / --only emdash, which already
# excludes this group, and the sentinel below survives someone widening that later.
HARNESS_ENV = "RMH_IN_HARNESS"

# "18/18 passed", with the backreference doing the work: a harness that ran zero
# assertions prints "0/0 passed" and exits 0, which is the silent-no-op failure these
# files exist to prevent, so it is rejected separately below.
HARNESS_SUMMARY = re.compile(r"\b(\d+)/\1 passed\b")


def check_harnesses(rep, local, quiet=False):
    """Run each planted-error harness. Non-zero exit, or a shapeless summary, fails."""
    if os.environ.get(HARNESS_ENV):
        return                           # we are inside a harness; do not recurse

    # The harnesses stage FILES ON THIS MACHINE either way: they are a self-test of the
    # validator's logic, not of the live site, so they run in both modes. In a bare run
    # `local` is None and the checkout is this file's grandparent.
    root = local or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ)
    env[HARNESS_ENV] = "1"

    for rel in HARNESSES:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            rep.fail("harness", f"{rel} is missing: the planted-error test for its "
                                f"check group is not running, and that check is now "
                                f"unwatched")
            continue

        proc = subprocess.run([sys.executable, path, "--repo", root],
                              capture_output=True, text=True, env=env)
        lines = (proc.stdout or "").strip().splitlines()
        summary = lines[-1].strip() if lines else "(no output)"

        if proc.returncode != 0:
            # Surface the individual assertions, not just the exit code. The whole
            # point is that this is readable on the gate without a second command.
            for ln in lines:
                if "[FAIL]" in ln:
                    rep.fail("harness", f"{rel}: {ln.strip()}")
            detail = (proc.stderr or "").strip().splitlines()
            rep.fail("harness", f"{rel}: exit {proc.returncode}, {summary}"
                                + (f" | {detail[-1]}" if detail else ""))
        elif not HARNESS_SUMMARY.search(summary):
            rep.fail("harness", f"{rel}: exit 0 but no N/N summary line; last line was "
                                f"{summary!r}. It ran nothing, or its shape changed.")
        elif not quiet:
            print(f"  harness:  {rel} {summary}")


def main():
    ap = argparse.ArgumentParser(description="Validate RetireMeHere against the City Database.")
    ap.add_argument("--db", default=DEFAULT_DB, help=f"database path (default: {DEFAULT_DB})")
    ap.add_argument("--local", help="validate a local checkout instead of live GitHub")
    ap.add_argument("--only", action="append",
                    choices=["figures", "profiles", "routing", "cards",
                             "superlatives", "emdash", "tags", "affiliate", "db",
                             "docs", "layout", "sitemap", "nav", "cta", "harness"],
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
        "tags", "affiliate", "db", "docs", "layout", "sitemap", "nav", "cta",
        "harness"}

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
        check_canonicals(rep, sitemap, args.local)
        check_pillar_links(rep, slug_to_city, args.local)

    if "figures" in groups:
        check_figures(rep, db, idx)
        check_afford_data(rep, args.db, args.local)
        check_taxtool_data(rep, args.db, args.local)
        check_tiers(rep, db, idx)
        check_highlight_homes(rep, db, idx, args.local)
        check_highlight_surfaces(rep, idx, args.local)
    if "profiles" in groups:
        if not slug_to_city:
            rep.fail("profiles", "no published profiles found; nothing was checked")
        check_profiles(rep, db, slug_to_city, args.local)
        check_statcard_faq(rep, db, slug_to_city, args.local)
    if "cards" in groups:
        check_cards(rep, db, idx, args.local)
        check_roster(rep, db, args.local)
    if "superlatives" in groups:
        check_superlatives(rep, db, idx, slug_to_city, args.local)
        check_budget_labels(rep, db, idx)
        check_dead_dimension_guards(rep, db, idx, slug_to_city, args.local)
        check_comparison_scores(rep, db, idx, slug_to_city, args.local)
        check_comparison_checkmarks(rep, db, idx, slug_to_city, args.local)
        check_comparison_cost_rows(rep, db, idx, slug_to_city, args.local)
        check_comparison_prose_scores(rep, db, idx, slug_to_city, args.local)
        check_comparison_vintage(rep, db, idx, slug_to_city, args.local)
        check_comparison_cta_reciprocity(rep, db, idx, slug_to_city, args.local)
        check_hardcoded_counts(rep, db, idx, slug_to_city, args.local)
        check_numeric_cells(rep, db, idx, slug_to_city, args.local)
    if "emdash" in groups:
        check_emdash(rep, idx, sitemap, slug_to_city, args.local)
    if "tags" in groups:
        check_tag_balance(rep, db, idx, sitemap, slug_to_city, args.local)
        check_jsonld(rep, args.local)
        check_js_parse(rep, args.local)
    if "affiliate" in groups:
        check_affiliate(rep, db, slug_to_city, args.local)
    if "db" in groups:
        check_db(rep, args.db)
        check_taxfacts(rep, args.db)
    if "docs" in groups:
        check_docs(rep, args.db, idx, sitemap, slug_to_city, args.local)
    if "layout" in groups:
        check_stray_artifacts(rep, args.local)
        check_typography(rep, args.local)
    if "sitemap" in groups:
        check_sitemap_lastmod(rep, sitemap, args.local)
    if "nav" in groups:
        check_nav_parity(rep, sitemap, args.local)
    if "cta" in groups:
        check_cta_contrast(rep, sitemap, args.local)
    # Last: it shells out once per harness and is the slowest group by a wide margin,
    # so everything cheap has already had its say by the time it starts.
    if "harness" in groups:
        check_harnesses(rep, args.local, args.quiet)

    return rep.render()


if __name__ == "__main__":
    sys.exit(main())
