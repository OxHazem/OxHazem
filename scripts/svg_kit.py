"""Shared helpers for the profile graphics.

Text is converted to outlines so every card looks identical on any OS. GitHub
serves README SVGs as images, so they cannot rely on web fonts or local fonts.
"""
from pathlib import Path
from xml.sax.saxutils import escape

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "profile"
FONT_DIR = Path(__file__).resolve().parent / "fonts"

DISPLAY = "InterDisplay-SemiBold"
REGULAR = "Inter-Regular"
MEDIUM = "Inter-Medium"
SEMIBOLD = "Inter-SemiBold"

# Both ramps run from "no signal" to "peak signal" along a magma-style colormap,
# the palette of the attention maps in the projects shown on the profile.
THEMES = {
    "dark": {
        "bg": "#10141B", "panel": "#161B23", "line": "#2A313C",
        "ink": "#F2F4F7", "body": "#AEB6C2", "mute": "#7D8693",
        "accent": "#FF9E5E",
        "ramp": ["#1F2530", "#51206F", "#B5367A", "#F4694C", "#FEC777"],
    },
    "light": {
        "bg": "#FFFFFF", "panel": "#FFFFFF", "line": "#DDE1E6",
        "ink": "#14181F", "body": "#4A525E", "mute": "#68717D",
        "accent": "#C2410C",
        "ramp": ["#EEF0F3", "#FBC39A", "#F0743F", "#B5247A", "#44106B"],
    },
}

_fonts = {}


def _font(name):
    if name not in _fonts:
        data = (FONT_DIR / f"{name}.otf").read_bytes()
        _fonts[name] = hb.Font(hb.Face(data))
    return _fonts[name]


def _shape(text, font_name, features=None):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    font = _font(font_name)
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    return font, buf.glyph_infos, buf.glyph_positions


def text_width(text, font_name, size, tracking=0.0):
    font, infos, positions = _shape(text, font_name)
    scale = size / font.face.upem
    return sum(p.x_advance for p in positions) * scale + tracking * len(infos)


def text(x, y, content, font_name, size, fill, anchor="start", tracking=0.0):
    """Return `content` as a single outlined <path> with its baseline at y."""
    width = text_width(content, font_name, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    font, infos, positions = _shape(content, font_name)
    scale = size / font.face.upem
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cursor = x
    for info, pos in zip(infos, positions):
        transform = (scale, 0, 0, -scale, cursor + pos.x_offset * scale, y - pos.y_offset * scale)
        font.draw_glyph_with_pen(info.codepoint, TransformPen(pen, transform))
        cursor += pos.x_advance * scale + tracking
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'


def wrap(content, font_name, size, max_width):
    lines, current = [], ""
    for word in content.split():
        candidate = f"{current} {word}".strip()
        if current and text_width(candidate, font_name, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    return lines + [current] if current else lines


def write_svg(name, width, height, body, title, style=""):
    style_block = f"<style>{style}</style>" if style else ""
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{escape(title, {chr(34): "&quot;"})}">'
        f"<title>{escape(title)}</title>{style_block}{body}</svg>\n"
    )
