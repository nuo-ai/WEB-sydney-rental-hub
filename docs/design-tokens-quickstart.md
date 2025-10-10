# Design Tokens 快速上手（Web 前端）

目的：用最少的规则和例子，说明“现在有哪些设计令牌（Design Tokens）”以及“如何在 Web 前端落地使用”。

来源与结构
- 令牌入口（网站实际使用）：apps/web/src/styles/design-tokens.css
- 三层模型
  1) 原始令牌 Primitive：物理值（颜色、尺寸、阴影、时长、字体族）
  2) 语义令牌 Semantic：含义化命名（文本/背景/边框/状态/间距/字号等）
  3) 组件令牌 Component：面向组件/模式（按钮/输入/卡片/筛选等）

一、你现在“已经有”的 Tokens（精选）
1) 原始令牌（举例）
- 颜色与灰阶
  - --color-white, --color-black
  - --gray-50 … --gray-900
- 品牌蓝与主色
  - --blue-50 … --blue-900
  - --brand-blue-400: #0047e5, --brand-blue-500: #0057ff, --brand-blue-600: #0036b3
- 功能色
  - --red-600/700, --green-500, --amber-500, --cyan-500
- 尺寸/排印/动效
  - --size-2 … --size-64, --size-580（卡片宽度参考）
  - --weight-regular/medium/semibold/bold, --leading-tight/normal/relaxed/loose
  - --shadow-100 … --shadow-400, --duration-150/200/300, --easing-standard
  - 字体族：--font-zh-base, --font-en-base, --font-system-base

2) 语义令牌（优先在业务/组件里使用）
- 品牌别名
  - --brand-primary/hover/active/light（主色 #0057FF 及其变体）
- Element Plus 主题基色（CSS 变量）
  - --el-color-primary, --el-color-primary-light-*, --el-color-primary-dark-2
- 背景/文本/边框/状态
  - **强调色 (Accent)**:
    - `--accent-primary`: #6699cc (蓝宝石钢蓝), 用于关键操作 (CTA按钮、链接)。
    - `--accent-hover`: `#7aaee6`, 强调色的悬浮状态。
  - **背景 (Background)**: --color-bg-primary/secondary/muted/card/page
  - **文本 (Text) - (新！)**:
    - `--text-contrast-strong`: 最强对比度，用于标题和重要文本。
    - `--text-contrast-medium`: 中等对比度，用于正文和次要信息。
    - `--text-contrast-weak`: 弱对比度，用于辅助性文字或禁用状态。
    - *旧版 `--color-text-*` 将逐步废弃。*
  - **边框 (Border)**: --color-border-default/strong/subtle/hover
  - **状态 (Status)**: --color-danger/success/warning/info, 以及 soft 背景与边框
  - **焦点环 (Focus Ring)**: --color-focus-ring
- 排印/字号/间距/圆角/阴影/过渡
  - **字体族/字重**: --font-family-*, --font-weight-*
  - **行高 (Line Height) - (新！)**:
    - `--line-height-title`: 用于页面或章节标题。
    - `--line-height-body`: 用于大段的正文内容。
    - `--line-height-ui`: 用于界面控件（按钮、输入框等）中的文本。
  - **字号**: --font-size-* 与别名 --text-*
  - **间距**: --space-*（2xs…4xl）、--gap-*
  - 圆角：--radius-*（2xs…full）
  - 阴影/动效：--shadow-*, --transition-*, --motion-*

3) 组件令牌（直接可用于组件样式）
- 按钮 Button：--button-*
- 筛选 Chip：--chip-*
- 搜索输入 Search：--search-*
- 列表项 List item：--list-item-*
- 面板 Panel：--panel-*
- 其它：--checkbox-*、--clear-btn-*、--areas-*、--focus-shadow

二、怎样在 Web 前端应用
1) 全局引入（确保 CSS 变量生效）
- 在入口文件或全局样式中引入 design-tokens.css：
  // main.ts / main.js / App.vue / 或全局 index.css
  import "@/styles/design-tokens.css";
  // 或
  @import "@/styles/design-tokens.css";

