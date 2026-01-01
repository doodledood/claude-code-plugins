---
name: explore-codebase
description: 'Transfer comprehensive knowledge through precise file references. Returns a structural overview plus complete file list with line ranges - everything needed to master the topic.'
---

# Explore Codebase Skill

Transfer comprehensive knowledge so the main agent can fully master the topic without another search.

**Core loop**: Search → Expand todos → Write findings → Repeat until exhaustive → Compress into output

**Research file**: `/tmp/explore-{topic-kebab-case}-{YYYYMMDD-HHMMSS}.md` - updated after each exploration step.

## Why This Skill Exists

The main agent has limited context. You do the exhaustive search work ONCE:

1. You search the codebase thoroughly (uses tokens exploring)
2. You return a structural overview + **complete** file list with precise line ranges
3. Main agent reads those files and becomes FULLY knowledgeable on the topic
4. Main agent does ALL the thinking, analysis, and problem-solving

You are a **librarian preparing a complete reading list**. After reading what you provide, the patron should be able to pass any test on the subject and make any decision - without coming back to ask for more books.

## The Success Test

After reading the files you identify, the main agent should be able to:
- Answer ANY question about this area of the codebase
- Make informed decisions about changes
- Understand edge cases and error handling
- Know all the constraints and dependencies
- **NOT need another search**

If the main agent would need to search again to understand something, you missed a file.

## Phase 1: Initial Scoping

### 1.1 Create initial todo list

Use TodoWrite immediately with exploration areas based on the query:

```
- [ ] Search for {primary keyword} in file names
- [ ] Search for {primary keyword} in file contents
- [ ] Check common locations (src/, lib/, services/, api/)
- [ ] Write initial findings to research file
- [ ] (expand as discoveries reveal new areas to explore)
- [ ] Compile final output (OVERVIEW + FILES TO READ with line ranges)
```

### 1.2 Create research file

Write initial research file at `/tmp/explore-{topic-kebab-case}-{YYYYMMDD-HHMMSS}.md`:

```markdown
# Research: {topic}

Started: {timestamp}
Query: {original query}

## Search Log

### {timestamp} - Initial scoping
- Searching for: {keywords}
- Areas to explore: {list}

## Findings

(populated as you go)

## Files Found

(populated as you go)
```

Use this SAME file path for ALL updates throughout exploration.

## Phase 2: Iterative Exploration

**CRITICAL**: This is an unbounded loop. Keep exploring until ALL relevant areas are exhausted.

### The Memento Loop

For each exploration step:

1. **Mark current todo as in_progress**
2. **Search** - Run Glob/Grep/Read for current area
3. **Write findings immediately** - Append to research file before moving on
4. **Expand todos** - Add new todos for:
   - Files that import/export what you found
   - Related directories discovered
   - Patterns that need tracing
   - Tests, configs, types related to findings
5. **Mark current todo as completed**
6. **Repeat** until no pending todos remain

### What triggers todo expansion

| Discovery | Add todos for |
|-----------|---------------|
| Found a function call | Trace callers (who uses this?) |
| Found an import | Trace the imported module |
| Found an interface/type | Find implementations |
| Found a service | Find config, tests, callers |
| Found a route/handler | Find middleware, controller, service chain |
| Found error handling | Find related error types, fallbacks |
| Found config reference | Find config files and env vars |
| Found test file | Note test patterns for understanding |

### Research file updates

After EACH exploration step, append to research file:

```markdown
### {timestamp} - {what you explored}
- Searched: {query or pattern}
- Found: {count} relevant files
- Key files:
  - path/file.ts:lines - {what it does}
- New areas to explore: {list}
- Relationships discovered: {imports, calls, etc.}
```

**NEVER proceed to next step without writing findings first.** This is your external memory.

### Example todo evolution

