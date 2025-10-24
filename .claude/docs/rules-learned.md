# Rules Learned - Koncerty Program

> Actionable rules extracted from experiment_log.md failures and discoveries.

---

## Data Validation Rules

### Rule: Always validate weekend coverage for large venues
**Context:** Palác Akropolis missing events (27-28 November) - 2025-10-23

**Enforcement:**
- Multi-level validation system (LEVEL 1-6)
- Anomaly detection for missing weekend days
- Cross-validation with WebSearch for suspicious results

**Rationale:**
- WebFetch may truncate results without warning
- Weekend days have high event probability for large venues
- Missing weekends indicates incomplete data fetch

---

### Rule: Always verify venue city via multiple independent sources
**Context:** Systematic venue location mislabeling - 2025-10-24

**Enforcement:**
- Cross-check kluby.json city against GoOut.net listings
- Verify with WebSearch for venue address
- Check venue website contact/about page

**Rationale:**
- Initial kluby.json had 4 venues with wrong cities (Praha instead of Plzeň)
- City errors affect data organization and filtering
- Multiple sources prevent systematic mislabeling

**Examples of verification:**
- Divadlo Pod lampou: Address confirmed as Havířská 11, Plzeň
- Kulturní dům JAS: Address confirmed as Jablonského 39, Plzeň
- Watt Music Club: GoOut listing showed Plzeň location

---

## Web Scraping Rules

### Rule: Use explicit date range prompts when fetching
**Context:** Palác Akropolis missing events - 2025-10-23

**Pattern:**
```
Bad:  "Get November 2025 events"
Good: "List EVERY date from 1-30 November 2025"
```

**Rationale:**
- Explicit prompts reduce pagination truncation
- Forces complete date coverage
- Prevents silent data loss

---

### Rule: Implement infinite scroll for lazy-loaded content
**Context:** MeetFactory missing 10 events - 2025-10-23

**Technical pattern:**
```python
def fetch_with_infinite_scroll(self) -> str:
    previous_height = 0
    scroll_attempts = 0
    max_scrolls = 10

    while scroll_attempts < max_scrolls:
        current_height = page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            break  # Reached bottom

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)  # Wait for AJAX load

        previous_height = current_height
        scroll_attempts += 1
```

**Detection criteria:**
- User reports more events than scraper finds
- Website has "Load more" or lazy loading behavior
- Event count significantly below expected range

---

### Rule: Use keyword-based filtering for mixed-content venues
**Context:** O2 Arena sports filtering - 2025-10-24

**Pattern:**
```python
def is_sports_event(self, event_name: str) -> bool:
    sports_keywords = [
        'HC Sparta', 'Bílí Tygři', 'hockey', 'FMX',
        'Global Champions', 'basketball', 'football',
        'extraliga', 'playoffs'
    ]
    event_lower = event_name.lower()
    return any(keyword.lower() in event_lower for keyword in sports_keywords)
```

**When to apply:**
- Venue hosts both music and non-music events (sports, theatre, film)
- kluby.json has note: "Jen hudební koncerty, ne sport"
- Manual inspection reveals mixed content

**Examples:**
- O2 Arena: Filters hockey (HC Sparta), FMX events
- Palác Akropolis: Filter divadlo (theatre) and film
- Moving Station: Filter divadlo and film

---

### Rule: Defer complex venues and maximize simpler implementations first
**Context:** Cross Club complex JavaScript calendar - 2025-10-23

**Decision criteria:**
- Venue requires >5 debugging iterations
- Time investment disproportionate to event count (1 venue = hours of debugging)
- Other venues with simpler structures remain unimplemented

**Strategy:**
1. Defer complex venue
2. Implement 5+ simpler venues in same time
3. Maximize total venue coverage
4. Return to complex cases after most venues complete
5. Fallback: Manual data collection if automation too complex

**Examples:**
- Deferred: Cross Club (complex AJAX calendar)
- Deferred: Sportovní hala Fortuna (complex Splide carousel)
- Prioritized: Simpler Playwright venues (Vagon, Jazz Dock, Roxy)

---

