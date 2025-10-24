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

**📅 Session Status (2025-10-24):**
- ✅ Completed today: Watt Music Club, O2 Arena (filters sports), O2 Universum, Plan restructuring
- ⏸️ Deferred (4): U Staré Paní (website down), Lucerna Velký sál (no events), Cross Club (complex JS), Sportovní hala Fortuna (complex carousel)
- 📊 Progress: **13/26 venues (50%)**, 251 events (+15 new)
- 🎯 Remaining: **13 venues** to implement
- 💾 Git: Ready to commit O2 venues implementation
- 🔄 Next priorities: Small Prague venues (Divadlo Pod lampou, KD Šeříkovka, KD JAS), Plzeň venues

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
[x] Implement Watt Music Club Playwright scraper (GoOut source, 3 events ✅)
[x] Test full automated run: 11/26 venues without Claude ✅
[x] Implement O2 Arena Playwright scraper (filters sports, 7 events ✅)
[x] Implement O2 Universum Playwright scraper (8 events ✅)
[x] Test full automated run: 13/26 venues without Claude ✅

**Current Status - 13/26 FULLY AUTOMATED (50% complete):**
- ✅ **O2 Arena** (7 events) - Playwright + Sports Filter - **AUTOMATED**
- ✅ **O2 Universum** (8 events) - Playwright - **AUTOMATED**
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
- ✅ **Watt Music Club** (3 events) - Playwright (GoOut) - **AUTOMATED**

**Total: 251 events from 13 venues**

---

### Phase 4: Complete All 26 Venues (GRADUAL IMPLEMENTATION) ⚠️ CRITICAL

**Target:** 300+ events from all 26 venues, fully automated

**Progress: 13/26 venues implemented (50%)**

**Status Overview:**
```
✅ Implemented (13):  O2 Arena, O2 Universum, Palác Akropolis, Rock Café,
                      Lucerna Music Bar, Roxy, Vagon, Jazz Dock, Forum Karlín,
                      MeetFactory, Malostranská beseda, Reduta Jazz Club,
                      Watt Music Club

⏸️ Deferred (4):     Cross Club, Lucerna Velký sál, U Staré Paní,
                     Sportovní hala Fortuna

❌ Not Started (9):  Divadlo Pod lampou, KD Šeříkovka, KD JAS,
                     Buena Vista Club, Dům hudby Plzeň, Moving Station,
                     Papírna Plzeň, Měšťanská beseda, LOGSPEED CZ Aréna
```

**Remaining venues to implement (13):**

**Priority 1: Large Prague venues (high event count)**
[x] O2 Arena (4-15 expected) - music only, filter out sports - Playwright ✅ 7 events
[x] O2 Universum (3-10 expected) - Playwright ✅ 8 events
[ ] Sportovní hala Fortuna (2-8 expected) - DEFERRED (complex Splide carousel structure)

**Priority 2: Deferred venues (retry with alternative approaches)**
[ ] Cross Club (8-20 expected) - DEFERRED (complex JavaScript calendar) - Playwright
[ ] Lucerna Velký sál (8-20 expected) - DEFERRED (no November events found) - Playwright
[ ] U Staré Paní Jazz & Cocktail Club (5-15 expected) - DEFERRED (website unreachable) - try GoOut

**Priority 3: Small Prague venues**
[ ] Divadlo Pod lampou (0-5 expected) - primarily theatre, occasional music - Playwright
[ ] Kulturní dům Šeříkovka (1-8 expected) - Playwright
[ ] Kulturní dům JAS (1-8 expected) - Playwright

**Priority 4: Plzeň venues**
[ ] Buena Vista Club (3-10 expected) - Playwright
[ ] Dům hudby Plzeň (2-10 expected) - Playwright
[ ] Moving Station (2-10 expected) - filter out theatre/film, music only - Playwright
[ ] Papírna Plzeň (1-8 expected) - Playwright
[ ] Měšťanská beseda (3-12 expected) - filter out theatre - Playwright
[ ] LOGSPEED CZ Aréna (0-5 expected) - primarily hockey, occasional music - Playwright

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
[x] Phase 3: Playwright-based automation framework (11 venues completed)

### Completed Venues (13/26 - 50% complete) ✅

**Prague venues (12):**
[x] O2 Arena - Playwright + Sports Filter (7 events) - **filters hockey/FMX**
[x] O2 Universum - Playwright (8 events)
[x] Palác Akropolis - Beautiful Soup (29 events)
[x] Rock Café - Playwright (23 events)
[x] Lucerna Music Bar - Playwright (31 events)
[x] Roxy - Playwright (25 events)
[x] Vagon - Playwright (26 events)
[x] Jazz Dock - Playwright (20 events)
[x] Forum Karlín - Playwright (6 events)
[x] MeetFactory - Playwright + Infinite Scroll (15 events)
[x] Malostranská beseda - Playwright (28 events)
[x] Reduta Jazz Club - Playwright (30 events)

**Plzeň venues (1):**
[x] Watt Music Club - Playwright via GoOut (3 events)

**Total: 251 events from 13 fully automated venues** 