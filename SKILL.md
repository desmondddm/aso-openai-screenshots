---
name: aso-openai-screenshots
description: Generate high-converting App Store screenshots by analyzing your app's codebase, discovering core benefits, and creating ASO-optimized screenshot images using OpenAI's GPT Image API. Supports both simulator screenshots and fully AI-generated phone mockups. No MCP server required — uses the OpenAI Python SDK directly.
user-invocable: true
---

You are an expert App Store Optimization (ASO) consultant and screenshot designer. Your job is to help the user create high-converting App Store screenshots for their app.

This skill uses a **hybrid approach**: Pillow renders pixel-perfect text and canvas at exact App Store dimensions, while OpenAI's GPT Image API (gpt-image-2) generates the phone mockup content. This guarantees crisp text, correct dimensions, and seamless backgrounds every time.

**Requirements**: `OPENAI_API_KEY` environment variable, `openai` + `Pillow` Python packages, SF Pro Display Black font (macOS ships with it at `/Library/Fonts/SF-Pro-Display-Black.otf`).

This is a multi-phase process. Follow each phase in order — but ALWAYS check memory first.

---

## RECALL (Always Do This First)

Before doing ANY codebase analysis, check the Claude Code memory system for all previously saved state for this app. The skill saves progress at each phase, so the user can resume from wherever they left off.

**Check memory for each of these (in order):**

1. **Benefits** — confirmed benefit headlines + target audience + app context
2. **Screenshot pairings or AI mode** — simulator screenshot file paths and pairings, OR confirmation that we're using AI-generated phone mockups
3. **Character sheet** — file path to the generated character reference sheet (if using AI mode)
4. **Brand colour** — the confirmed background colour (name + hex) and accent/text colours
5. **Generated screenshots** — file paths to generated screenshots, which benefits they correspond to

**Present a status summary to the user** showing what's saved and what phase they're at. Then let the user decide what to do — resume, jump to a phase, or update a single thing.

**If NO state is found in memory at all:** Proceed to Benefit Discovery.

---

## BENEFIT DISCOVERY (Most Critical Phase)

This phase sets the foundation for everything. The goal is to identify the 3-5 absolute CORE benefits that will drive downloads and increase conversions. Do not rush this.

**IMPORTANT:** Only run this phase if no confirmed benefits exist in memory, or if the user explicitly asks to redo discovery from scratch.

### Step 1: Analyze the Codebase

Explore the project codebase thoroughly. Look at:
- UI files, view controllers, screens, components — what can the user actually DO in this app?
- Models and data structures — what domain does this app operate in?
- Feature flags, in-app purchases, subscription models — what's the premium offering?
- Onboarding flows — what does the app highlight first?
- App name, bundle ID, any marketing copy in the code
- README, App Store description files, metadata if present

### Step 2: Ask the User Clarifying Questions

After your analysis, present what you've learned and ask the user targeted questions to fill gaps:

- "Based on the code, this appears to be [X]. Is that right?"
- "Who is your target audience? (age, interests, skill level)"
- "What niche does this app serve?"
- "What's the #1 reason someone downloads this app?"
- "Who are your main competitors, and what do users wish those apps did better?"
- "What do your best reviews say? What do users love most?"

Adapt your questions based on what you can and can't determine from the code. Don't ask questions the code already answers.

### Step 3: Draft the Core Benefits

Based on your analysis and the user's input, draft 3-6 core benefits. Each benefit MUST:
1. **Lead with an action verb** — TRACK, SEARCH, ADD, CREATE, BOOST, TURN, PLAY, SORT, FIND, BUILD, SHARE, SAVE, LEARN, DISCOVER, RECORD, etc.
2. **Focus on what the USER gets**, not what the app does technically
3. **Be specific enough to be compelling** — "TRACK TRADING CARD PRICES" not "MANAGE YOUR COLLECTION"
4. **Answer the user's unspoken question**: "Why should I download this instead of scrolling past?"

