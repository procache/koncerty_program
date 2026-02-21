"""
Debug script for Reduta Jazz Club
Analyze HTML structure
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

url = "https://www.redutajazzclub.cz/program"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

print(f"Got {len(html)} chars of HTML")

# Save HTML
with open('reduta.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'lxml')

# Look for event containers
print("\n=== Looking for event containers ===")

selectors = [
    ('div.event', 'div.event'),
    ('div.program-item', 'div.program-item'),
    ('article', 'article tags'),
    ('div[class*="event"]', 'div with event class'),
    ('div[class*="program"]', 'div with program class'),
    ('a[href*="/program/"]', 'program links'),
]

for selector, desc in selectors:
    elements = soup.select(selector)
    if elements:
        print(f"{desc}: {len(elements)} found")

# Look for November dates
print("\n=== Looking for November dates ===")
november_pattern = re.compile(r'\b(\d{1,2})\.\s*(11|XI)\b')
all_text = soup.get_text()
november_matches = november_pattern.findall(all_text)
print(f"Found {len(november_matches)} November date mentions")

# Look for links
print("\n=== Event links ===")
all_links = soup.find_all('a', href=True)
event_links = [a for a in all_links if '/program/' in a.get('href', '') or '/akce/' in a.get('href', '')]
print(f"Found {len(event_links)} event-related links")

if event_links:
    print("\nFirst 5:")
    for link in event_links[:5]:
        print(f"  {link.get('href', '')} -> {link.get_text(strip=True)[:40]}")

print("\n=== Done ===")
