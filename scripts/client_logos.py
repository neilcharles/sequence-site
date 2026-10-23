"""Turn the client logos in sources/client-logos/ into matching single-colour
marks for the home page's "Our clients" strip.

    python3 scripts/client_logos.py

Each logo, whatever its colours or background, becomes a PNG in one house
grey on a transparent background, trimmed to its ink and written to
assets/images/clients/<name>.png at a fixed height. How the ink is separated
from the background depends on the source:

- "alpha": the file already has transparency (or is an SVG); use it as is.
- "bg": a flat background (light or dark). Ink is anything that differs from
  the colour round the edge, scaled so the strongest ink is fully opaque;
  paler parts of a two-tone logo come out as a lighter grey.
- "white": white lettering on a busy background (Mother's tartan); keep only
  near-white pixels.

The home page sizes the marks by area so that wide wordmarks and square
badges carry similar weight. Needs Pillow, numpy and Inkscape (for SVGs).
"""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "client-logos"
OUT = ROOT / "assets" / "images" / "clients"

GREY = (0x63, 0x63, 0x69)  # --sa-grey
HEIGHT = 240  # output height in px; displayed at about a quarter of this

# name -> (source file, mode)
LOGOS = {
    "itv": ("ITV_plc_2025_logo.svg.webp", "alpha"),
    "barb": ("barb.jpg", "bg"),
    "ipa": ("ipa.png", "bg"),
    "trainline": ("trainline.svg", "alpha"),
    "mother": ("mother.jpg", "white"),
    "benenden": ("benenden.png", "bg"),
    "7stars": ("7Stars.svg", "alpha"),
    "origin": ("origin.webp", "bg"),
    "bamm": ("bamm_logo.jpeg", "bg"),
    "hsl": ("hsl.jpeg", "bg"),
    "boutique": ("boutique.png", "bg"),
    "tmwi": ("tmwi.webp", "bg"),
}


def load(path):
    if path.suffix == ".svg":
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            png = pathlib.Path(tmp) / "logo.png"
            subprocess.run(
                ["inkscape", str(path), "--export-type=png",
                 "--export-height=1000", f"--export-filename={png}"],
                check=True, capture_output=True)
            return Image.open(png).convert("RGBA")
    return Image.open(path).convert("RGBA")


def ink(im, mode):
    """Return the logo's ink as an alpha channel in 0..1."""
    a = np.asarray(im, dtype=float) / 255
    rgb, alpha = a[..., :3], a[..., 3]
    if mode == "alpha":
        return alpha
    if mode == "white":
        lo = rgb.min(axis=2)
        return np.clip((lo - 0.72) / 0.18, 0, 1)
    # "bg": distance from the edge colour, normalised by the strongest ink.
    edge = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    bg = np.median(edge, axis=0)
    d = np.linalg.norm(rgb - bg, axis=2)
    full = np.percentile(d[d > 0.15], 90) if (d > 0.15).any() else 1
    return np.clip((d - 0.06) / (full - 0.06), 0, 1)


def trim(alpha):
    ys, xs = np.nonzero(alpha > 0.08)
    return alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (file, mode) in LOGOS.items():
        alpha = trim(ink(load(SRC / file), mode))
        h, w = alpha.shape
        out = np.zeros((h, w, 4), dtype=np.uint8)
        out[..., :3] = GREY
        out[..., 3] = np.round(alpha * 255)
        im = Image.fromarray(out, "RGBA")
        im = im.resize((round(w * HEIGHT / h), HEIGHT), Image.LANCZOS)
        im.save(OUT / f"{name}.png", optimize=True)
        print(f"{name}: {im.width}x{im.height}", file=sys.stderr)


if __name__ == "__main__":
    main()
