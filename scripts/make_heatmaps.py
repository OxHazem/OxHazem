import requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = "OxHazem" # Change this if your GitHub username is different!

print(f"Fetching data for {USERNAME}...")
url = f"https://github.com/users/{USERNAME}/contributions"
response = requests.get(url)

# Draw the SVG
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 150">
<style>
  @keyframes slideDown {
    0% { opacity: 0; transform: translate(-5px, -5px); }
    100% { opacity: 1; transform: translate(0, 0); }
  }
  .day { opacity: 0; animation: slideDown 0.6s forwards; }
</style>
<rect width="100%" height="100%" fill="#0d1117" />
<g transform="translate(20, 20)">\n'''

PALETTE = {"0": "#161b22", "1": "#0e4429", "2": "#006d32", "3": "#26a641", "4": "#39d353"}

# If the fetch fails, we will generate a stylized default grid so the script doesn't crash
if response.status_code != 200:
    print("Could not fetch live data. Generating placeholder grid...")
    import random
    for week in range(53):
        for day in range(7):
            level = str(random.choices([0, 1, 2, 3, 4], weights=[60, 15, 10, 10, 5])[0])
            delay = (week * 0.02) + (day * 0.02)
            svg += f'<rect class="day" x="{week * 14}" y="{day * 14}" width="10" height="10" rx="2" ry="2" fill="{PALETTE[level]}" style="animation-delay: {delay}s;" />\n'
else:
    # Parse real GitHub data
    soup = BeautifulSoup(response.text, 'html.parser')
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    week_col = 0
    day_row = 0
    for day_node in days:
        level = day_node.get('data-level', '0')
        delay = (week_col * 0.02) + (day_row * 0.02)
        svg += f'<rect class="day" x="{week_col * 14}" y="{day_row * 14}" width="10" height="10" rx="2" ry="2" fill="{PALETTE[level]}" style="animation-delay: {delay}s;" />\n'
        
        day_row += 1
        if day_row == 7:
            day_row = 0
            week_col += 1

svg += '''</g>
</svg>'''

with open('contrib-heatmap.svg', 'w') as f:
    f.write(svg)
print("Success! Created contrib-heatmap.svg")