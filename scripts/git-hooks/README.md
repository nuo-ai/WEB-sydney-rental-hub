# Git Hooks (Lightweight)

This repo ships a lightweight pre-commit hook to catch low-level issues fast:
- Frontend: ESLint (`apps/web`)
- MCP server: TypeScript typecheck (no emit)
- Python: syntax errors via `compileall`

## Enable hooks

Option A — set hooks path once per repo:

```
git config core.hooksPath scripts/git-hooks
```

Option B — copy the hook into `.git/hooks/`:

```
cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Notes
- The hook uses installed local dev tools only; it won’t install packages.
- If `typescript` is not installed in `apps/mcp-server`, it falls back to `pnpm --filter @web-sydney/mcp-server build`.
- Keep hooks fast; add heavier checks to CI or pre-push if needed.

