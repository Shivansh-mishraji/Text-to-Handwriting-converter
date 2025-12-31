"""
Simple script: convert text into a handwriting-like PNG image using Pillow.

This minimal script is written to be easy to read. It applies small
random rotations and vertical jitter per character to simulate a
handwritten look. For best results, pass a handwriting TTF via
`--font path/to/font.ttf`.

Usage examples:
  pip install pillow
  python file.py --text "Hello world" --output note.png
  python file.py --text "Line1\nLine2" --font C:\\Windows\\Fonts\\seguisb.ttf --output note.png
"""

import argparse
import sys
import random
from PIL import Image, ImageDraw, ImageFont


def render_handwritten(text, out_path, font_path=None, font_size=32, color=(10, 10, 10)):
    # Split into lines
    lines = text.splitlines() or [text]

    # Load font if provided, else use default
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()

    # Measure image size
    dummy = Image.new('RGB', (1, 1))
    d = ImageDraw.Draw(dummy)
    max_w = 0
    total_h = 0
    line_spacing = int(font_size * 0.6)
    metrics = []
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        metrics.append((w, h))
        if w > max_w:
            max_w = w
        total_h += h + line_spacing

    img_w = max_w + 60
    img_h = total_h + 60

    # Paper-like background
    img = Image.new('RGB', (img_w, img_h), (250, 247, 240))
    draw = ImageDraw.Draw(img)

    x_start = 30
    y = 30
    for i, line in enumerate(lines):
        x = x_start
        for ch in line:
            # small random font-size jitter
            jitter = random.randint(-2, 3)
            size = max(12, font_size + jitter)
            try:
                f = ImageFont.truetype(font.path, size) if getattr(font, 'path', None) else font
            except Exception:
                f = font

            # measure char
            bbox = draw.textbbox((0, 0), ch, font=f)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            # draw char to its own image to allow rotation
            char_img = Image.new('RGBA', (w + 8, h + 8), (0, 0, 0, 0))
            cd = ImageDraw.Draw(char_img)
            cd.text((4, 4), ch, font=f, fill=color)

            # rotate and paste
            angle = random.uniform(-12, 12)
            char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)
            y_jitter = random.randint(-3, 3)
            img.paste(char_img, (int(x), int(y + y_jitter)), char_img)

            x += max(1, int(w * 0.9))

        y += metrics[i][1] + line_spacing

    img.save(out_path)


def main():
    parser = argparse.ArgumentParser(description='Convert text to a handwritten-like PNG (simple)')
    parser.add_argument('--text', '-t', help='Text to convert', required=True)
    parser.add_argument('--output', '-o', default='note.png', help='Output PNG filename')
    parser.add_argument('--font', help='Path to a TrueType font (optional)')
    parser.add_argument('--size', type=int, default=32, help='Base font size (default 32)')
    parser.add_argument('--color', default='10,10,10', help="Ink color as 'r,g,b' (default 10,10,10)")

    args = parser.parse_args()

    try:
        color = tuple(int(x) for x in args.color.split(','))
    except Exception:
        color = (10, 10, 10)

    render_handwritten(args.text, args.output, font_path=args.font, font_size=args.size, color=color)
    print(f'Saved handwritten-like image to: {args.output}')


if __name__ == '__main__':
    main()

