---
description: "禁止 AI 调用 git MCP 工具"
globs: ["**/*"]
alwaysApply: true
---

- **核心规则**: AI代理（我）不应使用 `git` MCP 工具执行任何 Git 操作。
- **原因**: 用户已明确表示希望手动处理所有 Git 提交、分支等操作。
- **具体禁止的工具**:
  - `git_add`
  - `git_branch`
  - `git_checkout`
  - `git_commit`
  - `git_diff`
  - `git_fetch`
  - `git_pull`
  - `git_push`
  - `git_rebase`
  - `git_reset`
  - `git_status`
  - 以及所有其他 `git` MCP 工具。
- **我的职责**: 当需要进行 Git 操作时，我将明确通知您，并由您来执行具体命令。
