# 系统设计模式与最佳实践

---

## 核心架构原则

### 数据流架构 (Data Flow Architecture)
```bash
# 核心数据流路径 (必须遵守)
Browser (Vue @ :5173) → Vite Proxy → Python Backend (@ :8000)
```

**禁止** ❌: AI Agent直接调用前端或其他反向依赖
**原因**: 引入脆弱中间层，增加延迟，隐藏真正的错误源

---

## 前端架构

- **组件框架**: Vue 3 (Composition API)
- **状态管理**: Pinia (单一数据源原则)
- **路由系统**: Vue Router (SPA架构)
- **UI库**: Element Plus (JUWO主题定制)

---

## CSS与布局模式

### 1. 样式作用域
**模式** ✅: 将布局影响的CSS规则 (`overflow`, `position`, `display`) 限定在组件作用域内
**反模式** ❌: 对顶级元素 (`body`, `html`) 应用全局 `overflow-x: hidden`

### 2. 布局对齐策略
**模式** ✅: 统一 `max-width: 1200px` 和 `padding: 0 32px` 确保垂直对齐
**反模式** ❌: 不同容器的对齐方式不一致

### 3. 全宽内容设计
**模式** ✅: 双层结构实现：
- 外层容器: `width: 100%` (背景)
- 内层容器: 居中内容区

---

## 状态管理原则

**单一数据源**: 组件负责触发action，业务逻辑在store actions中处理

**反模式** ❌: 在action中混合传入参数和未同步的旧state

---

## 移动端响应式模式

### 1. 渐进式间距系统
匀速递增的间距级别：`8px → 12px → 16px`
从核心元素到区域再到容器的视觉层次递增

### 2. 移动端滚动逻辑隔离
桌面端 vs 移动端使用不同的滚动判断机制：
- **桌面端**: `getBoundingClientRect()` 视窗位置判断
- **移动端**: `offsetHeight` 实际DOM高度判断

### 3. 性能优化的高度计算策略
使用缓存的DOM高度信息而非实时计算，以避免强制布局重计算

### 布局与对齐
- 桌面端（≥1200px）正文容器不做水平居中，使用内容卡 .content-card 外边距计算实现精确对齐：
  - 左：margin-left = 453px - var(--section-padding-x, 50px)
  - 右：margin-right = 496px - var(--section-padding-x, 50px)
- 不在多处硬编码 453/496，统一以变量/计算表达，减少维护成本。
- 分隔线使用伪元素并锚定到正文内边距：left/right 以 var(--section-padding-x, 50px) 对齐。

### 文本可读性
- 超宽屏（默认 ≥1920px）对长段落仅限 p 的 measure（建议 68ch，可通过 --paragraph-measure 调整），不改变容器宽度与对齐，避免破坏地图/描述右缘一致性。

### 响应式与兼容
- <1200px 沿用移动端容器与内边距；Hero 大图始终全宽，自适应留白不受正文约束。
- 覆盖层样式优先级以“有限 !important + 更具体选择器”为主，控制影响范围。

### 变量化与可配置
- 关键变量：--section-padding-x（默认 50px）、--paragraph-measure（默认 68ch）。
- 调整对齐或行长时优先改变量，避免散点修改。
- 反模式** ❌: 不同容器的对齐方式不一致

---

## 状态管理原则

**单一数据源**: 组件负责触发action，业务逻辑在store actions中处理

**反模式** ❌: 在action中混合传入参数和未同步的旧state

---

## 移动端响应式模式

### 1. 渐进式间距系统
匀速递增的间距级别：`8px → 12px → 16px`
从核心元素到区域再到容器的视觉层次递增

### 2. 移动端滚动逻辑隔离
桌面端 vs 移动端使用不同的滚动判断机制：
- **桌面端**: `getBoundingClientRect()` 视窗位置判断
- **移动端**: `offsetHeight` 实际DOM高度判断

### 3. 性能优化的高度计算策略
使用缓存的DOM高度信息而非实时计算，以避免强制布局重计算

---

## 经验教训总结

- **CSS全局影响**: 全局 `overflow-x: hidden` 会破坏 `position: sticky`
- **滚动判断差异**: 移动端和桌面端需要隔离的滚动处理逻辑
- **布局统一**: 容器对齐不一致会导致视觉错位
- **状态同步**: 异步action中参数与state的不一致会导致数据错误

---

## API 设计与契约一致性（新增）

