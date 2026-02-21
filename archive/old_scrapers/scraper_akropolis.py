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

from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Optional
from base_scraper import BaseScraper


class AkropolisScraper(BaseScraper):
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
        super().__init__(
            venue_name=self.VENUE_NAME,
            url=self.BASE_URL,
            city=self.CITY,
            month=month,
            year=year
        )

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

        self.logger.info(f"Found {len(self.events)} events")
        return self.events


def main():
    """Run proof of concept scraper"""
    # November 2025
    scraper = AkropolisScraper(month=11, year=2025)

    # Scrape
    events = scraper.scrape()

    # Validate (min_akci=15, max_akci=30 from kluby.json)
    validation = scraper.validate(min_events=15, max_events=30)

    print("\n" + "="*60)
    print("VALIDATION REPORT")
    print("="*60)
    print(f"Venue: {validation['venue']}")
    print(f"Total Events: {validation['total_events']} (expected: {validation['expected_range']})")
    print(f"Weekend Events: {validation['weekend_events']}")
    if validation['has_nov_27'] is not None:
        print(f"Has Nov 27: {'YES' if validation['has_nov_27'] else 'NO'}")
        print(f"Has Nov 28: {'YES' if validation['has_nov_28'] else 'NO'}")
    print(f"Status: {validation['status']}")
    print(f"Validation: {validation['validation']}")
    print("="*60)

    # Save
    scraper.save_json('palac_akropolis_events.json')

    # Show sample events
    print("\nSample Events (first 5):")
    for event in events[:5]:
        print(f"  {event['date']} - {event['artist'][:50]}")
        print(f"    {event['url']}")


if __name__ == '__main__':
    main()
