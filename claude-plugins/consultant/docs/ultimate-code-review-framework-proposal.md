# The Ultimate Code Review Framework
### *"The Bestest Reviewer in the World"*

---

## Core Principles (In Priority Order)

*When in doubt, apply these principles. They govern all categories.*

| # | Principle | Meaning |
|---|-----------|---------|
| **P1** | **Correctness Above All** | Working code > elegant code. A bug in production is worse than ugly code that works. |
| **P2** | **Fail Loud, Fail Fast** | Silent failures are unacceptable. Every error must be visible, logged, and actionable. |
| **P3** | **Make Illegal States Unrepresentable** | Types should prevent bugs at compile-time. If invalid state can't exist, it can't cause bugs. |
| **P4** | **Single Responsibility** | Every function, class, and module should do ONE thing. If you need "and" to describe it, split it. |
| **P5** | **Explicit Over Implicit** | Clarity beats cleverness. 3 readable lines > 1 clever line. No magic, no hidden behavior. |
| **P6** | **YAGNI** | Don't build for hypothetical futures. Solve today's problem today. |
| **P7** | **Prove It With Tests** | Untested code is unverified code. Tests prove correctness; coverage proves confidence. |
| **P8** | **Comments Tell Why, Code Tells What** | If a comment lies, it's worse than no comment. Comments explain reasoning, not mechanics. |
| **P9** | **Minimize Blast Radius** | Contain failures. One bad input shouldn't crash the system. Isolate concerns. |
| **P10** | **Least Surprise** | Code should behave as readers expect. No hidden side effects, no unexpected mutations. |

---

## Review Categories (Priority Order)

| P | Category | Core Question | Governing Principles |
|---|----------|---------------|---------------------|
| **1** | **Correctness & Logic** | Does it work correctly? | P1, P10 |
| **2** | **Silent Failure Detection** | Can errors hide? | P2, P9 |
| **3** | **Type Design & Invariants** | Do types prevent invalid states? | P3, P1 |
| **4** | **Scope & Responsibility** | Is each unit doing exactly one thing? | P4, P6 |
| **5** | **Simplicity & Design** | Is it over-engineered? | P5, P6 |
| **6** | **Test Quality & Coverage** | Would we catch regressions? | P7, P1 |
| **7** | **Comment & Doc Correctness** | Do comments tell the truth? | P8 |
| **8** | **Maintainability & Clarity** | Can future devs understand this? | P5, P10 |
| **9** | **Reliability & Error Handling** | Does it handle chaos gracefully? | P2, P9 |
| **10** | **Performance** | Any obvious bottlenecks? | (only when relevant) |
| **11** | **Security** | Auth, injection, data exposure? | P9 (when applicable) |

---

## 1. Correctness & Logic (HIGHEST PRIORITY)

**Governing Principle**: *P1 - Correctness Above All*

| Check | What to Look For | Example |
|-------|------------------|---------|
| **Logic Errors** | Incorrect conditionals, wrong operators | `if (a && b)` should be `if (a \|\| b)` |
| **Off-by-One** | Boundary conditions, loop termination | `i <= len` vs `i < len` |
| **State Bugs** | Invalid transitions, race conditions | Setting state before checking precondition |
| **Null/Undefined** | Unhandled nullish values | `user.profile.name` without null check |
| **Type Coercion** | Implicit conversions | `"5" + 3 = "53"` |
| **API Contract Violations** | Response mismatches | Expecting `{ data: [] }`, getting `{ items: [] }` |
| **Async Bugs** | Missing awaits, unhandled promises | `const data = fetchData()` (missing await) |
| **Data Transformation** | Wrong map/filter/reduce logic | Filtering when should be mapping |
| **Comparison Bugs** | Reference vs value comparison | `obj1 === obj2` for object equality |
| **Arithmetic Errors** | Overflow, precision, division by zero | Currency math with floats |

**Severity**: Logic bugs → **BLOCKER**

---

## 2. Silent Failure Detection (CRITICAL)

**Governing Principle**: *P2 - Fail Loud, Fail Fast*

### The Silent Failure Hierarchy of Evil

