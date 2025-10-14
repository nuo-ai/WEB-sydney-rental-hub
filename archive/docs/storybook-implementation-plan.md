# Storybook 实施计划：悉尼租房中心

**版本**: 1.0
**日期**: 2025-10-11
**负责人**: Cline (高级前端工程师)

## 摘要

本文档为“悉尼租房中心”项目制定了一套全面的 Storybook 实施策略。目标是创建一个服务于开发、设计和测试的“单一事实来源”，完整反映项目的设计系统和组件库，并与现有的 Monorepo 架构和技术栈无缝集成。

---

## 第一部分：项目设置 (Project Setup)

### 1. 框架与环境
- **框架**: Storybook 将基于 **Vue 3** 和 **Vite** 进行设置，以完全匹配项目 `apps/web` 的技术栈。
- **推荐版本**:
  - `storybook@^8.x`：这是当前的最新主版本，为 Vue 3 和 Vite 提供了最佳的性能和最完善的支持。
  - `storybook-builder-vite`：将作为 Storybook 的构建器。

### 2. 目录结构
- **位置**: Storybook 的所有配置文件和 Stories 将统一存放在共享 UI 包 `@sydney-rental-hub/ui` 中。
- **具体路径**: `packages/ui/.storybook/`
- **理由**: 此举强制要求组件在与业务逻辑隔离的环境中开发，从而保证其通用性和高复用性，符合项目 `systemPatterns.md` 中定义的“独立的组件开发环境”原则。

### 3. 技术细节
- **语言**: Stories 将使用 **JavaScript (`.js`)** 编写。
- **理由**: 尽管项目部分配置了 TypeScript，但现有组件 (`.vue`) 主要使用 Composition API 的 `<script setup>` 语法，并未强制 TypeScript。为保持一致性并降低初期引入的复杂性，建议使用 JavaScript。未来可根据需要逐步迁移至 TypeScript (`.ts`)。

---

## 第二部分：组件展示计划 (Component Showcase Plan)

### 1. 组件清单

#### Group A: 核心基础组件 (`@sydney-rental-hub/ui`)
这些是已经存在于共享 UI 包中的、高度可复用的基础组件。

- `[x] BaseBadge` - 基础徽章
- `[x] BaseButton` - 基础按钮
- `[x] BaseChip` - 基础标签
- `[x] BaseIconButton` - 图标按钮
- `[x] BaseListItem` - 列表项
- `[x] BaseSearchInput` - 搜索输入框
- `[x] BaseToggle` - 开关

#### Group B: 核心业务组件 (`apps/web/`)
这些是当前存在于主应用中的、与业务逻辑紧密相关但具有高复用潜力的组件。将它们纳入 Storybook 有助于标准化其行为，并为未来迁移至 `packages/ui` 做准备。

- `[ ] PropertyCard` - 房源卡片
- `[ ] FilterPanel` - 筛选面板 (整体)
- `[ ] FilterTabs` - 筛选标签页 (PC端)
- `[ ] SaveSearchModal` - 保存搜索弹窗
- `[ ] ImageCarousel` - 图片轮播 (可从 `PropertyCard` 中抽离)
- `[ ] SpecRow` - 规格行 (用于展示卧室、浴室数量等)
- `[ ] UserProfileMenu` - 用户资料菜单

### 2. 组件的变体与状态 (示例)

#### BaseButton
`BaseButton` 的 Story 应通过 Storybook 的 Controls Addon 清晰地展示其所有变体和状态。

- **变体 (Variants)**: 使用 `argTypes` 定义一个 `variant` prop，可选值为 `primary`, `secondary`, `danger`, `text`。
- **尺寸 (Sizes)**: 定义 `size` prop，可选值为 `small`, `medium`, `large`。
- **状态 (States)**:
  - **Disabled**: 通过一个布尔类型的 `disabled` prop 控制。
  - **Loading**: 通过一个布尔类型的 `loading` prop 控制，按钮内部应显示加载指示器并禁用交互。
- **带图标 (Icon)**: 允许通过 `slot` 或 `icon` prop 传入 `lucide-vue-next` 图标。

```javascript
// 示例 Story (BaseButton.stories.js)
export const Primary = {
  args: {
    variant: 'primary',
    label: 'Primary Button',
    disabled: false,
    loading: false,
  },
};
```

#### PropertyCard
`PropertyCard` 的 Story 需要模拟不同的业务场景和数据状态。

- **默认状态 (Default)**: 传入一个标准的房源对象，展示完整的卡片信息。
- **已收藏状态 (Favorited)**: 传入一个 `isFavorite: true` 的 prop，卡片右上角的收藏图标应为激活状态（使用 `--accent-primary` 颜色）。
- **新房源状态 (New Property)**: 传入一个 `isNew: true` 的 prop，卡片左上角应显示“新房源”徽章。
- **加载中状态 (Loading)**: 创建一个 `Loading` Story，展示该组件的骨架屏 (Skeleton Screen) 视图，用于数据加载时的占位。

---

## 第三部分：Storybook 结构与特性 (Storybook Structure & Features)

### 1. 侧边栏组织结构
为了使 Storybook 成为一个清晰的文档中心，侧边栏将采用以下三层结构：

- **`▶ 介绍 (Introduction)`**
  - `欢迎 (Welcome)`: Storybook 的首页，简要介绍此文档系统的目的。
  - `项目简介 (About)`: 链接到项目的核心文档，如 `projectbrief.md`。

- **`▶ 设计规范 (Foundations)`**
  - `Colors (颜色)`: 可视化展示所有的设计令牌颜色，包括原始层、语义层和组件层。每个颜色都应显示其变量名、十六进制值，并提供用法说明。
  - `Typography (排版)`: 展示不同的字号、字重和行高令牌，并提供 `<h1>` 到 `<h6>` 以及正文的排版示例。
  - `Spacing (间距)`: 可视化展示 `--space-*` 和 `--gap-*` 令牌，说明它们在布局中的应用。
  - `Shadows (阴影)`: 展示 `--shadow-*` 令牌，并提供卡片和面板的阴影示例。

- **`▶ 组件 (Components)`**
  - **`Form Elements`**:
    - `BaseButton`
    - `BaseIconButton`
    - `BaseSearchInput`
    - `BaseToggle`
  - **`Data Display`**:
    - `BaseBadge`
    - `BaseChip`
    - `BaseListItem`
    - `PropertyCard`
  - **`Overlays`**:
    - `SaveSearchModal`
  - **`Navigation`**:
    - `FilterPanel`
    - `FilterTabs`

### 2. 主题切换功能
- **实现**: 在 Storybook 的全局工具栏 (Toolbar) 中添加一个“主题切换”按钮。
- **技术方案**:
  1. 在 `packages/ui/.storybook/preview.js` 中定义一个 `globalTypes`，包含 `light` 和 `dark` 两个选项。
  2. 创建一个全局 `decorator`，它会根据工具栏中选择的主题，为所有组件的根 `div` 动态添加 `light` 或 `dark` 类。
  3. 确保 `preview.js` 导入了主应用的 `design-tokens.css`，这样 `.dark` 类下的所有 CSS 变量覆盖才能生效。
- **效果**: 用户可以一键在亮/暗模式之间切换，并实时预览所有组件在不同主题下的视觉表现，确保设计系统的一致性。
