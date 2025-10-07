# Frontend Style Guide

Conventions for the Vue 3 + Vite front end.

## General
- Use TypeScript with `<script setup lang="ts">` in single file components.
- Run `npm run lint` and `npm run format` before committing.
- Prettier controls formatting; do not hand craft spacing.
- State management uses Pinia; place stores in `src/stores`.
- Components use `PascalCase` filenames. Composables are `camelCase`.
- Scope styles by default and keep global CSS in `src/assets`.
- Prefer composition API and avoid options API in new code.
- Environment variables are accessed via `import.meta.env`.

## Directory Hints
- Reusable components: `src/components/`
- Pages and routes: `src/pages/`
- Composables: `src/composables/`
- Tests: `tests/` with `*.spec.ts` names.
