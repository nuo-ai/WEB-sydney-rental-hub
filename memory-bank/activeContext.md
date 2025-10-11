# 当前上下文与焦点
**最后更新**：2025-10-11

## 当前焦点 (Current Focus)
- 建立“可视化设计 Token 工具站”，实现所有 Token 的直观渲染与可视化调参，并形成“导出 JSON/SCSS → 回填 uni.scss → 多端一致”闭环。
- 先完善文字系统（中/英文家族、字重、字距、文本级别），同步扩展颜色/间距/阴影/圆角/图标与按钮尺寸等基础维度。

## 刚完成的工作 (Latest)
- 新建 Astro 工具站（tools/design-site-astro）
  - 页面：`/` 导航、`/tokens` 实时调参与导出 JSON/SCSS、`/components` 多状态卡片画廊。
  - 数据：`public/tokens/srh.json` 初始 Token（涵盖颜色/间距/比例/圆角/阴影/文本/字重/字距/级别等）。
  - 脚本：根级新增 `astro:dev/build/preview`；workspace 纳入 `tools/*`。
- 文字系统 Token 落地
  - 在 `apps/uni-app/src/uni.scss` 增加 `$srh-font-family-zh/en`、字重、字距、XS~XL 文本级别，并桥接为 `:root --srh-*`（H5 可运行时微调，小程序静态生效）。
  - Astro `/tokens` 与 `/components` 已应用字体/字重/字距变量，预览即时响应。
- uni-app 侧可视化
  - 新增 `pages/tokens/preview.vue` 预览页并在首页添加入口；支持 H5 端运行时调参与导出 JSON。

## 下一步行动 (Next Actions · P0)
1) “所有 Token 直观渲染”完善：
   - `/tokens` 页面增加专属可视化区：
     - 颜色色板（对比强/中/弱、语义/状态色）、间距标尺、圆角/阴影示例、图标/按钮尺寸对比、密度预设（紧凑/默认）。
   - `/components` 增加更多状态用例（hover/active/disabled/badge 变体）。
2) realestate 英文字体对齐：在 `/tokens` 的 `fontFamilyEN` 粘贴其完整 font-family 栈，确认字形与节律；回填 uni.scss。
3) 导出闭环增强：提供“导出→回填 uni.scss”清单提示与一键覆盖脚本（文档/脚本优先，谨慎自动写）。
4) 小程序真机校验：验证字体回退链与字距/行高在常见设备的表现，必要时微调中文家族优先级。

## 重要提醒/约束 (Constraints)
- 小程序端不支持运行时 `setProperty`，仅静态构建；H5 端支持运行时微调（`--srh-*`）。
- 字体可用性依赖设备/系统，英文与 realestate 对齐以“字体栈优先级”非“强制安装”实现。

## 相关命令 (Ops)
- 启动工具站：`pnpm astro:dev`（http://localhost:4321）
- 导出后回填：复制 `/tokens` 的 SCSS 片段至 `apps/uni-app/src/uni.scss` 的 `$srh-*`。
