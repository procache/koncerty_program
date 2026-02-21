"""
Debug script to analyze Tipsport Arena on Ticketportal
URL: https://www.ticketportal.cz/venue/TIPSPORT-ARENA
"""
from playwright.sync_api import sync_playwright
import re

def analyze_tipsport_arena():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.ticketportal.cz/venue/TIPSPORT-ARENA"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("tipsport_arena_ticketportal.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to tipsport_arena_ticketportal.html ({len(html)} bytes)")

        # Look for event containers
        selectors = [
            "div.event",
            "article.event",
            "div[class*='event']",
            "div.card",
            "a[href*='/event/']",
        ]

        for selector in selectors:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"\nFound {len(elements)} elements with selector: {selector}")

        # Look for November dates in various formats
        patterns = [
            (r'(\d{1,2})\.\s*11\.', 'DD. 11.'),
            (r'11/(\d{1,2})', '11/DD'),
            (r'listopad', 'listopad'),
            (r'November', 'November'),
            (r'2025-11-(\d{2})', '2025-11-DD'),
        ]

        for pattern, desc in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                print(f"\nPattern '{desc}': {len(matches)} matches - {set(list(matches)[:10])}")

        browser.close()

if __name__ == "__main__":
    analyze_tipsport_arena()
