# Troubleshooting - Pixel Heart OS

## 🔧 Common Issues

### 1. `bun install` hangs or fails

**Symptom**: Command stops at "Resolving dependencies" or exits with code 144.

**Cause**: Bun's registry access or network connectivity issues.

**Solutions**:

**Option A: Use npm instead (simplest)**
```bash
cd frontend
npm install
```
The project is compatible with npm - all scripts work the same.

**Option B: Clear Bun cache and retry**
```bash
bun pm cache rm
cd frontend
bun install --no-progress --verbose
```

**Option C: Use yarn**
```bash
npm install -g yarn
cd frontend
yarn install
```

---

### 2. Backend import errors

**Symptom**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. `uvicorn` not found

**Symptom**: `bash: uvicorn: command not found`

**Solution**: Install inside virtualenv:
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 4. Database errors

**Symptom**: `sqlite3.OperationalError: no such table: beads`

**Solution**: Initialize database:
```bash
cd backend
source .venv/bin/activate  # if using venv
python -m database.init
```

---

### 5. LLM API errors

**Symptom**: `Invalid API key` or `Rate limit exceeded`

**Solution**:
1. Check `backend/.env` file exists and has valid `ANTHROPIC_API_KEY`
2. Get a key from https://console.anthropic.com
3. Ensure you have credits on your account

**Testing your API key**:
```bash
python -c "from llm.service import LLMService; import asyncio; async def test(): s=LLMService(); print(await s.parse_heroine('test')); asyncio.run(test())"
```

---

### 6. Import errors in Svelte components

**Symptom**: `Cannot find module '$lib/...'`

**Cause**: SvelteKit alias not configured.

**Solution**:
```bash
cd frontend
bunx svelte-kit sync
# or
npm run check
```

---

### 7. Port already in use

**Symptom**: `Error: listen EADDRINUSE: address already in use :::5173`

**Solution**:
```bash
# Find and kill process
lsof -ti:5173 | xargs kill -9  # macOS/Linux
# or use different port:
bun run dev --port 5174
```

---

### 8. TypeScript errors in API client

**Symptom**: `error TS2307: Cannot find module ...`

**Solution**: Ensure API endpoints return types matching schemas in `backend/api/schemas.py`. The TypeScript client expects JSON responses.

---

### 9. Phaser not loading

**Symptom**: Canvas is blank or Phaser is undefined.

**Solution**:
- Check browser console for errors
- Ensure `phaser` is in `frontend/package.json` dependencies
- Reinstall: `cd frontend && bun install` (or npm install)

---

### 10. Beads timeline not showing

**Symptom**: `/timeline` page shows empty or error.

**Checklist**:
- [ ] Backend `/api/v1/beads/timeline` returns data (check http://localhost:8000/docs)
- [ ] Database has bead records (`SELECT * FROM beads;`)
- [ ] `state.beads` in frontend store is populated (check devtools)
- [ ] Phaser scene in `PhaserGame.svelte` receives bead data via EventBus

---

## 📊 Verify Installation

Run these checks:

### Backend
```bash
cd backend
source .venv/bin/activate  # if using venv
python -c "import main; print('✅ Backend imports OK')"
python -m database.init    # Should say "Database initialized"
uvicorn main:app --reload  # Visit http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
bun install --dry-run  # or npm install --dry-run
bun run check         # Type checking
bun run dev           # Should start on http://localhost:5173
```

---

## 🆘 Need More Help?

1. Check `DEVELOPMENT_SUMMARY.md` for architecture details
2. Review `CLAUDE.md` for codebase conventions
3. Open an issue with:
   - OS and versions (Bun, Python, Node)
   - Full error message
   - Steps to reproduce
   - Relevant log output

---

**Last updated**: 2025-03-15 | **Status**: Early development (API keys required)
