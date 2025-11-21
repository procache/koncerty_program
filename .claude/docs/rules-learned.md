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

### Rule: Use alternative data sources when official websites are unavailable or complex
**Context:** U Staré Paní, Papírna Plzeň, Tipsport Arena - 2025-10-25

**Alternative sources:**
1. **GoOut.net** - Standardized event aggregator
   - URL pattern: `https://goout.net/en/{venue-slug}/{venue-id}/events/`
   - Pros: Standardized HTML structure, reliable uptime
   - Cons: May have fewer events than official site

2. **Ticketportal.cz** - Official ticketing platform
   - URL pattern: `https://www.ticketportal.cz/venue/{VENUE-NAME}`
   - Pros: Official data source, includes ticket links
   - Cons: Only venues that use Ticketportal

**When to apply:**
- Official website unreachable (ERR_CONNECTION_REFUSED, DNS failure)
- Official website has complex JavaScript (carousel, infinite scroll that won't load)
- User provides alternative source as authoritative

**Examples:**
- U Staré Paní: Official site down → GoOut (25 events)
- Papírna Plzeň: Complex structure → GoOut (16 events)
- Tipsport Arena: Complex Splide carousel → Ticketportal (5 events)

---

### Rule: Use find_next() for nested HTML structures, not find_next_sibling()
**Context:** Cross Club scraper - 2025-10-25

**Technical pattern:**
```python
# WRONG: Only searches siblings at same level
h2 = predel.find_next_sibling('h2')  # Returns None

# CORRECT: Traverses down the tree
h2 = predel.find_next('h2')  # Finds h2 inside nested div.article
```

**When to apply:**
- HTML structure has intermediate wrapper divs
- `find_next_sibling()` returns None unexpectedly
- Element you're looking for is nested inside sibling

**HTML example:**
```html
<div class="predel">Date separator</div>
<div class="article">     <!-- Intermediate wrapper -->
  <h2>Event name</h2>     <!-- Target element -->
</div>
```

---

### Rule: Validate low event counts before flagging as errors
**Context:** Cross Club - 2025-10-25

**Pattern:**
- Some venues have legitimately low event counts for certain months
- Always verify with manual check before assuming scraper failure
- Low count ≠ broken scraper

**Detection:**
```python
# Don't immediately fail on low counts
if len(events) < min_expected:
    # Log warning but allow completion
    logger.warning(f"Low event count: {len(events)} (expected {min_expected}+)")
    # Manual verification needed
```

**Example:**
- Cross Club November 2025: Expected 8-20, found 1
- Manual check confirmed: Only 1 event scheduled for November
- Status: GREEN (accurate data, not scraper bug)

---

### Rule: Use ISO 8601 datetime parsing for attribute-based dates
**Context:** Tipsport Arena (Ticketportal) - 2025-10-25

**Technical pattern:**
```python
# Extract from data attribute, not visible text
iso_date = date_div.get('content', '')  # "2025-11-07T18:30"
dt = datetime.fromisoformat(iso_date)

# Extract components
day = dt.day
month = dt.month
year = dt.year
time = dt.strftime('%H:%M')
```

**When to apply:**
- Dates stored in `data-*` attributes or `content` attributes
- Format is ISO 8601 (YYYY-MM-DDTHH:MM or YYYY-MM-DDTHH:MM:SS)
- Microdata/Schema.org markup (`itemprop="startDate"`)

**HTML example:**
```html
<div itemprop="startDate" content="2025-11-07T18:30">
  Čt 7. listopadu 2025, 18:30
</div>
```

---

### Rule: Iterate on UI sizing based on user feedback
**Context:** Interactive calendar feature - 2025-10-26

**Pattern:**
1. Implement feature with reasonable defaults
2. Show to user
3. Adjust sizing/spacing based on feedback
4. Iterate until user satisfied

**Example:**
- **V1:** Calendar 800px wide → User: "Too large"
- **V2:** Calendar 400px wide → User: "Perfect"

**Key metrics to adjust:**
- `max-width` (overall size)
- `gap` (spacing between elements)
- `padding` (internal spacing)
- `font-size` (text size)
- `border` thickness

**When to apply:**
- Any visual UI feature (calendars, tables, cards)
- User sees feature for first time
- User provides specific feedback ("too large", "too small", "cluttered")

---

## Summary Statistics

**Total rules:** 16
**Categories:**
- Data Validation: 3 (venue city verification, weekend coverage, low event count validation)
- Web Scraping: 9 (date prompts, infinite scroll, filtering, deferral, GoOut fallback, alternative sources, find_next(), ISO dates, UI iteration)
- Testing: 1 (TDD workflow)
- Repository Management: 1 (gitignore patterns)
- Workflow: 2 (multi-level validation, documentation comments)

**Most critical rules:**
1. Use alternative data sources when official websites unavailable (GoOut, Ticketportal)
2. Always verify venue city via multiple sources
3. Use keyword-based filtering for mixed-content venues
4. Implement infinite scroll for lazy-loaded content
5. Multi-level validation required before HTML generation
6. Use find_next() for nested HTML structures
7. Validate low event counts before flagging as errors
