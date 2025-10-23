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

**Example:**

```
- Backend: Node.js 20.x with Express 4.x
- Database: PostgreSQL 15.x
- ORM: Prisma 5.x
- Authentication: JWT with bcrypt
- Testing: Jest 29.x
- Deployment: Docker + Railway
```

### Project Structure

```
[Your actual project structure - copy from your file tree]
```

**Example:**

```
src/
├── controllers/     # Request handlers
├── services/        # Business logic
├── models/          # Data models (Prisma)
├── middleware/      # Auth, validation, error handling
├── routes/          # API route definitions
├── utils/           # Helper functions
└── tests/           # Test files
```

### Key Components

- **[Component Name]:** [Description of what it does]
- **[Another Component]:** [Description]
- **[Data Layer]:** [How data flows through the system]

**Example:**

```
- **AuthController:** Handles login, registration, token refresh
- **UserService:** Business logic for user management, validation
- **PrismaClient:** Database access layer with type-safe queries
- **JWT Middleware:** Validates tokens and attaches user to request
```

## Development Commands

### Setup

```bash
# Initial setup commands
[Your specific setup commands]
```

**Example:**

```bash
# Install dependencies
npm install

# Setup database
npx prisma migrate dev

# Seed initial data (optional)
npm run seed
```

### Development

```bash
# Development server
[Your dev server command]

# Watch mode
[Your watch command if applicable]
```

**Example:**

```bash
# Start dev server with hot reload
npm run dev

# Watch tests
npm run test:watch
```

### Testing

```bash
# Run tests
[Your test command]

# Run specific test
[Command for running individual tests]

# Coverage
[Coverage command if applicable]
```

**Example:**

```bash
# Run all tests
npm test

# Run specific test file
npm test -- auth.test.js

# Coverage report
npm run test:coverage
```

### Build & Deploy

```bash
# Build for production
[Your build command]

# Deploy
[Your deployment command]
```

**Example:**

```bash
# Build
npm run build

# Start production server
npm start

# Deploy to Railway
railway up
```

## Environment Configuration

### Required Environment Variables

- `[VAR_NAME]`: [Description and example value]
- `[ANOTHER_VAR]`: [Description and where to get it]
- `[API_KEY]`: [Which service and how to obtain]

**Example:**

```
- `DATABASE_URL`: PostgreSQL connection string (postgresql://user:pass@host:5432/db)
- `JWT_SECRET`: Secret for signing tokens (generate with: openssl rand -base64 32)
- `PORT`: Server port (default: 3000)
```

### Optional Environment Variables

- `[OPTIONAL_VAR]`: [Description and default value]

**Example:**

```
- `LOG_LEVEL`: Logging verbosity (default: "info", options: "debug", "info", "warn", "error")
- `RATE_LIMIT_MAX`: Max requests per window (default: 100)
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Required variables to set:
# - [List the must-have variables]
```

**Example:**

```bash
# Copy template
cp .env.example .env

# Required variables:
# - DATABASE_URL (get from Railway or local postgres)
# - JWT_SECRET (generate new: openssl rand -base64 32)
- PORT (use 3000 for development)
```

🔒 **Secrets Management Guidance:**

- Never commit `.env` to version control
- `.env` is in `.gitignore` by default
- Use GitHub Actions Secrets for CI/CD
- For production: Railway/Heroku/Vercel environment variables
- Rotate secrets regularly (every 90 days recommended)

## Code Conventions

### Naming Conventions

- **Files:** [camelCase/kebab-case/snake_case + examples]
- **Functions:** [camelCase/snake_case + examples]
- **Classes:** [PascalCase + examples]
- **Variables:** [camelCase/snake_case + examples]
- **Constants:** [UPPER_SNAKE_CASE + examples]

**Example:**

```
- Files: kebab-case (auth-controller.js, user-service.js)
- Functions: camelCase (getUserById, validateToken)
- Classes: PascalCase (UserService, AuthController)
- Variables: camelCase (userId, tokenExpiry)
- Constants: UPPER_SNAKE_CASE (MAX_LOGIN_ATTEMPTS, TOKEN_EXPIRY_HOURS)
```

### Code Style

- **Indentation:** [Spaces/tabs and how many]
- **Line Length:** [Max characters per line]
- **Semicolons:** [Required/optional]
- **Quotes:** [Single/double quotes preference]

**Example:**

```
- Indentation: 2 spaces (no tabs)
- Line Length: 100 characters max
- Semicolons: Required
- Quotes: Single quotes for strings, double for JSX
- Trailing commas: Always in multi-line
```

### File Organization

- **Import Order:** [How to order imports]
- **Export Style:** [Named/default exports preference]
- **Directory Structure:** [How to organize new files]

**Example:**

```
Import Order:
1. Node built-ins (fs, path)
2. External packages (express, prisma)
3. Internal modules (@/services, @/utils)
4. Relative imports (./helpers, ../config)

Export Style:
- Named exports for utilities and services
- Default exports for controllers and routes

New Files:
- Controllers: src/controllers/
- Services: src/services/
- Tests: src/tests/ (mirror source structure)
```

## API Documentation

### Base URL

