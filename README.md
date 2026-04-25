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
- **Any OS** — the skill bundles [Inter Display Black](https://rsms.me/inter/) as a fallback font. On macOS, it automatically uses SF Pro Display Black if available (ships with macOS). See [Font Setup](#font-setup) for details.

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

## Font Setup

The skill automatically picks the best available font:

| Priority | Font | Where it comes from |
|----------|------|-------------------|
| 1st | **SF Pro Display Black** | Ships with macOS (`/Library/Fonts/SF-Pro-Display-Black.otf`) |
| 2nd | **Inter Display Black** | Bundled in `assets/InterDisplay-Black.ttf` (works on all platforms) |

**macOS users** — SF Pro Display Black is already installed. No action needed. It's Apple's system font and looks best on App Store screenshots.

**Linux/Windows users** — the skill falls back to Inter Display Black automatically. No configuration needed.

**(Optional) Install SF Pro on non-Mac systems** — download from [Apple's developer fonts page](https://developer.apple.com/fonts/) and place it at the path expected by the script, or update `_SF_PRO` in `generate_hybrid.py`.

## Usage

`cd` into any app project directory and run:

```
/aso-openai-screenshots
```

## What the Skill Does (Step by Step)

### Phase 1: Benefit Discovery

The skill starts by **reading your codebase** to understand what your app does:

- Scans UI files, components, view controllers, and screens to identify features
- Reads models and data structures to understand the domain
- Checks for in-app purchases, subscriptions, and premium features
- Looks at onboarding flows, app metadata, and any marketing copy

It then **presents what it learned** and asks clarifying questions:

- "Based on the code, this appears to be [X]. Is that right?"
- "Who is your target audience?"
- "What's the #1 reason someone downloads this app?"
- "Who are your main competitors?"
- "What do your best reviews say?"

Based on this, it **drafts 3-6 benefit headlines** — each starting with an action verb:

| Category | Example Benefits |
|----------|-----------------|
| Fitness | TRACK YOUR LIFTS, BUILD CUSTOM ROUTINES, CRUSH PERSONAL RECORDS |
| Finance | SAVE SMARTER, SPLIT EXPENSES INSTANTLY, SEE WHERE MONEY GOES |
| Productivity | CAPTURE IDEAS FAST, ORGANIZE EVERYTHING, NEVER MISS A DEADLINE |
| Games | PLAY INSTANTLY, SPOT THE LIAR, VOTE THEM OUT |
| Social | SHARE MOMENTS, FIND YOUR PEOPLE, GO LIVE ANYWHERE |

You review, reorder, reword, and confirm before anything is generated.

### Phase 2: Mode Selection

Choose how the phone content is created:

- **Mode A (Simulator Screenshots)** — You provide real screenshots from the iOS Simulator. The skill composites them into device frames.
- **Mode B (AI-Generated)** — No screenshots needed. The AI generates phone mockup content based on detailed descriptions of each app screen.

### Phase 3: Brand Colour

The skill **auto-detects your brand colour** by analyzing:
- Accent colours, tint colours, and theme files in your codebase
- The app's colour palette and domain personality

It presents its choice with reasoning. You can override if you prefer a different colour.

### Phase 4: Character Sheet (When Needed)

**Only for apps that show people across multiple screenshots** (games with player avatars, social apps with profiles, etc.).

The skill generates a character reference sheet — a single image with all named characters in a consistent cartoon style. This sheet is then passed as a reference to every screenshot generation, ensuring the same characters appear identically across the full set.

**Skipped automatically** for utility apps, productivity tools, and solo-user apps that don't show human avatars.

### Phase 5: Screenshot Generation

For each benefit, the skill runs the hybrid pipeline:

1. **Pillow** creates a 1290x2796 canvas with your headline text rendered in SF Pro Display Black
2. **gpt-image-2** generates a phone mockup showing the relevant app screen (with your logo and character sheet as references)
3. **Pillow** composites the phone onto the canvas with a gradient feather blend

Each screenshot takes ~30 seconds. The skill shows you each result and lets you approve or request changes before moving to the next.

### Phase 6: Output

Final screenshots are saved as numbered PNGs at exact App Store Connect dimensions — ready to upload directly. No cropping, resizing, or post-processing needed.

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
