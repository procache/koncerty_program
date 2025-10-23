"""
Debug script 5 for Malostranská beseda
Look for ALL row divs that might contain events
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

url = "https://www.malostranska-beseda.cz/club/program?year=2025&month=11"

print(f"Fetching: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)

    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'lxml')

# Find ALL divs with class row
rows = soup.find_all('div', class_='row')
print(f"Found {len(rows)} row divs total")

# Filter for rows that contain November dates
november_rows = []
for row in rows:
    text = row.get_text()
    if re.search(r'\d{1,2}\.\s*11\.\s*2025', text):
        november_rows.append(row)

print(f"Found {len(november_rows)} rows with November 2025 dates")

# Extract event data from each November row
for i, row in enumerate(november_rows):
    print(f"\n=== Event {i+1} ===")

    text = row.get_text(separator=' ', strip=True)

    # Date
    date_match = re.search(r'(\d{1,2})\.\s*11\.\s*2025', text)
    if date_match:
        print(f"Date: {date_match.group(0)}")

    # Time
    time_match = re.search(r'(\d{1,2}):(\d{2})', text)
    if time_match:
        print(f"Time: {time_match.group(0)}")

    # Artist (usually in h1-h4)
    h_tags = row.find_all(['h1', 'h2', 'h3', 'h4'])
    if h_tags:
        print(f"Artist: {h_tags[0].get_text(strip=True)}")

    # URL
    links = row.find_all('a', href=True)
    event_links = [a for a in links if 'ticketstream.cz/akce/' in a.get('href', '')]
    if event_links:
        print(f"URL: {event_links[0].get('href')}")
    else:
        # Maybe link is in the row somewhere else
        all_hrefs = [a.get('href') for a in links if a.get('href')]
        if all_hrefs:
            print(f"Links found: {all_hrefs[:3]}")

print("\n=== Done ===")
