# Draft: Pixel Heart OS Development Environment Setup

## Requirements (confirmed)
- [frontend-stack]: Bun package manager, Vite, Svelte 5, Phaser 3
- [backend-stack]: Python 3.12, FastAPI, LangGraph, SQLAlchemy, ChromaDB
- [dev-tools]: Makefile with dev, test, lint, format, build, docker, db-init commands
- [docker]: Development stack with frontend, backend, chromadb services
- [environment]: .env.example with ANTHROPIC_API_KEY and other variables
- [tests]: Both backend (pytest) and frontend (vitest) tests
- [versions]: Latest stable versions
- [data]: Empty data directories (no sample files)

## Technical Decisions
- [eventbus-pattern]: Use EventBus for Svelte-Phaser communication (official Phaser template pattern)
- [ssr-disabled]: SSR must be disabled for Phaser integration (frontend/src/routes/+layout.js: export const ssr = false)
- [database-sqlite]: Use SQLite with Alembic migrations for development simplicity
- [docker-volumes]: Use named volumes for ChromaDB persistence
- [parallel-waves]: 3 waves for maximum parallelism (6 concurrent tasks max)

## Research Findings
- [phaser-svelte-template]: Official Phaser Svelte template shows exact configuration needed
- [fastapi-template]: FastAPI full-stack template shows backend structure patterns
- [alembic-patterns]: Alembic documentation provides migration setup steps
- [docker-patterns]: Docker Compose patterns for multi-service development stacks

## Open Questions
- None - all requirements confirmed and researched

## Scope Boundaries
- INCLUDE: Project directory structure, configuration files, dev tooling, test setup, Docker setup
- EXCLUDE: Actual feature implementation (beads system, LangGraph workflows, UI components)

## Test Strategy Decision
- [infrastructure-exists]: NO (will be created as part of this plan)
- [automated-tests]: YES (Tests-after - implementation first, then tests)
- [framework]: Backend: pytest, Frontend: vitest
- [agent-qa]: ALWAYS (mandatory for all tasks regardless of test choice)
