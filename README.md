# 悉尼租房平台 (Sydney Rental Platform)

**欢迎来到本项目！**

为了确保所有协作者都能基于同一套信息进行工作，我们采用 **Memory-Bank-Driven Development (记忆库驱动开发)** 模式。

---

## 唯一的“真理之源” (The Single Source of Truth)

本项目所有的**产品需求、技术架构、开发计划和关键决策**，都统一记录在 `/memory-bank` 目录中。

**在开始任何工作之前，请务必首先阅读 `/memory-bank` 中的文档，以快速同步项目的最新状态。**

### 快速导航

- **`memory-bank/projectbrief.md`**: 项目要解决的核心问题和目标是什么？
- **`memory-bank/productContext.md`**: 我们的用户故事和核心交互流程是怎样的？
- **`memory-bank/systemPatterns.md`**: 我们的系统是如何设计和运作的？
- **`memory-bank/techContext.md`**: 我们使用什么技术？开发环境如何设置？
- **`memory-bank/activeContext.md`**: 我们当前的工作焦点和下一步计划是什么？
- **`memory-bank/progress.md`**: 我们完整的开发路线图和当前进展如何？

---

## 本地开发

1.  **安装依赖**
    ```bash
    pnpm install
    ```

2.  **启动前端开发服务器**
    要单独启动 `web` 应用，请在项目根目录运行：
    ```bash
    pnpm --filter @web-sydney/web dev
    ```
    应用将运行在 `http://localhost:5176`。

3.  **启动所有服务**
    如果您想同时启动前后端等所有服务，请运行：
    ```bash
    pnpm dev
    ```

更多详细信息，请参考 **`memory-bank/techContext.md`** 中的 “本地开发环境设置” 部分。

---

*该项目由AI软件工程师Cline协助开发和维护。*
