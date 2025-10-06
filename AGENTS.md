# Repository Guidelines

## Project Structure & Modules
- `apps/web/`: Vue 3 + Vite UI (pnpm workspace package `@web-sydney/web`).
- `apps/mcp-server/`: TypeScript MCP server for AI assistants (`@web-sydney/mcp-server`).
- `tools/playwright/`: Shared Playwright config + e2e specs (`@web-sydney/playwright`).
- `packages/*`: Shared linting/TypeScript configs consumed by workspace apps.
- `backend/`: FastAPI app, GraphQL schema, Celery tasks, DB CRUD and models.
- `scripts/` and `database/`: Utilities, ETL helpers, SQL and data processors.
- `crawler/`: Feature extraction and integration examples.
- Docs: see `README.md`, `AUTHENTICATION_GUIDE.md`, `FRONTEND_STYLE_GUIDE.md`, `SECURITY_CHECKLIST.md`, `GOOGLE_MAPS_API_SETUP.md`.

## Build, Test, Develop
- Backend
  - Create env: `python -m venv .venv && . .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
  - Install: `pip install -r requirements.txt`
  - Run API: `uvicorn backend.main:app --reload --port 8000`
  - Celery worker: `celery -A backend.celery_worker.celery_app worker -l info`
  - .env: copy from `backend/.env.example` or project `.env.example`.
- Frontend (`@web-sydney/web`)
  - Install workspace deps once: `pnpm install`
  - Dev: `pnpm --filter @web-sydney/web dev` (http://localhost:5173)
  - Build: `pnpm --filter @web-sydney/web build`
  - Lint/format: `pnpm --filter @web-sydney/web lint`, `pnpm --filter @web-sydney/web lint:style`, `pnpm --filter @web-sydney/web format`
- MCP Server (`@web-sydney/mcp-server`)
  - Build: `pnpm --filter @web-sydney/mcp-server build`
  - Dev/watch: `pnpm --filter @web-sydney/mcp-server dev`
  - Start: `pnpm --filter @web-sydney/mcp-server start` (requires backend + config)
- Playwright E2E (`@web-sydney/playwright`)
  - Run against running dev server: `pnpm --filter @web-sydney/playwright test`

## Coding Style & Naming
- Python: PEP 8, 4‑space indent, type hints; `snake_case` for modules/functions, `PascalCase` for classes. Keep API in `backend/api`, DB ops in `backend/crud`, models in `backend/models`.
- Vue/TS: follow `eslint.config.js` and Prettier; SFCs named `PascalCase` (e.g., `PropertyDetail.vue`), non‑component files `kebab-case`.
- Commits and PR titles use Conventional Commits (see below).

## Testing Guidelines
- Backend: targeted scripts exist; examples: `python backend/test_auth.py`, `python scripts/test_api.py`. Ensure DB/Redis and `.env` are set.
- Frontend E2E: Playwright lives in `tools/playwright/`. Run `pnpm --filter @web-sydney/playwright test` with the web dev server running.
- Aim for meaningful assertions around APIs and critical UI flows.

## Commits & Pull Requests
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:` (seen in history). Example: `feat(backend): add commute time query`.
- PRs: include scope/summary, linked issue, reproduction steps, and screenshots/GIFs for UI changes. Verify `pnpm turbo run lint` (and `lint:style`), backend starts, and key tests/scripts pass.

## Security & Config
- Never commit secrets. Use `.env` files from `*.env.example`. Review `SECURITY_CHECKLIST.md`.
- Configure external keys per `GOOGLE_MAPS_API_SETUP.md`. For auth flows see `AUTHENTICATION_GUIDE.md`.