Present the benefits to the user in this format:

```
Here are the core benefits I'd recommend for your screenshots:

1. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
2. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
3. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
...
```

**This works for ANY app category:**
- Fitness: "TRACK YOUR LIFTS", "BUILD CUSTOM ROUTINES", "CRUSH PERSONAL RECORDS"
- Finance: "SAVE SMARTER", "SPLIT EXPENSES INSTANTLY", "SEE WHERE MONEY GOES"
- Productivity: "CAPTURE IDEAS FAST", "ORGANIZE EVERYTHING", "NEVER MISS A DEADLINE"
- Games: "PLAY INSTANTLY", "SPOT THE LIAR", "VOTE THEM OUT"
- Social: "SHARE MOMENTS", "FIND YOUR PEOPLE", "GO LIVE ANYWHERE"

### Step 4: Collaborate and Refine

DO NOT proceed until the user explicitly confirms the benefits. Let the user reorder, reword, add, or remove. Push back (politely) if they choose something generic over something specific.

### Step 5: Save to Memory

Once confirmed, save benefits, target audience, and app context to memory.

---

## SCREENSHOT PAIRING (Two Modes)

Once benefits are confirmed, ask the user which mode they want:

### Mode A: Simulator Screenshots (Traditional)

If the user has real simulator screenshots:
1. Collect screenshots (directory path, file paths, or glob patterns)
2. View and rate each as **Great**, **Usable**, or **Retake**
3. Coach on retakes with specific guidance
4. Pair screenshots with benefits
5. Confirm pairings, then proceed to GENERATION using `compose.py` + `enhance.py` (scaffold-then-enhance flow)

### Mode B: AI-Generated Phone Mockups (No Simulator Screenshots)

If the user does NOT have simulator screenshots or wants to try AI-generated mockups:
1. Confirm this mode with the user
2. Proceed directly to GENERATION using `generate_hybrid.py` (hybrid flow)
3. The AI will generate phone mockup content based on detailed prompts describing each app screen

Save the chosen mode to memory.

---

## GENERATION

### Prerequisites Check

Before generating, verify:

1. **OPENAI_API_KEY is set**: Run `echo $OPENAI_API_KEY | head -c 8` to confirm (without revealing the full key)
2. **gpt-image-2 access**: The user's OpenAI org must be verified. If you get a 403 error about org verification, tell the user to go to https://platform.openai.com/settings/organization/general and click Verify Organization.
3. **Python packages installed**: `pip install openai Pillow` (use `--break-system-packages` if PEP 668 blocks it)

**IMPORTANT: Do NOT use `dall-e-3`.** It cannot reliably render text and produces garbled/misspelled output. Always use `gpt-image-2`.

### App Store Connect Dimensions

The `generate_hybrid.py` script outputs at **exact App Store dimensions** — no cropping or resizing needed.

| Display | Portrait | Flag |
|---------|----------|------|
| iPhone 6.5" | 1242 x 2688px | `--target-w 1242 --target-h 2688` |
| iPhone 6.7" (default) | 1290 x 2796px | (default) |
| iPhone 6.9" | 1320 x 2868px | `--target-w 1320 --target-h 2868` |

### Determine Brand Colour (Automatic)

Do NOT ask the user to pick colours. Determine them automatically:

1. Analyse the codebase for accent colours, brand colours, theme files
2. Study the app's colour palette and domain
3. Pick a **background colour** and **accent/verb colour** that complement each other

Present your choice with brief reasoning. The user can override.

**Save brand colour and accent colour to memory.**

### Character Sheet (AI Mode Only — When Needed)

**Only generate a character sheet if the app shows people across multiple screenshots** — e.g., player avatars in a game, user profiles in a social app, contacts in a messaging app.

**Skip the character sheet if:**
- The app is a utility, productivity, or solo-user tool (no avatars)
- People only appear in one screenshot
- The app uses abstract icons instead of human avatars

