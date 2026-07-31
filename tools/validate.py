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
    harness      the planted-error tests in tools/, run against this checkout

Why this exists: every figure on this site is a string that either matches a DB cell
or does not. That is machine-checkable. Before this script existed, it was not being
checked, and drift accumulated silently across 100 cities and 80 pages.
"""

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request

from html import unescape as html_unescape

# Used only by the other-time guard in _sc_scan. Wall-clock rather than a constant so
# the guard does not need editing every January; see the comment there for why the
# rollover is safe on the current corpus.
from datetime import date

CURRENT_YEAR = date.today().year

RAW = "https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main"
# The database already lives in the repo, in docs/. That is the canonical copy the
# validator reads. Update this constant when you bump the version, in the same commit
# that adds the new xlsx.
DEFAULT_DB = "docs/CityDatabase_Jul_27_v17.xlsx"

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



# Pages whose cost rows are known stale as of 2026-07-30, with their exact
# mismatch counts. A RATCHET, not an exemption: see check_comparison_cost_rows.
# Lower each number as batches land. Delete the entry at zero. Delete this dict
# when it is empty.
COST_ROW_BASELINE = {
    "bloomington-vs-lexington-retirement.html": 3,
    "knoxville-vs-chattanooga-retirement.html": 4,
    "knoxville-vs-nashville-retirement.html": 4,
    "naples-vs-fort-myers-retirement.html": 4,
    "naples-vs-sarasota-retirement.html": 4,
    "nashville-vs-memphis-retirement.html": 4,
    "sarasota-vs-tampa-retirement.html": 4,
}

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

    by_slug = {}
    for key, row in db.items():
        if row is None or "_" not in key:
            continue
        name = str(row.get("city", ""))
        by_slug[name.lower().replace(" ", "-").replace(".", "")] = row

    seen = set()
    for a_slug, b_slug in pages:
        page = f"{a_slug}-vs-{b_slug}-retirement.html"
        html = fetch(page, local)
        if not html:
            continue
        seen.add(page)
        a, b = by_slug.get(a_slug), by_slug.get(b_slug)
        if not a or not b:
            continue

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


# Profile CTA links pointing at a comparison page whose cost rows are still
# quarantined. A RATCHET in both directions, riding on COST_ROW_BASELINE:
# see check_comparison_cta_cost_debt. When COST_ROW_BASELINE is deleted this
# constant is necessarily 0; delete the constant and the check with it.
CTA_COST_DEBT_BASELINE = 9

# Any anchor in a profile pointing at a comparison page, leading slash optional.
PROFILE_COMPARISON_HREF = re.compile(
    r'href="/?([a-z0-9-]+-vs-[a-z0-9-]+-retirement\.html)(?:[?#][^"]*)?"')


def check_comparison_cta_cost_debt(rep, db, idx, slug_to_city, local):
    """
    Do not send readers from a profile to a page with known-bad money on it.

    Two repairs are in flight at once and they pull against each other. The
    orphaned-CTA item wants CTA blocks added to roughly eleven profiles. The
    cost-row item has 69 stale figures quarantined in COST_ROW_BASELINE across
    eighteen pages. Doing the first while the second is open wires new traffic
    into pages the validator already knows are wrong, and neither item's own
    check can see that happening: COST_ROW_BASELINE only reads the comparison
    page, and no check reads the profile's outbound links at all.

    So this counts the EDGES between the two, not the pages. 11 today, down
    from 21 when it shipped, because Tier 3 retired eight pages. It fails
    in both directions, for the same reason COST_ROW_BASELINE does:

      - going UP is a new CTA pointed at known-bad figures, which is the thing
        to stop while the repair is in flight
      - going DOWN means a page left quarantine (or a CTA was removed) and the
        constant is now overstating the debt, which is how a ratchet quietly
        turns into a number nobody trusts

    Note the count falls on its own as batches land, because deleting a
    COST_ROW_BASELINE entry retires every edge into it. That is intended: the
    same commit that lowers one lowers the other.
    """
    if not COST_ROW_BASELINE:
        if CTA_COST_DEBT_BASELINE:
            rep.fail("comparison",
                     f"COST_ROW_BASELINE is empty but CTA_COST_DEBT_BASELINE is "
                     f"{CTA_COST_DEBT_BASELINE}. There is no debt left to count. "
                     f"Delete CTA_COST_DEBT_BASELINE and "
                     f"check_comparison_cta_cost_debt.")
        return

    read = 0
    edges = []
    for slug, (city, state) in sorted(slug_to_city.items()):
        html = fetch(f"cities/{slug}/profile.html", local)
        if html is None:
            continue
        read += 1
        for page in PROFILE_COMPARISON_HREF.findall(html):
            if page in COST_ROW_BASELINE:
                edges.append((slug, page))

    if not read:
        # The failure this codebase keeps rediscovering: iterate over nothing,
        # count zero, report clean. Zero edges and zero profiles read are the
        # same number and must not be the same result.
        rep.fail("comparison",
                 "check_comparison_cta_cost_debt read zero profiles. It counted "
                 "nothing rather than finding nothing.")
        return

    debt = len(edges)
    if debt == CTA_COST_DEBT_BASELINE:
        return

    listing = ", ".join(f"{s} -> {p.replace('-retirement.html', '')}"
                        for s, p in sorted(edges))
    if debt > CTA_COST_DEBT_BASELINE:
        rep.fail("comparison",
                 f"{debt} profile CTA links now point at comparison pages with "
                 f"quarantined cost rows, against a baseline of "
                 f"{CTA_COST_DEBT_BASELINE}. A CTA was wired to a page whose "
                 f"figures the validator already knows are stale. Fix the page's "
                 f"cost rows first, or hold the CTA. Current edges: {listing}")
    else:
        rep.fail("comparison",
                 f"{debt} profile CTA links point at quarantined comparison "
                 f"pages, baseline says {CTA_COST_DEBT_BASELINE}. Debt fell. "
                 f"Lower CTA_COST_DEBT_BASELINE to {debt} in this same commit. "
                 f"Current edges: {listing}")


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


HARNESSES = ("tools/test_comparison_cost_rows.py",
             "tools/test_comparison_cta_debt.py",
             "tools/test_highlight_homes.py", "tools/test_emdash_forms.py",
             "tools/test_roster.py", "tools/test_stray_artifacts.py",
             "tools/test_statcard_faq.py")

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
                             "docs", "layout", "harness"],
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
        "tags", "affiliate", "db", "docs", "layout", "harness"}

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
        check_dead_dimension_guards(rep, db, idx, slug_to_city, args.local)
        check_comparison_scores(rep, db, idx, slug_to_city, args.local)
        check_comparison_cost_rows(rep, db, idx, slug_to_city, args.local)
        check_comparison_cta_cost_debt(rep, db, idx, slug_to_city, args.local)
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
    if "layout" in groups:
        check_stray_artifacts(rep, args.local)
    # Last: it shells out once per harness and is the slowest group by a wide margin,
    # so everything cheap has already had its say by the time it starts.
    if "harness" in groups:
        check_harnesses(rep, args.local, args.quiet)

    return rep.render()


if __name__ == "__main__":
    sys.exit(main())
