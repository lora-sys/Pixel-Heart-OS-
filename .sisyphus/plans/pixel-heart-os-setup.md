# Pixel Heart OS Development Environment Setup

## TL;DR

> **Quick Summary**: Set up a complete development environment for Pixel Heart OS with Bun-powered frontend (Svelte 5 + Phaser 3) and Python backend (FastAPI + LangGraph + SQLAlchemy + ChromaDB)
> 
> **Deliverables**:
> - Project directory structure matching README.md specification
> - Frontend: package.json, vite.config.ts, svelte.config.ts, EventBus setup
> - Backend: requirements.txt, pyproject.toml, alembic migrations, Docker configuration
> - Dev tooling: Makefile with dev/test/lint/format/build/docker commands
> - Environment: .env.example configuration
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Backend deps → Frontend deps → Integration & testing setup

---

## Context

### Original Request
User requested help implementing the Project Setup & Dev Environment for Pixel Heart OS based on the README.md and index.html files, focusing on setting up the development environment with all necessary dependencies and configurations.

### Interview Summary
**Key Discussions**:
- User wants to set up development environment matching the project structure in README.md
- Frontend: Bun package manager, Vite, Svelte 5, Phaser 3
- Backend: Python 3.12, FastAPI, LangGraph, SQLAlchemy, ChromaDB
- Dev environment: Makefile for common commands, Docker compose for optional full-stack
- Environment variables: .env.example for configuration
- Test strategy: Both backend (pytest) and frontend (vitest) tests
- Versions: Latest stable versions
- Data: Empty data directories (no sample files)
- Makefile: dev, test, lint, format, build, docker, db-init commands
- Docker: Development stack with frontend, backend, chromadb services

**Research Findings**:
- Bun + Svelte + Phaser pattern: Use Vite with Svelte plugin, EventBus for Svelte-Phaser communication, disable SSR
- Standard frontend structure: frontend/src/lib/ (stores, API client, EventBus), frontend/src/routes/ (Svelte pages), frontend/src/app.html (global styles)
- Backend structure: backend/api/v1/ (routers), backend/services/ (business logic), backend/database/ (models), backend/beads/ (DAG engine), backend/graphs/ (LangGraph workflows)
- Key backend dependencies: fastapi, langgraph, sqlalchemy, alembic, chromadb, anthropic, python-dotenv
- Key frontend dependencies: bun, svelte, vite, phaser, @sveltejs/vite-plugin-svelte
- Docker setup: Multi-stage build for frontend, separate backend service, shared volumes for data
- Makefile patterns: dev-backend, dev-frontend, test, lint, format, build, docker-build, docker-run, db-init, sample-data

### Metis Review
**Identified Gaps** (addressed):
- Missing Alembic migration setup for SQLAlchemy schema evolution
- Need explicit EventBus implementation details for Svelte-Phaser communication
- Missing environment variable examples for Anthropic API key and database configuration
- Need to specify exact versions for dependency reproducibility
- Missing test configuration files (pytest.ini, vitest.config.ts)

---

## Work Objectives

### Core Objective
Create a complete, reproducible development environment for Pixel Heart OS that allows developers to clone the repository and immediately start developing features with hot-reload, testing, and containerized dependencies.

### Concrete Deliverables
- Directory structure: frontend/, backend/, data/, .sisyphus/
- Configuration files: package.json, requirements.txt, pyproject.toml, vite.config.ts, svelte.config.ts, .env.example, docker-compose.yml, Makefile
- Setup scripts: Database initialization, dependency installation commands
- Test configuration: pytest.ini, vitest.config.ts
- Environment setup: .env.example with required variables

### Definition of Done
- [ ] Developer can run `make dev` to start both frontend and backend servers with hot-reload
- [ ] Developer can run `make test` to execute both backend and frontend tests
- [ ] Developer can run `make docker-run` to start full stack in containers
- [ ] Project structure matches specification from README.md
- [ ] All configuration files are present and functional

### Must Have
- Bun >=1.0 for frontend package management
- Python 3.12+ for backend
- EventBus pattern for Svelte-Phaser communication
- Alembic for database migrations
- Docker Compose for optional containerized development
- Test configuration for both frontend and backend

### Must NOT Have (Guardrails)
- No actual implementation of features (beads system, LangGraph, UI components) - this is setup only
- No hardcoded API keys or secrets in configuration files
- No Windows-specific paths or commands (use cross-platform solutions)
- No external service dependencies beyond what's in docker-compose
- No SSR (Server-Side Rendering) for Phaser integration (must be disabled)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.
> Acceptance criteria requiring "user manually tests/confirms" are FORBIDDEN.

### Test Decision
- **Infrastructure exists**: Will be created as part of this plan
- **Automated tests**: Tests-after (implementation first, then tests)
- **Framework**: Backend: pytest, Frontend: vitest
- **If TDD**: Not applicable - this is environment setup

### QA Policy
Every task MUST include agent-executed QA scenarios (see TODO template below).
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright (playwright skill) — Navigate, interact, assert DOM, screenshot
- **TUI/CLI**: Use interactive_bash (tmux) — Run command, send keystrokes, validates output, checks exit code
- **API/Backend**: Use Bash (curl) — Send requests, assert status + response fields
- **Library/Module**: Use Bash (bun/node REPL) — Import, call functions, compare output

---

## Execution Strategy

### Parallel Execution Waves

> Maximize throughput by grouping independent tasks into parallel waves.
> Each wave completes before the next begins.
> Target: 5-8 tasks per wave. Fewer than 3 per wave (except final) = under-splitting.

```
Wave 1 (Start Immediately — foundation + scaffolding):
├── Task 1: Create project directory structure [quick]
├── Task 2: Setup frontend configuration (package.json, vite.config.ts) [quick]
├── Task 3: Setup backend configuration (requirements.txt, pyproject.toml) [quick]
├── Task 4: Create .env.example with required variables [quick]
├── Task 5: Setup basic Makefile with dev commands [quick]
└── Task 6: Create empty data directories [quick]

Wave 2 (After Wave 1 — core modules, MAX PARALLEL):
├── Task 7: Setup Svelte configuration (svelte.config.ts, tsconfig.json) [unspecified-high]
├── Task 8: Setup Phaser integration with EventBus [unspecified-high]
├── Task 9: Setup backend services structure (api/, services/, database/, graphs/) [unspecified-high]
├── Task 10: Configure Alembic for SQLAlchemy migrations [deep]
├── Task 11: Setup Docker Compose for development stack [unspecified-high]
├── Task 12: Configure test frameworks (pytest.ini, vitest.config.ts) [quick]
└── Task 13: Add linting and formatting configs (ruff, black, prettier) [quick]

Wave 3 (After Wave 2 — integration + verification):
├── Task 14: Verify frontend can start with bun run dev [deep]
├── Task 15: Verify backend can start with uvicorn [deep]
├── Task 16: Verify Docker Compose starts all services [deep]
├── Task 17: Run backend tests to confirm setup [deep]
├── Task 18: Run frontend tests to confirm setup [deep]
└── Task 19: Final documentation update with usage instructions [quick]

Critical Path: Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9 → Task 10 → Task 11 → Task 12 → Task 13 → Task 14 → Task 15 → Task 16 → Task 17 → Task 18 → Task 19
Parallel Speedup: ~65% faster than sequential
Max Concurrent: 6 (Waves 1 & 2)
```

