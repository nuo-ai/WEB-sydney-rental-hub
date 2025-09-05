# Filter V2 参数映射规范（前端状态 → /api/properties 查询参数）
ID: SPEC-FILTER-PARAM-MAPPING-2025-09-05  
最后更新: 2025-09-05  
范围：仅文档（不改代码）。用于指导后续小步实现；与 DOC-FILTER-PLAN v1.0、Memory Bank“API 契约一致性”原则对齐。

---

## 1) 目标与边界
- 目标：统一筛选参数命名、类型与语义，消除 V1 中的驼峰/单数混用，支持“多区域 OR、跨字段 AND、闭区间日期、服务端分页与排序”。
- 不做：本地估算/降级；大规模 UI 重构；一次改动多文件。  
- 回滚：采用特性开关 `enableFilterV2`，关闭时回落到 V1 直传参数。

---

## 2) 白名单参数（后端 /api/properties）
- suburbs: string（CSV，URL 编码）示例 `Zetland,Sydney,Waterloo`（仅取 type===suburb 的 name；去重、保持输入顺序）
- date_from: string（ISO-8601 yyyy-mm-dd）
- date_to: string（ISO-8601 yyyy-mm-dd）——闭区间 [from, to]
- price_min: number（每周租金，最小值；单位 AUD）
- price_max: number（每周租金，最大值；单位 AUD）
- bedrooms: number（最小卧室数，支持 4+ → 4）
- page: number（默认 1）
- page_size: number（默认 20，上限 50）
- sort: enum（`rent_asc | rent_desc | date_asc | date_desc`；不传则使用后端默认）

扩展（P1/2，非本迭代必须）
- furnished: boolean（源于前端 `isFurnished`）
- bathrooms_min: number（`any` 省略；`3+` → 3）
- parking_min: number（`any` 省略；`3+` → 3）
- postcodes: string（CSV，当 selectedLocations 含 type===postcode 时使用；P1）

删除规则
- 空/缺省参数不参与过滤：null/undefined/'' 直接移除  
- 价格区间边界：当 `price_min === 0`、`price_max === 最大滑轨值(5000)` 时省略该边界

---

## 3) 前端状态来源（当前实现现状）
- FilterPanel.vue（当前值）
  - priceRange: [min:number, max:number]（0..5000，步长 50）
  - bedrooms: string[]（['1'|'2'|'3'|'4+']，单选但保存为数组）
  - bathrooms: string[]（['any'|'1'|'2'|'3+']，单选）
  - parking: string[]（['any'|'1'|'2'|'3+']，单选）
  - startDate/endDate: Date|null（格式化为 yyyy-mm-dd）
  - isFurnished: boolean
- Store：`properties.selectedLocations: { id, type: 'suburb'|'postcode', name, ... }[]`

---

## 4) 映射规则（V2 目标语义）
- 区域（suburbs）
  - 输入：`selectedLocations.filter(l => l.type === 'suburb').map(l => l.name)`
  - 输出：`suburbs=CSV`（去重、保序）
  - 语义：多区域 OR；与其他条件 AND
- 日期（date_from/date_to）
  - 输入：`startDate/endDate`（Date|null）
  - 输出：`date_from/date_to`（yyyy-mm-dd）
  - 语义：闭区间 [from, to]；若 from 或 to 为空则按单边约束
- 价格（price_min/price_max）
  - 输入：`priceRange=[min,max]`（0..5000）
  - 输出：`price_min/price_max`；当 min=0 省略 `price_min`，max=5000 省略 `price_max`
  - 纠偏：若 min > max，交换两者（或直接抛错；推荐“纠偏为交换”，减少用户困惑）
- 卧室（bedrooms）
  - 输入：`bedrooms[0]`（'1'|'2'|'3'|'4+'|undefined）
  - 输出：`bedrooms=number`；'4+' → 4
  - 语义：最小卧室数（min semantics）
- 分页（page/page_size）
  - 输入：store/page 控件（默认 1/20）
  - 输出：直接传递，page_size 限制 1..50
- 排序（sort）
  - 输入：UI 控件（尚未接入时不传）
  - 输出：`rent_asc | rent_desc | date_asc | date_desc`（不传则用后端默认）
- 扩展（P1/2）
  - isFurnished → furnished（boolean）；true 则传，false 省略
  - bathrooms: 'any' 省略；'3+' → bathrooms_min=3；'1' → 1
  - parking: 同理 → parking_min

---

## 5) 兼容层与回滚（V1 → V2）
- 特性开关：`enableFilterV2`（默认 off）
  - off（V1 行为）：沿用现参名（`suburb/minPrice/maxPrice/...`），不改现有调用链
  - on（V2 行为）：启用上述映射（白名单 + 纠偏 + 删除空值）
- 发生异常：关闭开关，回落到 V1；日志记录“V2 参数构造失败”

---

