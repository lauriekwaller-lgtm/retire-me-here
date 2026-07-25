#!/usr/bin/env python3
"""
apply-tulsa-photo.py  --  RetireMeHere: swap the Tulsa detail photo and fix its credits.

Run from the repo root, after `git pull` and after dropping the new image in:

    git pull
    # copy tulsa-detail.jpg -> cities/tulsa/detail.jpg   (overwrite the existing file)
    python3 apply-tulsa-photo.py
    python3 tools/validate.py --local .
    rm apply-tulsa-photo.py
    git status
    git add -A
    git commit -m "Tulsa: detail photo swapped to Boston Avenue Methodist Church, CC BY 2.0 credit"
    git push

Edits one file:
  cities/tulsa/profile.html   detail photo credit + footer photo credits

The image itself is dragged in, not patched. A script cannot diff a JPEG.

CC BY 2.0 requires credit, a link to the license, and a note that the work was changed.
All three are handled here: the on-image credit names CPacker and the license, and the
footer carries the full attribution with a live license link and the word "cropped".

Idempotent. Refuses to write anything if an anchor has moved.
Delete after use; not meant to be committed.
"""

import os
import sys

OLD_CREDIT = '<div class="detail-photo-credit">Photo · Daniel Nieto / Unsplash</div>'
NEW_CREDIT = '<div class="detail-photo-credit">Photo · CPacker / English Wikipedia · CC BY 2.0</div>'
OLD_FOOT = '      Photos: Mick Haupt, Daniel Nieto, both via Unsplash. <br>'
NEW_FOOT = '      Photos: Mick Haupt via Unsplash. Boston Avenue Methodist Church by CPacker at English Wikipedia, licensed <a href="https://creativecommons.org/licenses/by/2.0/" rel="license nofollow" style="color:rgba(255,255,255,0.6);text-decoration:underline;">CC BY 2.0</a>, cropped and resized. <br>'

P = "cities/tulsa/profile.html"

EDITS = [
    (P, OLD_CREDIT, NEW_CREDIT, "CPacker / English Wikipedia"),
    (P, OLD_FOOT, NEW_FOOT, "licensed <a href=\"https://creativecommons.org/licenses/by/2.0/\""),
]


def main():
    if not os.path.isfile("index.html") or not os.path.isdir("cities"):
        sys.exit("Run this from the repo root.")

    planned, skipped, missing, cache = [], [], [], {}
    for path, old, new, marker in EDITS:
        if not os.path.isfile(path):
            missing.append(path + ": file not found")
            continue
        if path not in cache:
            cache[path] = open(path, encoding="utf-8").read()
        text = cache[path]
        if marker in text:
            skipped.append(path + ": already applied (" + marker[:44] + "...)")
            continue
        n = text.count(old)
        if n != 1:
            missing.append(path + ": anchor found " + str(n) + " times, expected 1. File has drifted.")
            continue
        cache[path] = text.replace(old, new, 1)
        planned.append(path + ": patched")

    if missing:
        print("STOPPED. Nothing written.\n")
        for m in missing:
            print("  [FAIL]", m)
        sys.exit(1)

    for path in {p for p, *_ in EDITS}:
        open(path, "w", encoding="utf-8").write(cache[path])

    for line in planned:
        print("  [OK]  ", line)
    for line in skipped:
        print("  [SKIP]", line)

    img = "cities/tulsa/detail.jpg"
    if os.path.isfile(img):
        size = os.path.getsize(img)
        print("\n  detail.jpg present, " + str(round(size / 1024)) + " KB")
        print("  Confirm this is the Boston Avenue image, not the old Prayer Tower.")
    else:
        print("\n  WARNING: " + img + " is missing. Drag the new image in before committing.")

    print("\nNext: python3 tools/validate.py --local .")


if __name__ == "__main__":
    main()
