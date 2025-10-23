# Plan

> Claude executes tasks from here. Update by ticking `[ ] → [x]` when complete.  
> Claude may only tick after GREEN (tests/build pass, git clean).


## Overall

Připrav program českých hudebních klubů, jejichž seznam je v souboru kluby.md. Všechny úkoly jsou v seznamu v sekci Now. Zajímá mě program na listopad 2025. Vytvoř jednoduchou HTML stránku, kde budou seřazené hudební akce podle datumu. U každé akce bude odkaz na její URL a to, jestli se to koná v Praze nebo Plzni. Pro každé datum budou uvedené akce ve všech klubech, kde se něco koná. Zajímá mě jenom hudba, ne divadlo ani sportovní akce.

## Now - Python Scraper Implementation

### Phase 1: Proof of Concept - Palác Akropolis
[x] Analyze Palác Akropolis HTML structure (events in <td> elements)
[x] Create scraper_akropolis.py with Beautiful Soup parser
[x] Extract events with: date, time, artist, venue, URL
[x] Test on November 2025 data
[x] Validate: 29 events including Nov 27-28 ✓ GREEN STATUS
[x] Save output to palac_akropolis_events.json

### Phase 2: Framework & Configuration
[x] Create requirements.txt (requests, beautifulsoup4, lxml, requests-cache, pytest)
[x] Create scrape_concerts.py main framework with caching
[x] Add retry strategy (attempt other clubs first, log failures)
[x] Read month/year from kluby.json config (already in place)
[x] Create base scraper class for code reuse

### Phase 3: Parser Expansion
[ ] Create parsers for top 5 clubs (Rock Café, Roxy, Lucerna Music Bar, Forum Karlín, O2 Arena)
[ ] Implement per-club parser architecture in scrape_concerts.py
[ ] Add validation: weekend coverage, URL completeness, date ranges
[ ] Generate events_data.json with all club data

### Phase 4: Unit Testing
[ ] Create test_scraper.py
[ ] Test weekend coverage for large venues (min 2 events on Fri/Sat)
[ ] Test Nov 27-28 specifically (historically problematic dates)
[ ] Test URL validity (all URLs start with https://)
[ ] Test date/time format validation
[ ] Test retry/error logging

### Phase 5: HTML Generation
[ ] Create generate_html.py
[ ] Read events_data.json
[ ] Generate complete HTML (no context limits)
[ ] Add filtering by city (Praha/Plzeň)
[ ] Add search functionality
[ ] Add responsive design with gradient background

### Phase 6: Documentation & Commit
[ ] Update README.md with usage instructions
[ ] Document parser patterns in .claude/docs/parser-patterns.md
[ ] Test full workflow end-to-end (scrape → validate → HTML)
[ ] Run `/doc` workflow to update experiment_log.md and rules-learned.md
[ ] Commit: "feat: implement python scraper with beautiful soup"


## Done
<!-[ ]Claude moves completed items here with commit hash + date -->
[x] 001: 