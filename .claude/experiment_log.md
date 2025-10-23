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
