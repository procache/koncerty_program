"""
Rock Café Scraper
=================
Scrapes concert data from Rock Café Prague.
"""

from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from base_scraper import BaseScraper


class RockCafeScraper(BaseScraper):
    """Scrapes concert data from Rock Café"""

    BASE_URL = "https://rockcafe.cz/en/program/"
    VENUE_NAME = "Rock Café"
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

    def parse_event_from_link(self, link_tag) -> Optional[Dict]:
        """
        Parse event from event link element

        Args:
            link_tag: BeautifulSoup <a> tag element

        Returns:
            Dict with event data or None if not a valid event
        """
        # Get href
        href = link_tag.get('href', '')
        if not href or '/en/program/' not in href:
            return None

        # Skip archive links
        if any(f'/{year}/' in href for year in range(2010, 2027)):
            return None

        # Check for music category
        category_span = link_tag.find('span')
        if not category_span or 'music' not in category_span.get_text(strip=True).lower():
            return None

        # Get title
        title_h3 = link_tag.find('h3')
        if not title_h3:
            return None

        artist = title_h3.get_text(strip=True)

        # Get date from <p> tag
        date_p = link_tag.find('p')
        if not date_p:
            return None

        date_text = date_p.get_text(strip=True)

        # Parse date: "Friday 24.10.2025, 19:30" or "1.11.2025"
        date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_text)
        if not date_match:
            return None

        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year_parsed = int(date_match.group(3))

        # Filter by target month and year
        if month != self.month or year_parsed != self.year:
            return None

        # Extract time if available
        time_match = re.search(r'(\d{1,2}):(\d{2})', date_text)
        time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else None

        # Build full URL
        if href.startswith('http'):
            url = href
        else:
            url = f"https://rockcafe.cz{href}"

        # Build date string
        date_str = f"{day:02d}.{month:02d}.{self.year}"

        return {
            'date': date_str,
            'day': day,
            'month': month,
            'year': self.year,
            'time': time_str,
            'artist': artist,
            'venue': self.VENUE_NAME,
            'city': self.CITY,
            'url': url,
            'status': None
        }

    def scrape(self) -> List[Dict]:
        """
        Main scraping method

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Scraping {self.VENUE_NAME} for {self.month}/{self.year}...")

        html = self.fetch_html()
        soup = BeautifulSoup(html, 'lxml')

        # Find all event links
        all_links = soup.find_all('a', href=True)

        events = []
        for link in all_links:
            event = self.parse_event_from_link(link)
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
    """Run test scraper"""
    # November 2025
    scraper = RockCafeScraper(month=11, year=2025)

    # Scrape
    events = scraper.scrape()

    # Validate (min_akci=10, max_akci=25 from kluby.json)
    validation = scraper.validate(min_events=10, max_events=25)

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
    scraper.save_json('rock_cafe_events.json')

    # Show sample events
    print("\nSample Events (first 5):")
    for event in events[:5]:
        print(f"  {event['date']} {event['time'] or ''} - {event['artist'][:50]}")
        print(f"    {event['url']}")


if __name__ == '__main__':
    main()
