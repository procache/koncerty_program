# Workflow Summary - Koncerty Program

> Concise notes on the systematic data collection and validation workflow.

---

## 6-Level Validation Workflow

### LEVEL 1: Parallel WebFetch
- **Action**: Fetch all clubs simultaneously (26 WebFetch calls in parallel)
- **Config**: kluby.json defines URLs and expected ranges
- **Prompt**: "Extract ALL music concerts for [month] [year]. List EVERY date 1-[days]."
- **URL requirement**: "For each event, provide the direct event detail page URL (NOT the venue program page)"

### LEVEL 2: Global Analysis
- **Action**: Create date×club matrix for entire month
- **Check**: Every day 1-30 has at least 1 event
- **Output**: Aggregate statistics (total events, clubs with data)

### LEVEL 3: Anomaly Detection
**Checks:**
- actualEvents < min_akci → YELLOW flag
- actualEvents < min_akci * 0.5 → RED flag
- Large venue missing weekends → YELLOW flag
- Gap > 5 days for large venue → YELLOW flag
- **URL quality:** Event URL = venue program page → YELLOW flag (use ticket_sources)

### LEVEL 4: Targeted Re-fetch
- **Trigger**: YELLOW or RED flags from LEVEL 3
- **Action**: Re-fetch with explicit date prompts
- **Example**: "Show me ONLY events on November 27 and 28"
- **URL fallback**: If venue has no event URLs, check `ticket_sources` from kluby.json

### LEVEL 5: Cross-validation
- **Trigger**: Still suspicious after re-fetch
- **Action**: WebSearch for "[Club] program [month] [year]"
- **Compare**: Search results vs WebFetch results

### LEVEL 6: Validation Report
- **Generate**: Color-coded report (GREEN/YELLOW/RED clubs)
- **Include**: Statistics, anomalies, questions for user
- **Ask**: User confirmation before HTML generation

---

## Monthly Workflow (for new month)

```bash
# 1. Update configuration
# Edit kluby.json: mesic, rok, pocet_dni

# 2. Run scraping (Claude does this)
# - LEVEL 1-6 validation
# - Generate report

# 3. Review report
# - Check YELLOW/RED clubs
# - Confirm or request manual fixes

# 4. Generate HTML
# - Only after user says "yes"

# 5. Commit
git add .
git commit -m "feat: add [month] [year] concert program"
git push
```

---

## File Structure

```
koncerty_program/
├── kluby.json              ← Config: clubs + validation rules
├── program_[month]_[year].html  ← Output
├── .claude/
│   ├── CLAUDE.md           ← Main project doc
│   ├── experiment_log.md   ← Failures log
│   ├── rules-learned.md    ← Extracted rules
│   └── docs/
│       ├── data-summary.md      ← Data sources
│       ├── workflow-summary.md  ← This file
│       └── ...
```

---

## URL Sources Configuration

Some venues don't provide event-specific URLs. Use `ticket_sources` fallback:

```json
{
  "nazev": "Buena Vista Club",
  "url": "https://www.buenavistaclub.cz/program-klubu.aspx",
  "ticket_sources": [
    "https://www.smsticket.cz/misto/buena-vista-plzen",
    "https://goout.net/cs/buena-vista-club/vzptfs/"
  ]
}
```

**URL priority (best to worst):**
1. Venue's own event detail page
2. Ticket platform (smsticket.cz, goout.net)
3. Band's official concert page
4. Event aggregator (kdykde.cz, bandzone.cz)
5. Facebook event page
6. ❌ NEVER: Generic venue program page

---

## Key Commands

**Read configuration:**
```javascript
const config = require('./kluby.json');
const { mesic, rok, kluby } = config;
```

**Validation template:**
```javascript
const isGreen = actualEvents >= venue.min_akci;
const isYellow = actualEvents >= venue.min_akci * 0.5 && actualEvents < venue.min_akci;
const isRed = actualEvents < venue.min_akci * 0.5;
```

---

## Output Format (HTML)

**Features:**
- Responsive design with gradient background
- Filter by city (Praha/Plzeň)
- Search by artist/venue name
- Color-coded tags (VYPRODÁNO, ODLOŽENO)
- Direct links to official event pages
- Statistics per day (event count)

**Technologies:**
- Pure HTML/CSS/JavaScript
- No build step required
- Works in any modern browser

---

## Lessons Learned Integration

Every issue becomes a rule:
1. **Document** in `experiment_log.md` (what happened, why, proof)
2. **Extract** rule to `rules-learned.md` (actionable statement)
3. **Enforce** via validation checks in workflow
4. **Reference** in `CLAUDE.md` for future work

See: `.claude/docs/rules-learned.md` for current rules.

---
