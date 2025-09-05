# 筛选功能现状审计与差异清单（Filter V1 → V2 过渡基线）
ID: AUDIT-FILTER-2025-09-05  
最后更新: 2025-09-05  
范围：仅文档，无代码改动。目标是对齐 DOC-FILTER-PLAN 与 Memory Bank 原则，为后续小步实现提供事实依据与风险清单。

---

## 0) 结论速览（P0 差异）
- 参数命名不一致（需映射层统一）
  - 现状：`minPrice/maxPrice/suburb`、`bedrooms` 为 CSV 字符串（含 `4+`），`bathrooms/parking` 支持 `any/3+`，`isFurnished`；未实现 `sort`
  - 方案：对齐白名单参数（`suburbs,date_from,date_to,price_min,price_max,bedrooms,page,page_size,sort`），用映射函数统一前端状态 → API 参数（见后续规范文档）
- 计数接口复用列表接口（性能注意）
  - 现状：`getListWithPagination({ ...filters, page:1, page_size:1 })` 通过 `pagination.total` 获取总数
  - 风险：在高并发/大数据时可能放大压力；可保留但需关注 p95
- 图标库不一致
  - 现状：`FilterPanel.vue` 头部关闭按钮仍为 Font Awesome（`<i class="fa-solid fa-xmark">`）
  - 原则：统一使用 `lucide-vue-next`（系统模式要求）
- 错误策略偏“静默”
  - 现状：计数失败时直接置 `0`；UI 未 Toast 明确错误
  - 原则：快速失败 + 就近提示，禁止本地估算或静默降级

---

## 1) 组件与样式（FilterPanel.vue / src/style.css）
文件：`vue-frontend/src/components/FilterPanel.vue`  
现状：
- 筛选项（UI）
  - 价格：`el-slider`，0–5000/步长50；显示 `$min - $max` 或 `$min+`/`Any Price`
  - 卧室：单选（`1/2/3/4+`），内部状态为数组但仅保留1项
  - 浴室：单选（`any/1/2/3+`）；车位：单选（`any/0/1/2+`）
  - 日期：起止日期 `el-date-picker`（`YYYY-MM-DD` 格式化）
  - 家具：`el-switch`（仅传布尔）
- 行为与状态
  - `updateFilteredCount()`：通过 `store.getFilteredCount(filterParams)` 调后端计数（禁止本地估算）
  - `applyFilters()`：通过 `store.applyFilters(filterParams)` 服务端筛选，重置到第1页
- 参数键名（当前传参）
  - `minPrice/maxPrice/bedrooms/bathrooms/parking/date_from/date_to/isFurnished/suburb`
  - 区域来源：`propertiesStore.selectedLocations.map(loc => loc.name).join(',')`
- 样式与tokens
  - 主体样式引用 tokens：`var(--color-border-default) / var(--color-text-*) / var(--juwo-*)`
  - z-index：面板 2001，弹出层覆盖通过 `:deep(...popper){ z-index:10002 }` 处理
- 图标
  - 关闭按钮仍为 Font Awesome，违背“图标统一 lucide-vue-next”原则（系统模式）

文件：`vue-frontend/src/style.css`  
- tokens：`--juwo-primary/*`、`--color-text/*`、`--color-bg-*`、`--space-*`、`--text-*`、`--shadow-*` 已具备
- 布局：≥768/≥1200 断点与容器 padding 一致；全局 `overflow-x:hidden` 已移除（避免破坏 sticky）
- 注意：历史样式片段有少量重复块，不影响本次任务

---

## 2) 状态与数据流（Pinia Store）
文件：`vue-frontend/src/stores/properties.js`  
- 数据源：单一入口（组件收集输入 → 调用 store actions → API）
- 核心 actions
  - `fetchProperties(params)`：服务端分页（`/properties`），更新 `filteredProperties` 与 `pagination`
  - `applyFilters(filters)`：合并 `{ page:1, page_size:20, ...filters }` 后直调 `/properties`
  - `getFilteredCount(params)`：`{ ...params, page:1, page_size:1 }` 取 `pagination.total`
- 搜索与区域
  - `selectedLocations` 支持 `suburb/postcode` 两类建议；现仅将 `.name` 拼到 `suburb`（单数）参数中
- 错误策略
  - 失败时置 `error`，但组件侧计数失败显示为 `0`；缺少就近 Toast

