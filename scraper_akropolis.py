"""
Palác Akropolis Proof of Concept Scraper
========================================
Tests scraping approach on historically problematic venue.
Must capture ALL events including Nov 27-28.

HTML Pattern (verified via WebFetch):
<a href="/work/33298?event_id=XXXXX&no=62&page_id=33824">
    24. 10    Artist Name
</a>
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import List, Dict, Optional


class AkropolisScraper:
    """Scrapes concert data from Palác Akropolis"""

    BASE_URL = "https://palacakropolis.cz"
    VENUE_NAME = "Palác Akropolis"
    CITY = "Praha"

    def __init__(self, month: int, year: int):
        """
        Args:
            month: Month number (1-12)
            year: Year (e.g., 2025)
        """
        self.month = month
        self.year = year
        self.events: List[Dict] = []

    def fetch_html(self) -> str:
        """Fetch HTML from venue website"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(self.BASE_URL, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch {self.BASE_URL}: {e}")

    def parse_event_from_td(self, td_tag) -> Optional[Dict]:
        """
        Parse event from table cell (TD element)

        The page structure has events in TD elements with date patterns
        and event_id links.

        Args:
            td_tag: BeautifulSoup <td> tag element

        Returns:
            Dict with event data or None if not a valid event
        """
        # Get text content
        text = td_tag.get_text(strip=True)

        # Look for date pattern "DD. MM" in November
        date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})', text)
        if not date_match:
            return None

        day = int(date_match.group(1))
        month = int(date_match.group(2))

        # Filter by target month
        if month != self.month:
            return None

        # Find event_id link
        link = td_tag.find('a', href=re.compile(r'event_id=\d+'))
        if not link:
            return None

        href = link.get('href', '')
        url = self.BASE_URL + href if href.startswith('/') else href

        # Extract artist name - it's the text after the date
        artist_text = text[date_match.end():].strip()

        # Clean up artist name (remove extra whitespace, arrows, etc.)
        artist_text = re.sub(r'\s+', ' ', artist_text)
        artist_text = artist_text.split('\n')[0]  # Take first line if multiline

        if not artist_text or len(artist_text) < 2:
            return None

        # Build date string
        date_str = f"{day:02d}.{month:02d}.{self.year}"

        return {
            'date': date_str,
            'day': day,
            'month': month,
            'year': self.year,
            'time': None,  # Not available in listing
            'artist': artist_text,
            'venue': self.VENUE_NAME,
            'city': self.CITY,
            'url': url,
            'status': None  # No status tags in listing
        }

    def scrape(self) -> List[Dict]:
        """
        Main scraping method

        Returns:
            List of event dictionaries
        """
        print(f"Scraping {self.VENUE_NAME} for {self.month}/{self.year}...")

        html = self.fetch_html()
        soup = BeautifulSoup(html, 'lxml')

        # Find all table cells - events are in <td> elements
        all_tds = soup.find_all('td')

        events = []
        for td in all_tds:
            event = self.parse_event_from_td(td)
            if event:
                events.append(event)

        # Remove duplicates (same URL)
        seen_urls = set()
        unique_events = []
        for event in events:
            if event['url'] not in seen_urls:
                seen_urls.add(event['url'])
                unique_events.append(event)

        self.events = sorted(unique_events, key=lambda x: x['day'])

        print(f"[OK] Found {len(self.events)} events")
        return self.events

    def validate(self) -> Dict:
        """
        Validate scraped data

        Returns:
            Dict with validation results
        """
        total = len(self.events)

        # Check for Nov 27-28 (historically problematic)
        has_27 = any(e['day'] == 27 for e in self.events)
        has_28 = any(e['day'] == 28 for e in self.events)

        # Count weekend events (assuming November 2025)
        # Nov 2025: Fri=7,14,21,28  Sat=1,8,15,22,29  Sun=2,9,16,23,30
        weekends = {1,2, 7,8,9, 14,15,16, 21,22,23, 28,29,30}
        weekend_events = [e for e in self.events if e['day'] in weekends]

        # Expected range from kluby.json: min_akci=15, max_akci=30
        is_green = total >= 15
        is_yellow = 7.5 <= total < 15  # 50% of min
        is_red = total < 7.5

        status = 'GREEN' if is_green else ('YELLOW' if is_yellow else 'RED')

        return {
            'venue': self.VENUE_NAME,
            'total_events': total,
            'weekend_events': len(weekend_events),
            'has_nov_27': has_27,
            'has_nov_28': has_28,
            'status': status,
            'expected_range': '15-30',
            'validation': 'PASS' if is_green and has_27 and has_28 else 'FAIL'
        }

    def save_json(self, filename: str = 'palac_akropolis_events.json'):
        """Save events to JSON file"""
        output = {
            'venue': self.VENUE_NAME,
            'city': self.CITY,
            'month': self.month,
            'year': self.year,
            'total_events': len(self.events),
            'events': self.events
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"[OK] Saved to {filename}")


def main():
    """Run proof of concept scraper"""
    # November 2025
    scraper = AkropolisScraper(month=11, year=2025)

    # Scrape
    events = scraper.scrape()

    # Validate
    validation = scraper.validate()

    print("\n" + "="*60)
    print("VALIDATION REPORT")
    print("="*60)
    print(f"Venue: {validation['venue']}")
    print(f"Total Events: {validation['total_events']} (expected: {validation['expected_range']})")
    print(f"Weekend Events: {validation['weekend_events']}")
    print(f"Has Nov 27: {'YES' if validation['has_nov_27'] else 'NO'}")
    print(f"Has Nov 28: {'YES' if validation['has_nov_28'] else 'NO'}")
    print(f"Status: {validation['status']}")
    print(f"Validation: {validation['validation']}")
    print("="*60)

    # Save
    scraper.save_json()

    # Show sample events
    print("\nSample Events (first 5):")
    for event in events[:5]:
        print(f"  {event['date']} - {event['artist']}")
        print(f"    {event['url']}")


if __name__ == '__main__':
    main()
