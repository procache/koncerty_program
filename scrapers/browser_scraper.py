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
        """Main scraping method using Playwright with infinite scroll"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser (custom method with scrolling)
        html = self.fetch_with_infinite_scroll()

        # Parse HTML
        return self.parse_html(html)

    def fetch_with_infinite_scroll(self) -> str:
        """
        Fetch HTML with infinite scroll support
        Scrolls down page to load all lazy-loaded events
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                self.logger.info(f"Opening browser for {self.url}")
                page.goto(self.url, wait_until='networkidle', timeout=30000)

                # Wait for initial content
                self.logger.info("Waiting for initial event boxes")
                page.wait_for_selector('div.ab-box', timeout=10000)

                # Scroll down multiple times to trigger lazy loading
                previous_height = 0
                scroll_attempts = 0
                max_scrolls = 10  # Safety limit

                self.logger.info("Starting infinite scroll...")
                while scroll_attempts < max_scrolls:
                    # Get current scroll height
                    current_height = page.evaluate("document.body.scrollHeight")

                    # If height hasn't changed, we've reached the bottom
                    if current_height == previous_height:
                        self.logger.info(f"Reached bottom after {scroll_attempts} scrolls")
                        break

                    # Scroll to bottom
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                    # Wait for new content to load
                    page.wait_for_timeout(1500)  # 1.5 seconds between scrolls

                    previous_height = current_height
                    scroll_attempts += 1

                    # Count current event boxes
                    event_count = page.evaluate("document.querySelectorAll('div.ab-box').length")
                    self.logger.info(f"Scroll {scroll_attempts}: Found {event_count} event boxes")

                # Get final HTML
                html = page.content()
                browser.close()

                self.logger.info(f"Successfully fetched {len(html)} chars of HTML after scrolling")
                return html

        except Exception as e:
            self.logger.error(f"Failed to fetch with infinite scroll: {e}")
            raise Exception(f"Failed to fetch with infinite scroll: {e}")

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


class MalostranaskaBesedaBrowserScraper(BrowserScraper):
    """
    Malostranská beseda scraper using Playwright
    URL: https://www.malostranska-beseda.cz/club/program?year=YYYY&month=MM
    """

    def __init__(self, month: int, year: int):
        # Use URL with month/year parameters
        url = f"https://www.malostranska-beseda.cz/club/program?year={year}&month={month}"
        super().__init__(
            url=url,
            venue_name="Malostranská beseda",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.row')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse Malostranská beseda HTML and extract events"""

        soup = BeautifulSoup(html, 'lxml')

        # Find ALL divs with class row
        rows = soup.find_all('div', class_='row')
        self.logger.info(f"Found {len(rows)} row divs")

        events = []
        seen_urls = set()

        for row in rows:
            try:
                text = row.get_text()

                # Look for date in this row
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))
                year = int(date_match.group(3))

                # Skip if not our month/year
                if month != self.month or year != self.year:
                    continue

                # Find time
                time_match = re.search(r'(\d{1,2}):(\d{2})', text)
                time_str = time_match.group(0) if time_match else "20:00"

                # Find artist (from h1-h4 tags)
                h_tags = row.find_all(['h1', 'h2', 'h3', 'h4'])
                artist = h_tags[0].get_text(strip=True) if h_tags else ""

                if not artist:
                    continue  # Skip if no artist

                # Find URL - prefer ticketstream, then goout, then any href
                links = row.find_all('a', href=True)
                url = ""
                for link in links:
                    href = link.get('href', '')
                    if 'ticketstream.cz/akce/' in href or 'goout.net' in href:
                        url = href if href.startswith('http') else f"https://www.malostranska-beseda.cz{href}"
                        break

                # Skip if we've seen this URL before (deduplication)
                if url and url in seen_urls:
                    continue

                if url:
                    seen_urls.add(url)

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


