# HUM and HEAT Field Population Guide

This is your working reference for adding humidity and heat data fields to your cities. Use this alongside Step 5B in the implementation plan.

---

## Where to find a city's climate object

In your `index.html`, every city in the CITIES array has a `climate` object that looks something like this:

```javascript
climate: { W: 8, H: 9, M: 4 }
```

Or it may be on a single line as part of a larger city block, or formatted across multiple lines. The fields are:

- `W` = Winter score
- `H` = Summer/heat score (currently does double duty for both heat and humidity — that's the bug)
- `M` = Moisture/cloudiness score

**To find a specific city's climate object:**

1. In your editor, search for the city name (e.g., `Phoenix`)
2. You'll find the city's data block — could be 50+ lines long
3. Look for the `climate:` line within that block

---

## How to add the new fields

You're adding two new fields to each city's existing climate object. The old `W`, `H`, `M` fields stay — you're not removing anything, just adding.

**Example — Phoenix:**

**FIND something like:**

```javascript
climate: { W: 9, H: 10, M: 1 }
```

**REPLACE WITH:**

```javascript
climate: { W: 9, H: 10, M: 1, HUM: 1, HEAT: 10 }
```

That's it. Just two new fields tacked onto the end. Comma between each field. Closing `}` stays.

**Example — Miami:**

**FIND something like:**

```javascript
climate: { W: 9, H: 8, M: 7 }
```

**REPLACE WITH:**

```javascript
climate: { W: 9, H: 8, M: 7, HUM: 10, HEAT: 7 }
```

---

## Priority cities — populate these first

These are the cities where the heat/humidity split matters most. Spot-fixing these 20 gives you 80% of the value.

### Hot AND Dry (high HEAT, low HUM)

These should NOT trigger the "Humid summers" dealbreaker but SHOULD trigger "Extreme heat":

| City | HUM | HEAT | Notes |
|---|---|---|---|
| Phoenix, AZ | 1 | 10 | Most extreme dry heat in US |
| Tucson, AZ | 2 | 9 | Slightly less extreme than Phoenix |
| Las Vegas, NV | 1 | 10 | Desert, frequent 110°F+ |
| Palm Springs, CA | 1 | 10 | Often hotter than Phoenix |
| Sedona, AZ | 2 | 8 | Higher elevation softens it slightly |
| Scottsdale, AZ | 1 | 10 | Same as Phoenix |
| Albuquerque, NM | 2 | 7 | High desert, dry but cooler than Phoenix |
| St. George, UT | 2 | 9 | Desert |
| Santa Fe, NM | 3 | 5 | High elevation moderates heat |

### Hot AND Humid (high HEAT, high HUM)

These trigger BOTH dealbreakers:

| City | HUM | HEAT | Notes |
|---|---|---|---|
| Houston, TX | 9 | 9 | Hot and very humid |
| New Orleans, LA | 10 | 8 | Famously humid |
| San Antonio, TX | 8 | 9 | |
| Austin, TX | 8 | 9 | |
| Fort Worth, TX | 7 | 9 | |

### Humid but not extreme heat (high HUM, moderate HEAT)

These trigger "Humid summers" but NOT "Extreme heat":

| City | HUM | HEAT | Notes |
|---|---|---|---|
| Miami, FL | 10 | 7 | Very humid, ocean moderates heat |
| Charleston, SC | 10 | 7 | Famously humid |
| Savannah, GA | 10 | 7 | Same |
| Tampa, FL | 9 | 7 | |
| Sarasota, FL | 9 | 7 | |
| Naples, FL | 9 | 7 | |
| Fort Myers, FL | 9 | 7 | |
| Hilton Head, SC | 9 | 6 | Coastal moderation |
| Delray Beach, FL | 9 | 7 | |
| St. Pete, FL | 9 | 7 | |

### Mild — neither extreme

These shouldn't trigger either dealbreaker:

| City | HUM | HEAT | Notes |
|---|---|---|---|
| San Diego, CA | 5 | 2 | Famously mild |
| Santa Barbara, CA | 5 | 3 | |
| Carmel-by-the-Sea, CA | 5 | 2 | |
| Portland, OR | 5 | 3 | Mild summers |
| Portland, ME | 6 | 3 | Cool coastal |
| Provincetown, MA | 7 | 3 | Cool coastal |
| Annapolis, MD | 7 | 5 | |

### Cool / Mountain (low HUM, low HEAT)

| City | HUM | HEAT | Notes |
|---|---|---|---|
| Boulder, CO | 3 | 4 | Mountain, dry |
| Denver, CO | 3 | 5 | |
| Bend, OR | 3 | 4 | High desert |
| Boise, ID | 4 | 6 | Continental, gets warm |
| Bozeman, MT | 3 | 3 | Cool mountain |
| Missoula, MT | 4 | 4 | |
| Jackson Hole, WY | 3 | 3 | Cool mountain |
| Park City, UT | 3 | 3 | |
| Flagstaff, AZ | 4 | 3 | High elevation despite Arizona |
| Whitefish, MT | 5 | 3 | |
| Durango, CO | 4 | 4 | |

---

## Quick reference for any city not listed

If you need to score a city not on this list, ask yourself two questions:

**For HUM:**
- "Are summers known for being humid/sticky?"
- 0–2: Desert (Sun Belt dry — Phoenix, Vegas, ABQ)
- 3–4: Continental dry (Mountain West, high plains)
- 5–6: Moderate (much of California, parts of New England)
- 7–8: Humid (most Eastern US, Texas, Midwest in summer)
- 9–10: Very humid (Florida, Gulf Coast, Deep South)

**For HEAT:**
- "How often does this city hit 100°F+?"
- 0–2: Almost never. Cool summers all season.
- 3–4: Rare. Occasional 90°F day, 100°F is exceptional.
- 5–6: Hot summers but 100°F is uncommon (most Southeast/Mid-Atlantic)
- 7–8: Regular 90s, occasional 100°F (Texas, Atlanta, parts of South)
- 9–10: Frequent 100°F+ (Phoenix, Vegas, Palm Springs, parts of Texas)

---

## Workflow suggestion

You have 100 cities. Don't try to do them all at once.

**Session 1 (~30 min):** Add HUM and HEAT to the priority cities listed above (the 40-ish cities). These are your highest-impact wins.

**Session 2 (~45 min):** Walk through your remaining cities alphabetically. For each, glance at the climate description in the city data (you've already written climate notes for each city). Use the rubric above to assign HUM and HEAT scores.

**Session 3 (cleanup):** Spot-check by running the dealbreaker tests:
- Quiz with "Extreme heat" dealbreaker → confirm Phoenix, Las Vegas, Palm Springs are filtered out
- Quiz with "Humid summers" dealbreaker → confirm Miami, Charleston, Houston are filtered out
- Mild cities (San Diego, Portland OR/ME) should pass both dealbreaker filters

---

## Common mistakes to avoid

**Don't accidentally remove existing fields.** When you add HUM and HEAT, make sure the existing W, H, and M values stay. You're adding, not replacing.

**Don't forget the comma.** Each field needs a comma after it (except the last one). If you write `H: 9 HUM: 10` (no comma), you'll get a JavaScript error and your site will break.

**Use numbers, not strings.** Write `HUM: 10`, not `HUM: "10"`. Numbers don't have quotes around them.

**Watch for cities listed multiple times.** If you have both "Portland, OR" and "Portland, ME" in your data, make sure you score them differently.

---

## After you populate enough cities

Once you've added HUM and HEAT to your priority cities, you can deploy Step 5A (the code change that reads the new fields). Until then, the dealbreaker logic still uses the old `H` field as fallback — so deploying or not deploying Step 5A doesn't break anything either way.

Best workflow:
1. Populate priority cities (Session 1)
2. Deploy Step 5A code change
3. Test the dealbreaker filters with the priority cities
4. Continue populating remaining cities over time
