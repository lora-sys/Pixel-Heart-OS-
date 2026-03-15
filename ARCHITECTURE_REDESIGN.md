# Architecture Redesign - Module, Configuration, Performance, Sharing

## Goals
- **模块化**: Clear separation of concerns, each module independently testable
- **配置化**: All environment-specific values externalized, hot-reload support
- **性能化**: Connection pooling, caching, lazy loading, pagination
- **共享化**: Shared types between frontend/backend to avoid mismatches

---

## 1. Backend Architecture Refactor

### Current Issues
- ❌ Singleton management scattered (config.py, startup events)
- ❌ Bead API directly manipulates DB instead of using BeadEngine
- ❌ LLM Service instantiated per-request (wasteful)
- ❌ No caching layer (ChromaDB + DB queries repeated)
- ❌ Configuration not hot-reloadable

### Proposed Structure

```
backend/
├── core/
│   ├── __init__.py
│   ├── container.py          # Dependency injection container
│   ├── lifecycle.py          # App lifecycle manager
│   └── cache.py              # Redis-like in-memory cache (TTL)
├── services/
│   ├── __init__.py
│   ├── bead_service.py       # Business logic for beads (uses BeadEngine)
│   ├── npc_service.py        # NPC generation & refinement
│   ├── heroine_service.py    # Heroine creation
│   ├── scene_service.py      # Scene generation
│   ├── simulation_service.py # Orchestrates simulation flow
│   └── llm_service.py        # Multi-provider LLM (already abstracted)
├── infrastructure/
│   ├── database/
│   │   ├── connection.py     # Connection pool manager
│   │   ├── repositories/
│   │   │   ├── bead_repo.py
│   │   │   ├── character_repo.py
│   │   │   └── relationship_repo.py
│   │   └── models.py
│   ├── vector_store/
│   │   └── chroma_client.py  # Singleton wrapper (already good)
│   └── storage/
│       └── file_system.py    # Markdown/TOML I/O
├── interfaces/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── beads.py      # Thin layer: validate → call service
│   │   │   ├── heroine.py
│   │   │   ├── npcs.py
│   │   │   ├── scenes.py
│   │   │   └── simulation.py
│   │   └── deps.py           # FastAPI dependencies (get_session, get_services)
│   └── web/
│       └── schemas.py        # All Pydantic models (shared with frontend via codegen)
└── config/
    ├── settings.py           # Environment-based config
    ├── logging.py            # Structured logging
    └── feature_flags.py      # Toggle features (mock_llm, caching, etc.)
```

### Key Changes

1. **Container Pattern**
```python
# core/container.py
class Container:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._cache = {}
        self._services = {}

    def get_bead_engine(self) -> BeadEngine:
        if 'bead_engine' not in self._services:
            self._services['bead_engine'] = BeadEngine()
        return self._services['bead_engine']

    def get_llm_service(self) -> LLMService:
        if 'llm_service' not in self._services:
            self._services['llm_service'] = LLMService()
        return self._services['llm_service']

    def get_bead_service(self) -> BeadService:
        if 'bead_service' not in self._services:
            self._services['bead_service'] = BeadService(
                self.get_bead_engine(),
                self.get_cache()
            )
        return self._services['bead_service']
```

2. **Service Layer**
```python
# services/bead_service.py
class BeadService:
    def __init__(self, engine: BeadEngine, cache: Cache):
        self.engine = engine
        self.cache = cache

    async def create_bead(self, action: str, content: dict, branch: str = "main") -> Bead:
        # Business logic: validation, events, caching
        bead = await self.engine.create_bead(action, content, branch_name=branch)
        await self.cache.invalidate(f"timeline:{branch}")
        await self.cache.invalidate(f"head:{branch}")
        return bead

    async def get_timeline(self, branch: str, limit: int = 100) -> List[Bead]:
        cache_key = f"timeline:{branch}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        beads = await self.engine.get_timeline(branch, limit)
        await self.cache.set(cache_key, beads, ttl=60)
        return beads
```

3. **API Layer becomes thin**
```python
# interfaces/api/v1/beads.py
@router.post("", response_model=BeadResponse)
async def create_bead(
    data: BeadCreate,
    bead_service: BeadService = Depends(get_bead_service)
):
    bead = await bead_service.create_bead(
        action=data.action,
        content=data.content,
        branch=data.branch_name
    )
    return bead
```

---

## 2. Frontend Architecture Refactor

