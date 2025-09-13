# Design Foundations（一页式基础规则表）

目的

- 提供“唯一真源”的基础设计规则，确保新组件/新页面的前端表现统一、可回滚、可审查。
- 所有变量均使用 CSS 自定义属性（tokens），禁止硬编码色值/散点尺寸。
- 变更策略：先“声明新令牌”再“渐进替换”，不破坏现有视觉与行为。

文件总览（源码位置）

- 全局令牌与规则：`vue-frontend/src/style.css`
- 页面级令牌：`vue-frontend/src/styles/page-tokens.css`
- 文字系统：`vue-frontend/src/styles/typography.css`
- 颜色映射参考：`docs/color-token-mapping.md`
- 系统模式与约束：`memory-bank/systemPatterns.md`

通用守护（必须遵守）

- stylelint 已启用：运行代码禁止 `#hex/rgb/命名色`，必须使用 `var(--*)`
- 禁止 `var(--token, #hex)` 兜底（仅 tokens 定义入口可例外）
- 图标统一使用 `lucide-vue-next` + `currentColor`，严禁 `<i>`/位图

---

## 1. 颜色 Color（已建立）

根令牌（摘录）

- 文本：`--color-text-primary` / `--color-text-secondary`
- 背景：`--color-bg-page` / `--color-bg-card` / `--surface-2/3/4`
- 边框：`--color-border-default` / `--color-border-strong`
- 品牌：`--juwo-primary`（蓝）`--link-color`（链接）及 brand 系列
- 状态（补充）：`--semantic-danger/*` `--semantic-warning/*` `--semantic-success` `--semantic-favorite/*`

前端表现

- 页面灰、卡片白、中性灰分隔；品牌蓝仅用于 CTA/链接/少量强调；其它交互态全部走中性灰阶。

---

## 2. 字体与文字 Typography（已建立）

来源

- `styles/typography.css` 与 `.typo-*` 工具类；字号工具 `.text-xs/sm/base/lg` 对应 tokens。

要点

- 列表页 H1=22/26 与价格主数字对齐，段落/辅助文案与详情页一致。
- 中文化与 i18n：缺失 key 使用中文回退，禁止直出 key。

---

## 3. 间距 Spacing（已建立）

令牌

- 页面节奏：`--page-section-gap` / `--page-section-gap-lg`
- 基础：`--space-*`
- 规格行（spec）：`--spec-icon-size/text-size/line-height/icon-gap/item-gap`

前端表现

- 列表/详情“图标 + 数字”行尺寸与横向间距完全一致（容器内就近覆写 18/14/18/6/12）。

---

## 4. 圆角 Radius（刻度对外声明）

已有（全局）

- `--radius-sm` / `--radius-md` / `--radius-lg` / `--radius-xl` / `--radius-full`

建议（使用范式）

- 卡片/输入/按钮优先用 sm/md；连体（segmented）控件仅端部圆角（2px）。
- 禁止在组件内自创奇数值；统一来源 tokens。

---

## 5. 阴影 Shadow（刻度对外声明）

已有（全局）

- `--shadow-sm/md/lg/xl`（统一透明度/扩散）

使用建议

- 默认优先“边框 + 中性底”，必要时用 xs/sm/md，避免过度浮层。

---

## 6. 边框 Border（刻度补充）

新增刻度（声明，不影响现有）

- `--border-width-1: 1px`
- `--border-width-2: 2px`

使用建议

- 分隔/细线统一 1px；“强分隔/聚焦”使用 strong 颜色或 2px 加粗，不混用色值。

---

## 7. 层级 Z-index（刻度补充）

新增刻度（声明，不影响现有）

- `--z-search: 50`
- `--z-nav: 60`
- `--z-dropdown: 70`
- `--z-modal: 100`
- `--z-toast: 110`

使用建议

- 浮层不再与导航/下拉抢层级；组件内统一引用上述令牌。

---

## 8. 图标 Icon（刻度补充）

新增刻度（声明，不影响现有）

- `--icon-16` / `--icon-18` / `--icon-20` / `--icon-24`

使用建议

- BaseIconButton 默认 18px；导航/菜单 16px；统一比例不“忽大忽小”。

---

## 9. 焦点 Focus（已建立）

令牌

- `--focus-ring-color` / `--focus-ring-width` / `--focus-ring-offset`

策略

- 输入类控件显示中性灰 ring；导航链接/标题动作/卡片图标按钮默认去 ring（可用 `.focus-visible-ring` 强制启用）。

---

## 10. 断点与容器（已建立）

断点

- 768（平板）/ 1200（桌面）/ 1920（超宽）
- 容器 `max-width: 1200px`；左右 padding：Mobile 16 / Desktop 32

