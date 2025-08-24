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

1. **Decompose Plan**: Translate the approved plan into a `task_progress` checklist, which is managed via the Focus Chain feature.
   * *Example Task: Add a new `PropertyCard.vue` component*
     * `- [ ] Generate component skeleton`
     * `- [ ] Integrate with Element Plus for styling`
     * `- [ ] Connect to API endpoint`
     * `- [ ] Write unit tests with Vitest`
2. **Iterate & Verify**: Execute one tool at a time, await feedback, and update the checklist upon success. This is a strict "act-then-verify" loop.
3. **Document & Complete**: After all checklist items are complete, perform final validation and **update the `memory-bank/`** before using `<attempt_completion>`.

**Objective**: To ensure every task is executed in a predictable, systematic, and well-documented manner.

---

### 3. Technical & Coding Standards Principle (MANDATORY)

**Rule**: All code generated or modified within this project MUST adhere to the following technical standards:

1. **Vue.js & Naming**:
   * Components MUST use the **Composition API** (`<script setup>`).
   * Component filenames MUST use `PascalCase` (e.g., `PropertyCard.vue`).
   * Pinia store files MUST use the `useXxxStore` pattern (e.g., `usePropertiesStore.js`).
2. **Styling**:
   * Prioritize using variables and classes from the **Element Plus** UI library.
   * All custom component styles MUST be `scoped`.
3. **Directory Structure**:
   * Reusable components are located in `vue-frontend/src/components/`.
   * Pinia stores are located in `vue-frontend/src/stores/`.
4. **Testing**:
   * All significant business logic in components and stores requires unit tests using **Vitest**.
   * Critical user flows should have E2E tests using **Playwright**.
5. **Code Formatting**: Adhere strictly to the rules in the root `.prettierrc.json` file.
6. **API Integration**: All backend API calls must be routed through the abstractions in `vue-frontend/src/services/api.js`.

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
| **Environment & Execution** | 1.**Analyze error logs** and outputs to propose solutions.`<br>`2. Write **complex, one-off shell commands** that can be executed non-interactively.                                                                                 | 1.**Run any installation commands** (e.g., `npm install`).`<br>`2. **Start or stop any services** (e.g., `npm run dev`, `run_backend.py`).`<br>`3. **Execute any command requiring interactive input**.`<br>`4. **Perform any high-risk or destructive operations** (e.g., database migrations, `git push --force`).`<br>`*(In these cases, I should provide you with the complete command and instructions for you to execute.)* |
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

1. **计划分解**：将已批准的计划转化为 `task_progress` 清单，并通过 Focus Chain 功能进行管理。*示例任务：新增 `PropertyCard.vue` 组件*
   * `- [ ] 生成组件骨架`
   * `- [ ] 集成 Element Plus 样式`
   * `- [ ] 对接 API 端点`
   * `- [ ] 使用 Vitest 编写单元测试`
2. **迭代与验证**：一次只执行一个工具，等待反馈，成功后更新清单。这是严格的“先执行、后验证”循环。
3. **记录与完成**：在所有清单项目完成后，进行最终验证，并在使用 `<attempt_completion>` 之前**更新 `memory-bank/`**。

**目标**：确保每个任务以可预测、系统化、文档化的方式完成。

---

### 3. 技术与编码标准原则（强制）

**规则**：在本项目中生成或修改的所有代码必须遵循以下技术标准：

1. **Vue.js 与命名**：
   * 组件必须使用 **Composition API**（`<script setup>`）。
   * 组件文件名必须使用 `PascalCase`（如 `PropertyCard.vue`）。
   * Pinia store 文件必须采用 `useXxxStore` 命名模式（如 `usePropertiesStore.js`）。
2. **样式**：
   * 优先使用 **Element Plus** UI 库提供的变量与类。
   * 所有自定义组件样式必须为 `scoped`。
3. **目录结构**：
   * 可复用组件位于 `vue-frontend/src/components/`。
   * Pinia stores 位于 `vue-frontend/src/stores/`。
4. **测试**：
   * 组件与 stores 中的重要业务逻辑需要使用 **Vitest** 编写单元测试。
   * 关键用户流程应使用 **Playwright** 编写端到端（E2E）测试。
5. **代码格式**：严格遵循根目录 `.prettierrc.json` 的规则。
6. **API 集成**：所有后端 API 调用必须通过 `vue-frontend/src/services/api.js` 中的抽象层进行。

**目标**：保持代码库干净、一致、可维护。

---

### 4. 边界管理原则（强制）

**规则**：我将严格遵守既定的责任矩阵，以最大化协作效率。

**核心理念**：我（AI）专注于**复杂、创造性与分析性**的任务；你（开发者）负责**简单、确定性、依赖环境与高风险**的任务。

