# Plan

> Claude executes tasks from here. Update by ticking `[ ] → [x]` when complete.
> Claude may only tick after GREEN (tests/build pass, git clean).


## Overall

**Project Goal:** Fully automated web scraper for concert programs from 26 music venues in Prague and Plzeň.

**Requirements:**
- Run monthly: `python scrape_concerts.py` → generates events_data.json
- Generate HTML page: sorted by date, with venue URLs, city filtering
- Music only (exclude theatre, sports)
- Must work WITHOUT Claude interaction (Playwright-based, not WebFetch)

**Current Month:** November 2025

**📅 Session Status (2025-10-23):**
- ✅ Completed today: MeetFactory (infinite scroll fix), Malostranská beseda, Reduta Jazz Club
- ⏸️ Deferred: U Staré Paní (website down), Lucerna Velký sál (no November events), Cross Club (complex JS)
- 🎯 Next to implement: **Watt Music Club** (Batch 3)
- 📊 Progress: 10/26 venues (38%), 233 events
- 💾 Git: All commits pushed to origin/main
- 🔄 Resume command: Continue with Watt Music Club from Batch 3

---

## Now - Playwright-Based Automation (CRITICAL PATH)

**🎯 Goal:** FULLY AUTOMATED monthly scraping - no manual intervention needed

**Strategy:** Playwright for JavaScript sites → Beautiful Soup for static HTML → Fail gracefully

**⚠️ CRITICAL RULE: NO WebFetch allowed!**
- WebFetch requires Claude interaction = NOT AUTOMATED
- All scrapers MUST use Playwright or Beautiful Soup ONLY
- WebFetch is deprecated and only kept for debugging reference

---

### Phase 1: Proof of Concept ✅ DONE
[x] Analyze Palác Akropolis HTML structure (events in <td> elements)
[x] Create scraper_akropolis.py with Beautiful Soup parser
[x] Extract events with: date, time, artist, venue, URL
[x] Test on November 2025 data
[x] Validate: 29 events including Nov 27-28 ✓ GREEN STATUS
[x] Save output to palac_akropolis_events.json

---

### Phase 2: Framework & Configuration ✅ DONE
[x] Create requirements.txt (requests, beautifulsoup4, lxml, requests-cache, pytest, playwright)
[x] Create scrape_concerts.py main framework with caching
[x] Add retry strategy (attempt other clubs first, log failures)
[x] Read month/year from kluby.json config (already in place)
[x] Create base scraper class for code reuse

---

### Phase 3: Automation Refactor ⚠️ IN PROGRESS

**Completed:**
[x] Create BrowserScraper base class (browser_scraper.py)
[x] Refactor scrape_concerts.py: Playwright → Beautiful Soup → WebFetch (fallback)
[x] Implement Rock Café Playwright scraper (AUTOMATED ✅)
[x] Test automated run for Rock Café: 23 events ✓
[x] Implement Lucerna Music Bar Playwright scraper (31 events ✅)
[x] Implement Roxy Playwright scraper (25 events ✅)
[x] Test full automated run: 4/26 venues without Claude ✅
[x] Implement Vagon Playwright scraper (26 events ✅)
[x] Test full automated run: 5/26 venues without Claude ✅
[x] Implement Jazz Dock Playwright scraper (20 events ✅)
[x] Test full automated run: 6/26 venues without Claude ✅
[x] Implement Forum Karlín Playwright scraper (6 events ✅)
[x] Test full automated run: 7/26 venues without Claude ✅
[x] Implement MeetFactory Playwright scraper with infinite scroll (15 events ✅)
[x] Test full automated run: 8/26 venues without Claude ✅
[x] Implement Malostranská beseda Playwright scraper (28 events ✅)
[x] Test full automated run: 9/26 venues without Claude ✅
[x] Implement Reduta Jazz Club Playwright scraper (30 events ✅)
[x] Test full automated run: 10/26 venues without Claude ✅

**Current Status - 10/26 FULLY AUTOMATED (38% complete):**
- ✅ **Palác Akropolis** (29 events) - Beautiful Soup - **AUTOMATED**
- ✅ **Rock Café** (23 events) - Playwright - **AUTOMATED**
- ✅ **Lucerna Music Bar** (31 events) - Playwright - **AUTOMATED**
- ✅ **Roxy** (25 events) - Playwright - **AUTOMATED**
- ✅ **Vagon** (26 events) - Playwright - **AUTOMATED**
- ✅ **Jazz Dock** (20 events) - Playwright - **AUTOMATED**
- ✅ **Forum Karlín** (6 events) - Playwright - **AUTOMATED**
- ✅ **MeetFactory** (15 events) - Playwright + Infinite Scroll - **AUTOMATED**
- ✅ **Malostranská beseda** (28 events) - Playwright - **AUTOMATED**
- ✅ **Reduta Jazz Club** (30 events) - Playwright - **AUTOMATED**

