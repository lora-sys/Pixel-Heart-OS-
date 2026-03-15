# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status: Active Development (Phase 2 - Core Features)

Development is **actively underway**. The core architecture is implemented and functional. This document provides the developmental context and patterns needed to contribute effectively.

## Project Overview

**Pixel Heart OS** is an AI-driven, emergent social universe system built around a central heroine character. It features:
- Git-style memory management system ("Beads") - DAG-based narrative version control
- Multi-agent simulation powered by LangGraph with stateful workflows
- Pixel-art UI frontend (Svelte 5 + Phaser 3) with EventBus separation
- Full state persistence with branching timelines and merge capability

The system allows users to create a heroine from free-form descriptions, automatically generates a surrounding social network (NPCs and scenes), and simulates interactions with branching narrative possibilities.

## Technology Stack (Actual Implementation)

### Frontend
- **Framework**: Svelte 5 with Runes (`$state`, `$derived`, `$effect`) - no Svelte store compatibility layer
- **Game Engine**: Phaser 3.90.0 for rendering relationship nebula and timeline visualization
- **Styling**: Tailwind CSS v3.4 with custom pixel-art CSS in `src/app.html`
- **Package Manager**: Bun (for both frontend and backend tooling)
- **Build Tool**: Vite 5.4 with SvelteKit adapter-auto

### Backend
- **API Framework**: FastAPI (Python async) with lifespan lifecycle management
- **Multi-Agent Engine**: LangGraph for stateful agent workflows with checkpointing
- **Dependency Injection**: Custom Container pattern (see `backend/core/container.py`)
- **Memory System**: Custom "Beads" DAG engine (`backend/beads/engine.py`)
- **Databases**:
  - SQLite (aiosqlite) via SQLAlchemy 2.0 async ORM
  - ChromaDB for vector storage (semantic conversation retrieval)
- **Caching**: In-memory TTL cache for API responses

### Storage
- Markdown (`.md`) and TOML (`.toml`) files for character souls, identities, and voice configs
- File-based storage layer (`backend/storage/file_system.py`)
- Data directory: `backend/data/` (heroine, npcs, scenes subdirectories)

## High-Level Architecture Patterns

### Backend: Service Layer + Dependency Injection

The backend follows a clean service-oriented architecture:

```
API Endpoints (backend/api/v1/*.py)
    ↓ (call)
Service Layer (backend/services/*_service.py)
    ↓ (use)
Repositories (backend/infrastructure/database/repositories/*.py)
    ↓ (query)
SQLAlchemy Models (backend/database/models.py)
```

**Key services** (singletons managed by `Container`):
- `HeroineService` - Creates heroine from LLM parsing, manages storage
- `NPCService` - Generates NPCs with soul/identity/voice, handles refinement
- `SceneService` - Generates scenes matching narrative dynamics
- `BeadService` - Wraps BeadEngine with caching
- `SimulationService` - Orchestrates LangGraph simulation workflow

**Dependency injection** via `get_container()` pattern:
- Container initialized at app startup in `core/lifecycle.py`
- FastAPI `Depends(get_*_service)` in endpoint signatures
- Services receive dependencies via constructor injection

**Example**: Adding a new service
```python
# In container.py
def get_my_service(self):
    if 'my_service' not in self._singletons:
        from services.my_service import MyService
        self._singletons['my_service'] = MyService(
            llm_service=self.get_llm_service(),
            bead_service=self.get_bead_service()
        )
    return self._singletons['my_service']
```

### Beads Memory System (Git-inspired DAG)

The `BeadEngine` (`backend/beads/engine.py`) implements a Git-like DAG for narrative state:

- **Immutability**: Beads are never modified; new beads reference parent IDs
- **Branching**: Multiple timelines via `branch_name` column; `create_branch()` forks from any bead
- **Merging**: `merge_branches()` creates a merge bead linking two branch heads
- **Rebasing**: `rebase_branch()` rewrites bead IDs onto new base
- **Cycle prevention**: `_would_create_cycle()` ensures DAG invariant
- **Timeline traversal**: `get_timeline(branch_name)` returns chronological list
- **Diffing**: `diff_beads(bead_id1, bead_id2)` computes content differences

