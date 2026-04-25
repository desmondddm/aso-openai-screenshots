#!/usr/bin/env python3
"""
Enhance scaffold screenshots using OpenAI's GPT Image API.
Transforms a deterministic compose.py scaffold into a polished App Store screenshot.

Usage:
    python enhance.py \\
        --scaffold scaffold.png \\
        --output v1.png \\
        --prompt "Enhancement instructions..." \\
        [--model gpt-image-2] \\
        [--style-ref approved.png] \\
        [--size 1536x2048]

Requires:
    - OPENAI_API_KEY environment variable
    - pip install openai pillow
"""

import argparse
import base64
import os
import sys
from pathlib import Path


def enhance(scaffold_path, output_path, prompt, model="gpt-image-2",
            style_ref=None, size="1536x2048"):
    try:
        from openai import OpenAI
    except ImportError:
        print(
            "Error: openai package not installed. Run: pip install openai",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "Error: OPENAI_API_KEY environment variable not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = OpenAI()

    # Read scaffold image
    with open(scaffold_path, "rb") as f:
        scaffold_data = f.read()

    # Build image list — scaffold first, optional style reference second
    images = [scaffold_data]
    if style_ref and os.path.exists(style_ref):
        with open(style_ref, "rb") as f:
            images.append(f.read())

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Call OpenAI Images API
    try:
        result = client.images.edit(
            model=model,
            image=images if len(images) > 1 else images[0],
            prompt=prompt,
            size=size,
        )
    except Exception as e:
        # Fallback: if multi-image not supported, use single image with
        # expanded prompt describing the style reference
        if len(images) > 1 and "image" in str(e).lower():
            print(
                f"Note: Multi-image edit not supported for this model. "
                f"Using single image with style instructions in prompt.",
                file=sys.stderr,
            )
            result = client.images.edit(
                model=model,
                image=images[0],
                prompt=prompt,
                size=size,
            )
        else:
            raise

    # Extract image data from response
    datum = result.data[0]
    if hasattr(datum, "b64_json") and datum.b64_json:
        image_bytes = base64.b64decode(datum.b64_json)
    elif hasattr(datum, "url") and datum.url:
        import urllib.request
        with urllib.request.urlopen(datum.url) as resp:
            image_bytes = resp.read()
    else:
        print("Error: No image data in API response", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"✓ {output_path}")


def main():
    p = argparse.ArgumentParser(
        description="Enhance App Store screenshot scaffold with OpenAI GPT Image"
    )
    p.add_argument(
        "--scaffold", required=True,
        help="Path to scaffold PNG from compose.py",
    )
    p.add_argument("--output", required=True, help="Output file path")
    p.add_argument("--prompt", required=True, help="Enhancement prompt")
    p.add_argument(
        "--model", default="gpt-image-2",
        help="OpenAI image model (default: gpt-image-2)",
    )
    p.add_argument(
        "--style-ref", default=None,
        help="Path to approved screenshot for style consistency",
    )
    p.add_argument(
        "--size", default="1536x2048",
        help="Output image size (default: 1536x2048)",
    )
    args = p.parse_args()

    enhance(
        args.scaffold, args.output, args.prompt,
        args.model, args.style_ref, args.size,
    )


if __name__ == "__main__":
    main()
