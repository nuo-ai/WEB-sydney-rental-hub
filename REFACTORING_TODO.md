# JUWO 桔屋找房 · Design Token 合规性重构清单（Living Doc）

目的：以“品牌蓝 + 中性灰”的 Design Token 体系，渐进式、低风险地统一全站样式。  
范围：仅样式层替换，优先不触碰逻辑；小步提交、可回滚。  
前端表现：CTA/链接统一品牌蓝；非 CTA 交互（hover/focus/滚动条等）均为中性灰；页面背景/卡片/分隔线/副文案一致稳定。

---

## 元信息

- 负责人：@yourname
- 起始日期：2025-09-10
- 状态：进行中
- 设计系统基线：
  - 颜色（品牌）：`--juwo-primary | --juwo-primary-light | --juwo-primary-dark`
  - 链接：`--link-color | --link-hover-color`
  - 颜色（结构）：`--color-bg-page | --color-bg-card | --color-text-* | --color-border-*`
  - 交互/可达性：`--focus-ring-*` + `--neutral-scrollbar-*`
  - 筛选域：`src/styles/design-tokens.css`（`--filter-*`）

---

## 审计方法（保留以便复用）

建议以 VSCode 全局搜索 / ripgrep：

- 颜色字面量
  - Hex：`#[0-9a-fA-F]{3,4,6,8}`
  - RGB/A：`rgb\s*\(` / `rgba\s*\(`
  - HSL/A：`hsl\s*\(` / `hsla\s*\(`
  - 命名色：`white|black|red|blue|orange|gray|grey|silver|lightgray|darkgray`
- 旧主题/反模式
  - 橙色：`#FF5824|#ff5824|#f97316|#ffefe9|orange`
  - 非 CTA 用品牌色：`outline|box-shadow` 行内出现 `var(--juwo-primary)`
- 内联样式
  - `style="[^"]*(color|background|border|box-shadow)[^"]*"`
  - `:style="[^"]*(color|background|border|boxShadow)[^"]*"`
- 非语义 var
  - `var\(--(?!juwo|color-|text-|bg-|border-|link-|space-|radius-|shadow-|brand-|filter-).+\)`

命中后记录：文件、片段/行号、字面量、推断语义（text/border/bg/focus/link/cta）、建议 Token、优先级与风险。

---

## 执行原则（Code Review / 开发约束）

- 禁止新增硬编码颜色（Hex/RGBA/HSL/命名色）与非规范 var 名称。必须使用 `src/style.css` / `src/styles/design-tokens.css` 声明的变量。
- 非 CTA 交互（输入/选择/下拉/焦点/滚动条/标签 hover 等）不得使用品牌色；仅 CTA/链接/导航 hover 使用品牌蓝。
- 新增语义先补 :root Token，再在组件中使用 var()。禁止在组件内私自声明“全局语义”变量。
- 童子军军规：每次改动文件时，顺手替换 1–3 处最明显硬编码为 Token，控制范围，小步提交。
- 变量更名/大范围替换需考虑向后兼容：优先以“旧名→新值”的别名过渡。

---

## 优先级说明

- P0：全局/基础组件/影响面大/风险低（首选）
- P1：高频业务组件（列表/详情/筛选）
- P2：低频/边缘模块

风险：低/中/高（视觉微调=低；组件结构性覆盖=中；跨模块影响=高）

---

## 重构待办（Refactoring Backlog）

> 说明：Lines 可留空或填示例范围；每项必须写“前端表现”。

