#!/usr/bin/env python3
"""Downscale photos from assets/ into tex/figures/photos/ for the PDF.
Run: python3 .scripts/photos.py   (needs Pillow)"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets"
OUT = ROOT / "tex" / "figures" / "photos"
OUT.mkdir(parents=True, exist_ok=True)
for f in sorted(SRC.rglob("*")):
    if f.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    rel = f.relative_to(SRC)
    name = "_".join(rel.with_suffix("").parts)
    im = ImageOps.exif_transpose(Image.open(f))
    keep_png = name in {"rigging_cutter", "SimLE_Stardust_2023"}
    im.thumbnail((1600, 1600))
    if keep_png:
        im.save(OUT / f"{name}.png", optimize=True)
    else:
        im.convert("RGB").save(OUT / f"{name}.jpg", quality=82, optimize=True)
    print(name)
