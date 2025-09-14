# Backend API 端点文档（最新版）

最后更新：2025-09-15  
框架：FastAPI + Strawberry GraphQL  
基础URL：http://localhost:8000

---

目录
- 系统端点
- 房源API（REST）
- 位置/区域API（REST）
- AI聊天API
- 任务API（Celery）
- GraphQL端点
- 错误与返回体约定
- 环境变量
- 测试与回归（QA-001）

---

## 系统端点

### GET /
描述：根端点，返回服务状态
```json
{ "message": "Rental MCP Server is running. Access GraphQL at /graphql" }
```

### GET /api/health
描述：健康检查
```json
{ "status": "ok" }
```

### GET /test_db_connection
描述：检查数据库连接依赖是否正常注入
```json
{ "status": "ok", "db_type": "<class 'psycopg2.extensions.connection'>", "has_cursor": true }
```

---

## 房源API（REST）

### GET /api/properties
描述：获取房源列表（支持筛选、分页、排序）。返回统一响应体 APIResponse：
```json
{
  "status": "success",
  "data": [ { ...房源字段... } ],
  "pagination": {
    "total": 123,
    "page": 1,
    "page_size": 20,
    "pages": 7,
    "has_next": true,
    "has_prev": false,
    "next_cursor": null
  }
}
```

缓存：15分钟（缓存键包含完整URL，避免 page/page_size 污染）

当前支持的查询参数（V1 契约白名单）
- 筛选
  - suburb: string（支持 CSV，大小写不敏感 ILIKE；示例 "Zetland,Surry Hills"）
  - property_type: string（ILIKE）
  - bedrooms: string（CSV+下限语义，示例 "1,2,4+" → (==1 OR ==2 OR >=4)）
  - bathrooms: string（CSV+下限语义，示例 "3+" → >=3）
  - parking: string（CSV+下限语义，示例 "2+" → >=2；字段名对应 parking_spaces）
  - minPrice: number（rent_pw >= minPrice）
  - maxPrice: number（rent_pw <= maxPrice）
  - date_from: YYYY-MM-DD
  - date_to: YYYY-MM-DD
    - 口径：当 date_from <= today 时，包含 available_date IS NULL（Available now）；未来区间不包含 NULL
  - isFurnished: boolean（true/false，仅当显式传入时筛选；兼容历史 text/三态；不会把 "unknown" 当 true/false）
  - furnished: boolean（等价于 isFurnished，便于兼容）
  - listing_id: string（点名过滤，便于校验/复现）
- 分页/游标
  - page: int >=1（页码，从1开始）
  - page_size: int [1,100]（REST 内部上限100；前端 Store 默认 ≤50）
  - cursor: string（base64 的 listing_id；与排序未深度耦合，P0 简化版）
- 排序（白名单值，仅允许以下四种）
  - sort: "price_asc" | "available_date_asc" | "suburb_az" | "inspection_earliest"
  - 兜底：listing_id ASC（稳定次序键）

安全与一致性
- 始终 is_active = TRUE（排除下架房源）
- OR/下限条件均参数化占位 %s + params.extend(...)，杜绝字符串拼接注入
- 计数口径与列表使用同一 WHERE+params（REST 内部手动拼接；GraphQL 使用统一构建器）

错误与拦截（BE-002）
- 未知过滤键：HTTP 400 + 明确错误体
- 非白名单 sort 值：HTTP 400
- 示例（未知键 foo 与非法 sort 值 "price"）
```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid query parameters",
    "details": {
      "unknown_keys": ["foo"],
      "allowed_keys": [
        "bathrooms","bedrooms","cursor","date_from","date_to",
        "furnished","isFurnished","listing_id","maxPrice","minPrice",
        "page","page_size","parking","property_type","sort","suburb"
      ],
      "invalid_values": {
        "sort": { "got": "price", "allowed": ["available_date_asc","inspection_earliest","price_asc","suburb_az"] }
      }
    }
  }
}
```

请求示例
```bash
# 基础分页
curl "http://localhost:8000/api/properties?page=1&page_size=20"

# 区域 ILIKE + 价格区间 + 卧室 OR/下限 + 排序
curl "http://localhost:8000/api/properties?suburb=Zetland,Surry%20Hills&minPrice=600&maxPrice=1200&bedrooms=2,4+&sort=price_asc"

# 仅日期下限（包含 Available now）
curl "http://localhost:8000/api/properties?date_from=2025-09-01"

# 家具（true/false）
curl "http://localhost:8000/api/properties?isFurnished=true"

# 点名过滤（用于校验）
curl "http://localhost:8000/api/properties?listing_id=123456"
```

