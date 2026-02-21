"""
Debug script to analyze Divadlo Pod lampou website structure
URL: https://podlampou.cz/events/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_podlampou():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://podlampou.cz/events/"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("podlampou.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\n✅ HTML saved to podlampou.html ({len(html)} bytes)")

        # Look for event containers
        event_selectors = [
            ".event",
            ".event-item",
            ".program-item",
            "article",
            "[class*='event']",
            "[class*='program']",
        ]

        for selector in event_selectors:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"\n✅ Found {len(elements)} elements with selector: {selector}")

                # Inspect first element
                if len(elements) > 0:
                    first = elements[0]
                    print(f"   First element HTML:\n{first.inner_html()[:500]}")

        # Look for November dates
        november_pattern = r'(\d{1,2})[.\s-]+(11|listopadu|lis)'
        matches = re.findall(november_pattern, html, re.IGNORECASE)
        print(f"\n📅 Found {len(matches)} potential November date matches")

        # Look for links
        links = page.query_selector_all("a[href*='event'], a[href*='program'], a[href*='akce']")
        print(f"\n🔗 Found {len(links)} event/program links")
        if len(links) > 0:
            print(f"   Example: {links[0].get_attribute('href')}")

        browser.close()

if __name__ == "__main__":
    analyze_podlampou()