### Current Issues
- ❌ API client scattered, no error boundary
- ❌ Store mix of API data and UI state
- ❌ No request cancellation (race conditions)
- ❌ No caching of API responses
- ❌ Type definitions not shared with backend

### Proposed Structure

```
frontend/src/
├── lib/
│   ├── core/
│   │   ├── event-bus.ts        # Keep (good)
│   │   ├── store/
│   │   │   ├── app-store.ts    # UI state only
│   │   │   ├── api-store.ts    # API cache state
│   │   │   └── types.ts        # Shared with backend via codegen
│   │   └── cache/
│   │       └── api-cache.ts    # SWR-like caching
│   ├── services/
│   │   ├── api/
│   │   │   ├── client.ts       # Fetch wrapper with interceptors
│   │   │   ├── auth.ts         # Auth interceptors
│   │   │   ├── error-handler.ts# Centralized error handling
│   │   │   └── types.ts        # API response types
│   │   ├── heroine.service.ts
│   │   ├── npc.service.ts
│   │   ├── bead.service.ts
│   │   └── simulation.service.ts
│   ├── components/
│   │   ├── ui/                # Reusable UI (Button, Card, Modal)
│   │   ├── layout/            # Navigation, Footer
│   │   ├── create/            # Creation Mirror components
│   │   ├── universe/          # NPC Card, Scene Card, Diff Viewer
│   │   ├── simulate/          # Dialogue Panel, Timeline Mini
│   │   └── timeline/          # Beads DAG Canvas (Phaser wrapper)
│   └── utils/
│       ├── format.ts          # Date, number formatting
│       └── validation.ts      # Form validation
├── routes/
│   ├── +layout.ts             # Fetch initial state
│   ├── +layout.svelte
│   ├── create/
│   ├── universe/
│   ├── simulate/
│   └── timeline/
└── app.html + app.css
```

### Key Changes

1. **Service Layer with Caching**
```typescript
// lib/services/bead.service.ts
class BeadService {
  constructor(private api: ApiClient) {}

  async getTimeline(branch: string, limit: number = 100): Promise<Bead[]> {
    const cacheKey = `timeline:${branch}:${limit}`;
    const cached = apiCache.get(cacheKey);
    if (cached) return cached;

    const beads = await this.api.get<Bead[]>(`/beads/timeline?branch=${branch}&limit=${limit}`);
    apiCache.set(cacheKey, beads, 60000); // 1 min TTL
    return beads;
  }

  async createBead(data: BeadCreate): Promise<Bead> {
    const bead = await this.api.post<Bead>('/beads', data);
    // Invalidate related caches
    apiCache.delete(`timeline:${data.branch_name}`);
    apiCache.delete(`head:${data.branch_name}`);
    // Update app store
    appStore.beads.push(bead);
    return bead;
  }
}
```

2. **App Store: UI State Only**
```typescript
// lib/core/store/app-store.ts
export const uiStore = $state({
  // UI state only (loading, errors, modals)
  loading: false,
  error: null,
  modalOpen: false,
  // Server state references (IDs only)
  currentHeroineId: null,
  currentBeadId: null,
});

// Derived from API cache
export const heroine = $derived(() => {
  if (!uiStore.currentHeroineId) return null;
  return apiCache.get(`heroine:${uiStore.currentHeroineId}`);
});
```

3. **Centralized Error Handling**
```typescript
// lib/services/api/error-handler.ts
export function handleError(error: any): AppError {
  if (error.status === 401) {
    goto('/login');
    return new AppError('Unauthorized');
  }
  if (error.status === 429) {
    return new AppError('Rate limit exceeded. Please wait.');
  }
  return new AppError(error.message || 'Unknown error');
}
```

---

## 3. Communication Protocol

### REST API Design (Versioned)

```
Base: /api/v1

Heroine:
  POST   /heroine/create        { description, input_mode } → HeroineResponse
  GET    /heroine/              → HeroineResponse | 404

NPCs:
  POST   /npcs/generate         → NPCResponse[]
  GET    /npcs                 → NPCResponse[]
  GET    /npcs/{id}            → NPCResponse
  PATCH  /npcs/{id}/refine     → NPCRefineResponse {original, suggested, diff}
  POST  /npcs/{id}/refine/apply → {status, npc_id}

Scenes:
  POST   /scenes/generate       → SceneResponse[]
  GET    /scenes               → SceneResponse[]
  GET    /scenes/{id}          → SceneResponse

Beads:
  GET    /beads/timeline?branch=&limit=&offset= → BeadSummary[]
  POST   /beads                → BeadResponse
  POST   /beads/branch         → BranchResponse
  POST   /beads/merge          → BeadResponse
  GET    /beads/{id}/diff      → BeadDiffResponse

Simulation:
  GET    /simulate/state       → SimulationStateResponse
  POST   /simulate/turn        → SimulationTurnResponse
```

