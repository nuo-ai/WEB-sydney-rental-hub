# 原子组件样式测量记录

本文件记录了对 `realestate.com.au` 网站上各原子组件的 CSS 属性分析结果。

## B. 组件级测量项 (Component-Level Measurements)

### I. 输入与操作 (Inputs & Actions)

#### 1. `Button` (按钮)

##### **变体: `primary` (主要按钮 - "Search")**

- **状态: `default`**
  - **布局与尺寸**:
    - `padding`: `12px 24px`
    - `height`: `48px` (实际为 `47.9972px`)
    - `min-width`: `48px`
    - `gap`: `normal` (浏览器默认)
  - **外观**:
    - `background-color`: `rgb(228, 0, 43)`
    - `border-style`: `none`
    - `border-width`: `0px`
    - `border-color`: `rgb(255, 255, 255)`
    - `border-radius`: `24px`
    - `box-shadow`: `none`
  - **排印**:
    - `color`: `rgb(255, 255, 255)`
    - `font-size`: `16px`
    - `font-weight`: `500`
  - **交互**:
    - `transform`: `none`
    - `cursor`: `pointer`
  - **无障碍性**:
    - `aria-label`: (未指定)
    - `aria-busy`: (未指定)

- **状态: `hover`**
  - *自动化工具分析受限，待手动测量。*

- **状态: `active`**
  - *自动化工具分析受限，待手动测量。*

- **状态: `disabled`**
  - *待分析。*

- **状态: `loading`**
  - *待分析。*

---

##### **变体: `secondary` (次要按钮 - "Filters")**

- **状态: `default`**
  - **布局与尺寸**:
    - `padding`: `11px 23px`
    - `height`: `48px` (实际为 `47.9972px`)
    - `min-width`: `48px`
    - `gap`: `normal` (浏览器默认, 包含图标)
  - **外观**:
    - `background-color`: `transparent` (实际为 `rgba(0, 0, 0, 0)`)
    - `border-style`: `solid`
    - `border-width`: `1px` (实际为 `0.909091px`)
    - `border-color`: `rgb(114, 110, 117)`
    - `border-radius`: `24px`
    - `box-shadow`: `none`
  - **排印**:
    - `color`: `rgb(61, 59, 64)`
    - `font-size`: `16px`
    - `font-weight`: `500`
  - **交互**:
    - `transform`: `none`
    - `cursor`: `pointer`

- **状态: `hover`**
  - *自动化工具分析受限，待手动测量。*

- **状态: `active`**
  - *自动化工具分析受限，待手动测量。*

---

##### **变体: `tertiary` (标签页按钮 - "Rent")**

- **状态: `default` (active tab)**
  - **布局与尺寸**:
    - `padding`: `8px 12px`
    - `height`: `48px` (实际为 `47.9972px`)
    - `min-width`: `0px`
    - `gap`: `normal`
  - **外观**:
    - `background-color`: `transparent` (实际为 `rgba(0, 0, 0, 0)`)
    - `border-style`: `none`
    - `border-width`: `0px`
    - `border-color`: `rgb(61, 59, 64)`
    - `border-radius`: `0px`
    - `box-shadow`: `none` (Note: a separate element provides the underline)
  - **排印**:
    - `color`: `rgb(61, 59, 64)`
    - `font-size`: `16px`
    - `font-weight`: `500`
  - **交互**:
    - `transform`: `none`
    - `cursor`: `pointer`

- **状态: `hover`**
  - *自动化工具分析受限，待手动测量。*

---

##### **变体: `icon-only` (图标按钮 - "Save Search")**

- **状态: `default`**
  - **布局与尺寸**:
    - `padding`: `8px`
    - `height`: `40px`
    - `width`: `40px`
    - `min-width`: `40px`
  - **外观**:
    - `background-color`: `transparent` (实际为 `rgba(0, 0, 0, 0)`)
    - `border-style`: `none`
    - `border-width`: `0px`
    - `border-color`: `rgb(61, 59, 64)`
    - `border-radius`: `8px`
    - `box-shadow`: `none`
  - **排印**:
    - `color`: `rgb(61, 59, 64)` (This is for the icon SVG)
  - **交互**:
    - `cursor`: `pointer`

- **状态: `hover`**
  - *自动化工具分析受限，待手动测量。*

---

### II. 输入与操作 (Inputs & Actions) - Continued

#### 2. `Input` (输入框)

##### **变体: `text` (标准文本输入)**

- **状态: `default`**
  - **布局与尺寸**:
    - `padding`: `0px`
    - `height`: `32px` (实际为 `31.9886px`)
  - **外观**:
    - `background-color`: `rgb(255, 255, 255)`
    - `border-style`: `none` (Note: border is handled by a parent container)
    - `border-width`: `0px`
    - `border-color`: `rgb(61, 59, 64)`
    - `border-radius`: `0px`
  - **排印**:
    - `color`: `rgb(61, 59, 64)`
    - `font-size`: `16px`
    - `placeholder-color`: `rgb(114, 110, 117)`

- **状态: `focus`**
  - *自动化工具分析受限，待手动测量。*

---

#### 3. `Checkbox` (复选框)

##### **变体: `standard`**

- **状态: `checked`**
  - **容器 (Box)**:
    - `size`: `16px` (实际为 `15.9943px`)
    - `background-color`: `rgb(61, 59, 64)`
    - `border-style`: `solid`
    - `border-width`: `1px` (实际为 `0.909091px`)
    - `border-color`: `rgb(61, 59, 64)`
    - `border-radius`: `4px`
  - **内部标记 (Checkmark)**:
    - *Note: Checkmark is an SVG icon, its color is inherited.*
  - **标签 (Label)**:
    - *待分析*

- **状态: `unchecked`**
  - **容器 (Box)**:
    - `size`: `16px` (实际为 `15.9943px`)
    - `background-color`: `rgb(255, 255, 255)`
    - `border-style`: `solid`
    - `border-width`: `1px` (实际为 `0.909091px`)
    - `border-color`: `rgb(114, 110, 117)`
    - `border-radius`: `4px`

---

### III. 信息展示 (Data Display)

#### 9. `Divider` (分割线)

- **变体: `standard`**
  - `height`: `1px` (实际为 `0.909091px`)
  - `background-color`: `transparent`
  - `border-width`: `1px 0 0 0` (实际为 `0.909091px 0px 0px`)
  - `border-color`: `rgb(229, 227, 232)`
  - `margin`: `32px 0 0 0`

---
