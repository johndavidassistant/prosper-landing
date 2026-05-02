#!/usr/bin/env python3
"""
GO BIG — Instagram Carousel / Final
Black canvas · Gold Playfair punch lines · Inter body · GO BIG. wordmark footer
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Dimensions & colour ───────────────────────────────────
SIZE        = 1080
MARGIN      = 130           # wider than v1 (was 108)
CONTENT_TOP = 120
CONTENT_BOT = 900           # wordmark sits below this
TEXT_W      = SIZE - 2 * MARGIN
BG          = (0, 0, 0)
WHITE       = (255, 255, 255)
GOLD        = (200, 149, 46)
MUTED       = (120, 120, 120)   # less gray than v1 — better contrast

# ── Font paths ────────────────────────────────────────────
LF = os.path.expanduser("~/Library/Fonts")
def F(family, weight, size):
    files = {
        ("inter", "black"):     "Inter_28pt-Black.ttf",
        ("inter", "extrabold"): "Inter_28pt-ExtraBold.ttf",
        ("inter", "bold"):      "Inter_28pt-Bold.ttf",
        ("inter", "semibold"):  "Inter_28pt-SemiBold.ttf",
        ("inter", "medium"):    "Inter_28pt-Medium.ttf",
        ("inter", "regular"):   "Inter_18pt-Regular.ttf",
        ("playfair", "black"):  "PlayfairDisplay-Black.ttf",
        ("playfair", "bold"):   "PlayfairDisplay-Bold.ttf",
    }
    return ImageFont.truetype(os.path.join(LF, files[(family, weight)]), size)

# ── Wordmark ──────────────────────────────────────────────
LOGO_SRC = os.path.expanduser(
    "~/AI-OS/projects/prosper-landing/assets/gobig/approved/logo-v7-horizontal-transparent.png"
)
# Render at 300px wide (aspect 900:270 → 300×90)
_raw  = Image.open(LOGO_SRC).convert("RGBA")
LOGO  = _raw.resize((300, 90), Image.LANCZOS)

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

# ── Slide renderer ────────────────────────────────────────
# Element types:
#   ("t", text, font, color, lhm)   — text block
#   ("s", px)                        — spacer

def render(elements, out_path):
    img  = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # Measure
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

    # Wordmark — bottom centre
    lx = (SIZE - LOGO.size[0]) // 2
    ly = SIZE - LOGO.size[1] - 58
    img.paste(LOGO, (lx, ly), LOGO)

    img.save(out_path, "PNG")
    print(f"  ✓  {os.path.basename(out_path)}")

# ── Slide definitions ─────────────────────────────────────
OUT = os.path.dirname(os.path.abspath(__file__))

# Font instances (pre-built for clarity)
IEB64 = F("inter",    "extrabold", 64)   # Inter ExtraBold headline
IEB56 = F("inter",    "extrabold", 56)
ISB48 = F("inter",    "semibold",  48)
ISB46 = F("inter",    "semibold",  46)
IR42  = F("inter",    "regular",   42)
IR38  = F("inter",    "regular",   38)
PB96  = F("playfair", "black",     96)   # Playfair punch line — large
PB80  = F("playfair", "black",     80)
PB58  = F("playfair", "black",     58)

slides = {

  "slide-01.png": [
    # Hook: White setup → Gold punchline
    ("t", "Your business isn't the problem.",        IEB64, WHITE, 1.3),
    ("s", 80),   # generous pause before punchline
    ("t", "Your brand is.",                          PB96,  GOLD,  1.3),
  ],

  "slide-02.png": [
    # Opening statement
    ("t", "Before any conversation happens, someone has already made a decision about you.", IEB56, WHITE, 1.35),
    ("s", 56),
    # Evidence block — muted list
    ("t", "They looked at your website.",            IR42,  MUTED, 1.45),
    ("t", "They read how you describe what you do.", IR42,  MUTED, 1.45),
    ("t", "They saw your visual identity.",          IR42,  MUTED, 1.45),
    ("s", 56),
    # Landing line
    ("t", "And they decided whether you were worth their time.", ISB48, WHITE, 1.3),
  ],

  "slide-03.png": [
    # Setup
    ("t", "Most business owners lose deals they never knew they were in.", IEB56, WHITE, 1.35),
    ("s", 48),
    # Reasons — muted
    ("t", "Not because of price.",                   IR42,  MUTED, 1.45),
    ("t", "Not because of the product.",             IR42,  MUTED, 1.45),
    ("s", 72),   # big pause before punchline — fixes "spacing above gold line"
    # Gold punchline
    ("t", "They don't trust it enough to take the next step.", PB58, GOLD, 1.35),
  ],

  "slide-04.png": [
    # Statement
    ("t", "The gap is almost always the same.",      IEB56, WHITE, 1.3),
    ("s", 48),
    # Contrast — muted
    ("t", "The business is real.",                   IR42,  MUTED, 1.45),
    ("t", "The brand doesn't match it.",             IR42,  MUTED, 1.45),
    ("s", 52),
    # White then gold — two-part punch
    ("t", "You've built something that works.",      ISB46, WHITE, 1.3),
    ("t", "Your brand still looks like you're figuring it out.", PB58, GOLD, 1.35),
  ],

  "slide-05.png": [
    # Dominant headline — Playfair, fills the eye
    ("t", "Brand. Website. Positioning.",            PB80,  GOLD,  1.3),
    ("s", 60),
    # Contrast — muted reframe
    ("t", "Not three separate projects.",            IR38,  MUTED, 1.5),
    ("t", "One system.",                             IR38,  MUTED, 1.5),
    ("s", 60),
    # Payoff — white, semibold
    ("t", "When they work together, the quality of conversation changes before you say a word.", ISB46, WHITE, 1.35),
  ],

  "slide-06.png": [
    # Context — muted, sets the filter
    ("t", "We work with business owners who have already built something real and need the outside to match the inside.", IR42, MUTED, 1.45),
    ("s", 60),
    # Qualifier — white
    ("t", "We don't work with everyone.",            IEB56, WHITE, 1.3),
    ("s", 20),
    # Close — Playfair Gold, largest weight: this IS the close
    ("t", "If we're a fit, it's worth a conversation.", PB58, GOLD, 1.3),
  ],

}

print("\nGenerating final carousel...\n")
for filename, els in slides.items():
    render(els, os.path.join(OUT, filename))
print("\nDone.\n")
