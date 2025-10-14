阶段门提示：实施启动

上下文：一个功能文件夹，包括规划文档，已进入实施阶段，并且该文件夹在本次聊天中被引用

说明：

1.  分析计划：阅读并理解功能文件夹的内容，重点关注 `README.md`、`spec.md` 和 `design.md`。
2.  生成任务列表：根据规范和设计，生成构建此功能所需的主要实施任务的高级清单。清晰地措辞任务（例如，“设置数据库模式更改”、“为 X 构建 API 端点”、“创建前端组件 Y”、“为 Z 编写单元测试”）。将该任务列表保存到附加文件夹中，作为 `task_list.md`。
3.  建议跟踪：建议在功能文件夹中创建 `implementation_notes.md` 文件，以跟踪详细进度、技术决策、遇到的挑战。
4.  输出：提供生成的任务清单和创建 `implementation_notes.md` 的建议。

注意
一旦您创建了计划，然后继续实施，我希望这将是一个漫长的请求链，并且您将使用许多工具调用来实现此目的。

Stage Gate Prompt: Implementation Kick-off

Context: A feature folder, including planning documents, has been moved into 
the implementation stage and the folder is referenced in this chat

Instructions:

1.  Analyze Plan: Read and understand the contents of the feature folder,
    focusing on `README.md`, `spec.md`, and `design.md`.
2.  Generate Task List: Based on the spec and design, generate a high-level 
    checklist of the main implementation tasks required to build this feature. 
    Phrase tasks clearly (e.g., "Set up database schema changes", 
    "Build API endpoint for X", "Create frontend component Y", "Write unit tests for Z").
    Save that task list into the attached folder as task_list.md
3.  Suggest Tracking: Recommend creating an `implementation_notes.md` 
    file within the feature folder to track detailed progress, technical 
    decisions, challenges encountered.
4.  Output: Provide the generated task checklist and the suggestion for creating `implementation_notes.md`.

Note
Once you have created the plan, then go ahead and implement this, I expect this
to be a long chain of requests and that you will use a number of tool calls to
achieve this.