**Bead structure** (SQLAlchemy model `backend/database/models.py:Bead`):
- `id`: SHA-1 hash of (parent_id, content, action, timestamp)
- `parent_id`: Reference to parent bead (NULL for root)
- `branch_name`: Branch this bead belongs to (default: "main")
- `action`: Enum (turn, merge, create_heroine, generate_npc, etc.)
- `emotion_tag`: Optional emotion for UI coloring
- `content`: JSON blob with action-specific data
- `timestamp`: ISO format datetime

**Important**: The BeadEngine uses *stateless sessions* - each method accepts an optional `session` parameter. Services should pass request-scoped sessions to maintain transaction boundaries.

### LangGraph Simulation Workflow

The simulation (`backend/graphs/simulation_graph.py`) defines a cyclical state machine:

```
State: SimulationState (TypedDict)
  ├── heroine_soul: Dict
  ├── current_scene: Optional[Dict]
  ├── active_npcs: List[Dict]
  ├── player_action: str
  ├── conversation_history: List[Dict] (accumulates with reduce lambda)
  ├── retrieved_memories: List[Dict]
  ├── npc_responses: List[Dict]
  ├── updated_relationships: Dict[str, float]
  ├── bead_data: Dict
  └── new_bead_id: Optional[str]

Nodes (async functions):
  1. retrieve_context - ChromaDB semantic search + NPC backstories
  2. process_player_action - Parse intent (currently passthrough)
  3. generate_npc_responses - Parallel LLM calls via LLMService.simulate_npc_response()
  4. update_relationships - Aggregate deltas, clamp to [-1, 1]
  5. commit_bead - Create new bead via BeadEngine, attach to "main" branch

Compilation: workflow.compile(checkpointer=MemorySaver())
```

**Critical**: The graph uses `Annotated[List, lambda a,b: a+b]` for conversation_history to accumulate across turns. The `MemorySaver` checkpointer enables resuming from any state (used for branching scenarios).

### Frontend: Dual-Store Pattern

Svelte 5 stores are split into **two distinct domains**:

1. **`apiStore`** (`frontend/src/lib/core/store/api-store.ts`) - Server state
   - heroine, npcs, beads, scenes, relationshipNebula
   - Populated by API calls; cached in memory
   - Should be treated as read-only in components (use API to modify)

2. **`uiStore`** (`frontend/src/lib/core/store/app-store.ts`) - Client-side UI state
   - currentRoute, sidebarOpen, modal visibility flags
   - selected IDs, currentBranch, editorMode
   - isLoading, errorMessage, toast notifications
   - Phaser canvas options (scale, showNebula, showLabels)

**Rule**: Never mix server and UI state. Components subscribe to only what they need.

**Svelte 5 Runes usage**:
- `$state` for reactive store values in components
- `$derived` for computed values from store state
- `$effect` for side effects on state changes (use with cleanup!)

Example from `frontend/src/routes/+page.svelte`:
```svelte
<script>
  import { goto } from '$app/navigation';
  import { apiStore } from '$lib/core/store';

  $effect(() => {
    const unsubscribe = apiStore.subscribe(state => {
      if (state.heroine) {
        goto('/universe');
      } else {
        goto('/create');
      }
    });
    return () => unsubscribe(); // cleanup
  });
</script>
```

### Svelte–Phaser Bridge: EventBus Pattern

The two frameworks are kept **strictly separated** via an EventBus (`frontend/src/lib/event-bus.ts`):

- **Svelte → Phaser**: `bead-highlight`, `switch-scene`, `npc-move`, `show-dialogue`, `update-nebula`
- **Phaser → Svelte**: `scene-ready`, `npc-clicked`, `dialogue-choice`, `bead-selected`, `nebula-interaction`

**Implementation** (`frontend/src/lib/PhaserGame.svelte`):
- Phaser game instantiated in `onMount()` with EventBus plugin
- `afterUpdate` hook watches `apiStore` changes and emits events to Phaser
- Phaser scenes subscribe to internal events (`update-beads`, `update-nebula`, `update-npc`)
- All communication is unidirectional and event-driven

**Rule**: Never manipulate Phaser game objects directly from Svelte outside the EventBus pattern.

## Development Commands

