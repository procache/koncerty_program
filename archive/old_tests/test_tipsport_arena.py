"""
Test Tipsport Arena scraper
"""
from browser_scraper import TipsportArenaBrowserScraper

# Test for November 2025
scraper = TipsportArenaBrowserScraper(month=11, year=2025)
events = scraper.scrape()
validation = scraper.validate(min_events=2, max_events=8)

print(f"\n{'='*60}")
print(f"Tipsport Arena - Test Results")
print(f"{'='*60}")
print(f"Total events: {validation['total_events']}")
print(f"Status: {validation['status']}")
print(f"{'='*60}\n")

# Print all events
for i, event in enumerate(events, 1):
    print(f"{i}. {event['date']} {event['time']} - {event['artist']}")
    print(f"   URL: {event['url']}")
    print()
