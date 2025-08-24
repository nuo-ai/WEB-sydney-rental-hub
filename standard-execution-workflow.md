# Workflow: Standard Task Execution

**Objective**: To execute a pre-approved plan in a systematic, traceable, and verifiable manner after switching from "Plan Mode" to "Act Mode".

---

### **Phase 1: Initialization & Synchronization**

1. **Load Final Plan**: The approved plan from "Plan Mode" serves as the definitive action plan.
2. **Create Task Checklist (`task_progress`)**: Decompose the final plan into a detailed Markdown task checklist. This list will be the single source of truth for tracking progress.
3. **Final Context Sync**: Briefly review `activeContext.md` and `progress.md` from the memory-bank to ensure work commences within the latest project context.

---

### **Phase 2: Iterative Implementation & Feedback Loop**

1. **Select Next Task**: Choose the first incomplete (`- [ ]`) item from the task checklist.
2. **Select Optimal Tool**: Based on the task's nature (e.g., file creation, code modification, command execution), select the most appropriate tool (`write_to_file`, `replace_in_file`, `execute_command`, etc.).
3. **Execute Single Action**: Execute one, and only one, tool action.
4. **Await and Analyze Result**: **Crucially, pause and wait for the system's feedback.** Analyze the result, whether it's a success confirmation, an error message, a linter warning, or a failed test log.
5. **Update Task Checklist**: If the action was successful, use the `task_progress` parameter in the next tool call to mark the corresponding checklist item as complete (`- [x]`).
6. **Loop**: Repeat steps 1-5 until all items on the task checklist are marked as complete.

---

### **Phase 3: Verification & Documentation**

1. **Final Verification**: Once all tasks are complete, execute a final verification step. This could be:

   * Running the relevant test suite (`npm test`).
   * Launching the application for a quick visual and functional check using browser tools.
   * Running a linter to ensure code quality.
2. **Update Memory Bank**: **This is a critical step.** Archive the outcomes, learnings, new patterns, and key decisions from the completed task into the relevant memory-bank documents (`activeContext.md`, `progress.md`, `systemPatterns.md`). This ensures knowledge persistence.
3. **Complete the Task**: Use the `<attempt_completion>` tool to deliver a clear and comprehensive report of the work performed and the final outcome.

   ---

   ## 以下是中文翻译，AI 不必阅读

   ---


   # 工作流：通过代码层级分析复刻 UI 组件

   该工作流提供了一个系统化流程，用于将本地 UI 组件与参考实现（例如线上生产网站）进行对比，从而识别并记录所有结构与样式上的差异。

   ## 先决条件


   - 已运行用于被分析组件的本地开发服务器。
   - 参考实现的 URL。
   - `playwright` MCP 服务器可用。

   ---

   ## 阶段一：数据驱动的标准抽取（参考侧）

   1. **确定目标 URL**：给出包含待分析组件的参考网站 URL。
      ```xml
      <ask_followup_question>
      <question>Please provide the URL of the reference website containing the component to analyze.</question>
      </ask_followup_question>
      ```
   2. **导航并触发组件**：使用浏览器工具导航到页面，并执行必要操作使目标组件可见（例如点击按钮打开模态框或面板）。
      ```xml
      <use_mcp_tool>
      <server_name>playwright</server_name>
      <tool_name>browser_navigate</tool_name>
      <arguments>
      {
        "url": "[URL from previous step]"
      }
      </arguments>
      </use_mcp_tool>
      <!-- 如需暴露元素，可紧随其后调用 browser_click -->
      ```
   3. **执行分析脚本**：运行 `browser_evaluate` 脚本，将组件的 DOM 结构与计算后的 CSS 样式提取为结构化 JSON 对象。这会提供目标组件的精确、数据驱动快照。
      ```xml
      <use_mcp_tool>
      <server_name>playwright</server_name>
      <tool_name>browser_evaluate</tool_name>
      <arguments>
      {
        "function": "async (selector) => { const element = document.querySelector(selector); if (!element) return null; const style = window.getComputedStyle(element); const styleJSON = {}; for (const prop of style) { styleJSON[prop] = style.getPropertyValue(prop); } return { tagName: element.tagName, innerHTML: element.innerHTML, computedStyle: styleJSON }; }",
        "element": "The target UI component on the reference page",
        "ref": "[CSS selector for the reference component]"
      }
      </arguments>
      </use_mcp_tool>
      ```
      *备注：得到的 JSON 数据将在内部保存为“参考标准（reference standard）”。*

   ---

   ## 阶段二：数据驱动的实现侧分析（本地）

   1. **确定本地 URL**：给出本地开发服务器的 URL。
      ```xml
      <ask_followup_question>
      <question>Please provide the URL of your local development server (e.g., http://localhost:5174).</question>
      </ask_followup_question>
      ```
   2. **导航并触发组件**：在本地应用上重复阶段一的流程。
   3. **执行分析脚本**：在本地组件上运行**完全相同**的 `browser_evaluate` 脚本，提取数据用于对比。

   ---

   ## 阶段三：自动化差异分析

   1. **加载数据**：在内部加载参考标准与本地实现两端的 JSON 数据。
   2. **比较数据**：系统性比对两个 JSON 对象，识别以下差异：
      * HTML 结构（如 `tagName`、`innerHTML` 的差异）。
      * 计算样式（如 `box-shadow`、`border-radius`、`color` 等样式属性的不一致）。
   3. **生成报告**：以 Markdown 形式生成清晰、可读的差异报告，并用表格呈现所有发现的差距。

   ---

   ## 阶段四：精确行动方案

   1. **创建待办清单**：基于差异分析报告，生成详细且可执行的开发任务清单。
   2. **请求批准**：在切换到 `ACT MODE` 实施之前，向用户呈现最终行动方案并请求批准。
      ```xml
      <ask_followup_question>
      <question>I have completed the UI analysis and generated a detailed action plan. Please review the plan above. Shall I proceed with implementing these changes?</question>
      <options>["Yes, proceed with the plan.", "No, let's discuss some changes."]</options>
      </ask_followup_question>
      ```
