# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-09-06

---

## 1. 当前技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia
- **后端**: Python FastAPI + Strawberry GraphQL + Supabase (AWS悉尼区域)
- **数据库**: PostgreSQL (Supabase) + Redis缓存（默认 15 分钟 TTL；详情端点 /api/properties/{id} 为 30 分钟）
- **地图**: OpenStreetMap（底图）+ 后端 Google Directions（生产）+ Haversine（测试回退）

---

## 2. 项目架构概览

### 项目结构
```
vue-frontend/
├── src/views/          # 页面组件 (Home.vue, PropertyDetail.vue等)
├── src/components/     # 可复用组件 (PropertyCard.vue, Sidebar.vue等)
├── src/stores/         # Pinia状态管理 (properties.js, auth.js)
├── src/services/       # API服务层 (api.js)
├── src/router/         # Vue Router配置
└── vite.config.js      # Vite配置 (CORS代理到localhost:8000)
```

### JUWO品牌设计系统
- **主色**: #FF5824 (橙色)
- **统一圆角**: 6px（组件设计令牌）
- **标准房源卡片**: 580px宽度
- **布局对齐**: 1200px最大宽度，32px间距

### API集成架构
- **代理配置**: 默认将`/api`转发到 `http://localhost:8000`；在 WSL/容器环境可通过环境变量 `VITE_API_TARGET` 切换为 `http://172.31.16.1:8000`
- **拦截器**: 自动携带JWT认证头（按需启用；已具备框架基础）
- **响应格式**: 统一`{status, data, pagination, error}`结构
- **失败策略**: 前端已移除 testMode 与本地估算降级；当后端异常时快速失败并抛错，便于监控定位

---

## 3. 性能优化成果 🎯

**多项性能突破**:

1. **虚拟滚动优化**: DOM节点减少99.8% (17万+ → ~400)，列表加载提升83%
2. **API响应加速**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库索引**: 筛选查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存策略**: 15分钟客户端缓存 + Redis降级到内存缓存
5. **数据传输**: API字段优化减少70%响应体积

---

## 4. 开发环境

```bash
# Vue前端开发环境
cd vue-frontend
npm run dev              # localhost:5173

# 后端API服务
cd ../
python scripts/run_backend.py  # localhost:8000
```

**当前运行状态**:
- ✅ Vue前端: 正常运行 (虚拟DOM + 响应式系统)
- ✅ Python后端: 正常运行 (FastAPI + GraphQL)
- ✅ 数据库连接: 正常 (3456条示例数据；会随导入更新)
- ✅ CORS代理: 配置完成
- ✅ 地图服务: OpenStreetMap备选
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: 后端 Google Directions（生产）+ Haversine 回退；前端无本地估算

---

## 已解决的技术债务 ✅

**核心问题修复**:
- 用户认证体系完整 (注册/登录/邮箱验证)
- Google Places API完全替代方案 (本地存储/pre设数据)
- Redis依赖降级 (内存缓存备选)
- API响应格式统一 (description字段问题)
- 服务端分页完整迁移
- 代码注释规范建立
- PC 详情页风格一致性：统一背景/容器/内边距；替换硬编码为全局 tokens；在 src/style.css 补齐缺失变量映射

## 样式系统更新（2025-09-03）

- 在 `src/style.css` 的 `:root` 补充变量映射：`--space-1-5`, `--space-3`, `--space-3-5`, `--space-4`, `--space-6`, `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--font-semibold`, `--bg-base`, `--bg-hover`, `--bg-secondary`, `--radius-full`, `--shadow-xs`, `--brand-primary`, `--text-primary`, `--text-tertiary`, `--link-color`，与 JUWO 全局设计系统对齐。
- 在 `PropertyDetail.vue` 统一使用全局 tokens：如 `var(--color-bg-page)`, `var(--color-text-*)`, `var(--color-border-default)`；移除未定义变量（如 `--transition-all`）以避免回退。
- 统一 ≥1200px 与 1920px 断点的容器规范（`max-width: 1200px`, `padding: 0 32px`），与首页 Home 栅格一致，消除“另一套主题”观感。

### PropertyDetail 布局实现摘要
- 选择器基线：.property-detail-page .content-card 及其分区（description-section、map-section 等）
- 断点：
  - ≥1200px：启用 453px 左缘、496px 右缘的主版心计算；容器全宽布局
  - ≥1920px：仅对 .description-section p 应用 max-width: var(--paragraph-measure, 68ch)
