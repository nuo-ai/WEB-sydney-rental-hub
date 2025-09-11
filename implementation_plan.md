# Implementation Plan

[Overview]
为移动端网站的“顶部导航 + 搜索栏”建立品牌蓝基线，并关闭底部导航；同时预留可配置的底部导航变体（供后续小程序复用）。方案通过语义令牌与组件级开关实现，保证向后兼容与易回滚。

本次改造聚焦于：
- 统一导航/搜索的尺寸、间距、圆角、图标大小与交互反馈，前端表现与示例参考一致（轻量、克制）。
- 清理顶部导航左侧图标，仅保留“Juwo”文字标识，颜色使用品牌蓝（--juwo-primary）。
- 在网站默认关闭底部导航；通过组件 prop 与 CSS 令牌实现“随时可开启”的底栏变体，供未来小程序直接复用。
- 所有新数值先落在组件与 page-tokens.css 的语义令牌，后续可在不改结构前提下快速调整。

[Types]  
类型系统不做新增；仅定义“CSS 语义令牌”与“组件 Prop”的约束。

语义令牌（CSS Variables，单位 px 除非注明）：
- 导航（移动/桌面）
  - --nav-h-mob: 56
  - --nav-h-desk: 64
  - --nav-px-mob: 16
  - --nav-px-desk: 32
  - --nav-gap: 24
  - --nav-icon: 16
  - --nav-active-underline: 2
  - --nav-shadow: none（字符串，可选值 'none' 或阴影tokens）
  - --bottom-nav-height: 56（用于页面 padding-bottom 防遮挡）
  - --nav-safe-area-bottom: env(safe-area-inset-bottom, 0px)
- 搜索栏
  - --search-h-mob: 44
  - --search-h-desk: 44
  - --search-radius: 6
  - --search-padding-x: 12
  - --search-icon: 16
  - --search-chip-radius: 16
  - --search-chip-gap: 8
  - --search-suffix-right: 12
  - --search-suffix-hit: 32

组件 Prop：
- Navigation（src/components/Navigation.vue）
  - disableBottomNav?: boolean（默认 true；true=网站关闭底栏，false=显示底栏；小程序可设为 false）
  - isHidden?: boolean（已有，控制顶部隐藏）

[Files]
本次涉及的文件均为既有文件追加修改；不新增依赖与构建配置。

- 新文件：无

- 修改文件：
  1) vue-frontend/src/styles/page-tokens.css
     - 新增上述“导航/搜索”语义令牌（含注释与断点示例），不覆盖现有值，仅提供默认基线。
  2) vue-frontend/src/components/Navigation.vue
     - 模板：移除左侧 logo 图标，仅保留“Juwo”文字；新增 disableBottomNav prop；底栏显示条件修改为 v-if="isMobile && !disableBottomNav"。
     - 样式：移动端高度改为 var(--nav-h-mob, 56px)；顶部/底部导航内边距/间距/图标尺寸等读令牌；底栏高度包含安全区 calc(var(--nav-h-mob, 56px) + var(--nav-safe-area-bottom, 0px))；活动态 2px 下划线读令牌。
  3) vue-frontend/src/components/SearchBar.vue
     - 样式：高度/圆角/图标尺寸/左右内边距/Chip 圆角与间距统一读搜索令牌；提交按钮（如展示）颜色使用 --juwo-primary。
     - 逻辑：不改交互（移动端点击整框进入筛选；桌面展示建议列表）；仅在样式层读令牌。
  4) 如存在布局容器（App.vue/Layout.vue/Navigation 调用处）
     - 传入 :disableBottomNav="true"（网站默认）；若未集中调用则保持组件默认 true 即可。

- 删除/移动文件：无

- 配置更新：无

[Functions]
函数签名不新增，仅对现有属性读取与模板条件做小改。

- 新增/修改
  - Navigation.vue
    - defineProps 增加：disableBottomNav?: Boolean = true
    - 模板条件：<nav v-if="isMobile && !disableBottomNav" class="bottom-nav">（替换原先 v-if="isMobile"）
  - SearchBar.vue
    - 无函数改动；样式变量化，不影响 handleFocus/handleInput 等既有行为

- 移除：无

[Classes]
CSS 类组织不变，补充令牌读取与安全区计算。

- 新增/修改的关键样式（示意）
  - .top-nav: height: var(--nav-h-desk, 64px)
  - .top-nav-content: padding-inline: var(--nav-px-desk, 32px)
  - .nav-left/.main-nav: gap: var(--nav-gap, 24px)
  - .main-nav-item.active::after: height: var(--nav-active-underline, 2px)
  - .bottom-nav: height: calc(var(--nav-h-mob, 56px) + var(--nav-safe-area-bottom, 0px))
  - .nav-container: padding-inline: var(--nav-px-mob, 16px)
  - .nav-icon: width/height: var(--nav-icon, 16px)
  - 搜索类：wrapper/inner 高度/圆角/内边距引用 --search-*；Chip 圆角/间距引用 --search-chip-*；后缀间距引用 --search-suffix-*

[Dependencies]
不新增第三方依赖；继续使用 lucide-vue-next 图标与 Element Plus 组件。

[Testing]
采用手动验证 + 断点检查，保证视觉与交互符合预期。

- 断点自测（宽度 360、390、768、1024）
  - 顶部导航：移动 56/桌面 64 稳定；左侧仅“Juwo”文字；活动路由 2px 下划线；无过度阴影。
  - 底部导航：默认不出现（网站）；将 disableBottomNav 置 false 可临时启用验证，安全区计算正确。
  - 搜索栏：移动/桌面高度 44；圆角 6；左右 12；前缀图标 16；Chip 圆角 16、间距 8；右侧后缀对齐 12；按钮（若展示）品牌蓝。
  - 交互：移动端点击整框进入筛选；桌面建议列表键盘导航与选择正常。
- 回归：过滤/Overlay/相邻区域推荐等逻辑不受样式改动影响。

[Implementation Order]
先令牌再接线，逐步下沉到组件，最后开关验证底栏变体。

1) page-tokens.css：补齐 nav/search 语义令牌（含安全区变量），仅新增。
2) Navigation.vue：
   - 新增 disableBottomNav prop（默认 true）
   - 去除左侧 logo 图标，仅保留文字“Juwo”
   - 桌/移样式改为引用 nav 令牌；底栏高度含安全区
   - 活动态下划线读令牌
3) SearchBar.vue：样式统一读 search 令牌（高度/圆角/内边距/图标/Chip/后缀）
4) 若需要的容器处：显式传入 :disableBottomNav="true"（或保持默认）
5) 验证四断点前端表现；如需微调，优先改令牌值而非结构
6) 将“底栏变体使用说明”加入注释（供小程序直接启用）
