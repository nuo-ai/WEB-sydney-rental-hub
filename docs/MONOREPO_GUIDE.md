# Monorepo 开发团队指南

**最后更新**: 2025-10-07

本文档旨在为开发团队提供关于本项目 Monorepo 结构的清晰指引，确保所有成员都能高效地进行本地开发、测试和协作。

---

## 1. Monorepo 核心架构

本项目采用 `pnpm` + `Turborepo` 的 Monorepo 方案，以实现代码共享、统一依赖管理和高效的任务编排。

### 1.1. 工作区布局 (Workspace)

- **管理器**: `pnpm` 作为包管理器，通过根目录的 `pnpm-workspace.yaml` 文件定义工作区。
- **结构**: 所有独立的应用或包都统一存放在 **`apps/`** 目录下。
  - `apps/web`: Vue 3 前端应用 (`@web-sydney/web`)。
  - `apps/backend`: Python FastAPI 后端服务 (`@web-sydney/backend`)。
  - `apps/mcp-server`: 模型上下文协议（MCP）服务器。
- **优势**:
  - **依赖提升 (Hoisting)**: `pnpm` 将公共依赖项提升到根目录的 `node_modules`，减少磁盘空间占用和安装时间。
  - **代码共享**: 不同包之间可以轻松共享工具、组件和类型定义。

### 1.2. 任务编排 (Task Runner)

- **工具**: `Turborepo` 是我们统一的任务执行器，通过根目录的 `turbo.json` 进行配置。
- **核心脚本**: 根 `package.json` 定义了所有工作区共享的顶层脚本：
  - `dev`: 并行启动所有应用的开发模式。
  - `build`: 构建所有应用以备生产。
  - `lint`: 对整个代码库执行静态检查。
  - `test`: 运行所有测试。
  - `typecheck`: 在整个项目中进行类型检查。
- **缓存**: Turborepo 会缓存任务的输出。如果代码没有变化，重复执行 `build` 或 `lint` 等任务会几乎瞬时完成。

---

## 2. 标准开发工作流

遵循以下步骤来设置和维护您的本地开发环境。

### 2.1. 首次设置或同步上游

1.  **拉取代码**:
    ```bash
    git pull origin main
    ```
2.  **安装依赖**: 在项目**根目录**下运行，`pnpm` 会自动安装所有工作区的依赖。这是最关键的一步。
    ```bash
    pnpm install
    ```
    *注意：如果遇到 `pnpm-lock.yaml` 合并冲突，请接受上游（incoming a.k.a. theirs）的版本，然后再次运行 `pnpm install`。*

### 2.2. 日常开发

- **启动所有服务 (推荐)**:
  在项目**根目录**运行，Turborepo 会并行启动前端和后端。
  ```bash
  pnpm dev
  ```

- **单独启动特定服务**:
  如果只想启动前端或后端，可以使用 `--filter` 标志。

  ```bash
  # 只启动 Vue 前端 (http://localhost:5173)
  pnpm --filter @web-sydney/web dev

  # 只启动 FastAPI 后端 (http://localhost:8000)
  pnpm --filter @web-sydney/backend dev
  ```

---

## 3. 常见问题 (FAQ)

**问：为什么我看不到 `apps/web/node_modules` 目录？**
答：这是正常的。`pnpm` 将所有依赖都安装在了根目录的 `node_modules` 下，并通过符号链接（symlinks）的方式让每个工作区都能访问到它们。子目录中不应存在 `node_modules`。

**问：如何添加新的共享包（例如，一个UI库）？**
答：
1. 在根目录创建 `packages/` 文件夹。
2. 在 `packages/` 下创建你的新包，例如 `packages/ui`。
3. 在根 `pnpm-workspace.yaml` 文件中添加 `'packages/*'`。
4. 在需要使用它的应用（如 `apps/web`）的 `package.json` 中，通过 `pnpm add ui@workspace:*` 来引用它。