### Dependency Matrix (abbreviated — show ALL tasks in your generated plan)

- **1**: — — 2,3,4,5,6
- **2**: 1 — 7,8
- **3**: 1 — 9,10
- **4**: 1 — 11
- **5**: 1 — 12,13
- **6**: 1 —
- **7**: 2 — 14
- **8**: 2,9 — 14
- **9**: 3,6 — 10,11,14
- **10**: 9 — 11,15
- **11**: 4,9,10 — 16
- **12**: 5 — 17,18
- **13**: 5 — 17,18
- **14**: 7,8,9 — 17
- **15**: 10,11 — 17
- **16**: 11,14,15 — 17,18
- **17**: 12,13,14,15,16 — 18,19
- **18**: 12,13,16 — 19
- **19**: 17,18 —

### Agent Dispatch Summary

- **1**: **6** — T1-T6 → `quick`
- **2**: **4** — T2 → `quick`, T3 → `quick`, T4 → `quick`, T5 → `quick`, T6 → `quick`, T7 → `unspecified-high`, T8 → `unspecified-high`, T9 → `unspecified-high`, T10 → `deep`, T11 → `unspecified-high`, T12 → `quick`, T13 → `quick`
- **3**: **6** — T14 → `deep`, T15 → `deep`, T16 → `deep`, T17 → `deep`, T18 → `deep`, T19 → `quick`

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.
> **A task WITHOUT QA Scenarios is INCOMPLETE. No exceptions.**

- [x] 1. Create project directory structure

  **What to do**:
  - Create directories: frontend/, backend/, data/, .sisyphus/
  - Create subdirectories: frontend/src/{lib,routes}, backend/{api/v1,services,beads,graphs,database,storage,vector_store,prompts,core}
  - Create data subdirectories: data/heroine/, data/npcs/, data/scenes/
  - Ensure .sisyphus/plans/ and .sisyphus/drafts/ directories exist

  **Must NOT do**:
  - Create any source code files (.ts, .js, .py, etc.) - this is structure only
  - Initialize git repositories or make commits

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Simple directory creation task requiring no complex logic or domain expertise
  - **Skills**: `[]`
    - No special skills needed for basic directory creation

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2,3,4,5,6)
  - **Blocks**: Tasks 2-13 (all configuration tasks depend on directory structure)
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `README.md:101-130` - Project structure specification showing frontend/, backend/, data/ directories

  **API/Type References** (contracts to implement against):
  - None - this is infrastructure setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Official Bun documentation: https://bun.sh/guides/install - For understanding Bun project initialization

  **WHY Each Reference Matters** (explain the relevance):
  - README.md lines 101-130 show the exact project structure that must be implemented, including frontend/, backend/, and data/ directories with their subdirectories

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: find frontend backend data .sisyphus -type d | sort
      2. Verify output contains: backend, backend/api/v1, backend/services, data, data/heroine, data/npcs, data/scenes, frontend, frontend/src, frontend/src/lib, frontend/src/routes, .sisyphus, .sisyphus/plans, .sisyphus/drafts
    Expected Result: All required directories exist with correct structure
    Failure Indicators: Missing any of the required directories or incorrect nesting
    Evidence: .sisyphus/evidence/task-1-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: test -d frontend/src/lib && echo "PASS" || echo "FAIL"
      2. This should PASS since we just created it
      3. Execute: rm -rf frontend/src/lib
      4. Execute: test -d frontend/src/lib && echo "PASS" || echo "FAIL"
    Expected Result: First test PASSES, second test FAILS (directory was removed)
    Failure Indicators: Both tests PASS or both FAIL
    Evidence: .sisyphus/evidence/task-1-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(project): create directory structure`
  - Files: 
  - Pre-commit: `echo "Directory structure validation passed"`

- [x] 2. Setup frontend configuration (package.json, vite.config.ts)

  **What to do**:
  - Create frontend/package.json with Bun as package manager, Vite, Svelte, and Phaser dependencies
  - Create frontend/vite.config.ts with Svelte plugin configuration and Phaser optimization
  - Include scripts for dev, build, preview, and type checking
  - Set type to "module" for ES modules support

  **Must NOT do**:
  - Include actual source code or components
  - Use npm or yarn - must use Bun
  - Include Phaser in devDependencies (should be regular dependency)

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Configuration file creation with well-defined patterns from official templates
  - **Skills**: `[]`
    - Standard web configuration task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1,3,4,5,6)
  - **Blocks**: Tasks 7,8,14 (Svelte config, Phaser integration, frontend verification depend on this)
  - **Blocked By**: Task 1 (directory structure must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/package.json
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/vite.config.ts

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Bun documentation: https://bun.sh/guides/package-managers/creating-a-new-project - For Bun project initialization
  - Vite documentation: https://vitejs.dev/config/ - For Vite configuration
  - Svelte documentation: https://svelte.dev/docs/kit/configuration - For Svelte configuration

  **WHY Each Reference Matters** (explain the relevance):
  - Official Phaser Svelte template shows the exact configuration needed for Bun + Vite + Svelte + Phaser integration
  - Bun documentation ensures we use the correct package manager as specified in requirements
  - Vite and Svelte documentation provide the correct configuration patterns for optimal setup

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: bun install
      2. Execute: bun run dev -- --port 5173 & 
      3. Execute: sleep 10 (give dev server time to start)
      4. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      5. Execute: kill %1 (stop the background process)
    Expected Result: Dev server starts without dependency errors, serves basic HTML
    Failure Indicators: Dependency installation fails, dev server fails to start, or server returns error status
    Evidence: .sisyphus/evidence/task-2-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: echo "{ invalid json }" > package.json.broken
      2. Execute: bun install 2>&1 | grep -i "error\|fail" || echo "NO ERROR"
      3. Execute: rm package.json.broken
    Expected Result: bun install should fail with JSON parsing error when given invalid package.json
    Failure Indicators: bun install succeeds with invalid JSON or doesn't show error for invalid JSON
    Evidence: .sisyphus/evidence/task-2-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(frontend): add package.json and vite.config.ts`
  - Files: frontend/package.json, frontend/vite.config.ts
  - Pre-commit: `bun --version && echo "Bun version check passed"`

