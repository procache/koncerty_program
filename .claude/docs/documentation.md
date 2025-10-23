# Documentation & Compounding Learning Workflow

> **Purpose:** Keep docs simple, safe, and compounding. Claude only maintains documents — no extra scripts or tooling required.

---

## Principles
- **Docs-first:** CLAUDE.md and summaries are the primary context for Claude.
- **Simplicity:** Only documents, no helper scripts.
- **Safety:** Never document broken or unverified code.
- **Compounding learning:** Every failure turns into a durable rule.

---

## File Layout

- **`CLAUDE.md` (per project)**
  - Imports summaries from `.claude/docs/*.md`.
  - Acts as high-level index + table of contents.

- **`.claude/docs/` (summaries)**
  - `api-summary.md` → short bullets of API endpoints/changes.
  - `components-summary.md` → concise notes on components/modules.
  - `testing-summary.md` → key testing conventions.
  - `deps-summary.md` → bullet list of dependencies added/removed.
  - `rules-learned.md` → distilled lessons imported into CLAUDE.md.

- **`docs/` (canonical deep docs)**
  - `api/openapi.yml` → API spec.
  - `components/*` → detailed component docs.
  - `testing/*` → test playbooks.
  - `infra/*`, `deployment/*` → infrastructure/deployment details.

- **`experiment_log.md`**
  - Raw record of failures and lessons.
  - Periodically archive into `experiment_log/YYYY-QQ.md`.

---

## Documentation Workflow

### 1. Docs Guardrail (before any update)
Claude must only update summaries when:
1. **Tests pass** (or no tests exist yet).
2. **Build succeeds**.
3. **Git status is clean** (no untracked/dirty files).

If any check fails → **STOP, no doc updates.**

### 2. When to Update Summaries
- After a **stabilized milestone**, not every micro-step.
- Example milestones: completed feature slice, API change, bug fix, refactor checkpoint.

### 3. Updating Summaries
- Write short, bulleted notes (< ~5k chars per file).
- Link each bullet back to its canonical source in `/docs` or code.

**Example (`api-summary.md`):**
```
- Added POST /users (password policy enforced) — see docs/api/openapi.yml
- Updated GET /orders with pagination params — see docs/api/openapi.yml
```

**Example (`deps-summary.md`):**
```
- Added joi@^17 for input validation
- Added jest-extended for richer assertions
```

---

## Experiment Log → Rules Learned

### Log Entry Template
```markdown
## Issue: [short title]
- **Context:** what failed (steps, environment)
- **Failure Type:** bug / test gap / misconfig / misunderstanding

### 📎 Proof (Repro Test / Commit)
- commit: <hash> (adds failing test)
- path: tests/<area>/<name>.test.ts

### 📏 Rule Added
- .claude/docs/rules-learned.md: [rule statement]
- enforcement: [test/linter/validator that ensures it]
```

### Rules Learned
- Each new rule is appended to `.claude/docs/rules-learned.md`.
- Keep them short and actionable: *"Always validate empty strings in user input."*

### Weekly Roll-up (manual)
- Once a week, review `experiment_log.md`.
- Curate important rules into `rules-learned.md`.
- If needed, update `CLAUDE_GLOBAL.md` with new universal lessons.

---

## Documentation Quality Standards
- **One Source of Truth per domain:**
  - API → `docs/api/openapi.yml`
  - Components → `docs/components/*`
  - Testing → `docs/testing/*`
  - Rules → `.claude/docs/rules-learned.md`
- **Summaries stay small**: short bullets, links to canonical sources.
- **No duplication**: never repeat full specs in CLAUDE.md.
- **Always actionable**: bullets and rules must guide Claude’s coding.

---

## Communication Pattern
When Claude updates docs, output a compact checklist:
```
Tests ✅ | Build ✅ | Git clean ✅

Scope: [area]
Updating: [api-summary.md, rules-learned.md]
Log entry added: experiment_log.md#<issue>
```
Keeps the history concise and traceable.

---

## Net Effect
- **Simple:** Only documents, no scripts.
- **Safe:** Docs updated only when code is healthy.
- **Compounding:** Failures always become enforceable rules.
- **Fast:** Summaries keep CLAUDE.md lean and performant.
- **Universal:** Works across all projects with the same pattern.