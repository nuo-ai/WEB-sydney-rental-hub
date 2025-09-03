# Pull Request Template

## Summary
- What problem does this PR solve?
- Briefly describe the approach and scope.

## Related Issues
- Closes #
- Related #

## Changes
- [ ] Backend (FastAPI/Celery)
- [ ] Frontend (Vue 3)
- [ ] MCP Server (TypeScript)
- [ ] Scripts/ETL/Database
- Key changes:
  - 

## Screenshots / Demos
- UI changes: include before/after or a short GIF.

## How To Test
- Env: copy `.env.example` to `.env` and set required keys.
- Backend:
  - `pip install -r requirements.txt`
  - `uvicorn backend.main:app --reload --port 8000`
  - Optional targeted test: `python backend/test_auth.py` or `python scripts/test_api.py`
- Frontend:
  - `cd vue-frontend && npm install && npm run dev`
  - Optional e2e: `npx playwright test` (dev server on 5173)
- MCP Server:
  - `cd mcp-server && npm install && npm run build && npm start`
- List specific steps to verify the change:
  1. 
  2. 

## Risk & Rollback
- Risk level: Low / Medium / High
- Rollback plan: steps to revert and data migration notes.

## Checklist
- [ ] Conventional Commit message (feat/fix/docs/refactor, scope if relevant)
- [ ] Updated docs if needed (README/AGENTS/SECURITY)
- [ ] Lint passes: `cd vue-frontend && npm run lint`
- [ ] Backend runs locally without errors
- [ ] Tests/scripts executed (list which)
- [ ] No secrets or credentials committed

## Additional Notes
- Architecture or trade-offs, follow-ups, and out-of-scope items.

