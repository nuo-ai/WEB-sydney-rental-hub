# 当前上下文与紧急焦点

**最后更新**: 2025-09-05

---

2025-09-05｜DOCS-ALIGN｜对齐 Memory Bank：更新 /api/directions 为“后端 Google Directions（生产）+ Haversine 回退”，统一详情缓存 30min；纯文档，无代码改动

## 当前项目运行状态

### 服务状态

- ✅ Vue前端: `http://localhost:5173` - 虚拟DOM + 响应式系统
- ✅ Python后端: `http://localhost:8000` - FastAPI + GraphQL
- ✅ 数据库连接: 正常
- ✅ 后端API密钥: `GOOGLE_MAPS_API_KEY` 已在 `.env` 文件中正确配置 (2025-09-04)
- ✅ **通勤时间计算**: P0/P1 修复已于 2025-09-04 验证通过，前端正确调用后端 API。

---

## 当前无阻塞问题

所有核心功能均按预期运行。

---

## 下一步行动 (Next Action)

**目标**: 总结误差来源并撰写最终报告。

**操作**:
1.  总结Top 5误差来源，并与Google Maps行为进行对比。
2.  撰写最终报告，包含摘要、证据链、P0/P1/P2修复方案和实施清单。

### 计划中（未来开始，非优先）

1. **[国际化] 引入i18n框架**: 集成 `vue-i18n`，并将 `ProfileView.vue` 和 `PropertyDetail.vue` 中的硬编码中文抽离。
2. **[组件化] 抽象核心组件**: 将 `PropertyCard.vue` 中的按钮、标签等元素抽象为可复用的基础组件。
3. **[样式] 统一设计令牌使用（已完成 2025-09-03）**: 已集中改造 `PropertyDetail.vue`，将关键硬编码颜色/边框/过渡替换为全局 tokens（`var(--color-text-*)`, `var(--color-border-default)` 等），并将页面背景统一为 `var(--color-bg-page)`；全局 `src/style.css` 补齐详情页引用但缺失的设计令牌（如 `--space-*`, `--bg-*`, `--shadow-xs` 等），统一 ≥1200px 下容器宽度与左右 32px 内边距。

---

## 开发提醒

### 代码质量

- **注释规范**: 遵循CODE_COMMENT_RULES.md - 只解释原因，不解释结果
- **文档维护**: 每次主要变更后更新相关 memory-bank 文件
- **API接口**: 参考API_ENDPOINTS.md确认接口格式和字段名称

### 调试套件

- **终端测试**: 使用 `curl` 检查API端点和响应格式
- **浏览器工具**: 使用Vue DevTools检查Pinia状态和组件渲染
- **数据库检查**: 使用postgresql控制台验证查询性能
- **缓存控制**: 测试环境可调用 `/api/cache/invalidate` 进行选择性失效（仅测试/管理员上下文启用）

---

## 技术债务清理进度 (更新于2025-09-04)

### ✅ 已解决的核心问题

- [X] **通勤时间计算不准确**: 通过配置后端API密钥(P0)和移除前端静默降级(P1)修复。 (2025-09-04)
- [X] **看房时间数据持久化**: 通过补全详情接口返回 inspection_times 并更新后端 Property 模型，刷新后也能保留。
- [X] 用户认证和地址持久化完整实现
- [X] Google Places API替代方案建立
- [X] Redis依赖转为可选，内存缓存备选
- [X] API响应格式统一，字段命名规范化
- [X] 前后端分页完整迁移至服务端
- [X] 虚拟滚动性能优化，节点数量减少99.8%
- [X] 数据库索引自动优化，提升查询性能
- [X] **PC 详情页风格一致性**: 统一页面背景/容器宽度/左右内边距；用全局设计令牌替换硬编码颜色/边框/过渡，补齐缺失 CSS 变量映射（`src/style.css`）。
- [任务#TBD] 修复详情页 description 正文未按 Markdown 排版：在 PropertyDetail.vue 使用 MarkdownContent 渲染，保留展开/收起与样式（影响 PC/移动端），待用户验收
- 2025-09-04 | Task t4 | PropertyDetail 布局：桌面端正文左缘 453px、右缘距页面 496px，地图右缘与描述右缘对齐；≥1920px 仅限制描述段落行长为 --paragraph-measure(默认 68ch)；Hero 大图不受影响。Ref: t1,t2,t3,t4（commit: 待填）
- 2025-09-04｜ICON-UNIFY-20250904｜commit de033c4｜图标统一：PropertyCard 操作区、PropertyDetail 特征区；按钮容器 28×28 内图标 22px；下拉菜单图标 16px（8px 左右间距）；后续处理地址重复显示
