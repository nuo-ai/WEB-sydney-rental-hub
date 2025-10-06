# 悉尼租房平台 (Sydney Rental Platform)

**欢迎来到本项目！**

为了确保所有协作者都能基于同一套信息进行工作，我们采用 **Memory-Bank-Driven Development (记忆库驱动开发)** 模式。

---

## 唯一的“真理之源” (The Single Source of Truth)

本项目所有的**产品需求、技术架构、开发计划和关键决策**，都统一记录在 `/memory-bank` 目录中。

**在开始任何工作之前，请务必首先阅读 `/memory-bank` 中的文档，以快速同步项目的最新状态。**

### 快速导航

- **`memory-bank/projectbrief.md`**: 项目要解决的核心问题和目标是什么？
- **`memory-bank/productContext.md`**: 我们的用户故事和核心交互流程是怎样的？
- **`memory-bank/systemPatterns.md`**: 我们的系统是如何设计和运作的？
- **`memory-bank/techContext.md`**: 我们使用什么技术？开发环境如何设置？
- **`memory-bank/activeContext.md`**: 我们当前的工作焦点和下一步计划是什么？
- **`memory-bank/progress.md`**: 我们完整的开发路线图和当前进展如何？

---

## 本地开发

请参考 **`memory-bank/techContext.md`** 中的 “本地开发环境设置” 部分，来启动您的本地开发服务器。

### Monorepo 概览

该仓库采用 pnpm + Turborepo 工作区结构：

- `apps/web` (`@web-sydney/web`): Vite + Vue 3 前端应用。
- `apps/mcp-server` (`@web-sydney/mcp-server`): 面向 AI 助手的 TypeScript MCP Server。
- `tools/playwright` (`@web-sydney/playwright`): Playwright 配置与端到端测试集合。
- `packages/eslint-config`, `packages/stylelint-config`, `packages/tsconfig`: 供各应用复用的统一工程配置。

### 常用工作区命令

```bash
# 安装依赖并链接工作区
pnpm install

# 并行启动所有 dev 任务（例如前端 + MCP）
pnpm dev

# 构建全部包（turbo 会处理依赖关系）
pnpm build

# 仅在前端应用中运行开发服务器 / 构建 / Lint
pnpm --filter @web-sydney/web dev
pnpm --filter @web-sydney/web build
pnpm --filter @web-sydney/web lint
pnpm --filter @web-sydney/web lint:style

# MCP Server 编译与类型检查
pnpm --filter @web-sydney/mcp-server build
pnpm --filter @web-sydney/mcp-server lint

# 端到端测试（需先启动前端）
pnpm --filter @web-sydney/playwright test
```

### 质量检查与 CI

- Turborepo 任务：`pnpm turbo run lint`, `pnpm turbo run test`
- Netlify 部署：`pnpm install --frozen-lockfile && pnpm turbo run build --filter @web-sydney/web`
- GitHub Actions 如需 Node 流程，同样使用 `pnpm install` + 对应 `turbo` 任务。

---

*该项目由AI软件工程师Cline协助开发和维护。*
