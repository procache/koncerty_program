# Rules Learned - Koncerty Program

> Distilled lessons from experiment_log.md - actionable rules for future development.

---

## Web Scraping & Data Collection

### Rule: Always validate weekend day coverage for large venues
**Why:** Large clubs (Pal·c Akropolis, Rock CafÈ, Roxy) typically have events on Fridays and Saturdays. Missing weekend days indicates incomplete data.

**Enforcement:**
- Check: If large venue (min_akci >= 15) has < 2 weekend events in month í flag for re-fetch
- Validation: LEVEL 3 anomaly detection in workflow

**Example:**
```javascript
if (venue.velikost === "velky" && weekendEvents < 2) {
  console.warn(`† ${venue.nazev}: Only ${weekendEvents} weekend events - possible incomplete data`);
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
- LEVEL 2: Global analysis (date◊club matrix)
- LEVEL 3: Detect anomalies (min thresholds, weekend gaps, date gaps)
- LEVEL 4: Targeted re-fetch for flagged clubs
- LEVEL 5: Cross-validate with WebSearch
- LEVEL 6: Generate validation report í get user confirmation

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
WebFetch: Jazz Dock í 6 events (only 1-4 Nov)
WebSearch: "Jazz Dock Praha program listopad 2025" í mentions events on 16, 21, 24, 28 Nov
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
    console.error(`=® Day ${day}: ZERO events - data incomplete`);
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
  "mesic": "prosinec",      // ê Change this
  "mesic_en": "December",   // ê Change this
  "rok": 2025,              // ê Keep same (or update)
  "mesic_cislo": 12,        // ê Change this
  "pocet_dni": 31           // ê Update days in month
}
```

---

### Rule: Generate validation report before user confirmation
**Why:** User needs transparency about data quality before final HTML.

**Report must include:**
-  GREEN clubs: Complete data
- † YELLOW clubs: Possible gaps
- =® RED clubs: Fetch failures
- =  Global statistics: total events, day coverage
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
