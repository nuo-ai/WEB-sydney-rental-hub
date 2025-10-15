# 当前工作快照（apps/web-shadcn · PropertyDetail 重建与蓝图抓取）

更新时间：2025-10-15 06:02 AEST

一、已完成（快照）
- Tabs 组件家族落地并接入 PDP Details（可访问性符合，aria/data-state），详见 progress.md「2025-10-15｜Tabs 组件家族 + 详情页集成」
- TS 类型/别名基础修复（env.d.ts + include），详见 progress.md「2025-10-15｜类型与别名修复」
- 结构蓝图初版已生成（web_fetch），视觉度量待补，详见 progress.md「2025-10-15｜蓝图抓取（初版）」

二、仍存在的问题（需下一步处理）
- vue-tsc 构建出现大量 “找不到模块 '@/lib/utils' / '@/components/ui/*'” 报错
  - 可能原因：tsconfig.app 未显式继承 baseUrl/paths，或 references 构建读取不到根 tsconfig 路径映射
  - 另有 “Cannot find module 'markdown-it' 类型声明”
- MCP 浏览器工具暂失败，已用 web_fetch 回退产出 raw 蓝图，但缺少视觉度量

三、下一步（P0，小步补丁）
注：里程碑细节统一记录于 progress.md；activeContext 仅保留当前快照与下一步。
1) TS 别名与类型修正
   - 在 tsconfig.app.json 补充 compilerOptions.baseUrl="." 与 paths["@/*"]=["./src/*"]（保证 vue-tsc -b 引用时可见）
   - 安装并声明类型：@types/markdown-it 或临时在 env.d.ts 增加 declare module 'markdown-it'
2) 组件缺口继续补齐（批次 A 起）
   - DatePicker/Calendar、Sheet/Drawer、Select/Combobox、Tooltip/Popover/Dropdown、Progress/Spinner、Label/Form 等
3) 视觉蓝图补全
   - 待浏览器 MCP 恢复：对 1440/1024/390 注入探针，生成 tokens-suggestion.json（colors/radius/shadows/spacing/typography/layout）与截图基线
4) PDP 增强（对齐 Domain 节奏）
   - Schools/Transport（Tabs+Table）、Inspections（DatePicker+Sheet）、分享/收藏（Dropdown/Tooltip），移动端 Sticky CTA（无头实现）

四、关键文件
- apps/web-shadcn/src/components/ui/tabs/*（新增 Tabs 组件家族 + index.ts）
- apps/web-shadcn/src/views/PropertyDetail.vue（Details 卡片内集成 Tabs）
- apps/web-shadcn/tsconfig.app.json / src/env.d.ts（类型与别名修复）
- docs/blueprints/domain/.../blueprint-raw.json（结构蓝图初版，待补视觉 Tokens）

五、工作方式（保持）
- token-first + 蓝图先行（结构与度量）→ 有头/无头 80/20 组合落地
- 小步快跑、replace_in_file/精确写入；与 legacy 完全解耦
- 先完成 P0 页面要素，再接数据与跨端映射

六、补充快照（2025-10-15 08:33 AEST）
- req-2「Domain PDP 蓝图探针」进展：
  - task-8 页面级 tokens 与 3 断点视口截图 → Approved
  - task-9 hero_gallery 元素截图 + 容器尺寸（1440≈1425×506.34）→ Approved
  - task-10 summary_card 三断点元素截图 + 容器尺寸（1440=659×170）→ Approved
- 受限与策略：
  - Chrome MCP 截图 fullPage 存在限流（MAX_CAPTURE_VISIBLE_TAB_CALLS_PER_SECOND）
  - CSP/扩展隔离导致 computedStyle 抽取不稳定
  - 采取“占位 → 回填”策略：先落可靠度量（容器宽高/截图），其余字段置 null 待补，避免错误数据入库
- 交付与路径：
  - 三档元素截图已落 Downloads 并写入 JSON 绝对路径；如需纳入仓库，请手动移动到 docs/blueprints/domain/<slug>/... 后，我再将路径改为相对路径（遵守文件系统规则）
- 下一步（P0）：
  - 继续 task-11 features：定位 selector → 三档元素截图 → modules/features.json 占位与关键度量
  - 与产品确认 summary_card 回填路径优先级：自动定点采集（可行则先）或半自动（依据截图核对，确保“参数不遗漏”）
