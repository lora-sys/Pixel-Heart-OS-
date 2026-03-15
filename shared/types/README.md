# Shared Types

This directory contains type definitions shared between the Python backend and TypeScript frontend.

## Structure

- `shared/types/` - TypeScript types for frontend
- `shared/types.py` - Python types (mirroring Pydantic schemas)

## Keeping Types in Sync

### Option 1: Manual Maintenance (Current)
- Keep types manually in sync across backend schemas and frontend definitions
- Suitable for early development when schemas change frequently

### Option 2: OpenAPI Auto-generation (Future)
When the API stabilizes, generate TypeScript types from FastAPI's OpenAPI schema:

```bash
# Install openapi-typescript
npm install -D openapi-typescript

# Generate from backend OpenAPI spec
npx openapi-typescript http://localhost:8000/openapi.json --output src/lib/api/types.gen.ts
```

This ensures 100% type safety and eliminates manual sync errors.

## Type Mapping

| Python (Pydantic) | TypeScript |
|-------------------|------------|
| `str` | `string` |
| `int` | `number` |
| `float` | `number` |
| `bool` | `boolean` |
| `dict` | `Record<string, any>` |
| `list[T]` | `T[]` |
| `Optional[T]` | `T \| null` |
| `datetime` | `string` (ISO 8601) |
| `Enum` | `string` (union type) |

## Current Status

- [x] Basic types defined (Heroine, NPC, Bead, Scene)
- [ ] Automated generation script (TODO)
- [ ] CI/CD integration to check type mismatches (TODO)
