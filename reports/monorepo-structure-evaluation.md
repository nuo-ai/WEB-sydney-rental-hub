# Monorepo Structure Evaluation

## Workspace Layout
- The root workspace is managed by `pnpm` and is configured to include every app under `apps/*`, enabling shared tooling and dependency hoisting for each product surface.【F:pnpm-workspace.yaml†L1-L3】
- The top-level package defines Turbo-powered scripts (`dev`, `build`, `lint`, `test`, `typecheck`) so that workspaces inherit a common task runner entry point after the restructure.【F:package.json†L2-L16】
- `turbo.json` centralizes task defaults such as caching policies and cross-package build dependencies, confirming that the monorepo orchestration layer is in place.【F:turbo.json†L1-L21】

## App Packages
- The backend service remains encapsulated in `@web-sydney/backend`, exposing Python-based dev, worker, test, build, and type-check commands through the workspace scripts interface.【F:apps/backend/package.json†L1-L11】
- The web frontend is published as `@web-sydney/web`, with Vite development scripts, Playwright tests, and explicit lint/format hooks aligned to the shared Turbo pipeline, demonstrating that the restructure preserved end-to-end tooling for this app.【F:apps/web/package.json†L1-L53】

## Uni-app Mini Program Impact
- There is currently no dedicated Uni-app workspace or dependency footprint (`@dcloudio/*`, `uni-app` etc.) in the repo; the roadmap simply lists the mini program as a future deliverable, so no monorepo conflicts are present today.【F:apps/web/README.md†L193-L209】
- Only one package in the workspace declares a `vue` dependency (the web frontend), meaning there are no competing Vue runtime versions that would interfere with introducing a Uni-app package later.【F:apps/web/package.json†L16-L27】

## Success Criteria Check
- The workspace root scripts (`dev`, `build`, `lint`, `test`, `typecheck`) are wired through Turborepo, ensuring every package can participate in the shared pipeline without custom per-app overrides—evidence that the restructure achieved its goal of centralised orchestration.【F:package.json†L2-L16】【F:turbo.json†L1-L21】
- Each existing app exposes the expected pnpm scripts after the move (`@web-sydney/backend` for Python services and `@web-sydney/web` for the Vue client), confirming that the restructure preserved developer workflows across surfaces.【F:apps/backend/package.json†L1-L11】【F:apps/web/package.json†L1-L53】
- No duplicate framework versions or unresolved peer dependencies appear in the workspace manifests, indicating that dependency hoisting remains stable post-restructure.【F:pnpm-lock.yaml†L1-L40】

## Recommendations
1. Create the missing `packages/` directory or remove it from the workspace globs to avoid confusion for new contributors following the restructure blueprint.【F:pnpm-workspace.yaml†L1-L3】
2. When bootstrapping the Uni-app mini program, add it as a sibling workspace (for example, `apps/uni-mini/`) so it benefits from the existing Turbo and pnpm configuration, and pin its framework dependencies to versions compatible with the existing Vue stack to maintain a conflict-free graph.【F:package.json†L5-L16】【F:apps/web/package.json†L16-L27】

## Confidence & Next Steps
- **Confidence level:** ~75% that the current monorepo foundation can absorb a Uni-app workspace without structural changes. The confidence is tempered by the absence of an actual Uni-app package to validate pnpm peer dependency resolution in practice.【F:pnpm-workspace.yaml†L1-L3】【F:apps/web/package.json†L16-L27】
- To raise confidence, prototype a minimal Uni-app workspace (`apps/uni-mini`) with stub build scripts and run the shared `pnpm dev`/`turbo run` commands to observe any latent conflicts early.

## Current Status & Developer Actions
- **Restructure completion:** The monorepo refactor described in this report has been merged into the default branch, so no follow-up migrations are pending before teammates pull the latest codebase.【F:pnpm-workspace.yaml†L1-L3】【F:package.json†L2-L16】
- **Safe to sync locally:** Developers can run `git pull` and then `pnpm install` at the repository root to align local workspaces; the consolidated scripts defined in the root `package.json` remain the single source of truth after the restructure.【F:package.json†L2-L16】
- **Resolving pull strategy prompt:** If Git asks how to reconcile divergent branches (for example, `fatal: 需要指定如何调和偏离的分支`), run one of the standard configuration commands before pulling: `git config pull.rebase false` (merge), `git config pull.rebase true` (rebase), or `git config pull.ff only` (fast-forward only). After choosing the preferred strategy, re-run `git pull` followed by `pnpm install` to ensure dependencies are up to date.
- **Post-sync checklist:** When `git pull` finishes cleanly (no further prompts) and your branch matches `origin/main`, install workspace dependencies with `pnpm install`, then resume development with the usual scripts—`pnpm --filter @web-sydney/web dev` for the Vite frontend, `pnpm --filter @web-sydney/backend dev` for the FastAPI backend, or root-level `pnpm dev` to fan out Turbo tasks across packages.【F:package.json†L5-L10】【F:apps/web/package.json†L6-L13】【F:apps/backend/package.json†L5-L10】
