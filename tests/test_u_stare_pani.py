"""
Test U Staré Paní Jazz & Cocktail Club scraper
"""
from browser_scraper import UStarePaniJazzClubBrowserScraper

# Test for November 2025
scraper = UStarePaniJazzClubBrowserScraper(month=11, year=2025)
events = scraper.scrape()
validation = scraper.validate(min_events=5, max_events=15)

print(f"\n{'='*60}")
print(f"U Stare Pani Jazz & Cocktail Club - Test Results")
print(f"{'='*60}")
print(f"Total events: {validation['total_events']}")
print(f"Status: {validation['status']}")
print(f"{'='*60}\n")

# Print first 5 events
for i, event in enumerate(events[:5], 1):
    print(f"{i}. {event['date']} {event['time']} - {event['artist']}")
    print(f"   URL: {event['url']}")
    print()

if len(events) > 5:
    print(f"... and {len(events) - 5} more events")
