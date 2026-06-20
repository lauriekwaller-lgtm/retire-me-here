# v15.1 Transition — Commit Notes

**Date:** 2026-06-19
**Scope:** Median Home methodology v1.0 → v1.1, Database v14 → v15.1, index.html data fields

## Files in this commit

### Database
- **REPLACE** `CityDatabase_Jun_9_v14.xlsx` → `CityDatabase_Jun_19_v15_1.xlsx`
  - 99 cities (Henderson NV collapsed into Las Vegas)
  - Citywide medians for 97 cities; range format preserved for Wilmington DE and St. Paul MN
  - Monthly Est recomputed per BUDGET-METHODOLOGY.md
  - Budget Range column reassigned to v15.1 tiers (R1–R5)
  - Sequential numbering 1–99
  - Budget Tiers sheet rebuilt

### Methodology docs
- **REPLACE** `MEDIAN-HOME-METHODOLOGY.md` (v1.0 → v1.1)
  - Citywide-default policy + Median Honesty Rule
  - 8 callout cities documented
  - Multi-basis approach retired
- **DELETE** `MEDIAN-HOME-AUDIT-REFERENCE.md` (obsolete — 12 refinements were specific to v1.0)
- **DELETE** `MEDIAN-HOME-LABEL-CONVENTIONS.md` (obsolete — basis labeling no longer applies)

### Index
- **REPLACE** `index.html`
  - BUDGET_OPTIONS array: new boundaries
  - BUDGET_LABELS quiz UI: new boundaries
  - Quiz subtitle: full PITI + 6-category framing
  - budgetLabels (match explanations): new boundaries
  - CITIES array: 99 cities × (monthlyEst, medianHome, budgetRange) refreshed
  - 7 surgical Range-number prose fixes in tier-shift cities
  - console.log + inline transition marker

### New tracking artifacts
- **ADD** `v14-to-v15_1-audit-log.xlsx` (per-city delta log; reference for future)
- **ADD** `V15_1-TRANSITION-CHECKLIST.xlsx` (delete when all outstanding work done)
- **KEEP** `MedianHomeAuditMASTER.xlsx` (audit basket research, editorial reference for callouts)

### Operations log
- **UPDATE** `SITE-OPERATIONS-LOG.md`
  - New change log entry at top of section 7
  - Section 8 items marked done where complete
  - "Last full review" date updated

## What's outstanding (tracked in V15_1-TRANSITION-CHECKLIST.xlsx)

1. **Index prose review** — 60 cities with tier shifts have body-text dollar amounts in pros/cons/highlight/D2 strings that may reference v14 values. Stat cards and quiz logic are correct; only body prose remains.
2. **Per-city profile.html pages (35 live)** — stat cards, JSON-LD schema, inline copy mentions.
3. **Neighborhood Reality Check callouts (8 cities)** — above-fold callout block per methodology v1.1 §6.
4. **Other site files** — value-navigator.html, comparison pages, thematic landing pages, Pinterest pins.
5. **Future methodology items** — HOA fees, home maintenance line, range-city midpoint documentation (non-urgent, parked).

## Suggested commit sequence (atomic deploys)

```
git add CityDatabase_Jun_19_v15_1.xlsx
git rm CityDatabase_Jun_9_v14.xlsx
git commit -m "DB: v15.1 — citywide medians, recomputed Monthly Est, Henderson collapsed"

git add MEDIAN-HOME-METHODOLOGY.md v14-to-v15_1-audit-log.xlsx V15_1-TRANSITION-CHECKLIST.xlsx
git rm MEDIAN-HOME-AUDIT-REFERENCE.md MEDIAN-HOME-LABEL-CONVENTIONS.md
git commit -m "Methodology: Median Home v1.1 — citywide-default + Median Honesty Rule"

git add index.html
git commit -m "index.html: v15.1 quiz boundaries + 99 city data refresh + PITI framing"

git add SITE-OPERATIONS-LOG.md
git commit -m "Ops log: v15.1 transition entry"
```

## Sanity checks before deploy

- [ ] index.html parses (no syntax errors in JS)
- [ ] Quiz step "Budget" displays new boundaries
- [ ] Card stats show new dollar amounts on a tier-shift city (e.g., check Tampa shows $5,500–$6,800)
- [ ] Console.log says "99 cities (v15.1)"
- [ ] Sitemap.xml unchanged (no city additions/removals at the URL level)
- [ ] MailerLite form IDs unchanged in index.html (verify universal.js still loads)
- [ ] PUBLISHED_PROFILES map unchanged (no profile gain/loss)
