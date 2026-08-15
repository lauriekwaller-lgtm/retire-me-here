# DEPLOY: sitewide font sweep to system B; favicon 2

**Bundle:** `fontsweep-bundle.zip`
**New files:** `tools/test_typography.py`, `docs/DEPLOY-fontsweep.md`, `apply-fontsweep.py`
**Edited by the apply script:** every .html page (typography only), favicon.svg,
favicon.ico, favicon-16/32/48/192.png, apple-touch-icon.png, `tools/validate.py`,
`docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.

Operator-approved after side-by-side preview review. No content, DB, or score
changes: Playfair Display and Fraunces retired for bold Libre Franklin over DM
Sans; every 300 weight retired (display rules to 800, body to 400); text-wrap
balance on centered headlines and sublines; eight Google Fonts link variants
collapsed to one; the slab-serif favicon replaced by the map-pin mark at every
size. The apply script is a rule-based transformer with hard post-conditions:
it refuses to finish if any retired reference survives.

## Sequence

```bash
git pull
unzip -o fontsweep-bundle.zip && rm fontsweep-bundle.zip
python3 apply-fontsweep.py               # must end with "patched"
timeout 1800 python3 tools/validate.py --local .   # the gate. 0/0 or stop.
rm apply-fontsweep.py                    # BEFORE git add
git status --short --untracked-files=all | wc -l   # expect 111
git add -A && git commit -m "Sitewide font sweep to system B; favicon 2; check_typography + harness"
git push
python3 tools/validate.py                # post-deploy live verification
```

111 status lines = 109 modified (99 pages, 7 favicon files, validate.py, board,
log) plus 2 new (harness, this note).

## After deploy

Hard-refresh (or private window) before judging: browsers cache both fonts and
favicons aggressively, and favicons can take a day to update in some browsers.
Walk the homepage, one profile, one landing page, and the tax tool on desktop
and phone. Every headline should be bold Franklin, no thin gray paragraphs
anywhere, no single floating words under centered headlines, and the tab icon
is the teal map-pin. The pin studio is untouched by design: pin images are
their own aesthetic and keep their fonts until you decide otherwise.

`check_typography` now guards the layout group: any future page cloned from a
stale template that reintroduces a retired font, a thin weight, or a rogue
fonts link fails the gate before it ships.
