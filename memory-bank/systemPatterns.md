# 系统设计模式与最佳实践

---

## 核心架构原则

### Monorepo 架构
- **方案**: `pnpm` Workspaces + `Turborepo`
- **结构**: 所有应用（前端、后端等）均存放在 `apps/*` 目录下。
- **目标**: 统一依赖管理、共享工具链、高效任务编排（通过根目录的 `package.json` 和 `turbo.json`）。
- **原则**: 新功能或应用应作为新的 `apps/` 或 `packages/` 子目录加入工作区。

---

## 设计系统模式 (Design System Patterns)

### 1. 设计令牌分层架构 (Token Tiering)
- **核心原则**: 设计令牌必须遵循“原始 → 语义 → 组件”的三层架构，确保系统的可维护性与主题化能力。
  - **原始层 (Primitives)**: 物理值，如 `#0A0A0A`、`16px`。源自 `tokens/base/*.json`。
  - **语义层 (Semantic)**: 角色与意图命名，如 `--color-bg-page`、`--text-contrast-strong`。引用原始层。
  - **组件层 (Component)**: 特定组件的参数，如 `--button-primary-bg`。引用语义层。
- **实现**:
  - 原始/物理值定义在 `tokens/base/*.json`。
  - 语义/组件令牌在 `apps/web/src/styles/design-tokens.css` 中定义，并引用原始值。
  - 暗色主题 (`theme-dark.css`) **仅能**覆盖语义层令牌。
- **反模式** ❌:
  - 组件直接消费原始令牌 (`var(--gray-900)`)。
  - 在组件样式中出现任何硬编码的样式值（如 `#FFF`, `16px`）。

### 2. 自动化令牌管道 (Automated Token Pipeline)
- **模式**: 设计令牌通过自动化的构建流程，转换为前端可直接消费的多种代码格式。
- **实现**: `Style Dictionary` 工具链负责读取 `tokens/**/*.json` 并生成 CSS 自- **价值**: 确保设计变更可以安全、一致地同步到所有前端应用，杜绝手动修改和遗漏。

### 3. 独立的组件开发环境与单一事实来源
- **模式**: 设计规范和 UI 组件在一个与业务应用完全隔离的环境中进行开发、测试和文档化，形成项目的“单一事实来源”。
- **实现**: `@sydney-rental-hub/ui` 包内置 **Storybook** 作为核心开发工具，它不仅是组件的可视化“画廊”，也是设计规范的实时文档。
  - **设计规范 (Foundations)**: 通过 MDX 文件 (`Colors.mdx`, `Typography.mdx` 等) 可视化展示所有设计令牌。
  - **组件 (Components)**: 为每个组件编写独立的 stories，展示其所有变体、尺寸和状态。
- **原则**: 所有基础组件的开发和迭代都应在 Storybook 中优先进行。组件在 Storybook 中必须表现完美，才能被主应用消费。这强制实现了组件的上下文无关性和高复用性。

### 4. 组件消费原则
- **原则**: 组件**必须**优先消费语义令牌 (`--color-text-primary`) 或组件令牌 (`--button-primary-bg`)。
- **禁止**: 组件直接消费原始令牌 (`var(--gray-900)`)。
- **理由**: 保证组件能够自然地响应主题切换（如暗色模式），并与设计系统的意图保持一致。

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

### Uni-app 子应用模式（Monorepo）
- **位置与结构**: 子包位于 `apps/uni-app`，基于 Vite+Vue3 的 uni-app 官方模板。
- **组件库接入**: 统一使用官方 uni-ui；通过 `pages.json` 的 easycom 规则开启自动解析：
  - `"^uni-(.*)": "@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue"`
- **运行与构建**（通过 pnpm workspace）:
  - H5 开发：`pnpm --filter ./apps/uni-app run dev:h5`
  - 其他平台（示例）：`pnpm --filter ./apps/uni-app run dev:mp-weixin`
- **依赖恢复手册**: 出现安装异常（如 EPERM）：
  1) 删除根 `node_modules`；2) 在根执行 `pnpm install`；3) 子包内按需 `pnpm --filter ./apps/uni-app add <pkg>`。
- **第三方组件原则**: 优先官方 uni-ui；严格按 easycom 使用，避免手动 import/注册；平台差异通过条件编译隔离。

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

### 4. 布局与样式模式

#### 布局对齐策略
- **统一容器**: `max-width: 1200px` 和 `padding: 0 32px`
- **双层结构**: 外层容器全宽背景 + 内层居中内容区
- **响应式断点**: 768px（平板）、1200px（桌面）、1920px（超宽）

#### 设计令牌约束
- **强制使用**: `var(--*)` 形式的 CSS 自定义属性。
- **禁止**: 硬编码颜色、`var(--token, #hex)` 兜底形式。
- **护栏**: Stylelint 规则 (`.stylelintrc.json`) 已配置为拦截任何新增的硬编码样式值。
- **文字系统**:
  - **字号**: 优先使用 `--text-sm/base/lg/xl` 等语义字号。
  - **颜色**: 必须使用 `--text-contrast-strong/medium/weak` 别名来控制文本的视觉层级。
  - **行高**: 必须使用 `--line-height-title/body/ui` 场景化行高，以确保垂直节律一致。

#### 分段控件（Segmented）模式
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

### 5. 图标系统模式

#### 统一图标库
- **标准**: 以 `lucide-vue-next` 为标准图标库。
- **封装**: 图标应被封装为独立的组件，以便统一管理和使用。
- **颜色**: 图标颜色必须使用 `stroke: currentColor`，使其能够继承父元素的文字颜色 (`color`)，从而可以通过 Design Tokens 进行控制。

#### 规格行变量驱动
- **全局变量**: --spec-icon-size/--spec-text-size/--spec-line-height/--spec-icon-gap/--spec-item-gap
- **结构类**: .spec-row/.spec-item/.spec-text
- **原则**: 统一"图标 + 数字"信息行的尺寸与间距

---

## 经验教训总结

- **CSS全局影响**: 全局 `overflow-x: hidden` 会破坏 `position: sticky`
- **滚动判断差异**: 移动端和桌面端需要隔离的滚动处理逻辑
- **布局统一**: 容器对齐不一致会导致视觉错位
- **状态同步**: 异步action中参数与state的不一致会导致数据错误
