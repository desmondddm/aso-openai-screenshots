# ASO App Store Screenshots — Claude Code Skill

Generate high-converting App Store screenshots using OpenAI's GPT Image API (`gpt-image-2`). Works with or without simulator screenshots.

## What This Does

This [Claude Code](https://claude.ai/code) skill analyzes your app's codebase, identifies core benefits, and generates professional App Store screenshots — all from the command line.

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

- [Claude Code](https://claude.ai/code) (CLI, desktop app, or IDE extension)
- [OpenAI API key](https://platform.openai.com/api-keys) with **verified organization** (required for `gpt-image-2`)
- Python 3.10+
- **macOS** — the skill uses SF Pro Display Black font which ships with macOS at `/Library/Fonts/SF-Pro-Display-Black.otf`. On Linux/Windows, you'll need to install the font manually and update the `FONT_PATH` in `generate_hybrid.py`.

## Installation

### 1. Clone into your Claude Code skills directory

```bash
git clone https://github.com/desmondddm/aso-openai-screenshots ~/.claude/skills/aso-openai-screenshots
```

### 2. Install Python dependencies

```bash
pip install openai Pillow
```

### 3. Set your OpenAI API key

Get a key from https://platform.openai.com/api-keys, then:

```bash
export OPENAI_API_KEY="sk-..."
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist across sessions.

### 4. Verify your OpenAI organization

`gpt-image-2` requires organization verification. Go to:
https://platform.openai.com/settings/organization/general

Click **Verify Organization** and wait up to 15 minutes for access to propagate.

### 5. (Optional) Generate the device frame asset

Only needed if using Mode A (simulator screenshots with `compose.py`):

```bash
cd ~/.claude/skills/aso-openai-screenshots && python3 generate_frame.py
```

## Usage

`cd` into any app project directory and run:

```
/aso-openai-screenshots
```

The skill will walk you through:

1. **Benefit Discovery** — analyzes your codebase, proposes 3-6 benefit headlines (action verb + descriptor)
2. **Mode Selection** — choose between simulator screenshots or AI-generated phone mockups
3. **Brand Colour** — auto-detected from your codebase, user can override
4. **Character Sheet** — generates a reference sheet so player avatars/characters look consistent across all screenshots
5. **Screenshot Generation** — generates each screenshot using the hybrid approach (~30s per screenshot)
6. **Output** — App Store-ready PNGs at exact Apple dimensions, numbered in display order

## Cost

Each phone mockup generation costs roughly **$0.04–0.08** per image (gpt-image-2 pricing). A full set of 6 screenshots costs approximately **$0.30–0.50**.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill instructions (loaded automatically by Claude Code) |
| `generate_hybrid.py` | Hybrid generator: Pillow canvas + AI phone + gradient feather |
| `compose.py` | Scaffold generator: Pillow-only canvas with device frame (Mode A) |
| `enhance.py` | AI enhancer: sends scaffold to gpt-image-2 for polish (Mode A) |
| `generate_frame.py` | One-time device frame PNG generator |
| `showcase.py` | Combines final screenshots into a showcase image |
| `assets/` | Pre-generated device frame template |

## Output Dimensions

Screenshots are saved at exact App Store Connect dimensions — ready to upload directly:

| Display | Dimensions | Flag |
|---------|-----------|------|
| iPhone 6.5" | 1242 x 2688px | `--target-w 1242 --target-h 2688` |
| iPhone 6.7" (default) | 1290 x 2796px | (default) |
| iPhone 6.9" | 1320 x 2868px | `--target-w 1320 --target-h 2868` |

## Lessons Learned

These are hard-won lessons from battle-testing this skill:

1. **Never use `dall-e-3`** — it cannot render text reliably, output is always garbled
2. **Never generate full screenshots with AI in one shot** — text will be misspelled, dimensions will be wrong
3. **Never ask AI for "transparent background"** — it renders a literal checkerboard pattern
4. **Always generate phone mockups at `1024x1792` portrait** — `1024x1024` makes the phone too small with no visual weight
5. **Always generate a character sheet first** — without it, every screenshot has different-looking characters
6. **Never pad/crop to resize** — padding makes everything look small, cropping distorts. The hybrid approach generates at exact dimensions from the start.
7. **Always match the background colour** — tell the AI the exact hex code for the background around the phone so it blends seamlessly with the Pillow canvas

## Example Output

```
/output/directory/
  character_sheet.png    # Character reference (AI mode)
  1.png                  # PLAY INSTANTLY — 1290x2796
  2.png                  # SPOT THE LIAR — 1290x2796
  3.png                  # DEBATE ANSWERS — 1290x2796
  4.png                  # VOTE THEM OUT — 1290x2796
  5.png                  # UNLOCK 1,600+ — 1290x2796
  6.png                  # PLAY ANYWHERE — 1290x2796
```

## License

MIT
