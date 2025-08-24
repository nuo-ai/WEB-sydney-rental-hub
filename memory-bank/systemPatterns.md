# 系统设计模式与最佳实践

## 核心架构

-   **前端**: Vue 3 (Composition API) + Vite
-   **状态管理**: Pinia
-   **路由**: Vue Router
-   **UI库**: Element Plus

## CSS与布局模式

### 1. 全局样式 vs. 局部样式

-   **模式**: 审慎使用全局样式。应将影响布局和定位的规则（如 `overflow`, `position`, `display`）限定在组件作用域内，以避免意料之外的副作用。
-   **反模式 (应避免)**: 对 `html` 或 `body` 等顶级元素应用强制性的 `overflow` 规则（例如 `overflow-x: hidden`）。
-   **经验教训**: 在UI修复任务中，我们再次确认了全局`overflow-x: hidden`是导致`position: sticky`失效的根本原因。我们已将此规则从`html, body`移至根组件`.app-container`，从而在解决`sticky`定位问题的同时，避免了全局副作用。

### 2. 布局对齐策略

-   **模式**: 在整个应用中，对主要的布局容器使用**统一的 `max-width` 和水平 `padding`**，以确保从上到下所有内容块的垂直对齐。
-   **示例**:
    -   导航栏内容容器 (`.top-nav-content`)
    -   搜索/筛选内容容器 (`.search-content-container`)
    -   主内容区容器 (`.container`)
    -   以上所有容器都应共享相同的 `max-width` (例如 `1200px`) 和 `padding` (例如 `0 32px`)。
-   **反模式 (应避免)**: 对不同的主内容容器使用不同的`max-width`，这会导致视觉上的错位。
-   **经验教训**: 我们通过将所有核心容器的`max-width`统一为`1200px`，成功解决了导航栏Logo、搜索栏和房源列表之间的对齐问题。

### 3. 全宽背景与内容居中

-   **模式**: 要实现一个背景全宽、但内容居中对齐的UI元素（如粘性搜索栏），应采用两层结构：
    1.  **外层容器 (`.full-bleed`)**: 设为 `width: 100%`，负责背景颜色和阴影。
    2.  **内层容器**: 设为与主内容区统一的 `max-width` 和水平`margin: auto`，负责将内容约束在布局内。
-   **在Home.vue中的应用**: `.search-filter-section` 作为全宽背景层，而 `.search-content-container` 作为居中的内容层。

## 状态管理 (Pinia)

-   **模式**: 遵循单一数据源（Single Source of Truth）原则。组件负责触发action并传递用户输入，而所有的业务逻辑和状态变更都应在Pinia store的 `actions` 中处理。
-   **示例**: `FilterTabs.vue` 在用户选择筛选条件后，调用 `propertiesStore.applyFilters(filters)`。`applyFilters` action 负责接收参数，更新store自身的`state`，然后基于更新后的`state`计算出新的`filteredProperties`。
-   **反模式 (应避免)**: 在action中混合使用传入的参数和未同步的旧`state`，这会导致数据不一致。
-   **经验教训**: 我们修复了`applyFilters` action，使其在执行筛选前，首先用传入的参数更新相关的store state，从而解决了筛选功能不正常的问题。

## 移动端响应式设计模式

### 4. 渐进式间距系统

-   **模式**: 在移动端界面中采用渐进式间距设计，从视觉层次上由紧到松：`核心元素间距 < 区域间距 < 容器间距`。
-   **示例实现**:
    ```css
    /* 渐进式间距：8px → 12px → 16px */
    .mobile-logo-section {
      padding: 8px 0 12px 0;  /* logo核心间距 */
    }
    .search-filter-section {
      margin-bottom: 12px;     /* 区域间距 */
    }
    .container {
      padding: 16px 32px;      /* 容器间距 */
    }
    ```
-   **反模式 (应避免)**: 使用统一的大间距值（如24px），会造成移动端界面过于松散。
-   **经验教训**: 通过将logo区域padding从`16px 0`优化为`8px 0 12px 0`，显著改善了移动端界面的紧凑性。

### 5. 移动端滚动逻辑隔离

-   **模式**: 移动端和桌面端应使用不同的滚动处理逻辑，避免跨平台状态污染。
-   **核心实现**:
    ```javascript
    const handleScroll = () => {
      const isMobileView = windowWidth.value <= 768
      
      if (isMobileView) {
        // 移动端：基于实际DOM高度判断
        const logoSection = document.querySelector('.mobile-logo-section')
        const logoHeight = logoSection ? logoSection.offsetHeight : 32
        const shouldBeFixed = currentScrollY > logoHeight
        
        // 移动端状态清洁：避免污染全局导航状态
        if (isNavHidden.value) {
          isNavHidden.value = false
        }
      } else {
        // 桌面端：使用getBoundingClientRect判断
        const shouldBeFixed = searchBarRect.top <= 0
      }
    }
    ```
-   **反模式 (应避免)**: 移动端和桌面端使用相同的`getBoundingClientRect()`判断逻辑，会导致移动端回滚到顶部时的判断错误。
-   **经验教训**: 通过将移动端滚动判断改为基于`offsetHeight`的精确计算，解决了回滚到顶部时logo消失的问题。

### 6. 精确高度计算策略

-   **模式**: 对于需要精确定位的移动端组件，应使用实际DOM高度（`offsetHeight`）而非实时计算的边界信息（`getBoundingClientRect()`）。
-   **技术对比**:
    ```javascript
    // ❌ 错误方式：频繁的getBoundingClientRect调用
    const searchBarRect = searchBarElement.value.getBoundingClientRect()
    const shouldBeFixed = searchBarRect.top <= 0
    
    // ✅ 正确方式：基于实际DOM高度的一次性计算
    const logoHeight = logoSection ? logoSection.offsetHeight : 32
    const shouldBeFixed = currentScrollY > logoHeight
    ```
-   **性能优势**: `offsetHeight`获取的是缓存的布局信息，避免了`getBoundingClientRect()`引起的强制布局重计算。
-   **经验教训**: 移动端场景下，基于滚动距离的判断比基于视窗位置的判断更加可靠和高效。
