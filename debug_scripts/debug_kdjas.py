"""
Debug script to analyze KD JAS GoOut page
URL: https://goout.net/en/kd-jas/vzvtab/events/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_kdjas():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://goout.net/en/kd-jas/vzvtab/events/"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("kdjas.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to kdjas.html ({len(html)} bytes)")

        # Look for event divs
        event_divs = page.query_selector_all("div.event")
        print(f"\nFound {len(event_divs)} div.event elements")

        # Look for November dates
        november_pattern = r'(\d{2})/11'
        matches = re.findall(november_pattern, html)
        print(f"\nFound {len(matches)} potential November date matches: {matches}")

        # Check if page says "no events"
        if "no event" in html.lower() or "žádné akce" in html.lower():
            print("\nPage indicates no events found")

        browser.close()

if __name__ == "__main__":
    analyze_kdjas()
