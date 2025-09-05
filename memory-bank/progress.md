# 项目进展与演进

---

## 关键里程碑

### 2025年9月5日：图片计数器复刻与 ESLint 清理

- 主要成果：复刻图片计数器 Photos pill（min-width 118px、22×22 徽标、two-digits 胶囊、支持 99+），模板新增 two-digits 动态类以稳定多位数显示；清理 api.js 未使用函数，消除 ESLint no-unused-vars。
- 细节：
  - UI：容器 inline-flex 居中，背景 #fefefe、边框 #cfd1d7、文本 #3c475b、圆角 4px；数字使用 tabular-nums 防抖动；two-digits 时自动胶囊（padding: 0 4px, radius: 11px）。
  - 模板：当 images.length ≥ 10 添加 two-digits 类；99+ 场景显示“99+”。
  - 代码质量：移除 calculateDistance/estimateCommute/parseCoordinates，前端完全依赖后端 Google Directions。
- 影响与价值：保障视觉稳定并与历史“成功过”版本一致；前端通勤实现与后端契约一致，去除误导性本地估算路径。
- 溯源：activeContext 2025-09-05｜UI-PILL-COUNTER / API-CLEANUP

### 2025年9月5日：筛选入口统一（PC/Mobile）与入口回撤

- 主要成果：
  - PC 与移动端统一仅保留“筛选”一个入口。
  - FilterTabs 隐藏所有下拉/预设，仅作为“打开 FilterPanel”的触发器。
  - SearchBar 移动端撤回“筛选”按钮（SearchBar 仅负责搜索）。
  - HomeView 统一绑定 @toggleFullPanel ↔ FilterPanel v-model；移动端也渲染 FilterTabs 作为入口。
- 影响与价值：去除双通道与预设导致的状态不一致；交互对齐 Zillow 触发器模式；心智更简洁、回滚路径清晰。
- 向后兼容：旧直链 `parking=0` 视为 Any（不传）。
- 溯源：activeContext 2025-09-05｜UI-FILTER-ENTRY-UNIFY｜commit 6926962

### 2025年9月5日：筛选兼容与体验收束（V1→V2 基线）

- 主要成果：
  - 参数映射兼容层 + 特性开关 enableFilterV2（默认 off，零风险回滚）
  - 错误策略：快速失败 + 就近 Toast，移除本地估算/静默置 0
  - URL Query 同步：筛选应用→写入 query；onMounted→从 query 恢复（刷新/直链可复现）
  - i18n：FilterPanel 文案抽离到轻量 $t（默认 zh-CN），不引入外部依赖
  - postcodes 支持：前端区分 suburbs/postcodes，URL 与筛选参数双向透传
  - 性能埋点：计数/列表接口 >800ms 输出 [FILTER-PERF] 警告，便于观察 p95
  - 挂载期 bug 修复：propertiesStore 作用域问题导致 mounted 抛错，已通过显式入参与判空兜底修复
- 影响文件：src/stores/properties.js / src/components/FilterPanel.vue / src/i18n/index.js / src/main.js
- 溯源：activeContext 2025-09-05｜FILTER-EXPERIENCE-STACK｜commit d78d6def

### 2025年9月4日：通勤时间计算准确性问题修复

- **主要成果**: 彻底解决了通勤时间计算严重不准的问题。前端现在能够可靠地调用后端API，获取并展示来自Google Maps的真实、准确的通勤数据。
- **根因分析**:
  1. **P0 - API密钥缺失**: 后端 `.env` 文件中缺少 `GOOGLE_MAPS_API_KEY`，导致外部API调用失败。
  2. **P1 - 前端静默降级**: 前端 `api.js` 中存在“测试模式”下的静默降级逻辑，API调用失败时，系统会回退到一套不准确的本地估算算法，从而掩盖了后端错误。
  3. **P-dev - 开发环境缓存**: Vite开发服务器的缓存导致前端代码变更未能及时生效，延长了问题排查时间。
- **关键修复**:
  - **后端**: 在 `.env` 文件中正确配置了 `GOOGLE_MAPS_API_KEY`。
  - **前端**: 删除了 `api.js` 中的 `testMode` 开关、`estimateCommute` 本地估算函数及其相关的所有降级逻辑，确保API调用失败时会抛出明确错误。
- **验证手段**: 通过浏览器网络开发者工具，确认前端页面在计算通勤时间时，发起了对 `/api/directions` 的XHR请求，并收到了状态码为200的成功响应。
- **影响与价值**:
  - **准确性**: 通勤时间从误差高达50%-200%（基于本地估算）提升至与Google Maps官方结果一致。
  - **用户体验**: 用户可以获得可靠的通勤决策依据，显著提升产品信任度。
  - **系统可靠性**: 移除了错误的静默降级，使系统在遇到外部API问题时能够快速失败，便于监控和定位。
### 2025年1月30日：虚拟滚动性能优化
