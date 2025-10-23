# Data Summary - Koncerty Program

> Concise notes on data sources and collection methods.

---

## Data Sources (listopad 2025)

### Praha - Major Venues (✅ Complete)
- **O2 Arena**: 6 events → https://www.o2arena.cz/en/events/
- **O2 Universum**: 4 events → https://www.o2universum.cz/en/events/
- **Sportovní hala Fortuna**: 5 events → https://www.sportovnihalafortuna.cz/
- **Forum Karlín**: 6 events → https://www.forumkarlin.cz/en/events/
- **Palác Akropolis**: 27 events ✓ → https://palacakropolis.cz/
- **Lucerna Velký sál**: 14 events → https://www.lucpra.com/
- **Roxy**: 25 events → https://www.roxy.cz/tickets/
- **Lucerna Music Bar**: 30+ events → https://musicbar.cz/en/program/
- **Rock Café**: 21 events → https://rockcafe.cz/en/program/

### Praha - Medium/Small Venues (✅ Partial)
- **MeetFactory**: 5 events → https://meetfactory.cz/en/program/hudba
- **Vagon**: 24 events → https://www.vagon.cz/next.php
- **Reduta Jazz Club**: 17+ events → https://www.redutajazzclub.cz/program
- **Malostranská beseda**: 5 events → https://www.malostranska-beseda.cz/club/program

### Praha - Jazz Clubs (⚠️ Incomplete)
- **Jazz Dock**: 6 events (pagination issue) → https://www.jazzdock.cz/en/program
- **Cross Club**: 1 event (pagination issue) → https://www.crossclub.cz/cs/program/

### Plzeň (✅ Partial)
- **Buena Vista Club**: 4 events → https://www.buenavistaclub.cz/program-klubu.aspx
- **Měšťanská beseda**: Web error (404)

---

## Collection Method

**Automated Scraping Strategy:** See `scrape_concerts.py` and `browser_scraper.py`

1. **Playwright** for JavaScript-heavy sites (fully automated) → see browser_scraper.py
2. **Beautiful Soup** for static HTML sites (fully automated) → see scraper_akropolis.py
3. **Validation** against expected ranges (min_akci, max_akci in kluby.json)
4. **Retry** failed venues once
5. **Report** validation summary (GREEN/YELLOW/RED status)

**⚠️ WebFetch Deprecated:** WebFetch requires Claude interaction = NOT AUTOMATED. Only kept for debugging.

---

## Data Quality Metrics (listopad 2025) - Automated Run

- **Total events**: 154 (from 6/26 venues)
- **Venues automated**: 6/26 (23%)
  - Palác Akropolis: 29 events (Beautiful Soup)
  - Rock Café: 23 events (Playwright)
  - Lucerna Music Bar: 31 events (Playwright)
  - Roxy: 25 events (Playwright)
  - Vagon: 26 events (Playwright)
  - Jazz Dock: 20 events (Playwright)
- **All venues**: GREEN status ✅
- **Automation goal**: 26/26 venues without Claude interaction

---

## Known Limitations

- **Cross Club**: Deferred - complex JavaScript calendar requires advanced Playwright (click dates, wait AJAX)
- **Remaining 20 venues**: Not yet implemented (gradual rollout per plan.md)
- **No runtime errors**: System gracefully skips unimplemented scrapers

---

## Next Month Process

1. Update `kluby.json` → change mesic/rok/pocet_dni
2. Run validation workflow
3. Review validation report
4. Generate HTML
5. Commit with message: `feat: add [mesic] [rok] program`

---
