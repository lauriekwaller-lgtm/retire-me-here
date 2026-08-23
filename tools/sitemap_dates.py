#!/usr/bin/env python3
"""
One answer to "when did this file actually last change", shared by the sitemap
generator and the validator check that polices it.

This module exists because of the August 23 2026 Search Console read. Nine real
pages sat in "Crawled - currently not indexed", and every page-level explanation
failed: inbound internal links ran 4 to 20 against an indexed median of 11, word
counts ran 2,321 to 2,711 against an indexed median of 2,558, non-boilerplate
text share ran 92-93% against an indexed range of 90-95%, and all 51 profile
titles and meta descriptions were unique. The not-indexed pages sat in the
middle of the distribution on every measurable axis, which means there was no
page-level defect to fix.

What there WAS was a sitemap lying about seven of them. Every profile had been
edited on August 22 by the pillar-link batch, and before that by the June 23
formatting refresh and the August 17 canonical push. The sitemap still reported
May 11 for Scottsdale, May 20 for Salt Lake City, May 21 for Philadelphia, June
11 for Delray Beach, June 12 for Pensacola, June 21 for Kansas City and June 23
for St. Paul. The newest lastmod anywhere in the file was August 18, on a single
URL, and cities/chattanooga/profile.html carried no <lastmod> element at all.

Those dates were hand-maintained, one apply script at a time, and they rotted
exactly the way hand-maintained counts in this codebase always rot. A crawler
scheduling a revisit off a May date has no reason to come back, which is the
best available explanation for Scottsdale, Pensacola and Philadelphia not having
been recrawled since June.

So: nothing here is hand-maintained. The date comes from git, and the validator
fails when the sitemap disagrees with it.

Two callers, one definition, deliberately. An earlier draft duplicated this
logic into validate.py to keep that file self-contained, which is its house
style. That was rejected: a generator and its checker computing the same date
two different ways is a defect that reports clean.
"""

import os
import subprocess
from datetime import date

# The gate runs before `git add`, so a file edited by an apply script this
# session is real work that git has not been told about yet. Treating it as
# unchanged would make the generator write yesterday's date onto today's edit
# and the checker agree with it.
DIRTY_IS_TODAY = True


class GitUnavailable(RuntimeError):
    """Raised when the tree is not a git checkout, so no date can be derived."""


def _run(root, args):
    return subprocess.run(["git", "-C", root] + args,
                          capture_output=True, text=True)


def is_git_checkout(root):
    proc = _run(root, ["rev-parse", "--is-inside-work-tree"])
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def _last_commit_dates(root):
    """
    {relpath: 'YYYY-MM-DD'} for every path in history, in one pass.

    `git log` is newest-first, so the first date seen for a path is its most
    recent commit. Doing this per-file instead would be 98 subprocesses on a
    check that runs on every gate.
    """
    proc = _run(root, ["log", "--format=%x01%cs", "--name-only", "--no-renames"])
    if proc.returncode != 0:
        raise GitUnavailable(proc.stderr.strip() or "git log failed")

    dates = {}
    current = None
    for line in proc.stdout.splitlines():
        if line.startswith("\x01"):
            current = line[1:].strip()
        elif line.strip() and current and line not in dates:
            dates[line] = current
    return dates


def _dirty_paths(root):
    """Every path git considers modified, staged, or untracked."""
    proc = _run(root, ["status", "--porcelain", "--untracked-files=all"])
    if proc.returncode != 0:
        raise GitUnavailable(proc.stderr.strip() or "git status failed")

    dirty = set()
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        # "R  old -> new": the new name is the one on disk.
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        dirty.add(path.strip().strip('"'))
    return dirty


def effective_dates(root, today=None):
    """
    {relpath: 'YYYY-MM-DD'} -- when each tracked-or-present file last changed.

    Uncommitted work reads as today; everything else reads as its last commit.
    Raises GitUnavailable if `root` is not a git checkout, and never guesses:
    a sitemap date invented from a filesystem mtime would be the clone time on a
    fresh checkout, which is to say a fabricated freshness signal on every page
    at once.
    """
    if not is_git_checkout(root):
        raise GitUnavailable(f"{root} is not a git checkout")

    stamp = (today or date.today()).isoformat()
    dates = _last_commit_dates(root)
    if DIRTY_IS_TODAY:
        for path in _dirty_paths(root):
            dates[path] = stamp
    return dates


def effective_date(root, rel, dates=None, today=None):
    """One file's effective date, or None if git has never heard of it."""
    if dates is None:
        dates = effective_dates(root, today=today)
    return dates.get(rel.replace(os.sep, "/"))