**我的责任**：如果某个任务属于你的职责范围（如删除文件、运行 `npm install`），我不会尝试自行执行，而会提供明确的指令，并在收到你的确认后再继续。

**协作责任矩阵**：

| 类别                 | 我的职责（AI）                                                                                                                                                  | 你的职责（开发者）                                                                                                                                                                                                                                                                                                                        |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **代码编写**   | 1. 为**新组件/函数/类**生成完整代码。`<br>`2. 按既有模式编写**样板代码**（如测试、API 调用）。`<br>`3. 执行**复杂的代码重构**与逻辑修改。 | 1. 进行**小型、确定性修改**（如变量重命名）。`<br>`2. 执行**最终代码审查与合并**。                                                                                                                                                                                                                                          |
| **文件系统**   | 1. 创建包含复杂逻辑的新文件（`write_to_file`）。`<br>`2. 在文件内执行多处、复杂的修改（`replace_in_file`）。`<br>`3. **读取并分析**任意文件内容。 | 1.**创建空文件**。`<br>`2. **重命名或移动文件**。`<br>`3. **删除文件**。`<br>`*（此类情况下，我应给出清晰指令，例如：“请创建名为 `x.js` 的新文件”。）*                                                                                                                                                      |
| **环境与执行** | 1.**分析错误日志**与输出并提出解决方案。`<br>`2. 编写**复杂的一次性 Shell 命令**（可非交互执行）。                                                | 1.**执行任何安装命令**（如 `npm install`）。`<br>`2. **启动或停止服务**（如 `npm run dev`、`run_backend.py`）。`<br>`3. **执行任何需要交互输入的命令**。`<br>`4. **执行任何高风险或破坏性操作**（如数据库迁移、`git push --force`）。`<br>`*（此类情况下，我会提供完整命令与说明，由你执行。）* |
| **规划与决策** | 1. 对代码库进行**深入分析**并提出改进建议。`<br>`2. 创建**详细的实现计划**（`implementation_plan.md`）。`<br>`3. **起草文档**与注释。   | 1. 作出**最终架构决策**。`<br>`2. **批准或否决**我提出的计划。`<br>`3. **定义高层项目需求**。                                                                                                                                                                                                                       |

**目标**：充分发挥各自优势，节省时间与资源，确保流程安全高效。

---

### 5. 工具链与原生功能集成原则（强制）

**规则**：我们的协作将充分利用 Cline 的原生功能，以最大化效率并保持清晰。

1. **Plan/Act 模式**：所有非琐碎任务**必须**先在 **Plan Mode** 完成全面分析与策略制定，再进入 **Act Mode** 实施。
2. **Focus Chain**：在 **Act Mode** 中的所有实现工作**必须**由 `task_progress` 清单驱动，并由 Focus Chain 自动管理。该清单是我们任务状态的单一可信来源。
3. **工作流（`/workflows`）**：重复的多步骤任务（如部署、PR 审阅）**应**封装为可调用的工作流文件，存放于 `.clinerules/workflows/` 目录；起步阶段可不强制提供。

**目标**：确保我们的工作流与工具核心能力深度融合，形成无缝而强大的开发闭环。

---

### 6. 高级工程实践原则（强制）

**规则**：我们将遵循一组高级工程实践，确保质量、稳健性与可维护性。

1. **完成定义（DoD）**：只有当以下条件**全部满足**时，任务才被视为“完成”：
   * `task_progress` 清单 100% 完成；
   * 相关单元测试（Vitest）与端到端测试（Playwright）全部通过；
   * 代码通过所有 Lint 检查，无错误或告警；
2. **上下文确认**：在 **Act Mode** 中执行任何实质性的文件修改之前，我**必须**输出一段我对当前目标的简明理解，并在收到你的确认后再继续。
3. **提交信息规范**：我提出的所有提交信息**必须**遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。例如：`feat(filter): add price range slider`。
4. **风险管理**：
   * 对任何可能影响关键用户流程的更改（如认证、数据提交），我的实现计划**必须**建议使用特性开关（feature flag）。
   * 相应的 Pull Request 描述**必须**包含清晰的一步回滚命令或流程。
5. **资源管理（Token 效率）**：
   * 对于修改，我**必须**优先使用 `replace_in_file`（diff）而非 `write_to_file`。
   * 我**不得**请求或输出大段、整体的代码块；当需要大量上下文时，将改为引用具体文件与行号。
6. **错误处理与日志**：
   * 任何可能失败的新逻辑（如 API 调用、复杂数据变换）**必须**置于合适的 `try...catch` 中。
   * 关键的 `catch` 分支**必须**调用标准化日志服务（如 `logger.error(...)`），以确保问题可追踪。

**目标**：通过将行业级工程规范融入日常工作，打造专业、可靠、且可维护的产品。
