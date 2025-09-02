# Repository Guidelines

## Project Structure & Modules
- `backend/`: FastAPI app, GraphQL schema, Celery tasks, DB CRUD and models.
- `vue-frontend/`: Vue 3 + Vite UI, Pinia stores, routing, ESLint/Prettier.
- `mcp-server/`: TypeScript MCP server for AI assistants.
- `scripts/` and `database/`: Utilities, ETL helpers, SQL and data processors.
- `crawler/`: Feature extraction and integration examples.
- Docs: see `README.md`, `AUTHENTICATION_GUIDE.md`, `FRONTEND_STYLE_GUIDE.md`, `SECURITY_CHECKLIST.md`.

## Build, Test, Develop
- Backend
  - Create env: `python -m venv .venv && . .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
  - Install: `pip install -r requirements.txt`
  - Run API: `uvicorn backend.main:app --reload --port 8000`
  - Celery worker: `celery -A backend.celery_worker.celery_app worker -l info`
  - .env: copy from `backend/.env.example` or project `.env.example`.
- Frontend
  - `cd vue-frontend && npm install`
  - Dev: `npm run dev` (http://localhost:5173)
  - Build: `npm run build`; Lint/format: `npm run lint`, `npm run format`
- MCP Server (optional; currently disabled)
  - Only enable if needed for AI tooling integration.
  - `cd mcp-server && npm install && npm run build`
  - Start: `npm start` (requires local config and backend availability)

## Coding Style & Naming
- Python: PEP 8, 4‑space indent, type hints; `snake_case` for modules/functions, `PascalCase` for classes. Keep API in `backend/api`, DB ops in `backend/crud`, models in `backend/models`.
- Vue/TS: follow `eslint.config.js` and Prettier; SFCs named `PascalCase` (e.g., `PropertyDetail.vue`), non‑component files `kebab-case`.
- Commits and PR titles use Conventional Commits (see below).

## Testing Guidelines
- Backend: targeted scripts exist; examples: `python backend/test_auth.py`, `python scripts/test_api.py`. Ensure DB/Redis and `.env` are set.
- Frontend: Playwright configured (`playwright.config.js`). With dev server running, run: `npx playwright test`. Place specs under `tests/` as `*.spec.(ts|js)`.
- Aim for meaningful assertions around APIs and critical UI flows.

## Commits & Pull Requests
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:` (seen in history). Example: `feat(backend): add commute time query`.
- PRs: include scope/summary, linked issue, reproduction steps, and screenshots/GIFs for UI changes. Verify `npm run lint`, backend starts, and key tests/scripts pass.

## Security & Config
- Never commit secrets. Use `.env` files from `*.env.example`. Review `SECURITY_CHECKLIST.md`.
- Configure external keys per `GOOGLE_MAPS_API_SETUP.md`. For auth flows see `AUTHENTICATION_GUIDE.md`.
