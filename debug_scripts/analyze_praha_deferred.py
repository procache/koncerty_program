"""
Analyze remaining Praha deferred venues
"""
from playwright.sync_api import sync_playwright
import re

venues = [
    {
        'name': 'Lucerna Velky sal',
        'url': 'https://www.lucpra.com/index.php/cz/',
    },
    {
        'name': 'Sportovni hala Fortuna',
        'url': 'https://www.sportovnihalafortuna.cz/',
    },
    {
        'name': 'U Stare Pani (GoOut)',
        'url': 'https://goout.net/en/u-stare-pani-jazz-and-cocktail-club/vzlll/events/',
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for venue in venues:
        print(f"\n{'='*60}")
        print(f"Analyzing: {venue['name']}")
        print(f"URL: {venue['url']}")
        print(f"{'='*60}")

        try:
            page.goto(venue['url'], wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)

            html = page.content()

            # Save HTML
            filename = venue['name'].lower().replace(' ', '_') + '.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"Saved to: {filename} ({len(html)} bytes)")

            # Look for November dates
            patterns = [
                (r'(\d{1,2})\.\s*11\.', 'DD. 11.'),
                (r'11/(\d{1,2})', '11/DD'),
                (r'listopad', 'listopad'),
                (r'November', 'November'),
            ]

            for pattern, desc in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    print(f"  {desc}: {len(matches)} matches - {set(list(matches)[:10])}")

            # Look for common event containers
            selectors = [
                'div.event',
                'div[class*="event"]',
                'article',
                'div.program-item',
                'div[class*="program"]',
            ]

            for selector in selectors:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"  {selector}: {len(elements)} elements")

        except Exception as e:
            print(f"ERROR: {str(e)[:100]}")

    browser.close()
