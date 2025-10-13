# Token 冲突盘点与重命名建议（草案）

目标
- 建立“唯一命名体系 + 语义优先”的令牌规范，避免重复/歧义，降低暗→亮主题切换与跨端同步成本。
- 本稿仅为文档建议，不改任何源码；待你确认后再制定实施批次与回滚策略。

一、现状与来源
- 运行时（Web 真源）：packages/ui/src/styles/tokens.css（浅色）、tokens.dark.css（深色）
- 源数据（供批量治理/对照）：tokens/base/**、tokens/themes/{light,dark}.json、tokens/components/**、tokens/component-mapping.json

二、主要问题（分类盘点）
1) 命名重复/并行体系并存（高优先级）
- 同一语义存在多套命名：
  - 背景：--color-semantic-bg-page vs --color-background-page vs themes.color.semantic.bg.page / themes.color.background.page
  - 文字：--color-text-primary vs --color-semantic-text-primary vs themes.color.text.primary
- 影响：使用者不知选哪套；组件间易不一致；暗/亮切换时需要多处覆盖。

2) 行动色 vs 品牌色 混用（高优先级）
- 现状：同时存在“品牌色”与“行动色”，但组件使用不统一：
  - 例如列表选中、若干 focus/hover 用了 color.brand.primary，而 CTA 又用 color.action.primary。
- 风险：品牌色（橙）与行动色（蓝）语义不同，若混用会造成视觉与行为不一致。

3) 禁用/错误态在暗色主题下引用浅色中性色（高优先级）
- 例：tokens.dark.css 中多处 disabled 使用 --color-gray-200/50 等浅色中性；在深色背景显得突兀，且对比度可能异常。
- 建议统一引用 background.disabled / text.disabled（需要补充 text.disabled 语义）。

4) 组件层变量“冗余别名”较多（中优先级）
- 如：--component-button-primary-bg + --component-button-primary-background-color（后者仅转发前者）。
- 建议：保留一份“组件层主变量”，其余作为过渡别名并标注弃用计划。

5) 缺少焦点环/交互反馈语义（中优先级）
- 多处 focus-outline 直接绑定品牌色或行动色，缺少统一的 focus.ring.* 令牌。
- 建议新增：focus.ring.color / focus.ring.width / focus.ring.offset（light/dark 均有）。

6) 语义层定义不成对（中优先级）
- light/dark 主题对于 text.* / background.* / border.* / shadow.* 等应“成对存在”，当前有的语义在某主题缺失或未统一引用。

三、建议的“唯一命名体系”（目标态）
- 以 themes/{light,dark}.json 的“语义层”为唯一入口（推荐保留以下家族）：
  - background.{page,surface,hover,disabled}
  - text.{primary,secondary,muted,disabled,inverse}
  - border.{default,subtle}
  - color.brand.{primary,hover,active}（仅身份/品牌）
  - color.action.{primary,hover,active}（仅交互/CTA/选中/焦点）
  - focus.ring.{color,width,offset}
  - shadow.{sm,md,lg}
  - radius.{sm,md,lg,full}
  - space.{xs,sm,md,lg,xl,xxl,3xl}
- 组件层令牌：component.{button,input,select,textarea,chip,card,tabs,segmented,toggle,list-item,search-input}.*
  - 组件层只“转发”语义层，不直接使用原始值；不足的再按组件层新增。

四、具体重命名/映射建议（第一批）
- 统一 “background / text / border” 家族（用 themes 命名为准），保留旧名“临时别名”但标注弃用：
  - color-semantic-bg-page → background.page
  - color-background-page → background.page（建议保留该变量作为别名，过渡期内继续导出）
  - color-semantic-bg-primary → background.surface
  - color-semantic-bg-secondary → background.hover（或 background.surface-alt，如需要新增）
  - color-semantic-text-primary / color-text-primary → text.primary
  - color-semantic-text-secondary / color-text-secondary → text.secondary
  - color-semantic-text-muted → text.muted
  - color-semantic-border-default → border.default
  - color-semantic-border-subtle → border.subtle

- 禁用/状态类（确保暗/亮对等）
  - 所有 disabled 背景统一引用：background.disabled（dark: #3a3b3c，light: #EDEEF0）
  - 新增 text.disabled（dark: 建议 #8A8C90 左右；light: 建议 #9CA3AF 左右）；替换现有灰度直指。
  - 错误/成功/信息：保留 feedback.{error,success,warning,info}，组件层优先引用 feedback.*，避免直用具体色。

- 行动/品牌边界（规范化）
  - 规则：
    - color.action.* 用于 CTA、选中态、可交互元素的 hover/active/focus（按钮、开关、链接、选中项、焦点环…）。
    - color.brand.* 用于身份/徽章/品牌化容器（如 Logo、品牌 Banner、品牌强调背景，不涉交互逻辑）。
  - 调整建议（不立即改代码，先标注）：
    - list-item.selected.* → 从 color.brand.* 改为 color.action.*
    - focus-outline（组件内） → 统一引用 focus.ring.color（默认等于 color.action.primary）

- 组件层“冗余别名”收敛（示例）
  - --component-button-primary-background-color → 标注“别名 = component.button.primary.bg”，后续逐步替换模板类变量名为统一风格：component.button.primary.*
  - 统一命名风格：component.{name}.{part}.{state?}，如 component.button.primary.bg / component.input.focus.border / component.toggle.track.on.bg

五、暗色主题专项修正清单（不落地，仅建议）
- tokens.dark.css 中：
  - --component-button-secondary-disabled-background-color: var(--color-gray-50) → 应改为 background.disabled
  - --component-card-error-background-color: var(--color-gray-50) → 建议改为 background.surface（或 error 背景专用语义）
  - 各 input/textarea/select 的 disabled.* 一律替换为 background.disabled / text.disabled / border.subtle
- 焦点环：统一改为 focus.ring.*，默认 color=action.primary，width=2px，offset=1px（两主题可不同）。

六、实施策略（小步快跑）
- 第一步（仅添加不破坏）：
  - 在 tokens.css / tokens.dark.css 中“增加”新语义变量（background.*, text.*, border.*, focus.ring.*，text.disabled），并给旧变量提供“别名转发”（新→旧、旧→新二选一，以不破坏为准）。
  - 文档化“别名表 + 弃用时间线”。
- 第二步（局部组件迁移）：
  - 选 Button/Input/Toggle 三类基础件，优先替换为新语义（action.* / background.* / text.* / focus.ring.*）。
  - Astro /components 对照页（Baseline vs Adjusted）双主题/三尺寸矩阵截图固化。
- 第三步（状态面板统一）：
  - 将所有 disabled/error/success/info 的引用统一到“feedback.* + background.disabled + text.disabled + border.*”。
- 第四步（复杂件与适配层）：
  - SrhDateRangePicker/Select/Dialog 的“壳”实现统一引用新语义；小程序端做 uni.scss 桥接。

七、影响评估与回滚
- 风险点：类名/变量名替换导致样式回退；暗色对比度不达标。
- 降低风险：
  - 使用“别名+对照页”双保险；接受度量：对比度（WCAG）、状态可辨性；每步发“变更清单”。
- 回滚：保留旧变量出口，若出现问题仅回退某组件引用到旧变量即可。

八、附：建议的“别名映射表”（第一批）
- 变量别名（保留旧→新，或新→旧；最终以新为准）
```
/* 背景 */
--color-semantic-bg-primary     = var(--background-surface);
--color-semantic-bg-secondary   = var(--background-hover);
--color-semantic-bg-page        = var(--background-page);
--color-background-page         = var(--background-page); /* 别名保留，标注弃用 */

