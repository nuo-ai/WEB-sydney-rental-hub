# Core Rules for the Sydney Rental Hub Project

This file establishes the foundational principles and mandatory workflows for our collaboration. These rules are non-negotiable and must be adhered to in all tasks to ensure a streamlined, efficient, and predictable development process.

---

### 1. The Memory Bank Principle (MANDATORY)

**Rule**: At the absolute beginning of any new task, my first action MUST be to read all documents within the `memory-bank/` directory. This is my primary context-loading mechanism and the foundation for all subsequent actions.

**Objective**: To ensure I am always operating with the latest, complete project context, making my actions more accurate and reducing redundant questions.

---

### 2. Standard Task Execution Principle (MANDATORY)

**Rule**: When switching from "Plan Mode" to "Act Mode", I MUST adhere to the standard execution workflow. This is an innate process, not one triggered by an external command.

**Workflow Steps & Example**:

1.  **Decompose Plan**: Translate the approved plan into a `task_progress` checklist, which is managed via the Focus Chain feature.
    *   *Example Task: Add a new `PropertyCard.vue` component*
        *   `- [ ] Generate component skeleton`
        *   `- [ ] Integrate with Element Plus for styling`
        *   `- [ ] Connect to API endpoint`
        *   `- [ ] Write unit tests with Vitest`
