#!/usr/bin/env python3
"""Compose agency-style browser mockups from raw page screenshots."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAW_DIR = Path(__file__).resolve().parents[1] / "tmp" / "portfolio-raw"
OUT_DIR = Path(__file__).resolve().parents[1] / "apps" / "website" / "seed_media" / "portfolio"
PUBLIC_DIR = Path(__file__).resolve().parents[1] / "frontend" / "public" / "portfolio-covers"

CANVAS = (1680, 1050)
BG = (16, 18, 16)
CHROME = (28, 31, 28)
BAR = (22, 24, 22)
WINDOW = (12, 13, 13)
TEXT = (232, 228, 220)
MUTED = (160, 166, 158)
RADIUS = 22
CHROME_H = 46


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def compose(
    raw_path: Path,
    dest: Path,
    *,
    url: str,
    caption: str,
) -> None:
    canvas = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(canvas)

    # Soft studio glow behind the laptop frame.
    glow = Image.new("RGB", CANVAS, BG)
    gdraw = ImageDraw.Draw(glow)
    cx, cy = CANVAS[0] // 2, CANVAS[1] // 2 + 20
    gdraw.ellipse((cx - 620, cy - 360, cx + 620, cy + 420), fill=(32, 36, 31))
    canvas = Image.composite(glow.filter(ImageFilter.GaussianBlur(90)), canvas, Image.new("L", CANVAS, 180))
    draw = ImageDraw.Draw(canvas)

    pad_x, pad_y = 90, 86
    win_w = CANVAS[0] - pad_x * 2
    win_h = CANVAS[1] - pad_y * 2 - 18
    win_box = (pad_x, pad_y, pad_x + win_w, pad_y + win_h)

    shadow = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        (win_box[0] + 10, win_box[1] + 18, win_box[2] + 10, win_box[3] + 22),
        radius=RADIUS + 2,
        fill=(0, 0, 0, 140),
    )
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(22))).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle(win_box, radius=RADIUS, fill=WINDOW)

    chrome_box = (pad_x, pad_y, pad_x + win_w, pad_y + CHROME_H)
    chrome = Image.new("RGB", (win_w, CHROME_H), CHROME)
    canvas.paste(chrome, (pad_x, pad_y))

    # Traffic lights
    for i, color in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        x = pad_x + 22 + i * 18
        y = pad_y + CHROME_H // 2
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color)

    # URL bar
    bar_l = pad_x + 92
    bar_r = pad_x + win_w - 28
    bar_t = pad_y + 12
    bar_b = pad_y + CHROME_H - 12
    draw.rounded_rectangle((bar_l, bar_t, bar_r, bar_b), radius=8, fill=BAR)
    font = _font(13)
    draw.text((bar_l + 14, bar_t + 4), url, fill=MUTED, font=font)

    shot = Image.open(raw_path).convert("RGB")
    content_box = (pad_x + 1, pad_y + CHROME_H, pad_x + win_w - 1, pad_y + win_h - 1)
    cw = content_box[2] - content_box[0]
    ch = content_box[3] - content_box[1]
    scale = max(cw / shot.width, ch / shot.height)
    nw, nh = math.ceil(shot.width * scale), math.ceil(shot.height * scale)
    shot = shot.resize((nw, nh), Image.LANCZOS)
    left = (nw - cw) // 2
    top = 0
    shot = shot.crop((left, top, left + cw, top + ch))
    canvas.paste(shot, (content_box[0], content_box[1]))

    # Re-apply rounded mask so screenshot doesn't square the corners.
    rounded = Image.new("RGB", CANVAS, BG)
    mask = Image.new("L", CANVAS, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(win_box, radius=RADIUS, fill=255)
    rounded.paste(canvas, mask=mask)
    # Keep studio background outside the window.
    out = Image.new("RGB", CANVAS, BG)
    glow2 = Image.new("RGB", CANVAS, BG)
    gd = ImageDraw.Draw(glow2)
    gd.ellipse((cx - 620, cy - 360, cx + 620, cy + 420), fill=(32, 36, 31))
    out.paste(glow2.filter(ImageFilter.GaussianBlur(90)))
    out.paste(rounded, mask=mask)

    # Caption
    cap_font = _font(12)
    draw = ImageDraw.Draw(out)
    draw.text((pad_x + 4, CANVAS[1] - 42), caption, fill=(110, 116, 108), font=cap_font)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG", optimize=True)
    print(f"wrote {dest} ({dest.stat().st_size // 1024} KB)")


SHOTS = [
    ("artmagic-home.png", "artmagic.png", "artmagic.com.ua", "Chameleon Studio · Артмагія · головна"),
    ("artmagic-inner.png", "artmagic-inner.png", "artmagic.com.ua/category", "Chameleon Studio · Артмагія · каталог"),
    ("artmagic-detail.png", "artmagic-detail.png", "artmagic.com.ua/product", "Chameleon Studio · Артмагія · картка товару"),
    ("luxmeb-home.png", "luxmeb.png", "forma.studio", "Chameleon Studio · LuxMeb · головна"),
    ("luxmeb-inner.png", "luxmeb-inner.png", "forma.studio/#projects", "Chameleon Studio · LuxMeb · проєкти"),
    ("luxmeb-detail.png", "luxmeb-detail.png", "forma.studio/project", "Chameleon Studio · LuxMeb · деталей проєкту"),
    ("rudwood-home.png", "rudwood.png", "rudwood.com.ua", "Chameleon Studio · RudWood · головна"),
    ("rudwood-inner.png", "rudwood-inner.png", "rudwood.com.ua/catalog", "Chameleon Studio · RudWood · каталог"),
    ("rudwood-detail.png", "rudwood-detail.png", "rudwood.com.ua/catalog/item", "Chameleon Studio · RudWood · картка товару"),
    ("ac-clean-home.png", "ac-clean.png", "asclean.ua", "Chameleon Studio · AS clean · головна"),
    ("ac-clean-inner.png", "ac-clean-inner.png", "asclean.ua/#services", "Chameleon Studio · AS clean · послуги"),
    ("ac-clean-detail.png", "ac-clean-detail.png", "asclean.ua/#portfolio", "Chameleon Studio · AS clean · роботи"),
    ("elvet-home.png", "elvet.png", "elvetgroup.com", "Chameleon Studio · Elvet Group · головна"),
    ("elvet-inner.png", "elvet-inner.png", "elvetgroup.com/catalog", "Chameleon Studio · Elvet Group · каталог"),
    ("elvet-detail.png", "elvet-detail.png", "elvetgroup.com/products", "Chameleon Studio · Elvet Group · картка товару"),
]


def main() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for raw_name, out_name, url, caption in SHOTS:
        raw = RAW_DIR / raw_name
        if not raw.exists():
            missing.append(str(raw))
            continue
        dest = OUT_DIR / out_name
        compose(raw, dest, url=url, caption=caption)
        public = PUBLIC_DIR / out_name
        public.write_bytes(dest.read_bytes())
        print(f"copied {public}")
    if missing:
        raise SystemExit("Missing raw shots:\n" + "\n".join(missing))


if __name__ == "__main__":
    main()
