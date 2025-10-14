# Web（Vue 3 + Tailwind + shadcn-vue）组件清单与落地计划

目的
- 回应“组件不完整”的担忧，给出完整组件矩阵、当前项目现状、缺口与落地顺序。
- 面向 Domain 风格房源详情页（PDP），确保像素级还原与后续扩展。

项目上下文
- 仓库：apps/web-shadcn
- 已安装（来自 src/components/ui/）：alert, avatar, badge, button, card, carousel, dialog, input, separator, skeleton, sonner, textarea
- 工具：Tailwind v4、lucide-vue-next、markdown-it、vue-sonner

一、页面分区与组件映射（自上而下）
- 顶部导航区
  - Breadcrumb（面包屑）
  - Search（Combobox/Command + Popover/Dropdown Menu）
  - User/Menu（Dropdown Menu、Tooltip）
- Hero/Gallery 媒体区
  - Carousel 轮播（已具备）
  - Lightbox/Zoom（Dialog 已具备，需像素定制）
  - 缩略图条/指示器（无头/半无头，需自定义）
  - 视频播放（可选）
- 核心摘要（左主列）
  - Summary Card（Card+Badge+Icon）
  - 统计图标组（Bed/Bath/Car 已用）
  - 操作：收藏/分享（Tooltip + Dropdown Menu/Popover）
- 详情内容（左主列）
  - Description（Markdown 已具备）
  - Key Facts/Features（Grid + Tag/Badge）
  - Floorplan（Dialog + Zoom）
  - Schools/Transport（Tabs + Table/List）
  - Similar/Recommendations（横向 Carousel + 卡片）
- 侧栏（右列）
  - AgentCard（已具备 Avatar + 表单 + toast）
  - Enquiry 表单（表单控件全集 + 验证）
  - Inspections/预约（DatePicker/Calendar + Sheet/Drawer）
  - Mortgage/Costs（Slider + Input）
- 底部
  - Disclaimer（Accordion/Collapsible）
  - Report listing（Dialog）
  - Print/Share（Dropdown Menu + 原生分享/打印）

二、组件清单（优先级/有头-无头/现状）
说明：P0=详情页必要，P1=增强，P2=可选

基础布局（P0）
- Button（有头；已具备）
- Card（有头；已具备）
- Badge（有头；已具备）
- Separator（有头；已具备）
- Avatar（有头；已具备）
- Label（有头；缺）
- Table（有头；缺）
- Tabs（有头；缺）
- Accordion/Collapsible（有头；缺）

交互与覆盖（P0）
- Dialog（有头；已具备）
- Carousel（有头；已具备；缩略条建议无头/半无头）
- Sheet/Drawer（有头；缺）
- Tooltip（有头；缺）
- Popover（有头；缺）
- Dropdown Menu（有头；缺）
- Hover Card（有头；缺）

表单与选择（P0）
- Input（有头；已具备）
- Textarea（有头；已具备）
- Select（有头；缺）
- Combobox（有头；缺）
- Checkbox（有头；缺）
- Radio Group（有头；缺）
- Switch（有头；缺）
- Slider（有头；缺）
- DatePicker/Calendar（有头；缺）
- Form（有头；缺；或以组合模式集成 vee-validate/yup）

反馈与状态（P0）
- Sonner/Toast（有头；已具备）
- Alert（有头；已具备）
- Skeleton（有头；已具备）
- Progress/Spinner（有头；缺）

滚动/视图（P1）
- Scroll Area（有头；缺）
- Aspect Ratio（P2；缺）
- Resizable（P2；缺）

高级/搜索（P1）
- Command（命令面板/搜索；有头；缺）
- Pagination（P1；列表页用；缺）
- Breadcrumb（P1；缺）

三、有头 vs 无头建议（像素级对齐）
- 有头优先：Button/Card/Badge/Separator/Input/Textarea/Select/Checkbox/Radio/Switch/Slider/Tabs/Accordion/Table/Alert/Skeleton/Toast/Dialog/Sheet/Tooltip/Popover/Dropdown/Hover Card
  - 理由：速度与一致性高，可访问性与状态覆盖好；少量覆写类名即可贴近像素
