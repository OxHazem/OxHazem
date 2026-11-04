"""Builds profile/contributions-{dark,light}.svg from the public contribution calendar.

If GitHub cannot be reached or its markup changes, the existing graphics are kept.
"""
import re
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup

from svg_kit import DISPLAY, MEDIUM, REGULAR, THEMES, text, text_width, write_svg

USERNAME = "OxHazem"
W, CELL, GAP, GRID_TOP, LEFT = 1000, 14, 3.6, 92, 30


def fetch():
    url = f"https://github.com/users/{USERNAME}/contributions"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Could not fetch contributions ({error}). Keeping existing graphics.")
        sys.exit(0)
    soup = BeautifulSoup(response.text, "html.parser")
    # The calendar table is laid out by weekday, so order cells by date, not by markup.
    days = sorted(
        (date.fromisoformat(td["data-date"]), int(td.get("data-level", 0)))
        for td in soup.select("td.ContributionCalendar-day[data-date]")
    )
    heading = soup.select_one("#js-contribution-activity-description")
    match = re.search(r"[\d,]+", heading.get_text()) if heading else None
    if not days or not match:
        print("Contribution markup not recognised. Keeping existing graphics.")
        sys.exit(0)
    return days, match.group()


def render(days, total, mode):
    t = THEMES[mode]
    first_sunday = days[0][0].toordinal() - (days[0][0].weekday() + 1) % 7
    pitch = CELL + GAP
    height = GRID_TOP + 7 * pitch + 28
    body = (
        f'<rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
        + text(LEFT, 52, total, DISPLAY, 30, t["accent"])
    )
    body += text(LEFT + text_width(total, DISPLAY, 30) + 10, 51, "contributions in the last year", MEDIUM, 18, t["body"])

    last_month_col = -9
    for day, level in days:
        col = (day.toordinal() - first_sunday) // 7
        row = (day.weekday() + 1) % 7
        x, y = LEFT + col * pitch, GRID_TOP + row * pitch
        if day.day <= 7 and row == 0 or (col == 0 and row == 0 and day.day < 20):
            if col - last_month_col >= 3:
                body += text(x, GRID_TOP - 9, day.strftime("%b"), REGULAR, 13.5, t["mute"])
                last_month_col = col
        body += f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{t["ramp"][min(level, 4)]}"/>'

    more_width = text_width("More", REGULAR, 13.5)
    x = W - LEFT - more_width - 10 - 5 * pitch + GAP
    body += text(x - 10, 49, "Less", REGULAR, 13.5, t["mute"], anchor="end")
    body += text(W - LEFT, 49, "More", REGULAR, 13.5, t["mute"], anchor="end")
    for i, color in enumerate(t["ramp"]):
        body += f'<rect x="{x + i * pitch:.1f}" y="38" width="{CELL}" height="{CELL}" rx="3" fill="{color}"/>'
    write_svg(f"contributions-{mode}.svg", W, int(height), body,
              f"{total} GitHub contributions in the last year")


if __name__ == "__main__":
    calendar, count = fetch()
    for theme in THEMES:
        render(calendar, count, theme)
    print(f"Built contribution graphics ({count} contributions, {len(calendar)} days)")
