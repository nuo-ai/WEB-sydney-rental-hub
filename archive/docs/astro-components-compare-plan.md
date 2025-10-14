# Astro /components “基线 vs 微调”对照卡实施方案（规划稿）

目标
- 在 tools/design-site-astro 的 /components 页面，提供“基线（Baseline）”与“微调（Adjusted）”左右对照，作为视觉验收与快速调参的唯一入口。
- 不改业务代码；所有差异尽量通过 Design Tokens（CSS 变量）体现，验证“先有再调整，主要改 Tokens 即可”。

页面结构与交互（不写代码，仅说明）
- 页面布局：两列栅格（基线 | 微调），同步切换：
  - 主题切换：顶部 data-theme 开关（light/dark），两列同时切。
  - 尺寸档切换：sm/md/lg，应用于两列组件快照。
  - 密度/圆角预设：normal/compact，radius 级别 quick switch。
- 组件清单（P0 覆盖）
  - 按钮 Button（主/次/幽灵/危险）
  - 输入/搜索 Input/SearchInput（含前/后缀、错误/禁用）
  - 开关 Toggle/Switch（on/off/disabled/focus）
  - 日期范围选择器 DateRangePicker（库组件包“壳”，展示单月/双月/快捷项）
  - 下拉/自动补全 Select/Autocomplete（单选/多选/键盘导航）
  - 弹窗/抽屉 Dialog/Drawer（遮罩/标题/操作区）
  - 页签 Tabs / 分段 Segmented（激活/禁用/滚动）
  - 复选框 Checkbox（默认/hover/active/focus/disabled）
  - 徽标/标签 Badge/Chip（信息/成功/警告/危险）

基线与微调的定义方法
- 基线（Baseline）列
  - 直接消费现有 Tokens（:root 与 [data-theme='dark']），不做覆盖。
  - 验证项目当前“能用的默认值”。
- 微调（Adjusted）列
  - 不改源码：在列容器上“局部覆盖”CSS 变量（仅语义/组件层）来模拟调整后的效果：
    - 例：设置 style 作用域或 data-scope='adjusted' 容器内覆盖：
      - color.action.primary、color.brand.hover/active
      - radius.*、space.*、line-height.*、shadow.*
      - 组件层 component.button.* / component.input.*（若暂缺则用语义近似）
  - 这样可快速试错、截图比对，不污染全局。确认方案后再回填 Tokens 源。

数据与状态同步（可视化验证点）
- 两列始终展示相同的“组件状态矩阵”
  - 尺寸（sm/md/lg）、主题（light/dark）、状态（default/hover/active/focus/disabled/checked）
  - 确保“外观差异只来源于 Tokens 覆盖”，而非组件逻辑差异
- 可选：提供“导出微调差异”按钮（输出当前覆盖的变量清单），便于回填到 Tokens 文件

实施步骤（任务卡）
1) 页面框架
   - 在 /components 页面内新增 CompareSection，两列容器（Baseline | Adjusted），顶部放统一控制面板
   - 控制项：主题（light/dark）、尺寸（sm/md/lg）、密度/圆角预设
2) 组件快照卡片
   - 为每个组件生成 SnapshotCard（同一 props/slots），被 CompareSection 双渲染
   - 确保每张卡片包含“最少一个完整状态矩阵”
3) 覆盖策略（微调列专用）
   - 在 Adjusted 列根容器添加一个 CSS class（如 .scope-adjusted）
   - 在该作用域内用 :root 变量同名覆盖（仅语义/组件层），严禁写死颜色/px
4) 验收对照
   - 将本页作为 docs/visual-acceptance-checklist.md 的“指定验收入口”，逐项对照并记录差异
   - 通过“对照截图/短录屏”固化决策依据，放入 docs/reports/
5) 回填 Tokens（在确认后）
   - 将 .scope-adjusted 中“有效的变量覆盖”批量回填至 Tokens 源（tokens/* 或 packages/ui/src/styles/tokens*.css 的源数据），并删除临时覆盖
   - 小程序端：同步构建 WXSS

不改代码的“变量覆盖”示例（仅用于概念说明，不直接落库）
- 覆盖色阶：color.action.primary / color.brand.hover / color.brand.active
- 圆角与阴影：radius.md → radius.lg；shadow.md → shadow.lg
- 文本对比：text.secondary 在 dark 下提升一档
- 输入焦点：shadow.focus 由 0 0 0 0 → 0 0 0 3px（注意可访问性）

验收标准（关联清单）
- 对照 docs/visual-acceptance-checklist.md：对比度、视觉节奏、交互反馈、主题一致
- 所有改动均可通过“改 Tokens”实现（Web 分钟级见效），组件逻辑与 API 不应因此改变
- 截图/录屏留存，确保可回溯

注意事项
- 仅覆盖语义/组件层变量；禁止直接覆盖原始/物理值（如 #fff、16px）
- 若发现必须新增“组件层令牌”，先在 docs 中提交“令牌增量草案”，获批后再加入源
- 两列对照必须使用同一份组件实现，确保差异仅来自 Tokens

交付物
- /components 页面新增 CompareSection 与组件对照卡片（后续开发任务）
- 调参结果的“变量覆盖清单”与“截图/录屏证据”
- 批量回填 Tokens 的 MR（开发阶段）

小结
- 该方案把“好不好看”的判断转化为可视化的 A/B 对照，且所有调整尽量在 Tokens 层完成，满足“先有再调整、调整容易”的目标。
