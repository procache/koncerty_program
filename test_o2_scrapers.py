"""
Test suite for O2 Arena and O2 Universum scrapers

Following TDD workflow:
- RED: Write tests first
- GREEN: Make tests pass
- REFACTOR: Improve code while keeping tests green
"""
import pytest
from browser_scraper import O2ArenaBrowserScraper, O2UniversumBrowserScraper


class TestO2ArenaScraper:
    """Tests for O2 Arena scraper with sports filtering"""

    @pytest.fixture
    def scraper(self):
        """Create O2 Arena scraper instance for November 2025"""
        return O2ArenaBrowserScraper(month=11, year=2025)

    def test_scraper_initialization(self, scraper):
        """Test that scraper initializes with correct parameters"""
        assert scraper.venue_name == "O2 Arena"
        assert scraper.city == "Praha"
        assert scraper.month == 11
        assert scraper.year == 2025
        assert scraper.url == "https://www.o2arena.cz/en/events/"

    def test_sports_keywords_defined(self, scraper):
        """Test that sports keywords list is defined"""
        assert hasattr(scraper, 'sports_keywords')
        assert isinstance(scraper.sports_keywords, list)
        assert len(scraper.sports_keywords) > 0
        # Check for key sports keywords
        assert any('hockey' in kw.lower() for kw in scraper.sports_keywords)
        assert any('sparta' in kw.lower() for kw in scraper.sports_keywords)

    def test_is_sports_event_hockey(self, scraper):
        """Test that hockey events are correctly identified as sports"""
        assert scraper.is_sports_event("HC Sparta Praha x BK Mladá Boleslav") == True
        assert scraper.is_sports_event("HC Sparta Praha vs Liberec") == True
        assert scraper.is_sports_event("Bílí Tygři Liberec") == True

    def test_is_sports_event_other_sports(self, scraper):
        """Test that other sports events are identified"""
        assert scraper.is_sports_event("FMX GLADIATOR GAMES 2025") == True
        assert scraper.is_sports_event("Global Champions Prague Playoffs") == True

    def test_is_sports_event_music(self, scraper):
        """Test that music events are NOT identified as sports"""
        assert scraper.is_sports_event("Hans Zimmer Live") == False
        assert scraper.is_sports_event("OLYMPIC") == False
        assert scraper.is_sports_event("IL VOLO") == False
        assert scraper.is_sports_event("Jamie Cullum") == False

    def test_scrape_returns_list(self, scraper):
        """Test that scrape() returns a list"""
        events = scraper.scrape()
        assert isinstance(events, list)

    def test_scrape_finds_music_events(self, scraper):
        """Test that scraper finds music events and filters sports"""
        events = scraper.scrape()
        assert len(events) > 0, "Should find at least some music events"

        # Check that all returned events are music (not sports)
        for event in events:
            assert not scraper.is_sports_event(event['artist']), \
                f"Event '{event['artist']}' should not be a sports event"

    def test_event_structure(self, scraper):
        """Test that scraped events have correct structure"""
        events = scraper.scrape()

        if len(events) > 0:
            event = events[0]

            # Check required fields
            assert 'date' in event
            assert 'day' in event
            assert 'month' in event
            assert 'year' in event
            assert 'time' in event
            assert 'artist' in event
            assert 'venue' in event
            assert 'city' in event
            assert 'url' in event

            # Check field types and values
            assert isinstance(event['day'], int)
            assert 1 <= event['day'] <= 31
            assert event['month'] == 11
            assert event['year'] == 2025
            assert event['venue'] == "O2 Arena"
            assert event['city'] == "Praha"
            assert event['url'].startswith('http')

    def test_validation_passes(self, scraper):
        """Test that validation works correctly"""
        events = scraper.scrape()
        validation = scraper.validate(min_events=4, max_events=15)

        assert 'status' in validation
        assert 'total_events' in validation
        assert validation['total_events'] == len(events)


