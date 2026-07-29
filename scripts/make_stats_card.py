"""
Generates stats-card.svg — premium terminal-style GitHub stats card.
Fetches live data from the GitHub public REST API (no token needed).

Run from repo root: python scripts/make_stats_card.py [username]
"""
import requests, sys
from datetime import datetime

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "OxHazem"
HEADERS  = {"Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

print(f"Fetching stats for {USERNAME}...")

user      = fetch(f"https://api.github.com/users/{USERNAME}")
followers = user.get("followers", 0)
pub_repos = user.get("public_repos", 0)
name      = user.get("name") or USERNAME

stars = forks = 0
page  = 1
while True:
    repos = fetch(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}")
    if not repos: break
    for r in repos:
        stars += r.get("stargazers_count", 0)
        forks += r.get("forks_count", 0)
    page += 1

updated = datetime.utcnow().strftime("%Y-%m-%d")

# ── SVG ────────────────────────────────────────────────────────────────────────
W, H = 520, 210

def cell(x, y, w, h, accent, icon, value, label, delay):
    """Renders one stat cell with left accent bar, icon, value, label."""
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#161b22"/>
  <rect x="{x}" y="{y}" width="3" height="{h}" rx="2" fill="{accent}"/>
  <text x="{x+16}" y="{y+28}" font-family="'Segoe UI Emoji',monospace" font-size="18" opacity="0"
        style="animation:fadeSlide .4s {delay:.2f}s forwards;">{icon}</text>
  <text x="{x+16}" y="{y+58}" class="mono val fade" font-size="26" fill="#e6edf3"
        style="animation-delay:{delay+.05:.2f}s;">{value}</text>
  <text x="{x+16}" y="{y+76}" class="mono lbl fade" font-size="10" fill="#484f58"
        style="animation-delay:{delay+.09:.2f}s;">{label}</text>"""

GAP = 12
CW  = (W - 32 - GAP * 3) // 4    # cell width
CH  = 100

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  @keyframes fadeSlide {{
    0%   {{ opacity:0; transform:translateY(8px); }}
    100% {{ opacity:1; transform:translateY(0); }}
  }}
  @keyframes pulse {{
    0%,100% {{ opacity:.6; }} 50% {{ opacity:1; }}
  }}
  .mono {{ font-family:'Courier New',Courier,monospace; }}
  .fade {{ opacity:0; animation:fadeSlide .4s forwards; }}
  .val  {{ font-weight:bold; letter-spacing:-0.5px; }}
  .lbl  {{ letter-spacing:1.5px; text-transform:uppercase; }}
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
  github-stats — {USERNAME}
</text>

<!-- Prompt line -->
<text x="16" y="54" class="mono fade" font-size="12" style="animation-delay:.0s;">
  <tspan fill="#f78166">{USERNAME}</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">github</tspan>
  <tspan fill="#8b949e"> ~ $ </tspan><tspan fill="#c9d1d9">cat stats.json</tspan>
</text>

<!-- 4 stat cells -->
{cell(16,          64, CW, CH, "#58a6ff", "⭐", stars,    "Total  Stars",    .15)}
{cell(16+CW+GAP,   64, CW, CH, "#7ee787", "📁", pub_repos,"Public  Repos",   .25)}
{cell(16+CW*2+GAP*2, 64, CW, CH, "#f78166", "👥", followers,"Followers",     .35)}
{cell(16+CW*3+GAP*3, 64, CW, CH, "#d2a8ff", "🍴", forks,   "Total  Forks",   .45)}

<!-- Bottom bar -->
<rect x="16" y="175" width="{W-32}" height="22" rx="5" fill="#161b22"/>
<circle cx="28" cy="186" r="4" fill="#27c93f" style="animation:pulse 2s infinite;"/>
<text x="40" y="190" class="mono" font-size="11" fill="#7ee787">Live</text>
<text x="74" y="190" class="mono" font-size="11" fill="#484f58">
  Auto-refreshed daily via GitHub Actions · {updated}
</text>
</svg>"""

with open("stats-card.svg", "w") as f:
    f.write(svg)
print(f"✅ stats-card.svg  (⭐{stars} 📁{pub_repos} 👥{followers} 🍴{forks})")
