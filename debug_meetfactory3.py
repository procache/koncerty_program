"""Debug MeetFactory - detailed structure analysis"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://meetfactory.cz/cs/program/hudba", wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(3000)
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'lxml')

# Save HTML for inspection
with open('meetfactory_cs.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Get all divs
all_divs = soup.find_all('div')
print(f"Total divs: {len(all_divs)}")

# Check for any div with November date in text
nov_divs = []
for div in all_divs:
    text = div.get_text(strip=True)
    if re.search(r'\d{1,2}\.\s*11\.', text):
        classes = div.get('class', [])
        nov_divs.append({
            'classes': classes,
            'text': text[:100]
        })

print(f"\nDivs with November dates: {len(nov_divs)}")

if nov_divs:
    print("\nFirst 5:")
    for i, d in enumerate(nov_divs[:5]):
        print(f"\n{i+1}. Classes: {d['classes']}")
        with open(f'meetfactory_div_{i}.txt', 'w', encoding='utf-8') as f:
            f.write(d['text'])
        print(f"   Saved text to meetfactory_div_{i}.txt")

# Look for links
all_links = soup.find_all('a', href=True)
nov_links = [link for link in all_links if re.search(r'\d{1,2}\.\s*11\.', link.get_text(strip=True))]

print(f"\nLinks with November dates: {len(nov_links)}")
if nov_links:
    for i, link in enumerate(nov_links[:5]):
        print(f"{i+1}. {link.get('href')} - {link.get_text(strip=True)[:60]}")

print("\nSaved HTML to meetfactory_cs.html")