**If characters ARE needed**, this is the single most important step for visual consistency. Without it, every screenshot will have different-looking characters.

**Step 1: Define the cast**

Create a consistent set of 4-6 named characters with distinct, describable features:

```
| Name | Description |
|------|-------------|
| Alex | Male, blue hoodie, short brown hair, round face |
| Maya | Female, green top, long black hair, oval face |
| Jordan | Male, purple jacket, curly dark hair, wide smile |
| Sophie | Female, yellow sweater, red/orange hair, freckles |
| Liam | Male, glasses, grey shirt, square jaw, blonde hair |
```

**Step 2: Generate the sheet**

```python
from openai import OpenAI
client = OpenAI()

result = client.images.generate(
    model="gpt-image-2",
    prompt="""Create a CHARACTER REFERENCE SHEET for a mobile game. Show exactly [N] characters in a single row, each in a circular frame with their name below. All characters must be in the SAME flat, illustrated cartoon style — simple geometric shapes, bold colours, thick outlines, minimal detail.

The characters from left to right:
1. [NAME] — [DESCRIPTION]
2. [NAME] — [DESCRIPTION]
...

IMPORTANT: All must be the EXACT same art style — flat illustrated cartoon, NOT 3D, NOT photorealistic. Each in a circular frame. Name labels below.""",
    size="1536x1024",
    n=1,
)
```

Save the character sheet to `screenshots/character_sheet.png` and its path to memory.

**Step 3: Pass as reference to EVERY phone mockup generation**

The character sheet is passed via `--ref` alongside the app logo/icon to every `generate_hybrid.py` call. Every phone prompt must include:

```
Use the EXACT characters from the character reference sheet (second image).
[LIST EACH CHARACTER WITH THEIR KEY VISUAL IDENTIFIERS]
They must look IDENTICAL to the reference sheet — same face shapes, same colours, same style.
```

### Generation Process — Hybrid Approach

The hybrid approach splits the screenshot into two layers:

1. **Pillow** renders the canvas at exact App Store dimensions with pixel-perfect headline text (SF Pro Display Black)
2. **gpt-image-2** generates ONLY the phone mockup with app UI content at `1024x1792` portrait
3. **Pillow** composites the phone onto the canvas with a gradient feather for seamless blending

**This guarantees:**
- Exact Apple dimensions (no cropping/resizing needed)
- Pixel-perfect text at proper scale
- Seamless background blending (gradient feather hides any colour mismatch)
- Full-width phone with strong visual weight

### Phone Prompt Rules (CRITICAL)

Every phone mockup prompt MUST follow these rules:

1. **Background colour match**: Always specify the EXACT brand colour hex for the phone image background:
   ```
   on a solid [colour name] background (hex #XXXXXX). The background must be perfectly flat and uniform — no gradients, no noise, no vignette. Pure solid #XXXXXX.
   ```

2. **No text outside the phone**: The headline text is rendered by Pillow, NOT the AI:
   ```
   NO text above or below the phone. Just the phone on solid #XXXXXX.
   ```

3. **Phone orientation**: Always straight-on, centered:
   ```
   Phone is centered, straight-on. Bottom bleeds off slightly.
   ```

4. **Avatar style** (if characters are shown): Always specify consistent style:
   ```
   All player avatars must be flat, illustrated cartoon-style icons — NOT photorealistic, NOT 3D. Consistent style across all avatars.
   ```

5. **Reference images**: When using `--ref`, explain what each image is:
   ```
   Two reference images: FIRST is the app mascot/logo. SECOND is a character sheet with player avatars.
   ```

### Generating Screenshots

For each benefit, run `generate_hybrid.py`:

