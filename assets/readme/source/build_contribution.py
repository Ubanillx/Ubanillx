#!/usr/bin/env python3
"""Build the contribution grid SVG from a public GitHub contribution snapshot."""

import datetime as dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "contribution-data.json").read_text())
OUT = HERE.parent / "contribution.svg"

COLORS = ["#101A16", "#1E4B3A", "#2C7A58", "#45B37D", "#62E6A7"]
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif"

start = dt.date.fromisoformat(DATA["start"])
levels = {c["date"]: c["level"] for c in DATA["cells"]}
columns = (dt.date.fromisoformat(DATA["end"]) - start).days // 7 + 1

cells = []
for week in range(columns):
    for weekday in range(7):
        day = start + dt.timedelta(days=week * 7 + weekday)
        if day > dt.date.fromisoformat(DATA["end"]):
            continue
        level = levels.get(day.isoformat(), 0)
        x = 72 + week * 20
        y = 88 + weekday * 20
        cells.append(
            f'<rect x="{x}" y="{y}" width="16" height="16" rx="3" fill="{COLORS[level]}"/>'
        )

legend = []
for index, color in enumerate(COLORS):
    legend.append(
        f'<rect x="{1010 + index * 16}" y="40" width="12" height="12" rx="2.5" fill="{color}"/>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
  <title id="title">Ubanillx contribution grid, last 12 months</title>
  <desc id="desc">{DATA["total"]} contributions from {DATA["start"]} to {DATA["end"]}. Snapshot taken {DATA["snapshot"]}. Source: {DATA["source"]}</desc>

  <rect width="1200" height="260" rx="24" fill="#060A09"/>
  <rect x="0.5" y="0.5" width="1199" height="259" rx="23.5" fill="none" stroke="#17261F"/>

    <text x="72" y="56" font-family="{SANS}" font-size="28" font-weight="700" fill="#E9F3EE">{DATA["total"]}</text>
  <text x="131" y="56" font-family="{SANS}" font-size="20" fill="#8CA39A">contributions · last 12 months</text>

  <text x="1002" y="52" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="1.2" fill="#7A9086">LESS</text>
  {''.join(legend)}
  <text x="1128" y="52" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="1.2" fill="#7A9086">MORE</text>

  {''.join(cells)}

  <text x="1128" y="248" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="1.2" fill="#7A9086">SNAPSHOT · {DATA["snapshot"]}</text>
</svg>
'''
OUT.write_text(svg)
print(f"Wrote {OUT} ({len(cells)} cells, {columns} weeks)")
