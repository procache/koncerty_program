"""
Test Watt Music Club scraper
"""
from browser_scraper import WattMusicClubBrowserScraper

# Test for November 2025
scraper = WattMusicClubBrowserScraper(month=11, year=2025)
events = scraper.scrape()

print(f"\n{'='*60}")
print(f"Watt Music Club - November 2025")
print(f"{'='*60}")
print(f"Total events: {len(events)}\n")

for event in events:
    print(f"Day {event['day']:2d} | {event['time']} | {event['artist']}")
    print(f"  URL: {event['url']}")

# Validate
validation = scraper.validate(min_events=3, max_events=10)
print(f"\n{'='*60}")
print(f"Validation: {validation['status']}")
print(f"Expected: 3-10 events, Found: {validation['total_events']}")
print(f"{'='*60}")