- [x] 3. Setup backend configuration (requirements.txt, pyproject.toml)

  **What to do**:
  - Create backend/requirements.txt with FastAPI, LangGraph, SQLAlchemy, ChromaDB, and other dependencies
  - Create backend/pyproject.toml with project metadata and tool configurations (ruff, black, pytest)
  - Include version ranges for reproducible builds
  - Add development dependencies for testing and linting

  **Must NOT do**:
  - Include actual source code or implementation
  - Pin to exact versions that may cause conflicts
  - Include optional dependencies without explanation

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Configuration file creation with well-defined patterns from Python ecosystem
  - **Skills**: `[]`
    - Standard Python configuration task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1,2,4,5,6)
  - **Blocks**: Tasks 9,10,15 (backend services, Alembic, backend verification depend on this)
  - **Blocked By**: Task 1 (directory structure must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - Official FastAPI template: https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7B cookiecutter.project_slug %7D%7D/backend/requirements.txt
  - Official Python project: https://github.com/astral-sh/ruff/blob/master/pyproject.toml

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - FastAPI documentation: https://fastapi.tiangolo.com/ - For understanding FastAPI dependencies
  - SQLAlchemy documentation: https://docs.sqlalchemy.org/ - For SQLAlchemy async setup
  - LangGraph documentation: https://langchain-ai.github.io/langgraph/ - For LangGraph installation
  - ChromaDB documentation: https://docs.trychroma.com/ - For ChromaDB client
  - Ruff documentation: https://docs.astral.sh/ruff/ - For linting configuration
  - Black documentation: https://black.readthedocs.io/ - For formatting configuration

  **WHY Each Reference Matters** (explain the relevance):
  - These references show established patterns for configuring Python projects with the exact technologies needed for Pixel Heart OS
  - They ensure we follow community best practices for dependency management and tool configuration

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: pip install -r requirements.txt
      2. Execute: python -c "import fastapi; import langgraph; import sqlalchemy; import chromadb; print('All imports successful')"
      3. Execute: pip list | grep -E "(fastapi|langgraph|sqlalchemy|chromadb)" | wc -l
    Expected Result: All dependencies install successfully and can be imported
    Failure Indicators: Installation fails, import errors, or wrong number of packages installed
    Evidence: .sisyphus/evidence/task-3-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: echo "invalid-package-name==1.0.0" >> requirements.txt.bak
      2. Execute: cp requirements.txt requirements.txt.backup
      3. Execute: echo "invalid-package-name==1.0.0" >> requirements.txt
      4. Execute: pip install -r requirements.txt 2>&1 | grep -i "error\|not found\|failed" || echo "NO ERROR FOUND"
      5. Execute: mv requirements.txt.backup requirements.txt
    Expected Result: pip install should fail when trying to install invalid package
    Failure Indicators: pip succeeds with invalid package or doesn't show error for invalid package
    Evidence: .sisyphus/evidence/task-3-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(backend): add requirements.txt and pyproject.toml`
  - Files: backend/requirements.txt, backend/pyproject.toml
  - Pre-commit: `python --version && echo "Python version check passed"`

- [x] 4. Create .env.example with required variables

  **What to do**:
  - Create backend/.env.example with example environment variables
  - Include ANTHROPIC_API_KEY, DATABASE_URL, DEBUG, and other necessary variables
  - Add comments explaining each variable's purpose
  - Ensure no actual secrets are included

  **Must NOT do**:
  - Include actual API keys or secrets
  - Include production-specific settings that should be overridden
  - Make the file executable or modify permissions unnecessarily

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Simple environment file creation with well-defined patterns
  - **Skills**: `[]`
    - Standard configuration task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1,2,3,5,6)
  - **Blocks**: Tasks 11,16 (Docker setup and verification depend on environment variables)
  - **Blocked By**: Task 1 (directory structure must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:65-71 - Environment configuration instructions showing ANTHROPIC_API_KEY
  - Official Python-dotenv examples: https://saurabh-kumar.com/python-dotenv/ for .env.example patterns

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Python-dotenv documentation: https://pypi.org/project/python-dotenv/ - For understanding .env file format
  - FastAPI environment variables: https://fastapi.tiangolo.com/tutorial/environment-variables/ - For FastAPI env var usage

  **WHY Each Reference Matters** (explain the relevance):
  - README shows exactly which environment variables are needed (ANTHROPIC_API_KEY)
  - Python-dotenv documentation ensures we follow standard practices for environment files
  - FastAPI documentation shows how these variables will be used in the application

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: cp .env.example .env
      2. Execute: echo "ANTHROPIC_API_KEY=test_key_123" >> .env
      3. Execute: echo "DEBUG=true" >> .env
      4. Execute: python -c "from dotenv import load_dotenv; load_dotenv(); import os; assert os.getenv('ANTHROPIC_API_KEY') == 'test_key_123'; assert os.getenv('DEBUG') == 'true'; print('Environment variables loaded correctly')"
    Expected Result: Environment file loads correctly and variables are accessible
    Failure Indicators: File doesn't load, variables not found, or incorrect values
    Evidence: .sisyphus/evidence/task-4-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: echo "NOT_A_VALID_ENV_VAR=value" > .env.bad
      2. Execute: python -c "from dotenv import load_dotenv; load_dotenv('.env.bad'); import os; print(os.getenv('NOT_A_VALID_ENV_VAR', 'NOT_FOUND'))" 2>&1 | grep -i "error\|exception\|traceback" || echo "NO ERROR"
      3. Execute: rm .env.bad
    Expected Result: Loading invalid env file should not crash but may not set the variable
    Failure Indicators: Python throws an exception when loading the env file
    Evidence: .sisyphus/evidence/task-4-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(backend): add .env.example`
  - Files: backend/.env.example
  - Pre-commit: `test -f backend/.env.example && echo ".env.example file exists"`

- [x] 5. Setup basic Makefile with dev commands

  **What to do**:
  - Create Makefile with dev, test, lint, format, build, and help targets
  - Include dev-backend and dev-frontend targets for separate server startup
  - Add docker-build and docker-run targets for containerized development
  - Include db-init for database initialization

  **Must NOT do**:
  - Include actual source code compilation or complex build steps
  - Assume specific IDEs or editors
  - Include platform-specific commands without fallbacks

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Makefile creation with well-defined patterns from development tooling
  - **Skills**: `[]`
    - Standard build automation task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1,2,3,4,6)
  - **Blocks**: Tasks 12,13,14,15,16,17,18,19 (testing, linting, verification depend on Makefile)
  - **Blocked By**: Task 1 (directory structure must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing make lint, make format, make build, docker-compose up -d
  - Official Makefile documentation: https://www.gnu.org/software/make/manual/make.html for syntax and patterns

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - GNU Make documentation: https://www.gnu.org/software/make/ - For Makefile syntax and best practices
  - Docker documentation: https://docs.docker.com/compose/ - For docker-compose usage in Makefile
  - Bun documentation: https://bun.sh/guides/cli - For Bun commands in Makefile
  - Python documentation: https://docs.python.org/3/library/subprocess.html - For running Python commands

  **WHY Each Reference Matters** (explain the relevance):
  - README shows exactly which Makefile targets are expected (lint, format, build, docker)
  - GNU Make documentation ensures we follow proper Makefile syntax and conventions
  - Docker and Bun documentation show how to integrate these tools into Makefile targets

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: make help
      2. Execute: make dev-backend 2>&1 | head -20
      3. Execute: sleep 5 (give time to start seeing if it fails immediately)
      4. Execute: pkill -f "uvicorn" || true (cleanup)
    Expected Result: make help shows available targets, dev-backend starts without immediate errors
    Failure Indicators: make command not found, targets missing, or immediate failure to start
    Evidence: .sisyphus/evidence/task-5-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: echo "invalid-target:" > Makefile.test
      2. Execute: make -f Makefile.test invalid-target 2>&1 | grep -i "error\|unknown\|not found" || echo "NO ERROR"
      3. Execute: rm -f Makefile.test
    Expected Result: make should show error for invalid target or missing dependency
    Failure Indicators: make succeeds with invalid target or doesn't show error for invalid Makefile syntax
    Evidence: .sisyphus/evidence/task-5-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(dev): add Makefile with dev commands`
  - Files: Makefile
  - Pre-commit: `make --version && echo "Make version check passed"`

- [x] 6. Create empty data directories

  **What to do**:
  - Create data/heroine/, data/npcs/, data/scenes/ directories
  - Ensure they are empty (no sample files)
  - Add .gitkeep files if needed to track empty directories in git
  - Verify they match the structure from README.md

  **Must NOT do**:
  - Add any sample data, stories, or example files
  - Initialize git repositories in these directories
  - Add any configuration or metadata files

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Simple directory creation task requiring no complex logic
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1,2,3,4,5)
  - **Blocks**: Tasks 9,11 (backend services and Docker setup may reference these directories)
  - **Blocked By**: Task 1 (directory structure must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:122-125 - Project structure showing data/ with heroine/, npcs/, scenes/ subdirectories
  - README.md:76-78 - Database init section showing data directory usage

  **API/Type References** (contracts to implement against):
  - None - this is infrastructure setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Git documentation: https://git-scm.com/docs/gitignore#_how_to_ignore - For .gitkeep patterns
  - Linux Filesystem Hierarchy Standard: https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html - For data directory purpose

  **WHY Each Reference Matters** (explain the relevance):
  - README shows exactly what data directory structure is required
  - Git documentation shows how to track empty directories if needed
  - FHS explains the purpose of /var/lib-like directories for application data

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: find data -type f | wc -l
      2. Execute: ls -la data/heroine/ data/npcs/ data/scenes/
    Expected Result: Zero files in data subdirectories, directories exist and are readable
    Failure Indicators: Any files found in data subdirectories, missing directories, or permission errors
    Evidence: .sisyphus/evidence/task-6-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: touch data/heroine/sample.txt
      2. Execute: find data -type f | wc -l
      3. Execute: rm data/heroine/sample.txt
      4. Execute: find data -type f | wc -l
    Expected Result: First find shows 1 file, second find shows 0 files
    Failure Indicators: Both counts are the same, or file creation/deletion fails
    Evidence: .sisyphus/evidence/task-6-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(data): create empty data directories`
  - Files: data/heroine/, data/npcs/, data/scenes/
  - Pre-commit: `ls -la data/ && echo "Data directory structure verified"`

- [x] 7. Setup Svelte configuration (svelte.config.ts, tsconfig.json)

  **What to do**:
  - Create frontend/svelte.config.ts with SvelteKit configuration
  - Create frontend/tsconfig.json for TypeScript support
  - Configure alias paths for $lib and $phaser
  - Set up preprocess with vite-plugin-svelte

  **Must NOT do**:
  - Include actual source code or components
  - Configure SSR (must be disabled for Phaser integration)
  - Include project-specific settings that belong in vite.config.ts

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: Configuration requires understanding of SvelteKit specifics and TypeScript integration
  - **Skills**: `[]`
    - Standard frontend configuration task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8,9,10,11,12,13)
  - **Blocks**: Task 14 (frontend verification depends on Svelte config)
  - **Blocked By**: Task 2 (frontend package.json and vite.config.ts must exist first)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/svelte.config.js
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/tsconfig.json

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Svelte documentation: https://svelte.dev/docs/kit/configuration - For SvelteKit configuration
  - TypeScript documentation: https://www.typescriptlang.org/tsconfig - For tsconfig options
  - Vite documentation: https://vitejs.dev/config/ - For Vite plugin configuration

  **WHY Each Reference Matters** (explain the relevance):
  - Official Phaser Svelte template shows the exact configuration needed for Bun + Vite + Svelte + Phaser
  - Svelte and TypeScript documentation ensure we use correct configuration patterns
  - Vite documentation shows how to properly configure the Svelte plugin

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: bunx svelte-kit sync
      2. Execute: bunx svelte-check --tsconfig ./tsconfig.json
      3. Execute: bun run dev -- --port 5173 & 
      4. Execute: sleep 10 (give dev server time to start)
      5. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      6. Execute: kill %1 (stop the background process)
    Expected Result: Svelte checks pass, dev server starts without errors
    Failure Indicators: Svelte check fails, dev server fails to start, or server returns error status
    Evidence: .sisyphus/evidence/task-7-happy.txt
  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: echo "invalid json" > svelte.config.bad.ts
      2. Execute: bunx svelte-check --tsconfig ./tsconfig.json 2>&1 | grep -i "error\|fail\|exception" || echo "NO ERROR"
      3. Execute: rm svelte.config.bad.ts
    Expected Result: svelte-check should fail with parsing error for invalid TypeScript
    Failure Indicators: svelte-check succeeds with invalid TypeScript or doesn't show error
    Evidence: .sisyphus/evidence/task-7-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API
  **Commit**: NO
  - Message: `chore(frontend): add svelte.config.ts and tsconfig.json`
  - Files: frontend/svelte.config.ts, frontend/tsconfig.json
  - Pre-commit: `bunx svelte-check --tsconfig ./tsconfig.json && echo "Svelte TypeScript check passed"`

