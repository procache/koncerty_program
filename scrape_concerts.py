"""
Concert Scraper Framework
=========================
Main framework for scraping concert data from multiple venues.

Usage:
    python scrape_concerts.py

Configuration:
    Read from kluby.json - month, year, and venue list
"""

import json
import requests_cache
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime


# Enable HTTP caching for development
requests_cache.install_cache('concert_scraper_cache', expire_after=3600)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_file: str = 'kluby.json') -> Dict:
    """Load configuration from JSON file"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def scrape_venue(venue: Dict, month: int, year: int) -> Tuple[List[Dict], Dict, Optional[Exception]]:
    """
    Scrape a single venue with error handling (Hybrid approach)

    Uses Beautiful Soup for static sites, WebFetch data for dynamic sites.

    Args:
        venue: Venue configuration dict from kluby.json
        month: Month number
        year: Year

    Returns:
        Tuple of (events, validation, error)
        - events: List of event dicts (empty if failed)
        - validation: Validation dict (None if failed)
        - error: Exception if failed, None if success
    """
    venue_name = venue['nazev']
    url = venue['url']
    city = venue['mesto']
    min_events = venue.get('min_akci', 0)
    max_events = venue.get('max_akci', 100)

    try:
        # AUTOMATED APPROACH: Playwright → Beautiful Soup → Fail
        # (WebFetch is now only for manual debugging with Claude)

        # 1. Try Playwright scraper (JavaScript sites) - AUTOMATED
        if venue_name == "Rock Café":
            from browser_scraper import RockCafeBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RockCafeBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Lucerna Music Bar":
            from browser_scraper import LucernaMusicBarBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = LucernaMusicBarBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Roxy":
            from browser_scraper import RoxyBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RoxyBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Vagon":
            from browser_scraper import VagonBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = VagonBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Jazz Dock":
            from browser_scraper import JazzDockBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = JazzDockBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Forum Karlín":
            from browser_scraper import ForumKarlinBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = ForumKarlinBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "MeetFactory":
            from browser_scraper import MeetFactoryBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = MeetFactoryBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Malostranská beseda":
            from browser_scraper import MalostranaskaBesedaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = MalostranaskaBesedaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Reduta Jazz Club":
            from browser_scraper import RedutaJazzClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RedutaJazzClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Watt Music Club":
            from browser_scraper import WattMusicClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = WattMusicClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "O2 Arena":
            from browser_scraper import O2ArenaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters sports)")
            scraper = O2ArenaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "O2 Universum":
            from browser_scraper import O2UniversumBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = O2UniversumBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Divadlo Pod lampou":
            from browser_scraper import DivadloPodLampouBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters theatre)")
            scraper = DivadloPodLampouBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Kulturní dům Šeříkovka":
            from browser_scraper import KDSerikovkaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters non-music)")
            scraper = KDSerikovkaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Kulturní dům JAS":
            from browser_scraper import KDJASBrowserScraper
            logger.info(f"{venue_name}: Using Playwright via GoOut (automated)")
            scraper = KDJASBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        # 2. Try Beautiful Soup scraper (static HTML) - AUTOMATED
        if venue_name == "Palác Akropolis":
            from scraper_akropolis import AkropolisScraper
            logger.info(f"{venue_name}: Using Beautiful Soup (static HTML)")
            scraper = AkropolisScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        # 3. Fallback: Check if we have WebFetch data (manual debug mode)
        from webfetch_data import get_webfetch_data
        webfetch_data = get_webfetch_data(venue_name, month, year)

        if webfetch_data:
            # Use WebFetch scraper (not automated - for development only)
            from webfetch_scraper import get_webfetch_scraper
            from webfetch_scraper import store_webfetch_result

            store_webfetch_result(venue_name, webfetch_data)
            scraper = get_webfetch_scraper(venue_name, month, year)

            if scraper:
                logger.info(f"{venue_name}: Using WebFetch data (MANUAL DEBUG MODE)")
                events = scraper.scrape()
                validation = scraper.validate(min_events=min_events, max_events=max_events)
                logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
                return events, validation, None

        # 4. No scraper available
        logger.warning(f"No scraper implemented for {venue_name}")
        return [], None, Exception(f"No scraper for {venue_name}")

    except Exception as e:
        logger.error(f"Failed to scrape {venue_name}: {e}")
        return [], None, e


def main():
    """Main entry point with retry strategy"""
    logger.info("Concert Scraper Framework")
    logger.info("=" * 60)

    # Load configuration
    config = load_config()
    month = config['config']['mesic_cislo']
    year = config['config']['rok']
    month_name = config['config']['mesic']

    logger.info(f"Scraping concerts for {month_name} {year} (month {month})")
    logger.info(f"Total venues: {len(config['kluby'])}")
    logger.info("=" * 60)

    # First pass: attempt all venues
    successful_venues = []
    failed_venues = []

    for venue in config['kluby']:
        events, validation, error = scrape_venue(venue, month, year)

        if error is None and validation:
            successful_venues.append({
                'venue': venue['nazev'],
                'city': venue['mesto'],
                'events': events,
                'validation': validation
            })
        else:
            failed_venues.append((venue, error))

    # Second pass: retry failed venues
    if failed_venues:
        logger.info(f"\nRetrying {len(failed_venues)} failed venues...")

        for venue, first_error in failed_venues:
            logger.info(f"Retry: {venue['nazev']}")
            events, validation, error = scrape_venue(venue, month, year)

            if error is None and validation:
                successful_venues.append({
                    'venue': venue['nazev'],
                    'city': venue['mesto'],
                    'events': events,
                    'validation': validation
                })
                logger.info(f"  Success on retry!")
            else:
                logger.error(f"  Failed twice: {venue['nazev']} - {error}")

    # Summary
    total_events = sum(v['validation']['total_events'] for v in successful_venues)
    logger.info("\n" + "=" * 60)
    logger.info("SCRAPING COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Successful venues: {len(successful_venues)}/{len(config['kluby'])}")
    logger.info(f"Total events: {total_events}")

    # Count by status
    green = sum(1 for v in successful_venues if v['validation']['status'] == 'GREEN')
    yellow = sum(1 for v in successful_venues if v['validation']['status'] == 'YELLOW')
    red = sum(1 for v in successful_venues if v['validation']['status'] == 'RED')
    logger.info(f"Status: GREEN={green}, YELLOW={yellow}, RED={red}")
    logger.info("=" * 60)

    # Save to JSON
    all_events = {
        'month': month,
        'year': year,
        'month_name': month_name,
        'total_events': total_events,
        'venues': successful_venues
    }

    with open('events_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    logger.info("\n[OK] Saved to events_data.json")


if __name__ == '__main__':
    main()
