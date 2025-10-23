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


class LucernaMusicBarBrowserScraper(BrowserScraper):
    """Scrapes Lucerna Music Bar using Playwright"""

    def __init__(self, month: int, year: int):
        super().__init__(
            venue_name="Lucerna Music Bar",
            url="https://musicbar.cz/en/program/",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """
        Main scraping method using Playwright

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Scraping {self.venue_name} for {self.month}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='a.program-item')

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')

        # Find all event links with class="program-item"
        event_links = soup.find_all('a', class_='program-item')

        events = []
        for link in event_links:
            href = link.get('href', '')
            if not href:
                continue

            # Get full text
            text = link.get_text(separator=' ', strip=True)

            # Look for date pattern "day/month" (e.g., "1/11", "23/10")
            date_match = re.search(r'(\d{1,2})/(\d{1,2})', text)
            if not date_match:
                continue

            day = int(date_match.group(1))
            month = int(date_match.group(2))

            # Filter by target month
            if month != self.month:
                continue

            # Build full URL
            if href.startswith('http'):
                url = href
            elif href.startswith('/'):
                url = f"https://musicbar.cz{href}"
            else:
                url = f"https://musicbar.cz/{href}"

            # Extract time
            time_match = re.search(r'(\d{1,2}):(\d{2})', text)
            time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else None

            # Extract artist - remove date/time info from text
            artist = text
            # Remove "Today/Tomorrow/Monday/etc"
            artist = re.sub(r'^(Today|Tomorrow|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*', '', artist)
            # Remove date pattern
            artist = re.sub(r'\d{1,2}/\d{1,2}', '', artist)
            # Remove time
            artist = re.sub(r'\d{1,2}:\d{2}', '', artist)
            # Remove status text at end
            artist = re.sub(r'(Buy tickets|Tickets at the door|Sold out|More info|Postponed).*$', '', artist, flags=re.I)
            # Clean whitespace
            artist = re.sub(r'\s+', ' ', artist).strip()

            if not artist or len(artist) < 2:
                continue

            # Extract status
            status = None
            if 'sold out' in text.lower() or 'vyprodáno' in text.lower():
                status = 'sold_out'
            elif 'postponed' in text.lower() or 'odloženo' in text.lower():
                status = 'postponed'

            date_str = f"{day:02d}.{month:02d}.{self.year}"

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


class RoxyBrowserScraper(BrowserScraper):
    """Scrapes Roxy using Playwright"""

    def __init__(self, month: int, year: int):
        super().__init__(
            venue_name="Roxy",
            url="https://www.roxy.cz/tickets/",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """
        Main scraping method using Playwright

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Scraping {self.venue_name} for {self.month}/{self.year}...")

        # Fetch HTML with browser - wait longer for dynamic content
        html = self.fetch_html_with_browser(wait_for_selector='a.item[href*="/events/detail/"]', timeout=60000)

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')

        # Find all event links with href containing "/events/detail/"
        event_links = soup.find_all('a', class_='item', href=re.compile(r'/events/detail/'))

        events = []
        for link in event_links:
            href = link.get('href', '')
            if not href:
                continue

            # Get full text
            text = link.get_text(separator=' ', strip=True)

            # Look for date pattern with day abbreviation: "So 01/11" or just "01/11"
            date_match = re.search(r'(\d{1,2})/(\d{1,2})', text)
            if not date_match:
                continue

            day = int(date_match.group(1))
            month = int(date_match.group(2))

            # Filter by target month
            if month != self.month:
                continue

            # Build full URL
            if href.startswith('http'):
                url = href
            elif href.startswith('/'):
                url = f"https://www.roxy.cz{href}"
            else:
                url = f"https://www.roxy.cz/{href}"

            # Extract artist - remove date/time info from text
            artist = text
            # Remove day abbreviations
            artist = re.sub(r'^(Po|Út|St|Čt|Pá|So|Ne|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+', '', artist, flags=re.I)
            # Remove date pattern
            artist = re.sub(r'\d{1,2}/\d{1,2}', '', artist)
            # Remove "VYPRODÁNO:" prefix
            artist = re.sub(r'^VYPRODÁNO:\s*', '', artist, flags=re.I)
            artist = re.sub(r'^SOLD OUT:\s*', '', artist, flags=re.I)
            # Clean whitespace
            artist = re.sub(r'\s+', ' ', artist).strip()

            if not artist or len(artist) < 2:
                continue

            # Extract time if available (less common on Roxy)
            time_match = re.search(r'(\d{1,2}):(\d{2})', text)
            time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else None

            # Extract status
            status = None
            if 'vyprodáno' in text.lower() or 'sold out' in text.lower():
                status = 'sold_out'

            date_str = f"{day:02d}.{month:02d}.{self.year}"

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


class VagonBrowserScraper(BrowserScraper):
    """Scrapes Vagon using Playwright"""

    def __init__(self, month: int, year: int):
        super().__init__(
            venue_name="Vagon",
            url="https://www.vagon.cz/next.php",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """
        Main scraping method using Playwright

        Returns:
            List of event dictionaries
        """
        self.logger.info(f"Scraping {self.venue_name} for {self.month}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='table.table')

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')

        # Find the program table
        table = soup.find('table', class_='table')
        if not table:
            self.logger.warning("Could not find program table")
            return []

        # Find all table rows
        rows = table.find_all('tr')

        events = []
        for row in rows:
            tds = row.find_all('td')
            if len(tds) < 4:
                continue

            # Structure: [price, day_name, day_number, program, note]
            day_text = tds[2].get_text(strip=True)

            # Skip if not a number
            try:
                day = int(day_text)
            except ValueError:
                continue

            # Get program column
            program_td = tds[3]
            program_text = program_td.get_text(separator=' ', strip=True)

            # Skip closed days
            if 'ZAVŘENO' in program_text or 'CLOSED' in program_text:
                continue

            # Skip if no content
            if not program_text or len(program_text) < 3:
                continue

            # Extract artist names from links
            links = program_td.find_all('a', href=True)
            artists = []
            for link in links:
                artist_name = link.get_text(strip=True)
                if artist_name and len(artist_name) > 1:
                    artists.append(artist_name)

            # If no links, use text content
            if not artists:
                # Clean the text
                artist = program_text
                # Remove time
                artist = re.sub(r'\d{1,2}:\d{2}', '', artist)
                # Remove common prefixes
                artist = re.sub(r'^(Koncert v rámci|Koncert|V rámci).*?:', '', artist, flags=re.I)
                artist = re.sub(r'\s+', ' ', artist).strip()
                if artist and len(artist) > 2:
                    artists = [artist]

            if not artists:
                continue

            # Join multiple artists
            artist = ' + '.join(artists)

            # Extract time
            time_match = re.search(r'(\d{1,2}):(\d{2})', program_text)
            time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else "21:00"  # Default from page

            # Build URL - use first link if available
            url = links[0].get('href') if links else f"https://www.vagon.cz/next.php#{day}"

            date_str = f"{day:02d}.{self.month:02d}.{self.year}"

            events.append({
                'date': date_str,
                'day': day,
                'month': self.month,
                'year': self.year,
                'time': time_str,
                'artist': artist,
                'venue': self.venue_name,
                'city': self.city,
                'url': url,
                'status': None
            })

        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events")
        return self.events


class JazzDockBrowserScraper(BrowserScraper):
    """
    Jazz Dock scraper using Playwright
    URL: https://www.jazzdock.cz/en/program/2025/11
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url=f"https://www.jazzdock.cz/en/program/{year}/{month:02d}",
            venue_name="Jazz Dock",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.program-item')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse Jazz Dock HTML and extract events"""

        soup = BeautifulSoup(html, 'lxml')

        # Find all program items
        program_items = soup.find_all('div', class_='program-item')
        self.logger.info(f"Found {len(program_items)} program items")

        events = []
        for item in program_items:
            try:
                # Find date text: "Sa 01. 11. from 15:00"
                date_elem = item.find(class_=re.compile('date', re.I))
                if not date_elem:
                    continue

                date_text = date_elem.get_text(strip=True)

                # Parse date: "Sa 01. 11. from 15:00"
                # Pattern: day_abbrev DD. MM. from HH:MM
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*from\s*(\d{1,2}):(\d{2})', date_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))
                hour = date_match.group(3)
                minute = date_match.group(4)

                # Skip if not our month
                if month != self.month:
                    continue

                time_str = f"{hour}:{minute}"

                # Find artist name - get full text and parse
                full_text = item.get_text(separator='|', strip=True)
                # Format: "Sa 01. 11. from 15:00|Artist Name|Genre|Description..."
                parts = full_text.split('|')

                artist = ""
                if len(parts) >= 2:
                    # Artist is usually the second part (after date)
                    artist = parts[1].strip()

                # Sometimes there's a subtitle or additional info
                # Skip "Jazz Dock to Kids" label and "Concerts package" labels
                if len(parts) >= 3 and not any(skip in parts[1] for skip in ['Jazz Dock to Kids', 'Concerts package']):
                    artist = parts[1].strip()
                elif len(parts) >= 3:
                    # If part[1] is a label, use part[2]
                    artist = parts[2].strip()

                if not artist:
                    # Fallback: try to find link text
                    link = item.find('a', href=re.compile(r'/koncert/'))
                    if link:
                        artist = link.get_text(strip=True)

                # Find URL
                link = item.find('a', href=re.compile(r'/koncert/'))
                url = ""
                if link:
                    url = link.get('href', '')
                    if url.startswith('/'):
                        url = f"https://www.jazzdock.cz{url}"

                if not artist:
                    continue

                # Create event
                event = {
                    'date': f"{day:02d}.{self.month:02d}.{self.year}",
                    'day': day,
                    'month': self.month,
                    'year': self.year,
                    'time': time_str,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url,
                    'status': None
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events")
        return self.events


class ForumKarlinBrowserScraper(BrowserScraper):
    """
    Forum Karlín scraper using Playwright
    URL: https://www.forumkarlin.cz/en/events/
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.forumkarlin.cz/en/events/",
            venue_name="Forum Karlín",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div[class*="event"]')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse Forum Karlín HTML and extract events"""

        soup = BeautifulSoup(html, 'lxml')

        # Find all event divs
        event_divs = soup.find_all('div', class_=re.compile('event', re.I))
        self.logger.info(f"Found {len(event_divs)} event divs")

        events = []
        seen_urls = set()  # To avoid duplicates

        for div in event_divs:
            try:
                # Get full text
                text = div.get_text(separator='|', strip=True)

                # Look for date pattern: "DD. MM. YYYY"
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))
                year_parsed = int(date_match.group(3))

                # Skip if not our month
                if month != self.month or year_parsed != self.year:
                    continue

                # Find event link
                link = div.find('a', href=re.compile(r'/event/'))
                if not link:
                    continue

                url = link.get('href', '')
                if url.startswith('/'):
                    url = f"https://www.forumkarlin.cz{url}"

                # Skip duplicates (same event appearing multiple times)
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # Extract artist from text
                # Format: "ARTIST|DD. MM. YYYY|day_abbrev|Additional info"
                parts = text.split('|')
                artist = parts[0].strip() if parts else ""

                if not artist:
                    # Fallback: get from link text
                    artist = link.get_text(strip=True)

                # Look for time (19:00, 20:00, etc.)
                time_match = re.search(r'(\d{1,2}):(\d{2})', text)
                time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else "20:00"

                # Check for status (SOLD OUT, etc.)
                status = None
                if 'SOLD OUT' in text.upper():
                    status = "SOLD OUT"

                # Create event
                event = {
                    'date': f"{day:02d}.{self.month:02d}.{self.year}",
                    'day': day,
                    'month': self.month,
                    'year': self.year,
                    'time': time_str,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url,
                    'status': status
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events")
        return self.events


class MeetFactoryBrowserScraper(BrowserScraper):
    """
    MeetFactory scraper using Playwright
    URL: https://meetfactory.cz/cs/program/hudba
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://meetfactory.cz/cs/program/hudba",
            venue_name="MeetFactory",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.ab-box')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse MeetFactory HTML and extract events"""

        soup = BeautifulSoup(html, 'lxml')

        # Find all event boxes
        event_boxes = soup.find_all('div', class_='ab-box')
        self.logger.info(f"Found {len(event_boxes)} event boxes")

        events = []

        for box in event_boxes:
            try:
                # Find date: <p class="abb-date"><b>1. 11.</b>...
                date_elem = box.find('p', class_='abb-date')
                if not date_elem:
                    continue

                date_b = date_elem.find('b')
                if not date_elem:
                    continue

                date_text = date_b.get_text(strip=True)

                # Parse date: "1. 11." or "11. 11."
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.', date_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))

                # Skip if not our month
                if month != self.month:
                    continue

                # Find time in span
                time_spans = date_elem.find_all('span')
                time_str = "20:00"  # default
                for span in time_spans:
                    text = span.get_text(strip=True)
                    if re.match(r'\d{1,2}\.\d{2}', text):
                        time_str = text.replace('.', ':')
                        break

                # Find artist: <h3><a><span itemprop="name">Artist Name</span></a></h3>
                h3 = box.find('h3')
                if not h3:
                    continue

                artist_span = h3.find('span', itemprop='name')
                artist = artist_span.get_text(strip=True) if artist_span else ""

                if not artist:
                    # Fallback: get from h3 > a
                    a_tag = h3.find('a')
                    if a_tag:
                        artist = a_tag.get_text(strip=True)

                # Find URL
                link = box.find('a', href=re.compile(r'/program/detail/'))
                url = ""
                if link:
                    url = link.get('href', '')
                    if url.startswith('/'):
                        url = f"https://meetfactory.cz{url}"

                if not artist:
                    continue

                # Create event
                event = {
                    'date': f"{day:02d}.{self.month:02d}.{self.year}",
                    'day': day,
                    'month': self.month,
                    'year': self.year,
                    'time': time_str,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url,
                    'status': None
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events")
        return self.events


def main():
    """Test browser scrapers"""
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
