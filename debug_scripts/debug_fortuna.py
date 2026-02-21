"""
Debug script to analyze Sportovní hala Fortuna page structure
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.sportovnihalafortuna.cz/"

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
    with open('fortuna.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    print("\n=== Looking for event containers ===")

    # Try to find event listings
    event_lis = soup.find_all('li', class_=lambda x: x and 'event' in str(x).lower())
    print(f"Found {len(event_lis)} <li class='*event*'> elements")

    # Try any li elements
    all_lis = soup.find_all('li')
    print(f"Found {len(all_lis)} <li> elements total")

    # Look for h3 elements (from WebFetch)
    h3_elements = soup.find_all('h3')
    print(f"Found {len(h3_elements)} <h3> elements")

    # Print first few h3 elements with their parent
    print("\n=== First 5 H3 elements with parents ===")
    for i, h3 in enumerate(h3_elements[:5]):
        print(f"\nH3 #{i+1}: {h3.text.strip()}")
        parent = h3.parent
        if parent:
            print(f"Parent tag: {parent.name}, classes: {parent.get('class', [])}")

    browser.close()

print("\nHTML saved to fortuna.html")
