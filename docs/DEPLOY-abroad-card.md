# DEPLOY: abroad link becomes a card (October 23, 2026)

```bash
git pull
ls *.zip
unzip -o abroad-card-bundle.zip
rm abroad-card-bundle.zip
python3 apply-abroad-card.py              # expect 4 "applied"
python3 tools/validate.py --local .       # 0 failures, 0 warnings
rm apply-abroad-card.py
git status        # expect 3 modified + this file new
git add -A && git commit -m "Abroad link under results becomes a card"
git push
```

Live check: take the quiz; below "More cities that fit" there is a white card,
"Try living there first", that opens the abroad page.
