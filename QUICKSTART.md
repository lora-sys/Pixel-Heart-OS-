# 🚀 Quick Start Guide

Get Pixel Heart OS running in **5 minutes**.

## Prerequisites Check

```bash
# Required
bun --version         # ≥ 1.0 (or use npm)
python3 --version     # ≥ 3.11
git --version
```

## Installation

### Option 1: Automated (recommended)

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual

```bash
# Frontend
cd frontend
bun install          # or: npm install
cd ..

# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m database.init
cd ..
```

## Configuration

```bash
# Create .env file
cp backend/.env.example backend/.env

# Edit backend/.env, add:
# ANTHROPIC_API_KEY=sk-ant-...
```

⚠️ **API key required** - Get one from [Anthropic Console](https://console.anthropic.com)

## Running

### Development (2 terminals)

**Terminal 1 - Backend**:
```bash
cd backend
source .venv/bin/activate  # if using venv
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
bun run dev   # or: npm run dev
```

Open: **http://localhost:5173**

### Docker (single command)

```bash
docker-compose up -d
```

Visit: **http://localhost** (frontend) + **http://localhost:8000/docs** (API)

---

## First Run Walkthrough

1. **Create Heroine** (`/create`)
   - Type a description (e.g., "A shy librarian with abandonment issues...")
   - Click "Create Heroine"
   - Wait for LLM to parse (5-10 seconds)

2. **Universe** (`/universe`)
   - 3 NPCs generated automatically (Protector, Competitor, Shadow)
   - Click "Refine" on any NPC to AI-edit them
   - Click "Begin Simulation" when ready

3. **Simulate** (`/simulate`)
   - Type a message and press Enter/Send
   - Watch NPCs respond in character (parallel LLM calls)
   - Relationship scores update automatically

4. **Timeline** (`/timeline`)
   - See the Beads DAG visualization
   - Each node = one story turn, colored by emotion
   - Click "Branch from Here" to create alternate timeline

---

## Project Structure Recap

```
Pixel-Heart-OS/
├── frontend/         # Svelte 5 + Vite (bun/npm)
│   └── src/
│       ├── lib/     # stores, api, components
│       └── routes/  # create, universe, simulate, timeline
├── backend/          # FastAPI (Python)
│   ├── api/v1/      # REST endpoints
│   ├── beads/       # DAG memory engine
│   ├── graphs/      # LangGraph workflow
│   ├── llm/         # Claude integration
│   └── database/    # SQLAlchemy models
├── data/             # Generated story files (gitignored)
└── docker-compose.yml
```

---

## Common Issues

See **TROUBLESHOOTING.md** for:
- `bun install` hangs → use npm
- API key errors → check `.env`
- Database errors → `python -m database.init`
- Port conflicts → change ports

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure API key
3. ✅ Start servers
4. ✅ Create your first heroine
5. 🎨 **Optional**: Add custom pixel art sprites in `frontend/static/sprites/`
6. 🧪 **Optional**: Write tests (`pytest` / `vitest`)
7. 🐳 **Optional**: Deploy with Docker

---

**Enjoy building emergent stories!** ✨