| Severity | Anti-Pattern | Why It's Evil |
|----------|--------------|---------------|
| **BLOCKER** | Empty catch block | Errors vanish completely |
| **BLOCKER** | Catch-and-return-null without logging | Caller can't distinguish success from failure |
| **HIGH** | Broad exception catching | Masks unrelated errors |
| **HIGH** | Silent fallback to defaults | User unaware behavior changed |
| **HIGH** | Mock/fake data in production | Architectural rot indicator |
| **MEDIUM** | Console.log as only error handling | User sees nothing |
| **MEDIUM** | Boolean returns for failable operations | No error context for caller |

### Silent Failure Patterns to Detect

```
❌ catch (e) { }                           // Error vanishes
❌ catch (e) { return null }               // Silent failure
❌ catch (e) { return defaultValue }       // Hidden fallback
❌ catch (Exception e) { ... }             // Too broad
❌ data?.user?.settings?.theme ?? 'dark'   // Chains hiding bugs
❌ function process(data = [])             // Default hides caller bug
❌ if (!api) return mockData               // Production using mocks
❌ try { ...50 lines... } catch            // What actually failed?
```

### Required for Every Catch/Fallback

| Requirement | Question to Ask |
|-------------|-----------------|
| **Specific Error Type** | Are we catching exactly what we expect? |
| **Meaningful Logging** | Will we see this in logs with context? |
| **User Feedback** | Does the user know something went wrong? |
| **Justified Fallback** | Is there a comment explaining WHY we fall back? |
| **Recovery Path** | Is there a way to recover or retry? |

---

## 3. Type Design & Invariants

**Governing Principle**: *P3 - Make Illegal States Unrepresentable*

### Type Quality Dimensions

| Dimension | Rating Criteria | Questions |
|-----------|-----------------|-----------|
| **Encapsulation** (1-10) | Are internals hidden? | Can invariants be violated from outside? |
| **Invariant Expression** (1-10) | Is valid state obvious from the type? | Can you tell constraints from the definition? |
| **Invariant Usefulness** (1-10) | Do invariants prevent real bugs? | Aligned with business rules? |
| **Invariant Enforcement** (1-10) | Are invariants always enforced? | Validated at construction? All mutations guarded? |

### Type Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach |
|--------------|------------------|-----------------|
| **Primitive Obsession** | `userId: string` everywhere | `UserId` branded type or class |
| **Anemic Types** | Data bags with no behavior | Methods that enforce invariants |
| **Exposed Mutables** | `public items: Item[]` | Readonly + mutation methods |
| **Optional Everything** | `{ name?: string, email?: string }` | Distinct types for complete vs partial |
| **String-Typed Enums** | `status: string` | `status: 'pending' \| 'active' \| 'closed'` |
| **Boolean Blindness** | `process(true, false, true)` | Distinct types or objects |
| **Inconsistent Nullability** | Sometimes null, sometimes undefined | Pick one, be consistent |
| **God Types** | Type with 20+ fields | Break into focused types |
| **Validation Outside Constructor** | `if (user.isValid())` | Invalid users can't exist |
| **Stringly-Typed Data** | `JSON.parse(data)` as any | Validated parsing with schema |

### What Good Types Look Like

```typescript
// ❌ Bad: Invalid states representable
type User = {
  email: string;           // Could be empty or invalid
  emailVerified: boolean;  // Could be true with invalid email
  subscriptionEndDate?: Date;
  isSubscribed: boolean;   // Could mismatch with date
}

// ✅ Good: Invalid states unrepresentable
type UnverifiedUser = { email: Email; status: 'unverified' }
type VerifiedUser = { email: Email; status: 'verified' }
type SubscribedUser = { email: Email; status: 'verified'; subscription: Subscription }
type User = UnverifiedUser | VerifiedUser | SubscribedUser
```

**Severity**: Weak types allowing invalid state → **MEDIUM** to **HIGH**

---

## 4. Scope & Responsibility

**Governing Principle**: *P4 - Single Responsibility*

### The Scope Smell Test

| Smell | Indicator | Question |
|-------|-----------|----------|
| **"And" in Description** | "This function validates AND saves AND notifies" | Should this be 3 functions? |
| **Multiple Reasons to Change** | Would change for UI AND for business rules AND for DB | Too many concerns |
| **God Function/Class** | 200+ lines, 10+ dependencies | Doing too much |
| **Feature Envy** | Function uses more of another class than its own | Wrong home? |
| **Shotgun Surgery** | One change requires editing 10 files | Scattered responsibility |
| **Mixed Abstraction Levels** | SQL query next to UI formatting | Different concerns mixed |

### Scope Anti-Patterns

