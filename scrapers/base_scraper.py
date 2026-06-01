"""
Base Scraper Class
==================
Common functionality for all venue scrapers.
"""

import calendar
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging


class ScraperError(Exception):
    """Raised when scraping fails for a known reason (parsing, no data, etc.)"""
    pass


class NetworkError(ScraperError):
    """Raised when a network request fails (timeout, connection error, HTTP error)"""
    pass


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
        except requests.Timeout as e:
            raise NetworkError(f"Timeout fetching {target_url}") from e
        except requests.ConnectionError as e:
            raise NetworkError(f"Connection error fetching {target_url}") from e
        except requests.HTTPError as e:
            raise NetworkError(f"HTTP {e.response.status_code} fetching {target_url}") from e
        except requests.RequestException as e:
            raise NetworkError(f"Request failed for {target_url}") from e

    def fetch_html_with_retry(self, url: Optional[str] = None, timeout: int = 10, max_retries: int = 3, backoff: float = 2.0) -> str:
        """
        Fetch HTML with automatic retry on transient network errors.

        Retries on: timeout, connection error, HTTP 429/503.
        Does NOT retry on: HTTP 404, 400 (permanent failures).

        Args:
            url: URL to fetch (defaults to self.url)
            timeout: Request timeout in seconds
            max_retries: Maximum number of attempts
            backoff: Multiplier for exponential backoff (2s, 4s, 8s by default)
        """
        TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
        last_error: Exception = NetworkError("No attempts made")

        for attempt in range(1, max_retries + 1):
            try:
                return self.fetch_html(url=url, timeout=timeout)
            except NetworkError as e:
                last_error = e
                # Don't retry on permanent HTTP errors
                cause = e.__cause__
                if isinstance(cause, requests.HTTPError) and cause.response.status_code not in TRANSIENT_HTTP_CODES:
                    self.logger.error(f"Permanent error, not retrying: {e}")
                    raise
                if attempt < max_retries:
                    wait = backoff ** (attempt - 1)
                    self.logger.warning(f"Attempt {attempt}/{max_retries} failed ({e}), retrying in {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    self.logger.error(f"All {max_retries} attempts failed for {url or self.url}")

        raise last_error

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

        # Count weekend events — dynamically computed for correct month/year
        # calendar.monthcalendar returns weeks as lists [Mo,Tu,We,Th,Fr,Sa,Su], 0 = no day
        weekends = set()
        for week in calendar.monthcalendar(self.year, self.month):
            for idx in (4, 5, 6):  # Friday=4, Saturday=5, Sunday=6
                if week[idx] != 0:
                    weekends.add(week[idx])
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
