"""
Debug script to analyze Papírna Plzeň website structure
URL: https://www.informuji.cz/en/object/4515-papirna/
"""
from playwright.sync_api import sync_playwright
import re

def analyze_papirna():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.informuji.cz/en/object/4515-papirna/"
        print(f"Navigating to: {url}")

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            print("Page loaded successfully")

            # Wait for content to load
            page.wait_for_timeout(3000)

            html = page.content()

            # Save HTML for inspection
            with open("papirna.html", "w", encoding="utf-8") as f:
                f.write(html)

            print(f"\nHTML saved to papirna.html ({len(html)} bytes)")

            # Look for event-related elements
            event_divs = page.query_selector_all("div.event, div.akce, article")
            print(f"\nFound {len(event_divs)} potential event elements")

            # Look for November dates
            november_pattern = r'(\d{1,2})[.\s-]+(11|listopadu|nov)'
            matches = re.findall(november_pattern, html, re.IGNORECASE)
            print(f"\nFound {len(matches)} potential November date matches")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()

if __name__ == "__main__":
    analyze_papirna()
