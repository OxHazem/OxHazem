"""
Generates langs-card.svg — a terminal-style language breakdown card.
Uses the public GitHub REST API to count bytes per language across all public repos.

Run from repo root: python scripts/make_langs_card.py [username]
"""
import requests
import sys
from datetime import datetime

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "OxHazem"
HEADERS  = {"Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

print(f"Fetching language data for {USERNAME}...")

# ── Collect language bytes across all repos ──────────────────────
lang_bytes: dict[str, int] = {}
page = 1
while True:
    repos = fetch(f"https://api.github.com/users/{USERNAME}/repos"
                  f"?per_page=100&page={page}")
    if not repos:
        break
    for repo in repos:
        if repo.get("fork"):
            continue          # skip forks — count only original work
        if repo.get("language"):
            langs_url = repo["languages_url"]
            try:
                repo_langs = fetch(langs_url)
                for lang, b in repo_langs.items():
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + b
            except Exception:
                pass
    page += 1

if not lang_bytes:
    # Fallback: write a placeholder SVG so the profile doesn't break
    print("No language data found — writing placeholder.")
    lang_bytes = {"Python": 60, "C++": 20, "Java": 10, "SQL": 5, "Other": 5}

# ── Sort & pick top 8 ────────────────────────────────────────────
total   = sum(lang_bytes.values()) or 1
sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:8]

# ── Color palette (deterministic by lang name) ───────────────────
COLORS = {
    "Python":     "#3572A5",
    "C++":        "#f34b7d",
    "C":          "#555555",
    "Java":       "#b07219",
    "JavaScript": "#f1e05a",
    "TypeScript": "#2b7489",
    "C#":         "#178600",
    "HTML":       "#e34c26",
    "CSS":        "#563d7c",
    "Rust":       "#dea584",
    "Go":         "#00ADD8",
    "SQL":        "#e38c00",
    "Shell":      "#89e051",
    "Jupyter Notebook": "#DA5B0B",
}
FALLBACK_COLORS = ["#58a6ff","#7ee787","#f78166","#d2a8ff","#ffa657","#79c0ff","#56d364","#ff7b72"]

def color_for(lang, idx):
    return COLORS.get(lang, FALLBACK_COLORS[idx % len(FALLBACK_COLORS)])

# ── SVG dimensions ───────────────────────────────────────────────
W, H      = 420, 240
BAR_X     = 16
BAR_Y     = 116
BAR_W     = W - 32
BAR_H     = 10

svg_bars  = ""   # the stacked progress bar
svg_rows  = ""   # language rows below it

# Build stacked bar
bar_x_cursor = BAR_X
for idx, (lang, b) in enumerate(sorted_langs):
    pct   = b / total
    seg_w = max(int(BAR_W * pct), 2)
    c     = color_for(lang, idx)
    svg_bars += (f'<rect x="{bar_x_cursor}" y="{BAR_Y}" '
                 f'width="{seg_w}" height="{BAR_H}" fill="{c}" '
                 f'rx="2" ry="2" opacity="0" '
                 f'style="animation: fadeIn 0.4s {0.3 + idx*0.07:.2f}s forwards;"/>\n')
    bar_x_cursor += seg_w

# Build language rows — 2-column grid
cols = 2
col_w = (W - 32) // cols
for idx, (lang, b) in enumerate(sorted_langs):
    pct  = b / total * 100
    c    = color_for(lang, idx)
    col  = idx % cols
    row  = idx // cols
    rx   = BAR_X + col * col_w
    ry   = BAR_Y + 24 + row * 22
    delay = 0.5 + idx * 0.06
    svg_rows += (
        f'<circle cx="{rx+6}" cy="{ry-5}" r="5" fill="{c}" opacity="0" '
        f'style="animation: fadeIn 0.3s {delay:.2f}s forwards;"/>\n'
        f'<text x="{rx+16}" y="{ry}" class="mono fade" font-size="12" '
        f'fill="#c9d1d9" style="animation-delay:{delay:.2f}s;">'
        f'{lang}</text>\n'
        f'<text x="{rx+col_w-12}" y="{ry}" class="mono fade" font-size="11" '
        f'fill="#484f58" text-anchor="end" style="animation-delay:{delay+0.04:.2f}s;">'
        f'{pct:.1f}%</text>\n'
    )

updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<style>
  @keyframes fadeIn  {{ 0% {{ opacity:0; }} 100% {{ opacity:1; }} }}
  @keyframes fadeSlide {{
    0%   {{ opacity:0; transform:translateY(5px); }}
    100% {{ opacity:1; transform:translateY(0); }}
  }}
  .mono {{ font-family:'Courier New',Courier,monospace; }}
  .fade {{ opacity:0; animation:fadeSlide 0.4s forwards; }}
</style>

<!-- Background -->
<rect width="{W}" height="{H}" rx="10" ry="10" fill="#0d1117"/>
<!-- Title bar -->
<rect width="{W}" height="28" rx="10" ry="10" fill="#161b22"/>
<rect y="18" width="{W}" height="10" fill="#161b22"/>
<circle cx="18" cy="14" r="5" fill="#ff5f56"/>
<circle cx="34" cy="14" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="14" r="5" fill="#27c93f"/>
<text x="{W//2}" y="19" class="mono" font-size="11" fill="#484f58" text-anchor="middle">top-langs — OxHazem</text>

<!-- Prompt -->
<text x="16" y="52" class="mono fade" font-size="12" style="animation-delay:0.0s;">
  <tspan fill="#f78166">OxHazem</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">github</tspan><tspan fill="#c9d1d9"> ~ $ cloc --by-lang ~/projects/</tspan>
</text>

<!-- Heading -->
<text x="16" y="74" class="mono fade" font-size="13" fill="#7ee787" font-weight="bold" style="animation-delay:0.1s;">Most Used Languages</text>
<line x1="16" y1="82" x2="{W-16}" y2="82" stroke="#30363d" stroke-width="1"/>

<!-- Section label -->
<text x="16" y="100" class="mono fade" font-size="11" fill="#484f58" style="animation-delay:0.2s;">Language breakdown across public repos (excludes forks)</text>

<!-- Stacked progress bar background -->
<rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" rx="5" fill="#161b22"/>
<!-- Stacked segments -->
{svg_bars}
<!-- Language rows -->
{svg_rows}
<!-- Timestamp -->
<text x="16" y="{H-8}" class="mono" font-size="10" fill="#30363d">Updated: {updated}</text>
</svg>"""

with open("langs-card.svg", "w") as f:
    f.write(svg)
print(f"Success! Created langs-card.svg  ({len(sorted_langs)} languages)")