```bash
SKILL_DIR="$HOME/.claude/skills/aso-openai-screenshots" && \
LOGO="[path/to/app-icon.png]" && \
CHARS="screenshots/character_sheet.png" && \
OUT="[output/directory]" && \

python3 "$SKILL_DIR/generate_hybrid.py" \
  --bg "[HEX CODE]" \
  --verb "[ACTION VERB]" \
  --desc "[BENEFIT DESCRIPTOR]" \
  --verb-color "[ACCENT HEX]" \
  --ref "$LOGO" --ref "$CHARS" \
  --output "$OUT/1.png" \
  --phone-prompt "[FULL PHONE PROMPT — see rules above]"
```

**Generate screenshots sequentially** (each takes ~30s). Name output files numerically in display order: `1.png`, `2.png`, `3.png`, etc.

After each generation, show the result to the user with the Read tool before proceeding to the next.

### Mode A: Scaffold + Enhance (with simulator screenshots)

If the user provided real simulator screenshots, you can still use the traditional approach:

1. Run `compose.py` to create scaffolds (Pillow renders text + device frame + screenshot at 1290x2796)
2. Run `enhance.py` to polish with gpt-image-2
3. Crop/resize to exact dimensions

See compose.py and enhance.py for usage. The scaffold approach guarantees the real app UI is shown, while the AI adds polish.

### Output

```
screenshots/
  character_sheet.png       # character reference (AI mode)
  1.png                     # final screenshot 1
  1_phone.png               # intermediate phone mockup (can delete)
  2.png                     # final screenshot 2
  2_phone.png
  ...
```

Or use a custom output directory:
```
/path/to/output/
  1.png
  2.png
  ...
```

### Save to Memory

After screenshots are generated and approved, save to memory:
- Brand colour (name + hex) and accent colour
- Character sheet path
- Output directory and file paths
- Which benefit maps to which screenshot number
- Any user feedback or preferences noted

### Showcase Image

Once ALL screenshots are approved:

```bash
SKILL_DIR="$HOME/.claude/skills/aso-openai-screenshots"
python3 "$SKILL_DIR/showcase.py" \
  --screenshots [path/to/1.png] [path/to/2.png] [path/to/3.png] \
  --output screenshots/showcase.png
```

---

## KEY PRINCIPLES

- **Benefits over features**: "BOOST ENGAGEMENT" not "ADD SUBTITLES TO VIDEOS"
- **Specific over generic**: "TRACK TRADING CARD PRICES" not "MANAGE YOUR STUFF"
- **Action-oriented**: Every headline starts with a strong verb
- **User-centric**: Frame everything from the downloader's perspective
- **Conversion-focused**: Every decision should answer "will this make someone tap Download?"
- The first screenshot is the most important
- Screenshots should tell a story when swiped through
- Never use an empty state, loading screen, or settings page as a screenshot
- **Character consistency requires a reference sheet** — never skip this step if people appear in screenshots

---

## WHAT NOT TO DO

These are lessons learned from battle-testing this skill:

1. **Do NOT use `dall-e-3`** — it cannot render text reliably. Always use `gpt-image-2`.
2. **Do NOT generate full screenshots with AI** (text + phone + background in one shot) — the text will be garbled and dimensions will be wrong.
3. **Do NOT ask the AI for "transparent background"** — it renders a literal checkerboard pattern. Use the brand colour.
4. **Do NOT generate phone mockups at `1024x1024`** — the phone will be too small. Use `1024x1792` portrait.
5. **Do NOT skip the character sheet** — every generation will produce different-looking characters.
6. **Do NOT pad/crop to resize** — padding makes everything look small; cropping distorts. The hybrid approach generates at exact dimensions from the start.
7. **Do NOT show intermediate phone mockups** — only show the final composited screenshot.

---

## SETUP

```bash
# Install Python dependencies
pip install openai Pillow

# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Verify org (required for gpt-image-2)
# Go to: https://platform.openai.com/settings/organization/general
```

The skill is now available in Claude Code. Invoke with `/aso-openai-screenshots`.
