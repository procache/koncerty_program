# Rules Learned - Koncerty Program

> Distilled lessons from experiment_log.md - actionable rules for future development.

---

## Web Scraping & Data Collection

### Rule: Always validate weekend day coverage for large venues
**Why:** Large clubs (Pal�c Akropolis, Rock Caf�, Roxy) typically have events on Fridays and Saturdays. Missing weekend days indicates incomplete data.

**Enforcement:**
- Check: If large venue (min_akci >= 15) has < 2 weekend events in month � flag for re-fetch
- Validation: LEVEL 3 anomaly detection in workflow

**Example:**
```javascript
if (venue.velikost === "velky" && weekendEvents < 2) {
  console.warn(`� ${venue.nazev}: Only ${weekendEvents} weekend events - possible incomplete data`);
  needsRefetch.push(venue);
}
```

---

### Rule: Use explicit date range prompts for complete coverage
**Why:** WebFetch may truncate results or miss pagination. Explicit instructions improve completeness.

**Enforcement:**
- Prompt template must include: "List EVERY single concert from November 1 to November 30"
- Add: "Pay special attention to [specific suspicious dates]"

**Good prompt:**
```
Extract ALL music concerts scheduled for November 2025.
IMPORTANT: List EVERY date from November 1 to November 30.
Pay special attention to November 27 and 28.
For each event provide: exact date (DD.MM.YYYY), time, artist, full URL.
```

**Bad prompt:**
```
Extract concerts for November 2025.
```

---

### Rule: Implement multi-level validation before HTML generation
**Why:** Single-pass scraping misses errors. Systematic validation catches incomplete data before user sees it.

**Enforcement:**
- LEVEL 1: Parallel WebFetch for all clubs
- LEVEL 2: Global analysis (date�club matrix)
- LEVEL 3: Detect anomalies (min thresholds, weekend gaps, date gaps)
- LEVEL 4: Targeted re-fetch for flagged clubs
- LEVEL 5: Cross-validate with WebSearch
- LEVEL 6: Generate validation report � get user confirmation

**Never skip:** User must confirm validation report before HTML generation.

---

### Rule: Use kluby.json configuration for expected ranges
**Why:** Each club has different activity levels. Configuration enables automated validation.

**Required fields per club:**
```json
{
  "nazev": "Club Name",
  "url": "https://...",
  "mesto": "Praha/PlzeH",
  "velikost": "velky/stredni/maly",
  "min_akci": 15,           // Minimum expected events
  "max_akci": 30,           // Maximum expected events
  "vikend_akce_pravdepodobnost": 0.9  // Weekend probability
}
```

**Validation logic:**
```javascript
if (actualEvents < venue.min_akci * 0.5) {
  // RED FLAG: Significantly under expected
}
if (actualEvents < venue.min_akci) {
  // YELLOW FLAG: Below minimum
}
```

---

### Rule: Cross-validate with WebSearch for suspicious results
**Why:** Some clubs use JavaScript pagination that WebFetch can't access. WebSearch finds events that WebFetch missed.

**Enforcement:**
- When: actualEvents < min_akci OR weekend gaps detected
- How: WebSearch for "[Club] program listopad 2025"
- Compare: WebSearch results vs WebFetch results

**Example:**
```
WebFetch: Jazz Dock � 6 events (only 1-4 Nov)
WebSearch: "Jazz Dock Praha program listopad 2025" � mentions events on 16, 21, 24, 28 Nov
Action: Flag for manual review or alternative URL fetch
```

---

## Data Quality

### Rule: Flag clubs below 50% of expected minimum as RED
**Why:** Dramatically low counts indicate fetch failure, not legitimate low activity.

**Thresholds:**
- **GREEN:** actualEvents >= min_akci
- **YELLOW:** actualEvents >= min_akci * 0.5 AND < min_akci
- **RED:** actualEvents < min_akci * 0.5 OR actualEvents = 0

---

### Rule: All 30 days must have at least 1 event
**Why:** With 16+ clubs, statistically impossible to have zero events city-wide on any day.

**Enforcement:**
```javascript
for (let day = 1; day <= 30; day++) {
  const eventsOnDay = allEvents.filter(e => e.day === day).length;
  if (eventsOnDay === 0) {
    console.error(`=� Day ${day}: ZERO events - data incomplete`);
  }
}
```