- [x] 8. Setup Phaser integration with EventBus

  **What to do**:
  - Create frontend/src/lib/event-bus.ts for Svelte-Phaser communication
  - Create frontend/src/lib/PhaserGame.svelte component
  - Create frontend/src/phaser/main.ts for Phaser game configuration
  - Create frontend/src/phaser/scenes/ directory for game scenes
  - Update frontend/src/routes/+layout.svelte to include PhaserGame component
  - Create frontend/src/routes/+layout.js to disable SSR (ssr = false)

  **Must NOT do**:
  - Include actual game logic or scene implementations
  - Use virtual DOM approaches that conflict with Phaser
  - Include SSR-enabled layouts (must be disabled for Phaser)
  - Hardcode game dimensions or asset paths

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: Requires understanding of both Svelte and Phaser integration patterns
  - **Skills**: `["frontend-design"]`
    - Need frontend design skills for proper Svelte-Phaser integration

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,9,10,11,12,13)
  - **Blocks**: Task 14 (frontend verification depends on Phaser integration)
  - **Blocked By**: Task 2 (frontend configuration must exist), Task 7 (Svelte config needed for TypeScript)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/src/lib/event-bus.ts
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/src/lib/PhaserGame.svelte
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/src/phaser/main.ts
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/src/routes/+layout.svelte
  - Official Phaser Svelte template: https://github.com/phaserjs/template-svelte/blob/main/src/routes/+layout.js

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Phaser documentation: https://phaser.io/phaser3/api - For Phaser game configuration
  - Svelte documentation: https://svelte.dev/docs - For Svelte component syntax
  - Vite documentation: https://vitejs.dev/guide/ - For Vite setup with Svelte

  **WHY Each Reference Matters** (explain the relevance):
  - Official Phaser Svelte template shows the exact implementation needed for proper integration
  - Phaser documentation ensures we use correct game configuration patterns
  - Svelte documentation shows how to create components that work with Phaser via EventBus

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: bun run dev -- --port 5173 & 
      2. Execute: sleep 15 (give dev server time to start)
      3. Execute: curl -s http://localhost:5173 | grep -i "phaser" || echo "NOT FOUND"
      4. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      5. Execute: kill %1 (stop the background process)
    Expected Result: Dev server starts, serves page containing both Phaser and Pixel Heart OS references
    Failure Indicators: Dev server fails to start, or server returns error status, or missing expected content
    Evidence: .sisyphus/evidence/task-8-happy.txt
  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: echo "export const ssr = true;" > src/routes/+layout.js.bad
      2. Execute: cp src/routes/+layout.js src/routes/+layout.js.backup
      3. Execute: mv src/routes/+layout.js.bad src/routes/+layout.js
      4. Execute: bun run dev -- --port 5173 & 
      5. Execute: sleep 10
      6. Execute: curl -s http://localhost:5173 2>&1 | grep -i "error\|exception\|500" || echo "NO SERVER ERROR"
      7. Execute: kill %1 (stop the background process)
      8. Execute: mv src/routes/+layout.js.backup src/routes/+layout.js
    Expected Result: With SSR enabled, server should show error or fail to start properly with Phaser
    Failure Indicators: Server starts successfully with SSR enabled for Phaser (should fail)
    Evidence: .sisyphus/evidence/task-8-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(frontend): add Phaser integration with EventBus`
  - Files: frontend/src/lib/event-bus.ts, frontend/src/lib/PhaserGame.svelte, frontend/src/phaser/main.ts, frontend/src/routes/+layout.svelte, frontend/src/routes/+layout.js
  - Pre-commit: `ls -la frontend/src/lib/ && ls -la frontend/src/phaser/ && ls -la frontend/src/routes/ && echo "Phaser integration files created"`

- [x] 9. Setup backend services structure (api/, services/, database/, graphs/)

  **What to do**:
  - Create backend/api/v1/ directory with placeholder endpoint files
  - Create backend/services/ directory with placeholder service files
  - Create backend/database/ directory with placeholder model files
  - Create backend/graphs/ directory with placeholder workflow files
  - Create backend/storage/, backend/vector_store/, backend/prompts/, backend/core/ directories
  - Create __init__.py files in all Python packages to make them importable

  **Must NOT do**:
  - Include actual implementation of business logic
  - Include complex database models or API endpoints
  - Include actual LangGraph workflow implementations
  - Include actual bead system or NPC generation logic

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: Requires understanding of Python package structure and backend architecture
  - **Skills**: `[]`
    - Standard backend structure setup task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,8,10,11,12,13)
  - **Blocks**: Tasks 10,15 (Alembic setup and backend verification depend on this structure)
  - **Blocked By**: Task 3 (backend configuration must exist), Task 1 (directory structure must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:104-111 - Backend structure showing api/v1/, beads/, database/, graphs/, llm/, storage/, vector_store/, prompts/, scripts/, pyproject.toml, main.py
  - Official Python packaging guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/ for __init__.py usage

  **API/Type References** (contracts to implement against):
  - None - this is configuration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Python packaging documentation: https://docs.python.org/3/distributing/ - For package structure
  - FastAPI project generation: https://fastapi.tiangolo.com/tutorial/project-generation/ - For FastAPI structure
  - SQLAlchemy documentation: https://docs.sqlalchemy.org/en/20/tutorial/ - For defining models

  **WHY Each Reference Matters** (explain the relevance):
  - README shows the exact backend structure that must be implemented
  - Python packaging documentation ensures we follow proper package structure with __init__.py files
  - FastAPI and SQLAlchemy documentation show how to structure the backend components

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: find backend -name "*.py" | head -5
      2. Execute: ls -la backend/api/v1/ backend/services/ backend/database/ backend/graphs/
      3. Execute: test -f backend/api/v1/__init__.py && echo "API package valid" || echo "INVALID"
      4. Execute: test -f backend/services/__init__.py && echo "Services package valid" || echo "INVALID"
    Expected Result: All required directories exist with __init__.py files, basic Python package structure
    Failure Indicators: Missing directories, missing __init__.py files, or incorrect structure
    Evidence: .sisyphus/evidence/task-9-happy.txt
  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: echo "not a python file" > backend/api/v1/not_a_module.txt
      2. Execute: python -c "import backend.api.v1.not_a_module" 2>&1 | grep -i "error\|module\|import" || echo "NO IMPORT ERROR"
      3. Execute: rm backend/api/v1/not_a_module.txt
    Expected Result: Import should fail for non-Python file
    Failure Indicators: Import succeeds for non-Python file or doesn't show import error
    Evidence: .sisyphus/evidence/task-9-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(backend): add services structure`
  - Files: backend/api/v1/__init__.py, backend/services/__init__.py, backend/database/__init__.py, backend/graphs/__init__.py, backend/storage/__init__.py, backend/vector_store/__init__.py, backend/prompts/__init__.py, backend/core/__init__.py
  - Pre-commit: `python -c "import backend.api.v1; import backend.services; import backend.database; print('Backend packages importable')"`