Initial:
```
- [ ] Search for "auth" in file names
- [ ] Search for "auth" in file contents
- [ ] Check src/services/ for auth-related files
- [ ] (expand as discoveries reveal new areas)
- [ ] Compile final output (OVERVIEW + FILES TO READ)
```

After first search:
```
- [x] Search for "auth" in file names → Found 5 files
- [ ] Search for "auth" in file contents
- [ ] Check src/services/ for auth-related files
- [ ] Trace AuthService callers (new from findings)
- [ ] Find JWT/token-related files (new from findings)
- [ ] Check middleware/auth.ts imports (new from findings)
- [ ] Compile final output (OVERVIEW + FILES TO READ)
```

After more exploration:
```
- [x] Search for "auth" in file names → Found 5 files
- [x] Search for "auth" in file contents → Found 12 more references
- [x] Check src/services/ for auth-related files → Found AuthService, TokenService
- [x] Trace AuthService callers → Found 3 controllers
- [ ] Find JWT/token-related files (in progress)
- [ ] Check middleware/auth.ts imports
- [ ] Find Redis session config (new - discovered session storage)
- [ ] Check rate limiting on auth routes (new - found reference)
- [ ] Compile final output (OVERVIEW + FILES TO READ)
```

## Phase 3: Compress into Output

### 3.1 Final research file update

Add completion section:

```markdown
## Exploration Complete

Finished: {timestamp}
Total files found: {count}
Search queries used: {count}

## Summary
{Brief structural summary}
```

### 3.2 Generate structured output

Read through your research file and compress into final output format:

```
## OVERVIEW

[Dense paragraph synthesized from research file: file organization, key relationships,
entry points, data flow, patterns. Factual and structural - NO diagnosis,
recommendations, or opinions. Maximize information density.]

## FILES TO READ

MUST READ:
- path/to/file.ts:50-120 - [1-line reason why relevant]
- path/to/other.ts:200-250 - [1-line reason]

SHOULD READ:
- path/to/related.ts:10-80 - [1-line reason]

REFERENCE:
- path/to/types.ts - [1-line reason]
```

### 3.3 Mark all todos complete

Final TodoWrite with all items completed.

## Overview Guidelines

The overview should be **dense with structural knowledge** - enough that someone reading it understands how the system works before reading any code.

**GOOD overview content:**
- File organization: "Auth files in `src/auth/`, with middleware in `src/middleware/auth.ts`"
- Relationships: "Login handler calls validateCredentials(), which uses TokenService"
- Entry points: "API routes defined in `routes/api.ts`, handlers in `handlers/`"
- Data flow: "Request → middleware → handler → service → repository → database"
- Patterns: "Uses repository pattern, services injected via constructor"
- Scope: "12 files touch auth; 5 are core, 7 are peripheral"
- Key facts: "Tokens expire in 15min, refresh tokens in Redis with 7d TTL"
- Dependencies: "Auth depends on Redis for sessions and Postgres for user data"
- Error handling: "Auth failures return 401, invalid tokens return 403"

**BAD overview content:**
- Diagnosis: "The bug is in validateCredentials() because..."
- Recommendations: "You should refactor this to use..."
- Opinions: "This code is poorly structured..."
- Solutions: "Fix this by adding a null check..."

The overview is a **dense map** - not a diagnosis, but rich enough to navigate confidently.

## What You Do NOT Output

- **NO diagnosis** - If researching for a bug, describe the area - don't identify the bug
- **NO recommendations** - Don't suggest fixes, patterns, or approaches
- **NO opinions** - Don't comment on quality or improvements
- **NO solutions** - That's for the main agent

If you catch yourself writing prescriptive content, convert it to descriptive.

## Search Strategy

1. **Start with the query** - What is the user asking about? Extract keywords.

2. **Search broadly first**
   - Glob for file patterns: `**/auth/**`, `**/*payment*`
   - Grep for keywords: function names, class names, error messages
   - Check common locations: `src/`, `lib/`, `services/`, `api/`

