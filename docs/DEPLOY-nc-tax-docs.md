# DEPLOY: NC tax sweep, CITATION-RECIPE repair, skill file

**Built:** August 26, 2026
**Base:** fresh full clone of `main` at `1b8e466` (the Raleigh commit)
**Gate:** `python3 tools/validate.py --local .` at 0 failures, 0 warnings

Docs and copy only. No profile, no new page, no layout change.

---

## 1. Deploy sequence

```bash
git pull
unzip -o nc-tax-docs-bundle.zip
rm nc-tax-docs-bundle.zip
python3 apply-nc-tax-and-docs.py --check
python3 apply-nc-tax-and-docs.py
python3 tools/validate.py --local .
rm apply-nc-tax-and-docs.py
git status --short --untracked-files=all
git add -A && git commit -m "NC income tax corrected on 7 index.html surfaces; CITATION-RECIPE hand-off + DB + Highlight repairs; board + ops log"
git push
```

Expect **1 untracked** (`docs/DEPLOY-nc-tax-docs.md`) and **4 modified**
(`index.html`, `docs/CITATION-RECIPE-city-profiles.md`, `docs/TASKBOARD.md`,
`docs/SITE-OPERATIONS-LOG.md`). 12 edits across those 4 files.

---

## 2. Item 1: NC income tax. It was seven surfaces, not four.

The board entry written during the Raleigh build named four. Re-derived by grep
against live `main`, there were seven.

| # | Surface | Was | Now |
| --- | --- | --- | --- |
| 1 | Wilmington NC `pros` | 4.75% | 3.99% (2026) |
| 2 | Asheville `scoreNotes.D5` | 4.75% | 3.99% for 2026, with the pension/IRA treatment |
| 3 | Wilmington NC `scoreNotes.D5` | 4.75% | same |
| 4 | Beaufort NC `scoreNotes.D5` | 4.75% | same, Carteret clause kept |
| 5 | Pinehurst `cons` | flat 4.25% (3.99% in 2026) | a flat 3.99% (2.99% by 2028) |
| 6 | Pinehurst `scoreNotes.D5` | flat 4.25% (3.99% in 2026) | flat 3.99% for 2026 |
| 7 | `getTaxNote` state table | `'NC': '4.75% flat'` | `'NC': '3.99% flat'` |

Authoritative row, DB State Tax Facts sheet: **Flat / 3.99 / SS Exempt / retirement
income Taxed** / "Pension, IRA and 401(k) taxed at the flat 3.99 percent; no general
retiree exclusion" / sales 7.1 / proptax 0.66 / no estate or inheritance tax /
vintage 2026.

**Why the board's count was wrong, which matters more than the count.** That entry
was built by grepping `4.75` and reading the hits as a complete enumeration. It could
not see Pinehurst, because Pinehurst phrases the same fact as 4.25% with a 2026
projection. And nothing city-shaped would have surfaced `getTaxNote`, because that is
a state-level lookup table, not a city entry. **Grepping one string is not enumerating
a subject.**

`getTaxNote` was also the widest-reach instance: it feeds the quiz city-detail stat
card for every NC city, published or not, so it was wrong on more surfaces than all
six city entries combined, and it was the one nothing pointed at.

**Not fixed, deliberately, and boarded P3:** `getTaxNote` is stale for states other
than NC. Spot-checks suggest GA (5.49%), KY (4.5%) and IN (3.15%) are behind their
2026 figures. This was an NC job. Do not sweep those from memory; do it against the
State Tax Facts sheet.

**Boarded P2, the fix worth more than the sweep:** nothing compares `index.html` tax
prose to the State Tax Facts sheet. `check_taxfacts` holds the sheet to its own
promises and `check_taxtool` holds the tax tool to the sheet, but the quiz's own copy
is unchecked in both directions. That gap is why seven surfaces survived two
dedicated passes. Per house rule the planted-error harness comes first, and it has to
discriminate across all three shapes (`getTaxNote`, `pros`/`cons`, `scoreNotes.D5`):
a check reading only `scoreNotes` would have passed every pass this week while
`getTaxNote` stayed wrong.

**Negative finding.** No comparison page, profile, or landing page asserts an NC
income tax rate. `grep -rn "4\.75\|flat 4\.25" --include=*.html .` now returns nothing
tax-related. `states-that-dont-tax-retirement-income.html` was already correct at
3.99% and is covered by `check_taxfacts`.

---

## 3. Item 2: `docs/CITATION-RECIPE-city-profiles.md`, three repairs

1. **Hand-off conventions.** It still said to hand off `bentonville-hero.jpg` and
   `<city>-profile.html` for renaming at deploy. `DEPLOY-CHEATSHEET.md` section 4
   superseded that on July 14, and this is the same rot that put three builds in the
   wrong shape when the skill file carried it. The section now delegates and says why.
   Photo specs stay, since no other repo doc carries them.
2. **Database filename.** Named `CityDatabase_Jun_9_v14.xlsx`, five versions behind.
   Now names v19.1 with the date it was true, and tells the reader to list `docs/`
   rather than trust the line.
3. **The phantom `Highlight` column.** It described "a `Highlight` field with quotable
   facts". No sheet in v19.1 has that column, verified by scanning all six sheets at
   both header rows. The per-city `highlight:` strings live in `index.html` and are
   editorial copy, not a data source.

---

## 4. Item 3: the skill file. ALREADY EDITED, not in this bundle.

`retiremehere-city-profile/SKILL.md` lives outside the repo, so it cannot ride a
commit. It has been edited in place. Four changes:

1. **Two delegation rows added:** `PROFILE_CONVENTIONS.md` (heading emphasis,
   pull-quote and dropcap conventions) and `CITATION-RECIPE-city-profiles.md` (FAQ
   format, score citation). Plus a warning under the table that it is not the whole
   list, naming the August 25 build that read only the six listed subjects and shipped
   two heading defects the gate cannot see, and instructing a build to list `docs/`
   and open anything profile-shaped regardless.

2. **The `/10` rule was wrong and is now per-surface.** It said "never display a /10",
   including on the healthcare card. Deployed St. Louis shows 10/10 on that card, and
   `CITATION-RECIPE` is explicit that FAQ answers citing scores are what gets lifted
   into an AI Overview. The file now carries a four-row table: No on the stats bar, No
   in body prose, **Yes on the healthcare card, Yes in FAQ answers**. It also explains
   that Prescott uses a bed count because that is the honest proof for a hospital that
   is not nationally ranked, not because a grade is banned. This closes the P3 that has
   been reopened on every build since June.

3. **The phantom `Highlight` field** removed from the distinctions checklist, same as
   the recipe.

4. **DB filename example** refreshed to v19.1, with the naming trap named: the date in
   the filename is not the version date, so `Jul_27` has covered v17 through v19.1.

**One thing this does not fix.** The skill still sits outside the repo, so section 4a
and the enumeration rule still cannot keep it current, and it will rot again. The
structural fix is to move it into `docs/` and have the skill point at it rather than
restate it. That is a real decision, not a chore, so it is not boarded as a task.
