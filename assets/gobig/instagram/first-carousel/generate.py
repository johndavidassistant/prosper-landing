#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# ── Config ────────────────────────────────────────────────
SIZE        = 1080
MARGIN      = 108          # left / right padding
BG          = (0, 0, 0)
WHITE       = (255, 255, 255)
GOLD        = (200, 149, 46)
MUTED       = (140, 140, 140)
CONTENT_TOP = 130          # usable content starts here
CONTENT_BOT = 888          # usable content ends here (logo below)
TEXT_W      = SIZE - 2 * MARGIN

FONTS_DIR = os.path.expanduser("~/Library/Fonts")

def F(weight, size):
    files = {
        "black":     "Inter_28pt-Black.ttf",
        "extrabold": "Inter_28pt-ExtraBold.ttf",
        "bold":      "Inter_28pt-Bold.ttf",
        "semibold":  "Inter_28pt-SemiBold.ttf",
        "medium":    "Inter_28pt-Medium.ttf",
        "regular":   "Inter_18pt-Regular.ttf",
    }
    return ImageFont.truetype(os.path.join(FONTS_DIR, files[weight]), size)

# ── Logo ──────────────────────────────────────────────────
def build_logo(size=76):
    src = os.path.expanduser(
        "~/AI-OS/projects/prosper-landing/assets/gobig/logo-v6-monogram-white-1080.png"
    )
    raw = Image.open(src).resize((size, size), Image.LANCZOS).convert("RGBA")
    pixels = list(raw.getdata())
    new = [(255, 255, 255, 255 - int((p[0]+p[1]+p[2])/3)) for p in pixels]
    raw.putdata(new)
    return raw

LOGO = build_logo()

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

def line_h(draw, font, mult=1.35):
    bx = draw.textbbox((0, 0), "Ag", font=font)
    return int((bx[3] - bx[1]) * mult)

def block_height(draw, text, font, lhm=1.35):
    lines = wrap(draw, text, font, TEXT_W)
    return line_h(draw, font, lhm) * len(lines)

# ── Render engine ─────────────────────────────────────────
# Each element in a slide spec:
#   ("text", text_str, font, color, line_height_mult)
#   ("spacer", px)

def render_slide(elements, out_path):
    img  = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # Measure total height
    total = 0
    for el in elements:
        if el[0] == "spacer":
            total += el[1]
        else:
            _, text, font, color, lhm = el
            total += block_height(draw, text, font, lhm)

    content_h = CONTENT_BOT - CONTENT_TOP
    y = CONTENT_TOP + max(0, (content_h - total) // 2)

    for el in elements:
        if el[0] == "spacer":
            y += el[1]
        else:
            _, text, font, color, lhm = el
            lh = line_h(draw, font, lhm)
            for line in wrap(draw, text, font, TEXT_W):
                draw.text((MARGIN, y), line, font=font, fill=color)
                y += lh

    # Logo — bottom center
    lx = (SIZE - LOGO.size[0]) // 2
    ly = SIZE - LOGO.size[1] - 64
    img.paste(LOGO, (lx, ly), LOGO)

    img.save(out_path, "PNG")
    print(f"  ✓  {os.path.basename(out_path)}")

# ── Slide definitions ─────────────────────────────────────

OUT = os.path.dirname(os.path.abspath(__file__))

slides = {
    "slide-01.png": [
        ("text", "Your business isn't the problem.",    F("extrabold", 64), WHITE, 1.3),
        ("spacer", 48),
        ("text", "Your brand is.",                      F("black",     88), GOLD,  1.3),
    ],
    "slide-02.png": [
        ("text", "Before any conversation happens,",    F("extrabold", 54), WHITE, 1.3),
        ("text", "someone has already made a decision about you.", F("extrabold", 54), WHITE, 1.3),
        ("spacer", 44),
        ("text", "They looked at your website.",        F("regular",   42), MUTED, 1.4),
        ("text", "They read how you describe what you do.", F("regular", 42), MUTED, 1.4),
        ("text", "They saw your visual identity.",      F("regular",   42), MUTED, 1.4),
        ("spacer", 44),
        ("text", "And they decided whether you were worth their time.", F("semibold", 46), WHITE, 1.35),
    ],
    "slide-03.png": [
        ("text", "Most business owners lose deals they never knew they were in.", F("extrabold", 56), WHITE, 1.3),
        ("spacer", 44),
        ("text", "Not because of price.",               F("regular",   42), MUTED, 1.4),
        ("text", "Not because of the product.",         F("regular",   42), MUTED, 1.4),
        ("spacer", 44),
        ("text", "They don't trust it enough to take the next step.", F("semibold", 52), GOLD, 1.35),
    ],
    "slide-04.png": [
        ("text", "The gap is almost always the same.",  F("extrabold", 54), WHITE, 1.3),
        ("spacer", 44),
        ("text", "The business is real.",               F("regular",   42), MUTED, 1.4),
        ("text", "The brand doesn't match it.",         F("regular",   42), MUTED, 1.4),
        ("spacer", 44),
        ("text", "You've built something that works.",  F("semibold",  52), WHITE, 1.3),
        ("text", "Your brand still looks like you're figuring it out.", F("semibold", 52), GOLD, 1.3),
    ],
    "slide-05.png": [
        ("text", "Brand. Website. Positioning.",        F("black",     72), GOLD,  1.3),
        ("spacer", 52),
        ("text", "Not three separate projects.",        F("regular",   42), MUTED, 1.4),
        ("text", "One system.",                         F("regular",   42), MUTED, 1.4),
        ("spacer", 52),
        ("text", "When they work together, the quality of conversation changes before you say a word.", F("semibold", 48), WHITE, 1.35),
    ],
    "slide-06.png": [
        ("text", "We work with business owners who have already built something real and need the outside to match the inside.", F("regular", 42), MUTED, 1.4),
        ("spacer", 52),
        ("text", "We don't work with everyone.",        F("semibold",  52), WHITE, 1.3),
        ("text", "If we're a fit, it's worth a conversation.", F("black", 52), GOLD, 1.3),
    ],
}

print("\nGenerating carousel slides...\n")
for filename, elements in slides.items():
    render_slide(elements, os.path.join(OUT, filename))

print("\nDone. 6 slides generated.\n")
