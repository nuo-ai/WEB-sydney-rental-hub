# 当前上下文与焦点
**最后更新**：2025-10-11

## 当前焦点 (Current Focus)
- **逆向工程原子组件样式**: 根据 `docs/task-list.md` 清单，系统性地分析 `realestate.com.au` 网站，抓取原子组件的 CSS 属性，为设计系统提供数据基础。

## 刚完成的工作 (Latest)
- **清单纠正与数据迁移**:
  - 发现并废弃了不完整的旧版 `component-analysis-checklist.md`。
  - 成功将用户提供的、完整的清单模板更新为新的工作基准。
  - 将所有之前已测量的精确数据 (`Button`, `Input`, `Checkbox`, `Divider`) 成功填充到新清单的正确结构中。
  - 纠正了关于 `Input` `focus` 状态的错误推断，确保了数据的准确性。

## 下一步行动 (Next · P0)
- **继续数据抓取**: 按照新的、完整的清单，继续系统性地分析 `realestate.com.au` 上的组件。
- **下一个目标**: 分析 `Switch / Toggle` (开关) 组件的样式。

## 重要约束 (Constraints)
- 本阶段以 Astro 为设计系统验证环境；Storybook 暂不启用，避免多环境复杂度
- 小程序不支持运行时 setProperty，统一采用静态构建；H5 端支持 --srh-* 运行时调参

## 相关命令 (Ops)
- 构建 Tokens：pnpm run build:tokens
- 启动 Astro 工具站：pnpm --filter @srh/design-site-astro dev（端口占用自动切换）
- 访问：/、/tokens、/components（按钮“切换暗色”验证主题）