- [x] 10. Configure Alembic for SQLAlchemy migrations

  **What to do**:
  - Create backend/alembic/ directory structure with alembic init
  - Configure alembic.ini with database URL (SQLite by default)
  - Create migration scripts directory and environment.py
  - Configure alembic to use SQLAlchemy models from backend.database.models
  - Create initial migration that creates all database tables
  - Add alembic commands to Makefile (db-init, db-migrate, db-upgrade)

  **Must NOT do**:
  - Hardcode actual database credentials
  - Include production database URLs
  - Modify existing database files during setup

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `deep`
    - Reason: Requires understanding of Alembic migration system and SQLAlchemy integration
  - **Skills**: `[]`
    - Standard database migration setup task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,8,9,11,12,13)
  - **Blocks**: Task 11,15 (Docker setup and backend verification depend on migrations)
  - **Blocked By**: Task 9 (backend services structure must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing db-init command
  - Official Alembic documentation: https://alembic.sqlalchemy.org/en/latest/tutorial.html

  **API/Type References** (contracts to implement against):
  - None - this is migration setup

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Alembic documentation: https://alembic.sqlalchemy.org - For migration setup
  - SQLAlchemy async documentation: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html - For async session setup
  - Python-dotenv documentation: https://pypi.org/project/python-dotenv/ - For environment variable loading

  **WHY Each Reference Matters** (explain the relevance):
  - README shows db-init command is expected in Makefile
  - Alembic documentation provides the exact steps for setting up migrations with SQLAlchemy

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: source .venv/bin/activate 2>/dev/null || echo "Venv not active"
      2. Execute: python -m alembic upgrade head 2>&1 | head -10
      3. Execute: ls -la alembic/versions/ | head -5
      4. Execute: sqlite3 instance/app.db ".tables" 2>&1 | head -5
    Expected Result: Alembic runs successfully, creates version files, database tables exist
    Failure Indicators: Alembic fails, no migration files created, or database tables missing
    Evidence: .sisyphus/evidence/task-10-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: cp alembic.ini alembic.ini.backup
      2. Execute: echo "invalid_config = " > alembic.ini
      3. Execute: python -m alembic current 2>&1 | grep -i "error\|invalid\|exception" || echo "NO ERROR"
      4. Execute: mv alembic.ini.backup alembic.ini
    Expected Result: Alembic should show error for invalid alembic.ini configuration
    Failure Indicators: Alembic succeeds with invalid config or doesn't show error
    Evidence: .sisyphus/evidence/task-10-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(backend): setup Alembic migrations`
  - Files: backend/alembic/, backend/alembic.ini, backend/instance/
  - Pre-commit: `python -m alembic current && echo "Alembic configured successfully"`

- [x] 11. Setup Docker Compose for development stack

  **What to do**:
  - Create docker-compose.yml with frontend, backend, and chromadb services
  - Configure frontend service with Bun and Vite dev server
  - Configure backend service with Uvicorn and hot reload
  - Configure chromadb service with persistent volume
  - Add health checks and dependency ordering
  - Create Dockerfile for frontend (multi-stage build)
  - Create Dockerfile for backend

  **Must NOT do**:
  - Include production secrets or hardcoded credentials
  - Use latest tag for images (use specific versions)
  - Expose unnecessary ports

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: Requires understanding of Docker Compose and container orchestration
  - **Skills**: `[]`
    - Standard containerization task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,8,9,10,12,13)
  - **Blocks**: Task 16 (Docker verification depends on this)
  - **Blocked By**: Task 4 (environment variables), Task 9 (backend structure), Task 10 (Alembic setup)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:101-130 - Project structure showing docker-compose.yml
  - README.md:171-180 - Development section showing docker-compose up -d

  **API/Type References** (contracts to implement against):
  - None - this is container configuration

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Docker Compose documentation: https://docs.docker.com/compose/ - For compose file syntax
  - Docker documentation: https://docs.docker.com/ - For Dockerfile creation
  - Bun documentation: https://bun.sh/guides/docker - For Bun in Docker

  **WHY Each Reference Matters** (explain the relevance):
  - README shows docker-compose.yml is expected and docker-compose up -d is a development command
  - Docker documentation provides the exact patterns for multi-service development stacks

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: docker-compose config --services
      2. Execute: docker-compose up -d
      3. Execute: sleep 15
      4. Execute: docker-compose ps
      5. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      6. Execute: docker-compose down
    Expected Result: All services start, frontend accessible on port 5173
    Failure Indicators: Services fail to start, health checks fail, or ports not accessible
    Evidence: .sisyphus/evidence/task-11-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cp docker-compose.yml docker-compose.yml.backup
      2. Execute: echo "invalid yaml: [" > docker-compose.yml
      3. Execute: docker-compose config 2>&1 | grep -i "error\|invalid\|yaml" || echo "NO ERROR"
      4. Execute: mv docker-compose.yml.backup docker-compose.yml
    Expected Result: docker-compose config should fail with YAML parsing error
    Failure Indicators: docker-compose succeeds with invalid YAML or doesn't show error
    Evidence: .sisyphus/evidence/task-11-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(docker): setup development stack`
  - Files: docker-compose.yml, Dockerfile, Dockerfile.frontend
  - Pre-commit: `docker-compose config && echo "Docker Compose configuration valid"`

- [x] 12. Configure test frameworks (pytest.ini, vitest.config.ts)

  **What to do**:
  - Create backend/pytest.ini with test configuration
  - Create frontend/vitest.config.ts with test configuration
  - Configure coverage thresholds and test directories
  - Add test scripts to package.json and pyproject.toml
  - Create example test files to verify setup

  **Must NOT do**:
  - Include actual feature tests (this is setup only)
  - Configure test frameworks to skip important checks

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Standard test configuration with well-defined patterns
  - **Skills**: `[]`
    - Standard test setup task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,8,9,10,11,13)
  - **Blocks**: Tasks 17,18 (test execution depends on configuration)
  - **Blocked By**: Task 5 (Makefile must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing test commands
  - Official pytest documentation: https://docs.pytest.org/en/stable/
  - Official vitest documentation: https://vitest.dev/config/

  **API/Type References** (contracts to implement against):
  - None - this is test configuration

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - pytest documentation: https://docs.pytest.org - For pytest configuration
  - vitest documentation: https://vitest.dev - For vitest configuration

  **WHY Each Reference Matters** (explain the relevance):
  - README shows make test command is expected
  - Official documentation provides correct configuration patterns

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cd backend && python -m pytest --collect-only 2>&1 | head -10
      2. Execute: cd ../frontend && bunx vitest run --reporter=verbose 2>&1 | head -10
    Expected Result: Test frameworks can discover and collect tests without errors
    Failure Indicators: pytest or vitest fails to collect tests or shows configuration errors
    Evidence: .sisyphus/evidence/task-12-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cd backend && cp pytest.ini pytest.ini.backup
      2. Execute: echo "invalid config" > pytest.ini
      3. Execute: python -m pytest --collect-only 2>&1 | grep -i "error\|invalid\|exception" || echo "NO ERROR"
      4. Execute: mv pytest.ini.backup pytest.ini
    Expected Result: pytest should show error for invalid configuration
    Failure Indicators: pytest succeeds with invalid config or doesn't show error
    Evidence: .sisyphus/evidence/task-12-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(test): configure test frameworks`
  - Files: backend/pytest.ini, frontend/vitest.config.ts
  - Pre-commit: `cd backend && python -m pytest --version && cd ../frontend && bunx vitest --version`

- [x] 13. Add linting and formatting configs (ruff, black, prettier)

  **What to do**:
  - Create backend/pyproject.toml sections for ruff and black configuration
  - Create frontend/.prettierrc for Prettier configuration
  - Add lint and format commands to Makefile
  - Configure ruff with common rules (E, F, B, I, N, UP, PL, RUF)
  - Configure black with line length 88
  - Configure Prettier with Svelte plugin

  **Must NOT do**:
  - Include project-specific linting rules that belong in code
  - Configure linting to ignore important errors

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Standard linting configuration with well-defined patterns
  - **Skills**: `[]`
    - Standard linting setup task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7,8,9,10,11,12)
  - **Blocks**: Tasks 17,18 (test execution may depend on linting)
  - **Blocked By**: Task 5 (Makefile must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing make lint, make format
  - Official ruff documentation: https://docs.astral.sh/ruff/

  **API/Type References** (contracts to implement against):
  - None - this is linting configuration

  **Test References** (testing patterns to follow):
  - None - this is infrastructure setup

  **External References** (libraries and frameworks):
  - Ruff documentation: https://docs.astral.sh/ruff/ - For Python linting
  - Black documentation: https://black.readthedocs.io/ - For Python formatting
  - Prettier documentation: https://prettier.io/ - For JavaScript/TypeScript formatting

  **WHY Each Reference Matters** (explain the relevance):
  - README shows make lint and make format commands are expected
  - Official documentation provides correct configuration patterns

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cd backend && python -m ruff check . --select E,F,B,I,N,UP,PL,RUF 2>&1 | head -10
      2. Execute: cd ../frontend && bunx prettier --check src/ 2>&1 | head -10
    Expected Result: Linting runs without errors (or shows only minor issues)
    Failure Indicators: Linting fails due to configuration errors
    Evidence: .sisyphus/evidence/task-13-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cd backend && cp pyproject.toml pyproject.toml.backup
      2. Execute: echo "[tool.ruff]\ninvalid = " >> pyproject.toml
      3. Execute: python -m ruff check . 2>&1 | grep -i "error\|invalid\|exception" || echo "NO ERROR"
      4. Execute: mv pyproject.toml.backup pyproject.toml
    Expected Result: ruff should show error for invalid configuration
    Failure Indicators: ruff succeeds with invalid config or doesn't show error
    Evidence: .sisyphus/evidence/task-13-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(lint): add linting and formatting configs`
  - Files: backend/pyproject.toml (ruff/black sections), frontend/.prettierrc
  - Pre-commit: `cd backend && python -m ruff --version && cd ../frontend && bunx prettier --version`

- [x] 14. Verify frontend can start with bun run dev

  **What to do**:
  - Start frontend dev server in background
  - Verify server starts without errors
  - Verify server responds to HTTP requests
  - Verify Phaser canvas is rendered
  - Kill background process after verification

  **Must NOT do**:
  - Leave background processes running after verification
  - Skip verification steps

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `deep`
    - Reason: Requires understanding of frontend server startup and verification
  - **Skills**: `["playwright"]`
    - Need browser automation to verify Phaser canvas rendering

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final verification wave)
  - **Blocks**: Task 17 (backend verification may depend on frontend)
  - **Blocked By**: Tasks 7,8 (Svelte config and Phaser integration must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing bun run dev command
  - Official Bun documentation: https://bun.sh/guides/cli

  **API/Type References** (contracts to implement against):
  - None - this is verification task

  **Test References** (testing patterns to follow):
  - None - this is verification task

  **External References** (libraries and frameworks):
  - Bun documentation: https://bun.sh/guides/cli - For bun run dev command
  - Playwright documentation: https://playwright.dev - For browser verification

  **WHY Each Reference Matters** (explain the relevance):
  - README shows bun run dev is the expected frontend development command
  - Playwright documentation provides patterns for verifying web applications

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: bun run dev -- --port 5173 &
      2. Execute: sleep 15
      3. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      4. Execute: curl -s http://localhost:5173 | grep -i "phaser" || echo "NO PHASER"
      5. Execute: kill %1 2>/dev/null || pkill -f "bun run dev"
    Expected Result: Server starts, serves page with Pixel Heart and Phaser references
    Failure Indicators: Server fails to start or doesn't serve expected content
    Evidence: .sisyphus/evidence/task-14-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/frontend directory
    Steps:
      1. Execute: cp vite.config.ts vite.config.ts.backup
      2. Execute: echo "export default { invalid: " > vite.config.ts
      3. Execute: bun run dev -- --port 5173 2>&1 | head -5
      4. Execute: mv vite.config.ts.backup vite.config.ts
      5. Execute: pkill -f "bun run dev" 2>/dev/null || true
    Expected Result: bun run dev should fail with Vite configuration error
    Failure Indicators: bun run dev succeeds with invalid config or doesn't show error
    Evidence: .sisyphus/evidence/task-14-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(frontend): verify dev server startup`
  - Files: none
  - Pre-commit: `echo "Frontend dev server verification complete"`

- [x] 15. Verify backend can start with uvicorn

  **What to do**:
  - Start backend server in background
  - Verify server starts without errors
  - Verify API docs are accessible
  - Kill background process after verification

  **Must NOT do**:
  - Leave background processes running after verification
  - Skip verification steps

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `deep`
    - Reason: Requires understanding of FastAPI server startup and verification
  - **Skills**: `[]`
    - Standard server verification task

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final verification wave)
  - **Blocks**: Task 17 (backend verification depends on this)
  - **Blocked By**: Tasks 10,11 (Alembic and Docker setup must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing uvicorn command
  - Official Uvicorn documentation: https://www.uvicorn.org/

  **API/Type References** (contracts to implement against):
  - None - this is verification task

  **Test References** (testing patterns to follow):
  - None - this is verification task

  **External References** (libraries and frameworks):
  - Uvicorn documentation: https://www.uvicorn.org - For server startup
  - FastAPI documentation: https://fastapi.tiangolo.com - For API verification

  **WHY Each Reference Matters** (explain the relevance):
  - README shows uvicorn command is expected for backend development
  - Uvicorn documentation provides patterns for server startup

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: source .venv/bin/activate 2>/dev/null || echo "Venv not active"
      2. Execute: uvicorn main:app --reload --port 8000 &
      3. Execute: sleep 10
      4. Execute: curl -s http://localhost:8000/docs | grep -i "swagger" || echo "NO DOCS"
      5. Execute: curl -s http://localhost:8000/health 2>&1 | head -5
      6. Execute: kill %1 2>/dev/null || pkill -f "uvicorn"
    Expected Result: Server starts, API docs accessible at /docs
    Failure Indicators: Server fails to start or /docs not accessible
    Evidence: .sisyphus/evidence/task-15-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS-/backend directory
    Steps:
      1. Execute: cp main.py main.py.backup
      2. Execute: echo "invalid python syntax" > main.py
      3. Execute: uvicorn main:app --reload --port 8000 2>&1 | head -5
      4. Execute: mv main.py.backup main.py
      5. Execute: pkill -f "uvicorn" 2>/dev/null || true
    Expected Result: uvicorn should fail with Python syntax error
    Failure Indicators: uvicorn succeeds with invalid Python or doesn't show error
    Evidence: .sisyphus/evidence/task-15-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(backend): verify server startup`
  - Files: none
  - Pre-commit: `echo "Backend server verification complete"`

- [x] 16. Verify Docker Compose starts all services

  **What to do**:
  - Start docker-compose services
  - Verify all services are healthy
  - Verify frontend accessible on port 5173
  - Verify backend accessible on port 8000
  - Stop docker-compose services after verification

  **Must NOT do**:
  - Leave docker-compose running after verification
  - Skip service health checks

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `deep`
    - Reason: Requires understanding of Docker Compose and service health checks
  - **Skills**: `[]`
    - Standard container verification task

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final verification wave)
  - **Blocks**: Task 17,18 (test execution may depend on Docker services)
  - **Blocked By**: Task 11 (Docker Compose setup must exist)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:171-180 - Development section showing docker-compose up -d command
  - Official Docker Compose documentation: https://docs.docker.com/compose/

  **API/Type References** (contracts to implement against):
  - None - this is verification task

  **Test References** (testing patterns to follow):
  - None - this is verification task

  **External References** (libraries and frameworks):
  - Docker Compose documentation: https://docs.docker.com/compose/ - For service management

  **WHY Each Reference Matters** (explain the relevance):
  - README shows docker-compose up -d is the expected Docker development command
  - Docker Compose documentation provides patterns for service health checks

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: docker-compose up -d
      2. Execute: sleep 20
      3. Execute: docker-compose ps
      4. Execute: curl -s http://localhost:5173 | grep -i "pixel heart" || echo "NOT FOUND"
      5. Execute: curl -s http://localhost:8000/docs | grep -i "swagger" || echo "NO DOCS"
      6. Execute: docker-compose down
    Expected Result: All services start and respond to HTTP requests
    Failure Indicators: Services fail to start or don't respond to requests
    Evidence: .sisyphus/evidence/task-16-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cp docker-compose.yml docker-compose.yml.backup
      2. Execute: echo "services:" > docker-compose.yml
      3. Execute: echo "  frontend:" >> docker-compose.yml
      4. Execute: echo "    image: invalid-image-that-does-not-exist" >> docker-compose.yml
      5. Execute: docker-compose up -d 2>&1 | grep -i "error\|pull\|failed" || echo "NO ERROR"
      6. Execute: mv docker-compose.yml.backup docker-compose.yml
      7. Execute: docker-compose down 2>/dev/null || true
    Expected Result: docker-compose should fail when trying to pull invalid image
    Failure Indicators: docker-compose succeeds with invalid image or doesn't show error
    Evidence: .sisyphus/evidence/task-16-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `chore(docker): verify service startup`
  - Files: none
  - Pre-commit: `echo "Docker Compose verification complete"`

