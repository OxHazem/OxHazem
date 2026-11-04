"""Builds the static profile graphics in profile/ (dark and light versions).

Edit the content below and run from anywhere: python scripts/build_profile.py
"""
import math
import random

from svg_kit import (DISPLAY, MEDIUM, REGULAR, SEMIBOLD, THEMES, text, text_width, wrap,
                     write_svg)

PROJECTS = [
    {
        "slug": "tissueinsight", "name": "TissueInsight", "year": "2025",
        "summary": "Multi-modal cancer detection app combining gene expression analysis, "
                   "microscopy image classification and a RAG assistant.",
        "metrics": [("91%", "F1-score, gene expression")],
        "tags": "Python · CNN · RAG",
    },
    {
        "slug": "colorization", "name": "Automatic Video Colorization", "year": "2025",
        "summary": "ResNet34-UNet that predicts Lab chrominance from grayscale, with temporal "
                   "smoothing to remove flicker in historic footage.",
        "metrics": [("0.9235", "SSIM"), ("23.71 dB", "PSNR")],
        "tags": "PyTorch · U-Net · FFmpeg",
    },
    {
        "slug": "tracking", "name": "Object Detection & State Tracking", "year": "2026",
        "summary": "Real-time YOLOv8 pipeline with a multi-layer state tracker that logs "
                   "temporal transitions and rejects false positives.",
        "metrics": [("98.19%", "mAP@50")],
        "tags": "YOLOv8 · PyTorch · OpenCV",
    },
    {
        "slug": "summarization", "name": "Video Keyframe Summarization", "year": "2026",
        "summary": "Interpretable Transformer and BiLSTM keyframe selection, with self-attention "
                   "heatmaps that explain each model's choices.",
        "metrics": [("Top 15%", "duration budget")],
        "tags": "Transformers · BiLSTM · XAI",
    },
    {
        "slug": "intrusion", "name": "ML Intrusion Detection", "year": "2025",
        "summary": "Leakage-safe pipeline for highly imbalanced network traffic, using SMOTE "
                   "and Bayesian hyperparameter search with Optuna.",
        "metrics": [("99%", "precision"), ("96%", "recall")],
        "tags": "scikit-learn · imblearn · Optuna",
    },
    {
        "slug": "code-lab", "name": "Adaptive Code Learning Lab", "year": "",
        "summary": "Clean Architecture Flask backend for programming education, with code "
                   "execution, plagiarism detection and GenAI hints.",
        "metrics": [("560+", "tests"), ("74%", "coverage")],
        "tags": "Flask · Docker · CI/CD",
    },
]

TOOLKIT = [
    ("Languages", "Python, C++, R, JavaScript, SQL"),
    ("Machine learning", "PyTorch, scikit-learn, XGBoost, Optuna, imblearn"),
    ("Computer vision", "OpenCV, YOLOv8, FFmpeg"),
    ("AI systems", "RAG, NLP, Generative AI, Explainable AI"),
    ("Engineering", "Flask, Docker, PostgreSQL, SQLite, GitHub Actions, Pytest"),
]

BUTTONS = {
    "linkedin": ("LinkedIn", "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"),
    "github": ("GitHub", "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.03 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"),
    "email": ("Email", "M2 4h20a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm10 9.2L22 7.1V6L12 12 2 6v1.1z"),
    "resume": ("Resume", "M5 0h9.5L21 6.5V22a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2zm8.5 1.8V7.5h5.7zM7 12v1.8h10V12zm0 4v1.8h10V16z"),
}

W, H = 1000, 340


def hex_rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def ramp_color(ramp, t):
    t = max(0.0, min(1.0, t)) * (len(ramp) - 1)
    i = min(int(t), len(ramp) - 2)
    a, b = hex_rgb(ramp[i]), hex_rgb(ramp[i + 1])
    return "#%02x%02x%02x" % tuple(round(a[k] + (b[k] - a[k]) * (t - i)) for k in range(3))


def field_layer(ramp, hotspots, seed):
    """One frame of the attention map: a dot grid lit by Gaussian hot spots."""
    rng = random.Random(seed)
    dots, step = [], 15
    for gy in range(int(H / step) + 1):
        for gx in range(int(W * 0.47 / step) + 2):
            x, y = W - 8 - gx * step, 8 + gy * step
            energy = sum(a * math.exp(-((x - hx) ** 2 + (y - hy) ** 2) / (2 * s * s))
                         for hx, hy, s, a in hotspots)
            # Fade the field out toward the text column so copy stays clean.
            fade = min(1.0, max(0.0, (x - W * 0.53) / (W * 0.16)))
            value = min(1.0, energy + rng.uniform(0, 0.05)) * fade
            if value < 0.035:
                continue
            radius = 1.1 + 4.3 * value
            dots.append(f'<circle cx="{x}" cy="{y}" r="{radius:.1f}" fill="{ramp_color(ramp, 0.1 + value * 0.9)}"/>')
    return "".join(dots)


