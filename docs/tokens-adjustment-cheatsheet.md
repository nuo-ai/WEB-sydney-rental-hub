# 常见诉求 → 改哪个 Token（速查表）

使用说明
- 原则：优先改“语义/组件层”Tokens，尽量不动组件代码。
- 生效路径：
  - Web：保存后通常即刻/热更新可见（若走构建管线，则 `pnpm build:tokens` 后在页面验证）。
  - 小程序：同改 Tokens 源，重新构建生成 WXSS 后生效（需发版）。
- 命名说明：文中形如 `color.brand.primary` 为 Token 逻辑名；对应 CSS 变量可能是 `--color-brand-primary`（具体以 packages/ui/src/styles/tokens*.css 为准）。

一、颜色相关
- “主色偏淡/偏深” → 调 `color.action.primary`（以及 hover/active 阶梯：`color.brand.hover` / `color.brand.active`）
- “文字层级不够明显” → 调 `text.primary/secondary/weak`（语义文字对比度）
- “禁用态太浅/太深” → 调 `text.disabled`、`background.disabled`（必要时加 `opacity.disabled`）
- “边框不够显眼” → 调 `border-interactive`（必要时增加 hover/focus 深一阶）
- “深色模式对比度不足” → 在 dark 作用域覆盖同名语义 Token（仅语义层，勿直接改原始色值）

二、尺寸与圆角
- “整体更圆润/更硬朗” → 调 `radius.*`（如 `radius.sm/md/lg`，全站统一）
- “按钮太瘦/太胖” → 调 组件层 `component.button.height/padding`（若缺失，先用 `space.*` 组合；提出组件层令牌增量草案）
- “输入框边框太细/太粗” → 调 `component.input.border.width`（若缺失，先在语义层补 `border.width.field`）

三、间距节奏
- “列表/卡片挤/松” → 调 `space.*`（如 `space.4/6/8`），组件内用空间令牌拼装，不写死 px
- “文字行距不舒服” → 调 `line-height.*`（如 `line-height.body/ui/title`），配合 `text.*` 层级

四、阴影与层级
- “浮层不够立体/太浓” → 调 `shadow.*`（如 `shadow.sm/md/lg`）
- “弹窗遮罩太亮/太暗” → 调 `overlay.alpha`（若无，先用阴影/rgba 表达，并提出 `overlay.*` 令牌增量）

五、交互反馈
- “hover 没反馈/反馈过猛” → 调 `background.hover` / `border-interactive` 的 hover 深度（或为组件专属补 `component.*.hover.*`）
- “active 压下感不够” → 调 `color.brand.active` 或 `shadow.press`（若无，新增 `shadow.active` 增量建议）
- “focus 不明显” → 调 `focus.ring.color/width/offset`（若无，建议增加 `focus.ring.*` 语义令牌）

六、组件专项（优先通过组件层令牌解决）
- Button（按钮）
  - 主色/文字：`color.action.primary` / `text.on.action`
  - 尺寸/圆角：`component.button.height/padding/radius`（缺失则用 `radius.*` + `space.*`）
  - 阴影/按压：`component.button.shadow` / `shadow.active`
- Input / SearchInput（输入/搜索）
  - 边框/背景/占位符：`border-interactive` / `background.surface` / `text.placeholder`
  - focus 阴影：`shadow.focus`
- Toggle / Switch（开关）
  - 选中色：`component.toggle.on.bg`（若无，临时用 `color.action.primary`）
  - 轨道/拇指：`component.toggle.track/bg/thumb`
- DateRangePicker（日期范围，库组件外包“壳”）
  - 高亮/选中段：`component.calendar.range/bg`、`component.calendar.selected/bg`
  - 文本层级/分隔线：`text.secondary` / `border.*`
  - 浮层阴影：`shadow.lg`
- Select / Autocomplete（下拉/联想，库组件外包“壳”）
  - 菜单项 hover/active：`component.menu.item.hover/bg`、`component.menu.item.active/bg`
  - 多选 Chip：`component.chip.bg/border/text`
- Dialog / Drawer（弹窗/抽屉，库组件外包“壳”）
  - 背景/阴影/遮罩：`background.surface` / `shadow.lg` / `overlay.alpha`
  - 标题字号/权重：`text.title` + `font-weight.semibold/bold`
- Tabs / Segmented（页签/分段）
  - 激活态：`component.tabs.active.*` / `component.segmented.active.*`
  - 分隔线：`border.*`
- Checkbox（复选）
  - 勾选/边框色：`action.on.checkbox` / `border-interactive`

七、遇到缺口怎么做
- 先用“语义层”近似替代，确保不阻塞交付（例如用 `color.action.primary` 暂代 `component.toggle.on.bg`）。
- 同时在 docs/ 中开“令牌增量草案”，建议命名、用途、示例组件，待批准后再补入 Tokens 源（避免直接硬编码）。

八、排错与核对
- 看不出变化 → 检查是否改在“语义/组件层”，是否被组件内硬编码覆盖；或是否在 dark 作用域未同步覆盖。
- 不同端不一致 → 检查小程序 WXSS 是否已重构建；检查 uni.scss 桥接是否覆盖到了对应变量。
- 依赖层级冲突 → 用 Stylelint/ESLint 约束“禁止硬编码”，保证组件只消费 Tokens。

小结
- 先用“基线”跑通业务，再通过 Tokens 做细腻抛光；Web 分钟级见效，小程序经构建发版同步。
- 任何找不到对口的诉求，优先用“语义层近似 + 增量令牌草案”的方式解决，避免硬编码和一次性写死。
