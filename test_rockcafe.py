"""Test Rock Café HTML structure"""
import requests
from bs4 import BeautifulSoup

url = 'https://rockcafe.cz/en/program/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# Find all event links (exclude archive links with year patterns)
links = soup.find_all('a', href=True)
event_links = []
for a in links:
    href = a.get('href', '')
    if '/en/program/' in href and href != '/en/program/':
        # Skip archive links like /en/program/2019/10
        if not any(f'/{year}/' in href for year in range(2010, 2026)):
            event_links.append(a)

print(f'Found {len(event_links)} event links\n')

# Filter for music events only
music_events = []
for link in event_links:
    category = link.find('span')
    if category and 'music' in category.get_text(strip=True).lower():
        music_events.append(link)

print(f'Music events: {len(music_events)}\n')

# Show first 5 music events
for i, link in enumerate(music_events[:5]):
    print(f"Event {i+1}:")
    print(f"  URL: {link.get('href')}")

    # Get category span
    category = link.find('span')
    if category:
        print(f"  Category: {category.get_text(strip=True)}")

    # Get title (h3)
    title = link.find('h3')
    if title:
        print(f"  Title: {title.get_text(strip=True)}")

    # Get date (p tag)
    date_p = link.find('p')
    if date_p:
        date_text = date_p.get_text(strip=True)
        print(f"  Date: {date_text}")

        # Try to parse date for November
        import re
        # Look for pattern like "Friday 24.10.2025" or "1.11.2025"
        date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_text)
        if date_match:
            day, month, year = date_match.groups()
            if month == '11':
                print(f"  -> NOVEMBER EVENT: {day}.{month}.{year}")

    print()
