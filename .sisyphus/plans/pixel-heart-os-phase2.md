# Pixel Heart OS - Core Feature Implementation (Phase 2)

## TL;DR

> **Quick Summary**: Implement the core application features - database models, API endpoints, services, Beads DAG engine, LangGraph simulation, and frontend integration
> 
> **Deliverables**:
> - Backend: Database models, API endpoints, services, Beads engine, LangGraph workflows
> - Frontend: Stores, API client, SvelteKit pages
> - Full integration: Working CRUD for heroine/NPCs/scenes with memory system
> 
> **Estimated Effort**: High
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Database Models → Services → API → Frontend

---

## Context

### Original Request
User completed Phase 1 (environment setup) and requested continuation to implement the core application features.

### Implementation Decisions (Auto-resolved)
- **Scope**: Full implementation following CLAUDE.md patterns
- **LLM Mode**: Mock mode enabled (USE_MOCK_LLM=True) for development/testing
- **Data**: Sample data generated on first run
- **Frontend Style**: Follow existing Tailwind + pixel-art CSS patterns

---

## Technical Specifications

### Database Schema

```python
# Core tables needed:
- beads: id (PK), parent_id, branch_name, action, emotion_tag, content (JSON), timestamp
- sessions: id (PK), thread_id, branch_name, created_at, updated_at
```

### API Endpoints Structure

```
POST   /api/v1/heroine          - Create heroine from description
GET    /api/v1/heroine          - Get current heroine
POST   /api/v1/npcs            - Generate NPCs for heroine
GET    /api/v1/npcs            - List all NPCs
PATCH  /api/v1/npcs/{id}       - Update NPC
POST   /api/v1/scenes          - Generate scene
GET    /api/v1/scenes          - List scenes
POST   /api/v1/beads           - Create new bead
GET    /api/v1/beads           - List beads (paginated)
GET    /api/v1/beads/{id}      - Get specific bead
GET    /api/v1/beads/branch/{name} - Get branch timeline
POST   /api/v1/simulation/run  - Run simulation turn
POST   /api/v1/simulation/reset - Reset simulation state
```

### Service Layer Pattern

```
services/
├── heroine_service.py    - Create heroine, parse description → soul/identity/voice
├── npc_service.py       - Generate NPCs, handle refinement
├── scene_service.py      - Generate scenes matching narrative
├── bead_service.py       - Wrapper around BeadEngine with caching
└── simulation_service.py - Orchestrates LangGraph workflow
```

### Beads DAG Operations

```
- create_bead(parent_id, content, action, branch) → bead_id
- get_bead(bead_id) → bead
- get_timeline(branch_name, limit, offset) → [beads]
- create_branch(branch_name, from_bead_id) → branch_id
- merge_branches(source_branch, target_branch) → merge_bead_id
- rebase_branch(branch_name, new_base_bead_id) → rebase_result
- diff_beads(bead_id1, bead_id2) → diff_result
```

### LangGraph Simulation State

```python
SimulationState = {
    heroine_soul: Dict,
    current_scene: Optional[Dict],
    active_npcs: List[Dict],
    player_action: str,
    conversation_history: List[Dict],
    retrieved_memories: List[Dict],
    npc_responses: List[Dict],
    updated_relationships: Dict[str, float],
    bead_data: Dict,
    new_bead_id: Optional[str]
}
```

---

## Implementation Waves

### Wave 1: Database & Core Infrastructure

1. **Database Models** (`database/models.py`)
   - SQLAlchemy Bead model
   - SQLAlchemy Session model
   - Type definitions

2. **Database Init** (`database/init.py`)
   - Create all tables
   - Seed initial data if empty

3. **Config** (`config.py`)
   - Settings singleton
   - Environment variable loading

4. **Container/DI** (`core/container.py`)
   - Service container
   - Singleton management

### Wave 2: Beads Engine & Services

5. **Bead Engine** (`beads/engine.py`)
   - create_bead()
   - get_bead()
   - get_timeline()
   - create_branch()
   - merge_branches()
   - rebase_branch()
   - diff_beads()
   - Cycle detection

6. **LLM Service** (`llm/service.py`)
   - Anthropic API client
   - Mock mode support
   - Response parsing

7. **Storage Service** (`storage/file_system.py`)
   - Read/write Markdown files
   - Read/write TOML files

### Wave 3: Business Logic Services

8. **Heroine Service** (`services/heroine_service.py`)
   - create_heroine(description) → soul/identity/voice
   - get_heroine()

9. **NPC Service** (`services/npc_service.py`)
   - generate_npcs(heroine_soul, count)
   - get_npcs()
   - update_npc()

10. **Scene Service** (`services/scene_service.py`)
    - generate_scene(heroine, npcs, context)
    - get_scenes()

11. **Bead Service** (`services/bead_service.py`)
    - Thin wrapper around BeadEngine
    - Add caching layer

