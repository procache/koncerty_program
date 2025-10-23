"""
Debug script 3 for Malostranská beseda
Examine event structure in detail
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

url = "https://www.malostranska-beseda.cz/club/program?year=2025&month=11"

print(f"Fetching: {url} (direct URL with November)")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

print(f"Got {len(html)} chars of HTML")

soup = BeautifulSoup(html, 'lxml')

# Find ticket buttons
ticket_links = soup.find_all('a', href=re.compile(r'ticketstream\.cz/akce/'))
print(f"\nFound {len(ticket_links)} ticket links")

# For each ticket link, traverse up to find the event container
for i, link in enumerate(ticket_links):
    print(f"\n=== Event {i+1} ===")

    # Go up the tree to find a reasonable container
    # Try to find parent with row/card/event class
    current = link
    for _ in range(10):  # Max 10 levels up
        current = current.parent
        if not current:
            break

        classes = current.get('class', [])
        if any(keyword in str(classes).lower() for keyword in ['row', 'event', 'program', 'item']):
            print(f"Found container: {current.name} with classes {classes}")

            # Extract text
            text = current.get_text(separator=' ', strip=True)[:300]
            print(f"Text preview: {text}")

            # Look for date in this container
            date_match = re.search(r'(\d{1,2})\.\s*11\.\s*(\d{4})', text)
            if date_match:
                print(f"Date found: {date_match.group(0)}")

            # Look for time
            time_match = re.search(r'(\d{1,2}):(\d{2})', text)
            if time_match:
                print(f"Time found: {time_match.group(0)}")

            break

print("\n=== Analysis complete ===")
