# Pixel Heart OS - Phase 3: Advanced Features & Integration

## TL;DR

> **Quick Summary**: Implement advanced features including real LLM integration, LangGraph workflows, ChromaDB vector storage, frontend-backend integration, and Phaser visualization
> 
> **Deliverables**:
> - Real LLM service with Anthropic API integration
> - LangGraph simulation workflow with state persistence
> - ChromaDB integration for semantic search
> - Full frontend-backend integration
> - Phaser relationship nebula visualization
> - Timeline visualization component
> 
> **Estimated Effort**: High
> **Parallel Execution**: YES - 5 waves
> **Critical Path**: LLM Service → LangGraph → Frontend Integration

---

## Context

### Original Request
User completed Phase 2 (core features) and requested end-to-end testing, git commit/push, and Phase 3 planning with ultrawork mode.

### Implementation Decisions
- **Scope**: Full implementation following CLAUDE.md patterns
- **LLM Integration**: Real Anthropic API with mock fallback
- **Vector Store**: ChromaDB for semantic conversation retrieval
- **Frontend Integration**: Complete SvelteKit pages with real API calls
- **Visualization**: Phaser 3 for relationship nebula and timeline

---

## Phase 3 Features

### Wave 1: LLM Service & Integration

1. **LLM Service** (`backend/llm/service.py`)
   - Anthropic API integration
   - Mock mode fallback (USE_MOCK_LLM=True)
   - Prompt templates for heroine parsing, NPC generation, dialogue generation
   - Error handling and retry logic
   - Response caching

2. **Prompt Templates** (`backend/prompts/*.txt`)
   - `heroine_parsing.txt` - Parse description into soul/identity/voice
   - `npc_generation.txt` - Generate NPC personalities
   - `dialogue_generation.txt` - Generate NPC dialogue responses
   - `scene_generation.txt` - Generate scene descriptions

### Wave 2: LangGraph Simulation Workflow

3. **Simulation Graph** (`backend/graphs/simulation_graph.py`)
   - State machine with retrieve_context, process_action, generate_responses, update_relationships, commit_bead nodes
   - ChromaDB integration for context retrieval
   - Parallel NPC response generation
   - Relationship delta aggregation
   - Bead commit with checkpoint

4. **Graph Nodes** (individual async functions)
   - `retrieve_context` - Semantic search + NPC backstories
   - `process_player_action` - Intent parsing
   - `generate_npc_responses` - Parallel LLM calls
   - `update_relationships` - Aggregate deltas, clamp to [-1, 1]
   - `commit_bead` - Create bead, attach to branch

### Wave 3: ChromaDB Vector Store

5. **ChromaDB Client** (`backend/vector_store/chroma_client.py`)
   - Collection management (conversations, npc_backstories)
   - Embedding generation (all-MiniLM-L6-v2)
   - Semantic search with similarity scores
   - CRUD operations for embeddings

6. **Conversation Indexing**
   - Index each turn with metadata (branch_name, timestamp, participants)
   - Query by semantic similarity for context retrieval

### Wave 4: Frontend Integration

7. **Frontend Pages** (complete implementation)
   - `routes/+page.svelte` - Heroine creation (already created)
   - `routes/universe/+page.svelte` - Universe view (needs real API integration)
   - `routes/simulate/+page.svelte` - Simulation interface (needs real API integration)
   - `routes/timeline/+page.svelte` - Timeline visualization (NEW)

8. **Frontend Components**
   - `NPCCard.svelte` - NPC display with relationship indicator
   - `SceneCard.svelte` - Scene display with atmosphere badge
   - `DiffViewer.svelte` - Bead diff comparison
   - `Navigation.svelte` - Top navigation bar
   - `TerminalInput.svelte` - Retro-style text input

9. **Phaser Visualization** (`frontend/src/lib/PhaserGame.svelte`)
   - Relationship nebula (nodes = NPCs, edges = relationships)
   - Node coloring by archetype
   - Edge coloring by relationship strength
   - Timeline bar at bottom with bead markers
   - Click interaction to select bead

### Wave 5: Advanced Features

10. **Bead Engine Full Implementation** (`backend/beads/engine.py`)
    - Cycle detection with `_would_create_cycle()`
    - Branch management with `create_branch()`, `merge_branches()`, `rebase_branch()`
    - Diff computation with `diff_beads()`
    - Timeline traversal with `get_timeline()`

