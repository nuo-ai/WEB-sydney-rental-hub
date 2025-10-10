# 当前上下文与焦点
**最后更新**：2025-10-10

## 已完成状态 (Completed Status)
- **开发环境稳定性修复 (2025-10-10)**: 成功解决了 Storybook 的构建崩溃问题。通过统一 `pnpm overrides` 中的依赖版本、清理并重装 `node_modules`、修复设计令牌中的重复定义和无效引用，项目构建流程已恢复健康和稳定。

## 当前焦点 (Current Focus)
- **项目健康**: 开发环境稳定，Storybook 构建正常。
- **准备就绪**: 等待新的开发任务。

## 技术提醒
- **开发流程**: 所有新组件或迁移组件都必须在 `@sydney-rental-hub/ui` 的 Storybook 环境中进行开发和验证。
- **Storybook 命令**: 所有 `storybook` 命令都应从项目根目录执行，并使用 `-c packages/ui/.storybook` 参数来指定配置文件。
