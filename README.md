# ASO App Store Screenshots — Claude Code Skill

Generate high-converting App Store screenshots using OpenAI's GPT Image API (`gpt-image-2`). Works with or without simulator screenshots.

![Example screenshots](https://img.shields.io/badge/App_Store-Ready-blue)

## What This Does

This Claude Code skill analyzes your app's codebase, identifies core benefits, and generates professional App Store screenshots — all from the command line.

**Two modes:**
- **With simulator screenshots** — Pillow composites your real app screenshots into device frames with pixel-perfect headlines
- **Without simulator screenshots** — AI generates the phone mockup content, Pillow handles text and layout at exact Apple dimensions

## How It Works (Hybrid Approach)

The skill uses a hybrid approach that combines the best of both worlds:

1. **Pillow** renders pixel-perfect text (SF Pro Display Black) on a canvas at exact App Store dimensions (1290x2796)
2. **gpt-image-2** generates only the phone mockup with app UI at 1024x1792 portrait
3. **Pillow** composites the phone onto the canvas with a gradient feather for seamless blending

This guarantees:
- Exact Apple dimensions — no cropping or resizing needed
- Crisp, readable text every time (never AI-generated text)
- Seamless background blending
- Consistent character appearances via reference sheets

## Requirements

- **Claude Code** (CLI or IDE extension)
- **OpenAI API key** with verified organization (required for `gpt-image-2`)
- **Python 3.10+** with `openai` and `Pillow` packages
- **macOS** with SF Pro Display font (ships with macOS at `/Library/Fonts/SF-Pro-Display-Black.otf`)

## Installation

### 1. Clone into your Claude Code skills directory

```bash
git clone https://github.com/YOUR_USERNAME/aso-openai-screenshots ~/.claude/skills/aso-openai-screenshots
```

### 2. Install Python dependencies

```bash
pip install openai Pillow
```

### 3. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist across sessions.

### 4. Verify your OpenAI organization

`gpt-image-2` requires organization verification. Go to:
https://platform.openai.com/settings/organization/general

Click **Verify Organization** and wait up to 15 minutes.

### 5. (Optional) Generate the device frame asset

Only needed if using Mode A (simulator screenshots with `compose.py`):

```bash
cd ~/.claude/skills/aso-openai-screenshots && python3 generate_frame.py
```

## Usage

In any project directory, run:

```
/aso-openai-screenshots
```

The skill will:
1. Analyze your codebase to understand what your app does
2. Propose 3-6 benefit headlines (action verb + descriptor)
3. Determine brand colours automatically
4. Generate a character reference sheet (for avatar consistency)
5. Generate each screenshot using the hybrid approach
6. Output App Store-ready PNGs at exact Apple dimensions

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill instructions (loaded by Claude Code) |
| `generate_hybrid.py` | Hybrid generator: Pillow canvas + AI phone + gradient feather |
| `compose.py` | Scaffold generator: Pillow-only canvas with device frame (Mode A) |
| `enhance.py` | AI enhancer: sends scaffold to gpt-image-2 for polish (Mode A) |
| `generate_frame.py` | One-time device frame PNG generator |
| `showcase.py` | Combines final screenshots into a showcase image |
| `assets/` | Pre-generated device frame template |

## Output

Screenshots are saved at exact App Store Connect dimensions:

| Display | Dimensions |
|---------|-----------|
| iPhone 6.5" | 1242 x 2688px |
| iPhone 6.7" (default) | 1290 x 2796px |
| iPhone 6.9" | 1320 x 2868px |

## Lessons Learned

These are hard-won lessons from battle-testing this skill:

1. **Never use `dall-e-3`** — it cannot render text reliably
2. **Never generate full screenshots with AI** — text will be garbled, dimensions will be wrong
3. **Never ask AI for "transparent background"** — it renders a literal checkerboard
4. **Always generate phone mockups at `1024x1792`** — `1024x1024` makes the phone too small
5. **Always generate a character sheet first** — without it, every screenshot has different-looking characters
6. **Never pad/crop to resize** — the hybrid approach generates at exact dimensions from the start

## Example Output

```
/output/directory/
  character_sheet.png    # Character reference (AI mode)
  1.png                  # PLAY INSTANTLY — 1290x2796
  2.png                  # SPOT THE LIAR — 1290x2796
  3.png                  # DEBATE ANSWERS — 1290x2796
  ...
```

## License

MIT