- [x] 17. Run backend tests to confirm setup
- [x] 18. Run frontend tests to confirm setup
- [x] 19. Final documentation update with usage instructions

  **What to do**:
  - Update README.md with complete setup instructions
  - Add usage examples for all Makefile commands
  - Document environment variables
  - Add troubleshooting section

  **Must NOT do**:
  - Include actual implementation details
  - Document incomplete features

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: Standard documentation update
  - **Skills**: `[]`
    - Standard documentation task

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final verification wave)
  - **Blocks**: None (final task)
  - **Blocked By**: Tasks 17,18 (test execution must complete)

  **References** (CRITICAL - Be Exhaustive):
  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - README.md:101-130 - Current README structure
  - README.md:171-180 - Development section

  **API/Type References** (contracts to implement against):
  - None - this is documentation task

  **Test References** (testing patterns to follow):
  - None - this is documentation task

  **External References** (libraries and frameworks):
  - None - this is documentation task

  **WHY Each Reference Matters** (explain the relevance):
  - README shows the current documentation structure that should be maintained

  **Acceptance Criteria**:
  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.

  **If TDD (tests enabled):**
  - [ ] Not applicable - environment setup task

  **QA Scenarios (MANDATORY — task is INCOMPLETE without these):**

  ```
  Scenario: [Happy path — what SHOULD work]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: grep -i "make dev" README.md
      2. Execute: grep -i "make test" README.md
      3. Execute: grep -i "docker-compose" README.md
      4. Execute: grep -i "environment" README.md
    Expected Result: README contains instructions for all major commands
    Failure Indicators: README missing key instructions
    Evidence: .sisyphus/evidence/task-19-happy.txt

  Scenario: [Failure/edge case — what SHOULD fail gracefully]
    Tool: Bash
    Preconditions: Working in /home/lora/repos/Pixel-Heart-OS- directory
    Steps:
      1. Execute: cp README.md README.md.backup
      2. Execute: echo "# Broken Documentation" > README.md
      3. Execute: grep -i "make dev" README.md || echo "NOT FOUND (expected)"
      4. Execute: mv README.md.backup README.md
    Expected Result: Broken documentation should be missing key info
    Failure Indicators: README still contains key instructions when it shouldn't
    Evidence: .sisyphus/evidence/task-19-error.txt
  ```

  **Evidence to Capture**:
  - [ ] Each evidence file named: task-{N}-{scenario-slug}.{ext}
  - [ ] Screenshots for UI, terminal output for CLI, response bodies for API

  **Commit**: NO
  - Message: `docs(readme): update setup instructions`
  - Files: README.md
  - Pre-commit: `grep -i "make dev" README.md && echo "README contains setup instructions"`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `tsc --noEmit` + linter + `bun test`. Review all changed files for: `as any`/`@ts-ignore`, empty catches, console.log in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names (data/result/item/temp).
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill if UI)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (features working together, not isolation). Test edge cases: empty state, invalid input, rapid actions. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination: Task N touching Task M's files. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

