"""
Generates langs-card.svg — premium horizontal-bar language breakdown card.
Uses the GitHub REST API.

In GitHub Actions the GITHUB_TOKEN secret is injected automatically (5000 req/hr).
Locally it falls back to unauthenticated (60 req/hr). You can also set:
  export GITHUB_TOKEN=ghp_your_token

Run from repo root: python scripts/make_langs_card.py [username]
"""
import requests, sys, os
from datetime import datetime

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "OxHazem"
TOKEN    = os.environ.get("GITHUB_TOKEN", "")
HEADERS  = {"Accept": "application/vnd.github+json",
             "X-GitHub-Api-Version": "2022-11-28"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"
    print("Using GITHUB_TOKEN (5000 req/hr)")
else:
    print("No GITHUB_TOKEN found — using unauthenticated (60 req/hr)")

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code == 403:
        # Rate limited — exit gracefully so the old SVG is kept
        remaining = r.headers.get("X-RateLimit-Remaining", "?")
        reset     = r.headers.get("X-RateLimit-Reset", "?")
        print(f"⚠️  Rate limited (remaining={remaining}, resets={reset}). "
              f"Keeping existing langs-card.svg.")
        sys.exit(0)
    r.raise_for_status()
    return r.json()

# Languages to skip — these inflate byte counts but don't represent code you *wrote*.
# Jupyter Notebook = raw JSON with embedded outputs/images (1 notebook ≈ 50 MB)
# TeX, Markdown, HTML etc. are markup, not programming languages.
SKIP_LANGS = {
    "Jupyter Notebook", "TeX", "Procfile", "Makefile",
    "Dockerfile", "Shell", "Batchfile", "PowerShell",
    "HTML", "CSS", "SCSS", "Less",
}

print(f"Fetching language data for {USERNAME}...")

lang_bytes: dict[str, int] = {}
page = 1
while True:
    repos = fetch(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}")
    if not repos: break
    for repo in repos:
        if repo.get("fork"): continue
        try:
            for lang, b in fetch(repo["languages_url"]).items():
                if lang in SKIP_LANGS:
                    continue   # skip inflated / non-programming languages
                lang_bytes[lang] = lang_bytes.get(lang, 0) + b
        except Exception:
            pass
    page += 1

if not lang_bytes:
    lang_bytes = {"Python": 60, "C++": 20, "Java": 10, "SQL": 5, "Other": 5}

total        = sum(lang_bytes.values()) or 1
sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:7]
max_pct      = sorted_langs[0][1] / total   # for normalising bar width

COLORS = {
    "Python":           "#3572A5", "C++":        "#f34b7d",
    "C":                "#555555", "Java":       "#b07219",
    "JavaScript":       "#f1e05a", "TypeScript": "#2b7489",
    "C#":               "#178600", "HTML":       "#e34c26",
    "CSS":              "#563d7c", "Rust":       "#dea584",
    "Go":               "#00ADD8", "SQL":        "#e38c00",
    "Shell":            "#89e051", "Jupyter Notebook": "#DA5B0B",
    "TeX":              "#3D6117",
}
FALLBACK = ["#58a6ff","#7ee787","#f78166","#d2a8ff","#ffa657","#79c0ff","#56d364"]

def lang_color(lang, idx):
    return COLORS.get(lang, FALLBACK[idx % len(FALLBACK)])

updated = datetime.utcnow().strftime("%Y-%m-%d")

# ── SVG layout ────────────────────────────────────────────────────
W      = 420
ROWS   = len(sorted_langs)
ROW_H  = 32
H      = 54 + 40 + ROWS * ROW_H + 24    # title-bar + header + rows + footer
BAR_X  = 130   # left edge of bars
BAR_W  = W - BAR_X - 16   # max bar width

