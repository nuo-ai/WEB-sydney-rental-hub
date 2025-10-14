# P0 视觉验收清单（基线→微调）

说明
- 目标：给“好不好看”的可执行标准，先跑出“能用的基线”，再只改 Design Tokens 做微调（尽量不动组件代码/逻辑）。
- 验收位置：
  - Web 基线与对照：tools/design-site-astro 的 /components 页面（建议新增“Baseline vs Adjusted”对照卡）。
  - 业务页抽查：apps/web（首页/详情/筛选面板）。
  - 小程序/H5：apps/uni-app（基于静态构建的 WXSS，需重构建发版）。
- 修改方式优先级：语义/组件层 Tokens（首选） →（如确实缺口）提出“增量令牌”建议（暂不直接写代码）。

统一通用标准（所有组件通用）
- 对比度（深/浅色均需）
  - 主文案/重要数值 ≥ 4.5:1；次文案/说明 ≥ 3:1
  - 图标 stroke 继承 currentColor，与文字对齐
- 视觉节奏
  - 字号/行高取自文字系统 Token（--text-*/--line-height-*）；行距稳定
  - 圆角/间距使用统一 Token（radius.*、space.*），不写死具体数值
- 交互反馈
  - hover/active/focus/disabled 各状态清晰可辨（颜色/边框/阴影/不透明度）
  - 键盘导航可见（focus ring 明确），动效不过度（200ms 左右）
- 主题一致
  - [data-theme='dark'] 下自动适配，无“反白/反差不足/幽灵色”
  - 禁止组件内写死颜色/尺寸（全部经由 Tokens）

如何调整（原则）
- Web（Astro + apps/web）：优先改 Tokens（分钟级见效）
  - 颜色：color.brand.* / color.action.primary / background.* / text.* / border-interactive
  - 圆角：radius.*（如 --radius-sm/md/lg）
  - 字号/行高：--text-* / --line-height-*
  - 间距：space.*（如 --space-4/6/8）
  - 阴影：shadow.*（如 --shadow-sm/md/lg）
- 小程序（apps/uni-app）：同改 Tokens 源，重新构建生成 WXSS 后生效（通常半天内完成）

组件逐项验收（P0）

1) 按钮 Button（含主按钮/次按钮/幽灵/危险态）
- 验收点
  - 三档尺寸统一：高度、左右内边距、圆角值、字重一致性
  - hover/active 明暗层级有区分；disabled 对比度合规且可辨
  - 点击与键盘 focus ring 明确
- 常改 Tokens（举例）
  - 主色：color.action.primary（及其 hover/active 对应）
  - 文本/图标：text.on.action（反白/反黑对比）
  - 圆角/间距：radius.md、space.*
  - 阴影：shadow.sm/md（如有）

2) 输入框/搜索框 Input / SearchInput
- 验收点
  - 占位符与正文对比度合规；清除按钮/前后缀图标对齐
  - hover 边框增强，focus 边框+阴影/外发光可见
  - 错误态/禁用态明显（颜色/游标/不可点击反馈）
- 常改 Tokens
  - 边框：border-interactive（含 hover/focus 深度）
  - 文本：text.primary / text.placeholder
  - 背景：background.surface
  - 阴影：shadow.focus（如采用）

3) 开关 Toggle / Switch
- 验收点
  - 轨道/拇指尺寸比例；checked 与 unchecked 背景对比明显
  - disabled 淡化但仍可读；键盘切换可见（focus ring）
  - 动效自然（拇指位移动画 ~120–200ms）
- 常改 Tokens
  - 选中色：action/on.toggle（如无语义，先用 color.action.primary）
  - 轨道/拇指背景：background.surface / background.disabled
  - 边框/阴影：border-interactive / shadow.*

4) 日期范围选择器 DateRangePicker（库组件外包“壳”）
- 验收点
  - 头部/星期/日期单元对齐；hover、range 高亮、today 标识清楚
  - 快捷项（如最近7天）样式统一；深/浅色下分隔线与阴影不过暗/不过亮
  - 打开/关闭动效柔和；遮罩层透明度合适