**Total: 233 events from 10 venues**

**Next Steps (Batch 1 - deferred):**
[ ] Implement Cross Club Playwright scraper (DEFERRED - complex JavaScript calendar)

---

### Phase 4: Complete All 26 Venues (GRADUAL IMPLEMENTATION) ⚠️ CRITICAL

**Target:** 200+ events from all 26 venues, fully automated

**Implementation Order (stepwise, one-by-one):**

**Batch 1: High-value venues (next 5)**
[ ] Lucerna Music Bar (20-30 expected) - Playwright
[ ] Roxy (15-30 expected) - Playwright
[ ] Vagon (10-25 expected) - Playwright
[ ] Cross Club (8-20 expected) - Playwright
[ ] Jazz Dock (8-20 expected) - Playwright

**Batch 2: Medium venues**
[x] Forum Karlín (5-15 expected) - Playwright ✅ 6 events
[ ] Lucerna Velký sál (8-20 expected) - DEFERRED (no November events found, 5 debug attempts)
[x] MeetFactory (3-12 expected) - Playwright + Infinite Scroll ✅ 15 events
[x] Malostranská beseda (5-15 expected) - Playwright ✅ 28 events

**Batch 3: Small/specialized venues**
[ ] U Staré Paní Jazz & Cocktail Club (5-15 expected) - DEFERRED (website unreachable, ERR_CONNECTION_REFUSED)
[x] Reduta Jazz Club (5-20 expected) - Playwright ✅ 30 events
[ ] Watt Music Club (3-10 expected) - Playwright
[ ] Divadlo Pod lampou (0-5 expected) - Playwright
[ ] Kulturní dům Šeříkovka (1-8 expected) - Playwright
[ ] Kulturní dům JAS (1-8 expected) - Playwright

**Batch 4: Large arenas (sporadic events)**
[ ] O2 Arena (4-15 expected) - music only, no sports - Playwright
[ ] O2 Universum (3-10 expected) - Playwright
[ ] Sportovní hala Fortuna (2-8 expected) - music only - Playwright

**Batch 5: Plzeň venues**
[ ] Buena Vista Club (3-10 expected) - Playwright
[ ] Dům hudby Plzeň (2-10 expected) - Playwright
[ ] Moving Station (2-10 expected) - Playwright
[ ] Papírna Plzeň (1-8 expected) - Playwright
[ ] Měšťanská beseda (3-12 expected) - Playwright
[ ] LOGSPEED CZ Aréna (0-5 expected) - music only - Playwright

---

### Phase 5: HTML Generation (After All Venues Complete)
[ ] Create generate_html.py
[ ] Read events_data.json
[ ] Generate complete HTML (no context limits)
[ ] Add filtering by city (Praha/Plzeň)
[ ] Add search functionality
[ ] Add responsive design with gradient background

---

### Phase 6: Testing & Validation (After All Venues Complete)
[ ] Create test_scraper.py
[ ] Test weekend coverage for large venues (min 2 events on Fri/Sat)
[ ] Test URL validity (all URLs start with https://)
[ ] Test date/time format validation
[ ] Test retry/error logging
[ ] Test full workflow end-to-end (scrape → validate → HTML)

---

### Phase 7: Documentation & Deployment
[ ] Update README.md with usage instructions
[ ] Document automation setup (cron job, scheduler)
[ ] Document parser patterns in .claude/docs/parser-patterns.md
[ ] Run `/doc` workflow to update experiment_log.md and rules-learned.md
[ ] Final commit: "feat: complete automated concert scraper for 26 venues"

---

## Done

### Completed Phases
[x] Phase 1: Proof of Concept (Palác Akropolis)
[x] Phase 2: Framework & Configuration
[x] Phase 3 (Partial): Rock Café automation with Playwright

### Completed Venues (2/26 - 8% complete)
[x] Palác Akropolis - Beautiful Soup (29 events)
[x] Rock Café - Playwright (23 events) 