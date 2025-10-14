# 新页面视觉标准 v1（前端表现与落地规范）

适用范围
- 本规范适用于 apps/web/src/views 下新增的所有页面
- 目标：保证“前端表现”统一，避免各自为政（间距/配色/交互不一致）
- 仅使用项目设计令牌（design tokens），禁止硬编码颜色与阴影/圆角

页面骨架（统一结构）
- Header：面包屑 + H1 + 可选副标题/统计
- Toolbar：搜索/筛选/排序等操作区（尽量复用现有组件）
- Content：列表/网格/卡片内容主体
- Footer：分页/统计汇总
- 前端表现：移动端左右 16px，桌面 32px；区块间距用 --page-section-gap/--page-section-gap-lg 控制

布局与间距（页面级令牌）
- 左右留白
  - 移动端：padding-left/right = var(--page-x-padding-mob)
  - 桌面端：padding-left/right = var(--page-x-padding-desktop)
- 区块间距
  - Header/Toolbar/Content/Footer 间距为 var(--page-section-gap)，桌面端切换到 var(--page-section-gap-lg)
- 底部导航适配
  - 使用 padding-bottom: var(--bottom-nav-height) 防遮挡（仅在启用固定底部导航的页面）

颜色与主题（语义令牌，禁止硬编码）
- 文案色：--color-text-primary / --color-text-secondary
- 边框色：--color-border-default（分隔线、弱边框）
- 交互弱底：--bg-hover（悬停反馈）
- 品牌主色：--juwo-primary（链接/CTA/强调）
- 容器背景：--color-bg-card（卡片、白底容器）
- 阴影：--shadow-level-*（统一卡片投影层级）

文本系统（styles/typography.css）
- 使用 .typo-* 工具类（示例）
  - h1/h2：.typo-h1 / .typo-h2
  - 正文：.typo-body
  - 次要/说明：.typo-secondary / .typo-small
- 前端表现：标题层级清晰，正文与辅助文一致节奏

图标规范（lucide + currentColor）
- 使用 lucide-vue-next 组件，颜色继承 currentColor
- 不在图标内部写死颜色；外层通过 class 或令牌控制颜色
- 尺寸遵循 --nav-icon 或场景定义的统一尺寸

组件复用与限制
- 按钮：BaseButton（大小/状态走令牌）
- 输入：BaseSearchInput 或 SearchBar 中的内置输入样式
- 过滤：FilterTabs、FilterPanel 等现有稳定组件
- 卡片：PropertyCard 或其派生样式；圆角、阴影、内边距走令牌
- 禁止在页面内重新定义品牌色/阴影/圆角

列表与卡片（PropertyCard 优先）
- 列表/网格的行间距、卡片间距统一
- 分隔线统一使用 --color-border-default
- 收藏/徽标/操作按钮与现有卡片一致（颜色、悬停、尺寸统一）

空状态与骨架屏（一致化）
- 空状态：图标 + 主/副文案，中性灰体系；按钮为引导操作
- 骨架屏：高度/圆角/间距统一，避免加载跳变
- 前端表现：加载、无数据在各页面表现一致

响应式断点与网格
- 断点：宽度 <= 768px 视为移动端；> 768px 视为桌面端
- 网格列数建议：移动端 1 列；桌面 2–3 列（按内容密度选择）
- 容器最大宽度：1200px（与现有页面一致）

可访问性（A11y）
- 焦点管理：优先使用 :focus-visible，避免默认 focus ring 干扰；必要处提供明显焦点样式
- 键盘支持：Esc 关闭弹层/面板，Tab 循环，关闭后焦点回到触发器
- ARIA：aria-label/aria-live/role 等语义补充（筛选变更/计数提示）

导航与入口模式
- 顶栏：方案 A（搜索/收藏 | AI 助手/我的）
- 地图入口：从首页/列表页操作区提供“地图视图”按钮（而非顶栏）
- 详情/通勤入口：从列表卡片/详情页进入；不在顶栏暴露 compare/commute

禁止事项（Lint Guard）
- 禁止 hex/rgb/hsla/命名色（除 design-tokens.css、style.css 定义处）
- 禁止内联样式写死颜色/阴影/圆角
- 禁止为局部组件引入与设计系统冲突的第三方样式

新页面 Checklist
- 复制 views/_PageScaffoldExample.vue 作为基底
- 仅使用设计令牌 + .typo-* 工具类
- 图标用 lucide + currentColor；按钮/输入复用基础组件
- 使用 FilterTabs/FilterPanel 等稳定组件集成筛选
- 空状态/骨架屏使用统一样式
- 不新增硬编码颜色、阴影、圆角
- 本地自检：npm run lint 与 npm run lint:style

示例骨架（伪代码）
- Header：面包屑（aria-label="Breadcrumb"）+ h1（.typo-h1）
- Toolbar：SearchBar / FilterTabs / 排序按钮（药丸按钮 + 下拉）
- Content：properties-grid 或表格容器
- Footer：分页（Element Plus 的 el-pagination）

落地说明
- 令牌定义见：styles/design-tokens.css、styles/page-tokens.css、styles/typography.css
- 如果遇到未覆盖的视觉需求，优先新增“语义令牌”，再引用到页面；不要直接写死色值