- 关键计算：
  - margin-left: calc(453px - var(--section-padding-x, 50px))
  - margin-right: calc(496px - var(--section-padding-x, 50px))
- 分隔线伪元素：left/right = var(--section-padding-x, 50px)，保证与正文内边距对齐
- 不影响区域：Hero 顶部大图、<1200px 移动端布局
- 潜在风险/注意：
  - 若后续修改 --section-padding-x，需同时验证分隔线、标题与卡片边缘是否仍一致
  - 长段落 measure 仅对 p 生效，富文本内其他块级元素（如 ul/ol、表格）如需限制应另行评估

---

## 运行与集成增补（2025-09-06）

- 搜索框内嵌筛选入口（SearchBar.vue / HomeView.vue）
  - 在 el-input 的 suffix 内嵌 sliders-horizontal SVG（16×16，stroke: currentColor），颜色使用 var(--color-text-secondary) 与搜索 icon 一致；
  - 绝对定位相对 .el-input__wrapper：right: var(--search-suffix-right, 12px); top: 50%; transform: translateY(-50%);
  - wrapper 右侧 padding-right 使用令牌化计算：calc(var(--search-suffix-right, 12px) + var(--search-suffix-hit, 32px))，避免占位符/文本被覆盖；
  - 交互：button 语义 + aria-label="筛选"，点击 emit('openFilterPanel') 打开统一 FilterPanel；移除 clearable；
  - HomeView 监听 openFilterPanel 并隐藏 FilterTabs（v-if=false），维持“筛选入口单一”。

- 移动端房源卡片 full-bleed（PropertyCard.vue）
  - @media (max-width: 767px) 下：width/max-width:100vw；左右 margin: calc(50% - 50vw) 实现贴边；border-radius:0；
  - 高度不变：图片容器与轮播容器保持 250px，object-fit: cover；桌面端不受影响。

- 后端列表接口修复（backend/main.py）
  - 移除 /api/properties 列表查询中的 cover_image 字段（数据库 schema 无此列），解决 500 错误，保证分页/筛选稳定。

- 设计令牌（新增/约定）
  - --search-suffix-right: 12px（后缀右间距）
  - --search-suffix-hit: 32px（后缀命中区域宽高，可收紧为 24–28px）

## 运行与集成增补（2025-09-05）

- 变更文件与路径
  - src/stores/properties.js：引入参数映射层（mapFilterStateToApiParams），统一 applyFilters/getFilteredCount 入参；分页/排序透传；性能埋点
  - src/components/FilterPanel.vue：URL Query 同步（读写）；错误 Toast（ElMessage）；文案 i18n（$t）；suburbs/postcodes 区分；挂载期作用域修复
  - src/components/FilterTabs.vue：触发器模式（仅 emit('toggleFullPanel', true) 打开面板），隐藏所有下拉/预设；移动端/桌面端统一入口
  - src/components/SearchBar.vue：撤回移动端“筛选”按钮（仅保留搜索）
  - src/views/HomeView.vue：FilterTabs 在移动端也渲染；统一绑定 @toggleFullPanel ↔ FilterPanel v-model
  - src/i18n/index.js：轻量 i18n 插件（无依赖），默认 zh-CN，提供 $t 与 inject('t')
  - src/main.js：挂载 i18n（app.use(i18n)）
- 特性开关
  - enableFilterV2 = false（默认关闭，零风险回滚）；开启后输出 V2 契约参数（suburbs/price_min/price_max/bedrooms/...），并可扩展 furnished/bathrooms_min/parking_min/postcodes 等
- URL 状态同步
  - 应用筛选后写入 URL；进入页面时从 URL 恢复（刷新/直链可复现）
  - 仅写入非空参数；写入前做幂等判断，避免 replace 循环
  - 支持 suburbs 与 postcodes 两类 CSV 参数
- 错误处理
  - 快速失败 + 就近 Toast；移除本地估算与静默置 0，所有数据以后端返回为准
- 性能观测
  - fetchProperties / applyFilters / getFilteredCount 超过 800ms 打印 [FILTER-PERF] 警告，用于观察 p95 并驱动后续优化（如轻量 count 端点或索引）
- 其它注意
  - FilterPanel 关闭图标改为内联 SVG，统一走 SVG 路线（后续全站逐步迁移至 lucide-vue-next）
