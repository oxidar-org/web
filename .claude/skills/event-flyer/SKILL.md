---
name: event-flyer
description: Use when an Oxidar.org post needs an event flyer, poster or promotional image for a meetup, charla, workshop or conference, or when an existing flyer has a wrong or missing date, time, venue, speaker or talk title.
---

# Event Flyer

## Overview

Every Oxidar flyer shares one house style: a 1728x2304 paper-white poster with
Rust orange accents, rounded cards, and a QR to registration. It is rendered
from JSON by `scripts/flyer/generate_flyer.py` — you do not draw it by hand and
you do not edit the pixels of an existing one.

## When to Use

- A post announces an event and needs its flyer
- A flyer has the wrong date, time, venue, speaker or talk title
- **Not** for photos, diagrams, or social share cards — the `social-share`
  workflow generates those from post images

## Quick Reference

```bash
pip install -r scripts/flyer/requirements.txt
cp scripts/flyer/events/criptografia-webapps.json scripts/flyer/events/<slug>.json
$EDITOR scripts/flyer/events/<slug>.json
python scripts/flyer/generate_flyer.py scripts/flyer/events/<slug>.json
```

The image lands at the config's `"output"` path. Commit **both** the JSON and
the JPEG — the JSON is what makes the next correction a one-line edit.

| Key | Notes |
|-----|-------|
| `title` / `subtitle` | Auto-shrink to fit the width; no manual sizing |
| `talks[]` | `label`, `icon`, `title`, `speaker`, `topic` — 1 to 3 talks |
| `info[]` | `icon`, `strong`, `weak` — date, venue, format |
| `qr_url` | Registration link, verified by reading it back out of the JPEG |
| `host` | Optional `label` + `logo` partner credit |
| `footer_right` | Two muted lines, bottom right |

Icons: `key` `nodes` `calendar` `clock` `pin` `screen` `globe` `mail` `telegram`

## Rules

- **Never re-derive the palette or the typeface.** Both are pinned in the
  script, sampled from the published flyers (orange `#F37233`, ink `#262626`,
  display face Inter Tight 800). Re-picking them by eye breaks the family.
- **Never hand-edit a rendered flyer.** Change the JSON and re-render, so the
  next person inherits a source of truth instead of a JPEG.
- **Fix the post too.** A date, time or talk title on a flyer also appears in
  the post body — in both `<slug>.md` and `<slug>.en.md`.
- Partner logos belong in `scripts/flyer/assets/partner-*.png`, transparent
  background, dark artwork (the canvas is light).

## Common Mistakes

| Mistake | What happens |
|---------|--------------|
| Cramming in a 4th talk, or very long titles | The script steps down through its density presets and then exits with an overflow message. Shorten the copy — do not force it |
| Not installing opencv | The QR is never verified; the script warns. A flyer whose QR does not scan is worse than no QR |
| Redrawing the flyer in an image editor | It drifts from the house style, and the next flyer no longer matches |
| Editing the JPEG to fix a typo | The JSON and the image disagree from then on |

## Adding a New Icon

Icons are drawn, not fonts or emoji, so they render identically everywhere.
Add a `_icon_<name>` method to `Flyer` taking `(cx, cy, s, col)` and draw in
units relative to `s`, centred on `(cx, cy)`. Then reference it by `<name>` in
the config.
