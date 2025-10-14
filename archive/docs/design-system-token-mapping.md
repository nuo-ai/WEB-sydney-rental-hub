# 设计令牌 × 组件映射指南

> 目标：一页掌握「设计令牌如何生成、被哪些组件消费、Storybook 如何验证」。  
> 最近更新：2025-10-10

---

## 1. 体系总览

| 阶段 | 说明 | 产出 / 文件 | 下游使用者 |
| --- | --- | --- | --- |
| 设计令牌源 | JSON 定义在 `tokens/`（base / semantic / components） | `tokens/**.json` | Style Dictionary |
| 自动化构建 | `pnpm build:tokens` & `tools/style-dictionary` 管道 | `packages/ui/dist/tokens.css`、`packages/ui/dist/style-dictionary/css/variables.css`、`apps/mini-program/src/styles/generated/*.wxss` | 主站、设计系统、Storybook、小程序 |
| 设计系统消费 | 组件封装在 `packages/ui/src/components` | 各组件 scoped 样式、stories | 主站 `apps/web`、Storybook |
| 前端引入 | 主站 `main.js`、Storybook `preview.js`、小程序 `app.vue` | `import '@sydney-rental-hub/ui/dist/tokens.css'` 等 | 浏览器 / 微信小程序 |

流程：  
`tokens/*.json` → `pnpm build:tokens` → `dist/tokens.css` →  
- `apps/web/src/main.js`  
- `packages/ui/.storybook/preview.js`  
- `apps/mini-program/src/styles/generated/*.wxss`

---

## 2. 令牌消费映射表

### 2.1 基础色彩（Color）

| Token | 值 | 被消费的组件 / Story | 备注 |
| --- | --- | --- | --- |
| `--color-brand-primary` | #0057ff | BaseButton (primary)、BaseBadge、BaseCard、PropertyCard 收藏图标 | Storybook: `Design System/Colors`, `BaseButton` |
| `--color-brand-hover` | #0047e5 | BaseButton hover、FilterWizard CTA | Storybook: `BaseButton` |
| `--color-brand-active` | #0036b3 | BaseButton active、全局 CTA | |
| `--color-gray-800` / `--color-gray-500` | 灰阶 | BaseCard 文案、BaseListItem、副标题、FilterWizard | `Design System/Typography`、`BaseCard` |
| `--color-semantic-feedback-*` | success/warning/error/info | BaseBadge 状态、BaseNotification（计划中）、表单校验 | Storybook: `BaseBadge`、`BaseInput` |

> 待消费：`--color-favorite-icon`、其它品牌别名。建议在新组件接入时按表补充。

### 2.2 排版（Typography）

| Token | 值 | 使用位置 | Story |
| --- | --- | --- | --- |
| `--font-family-base` | Inter, sans-serif | 所有基础文本 | `Design System/Typography` |
| `--font-size-md` | 14px | BaseButton、BaseInput、BaseCard 主文案 | |
| `--font-size-lg` / `--font-size-xl` | 16px / 18px | PropertyCard 价格、标题 | |
| `--font-line-height-md` | 1.5 | BaseCard 段落、表单输入 | |

> Storybook 的 `Typography.mdx` 用 `@sydney-rental-hub/ui/tokens` 直读 TypeScript tokens。

### 2.3 间距 & 圆角（Spacing & Radius）

| Token | 值 | 消费组件 | Story |
| --- | --- | --- | --- |
| `--space-md (12px)` | 按钮 padding、卡片内边距、List item 间距 | BaseButton、BaseCard、BaseListItem | `BaseButton`、`BaseCard` |
| `--space-lg (16px)` | Card 外距、布局容器 | PropertyCard、FilterWizard | |
| `--radius-sm (6px)` | 按钮、输入框 | BaseButton、BaseInput | |
| `--radius-md (8px)` | 卡片、列表项 | BaseCard、PropertyCard | |

> 若新增组件用到未定义的间距/圆角，请优先新增 token，再使用。

### 2.4 阴影 & 组件层级（Shadow & Component Tokens）

| Token | 值 | 消费组件 | Story |
| --- | --- | --- | --- |
| `--shadow-sm` | 0 1px 2px ... | BaseCard 默认阴影、PropertyCard hover 前 | `BaseCard` |
| `--shadow-md` | 0 4px 6px ... | PropertyCard hover、BaseChip 下拉 | |

### 2.5 组件专用令牌

| 组件 | 关键 token | Story |
| --- | --- | --- |
| BaseButton | `--component-button-primary-*`、`--component-button-secondary-*` | `BaseButton` |
| BaseInput / BaseSearchInput | `--component-input-*` | `BaseInput`, `BaseSearchInput` |
| BaseCard | `--component-card-*` | `BaseCard` |
| BaseChip | `--chip-bg`、`--chip-bg-hover` (语义 token) | `BaseChip` |
| BaseToggle | 品牌色 + radius token | `BaseToggle` |
| PropertyCard | 组合使用 color/spacing/typography + Card token | `BaseCard`, `PropertyCard` Story (计划) |

> **空缺**：尚未有组件消费 `--component-select-*`（投入计划：FilterPanel Select 模块）。  
> 建议将 `FilterWizard`、`SaveSearchModal`（现位于应用层）逐步迁移至设计系统，以减少 scoped 重复样式。

---

## 3. Storybook 验证指引

1. **全局引入**  
   - `.storybook/preview.js` 已加载 `../dist/tokens.css` + `../dist/style-dictionary/css/variables.css`。  
   - Light / Dark 主题通过 decorators 包裹 `<div class="{theme}-theme">` 验证多主题变量。

2. **Stories 对应关系**  
   - `Design System/Colors`（计划增加）：对照 tokens 展示色板 ↔ JSON 值。  
   - `Design System/Typography`：已完成字体、字号、行高示例。  
   - `BaseButton` / `BaseCard` / `BaseInput` …：验证组件是否使用 token，而非硬编码。  
   - `Future`: PropertyCard Story → 结合 tokens 演示真实业务组件。

3. **开发流程 Checklist**  
   1. 新需求 → 在 `tokens/**/*.json` 中新增/调整 token。  
   2. 运行 `pnpm build:tokens` 同步所有目标产物。  
   3. 在组件中通过 `var(--token-name)` 使用。  
   4. 补充/更新 Storybook stories，观察 Light/Dark 表现。  
   5. 若 Storybook 中出现原始颜色/尺寸，说明 token 未定义或未引入 → 更新表格并回补。  
   6. 提交 PR 时附上 Storybook 截图或 Chromatic 变更。

---

## 4. 后续规划

- **补充 Stories**：为 Color、Spacing、Shadow 等基础 token 增加演示页面。  
- **迁移业务组件**：将 `FilterWizard` 等继续迁移到 `packages/ui`，更新映射表。  
- **自动检测**：结合 Stylelint/ESLint 规则，检测非 token 样式值，保持体系一致。

如需扩展或发现 token 与组件不匹配，请更新本文档对应表格，并同步 Storybook 以便团队共享。 🍊
