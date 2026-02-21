"""Test Playwright scraping"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

url = 'https://rockcafe.cz/en/program/'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Loading {url}...")
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

    print(f"Fetched {len(html)} chars of HTML\n")

    soup = BeautifulSoup(html, 'lxml')

    # Find all links
    links = soup.find_all('a', href=True)
    event_links = [a for a in links if '/en/program/' in a.get('href', '')]

    print(f"Found {len(event_links)} links with /en/program/\n")

    # Show first 5 music events
    music_count = 0
    for link in event_links[:50]:
        href = link.get('href', '')

        # Skip archive
        if any(f'/{year}/' in href for year in range(2010, 2027)):
            continue

        category = link.find('span')
        if category and 'music' in category.get_text(strip=True).lower():
            music_count += 1

            if music_count <= 5:
                print(f"Event {music_count}:")
                print(f"  URL: {href}")
                print(f"  Category: {category.get_text(strip=True)}")

                title = link.find('h3')
                if title:
                    print(f"  Title: {title.get_text(strip=True)}")

                date_p = link.find('p')
                if date_p:
                    date_text = date_p.get_text(strip=True)
                    print(f"  Date text: {date_text}")

                    # Try to parse date
                    date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_text)
                    if date_match:
                        day, month, year = date_match.groups()
                        print(f"  Parsed: {day}.{month}.{year}")
                        if month == '11':
                            print(f"  -> NOVEMBER EVENT!")

                print()

    print(f"\nTotal music events found: {music_count}")
