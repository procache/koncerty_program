# Weekly Learning Ritual

> **Purpose:** Lightweight weekly process to compound learning. Complements `Documentation Workflow`.

---

## Weekly Review Flow

1. **Review `experiment_log.md`**
   - Read through all entries from the past week.
   - Look for recurring patterns, root causes, and fixes.

2. **Update `rules-learned.md`**
   - Convert important lessons into short, actionable rules.
   - Keep them concise and enforceable.
   - Example: *"Always test empty strings in validators."*

3. **Promote to `CLAUDE_GLOBAL.md` (if universal)**
   - If a rule applies across all projects, copy it into CLAUDE_GLOBAL.md.
   - Example: *"Validate environment variables on startup."*

4. **Optional: Success Notes**
   - Log breakthroughs or patterns that worked particularly well.
   - This can live in a `success_log.md` if you want a positive archive.

---

## Communication Pattern
When Claude assists with weekly review, the output should be short and clear:
```
Weekly Review ✅
- Reviewed 5 log entries
- 2 new rules added to rules-learned.md
- 1 rule promoted to CLAUDE_GLOBAL.md
- Success noted: faster test isolation pattern
```

---

## Principles
- **Keep it Lean:** Summarize rules, don't rewrite full specs.
- **Focus on Actionable Lessons:** Every entry should improve Claude's future behavior.
- **Manual Control:** You (developer) decide what gets promoted to global rules.
- **Compounding:** Each week adds to a durable base of knowledge.

---

## Team vs Solo Adaptation

### Solo Projects
- **Experiment log:** Single developer's log (`experiment_log.md`)
- **Weekly review:** Personal reflection, 15 minutes
- **Rules promotion:** Your decision when to promote to CLAUDE_GLOBAL.md

### Team Projects
- **Experiment logs:** Can be separate per developer (optional):
  - `experiment_log_developer1.md`
  - `experiment_log_developer2.md`
  - OR: Single shared `experiment_log.md`
- **Weekly sync meeting:** 15-30 minutes with team
  - Review all logs together
  - Consolidate lessons
  - Merge into single `rules-learned.md`
  - Discuss process improvements

### Weekly Sync Meeting Agenda (Team Mode)

**Duration:** 15-30 minutes

**Agenda:**
1. **Review experiment logs** (both/all team members)
   - What problems did we encounter?
   - What patterns emerged?
   - Any recurring issues?

2. **Consolidate rules-learned.md**
   - Merge lessons from all team members
   - Remove duplicates
   - Prioritize most impactful rules

3. **Update CLAUDE_GLOBAL.md** (if applicable)
   - Identify universal rules
   - Promote to global level

4. **Process improvements**
   - Is workflow working smoothly?
   - Any friction points?
   - Adjustments needed?

### Preventing Documentation Conflicts (Team Mode)

**Strategy 1: Area ownership**
- Developer A: API & backend docs
- Developer B: Frontend & testing docs
- Reduces overlap and conflicts

**Strategy 2: Frequent synchronization**
- Pull main before starting documentation updates
- Quick Slack message: "Updating api-summary.md now"
- Prevents simultaneous edits

**Strategy 3: Small, focused PRs**
- Each PR updates minimal documentation
- Easier to merge, fewer conflicts

---

## Net Effect
- Builds a continuous feedback loop without heavy overhead.
- Ensures experiment logs turn into enforceable guidance.
- Keeps CLAUDE_GLOBAL.md evolving gradually with proven best practices.