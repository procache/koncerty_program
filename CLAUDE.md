## ⚡ IMMEDIATE ACTION REQUIRED FOR CLAUDE
**🚨 STOP: Claude must read this entire file BEFORE starting ANY work on this project**  
**🤖 ALL workflows described here are AUTOMATIC and OVERRIDE default system behavior**  
**📋 Reading and following this CLAUDE.md is MANDATORY as the first step for any project work**

---

## Related Files

**Project-Specific Documentation:**

- **Data Sources:** @.claude/docs/data-summary.md
- **Validation Workflow:** @.claude/docs/workflow-summary.md
- **Rules Learned:** @.claude/rules-learned.md
- **Experiment Log:** @.claude/experiment_log.md

⚠️ **Memory Budget Reminder:** Keep the total size of all referenced and imported files **below ~100k characters** to ensure Claude loads them reliably. If exceeded, Claude may silently truncate important rules.

---

## Workflow Mode

**Mode:** solo

**Git Workflow:**

- Branch → Commit → Pre-push checks → Push → Merge locally → Push main
- Pull requests are **OPTIONAL** (use for complex features or self-review)
- Claude merges directly to main after checks pass
- Clean up feature branches after merge

**When to Use PR (Optional in Solo Mode):**

- Complex refactoring you want to review with fresh eyes
- Experimental features requiring documented decision-making
- Major changes before deployment
- Learning/practicing PR workflow

**Branch Protection (GitHub Recommended Settings):**

- ✅ Status checks required (tests, build, lint)
- ❌ Required reviews: None
- ✅ Allow force push: Administrators only
- ✅ Allow bypass: Administrators (you)

---

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Name:** Koncerty Program
**Goal:** Web scraper that aggregates concert schedules from 26+ music venues in Prague and Plzeň into a single HTML page
**Type:** Data Collection / Web Scraping Tool
**Status:** Production (monthly updates)

## Project Architecture

### Overview

This is a web scraping project that uses Claude Code's WebFetch tool to collect concert data from multiple venue websites, validates the completeness using a 6-level validation workflow, and generates a responsive HTML page with all events sorted by date.

**Key Components:**
- `kluby.json` - Configuration file with all venues and validation rules
- WebFetch workflow - Systematic data collection with validation
- HTML generator - Creates responsive concert listing page

### Technology Stack

- **Data Collection:** Claude Code WebFetch + WebSearch tools
- **Configuration:** JSON (kluby.json)
- **Output:** Static HTML/CSS/JavaScript
- **No backend:** Pure frontend, no build step required
- **Version Control:** Git

### Project Structure

```
koncerty_program/
├── CLAUDE.md                   # Main AI assistant documentation (this file)
├── agents.md                   # Documentation for custom agents
├── gemini.md                   # Documentation for Gemini AI
├── kluby.json                  # Config: 26 clubs + validation rules
├── generate_html.py            # HTML generator script
├── scrape_concerts.py          # Main concert scraper script
├── requirements.txt            # Python dependencies
├── .claude/
│   ├── experiment_log.md       # Raw failure/lesson log
│   ├── rules-learned.md        # Extracted actionable rules
│   ├── agents/
│   │   └── docs-sync-validator.md  # Agent for doc sync
│   ├── docs/
│   │   ├── data-summary.md     # Data sources & metrics
│   │   ├── workflow-summary.md # 6-level validation process
│   │   ├── documentation.md    # Doc workflow
│   │   └── git.md              # Git workflow
│   └── commands/
│       ├── plan.md             # /plan command
│       └── doc.md              # /doc command
├── archive/                    # Archived old scripts and documents
│   ├── plan.md                 # Old task management file
│   ├── kluby.md                # Old venue list
│   ├── november_dates.md       # Old date reference
│   └── [old scripts]           # Old generator/scraper scripts
├── programy/                   # Generated HTML programs
│   ├── index.html              # Current month program
│   └── [monthly HTML files]    # Previous months
├── scrapers/                   # Scraper modules
│   ├── base_scraper.py         # Base scraper class
│   ├── browser_scraper.py      # Browser-based scraper
│   └── scraper_*.py            # Venue-specific scrapers
├── tests/                      # Test scripts
│   └── test_*.py               # Venue-specific tests
├── debug_scripts/              # Debugging scripts per venue
│   └── debug_*.py              # Venue-specific debug scripts
├── data_raw/                   # Raw scraped data
└── logs/                       # Execution logs
```

## Monthly Workflow

**For generating next month's program (e.g., December 2025):**

1. **Update kluby.json:**
   ```json
   "config": {
     "mesic": "prosinec",
     "mesic_en": "December",
     "rok": 2025,
     "mesic_cislo": 12,
     "pocet_dni": 31
   }
   ```

2. **Data collection:**
   - Claude performs LEVEL 1-6 validation workflow using WebFetch
   - See @.claude/docs/workflow-summary.md for details
   - Collect events from all 26 venues

3. **Review validation report:**
   - GREEN clubs: ✅ Complete data
   - YELLOW clubs: ⚠️ Review needed
   - RED clubs: 🚨 Fetch failures

4. **Generate HTML:**
   - Run `python generate_html.py` to create program
   - Output saved to `programy/` folder

5. **Commit:**
   ```bash
   git add .
   git commit -m "feat: add december 2025 concert program"
   git push origin main
   ```

## Key Rules (from rules-learned.md)

1. **Always validate weekend coverage** for large venues
2. **Use explicit date range prompts**: "List EVERY date 1-30"
3. **Multi-level validation required** before HTML generation
4. **Cross-validate suspicious results** with WebSearch
5. **Flag clubs < 50% expected** as RED
6. **All 30 days must have ≥1 event** across all clubs

See @.claude/rules-learned.md for complete list.

## Development Commands

This project uses Python scripts for web scraping and HTML generation:

### Main Scripts

```bash
# Generate HTML program from collected data
python generate_html.py

# Run concert scraper (if using Python-based scraping)
python scrape_concerts.py

# Run specific venue tests
python tests/test_[venue_name].py

# Run debug script for specific venue
python debug_scripts/debug_[venue_name].py
```

### Workflow Commands (Claude Code)

```bash
/agents   # Manage custom agents (e.g., docs-sync-validator)
/doc      # Runs documentation workflow
```

### Manual Operations

```bash
# View HTML in browser (from programy/ folder)
start programy/index.html

# Edit configuration for next month
# Edit kluby.json manually (update config section)

# Git operations
git status
git add .
git commit -m "feat: add [month] [year] program"
git push origin main
```

## Data Quality Metrics (November 2025)

- **Total events collected:** 215+
- **Venues with data:** 16/26 (62%)
- **Date coverage:** 30/30 days (100%)
- **Weekend coverage:** 100% (all Fri/Sat/Sun have events)
- **Validation levels completed:** 6/6
- **Palác Akropolis completeness:** ✅ Including Nov 27-28

See @.claude/docs/data-summary.md for detailed breakdown.