2.  **Iterate & Verify**: Execute one tool at a time for the **first incomplete item** on the checklist, await feedback, and update the checklist upon success. This is a strict "act-then-verify" loop.
3.  **Validation**: Once the checklist is complete, I will propose a final validation step (e.g., via browser interaction). I will **always assume the development environment (e.g., http://localhost:5173/) is already running** and will not attempt to start or stop any services.
4.  **Document & Complete**: Following successful validation and your request, I will **update the `memory-bank/`** and then use `<attempt_completion>`.

**Objective**: To ensure every task is executed in a predictable, systematic, and well-documented manner.

---

### 3. Technical & Coding Standards Principle (MANDATORY)

**Rule**: All code generated or modified within this project MUST adhere to the following technical standards:

1.  **Vue.js & Naming**:
    *   Components MUST use the **Composition API** (`<script setup>`).
    *   Component filenames MUST use `PascalCase` (e.g., `PropertyCard.vue`).
    *   Pinia store files MUST use the `useXxxStore` pattern (e.g., `usePropertiesStore.js`).
2.  **Styling**:
    *   Prioritize using variables and classes from the **Element Plus** UI library.
    *   All custom component styles MUST be `scoped`.
3.  **Directory Structure**:
    *   Reusable components are located in `vue-frontend/src/components/`.
    *   Pinia stores are located in `vue-frontend/src/stores/`.
4.  **Testing**:
    *   All significant business logic in components and stores requires unit tests using **Vitest**.
    *   Critical user flows should have E2E tests using **Playwright**.
5.  **Code Formatting**: Adhere strictly to the rules in the root `.prettierrc.json` file.
6.  **API Integration**: All backend API calls must be routed through the abstractions in `vue-frontend/src/services/api.js`.

**Objective**: To maintain a clean, consistent, and maintainable codebase.

---

### 4. Boundary Management Principle (MANDATORY)

**Rule**: I will strictly adhere to the defined responsibility matrix to maximize our collaborative efficiency.

**Core Idea**: I will focus on **complex, creative, and analytical** tasks. You (the Developer) will handle **simple, deterministic, environment-dependent, and high-risk** tasks.

**My Responsibility**: If a task falls under your responsibility (e.g., deleting a file, running `npm install`), I will not attempt to perform it myself. Instead, I will provide you with a clear, explicit instruction and wait for your confirmation before proceeding.

**Collaboration Responsibility Matrix**:

| Category                          | My Responsibilities (AI)                                                                                                                                                                                                                           | Your Responsibilities (Developer)                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code Writing**            | 1. Generate full code for**new components/functions/classes**.`<br>`2. Write **boilerplate code** (e.g., tests, API calls) based on existing patterns.`<br>`3. Perform **complex code refactoring** and logic modifications. | 1. Make**minor, deterministic changes** (e.g., renaming a variable).`<br>`2. Conduct the **final code review and merge**.                                                                                                                                                                                                                                                                                                                                     |
| **File System**             | 1. Create**new files with complex logic** (`write_to_file`).`<br>`2. Perform **multiple, complex modifications** within files (`replace_in_file`).`<br>`3. **Read and analyze** the content of any file.                 | 1.**Create empty files**.`<br>`2. **Rename or move files**.`<br>`3. **Delete files**.`<br>`*(In these cases, I should provide you with a clear instruction, e.g., "Please create a new file named `x.js`.")*                                                                                                                                                                                                                                    |
| **Environment & Execution** | 1.**Analyze error logs** and outputs to propose solutions.`<br>`2. Write **complex, one-off shell commands** that can be executed non-interactively.                                                                                 | 1.**Run any installation commands** (e.g., `npm install`).`<br>`2. **Start or stop any services. Crucially, all development servers (e.g., frontend on http://localhost:5173, backend API) are considered "always-on". I will never attempt to start or stop them.**`<br>`3. **Execute any command requiring interactive input**.`<br>`4. **Perform any high-risk or destructive operations** (e.g., database migrations, `git push --force`).`<br>`*(In these cases, I should provide you with the complete command and instructions for you to execute.)* |
| **Planning & Decision**     | 1.**In-depth analysis** of the codebase to suggest improvements.`<br>`2. Create **detailed implementation plans** (`implementation_plan.md`).`<br>`3. **Draft documentation** and comments.                                | 1. Make**final architectural decisions**.`<br>`2. **Approve or veto** plans I propose.`<br>`3. **Define high-level project requirements**.                                                                                                                                                                                                                                                                                                            |

**Objective**: To leverage our respective strengths, save time and resources, and ensure a safe and efficient workflow.

---

### 5. Toolchain & Native Feature Integration Principle (MANDATORY)

**Rule**: Our collaboration will fully leverage Cline's native features to maximize efficiency and maintain clarity.

1. **Plan/Act Modes**: All non-trivial tasks MUST start in **Plan Mode** for thorough analysis and strategy definition before proceeding to **Act Mode** for implementation.
2. **Focus Chain**: All implementation work in **Act Mode** MUST be driven by a `task_progress` checklist, which is automatically managed by the Focus Chain feature. This serves as our single source of truth for task status.
3. **Workflows (`/workflows`)**: Repetitive, multi-step tasks (e.g., deployments, PR reviews) SHOULD be encapsulated into callable workflow files stored in the `.clinerules/workflows/` directory, though none are required at initiation.

**Objective**: To ensure our workflow is deeply integrated with the tool's core capabilities, creating a seamless and powerful development loop.

---

### 6. Advanced Engineering Practices Principle (MANDATORY)

**Rule**: We will adhere to a set of advanced engineering practices to ensure quality, robustness, and maintainability.

1. **Definition of Done (DoD)**: A task is only considered "done" when the following criteria are ALL met:

   * The `task_progress` checklist is 100% complete.
   * All related unit tests (Vitest) and E2E tests (Playwright) are passing.
   * The code passes all linting checks without errors or warnings.
2. **Context Confirmation**: Before executing any substantive file modifications in `Act Mode`, I MUST output a concise summary of my understanding of the current objective. I will only proceed after receiving your confirmation.
3. **Commit Message Standard**: All commit messages I propose MUST follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Example: `feat(filter): add price range slider`.
4. **Risk Management**:

   * For any change that could impact a critical user flow (e.g., authentication, data submission), my implementation plan MUST recommend the use of a feature flag.
   * The corresponding Pull Request description MUST include a clear, one-step rollback command or procedure.
5. **Resource Management (Token Efficiency)**:

   * I MUST prioritize using `replace_in_file` (diffs) over `write_to_file` for modifications.
   * I MUST NOT request or output large, monolithic code blocks. When significant context is needed, I will instead refer to the specific file and line numbers.
6. **Error Handling & Logging**:

   * Any new logic that can fail (e.g., API calls, complex data transformations) MUST be wrapped in appropriate `try...catch` blocks.
   * Critical `catch` blocks MUST include a call to a standardized logging service (e.g., `logger.error(...)`) to ensure issues are traceable.

**Objective**: To build a professional-grade, resilient, and maintainable product by embedding industry-standard engineering disciplines into our daily workflow.

---

## 以下是中文翻译，AI 不必阅读

---

# 悉尼租房 Hub 项目核心规则

本文档确立了本项目协作的基础原则和强制性工作流。这些规则不可协商，必须在所有任务中遵守，以确保开发过程精简、高效、可预测。

---

### 1. 记忆库原则（强制）

**规则**：在任何新任务开始时，我的首要动作**必须**是读取 `memory-bank/` 目录中的所有文档。这是我主要的上下文加载机制，也是后续一切行动的基础。

**目标**：确保我始终在最新、完整的项目上下文下运作，从而提升行动的准确性并减少冗余提问。

---

### 2. 标准任务执行原则（强制）

**规则**：当从「计划模式（Plan Mode）」切换到「执行模式（Act Mode）」时，我**必须**遵循标准执行工作流。这是一个内置流程，而不是由外部命令触发的。

**工作流步骤与示例**：

1.  **计划分解**：将已批准的计划转化为 `task_progress` 清单，并通过 Focus Chain 功能进行管理。*示例任务：新增 `PropertyCard.vue` 组件*
    *   `- [ ] 生成组件骨架`
    *   `- [ ] 集成 Element Plus 样式`
    *   `- [ ] 对接 API 端点`
    *   `- [ ] 使用 Vitest 编写单元测试`
2.  **迭代与验证**：针对清单上的**第一个未完成项**，一次只执行一个工具，等待反馈，成功后更新清单。这是严格的“先执行、后验证”循环。
3.  **验证**：清单完成后，我将提议一个最终验证步骤（例如，通过浏览器交互）。我将**始终假定开发环境（如 http://localhost:5173/）已在运行**，并且绝不会尝试启动或停止任何服务。
4.  **记录与完成**：在验证成功且收到您的指示后，我将**更新 `memory-bank/`**，然后使用 `<attempt_completion>`。

**目标**：确保每个任务以可预测、系统化、文档化的方式完成。

---

### 3. 技术与编码标准原则（强制）

**(内容无变化)**

---

### 4. 边界管理原则（强制）

**规则**：我将严格遵守既定的责任矩阵，以最大化协作效率。

**核心理念**：我（AI）专注于**复杂、创造性与分析性**的任务；你（开发者）负责**简单、确定性、依赖环境与高风险**的任务。

**我的责任**：如果某个任务属于你的职责范围（如删除文件、运行 `npm install`），我不会尝试自行执行，而会提供明确的指令，并在收到你的确认后再继续。

**协作责任矩阵**：

| 类别                 | 我的职责（AI）                                                                                                                                                  | 你的职责（开发者）                                                                                                                                                                                                                                                                                                                        |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **代码编写**   | （无变化） | （无变化） |
| **文件系统**   | （无变化） | （无变化） |
| **环境与执行** | 1. 分析错误日志与输出并提出解决方案。<br>2. 编写复杂的一次性 Shell 命令（可非交互执行）。 | 1. 执行任何安装命令（如 `npm install`）。<br>2. **启动或停止服务。至关重要的一点是：所有开发服务器（如前端 http://localhost:5173/、后端API）都被视为“永远在线”状态。我绝不会尝试启动或停止它们。**<br>3. 执行任何需要交互输入的命令。<br>4. 执行任何高风险或破坏性操作（如数据库迁移、`git push --force`）。<br>*（此类情况下，我会提供完整命令与说明，由你执行。）* |
| **规划与决策** | （无变化） | （无变化） |

**目标**：充分发挥各自优势，节省时间与资源，确保流程安全高效。

---

### 5. 工具链与原生功能集成原则（强制）

**(内容无变化)**

---

### 6. 高级工程实践原则（强制）

**(内容无变化)**
