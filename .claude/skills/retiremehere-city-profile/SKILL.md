---
name: retiremehere-city-profile
description: Build or refresh a RetireMeHere.com city profile from City Database scores. Generate the emphasis brief, build from the live canonical template, add the Visit block, and produce the deploy package.
---

# RetireMeHere City Profile

**This file is a pointer, not a spec.** Everything that governs a profile build lives
in the repo, where a commit can fix it and the validator can watch it.

Pull this doc live and follow it:

```
https://raw.githubusercontent.com/lauriekwaller-lgtm/retire-me-here/main/docs/PROFILE-BUILD-SOP.md
```

It carries the data rule, the brief thresholds, the score-display table, the
live-canonical rule, build order, photo specs, the file list, and a delegation table
pointing at the docs that own everything else.

If this file and that doc ever disagree, **the doc wins and this file is the bug.**
Say so in the hand-off.

## Why this file is nearly empty

It lives outside the repo, so section 4a and the enumeration rule cannot keep it
current. Anything restated here is a copy that will rot, and it has: a superseded
hand-off shape that put three builds in the wrong shape, a database filename two
versions stale, a flat "never display a /10" that contradicted the deployed
canonical, and a database field that does not exist. Every one was a convenience
copy of a fact that lived somewhere else.

So the rule is: **own or delegate, never restate.** This file owns nothing. If you
are tempted to add a specification here, add it to the SOP instead.