- 原则：相同资源的列表端点与详情端点必须返回一致的字段集合，详情端点应为列表端点的“超集”（superset），避免刷新或直链访问出现字段缺失导致的 UI 回退。
- 案例：`inspection_times` 需同时出现在 `/api/properties` 与 `/api/properties/{id}`。此次问题根因即为详情端点缺失该字段。
- 约束：
  - 新增字段时，优先在详情端点补齐，再在列表端点评估是否需要（考虑有效负载与性能）。
  - 任何字段移除/更名，必须通过后端兼容层或版本化保证向后兼容。
  - 启用缓存（FastAPI Cache/Redis）时，更新接口契约后应提供选择性失效端点，避免旧缓存长期污染响应。
- 实施建议：
  - 在后端添加契约单元测试/契约快照测试，校验两个端点的字段一致性（至少对关键字段如 `inspection_times`）。
  - 在 PR 审查清单中加入“端点字段一致性检查”项。

## 前端样式一致性（新增）

- 页面背景与卡片
  - 页面背景统一使用 `var(--color-bg-page)`，卡片/表面背景使用 `var(--color-bg-card)`，保持“页灰 + 卡片白”的视觉层次与列表页一致。
- 栅格与容器
  - 桌面端（≥1200px）统一容器 `max-width: 1200px`，左右内边距 `32px`；1920px 超宽断点仅居中不改变主容器宽度，避免“另一套主题”的观感。
- 设计令牌约束
  - 禁止硬编码颜色/边框/阴影/字号，统一使用 `src/style.css` 中的 tokens：如 `var(--color-text-primary/secondary)`, `var(--color-border-default)`, `var(--juwo-primary)` 等。
  - 新增/引用 CSS 变量时，必须先在 `:root`（`src/style.css`）声明再使用；禁止使用未定义变量（避免样式回退）。
  - 对详情页使用到的 tokens 已补齐映射：如 `--space-*`, `--bg-*`, `--shadow-xs`, `--brand-primary`, `--text-*`, `--link-color`。
- 断点与响应式
  - 统一断点：`768px`（平板）、`1200px`（桌面）、`1920px`（超宽）。优先小范围覆盖，避免在断点内“大改”造成体系分裂。
- 兼容性原则
  - 样式调整不得修改组件逻辑与数据流；以最小变更保证与首页风格、节奏一致。

## 富文本渲染统一原则（PropertyDetail.description 实战沉淀）
- 原则：页面中的富文本一律使用统一的 Markdown 渲染组件（如 MarkdownContent），组件内部完成 XSS 清理与必要的轻量预处理（GFM、换行转 <br>、项目符号 •/- 归一），页面侧仅负责容器样式与交互（折叠/展开）。
- 为什么：避免在各视图重复手写 v-html，降低 XSS 风险；实现一致的列表/段落/强调/链接样式；便于全局升级与样式统一。
- 技术权衡：不额外引入新依赖，优先复用既有组件；在保持体积可控的同时兼顾可读性与安全性。
- 适用范围：PropertyDetail.description 以及后续所有富文本字段（如房源须知、注意事项等）。
- 溯源：任务#TBD

## 图标系统与组件化 (Icon System & Componentization)

- **原则**: 全站图标统一使用 `lucide-vue-next` SVG 图标库，彻底弃用 Font Awesome (`<i>` 标签)。所有图标必须作为 Vue 组件导入和使用，并统一应用 `.spec-icon` 样式类。
- **为什么**:
    - **视觉一致性**: 确保全站所有图标风格、粗细、尺寸完全统一。
    - **性能**: SVG-in-JS 方案支持摇树优化 (tree-shaking)，只打包用到的图标，减小最终构建体积。相比之下，字体图标库需要加载整个字体文件。
    - **可维护性**: 通过组件化方式引用图标 (`<IconName />`)，代码更具可读性，且易于通过全局搜索进行管理和替换。
    - **样式控制**: SVG 图标可以通过 CSS (`fill`, `stroke`) 进行更精确的颜色、大小和动画控制，无需依赖 `font-size` 和 `color` 等hacky的文本样式。
- **实施规范**:
    - **导入**: `import { IconName } from 'lucide-vue-next'`
    - **使用**: `<IconName class="spec-icon" />`
    - **样式**:
        - 默认尺寸由 `.spec-icon` 全局控制 (e.g., `width: 24px; height: 24px;`)。
        - 特殊区域（如按钮、下拉菜单）可局部覆盖尺寸，但需保持比例，如 `.action-btn .spec-icon { width: 22px; height: 22px; }`。
        - 颜色通过 `color` 或 `fill` 属性继承或指定。
- **反模式** ❌:
    - 混合使用 Font Awesome 和 Lucide。
    - 使用 `<i>` 标签或图像文件作为图标。
    - 在组件内硬编码图标的 `width`, `height`, `color` 样式，破坏全局一致性。
- **溯源**: 本次从 `PropertyCard.vue` 到 `PropertyDetail.vue` 的图标统一重构工作。