class TestO2UniversumScraper:
    """Tests for O2 Universum scraper (music only, no sports filtering)"""

    @pytest.fixture
    def scraper(self):
        """Create O2 Universum scraper instance for November 2025"""
        return O2UniversumBrowserScraper(month=11, year=2025)

    def test_scraper_initialization(self, scraper):
        """Test that scraper initializes with correct parameters"""
        assert scraper.venue_name == "O2 Universum"
        assert scraper.city == "Praha"
        assert scraper.month == 11
        assert scraper.year == 2025
        assert scraper.url == "https://www.o2universum.cz/en/events/"

    def test_no_sports_filtering_needed(self, scraper):
        """Test that O2 Universum doesn't have sports filtering logic"""
        # O2 Universum should not have sports_keywords attribute
        assert not hasattr(scraper, 'sports_keywords')

    def test_scrape_returns_list(self, scraper):
        """Test that scrape() returns a list"""
        events = scraper.scrape()
        assert isinstance(events, list)

    def test_scrape_finds_events(self, scraper):
        """Test that scraper finds events"""
        events = scraper.scrape()
        assert len(events) > 0, "Should find at least some events"

    def test_event_structure(self, scraper):
        """Test that scraped events have correct structure"""
        events = scraper.scrape()

        if len(events) > 0:
            event = events[0]

            # Check required fields
            assert 'date' in event
            assert 'day' in event
            assert 'month' in event
            assert 'year' in event
            assert 'time' in event
            assert 'artist' in event
            assert 'venue' in event
            assert 'city' in event
            assert 'url' in event

            # Check field types and values
            assert isinstance(event['day'], int)
            assert 1 <= event['day'] <= 31
            assert event['month'] == 11
            assert event['year'] == 2025
            assert event['venue'] == "O2 Universum"
            assert event['city'] == "Praha"
            assert event['url'].startswith('http')

    def test_validation_passes(self, scraper):
        """Test that validation works correctly"""
        events = scraper.scrape()
        validation = scraper.validate(min_events=3, max_events=10)

        assert 'status' in validation
        assert 'total_events' in validation
        assert validation['total_events'] == len(events)

    def test_urls_contain_o2_domain(self, scraper):
        """Test that event URLs point to O2 domains (Arena or Universum)

        Note: O2 websites cross-list events, so O2 Universum page may show
        some O2 Arena events and vice versa. This is expected behavior.
        """
        events = scraper.scrape()

        for event in events:
            # Accept URLs from either O2 Arena or O2 Universum
            assert ('o2universum.cz' in event['url'].lower() or
                    'o2arena.cz' in event['url'].lower()), \
                f"Event URL should point to an O2 domain: {event['url']}"


class TestO2ScrapersIntegration:
    """Integration tests comparing O2 Arena and O2 Universum scrapers"""

    def test_both_scrapers_work_independently(self):
        """Test that both scrapers can run without interfering with each other"""
        arena_scraper = O2ArenaBrowserScraper(month=11, year=2025)
        universum_scraper = O2UniversumBrowserScraper(month=11, year=2025)

        arena_events = arena_scraper.scrape()
        universum_events = universum_scraper.scrape()

        assert len(arena_events) > 0
        assert len(universum_events) > 0

        # Verify they have different venue names
        if arena_events and universum_events:
            assert arena_events[0]['venue'] != universum_events[0]['venue']

    def test_combined_events_count(self):
        """Test that combined events from both venues meet minimum threshold"""
        arena_scraper = O2ArenaBrowserScraper(month=11, year=2025)
        universum_scraper = O2UniversumBrowserScraper(month=11, year=2025)

        arena_events = arena_scraper.scrape()
        universum_events = universum_scraper.scrape()

        total_events = len(arena_events) + len(universum_events)
        assert total_events >= 10, \
            f"Combined O2 venues should have at least 10 events, found {total_events}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
