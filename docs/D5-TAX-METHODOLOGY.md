# D5 Tax Friendliness: Methodology

**Version 1.0 — July 12, 2026**
Authoritative for all D5 scoring. Governs `D5 Tax` in the City Database.
Companion to `scoring_rubric_v3_2` (D5 section) and `BUDGET-METHODOLOGY.md`.

---

## 1. The rule

**D5 is a state-level score. Every city in a state gets the same D5.**

The validator enforces this. `tools/validate.py --only db` fails the deploy when any
state's D5 values span more than `D5_MAX_SPREAD` (currently 1 point).

## 2. Why

Every input the rubric lists for D5 is set at the state line or above:

- state income tax on Social Security
- state income tax on pension, IRA and 401(k) distributions
- overall state income tax rate
- property tax rates and senior exemptions
- sales tax burden

Two further facts close the question:

**The neighborhood carve-out does not reach D5.** The rubric's Universal Methodology,
which scores retiree-target neighborhoods instead of the citywide average, is scoped
explicitly to D2 (Affordability), D6 (Walkability), and D9 (Safety). D5 is not on that
list. There is no mechanism in the rubric by which two cities in one state may differ
on tax.

**The database holds no per-city tax input.** `PropTax Rate %` carries exactly one
value per state, across all 39 states in the file. Nothing else in the database
measures tax. So a within-state D5 spread cannot be sourced to anything. It is not a
judgment call; it is an unsourced number.

## 3. Why 1 point of slack, and not zero

Local sales-tax add-ons and county millage genuinely do vary within a state. The
database does not currently record them, but they are real, so a 1-point spread is
tolerated rather than banned.

**A 1-point spread is a tolerance, not a licence.** Do not introduce one to express an
editorial hunch. If two cities in a state differ by a point, there should be a reason
written down, and today there is no column to write it in.

If per-city tax granularity is ever wanted properly, the fix is a `Local Tax Adj`
column in the database, not looser scoring. Twelve states currently carry an
inherited 1-point spread (DE, FL, ID, KY, NC, NM, PA, SC, TN, TX, UT, WI). These pass
the check and are unreviewed.

## 4. How to score a new state

Read the rubric's five D5 bands and place the state in one. Anchor on how the state
treats **pension, IRA and 401(k) withdrawals**, because that is the money a relocating
retiree actually draws down. Then adjust within the band for Social Security
treatment, sales tax, and property tax.

Score the state once. Apply it to every city in that state.

## 5. What went wrong (July 2026)

Six states carried a D5 spread of 2 or more points: CO (5–8), MT (4–8), OR (3–6),
TN (8–10), VA (5–7), IA (6–8).

Oregon was the clearest case. Bend scored 6 and Eugene scored 3 on identical state tax
law and an identical `PropTax Rate %` of 0.81. Bend's own cons list in `index.html`
read "Oregon income tax 8–9.9%, worst for retirees in the Pacific Northwest" while its
score said 6. The prose knew; the score did not.

Worse, the site had begun *explaining* the errors. `fort-collins-vs-boulder-retirement.html`
told readers that the Boulder 7 / Fort Collins 5 gap "reflects local tax burden captured
in the scoring," in a paragraph that also stated both cities pay Colorado's identical
0.50% property rate. A page had reasoned its way into justifying a data-entry mistake.
That is the failure mode this rule exists to prevent: a wrong number is cheap to fix,
but a wrong number that has grown a defence is not.

## 6. Corrections applied (v16.1 to v16.2)

| State | Anchor | Reasoning | Cities changed |
|---|---|---|---|
| **CO** | **7** | SS exempt at 65+, $24K retirement-income deduction, flat 4.4%, 0.50% property tax. Rubric band 7–8: "partial exemptions or low flat tax rate." | Grand Junction, Fort Collins, Vail, Steamboat Springs 5→7; Durango 8→7 |
| **IA** | **8** | Retirement income fully exempt at 55+ (2023 reform), SS exempt, flat 3.8%, no inheritance tax, but 1.33% property tax. Rubric band 7–8, second clause exactly: "no income tax but higher property taxes." | Des Moines 6→8 |
| **MT** | **5** | Taxes SS *and* pensions/IRAs, only a $5,500 retirement subtraction, top rate 5.65%. Offset by no sales tax and 0.61% property tax. Rubric band 5–6: "moderate burden, some retirement income taxed." | Missoula 4→5; Whitefish 8→5 |
| **OR** | **4** | Taxes pension/IRA/401(k) at up to 9.9%. SS exempt and no sales tax are real offsets, and a $1M estate-tax exemption is a real drag. Rubric band 3–4: "above-average burden, retirement distributions taxed at a meaningful rate." Top of band. | Bend 6→4; Eugene 3→4 |
| **TN** | **9** | No income tax on any retirement income, 0.52% property tax. Not a clean 10 only because combined sales tax is the highest in the nation. Rubric band 9–10, and the rubric names Chattanooga as its exemplar. | Johnson City 8→9 |
| **VA** | **6** | SS exempt, but other retirement income taxed up to 5.75% with only a means-tested $12K age deduction. 0.78% property tax. Rubric band 5–6. | Roanoke 5→6; Virginia Beach 7→6 |

Chattanooga stays at 10 against Tennessee's 9: Hamilton County carries a lower combined
sales-tax rate and lower property tax than Memphis or Nashville. This is a tolerated
1-point spread under section 3 and is the only one in the six states above. It is
unbacked by any database column and should be revisited if a `Local Tax Adj` column
is ever added.

## 7. Open item

The rubric's own 3–4 band names **Charleston (SC)** as an exemplar, but the database
scores Charleston 6. South Carolina exempts Social Security and grants a large 65+
deduction, so the database is right and the rubric example is stale. Fix in rubric v3.3
so the two documents stop contradicting each other.
