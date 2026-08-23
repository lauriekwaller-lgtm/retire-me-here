#!/usr/bin/env python3
"""
Rewrite sitemap.xml so every <lastmod> comes from git instead of from memory.

    python3 tools/build_sitemap.py            # rewrite sitemap.xml in place
    python3 tools/build_sitemap.py --check    # report drift, write nothing
    python3 tools/build_sitemap.py --repo ..  # operate on another checkout

WHAT IT DOES NOT DO, deliberately: it does not decide which pages belong in the
sitemap. The <loc> list is read from the existing sitemap.xml and preserved
exactly. Adding a page is still an apply-script edit that inserts a <url> block,
the same as it has always been, and this script then fills in its date on the
next run.

That split is the whole point. A generator that globbed the disk would have
silently added privacy.html and scouting-trip-workbook.html on its first run,
both of which are out of the sitemap today, at least one of them on purpose.
Deciding page membership is an editorial judgment; deciding a date is not. Only
the second one is safe to automate, so only the second one is automated.

Also dropped on rewrite: <changefreq> and <priority>. Google has publicly
ignored both for years. They were 196 lines of hand-maintained fiction sitting
next to the hand-maintained dates that actually broke, and keeping them means
keeping something that can drift and cannot be checked.

Exit codes: 0 clean (or written), 1 drift found under --check, 2 setup problem.
"""

import argparse
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sitemap_dates import GitUnavailable, effective_dates   # noqa: E402

SITE = "https://retiremehere.com"
SITEMAP = "sitemap.xml"

HEADER = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
FOOTER = '</urlset>\n'


def loc_to_path(loc):
    """https://retiremehere.com/foo.html -> foo.html; the bare root -> index.html."""
    rest = loc[len(SITE):].lstrip("/") if loc.startswith(SITE) else None
    if rest is None:
        return None
    return rest if rest else "index.html"


def read_locs(root):
    path = os.path.join(root, SITEMAP)
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
    if not locs:
        raise SystemExit(f"{SITEMAP} yielded no <loc> entries; refusing to "
                         f"rewrite a file whose shape has changed")
    return locs


def render(rows):
    out = [HEADER]
    for loc, lastmod in rows:
        out.append(f"\n  <url>\n    <loc>{loc}</loc>\n"
                   f"    <lastmod>{lastmod}</lastmod>\n  </url>\n")
    out.append("\n" + FOOTER)
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--check", action="store_true",
                    help="report drift and exit 1; write nothing")
    args = ap.parse_args()
    root = os.path.abspath(args.repo)

    try:
        dates = effective_dates(root)
    except GitUnavailable as exc:
        print(f"Cannot derive dates: {exc}", file=sys.stderr)
        print("This script reads git history. Run it inside a real checkout, "
              "not an unzipped tarball.", file=sys.stderr)
        return 2

    locs = read_locs(root)
    today = date.today().isoformat()

    rows, missing, undated = [], [], []
    for loc in locs:
        rel = loc_to_path(loc)
        if rel is None:
            print(f"sitemap entry {loc} is not on {SITE}", file=sys.stderr)
            return 2
        if not os.path.exists(os.path.join(root, rel)):
            missing.append(rel)
            continue
        lastmod = dates.get(rel)
        if lastmod is None:
            # Present on disk, unknown to git: impossible unless status and log
            # disagree. Say so rather than stamping today and moving on.
            undated.append(rel)
            lastmod = today
        rows.append((loc, lastmod))

    if missing:
        print(f"{len(missing)} sitemap entries have no file on disk:", file=sys.stderr)
        for rel in missing:
            print(f"  {rel}", file=sys.stderr)
        return 2
    if undated:
        print(f"{len(undated)} files git has never seen (stamped today):", file=sys.stderr)
        for rel in undated:
            print(f"  {rel}", file=sys.stderr)

    new = render(rows)
    path = os.path.join(root, SITEMAP)
    with open(path, encoding="utf-8") as fh:
        old = fh.read()

    if args.check:
        if new == old:
            print(f"sitemap.xml is current: {len(rows)} URLs")
            return 0
        old_dates = dict(zip(
            re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", old),
            re.findall(r"<lastmod>\s*([^<\s]+)\s*</lastmod>", old)))
        drift = [(loc, old_dates.get(loc, "(none)"), lm)
                 for loc, lm in rows if old_dates.get(loc) != lm]
        print(f"sitemap.xml is stale: {len(drift)} of {len(rows)} URLs")
        for loc, was, now in drift:
            print(f"  {was:>10} -> {now}   {loc_to_path(loc)}")
        return 1

    if new == old:
        print(f"sitemap.xml already current: {len(rows)} URLs, nothing written")
        return 0

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new)
    print(f"sitemap.xml rewritten: {len(rows)} URLs, lastmod from git")
    return 0


if __name__ == "__main__":
    sys.exit(main())
