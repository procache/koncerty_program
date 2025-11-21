"""
Debug script 6 for Malostranská beseda
Extract all November events and save to JSON (avoid console encoding issues)
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

url = "https://www.malostranska-beseda.cz/club/program?year=2025&month=11"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'lxml')

# Find ALL divs with class row
rows = soup.find_all('div', class_='row')

# Filter for rows that contain November dates
events = []
seen_urls = set()

for row in rows:
    text = row.get_text()
    date_match = re.search(r'(\d{1,2})\.\s*11\.\s*2025', text)

    if not date_match:
        continue

    day = int(date_match.group(1))

    # Time
    time_match = re.search(r'(\d{1,2}):(\d{2})', text)
    time_str = time_match.group(0) if time_match else "20:00"

    # Artist (from h1-h4)
    h_tags = row.find_all(['h1', 'h2', 'h3', 'h4'])
    artist = h_tags[0].get_text(strip=True) if h_tags else ""

    if not artist:
        continue  # Skip if no artist

    # URL - prefer ticketstream, fallback to goout or other
    links = row.find_all('a', href=True)
    url = ""
    for link in links:
        href = link.get('href', '')
        if 'ticketstream.cz/akce/' in href or 'goout.net' in href:
            url = href if href.startswith('http') else f"https://www.malostranska-beseda.cz{href}"
            break

    # Skip if we've seen this URL before (deduplication)
    if url and url in seen_urls:
        continue

    if url:
        seen_urls.add(url)

    events.append({
        'day': day,
        'date': f"{day:02d}.11.2025",
        'time': time_str,
        'artist': artist,
        'url': url
    })

# Sort by day
events.sort(key=lambda x: x['day'])

# Save to JSON
with open('malostranskabeseda_all_events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(events)} unique events")
print("Saved to malostranskabeseda_all_events.json")
