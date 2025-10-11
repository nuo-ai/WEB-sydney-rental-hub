# Implementation Plan

[Overview]
本计划旨在修复 Astro 与 Docusaurus 站点中 Token 预览器无法响应暗色主题的问题。我们将修改相关页面的 JavaScript 逻辑，移除对静态 JSON 文件 (`srh.json`) 的硬依赖，转而动态地从 CSS 主题变量中读取初始值，并监听主题变化，从而确保预览组件能正确地、自动地反映当前的亮/暗色主题。

[Types]
本次变更无需新增或修改任何类型、接口或数据结构。

[Files]
- **将修改:** `tools/design-site-astro/src/pages/tokens.astro`
  - **变更内容:**
    1.  移除 `<script>` 块中 `fetch('/tokens/srh.json', ...)` 的逻辑。
    2.  修改页面加载时的初始化脚本，使其不再依赖 `srh.json`。改为定义一个 `initFromTheme()` 函数，该函数使用 `getComputedStyle` 从 DOM 读取当前生效的主题变量（如 `--color-text-primary`, `--color-background-surface` 等），并用这些值来初始化 `tokens` 对象和左侧的输入控件。
    3.  添加一个 `MutationObserver` 来监听 `<html>` 元素上 `data-theme` 属性的变化。当主题切换时，重新调用 `initFromTheme()` 函数，以更新预览和控件的值。
    4.  保留 `applyTokens` 函数，以便用户在控制面板中手动修改值时，能够通过内联样式实时预览效果。

- **将修改:** `tools/design-site-astro/src/pages/components.astro`
  - **变更内容:**
    1.  移除 `<script>` 块中 `fetch('/tokens/srh.json', ...)` 的逻辑。
    2.  由于此页面仅为静态展示，无需复杂的 `applyTokens` 逻辑。我们将完全移除该脚本，因为在 `tokens.astro` 中对 `--srh-*` 变量的默认值映射修复后，此页面已能直接通过 CSS 继承正确的主题样式。

- **将修改:** `apps/docs-site/src/components/TokenPreview.jsx`
  - **变更内容:**
    1.  修改 `useEffect` 钩子，移除 `fetch('/tokens/srh.json', ...)` 逻辑。
    2.  在 `useEffect` 中，改为使用 `getComputedStyle` 读取 CSS 变量来构建 `fallback`（即初始）`tokens` 对象。
    3.  (可选，作为增强) 添加对 Docusaurus 主题切换的监听。由于 Docusaurus 通过 `<html>` 上的 `data-theme` 属性控制主题，我们可以使用 `MutationObserver` 来监听此属性的变化，并在变化时重新读取 CSS 变量并更新组件状态。

[Functions]
- **将新增:** `initFromTheme()` (在 `tokens.astro` 的 `<script>` 中)
  - **签名:** `function initFromTheme()`
  - **路径:** `tools/design-site-astro/src/pages/tokens.astro`
  - **目的:** 读取当前页面的计算样式，提取主题颜色值，并用它们来设置 `tokens` 对象和更新输入控件的显示值。

- **将移除:** `fetch('/tokens/srh.json', ...)` 调用 (在 `tokens.astro`, `components.astro`, 和 `TokenPreview.jsx` 中)
  - **原因:** 这是导致主题被写死为亮色的根源。

[Classes]
本次变更无需修改任何类。

[Dependencies]
本次变更无需修改任何依赖。

[Testing]
需要手动测试以验证修复效果：
1.  访问 Astro 组件预览页 (`/components`)。点击 “切换暗色” 按钮。**预期结果:** 卡片背景和文字颜色应立即切换到暗色。
2.  访问 Astro Tokens Playground 页面 (`/tokens`)。点击 “切换暗色” 按钮。**预期结果:** 右侧的预览卡片和左侧的控制面板都应切换到暗色模式，并且左侧的颜色选择器和输入框中的值也应更新为暗色主题的颜色代码。
3.  在 Astro Tokens Playground 的暗色模式下，手动修改一个颜色（例如 `cardBg`）。**预期结果:** 只有预览卡片的背景色会变为你修改的值，页面的其他部分保持暗色主题。
4.  再次点击 “切换亮色”。**预期结果:** 页面应切换回亮色主题，并且左侧控制面板的值也应重置为亮色主题的对应值。
5.  (可选) 在 Docusaurus 站点中进行相同的测试，确认 `TokenPreview` 组件也能正常工作。

[Implementation Order]
1.  将此计划内容写入项目根目录的 `implementation_plan.md` 文件中。
2.  修改 `tools/design-site-astro/src/pages/components.astro`，移除其 JavaScript 部分。
3.  修改 `tools/design-site-astro/src/pages/tokens.astro`，重构其 JavaScript 以移除 `fetch` 并实现动态主题加载。
4.  修改 `apps/docs-site/src/components/TokenPreview.jsx`，同样移除 `fetch` 并改为动态读取主题。
