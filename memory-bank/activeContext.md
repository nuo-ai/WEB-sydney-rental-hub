# 当前上下文与焦点
最后更新：2025-10-14（根据当前代码同步修订）

## 当前焦点（P0）
- 主题链路核实：apps/web 现已同时加载 `theme.css`、`design-tokens.css` 与 Element Plus 桥接层，确保 Tailwind v4、业务样式与组件库共用同一套 HSL 变量。
- 变量收敛：梳理 PropertyCard.vue、PropertyDetail.vue 等历史样式，替换掉仍直接引用 `--color-*` 或硬编码的遗留值。
- 品牌一致性：`tokens/themes/light.json` 仍输出桔色 `#F28C00`，而前端主题已切换为蓝色；需要在 tokens 层更新 brand.*，重新构建并回填 UI 包产物。

## 刚完成
- 引入 Tailwind v4（@tailwindcss/postcss；preflight=false），新增 `theme.css`（核心 HSL 变量）与 `el-theme-bridge.css`（映射 `--el-color-*`、`--el-bg-color`、`--el-text-color-*`、`--el-border-*` 等）。
- `tailwind.config.js`：`darkMode` 同时支持 `class` 与 `[data-theme="dark"]`，扩展颜色/字体/圆角/间距并禁用 preflight；`tailwind.css` 作为唯一入口。
- `main.js` 全局引入 UI 包 tokens、`design-tokens.css`、`theme.css`、Element Plus 桥接与 Tailwind，维持 cursor 调试链路。
- 路由与演示：`/globals-demo`、`/cards-demo` 对齐主题变量；PropertyCard/PropertyDetail 聚焦 `focus-visible` 与 `--ring` 联动。
- 细节修复：从 `/cards-demo` 跳详情 404 → 通过在 CardsDemo 预注入 `store.currentProperty` + 详情页 `onMounted` fetch guard 解决。
- DevServer：`vite` 默认跑在 **5174** 且 `strictPort: true`，与当前 `package.json`、`vite.config.js` 设置一致。

## 下一步
- P0：变量收敛（卡片/详情命中项替换）。必要时在 theme.css 添加“临时别名区”兜底，完成后删除。
- P1：密度统一（间距/字号采用 Tailwind 量表），按段落小步提交并双端验证。
- P2（可选）：shadcn-vue 试点（Button/Input/Dialog）A/B 对比 EP；EP 继续承担复杂组件（表格/日期/树/上传）。

## 重要约束
- 业务/组件仅消费语义层或组件层 Token，禁止硬编码与直接使用原始层；EP 优先通过 bridge 继承统一风格，减少逐组件覆写。
- 视觉改动走小补丁、可回滚；关键变更需经 Storybook/Chromatic 校验；暗色/焦点环对比度满足 WCAG AA。

## 常用命令
- 构建设计 Tokens：pnpm build:tokens
- 启动 UI Storybook：pnpm --filter @sydney-rental-hub/ui storybook
- 启动 Web：pnpm --filter @web-sydney/web dev
