# Common File Glob Patterns for Consultant Queries

This reference provides common file selection patterns optimized for different types of consultant queries. The goal is to maximize **recall** - include all relevant context for comprehensive analysis.

## Security Audits

**Authentication & Authorization:**
```bash
--file "src/auth/**/*.ts" \
--file "src/middleware/auth*.ts" \
--file "src/middleware/permission*.ts" \
--file "src/guards/**/*.ts"
```

**API Security:**
```bash
--file "src/api/**/*.ts" \
--file "src/controllers/**/*.ts" \
--file "src/middleware/**/*.ts" \
--file "src/validators/**/*.ts" \
--file "!**/*.test.ts"
```

**Data Access Security:**
```bash
--file "src/db/**/*.ts" \
--file "src/models/**/*.ts" \
--file "src/repositories/**/*.ts" \
--file "src/services/database*.ts"
```

## Architectural Reviews

**Overall Architecture:**
```bash
--file "src/**/*.ts" \
--file "!**/*.test.ts" \
--file "!**/*.spec.ts" \
--file "README.md" \
--file "ARCHITECTURE.md" \
--file "package.json"
```

**Service Layer:**
```bash
--file "src/services/**/*.ts" \
--file "src/providers/**/*.ts" \
--file "src/adapters/**/*.ts" \
--file "!**/*.test.ts"
```

**API Design:**
```bash
--file "src/api/**/*.ts" \
--file "src/routes/**/*.ts" \
--file "src/controllers/**/*.ts" \
--file "src/dto/**/*.ts" \
--file "src/schemas/**/*.ts"
```

## Data Flow Analysis

**End-to-End Flow:**
```bash
--file "src/api/**/*.ts" \
--file "src/controllers/**/*.ts" \
--file "src/services/**/*.ts" \
--file "src/models/**/*.ts" \
--file "src/db/**/*.ts" \
--file "src/transformers/**/*.ts" \
--file "!**/*.test.ts"
```

**Event Flow:**
```bash
--file "src/events/**/*.ts" \
--file "src/handlers/**/*.ts" \
--file "src/listeners/**/*.ts" \
--file "src/subscribers/**/*.ts"
```

## Domain-Specific Analysis

**Feature Analysis:**
```bash
--file "src/features/<feature-name>/**/*.ts" \
--file "src/services/*<feature-name>*.ts" \
--file "src/models/*<feature-name>*.ts" \
--file "!**/*.test.ts"
```

**Module Analysis:**
```bash
--file "src/modules/<module-name>/**/*.ts" \
--file "!**/*.test.ts" \
--file "!**/node_modules/**"
```

## Error Handling & Resilience

**Error Handling:**
```bash
--file "src/**/*.ts" \
--file "!**/*.test.ts" \
| grep -E "(throw|catch|Error|Exception)"
```

**Logging & Monitoring:**
```bash
--file "src/**/*.ts" \
--file "src/logger/**/*.ts" \
--file "src/monitoring/**/*.ts" \
--file "!**/*.test.ts"
```

## Performance Analysis

**Query Performance:**
```bash
--file "src/db/**/*.ts" \
--file "src/repositories/**/*.ts" \
--file "src/models/**/*.ts" \
--file "src/services/**/*.ts"
```

**Caching Strategies:**
```bash
--file "src/**/*.ts" \
--file "src/cache/**/*.ts" \
--file "!**/*.test.ts" \
| grep -E "(cache|redis|memcache)"
```

## Testing & Quality

**Test Coverage Analysis:**
```bash
--file "src/**/*.test.ts" \
--file "src/**/*.spec.ts" \
--file "test/**/*.ts"
```

**Implementation vs Tests:**
```bash
--file "src/<feature>/**/*.ts" \
--file "test/<feature>/**/*.ts"
```

## Configuration & Infrastructure

**Configuration:**
```bash
--file "src/config/**/*.ts" \
--file "*.config.ts" \
--file "*.config.js" \
--file ".env.example" \
--file "tsconfig.json"
```

**Infrastructure as Code:**
```bash
--file "infrastructure/**/*" \
--file "*.tf" \
--file "docker-compose.yml" \
--file "Dockerfile" \
--file "k8s/**/*.yml"
```

## Frontend Analysis

**React Components:**
```bash
--file "src/components/**/*.{tsx,ts}" \
--file "src/hooks/**/*.ts" \
--file "src/contexts/**/*.tsx"
```

**State Management:**
```bash
--file "src/store/**/*.ts" \
--file "src/reducers/**/*.ts" \
--file "src/actions/**/*.ts" \
--file "src/selectors/**/*.ts"
```

## Exclusion Patterns

**Common exclusions:**
```bash
--file "!**/*.test.ts"        # Exclude tests
--file "!**/*.spec.ts"        # Exclude specs
--file "!**/node_modules/**"  # Exclude dependencies
--file "!**/dist/**"          # Exclude build output
--file "!**/*.d.ts"           # Exclude type declarations
--file "!**/coverage/**"      # Exclude coverage reports
```

## Multi-Project/Monorepo Patterns

**Specific Package:**
```bash
--file "packages/<package-name>/src/**/*.ts" \
--file "packages/<package-name>/package.json" \
--file "!**/*.test.ts"
```

**Cross-Package Analysis:**
```bash
--file "packages/*/src/**/*.ts" \
--file "packages/*/package.json" \
--file "!**/*.test.ts" \
--file "!**/node_modules/**"
```

## Tips for Effective File Selection

1. **Start broad, then narrow:** Begin with comprehensive globs, then add exclusions
2. **Include documentation:** Add README.md, ARCHITECTURE.md for context
3. **Include configuration:** Config files often reveal important patterns
4. **Exclude generated code:** Build outputs, type declarations add noise
5. **Include related tests selectively:** Useful for understanding behavior, but can add significant volume
6. **Use negation patterns:** `!` prefix to exclude specific patterns
7. **Check file count:** Use `--preview summary` to verify selection before sending
