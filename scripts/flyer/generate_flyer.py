#!/usr/bin/env python3
"""Generate an Oxidar.org event flyer in the house style.

Reads a JSON description of the event and renders a 1728x2304 poster
matching the existing flyers (raytracing, DebConf 26, criptografia-webapps):
paper-white canvas, Rust orange accents, rounded cards, QR to registration.

    python scripts/flyer/generate_flyer.py events/my-event.json

Everything is drawn at 2x and downsampled, so shapes and icons stay smooth.
See .claude/skills/event-flyer/SKILL.md for the authoring guide.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    import segno
except ImportError:  # pragma: no cover - guidance beats a traceback
    sys.exit('Missing deps. Run: pip install -r scripts/flyer/requirements.txt')

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
FONT_DIR = HERE / '.fonts'

# --- canvas -----------------------------------------------------------------
SS = 2                      # supersampling factor
W, H = 1728, 2304
M = 104                     # page margin
CW = W - 2 * M

# --- palette (sampled from the existing flyers; do not eyeball these) -------
PAPER = (254, 254, 254)
INK = (38, 38, 38)
INK2 = (61, 62, 61)
MUTED = (126, 128, 126)
LIGHT = (172, 174, 172)
ORANGE = (243, 114, 51)
LINE = (227, 227, 224)
TINT = (253, 239, 231)
WHITE = (255, 255, 255)
TELEGRAM_BLUE = (41, 169, 234)

# --- type -------------------------------------------------------------------
# Inter Tight 800 matches the display face used on the existing flyers.
GOOGLE_FONTS = {
    'display': ('Inter+Tight', 800),
    'display7': ('Inter+Tight', 700),
    'bold': ('Inter', 700),
    'semi': ('Inter', 600),
    'body': ('Inter', 400),
}

# --- vertical rhythm --------------------------------------------------------
STRIPE_H = 34
CREDIT_H = 118
FOOT_H = 236
DIVIDER_Y = 664

# Tried in order; the first that fits the page wins. The first entry is the
# reference density used by the published flyers - do not reorder it.
DENSITIES = [
    {'pad': 46, 'tile': 104, 'title': 54, 'lead': 64, 'row_h': 106, 'gap': 44},
    {'pad': 42, 'tile': 98, 'title': 50, 'lead': 59, 'row_h': 99, 'gap': 38},
    {'pad': 36, 'tile': 90, 'title': 46, 'lead': 55, 'row_h': 92, 'gap': 33},
    {'pad': 32, 'tile': 82, 'title': 43, 'lead': 51, 'row_h': 86, 'gap': 28},
]


def fetch_fonts() -> dict[str, Path]:
    """Download the Inter / Inter Tight weights once into scripts/flyer/.fonts."""
    FONT_DIR.mkdir(exist_ok=True)
    paths = {}
    for key, (family, weight) in GOOGLE_FONTS.items():
        dest = FONT_DIR / f'{family.replace("+", "")}-{weight}.ttf'
        if not dest.exists():
            css_url = (f'https://fonts.googleapis.com/css2?family={family}'
                       f':wght@{weight}&display=swap')
            req = urllib.request.Request(css_url, headers={'User-Agent': 'Mozilla/5.0'})
            css = urllib.request.urlopen(req).read().decode()
            start = css.index('https://fonts.gstatic.com')
            url = css[start:css.index('.ttf', start) + 4]
            dest.write_bytes(urllib.request.urlopen(url).read())
            print(f'  fetched {dest.name}')
        paths[key] = dest
    return paths


class Flyer:
    def __init__(self, cfg: dict, base: Path):
        self.cfg = cfg
        self.base = base
        self.fonts = fetch_fonts()
        self._cache: dict = {}
        self.img = Image.new('RGB', (W * SS, H * SS), PAPER)
        self.dr = ImageDraw.Draw(self.img)

    # --- primitives ---------------------------------------------------------
    def font(self, name: str, size: int):
        key = (name, size)
        if key not in self._cache:
            self._cache[key] = ImageFont.truetype(str(self.fonts[name]), size * SS)
        return self._cache[key]

    def sc(self, box):
        return [v * SS for v in box]

    def rrect(self, box, r, fill=None, outline=None, width=1):
        self.dr.rounded_rectangle(self.sc(box), radius=r * SS, fill=fill,
                                  outline=outline, width=width * SS)

    def ellipse(self, box, fill=None, outline=None, width=1):
        self.dr.ellipse(self.sc(box), fill=fill, outline=outline, width=width * SS)

    def line(self, pts, fill, width=1):
        self.dr.line([v * SS for v in pts], fill=fill, width=width * SS, joint='curve')

    def text(self, xy, s, fnt, fill, anchor='la'):
        self.dr.text((xy[0] * SS, xy[1] * SS), s, font=fnt, fill=fill, anchor=anchor)

    def measure(self, s, fnt):
        return self.dr.textlength(s, font=fnt) / SS

    def tracked(self, xy, s, fnt, fill, track, anchor='l'):
        """Letterspaced text; PIL has no tracking, so glyphs are placed by hand."""
        total = sum(self.measure(c, fnt) + track for c in s) - track
        x = xy[0] - total / 2 if anchor == 'm' else xy[0]
        for ch in s:
            self.text((x, xy[1]), ch, fnt, fill)
            x += self.measure(ch, fnt) + track
        return total

    def fit(self, name, s, max_size, max_width):
        size = max_size
        while size > 8 and self.measure(s, self.font(name, size)) > max_width:
            size -= 1
        return self.font(name, size)

    def wrap(self, s, fnt, max_width):
        lines, cur = [], ''
        for word in s.split():
            trial = f'{cur} {word}'.strip()
            if self.measure(trial, fnt) <= max_width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def wrap_balanced(self, s, fnt, max_width):
        """Same line count, but as even as possible - avoids orphan words."""
        lines = self.wrap(s, fnt, max_width)
        if len(lines) < 2:
            return lines
        best, w = lines, max_width
        while w > 120:
            w -= 8
            cand = self.wrap(s, fnt, w)
            if len(cand) > len(lines):
                break
            best = cand
        return best

    def paste(self, im, box_w, xy, anchor='lt'):
        w = int(box_w * SS)
        h = int(im.size[1] * w / im.size[0])
        im = im.resize((w, h), Image.LANCZOS)
        x, y = int(xy[0] * SS), int(xy[1] * SS)
        if anchor[0] == 'm':
            x -= w // 2
        elif anchor[0] == 'r':
            x -= w
        if anchor[1] == 'm':
            y -= h // 2
        elif anchor[1] == 'b':
            y -= h
        self.img.paste(im, (x, y), im)
        return h / SS

    # --- icons --------------------------------------------------------------
    def icon(self, name, cx, cy, s, col=ORANGE):
        getattr(self, f'_icon_{name}')(cx, cy, s, col)

    def _icon_key(self, cx, cy, s, col):
        r, w = s * 0.26, max(1, int(s * 0.11))
        self.ellipse([cx - s * 0.46, cy - r, cx - s * 0.46 + 2 * r, cy + r],
                     outline=col, width=w)
        self.line([cx - s * 0.46 + r + w, cy, cx + s * 0.5, cy], col, w)
        self.line([cx + s * 0.5, cy, cx + s * 0.5, cy + s * 0.26], col, w)
        self.line([cx + s * 0.18, cy, cx + s * 0.18, cy + s * 0.22], col, w)

    def _icon_nodes(self, cx, cy, s, col):
        w = max(1, int(s * 0.09))
        bw, bh = s * 0.30, s * 0.20
        lx = cx - s * 0.46
        self.rrect([lx, cy - bh, lx + bw, cy + bh], s * 0.05, outline=col, width=w)
        for dy in (-s * 0.32, 0, s * 0.32):
            rx, ry = cx + s * 0.16, cy + dy
            self.rrect([rx, ry - bh * 0.62, rx + bw, ry + bh * 0.62], s * 0.05,
                       outline=col, width=w)
            self.line([lx + bw, cy, rx - s * 0.06, ry], col, w)

    def _icon_calendar(self, cx, cy, s, col):
        w = max(1, int(s * 0.09))
        self.rrect([cx - s * 0.4, cy - s * 0.34, cx + s * 0.4, cy + s * 0.42],
                   s * 0.10, outline=col, width=w)
        self.line([cx - s * 0.4, cy - s * 0.10, cx + s * 0.4, cy - s * 0.10], col, w)
        for dx in (-s * 0.20, s * 0.20):
            self.line([cx + dx, cy - s * 0.48, cx + dx, cy - s * 0.26], col, w)

    def _icon_clock(self, cx, cy, s, col):
        w, r = max(1, int(s * 0.09)), s * 0.40
        self.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
        self.line([cx, cy - s * 0.22, cx, cy], col, w)
        self.line([cx, cy, cx + s * 0.20, cy + s * 0.10], col, w)

    def _icon_pin(self, cx, cy, s, col):
        w, r = max(1, int(s * 0.09)), s * 0.31
        top = cy - s * 0.12
        self.dr.arc(self.sc([cx - r, top - r, cx + r, top + r]), 145, 395,
                    fill=col, width=w * SS)
        self.line([cx - r * 0.82, top + r * 0.56, cx, cy + s * 0.46], col, w)
        self.line([cx + r * 0.82, top + r * 0.56, cx, cy + s * 0.46], col, w)
        self.ellipse([cx - r * 0.34, top - r * 0.34, cx + r * 0.34, top + r * 0.34],
                     outline=col, width=w)

    def _icon_screen(self, cx, cy, s, col):
        w = max(1, int(s * 0.09))
        self.rrect([cx - s * 0.44, cy - s * 0.36, cx + s * 0.44, cy + s * 0.18],
                   s * 0.08, outline=col, width=w)
        self.line([cx, cy + s * 0.18, cx, cy + s * 0.36], col, w)
        self.line([cx - s * 0.24, cy + s * 0.38, cx + s * 0.24, cy + s * 0.38], col, w)

    def _icon_globe(self, cx, cy, s, col):
        w, r = max(1, int(s * 0.085)), s * 0.40
        self.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
        self.ellipse([cx - r * 0.46, cy - r, cx + r * 0.46, cy + r], outline=col, width=w)
        self.line([cx - r, cy, cx + r, cy], col, w)

    def _icon_mail(self, cx, cy, s, col):
        w = max(1, int(s * 0.085))
        self.rrect([cx - s * 0.42, cy - s * 0.30, cx + s * 0.42, cy + s * 0.30],
                   s * 0.07, outline=col, width=w)
        self.line([cx - s * 0.36, cy - s * 0.22, cx, cy + s * 0.06], col, w)
        self.line([cx + s * 0.36, cy - s * 0.22, cx, cy + s * 0.06], col, w)

    def _icon_telegram(self, cx, cy, s, col):
        """Telegram's own mark in brand colour, as on the other Oxidar flyers."""
        plane = [(54, 118), (182, 70), (152, 174), (112, 146), (96, 168), (96, 134)]
        fold = [(96, 134), (182, 70), (112, 146)]
        r, f = s / 2, s / 240.0
        self.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TELEGRAM_BLUE)

        def pts(poly):
            return [v for px, py in poly
                    for v in ((cx + (px - 120) * f) * SS, (cy + (py - 120) * f) * SS)]

        self.dr.polygon(pts(plane), fill=WHITE)
        self.dr.polygon(pts(fold), fill=(206, 227, 241))

    # --- sections -----------------------------------------------------------
    def asset(self, rel: str) -> Image.Image:
        for root in (self.base, REPO, HERE):
            p = (root / rel)
            if p.exists():
                return Image.open(p)
        raise FileNotFoundError(f'asset not found: {rel}')

    def draw_header(self):
        for row in range(4):
            for col in range(5):
                x, y = M + col * 26, 110 + row * 26
                t = (row + col) / 7.0
                fade = tuple(int(c + (p - c) * t * 0.72) for c, p in zip(ORANGE, PAPER))
                self.ellipse([x, y, x + 13, y + 13], fill=fade)
        self.paste(self.asset('scripts/flyer/assets/rust-mark.png'), 104, (W - M, 104),
                   anchor='rt')
        self.paste(self.asset('assets/images/logo-text.png'), 480, (W / 2, 206),
                   anchor='mt')

        self.tracked((W / 2, 372), self.cfg['eyebrow'], self.font('bold', 34),
                     ORANGE, 12, anchor='m')
        title = self.cfg['title']
        self.text((W / 2, 428), title, self.fit('display', title, 112, CW), INK,
                  anchor='ma')
        sub = self.cfg.get('subtitle')
        if sub:
            self.text((W / 2, 556), sub, self.fit('display7', sub, 66, CW), ORANGE,
                      anchor='ma')

        mark = 42
        self.line([M, DIVIDER_Y, W / 2 - mark - 26, DIVIDER_Y], LINE, 2)
        self.line([W / 2 + mark + 26, DIVIDER_Y, W - M, DIVIDER_Y], LINE, 2)
        self.paste(self.asset('scripts/flyer/assets/rust-mark.png'), mark,
                   (W / 2 - mark / 2 - 1, DIVIDER_Y), anchor='lm')

    def layout(self):
        """Anchor the stack from the bottom edge so cards can't silently overflow.

        Steps down through DENSITIES until the content fits; raises rather than
        letting a card run off the page or under the footer.
        """
        talks = self.cfg['talks']
        best = None
        for d in DENSITIES:
            self.d = d
            self.card_x = M + d['pad'] + d['tile'] + 36
            self.card_w = W - M - d['pad'] - self.card_x
            f_title = self.font('display7', d['title'])
            self.wrapped = [self.wrap_balanced(t['title'], f_title, self.card_w - 30)
                            for t in talks]
            content = max(28 + 18 + len(ls) * d['lead'] + 14 + 42
                          for ls in self.wrapped)
            self.card_h = max(d['pad'] * 2 + d['tile'], d['pad'] * 2 + content)
            self.info_h = 40 + d['row_h'] * len(self.cfg['info'])

            self.credit_top = H - STRIPE_H - 30 - CREDIT_H
            self.foot_top = self.credit_top - d['gap'] - FOOT_H
            self.info_top = self.foot_top - d['gap'] - self.info_h
            stack = len(talks) * self.card_h + (len(talks) - 1) * 34
            self.cards_top = self.info_top - d['gap'] - stack
            best = self.cards_top
            if self.cards_top > DIVIDER_Y + 46:
                return
        raise SystemExit(
            f'Content overflows the page even at the tightest density (cards would '
            f'start at {best:.0f}, need > {DIVIDER_Y + 46}). Shorten the talk titles, '
            f'drop an info row, or split the event across two flyers.')

    def draw_talks(self):
        d = self.d
        tile = d['tile']
        f_title = self.font('display7', d['title'])
        y = self.cards_top
        for talk, lines in zip(self.cfg['talks'], self.wrapped):
            self.rrect([M, y, W - M, y + self.card_h], 34, fill=WHITE,
                       outline=LINE, width=3)
            by = y + (self.card_h - tile) / 2
            self.rrect([M + d['pad'], by, M + d['pad'] + tile, by + tile],
                       26, fill=TINT)
            self.icon(talk['icon'], M + d['pad'] + tile / 2, by + tile / 2, tile * 0.60)

            block = 28 + 18 + len(lines) * d['lead'] + 14 + 42
            ty = y + (self.card_h - block) / 2
            self.tracked((self.card_x, ty), talk['label'], self.font('bold', 26),
                         ORANGE, 6)
            ty += 46
            for ln in lines:
                self.text((self.card_x, ty), ln, f_title, INK)
                ty += d['lead']
            ty += 14
            speaker = talk['speaker']
            self.text((self.card_x, ty), speaker, self.font('bold', 34), INK2)
            if talk.get('topic'):
                w = self.measure(speaker, self.font('bold', 34))
                self.text((self.card_x + w + 18, ty + 3), talk['topic'],
                          self.font('body', 31), MUTED)
            y += self.card_h + 34

    def draw_info(self):
        top = self.info_top
        self.rrect([M, top, W - M, top + self.info_h], 34, fill=WHITE,
                   outline=LINE, width=3)
        row_h = self.d['row_h']
        for i, row in enumerate(self.cfg['info']):
            cy = top + 20 + row_h * i + row_h / 2
            if i:
                self.line([M + 46, cy - row_h / 2, W - M - 46, cy - row_h / 2], LINE, 2)
            self.icon(row['icon'], M + 92, cy, 54)
            x = M + 150
            self.text((x, cy), row['strong'], self.font('bold', 40), INK, anchor='lm')
            if row.get('weak'):
                x += self.measure(row['strong'], self.font('bold', 40)) + 22
                self.ellipse([x, cy - 4, x + 8, cy + 4], fill=ORANGE)
                self.text((x + 24, cy + 1), row['weak'], self.font('body', 36),
                          MUTED, anchor='lm')

    def draw_footer(self):
        top, qr_w = self.foot_top, 560
        self.rrect([M, top, M + qr_w, top + FOOT_H], 30, fill=ORANGE)
        buf = io.BytesIO()
        segno.make(self.cfg['qr_url'], error='h').save(
            buf, kind='png', scale=20, border=2, dark='#262626', light='#ffffff')
        qr = Image.open(io.BytesIO(buf.getvalue())).convert('RGBA')
        card = FOOT_H - 56
        self.rrect([M + 28, top + 28, M + 28 + card, top + 28 + card], 16, fill=WHITE)
        self.paste(qr, card - 20, (M + 38, top + 38))
        tx = M + 28 + card + 30
        for i, ln in enumerate(self.cfg['qr_caption']):
            self.text((tx, top + FOOT_H / 2 + (i - 0.5) * 52), ln,
                      self.font('bold', 38), WHITE, anchor='lm')

        cx0 = M + qr_w + 30
        self.rrect([cx0, top, W - M, top + FOOT_H], 30, fill=WHITE,
                   outline=LINE, width=3)
        contacts = self.cfg['contacts']
        for i, c in enumerate(contacts):
            cy = top + FOOT_H / 2 + (i - (len(contacts) - 1) / 2) * 68
            self.icon(c['icon'], cx0 + 62, cy, 50)
            self.text((cx0 + 110, cy + 1), c['label'], self.font('bold', 34), INK,
                      anchor='lm')

    def draw_credit(self):
        cy = self.credit_top + 26
        host = self.cfg.get('host')
        if host:
            self.tracked((M, cy - 26), host['label'], self.font('bold', 26), MUTED, 7)
            logo = self.asset(host['logo'])
            self.paste(logo, logo.size[0] * 96 / logo.size[1], (M, cy + 4))
        right = self.cfg.get('footer_right', [])
        for i, ln in enumerate(right):
            style = ('semi', 32, MUTED) if i == 0 else ('body', 30, LIGHT)
            self.text((W - M, cy + 26 + i * 48), ln,
                      self.font(style[0], style[1]), style[2], anchor='rm')

        for a, b, col in [(0, .16, ORANGE), (.16, .44, INK), (.44, .60, ORANGE),
                          (.60, .74, (246, 197, 168)), (.74, .88, INK), (.88, 1, ORANGE)]:
            self.dr.rectangle(self.sc([W * a, H - STRIPE_H, W * b, H]), fill=col)

    def render(self, out: Path):
        self.draw_header()
        self.layout()
        self.draw_talks()
        self.draw_info()
        self.draw_footer()
        self.draw_credit()
        out.parent.mkdir(parents=True, exist_ok=True)
        self.img.resize((W, H), Image.LANCZOS).save(
            out, quality=94, dpi=(300, 300), subsampling=0, progressive=True)
        return out


def verify_qr(path: Path, expected: str) -> bool:
    """Read the QR back out of the finished JPEG. Never ship an unscannable QR."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        print('  ! opencv not installed - QR NOT verified')
        return False
    a = np.array(Image.open(path).convert('RGB'))[:, :, ::-1].copy()
    got = cv2.QRCodeDetector().detectAndDecode(a)[0]
    ok = got == expected
    print(f'  QR decodes to {got!r} - {"ok" if ok else "MISMATCH"}')
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('config', type=Path, help='JSON event description')
    ap.add_argument('-o', '--output', type=Path, help='override output path')
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text())
    out = args.output or (REPO / cfg['output'])
    print(f'rendering {out.relative_to(REPO) if out.is_relative_to(REPO) else out}')
    Flyer(cfg, args.config.resolve().parent).render(out)
    verify_qr(out, cfg['qr_url'])
    print(f'  wrote {out} ({out.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
