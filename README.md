# 悉尼租房平台 (Sydney Rental Platform)

这是一个专为悉尼学生设计的租房平台，以“到校通勤时间”为核心，帮助用户快速找到最合适的房源。

## 快速开始 (本地开发)

本项目包含多个服务（前端、后端等）。为了简化本地开发，我们提供了一个统一的启动脚本。

**1. 环境配置**
   - 复制根目录下的 `.env.example` 文件，并重命名为 `.env`。
   - 根据你的环境（特别是Supabase数据库连接信息）填写 `.env` 文件中的必要变量。

**2. 安装依赖**
   - **后端 (Python)**:
     ```bash
     pip install -r requirements.txt
     ```
   - **MCP Server (Node.js)**:
     ```bash
     npm install --prefix mcp-server
     ```

**3. 一键启动所有服务**
   - 运行以下命令来启动后端和前端服务：
     ```bash
     python scripts/start_services.py
     ```
   - 这将启动：
     - ✅ **后端服务**: `http://localhost:8000`
     - ✅ **前端服务**: `http://localhost:8080`
   - 在终端中按 `Ctrl+C` 可以一次性关闭所有服务。

---

## 项目结构

- `backend/`: FastAPI 后端，提供GraphQL API。
- `frontend/`: 原生的 HTML/CSS/JS 前端应用。
- `mcp-server/`: 用于AI Agent集成的MCP服务器 (Node.js)。
- `database/`: 数据库迁移、ETL脚本和SQL文件。
- `scripts/`: 用于开发和管理的辅助脚本。
- `sydney-rental-taro/`: 基于Taro的跨平台小程序代码。
- `docs/` & `memory-bank/`: 项目文档和开发记忆库。

---

## 部署 (Deployment)

Taro小程序 (`sydney-rental-taro`) 已配置为可轻松部署到 [Netlify](https://www.netlify.com/)。

### 部署步骤

1.  **登录 Netlify**: 使用你的 GitHub 账户登录 Netlify。
2.  **导入项目**:
    - 在 Netlify Dashboard 中，点击 "Add new site -> Import an existing project"。
    - 选择 "Deploy with GitHub" 并授权访问此项目的 GitHub 仓库。
3.  **配置项目**:
    - Netlify 会自动检测到 `sydney-rental-taro` 目录。如果未自动检测，请将 **Base directory** 设置为 `sydney-rental-taro`。
    - Netlify 将使用 `sydney-rental-taro/netlify.toml` 中的配置来构建和部署应用。构建命令 (`npm run build:h5`) 和发布目录 (`dist`) 已预先配置好。
4.  **添加环境变量**:
    - 在项目的 "Site settings -> Build & deploy -> Environment" 中，添加后端 API 的地址。例如:
      - `VITE_API_BASE_URL` = `https://your-backend-api.com` (Taro/Vite项目通常使用 `VITE_` 前缀)
5.  **部署**: 点击 "Deploy site" 按钮。Netlify 将会自动安装依赖、构建项目并将其部署到全球CDN。

*该项目由AI软件工程师Cline协助开发和维护。*
