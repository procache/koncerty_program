"""
Debug script to analyze O2 Arena page structure
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.o2arena.cz/en/events/"

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
    with open('o2arena.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    print("\n=== Looking for event containers ===")

    # Try to find event listings
    events = soup.find_all('div', class_=lambda x: x and 'event' in x.lower())
    print(f"Found {len(events)} <div class='*event*'> elements")

    # Try article tags
    articles = soup.find_all('article')
    print(f"Found {len(articles)} <article> elements")

    # Try h3 tags with links (from WebFetch result)
    h3_links = soup.find_all('h3')
    print(f"Found {len(h3_links)} <h3> elements")

    # Print first few h3 elements
    print("\n=== First 5 H3 elements ===")
    for i, h3 in enumerate(h3_links[:5]):
        print(f"\nH3 #{i+1}:")
        print(h3.prettify()[:300])

    # Look for date/time elements
    time_elements = soup.find_all('time')
    print(f"\n=== Found {len(time_elements)} <time> elements ===")
    for i, time_elem in enumerate(time_elements[:5]):
        print(f"Time #{i+1}: {time_elem}")

    browser.close()

print("\nHTML saved to o2arena.html")