| Anti-Pattern | Example | Better Approach |
|--------------|---------|-----------------|
| **Kitchen Sink Function** | `processOrder()` does validation, pricing, inventory, email, logging | Extract each concern |
| **Util Classes** | `StringUtils` with 50 unrelated methods | Domain-specific helpers |
| **Manager/Handler/Service** | Generic names hiding unclear scope | Name after single responsibility |
| **Middleware Doing Business Logic** | Auth middleware also does rate limiting and logging | Separate middlewares |
| **Component Fetching Own Data** | React component with API calls inside | Container/presenter split |

### Scope Guidelines

- **Function**: Does ONE thing, fits on one screen (~30 lines max ideal)
- **Class/Module**: ONE reason to change, ONE axis of responsibility
- **File**: ONE concept, ONE export default (ideally)
- **Package**: ONE bounded context, ONE team could own it

**Severity**: God class/function → **MEDIUM**; Scattered responsibility → **HIGH**

---

## 5. Simplicity & Design

**Governing Principles**: *P5 - Explicit Over Implicit*, *P6 - YAGNI*

| Anti-Pattern | What to Look For |
|--------------|------------------|
| **Premature Abstraction** | Generic helper for one use case |
| **Speculative Generality** | "We might need this later" |
| **Abstraction Astronautics** | FactoryFactoryBuilder patterns |
| **Nested Ternaries** | `a ? b ? c : d : e` |
| **Dense One-Liners** | Clever but unreadable |
| **Config-Driven Everything** | YAML controlling what code should |
| **Wrapper Adding Nothing** | Class that just delegates |
| **Unnecessary DRY** | Abstraction to avoid 3 similar lines |
| **Framework Worship** | Using patterns because framework suggests them |

### Simplicity Guidelines

| Prefer | Over |
|--------|------|
| Switch/if-else chains | Nested ternaries |
| 3 clear lines | 1 clever line |
| Inline code | Premature abstraction |
| Hardcoded (initially) | Configurable (until needed) |
| Simple loop | Complex reduce |
| Explicit parameters | Magic configuration |

**Severity**: Over-engineering → **MEDIUM**; Unreadable complexity → **HIGH**

---

## 6. Test Quality & Coverage

**Governing Principle**: *P7 - Prove It With Tests*

### Coverage Priority Matrix

| Priority | What MUST Be Tested | Criticality |
|----------|---------------------|-------------|
| **9-10** | Data mutations, money/finance, auth, state machines | Critical |
| **7-8** | Business logic branches, API contracts, error paths | Important |
| **5-6** | Edge cases, boundaries, integration points | Standard |
| **3-4** | Unlikely error paths, cosmetic variations | Nice-to-have |
| **1-2** | Trivial getters, simple pass-through | Optional |

### Test Quality Checks

| Issue | What to Look For |
|-------|------------------|
| **Implementation Coupling** | Test breaks when refactoring (but behavior unchanged) |
| **Missing Negative Cases** | Only happy path tested |
| **Assertion-Free Tests** | Test runs code but verifies nothing |
| **Brittle Assertions** | Exact string matching, timestamps |
| **Test Interdependence** | Tests rely on run order |
| **Mocking Reality Away** | So mocked you're testing nothing real |
| **Missing Error Path Tests** | What happens when X fails? |
| **Flaky Tests** | Race conditions, timing assumptions |

### Must-Have Test Scenarios

- ✅ Happy path for new functionality
- ✅ Error handling (what happens when X fails?)
- ✅ Boundary conditions (empty, null, zero, max)
- ✅ State transitions (valid AND invalid)
- ✅ Each branch of conditional logic
- ✅ Integration points with real behavior

**Severity**: Missing critical test → **HIGH**; Brittle tests → **MEDIUM**

---

## 7. Comment & Documentation Correctness

**Governing Principle**: *P8 - Comments Tell Why, Code Tells What*

| Issue | What to Look For | Severity |
|-------|------------------|----------|
| **Stale Comment** | Comment describes old behavior | MEDIUM |
| **Lie Comment** | `// returns user` but returns `userId` | MEDIUM |
| **Redundant Comment** | `i++ // increment i` | LOW |
| **TODO Graveyard** | Ancient TODOs from 2019 | LOW |
| **Commented-Out Code** | Dead code "just in case" | LOW |
| **Missing "Why"** | Complex logic with no reasoning | LOW |
| **Outdated Examples** | Doc examples that don't compile | MEDIUM |

