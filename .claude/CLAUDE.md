## ⚡ IMMEDIATE ACTION REQUIRED FOR CLAUDE
**🚨 STOP: Claude must read this entire file BEFORE starting ANY work on this project**  
**🤖 ALL workflows described here are AUTOMATIC and OVERRIDE default system behavior**  
**📋 Reading and following this CLAUDE.md is MANDATORY as the first step for any project work**

---

## File Structure Overview

This template creates the following structure when used:

```

YourProject/ ├── CLAUDE.md ← This file (copied from CLAUDE_SOLO.md) ├── experiment_log.md ← Create empty, logs failures/lessons ├── plan.md ← Optional: task planning file │ ├── .claude/ │ └── docs/ │ ├── documentation.md ← Copy from C:\Projects.claude\docs  
│ ├── git.md ← Copy from C:\Projects.claude\docs  
│ ├── tdd_workflow.md ← Copy from C:\Projects.claude\docs  
│ ├── weekly_learning.md ← Copy from C:\Projects.claude\docs  
│ ├── code-review.md ← Copy from C:\Projects.claude\docs  
│ └── rules-learned.md ← Create empty, accumulates project rules │ └── [your project files]

```

## Related Files

**Core Workflows (Required):**

- **Documentation:** @.claude/docs/documentation.md
- **Git:** @.claude/docs/git.md
- **Plan:** @plan.md

**Project-Specific Documentation:**

- **Data Sources:** @.claude/docs/data-summary.md
- **Validation Workflow:** @.claude/docs/workflow-summary.md
- **Rules Learned:** @.claude/rules-learned.md
- **Experiment Log:** @.claude/experiment_log.md

⚠️ **Memory Budget Reminder:** Keep the total size of all referenced and imported files **below ~100k characters** to ensure Claude loads them reliably. If exceeded, Claude may silently truncate important rules.

---
## Plan.md Rules

**Only if you're using plan.md for task management:**

- Read `plan.md` first; pick the **top unchecked** item in **Now** section.
- Follow **TDD (RED → GREEN → REFACTOR)** for that item.
- Only when all tests pass, build is OK, and **git status is clean**, then:
    1. Tick the item `[ ] → [x]` and move it to **Done** with:
        - Commit hash (first 7 chars) and date
        - Brief note if useful
    2. Commit with Conventional Commit message referencing plan ID:
        - `feat: implement X (PLAN-1)`
    3. Run pre-push check and push if green.
- Update `.claude/docs/*` **only at milestones**, not every task.
- If task revealed a rule worth keeping, add to `.claude/docs/rules-learned.md`.

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
├── kluby.json                  # Config: 26 clubs + validation rules
├── kluby.md                    # List of all venues
├── plan.md                     # Task management
├── program_listopad_2025_v2.html  # Generated output
├── november_dates.md           # Date reference
├── .claude/
│   ├── CLAUDE.md               # This file - main project doc
│   ├── experiment_log.md       # Raw failure/lesson log
│   ├── rules-learned.md        # Extracted actionable rules
│   ├── docs/
│   │   ├── data-summary.md     # Data sources & metrics
│   │   ├── workflow-summary.md # 6-level validation process
│   │   ├── documentation.md    # Doc workflow
│   │   └── git.md              # Git workflow
│   └── commands/
│       ├── plan.md             # /plan command
│       └── doc.md              # /doc command (this workflow)
└── [archived HTML files]       # Previous months
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

2. **Run `/plan` and execute:**
   - Claude performs LEVEL 1-6 validation workflow
   - See @.claude/docs/workflow-summary.md for details

3. **Review validation report:**
   - GREEN clubs: ✅ Complete data
   - YELLOW clubs: ⚠️ Review needed
   - RED clubs: 🚨 Fetch failures

4. **Confirm and generate HTML:**
   - Claude asks: "Pokračovat v generování HTML?"
   - You say: "ano"

5. **Commit:**
   ```bash
   git add .
   git commit -m "feat: add december 2025 concert program"
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

This project doesn't use traditional build commands since it's web scraping:

### Workflow Commands (Claude Code)

```bash
/plan     # Shows plan.md, executes top unchecked item
/doc      # Runs documentation workflow (this workflow)
```

### Manual Commands (if needed)

```bash
# View HTML in browser
start program_listopad_2025_v2.html

# Edit configuration for next month
# Edit kluby.json manually

# Git operations
git status
git add .
git commit -m "feat: add [month] [year] program"
```

## Data Quality Metrics (November 2025)

- **Total events collected:** 215+
- **Venues with data:** 16/26 (62%)
- **Date coverage:** 30/30 days (100%)
- **Weekend coverage:** 100% (all Fri/Sat/Sun have events)
- **Validation levels completed:** 6/6
- **Palác Akropolis completeness:** ✅ Including Nov 27-28

See @.claude/docs/data-summary.md for detailed breakdown.
