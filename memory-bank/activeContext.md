# 当前上下文与紧急焦点
最后更新：2025-10-07

## 当前状态
- **服务运行**：前端 :5173 / 后端 :8000 正常；数据库、Directions API 配置完好。
- **阶段目标**：聚焦“小程序 → App → Android”多端战略，小程序为所有设计规范基线；引入 TorUI 组件库，建立统一 Design Token 体系。
- **关键资产**：现有 Polaris Migrator 研究结论、Storybook 初版、保存搜索与筛选系统均已稳定，可作为 Token 统一后的验证场景。

## 当前焦点
1. **讨论 → 计划 → 执行 → 验收 流程固化**：所有任务先讨论方案，再执行，小步交付并等待验收，通过后输出 commit message 与 Memory Bank 更新。
2. **Design Token 先行**：完成颜色/字体/图标/标签/间距的第一轮统一，输出设计说明与代码映射。
3. **TorUI 验证**：在 VS Code 环境下测试 TorUI 主题与 Token 扩展可行性，验证小程序端组件拼装能力。
4. **MVP 功能范围控制**：小程序端优先交付房源筛选、排序、查看详情、收藏、浏览历史、联络客服；暂缓地铁站点、帖子发布和查看、付费通知等增强功能。

## 下一步计划
- **[讨论]** 召开设计/前端对齐会，确认 Design Token 命名与 TorUI 适配策略。
- **[计划]** 编写 Token 落地路线图：原子组件 → 业务组件 → 页面验证，制定 lint/codemod 方案。
- **[执行]** 在实验分支引入 TorUI，搭建小程序 demo，应用首批 Token 并记录差异。
- **[验收]** 与设计/业务复核 Token 映射和页面效果，通过后整理 commit message，并同步更新 Memory Bank。

## 技术提醒
- **筛选系统**：V1 契约稳定，V2 映射默认关闭（enableFilterV2=false），可随时回滚。
- **设计护栏**：Stylelint 已强制 var(--*) 使用，继续禁止硬编码颜色。
- **Memory Bank**：activeContext 仅记录当前与下一步任务快照，完成事项已归档至 progress/systemPatterns。
- **运维约束**：本地需使用 PowerShell 执行 Python/SQL/HTTP，避免跨壳路径问题。
