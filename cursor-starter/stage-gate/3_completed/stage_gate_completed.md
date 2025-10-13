上下文：一个功能文件夹已进入完成阶段。该文件夹在本次聊天中被引用。

说明：

审查功能：阅读并综合引用文件夹中的内容——包括 README.md、spec.md、design.md 和任何 implementation_notes.md——以清楚地了解交付了什么、它是如何工作的以及它实现了什么结果。

生成完成摘要：编写一个简洁的 1-3 段摘要，描述：

- 功能的目的
- 构建了什么
- 任何值得注意的设计决策或功能结果

创建 summary.md：将摘要保存到同一文件夹中，作为名为 summary.md 的新文件。

记录完成情况：为组织范围的 completed_features_log.md 创建一个单行日志条目：

格式：
- **[功能名称]：** 完成于 [YYYY-MM-DD]。[目的/结果的一句话摘要]。

建议架构审查：识别 docs/_reference/architecture.md 的哪些特定部分可能需要根据此功能进行人工审查。不要直接编辑架构文件——只需建议需要考虑的目标区域（例如，“考虑由于新端点 X 更新‘API 端点’部分”）。

输出：

- 提供生成的 summary.md 的内容。
- 提供要附加到 docs/_reference/completed_features_log.md 的确切日志条目。
- 提供可能需要审查的 architecture.md 中建议部分的列表。

注意
完成此操作后，继续协助进行任何架构审查、文档更新或发布任务。此过程可能涉及多个步骤和工具调用。

Context: A feature folder has been moved into the completed stage. 
The folder is referenced in this chat.

Instructions:

Review the Feature: Read and synthesise the content within the referenced 
folder — including README.md, spec.md, design.md, and any 
implementation_notes.md — to gain a clear understanding of what was delivered,
how it works, and what outcomes it achieves.

Generate Completion Summary: Write a concise 1–3 paragraph summary describing:

- The purpose of the feature
- What was built
- Any notable design decisions or functional results

Create summary.md: Save the summary into the same folder as a new file titled 
summary.md.

Log the Completion: Create a single-line log entry for inclusion in the 
organisation-wide completed_features_log.md:

Format:
- **[Feature Name]:** Completed [YYYY-MM-DD]. 
[One-sentence summary of purpose/outcome].

Suggest Architecture Review: Identify which specific sections of 
docs/_reference/architecture.md might need a human review based on 
this feature. Do not edit the architecture file directly — 
simply suggest targeted areas for consideration 
(e.g., “Consider updating the 'API Endpoints' section due to new endpoint X”).

Output:

- Provide the content of the generated summary.md.
- Provide the exact log entry to append to 
  docs/_reference/completed_features_log.md.
- Provide the list of suggested sections in architecture.md that may 
  need review.

Note
Once you’ve completed this, continue by assisting with any architectural 
review, documentation updates, or rollout tasks. This process may involve multiple steps and tool calls.
