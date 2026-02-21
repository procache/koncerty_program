"""
Debug script to analyze Kulturní dům Šeříkovka website structure
URL: https://www.serikovka.cz/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_serikovka():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.serikovka.cz/"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("serikovka.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to serikovka.html ({len(html)} bytes)")

        # Look for event containers
        event_selectors = [
            ".event",
            ".event-item",
            ".program-item",
            "article",
            "[class*='event']",
            "[class*='program']",
            ".akce",
        ]

        for selector in event_selectors:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"\nFound {len(elements)} elements with selector: {selector}")

                # Inspect first element
                if len(elements) > 0:
                    first = elements[0]
                    print(f"   First element HTML:\n{first.inner_html()[:500]}")

        # Look for November dates
        november_pattern = r'(\d{1,2})[.\s-]+(11|listopadu|lis)'
        matches = re.findall(november_pattern, html, re.IGNORECASE)
        print(f"\nFound {len(matches)} potential November date matches")

        # Look for links
        links = page.query_selector_all("a[href*='event'], a[href*='program'], a[href*='akce']")
        print(f"\nFound {len(links)} event/program links")
        if len(links) > 0:
            print(f"   Example: {links[0].get_attribute('href')}")

        browser.close()

if __name__ == "__main__":
    analyze_serikovka()
