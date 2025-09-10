# AI Prompt: 前端详情页 (PropertyDetail) 全方位令牌化冲刺行动计划

## 1. 角色 (Persona)

**你是一位经验丰富的 ****高级前端工程师** 和  **设计系统架构师** **。你正在指导我完成一个关键的重构冲刺：将一个复杂的核心页面 (**`<span class="selected">PropertyDetail.vue</span>`) 完全迁移到既有的、成熟的 Design Token 系统上。

## 2. 项目上下文 (Context)

**我正在开发一个名为“** **JUWO 桔屋找房** **”的 Vue 3 应用。我们已经取得了重大进展：**

* **设计系统已建立** **: 我们已经定义并实施了一套完整的 Design Token 系统，包括：**
* **颜色系统** **: 以蓝色为品牌主色，并搭配专业的中性灰阶。**
* **文字系统** **: 定义了基础/语义文字令牌，并创建了对应的 **`<span class="selected">.typo-*</span>` CSS 工具类。
* **国际化 (i18n)** **: 建立了一个轻量 i18n 框架，并创建了 **`<span class="selected">zh-CN.js</span>` 语言文件。
* **“护栏”已就位** **: 我们通过 Stylelint 和 pre-commit hook 防止了新的硬编码样式进入代码库。**
* **试点已成功** **: 我们已经在 **`<span class="selected">PropertyCard.vue</span>`、`<span class="selected">CommuteTimes</span>` 等多个组件上成功应用了新的系统，验证了其有效性。

 **当前核心任务 (P0)** **: 根据我们的项目路线图，现在的最高优先级任务是：对 **`<span class="selected">PropertyDetail.vue</span>` 页面进行**全量**的、**彻底的**令牌化改造，清除所有遗留的硬编码样式和英文静态文本。

## 3. 核心任务 (Task)

**你的核心任务是，为我提供一份** **详尽的、分步的、可立即执行的行动计划** **，指导我完成 **`<span class="selected">PropertyDetail.vue</span>` 页面的全方位重构。这份计划需要像一份“施工图”一样清晰，涵盖从审计、规划到具体代码实现的每一个环节。

## 4. 关键原则与约束 (Principles & Constraints)

* **彻底性** **: 本次冲刺的目标是 ** **100% 合规** **。不允许在 **`<span class="selected">PropertyDetail.vue</span>` 及其子组件中保留任何硬编码的颜色、字体或静态 UI 文本。
* **一致性** **: 严格使用已定义的语义令牌和 **`<span class="selected">.typo-*</span>` 工具类，不得创造一次性的局部样式。
* **结构化** **: i18n 的 key 命名必须遵循既有的、按页面/功能组织的结构。**

## 5. 期望的输出格式 (Output Format)

**请严格按照以下结构来组织你的回复，确保方案的完整性和可操作性。**

### **第一部分：审计与规划 (Audit & Plan) - “制定作战地图”**

* **1.1 `<span class="selected">PropertyDetail.vue</span>` 改造点审计清单** **:**
* **请为我列出一个典型的房源详情页中，** **所有需要被审计和改造的关键 UI 元素清单** **。这应作为一个 Checklist，帮助我确保没有任何遗漏。例如：**
  * **[ ] 页面主标题 (Headline)**
  * **[ ] 地址与区域信息**
  * **[ ] 价格与空出日期**
  * **[ ] 关键属性展示区 (卧室、浴室、车位)**
  * **[ ] 房源描述/详情富文本区域**
  * **[ ] 地图与周边设施模块**
  * **[ ] “联系我们”等主要行动召唤 (CTA) 按钮**
  * **[ ] 页面内所有分隔线 (Dividers)**
  * **[ ] 各个区域块 (Section) 的背景与边框**
  * **[ ] 所有标签 (Tags/Badges)**
  * **[ ] 所有次要按钮和链接**
* **1.2 国际化 (i18n) Key 结构规划** **:**
* **请在 **`<span class="selected">src/i18n/locales/zh-CN.js</span>` 文件中，为详情页规划一个清晰的、可扩展的 key 结构。请提供一个包含示例 key 的代码片段。
  ```
  // 例如:
  // zh-CN.js
  export default {
    // ...
    propertyDetail: {
      priceLabel: '价格',
      availabilityLabel: '空出日期',
      descriptionTitle: '房源详情',
      featuresTitle: '房屋设施',
      contactAgentButton: '联系我们',
      // ...
    },
  };

  ```

### **第二部分：执行手册 (Execution Manual) - “开始施工”**

* **2.1 推荐的执行顺序** **:**
* **请建议一个合理的改造顺序。例如：从页面的顶层容器和背景开始，然后是标题区，再逐个处理内容模块，最后处理交互元素。**
* **2.2 提供一个详尽的“操作手册” (核心部分)** **:**
* **这部分至关重要。** 请选择详情页中一个 **最复杂的区域** **（例如，包含标题、地址、价格和关键属性的“头部信息区”），并为其提供一个完整的 ** **Before & After 代码对比** **。**
* **Before** **: 展示该区域可能存在的、包含大量硬编码颜色、**`<span class="selected">font-*</span>` 样式和英文静态文本的“坏代码” (HTML 结构 + CSS)。
* **思考过程** **: 详细描述开发者看到这段代码后的思考步骤，将每一个硬编码值精确地映射到对应的 Design Token 或 i18n key。**
* **After** **: 展示经过重构后的、完全合规的“好代码” (HTML 结构 + CSS)。这段代码应该清晰地展示出：**
  1. **所有静态文本都已通过 **`<span class="selected">$t()</span>` 函数替换。
  1. **所有文本样式都已通过添加 **`<span class="selected">.typo-*</span>` 工具类来实现。
  1. **所有颜色（背景、边框、文字等）都已通过 **`<span class="selected">var(–-color-…)</span>` 令牌来应用。
  1. **所有间距都已通过 **`<span class="selected">var(–-space-…)</span>` 令牌来应用。

**请开始提供这份详细的行动计划。**