- 常改 Tokens
  - 主色/高亮：color.action.primary
  - 文本层级：text.primary/secondary
  - 分隔线：border.*
  - 弹层背景/阴影：background.surface、shadow.md/lg

5) 下拉选择/自动补全 Select / Autocomplete（库组件外包“壳”）
- 验收点
  - 候选项 hover/active 背景与文字对比明确；多选 tag（chip）尺寸与节奏统一
  - 输入“2000”“Syd”时建议项清晰，键盘导航有高亮
  - 空态与加载态有明确提示
- 常改 Tokens
  - 菜单背景/项 hover：background.surface / background.hover
  - 文本层级：text.primary/secondary
  - Tag（chip）背景/边框：component.chip.*（若缺少，提出增量令牌建议）

6) 弹窗/抽屉 Dialog / Drawer（库组件外包“壳”）
- 验收点
  - 标题/正文/操作区间距统一；遮罩透明度不刺眼
  - 关闭按钮可见/可点；Esc/遮罩点击行为可配置（按产品预期）
  - 小屏适配（纵向滚动与底部按钮固定不冲突）
- 常改 Tokens
  - 背景：background.surface
  - 阴影：shadow.lg
  - 标题字号/权重：text.* + font-weight.*
  - 遮罩：overlay.alpha（如缺失，用 shadow/rgba 表达并提出增量建议）

7) 页签 Tabs / 分段控件 Segmented
- 验收点
  - 相邻无缝、端部圆角一致；激活项有下划线/底色/粗体之一，不混乱
  - 尺寸档（sm/md/lg）在高度/内边距/字号/圆角上统一
- 常改 Tokens
  - 激活态：component.tabs.active.* / component.segmented.active.*（若缺口，以语义层提出）
  - 分隔/边框：border.*
  - 字号/行高：text.* / line-height.ui

8) 复选框 Checkbox
- 验收点
  - 勾选图标大小与方框匹配；hover/active/focus/disabled 区分明确
  - 文案与控制的垂直对齐；点击文字可切换
- 常改 Tokens
  - 勾选/边框色：action/on.checkbox / border-interactive
  - 文本色：text.primary/secondary

9) 徽标/标签 Badge / Chip
- 验收点
  - 颜色/tone（信息/成功/警告/危险）体系统一；圆角与间距与按钮/输入一致
  - 文本与图标对齐；可关闭态视觉稳健
- 常改 Tokens
  - 背景/描边/文本：component.badge.* / component.chip.*（若缺失，提出增量建议）

10) 提示气泡/菜单 Tooltip / Dropdown（库组件外包“壳”）
- 验收点
  - 文字对比度与阴影清晰；箭头与边缘对齐
  - 小屏/密集场景无遮挡关键元素
- 常改 Tokens
  - 背景/文本/阴影：background.surface / text.primary / shadow.md

联动与一致性检查（抽样）
- 首页筛选：点击“应用（N）”后 URL/Pinia 同步仅写非空键，刷新直链可复现；深/浅色下按钮/输入/弹窗一致
- 详情页 CTA：主按钮与列表页主按钮一致（同一套 Tokens）
- Profile：收藏/历史/弹窗风格一致，Chip/Badge 与列表项一致

问题与后续（先记录，不立刻改代码）
- 若发现需要“组件层令牌”但当前不存在：在 docs/ 中开出“令牌增量草案”，命名与语义对齐（避免直接硬编码）
- 进度与证据：建议配合截图/短录屏放入 docs/reports/ 下，以便回溯与比对

小结
- 判断“好不好看”的依据 = 标杆（realestate.com.au 原子数据） + 我们的品牌基调 + 令牌三层规范 + Astro 可视化对照。
- 调整优先改 Tokens，Web 分钟级见效；小程序经重构建发版生效。只要遵守“组件仅消费语义/组件令牌”的原则，后续统一与迭代成本最低。