class RedutaJazzClubBrowserScraper(BrowserScraper):
    """
    Reduta Jazz Club scraper using Playwright
    URL: https://www.redutajazzclub.cz/program-cs/MMYYYY
    """

    def __init__(self, month: int, year: int):
        # Use URL with month/year in format MMYYYY
        url = f"https://www.redutajazzclub.cz/program-cs/{month:02d}{year}"
        super().__init__(
            url=url,
            venue_name="Reduta Jazz Club",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='td[data-link]')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse Reduta Jazz Club HTML and extract events from calendar"""
        import json as json_module

        soup = BeautifulSoup(html, 'lxml')

        # Find all td elements with our month/year in ID
        pattern = re.compile(rf'{self.year}-{self.month:02d}-\d{{2}}')
        event_tds = soup.find_all('td', id=pattern)
        self.logger.info(f"Found {len(event_tds)} event cells")

        events = []

        for td in event_tds:
            try:
                # Extract date from ID
                td_id = td.get('id', '')
                date_match = re.search(rf'{self.year}-{self.month:02d}-(\d{{2}})', td_id)
                if not date_match:
                    continue

                day = int(date_match.group(1))

                # Get data-label JSON
                data_label = td.get('data-label', '')
                if not data_label:
                    continue

                # Parse JSON
                event_data = json_module.loads(data_label)

                # Extract time and artist from body HTML
                body_html = event_data.get('body', '')
                body_soup = BeautifulSoup(body_html, 'lxml')

                # Time from span.tt-time
                time_span = body_soup.find('span', class_='tt-time')
                time_str = time_span.get_text(strip=True) if time_span else "19:00"

                # Artist from span.tt-text
                text_span = body_soup.find('span', class_='tt-text')
                artist = text_span.get_text(strip=True) if text_span else ""

                if not artist:
                    continue

                # URL from data-link
                url = td.get('data-link', '')

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


class WattMusicClubBrowserScraper(BrowserScraper):
    """
    Watt Music Club scraper using Playwright (GoOut source)
    URL: https://goout.net/en/watt-music-club/vztpab/events/
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://goout.net/en/watt-music-club/vztpab/events/",
            venue_name="Watt Music Club",
            city="Plzeň",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.event')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse GoOut events page and extract events"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event divs
        event_divs = soup.find_all('div', class_='event')
        self.logger.info(f"Found {len(event_divs)} event divs on page")

        events = []

        for event_div in event_divs:
            try:
                # Extract title
                title_link = event_div.find('a', class_='title')
                if not title_link:
                    continue

                artist = title_link.text.strip()
                relative_url = title_link.get('href', '')
                url = f"https://goout.net{relative_url}" if relative_url.startswith('/') else relative_url

                # Extract time element
                time_elem = event_div.find('time')
                if not time_elem:
                    continue

                # Parse date/time from text like "Sat, 01/11, 21:00"
                time_text = time_elem.text.strip()

                # Extract day and month from "01/11"
                date_match = re.search(r'(\d{2})/(\d{2})', time_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))

                # Only include events for the requested month
                if month_num != self.month:
                    self.logger.debug(f"Skipping event from month {month_num} (looking for {self.month})")
                    continue

                # Extract time (21:00)
                time_match = re.search(r'(\d{2}:\d{2})', time_text)
                time_str = time_match.group(1) if time_match else None

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
                    # Legacy fields for backwards compatibility
                    'den': day,
                    'den_tydne': None,
                    'cas': time_str,
                    'umelec': artist,
                    'misto': self.venue_name,
                    'status': None
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class O2ArenaBrowserScraper(BrowserScraper):
    """
    O2 Arena scraper using Playwright
    URL: https://www.o2arena.cz/en/events/
    Filters out sports events (hockey, FMX, etc.), keeps only music concerts
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.o2arena.cz/en/events/",
            venue_name="O2 Arena",
            city="Praha",
            month=month,
            year=year
        )
        # Sports keywords to filter out
        self.sports_keywords = [
            'HC Sparta', 'Bílí Tygři', 'hockey', 'FMX', 'Global Champions',
            'Equestrian', 'football', 'basketball', 'volleyball', 'Sparta Praha',
            'Tipsport', 'extraliga', 'playoffs', 'Liberec', 'Litvínov',
            'Mladá Boleslav', 'hokey', 'hokej'
        ]

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.event_preview')

        # Parse HTML
        return self.parse_html(html)

    def is_sports_event(self, event_name: str) -> bool:
        """Check if event is a sports event based on keywords"""
        event_lower = event_name.lower()
        return any(keyword.lower() in event_lower for keyword in self.sports_keywords)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse O2 Arena events page and extract music concerts only"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event preview divs
        event_divs = soup.find_all('div', class_='event_preview')
        self.logger.info(f"Found {len(event_divs)} event divs on page")

        events = []
        sports_filtered = 0

        for event_div in event_divs:
            try:
                # Extract time
                time_p = event_div.find('p', class_='time')
                if not time_p:
                    continue

                time_text = time_p.text.strip()

                # Parse date DD.MM.YYYY HH:MM
                date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}:\d{2})', time_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))
                year_num = int(date_match.group(3))
                time_str = date_match.group(4)

                # Only include events for the requested month and year
                if month_num != self.month or year_num != self.year:
                    continue

                # Extract event name and URL
                h3 = event_div.find('h3')
                if not h3:
                    continue

                link = h3.find('a')
                if not link:
                    continue

                artist = link.text.strip()
                url = link.get('href', '')

                # Filter out sports events
                if self.is_sports_event(artist):
                    self.logger.debug(f"Filtering out sports event: {artist}")
                    sports_filtered += 1
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
                    'url': url if url.startswith('http') else f"https://www.o2arena.cz{url}",
                    # Legacy fields for backwards compatibility
                    'den': day,
                    'den_tydne': None,
                    'cas': time_str,
                    'umelec': artist,
                    'misto': self.venue_name,
                    'status': None
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} music events for {self.month:02d}/{self.year} (filtered out {sports_filtered} sports events)")
        return self.events


class O2UniversumBrowserScraper(BrowserScraper):
    """
    O2 Universum scraper using Playwright
    URL: https://www.o2universum.cz/en/events/
    No sports filtering needed (music venue only)
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.o2universum.cz/en/events/",
            venue_name="O2 Universum",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='div.event_preview')

        # Parse HTML
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse O2 Universum events page"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event preview divs
        event_divs = soup.find_all('div', class_='event_preview')
        self.logger.info(f"Found {len(event_divs)} event divs on page")

        events = []

        for event_div in event_divs:
            try:
                # Extract time
                time_p = event_div.find('p', class_='time')
                if not time_p:
                    continue

                time_text = time_p.text.strip()

                # Parse date DD.MM.YYYY HH:MM
                date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}:\d{2})', time_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))
                year_num = int(date_match.group(3))
                time_str = date_match.group(4)

                # Only include events for the requested month and year
                if month_num != self.month or year_num != self.year:
                    continue

                # Extract event name and URL
                h3 = event_div.find('h3')
                if not h3:
                    continue

                link = h3.find('a')
                if not link:
                    continue

                artist = link.text.strip()
                url = link.get('href', '')

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
                    'url': url if url.startswith('http') else f"https://www.o2universum.cz{url}",
                    # Legacy fields for backwards compatibility
                    'den': day,
                    'den_tydne': None,
                    'cas': time_str,
                    'umelec': artist,
                    'misto': self.venue_name,
                    'status': None
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class DivadloPodLampouBrowserScraper(BrowserScraper):
    """
    Divadlo Pod lampou scraper using Playwright
    URL: https://podlampou.cz/events/
    Note: Primarily theatre venue, filters music events only
    """
    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://podlampou.cz/events/",
            venue_name="Divadlo Pod lampou",
            city="Plzeň",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser
        html = self.fetch_html_with_browser(wait_for_selector='a.list-item')

        # Parse HTML
        return self.parse_events(html)

    def parse_events(self, html: str) -> list:
        """
        Parse events from Divadlo Pod lampou HTML
        Structure: <a class="list-item"> with <span class="date">
        """
        from bs4 import BeautifulSoup
        import re
        from datetime import datetime

        soup = BeautifulSoup(html, 'lxml')
        events = []

        # Find all event items
        event_items = soup.find_all('a', class_='list-item')
        self.logger.info(f"Found {len(event_items)} total event items")

        for item in event_items:
            try:
                # Get date span
                date_span = item.find('span', class_='date')
                if not date_span:
                    continue

                date_text = date_span.get_text(strip=True)
                # Example: "So 1. 11. 20:00" (day_name day. month. time)

                # Parse date using regex
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{1,2}:\d{2})', date_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))
                time = date_match.group(3)

                # Filter for our target month
                if month != self.month:
                    continue

                # Get artist name
                h2 = item.find('h2')
                if not h2:
                    continue

                artist = h2.get_text(strip=True)

                # Get URL
                url = item.get('href', '')
                if not url.startswith('http'):
                    url = f"https://podlampou.cz{url}"

                # Filter for music events (exclude theatre, readings, workshops)
                # Look for music-related keywords or lack of theatre keywords
                artist_lower = artist.lower()
                theatre_keywords = ['divadlo', 'theatre', 'workshop', 'seminář', 'čtení', 'beseda', 'vernisáž']

                # Skip if it's clearly theatre/non-music
                if any(kw in artist_lower for kw in theatre_keywords):
                    self.logger.debug(f"Skipping theatre event: {artist}")
                    continue

                # Add event
                event = {
                    'date': f"{day:02d}.{month:02d}.{self.year}",
                    'day': day,
                    'month': month,
                    'year': self.year,
                    'time': time,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url
                }
                events.append(event)
                self.logger.debug(f"Added event: {artist} on {day}.{month}. at {time}")

            except Exception as e:
                self.logger.error(f"Error parsing event item: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} music events for {self.month:02d}/{self.year}")
        return self.events


