"""
Test O2 Arena scraper
"""
from browser_scraper import O2ArenaBrowserScraper

# Test for November 2025
scraper = O2ArenaBrowserScraper(month=11, year=2025)
events = scraper.scrape()

print(f"\n{'='*60}")
print(f"O2 Arena - November 2025 (Music Only)")
print(f"{'='*60}")
print(f"Total music events: {len(events)}\n")

for event in events:
    print(f"Day {event['day']:2d} | {event['time']} | {event['artist']}")
    print(f"  URL: {event['url']}")

# Validate
validation = scraper.validate(min_events=4, max_events=15)
print(f"\n{'='*60}")
print(f"Validation: {validation['status']}")
print(f"Expected: 4-15 events, Found: {validation['total_events']}")
print(f"{'='*60}")