def corner_box(x, y, w, h, color, tick=14):
    d = (f"M{x},{y + tick}V{y}H{x + tick}M{x + w - tick},{y}H{x + w}V{y + tick}"
         f"M{x + w},{y + h - tick}V{y + h}H{x + w - tick}M{x + tick},{y + h}H{x}V{y + h - tick}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"/>'


def hero(mode):
    t = THEMES[mode]
    a = [(835, 120, 62, 1.0), (680, 262, 42, 0.42), (955, 275, 46, 0.34)]
    b = [(735, 232, 58, 0.98), (915, 74, 44, 0.46), (640, 70, 36, 0.28)]
    box_w, box_h = 166, 148
    ax, ay = a[0][0] - box_w / 2, a[0][1] - box_h / 2
    dx, dy = b[0][0] - a[0][0], b[0][1] - a[0][1]
    style = (
        "@keyframes a{0%,38%{opacity:1}52%,88%{opacity:0}100%{opacity:1}}"
        "@keyframes b{0%,38%{opacity:0}52%,88%{opacity:1}100%{opacity:0}}"
        f"@keyframes t{{0%,38%{{transform:translate(0,0)}}52%,88%{{transform:translate({dx}px,{dy}px)}}100%{{transform:translate(0,0)}}}}"
        ".a{animation:a 12s ease-in-out infinite}.b{opacity:0;animation:b 12s ease-in-out infinite}"
        ".t{animation:t 12s cubic-bezier(.65,0,.35,1) infinite}"
        "@media (prefers-reduced-motion:reduce){.a,.b,.t{animation:none}}"
    )
    label = "attention"
    label_w = text_width(label, MEDIUM, 13, 0.3) + 16
    body = (
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>'
        f'<g class="a">{field_layer(t["ramp"], a, 7)}</g><g class="b">{field_layer(t["ramp"], b, 11)}</g>'
        f'<g class="t">{corner_box(ax, ay, box_w, box_h, t["ink"])}'
        f'<rect x="{ax}" y="{ay - 25}" width="{label_w:.1f}" height="21" rx="3" fill="{t["ink"]}"/>'
        f'{text(ax + 8, ay - 10, label, MEDIUM, 13, t["bg"], tracking=0.3)}</g></g>'
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="13.5" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
        + text(52, 74, "DATA SCIENTIST & SOFTWARE DEVELOPER", SEMIBOLD, 14.5, t["accent"], tracking=1.5)
        + text(49, 162, "Omar Hazem", DISPLAY, 86, t["ink"], tracking=-1.6)
    )
    for i, line in enumerate(wrap("I build computer vision and machine learning systems, from pipelines to explainable models.", REGULAR, 22.5, 505)):
        body += text(52, 208 + i * 32, line, REGULAR, 22.5, t["body"])
    body += text(52, 296, "Data Science & AI at Zewail City  ·  Egypt", MEDIUM, 15.5, t["mute"])
    write_svg(f"hero-{mode}.svg", W, H, body,
              "Omar Hazem, Data Scientist and Software Developer. Builds computer vision and machine learning systems.",
              style)


def button(slug, mode):
    t = THEMES[mode]
    label, icon = BUTTONS[slug]
    w, h = 212, 58
    primary = slug == "resume"
    bg = t["ink"] if primary else t["panel"]
    fg = t["bg"] if primary else t["ink"]
    size = 21
    scale = size / 24
    content_w = size + 11 + text_width(label, SEMIBOLD, 18.5)
    x = (w - content_w) / 2
    body = (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="{bg}" stroke="{bg if primary else t["line"]}" stroke-width="1.5"/>'
        f'<path transform="translate({x:.1f} {(h - size) / 2:.1f}) scale({scale:.3f})" fill="{fg}" fill-rule="evenodd" d="{icon}"/>'
        + text(x + size + 11, 35.5, label, SEMIBOLD, 18.5, fg)
    )
    write_svg(f"btn-{slug}-{mode}.svg", w, h, body, label)


def project_card(p, mode):
    t = THEMES[mode]
    w, h, pad = 490, 312, 28
    body = f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
    body += text(pad, 52, p["name"], DISPLAY, 24, t["ink"])
    if p["year"]:
        body += text(w - pad, 52, p["year"], MEDIUM, 15.5, t["mute"], anchor="end")
    for i, line in enumerate(wrap(p["summary"], REGULAR, 17.5, w - pad * 2)):
        body += text(pad, 88 + i * 26, line, REGULAR, 17.5, t["body"])
    x = pad
    for value, label in p["metrics"]:
        body += text(x, 204, value, DISPLAY, 33, t["accent"])
        body += text(x, 228, label, MEDIUM, 14.5, t["mute"])
        x += max(text_width(value, DISPLAY, 33), text_width(label, MEDIUM, 14.5)) + 34
    body += f'<line x1="{pad}" x2="{w - pad}" y1="252" y2="252" stroke="{t["line"]}" stroke-width="1.5"/>'
    body += text(pad, 283, p["tags"], MEDIUM, 15, t["body"])
    body += text(w - pad, 283, "View repo →", SEMIBOLD, 15, t["ink"], anchor="end")
    metric_text = ", ".join(f"{v} {l}" for v, l in p["metrics"])
    write_svg(f'project-{p["slug"]}-{mode}.svg', w, h, body, f'{p["name"]}: {metric_text}')


def toolkit(mode):
    t = THEMES[mode]
    row, top = 56, 8
    h = top * 2 + row * len(TOOLKIT)
    body = f'<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
    for i, (label, items) in enumerate(TOOLKIT):
        y = top + row * i + 35
        body += text(30, y, label, SEMIBOLD, 18.5, t["ink"])
        body += text(240, y, items, REGULAR, 18.5, t["body"])
        if i:
            line_y = top + row * i
            body += f'<line x1="30" x2="{W - 30}" y1="{line_y}" y2="{line_y}" stroke="{t["line"]}" stroke-width="1.5"/>'
    write_svg(f"toolkit-{mode}.svg", W, h, body, "Technical toolkit")


if __name__ == "__main__":
    for theme in THEMES:
        hero(theme)
        toolkit(theme)
        for slug in BUTTONS:
            button(slug, theme)
        for project in PROJECTS:
            project_card(project, theme)
    print("Built profile graphics")
