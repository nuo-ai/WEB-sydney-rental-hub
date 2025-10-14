# Implementation Plan

[Overview]
目标：修复设计站点 tools/design-site-astro 的信息架构与暗色主题一致性问题，使首页与索引页不再出现“返回”按钮，暗色模式下导航/卡片/secondary 等组件与语义背景协调，并补齐基础 Tokens 演示页，建立可持续扩展的设计系统展示站点。

范围与背景：
- 当前 BaseLayout.astro 在所有页面（包括首页/索引页）统一渲染 backbar，导致首页出现“返回上一页/返回首页”按钮。
- tokens.dark.css（自动生成）中的 component-* 变量在暗色模式下仍偏向浅色（如 secondary-bg 为白），使导航、卡片等呈现明色视觉，不和谐。
- /tokens 仅有 blackwhite 演示页，缺少 Colors/Typo/Spacing/Radius/Shadows 等基础类目页，不利于系统化理解与复制使用。
- 需要遵循“自动生成文件不直接修改”的安全策略，通过叠加覆盖（overrides）方式进行暗色统一。

高层方案：
- 新增覆盖样式 tokens.overrides.css，后置引入于 BaseLayout，使暗色模式下的组件层变量（component-*）统一使用语义变量（var(--color-semantic-*)）。
- 为 BaseLayout 增加 showBackbar 可选属性，首页/索引页隐藏返回区，仅二级详情页显示。
- 补齐基础 Tokens 五类演示页并更新 /tokens/index 索引；优化 /tokens/blackwhite 的明/暗对比与阴影演示细节。
- 最终进行明/暗主题与可访问性基线检查（对比度/焦点可视化/移动断点）。

[Types]  
类型系统变化极小，仅在 Astro 组件层增加 props 类型约定，并可选抽象 tokens 索引数据结构。
- BaseLayout props
  - title?: string
  - showBackbar?: boolean（默认 true）
- 可选：TokenLink（若后续用数据驱动 /tokens/index）
  - interface TokenLink { href: string; label: string; desc?: string }

[Files]
文件改动以“新增覆盖 + 小幅修改 + 新增页面”为主，不删除/移动现有文件；不直接修改自动生成的 tokens.css / tokens.dark.css。

- 新增文件（目的）
  1) tools/design-site-astro/src/styles/tokens.overrides.css
     - 仅在暗色模式下覆盖组件层变量，示例：
       - [data-theme='dark'] --component-button-secondary-bg: var(--color-semantic-bg-primary) 或 var(--color-gray-800)
       - [data-theme='dark'] --component-button-secondary-text: var(--color-text-primary)
       - [data-theme='dark'] --component-button-secondary-border: var(--color-semantic-border-default)
     - 如有需要，同步为 card/nav 所依赖的 component-* 变量提供暗色适配。
  2) 基础 Tokens 演示页（统一骨架、可复制变量名）：
     - tools/design-site-astro/src/pages/tokens/colors.astro
     - tools/design-site-astro/src/pages/tokens/typography.astro
     - tools/design-site-astro/src/pages/tokens/spacing.astro
     - tools/design-site-astro/src/pages/tokens/radius.astro
     - tools/design-site-astro/src/pages/tokens/shadows.astro

- 修改文件（具体修改）
  1) tools/design-site-astro/src/layouts/BaseLayout.astro
     - props 增加 showBackbar?: boolean（默认 true）
     - backbar 使用条件渲染：{showBackbar && <div class="backbar">…</div>}
     - 在 <style> 中于 tokens.css / tokens.dark.css 之后引入 tokens.overrides.css（保证覆盖生效）
     - 主题切换按钮文案根据当前主题联动（暗色→显示“切换浅色”，浅色→显示“切换暗色”）
  2) tools/design-site-astro/src/pages/index.astro
     - 使用 <BaseLayout showBackbar={false} …>，首页隐藏返回区
  3) tools/design-site-astro/src/pages/tokens/index.astro
     - 补充五个基础 Tokens 页链接与简述（colors/typography/spacing/radius/shadows），保留 blackwhite
  4) tools/design-site-astro/src/pages/components/index.astro
     - 卡片/边框/文字不再直接依赖“button-secondary”变量；依赖语义变量（或由 overrides 统一），暗色下不再显得“白底突兀”
  5) tools/design-site-astro/src/pages/tokens/blackwhite.astro
     - 明色主题下提升说明文字对比度（例如 .desc 在 light 使用 #444）
     - 暗色模式下示例阴影层级可见但不过度抢眼，整体与导航/卡片一致

- 配置更新
  - 无构建/依赖变更；仅 CSS 文件新增与 Astro 页面/布局小改。

[Functions]
函数级改动很少，核心为布局脚本与 DOM 事件。
- BaseLayout.astro
  - props 解构：const { title = 'SRH Design Site', showBackbar = true } = Astro.props;
  - 主题切换脚本：依据 html[data-theme] 实时更新按钮文本与 localStorage('astro-theme')
- 可选：/tokens/index 由静态链接改为数组渲染（使用 TokenLink[]），当前可先保持静态。

[Classes]
无新建 JS 类。CSS 类与变量层面：
- 暗色主题下 .nav / .card / .btn--secondary 等从“浅色 secondary”回归“暗色语义背景”变量（通过 overrides 覆盖）。
- .desc 在 light 提升对比度；focus outline 通过 tokens 变量统一显著性。

[Dependencies]
无新增第三方依赖；维持现有 astro 版本与脚本。新增的仅为覆盖 CSS 文件（源内维护、可回滚）。

[Testing]
测试策略：以视觉一致性与可访问性为核心的手测与基线检查。
- 巡检路径：/、/tokens/、/components/、/tokens/blackwhite 于明/暗两种主题
- 对比度：正文 ≥ 4.5:1；说明文字≥ 4.0:1（实用标准）；链接/按钮 hover/active 明显；focus outline 可见
- 交互：主题切换文案与状态一致，localStorage 生效；backbar 仅二级页显示
- 响应式：720px/640px 等断点下网格与间距合理

[Implementation Order]
最小风险顺序，先“覆盖”再“结构”，最后“扩展”：
1) 新增 tokens.overrides.css（仅暗色覆盖关键 component-*）
2) 修改 BaseLayout：引入 overrides；加 showBackbar 条件渲染；主题切换按钮文案联动
3) 首页与两个索引页应用 showBackbar={false}；调整 components/index 卡片样式（或依赖 overrides 达成）
4) 新增五个基础 Tokens 页并更新 /tokens/index
5) 优化 /tokens/blackwhite 的明/暗可读性与阴影演示细节
6) 明/暗主题全面自测与可访问性核对（桌面/移动），修正问题后收尾
