"""
Debug script 2 for U Staré Paní
Try with user agent
"""

from playwright.sync_api import sync_playwright
import requests

url = "https://www.ustarepani.cz/program/"

# First try with requests
print("Trying with requests library...")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
except Exception as e:
    print(f"Requests failed: {e}")

# Try with Playwright with user agent
print("\nTrying with Playwright + user agent...")
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        page.goto(url, timeout=30000)
        page.wait_for_timeout(3000)

        html = page.content()
        print(f"Got {len(html)} chars of HTML")

        # Save
        with open('ustarepani.html', 'w', encoding='utf-8') as f:
            f.write(html)

        browser.close()
        print("Success!")
except Exception as e:
    print(f"Playwright failed: {e}")