class KDSerikovkaBrowserScraper(BrowserScraper):
    """
    Kulturní dům Šeříkovka scraper using Playwright
    URL: https://www.serikovka.cz/
    Note: Uses domcontentloaded wait strategy (faster than networkidle)
    """
    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.serikovka.cz/",
            venue_name="Kulturní dům Šeříkovka",
            city="Plzeň",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright with custom wait strategy"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")

        # Fetch HTML with browser (use domcontentloaded instead of networkidle)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                self.logger.info(f"Opening browser for {self.url}")
                page.goto(self.url, wait_until="domcontentloaded", timeout=60000)

                # Wait a bit more for content
                page.wait_for_timeout(5000)

                html = page.content()
                browser.close()

                self.logger.info(f"Successfully fetched {len(html)} chars of HTML")

                # Parse HTML
                return self.parse_events(html)

        except Exception as e:
            self.logger.error(f"Failed to fetch {self.url}: {e}")
            raise

    def parse_events(self, html: str) -> list:
        """
        Parse events from KD Šeříkovka HTML
        Structure: <article class="mod-articles-item"> with <a class="mod-articles-link">
        """
        from bs4 import BeautifulSoup
        import re

        soup = BeautifulSoup(html, 'lxml')
        events = []

        # Find all article items
        articles = soup.find_all('article', class_='mod-articles-item')
        self.logger.info(f"Found {len(articles)} total article items")

        for article in articles:
            try:
                # Get title link
                link = article.find('a', class_='mod-articles-link')
                if not link:
                    continue

                link_text = link.get_text(strip=True)
                # Example: "03.11. 2025 / BONFIRE (DE) + WHITE TYGËR (UK)"

                # Parse date using regex
                date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.\s*(\d{4})', link_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month = int(date_match.group(2))
                year = int(date_match.group(3))

                # Filter for our target month/year
                if month != self.month or year != self.year:
                    continue

                # Extract artist name (everything after " / ")
                if " / " in link_text:
                    artist = link_text.split(" / ", 1)[1].strip()
                else:
                    artist = link_text.strip()

                # Get URL
                url = link.get('href', '')
                if url and not url.startswith('http'):
                    url = f"https://www.serikovka.cz{url}"

                # Default time (no specific time shown on website)
                time = "20:00"

                # Filter out non-music events
                artist_lower = artist.lower()
                non_music_keywords = [
                    'pawlowská', 'manuál', 'show', 'bambuláček',
                    'divadlo', 'theatre', 'čtení', 'beseda'
                ]

                # Skip if it's clearly not music
                if any(kw in artist_lower for kw in non_music_keywords):
                    self.logger.debug(f"Skipping non-music event: {artist}")
                    continue

                # Add event
                event = {
                    'date': f"{day:02d}.{month:02d}.{year}",
                    'day': day,
                    'month': month,
                    'year': year,
                    'time': time,
                    'artist': artist,
                    'venue': self.venue_name,
                    'city': self.city,
                    'url': url
                }
                events.append(event)
                self.logger.debug(f"Added event: {artist} on {day}.{month}. at {time}")

            except Exception as e:
                self.logger.error(f"Error parsing article item: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} music events for {self.month:02d}/{self.year}")
        return self.events


