# 前端 UI × Design Token 目录对照指南

> 目标：厘清“Design Token → UI 组件包 → 应用（apps/web）”之间的目录分工与交付物，便于设计、前端在查阅和落地时不再迷路。

---

## 1. 三层结构速览

| 层级 | 目录 / 文件 | 说明 | 产物 |
| --- | --- | --- | --- |
| **Token 源** | `tokens/base/**/*.json`<br>`tokens/components/**/*.json`<br>`tokens/themes/*.json` | 单一事实来源：基线值、组件语义、主题别名全部以 JSON 维护，供 Style Dictionary 消费。【F:tokens/base/layout.json†L1-L7】【F:tokens/components/card.json†L1-L92】【F:tokens/themes/light.json†L1-L38】 | JSON 输入（不直接发布） |
| **构建脚本** | `scripts/build-tokens.js` | Style Dictionary 管道入口：同时输出 CSS、WXSS、JSON、TS，多端共用；`platforms.css` 会把主题写回 UI 包源码，确保对外发布的是最新变量。【F:scripts/build-tokens.js†L1-L112】 | `packages/ui/src/styles/tokens*.css` 等产物 |
| **UI 组件包** | `packages/ui/src/styles/tokens.css`<br>`packages/ui/src/components/*.vue` | UI 包发布给业务侧：`tokens.css` 是基础层变量，组件内部通过 `var(--component-*)` 等变量消费，无需关心 JSON 细节。【F:packages/ui/src/styles/tokens.css†L1-L112】【F:packages/ui/src/components/BaseButton.vue†L80-L141】 | npm 包：`@sydney-rental-hub/ui` |
| **应用语义层** | `apps/web/src/styles/design-tokens.css`<br>`apps/web/src/styles/page-tokens.css` | Web 端在 UI 包变量之上补充/覆盖本地语义（例如品牌蓝、页面工具类）。默认按“Tier1 原始→Tier2 语义→Tier3 组件”组织，方便和设计稿一一对应。【F:apps/web/src/styles/design-tokens.css†L1-L86】【F:apps/web/src/styles/page-tokens.css†L1-L54】 | 项目自定义 CSS |
| **入口装配** | `apps/web/src/main.js` | 导入顺序：先加载 UI 包的 tokens，再加载本地语义、暗色主题与全局样式，保证变量依赖链正确。【F:apps/web/src/main.js†L10-L18】 | 浏览器最终生效样式 |

---

## 2. 从 Token 到 UI 的生成链路

1. **维护 JSON**：在 `tokens/base` 里更新原始值（如色板、间距），在 `tokens/components` 写组件专属变量，在 `tokens/themes` 调整不同主题的引用关系。【F:tokens/base/layout.json†L1-L7】【F:tokens/components/card.json†L1-L92】【F:tokens/themes/light.json†L1-L38】
2. **运行构建**：执行 `pnpm build:tokens` 会调用 `scripts/build-tokens.js`，Style Dictionary 读取上述 JSON 并输出：
   - `packages/ui/src/styles/tokens.css` / `tokens.dark.css`：供 UI 包与 Storybook 使用；
   - `packages/ui/dist/style-dictionary/json/tokens.json`：Storybook/脚本可消费的嵌套 JSON；
   - `apps/mini-program/src/styles/generated/*.wxss`：小程序端变量；
   - `packages/ui/dist/tokens.mjs`：JS 环境下的 token 常量。【F:scripts/build-tokens.js†L1-L112】
3. **发布 UI 包**：`packages/ui` 打包时会把最新的 `tokens.css` 一并发布，业务侧仅需安装 npm 包即可共享统一变量。【F:packages/ui/src/styles/tokens.css†L1-L112】
4. **应用侧接入**：Web 端通过 `apps/web/src/main.js` 引入 UI 包提供的 `tokens.css`，再叠加 `design-tokens.css` 里定义的语义/页面 token，实现按需覆写。【F:apps/web/src/main.js†L10-L18】【F:apps/web/src/styles/design-tokens.css†L1-L86】

