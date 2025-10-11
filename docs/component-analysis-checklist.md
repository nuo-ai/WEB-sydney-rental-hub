# 原子组件样式测量记录

本文件记录了对 `realestate.com.au` 网站上各原子组件的 CSS 属性分析结果。

## A. 系统级测量项 (System-Level Measurements)
这些属性应被视为全局 Design Tokens，并应用到所有相关组件中。

### 动效与过渡 (Motion & Transitions)

- **transition-property**: 参与动画的 CSS 属性 (e.g., background-color, transform)。
- **transition-duration**: 动画标准时长 (e.g., 150ms, 300ms)。
- **transition-timing-function**: 缓动函数 (e.g., ease-in-out)。

### 焦点状态 (Focus States)

- **outline-style, outline-width, outline-color, outline-offset**: 键盘导航 (:focus-visible) 时的外轮廓样式。
- **focus-visible-box-shadow**: 一种更美观的、用 box-shadow 模拟的焦点辉光效果。

### 无障碍性属性 (Accessibility Attributes)

- **aria-* 属性**: 测量组件在不同状态下使用的所有 aria- 属性 (e.g., aria-label, aria-checked, aria-invalid)。
- **role 属性**: 测量非语义化标签（如`<div>`）模拟原生组件时使用的 role 属性。

---

## B. 组件级测量项 (Component-Level Measurements)

### I. 输入与操作 (Inputs & Actions)

#### 1. `Button` (按钮)

- **变体**: `primary`, `secondary`, `tertiary`, `danger`, `icon-only`
- **状态**: `default`, `hover`, `active`, `disabled`, `loading`
##### **数据记录**

**`primary` (主要按钮 - "Search")**
- **`default`**
  - **布局与尺寸**: `padding`: `12px 24px`, `height`: `48px`, `min-width`: `48px`
  - **外观**: `background-color`: `rgb(228, 0, 43)`, `border-style`: `none`, `border-radius`: `24px`, `box-shadow`: `none`
  - **排印**: `color`: `rgb(255, 255, 255)`, `font-size`: `16px`, `font-weight`: `500`
  - **交互**: `cursor`: `pointer`
- **`hover`**
  - **外观**: `background-color`: `rgb(168, 30, 53)`
- **`active`**
  - **外观**: `background-color`: `rgb(128, 25, 43)`
- **`disabled`**: *待分析*
- **`loading`**: *待分析*

**`secondary` (次要按钮 - "Filters")**
- **`default`**
  - **布局与尺寸**: `padding`: `11px 23px`, `height`: `48px`, `min-width`: `48px`
  - **外观**: `background-color`: `transparent`, `border-style`: `solid`, `border-width`: `1px`, `border-color`: `rgb(114, 110, 117)`, `border-radius`: `24px`
  - **排印**: `color`: `rgb(61, 59, 64)`, `font-size`: `16px`, `font-weight`: `500`
  - **交互**: `cursor`: `pointer`
- **`hover` & `active`**
  - **外观**: `background-color`: `rgb(246, 245, 247)`

**`tertiary` (标签页按钮 - "Rent")**
- **`default` (active tab)**
  - **布局与尺寸**: `padding`: `8px 12px`, `height`: `48px`
  - **外观**: `background-color`: `transparent`
  - **排印**: `color`: `rgb(61, 59, 64)`, `font-size`: `16px`, `font-weight`: `500`
  - **交互**: `cursor`: `pointer`
- **`hover`**
  - **外观**: `background-color`: `rgb(246, 245, 247)`

**`icon-only` (图标按钮 - "Save Search")**
- **`default`**
  - **布局与尺寸**: `padding`: `8px`, `height`: `40px`, `width`: `40px`
  - **外观**: `background-color`: `transparent`, `border-radius`: `8px`
  - **排印**: `color`: `rgb(61, 59, 64)` (for icon)
  - **交互**: `cursor`: `pointer`
- **`hover`**
  - **外观**: `background-color`: `rgb(246, 245, 247)`

#### 2. `Input` (输入框)

- **变体**: `text`, `password`, `search` (带图标)
- **状态**: `default`, `hover`, `focus`, `disabled`, `error`
##### **数据记录**