class PapirnaPlzenBrowserScraper(BrowserScraper):
    """
    Papírna Plzeň scraper using Playwright (GoOut source)
    URL: https://goout.net/en/papirna/vzkoab/events/
    Note: Official website unavailable, using GoOut.net as data source
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://goout.net/en/papirna/vzkoab/events/",
            venue_name="Papírna Plzeň",
            city="Plzeň",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")
        html = self.fetch_html_with_browser(wait_for_selector='div.event')
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse GoOut events page and extract events"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event divs
        event_divs = soup.find_all('div', class_='event')
        self.logger.info(f"Found {len(event_divs)} event divs on page")

        events = []

        for event_div in event_divs:
            try:
                # Extract title
                title_link = event_div.find('a', class_='title')
                if not title_link:
                    continue

                artist = title_link.text.strip()
                relative_url = title_link.get('href', '')
                url = f"https://goout.net{relative_url}" if relative_url.startswith('/') else relative_url

                # Extract time element
                time_elem = event_div.find('time')
                if not time_elem:
                    continue

                # Parse date/time from text like "Sat, 01/11, 21:00"
                time_text = time_elem.text.strip()

                # Extract day and month from "01/11"
                date_match = re.search(r'(\d{2})/(\d{2})', time_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))

                # Only include events for the requested month
                if month_num != self.month:
                    self.logger.debug(f"Skipping event from month {month_num} (looking for {self.month})")
                    continue

                # Extract time (21:00)
                time_match = re.search(r'(\d{2}:\d{2})', time_text)
                time_str = time_match.group(1) if time_match else "20:00"

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
                    'url': url
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class BuenaVistaClubBrowserScraper(BrowserScraper):
    """
    Buena Vista Club scraper using Playwright
    URL: https://www.buenavistaclub.cz/program-klubu.aspx
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.buenavistaclub.cz/program-klubu.aspx",
            venue_name="Buena Vista Club",
            city="Plzeň",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")
        html = self.fetch_html_with_browser()
        return self.parse_events(html)

    def parse_events(self, html: str) -> list:
        """Parse events from Buena Vista Club page"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all h2.nadpis elements (artist names)
        # Each event follows pattern: h2 (artist) → h4 (date) → p (description)
        h2_elements = soup.find_all('h2', class_='nadpis')
        self.logger.info(f"Found {len(h2_elements)} h2.nadpis elements (event headers)")

        events = []

        for h2 in h2_elements:
            try:
                # Extract artist name from h2
                artist_link = h2.find('a')
                if not artist_link:
                    continue

                artist = artist_link.text.strip()

                # Find next h4.podnadpis (date)
                h4 = h2.find_next_sibling('h4', class_='podnadpis')
                if not h4:
                    continue

                date_text = h4.text.strip()

                # Parse date format: DD.MM.YYYY
                date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))
                year_num = int(date_match.group(3))

                # Only include events for the requested month and year
                if month_num != self.month or year_num != self.year:
                    self.logger.debug(f"Skipping event from {day:02d}.{month_num:02d}.{year_num} (looking for {self.month:02d}/{self.year})")
                    continue

                # Time is usually not specified, default to 20:00
                time_str = "20:00"

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
                    'url': self.url
                }

                events.append(event)
                self.logger.debug(f"Added event: {day:02d}.{month_num:02d} - {artist}")

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class UStarePaniJazzClubBrowserScraper(BrowserScraper):
    """
    U Staré Paní Jazz & Cocktail Club scraper using Playwright (GoOut source)
    URL: https://goout.net/en/u-stare-pani-jazz-and-cocktail-club/vzlll/events/
    Note: Official website unavailable, using GoOut.net as data source
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://goout.net/en/u-stare-pani-jazz-and-cocktail-club/vzlll/events/",
            venue_name="U Staré Paní Jazz & Cocktail Club",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")
        html = self.fetch_html_with_browser(wait_for_selector='div.event')
        return self.parse_html(html)

    def parse_html(self, html: str) -> List[Dict]:
        """Parse GoOut events page and extract events"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event divs
        event_divs = soup.find_all('div', class_='event')
        self.logger.info(f"Found {len(event_divs)} event divs on page")

        events = []

        for event_div in event_divs:
            try:
                # Extract title
                title_link = event_div.find('a', class_='title')
                if not title_link:
                    continue

                artist = title_link.text.strip()
                relative_url = title_link.get('href', '')
                url = f"https://goout.net{relative_url}" if relative_url.startswith('/') else relative_url

                # Extract time element
                time_elem = event_div.find('time')
                if not time_elem:
                    continue

                # Parse date/time from text like "Sat, 01/11, 21:00"
                time_text = time_elem.text.strip()

                # Extract day and month from "01/11"
                date_match = re.search(r'(\d{2})/(\d{2})', time_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))

                # Only include events for the requested month
                if month_num != self.month:
                    self.logger.debug(f"Skipping event from month {month_num} (looking for {self.month})")
                    continue

                # Extract time (21:00)
                time_match = re.search(r'(\d{2}:\d{2})', time_text)
                time_str = time_match.group(1) if time_match else "20:00"

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
                    'url': url
                }

                events.append(event)

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class CrossClubBrowserScraper(BrowserScraper):
    """
    Cross Club scraper using Playwright
    URL: https://www.crossclub.cz/cs/program/
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.crossclub.cz/cs/program/",
            venue_name="Cross Club",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")
        html = self.fetch_html_with_browser()
        return self.parse_events(html)

    def parse_events(self, html: str) -> list:
        """Parse events from Cross Club page"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all div.predel elements (date separators)
        # Structure: <div class="predel"><div>01. 11. 2025 - Sobota</div></div>
        # Followed by: <h2><a href="...">EVENT NAME</a></h2>

        predel_divs = soup.find_all('div', class_='predel')
        self.logger.info(f"Found {len(predel_divs)} date separator divs")

        events = []

        for predel in predel_divs:
            try:
                # Extract date from inner div
                inner_div = predel.find('div')
                if not inner_div:
                    continue

                date_text = inner_div.text.strip()
                # Example: "01. 11. 2025 - Sobota"

                # Parse date using regex: DD. MM. YYYY
                date_match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', date_text)
                if not date_match:
                    continue

                day = int(date_match.group(1))
                month_num = int(date_match.group(2))
                year_num = int(date_match.group(3))

                # Only include events for the requested month/year
                if month_num != self.month or year_num != self.year:
                    self.logger.debug(f"Skipping event from {day:02d}.{month_num:02d}.{year_num} (looking for {self.month:02d}/{self.year})")
                    continue

                # Find the next h2 element (event name)
                # Structure: div.predel → div.article → h2
                # So we use find_next instead of find_next_sibling
                h2 = predel.find_next('h2')
                if not h2:
                    continue

                # Extract artist name from h2 > a
                artist_link = h2.find('a')
                if not artist_link:
                    continue

                artist = artist_link.text.strip()
                relative_url = artist_link.get('href', '')
                url = f"https://www.crossclub.cz{relative_url}" if relative_url.startswith('/') else relative_url

                # Time is usually not specified on Cross Club, default to 20:00
                time_str = "20:00"

                # Filter out non-music events (theatre, film, etc.)
                artist_lower = artist.lower()
                non_music_keywords = ['divadlo', 'theatre', 'film', 'movie', 'přednáška', 'lecture']

                if any(kw in artist_lower for kw in non_music_keywords):
                    self.logger.debug(f"Skipping non-music event: {artist}")
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
                    'url': url
                }

                events.append(event)
                self.logger.debug(f"Added event: {day:02d}.{month_num:02d} - {artist}")

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


class TipsportArenaBrowserScraper(BrowserScraper):
    """
    Tipsport Arena (Sportovní hala Fortuna) scraper using Playwright
    URL: https://www.ticketportal.cz/venue/TIPSPORT-ARENA
    Data source: Ticketportal (official tickets website)
    """

    def __init__(self, month: int, year: int):
        super().__init__(
            url="https://www.ticketportal.cz/venue/TIPSPORT-ARENA",
            venue_name="Sportovní hala Fortuna (Tipsport Arena)",
            city="Praha",
            month=month,
            year=year
        )

    def scrape(self) -> List[Dict]:
        """Main scraping method using Playwright"""
        self.logger.info(f"Scraping {self.venue_name} for {self.month:02d}/{self.year}...")
        html = self.fetch_html_with_browser()
        return self.parse_events(html)

    def parse_events(self, html: str) -> list:
        """Parse events from Ticketportal page"""
        soup = BeautifulSoup(html, 'lxml')

        # Find all event date elements
        # Structure: div[itemprop="startDate"][content="2025-11-07T18:30"]
        date_divs = soup.find_all('div', attrs={'itemprop': 'startDate'})
        self.logger.info(f"Found {len(date_divs)} date elements on page")

        events = []

        for date_div in date_divs:
            try:
                # Extract ISO date from content attribute
                # Example: "2025-11-07T18:30"
                iso_date = date_div.get('content', '')
                if not iso_date:
                    continue

                # Parse ISO date: YYYY-MM-DDTHH:MM
                date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})', iso_date)
                if not date_match:
                    continue

                year_num = int(date_match.group(1))
                month_num = int(date_match.group(2))
                day = int(date_match.group(3))
                hour = date_match.group(4)
                minute = date_match.group(5)

                # Only include events for the requested month/year
                if month_num != self.month or year_num != self.year:
                    self.logger.debug(f"Skipping event from {day:02d}.{month_num:02d}.{year_num} (looking for {self.month:02d}/{self.year})")
                    continue

                time_str = f"{hour}:{minute}"

                # Find the event name
                # Navigate up to find the container, then find the a.event element
                container = date_div.find_parent('div', class_='ticket-cover')
                if not container:
                    continue

                event_link = container.find('a', class_='event')
                if not event_link:
                    continue

                artist = event_link.text.strip()
                relative_url = event_link.get('href', '')
                url = f"https://www.ticketportal.cz{relative_url}" if relative_url.startswith('/') else relative_url

                # Filter out sports events (hockey, football, etc.)
                artist_lower = artist.lower()
                sports_keywords = [
                    'hokej', 'hockey', 'sparta', 'slavia', 'fotbal', 'football',
                    'extraliga', 'liiga', 'nhl', 'play-off', 'playoff',
                    'házená', 'handball', 'basket', 'volejbal', 'volleyball'
                ]

                if any(kw in artist_lower for kw in sports_keywords):
                    self.logger.debug(f"Skipping sports event: {artist}")
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
                    'url': url
                }

                events.append(event)
                self.logger.debug(f"Added event: {day:02d}.{month_num:02d} - {artist}")

            except Exception as e:
                self.logger.warning(f"Failed to parse event: {e}")
                continue

        # Sort by day
        self.events = sorted(events, key=lambda x: x['day'])

        self.logger.info(f"Found {len(self.events)} events for {self.month:02d}/{self.year}")
        return self.events


if __name__ == '__main__':
    main()
