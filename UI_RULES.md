# Sydney Rental Hub - UI 开发法典 (UI Development Codex)

本文件定义了项目前端开发的视觉与交互规范，是确保UI一致性、可维护性和高质量的“唯一信息源”。所有开发工作必须严格遵守此法典。

---

## 第一基石：布局与间距 (Layout & Spacing)

**核心原则：** 所有布局和间距必须遵循 **8px 网格系统**。这意味着任何边距(margin)、内边距(padding)或尺寸都应是8的倍数。

- **基础单位：** 1 unit = 8px。
- **Tailwind实践：**
  - 使用 `p-{size}`, `m-{size}` 等工具类。例如, `p-4` 代表 `16px` (2 units) 的内边距。
  - 间距单位应为 `...-2, ...-4, ...-6, ...-8` 等，对应 `8px, 16px, 24px, 32px`。
- **规则：**
  1.  **禁止使用任意数值**，如 `top: 13px` 或 `margin-left: 7px`。
  2.  组件与组件之间的标准间距为 `gap-4` (16px) 或 `gap-6` (24px)。
  3.  卡片等容器的内边距必须使用 `p-4` (16px) 或 `p-6` (24px)。

---

## 第二基石：颜色 (Color)

**核心原则：** **绝不允许** 在代码中直接使用HEX、RGB等硬编码色值。所有颜色必须通过预定义的Tailwind颜色变量调用。

- **Tailwind实践：**
  - 使用 `bg-{color}`, `text-{color}`, `border-{color}` 等工具类。
- **颜色变量与应用场景：**
  - `primary`: `bg-primary`, `text-primary`。用于最重要的按钮（如“搜索”、“联系中介”）、当前激活状态、品牌Logo等。
  - `action`: `bg-action`, `text-action`。用于所有可点击的链接、次要按钮、筛选器等交互元素。
  - `grey-darkest`: `text-grey-darkest`。用于页面主标题 (H1, H2)。
  - `grey-darker`: `text-grey-darker`。用于正文文本、段落。
  - `grey-dark`: `text-grey-dark`。用于辅助信息、图标、时间戳等次要文本。
  - `grey-base`: `border-grey-base`。用于所有卡片、输入框的边框和分割线。
  - `grey-light`: `bg-grey-light`。用于输入框、下拉菜单的背景。
  - `grey-lighter`: `bg-grey-lighter`。用于页面主要背景色。
  - `grey-lightest`: `bg-grey-lightest`。用于需要轻微区分的背景区域，如表格的交替行。

---

## 第三基石：文字 (Typography)

**核心原则：** 所有文本样式必须使用预定义的字体层级。禁止自定义 `font-size` 或 `line-height`。

- **Tailwind实践：**
  - 组合使用 `text-{size}` 和 `font-{weight}`。
- **字体层级与应用场景：**
  - `text-4xl font-bold`: 页面级主标题 (Hero-Title)。
  - `text-2xl font-bold`: 房源卡片标题、区域标题。
  - `text-xl font-semibold`: 弹窗标题、重要信息标题。
  - `text-lg font-medium`: 文章小标题、列表项标题。
  - `text-base font-normal`: 默认正文文本。
  - `text-sm font-normal`: 辅助性文本、标签、说明文字。
  - `text-xs font-normal`: 最小号字体，用于法律声明、时间戳等。

---

## 第四基石：组件 (Components)

**核心原则：** 组件的外观由其内部预设的原子样式构成，外部调用时只负责布局，不应覆盖内部样式。

- **按钮 (Button):**
  - **主要按钮:** `bg-primary text-white font-semibold py-2 px-4 rounded-md shadow-DEFAULT`
  - **次要按钮:** `bg-action text-white font-semibold py-2 px-4 rounded-md shadow-DEFAULT`
  - **文本链接按钮:** `text-action font-medium`
- **卡片 (Card):**
  - `bg-white border border-grey-base rounded-md shadow-DEFAULT p-4`
- **输入框 (Input):**
  - `bg-grey-light border border-grey-base rounded-md p-2 focus:border-action focus:ring-2 focus:ring-action/50`
- **标签 (Tag/Badge):**
  - `bg-grey-lighter text-grey-darker text-sm font-medium px-3 py-1 rounded-full`

---

## 第五基石：无障碍设计 (Accessibility)

**核心原则：** 确保所有用户，包括有视觉或运动障碍的用户，都能顺畅使用我们的应用。

1.  **颜色对比度：** 所有文本颜色和背景色的组合必须符合WCAG AA级标准（对比度至少为4.5:1）。
2.  **焦点状态 (Focus State):** 所有可交互元素（按钮、链接、输入框）必须有清晰的 `:focus` 状态。默认使用 `focus:ring-2 focus:ring-action/50`。
3.  **语义化HTML：** 使用正确的HTML标签（如 `<nav>`, `<main>`, `<button>`），而不是用 `<div>` 模拟一切。
4.  **图像替代文本：** 所有 `<img>` 标签必须包含描述性的 `alt` 属性。
