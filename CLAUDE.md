# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status: Greenfield (Planning Phase)

This repository is currently in the **design and planning phase**. No source code exists yet—only requirements documentation and visualizations. When development begins, this document will be updated with concrete commands and patterns.

## Project Overview

**Pixel Heart OS** is an AI-driven, emergent social universe system built around a central heroine character. It features:
- Git-style memory management system ("Beads")
- Multi-agent simulation powered by LangGraph
- Pixel-art UI frontend (Svelte 5 + Phaser 3)
- Full state persistence with branching timelines

The system allows users to create a heroine from free-form descriptions, automatically generates a surrounding social network (NPCs and scenes), and simulates interactions with branching narrative possibilities.

## Technology Stack (Planned)

### Frontend
- **Framework**: Svelte 5 with Runes (`$state`, `$derived`, `$effect`)
- **Game Engine**: Phaser 3 (v3.90.0) for rendering relationship nebula and scenes
- **Styling**: Tailwind CSS with custom pixel-art patterns
- **Integration**: `PhaserGame.svelte` bridge component with EventBus communication

### Backend
- **API Framework**: FastAPI (Python) with async endpoints
- **Multi-Agent Engine**: LangGraph for stateful agent workflows
- **Memory System**: Custom "Beads" system (Git-like DAG for narrative state)
- **Databases**:
  - SQLite for indexing Beads relationships
  - ChromaDB or Qdrant for vector storage (semantic retrieval)

### File Storage
- Markdown (`.md`) and TOML (`.toml`) files for character souls, identities, and voice configurations

## Key Architectural Concepts

### Beads Memory System
- Git-inspired version control for narrative state
- Directed Acyclic Graph (DAG) structure
- Enables timeline branching and parallel universe exploration
- Every significant interaction becomes a new Bead

### Multi-Agent Workflows
- LangGraph orchestrates NPC agents with state persistence
- Supports cyclical graph execution (not linear chains)
- Agents maintain context using vector database retrieval

### Frontend Integration Pattern
- Svelte handles UI state with Runes
- Phaser renders canvas-based pixel art (relationship nebula, timeline visualization)
- EventBus mediates communication between Svelte and Phaser
- Avoids virtual DOM conflicts by separating concerns

### Data Models
- `soul.md` - Core character traits, traumas, defense mechanisms
- `identity.md` - Surface-level character expression
- `voice.toml` - Speech patterns and linguistic markers
- Scene configurations in Markdown/TOML

## Core Workflows

1. **Heroine Creation**: User input (free description/questionnaire/chat import) → LLM parses soul structure → generates soul.md, identity.md, voice.toml
2. **Universe Emergence**: System generates Protector, Competitor, Shadow NPCs + matching scenes based on heroine's soul
3. **Simulation**: Turn-based interactions trigger LangGraph agents → updates state → commits new Bead
4. **Branching**: Player can branch timeline at any point to explore alternatives without losing main progression
5. **AI Collaborative Editing**: User can flag elements for refinement → AI proposes diffs → user reviews/approves changes

## Important References

- Requirements Document: `Pixel Heart OS_ AI-Readable Requirements Document v2.0.md`
- Online Design Doc: https://a56cf98f.pinme.dev (linked in README.md)
- Svelte 5 Runes: https://svelte.dev/blog/runes
- Phaser 3.90.0: https://phaser.io/news/2025/05/phaser-v390-released
- LangGraph: https://www.langchain.com/langgraph
- FastAPI Async: https://fastapi.tiangolo.com/async/

## When Development Begins

✅ **Development has BEGUN!** Source code is being implemented from scratch according to this architecture.

### Current Build Commands

```bash
# Backend (Python FastAPI)
cd backend
uvicorn main:app --reload --port 8000

# Frontend (Svelte 5 + Phaser)
cd frontend
bun run dev   # Starts on http://localhost:5173

# Full stack with Docker
docker-compose up -d
```

### Linting & Formatting