### WebSocket (Future)
For real-time narrative updates:
```
WS /ws/simulation
Message: { type: 'turn_complete', bead_id: '...', npc_responses: [...] }
```

---

## 4. Performance Optimizations

### Backend
- **Connection Pool**: SQLAlchemy async engine with pool_size=10, max_overflow=20
- **Caching**: Redis (optional) for frequently accessed data (current HEAD, heroine profile)
- **ChromaDB**: Single persistent client (singleton), batch embeddings
- **LLM**: Concurrent requests using asyncio.gather (already in graph)
- **DB Indexes**: Already defined on `beads(branch_name, timestamp)`, `beads(action)`, `relationships(character_id, target_character_id)`

### Frontend
- **SWR/LRU Cache**: API responses cached in memory (1-5 min TTL)
- **Request Coalescing**: Duplicate concurrent requests deduped
- **Lazy Loading**: Phaser scenes only load resources when needed
- **Virtual Scrolling**: For beads timeline > 100 nodes
- **Debounced Events**: Search inputs, resize handlers

---

## 5. Shared Types (Code Generation)

To prevent type mismatches:

```
shared/
├── types/
│   ├── bead.ts              # Frontend: interface Bead
│   ├── bead.py              # Backend: @dataclass Bead
│   ├── heroine.ts
│   ├── heroine.py
│   ├── npc.ts
│   ├── npc.py
│   └── api-responses.ts     # All API response types
├── generate.js               # Codegen script: generates .ts from .py or vice versa
└── package.json             # NPM package to publish types (optional)
```

Or use **OpenAPI/Swagger** auto-generation:
```bash
# Generate TypeScript from FastAPI OpenAPI spec
openapi-typescript https://localhost:8000/openapi.json --output src/lib/api/types.ts
```

---

## 6. Configuration Management

### Backend (`config.py`)

```python
class Settings(BaseSettings):
    # Providers
    llm_provider: Literal["anthropic", "stepfun", "mock"] = "mock"
    anthropic_api_key: Optional[str] = None
    stepfun_api_key: Optional[str] = None

    # Performance
    cache_enabled: bool = True
    cache_ttl_beads: int = 60  # seconds
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Features
    enable_websocket: bool = False
    enable_analytics: bool = False

    # Paths (absolute)
    data_dir: Path = Path(__file__).parent.parent / "data"
    chroma_db_path: Path = Path(__file__).parent.parent / "chroma_db"

    class Config:
        env_file = ".env"
        case_sensitive = False
```

### Frontend (`lib/config/index.ts`)

```typescript
export const config = {
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
    timeout: 30000,
    retry: 2,
  },
  cache: {
    enabled: true,
    defaultTTL: 60000,
  },
  features: {
    mockLLM: import.meta.env.VITE_USE_MOCK_LLM === 'true',
    websocket: false,
  },
  phaser: {
    width: 800,
    height: 600,
    pixelSize: 4,
  } as const,
};
```

---

## 7. Implementation priorities

### Phase 1: Fix Critical Bugs (P0)
1. ✅ Bead ID hash unified (use BeadEngine everywhere)
2. ✅ Beads API uses BeadService instead of direct DB
3. ✅ Config singleton getters (done)
4. ✅ Simulation graph singleton injection (done)

### Phase 2: Performance & Architecture (P1)
5. Implement BeadService layer
6. Add API response caching (LRU)
7. Refactor API endpoints to use service layer
8. Add request deduplication in API client

### Phase 3: UX Polish (P2)
9. Implement Phaser reactive updates (listen to store changes)
10. Add SWR caching for API responses
11. Implement Nebula visualization
12. Add transitions/animations

### Phase 4: Quality (P2)
13. Write unit tests for services
14. Add integration tests
15. Set up Sentry/error tracking
16. Add logging middleware

---

## Conclusion

This redesign separates concerns:
- **Services** encapsulate business logic
- **Repositories** encapsulate data access
- **API** only validates and serializes
- **Frontend** has clear service layer + cache
- **Configuration** is centralized and type-safe

Next: Implement these changes systematically.