- **Development:** [http://localhost:PORT]
- **Production:** [Your production URL]

**Example:**

```
- Development: http://localhost:3000
- Production: https://api.yourapp.com
```

### Authentication

[How authentication works if applicable]

**Example:**

```
JWT Bearer token authentication:
1. Login via POST /auth/login with email + password
2. Receive access token (expires 1h) and refresh token (expires 7d)
3. Include in requests: Authorization: Bearer <token>
4. Refresh via POST /auth/refresh with refresh token
```

### Key Endpoints

- `GET /[endpoint]` - [Description]
- `POST /[endpoint]` - [Description]
- `PUT /[endpoint]` - [Description]
- `DELETE /[endpoint]` - [Description]

**Example:**

```
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Login and receive tokens
- `POST /auth/refresh` - Refresh access token
- `GET /users/me` - Get current user profile (auth required)
- `PUT /users/me` - Update current user profile (auth required)
- `GET /products` - List all products (public)
- `POST /products` - Create product (admin only)
```

### Request/Response Examples

[Include common request/response patterns]

**Example:**

```
POST /auth/login
Request:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (200):
{
  "accessToken": "eyJhbG...",
  "refreshToken": "eyJhbG...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}

Response (401):
{
  "error": "Invalid credentials"
}
```

## Dependencies

### Core Dependencies

- **[dependency-name]:** [Why you use it, what it does]

**Example:**

```
- **express:** Web framework for handling HTTP requests/routing
- **@prisma/client:** Type-safe database ORM
- **jsonwebtoken:** JWT token generation and verification
- **bcrypt:** Password hashing
- **zod:** Runtime type validation for request bodies
```

### Development Dependencies

- **[dev-dependency]:** [What it's used for]

**Example:**

```
- **jest:** Testing framework
- **supertest:** HTTP endpoint testing
- **eslint:** Code linting
- **prettier:** Code formatting
- **nodemon:** Auto-restart dev server on changes
```

### Dependency Management

- [How you manage versions, any specific rules]

**Example:**

```
- Use exact versions in package.json (no ^ or ~)
- Update dependencies monthly via npm outdated
- Test thoroughly after updates
- Major version updates require approval
```

## Testing Strategy

### Test Types

- **Unit Tests:** [What you unit test and how]
- **Integration Tests:** [What integration points you test]
- **E2E Tests:** [If applicable, what user flows you test]

**Example:**

```
- Unit Tests: Services, utilities, pure functions (70% coverage target)
- Integration Tests: API endpoints with test database (required for all endpoints)
- E2E Tests: Not currently implemented (future: critical user flows)
```

### Test Structure

- **Test Files:** [Where tests live, naming convention]
- **Test Data:** [How you handle test fixtures/mocks]
- **Coverage Goals:** [Coverage targets if any]

**Example:**

```
- Test Files: src/tests/ mirroring source structure (user-service.test.js)
- Test Data: Fixtures in src/tests/fixtures/, Prisma test DB reset before each test
- Coverage Goals: 80% overall, 100% for critical paths (auth, payments)
```

### Testing Best Practices

- Use deterministic data and seeding to avoid flaky tests
- Maintain shared fixtures/mocks to reduce duplication
- Ensure tests run consistently in CI/CD
- Isolate tests (no shared state between tests)

**Example:**

```
- Reset test database before each test suite
- Use fixed timestamps for date-dependent tests
- Mock external APIs (email, payment gateways)
- Run tests in random order to catch dependencies
```

## Development Notes

### Known Issues

- [Any current bugs or limitations]

**Example:**

```
- Email notifications are currently mocked (not sending real emails)
- File uploads limited to 5MB (needs CDN for larger files)
- Search is case-sensitive (needs full-text search implementation)
```

### Performance Considerations

- [Any performance bottlenecks or optimizations]

**Example:**

```
- Database queries use indexes on frequently queried fields
- API responses are cached for 5 minutes (public endpoints)
- Pagination required for list endpoints (max 100 items)
- Large file operations run async with job queue
```

### Security Notes

- [Security considerations specific to this project]

**Example:**

```
- Passwords hashed with bcrypt (12 rounds)
- Rate limiting on auth endpoints (5 attempts/15min)
- SQL injection prevented via Prisma parameterized queries
- XSS protection via input sanitization
- CORS restricted to allowed origins only
```

### Future Improvements

- [Planned features or refactoring]

**Example:**

```
- Add email verification for new accounts
- Implement OAuth (Google, GitHub)
- Add real-time notifications via WebSocket
- Migrate to microservices architecture (when scaling needed)
- Add comprehensive E2E test suite
```

---

## Quick Start Checklist

After copying this template:

- [ ] Fill in all [placeholders] with your project details
- [ ] Create `.claude/docs/` folder and copy workflow files
- [ ] Create empty `experiment_log.md`
- [ ] Create empty `.claude/docs/rules-learned.md`
- [ ] Optional: Create `plan.md` if using plan-based workflow
- [ ] Set up `.env` file with required variables
- [ ] Verify GitHub branch protection (if using GitHub)
- [ ] Run initial tests to verify setup
- [ ] Commit initial CLAUDE.md to repository

✅ Claude is now ready to work on your solo project with full context!

```

Nyní máš dokument v Canvas módu, který můžeš celý zkopírovat najednou! Chceš teď stejným způsobem i CLAUDE_TEAM.md? 😊
```