```bash
# Backend
cd backend
black .           # Format Python
ruff check .      # Lint
pytest tests/     # Run tests

# Frontend
cd frontend
bunx eslint src/          # Lint
bunx prettier --write src/ # Format
bunx svelte-check        # Type check
bunx vitest run          # Unit tests
```

### Project Structure (ACTUAL)

```
pixel-heart-os/
├── backend/            # FastAPI + LangGraph + SQLAlchemy
│   ├── api/v1/         # REST endpoints (heroine, npcs, scenes, beads, simulation)
│   ├── beads/          # DAG memory engine (Git-style)
│   ├── database/       # SQLAlchemy models + async engine
│   ├── graphs/         # LangGraph workflows
│   ├── llm/            # Anthropic API integration
│   ├── storage/        # File system (Markdown/TOML)
│   ├── vector_store/   # ChromaDB semantic检索
│   └── main.py         # FastAPI app
├── frontend/           # Svelte 5 + Vite + Bun
│   ├── src/lib/
│   │   ├── stores/     # $state global app state
│   │   ├── api/        # Fetch clients
│   │   ├── components/ # Svelte components
│   │   └── event-bus.ts# Svelte⇄Phaser bridge
│   ├── src/routes/     # create, universe, simulate, timeline
│   └── src/app.html    # Global pixel art CSS
├── data/               # Generated markdown/toml files (gitignored)
├── docker-compose.yml  # Full-stack orchestration
└── Makefile            # Dev shortcuts
```

### Development Setup

1. **Install Bun**: https://bun.sh
2. **Python 3.11+**: with venv support
3. **Anthropic API key**: set in `backend/.env`
4. Run: `python -m database.init` to create SQLite tables
5. Start servers: `make dev` (or separate terminals)

### Common Tasks

- **Add new NPC role**: Modify `backend/llm/service.py:generate_npc()` role_descriptions dict
- **Add new scene type**: Extend `backend/llm/service.py:generate_scene()` prompt
- **Modify Beads DAG**: `backend/beads/engine.py` - add branching/merging logic
- **Change pixel art style**: `frontend/src/app.html` CSS variables (colors, borders)
- **Add new LangGraph node**: `backend/graphs/simulation_graph.py` - add node to workflow
- **Adjust Svelte 5 reactivity**: `frontend/src/lib/stores/app-store.ts` - modify $state

---

## Current Repository Status (Phase 1 Complete)

✅ **Project scaffolding complete**:
- [x] Directory structure created
- [x] Backend FastAPI + SQLAlchemy + LangGraph foundation
- [x] Frontend Svelte 5 + Vite + Tailwind setup
- [x] Core API endpoints (heroine, npcs, scenes, beads, simulation)
- [x] Beads DAG engine (basic CRUD, branching)
- [x] LLM service integration (Anthropic API)
- [x] File storage layer (Markdown/TOML)
- [x] ChromaDB vector store
- [x] Phaser 3 + Svelte EventBus integration
- [x] Navigation & basic pages (create, universe, simulate, timeline)
- [x] Docker & CI/CD configuration
- [x] Updated README with developer docs

🟡 **Next**: Integrate and test end-to-end flow (requires live API key)

See `TaskList` for detailed progress tracking.

## Current Repository Contents

- `README.md` - Project introduction with link to design doc
- `Pixel Heart OS_ AI-Readable Requirements Document v2.0.md` - Comprehensive specifications (the source of truth)
- `index.html` - Interactive HTML visualization of the requirements (for presentation)
- `.git/` - Version control
- `.claude/` - Claude Code settings

## Notes for Future Claude Instances

- The requirements document is detailed and should be treated as the authoritative design specification
- The architecture intentionally separates Svelte (UI state) from Phaser (canvas rendering) via an EventBus pattern—maintain this separation
- The Beads system is a core innovation—any changes to memory management should be considered carefully
- LangGraph state graphs should mirror narrative flow; avoid linear agent chains where state needs to persist across turns
- All character data (soul, identity, voice) is stored as plain text files (md/toml) for editability and version control friendliness
