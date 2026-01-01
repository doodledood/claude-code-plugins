# Vibe Workflow Plugin

Autonomous development workflow with code review agents and quality gates.

## What It Does

- **Spec → Plan → Implement Pipeline** - Full autonomous development workflow:
  - `/spec` - Build requirements through interactive interview (EARS syntax)
  - `/plan` - Create mini-PR implementation plans with iterative codebase research
  - `/implement` - Execute plans autonomously chunk by chunk with auto-fix quality gates
- **Code Review** - Run `/review` to audit your changes for bugs, maintainability issues, type safety problems, documentation gaps, and test coverage
- **Codebase Explorer** - The `codebase-explorer` agent returns a structural overview + prioritized file list with line ranges - prefer over built-in Explore for context gathering
- **Bug Fixing** - Run `/bugfix` for systematic investigation with root cause analysis and test-driven verification
- **Web Research** - Run `/web-research` to research external topics with structured hypothesis tracking

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