11. **Dependency Injection Container** (`backend/core/container.py`)
    - Singleton management for all services
    - Lazy initialization
    - Service interdependency injection

12. **Storage Service** (`backend/storage/file_system.py`)
    - Markdown file I/O for soul/identity
    - TOML file I/O for voice config
    - Directory management for heroine/npcs/scenes

---

## Technical Specifications

### LLM Service API

```python
class LLMService:
    async def parse_heroine_description(self, description: str) -> Dict[str, Any]:
        # Returns soul, identity, voice dictionaries
    
    async def generate_npc_personality(self, archetype: str, context: Dict) -> Dict[str, Any]:
        # Returns personality traits, backstory, dialogue_style
    
    async def generate_dialogue(self, npc: Dict, context: Dict, player_action: str) -> str:
        # Returns NPC dialogue response
```

### LangGraph State

```python
SimulationState = TypedDict('SimulationState', {
    'heroine_soul': Dict,
    'current_scene': Optional[Dict],
    'active_npcs': List[Dict],
    'player_action': str,
    'conversation_history': Annotated[List[Dict], lambda a, b: a + b],
    'retrieved_memories': List[Dict],
    'npc_responses': List[Dict],
    'updated_relationships': Dict[str, float],
    'bead_data': Dict,
    'new_bead_id': Optional[str]
})
```

### ChromaDB Collections

```
conversations:
  - id: {bead_id}
  - embedding: [768 floats]
  - metadata: {branch_name, timestamp, npc_ids}
  - document: "{player_action}\n{npc_responses}"

npc_backstories:
  - id: {npc_id}
  - embedding: [768 floats]
  - metadata: {archetype, role}
  - document: "{npc_personality}\n{backstory}"
```

---

## File Manifest

### Backend (Python)

```
backend/
├── llm/
│   ├── __init__.py
│   └── service.py                     # NEW
├── graphs/
│   ├── __init__.py
│   └── simulation_graph.py            # UPDATE
├── vector_store/
│   ├── __init__.py
│   └── chroma_client.py               # NEW
├── beads/
│   ├── __init__.py
│   └── engine.py                      # NEW
├── core/
│   ├── __init__.py
│   ├── container.py                   # NEW
│   └── lifecycle.py                   # NEW
├── storage/
│   ├── __init__.py
│   └── file_system.py                 # NEW
├── prompts/
│   ├── __init__.py
│   ├── heroine_parsing.txt            # NEW
│   ├── npc_generation.txt             # NEW
│   ├── dialogue_generation.txt        # NEW
│   └── scene_generation.txt           # NEW
└── infrastructure/
    └── database/
        └── repositories/
            ├── __init__.py
            ├── bead_repository.py     # NEW
            └── session_repository.py  # NEW
```

### Frontend (TypeScript/Svelte)

```
frontend/src/
├── lib/
│   ├── api/
│   │   └── client.ts                  # UPDATE (already created)
│   ├── core/
│   │   └── store/
│   │       ├── api-store.ts           # UPDATE (already created)
│   │       └── app-store.ts           # UPDATE (already created)
│   ├── components/
│   │   ├── NPCCard.svelte             # NEW
│   │   ├── SceneCard.svelte           # NEW
│   │   ├── DiffViewer.svelte          # NEW
│   │   ├── Navigation.svelte          # NEW
│   │   └── TerminalInput.svelte       # NEW
│   └── PhaserGame.svelte              # UPDATE
├── routes/
│   ├── +page.svelte                   # UPDATE (already created)
│   ├── universe/
│   │   └── +page.svelte               # UPDATE (already created)
│   ├── simulate/
│   │   └── +page.svelte               # UPDATE (already created)
│   └── timeline/
│       └── +page.svelte               # NEW
└── phaser/
    ├── main.ts                        # UPDATE
    └── scenes/
        ├── NebulaScene.ts             # NEW
        └── TimelineScene.ts           # NEW
```

---

## Success Criteria

- [ ] LLM service successfully parses heroine descriptions
- [ ] LangGraph simulation runs complete turn with real LLM
- [ ] ChromaDB indexes conversations and retrieves similar context
- [ ] Frontend can create heroine and see real data
- [ ] Frontend can run simulation and see NPC responses
- [ ] Phaser displays relationship nebula with real NPC data
- [ ] Timeline shows bead history with emotion colors
- [ ] All API endpoints work with real data flow