For each task, commits are made after verification passes:
- Task 1-6: No commit (infrastructure setup)
- Task 7-9: No commit (configuration setup)
- Task 10-13: No commit (configuration setup)
- Task 14-16: No commit (verification tasks)
- Task 17-18: No commit (test execution)
- Task 19: Commit with documentation update

All commits use conventional commit format:
- `chore(project): create directory structure`
- `chore(frontend): add package.json and vite.config.ts`
- `chore(backend): add requirements.txt and pyproject.toml`
- etc.

---

## Success Criteria

### Verification Commands
```bash
# Frontend dev server
cd frontend && bun run dev -- --port 5173 &
sleep 15
curl -s http://localhost:5173 | grep -i "pixel heart"
# Expected: HTML containing "Pixel Heart"

# Backend dev server
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
sleep 10
curl -s http://localhost:8000/docs | grep -i "swagger"
# Expected: Swagger UI documentation

# Docker Compose
docker-compose up -d
sleep 20
docker-compose ps
# Expected: All services running

# Backend tests
cd backend
python -m pytest tests/ -v
# Expected: Test results (may be empty if no tests yet)

# Frontend tests
cd frontend
bunx vitest run
# Expected: Test results (may be empty if no tests yet)

# Linting
cd backend && python -m ruff check .
cd frontend && bunx prettier --check src/
# Expected: No linting errors
```

### Final Checklist
- [ ] All "Must Have" present (Bun >=1.0, Python 3.12+, EventBus, Alembic, Docker Compose, test config)
- [ ] All "Must NOT Have" absent (no hardcoded secrets, no SSR for Phaser, no platform-specific paths)
- [ ] All tests pass (pytest and vitest run without errors)
- [ ] All verification scenarios pass (evidence files created)
- [ ] Project structure matches README.md specification
- [ ] Developer can run `make dev` to start servers
- [ ] Developer can run `make test` to execute tests
- [ ] Developer can run `make docker-run` to start full stack
