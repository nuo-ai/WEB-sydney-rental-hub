# 筛选功能与面板升级技术方案 v1.0
ID: DOC-FILTER-PLAN-2025-09-05
最后更新: 2025-09-05

本文为“仅文档”变更，不涉及代码改动。目标是在不破坏现有功能的前提下，明确筛选系统的契约、交互与实施路径，为后续小步实现提供依据。

---

## 1) 概述

- 目标：在现有“区域自动补全 + 日期范围筛选”的基础上，统一筛选数据流、API 契约与样式约束，支持性能可控的服务端筛选与分页。
- 范围：前端 FilterPanel 交互与状态流、/api/properties 查询参数规范、验收与风险；不引入新依赖，不改动后端非必要逻辑。
- 非目标：不实现本地数据估算/降级（已在通勤模块移除）；不做大规模 UI 重构；不引入复杂聚合查询。

---

## 2) 现状审计清单（实施前必须完成）

请按以下清单审计现状，仅记录差异与风险（不修改代码）：
- 组件与样式
  - src/components/FilterPanel.vue：筛选项、校验、触发事件、tokens 使用情况（禁止硬编码颜色/阴影/间距）。
  - src/style.css：是否具备所需设计令牌；容器与断点（1200px、左右 32px）是否统一。
- 状态与数据流
  - src/stores/properties.js（或等价 store）：筛选 state 结构、actions 参数与 API 调用映射；分页与排序的默认值。
  - URL 状态同步（可选）：是否已有 query 同步（P1 才考虑）。
- API 与契约
  - src/services/api.js：/api/properties 参数拼装与错误处理；确保“快速失败”，不做静默降级。
  - 后端契约核对：列表/详情字段一致性（详情为列表超集），新增字段优先在详情补齐，再评估列表返回。
- 性能与缓存
  - 服务端分页（页大小、排序）与前端虚拟滚动的协作关系。
  - 缓存策略与失效（Redis/内存；是否需要选择性失效端点参与调试）。

输出：一页审计记录（diff 摘要 + 风险列表）。

---

## 3) 方案设计

### 3.1 筛选项与交互（P0 基线）
- 区域（suburbs）
  - 交互：自动补全 + 多选标签（符合 Product “可选择一个或多个区域”的叙述）。
  - 语义：多区域为“或”关系（OR），与其他条件“且”关系（AND）。
- 可入住日期范围（available_date）
  - 交互：起止日期范围；“包含结束日”语义（便于入驻当天）。
  - 语义：闭区间 [from, to]，服务端以日期（不含时分秒）比较。
- 价格（rent_pw）
  - 交互：min/max 滑块或输入框；默认不限。
- 卧室（bedrooms）
  - 交互：单选（系统一致性：“单选逻辑 + 服务端筛选”）。
- 其他（P1/2）：浴室、停车位、物业类型等，延后。

可访问性：控件有 aria-label；按 Tab 顺序合理；标签可键盘移除。

### 3.2 API 契约与查询参数（/api/properties）
- 查询参数（草案）
  - suburbs: CSV 字符串（URL 编码），例如 `suburbs=Zetland,Sydney,Waterloo`
  - date_from: ISO-8601（yyyy-mm-dd）
  - date_to: ISO-8601（yyyy-mm-dd）
  - price_min: number
  - price_max: number
  - bedrooms: number
  - page: number（默认 1）
  - page_size: number（默认 20；上限 50，防止过载）
  - sort: 枚举（rent_asc | rent_desc | date_asc | date_desc）
- 规则
  - 空/缺省参数不参与过滤；服务端做白名单解析，避免注入。
  - 多区域 OR，跨字段 AND。
  - 结果结构统一：`{ status, data, pagination: { page, page_size, total }, error }`
- 示例
  - `GET /api/properties?suburbs=Zetland,Sydney&date_from=2025-07-01&date_to=2025-07-15&price_min=600&bedrooms=1&page=1&page_size=20&sort=rent_asc`

### 3.3 前端状态流（单一数据源）
- 组件（FilterPanel）只负责收集输入、触发 store actions；不做本地过滤。
- Store（properties）
  - state: `filterState`, `list`, `pagination`, `loading`, `error`
  - actions: `applyFilters(payload)`, `fetchList()`, `resetFilters()`
  - 映射：`filterState → api.js 参数` 有统一函数，便于回收与测试。
