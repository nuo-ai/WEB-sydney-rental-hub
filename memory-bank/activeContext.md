# 当前上下文与焦点
**最后更新**：2025-10-09

## 已完成状态 (Completed Status)
- **Monorepo 治理**: 已完成基础治理，包括统一 pnpm 工作流、扩展 workspace、标准化 `.env.example` 以及为 Python 栈生成 `requirements.lock`。
- **设计系统奠基**: 已成功搭建设计系统脚手架。
  - **核心包**: 创建了 `@sydney-rental-hub/ui`。
  - **Tokens 自动化**: 引入 `Style Dictionary` 并建立了完整的自动化流程。
  - **组件开发环境**: 成功配置 `Storybook` 并展示了第一个由 Tokens 驱动的 `BaseButton` 组件。
  - **初步集成**: 主应用 `apps/web` 已成功集成 Tokens CSS 文件。
- **设计系统建设 - 第三阶段**: 成功将 `apps/web/src/components/base/` 目录下的所有基础组件 (`BaseBadge`, `BaseChip`, `BaseButton`, `BaseIconButton`, `BaseListItem`, `BaseSearchInput`, `BaseToggle`) 迁移至 `@sydney-rental-hub/ui` 设计系统包。

## 当前焦点 (Current Focus)
- **设计系统建设 - 第三阶段**: 丰富组件库，并逐步将 `apps/web` 中的旧组件替换为设计系统组件。

## 下一步计划 (Next Steps)
1.  **[执行] 修复 Storybook MDX 解析错误**:
    - 修复了 Typography.mdx 文件中设计令牌变量引用错误
    - 解决了 "Could not parse expression with acorn" 问题
    - 确保所有组件文档能正确显示

## 技术提醒
- **开发流程**: 所有新组件或迁移组件都必须在 `@sydney-rental-hub/ui` 的 Storybook 环境中进行开发和验证。
- **代码提交**: 所有与设计系统相关的变更，完成后将由我（Cline）负责提交和推送。
