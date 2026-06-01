"""
Concert Scraper Framework
=========================
Main framework for scraping concert data from multiple venues.

Usage:
    python scrape_concerts.py

Configuration:
    Read from kluby.json - month, year, and venue list
"""

import argparse
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
            from scrapers.browser_scraper import RockCafeBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RockCafeBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Lucerna Music Bar":
            from scrapers.browser_scraper import LucernaMusicBarBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = LucernaMusicBarBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Roxy":
            from scrapers.browser_scraper import RoxyBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RoxyBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Vagon":
            from scrapers.browser_scraper import VagonBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = VagonBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Jazz Dock":
            from scrapers.browser_scraper import JazzDockBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = JazzDockBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Forum Karlín":
            from scrapers.browser_scraper import ForumKarlinBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = ForumKarlinBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "MeetFactory":
            from scrapers.browser_scraper import MeetFactoryBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = MeetFactoryBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Malostranská beseda":
            from scrapers.browser_scraper import MalostranaskaBesedaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = MalostranaskaBesedaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Reduta Jazz Club":
            from scrapers.browser_scraper import RedutaJazzClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = RedutaJazzClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Watt Music Club":
            from scrapers.browser_scraper import WattMusicClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = WattMusicClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "O2 Arena":
            from scrapers.browser_scraper import O2ArenaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters sports)")
            scraper = O2ArenaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "O2 Universum":
            from scrapers.browser_scraper import O2UniversumBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = O2UniversumBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Divadlo Pod lampou":
            from scrapers.browser_scraper import DivadloPodLampouBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters theatre)")
            scraper = DivadloPodLampouBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Kulturní dům Šeříkovka":
            from scrapers.browser_scraper import KDSerikovkaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated, filters non-music)")
            scraper = KDSerikovkaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Buena Vista Club":
            from scrapers.browser_scraper import BuenaVistaClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = BuenaVistaClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Papírna Plzeň":
            from scrapers.browser_scraper import PapirnaPlzenBrowserScraper
            logger.info(f"{venue_name}: Using Playwright via GoOut (automated)")
            scraper = PapirnaPlzenBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "U Staré Paní Jazz & Cocktail Club":
            from scrapers.browser_scraper import UStarePaniJazzClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright via GoOut (automated)")
            scraper = UStarePaniJazzClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Cross Club":
            from scrapers.browser_scraper import CrossClubBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = CrossClubBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Sportovní hala Fortuna (Tipsport Arena)":
            from scrapers.browser_scraper import TipsportArenaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright via Ticketportal (automated, filters sports)")
            scraper = TipsportArenaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Sono Centrum":
            from scrapers.browser_scraper import SonoCentrumBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = SonoCentrumBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Fléda":
            from scrapers.browser_scraper import FledaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = FledaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Kabinet Múz":
            from scrapers.browser_scraper import KabinetMuzBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = KabinetMuzBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Stará Pekárna":
            from scrapers.browser_scraper import StaraPekarnaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = StaraPekarnaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        if venue_name == "Melodka":
            from scrapers.browser_scraper import MelodkaBrowserScraper
            logger.info(f"{venue_name}: Using Playwright (automated)")
            scraper = MelodkaBrowserScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        # 2. Try Beautiful Soup scraper (static HTML) - AUTOMATED
        if venue_name == "Palác Akropolis":
            from scrapers.scraper_akropolis import AkropolisScraper
            logger.info(f"{venue_name}: Using Beautiful Soup (static HTML)")
            scraper = AkropolisScraper(month=month, year=year)
            events = scraper.scrape()
            validation = scraper.validate(min_events=min_events, max_events=max_events)
            logger.info(f"{venue_name}: {validation['total_events']} events ({validation['status']})")
            return events, validation, None

        # 3. No scraper available
        logger.warning(f"No scraper implemented for {venue_name}")
        return [], None, Exception(f"No scraper for {venue_name}")

    except Exception as e:
        logger.error(f"Failed to scrape {venue_name}: {e}")
        return [], None, e


def print_validation_report(successful_venues: List[Dict], config_kluby: List[Dict]) -> List[str]:
    """
    Print color-coded validation report and return list of problem venue names.

    Returns:
        List of venue names with 0 events where min_akci > 0 (RED alert venues)
    """
    print("\n" + "=" * 60)
    print("VALIDAČNÍ REPORT")
    print("=" * 60)

    red_venues = []
    venue_min = {v['nazev']: v.get('min_akci', 0) for v in config_kluby}

    for v in successful_venues:
        status = v['validation']['status']
        name = v['venue']
        count = v['validation']['total_events']
        expected = v['validation']['expected_range']
        icon = "✅" if status == 'GREEN' else ("⚠️ " if status == 'YELLOW' else "🚨")
        print(f"  {icon} {name}: {count} eventů (očekáváno {expected}) [{status}]")
        if count == 0 and venue_min.get(name, 0) > 0:
            red_venues.append(name)

    print("=" * 60)

    if red_venues:
        print("\n🚨 VENUES S 0 EVENTY (možné selhání scraperu):")
        for name in red_venues:
            print(f"   - {name}")
        print()

    return red_venues


def main():
    """Main entry point with retry strategy"""
    parser = argparse.ArgumentParser(description='Concert scraper')
    parser.add_argument('--force', action='store_true',
                        help='Přeskočit interaktivní potvrzení a vždy uložit výstup')
    args = parser.parse_args()

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
    logger.info(f"\nÚspěšné venues: {len(successful_venues)}/{len(config['kluby'])}")
    logger.info(f"Celkem eventů: {total_events}")

    # Validation report + interactive confirmation
    red_venues = print_validation_report(successful_venues, config['kluby'])

    if red_venues and not args.force:
        answer = input("Pokračovat a uložit events_data.json i přes chybějící data? [y/N]: ").strip().lower()
        if answer != 'y':
            logger.info("Přerušeno uživatelem. events_data.json nebyl přepsán.")
            return

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

    logger.info("\n✅ Uloženo do events_data.json")
    logger.info("Spusť python generate_html.py pro vygenerování HTML.")


if __name__ == '__main__':
    main()