## 6) 参考实现（伪代码，仅说明意图）
```ts
type FilterState = {
  priceRange: [number, number]
  bedrooms: string[]           // e.g. ['3'] | ['4+'] | []
  bathrooms: string[]          // e.g. ['any'] | ['2'] | ['3+'] | []
  parking: string[]            // e.g. ['any'] | ['1'] | ['3+'] | []
  startDate: Date | null
  endDate: Date | null
  isFurnished: boolean
}

type Location = { id: string; type: 'suburb'|'postcode'; name: string; [k: string]: any }

type Paging = { page?: number; page_size?: number; sort?: 'rent_asc'|'rent_desc'|'date_asc'|'date_desc' }

type MapOptions = { enableFilterV2: boolean }

function mapFilterStateToApiParams(
  filter: FilterState,
  selectedLocations: Location[],
  paging: Paging = {},
  opts: MapOptions
): Record<string, string | number | boolean> {
  if (!opts.enableFilterV2) {
    // V1 回退（示意）：保持现有键名，最小改动
    const legacy: any = {}
    const [min, max] = filter.priceRange ?? [0, 5000]
    if (min > 0) legacy.minPrice = min
    if (max < 5000) legacy.maxPrice = max
    if (filter.bedrooms.length) legacy.bedrooms = filter.bedrooms.join(',')
    if (filter.bathrooms.length) legacy.bathrooms = filter.bathrooms.join(',')
    if (filter.parking.length) legacy.parking = filter.parking.join(',')
    if (filter.startDate) legacy.date_from = fmt(filter.startDate)
    if (filter.endDate) legacy.date_to = fmt(filter.endDate)
    if (filter.isFurnished) legacy.isFurnished = true
    const suburbs = selectedLocations.filter(l => l.type === 'suburb').map(l => l.name)
    if (suburbs.length) legacy.suburb = suburbs.join(',')
    legacy.page = paging.page ?? 1
    legacy.page_size = Math.min(Math.max(paging.page_size ?? 20, 1), 50)
    if (paging.sort) legacy.sort = paging.sort
    return legacy
  }

  // V2 规范
  const params: any = {}
  // suburbs
  const suburbs = Array.from(new Set(
    selectedLocations.filter(l => l.type === 'suburb').map(l => l.name)
  ))
  if (suburbs.length) params.suburbs = suburbs.join(',')

  // date range
  if (filter.startDate) params.date_from = fmt(filter.startDate)
  if (filter.endDate) params.date_to = fmt(filter.endDate)

  // price
  let [min, max] = filter.priceRange ?? [0, 5000]
  if (min > max) [min, max] = [max, min] // 纠偏
  if (min > 0) params.price_min = min
  if (max < 5000) params.price_max = max

  // bedrooms（最小数）
  if (filter.bedrooms.length) {
    const b = filter.bedrooms[0] // 单选
    params.bedrooms = b.endsWith('+') ? parseInt(b) : parseInt(b) // '4+'→4
  }

  // paging/sort
  params.page = paging.page ?? 1
  params.page_size = Math.min(Math.max(paging.page_size ?? 20, 1), 50)
  if (paging.sort) params.sort = paging.sort

  // 扩展（P1/2，仅当启用才传）
  // furnished
  if (filter.isFurnished) params.furnished = true
  // bathrooms_min / parking_min 规则略（P1），'any' 省略，'3+'→3

  // 删除空值
  Object.keys(params).forEach(k => {
    if (params[k] === '' || params[k] === null || typeof params[k] === 'undefined') {
      delete params[k]
    }
  })
  return params
}

function fmt(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}
```

---

## 7) 验收用例（对齐 DOC-FILTER-PLAN §6）
功能
- 多区域 OR 与跨字段 AND 生效
- 日期闭区间（`from=to` 命中）
- 价格/卧室/排序/分页可组合；空/缺省不参与过滤

数据与契约
- 响应结构稳定 `{ status, data, pagination, error }`
- 新字段优先在详情端点补齐，再评估列表端点返回（契约一致性）

性能
- 列表接口 p95 ≤ 800ms（测试数据量）
- 计数复用列表接口（page_size=1）观察负载（保留但监控）

稳定性
- 参数非法（如 price_min>price_max）纠偏或抛错；前端 Toast 告知
- 禁止本地降级与静默失败

---

## 8) 示例映射
输入（FilterPanel + 选区）
```json
{
  "priceRange": [650, 900],
  "bedrooms": ["2"],
  "bathrooms": ["any"],
  "parking": [],
  "startDate": "2025-07-01",
  "endDate": "2025-07-15",
  "isFurnished": false
}
```
`selectedLocations = [{type:"suburb", name:"Zetland"}, {type:"suburb", name:"Sydney"}]`  
`paging = { page:1, page_size:20, sort:"rent_asc" }`

输出（V2）
```
GET /api/properties?suburbs=Zetland,Sydney&date_from=2025-07-01&date_to=2025-07-15&price_min=650&price_max=900&bedrooms=2&page=1&page_size=20&sort=rent_asc
```

---

## 9) 实施建议（小步、最小改动）
- 首次改动：在服务层（api.js）或 store（properties.js）添加纯函数 `mapFilterStateToApiParams(...)`；引入特性开关；其余调用不变
- 第二步：接入 `sort` 与错误 Toast（就近提示）
- 第三步：逐步将 Font Awesome 图标替换为 `lucide-vue-next`

---

## 10) 风险与回滚
- 契约不一致或后端白名单未更新 → 关闭 `enableFilterV2` 回滚到 V1
- 计数压力升高 → 观察 p95，必要时讨论增加轻量 `count` 端点
