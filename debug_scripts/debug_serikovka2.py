"""
Debug script to analyze Kulturní dům Šeříkovka website structure (v2 - longer timeout)
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

        try:
            # Try with domcontentloaded instead of networkidle
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print("Page loaded (domcontentloaded)")

            # Wait a bit more
            page.wait_for_timeout(5000)

            html = page.content()

            # Save HTML for inspection
            with open("serikovka.html", "w", encoding="utf-8") as f:
                f.write(html)

            print(f"\nHTML saved to serikovka.html ({len(html)} bytes)")

            # Look for November dates
            november_pattern = r'(\d{1,2})[.\s-]+(11|listopadu|lis)'
            matches = re.findall(november_pattern, html, re.IGNORECASE)
            print(f"\nFound {len(matches)} potential November date matches")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()

if __name__ == "__main__":
    analyze_serikovka()
