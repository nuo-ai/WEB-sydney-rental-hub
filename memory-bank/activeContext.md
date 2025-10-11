# 当前上下文与焦点
**最后更新**：2025-02-14

## 当前焦点 (Current Focus)
- 巩固设计系统基础设施：统一 Storybook 8.6.x 依赖、保持 `packages/ui` 与 `apps/web` 的组件规范一致。
- 确保仓库以 pnpm + Turborepo 为唯一事实来源，杜绝遗留的 npm/原型文件引入的歧义。 

## 刚完成的工作 (Latest)
- 移除过时的 `package-lock.json` 及静态原型 HTML，清理空目录，恢复精简的仓库视图。 
- 在根工作区与子包中统一 Storybook 版本到 8.6.14，消除跨包冲突。
- 更新技术记忆库（techContext、systemPatterns）以反映最新工具链与工作流。 

## 下一步行动 (Next · P0)
- 验证 Storybook 8.6.x 在 `@sydney-rental-hub/ui` 与 `@web-sydney/web` 中均可正常启动并通过 Chromatic。
- 持续梳理文档站与设计 Token 输出，确保 Astro 站与 Storybook 说明一致。 

## 重要约束 (Constraints)
- 设计系统的任何组件/令牌改动必须先在 Storybook 中通过评审，Chromatic 可视化差异通过后才可合并。 
- Turborepo 任务依赖 pnpm workspace 名称，新增包需更新 `turbo.json` 与 `pnpm-workspace.yaml`。 

## 相关命令 (Ops)
- 安装依赖：`pnpm install`
- 启动前端/后端：`pnpm dev`
- 启动 UI Storybook：`pnpm --filter @sydney-rental-hub/ui storybook`
- 启动 Web Storybook：`pnpm --filter @web-sydney/web storybook`
- 构建设计 Tokens：`pnpm build:tokens`
