"""
Debug script to analyze O2 Universum page structure
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.o2universum.cz/en/events/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print(f"Opening {url}...")
    page.goto(url, wait_until='networkidle', timeout=60000)

    # Wait for events to load
    page.wait_for_timeout(5000)

    # Get HTML
    html = page.content()

    # Save for analysis
    with open('o2universum.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    print("\n=== Looking for event containers ===")

    # Try to find event listings
    event_divs = soup.find_all('div', class_='event_preview')
    print(f"Found {len(event_divs)} <div class='event_preview'> elements")

    # Print first event
    if event_divs:
        print("\n=== First event structure ===")
        print(event_divs[0].prettify()[:500])

    browser.close()

print("\nHTML saved to o2universum.html")
