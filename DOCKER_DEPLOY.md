# 🐳 Docker Deployment Guide

## Quick Start (3 Commands)

```bash
# 1. Configure environment
cd backend
cp .env.example .env
# Edit .env: choose LLM provider (see below)

# 2. Build and run
cd ..
docker-compose up -d

# 3. Access
# Frontend: http://localhost
# Backend API: http://localhost:8000/docs
# Health: http://localhost:8000/health
```

---

## ⚙️ Environment Configuration (`.env`)

### Option A: Use StepFun (你指定的 API)

```bash
LLM_PROVIDER=stepfun
STEPFUN_API_KEY=your_stepfun_key_here
STEPFUN_MODEL=step-1-8k  # or step-1-32k, step-2-16k
```

### Option B: Use Anthropic (original plan)

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Option C: Mock Mode (No API key - for testing UI)

```bash
LLM_PROVIDER=mock
USE_MOCK_LLM=True
```

**Note**: Mock mode returns preset responses so you can test the full UI flow without spending API credits.

---

## 📦 What Gets Built

### Backend Container (`pixel-heart-backend`)
- Python 3.12 slim
- FastAPI + Uvicorn
- All Python dependencies from `pyproject.toml`
- Volume: `./backend/data` → `/app/data` (persists story files)
- Volume: `./backend/chroma_db` → `/app/chroma_db` (vector store)
- Health check: `GET /health`

### Frontend Container (`pixel-heart-frontend`)
- Node 20 + Bun for install
- Production build with Vite
- Served via Nginx on port 80
- Volume: `./frontend/dist` (static assets)
- Proxy: `/api/*` → `http://backend:8000`

---

## 🔍 Verify Installation

```bash
# Check containers are running
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI

# Test frontend (should load)
curl http://localhost | head -20
```

---

## 🎯 First Run Walkthrough

1. Open http://localhost → redirects to http://localhost/create
2. Enter heroine description (e.g., "A shy librarian...")
3. Click "Create Heroine" → LLM processes (5-10s)
4. Universe page auto-generates 3 NPCs + scenes
5. Click "Begin Simulation" → start chatting
6. Visit Timeline to see Beads DAG grow

---

## 🗂️ Data Persistence

All story data persists in:
- `backend/data/` - Markdown/TOML files (heroine, NPCs, scenes)
- `backend/chroma_db/` - Vector embeddings for memory
- `backend/pixel_heart.db` - SQLite database

**These are mounted as volumes**, so they survive container restarts.

---

## 🐛 Troubleshooting Docker

### Containers exit immediately
```bash
docker-compose logs backend
# Check .env file exists and has valid API key
```

### API 500 errors
```bash
# Check backend logs
docker-compose logs backend | tail -50

# Common causes:
# - Missing API key (set in .env)
# - Database not initialized (should auto-init on startup)
```

### Frontend can't reach API
```bash
# Verify CORS settings in config.py include http://localhost
# docker-compose.yml proxies /api to backend:8000
curl http://localhost/api/v1/health  # Should return JSON
```

### Port conflicts
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:80"   # change 5173 → 8080 for frontend
  - "8081:8000" # change 8000 → 8081 for backend
```

### Rebuild from scratch
```bash
docker-compose down -v  # remove containers + volumes
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Development vs Production

**Development** (current):
- `DEBUG=True` in .env
- FastAPI auto-reload enabled (via uvicorn --reload)
- Volumes mount source code not needed (Python interpreted)

**Production** (future):
- `DEBUG=False`
- Build optimized frontend (already done)
- Add gunicorn + uvicorn workers
- Add nginx rate limiting
- SSL termination

---

## 🎨 Pixel Art Assets

Currently using placeholder graphics. To add real sprites:

1. Add PNG files to `frontend/public/assets/sprites/`
2. Update `PhaserGame.svelte` to load them:
   ```javascript
   this.load.image('npc_portrait', '/assets/sprites/npc1.png');
   ```
3. Modify scene rendering to use sprites instead of circles

---

## 🚀 Performance Tips

- ChromaDB embeddings computed on first add (slow) - pre-warm cache
- Beads timeline uses SQLite indexes - paginate for >1000 beads
- LLM calls are async - don't block the event loop
- Use mock mode for UI testing (no API latency)

---

**Ready to run?** `docker-compose up -d` and open http://localhost! 🎮
