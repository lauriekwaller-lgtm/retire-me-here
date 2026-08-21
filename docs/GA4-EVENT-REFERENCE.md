# GA4 EVENT REFERENCE

**Purpose:** what every event on the site means, where it fires, and what to
divide it by. Written for the moment you open GA4 in October and need to read
the numbers without reconstructing the reasoning.

**Last updated:** August 21, 2026, key events wired.
**Property:** `G-BTL743DSJQ`. Loads on `index.html`, all 51 profiles, and 48 of
49 root pages. `privacy.html` deliberately has no tag.

---

## 1. The two that matter

### `affiliate_click`

**Fires when:** a visitor clicks any outbound link to Expedia, Vrbo, or
Hotels.com.

**Where from:** all 51 city profiles, plus `visit-before-you-decide.html`.
52 pages.

**Parameters:**

| Parameter | Value | Example |
|---|---|---|
| `merchant` | which partner | `expedia`, `vrbo`, `hotels` |
| `surface` | which page | `tucson`, `visit-before-you-decide` |
| `city_slug` | same as surface | `tucson` |

**What it is for.** This is the revenue path and it was completely dark before
August 21. It answers: how many people click through to book at all, which
cities produce them, and whether Expedia or Vrbo is doing the work.

**Divide it by:** page views of that profile. That gives a click-through rate
per city, which is the number that tells you whether a profile is persuading
anyone to act.

**Read with care.** A click is not a booking. Partnerize holds the actual
conversion data on a 7-day cookie. This event counts intent leaving the site,
which is the part you control and the part you can improve.

### `signup_submit`

**Fires when:** a visitor hits submit on the MailerLite email form.

**Where from:** all three places the form appears. The `surface` parameter is
the important part of this event, because each surface has a DIFFERENT correct
denominator.

| `surface` value | Where the visitor was |
|---|---|
| `results_band` | the quiz results screen, field inline |
| `profile` | a city profile page, field inline |
| `modal` | the popup opened from a city detail card |
| `vault` | should never appear, see below |

**Divide it by:**

- `results_band` divided by `quiz_complete`. **This is the board's grading
  rule**, signup rate per results-screen session. It was uncomputable before
  August 21 because the numerator did not exist.
- `profile` divided by profile page views.
- `modal` divided by `signup_modal_open`, the only surface where opening the
  form is still a separate act.

**Read with care.** This counts an attempted submit, not a confirmed
subscriber. That is deliberate. MailerLite already counts confirmed subscribers
exactly, so GA4 only ever needed to supply the denominator and an attempt
signal. If GA4 attempts run well above MailerLite subscribers, the gap is
validation failures or delivery problems, and that gap is itself worth knowing.

**If `vault` ever appears**, something is wrong: the vault is the hidden holding
container and a form inside it should not be visible to submit. Investigate
rather than counting it.

---

## 2. The supporting cast

### `quiz_start`
Fires on quiz entry. Carries the referrer, or `direct`. The top of the quiz
funnel.

### `quiz_complete`
Fires when results are calculated and shown. **This is the denominator for the
headline capture rate.** Roughly: `signup_submit` (results_band) divided by
`quiz_complete` is the number to grade this year's capture work on.

### `match_reveal`
Fires when a city detail is rendered from the results. Engagement depth: how
many people who finished the quiz actually looked at a match.

### `breakdown_click`
Fires when someone opens the score breakdown on a results card. Carries the
city name. Signals appetite for the scoring detail.

### `signup_modal_open`
Fires when the signup popup opens. **Renamed from `report_request`**, which
implied someone requested a report. They did not; they opened a form.

**Important nuance.** Since the August 20 rebuild the field is inline on the
results screen and on profiles, so there is no "open" step on those surfaces.
This event now fires ONLY from city detail cards. It got quieter on August 20,
not louder. Do not treat it as the top of a site-wide signup funnel. It is the
denominator for `modal` submits and nothing else.

### `signup_submit_fallback`
**Renamed from `report_signup`.** Fires only on the Netlify backup path, used
when the MailerLite form fails to load. It should be near zero. If it starts
climbing, MailerLite is failing to render and that is a live defect, not a
signup channel.

### `pick_compare_run`
Fires on `pick-and-compare.html` when a comparison is run.

### `afford_tenure` and `afford_city_click`
Fire on `where-can-i-afford-to-retire.html`. Tenure mode changes and clicks
through to a city from the calculator results.

---

## 3. Retired names, so old data still makes sense

| Old name | Status | Why |
|---|---|---|
| `report_request` | renamed `signup_modal_open` | fired on modal open, never on a report request |
| `report_signup` | renamed `signup_submit_fallback` | fired only on the rare backup path, despite the name |
| `profile_capture` | deleted | attached to a function with zero call sites, could never fire |

Historical data under the old names stays queryable in GA4. Any report spanning
August 21 will show a break: the old name stops, the new name starts.

---

## 4. Required GA4 admin setup

The events are inert until these are done. Firing an event is not the same as
GA4 reporting it.

1. **Admin > Events.** Mark `affiliate_click` and `signup_submit` as key
   events.
2. **Admin > Custom definitions.** Register `merchant`, `surface`, and
   `city_slug` as event-scoped custom dimensions. Without this the events
   arrive but every breakdown reads `(not set)`.
3. **Admin > Data streams > Enhanced measurement.** Confirm Form interactions
   is ON. This gives an independent `form_submit` signal as a cross-check.
4. **DebugView, on production.** Click one affiliate link on any profile and
   complete one real signup from the results band. This is the only real
   verification available: the validator cannot see analytics and neither can a
   node test.

---

## 5. What to look at first, in October

In order, because each one answers a question the next one depends on:

1. **`affiliate_click` total, and by city.** Is anyone clicking through at all?
   This is the revenue path. If it is near zero across 51 profiles, the visit
   block is not doing its job and that is the biggest finding available.
2. **`signup_submit` (results_band) over `quiz_complete`.** The headline
   capture rate. The August 20 work exists to move this number.
3. **`signup_submit` by surface.** Which of the three asks earns its place.
   If profiles massively outperform the results band, that reorders the
   roadmap.
4. **`signup_submit_fallback`.** Should be near zero. Anything else is a
   MailerLite rendering fault.

**Grade no earlier than October.** At roughly 360 users a month the monthly
numbers are small enough that a single good week looks like a trend. The point
of this instrumentation is not this quarter's revenue, it is making the next
twelve months readable.

---

## 6. The standing caveat

Everything here describes what the code emits. Whether MailerLite emits a
native submit event on its rendered form was never verifiable outside a
browser, so `signup_submit` is proven in test and assumed in production until
DebugView confirms it. `affiliate_click` has no third-party dependency and is
the lower-risk half. If one arrives and the other does not, that is the
expected shape of the failure, and the fallback is the enhanced-measurement
`form_submit` signal.