---

## Project Structure

### Rule: Keep kluby.json as single source of truth
**Why:** Centralized configuration enables:
- Easy updates for new months (just change mesic/rok)
- Consistent validation rules
- Version control tracking of club changes

**Monthly update:**
```json
"config": {
  "mesic": "prosinec",      // � Change this
  "mesic_en": "December",   // � Change this
  "rok": 2025,              // � Keep same (or update)
  "mesic_cislo": 12,        // � Change this
  "pocet_dni": 31           // � Update days in month
}
```

---

### Rule: Generate validation report before user confirmation
**Why:** User needs transparency about data quality before final HTML.

**Report must include:**
-  GREEN clubs: Complete data
- � YELLOW clubs: Possible gaps
- =� RED clubs: Fetch failures
- =� Global statistics: total events, day coverage
- S Questions for user: "Manual check needed for X?"

**Communication pattern:**
```
Tests  | Build  | Git clean 

Scope: Web scraping validation
Updating: rules-learned.md, experiment_log.md
Validation: 215+ events, 30/30 days covered
```

---

## Future Improvements

### Potential rules for next iterations:
1. **Automated retry logic:** If WebFetch returns < expected, auto-retry with different URL/prompt
2. **Historical baseline:** Track typical event counts per club to improve min/max ranges
3. **Genre filtering:** Better exclusion of theater/sport from music venues
4. **URL validation:** Check that all event URLs are actually accessible (HTTP 200)
5. **Duplicate detection:** Same event listed by multiple sources

---

## Meta-Rule: Document failures immediately

Every time data is incomplete:
1. Add entry to `experiment_log.md` with repro steps
2. Extract actionable rule to `rules-learned.md`
3. Implement enforcement (validation check, test, config)
4. Update `CLAUDE.md` to reference the new rule

**Never let the same failure happen twice.**

---

## Python Scraping

### Rule: Use Beautiful Soup for static HTML, not just WebFetch
**Why:** Many venue websites have events in static HTML (in <td> elements, divs, etc.). Beautiful Soup can parse these efficiently without Claude Code's context limits.

**When to use:**
- Events are in the page HTML (not loaded by JavaScript AFTER page load)
- Need to scrape 100+ events (WebFetch hits context limits)
- Want full control over parsing logic

**Enforcement:**
- Phase 1: Test with proof-of-concept venue (Palac Akropolis)
- Validate results match or exceed WebFetch results
- Check for Nov 27-28 specifically (historically problematic dates)

**Example:**
```python
from bs4 import BeautifulSoup
import requests

html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
all_tds = soup.find_all('td')

for td in all_tds:
    # Find date pattern and event_id link
    if date_match and event_link:
        events.append(parse_event(td))
```

---

### Rule: Implement HTTP caching for development
**Why:** During development, you'll re-run scrapers many times. Caching prevents hammering venue servers and speeds up development.

**Enforcement:**
```python
import requests_cache
requests_cache.install_cache('scraper_cache', expire_after=3600)
```

**Settings:**
- Expire after: 1 hour (3600 seconds) for development
- Cache file: Add to .gitignore
- Disable for production runs

---

### Rule: Parse events from <td> elements, not just <a> links
**Why:** Many venues (like Palac Akropolis) structure events in table cells with complex nested HTML. Links alone don't contain artist names or dates.

**Pattern discovered:**
```html
<td>
  <a href="/work/33298?event_id=39277"></a>
  01. 11  <!-- Date -->
  ARTIST NAME  <!-- Artist text -->
</td>
```

**Enforcement:**
- Search for all <td> tags
- Match date pattern with regex: r'(\d{1,2})\.\s*(\d{1,2})'
- Find associated event_id link within same <td>
- Extract artist text after date

---

### Rule: Validate Nov 27-28 specifically in unit tests
**Why:** These dates were historically problematic (missed in initial scrapes). Explicit test prevents regression.

**Enforcement:**
```python
def test_november_27_28_coverage(events):
    has_27 = any(e['day'] == 27 for e in events)
    has_28 = any(e['day'] == 28 for e in events)
    assert has_27, "Missing Nov 27 events"
    assert has_28, "Missing Nov 28 events"
```

---