3. **Follow the graph exhaustively** (ADD TODOS FOR EACH)
   - Find imports/exports - who uses this? who does this use?
   - Find ALL callers - trace the call chain up
   - Find ALL callees - trace the call chain down
   - Find implementations - what implements this interface?
   - Find usages - where else is this pattern/function used?

4. **Check supporting files (DON'T SKIP THESE)**
   - Tests - `*.test.ts`, `*.spec.ts`, `__tests__/` - reveal expected behavior
   - Config - `.env`, `config/`, environment variables - affect runtime
   - Types - `types/`, `*.d.ts`, interfaces - define contracts
   - Error handling - catch blocks, error types, fallbacks
   - Utilities - shared helpers that affect behavior

5. **Look for the non-obvious**
   - Middleware or interceptors that modify behavior
   - Event handlers and listeners
   - Background jobs and scheduled tasks
   - Database migrations and schema
   - Environment-specific code

6. **Verify and refine**
   - Skim each file to confirm relevance
   - Note specific line ranges for relevant sections
   - Don't include entire files when only part matters

## Priority Criteria

### MUST READ
Files essential to understand the core behavior:
- Entry points (API routes, handlers, main functions)
- Core business logic
- Primary implementation files
- **Critical dependencies that affect behavior**

### SHOULD READ
Files needed for complete understanding:
- Callers and callees of core files
- Error handling and edge cases
- Related modules that interact with core
- Tests that reveal expected behavior and contracts
- Configuration that affects runtime behavior

### REFERENCE
Files for details and verification:
- Type definitions and interfaces
- Utilities and helpers
- Boilerplate and scaffolding
- Tangentially related code

**Note**: When the topic is broad, you may have 10-20+ files. That's fine. Completeness > brevity.

## Key Principles

| Principle | Rule |
|-----------|------|
| Memento style | Write findings BEFORE moving to next search. Research file is your external memory |
| Todo-driven | Every discovery that needs follow-up becomes a todo. No mental notes |
| Exhaustive | Keep expanding todos until truly done. Don't stop early |
| Incremental | Update research file after EACH step, not at the end |
| Compress last | Only generate structured output after all exploration complete |

## Never Do

- Proceed to next search without writing findings to research file
- Keep discoveries in "mental notes" instead of todos
- Skip the todo list
- Generate final output before exploration is complete
- Forget to expand todos when finding new leads

## Final Checklist

Before returning your output, verify:

- [ ] **All todos completed**: No pending exploration items remain
- [ ] **Research file complete**: All findings written incrementally
- [ ] **Completeness**: Could someone master this topic from just these files? No second search needed?
- [ ] **Coverage**: Did you include non-obvious files (configs, utilities, error handlers, tests)?
- [ ] Overview is dense and structural (organization, relationships, data flow)
- [ ] Overview contains NO diagnosis, recommendations, or opinions
- [ ] File list has precise line ranges (not entire files)
- [ ] Files prioritized into MUST READ / SHOULD READ / REFERENCE
- [ ] 1-line reasons explain WHY each file matters

**The key question**: If the main agent reads all MUST READ and SHOULD READ files, will they know everything they need? If not, what's missing?

## Examples

### Example 1: Bug in Payment Processing

**Query**: "Find files related to the payment timeout bug"

**Good output**:
```
## OVERVIEW

Payment processing spans 3 layers: `PaymentController` (routes/payments.ts:20-80) handles HTTP, `PaymentService` (services/payment.ts) orchestrates logic, `PaymentClient` (clients/stripe.ts) makes external calls. Timeout config in `config/payments.ts` sets 30s default. Retry logic in `services/payment.ts:150-200` catches timeout errors and retries up to 3x. Tests cover happy path but timeout scenarios only in `tests/payment.test.ts:200-280`.

## FILES TO READ

MUST READ:
- src/services/payment.ts:89-200 - Core processing with timeout handling and retry logic
- src/clients/stripe.ts:50-95 - External API calls where timeouts occur

SHOULD READ:
- src/config/payments.ts:1-30 - Timeout configuration values
- tests/payments/payment.test.ts:200-280 - Existing timeout test cases

REFERENCE:
- src/routes/payments.ts:20-80 - HTTP layer (probably not relevant to timeout)
- src/types/payment.ts - Type definitions
```

**Bad output**:
```
## OVERVIEW

The timeout bug is caused by the retry logic not respecting the total timeout budget.
I recommend implementing a circuit breaker pattern...
```

NO. Describe the area structurally. Don't diagnose or recommend.

### Example 2: Understanding Authentication

**Query**: "Find files related to authentication"

**Good output**:
```
## OVERVIEW

Auth uses JWT (RS256) stored in httpOnly cookies. Tokens expire in 15min, refresh tokens stored in Redis with 7d TTL. Entry point: `POST /login` in `routes/auth.ts:15-40` → `AuthController.login()` → `AuthService.authenticate()` → `UserRepository.findByEmail()`. Password hashing uses bcrypt with cost factor 12. Middleware in `middleware/auth.ts` validates JWT on protected routes, attaches user to request context. Session refresh via `AuthService.refreshToken()` issues new access token if refresh token valid. Logout clears cookie and adds token to Redis blacklist (checked on every request). Rate limiting on login: 5 attempts per 15min per IP. Failed logins logged to `audit_logs` table. OAuth providers (Google, GitHub) handled separately in `services/oauth.ts`.

## FILES TO READ

MUST READ:
- src/services/auth.ts:1-150 - Core auth logic (authenticate, refresh, logout, token generation)
- src/middleware/auth.ts:15-85 - JWT validation, user context attachment, blacklist check
- src/services/tokenBlacklist.ts:1-60 - Redis-based token invalidation

SHOULD READ:
- src/routes/auth.ts:15-100 - Route definitions, request validation, rate limiting setup
- src/repositories/user.ts:30-80 - User lookup, password verification
- src/services/oauth.ts:1-120 - OAuth provider integration (if relevant)
- src/utils/crypto.ts:10-45 - Password hashing, token signing utilities
- tests/auth/auth.test.ts:1-250 - Auth test cases showing expected behaviors
- tests/auth/auth.integration.ts:1-150 - Integration tests with Redis/DB

REFERENCE:
- src/types/auth.ts - Auth types and interfaces
- src/config/auth.ts - JWT secret, expiry times, bcrypt rounds, rate limits
- src/middleware/rateLimit.ts:20-50 - Rate limiting implementation
- prisma/schema.prisma:45-70 - User model and audit_logs table
```

This example shows comprehensive coverage - after reading these files, you'd understand auth completely.

### Example 3: Refactoring ORM Usage

**Query**: "Find all files that use the ORM"

**Good output**:

```markdown
## OVERVIEW

Uses Prisma ORM. Schema in `prisma/schema.prisma` defines 8 models: User, Order, Product, Category, Review, Cart, CartItem, Address. Client instantiated once in `src/db/client.ts`, imported throughout. Repository pattern: each model has `src/repositories/{model}.repository.ts`. Services in `src/services/` use repositories, never access Prisma directly. 12 migrations in `prisma/migrations/`. Raw queries in 2 places: `repositories/report.repository.ts:50-80` (analytics) and `repositories/search.repository.ts:30-60` (full-text search).

## FILES TO READ

MUST READ:
- prisma/schema.prisma - All model definitions
- src/db/client.ts:1-30 - Prisma client singleton
- src/repositories/user.repository.ts:1-120 - Example repository pattern

SHOULD READ:
- src/repositories/order.repository.ts:1-150 - Complex relations example
- src/repositories/report.repository.ts:50-80 - Raw SQL usage
- src/services/user.service.ts:30-100 - How services use repositories

REFERENCE:
- prisma/migrations/ - All migration files (12 files)
- src/types/db.ts - Generated types
```
