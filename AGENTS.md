# Repository Guidelines

## Project Structure & Modules
- `apps/backend/`: FastAPI app, GraphQL schema, Celery tasks, DB CRUD and models.
- `vue-frontend/`: Vue 3 + Vite UI, Pinia stores, routing, ESLint/Prettier.
- `apps/mcp-server/`: TypeScript MCP server for AI assistants.
- `scripts/` and `database/`: Utilities, ETL helpers, SQL and data processors.
- `crawler/`: Feature extraction and integration examples.
- Docs: see `README.md`, `AUTHENTICATION_GUIDE.md`, `FRONTEND_STYLE_GUIDE.md`, `SECURITY_CHECKLIST.md`, `GOOGLE_MAPS_API_SETUP.md`.

## Build, Test, Develop
- Backend
  - Create env: `python -m venv .venv && . .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
  - Install: `pip install -r requirements.txt`
  - Run API: `pnpm --filter @web-sydney/backend dev`
  - Celery worker: `pnpm --filter @web-sydney/backend worker`
  - .env: copy from `apps/backend/.env.example` or project `.env.example`.
- Frontend
  - `pnpm install --filter @web-sydney/web`
  - Dev: `pnpm --filter @web-sydney/web dev` (http://localhost:5173)
  - Build: `pnpm --filter @web-sydney/web build`; Lint/format: `pnpm --filter @web-sydney/web lint`, `pnpm --filter @web-sydney/web format`
- MCP Server (optional; currently disabled)
  - Only enable if needed for AI tooling integration.
  - `cd apps/mcp-server && pnpm install && pnpm run build`
  - Start: `pnpm start` (requires local config and backend availability)

## Coding Style & Naming
- Python: PEP 8, 4‑space indent, type hints; `snake_case` for modules/functions, `PascalCase` for classes. Keep API in `apps/backend/api`, DB ops in `apps/backend/crud`, models in `apps/backend/models`.
- Vue/TS: follow `eslint.config.js` and Prettier; SFCs named `PascalCase` (e.g., `PropertyDetail.vue`), non‑component files `kebab-case`.
- Commits and PR titles use Conventional Commits (see below).

## Testing Guidelines
- Backend: targeted scripts exist; examples: `python apps/backend/test_auth.py`, `python scripts/test_api.py`. Ensure DB/Redis and `.env` are set.
- Frontend: Playwright configured (`playwright.config.js`). With dev server running, run: `npx playwright test`. Place specs under `tests/` as `*.spec.(ts|js)`.
- Aim for meaningful assertions around APIs and critical UI flows.

## Commits & Pull Requests
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:` (seen in history). Example: `feat(backend): add commute time query`.
- PRs: include scope/summary, linked issue, reproduction steps, and screenshots/GIFs for UI changes. Verify `npm run lint`, backend starts, and key tests/scripts pass.

## Security & Config
- Never commit secrets. Use `.env` files from `*.env.example`. Review `SECURITY_CHECKLIST.md`.
- Configure external keys per `GOOGLE_MAPS_API_SETUP.md`. For auth flows see `AUTHENTICATION_GUIDE.md`.