rows_svg = ""
for idx, (lang, b) in enumerate(sorted_langs):
    pct      = b / total
    bar_fill = int(BAR_W * (pct / max_pct))   # normalised to widest bar
    color    = lang_color(lang, idx)
    y        = 92 + idx * ROW_H
    delay    = 0.2 + idx * 0.07

    # Label
    rows_svg += (
        f'<circle cx="18" cy="{y+1}" r="5" fill="{color}" opacity="0" '
        f'style="animation:fadeSlide .3s {delay:.2f}s forwards;"/>\n'
        f'<text x="30" y="{y+5}" class="mono fade lname" font-size="12" fill="#c9d1d9" '
        f'style="animation-delay:{delay:.2f}s;">{lang}</text>\n'
    )
    # Bar background
    rows_svg += (
        f'<rect x="{BAR_X}" y="{y-9}" width="{BAR_W}" height="14" rx="4" fill="#161b22"/>\n'
    )
    # Bar fill (animated width via clip trick)
    rows_svg += (
        f'<rect x="{BAR_X}" y="{y-9}" width="{bar_fill}" height="14" rx="4" fill="{color}" '
        f'opacity="0" style="animation:fadeSlide .4s {delay+.05:.2f}s forwards;"/>\n'
    )
    # Percentage
    rows_svg += (
        f'<text x="{W-8}" y="{y+5}" class="mono fade pct" font-size="11" fill="#8b949e" '
        f'text-anchor="end" style="animation-delay:{delay+.08:.2f}s;">{pct*100:.1f}%</text>\n'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<style>
  @keyframes fadeSlide {{
    0%   {{ opacity:0; transform:translateY(5px); }}
    100% {{ opacity:1; transform:translateY(0); }}
  }}
  .mono  {{ font-family:'Courier New',Courier,monospace; }}
  .fade  {{ opacity:0; animation:fadeSlide .4s forwards; }}
  .lname {{ font-weight:500; }}
  .pct   {{ font-weight:bold; }}
</style>

<!-- Background -->
<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>

<!-- Title bar -->
<rect width="{W}" height="30" rx="10" fill="#161b22"/>
<rect y="20" width="{W}" height="10" fill="#161b22"/>
<circle cx="18" cy="15" r="5.5" fill="#ff5f56"/>
<circle cx="36" cy="15" r="5.5" fill="#ffbd2e"/>
<circle cx="54" cy="15" r="5.5" fill="#27c93f"/>
<text x="{W//2}" y="20" class="mono" font-size="11" fill="#484f58" text-anchor="middle">
  top-langs — {USERNAME}
</text>

<!-- Prompt -->
<text x="16" y="54" class="mono fade" font-size="12" style="animation-delay:.0s;">
  <tspan fill="#f78166">{USERNAME}</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">github</tspan>
  <tspan fill="#8b949e"> ~ $ </tspan><tspan fill="#c9d1d9">cloc --sort=code ~/projects/</tspan>
</text>

<!-- Section heading -->
<text x="16" y="78" class="mono fade" font-size="13" fill="#7ee787" font-weight="bold"
      style="animation-delay:.08s;">Most Used Languages</text>
<line x1="16" y1="84" x2="{W-16}" y2="84" stroke="#21262d" stroke-width="1"/>

<!-- Column headers -->
<text x="30"      y="98" class="mono" font-size="10" fill="#30363d">LANGUAGE</text>
<text x="{BAR_X}" y="98" class="mono" font-size="10" fill="#30363d">USAGE</text>
<text x="{W-8}"   y="98" class="mono" font-size="10" fill="#30363d" text-anchor="end">%</text>

<!-- Language rows -->
{rows_svg}
<!-- Footer -->
<text x="16" y="{H-6}" class="mono" font-size="10" fill="#30363d">
  Public repos only · excludes forks · {updated}
</text>
</svg>"""

with open("langs-card.svg", "w") as f:
    f.write(svg)
print(f"✅ langs-card.svg  ({len(sorted_langs)} languages)")
