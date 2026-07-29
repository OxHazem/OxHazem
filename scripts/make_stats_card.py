"""
Generates stats-card.svg — a terminal-style card showing GitHub stats
fetched via the public GitHub REST API (no token required).

Run from repo root: python scripts/make_stats_card.py [username]
"""
import requests
import sys
import json
from datetime import datetime

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "OxHazem"
HEADERS  = {"Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

print(f"Fetching stats for {USERNAME}...")

# ── Basic user info ──────────────────────────────────────────────
user      = fetch(f"https://api.github.com/users/{USERNAME}")
followers = user.get("followers", 0)
following = user.get("following", 0)
pub_repos = user.get("public_repos", 0)

# ── Aggregate across all public repos ───────────────────────────
stars = forks = watchers = 0
page  = 1
while True:
    repos = fetch(f"https://api.github.com/users/{USERNAME}/repos"
                  f"?per_page=100&page={page}")
    if not repos:
        break
    for r in repos:
        stars    += r.get("stargazers_count", 0)
        forks    += r.get("forks_count", 0)
        watchers += r.get("watchers_count", 0)
    page += 1

updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# ── SVG ─────────────────────────────────────────────────────────
W, H = 480, 220

def stat_block(x, y, icon, label, value, delay):
    return f"""
  <!-- {label} -->
  <text x="{x}" y="{y}" class="mono fade" font-size="22" fill="#7ee787" style="animation-delay:{delay}s;">{icon}</text>
  <text x="{x+28}" y="{y}"   class="mono fade val" font-size="18" fill="#c9d1d9" style="animation-delay:{delay+0.05}s;">{value}</text>
  <text x="{x+28}" y="{y+16}" class="mono fade lbl" font-size="11" fill="#484f58" style="animation-delay:{delay+0.08}s;">{label}</text>"""

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<style>
  @keyframes fadeSlide {{
    0%   {{ opacity:0; transform:translateY(6px); }}
    100% {{ opacity:1; transform:translateY(0); }}
  }}
  .mono {{ font-family:'Courier New',Courier,monospace; }}
  .fade {{ opacity:0; animation:fadeSlide 0.4s forwards; }}
  .val  {{ font-weight:bold; }}
  .lbl  {{ letter-spacing:1px; text-transform:uppercase; }}
</style>

<!-- Background -->
<rect width="{W}" height="{H}" rx="10" ry="10" fill="#0d1117"/>
<!-- Title bar -->
<rect width="{W}" height="28" rx="10" ry="10" fill="#161b22"/>
<rect y="18" width="{W}" height="10" fill="#161b22"/>
<circle cx="18" cy="14" r="5" fill="#ff5f56"/>
<circle cx="34" cy="14" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="14" r="5" fill="#27c93f"/>
<text x="{W//2}" y="19" class="mono" font-size="11" fill="#484f58" text-anchor="middle">git log --stat — OxHazem</text>

<!-- Prompt -->
<text x="16" y="56" class="mono fade" font-size="12" style="animation-delay:0.0s;">
  <tspan fill="#f78166">OxHazem</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">github</tspan><tspan fill="#c9d1d9"> ~ $ cat github-stats.json</tspan>
</text>

<!-- Separator -->
<line x1="16" y1="66" x2="{W-16}" y2="66" stroke="#30363d" stroke-width="1"/>

<!-- Stat blocks — row 1 -->
{stat_block(20,  100, "⭐", "Total Stars",    stars,    0.15)}
{stat_block(135, 100, "📁", "Public Repos",   pub_repos,0.25)}
{stat_block(250, 100, "👥", "Followers",      followers,0.35)}
{stat_block(365, 100, "🍴", "Forks",          forks,    0.45)}

<!-- Separator -->
<line x1="16" y1="138" x2="{W-16}" y2="138" stroke="#30363d" stroke-width="1"/>

<!-- Footer timestamp -->
<text x="16" y="155" class="mono fade" font-size="11" fill="#484f58" style="animation-delay:0.55s;">Last refreshed: {updated}</text>

<!-- Status bar -->
<rect x="16" y="170" width="{W-32}" height="28" rx="5" fill="#161b22"/>
<text x="24" y="188" class="mono fade" font-size="12" fill="#7ee787" style="animation-delay:0.6s;">● Live</text>
<text x="70" y="188" class="mono fade" font-size="12" fill="#8b949e" style="animation-delay:0.65s;">Auto-updated daily via GitHub Actions</text>
</svg>"""

with open("stats-card.svg", "w") as f:
    f.write(svg)
print(f"Success! Created stats-card.svg  (stars={stars}, repos={pub_repos}, followers={followers}, forks={forks})")
