# 系统设计模式与最佳实践

---

## 设计系统与主题

- **双色主题**: Style Dictionary 输出 `:root` 与 `[data-theme='dark']` 两套变量，组件通过语义层 Token 自动适配主题。 
- **令牌分层**: 坚持“原始 → 语义 → 组件”三级结构；业务代码只允许消费语义层或组件层。 
- **Storybook 为事实来源**: 设计规范与组件使用说明全部记录在 Storybook 8.6.x 内的 MDX 与 stories 中。任何组件改动必须同时更新 Storybook。
- **Astro 站角色**: 设计 Token 工具站用于预览与调参，不承载组件开发职责。

---

## Monorepo 原则

- 使用 `pnpm` + `Turborepo` 统筹所有应用与包。新增项目需在 `pnpm-workspace.yaml` 中登记，并在 `turbo.json` 中定义缓存/依赖关系。 
- 根 `package.json` 提供统一脚本；请优先通过 `pnpm <script>` 而非直接调用子包二进制，以便复用 Turbo 缓存。 
- 共享代码应沉淀到 `packages/*`，业务应用避免彼此直接引用源文件。

---

## 组件开发模式

- **提取流程**: 在业务应用中发现的基础 UI 优先抽离到 `packages/ui`，补充 Storybook stories 与单元测试，再通过工作区引用。 
- **样式约束**: 
  - 禁止硬编码颜色/间距/字号等数值；必须使用 Design Token。 
  - CSS 自定义属性不得提供 `var(--token, #fff)` 形式的兜底值，以防止绕过暗色主题。 
- **可访问性**: 使用 `@storybook/addon-a11y` 校验组件无障碍问题，并在业务代码中继承同样的语义标签/ARIA 属性。

---

## 数据与服务模式

- **前端数据流**: Vue + Pinia 作为单一数据源；组件只通过 action 修改状态，禁止直接写入 store state。 
- **API 契约**: 后端 FastAPI 提供 REST 接口，响应结构统一 `{ status, data, error, pagination }`。前端通过 axios 拦截器处理错误与鉴权。 
- **缓存策略**: Redis/内存缓存 15 分钟过期，用于加速热门筛选；前端在必要时进行请求去抖。 

---

## 测试与质量

- **单元测试**: Vitest 3.x 运行在各包的 `test` 目标中；组件测试应覆盖主要交互状态。 
- **端到端**: Playwright 用于 URL 幂等和关键用户路径验证，可通过 `pnpm --filter @web-sydney/web exec npx playwright test` 运行。 
- **视觉基线**: Chromatic 连接 Storybook 构建，任何视觉差异需在 PR 中审核并手动批准。 
- **Lint 约束**: ESLint + Stylelint 强制校验代码与样式规范，CI 中会阻断不合规提交。

---

## 运行时守则

- Turborepo 的缓存依赖 Git 状态，提交前务必 `pnpm lint && pnpm test` 确保缓存未产生陈旧产物。 
- Storybook 8.6.x 依赖与 Vite 插件版本耦合度高，升级时先在 `apps/web` 与 `packages/ui` 分支验证兼容性，再合并到主分支。
- 删除或新增 Token 后必须运行 `pnpm build:tokens` 并同步更新 Storybook/文档站截图，避免不同端出现视觉漂移。
