#!/usr/bin/env python3
"""Extract gold GO BIG wordmark from V8 square (navy bg) -> transparent PNG, cropped tight."""
from PIL import Image
import os

SRC = os.path.expanduser(
    "~/AI-OS/projects/prosper-landing/assets/gobig/approved/logo-v8-square-clean-1080.png"
)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-v8-wordmark.png")

img = Image.open(SRC).convert("RGBA")
px = img.load()
w, h = img.size

for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        # Navy is roughly (10-30, 20-40, 50-70). Gold is (~200, 150, 50).
        # Distance-from-navy as alpha proxy.
        navy_dist = abs(r - 15) + abs(g - 27) + abs(b - 60)
        if navy_dist < 40:
            px[x, y] = (0, 0, 0, 0)
        else:
            # Keep gold pixel, drop alpha for any dark blend halo
            # Brighten slightly so it reads cleanly on pure black
            px[x, y] = (r, g, b, min(255, max(0, navy_dist * 4)))

# Crop to bounding box of non-transparent pixels
bbox = img.getbbox()
cropped = img.crop(bbox)
cropped.save(OUT, "PNG")
print(f"Extracted: {OUT}  size={cropped.size}")
