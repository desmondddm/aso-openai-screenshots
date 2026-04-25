#!/usr/bin/env python3
"""
Hybrid App Store Screenshot Generator
- Pillow renders pixel-perfect canvas at exact App Store dimensions with headline text
- gpt-image-2 generates phone mockup at 1024x1792 (portrait, fills canvas)
- Pillow composites with gradient feather for seamless blending

Usage:
    python3 generate_hybrid.py \
        --bg "#1A0A3B" \
        --verb "PLAY INSTANTLY" \
        --desc "No Downloads for Friends" \
        --phone-prompt "iPhone showing game lobby..." \
        --output screenshots/final/1.png \
        [--ref logo.png] [--ref characters.png] \
        [--verb-color "#F5C518"] [--desc-color white] \
        [--target-w 1290] [--target-h 2796]
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

# ── Default Canvas (App Store Connect iPhone 6.7") ───────────────
DEFAULT_W = 1290
DEFAULT_H = 2796

# ── Typography ───────────────────────────────────────────────────
# Try SF Pro Display Black (macOS), fall back to bundled Inter Display Black
_SF_PRO = "/Library/Fonts/SF-Pro-Display-Black.otf"
_INTER = os.path.join(os.path.dirname(__file__), "assets", "InterDisplay-Black.ttf")
FONT_PATH = _SF_PRO if os.path.exists(_SF_PRO) else _INTER
VERB_SIZE_MAX = 220
VERB_SIZE_MIN = 140
DESC_SIZE = 90
VERB_DESC_GAP = 20
LINE_GAP = 10
TEXT_TOP = 120
TEXT_WIDTH_RATIO = 0.88  # text occupies 88% of canvas width

# ── Phone placement ─────────────────────────────────────────────
PHONE_TOP = 520       # where phone image top edge sits on canvas
FEATHER_HEIGHT = 120  # gradient blend zone at top of phone image


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def fit_font(text, max_w, size_max, size_min):
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    for size in range(size_max, size_min - 1, -4):
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            return font, size
    return ImageFont.truetype(FONT_PATH, size_min), size_min


def word_wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_text(draw, y, text, font, canvas_w, fill="white", max_w=None):
    lines = word_wrap(draw, text, font, max_w) if max_w else [text]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        draw.text((canvas_w // 2, y - bbox[1]), line, fill=fill, font=font, anchor="mt")
        y += h + LINE_GAP
    return y


def generate_phone(prompt, output_path, model="gpt-image-2", refs=None):
    """Generate phone mockup image using OpenAI at 1024x1792 portrait."""
    from openai import OpenAI
    client = OpenAI()

    print(f"  Generating phone mockup (1024x1792)...")

    if refs:
        files = [open(r, "rb") for r in refs]
        try:
            result = client.images.edit(
                model=model,
                image=files if len(files) > 1 else files[0],
                prompt=prompt,
                size="1024x1792",
            )
        finally:
            for f in files:
                f.close()
    else:
        result = client.images.generate(
            model=model,
            prompt=prompt,
            size="1024x1792",
            n=1,
        )

    datum = result.data[0]
    if hasattr(datum, "b64_json") and datum.b64_json:
        img_bytes = base64.b64decode(datum.b64_json)
    elif hasattr(datum, "url") and datum.url:
        import urllib.request
        with urllib.request.urlopen(datum.url) as resp:
            img_bytes = resp.read()
    else:
        print("Error: No image data", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "wb") as f:
        f.write(img_bytes)
    print(f"  Phone mockup saved: {output_path}")


def composite(bg_hex, verb, desc, phone_path, output_path,
              verb_color="#F5C518", desc_color="white",
              canvas_w=DEFAULT_W, canvas_h=DEFAULT_H):
    """Compose final screenshot: text layer + phone layer with gradient blend."""
    bg = hex_to_rgb(bg_hex)
    max_text_w = int(canvas_w * TEXT_WIDTH_RATIO)

    # 1. Create canvas
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (*bg, 255))
    draw = ImageDraw.Draw(canvas)

    # 2. Draw verb — largest text, typically brand accent colour
    verb_font, _ = fit_font(verb.upper(), max_text_w, VERB_SIZE_MAX, VERB_SIZE_MIN)
    y = TEXT_TOP
    y = draw_centered_text(draw, y, verb.upper(), verb_font, canvas_w, fill=verb_color)

    # 3. Draw descriptor — smaller, white
    y += VERB_DESC_GAP
    desc_font = ImageFont.truetype(FONT_PATH, DESC_SIZE)
    draw_centered_text(draw, y, desc.upper(), desc_font, canvas_w,
                       fill=desc_color, max_w=max_text_w)

    # 4. Load and scale phone mockup to fill canvas width
    phone = Image.open(phone_path).convert("RGBA")
    scale = canvas_w / phone.width
    phone_h = int(phone.height * scale)
    phone = phone.resize((canvas_w, phone_h), Image.LANCZOS)

    # 5. Gradient feather mask — fades top edge for seamless blending
    mask = Image.new("L", (canvas_w, phone_h), 255)
    mask_draw = ImageDraw.Draw(mask)
    for i in range(FEATHER_HEIGHT):
        opacity = int(255 * (i / FEATHER_HEIGHT))
        mask_draw.line([(0, i), (canvas_w, i)], fill=opacity)

    phone_r, phone_g, phone_b, phone_a = phone.split()
    blended_alpha = ImageChops.multiply(phone_a, mask)
    phone = Image.merge("RGBA", (phone_r, phone_g, phone_b, blended_alpha))

    # 6. Paste phone (full width, PHONE_TOP position)
    canvas.paste(phone, (0, PHONE_TOP), phone)

    # 7. Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")
    print(f"  Done: {output_path} ({canvas_w}x{canvas_h})")


def main():
    p = argparse.ArgumentParser(description="Hybrid App Store screenshot generator")
    p.add_argument("--bg", required=True, help="Background hex colour (#1A0A3B)")
    p.add_argument("--verb", required=True, help="Action verb headline (PLAY INSTANTLY)")
    p.add_argument("--desc", required=True, help="Benefit descriptor (No Downloads for Friends)")
    p.add_argument("--phone-prompt", required=True, help="Prompt for AI phone mockup generation")
    p.add_argument("--output", required=True, help="Final output path")
    p.add_argument("--ref", action="append", default=None,
                   help="Reference image path — can repeat (e.g. --ref logo.png --ref chars.png)")
    p.add_argument("--verb-color", default="#F5C518", help="Verb text colour (default: gold)")
    p.add_argument("--desc-color", default="white", help="Descriptor text colour")
    p.add_argument("--model", default="gpt-image-2", help="OpenAI model")
    p.add_argument("--target-w", type=int, default=DEFAULT_W, help="Canvas width (default: 1290)")
    p.add_argument("--target-h", type=int, default=DEFAULT_H, help="Canvas height (default: 2796)")
    args = p.parse_args()

    phone_tmp = args.output.replace(".png", "_phone.png")
    generate_phone(args.phone_prompt, phone_tmp, args.model, args.ref)
    composite(args.bg, args.verb, args.desc, phone_tmp, args.output,
              args.verb_color, args.desc_color, args.target_w, args.target_h)


if __name__ == "__main__":
    main()
