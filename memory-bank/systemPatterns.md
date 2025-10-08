# 系统设计模式与最佳实践

---

## 核心架构原则

### Monorepo 架构
- **方案**: `pnpm` Workspaces + `Turborepo`
- **结构**: 所有应用（前端、后端等）均存放在 `apps/*` 目录下。
- **目标**: 统一依赖管理、共享工具链、高效任务编排（通过根目录的 `package.json` 和 `turbo.json`）。
- **原则**: 新功能或应用应作为新的 `apps/` 子目录加入工作区，以继承现有配置。

### 数据流架构
```bash
# 核心数据流路径 (必须遵守)
Browser (Vue @ :5173) → Vite Proxy → Python Backend (@ :8000)
```

**禁止** ❌: AI Agent直接调用前端或其他反向依赖
**原因**: 引入脆弱中间层，增加延迟，隐藏真正的错误源

### 前端架构
- **组件框架**: Vue 3 (Composition API)
- **状态管理**: Pinia (单一数据源原则)
- **路由系统**: Vue Router (SPA架构)
- **UI库**: Element Plus (JUWO主题定制)

---

## 保存搜索功能模式

### 事件驱动架构
- **模式**: 组件间事件发射链路 `SaveSearchModal` → `FilterTabs` → `HomeView`
- **实现**: Vue `emit()` 系统，确保事件正确传递和处理
- **用户反馈**: 保存成功后立即显示 `ElMessage.success()` 提示

### 智能命名策略
- **算法**: 基于筛选条件自动生成有意义的搜索名称
- **格式**: "区域名称 + 房型 + 价格范围 + 特殊条件"
- **示例**: "Ashfield 等 3 个区域 2房 $400-800" 或 "Burwood 有家具房源"

### 本地存储管理
- **存储**: localStorage 作为第一阶段实现
- **结构**: JSON 数组，包含 id/name/conditions/locations/createdAt 等字段
- **扩展性**: 为后续云端同步预留接口设计

---

## 筛选系统核心模式

### URL 幂等与状态同步
- **模式**: 最终写入点清洗 + 幂等对比
- **实现**: `sanitizeQueryParams` 过滤空值键，`isSameQuery` 比较新旧查询
- **效果**: 应用后 URL 可直链/刷新恢复，不写空键，地址栏不抖动

### 预估计数统一
- **composable**: useFilterPreviewCount 统一"应用（N）"口径
- **特性**: 并发序号守卫、300ms 防抖、组件卸载清理
- **降级**: 计数失败返回 null，按钮退回"应用/确定"

### 分组边界隔离
- **API**: `applyFilters(filters, { sections })`
- **原则**: 仅删除指定分组旧键再合并，避免跨面板覆盖
- **分组**: area/price/bedrooms/availability/more

---

## CSS与布局模式

### 布局对齐策略
- **统一容器**: `max-width: 1200px` 和 `padding: 0 32px`
- **双层结构**: 外层容器全宽背景 + 内层居中内容区
- **响应式断点**: 768px（平板）、1200px（桌面）、1920px（超宽）

### 设计令牌约束
- **强制使用**: `var(--*)` 形式的 CSS 自定义属性
- **禁止**: 硬编码颜色、`var(--token, #hex)` 兜底形式
- **护栏**: Stylelint 规则拦截新增硬编码色

### 分段控件（Segmented）模式
- **目的**: 数字/枚举按钮视觉连体，仅改几何关系
- **实现**: 相邻无缝、端部圆角 2px、边框折叠
- **约束**: 不覆写颜色/状态逻辑，沿用既有设计令牌

---

## 状态管理原则

### 单一数据源
- **原则**: 组件负责触发action，业务逻辑在store actions中处理
- **反模式** ❌: 在action中混合传入参数和未同步的旧state

### 特性开关模式
- **V1→V2演进**: 映射函数 + 特性开关，默认关闭新契约
- **回滚保障**: enableFilterV2=false，任何异常可一键回退

---

## API 设计与契约一致性

### 端点字段一致性
- **原则**: 详情端点应为列表端点的"超集"（superset）
- **避免**: 刷新或直链访问出现字段缺失导致的 UI 回退
- **缓存策略**: 提供选择性失效端点，避免旧缓存污染

### 统一响应格式
- **结构**: `{status, data, pagination, error}`
- **建议**: 契约单元测试校验字段一致性

---

## 图标系统与组件化

### 统一图标库
- **标准**: 迁移进行中——以 `lucide-vue-next` 为标准，允许少量 Font Awesome 遗留（待清理）
- **导入**: `import { IconName } from 'lucide-vue-next'`
- **使用**: `<IconName class="spec-icon" />`
- **颜色**: `stroke: currentColor`，由外层控制

### 规格行变量驱动
- **全局变量**: --spec-icon-size/--spec-text-size/--spec-line-height/--spec-icon-gap/--spec-item-gap
- **结构类**: .spec-row/.spec-item/.spec-text
- **原则**: 统一"图标 + 数字"信息行的尺寸与间距

---

## 经验教训总结

- **CSS全局影响**: 全局 `overflow-x: hidden` 会破坏 `position: sticky`
- **滚动判断差异**: 移动端和桌面端需要隔离的滚动处理逻辑
- **布局统一**: 容器对齐不一致会导致视觉错位
- **状态同步**: 异步action中参数与state的不一致会导致数据错误
