# 筛选与计数专项一页纸（P0 版）

## 1. 目标与问题
- 统一口径：确保“列表 pagination.total”与按钮“应用（N）/确定（N）”一致。
- 防注入与契约稳定：消除字符串拼接风险，限制未知参数输入。
- 前端“预估 N”稳定：防止旧响应回写、避免“幽灵计数”，失败时合理降级。
- 可回滚：改动小步走，出现异常可快速回退。

## 2. 核心方案（后端/前端）
后端（FastAPI/psycopg2）
- 参数构建器模式（GraphQL 已接入）：`_build_where_and_params_for_properties(...) -> (where_sql, params)`，数据与计数共用条件，避免口径漂移。
- 参数化占位：OR/下限语义（如 bedrooms "4+" → bedrooms >= %s）全部使用 `%s` + `params.extend(...)`，无 f-string 拼接。
- REST 白名单（BE-002，/api/properties）：
  - 允许键：`suburb, property_type, bedrooms, bathrooms, parking, minPrice, maxPrice, date_from, date_to, isFurnished, furnished, listing_id, page, page_size, cursor, sort`
  - 排序白名单：`price_asc | available_date_asc | suburb_az | inspection_earliest`（兜底 `listing_id ASC`）
  - 未知键或非法 sort → HTTP 400，错误体包含 `unknown_keys/allowed_keys/invalid_values`
- 日期语义：`date_from <= today` 时包含 `available_date IS NULL`（Available now）；未来区间不包含 NULL。
- 始终过滤 `is_active = TRUE`。

前端（Vue3 + Pinia）
- 计数失败降级：`getFilteredCount/getPreviewCount` 失败返回 `null`（不再返回 0），按钮文案退回“应用/确定”，不误导为“0 条”。
- 可复用预估逻辑：`useFilterPreviewCount(section, buildDraftFn, { debounceMs=300 })`
  - 并发序号守卫：丢弃过期响应，防止旧结果回写（前端表现：N 不回跳）。
  - 防抖与卸载清理：减少请求风暴，避免“幽灵计数”。
  - 草稿聚合：分组删键后再叠加草稿，预估口径与应用一致。
- V1 契约兜底：仅选 `postcode` 时，展开为多个 `suburb` 注入 `suburb CSV`，保证 N 与列表一致。
- URL 幂等：仅写非空有效键，刷新/直链可恢复。

## 3. 数据流/口径统一（文字图）
用户操作 → 组件（各分面） → useFilterPreviewCount（并发守卫/防抖/草稿聚合） → Pinia Store（getPreviewCount → 构参） → REST /api/properties（白名单/参数化/共享 WHERE 条件）  
→ 后端计数：`page_size=1` 返回 `pagination.total` → 前端按钮“应用（N）/确定（N）”展示 N  
→ 用户点击应用 → Store 合并分组参数（删键+叠加）→ 列表请求 → pagination.total 与 N 一致

## 4. 错误与降级策略
- 网络/500：计数返回 `null`，按钮退回“应用/确定”，列表不清空；就近轻量提示（Toast/Inline）。
- 仅选 postcode：通过 `areasCache` 做 postcode→suburbs 映射展开（失败不阻塞列表）。
- REST 契约错误：未知键或非法 sort → HTTP 400（错误体含 `unknown_keys` 等），便于快速定位。

## 5. REST 契约（/api/properties）白名单
- 过滤：`suburb, property_type, bedrooms, bathrooms, parking, minPrice, maxPrice, date_from, date_to, isFurnished, furnished, listing_id`
- 分页/游标：`page, page_size, cursor`
- 排序（白名单）：`price_asc | available_date_asc | suburb_az | inspection_earliest`
- 兜底：`ORDER BY listing_id ASC`（稳定次序键）

## 6. 验收口径（前端表现）
- “应用（N）/确定（N）”不回跳旧值；关闭面板后无“幽灵计数”。
- 计数失败降级：返回 `null` → 按钮退回“应用/确定”，不误显示“0 条”。
- 仅选邮编：N 与应用后列表总数一致（V1 兜底展开）。
- URL 幂等：仅写非空有效键；刷新/直链可恢复。
- 排序/分页：排序白名单实际生效；非法值明确 400；分页与计数解耦。

## 7. 测试与回归（QA-001）
范围（最少集）：
- 区域（suburb/postcode/混合/仅 postcode）、价格（0/5000/区间/≥/≤）、卧室（0/4+）、浴室（any/3+）、车位（0/2+）
- 日期（包含/不包含 Available now）、家具（on/off）、URL 恢复、并发切换、卸载清理、失败降级、分页/排序白名单
用例位置：`tools/playwright/tests/api/test_properties_filters.py`（10 passed）
说明：为避免硬编码，suburb 从 `/api/locations/all` 动态选择。  
测试基座：`pytest.ini` 注册了 `timeout` 标记（建议搭配 `pytest-timeout` 插件）。

## 8. 发布与回滚（P0）
- 金丝雀发布（10%）：关注 p95、错误率、计数失败率；异常立即回滚。
- 回滚开关：关闭白名单校验、恢复旧参数写入策略、禁用新排序项、必要时回退上一个稳定 commit。

## 9. 示例
请求（价格+卧室下限+区域 ILIKE，排序）：
```bash
curl "http://localhost:8000/api/properties?suburb=Zetland,Surry%20Hills&minPrice=600&maxPrice=1200&bedrooms=2,4+&sort=price_asc&page=1&page_size=20"
```

错误体（未知键+非法 sort）：
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

## 10. 关联与溯源
- 后端：`backend/main.py`（REST 白名单/日期语义）；`backend/crud/properties_crud.py`（构建器）
- 前端：`apps/web/src/stores/properties.js`（失败降级/邮编兜底）；`apps/web/src/composables/useFilterPreviewCount.js`（并发守卫/防抖/卸载）
- 文档：`backend/API_ENDPOINTS.md`、`docs/roadmap/TASKS.md`
- 测试：`tools/playwright/tests/api/test_properties_filters.py`（10 passed）
- 最近提交：17527a4（参考）
