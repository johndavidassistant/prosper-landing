#!/usr/bin/env python3
"""
GO BIG — Instagram Carousel / final-v8
Black bg · White + gold accents · Inter only (no serif) · V8 wordmark footer (small, centered)
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Canvas ────────────────────────────────────────────────
SIZE        = 1080
MARGIN      = 130
CONTENT_TOP = 130
CONTENT_BOT = 880        # wordmark sits below this
TEXT_W      = SIZE - 2 * MARGIN

BG    = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD  = (200, 149, 46)
MUTED = (130, 130, 130)

# ── Inter (only) ──────────────────────────────────────────
LF = os.path.expanduser("~/Library/Fonts")
def F(weight, size):
    files = {
        "black":     "Inter_28pt-Black.ttf",
        "extrabold": "Inter_28pt-ExtraBold.ttf",
        "bold":      "Inter_28pt-Bold.ttf",
        "semibold":  "Inter_28pt-SemiBold.ttf",
        "medium":    "Inter_28pt-Medium.ttf",
        "regular":   "Inter_18pt-Regular.ttf",
    }
    return ImageFont.truetype(os.path.join(LF, files[weight]), size)

# ── V8 wordmark (extracted, transparent) ──────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
LOGO_SRC = os.path.join(HERE, "logo-v8-wordmark.png")

# Original aspect 900:192 ≈ 4.6875:1. Render at 220×47 (small, classy).
_raw      = Image.open(LOGO_SRC).convert("RGBA")
LOGO_W    = 220
LOGO_H    = int(LOGO_W * _raw.size[1] / _raw.size[0])
LOGO      = _raw.resize((LOGO_W, LOGO_H), Image.LANCZOS)

# ── Helpers ───────────────────────────────────────────────
def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        bx = draw.textbbox((0, 0), test, font=font)
        if bx[2] - bx[0] <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines

def lh(draw, font, mult=1.3):
    bx = draw.textbbox((0, 0), "Ag", font=font)
    return int((bx[3] - bx[1]) * mult)

def block_h(draw, text, font, lhm=1.3):
    return lh(draw, font, lhm) * len(wrap(draw, text, font, TEXT_W))

# ── Renderer ──────────────────────────────────────────────
# Element types:
#   ("t", text, font, color, lhm)
#   ("s", px)

def render(elements, out_path):
    img  = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    total = sum(
        el[1] if el[0] == "s"
        else block_h(draw, el[1], el[2], el[4])
        for el in elements
    )
    content_h = CONTENT_BOT - CONTENT_TOP
    y = CONTENT_TOP + max(0, (content_h - total) // 2)

    for el in elements:
        if el[0] == "s":
            y += el[1]
        else:
            _, text, font, color, lhm = el
            step = lh(draw, font, lhm)
            for line in wrap(draw, text, font, TEXT_W):
                draw.text((MARGIN, y), line, font=font, fill=color)
                y += step

    # Wordmark — bottom centre, small
    lx = (SIZE - LOGO.size[0]) // 2
    ly = SIZE - LOGO.size[1] - 72
    img.paste(LOGO, (lx, ly), LOGO)

    img.save(out_path, "PNG")
    print(f"  ✓  {os.path.basename(out_path)}")

# ── Type system (Inter only) ──────────────────────────────
H_HOOK   = F("black",     104)   # Slide-01 punchline (gold)
H_LARGE  = F("black",     88)    # Slide-05 dominant headline (gold)
H_HEAD   = F("extrabold", 64)    # Hero white headlines
H_STMT   = F("extrabold", 56)    # Statement headlines
PUNCH    = F("black",     58)    # Gold punchlines (replaces serif punchlines)
SUB      = F("semibold",  48)    # White landing lines
SUB2     = F("semibold",  46)
BODY     = F("regular",   42)    # Muted body
BODYSM   = F("regular",   38)

# ── Slides ────────────────────────────────────────────────
slides = {

  "slide-01.png": [
    ("t", "Your business isn't the problem.",        H_HEAD, WHITE, 1.3),
    ("s", 80),
    ("t", "Your brand is.",                          H_HOOK, GOLD,  1.2),
  ],

  "slide-02.png": [
    ("t", "Before any conversation happens, someone has already made a decision about you.", H_STMT, WHITE, 1.35),
    ("s", 56),
    ("t", "They looked at your website.",            BODY,  MUTED, 1.45),
    ("t", "They read how you describe what you do.", BODY,  MUTED, 1.45),
    ("t", "They saw your visual identity.",          BODY,  MUTED, 1.45),
    ("s", 56),
    ("t", "And they decided whether you were worth their time.", SUB, WHITE, 1.3),
  ],

  "slide-03.png": [
    ("t", "Most business owners lose deals they never knew they were in.", H_STMT, WHITE, 1.35),
    ("s", 48),
    ("t", "Not because of price.",                   BODY,  MUTED, 1.45),
    ("t", "Not because of the product.",             BODY,  MUTED, 1.45),
    ("s", 72),
    ("t", "They don't trust it enough to take the next step.", PUNCH, GOLD, 1.3),
  ],

  "slide-04.png": [
    ("t", "The gap is almost always the same.",      H_STMT, WHITE, 1.3),
    ("s", 48),
    ("t", "The business is real.",                   BODY,  MUTED, 1.45),
    ("t", "The brand doesn't match it.",             BODY,  MUTED, 1.45),
    ("s", 52),
    ("t", "You've built something that works.",      SUB2,  WHITE, 1.3),
    ("t", "Your brand still looks like you're figuring it out.", PUNCH, GOLD, 1.3),
  ],

  "slide-05.png": [
    ("t", "Brand. Website. Positioning.",            H_LARGE, GOLD,  1.2),
    ("s", 60),
    ("t", "Not three separate projects.",            BODYSM, MUTED, 1.5),
    ("t", "One system.",                             BODYSM, MUTED, 1.5),
    ("s", 60),
    ("t", "When they work together, the quality of conversation changes before you say a word.", SUB2, WHITE, 1.35),
  ],

  "slide-06.png": [
    ("t", "We work with business owners who have already built something real and need the outside to match the inside.", BODY, MUTED, 1.45),
    ("s", 60),
    ("t", "We don't work with everyone.",            H_STMT, WHITE, 1.3),
    ("s", 20),
    ("t", "If we're a fit, it's worth a conversation.", PUNCH, GOLD, 1.3),
  ],

}

print("\nGenerating final-v8 carousel...\n")
for filename, els in slides.items():
    render(els, os.path.join(HERE, filename))
print("\nDone.\n")
