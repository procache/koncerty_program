"""
Debug script 4 for Malostranská beseda
Examine event structure and save to JSON
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

url = "https://www.malostranska-beseda.cz/club/program?year=2025&month=11"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'lxml')

# Find ticket buttons
ticket_links = soup.find_all('a', href=re.compile(r'ticketstream\.cz/akce/'))
print(f"Found {len(ticket_links)} ticket links")

events_data = []

# For each ticket link, traverse up to find the event container
for i, link in enumerate(ticket_links):
    # Go up the tree to find a reasonable container
    current = link
    for _ in range(10):  # Max 10 levels up
        current = current.parent
        if not current:
            break

        classes = current.get('class', [])
        if 'row' in classes:
            # Extract all text
            text = current.get_text(separator=' ', strip=True)

            # Extract URL
            url = link.get('href', '')

            # Look for date
            date_match = re.search(r'(\d{1,2})\.\s*11\.\s*(\d{4})', text)
            date_str = date_match.group(0) if date_match else "not found"

            # Look for time
            time_match = re.search(r'(\d{1,2}):(\d{2})', text)
            time_str = time_match.group(0) if time_match else "not found"

            # Look for artist name (usually first line or in h2/h3)
            h_tags = current.find_all(['h1', 'h2', 'h3', 'h4'])
            artist = h_tags[0].get_text(strip=True) if h_tags else "not found"

            events_data.append({
                'event_num': i + 1,
                'url': url,
                'date': date_str,
                'time': time_str,
                'artist': artist,
                'text_preview': text[:200]
            })

            break

# Save to JSON
with open('malostranskabeseda_events.json', 'w', encoding='utf-8') as f:
    json.dump(events_data, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(events_data)} events to malostranskabeseda_events.json")
print("\nDone!")