符合原则：
- “组件仅负责触发 action，业务逻辑在 store 中处理”——符合
- “禁止前端本地降级/估算”——已移除本地估算逻辑，符合

---

## 3) API 与契约（api.js）
文件：`vue-frontend/src/services/api.js`  
- 基础：`/api` 代理；axios 15分钟内存缓存；统一响应期望 `{ status, data, pagination, error }`
- 列表：
  - `getList(params)`：默认 `page_size:20`，返回 `data`
  - `getListWithPagination(params)`：返回 `{ data, pagination }`
- 详情：`/properties/{id}`，使用缓存（30分钟后端 TTL 对齐）
- 位置建议：`/locations/...` 已封装
- 计数：无独立端点，复用列表接口 + `page_size:1`

参数映射差异（现状 vs 方案）：
- 区域：`suburb`（现状，单数） vs `suburbs`（方案，CSV）
- 价格：`minPrice/maxPrice`（现状，驼峰） vs `price_min/price_max`（方案，下划线）
- 卧室：CSV 字符串（含 `4+`） vs `bedrooms: number`（方案，建议最小值语义）
- 浴室/车位：`any/3+` 这类表达需要转成数值+语义（`min`），方案列为 P1/2
- 排序：未传 `sort`；方案提供 `rent_asc|rent_desc|date_asc|date_desc`
- 家具：`isFurnished` 非方案 P0 字段（可作为扩展字段 `furnished`，默认不传）

---

## 4) 性能与缓存
- 前端缓存：15分钟内存缓存（相同 `url + params`）  
  风险：筛选参数频繁变化导致缓存命中率低；过期值在 TTL 内返回可能造成“计数/列表”与后端不一致的短期现象
- 列表 p95 目标：≤ 800ms（DOC-FILTER-PLAN §6）；计数复用列表接口需观察实际负载

---

## 5) 用例与覆盖（抽样校验）
- 多区域 OR、跨字段 AND：组件可构造；需要映射为 `suburbs=CSV`
- 日期闭区间（含结束日）：组件 `YYYY-MM-DD` 输出，符合
- 价格/卧室/排序/分页组合：UI 已有（排序 UI 尚未接入）
- 空/错：无本地降级；需 Toast 就近提示（后续实现）

---

## 6) 风险清单
1) 参数契约不一致  
- 现状：驼峰 + 单参数名（`suburb/minPrice/...`）  
- 风险：后端白名单解析可能直接忽略，造成“筛选看似生效但实际未过滤”  
- 缓解：新增“映射函数 + 白名单”，统一为方案参数名

2) 计数复用列表  
- 现状：`page_size=1` 取 `total`  
- 风险：在高并发/复杂过滤时影响 p95  
- 缓解：保留但观察；必要时新增专用 count 端点或轻量聚合

3) 图标系统不一致  
- 现状：Font Awesome 残留  
- 风险：风格不统一、体积浪费  
- 缓解：后续小步替换为 `lucide-vue-next`

4) 错误反馈不足  
- 现状：计数失败置 0  
- 风险：误导用户“无结果”  
- 缓解：后续接入 Toast/Message，显示“筛选失败”

5) 位置类型混杂  
- 现状：`selectedLocations` 既含 suburb 又含 postcode  
- 风险：当前仅拼 suburb 名称；与用户期望可能不一致  
- 缓解：P0 仅传 suburb；postcode 另起参数（如 `postcodes`，P1/2）

---

## 7) 回滚策略
- 保留 V1 直传参数逻辑（组件 → store → API），在映射层后插  
- 用特性开关 `enableFilterV2` 控制是否启用新映射  
- 异常时关闭开关，回到 V1 参数直传

---

## 8) 建议与下一步（不改代码）
- 生成《参数映射规范》文档（本审计的配套输出）
  - 定义 filterState → API 的白名单映射与类型约束
  - 约定 `bedrooms` 的“下限”语义以支持 `4+`
  - 明确 `suburbs` 仅取 `type==='suburb'` 的 `name`
  - 定义删除空值/空串的规则
- 实施阶段（获批后）
  - 在服务层或 store 增加映射函数；最小改动、不破坏现有功能
  - 接入 `sort` 与 Toast 错误提示
  - 逐步替换 Font Awesome → lucide-vue-next

注：本页仅记录“事实与差异”，不触发代码变更。