---

## 11. 表单尺寸 Scale（刻度补充）

建议（宣贯，不破坏现有）

- sm：高度 32px / 字号 13px
- md：高度 36-40px / 字号 14-16px（iOS 防缩放 ≥16px）
- 筛选场景：pc 40px / mob 44px（已有 `--filter-field-*`）

---

## 12. Skeleton（建议）

- 统一骨架色与闪动动效；后续新增 `BaseSkeleton` 原子以替换散点实现。

---

## 13. 点击命中区 Hit Area（已建立）

- BaseIconButton / BaseToggle：36–40px；移动端优先 40px

---

## 14. 输入后缀对齐（已建立）

- 规则：相对 `.el-input__wrapper` 定位，tokens `--search-suffix-right` / `--search-suffix-hit`
- 避免以 `.el-input__suffix` 为锚点

---

## 15. 导航交互（已建立）

- hover：文字变品牌色，不加粗，不灰底
- focus：移除默认外框，仅导航链接作用域生效

---

## 16. 对齐 Alignment（已建立）

来源与令牌

- 页面级（page-tokens.css）
  - 左右留白：`--page-x-padding-mob: 16px`、`--page-x-padding-desktop: 32px`
  - 容器与区块：`--page-section-gap`、`--page-section-gap-lg`
  - 导航：`--nav-px-mob`、`--nav-px-desk`（与导航容器左右内边距一致）
  - 卡片内容宽度（单列对齐场景）：`--card-content-w: 580px`
  - 其它：`--header-height`、`--bottom-nav-height`、`--scrollbar-w`
- 全局（style.css）
  - 容器最大宽度：`max-width: 1200px`（所有页面主容器）
  - H1/工具条与卡片对齐示例：`.title-block .actions-row { width: var(--card-content-w); }`

对齐规则（约定）

- 容器
  - PC 主容器 `max-width: 1200px` 居中；Mobile/Pad 左右内边距：16px；Desktop 左右内边距：32px（取自 page tokens）
- 内容对齐
  - 单列卡片页面（如房源列表）：标题区的工具条/actions 与卡片内容宽度一致（用 `--card-content-w`）
  - 左/右缘以“内容卡片”为锚：避免多处硬编码 453/496 类数值，统一以令牌/计算表达
- 导航与搜索
  - 导航左右 padding 使用 `--nav-px-*`；搜索容器内与页面容器保持一致，对齐到 16/32
- 断点策略
  - 断点：768/1200/1920（参考）；在断点内仅做小范围覆盖，避免“大改”导致体系分裂

用法示例

```css
/* 标题区操作行与卡片内容宽度对齐（PC） */
@media (width >= 1024px) {
  .title-block .actions-row {
    width: var(--card-content-w);
  }
}

/* 页面根容器左右留白（样板 .page 已内置） */
.page {
  padding-left: var(--page-x-padding-mob);
  padding-right: var(--page-x-padding-mob);
}
@media (min-width: 768px) {
  .page {
    padding-left: var(--page-x-padding-desktop);
    padding-right: var(--page-x-padding-desktop);
  }
}
```

前端表现

- 所有新页面/组件默认获得统一左右留白与区块节奏；列表页标题区/工具条与卡片内容区左缘严格对齐；导航与搜索区与页面水平节奏一致。

---

## 执行与审查

落地检查清单（PR Review 必看）

- [ ] 新/改样式是否全部使用 `var(--*)`
- [ ] 是否复用 base 原子组件（BaseButton/BaseIconButton/BaseToggle/BaseChip/…）
- [ ] 是否引用页面级令牌（左右 16/32、节奏/动效）
- [ ] 图标是否使用 lucide + currentColor
- [ ] 断点/容器是否遵循 768/1200/1920 与 `max-width:1200`

渐进替换优先级

- P0：导航/卡片/按钮的散点尺寸 → 令牌化
- P1：排序按钮 → BaseDropdownButton；照片计数/“New” → BasePillBadge；分隔线 → BaseDivider
- P2：面包屑 → BaseBreadcrumb；规格 segmented → BaseSegmented；骨架 → BaseSkeleton

变更策略（安全回滚）

- 仅“声明新令牌”，不直接替换现有引用；待审查通过后分模块替换。
- 任何替换支持“删除或改回 token 引用”即可回滚；不影响逻辑与数据流。

附录：当前令牌入口

- `src/style.css`：根 tokens、系统护栏、全局工具类
- `src/styles/page-tokens.css`：页面级令牌（左右留白/区块节奏/动效）
- `src/styles/typography.css`：文字系统与 .typo-* 工具类
