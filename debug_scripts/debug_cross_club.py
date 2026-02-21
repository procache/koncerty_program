"""
Debug script to analyze Cross Club structure
URL: https://www.crossclub.cz/cs/program/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_cross_club():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.crossclub.cz/cs/program/"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("cross_club.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to cross_club.html ({len(html)} bytes)")

        # Look for various event containers
        selectors = [
            "div.event",
            "div.program-item",
            "article.event",
            "div[class*='event']",
            "div[class*='program']",
            ".fc-event",  # FullCalendar events
            "a.fc-event",
        ]

        for selector in selectors:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"\nFound {len(elements)} elements with selector: {selector}")

        # Look for November dates in various formats
        patterns = [
            r'(\d{1,2})\.\s*11\.',  # DD. 11.
            r'11/(\d{1,2})',         # 11/DD
            r'listopad',             # Czech word for November
            r'November',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                print(f"\nPattern '{pattern}': {len(matches)} matches")

        # Check for calendar/scheduler libraries
        calendar_indicators = ['fullcalendar', 'scheduler', 'calendar', 'fc-']
        for indicator in calendar_indicators:
            if indicator.lower() in html.lower():
                print(f"\n✓ Found '{indicator}' in HTML")

        browser.close()

if __name__ == "__main__":
    analyze_cross_club()
