# Context Management & Token Optimization Best Practices

## Core Principle
My operational efficiency and token consumption are directly linked. To maintain high performance and cost-effectiveness throughout the project lifecycle, I must strictly adhere to the following context management principles. The goal is not to avoid token consumption, but to ensure every token is spent on solving core problems, preventing waste on irrelevant context and repetitive tasks.

## Workflow

### 1. Tiered Context Strategy
I must treat context as a three-tiered system and use it strategically:
-   **Long-Term Memory (LTM) - The Memory Bank**:
    -   **Purpose**: To store the project's core facts, architecture, key decisions, and infrequently changing technical background.
    -   **Protocol**: At the start of every new task, I **must** first read `activeContext.md` and `progress.md`. Then, I will load other files from the Memory Bank **on-demand and with precision**, based on what is **directly relevant** to the current task. I **must not** load all Memory Bank files at once without a clear purpose.
-   **Mid-Term Memory (MTM) - `activeContext.md`**:
    -   **Purpose**: To track the specific goals, implementation plans, obstacles, and immediate decisions of the current work cycle. This is my most frequently read and written file.
    -   **Protocol**: Before and after every tool execution, I must evaluate in my `<thinking>` block whether `activeContext.md` needs to be updated to accurately reflect my work status and next steps.
-   **Short-Term Memory (STM) - Conversation History**:
    -   **Purpose**: For immediate, sequential interaction.
    -   **Protocol**: I must recognize that STM is expensive and volatile. I should not rely on it to "remember" information beyond a few turns. Any important information (like new user requirements or key decisions) must be **immediately persisted** to `activeContext.md`.

### 2. Task-Driven Context Loading
-   When beginning a new task (or a major step), my first thought process must be: "What is the minimum information I need to complete this task?"
-   I will then formulate a plan to read only the files containing that minimum necessary information. For example, to fix a backend bug, I should only load the relevant code from the `backend/` directory and the backend-related sections of `techContext.md`, not the entire project's files.

### 3. Proactive Context "Garbage Collection"
-   **Identifying Task Completion**: When a clear sub-task is finished (e.g., "database migration," "user login UI build"), I should proactively suggest a "context consolidation" to the user.
-   **Executing Consolidation and Refresh**:
    1.  **Summarize Achievements**: Update the relevant Memory Bank files with the key outcomes, final code, and important decisions from the completed task.
    2.  **Update `progress.md`**: Clearly mark the task as complete.
    3.  **Recommend a New Task**: I should advise the user to start a new session using the `new_task` tool. This will clear the current conversation history (STM), allowing me to start the next task in a clean, low-cost environment, loading only the context relevant to the new task.

### 4. Isolate Tangential Tasks
-   When encountering "side-quests" unrelated to the core task (like local network configuration, tool installation failures), I must consciously isolate them.
-   **Protocol**:
    1.  Clearly state in `activeContext.md`: "Pausing main task to resolve [tangential issue]."
    2.  After resolving the issue, record only the **final, actionable conclusion** (e.g., "Database connection must use the pooler URL, which has been updated in .env") into the relevant Memory Bank file (like `techContext.md`) or a `.clinerules` file.
    3.  **Strictly avoid** retaining the entire verbose diagnostic process (e.g., multiple `ping` or `nslookup` attempts) in my core memory. Once resolved, the context should be refreshed immediately via `new_task` or other means to return to the main task.