**`text` (标准文本输入)**
- **`default`**
  - **布局与尺寸**: `padding`: `0px`, `height`: `32px`
  - **外观**: `background-color`: `rgb(255, 255, 255)`, `border-style`: `none` (*由父容器处理*)
  - **排印**: `color`: `rgb(61, 59, 64)`, `font-size`: `16px`, `placeholder-color`: `rgb(114, 110, 117)`
- **`focus`**: *待分析*
- **`hover`**: *待分析*
- **`disabled`**: *待分析*
- **`error`**: *待分析*

#### 3. `Checkbox` & `Radio Button` (复选框 & 单选按钮)

- **状态**: `unchecked`, `checked/selected`, `disabled`, `hover`, `focus`
##### **数据记录**

- **`unchecked`**
  - **容器**: `size`: `16px`, `background-color`: `rgb(255, 255, 255)`, `border-style`: `solid`, `border-width`: `1px`, `border-color`: `rgb(114, 110, 117)`, `border-radius`: `4px`
- **`checked`**
  - **容器**: `size`: `16px`, `background-color`: `rgb(61, 59, 64)`, `border-color`: `rgb(61, 59, 64)`
- **标签**
  - **排印**: `label-color`: `rgb(61, 59, 64)`, `label-font-size`: `16px`
- **`disabled`**: *待分析*
- **`hover`**: *待分析*
- **`focus`**: *待分析*

#### 4. `Switch / Toggle` (开关)

- **状态**: `on`, `off`, `disabled`, `hover`, `focus`
- **测量属性**:
  - **轨道 (Track)**: `width`, `height`, `border-radius`, `track-background-color-on`, `track-background-color-off`。
  - **滑块 (Thumb)**: `size` (宽高), `background-color`, `box-shadow`。
  - **动效**: `transition` 属性 (用于滑块的平滑移动)。
  - **无障碍性**: `role="switch"`, `aria-checked`。

#### 5. `Textarea` (文本域)

- **测量属性**基本同 `Input`，但需额外关注:
  - **布局与尺寸**: `min-height`, `resize` 属性 (e.g., vertical, none)。

---

### II. 信息展示 (Data Display)

#### 6. `Icon` (图标)

- **测量属性**:
  - **尺寸**: 定义一套标准尺寸，如 `size-sm: 16px`, `size-md: 20px`, `size-lg: 24px`。
  - **颜色**: `color` (默认颜色), `color-interactive` (可交互颜色), `color-on-brand` (在品牌色上的颜色)。

#### 7. `Badge / Tag` (徽章 / 标签)

- **变体**: `neutral`, `info`, `success`, `warning`, `danger`
- **测量属性**: `padding`, `background-color`, `color`, `font-size`, `font-weight`, `border-radius`, `border-width` (for outlined tags)。

#### 8. `Avatar` (头像)

- **变体**: `circle`, `square`; `sm`, `md`, `lg`; `image`, `text`
- **测量属性**: `size` (宽高), `border-radius`, `font-size` (for text avatar), `background-color` (for text avatar), `group-overlap-margin` (头像组中的重叠边距)。

#### 9. `Divider` (分割线)

##### **数据记录**

- **`standard`**
  - **尺寸**: `height`: `1px`
  - **外观**: `border-color`: `rgb(229, 227, 232)`
  - **布局**: `margin`: `32px 0 0 0`

#### 10. `Tooltip` (文字提示)

- **测量属性**: `max-width`, `padding`, `background-color`, `color`, `font-size`, `border-radius`, `box-shadow`, `arrow-size`, `arrow-color`。

---

### III. 反馈与状态 (Feedback & Status)

#### 11. `Spinner / Loader` (加载指示器)

- **测量属性**: `size`, `color`, `stroke-width` (轨道粗细)。

#### 12. `Progress Bar` (进度条)

- **变体**: `linear`, `circular`
- **测量属性**: `track-color` (轨道颜色), `progress-color` (进度颜色), `height` (轨道粗细)。

#### 13. `Alert` (警告提示)

- **变体**: `info`, `success`, `warning`, `error`
- **测量属性**: `padding`, `border-radius`, `background-color` (柔和的背景色), `border-left-width`, `border-left-color`, `icon-color`, `text-color` (标题和正文)。

#### 14. `Skeleton` (骨架屏)

- **测量属性**: `background-color` (占位符底色), `shimmer-animation` (闪烁动画的`background-image`渐变和`animation`属性)。