### Prerequisites
- **Bun** ≥ 1.0 (https://bun.sh)
- **Python** ≥ 3.11 (3.12 recommended) with venv
- **Anthropic API key** (or set `USE_MOCK_LLM=True` for testing)

### Environment Setup

```bash
# 1. Clone and install dependencies
cd frontend && bun install
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cd backend
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY, optionally USE_MOCK_LLM=True for dev without key

# 3. Initialize database
python -m database.init
```

### Running the Application

**Option A: Using Make (recommended)**
```bash
# Start both backend and frontend in parallel
make dev

# Or separately:
make dev-backend   # Backend on http://localhost:8000
make dev-frontend  # Frontend on http://localhost:5173
```

**Option B: Manual**
```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
bun run dev
```

**Option C: Docker (full stack)**
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Testing

```bash
# Backend tests (pytest with coverage)
cd backend
pytest tests/ -v --cov=. --cov-report=html

# Watch mode
pytest tests/ -v --watch

# Single test file
pytest tests/test_beads.py -v

# Single test function
pytest tests/test_beads.py::test_create_bead -v
```

**Note**: The `tests/` directory is currently minimal (only `__init__.py`). Add tests following pytest conventions: `test_*.py` with `test_` functions.

```bash
# Frontend tests (Vitest)
cd frontend
bunx vitest run          # all tests
bunx vitest run --watch  # watch mode
bunx vitest run src/lib/components/NPCCard.svelte  # single file

# Type checking
bunx svelte-check        # Svelte component types
bunx tsc --noEmit        # TypeScript only
```

### Linting & Formatting

```bash
# Everything
make lint      # Check only
make format    # Auto-fix

# Backend only
cd backend
bunx ruff check .          # Lint
bunx black --check .       # Check formatting
bunx black .               # Format
bunx ruff check --fix .    # Fix lint issues

# Frontend only
cd frontend
bunx eslint src/           # Lint
bunx eslint src/ --fix     # Lint + fix
bunx prettier --write src/ # Format
```

### Useful Make Targets

```bash
make help          # Show all targets
make build         # Build frontend for production
make docker-build  # Build Docker images
make docker-run    # Start docker-compose
make db-init       # Initialize SQLite database only
make sample-data   # Generate sample heroine/NPCs/scenes
```

### Database Migrations (Alembic)

```bash
cd backend
# Create migration
bunx alembic revision --autogenerate -m "Description"

# Upgrade
bunx alembic upgrade head

# Downgrade
bunx alembic downgrade -1
```

### API Documentation

When backend is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Development Tasks

### Adding a New Endpoint

1. **Define schema** in `backend/api/schemas.py` (Pydantic models)
2. **Add endpoint** in appropriate `backend/api/v1/*.py` router file
3. **Register router** in `backend/api/v1/__init__.py` if new domain
4. **Add service method** if business logic needed (in `backend/services/*_service.py`)
5. **Frontend API client** - add function to `frontend/src/lib/api/client.ts`
6. **Consume in Svelte** - call API function, update `apiStore`

### Modifying the Beads DAG

- **Add bead operations** in `backend/beads/engine.py` (core logic)
- **Expose via service** in `backend/services/bead_service.py` (with caching)
- **Add API endpoints** in `backend/api/v1/beads.py` if external access needed
- **Update frontend** in `frontend/src/lib/core/store/api-store.ts` and relevant routes

**Important**: Maintain DAG acyclicity invariant. Use `_would_create_cycle()` validator.

### Extending the LangGraph Simulation

Modify `backend/graphs/simulation_graph.py`:

1. **Add state field** to `SimulationState` TypedDict
2. **Create node function** (async, returns modified state)
3. **Add node to graph**: `workflow.add_node("node_name", node_function)`
4. **Wire edges**: `workflow.add_edge("prev_node", "node_name")`
5. **Update default state** in `SimulationGraph.arun()`

**Node dependencies**: Inject services via lambda wrappers:
```python
workflow.add_node("my_node", lambda s: my_node(s, self.llm, self.chroma))
```

### Changing Pixel Art Styling

All styles centralized in `frontend/src/app.html`:
- CSS variables for colors (e.g., `--color-accent-2: #ff6eb4;`)
- Tailwind config for pixel font in `frontend/tailwind.config.js`
- Phaser color constants in `frontend/src/lib/PhaserGame.svelte` (getEmotionColor, getEdgeColor)

### Adding a New Service

Follow the pattern in `backend/core/container.py`:
1. Create `backend/services/my_service.py` with class receiving dependencies
2. Add getter in `Container` class (singleton pattern)
3. Register via `get_*_service()` Functions
4. Inject into other services via constructor

## Code Conventions

### Python
- Type hints on all function signatures
- Async/await throughout (no blocking calls)
- SQLAlchemy 2.0 style (await session.execute())
- Pydantic for validation (v2)
- Black formatting (line length 88)
- Ruff linting (E, F, B, I, N, UP, PL, RUF)

### TypeScript/Svelte
- Strict mode enabled (`tsconfig.json`)
- Svelte 5 runes syntax (no `$:` derived stores)
- Components: `<script lang="ts">` with export let props
- Stores: use `writable<T>()` from 'svelte/store'
- ESLint + Prettier with svelte plugin

### Git Workflow
- Branch off `main` for features
- Commit often with descriptive messages
- Run `make lint && make format` before committing
- Use pre-commit hooks (configured in `.pre-commit-config.yaml`)

## Testing Strategy

**Backend**: pytest with pytest-asyncio
- Place tests in `backend/tests/` matching module structure
- Use `httpx.AsyncClient` for endpoint testing
- Mock external LLM calls with `USE_MOCK_LLM=True` or pytest fixtures

**Frontend**: Vitest with testing-library
- Component tests in `__tests__` adjacent to components or in `src/routes/__tests__`
- Use Svelte Testing Library for DOM assertions

**Current state**: Test suite is minimal. Prioritize adding tests for:
- `BeadEngine` operations (create, branch, merge, rebase, cycle detection)
- LangGraph simulation end-to-end
- API endpoint contracts
- Store update logic

## Important Implementation Notes

### Dependency Injection Lifecycle
- Container initialized in `AppLifecycle.startup()`
- Services are **singletons** - store no per-request state
- Database sessions are **request-scoped** - use `Depends(get_session)` in endpoints
- BeadEngine is stateless w.r.t. sessions - session passed as parameter

### EventBus Usage
- Always unsubscribe in `onDestroy` or cleanup return function
- Events are **case-sensitive** strings defined in `Events` const
- Payload types are not enforced at runtime (any)

### State Management
- `apiStore` updates should be **atomic** - update entire object, not nested fields
- Use convenience helpers (`setHeroine()`, `setNPCs()`, etc.) from `api-store.ts`
- UI-only state goes in `uiStore`; never mix with server data

### Error Handling
- Backend: Catch exceptions in services, re-raise as HTTPException in endpoints
- Frontend: API errors throw; wrap calls in try/catch and set `uiStore.errorMessage`
- LLM failures: Simulated gracefully in `simulate_npc_response()` with fallback dialogue

### ChromaDB Vector Store
- Lazy-initialized on first access via `get_chroma_client()`
- Collections: `conversations` (semantic search), `npc_backstories` (character traits)
- Embeddings auto-generated by Chroma (all-MiniLM-L6-v2 default)

## File Structure Reference

```
pixel-heart-os/
├── backend/
│   ├── api/v1/              # FastAPI routers (heroine, npcs, scenes, beads, simulation)
│   ├── beads/               # BeadEngine (DAG operations)
│   ├── core/                # Lifecycle, Container, Cache
│   ├── database/            # SQLAlchemy models, init, session management
│   ├── graphs/              # LangGraph workflows (simulation_graph.py)
│   ├── infrastructure/      # Repositories (data access layer)
│   ├── llm/                 # LLMService (Anthropic/StepFun integration)
│   ├── prompts/             # Text prompt templates (.txt files)
│   ├── services/            # Business logic layer (heroine, npc, scene, bead, simulation)
│   ├── storage/             # FileSystemService (Markdown/TOML I/O)
│   ├── vector_store/        # ChromaClient wrapper
│   ├── tests/               # pytest tests
│   ├── config.py            # Settings singleton
│   ├── main.py              # FastAPI app entry
│   └── pyproject.toml       # Python deps and tool config
├── frontend/
│   ├── src/lib/
│   │   ├── api/             # API client (client.ts)
│   │   ├── components/      # Svelte components (NPCCard, SceneCard, DiffViewer, Navigation, TerminalInput)
│   │   ├── core/
│   │   │   └── store/       # app-store.ts (uiStore), api-store.ts (apiStore)
│   │   ├── event-bus.ts     # Svelte↔Phaser bridge
│   │   └── PhaserGame.svelte# Phaser wrapper with scene definitions
│   ├── src/routes/          # SvelteKit pages (+, create, universe, simulate, timeline)
│   ├── src/app.html         # Global styles, Google Fonts, CSS variables
│   ├── package.json         # Bun dependencies
│   └── vite.config.ts       # Vite/Svelte config
├── data/                    # Generated story data (gitignored)
│   ├── heroine/             # soul.md, identity.md, voice.toml
│   ├── npcs/                # Per-NPC markdown/TOML
│   └── scenes/              # Scene configurations
├── docker-compose.yml       # Full-stack orchestration
├── Makefile                 # Dev shortcuts
└── README.md                # Project intro and quick start
```

## Known Issues & Gotchas

1. **BeadEngine session management**: Current implementation mixes session ownership. Services must pass request-scoped sessions to BeadEngine methods; don't let engine create its own sessions in production. See `beads/engine.py:L24-32`.

2. **LLM mock mode**: Set `USE_MOCK_LLM=True` in `.env` to bypass Anthropic API for development/testing. LLMService returns canned responses.

3. **CORS**: Allowed origins configured in `config.py:allowed_origins` (defaults to dev ports). Update for production.

4. **File storage paths**: `settings.data_dir` uses absolute path based on `config.py` location. Ensure `backend/data/` exists and is writable.

5. **ChromaDB persistence**:数据库路径在`chroma_db_path`设置。生产环境中，确保卷已挂载以持久化向量数据。

6. **Phaser scene cleanup**: `PhaserGame.svelte` destroys game instance in `onMount` cleanup. Always unsubscribe EventBus listeners to prevent memory leaks.

7. **Svelte 5 reactivity**: `$effect` runs after every update; guard with conditionals. Cleanup functions run before next effect invocation.

## Quick Decision Guide

**Adding a new data field?**
- Stored in Bead `content`? → Update relevant service's bead creation, define in `schemas.py`
- Shown in UI? → Add to `apiStore` type in `api-store.ts`
- Transient UI state? → Add to `uiStore` type in `app-store.ts`

**Changing simulation logic?**
- Edit `backend/graphs/simulation_graph.py` nodes
- Preserve state shape (add fields to `SimulationState`)
- Keep async throughout

**Fixing a UI bug?**
- Check `uiStore` for relevant flags
- Inspect `PhaserGame.svelte` if canvas-related
- Verify EventBus event names match `Events` const

**Performance issue?**
- Backend: Check `Cache` usage in service layer (TTLs in `config.py`)
- Frontend: Avoid `$effect` heavy computation; use `$derived` for memoization
- Beads: Timeline queries use `limit` parameter; paginate if >50 beads

## Resources

- **Requirements Document**: `Pixel Heart OS_ AI-Readable Requirements Document v2.0.md` (source of truth)
- **Online Design Doc**: https://a56cf98f.pinme.dev
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Svelte 5 Runes**: https://svelte.dev/blog/runes
- **Phaser 3.90**: https://phaser.io/news/2025/05/phaser-v390-released
- **FastAPI Async**: https://fastapi.tiangolo.com/async/

## Notes for Future Claude Instances

- The requirements document is **authoritative** - align architectural changes with v2.0 spec
- **Separation of concerns** is critical: Svelte (DOM) vs Phaser (canvas); API (server) vs UI (client) stores
- **Beads DAG** is the core innovation - maintain immutability and acyclicity invariants
- **LangGraph** workflows should be **stateful and cyclical**, not linear chains
- **All character data** (soul, identity, voice) must remain as plain text files (md/toml) for editability and version control
- **Service layer** is the primary place for business logic; keep API endpoints thin
- **Dependency injection** via Container - never instantiate services directly with `()`; use `container.get_*_service()`
