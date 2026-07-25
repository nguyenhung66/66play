import json
from html import unescape

import requests
from bs4 import BeautifulSoup

URL = "https://phaohoa1.live/"
URL = "https://tinhlagi.pro/sport/"
URL = "https://biaomtv09.live/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

m3u = ["#EXTM3U"]
seen = set()

for btn in soup.select(".js-match-btn"):
    title = btn.get("data-title")
    if not title or title in seen:
        continue
    seen.add(title)

    link = unescape(btn.get("data-url", ""))
    league = btn.get("data-league", "")
    logo = ""

    try:
        sources = json.loads(unescape(btn.get("data-sources", "[]")))
        if sources:
            logo = sources[0].get("logo", "")
    except Exception:
        pass

    m3u.append(
        f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}" group-title="{league}",{title}'
    )
    m3u.append(link)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u))

print(f"Đã tạo playlist.m3u với {len(seen)} trận.")
