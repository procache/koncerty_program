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

**Workflow:** See `kluby.json` for configuration

1. **WebFetch** all club URLs with month-specific prompts
2. **Validation** against expected ranges (min_akci, max_akci)
3. **Re-fetch** for anomalies (missing weekends, low counts)
4. **Cross-validate** with WebSearch for suspicious results
5. **Report** validation summary to user
6. **Generate** HTML only after user confirms

---

## Data Quality Metrics (listopad 2025)

- **Total events**: 215+
- **Clubs with data**: 16/26 (62%)
- **Days covered**: 30/30 (100%)
- **Weekend coverage**: 100%
- **Validation level**: LEVEL 1-6 complete

---

## Known Limitations

- **Jazz Dock**: Only first 4 days loaded (pagination not accessible)
- **Cross Club**: Only Nov 1 loaded (pagination not accessible)
- **Small cultural centers**: Many don't publish online programs
- **Dynamic content**: JavaScript-loaded events may be missed

---

## Next Month Process

1. Update `kluby.json` → change mesic/rok/pocet_dni
2. Run validation workflow
3. Review validation report
4. Generate HTML
5. Commit with message: `feat: add [mesic] [rok] program`

---
