"""Debug script for MeetFactory Czech version"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

# Fetch Czech version
print("Fetching MeetFactory Czech page...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://meetfactory.cz/cs/program/hudba", wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(3000)
    html = page.content()
    browser.close()

print(f"HTML fetched: {len(html)} chars")

soup = BeautifulSoup(html, 'lxml')

# Look for November dates
print("\n=== Looking for November dates ===\n")
all_text = soup.get_text(separator='\n')
lines = [l.strip() for l in all_text.split('\n') if l.strip()]

# Find November patterns
nov_patterns = [
    r'(\d{1,2})\.\s*11\.',
    r'(\d{1,2})/11',
    r'listopad',
]

for pattern in nov_patterns:
    matches = re.findall(pattern, all_text, re.I)
    if matches:
        print(f'Pattern "{pattern}": {len(matches)} matches')
        if pattern == r'(\d{1,2})\.\s*11\.':
            print(f'  Dates: {set(matches)}')

# Look for event containers
print("\n=== Looking for event containers ===\n")
article_tags = soup.find_all('article')
print(f'Found {len(article_tags)} article tags')

div_items = soup.find_all('div', class_=re.compile('item|event|program', re.I))
print(f'Found {len(div_items)} div.item/event/program elements')

# Try to extract events
print("\n=== Extracting events ===\n")
events = []

# Look for article or div containers
containers = soup.find_all(['article', 'div'], class_=re.compile('event|item|program', re.I))
print(f'Found {len(containers)} potential event containers')

for i, container in enumerate(containers[:10]):
    text = container.get_text(separator='|', strip=True)

    # Look for date
    date_match = re.search(r'(\d{1,2})\.\s*11\.', text)

    if date_match:
        day = date_match.group(1)

        # Look for link
        link = container.find('a', href=True)
        url = link.get('href', '') if link else ''
        if url.startswith('/'):
            url = f"https://meetfactory.cz{url}"

        # Get artist (link text or nearby text)
        artist = link.get_text(strip=True) if link else ""

        print(f"{day}.11. - {artist[:50]} - {url[:60]}")

        events.append({
            'day': day,
            'artist': artist,
            'url': url,
            'raw_text': text[:150]
        })

print(f"\nTotal November events found: {len(events)}")

# Save to JSON
with open('meetfactory_nov_events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=2, ensure_ascii=False)

print("Saved to meetfactory_nov_events.json")