原理：引入后，:root 上的 CSS 变量对全站生效，组件可直接 var(--xxx) 使用。

2) 在组件样式中消费 Tokens（推荐用语义层）
- 主按钮（前端表现：主色背景，hover 变浅，active 变深；文字白色）
  .btn-primary {
    background: var(--button-primary-bg);        /* -> --brand-primary -> #0057FF */
    color: var(--button-primary-color);          /* -> 白色 */
    border-radius: var(--button-radius);         /* -> 12px（示例） */
    padding: var(--button-padding-y) var(--button-padding-x); /* -> 8px 16px */
    font-size: var(--button-font-size);          /* -> 14px */
    font-weight: var(--button-font-weight);      /* -> 500 */
    transition: var(--transition-colors);
    box-shadow: var(--shadow-button);
  }
  .btn-primary:hover  { background: var(--button-primary-hover-bg); }
  .btn-primary:active { background: var(--button-primary-active-bg); }

- 卡片/面板（白卡、灰边、hover 提升）
  .card {
    background: var(--panel-bg);                 /* -> 白色 */
    border: 1px solid var(--panel-header-border);/* -> 灰300 */
    border-radius: var(--panel-radius);          /* -> 8px */
    box-shadow: var(--shadow-sm);
  }
  .card:hover { box-shadow: var(--shadow-md); }

- 文本与间距（统一用语义）
  .title   { color: var(--text-primary); font-weight: var(--font-weight-semibold); }
  .caption { color: var(--text-secondary); font-size: var(--text-sm); }
  .section { margin-bottom: var(--space-xl); }

3) 在 Vue 组件中内联使用
  <template>
    <div :style="{ color: 'var(--text-primary)', padding: 'var(--space-md)' }">
      示例文本
    </div>
  </template>

4) 与 Element Plus 的配合
- 你的语义层已经提供 --el-color-primary（及其梯度）。
- Element Plus 使用 CSS 变量模式时会读取这些变量作为主题色来源（视组件实现而定）。
- 若个别组件未读取到，可在覆盖样式中显式使用你的语义令牌，或在 ElConfigProvider 主题配置中映射到 CSS 变量。

5) 最佳实践（Do/Don’t）
- Do：优先使用语义令牌（如 --text-primary/--border-default/--bg-card）
- Do：组件内部引用“组件令牌”（如 --button-*、--panel-*）
- Don’t：在业务样式里直接写具体十六进制或硬编码 px（除非新增令牌不合理）
- 当出现新需求且语义不足时：先补充“语义层”→ 再考虑“组件层”→ 最后才是“原始层”

6) 主题扩展（暗色举例）
- 给 html 或 body 添加 .dark 类，在 .dark 作用域内仅“覆盖语义层”变量（如 --color-bg-page、--text-primary 等），组件层会自动跟随。
  .dark {
    --color-bg-page: #111827;
    --color-text-primary: #ffffff;
    /* …其余需要的语义覆盖… */
  }

三、非技术同学如何看颜色
- #0057FF（--brand-blue-500 / --brand-primary）：你的品牌主色，鲜亮但稳重，适合主按钮/主链接。
- 可视化查看器：tools/token-playground/color-inspector.html
  - 直接打开文件，输入十六进制色值即可预览颜色、对比度以及 RGB/HSL。

四、常见问题（FAQ）
Q1：为什么优先用语义令牌？
- 语义 = 统一、可主题化、后期可全局替换；避免到处散落具体色值导致风格难以维护。

Q2：Storybook 与网站颜色不一致？
- 需要保证 Storybook 也加载 apps/web/src/styles/design-tokens.css，并处在相同主题/Provider 环境。若缺失，Storybook 会退回到它自己的默认变量，导致偏色。后续有独立的对齐计划文档。

附：关键文件
- apps/web/src/styles/design-tokens.css（本项目的“真实来源”）
- tools/token-playground/color-inspector.html（颜色预览工具）

一句话总结
- 入口引入 design-tokens.css → 组件里用 var(--语义令牌) → 不硬编码值 → UI 一致、易主题化、易维护。
