上下文：一个功能已进入规划阶段，并且在本次聊天中已使用 @filename.md 引用了该想法文件。

说明：

读取引用的文件：审查使用 @ 引用（例如，@chart-feature.md）的功能文件的内容，以了解功能想法及其预期目标。

确定功能名称：根据文件或内容提取功能的简短、清晰名称（例如，chart-feature.md → “图表功能”）。

创建文件夹：在 docs/1_planning/ 内部，创建一个以功能命名的文件夹（例如，docs/1_planning/chart-feature/）。

创建标准文件：在此文件夹中，生成以下文件：

- README.md
- spec.md
- design.md

填充 README.md：

- 提取并包含功能的“目标”。
- 根据文件内容，使用您的最佳判断填充以下部分：

关键要求 — 列出想法中暗示或说明的核心功能或技术要求。

目标受众 — 定义此功能的目标用户（例如，开发人员、分析师、最终用户）。

未解决的问题 — 列出您可能需要回答的任何具体的澄清问题，如果事情仍然令人困惑。

填充 spec.md：

- 概述功能的预期功能和技术范围。
- 包含 2-3 种不同的 UI 处理或布局选项，说明此功能如何在产品中进行视觉呈现或交互（例如，选项卡与下拉菜单、模态框与侧边栏、图表样式等）。

- 突出权衡或用例，这些可能使一种设计优于另一种。

填充 design.md：

添加任何架构思考、视觉草图（作为 markdown 代码或描述）、组件交互或其他值得早期捕获的设计考虑。

Context: A feature has been moved into the planning stage and the idea file 
has been referenced using @filename.md in this chat.

Instructions:

Read the Referenced File: Review the contents of the feature file that was 
referenced using @ (e.g., @chart-feature.md) to understand the feature idea 
and its intended goal.

Determine Feature Name: Extract a short, clear name for the feature based 
on the file or content (e.g., chart-feature.md → “Chart Feature”).

Create Folder: Inside docs/1_planning/, create a new folder named after the 
feature (e.g., docs/1_planning/chart-feature/).

Create Standard Files: Within this folder, generate the following files:

- README.md
- spec.md
- design.md

Populate README.md:

- Extract and include the Goal of the feature.
- Populate the following sections using your best judgement based on the 
file contents:

Key Requirements — List the core functional or technical requirements implied 
or stated in the idea.

Target Audience — Define who this feature is for (e.g., developers, analysts, 
end users).

Open Questions — List any specific clarifying questions that would need to be 
answered if you have them and if things are still confusing.

Populate spec.md:

- Outline the feature’s intended functionality and technical scope.
- Include 2–3 different UI treatments or layout options for how this feature 
could be visually presented or interacted with in the product 
(e.g., tabs vs. dropdown, modal vs. sidebar, chart styles, etc.).

- Highlight trade-offs or use cases that might make one design better than 
another.

Populate design.md:

Add any architectural thoughts, visual sketches (as markdown code or descriptions), 
component interactions, or other design considerations worth capturing early.