### Rule: Store month/year in config, not command-line arguments
**Why:** User requested: "Chci parametr, pro ktery mesic a rok se data stahuji, ulozit do config souboru"

**Enforcement:**
- Read from kluby.json: config.mesic_cislo, config.rok
- No argparse or sys.argv for month/year
- Command-line args only for optional flags (--debug, --no-cache)

**Example:**
```python
config = json.load(open('kluby.json'))
month = config['config']['mesic_cislo']  # 11
year = config['config']['rok']           # 2025
```

---

### Rule: Implement per-club parser architecture
**Why:** Each venue has different HTML structure. Generic parser will fail or miss events.

**Enforcement:**
- Phase 1: One parser per club (scraper_akropolis.py, scraper_roxy.py, etc.)
- Each parser inherits from base class with common methods
- Main framework calls appropriate parser based on venue name

**Structure:**
```python
class BaseScraper:
    def fetch_html(self): ...
    def validate(self): ...
    def save_json(self): ...

class AkropolisScraper(BaseScraper):
    def parse_event_from_td(self, td): ...
    def scrape(self): ...

class RoxyScraper(BaseScraper):
    def parse_event_from_div(self, div): ...
    def scrape(self): ...
```

---

## Prioritization & Time Management

### Rule: Defer complex venues, maximize simple venue coverage first
**Why:** One complex venue requiring hours of debugging provides less value than implementing 5+ simple venues in the same time.

**Decision criteria:**
- If a venue requires >3 debug attempts without success → defer it
- Continue with simpler venues to maximize coverage percentage
- Return to complex cases after implementing majority of venues

**Example - Cross Club:**
- **Problem:** Complex JavaScript calendar, events load via AJAX
- **Attempts:** 5 debug scripts, no events extracted
- **Decision:** Defer (1 venue, 8-20 events) → implement simpler venues instead
- **Result:** Better ROI - can implement 5+ venues in same time

**Enforcement:**
- Mark deferred venues clearly in plan.md with reason
- Revisit after reaching 70%+ coverage of simpler venues
- Consider manual data collection as fallback for very complex sites

---

## Playwright & Browser Automation

### Rule: Implement infinite scroll for lazy-loaded content
**Why:** Many modern websites use infinite scroll or lazy loading to load content dynamically as the user scrolls. Without scrolling, Playwright only captures initially visible content, missing events below the fold.

**Signs a website needs infinite scroll:**
- Event count significantly lower than expected
- Page shows loading spinners or "Load more" buttons
- Network tab shows AJAX requests triggered by scrolling
- Manual inspection shows more events when scrolling

**Enforcement:**
```python
def fetch_with_infinite_scroll(self) -> str:
    """Scroll down page until no new content loads"""
    previous_height = 0
    scroll_attempts = 0
    max_scrolls = 10  # Safety limit

    while scroll_attempts < max_scrolls:
        current_height = page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            # Height unchanged = reached bottom
            break

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for AJAX content to load
        page.wait_for_timeout(1500)  # 1.5 seconds

        previous_height = current_height
        scroll_attempts += 1

    return page.content()
```

**Settings:**
- Wait time: 1.5 seconds between scrolls (adjust per site)
- Max scrolls: 10 (prevents infinite loops)
- Break condition: Page height unchanged = no new content

**Example - MeetFactory:**
- Without scroll: 5 events from 10 visible boxes
- With scroll: 15 events from 41 total boxes
- Scrolls needed: 5 (reached bottom when height stopped changing)

**Testing:**
```python
# Log progress to verify scrolling works
event_count = page.evaluate("document.querySelectorAll('div.ab-box').length")
logger.info(f"Scroll {scroll_attempts}: Found {event_count} event boxes")
```

---

## HTML Parsing Patterns

### Rule: Parse nested JSON-HTML hybrid structures in calendar systems
**Why:** Modern calendar systems often embed event data as JSON in HTML attributes, with event details as HTML within that JSON. Requires multi-stage parsing.

**Pattern discovered in:** Reduta Jazz Club calendar

**Structure:**
```html
<td id="calendar_2025-11-01" data-label='{"id":"...","body":"<span class=\"tt-time\">19:00</span>..."}'>
```