/* 文字 */
--color-semantic-text-primary   = var(--text-primary);
--color-semantic-text-secondary = var(--text-secondary);
--color-semantic-text-muted     = var(--text-muted);
--color-text-primary            = var(--text-primary);     /* 别名保留，标注弃用 */
--color-text-secondary          = var(--text-secondary);

/* 边框 */
--color-semantic-border-default = var(--border-default);
--color-semantic-border-subtle  = var(--border-subtle);

/* 新增（建议） */
--text-disabled                 = ...;  /* light: #9CA3AF; dark: #8A8C90（建议） */
--focus-ring-color              = var(--color-action-primary);
--focus-ring-width              = 2px;
--focus-ring-offset             = 1px;
```

九、下一步（待你确认后执行）
- 在 tokens.css / tokens.dark.css 内“只增加不破坏”地引入新语义与别名（不删旧名）。
- 在 docs/ 中补“变量变更记录表”，列出：改了哪些、为何改、影响组件与回滚路径。
- 在 Astro 对照页上验证 Button/Input/Toggle 的双主题/三尺寸矩阵，截图固化。
- 小程序 uni.scss 同步新增 text.disabled / focus.ring.* 与 background.* 的桥接变量。

说明
- 本稿仅为建议，不改代码。建议你确认“命名体系与行动色/品牌色边界”后，我再按上述步骤小步实施。