### Good Comments Explain

- **WHY** this non-obvious approach was chosen
- **CONSTRAINTS** that must be maintained
- **WARNINGS** about non-obvious gotchas
- **LINKS** to specs/tickets for complex requirements

---

## 8. Maintainability & Clarity

**Governing Principles**: *P5 - Explicit Over Implicit*, *P10 - Least Surprise*

| Issue | What to Look For |
|-------|------------------|
| **Cryptic Names** | `x`, `temp`, `data2`, `handleStuff` |
| **Hidden Dependencies** | Global state, singletons reached for |
| **Deep Nesting** | 5+ levels of if/for/try |
| **Magic Values** | `if (status === 3)` |
| **Inconsistent Patterns** | Different approaches for same problem |
| **Temporal Coupling** | Must call A before B (not enforced) |
| **Action at a Distance** | Mutation in unexpected place |
| **Non-Obvious Side Effects** | Function name doesn't hint at mutation |

**Severity**: Unmaintainable code → **MEDIUM** to **HIGH**

---

## 9. Reliability & Error Handling

**Governing Principles**: *P2 - Fail Loud*, *P9 - Minimize Blast Radius*

| Issue | What to Look For |
|-------|------------------|
| **Missing Error Handling** | No catch for network calls |
| **Incomplete Cleanup** | Resources leaked on error |
| **Retry Without Backoff** | Hammering failed service |
| **No Timeout** | Waiting forever |
| **Partial Failure Ignored** | Batch continues despite errors |
| **No Circuit Breaker** | Infinite retry |

**Required Pattern**:
- External calls: timeout + retry + fallback
- Resources: always cleanup (finally/defer/using)
- Transactions: commit or rollback, never partial

---

## 10. Performance (When Relevant)

*Only flag actual impact, not theoretical concerns.*

| Issue | Indicator |
|-------|-----------|
| **N+1 Queries** | Query in loop |
| **Unbounded Fetch** | `findAll()` no limit |
| **Missing Index** | Filter on non-indexed column |
| **Expensive in Loop** | Regex compile, JSON parse repeatedly |
| **Missing Pagination** | Loading unlimited records |

---

## 11. Security (When Applicable)

| Issue | What to Look For |
|-------|------------------|
| **Auth Bypass** | Missing auth check |
| **Injection** | Unsanitized input in query |
| **Secrets in Code** | Hardcoded keys |
| **IDOR** | Access by changing ID |
| **Sensitive Data Logged** | PII in logs |

---

## Severity Matrix

| Level | Triggers | Action |
|-------|----------|--------|
| **BLOCKER** | Logic bug causing wrong outcomes • Silent failure hiding critical error • Data corruption possible • Security breach | **MUST fix before merge** |
| **HIGH** | Bug that will manifest in prod • Silent failures • Missing critical test • Weak type allowing invalid state • Security issue | **SHOULD fix before merge** |
| **MEDIUM** | Over-engineering • Stale comments • Scope violation • Edge case gap • Maintainability debt | **Fix soon / discuss** |
| **LOW** | Minor simplification • Style consistency • Documentation improvement | **Nice to have** |
| **INFO** | Observation • Architectural note • Good patterns worth praising | **FYI** |

---

## Output Format

```markdown
## Summary
[1-2 sentence overall assessment with risk level]

## Principles Violated
- P2 (Fail Loud): [specific violation]
- P4 (Single Responsibility): [specific violation]

## Findings

### 🚨 BLOCKER
- **[Category]** `file.ts:123-145`
  - **Issue**: [What's wrong]
  - **Impact**: [Why it matters]
  - **Fix**: [Specific recommendation]

### ⚠️ HIGH
...

### 📋 MEDIUM
...

### 💡 LOW / INFO
...

## Type Design Assessment
[For any new/modified types]
- Encapsulation: X/10
- Invariant Expression: X/10
- Invariant Usefulness: X/10
- Invariant Enforcement: X/10

## Test Coverage Assessment
- Critical gaps (8-10): [List]
- Important gaps (5-7): [List]
- Coverage quality: [Assessment]

## Silent Failure Scan
- Patterns detected: [List any catch blocks, fallbacks, optionals]
- Risk level: [Assessment]

## ✅ Positive Observations
[What's done well - important for balance]

## Metadata
- Model: [model used]
- Files analyzed: [count]
- Lines reviewed: [count]
```