**Enforcement:**
```python
# Stage 1: Parse main HTML
soup = BeautifulSoup(html, 'lxml')

# Stage 2: Find elements with JSON data
event_tds = soup.find_all('td', {'data-label': True})

for td in event_tds:
    # Stage 3: Parse JSON from attribute
    data_label = td.get('data-label', '')
    event_data = json.loads(data_label)

    # Stage 4: Parse HTML from JSON body
    body_html = event_data.get('body', '')
    body_soup = BeautifulSoup(body_html, 'lxml')

    # Stage 5: Extract data from nested HTML
    time = body_soup.find('span', class_='tt-time').get_text()
    artist = body_soup.find('span', class_='tt-text').get_text()
```

**Key points:**
- Import `json` module for JSON parsing
- Use try/except around JSON parsing (may be malformed)
- Nested BeautifulSoup instances are fine - creates new parser
- Data flows: HTML → JSON → HTML → Data

**Example - Reduta Jazz Club:**
- URL: `/program-cs/MMYYYY` (month-year format)
- Calendar cells: `<td id="zabuto_calendar_2025-11-DD">`
- Data attribute: `data-label` contains JSON
- JSON body field: Contains HTML with event details

---

### Rule: Extract artists from flexible heading tags (h1-h4)
**Why:** Different venues use different heading levels for artist names. Searching all heading tags ensures we catch the artist regardless of HTML structure.

**Enforcement:**
```python
# Search all heading levels at once
h_tags = row.find_all(['h1', 'h2', 'h3', 'h4'])
artist = h_tags[0].get_text(strip=True) if h_tags else ""

if not artist:
    continue  # Skip events without artist names
```

**Benefits:**
- Handles varying HTML structures across venues
- Doesn't assume specific heading level
- Falls back gracefully if no heading found

**Example usage:**
- Malostranská beseda: Artist in various heading levels within `div.row`
- Works even when HTML structure changes between page updates

---

## Data Validation

### Rule: Max event counts are soft limits, not hard failures
**Why:** Venues may have more events than expected during active months. Validation should warn but not fail on exceeding maximum.

**Evidence:**
- Malostranská beseda: Expected 5-15 events, found 28 (GREEN status)
- Reduta Jazz Club: Expected 5-20 events, found 30 (GREEN status)

**Enforcement:**
```python
def validate(self, min_events: int, max_events: int):
    # Fail only on minimum threshold
    if total_events < min_events * 0.5:
        status = 'RED'
    elif total_events < min_events:
        status = 'YELLOW'
    else:
        status = 'GREEN'  # Even if > max_events

    # Log if over max, but don't fail
    if total_events > max_events:
        logger.info(f"Above expected max ({max_events}), but still GREEN")
```

**Rationale:**
- Min threshold: Hard requirement (indicates scraper failure)
- Max threshold: Soft guidance (venues can have high activity)
- GREEN status based on meeting minimum, not staying under maximum

---

## URL Patterns & Navigation

### Rule: Try direct URL construction before calendar navigation
**Why:** Faster and more reliable to construct URLs with month/year parameters than to navigate JavaScript calendars.

**Patterns discovered:**

**Month-Year in URL path:**
```python
# Reduta Jazz Club
url = f"https://www.redutajazzclub.cz/program-cs/{month:02d}{year}"
# Example: /program-cs/112025 (November 2025)
```

**Month-Year in query parameters:**
```python
# Malostranská beseda
url = f"https://www.malostranska-beseda.cz/club/program?year={year}&month={month}"
# Example: ?year=2025&month=11
```

**Enforcement:**
- Always inspect URL patterns in browser first
- Look for month/year in URL when viewing current month
- Construct URL directly rather than clicking navigation
- Falls back to calendar navigation only if direct URL doesn't work

**Benefits:**
- Faster (one page load vs multiple clicks)
- More reliable (no timing issues with clicks)
- Easier to debug (direct URL inspection)

---

## Future Python Improvements

### Planned enhancements for Phase 2-6:
1. **Retry logic:** If scraper fails, attempt other clubs first, retry once, log failure
2. **Unit tests:** Weekend coverage, URL validity, date range, Nov 27-28 specific
3. **HTML generation:** Read events_data.json, generate full HTML with no context limits
4. **Logging:** Use Python logging module instead of print statements
5. **Type safety:** Add mypy checks for type hints

---
