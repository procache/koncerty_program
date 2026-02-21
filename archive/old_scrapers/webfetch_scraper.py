"""
WebFetch Scraper Wrapper
========================
Uses Claude Code's WebFetch for JavaScript-heavy sites.

This is a fallback for sites where Beautiful Soup cannot access
dynamically-loaded content.
"""

import re
from typing import List, Dict
from base_scraper import BaseScraper


class WebFetchScraper(BaseScraper):
    """
    Base class for scrapers that use WebFetch results

    Subclasses should implement parse_webfetch_results()
    """

    def __init__(self, venue_name: str, url: str, city: str, month: int, year: int, webfetch_data: str):
        """
        Args:
            venue_name: Name of the venue
            url: Base URL of the venue website
            city: City where venue is located
            month: Month number (1-12)
            year: Year (e.g., 2025)
            webfetch_data: Raw text output from Claude Code WebFetch
        """
        super().__init__(venue_name, url, city, month, year)
        self.webfetch_data = webfetch_data

    def parse_webfetch_results(self) -> List[Dict]:
        """
        Parse WebFetch results into event list

        Must be implemented by subclass

        Returns:
            List of event dictionaries
        """
        raise NotImplementedError("Subclass must implement parse_webfetch_results()")

    def scrape(self) -> List[Dict]:
        """
        Main scraping method using WebFetch data

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Parsing WebFetch data for {self.venue_name}")

        events = self.parse_webfetch_results()

        # Remove duplicates (same URL)
        seen_urls = set()
        unique_events = []
        for event in events:
            if event['url'] not in seen_urls:
                seen_urls.add(event['url'])
                unique_events.append(event)

        self.events = sorted(unique_events, key=lambda x: x['day'])

        self.logger.info(f"Parsed {len(self.events)} events")
        return self.events


class RockCafeWebFetchScraper(WebFetchScraper):
    """Parses Rock Café WebFetch results"""

    def __init__(self, month: int, year: int, webfetch_data: str):
        super().__init__(
            venue_name="Rock Café",
            url="https://rockcafe.cz/en/program/",
            city="Praha",
            month=month,
            year=year,
            webfetch_data=webfetch_data
        )

    def parse_webfetch_results(self) -> List[Dict]:
        """
        Parse Rock Café WebFetch output

        Expected format:
        1. **01.11.2025 | 20:00**
           Artist Name
           https://rockcafe.cz/...
        """
        events = []
        lines = self.webfetch_data.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for date pattern: **01.11.2025 | 20:00**
            date_match = re.search(r'\*\*(\d{1,2})\.(\d{1,2})\.(\d{4})\s*\|\s*(\d{1,2}):(\d{2})\*\*', line)

            if date_match:
                day = int(date_match.group(1))
                month = int(date_match.group(2))
                year_parsed = int(date_match.group(3))
                time_hour = date_match.group(4)
                time_min = date_match.group(5)

                # Verify it's our target month/year
                if month != self.month or year_parsed != self.year:
                    i += 1
                    continue

                # Next line should be artist name
                i += 1
                if i >= len(lines):
                    break

                artist_line = lines[i].strip()
                # Remove markdown formatting and status tags
                artist = re.sub(r'\[.*?\]', '', artist_line).strip()

                # Next line should be URL
                i += 1
                if i >= len(lines):
                    break

                url_line = lines[i].strip()
                url_match = re.search(r'https?://[^\s]+', url_line)
                url = url_match.group(0) if url_match else self.url

                # Check for status (CANCELED, MOVED, etc)
                status_match = re.search(r'\[(.*?)\]', artist_line)
                status = status_match.group(1) if status_match else None

                date_str = f"{day:02d}.{month:02d}.{self.year}"
                time_str = f"{time_hour}:{time_min}"

                events.append({
                    'date': date_str,
                    'day': day,
                    'month': month,
                    'year': self.year,
                    'time': time_str,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url,
                    'status': status
                })

            i += 1

        return events


# Store WebFetch results here (to be populated by scrape_concerts.py)
WEBFETCH_RESULTS = {}


def store_webfetch_result(venue_name: str, data: str):
    """Store WebFetch result for a venue"""
    WEBFETCH_RESULTS[venue_name] = data


def get_webfetch_scraper(venue_name: str, month: int, year: int):
    """
    Get appropriate WebFetch scraper for venue

    Args:
        venue_name: Name of the venue
        month: Month number
        year: Year

    Returns:
        WebFetchScraper instance or None if not available
    """
    if venue_name not in WEBFETCH_RESULTS:
        return None

    data = WEBFETCH_RESULTS[venue_name]

    if venue_name == "Rock Café":
        return RockCafeWebFetchScraper(month, year, data)

    # Add more venue parsers here

    return None