12. **Simulation Service** (`services/simulation_service.py`)
    - Run LangGraph workflow
    - State management

### Wave 4: API Endpoints

13. **API Schemas** (`api/schemas.py`)
    - Pydantic models for all endpoints

14. **Heroine Router** (`api/v1/heroine.py`)
    - POST /heroine
    - GET /heroine

15. **NPC Router** (`api/v1/npcs.py`)
    - POST /npcs
    - GET /npcs
    - PATCH /npcs/{id}

16. **Scene Router** (`api/v1/scenes.py`)
    - POST /scenes
    - GET /scenes

17. **Bead Router** (`api/v1/beads.py`)
    - Full CRUD + branch operations

18. **Simulation Router** (`api/v1/simulation.py`)
    - POST /run
    - POST /reset

19. **API Router Registration** (`api/v1/__init__.py`)
    - Combine all routers
    - Register in main.py

### Wave 5: Frontend Integration

20. **Frontend API Client** (`lib/api/client.ts`)
    - HTTP client functions
    - TypeScript types matching API schemas

21. **Frontend Stores** (`lib/core/store/`)
    - api-store.ts (server state)
    - app-store.ts (UI state)

22. **Frontend Pages** (`routes/`)
    - +page.svelte (redirect based on state)
    - create/ (heroine creation)
    - universe/ (main view with NPCs)
    - simulate/ (conversation interface)
    - timeline/ (bead visualization)

23. **Frontend Components** (`lib/components/`)
    - NPCCard
    - SceneCard
    - DiffViewer
    - Navigation
    - TerminalInput

---

## File Manifest

### Backend (Python)

```
backend/
├── config.py                           # NEW - Settings
├── core/
│   ├── container.py                   # NEW - DI container
│   └── lifecycle.py                   # NEW - App lifecycle
├── database/
│   ├── __init__.py
│   ├── models.py                      # NEW - SQLAlchemy models
│   └── init.py                        # NEW - DB initialization
├── beads/
│   └── engine.py                      # NEW - DAG engine
├── llm/
│   └── service.py                     # NEW - LLM client
├── storage/
│   └── file_system.py                 # NEW - File I/O
├── services/
│   ├── __init__.py
│   ├── heroine_service.py             # NEW
│   ├── npc_service.py                 # NEW
│   ├── scene_service.py               # NEW
│   ├── bead_service.py                # NEW
│   └── simulation_service.py           # NEW
├── api/
│   ├── __init__.py
│   ├── schemas.py                     # NEW - Pydantic models
│   └── v1/
│       ├── __init__.py
│       ├── heroine.py                  # NEW
│       ├── npcs.py                     # NEW
│       ├── scenes.py                   # NEW
│       ├── beads.py                    # NEW
│       └── simulation.py               # NEW
├── prompts/                           # Existing (empty)
│   └── .gitkeep
└── main.py                            # EXISTING - Update imports

```

### Frontend (TypeScript/Svelte)

```
frontend/src/
├── lib/
│   ├── api/
│   │   └── client.ts                  # NEW - API client
│   ├── core/
│   │   └── store/
│   │       ├── api-store.ts           # NEW
│   │       └── app-store.ts           # NEW
│   ├── components/
│   │   ├── NPCCard.svelte             # NEW
│   │   ├── SceneCard.svelte           # NEW
│   │   ├── DiffViewer.svelte          # NEW
│   │   ├── Navigation.svelte          # NEW
│   │   └── TerminalInput.svelte       # NEW
│   └── event-bus.ts                   # EXISTING
├── routes/
│   ├── +page.svelte                   # UPDATE - Redirect logic
│   ├── +layout.js                     # EXISTING
│   ├── +layout.svelte                 # EXISTING
│   ├── create/
│   │   └── +page.svelte               # NEW
│   ├── universe/
│   │   └── +page.svelte              # NEW
│   ├── simulate/
│   │   └── +page.svelte              # NEW
│   └── timeline/
│       └── +page.svelte               # NEW
└── app.html                           # EXISTING - Styles
```

---

## Dependencies

### Backend (additions to requirements.txt)

```
anthropic
aiofiles
toml
```

### Frontend (additions to package.json)

```
@types/node (dev)
```

---

## Testing Strategy

### Backend Tests
- BeadEngine: create, branch, merge, rebase, cycle detection
- API endpoints: Contract tests with httpx
- Services: Unit tests with mocks

### Frontend Tests
- Stores: State update logic
- Components: Render tests

---

## Success Criteria

- [x] Database tables created and initialized
- [x] All API endpoints return correct responses
- [x] Beads DAG operations work (create, branch, merge, diff)
- [x] LangGraph simulation runs a turn
- [x] Frontend can create heroine
- [x] Frontend can view NPCs and scenes
- [x] Frontend can run simulation turn
- [x] Frontend can view timeline
