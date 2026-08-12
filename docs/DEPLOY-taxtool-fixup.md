# DEPLOY: tax tool fixup, URL deep linking and heading scope

**Delivered by terminal paste (the zip download failed); content identical to
the tested bundle.**
**New files:** `docs/DEPLOY-taxtool-fixup.md`, `apply-taxtool-fixup.py`
**Existing files edited by the apply script:**
`states-that-dont-tax-retirement-income.html`, `docs/DEPLOY-taxtool.md`,
`docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.

The first tool bundle deployed before two improvements landed. This commit
carries them: filter state syncs to the URL query string both ways (every
combination is a shareable landing page; canonical stays on the bare URL), and
the filter heading reads "every state with a RetireMeHere city". No DB change,
no score change, no validator change. The script is safe whatever state the
working tree is in: each edit checks its own marker and skips work already
present, and the result is byte-identical either way.

## After deploy

On the live page: set filters, watch the address bar pick them up, paste the
URL into a new tab and confirm it opens pre-filtered. Then the deep links are
ready to carry Pinterest pins, for example `?ret=1&inherit=1` for the
no-withdrawal-tax, no-inheritance-tax pin.
