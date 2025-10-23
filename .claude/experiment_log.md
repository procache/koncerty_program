# Experiment Log - Koncerty Program

> Raw record of failures and lessons learned during development.

---

## Issue: Palác Akropolis missing events (27-28 November)
**Date:** 2025-10-23

- **Context:** Initial WebFetch of Palác Akropolis returned 22 events but skipped November 27-28 (weekend days)
- **Failure Type:** Data completeness issue - pagination/truncation in WebFetch results

### =Î Proof
- First fetch: 22 events, missing dates 27, 28 (Friday, Saturday - high-probability days)
- Second fetch with explicit instructions: returned complete 27 events including 27-28 Nov

### =Ï Rule Added
- `.claude/docs/rules-learned.md`: Always validate weekend day coverage for large venues
- Enforcement: Multi-level validation system with anomaly detection

### Resolution
- Implemented systematic validation workflow (LEVEL 1-6)
- Added specific prompts requesting ALL dates 1-30
- Cross-validated with WebSearch when data looked incomplete

---

## Issue: Jazz Dock and Cross Club pagination not loaded
**Date:** 2025-10-23

- **Context:** WebFetch only returned first page of events, didn't load pagination
- **Failure Type:** Dynamic content loading - JavaScript pagination not accessible to WebFetch

### =Î Proof
- Jazz Dock: Only 6 events (1-4 Nov) returned, expected 8-20
- Cross Club: Only 1 event returned, expected 8-20

### =Ï Rule Added
- `.claude/docs/rules-learned.md`: For clubs with < expected minimum, use WebSearch cross-validation
- Enforcement: Validation report flags clubs below min_akci threshold

### Workaround
- Used WebSearch to find additional events
- Documented in validation report as "yellow clubs" needing attention

---

## Issue: Initial approach lacked systematic validation
**Date:** 2025-10-23

- **Context:** First version generated HTML directly without validation, missed missing events
- **Failure Type:** Process gap - no quality assurance before HTML generation

### =Ï Rule Added
- `.claude/docs/rules-learned.md`: Always run multi-level validation before HTML generation
- Enforcement: 6-level validation workflow documented in kluby.json approach

### Resolution
- Created kluby.json with validation rules per club
- Implemented LEVEL 1-6 validation workflow
- Generated validation report before asking user confirmation

---

## Success: Systematic approach with kluby.json
**Date:** 2025-10-23

- **Context:** Second iteration used structured configuration + validation
- **Result:** 215+ events from 16 clubs, all 30 days covered, Palác Akropolis complete

### Key Improvements
1. Configuration file (kluby.json) with expected ranges per club
2. Parallel WebFetch for all clubs
3. Global date×club matrix analysis
4. Anomaly detection (missing weekends, gaps, low counts)
5. Targeted re-fetch for problematic clubs
6. Cross-validation with WebSearch
7. User confirmation before HTML generation

### Metrics
- Clubs with data: 16/26 (62%)
- Total events: 215+
- Days covered: 30/30 (100%)
- Weekend coverage: 100%
- Palác Akropolis: 27 events including 27-28 Nov 

---

## Decision: Migration from Claude Code WebFetch to Python Beautiful Soup
**Date:** 2025-10-23

- **Context:** HTML generation hit context limits with 215+ events, needed scalable solution
- **Decision Type:** Architectural change - migrate from Claude Code tools to pure Python scraper

### Rationale
- WebFetch approach worked but couldn't scale to full HTML generation
- User preference: "Radsi stravim vic casu na zacatku pripravou celeho workflow, ktery pak bude fungovat spolehlave"
- Python + Beautiful Soup provides full control and no context limits

### Implementation Approach
- **Phase 1:** Proof of concept with Palac Akropolis (historically problematic venue)
- **Phase 2:** Framework with retry logic and HTTP caching
- **Phase 3:** Expand to top 5 clubs with per-club parsers
- **Phase 4:** Unit tests for validation (weekend coverage, Nov 27-28 specifically)
- **Phase 5:** HTML generation from JSON
- **Phase 6:** Documentation and finalization

---

## Discovery: Palac Akropolis events are in static HTML (not JavaScript)
**Date:** 2025-10-23

- **Context:** Initial assumption was JavaScript-rendered content based on WebFetch behavior
- **Discovery:** Events ARE in raw HTML, embedded in <td> table elements

### Proof
- Beautiful Soup found 62 TD elements with November dates
- Pattern: Events in <td> tags with date format "DD. MM" and event_id= links
- Successfully extracted 29 events using static HTML parsing

### Technical Details
```python
# HTML structure discovered:
<td>
  <a href="/work/33298?event_id=39277&no=62&page_id=33824"></a>
  [Date pattern: "01. 11"]
  [Artist name text]
</td>
```

### Implementation
- Created scraper_akropolis.py with Beautiful Soup parser
- Method: Find all <td> tags, match date regex, extract event_id links
- Result: 29 events for November 2025, includes Nov 27-28 PASS

### Validation Results
- **Total events:** 29 (expected range: 15-30)
- **Weekend events:** 13
- **Nov 27:** YES
- **Nov 28:** YES
- **Status:** GREEN
- **Validation:** PASS

---

## Success: Phase 1 - Python Scraper Proof of Concept
**Date:** 2025-10-23

- **Context:** First phase of Python migration complete
- **Result:** Functional scraper for Palac Akropolis with validation

### Deliverables
1. scraper_akropolis.py - Beautiful Soup parser for Palac Akropolis
2. scrape_concerts.py - Main framework with HTTP caching
3. requirements.txt - Dependencies (requests, beautifulsoup4, lxml, requests-cache, pytest)
4. .gitignore - Python/cache file exclusions
5. palac_akropolis_events.json - Output with 29 events

### Key Achievements
- Successfully scraped 29 events (within expected range 15-30)
- Includes Nov 27-28 (historically problematic dates)
- Validation: GREEN status, PASS
- HTTP caching implemented for development efficiency
- Configuration read from kluby.json (month/year parameters)

### Code Quality
- Docstrings for all methods
- Type hints for function signatures
- Proper error handling with try/except
- Duplicate removal by URL
- Sorted output by date

### Next Steps
- Phase 2: Expand framework with retry logic
- Phase 3: Create parsers for top 5 clubs
- Phase 4: Implement comprehensive unit tests

---
