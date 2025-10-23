"""
Debug script 3 for Reduta Jazz Club
Parse event data from data-label JSON
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

url = "https://www.redutajazzclub.cz/program-cs/112025"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'lxml')

# Find all td elements with November 2025 dates
event_tds = soup.find_all('td', id=re.compile(r'2025-11-\d{2}'))
print(f"Found {len(event_tds)} November event cells")

events = []

for td in event_tds:
    try:
        # Get the ID to extract date
        td_id = td.get('id', '')
        date_match = re.search(r'2025-11-(\d{2})', td_id)
        if not date_match:
            continue

        day = int(date_match.group(1))

        # Get data-label which contains JSON
        data_label = td.get('data-label', '')
        if not data_label:
            continue

        # Parse JSON
        event_data = json.loads(data_label)

        # Extract time and artist from body HTML
        body_html = event_data.get('body', '')
        body_soup = BeautifulSoup(body_html, 'lxml')

        # Time
        time_span = body_soup.find('span', class_='tt-time')
        time_str = time_span.get_text(strip=True) if time_span else "19:00"

        # Artist
        text_span = body_soup.find('span', class_='tt-text')
        artist = text_span.get_text(strip=True) if text_span else ""

        # URL
        url_link = td.get('data-link', '')

        if artist:
            events.append({
                'day': day,
                'date': f"{day:02d}.11.2025",
                'time': time_str,
                'artist': artist,
                'url': url_link
            })

    except Exception as e:
        print(f"Error parsing event: {e}")
        continue

# Sort by day
events.sort(key=lambda x: x['day'])

print(f"\nExtracted {len(events)} events")

# Save
with open('reduta_all_events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print("Saved to reduta_all_events.json")

# Show first 3
print("\nFirst 3 events:")
for event in events[:3]:
    print(f"  {event['date']} {event['time']} - {event['artist'][:60]}")
