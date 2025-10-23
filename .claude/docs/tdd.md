# Test-Driven Development (TDD) Workflow

> **Purpose:** Define the default coding methodology for Claude. Other workflow docs (Git, Documentation, Weekly Ritual) reference this process. This file is about **how to work (RED → GREEN → REFACTOR)**, not about every specific test rule — those belong in `rules-learned.md`.

---

## Core Principles
- **TDD is the default.** Claude must always follow RED → GREEN → REFACTOR unless explicitly told otherwise.
- **Pushes & docs only happen on GREEN.** Only when all tests pass may Claude push commits or update documentation.
- **Keep tests behavioral.** Test *what* the code should do, not *how* it is implemented.

---

## The TDD Cycle

### 1. RED – Write Failing Tests
- Always start with tests that describe expected behavior.
- Cover happy path, edge cases, and error scenarios.
- Tests must fail initially.

### 2. GREEN – Implement Minimal Code
- Write the simplest code to make tests pass.
- No extras, no premature optimization.

### 3. REFACTOR – Improve While Staying Green
- Clean up duplication, improve naming, apply conventions.
- Keep tests green at all times.

### 4. VERIFY – Confirm & Extend
- Re-run all tests.
- Add new tests if gaps are discovered.
- Only after this step can docs be updated and commits pushed.

---

## When to Use TDD

| ✅ Use TDD for | ❌ Skip TDD for |
|---------------|----------------|
| New functions or methods | Config file changes |
| API endpoints | Documentation-only changes |
| Business logic | Simple file operations (copying files, static content) |
| Features & bug fixes | UI styling/layout (unless logic involved) |
| Refactoring existing code | Setup/installation scripts |

---

## Communication Pattern
Claude should narrate the workflow in short, structured updates:

```
Starting TDD → Writing failing tests (RED)...
Tests written, now minimal implementation (GREEN)...
All tests passing, refactoring for clarity (REFACTOR)...
Cycle complete ✅
```

---

## Test Writing Guidelines
- Follow **AAA pattern (Arrange, Act, Assert)**.
- Use descriptive names: `should_do_X_when_Y`.
- Include categories: happy path, edge cases, error handling, integration as needed.
- Keep tests reliable and readable.

---

## Relationship to Other Docs
- **Documentation Workflow:** Only update summaries after a GREEN phase at a milestone.
- **Git Workflow:** Commits and pushes must pass the pre-push check (tests green).
- **Weekly Ritual:** Failures captured here feed into `experiment_log.md` and then into `rules-learned.md`.
- **rules-learned.md:** Holds the evolving catalog of specific test patterns (e.g. "always test empty strings").

---

## Net Effect
- Ensures Claude always codes with safety nets.
- Keeps the workflow consistent and predictable.
- Prevents drift by separating **process (this file)** from **rules (rules-learned.md)**.