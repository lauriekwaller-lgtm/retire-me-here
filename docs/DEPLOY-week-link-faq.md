# DEPLOY: week link on results cards + quiz FAQ fix (October 23, 2026)

## Deploy (Codespaces terminal)

```bash
git pull
ls *.zip                                  # after dragging the zip to the top level
unzip -o week-link-faq-bundle.zip
rm week-link-faq-bundle.zip
python3 apply-week-link-faq.py            # expect 12 "applied", 1 "already in"
python3 tools/validate.py --local .       # 0 failures, 0 warnings
rm apply-week-link-faq.py
git status        # expect 6 modified + this file new
git add -A && git commit -m "Week link on results cards; quiz FAQ markup fix"
git push
```

Run it on the day you commit (it stamps today on the quiz page's sitemap date).

## What changes

- `index.html`: "What a week in [city] looks like" under the button on each of
  the three result cards, for the 53 cities with a profile. Opens the profile at
  its week section. New GA4 event `week_click`. `PUBLISHED_PROFILES` moved out of
  `showCityDetail()` to top level, entries unchanged; still the one place to
  register a profile.
- `where-should-i-retire-quiz.html`: the FAQ wrapper fixed.
- `sitemap.xml`: quiz page date.
- `docs/GA4-EVENT-REFERENCE.md`, `docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.

## Live check

Take the quiz on your phone. Each of the three cards shows the week link under
the orange button. Tap one: the profile opens and scrolls to "A week in...".
