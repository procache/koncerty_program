"""
Debug script for Malostranská beseda
Analyze HTML structure to understand event layout
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

url = "https://www.malostranska-beseda.cz/club/program"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)

    # Wait a bit for content
    page.wait_for_timeout(3000)

    html = page.content()

    browser.close()

print(f"Got {len(html)} chars of HTML")

# Save HTML
with open('malostranskabeseda.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'lxml')

# Look for common event patterns
print("\n=== Looking for event containers ===")

# Try different selectors
selectors = [
    ('div.event', 'div with class event'),
    ('div.program', 'div with class program'),
    ('div.item', 'div with class item'),
    ('article', 'article tags'),
    ('div[class*="event"]', 'div with event in class'),
    ('div[class*="program"]', 'div with program in class'),
]

for selector, desc in selectors:
    elements = soup.select(selector)
    if elements:
        print(f"\n{desc}: {len(elements)} found")
        print(f"First element classes: {elements[0].get('class', [])}")

# Look for dates in November
print("\n=== Looking for November dates ===")
november_pattern = re.compile(r'\b(\d{1,2})\.\s*(11|XI)\b')

all_text = soup.get_text()
november_matches = november_pattern.findall(all_text)
print(f"Found {len(november_matches)} November date mentions")

# Look for links with /program/ or /event/
print("\n=== Looking for event links ===")
event_links = soup.find_all('a', href=re.compile(r'/(program|event|akce|concert)/'))
print(f"Found {len(event_links)} potential event links")

if event_links:
    print("\nFirst 5 event links:")
    for link in event_links[:5]:
        print(f"  {link.get('href', '')}")

print("\n=== Analysis complete ===")
