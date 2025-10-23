# Solo Git Workflow

> **Purpose:** Simple, safe, universal Git process for a solo developer. Designed to be imported into `CLAUDE.md`. No team/PR overhead by default.

---

## Principles
- Keep history **clean and recoverable**.
- Push **after important milestones** only, never broken code to `main`.
- Prefer clarity over automation that can surprise you.

> **Claude:** Follow this document exactly. If any safety check fails, **stop and ask**.

---

## Project Mode Detection

Claude automatically detects the workflow mode from the project's `CLAUDE.md` file:

**Solo Mode:**
```markdown
## Workflow Mode
Mode: solo
```

**Team Mode:**
```markdown
## Workflow Mode
Mode: team
```

**If mode is not specified:** Claude asks the developer which mode to use before proceeding.

---

## Branching (simple)
- Default branch: `main`
- One task per feature branch:
  - `feat/<slug>` for new features
  - `fix/<slug>` for bug fixes
  - `chore/<slug>` for maintenance
  - `docs/<slug>` for documentation-only

**Claude:** When work is requested, create/switch to a focused branch:
```bash
git checkout -b feat/<slug>   # or fix/<slug>, chore/<slug>, docs/<slug>
```

---

## Commits
- Use **Conventional Commits**: `feat: …`, `fix: …`, `chore: …`, `docs: …`, `refactor: …`, `test: …`.
- Keep subject lines imperative and clear; add short body bullets only when helpful.

**Examples**
```
feat: add JWT auth middleware
fix: correct timezone handling in report export
refactor: extract invoice total calculator
```

---

## Solo Mode Workflow

**When to use:** Working alone on a project.

**Process:** Branch → Commit → Pre-push Check → Push → Merge Locally → Push Main

### What counts as an important change (when to push)
Push after a commit **only if all** of the following are true:
1) Tests pass (or tests aren't set up yet).
2) Lint/build succeeds.
3) The change is a logical milestone (behavior complete, bug fixed, API/schema updated, or major refactor checkpoint).

### Pre-push check (automated gate)
Run these in order. If any fail, **do not push**.
```bash
# test
npm test || pnpm test || yarn test || true

# lint
npm run lint || pnpm lint || yarn lint || true

# build
npm run build || pnpm build || yarn build || true

# optional secret scan (if installed)
git secrets --scan 2>/dev/null || true
```

- If scripts are missing (e.g., early project), skip gracefully and report what was skipped.
- If tests or build fail, fix issues, commit, and re-run.

**Claude:** On success, push:
```bash
git push -u origin $(git branch --show-current)
```

### Merging to main (Solo Mode)
After feature is complete and checks pass:
```bash
git checkout main
git pull --ff-only origin main

# Try fast-forward first
git merge --ff-only <feature-branch>

# If not possible and you prefer a single commit, use squash
# git merge --squash <feature-branch>
# git commit -m "feat: <description>"

git push origin main

# Delete branch only after confirming main is healthy
git branch -d <feature-branch>
# Optional: remove remote branch
git push origin :<feature-branch>
```

### When to use PR even in Solo Mode
- Complex refactoring (want to review with fresh eyes later)
- Experimental features (want to document decision-making)
- Before major deployment (final safety check)
- Learning/practicing PR workflow

---

## Team Mode Workflow

**When to use:** Working with one or more teammates.

**Process:** Branch → Commit → Pre-push Check → Push → Create PR → Review → Merge

### Pre-push check (same as Solo Mode)
```bash
npm test && npm run lint && npm run build
```

If any check fails, **do not push**. Fix issues, commit, and re-run.

**Claude:** On success, push:
```bash
git push -u origin $(git branch --show-current)
```

### Creating a Pull Request
After pushing your feature branch:
```bash
# Push feature branch
git push -u origin feat/email-validation

# Create PR via GitHub CLI (if installed)
gh pr create --title "feat: add email validation" \
  --body "Implements email validation with comprehensive tests"

# OR: Create PR manually on GitHub web interface
```

### PR Description Template
Use this template when creating PRs:
```markdown
## What
[Brief description of changes]

## Why
[Reason for the change - bug fix, new feature, refactor]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Edge cases covered

## Documentation
- [ ] API docs updated (if applicable)
- [ ] README updated (if applicable)
- [ ] Rules learned documented (if applicable)

## Checklist
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Lint passes
- [ ] No console.log or debug code
- [ ] No secrets committed
```

### Review Process
1. **Reviewer checks:**
   - Code quality and readability
   - Test coverage
   - Documentation accuracy
   - No breaking changes

2. **Address feedback:**
   - Make requested changes
   - Push to same branch (PR auto-updates)
   - Re-request review

3. **Merge after approval:**
   - Preferred: **Squash and merge** (clean history)
   - Alternative: **Merge commit** (preserves all commits)
   - Never: **Force push to main**

### After Merge
```bash
# Update local main
git checkout main
git pull origin main

# Delete local branch
git branch -d feat/email-validation

# Delete remote branch (auto-deleted if enabled on GitHub)
git push origin :feat/email-validation
```

---

## Claude Behavior Rules

### In SOLO MODE:
- ✅ Merge feature branches locally after pre-push checks pass
- ✅ Push directly to main after successful merge
- ✅ Can skip PR for standard features
- ✅ Clean up feature branches after merge
- ⚠️ May create PR for complex features if developer requests

### In TEAM MODE:
- ❌ NEVER merge to main directly
- ✅ Always create PR after pushing feature branch
- ✅ STOP and wait for human review
- ✅ Address review feedback when requested
- ✅ Human or Claude merges after approval (based on team preference)

### Mode Detection:
If `Mode:` is not clearly specified in CLAUDE.md, Claude asks:
```
"I don't see a workflow mode specified in CLAUDE.md. 
Is this a solo or team project? I'll work accordingly."
```

---

## Minimal TDD rhythm (optional)
Use when helpful; keep messages short:
```
test: add failing tests for invoice rounding (RED)
feat: implement invoice rounding to 2dp (GREEN)
refactor: extract rounding util (REFACTOR)
```

---

## Safety rules
- **Never** force-push to `origin/main`.
- Only use `--force-with-lease` on **your** feature branches when necessary and understood.
- Keep `.env`, keys, and large artifacts out of Git.
- If the pre-push check fails or required scripts are missing, **stop** and ask how to proceed.

---

## Setup helpers (one-time)

### `.gitignore` (extend per stack)
```
node_modules/
dist/
.build/
.env
.env.*
*.log
coverage/
.DS_Store
```

### Conventional Commits `commit-msg` hook (optional)
```bash
# .git/hooks/commit-msg (chmod +x)
#!/usr/bin/env bash
grep -E '^(feat|fix|docs|style|refactor|perf|test|chore|revert)(\(.+\))?: ' "$1" >/dev/null || {
  echo "Commit message must follow Conventional Commits, e.g. 'feat: ...'" >&2
  exit 1
}
```

---

## Claude quick reference
- Create branch → commit small steps → run **pre-push check** → push if green.
- **Solo mode:** Merge locally, push main.
- **Team mode:** Create PR, wait for review.
- Ask for confirmation before any destructive action (branch deletion, rewrites).