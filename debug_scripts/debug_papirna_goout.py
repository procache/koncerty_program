"""
Debug script to analyze Papírna Plzeň on GoOut
URL: https://goout.net/en/papirna/vzkoab/events/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_papirna_goout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://goout.net/en/papirna/vzkoab/events/"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("papirna_goout.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to papirna_goout.html ({len(html)} bytes)")

        # Look for event divs (GoOut structure)
        event_divs = page.query_selector_all("div.event")
        print(f"\nFound {len(event_divs)} div.event elements")

        # Look for November dates in GoOut format
        november_pattern = r'(\d{2})/11'
        matches = re.findall(november_pattern, html)
        print(f"\nFound {len(matches)} November date matches: {set(matches)}")

        browser.close()

if __name__ == "__main__":
    analyze_papirna_goout()
