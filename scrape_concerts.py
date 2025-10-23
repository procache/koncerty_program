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
from typing import List, Dict
from datetime import datetime


# Enable HTTP caching for development
requests_cache.install_cache('concert_scraper_cache', expire_after=3600)


def load_config(config_file: str = 'kluby.json') -> Dict:
    """Load configuration from JSON file"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main entry point"""
    print("Concert Scraper Framework")
    print("=" * 60)

    # Load configuration
    config = load_config()
    month = config['config']['mesic_cislo']
    year = config['config']['rok']
    month_name = config['config']['mesic']

    print(f"Scraping concerts for {month_name} {year} (month {month})")
    print(f"Total venues: {len(config['kluby'])}")
    print("=" * 60)

    # TODO: Implement scraping loop
    # For now, just use the proof-of-concept scraper

    from scraper_akropolis import AkropolisScraper

    # Test with Palác Akropolis
    scraper = AkropolisScraper(month=month, year=year)
    events = scraper.scrape()
    validation = scraper.validate()

    print(f"\nValidation: {validation['validation']}")
    print(f"Total events: {validation['total_events']}")

    # Save to JSON
    all_events = {
        'month': month,
        'year': year,
        'month_name': month_name,
        'venues': [
            {
                'venue': scraper.VENUE_NAME,
                'city': scraper.CITY,
                'events': events,
                'validation': validation
            }
        ]
    }

    with open('events_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    print("\n[OK] Saved to events_data.json")


if __name__ == '__main__':
    main()