> **建议**：当 JSON 与 CSS 出现不一致时，优先检查构建是否执行、UI 包是否重新发布/安装。

---

## 3. 应用层（apps/web）如何划分职责

- `styles/design-tokens.css`：只存放与业务语义相关的变量（例如 `--brand-primary`、`--filter-chip-bg`），并清晰标注 Tier 层级，便于和设计稿同步。【F:apps/web/src/styles/design-tokens.css†L1-L86】
- `styles/page-tokens.css`：按页面/模块拆分的局部变量，适合放置导航高度、面板宽度等场景化 token（可在组件中通过 `var()` 访问）。【F:apps/web/src/styles/page-tokens.css†L1-L54】
- `style.css` 与 `cursor-globals*.css`：承载遗留全局样式或第三方覆盖，需逐步下沉到 `design-tokens.css` 与组件中，避免散落变量。【F:apps/web/src/style.css†L4-L14】【F:apps/web/src/style.css†L640-L659】
- 组件（`components/base/*.vue` 等）仅通过 CSS 变量消费 token，不直接写死颜色/尺寸；若缺少变量，回到 `design-tokens.css` 或 JSON 新增后再引用。【F:apps/web/src/components/base/README.md†L13-L39】【F:apps/web/src/components/base/README.md†L204-L230】

---

## 4. 常见工作流清单

| 任务 | 推荐步骤 |
| --- | --- |
| 新增全局颜色 / 间距 | 更新 `tokens/base` → 运行 `pnpm build:tokens` → 检查 `packages/ui/src/styles/tokens.css` → 在 `apps/web/src/styles/design-tokens.css` 中声明语义别名 → 在组件中引用。|
| 新增组件专用变量 | 在 `tokens/components/<component>.json` 添加条目 → 构建 → 在 UI 包组件中通过 `var(--component-xxx)` 使用 → 如果需要项目侧覆写，再在 `apps/web/src/styles/page-tokens.css` 中设置作用域变量。|
| 主题适配（暗色） | 更新 `tokens/themes/dark.json` → 构建后检查 `packages/ui/src/styles/tokens.dark.css` → 应用层通过 `[data-theme='dark']` 或 `.dark` 作用域覆写。【F:scripts/build-tokens.js†L64-L83】|
| 快速定位变量来源 | 查看组件使用的 `var(--component-xxx)` → 在 `packages/ui/src/styles/tokens.css` 搜索 → 若为引用型变量，再追溯到 `tokens` JSON。|

---

## 5. FAQ

- **Q：为什么 UI 包和应用里都有 design tokens？**<br>
  **A**：UI 包提供跨项目共享的“基础语义 + 组件变量”，而 `apps/web` 需要进一步落地业务语义（例如租房品牌蓝、页面特定布局），因此需要在本地补充/覆写，但必须遵循 `main.js` 中的引入顺序，避免覆盖失效。【F:apps/web/src/main.js†L10-L18】

- **Q：如何确认变量是否生效？**<br>
  **A**：`apps/web/src/main.js` 默认给 `<html>` 注入 `__globals-debug` 调试类，可在浏览器检查元素时验证变量链路；若无效，检查构建是否跑过、UI 包版本是否更新。【F:apps/web/src/main.js†L16-L21】

- **Q：能否直接修改 `packages/ui/src/styles/tokens.css`？**<br>
  **A**：不推荐。该文件由 Style Dictionary 自动生成，一旦手工修改在下次构建时会被覆盖，应回到 `tokens/*.json` 维护。【F:packages/ui/src/styles/tokens.css†L1-L6】

---

> 如需补充其它端（小程序 / Storybook）链路，请在本指南基础上增补对应目录与脚本，保持“一处入口，多处消费”的原则。