### Rule: Use GoOut.net as fallback when official websites fail
**Context:** Watt Music Club, Kulturní dům JAS - 2025-10-24

**Pattern:**
```python
# When official website unreachable
url = "https://goout.net/en/venue-name/venue-id/events/"
```

**When to apply:**
- Official website returns connection errors (ERR_CONNECTION_REFUSED, DNS failure)
- Official website has no structured events page
- GoOut has verified listing for the venue

**Advantages:**
- GoOut has standardized HTML structure (easier parsing)
- Reliable uptime
- Covers many Czech venues

**Limitation:**
- May have fewer events than official website
- Update lag possible

---

## Testing Rules

### Rule: Follow TDD workflow for all new scrapers
**Context:** O2 venues test suite - 2025-10-24

**Workflow: RED → GREEN → REFACTOR**
1. **RED:** Write tests first (expect failures)
2. **GREEN:** Make tests pass (adjust expectations if behavior is correct)
3. **REFACTOR:** Review for duplication, improve code quality

**Test coverage requirements:**
- Scraper initialization and configuration
- Event structure validation (required fields, types, ranges)
- Special logic (filtering, deduplication, parsing)
- Validation workflow (min/max events)
- Integration tests (if multiple scrapers interact)

**Example:**
```python
def test_is_sports_event_hockey(self, scraper):
    """Test that hockey events are correctly identified as sports"""
    assert scraper.is_sports_event("HC Sparta Praha x BK Mladá Boleslav") == True

def test_is_sports_event_music(self, scraper):
    """Test that music events are NOT identified as sports"""
    assert scraper.is_sports_event("Hans Zimmer Live") == False
```

---

## Repository Management Rules

### Rule: Keep repository clean with proper .gitignore patterns
**Context:** Repository cleanup - 2025-10-24

**Always exclude:**
1. **Debug scripts:** `debug_*.py`, `parse_*.py`
2. **HTML snapshots:** `*_goout.html`, `o2arena.html`, etc.
3. **Log files:** `scrape_output*.log`
4. **Temporary test scripts:** `test_venue.py` (not in main test suite)

**Always track:**
- Production scrapers (`browser_scraper.py`, `scrape_concerts.py`)
- Official test suite (`test_o2_scrapers.py`)
- Configuration (`kluby.json`, `requirements.txt`)
- Documentation (`.claude/docs/`, `plan.md`)

**Pattern in .gitignore:**
```gitignore
# Debug scripts (temporary development files)
debug_*.py
parse_*.py

# HTML snapshots from debug scripts
*_goout.html
o2arena.html

# Log files
scrape_output*.log
```

---

## Workflow Rules

### Rule: Multi-level validation required before HTML generation
**Context:** Initial approach lacked validation - 2025-10-23

**Validation levels (kluby.json approach):**
1. **LEVEL 1:** Total events count vs. global minimum
2. **LEVEL 2:** Per-club event count vs. expected range
3. **LEVEL 3:** Weekend coverage check (all Fri/Sat/Sun)
4. **LEVEL 4:** Date coverage (all 30 days have ≥1 event)
5. **LEVEL 5:** Anomaly detection (clubs < 50% expected flagged RED)
6. **LEVEL 6:** Cross-validation with WebSearch for suspicious results

**Enforcement:**
- Generate validation report after all scrapers run
- Ask user confirmation before HTML generation
- Only proceed if no RED flags or user approves

---

### Rule: Document exclusion patterns with comments
**Context:** .gitignore update - 2025-10-24

**Pattern:**
```gitignore
# Category name (why excluded)
pattern1
pattern2

# Another category (why excluded)
pattern3
```

**Rationale:**
- Explains rationale for future maintainers
- Prevents accidental removal of important patterns
- Documents project evolution

---

## Summary Statistics

**Total rules:** 11
**Categories:**
- Data Validation: 2
- Web Scraping: 5
- Testing: 1
- Repository Management: 1
- Workflow: 2

**Most critical rules:**
1. Always verify venue city via multiple sources
2. Use keyword-based filtering for mixed-content venues
3. Implement infinite scroll for lazy-loaded content
4. Follow TDD workflow for all new scrapers
5. Multi-level validation required before HTML generation
