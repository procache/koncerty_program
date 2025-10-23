"""
Debug script 2 for Reduta Jazz Club
Try direct URL with month/year
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

# Try November 2025 directly
url = "https://www.redutajazzclub.cz/program-cs/112025"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

print(f"Got {len(html)} chars of HTML")

# Save
with open('reduta_november.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'lxml')

# Look for November dates
november_pattern = re.compile(r'2025-11-(\d{2})')
dates_found = november_pattern.findall(html)
print(f"\nFound {len(set(dates_found))} unique November 2025 dates")

# Look for event data in data-link attributes
event_tds = soup.find_all('td', {'data-link': True})
print(f"Found {len(event_tds)} td elements with data-link")

november_events = []
for td in event_tds:
    td_id = td.get('id', '')
    if '2025-11' in td_id:
        data_label = td.get('data-label', '')
        data_link = td.get('data-link', '')

        november_events.append({
            'id': td_id,
            'link': data_link,
            'data': data_label[:100]
        })

print(f"Found {len(november_events)} November events")

# Save to JSON
with open('reduta_november_events.json', 'w', encoding='utf-8') as f:
    json.dump(november_events, f, ensure_ascii=False, indent=2)

print("Saved to reduta_november_events.json")
