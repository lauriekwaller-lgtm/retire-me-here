#!/usr/bin/env python3
"""
Work out what colour a header CTA actually renders, by resolving the cascade.

This module exists because I got the same question wrong three times by eye on
August 23 2026, and each wrong answer was confident and came with a page count
attached.

  Attempt 1: compared specificity of `.header-nav a` (0-1-1) against
             `.header-quiz-btn` (0-1-0), concluded the nav rule wins, reported
             46 broken pages. Ignored !important entirely.
  Attempt 2: added !important, but matched selectors against a hard-coded list
             of four exact strings. The rule that actually wins on 45 pages is a
             six-selector group introduced by two CSS comments. Never matched
             it, so the win was misattributed to `.header-nav a` again. Reported
             46 broken pages a second time.
  Truth:     one page. visit-before-you-decide.html, the one Laurie reported.

Four things have to be handled together or the answer is wrong, and each of them
is what broke one of those attempts:

  1. !important beats specificity, always
  2. selector GROUPS -- `a.x, a.x:link, button.x, .x { }` -- where the winning
     selector may be any member, so specificity is the max across matching ones
  3. comments inside and before a selector group, which is how the real rule is
     written and how attempt 2 failed to see it
  4. var(--name) indirection, since colours are declared once and referenced

So it is code with a test, not a judgment call made by reading CSS.

Deliberately NOT a general CSS engine. It answers one question -- what colour
and background land on the header CTA -- for the simple descendant/class/pseudo
selectors this site actually uses. Anything it cannot parse it reports as
unknown rather than guessing, because a wrong confident answer is the failure
mode this module was written in response to.
"""

import re

# The element under test: <a class="header-quiz-btn"> inside <nav class="header-nav">.
TARGET_CLASS = "header-quiz-btn"
TARGET_PARENT_CLASS = "header-nav"

COMMENT = re.compile(r"/\*.*?\*/", re.S)
RULE = re.compile(r"([^{}]+?)\s*\{([^}]*)\}", re.S)
STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,([^)]*))?\)")


def relative_luminance(hex_colour):
    h = hex_colour.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {hex_colour!r}")
    parts = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        parts.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = parts
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    a, b = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def stylesheet(html):
    """All <style> content joined. Inline style="" attributes are not cascade."""
    return "\n".join(STYLE.findall(html))


def resolve_var(css, value, depth=0):
    """var(--x) -> its declared value, following one level at a time."""
    if depth > 5:
        return None
    m = VAR.search(value)
    if not m:
        return value.strip()
    decl = re.search(re.escape(m.group(1)) + r"\s*:\s*([^;}]+)[;}]", css)
    if decl:
        sub = decl.group(1).strip()
    elif m.group(2):
        sub = m.group(2).strip()          # var(--x, fallback)
    else:
        return None                        # undefined, and no fallback
    return resolve_var(css, value.replace(m.group(0), sub), depth + 1)


def specificity(selector):
    """(classes+pseudo-classes, elements). Ids are unused in this stylesheet."""
    sel = re.sub(r"::[a-z-]+", "", selector)
    classes = len(re.findall(r"\.[\w-]+", sel)) + len(re.findall(r":[a-z-]+", sel))
    elements = len(re.findall(r"(?:^|[\s>+~])([a-z]+)(?![\w-]*[\(])", sel))
    return (classes, elements)


def _compound_matches(compound, classes, tag, allow_hover):
    """One compound selector (no combinators) against a simple element."""
    compound = compound.strip()
    if not compound:
        return False
    pseudos = re.findall(r":([a-z-]+)", compound)
    for p in pseudos:
        if p in ("hover", "focus", "focus-visible"):
            if not allow_hover:
                return False
        elif p not in ("link", "visited", "active"):
            return False
    bare = re.sub(r":[a-z-]+", "", compound)
    want_classes = set(re.findall(r"\.([\w-]+)", bare))
    want_tag = re.match(r"^([a-z]+)", bare)
    if want_tag and want_tag.group(1) != tag:
        return False
    return want_classes <= classes


def selector_matches(selector, allow_hover=False):
    """
    Does `selector` match the header CTA anchor?

    Modelled as: <a class="header-quiz-btn"> inside <nav class="header-nav">
    inside <header class="site-header">. Only descendant combinators are used
    on this site; a selector with > + or ~ is reported as unmatched rather than
    guessed at.
    """
    sel = COMMENT.sub(" ", selector).strip()
    if not sel or re.search(r"[>+~]", sel):
        return False
    parts = sel.split()
    if not _compound_matches(parts[-1], {TARGET_CLASS}, "a", allow_hover):
        return False
    ancestors = [({TARGET_PARENT_CLASS}, "nav"), ({"site-header"}, "header")]
    for part in reversed(parts[:-1]):
        if not any(_compound_matches(part, cls, tag, allow_hover=True)
                   for cls, tag in ancestors):
            return False
    return True


def _declaration(body, prop):
    """Last declaration of `prop` in a rule body, with its !important flag."""
    found = None
    for m in re.finditer(r"(?<![-\w])" + prop + r"\s*:\s*([^;}]+)", body):
        raw = m.group(1)
        found = (raw.replace("!important", "").strip(), "!important" in raw)
    return found


def resolve(html, prop, hover=False, background=False):
    """
    Winning value of `prop` on the header CTA, as (value, selector) or None.

    Ordering is CSS's: !important first, then specificity, then source order.
    """
    css = stylesheet(html)
    if not css:
        return None
    winner = None
    for m in RULE.finditer(css):
        selectors = [s for s in COMMENT.sub(" ", m.group(1)).split(",")]
        hits = [s.strip() for s in selectors
                if selector_matches(s, allow_hover=hover)]
        if hover:
            hits = [s for s in hits if ":hover" in s]
        else:
            hits = [s for s in hits if ":hover" not in s]
        if not hits:
            continue
        for name in (("background-color", "background") if background
                     else (prop,)):
            decl = _declaration(m.group(2), name)
            if not decl:
                continue
            value, important = decl
            key = (1 if important else 0,) + max(specificity(s) for s in hits)
            if winner is None or key >= winner[0]:
                winner = (key, value, max(hits, key=specificity))
    if winner is None:
        return None
    resolved = resolve_var(css, winner[1])
    if resolved is None:
        return None
    return resolved, winner[2]


def cta_contrast(html, hover=False):
    """
    (ratio, fg, bg, fg_selector) for the header CTA, or None if not determinable.

    None means "this page has no CTA anchor, or its colours cannot be resolved",
    and callers must treat that as unknown rather than as passing.
    """
    nav = re.search(r"<nav\b.*?</nav>", html, re.S | re.I)
    if not nav or not re.search(r"<a[^>]*" + TARGET_CLASS, nav.group(0)):
        return None
    fg = resolve(html, "color", hover=hover)
    bg = resolve(html, "background-color", hover=hover, background=True)
    if not fg or not bg:
        return None
    try:
        return contrast_ratio(fg[0], bg[0]), fg[0], bg[0], fg[1]
    except ValueError:
        return None
