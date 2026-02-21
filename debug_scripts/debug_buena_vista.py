"""
Debug script to analyze Buena Vista Club website structure
URL: https://www.buenavistaclub.cz/program-klubu.aspx
"""
from playwright.sync_api import sync_playwright
import re

def analyze_buena_vista():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.buenavistaclub.cz/program-klubu.aspx"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        html = page.content()

        # Save HTML for inspection
        with open("buena_vista.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\nHTML saved to buena_vista.html ({len(html)} bytes)")

        # Look for h4 elements (dates)
        h4_elements = page.query_selector_all("h4")
        print(f"\nFound {len(h4_elements)} h4 elements")

        # Print first few h4 texts
        for i, elem in enumerate(h4_elements[:10]):
            text = elem.text_content().strip()
            print(f"  h4[{i}]: {text}")

        # Look for November dates
        november_pattern = r'(\d{2})\.11\.2025'
        matches = re.findall(november_pattern, html)
        print(f"\nFound {len(matches)} November 2025 date matches: {matches}")

        browser.close()

if __name__ == "__main__":
    analyze_buena_vista()
