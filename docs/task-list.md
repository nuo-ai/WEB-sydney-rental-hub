### **原子组件最终测量清单 (Final Atomic Components Measurement Checklist)**

**简介:** 本清单旨在指导 AI 代理对参考网站的原子组件进行全面的逆向工程。代理需测量并记录下述所有属性，为后续的“设计令牌映射”和“组件构建”阶段提供一份完整、精确的组件蓝图。

#### **A. 系统级测量项 (System-Level Measurements)**

*这些属性应被视为全局 Design Tokens，并应用到所有相关组件中。*

1. **动效与过渡 (Motion & Transitions)**
   * `transition-property`: 参与动画的 CSS 属性 (e.g., `background-color, transform`)。
   * `transition-duration`: 动画标准时长 (e.g., `150ms`, `300ms`)。
   * `transition-timing-function`: 缓动函数 (e.g., `ease-in-out`)。
2. **焦点状态 (Focus States)**
   * `outline-style`, `outline-width`, `outline-color`, `outline-offset`: 键盘导航 (`:focus-visible`) 时的外轮廓样式。
   * `focus-visible-box-shadow`: 一种更美观的、用 `box-shadow` 模拟的焦点辉光效果。
3. **无障碍性属性 (Accessibility Attributes)**
   * `aria-*` 属性: 测量组件在不同状态下使用的所有 `aria-` 属性 (e.g., `aria-label`, `aria-checked`, `aria-invalid`)。
   * `role` 属性: 测量非语义化标签（如 `<div>`）模拟原生组件时使用的 `role` 属性。

---

#### **B. 组件级测量项 (Component-Level Measurements)**

##### **I. 输入与操作 (Inputs & Actions)**

**1. `Button` (按钮)**

* **变体** : `primary`, `secondary`, `tertiary`, `danger`, `icon-only`
* **状态** : `default`, `hover`, `active`, `disabled`, `loading`
* **测量属性** :
* **布局与尺寸** : `padding` (区分带文字和纯图标), `height`, `min-width`, `gap` (图标与文字间距)。
* **外观** : `background-color`, `border-style`, `border-width`, `border-color`, `border-radius`, `box-shadow`。
* **排印** : `color` (文字颜色), `font-size`, `font-weight`。
* **交互** : `transform` (e.g., `scale` on active), `cursor`。
* **无障碍性** : `aria-label` (for `icon-only`), `aria-busy` (for `loading`)。

**2. `Input` (输入框)**

* **变体** : `text`, `password`, `search` (带图标)
* **状态** : `default`, `hover`, `focus`, `disabled`, `error`
* **测量属性** :
* **布局与尺寸** : `padding`, `height`。
* **外观** : `background-color`, `border-style`, `border-width`, `border-color`, `border-radius`。
* **排印** : `color` (文字颜色), `font-size`, `placeholder-color` (占位符颜色)。
* **状态样式** : `focus-border-color`, `focus-box-shadow`, `error-border-color`, `disabled-background-color`, `disabled-color`。
* **内嵌元素** : `icon-color`, `icon-size`, `prefix/suffix-color`, `prefix/suffix-padding`。
* **无障碍性** : `aria-invalid` (for `error`)。

**3. `Checkbox` & `Radio Button` (复选框 & 单选按钮)**

* **状态** : `unchecked`, `checked`/`selected`, `disabled`, `hover`, `focus`
* **测量属性** :
* **容器** : `size` (方框/圆圈的宽高), `background-color`, `border-style`, `border-width`, `border-color`, `border-radius`。
* **内部标记** : `checkmark-color`/`dot-color`, `checkmark-size`/`dot-size`。
* **标签** : `label-color`, `label-font-size`, `gap` (容器与标签的间距)。
* **无障碍性** : `role`, `aria-checked`。

**4. `Switch / Toggle` (开关)**

* **状态** : `on`, `off`, `disabled`, `hover`, `focus`
* **测量属性** :
* **轨道 (Track)** : `width`, `height`, `border-radius`, `track-background-color-on`, `track-background-color-off`。
* **滑块 (Thumb)** : `size` (宽高), `background-color`, `box-shadow`。
* **动效** : `transition` 属性 (用于滑块的平滑移动)。
* **无障碍性** : `role="switch"`, `aria-checked`。

**5. `Textarea` (文本域)**

* *测量属性基本同 `Input`，但需额外关注:*
  * **布局与尺寸** : `min-height`, `resize` 属性 (e.g., `vertical`, `none`)。

##### **II. 信息展示 (Data Display)**

**6. `Icon` (图标)**

* **测量属性** :
* **尺寸** : 定义一套标准尺寸，如 `size-sm: 16px`, `size-md: 20px`, `size-lg: 24px`。
* **颜色** : `color` (默认颜色), `color-interactive` (可交互颜色), `color-on-brand` (在品牌色上的颜色)。

**7. `Badge / Tag` (徽章 / 标签)**

* **变体** : `neutral`, `info`, `success`, `warning`, `danger`
* **测量属性** : `padding`, `background-color`, `color`, `font-size`, `font-weight`, `border-radius`, `border-width` (for outlined tags)。

**8. `Avatar` (头像)**

* **变体** : `circle`, `square`; `sm`, `md`, `lg`; `image`, `text`
* **测量属性** : `size` (宽高), `border-radius`, `font-size` (for text avatar), `background-color` (for text avatar), `group-overlap-margin` (头像组中的重叠边距)。

**9. `Divider` (分割线)**

* **测量属性** : `height`/`width` (粗细), `border-color`/`background-color`, `margin` (与内容的距离)。

**10. `Tooltip` (文字提示)**

* **测量属性** : `max-width`, `padding`, `background-color`, `color`, `font-size`, `border-radius`, `box-shadow`, `arrow-size`, `arrow-color`。

##### **III. 反馈与状态 (Feedback & Status)**

**11. `Spinner / Loader` (加载指示器)**

* **测量属性** : `size`, `color`, `stroke-width` (轨道粗细)。

**12. `Progress Bar` (进度条)**

* **变体** : `linear`, `circular`
* **测量属性** : `track-color` (轨道颜色), `progress-color` (进度颜色), `height` (轨道粗细)。

**13. `Alert` (警告提示)**

* **变体** : `info`, `success`, `warning`, `error`
* **测量属性** : `padding`, `border-radius`, `background-color` (柔和的背景色), `border-left-width`, `border-left-color`, `icon-color`, `text-color` (标题和正文)。

**14. `Skeleton` (骨架屏)**

* **测量属性** : `background-color` (占位符底色), `shimmer-animation` (闪烁动画的 `background-image`渐变和 `animation`属性)。

---

**使用说明:**

1. **测量 (Measure)** : AI代理使用本清单对参考组件进行彻底分析，提取所有原始CSS值。
2. **映射 (Map)** : 人类开发者/设计师审核测量结果，并将原始值**映射**到已定义的全局Design Tokens。
3. **构建 (Build)** : 使用映射后的Tokens构建最终的Vue组件。
