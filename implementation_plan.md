# Implementation Plan

[Overview]
目标：将筛选组件提升到“成熟可用”的一致性标准，支持用户在“区域、卧室、浴室、车位、价格、家具（更多）”六个分组中任意顺序连续设置并“应用”，任何一次“应用”都仅影响本次涉及分组，其他已应用条件保持不变；“清空/取消”仅影响当前分组；顶部标签“颜色+文案”和列表结果仅在“应用”后更新；样式严格遵循 design token；URL 同步与刷新后的状态恢复正常。

为此，我们以“Store 分组级合并 + draft/applied 双态 + 顶部标签文案生成规则 + URL 同步”统一口径。PC 分离式和移动端统一面板共享同一数据层策略，确保跨端一致。

[Types]  
本项变更不引入外部类型系统；在 Pinia Store 中规范内部结构字段与语义。

- State（Pinia / properties.js）
  - selectedLocations: Location[]（已应用区域）
  - draftSelectedLocations: Location[]（区域草稿）
  - currentFilterParams: Record<string, string|number|boolean>（所有分组的“已应用”请求参数合集）
  - previewDraftSections: Record<sectionKey, PartialParams & { __mark?: true }>
  - sort: string
  - page/page_size: number

- 分组键管理（键与分组的映射关系）
  - SECTION_KEY_MAP（已存在，并作为全局真源）
    - area: ['suburb','suburbs','postcodes','include_nearby']
    - price: ['minPrice','maxPrice','price_min','price_max']
    - bedrooms: ['bedrooms']
    - availability: ['date_from','date_to']
    - more: ['isFurnished','furnished','bathrooms','bathrooms_min','parking','parking_min']

- Draft/Applied 语义
  - draft*：面板内临时编辑与预览计数（getPreviewCount），不影响顶部文案与列表。
  - applied：selectedLocations + currentFilterParams；顶部文案与列表依赖“已应用”。
  - URL：仅在“应用”后写入已应用参数，刷新后能复现。

[Files]
本次工作主要“修复与加固”现有实现，文件清单如下。

- 新增文件
  - /implementation_plan.md（当前文档）

- 已修改文件（已完成的改动需回归验证）
  - vue-frontend/src/stores/properties.js
    - applyFilters：新增“分组级合并”逻辑（推断触达分组→清理 base→合并 mapped→请求→写回 currentFilterParams）
    - getFilteredCount：与 applyFilters 口径一致（日期/价格/邮编展开/白名单）
    - draftSelectedLocations 家族 API：setDraft/resetDraft/applySelectedLocations/hasAreaDraftDiff
    - SECTION_KEY_MAP：集中管理分组键映射
  - vue-frontend/src/components/FilterPanel.vue（移动端统一面板）
    - 区域使用 draftSelectedLocations；应用时 applySelectedLocations；预览计数走草稿；关闭时丢弃草稿
  - vue-frontend/src/components/filter-panels/AreaFilterPanel.vue（PC 分离式“区域”）
    - 同 FilterPanel 的区域草稿逻辑；应用/取消流程及草稿清理
  - vue-frontend/src/components/FilterTabs.vue（PC 顶部标签）
    - 文案基于“已应用”，移除未应用小蓝点；样式走 design token；moreApplied/moreTabText 忽略 'any'，保留 0 的有效值

- 需要核查/加固（若不满足需补丁）
  - vue-frontend/src/components/filter-panels/PriceFilterPanel.vue
  - vue-frontend/src/components/filter-panels/BedroomsFilterPanel.vue
  - vue-frontend/src/components/filter-panels/AvailabilityFilterPanel.vue
  - vue-frontend/src/components/filter-panels/MoreFilterPanel.vue
  - 核查点：
    - 预览计数阶段：updatePreviewDraft(section)、getPreviewCount()
    - 应用阶段：仅提交本分组参数；区域先 applySelectedLocations() 再 applyFilters()
    - 取消/关闭：清理草稿 clearPreviewDraft(section) / resetDraftSelectedLocations（区域）
    - URL 同步与恢复仅针对“已应用”的 currentFilterParams

[Functions]
函数清单与具体要求如下。

- Store（properties.js）
  - 新增/已存在（需保留）
    - setDraftSelectedLocations(list: Location[])
    - resetDraftSelectedLocations(): void
    - applySelectedLocations(): void
    - hasAreaDraftDiff(): boolean
    - updatePreviewDraft(section: string, partial: Record<string,any>): void
    - clearPreviewDraft(section: string): void
    - markPreviewSection(section: string): void
  - 修改（已完成）
    - applyFilters(filters: PartialParams)
      - 逻辑：mapFilterStateToApiParams → base = currentFilterParams → 推断触达分组（SECTION_KEY_MAP）→ 从 base 删除该分组键 → merged = { ...base, ...mapped } → 清空空值 → 请求 → currentFilterParams = merged
      - 补齐 page/page_size/sort；只在“应用”后写入 URL（组件负责）
    - getFilteredCount(params: PartialParams)
      - 保持与 applyFilters 同一映射口径，避免预览与实际不一致
- 组件（各分组面板）
  - 预览：updatePreviewDraft(section)、getPreviewCount()
  - 应用：仅提交本分组参数；区域先 applySelectedLocations() 再 applyFilters()
  - 取消/关闭：resetDraftSelectedLocations()/clearPreviewDraft(section)

[Classes]
本次不涉及 class 的新增/修改/删除（Vue SFC + Pinia 为主）。

[Dependencies]
不新增第三方依赖；样式严格使用既有 design token；移除“胶囊”样式与自定义 color-mix；维持 Element Plus 等现有依赖。

[Testing]
采用“矩阵化回归 + 可选组件单测（如已配置）”。

- PC 分离式面板矩阵（任意顺序交叉）
  1) 区域→价格→更多→卧室→可入住→车位：每次“应用”仅影响本分组，前次分组保持不变
  2) 在任一分组“清空并应用”：仅清此分组；其它分组保持
  3) any/0 边界：bathrooms='any' 不触发已应用；parking_min=0 有效（如需特殊展示另议）
  4) 价格单边：≥min 或 ≤max；跨分组叠加不互斥
  5) URL 同步：应用后刷新页面，筛选可还原；分页/排序与筛选并用
- 移动端统一面板：
  - 一次设置多个分组并“确定”：应全部生效；下一次设置其它分组不覆盖已应用
- 样式/文案：
  - 顶部标签文案“首项 +N”；严格 design token；仅应用后更新

[Implementation Order]
实施顺序与回归路径如下（最小风险顺序）。

1) Store 合并逻辑（已完成）→ 确认 SECTION_KEY_MAP 全覆盖键  
2) 各面板预览/应用/取消流程一致性复核（Price/Bedrooms/Availability/More）  
3) 顶部标签文案与高亮规则核查（忽略 'any'，保留 0；中英混排；仅应用后更新）  
4) URL 同步与恢复：仅写入已应用；刷新后能还原  
5) 手工矩阵回归（PC/移动端）  
6) 记录调试日志与重要断言（仅开发环境可见）；清理后保留必要 Debug 开关
