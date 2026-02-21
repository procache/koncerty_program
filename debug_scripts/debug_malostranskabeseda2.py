"""
Debug script 2 for Malostranská beseda
Try clicking the November 2025 link to load events
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
    print("Initial page loaded")

    # Wait for page to settle
    page.wait_for_timeout(2000)

    # Look for November 2025 link
    print("\nLooking for November 2025 link...")
    november_link = page.query_selector('a[href*="year=2025"][href*="month=11"]')

    if november_link:
        print("Found November link, clicking...")
        november_link.click()

        # Wait for AJAX content to load
        page.wait_for_timeout(3000)

        html = page.content()
        print(f"After click: {len(html)} chars of HTML")

        # Save HTML after click
        with open('malostranskabeseda_november.html', 'w', encoding='utf-8') as f:
            f.write(html)

        soup = BeautifulSoup(html, 'lxml')

        # Look for event cards/items
        print("\n=== Looking for event containers after click ===")

        # Try different patterns
        patterns = [
            ('div.card', 'event cards'),
            ('div.event-item', 'event items'),
            ('article', 'articles'),
            ('div[class*="event"]', 'divs with event class'),
        ]

        for selector, desc in patterns:
            elements = soup.select(selector)
            if elements:
                print(f"{desc}: {len(elements)} found")

        # Count November dates
        november_pattern = re.compile(r'\b(\d{1,2})\.\s*(11|XI)\b')
        all_text = soup.get_text()
        november_matches = november_pattern.findall(all_text)
        print(f"\nNovember date mentions: {len(november_matches)}")

        # Look for all links
        all_links = soup.find_all('a', href=True)
        event_links = [a for a in all_links if '/akce/' in a.get('href', '') or 'ticketstream' in a.get('href', '')]
        print(f"Event links (akce/ticketstream): {len(event_links)}")

        if event_links:
            print("\nFirst 10 event links:")
            for link in event_links[:10]:
                href = link.get('href', '')
                text = link.get_text(strip=True)[:50]
                print(f"  {href} -> {text}")

    else:
        print("November link not found!")

    browser.close()

print("\n=== Analysis complete ===")
