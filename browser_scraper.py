"""
Browser-Based Scraper
=====================
Uses Playwright for JavaScript-heavy sites (automatic browser automation).
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from base_scraper import BaseScraper


class BrowserScraper(BaseScraper):
    """
    Base class for scrapers that need browser automation

    Uses Playwright to handle JavaScript-rendered content
    """

    def __init__(self, venue_name: str, url: str, city: str, month: int, year: int):
        super().__init__(venue_name, url, city, month, year)
        self.headless = True  # Run browser in background

    def fetch_html_with_browser(self, url: Optional[str] = None, wait_for_selector: Optional[str] = None, timeout: int = 30000) -> str:
        """
        Fetch HTML using Playwright browser automation

        Args:
            url: URL to fetch (defaults to self.url)
            wait_for_selector: CSS selector to wait for before extracting HTML
            timeout: Timeout in milliseconds

        Returns:
            HTML content as string

        Raises:
            Exception: If browser automation fails
        """
        target_url = url or self.url

        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                self.logger.info(f"Opening browser for {target_url}")

                # Navigate to page
                page.goto(target_url, wait_until='networkidle', timeout=timeout)

                # Wait for specific selector if provided
                if wait_for_selector:
                    self.logger.info(f"Waiting for selector: {wait_for_selector}")
                    page.wait_for_selector(wait_for_selector, timeout=timeout)
                else:
                    # Default: wait a bit for JavaScript to load
                    page.wait_for_timeout(3000)

                # Get HTML
                html = page.content()

                browser.close()

                self.logger.info(f"Successfully fetched {len(html)} chars of HTML")
                return html

        except PlaywrightTimeout as e:
            self.logger.error(f"Timeout fetching {target_url}: {e}")
            raise Exception(f"Timeout fetching {target_url}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to fetch {target_url} with browser: {e}")
            raise Exception(f"Failed to fetch {target_url} with browser: {e}")

    def scrape(self) -> List[Dict]:
        """
        Main scraping method - must be implemented by subclass

        Returns:
            List of event dictionaries
        """
        raise NotImplementedError("Subclass must implement scrape() method")


class RockCafeBrowserScraper(BrowserScraper):
    """Scrapes Rock Café using Playwright"""

    def __init__(self, month: int, year: int):
        super().__init__(
            venue_name="Rock Café",
            url="https://rockcafe.cz/en/program/",
            city="Praha",
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

        # Get title (h2 or h3)
        title = link_tag.find('h2') or link_tag.find('h3')
        if not title:
            return None

        artist = title.get_text(strip=True)

        # Get date from <span class="date"> tag
        date_span = link_tag.find('span', class_='date')
        if not date_span:
            return None

        date_text = date_span.get_text(strip=True)

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
            'venue': self.venue_name,
            'city': self.city,
            'url': url,
            'status': None
        }

    def scrape(self) -> List[Dict]:
        """
        Main scraping method using Playwright

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Scraping {self.venue_name} for {self.month}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='a[href*="/en/program/"]')

        # Parse with Beautiful Soup
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
    """Test Rock Café browser scraper"""
    # November 2025
    scraper = RockCafeBrowserScraper(month=11, year=2025)

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
    scraper.save_json('rock_cafe_browser_events.json')

    # Show sample events
    print("\nSample Events (first 5):")
    for event in events[:5]:
        print(f"  {event['date']} {event['time'] or ''} - {event['artist'][:50]}")


if __name__ == '__main__':
    main()
