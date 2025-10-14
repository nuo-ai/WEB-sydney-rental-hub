# 当前上下文与焦点
最后更新：2025-10-14

## 当前焦点（P0）
- apps/web 主题层重构：Tailwind v4 + 核心 HSL 变量 + Element Plus 桥接，确保“Tailwind + EP”统一视觉与可访问性（A11y）。
- 变量收敛：将遗留自定义变量统一映射到核心/语义变量，优先覆盖 PropertyCard.vue、PropertyDetail.vue。
- 暗色模式：同时支持 .dark 与 [data-theme="dark"]，两者视觉一致。

## 刚完成
- 引入 Tailwind v4（@tailwindcss/postcss；preflight=false），新增 theme.css（~10–15 个核心 HSL 变量）与 el-theme-bridge.css（映射 --el-color-*、--el-bg-color、--el-text-color-*、--el-border-* 等）。
- tailwind.config.js：darkMode ['class','[data-theme="dark"]']；colors/font/radius/spacing 映射到变量；禁用 preflight。
- main.js 全局引入 theme.css / el-theme-bridge.css / tailwind.css。
- 路由与演示：/globals-demo、/cards-demo；PropertyCard/PropertyDetail 改为消费核心变量并加入 focus-visible ring（--ring）。
- 细节修复：从 /cards-demo 跳详情 404 → 通过在 CardsDemo 预注入 store.currentProperty + 详情页 onMounted fetch guard 解决。
- DevServer：vite --port 5199 --strictPort，避免端口冲突。

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
