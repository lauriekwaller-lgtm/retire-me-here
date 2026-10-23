# DEPLOY: tradeoff line de-duplicated on results cards (October 23, 2026)

## Deploy (Codespaces terminal)

```bash
git pull
ls *.zip                                  # after dragging the zip to the top level
unzip -o tradeoff-dedupe-bundle.zip
rm tradeoff-dedupe-bundle.zip
python3 apply-tradeoff-dedupe.py          # expect 9 "applied", 1 "already in"
python3 tools/validate.py --local .       # 0 failures, 0 warnings
rm apply-tradeoff-dedupe.py
git status        # expect 3 modified + this file new
git add -A && git commit -m "Results cards: tradeoff line no longer repeats"
git push
```

If you deploy on a later day than October 23, expect 10 "applied" (the
sitemap date is included then).

## What changes

- `index.html`: every card shows its own weakest point; when it matches an
  earlier card it reads "Same tradeoff as [city]: ... here too." D4 reads
  "climate resilience" in the sentence.
- `docs/TASKBOARD.md`, `docs/SITE-OPERATIONS-LOG.md`.

## Live check

Take the quiz without marking anything Must Have or Very Important, pick warm
weather. Card 1 shows the tradeoff; cards 2 and 3 say "Same tradeoff as
[card 1 city]".
