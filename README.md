# Pixel Heart OS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An AI-driven, emergent social universe system with Git-style memory branching.

📖 [Design Document v2.0](Pixel%20Heart%20OS%20_AI-Readable%20Requirements%20Document%20v2.0.md) | 🚧 [Development Status](#status) | 🛠️ [Setup](#setup) | 📦 [Tech Stack](#tech-stack)

---

## 📋 Overview

Pixel Heart OS is an innovative narrative simulation system where:

- 🎭 Create a **heroine** from free-form natural language descriptions
- 🌌 System **generates** an emergent universe: Protector, Competitor, Shadow NPCs + matching scenes
- 🔄 **Simulate** turn-based conversations with stateful AI agents (LangGraph)
- 📊 **Beads Memory System**: Git-like DAG for narrative version control with branching
- 🎨 Beautiful **pixel-art UI** (Svelte 5 + Phaser 3)

**Status**: 🟡 In Early Development (Core architecture in progress)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Svelte 5 (Runes), Phaser 3.90, Tailwind CSS |
| **Backend** | FastAPI (Python async), LangGraph |
| **Memory** | Custom Beads DAG, SQLite, ChromaDB |
| **Storage** | Markdown + TOML files |
| **AI** | Anthropic Claude API |
| **Package Manager** | **Bun** (JavaScript/TypeScript) |

---

## 🚀 Quick Start

### Prerequisites

- **Bun** ≥ 1.0 ([install](https://bun.sh))
- **Python** ≥ 3.11 (recommended 3.12)
- **Anthropic API key**

### 1. Clone & Setup

```bash
git clone <your-repo>
cd Pixel-Heart-OS-

# Install frontend dependencies (using Bun)
cd frontend
bun install

# Setup backend virtualenv
cd ../backend
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cd backend
cp .env.example .env
# Edit .env:
# - Set ANTHROPIC_API_KEY=your_key
# - (Optional) adjust DATABASE_URL, DEBUG
```

### 3. Database Init

```bash
cd backend
python -m database.init
```

### 4. Run Dev Servers

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate  # if not already
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```

Open http://localhost:5173

---

## 📁 Project Structure

```
Pixel-Heart-OS/
├── backend/
│   ├── api/v1/           # FastAPI endpoints
│   ├── beads/            # Beads DAG engine
│   ├── database/         # SQLAlchemy models
│   ├── graphs/           # LangGraph workflows
│   ├── llm/              # LLM service (Anthropic)
│   ├── storage/          # File system layer (Markdown/TOML)
│   ├── vector_store/     # ChromaDB integration
│   ├── prompts/          # LLM prompt templates
│   ├── scripts/          # Dev utilities
│   ├── pyproject.toml    # Python deps
│   └── main.py           # App entry
├── frontend/
│   ├── src/
│   │   ├── lib/          # Shared lib (stores, API client, EventBus)
│   │   ├── routes/       # Svelte pages (create, universe, simulate, timeline)
│   │   └── app.html/css  # Global styles
│   ├── package.json      # Bun-managed dependencies
│   └── vite.config.ts    # Vite configuration
├── data/                 # Generated story data (gitignored)
│   ├── heroine/
│   ├── npcs/
│   └── scenes/
├── docs/                 # Architecture docs
├── CLAUDE.md            # Claude Code guide
├── Makefile             # Dev shortcuts
└── docker-compose.yml   # Full-stack deployment
```

---

## 🧠 Core Concepts

### Beads (Memory System)

Inspired by Git, every narrative event is a **Bead** - an immutable node in a **DAG**:

- Each bead has an `id` (SHA-1), `parent` link, `branch`, `timestamp`, `action`, `content`
- Branches allow exploring "what-if" scenarios without losing main timeline
- Full history preserves every change for diffing and rollback

### LangGraph Simulation

Multi-agent workflow:

1. Retrieve context from vector memory
2. Process player action
3. Generate parallel NPC responses
4. Update relationship scores
5. Commit new bead

### Svelte 5 + Phaser 3

- **Svelte Runes** (`$state`, `$derived`, `$effect`) for UI state
- **Phaser** for pixel-art canvases (Timeline DAG, Nebula, Scenes)
- **EventBus** bridges the two without virtual DOM conflicts

---

## 🧪 Development

```bash
# Backend tests
cd backend && pytest tests/

# Frontend tests
cd frontend && bunx vitest

# Lint & format
make lint
make format

# Build for production
make build

# Docker dev environment
docker-compose up -d
```

See [Makefile](./Makefile) for more commands.

---

## 📚 Documentation

- Design Spec: [Pixel Heart OS_ AI-Readable Requirements Document v2.0.md](Pixel%20Heart%20OS%20_AI-Readable%20Requirements%20Document%20v2.0.md)
- Online Preview: https://a56cf98f.pinme.dev
- API Docs: http://localhost:8000/docs (when backend running)
- CLAUDE.md: Guidance for Claude Code instances

---

## 🤝 Contributing

This is a solo project in active development. Design decisions are documented in CLAUDE.md.

**Development principles**:

- Strict separation: Svelte handles DOM, Phaser handles canvas
- Immutability: Beads are never modified, only new ones added
- File-based storage: all narrative data as plain text (md/toml)
- Type safety: Python type hints + TypeScript

---

## 📄 License

MIT © 2025