前端表现（关键说明）
- “应用（N）/确定（N）”稳定：快速操作不会回跳旧值；关闭面板后不再“幽灵计数”（前端 useFilterPreviewCount 并发守卫+防抖+卸载清理）
- 失败降级：计数失败返回 null 时，按钮退回“应用/确定”，不误显示“0 条”
- 仅选邮编：前端将 postcode 展开为多个 suburb（V1 兜底），确保 N 与应用后列表总数一致
- URL 幂等：仅写非空有效键；刷新/直链可恢复当前筛选

### GET /api/properties/{property_id}
描述：获取单个房源详情（缓存 30 分钟）  
响应：APIResponse[data=完整房源对象]  
不存在时：404 + RESOURCE_NOT_FOUND

---

## 位置/区域API（REST）

### GET /api/locations/suggestions
描述：输入模糊匹配，返回 suburb/postcode 建议及数量；缓存 15 分钟

### GET /api/locations/all
描述：返回全量去重的 suburb 列表 + postcode 聚合（含其下属 suburbs 预览）；缓存 15 分钟

### GET /api/locations/nearby?suburb=Zetland&limit=6
描述：基于固定映射 + 数据回退，返回附近区域建议；缓存 15 分钟

---

## AI聊天API

### POST /api/chat
描述：AI 聊天助手（房源/法律/合同/服务多路由）；返回 ChatResponse

---

## 任务API（Celery）

- POST /api/tasks/debug（调试任务）
- POST /api/tasks/db（示例 DB 任务）
- GET /api/tasks/{task_id}（查询任务状态，成功/失败）

---

## GraphQL端点

### POST /graphql
- 支持：properties、property、universityCommuteProfile、propertiesNearLocation 等
- GraphiQL：/graphql

说明
- GraphQL 的列表/计数口径由构建器 `_build_where_and_params_for_properties`（backend/crud/properties_crud.py）统一生成 WHERE+params，保证数据查询与计数查询一致。

---

## 错误与返回体约定

统一响应体（APIResponse）
- 成功
```json
{ "status": "success", "data": {...}, "pagination": {...} }
```
- 失败
```json
{ "status": "error", "error": { "code": "BAD_REQUEST", "message": "...", "details": {...} } }
```

常见错误码
- BAD_REQUEST：参数无效（BE-002 未知键/非法 sort）
- RESOURCE_NOT_FOUND：资源不存在
- VALIDATION_ERROR：Pydantic 校验失败
- INTERNAL_SERVER_ERROR：内部错误
- RATE_LIMIT_EXCEEDED：频率限制

---

## 环境变量

- DATABASE_URL
- REDIS_URL
- ENVIRONMENT（development/production）
- FRONTEND_URL, ADDITIONAL_CORS
- SECRET_KEY（JWT 预留）
- GOOGLE_MAPS_API_KEY

---

## 测试与回归（QA-001 最小可检清单）

目标
- “列表 total 与分页累加一致”（统一口径）
- 排序白名单、未知键 400（BE-002）
- 点名过滤稳定性

用例位置
- tests/api/test_properties_filters.py（pytest + requests）

运行
```bash
# 先确保后端服务运行在 http://localhost:8000
# 可通过环境变量覆盖：BACKEND_BASE_URL=http://localhost:8001

pytest -q tests/api/test_properties_filters.py
```

断言要点
- 对相同 filters：page_size=1 的 pagination.total = 累加各页 items 总和
- sort=price_asc/available_date_asc/suburb_az/inspection_earliest 返回 200；其他值 400
- 未知键（如 foo=bar）返回 400（错误体含 unknown_keys 与 allowed_keys）

---

变更记录（与此文档相关）
- 2025-09-15
  - BE-002：对 /api/properties 增加查询参数白名单校验与排序值白名单；未知键/非法 sort 返回 400（error_response）
  - 文档对齐：参数名对齐代码（minPrice/maxPrice、date_from/date_to 等），补充错误体样例与 QA-001 运行说明
- 2025-01-24 初稿
