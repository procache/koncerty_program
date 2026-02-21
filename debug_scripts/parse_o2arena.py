from bs4 import BeautifulSoup
import re

html = open('o2arena.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'lxml')

event_divs = soup.find_all('div', class_='event_preview')

print('=== November 2025 Events ===\n')

sports_keywords = ['HC Sparta', 'Bílí Tygři', 'hockey', 'FMX', 'Global Champions', 'Equestrian', 'football', 'basketball', 'volleyball']

for event_div in event_divs:
    time_p = event_div.find('p', class_='time')
    h3 = event_div.find('h3')

    if not time_p or not h3:
        continue

    time_text = time_p.text.strip()
    # Parse date DD.MM.YYYY HH:MM
    date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}:\d{2})', time_text)

    if not date_match:
        continue

    day = int(date_match.group(1))
    month = int(date_match.group(2))
    year = int(date_match.group(3))
    time_str = date_match.group(4)

    # Filter November 2025
    if month != 11 or year != 2025:
        continue

    link = h3.find('a')
    artist = link.text.strip() if link else 'N/A'
    url = link.get('href', '') if link else ''

    # Detect sports
    is_sport = any(keyword.lower() in artist.lower() for keyword in sports_keywords)
    event_type = 'SPORT' if is_sport else 'MUSIC'

    print(f'{event_type:6} | {day:02d}.{month:02d} {time_str} | {artist}')
