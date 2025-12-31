"""Convert text to a handwriting-like PNG (improved, ready-to-use).

Features:
- Uses `pywhatkit.text_to_handwriting` if available for best realism.
- Pillow fallback with word-wrapping, per-character rotation, simulated
  ink thickness and light paper texture.

Usage examples:
  python file.py --text "Hello world" --output note.png
  python file.py --input-file notes.txt --output notes.png --font C:\\Windows\\Fonts\\seguisb.ttf
"""

import argparse
import os
import sys
import random

"""Convert text to a handwriting-like PNG (improved, ready-to-use).

Features:
- Uses `pywhatkit.text_to_handwriting` if available for best realism.
- Pillow fallback with word-wrapping, per-character rotation, simulated
  ink thickness and light paper texture.

Usage examples:
  python file.py --text "Hello world" --output note.png
  python file.py --input-file notes.txt --output notes.png --font C:\\Windows\\Fonts\\seguisb.ttf
"""

import argparse
import os
import sys
import random

from PIL import Image, ImageDraw, ImageFont


try:
    import pywhatkit as _pwk
    HAS_PYWHATKIT = True
except Exception:
    HAS_PYWHATKIT = False


def find_handwriting_font():
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/SegoeScript.ttf",
        "C:/Windows/Fonts/SegoePrint.ttf",
        "C:/Windows/Fonts/BRADHITC.TTF",
        "C:/Windows/Fonts/Bradley.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _fallback(text, out_path, font_path=None, size=48, color=(0, 0, 0), pad=36, max_width=1200):
    # prepare font and measurement helper
    font = ImageFont.truetype(font_path, size) if font_path and os.path.exists(font_path) else ImageFont.load_default()
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    # wrap lines to width
    raw_lines = text.splitlines() or [text]
    wrap_width = max_width - pad * 2
    lines = []
    for raw in raw_lines:
        words = raw.split(" ")
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            bbox = measure.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > wrap_width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)

    # compute image size
    maxw = 0
    heights = []
    for L in lines:
        bbox = measure.textbbox((0, 0), L, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        maxw = max(maxw, w)
        heights.append(h)
    W = min(max(maxw + pad * 2, 400), max_width)
    H = sum(int(h * 1.4) for h in heights) + pad * 2

    # paper background + subtle noise
    img = Image.new("RGB", (W, H), (254, 250, 240))
    px = img.load()
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            if random.random() < 0.02:
                r = max(0, px[j, i][0] - random.randint(6, 18))
                px[j, i] = (r, max(0, r - 2), max(0, r - 6))

    y = pad
    for idx, line in enumerate(lines):
        x = pad
        for ch in line:
            if ch == " ":
                sb = measure.textbbox((0, 0), " ", font=font)
                x += sb[2] - sb[0]
                continue

            # render character to a small RGBA canvas to allow rotation
            cb = measure.textbbox((0, 0), ch, font=font)
            cw = max(1, cb[2] - cb[0])
            ch_h = max(1, cb[3] - cb[1])
            canvas = Image.new("RGBA", (cw + 12, ch_h + 12), (0, 0, 0, 0))
            cd = ImageDraw.Draw(canvas)
            # simulate ink thickness by drawing multiple slightly-offset strokes
            for ox, oy in [(-1, 0), (0, 0), (1, 0)]:
                cd.text((6 + ox, 6 + oy), ch, font=font, fill=color)
            angle = random.uniform(-6, 6)
            canvas = canvas.rotate(angle, resample=Image.BICUBIC, expand=1)
            paste_x = int(x + random.randint(-1, 2))
            paste_y = int(y + random.randint(-2, 2))
            img.paste(canvas, (paste_x, paste_y), canvas)
            x += cw + random.randint(0, 2)

        y += int(heights[idx] * 1.4)
    img.save(out_path)


def convert(text, out_path, font=None, size=48, color=(0, 0, 0)):
    # if no font provided, try to pick a handwriting-like one
    if font is None:
        font = find_handwriting_font()
    if HAS_PYWHATKIT:
        try:
            _pwk.text_to_handwriting(text, out_path, rgb=color)
            return
        except Exception:
            pass
    _fallback(text, out_path, font_path=font, size=size, color=color)


def main():
    parser = argparse.ArgumentParser(description="Convert text to handwriting PNG")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", type=str, help="Text to convert")
    g.add_argument("--input-file", type=str, help="Path to text file")
    parser.add_argument("--output", type=str, default="out.png", help="Output PNG path")
    parser.add_argument("--font", type=str, default=None, help="TTF font path (optional)")
    parser.add_argument("--size", type=int, default=48, help="Fallback font size")
    parser.add_argument("--rgb", type=str, default="0,0,0", help="Ink color R,G,B")

    args = parser.parse_args()
    if args.input_file:
        if not os.path.exists(args.input_file):
            print("Input file not found:", args.input_file)
            sys.exit(2)
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text

    try:
        color = tuple(int(x) for x in args.rgb.split(","))
        if len(color) != 3:
            raise ValueError()
    except Exception:
        print("Invalid --rgb. Use R,G,B")
        sys.exit(2)

    convert(text, args.output, font=args.font, size=args.size, color=color)
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
try:
    import pywhatkit as _pwk
    HAS_PYWHATKIT = True
except Exception:
    HAS_PYWHATKIT = False


def _fallback(text, out_path, font_path=None, size=48, color=(0, 0, 0), pad=36, max_width=1200):
    font = ImageFont.truetype(font_path, size) if font_path and os.path.exists(font_path) else ImageFont.load_default()
    lines = text.splitlines() or [text]
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        raw_lines = text.splitlines() or [text]
        measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

        # Wrap text to target width
        wrap_width = max_width - pad * 2
        lines = []
        for raw in raw_lines:
            words = raw.split(" ")
            cur = ""
            for w in words:
                test = (cur + " " + w).strip()
                bbox = measure.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] > wrap_width and cur:
                    lines.append(cur)
                    cur = w
                else:
                    cur = test
            if cur:
                lines.append(cur)

        # compute image size
        maxw = 0
        heights = []
        for L in lines:
            bbox = measure.textbbox((0, 0), L, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            maxw = max(maxw, w)
            heights.append(h)
        W = min(max(maxw + pad * 2, 400), max_width)
        H = sum(int(h * 1.4) for h in heights) + pad * 2

        # paper background + light texture
        img = Image.new("RGB", (W, H), (254, 250, 240))
        px = img.load()
        for i in range(0, H, 10):
            for j in range(0, W, 10):
                if random.random() < 0.02:
                    r = max(0, min(255, px[j, i][0] - random.randint(5, 18)))
                    px[j, i] = (r, r - 2 if r > 2 else r, r - 5 if r > 5 else r)

        y = pad
        for idx, line in enumerate(lines):
            x = pad
            for ch in line:
                if ch == " ":
                    sb = measure.textbbox((0, 0), " ", font=font)
                    x += sb[2] - sb[0]
                    continue

                # draw character onto a small image for rotation and thickness
                cb = measure.textbbox((0, 0), ch, font=font)
                cw = cb[2] - cb[0]
                ch_h = cb[3] - cb[1]
                canvas = Image.new("RGBA", (cw + 12, ch_h + 12), (0, 0, 0, 0))
                cd = ImageDraw.Draw(canvas)
                # simulate ink thickness by drawing text multiple times with subtle offsets
                offsets = [(-1, 0), (0, 0), (1, 0)]
                for ox, oy in offsets:
                    cd.text((6 + ox, 6 + oy), ch, font=font, fill=color)
                angle = random.uniform(-6, 6)
                canvas = canvas.rotate(angle, resample=Image.BICUBIC, expand=1)
                img.paste(canvas, (int(x + random.randint(-1, 2)), int(y + random.randint(-2, 2))), canvas)
                x += cw + random.randint(0, 2)

            # line height
            y += int(heights[idx] * 1.4)
        img.save(out_path)


def convert(text, out_path, font=None, size=48, color=(0, 0, 0)):
    if HAS_PYWHATKIT:
        try:
            _pwk.text_to_handwriting(text, out_path, rgb=color)
            return
        except Exception:
            pass
    _fallback(text, out_path, font_path=font, size=size, color=color)


def main():
    parser = argparse.ArgumentParser(description="Convert text to handwriting PNG")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", type=str, help="Text to convert")
    g.add_argument("--input-file", type=str, help="Path to text file")
    parser.add_argument("--output", type=str, default="out.png", help="Output PNG path")
    parser.add_argument("--font", type=str, default=None, help="TTF font path (optional)")
    parser.add_argument("--size", type=int, default=48, help="Fallback font size")
    parser.add_argument("--rgb", type=str, default="0,0,0", help="Ink color R,G,B")

    args = parser.parse_args()
    if args.input_file:
        if not os.path.exists(args.input_file):
            print("Input file not found:", args.input_file)
            sys.exit(2)
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text
    try:
        color = tuple(int(x) for x in args.rgb.split(","))
        if len(color) != 3:
            raise ValueError()
    except Exception:
        print("Invalid --rgb. Use R,G,B")
        sys.exit(2)
    convert(text, args.output, font=args.font, size=args.size, color=color)
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