- 错误策略：请求失败直接抛错 + UI Toast；禁止静默降级或本地估算。

### 3.4 UX 与样式约束（统一到 tokens）
- 容器：max-width 1200px；padding: 0 32px；断点 768 / 1200 / 1920。
- 令牌：仅使用 src/style.css 中 tokens（color/bg/space/shadow/text/radius 等）；缺失先在 :root 声明再用。
- 交互反馈：loading/empty/error 三态就近展示；一致的卡片骨架屏（如适用）。

### 3.5 性能与缓存
- 分页：严格服务端分页；前端虚拟滚动继续启用（不依赖一次性拿全量）。
- 缓存：短 TTL（例如列表 15min）；筛选参数变化直接绕过命中；测试可用选择性失效端点。
- 防御：page_size 上限；参数校验；慢查询观察（后端索引另行管理）。

---

## 4) 任务拆解与优先级

- P0（本迭代必须）
  1. 审计现状并出差异清单（文档）。
  2. 固化“查询参数契约 + 参数映射函数签名”（文档级别）。
  3. 验收标准与用例清单（见 §6）。
  4. 风险与回滚策略（特性开关 + 还原路径）。
- P1（次迭代）
  1. URL query 同步（分享/刷新可复现）。
  2. 筛选项的 i18n 文案抽离（与全站 i18n 一致）。
- P2（规划）
  1. 扩展筛选（浴室/停车/物业类型）。
  2. 最近搜索/常用筛选模板（本地存储）。

---

## 5) 风险与回滚

- 契约不一致：列表/详情字段差异导致 UI 回退。
  - 缓解：先补详情，再评估列表；加入后端契约快照测试。
- 缓存污染：更改契约后旧缓存未失效。
  - 缓解：测试环境使用选择性失效；变更期缩短 TTL。
- 参数爆炸：前端传参不规范导致后端负载飙升。
  - 缓解：白名单解析 + 上限（page_size）+ 指数退避重试（如必要）。
- 回滚：启用特性开关 `enableFilterV2`（默认 off）；出现问题时切回 V1（保留旧映射）。

---

## 6) 验收标准（抽样）

- 功能
  - 多区域 OR 生效；与其他条件 AND。
  - 日期范围闭区间；同一天 from=to 可命中。
  - 价格/卧室筛选与排序可组合；分页稳定。
- 数据与契约
  - API 响应结构与字段稳定，空结果与错误可区分。
  - 任何新字段优先在详情端点可见，列表端点评估后再加入。
- 性能
  - 列表接口 p95 ≤ 800ms（测试数据量下）；页面交互无明显卡顿。
  - DOM 节点维持在虚拟滚动既定规模（~400）。
- 稳定性
  - 参数非法时后端 4xx，前端 Toast 告知；无静默降级。

---

## 7) 字段契约清单（草案，用于后端快照测试）

关键字段（列表/详情一致；详情为超集）：
- listing_id, address, suburb, rent_pw, bedrooms, bathrooms, available_date, images, latitude, longitude
- inspection_times（案例字段：需在列表与详情保持一致性；如仅在详情，需文档标注）

---

## 8) 里程碑与输出

- M1（当天）：完成现状审计与本方案（本文）。
- M2：产出“参数映射与验收用例”文档页（或附录）。
- M3：小步落地（组件/Store/服务层），每次仅 1–2 个文件改动；跟随规则更新 Memory Bank。

---

## 附：示例请求

```
GET /api/properties?suburbs=Zetland,Sydney&date_from=2025-07-01&date_to=2025-07-15&price_min=600&bedrooms=1&page=1&page_size=20&sort=rent_asc
```

响应（示意）：
```json
{
  "status": "ok",
  "data": [ /* items */ ],
  "pagination": { "page": 1, "page_size": 20, "total": 3456 },
  "error": null
}
```

---

注：
- 全文遵循 systemPatterns “API 设计与契约一致性”、tokens 与容器约束；不引入本地估算/降级。
- 任何实现性改动将另起任务，采用小步补丁（prefer replace_in_file），并先更新 activeContext 一行记录。
