# Implementation Plan

[Overview]
修复“刷新后顶部区域 Chips 与下方 A→Z 列表复选框不同步”的不一致问题。根因是两套区域标识 id（后端 raw.id 与前端生成的 suburb_${name}/postcode_${code}）并存，导致 isSelected 按 id 比较失败，表现为：顶部有标签，列表不勾选；再点列表只影响“后端 id”条目，顶部标签不消失。方案：在进入前端状态前强制规范化（canonicalization）区域实体，任何来源（接口/回退/URL）一律生成稳定 id，并在 Store/组件内使用该稳定 id 做增删查对比，确保三处入口（Chips/列表/搜索结果）一致。

[Types]  
类型系统只引入本地工具定义，统一生成稳定 id。

- interface AreaNormalized
  - id: string                  // 'suburb_${name}' | 'postcode_${code}'
  - type: 'suburb' | 'postcode'
  - name: string                // suburb 名或邮编字符串
  - postcode?: string
  - fullName: string            // 展示名，如 'Ashfield NSW 2131' 或 '2131'
  - …raw                        // 透传原始字段（如 postcode 节点的 suburbs 聚合）

- function canonicalizeArea(raw: any): AreaNormalized
  - name 提取：raw.name/raw.suburb/raw.label → fallback ''
  - postcode 提取：raw.postcode/raw.code/raw.postcode_str → 4 位字符串
  - type 判定：优先原始 type；否则识别 4 位数字邮编 → postcode，否则 suburb
  - id 生成：postcode → `postcode_${code}`；suburb → `suburb_${name}`
  - fullName：suburb → `${name} NSW ${postcode}`（若有）；postcode → `${code}`

- function canonicalIdOf(a: any): string
  - 返回规范 id；若 a.id 已是规范形式直接复用，否则先 canonicalize 再取 id

[Files]
以最小改动修改 2 个现有文件，新增 1 个工具文件。无删除/移动。

- 新增
  - vue-frontend/src/utils/areas.js
    - 导出 canonicalizeArea, canonicalIdOf, isSameArea（按规范 id 比较）

- 修改
  - vue-frontend/src/stores/properties.js
    - import { canonicalizeArea, canonicalIdOf } from '@/utils/areas'
    - getAllAreas(): 在写入缓存前对 list 做 canonicalize，确保缓存即为规范 id
    - setSelectedLocations(): 对入参做 canonicalize + Map(id) 去重
    - addSelectedLocation(): canonicalize 后按 canonicalId 判重
    - removeSelectedLocation(): 按 canonicalId 删除，避免“异构 id”残留
  - vue-frontend/src/components/AreasSelector.vue
    - 使用 utils/areas 替换本地 normalize；在 displayName/filteredAreas/grouped/areaKey/isSelected/toggle/ensureAreasLoaded 中全量基于 canonicalizeArea/canonicalIdOf
    - 删除冗余 normalizeArea（避免 ESLint 报“已定义未使用”）

- 不需改动（观测保持一致）
  - FilterPanel.vue / filter-panels/AreaFilterPanel.vue：它们通过 store.selectedLocations 与 AreasSelector 交互，store 已保证规范化

[Functions]
只增加工具函数与替换对比/增删逻辑；无破坏性删除。

- 新函数
  - utils/areas.js
    - canonicalizeArea(raw)
    - canonicalIdOf(a)
    - isSameArea(a, b)

- 修改函数
  - properties.js
    - getAllAreas → 规范化缓存
    - setSelectedLocations/addSelectedLocation/removeSelectedLocation → 规范化 + 去重/按规范 id 操作
  - AreasSelector.vue
    - displayName/filteredAreas/grouped/areaKey/isSelected/toggle/ensureAreasLoaded → 统一使用规范对象与规范 id

- 移除函数
  - AreasSelector.vue: normalizeArea（已被 utils 替代）

[Classes]
无类（组合式 API/Pinia），无需改动。

[Dependencies]
无三

[Testing]
- 刷新后 URL 恢复：顶部 Chips 与列表勾选同步
- 接口成功/失败回退两种路径一致（可清缓存/断网验证）
- 同一 suburb 反复勾/取消，Chips 和复选框同步变化
- 仅选择 postcode 的通路不受影响（store 已做 postcode→suburbs 展开）
- PC/移动端、搜索框联动、A→Z 分组滚动可用

[Implementation Order]
1. 新增 utils/areas.js 并导出 canonicalizeArea/canonicalIdOf/isSameArea
2. properties.getAllAreas() 写缓存前 canonicalize
3. set/add/removeSelectedLocation 入口规范化 + 去重（按规范 id）
4. AreasSelector 全量改用规范 id 比对
5. 人工测试与无障碍验证
6. npm run lint && npm run format

[task_progress]
- [x] 步骤1：新增 src/utils/areas.js 并实现 canonicalizeArea/canonicalIdOf/isSameArea
- [x] 步骤2：在 stores/properties.js 的 getAllAreas() 写缓存前对列表做 canonicalize
- [x] 步骤3：为 setSelectedLocations/addSelectedLocation/removeSelectedLocation 增加规范化与去重
- [x] 步骤4：重构 components/AreasSelector.vue 使用 utils/areas；统一 isSelected/areaKey/toggle 逻辑
- [ ] 步骤5：测试刷新/接口与回退两条路径、URL 恢复、PC/移动、Chips/列表/搜索三处交互
- [x] 步骤6：npm run lint 和 npm run format 通过
- [ ] 步骤7：提交代码并在 PR 中记录“规范化区域 id 方案与回滚路径”
