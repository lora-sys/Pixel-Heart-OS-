# Draft: Pixel Heart OS

## Requirements (confirmed)
- User wants help implementing the Project Setup & Dev Environment for Pixel Heart OS
- Based on README.md: Project uses Bun for frontend, Python virtualenv for backend
- Need to set up development environment with all dependencies
- Project structure should match the one described in README.md section "Project Structure"

## Technical Decisions
- Frontend: Bun package manager, Vite, Svelte 5, Phaser 3
- Backend: Python 3.12, FastAPI, LangGraph, SQLAlchemy, ChromaDB
- Dev environment: Makefile for common commands, Docker compose for optional full-stack
- Environment variables: .env.example for configuration

## Research Findings
- From README: Prerequisites: Bun >=1.0, Python >=3.11, Anthropic API key
- From README: Setup steps: clone, bun install frontend, python -m venv backend, pip install -r requirements.txt, database init, run dev servers
- From index.html: No additional setup info
- From explore agents: 
  * Bun + Svelte + Phaser pattern: Use Vite with Svelte plugin, install phaser as dependency, set up EventBus for communication between Svelte and Phaser
  * Standard frontend structure: frontend/src/lib/ (stores, API client, EventBus), frontend/src/routes/ (Svelte pages), frontend/src/app.html (global styles)
  * Backend structure: backend/api/v1/ (routers), backend/services/ (business logic), backend/database/ (models), backend/beads/ (DAG engine), backend/graphs/ (LangGraph workflows)
  * Key backend dependencies: fastapi, langgraph, sqlalchemy, alembic, chromadb, anthropic, python-dotenv
  * Key frontend dependencies: bun, svelte, vite, phaser, @sveltejs/vite-plugin-svelte
  * Docker setup: Multi-stage build for frontend, separate backend service, shared volumes for data
  * Makefile patterns: dev-backend, dev-frontend, test, lint, format, build, docker-build, docker-run, db-init, sample-data

## Open Questions
- What specific versions of dependencies should be used? (e.g., Bun version, Python version, specific package versions)
- Should we include example data or just empty directories?
- Should the Makefile include specific commands for testing, linting, building?
- Should Docker compose be included for development or just production?

## Scope Boundaries
- INCLUDE: Creating directory structure, configuration files (package.json, requirements.txt, Makefile, docker-compose.yml, .env.example), initializing basic scripts
- EXCLUDE: Actual implementation of features (beads system, LangGraph, UI components), writing source code for backend/frontend logic