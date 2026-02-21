"""
Debug script to analyze Watt Music Club GoOut page structure
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://goout.net/en/watt-music-club/vztpab/events/"

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
    with open('watt_goout.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    # Look for event containers
    print("\n=== Looking for event containers ===")

    # Try common GoOut selectors
    events = soup.find_all('article', class_=lambda x: x and 'event' in x.lower())
    print(f"Found {len(events)} <article class='*event*'> elements")

    events2 = soup.find_all('div', class_=lambda x: x and 'event' in x.lower())
    print(f"Found {len(events2)} <div class='*event*'> elements")

    # Print first event structure
    if events:
        print("\n=== First event HTML ===")
        print(events[0].prettify()[:1000])
    elif events2:
        print("\n=== First event HTML ===")
        print(events2[0].prettify()[:1000])

    browser.close()

print("\nHTML saved to watt_goout.html")
