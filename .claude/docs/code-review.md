# Code Review Guidelines

> **Purpose:** Ensure code quality, knowledge sharing, and catch issues before they reach main.

---

## Applicability

**Team Mode:** Code reviews are mandatory for all changes to main branch.

**Solo Mode:** Code reviews are optional but recommended for:
- Complex refactoring
- Experimental features
- Major architectural changes
- Learning and self-improvement

In Solo Mode, you review your own PRs with fresh eyes (e.g., review in the morning what you coded the evening before).

---

## Reviewer Responsibilities

### What to Check
1. **Functionality**
   - Do tests pass locally?
   - Does the code do what the PR description claims?

2. **Code Quality**
   - Is it readable and maintainable?
   - Are naming conventions followed?
   - No obvious bugs or edge cases missed?

3. **Tests**
   - Are new features tested?
   - Do tests cover edge cases?
   - Are tests clear and maintainable?

4. **Documentation**
   - Is relevant documentation updated?
   - Are API changes documented?
   - Are breaking changes clearly marked?

5. **Security & Safety**
   - No secrets committed (.env, API keys)
   - No obvious security vulnerabilities
   - Input validation where needed

### Review Timeline
- **Aim for < 24 hours** for standard PRs
- **< 4 hours** for urgent fixes
- **Same day** for small documentation changes

---

## Author Responsibilities

### Before Creating PR
- Run full test suite locally
- Check PR against checklist (tests, build, lint, docs)
- Write clear PR description explaining **what** and **why**

### PR Description Template
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

### Responding to Feedback
- **Be receptive:** Reviews help us improve
- **Ask questions:** If feedback unclear, ask for clarification
- **Discuss alternatives:** If you disagree, explain your reasoning
- **Update PR:** Push changes to same branch

---

## Common Review Patterns

### ✅ Approve When
- Code meets quality standards
- Tests are comprehensive
- Documentation is clear
- No obvious issues

### 💬 Comment When
- Small improvements possible (non-blocking)
- Questions about approach
- Suggestions for future refactoring

### ❌ Request Changes When
- Tests missing or failing
- Security issues present
- Breaking changes undocumented
- Code unreadable or overly complex

---

## Claude's Role in Reviews

**Claude cannot be the reviewer** (AI limitation), but Claude can:
- ✅ Address review feedback (make requested changes)
- ✅ Answer questions about code
- ✅ Run additional tests
- ✅ Update documentation based on feedback

**Human must:**
- ❌ Provide the actual code review
- ❌ Make final merge decision
- ❌ Ensure quality standards