- 无头/半无头：Gallery 缩略条、Lightbox 动画、Sticky CTA（移动端吸附条）、Map Overlay、Floorplan Zoom
  - 理由：需要完全控制 DOM/CSS，以满足对标站特殊结构/动效/吸附阈值

四、当前缺口与落地顺序（最小增量交付）
批次 A（优先覆盖 PDP 关键交互）
1) DatePicker/Calendar（预约/看房时间）
2) Sheet/Drawer（移动端预约与分享）
3) Select/Combobox（下拉选择与搜索建议）
4) Tooltip/Popover/Dropdown Menu（顶部菜单与分享/操作）
5) Progress/Spinner（加载/提交态）
6) Label/Form（表单语义/错误态统一）

批次 B（结构与数据展示）
1) Tabs（Schools/Transport 切换）
2) Accordion/Collapsible（Disclaimer/可折叠段落）
3) Table（周边数据表格）
4) Scroll Area（局部滚动列表）
5) Breadcrumb（面包屑）

批次 C（增强与可选）
1) Command（快速搜索/命令面板）
2) Pagination（列表页用）
3) Aspect Ratio/Resizable（特定媒体布局/对比）

五、目录与命名规范（保持一致性）
- 生成路径：src/components/ui/<component>/
- 子组件命名：以 PascalCase 与功能后缀（如 DialogContent.vue、DropdownMenuItem.vue）
- index.ts：导出默认与子组件，便于按需导入
- 变量：通过 CSS 变量（HSL）与 Tailwind 主题映射，尽量不用硬编码色值
- 图标：统一用 lucide-vue-next；尺寸 h-4 w-4 为默认基线

六、像素级 PDP 的组件用法建议（对标要点）
- Gallery：Carousel + Dialog；缩略条/指示器/遮罩用无头实现，支持键盘左右与 ESC
- Summary Card：Card + Badge + lucide 图标；价格字号/字重/行高按 Tokens 固化
- Description：markdown-it + @tailwindcss/typography（可选），统一段落/列表/链接样式
- Inspections：Tabs + Calendar + Sheet/Drawer + 表单；提交 toast 与错误态一致
- Schools/Transport：Tabs + Table/List + Tag；空态/错误态用 Skeleton/Alert
- Recommendations：横向 Carousel + 卡片；移动端可改为横向滚动列表
- Sticky CTA（移动端）：无头，滚动阈值、阴影与高度由 Tokens 控制

七、后续动作（建议）
- A 批次组件的 CLI 生成（仅写文件，不执行安装/不启动服务）：Tooltip、Popover、Dropdown Menu、Hover Card、Tabs、Accordion、Collapsible、Table、Select、Combobox、Checkbox、Radio Group、Switch、Slider、DatePicker/Calendar、Progress/Spinner、Label、Form、Breadcrumb、Scroll Area、Sheet/Drawer
- 在 docs/ 下补充《组件生成计划清单.md》（列出每个组件：用途、落点路径、是否可替代、风险与回滚）
- 完成后在 PDP 增强：预约/分享/周边/推荐/Sticky CTA，并进行叠图验收

附：检查表（P0 覆盖）
- [x] Button/Card/Badge/Separator/Input/Textarea/Avatar/Dialog/Carousel/Skeleton/Alert/Toast
- [ ] Select/Combobox/Checkbox/Radio/Switch/Slider
- [ ] DatePicker/Calendar
- [ ] Sheet/Drawer
- [ ] Tooltip/Popover/Dropdown Menu/Hover Card
- [ ] Progress/Spinner
- [ ] Label/Form
- [ ] Tabs/Accordion/Collapsible/Table
- [ ] Breadcrumb/Scroll Area

说明
- 本清单是“设计与工程双向对表”的依据，不涉及任何受版权保护资产拷贝。
- 完成 A 批次后即可进入 PDP 的“像素级细化与叠图验收”。
