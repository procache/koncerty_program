"""
Base Scraper Class
==================
Common functionality for all venue scrapers.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseScraper:
    """Base class for all venue scrapers"""

    def __init__(self, venue_name: str, url: str, city: str, month: int, year: int):
        """
        Args:
            venue_name: Name of the venue
            url: Base URL of the venue website
            city: City where venue is located (Praha/Plzeň)
            month: Month number (1-12)
            year: Year (e.g., 2025)
        """
        self.venue_name = venue_name
        self.url = url
        self.city = city
        self.month = month
        self.year = year
        self.events: List[Dict] = []
        self.logger = logging.getLogger(f"scraper.{venue_name}")

    def fetch_html(self, url: Optional[str] = None, timeout: int = 10) -> str:
        """
        Fetch HTML from URL

        Args:
            url: URL to fetch (defaults to self.url)
            timeout: Request timeout in seconds

        Returns:
            HTML content as string

        Raises:
            Exception: If request fails
        """
        target_url = url or self.url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            self.logger.info(f"Fetching {target_url}")
            response = requests.get(target_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {target_url}: {e}")
            raise Exception(f"Failed to fetch {target_url}: {e}")

    def scrape(self) -> List[Dict]:
        """
        Main scraping method - must be implemented by subclass

        Returns:
            List of event dictionaries
        """
        raise NotImplementedError("Subclass must implement scrape() method")

    def validate(self, min_events: int = 0, max_events: int = 100) -> Dict:
        """
        Validate scraped data

        Args:
            min_events: Minimum expected events
            max_events: Maximum expected events

        Returns:
            Dict with validation results
        """
        total = len(self.events)

        # Check for Nov 27-28 (historically problematic)
        has_27 = any(e['day'] == 27 for e in self.events if e['month'] == 11)
        has_28 = any(e['day'] == 28 for e in self.events if e['month'] == 11)

        # Count weekend events
        # November 2025: Fri=7,14,21,28  Sat=1,8,15,22,29  Sun=2,9,16,23,30
        weekends = {1, 2, 7, 8, 9, 14, 15, 16, 21, 22, 23, 28, 29, 30}
        weekend_events = [e for e in self.events if e['day'] in weekends]

        # Determine status
        is_green = total >= min_events
        is_yellow = total >= min_events * 0.5 and total < min_events
        is_red = total < min_events * 0.5

        status = 'GREEN' if is_green else ('YELLOW' if is_yellow else 'RED')

        # Overall validation passes if green and (not November OR has Nov 27-28)
        validation_pass = is_green and (self.month != 11 or (has_27 and has_28))

        return {
            'venue': self.venue_name,
            'total_events': total,
            'weekend_events': len(weekend_events),
            'has_nov_27': has_27 if self.month == 11 else None,
            'has_nov_28': has_28 if self.month == 11 else None,
            'status': status,
            'expected_range': f'{min_events}-{max_events}',
            'validation': 'PASS' if validation_pass else 'FAIL'
        }

    def save_json(self, filename: str) -> None:
        """
        Save events to JSON file

        Args:
            filename: Output filename
        """
        import json

        output = {
            'venue': self.venue_name,
            'city': self.city,
            'month': self.month,
            'year': self.year,
            'total_events': len(self.events),
            'events': self.events
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Saved {len(self.events)} events to {filename}")