| ID | File | Lines | Offense | Role (语义) | Token 建议 | Scope | Priority | Risk | Status | Notes（含前端表现） |
|---|---|---|---|---|---|---|---|---|---|---|
| P0-001 | src/App.vue | N/A | 全局滚动条/焦点用品牌色 | scrollbar.thumb / focus.ring | `--neutral-scrollbar-*` / `--focus-ring-*` | 全局 | P0 | 低 | done | 前端表现：滚动条/输入焦点改为中性灰，CTA/链接仍为品牌蓝（已完成，见 commit 本地变更） |
| P0-002 | src/App.vue | N/A | a / a:hover 用品牌色字面语义不统一 | link | `--link-color` / `--link-hover-color` | 全局 | P0 | 低 | done | 前端表现：链接颜色统一品牌蓝，hover 深一档（已完成） |
| P0-003 | src/style.css | property-price .price-unit | `#666666` | text.secondary | `--color-text-secondary` | 组件 | P0 | 低 | todo | 前端表现：副价文案改中性灰二级，和全站一致 |
| P0-004 | src/style.css | property-address-primary | `#333333` | text.primary | `--color-text-primary` | 组件 | P0 | 低 | todo | 前端表现：地址主行统一一级文本色 |
| P0-005 | src/style.css | property-features | `#666666` | text.secondary | `--color-text-secondary` | 组件 | P0 | 低 | todo | 前端表现：规格行统一二级文本色 |
| P0-006 | src/style.css | property-footer | `border-top: 1px solid #e5e7eb` | border.default | `--color-border-default` | 组件 | P0 | 低 | todo | 前端表现：分隔线中性灰，和卡片/面板一致 |
| P0-007 | src/style.css | .inspection-text | `#2563eb` | link（强调/链接色） | `--link-color` | 组件 | P0 | 低 | todo | 前端表现：看房时间蓝色与链接一致，hover 可走 `--link-hover-color` |
| P0-008 | src/style.css | .suggestion-item:hover | `#f7f8fa` | bg.hover | `--bg-hover` | 组件 | P0 | 低 | todo | 前端表现：下拉建议 hover 统一浅灰 |
| P1-009 | src/style.css | .location-tag（旧实现块） | `#fafbfc/#f3f4f6` 等 | chip.* | `--chip-*` / filter chip tokens | 组件 | P1 | 中 | todo | 前端表现：标签底/hover 使用 Chip 令牌；与筛选面板一致 |
| P1-010 | src/components/PropertyCard.vue | N/A | scoped 样式若含硬编码 | border/text/bg | 统一改 `--color-*` | 组件 | P1 | 中 | todo | 前端表现：卡片与列表页/详情页视觉一致 |
| P1-011 | src/views/PropertyDetail.vue | N/A | 富文本/分隔线残留 | text/border | `--color-text-*` / `--color-border-*` | 视图 | P1 | 中 | todo | 前端表现：正文/分隔线一致；链接走 `--link-*` |
| P1-012 | src/components/filter-*/** | N/A | hover/focus 残留品牌色 | hover/focus | 用中性令牌或 `--filter-*` | 组件 | P1 | 低 | todo | 前端表现：非 CTA 交互全部中性化 |
| P2-013 | 全局 | N/A | Font Awesome 遗留（图标系统） | icon | 迁移至 lucide-vue-next | 全局 | P2 | 中 | todo | 前端表现：图标风格统一（非本轮重点） |

> 备注：style.css 中包含通用样式（非纯 Token 文件），因此可纳入替换范围；但一次仅提交小块（2–5 处），控制风险。

---

## 每周小冲刺（Focused Sprints）建议

- Week N：PropertyCard 合规（P0-003/004/005/006/007）
- Week N+1：PropertyDetail 文本/分隔线/链接统一（P1-011）
- Week N+2：筛选面板 hover/focus 全面中性化核对（P1-012）
- 持续：童子军军规：每次 PR 至少完成 1–2 条 backlog 项（小范围）

---

## 变更记录（Changelog）

- 2025-09-10
  - 初始化文档与方法论。
  - 已完成：App.vue 中“滚动条/全局焦点/输入 hover/链接”语义化（see local changes）。  
    前端表现：滚动条/输入焦点统一中性灰；链接仍为品牌蓝，hover 更深。

---

## 附：Token 角色速查表（常用）

- 文本：`--color-text-primary|secondary|tertiary`
- 边框：`--color-border-default|strong`
- 背景：`--color-bg-page|card`，hover：`--bg-hover`
- CTA：`--juwo-primary | --juwo-primary-light | --juwo-primary-dark`
- 链接：`--link-color | --link-hover-color`
- 焦点/滚动：`--focus-ring-*` / `--neutral-scrollbar-*`
- Chip/筛选：`--chip-*` / `--filter-*`
