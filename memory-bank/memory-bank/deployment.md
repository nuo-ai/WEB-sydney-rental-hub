# 部署与运行指南 (deployment.md)

**最新更新**: 2025年7月10日

本文档是运行和部署本项目的唯一权威指南，为不同需求的用户提供清晰的指引。

---

## 1. 给普通用户：如何在本地一键运行 (Windows)

这是最简单的方式，无需任何技术背景，只需在你的电脑上查看项目效果。

### 只需要3步：

1.  **确保安装了Python**:
    *   打开命令提示符 (Win+R, 输入`cmd`)，然后输入 `python --version`。
    *   如果显示版本号，说明已安装。
    *   如果没有，请从 [python.org](https://www.python.org/downloads/) 下载并安装。**安装时务必勾选 "Add Python to PATH"**。

2.  **双击启动所有服务**:
    *   双击项目中的 `start_all_services.bat` 文件。
    *   脚本会自动安装所需依赖，并启动前后端服务。
    *   成功后，会自动在浏览器中打开网站 (http://localhost:8080)。

3.  **更新房源数据 (需要时)**:
    *   双击 `test_auto_update.bat` 文件，脚本会自动获取最新的房源数据并存入数据库。

---

## 2. 给部署者：如何部署到云端服务器

本节将指导你如何将项目免费部署到云端，使其可以被公开访问。

### 2.1. 准备工作

1.  **服务账号**: 确保你拥有以下服务的GitHub账号：
    *   [GitHub](https://github.com) (代码托管)
    *   [Netlify](https://www.netlify.com) (前端托管)
    *   [Railway](https://railway.app) (后端托管)
    *   [Supabase](https://supabase.com) (数据库)

2.  **上传代码到GitHub**:
    *   在GitHub上创建一个**私有**仓库。
    *   将本项目的全部代码上传到你的仓库中。

### 2.2. 部署数据库 (Supabase)

1.  **创建项目**: 在 Supabase 上创建一个新项目，选择一个离用户近的区域，并设置一个安全的数据库密码。
2.  **初始化数据库**:
    *   项目创建后，进入 **SQL Editor**。
    *   复制 `database/setup_database.sql` 的全部内容并执行，以创建表结构和启用PostGIS扩展。
3.  **获取连接信息**: 进入 **Project Settings > Database**，找到并安全地保存数据库的连接信息。

### 2.3. 部署后端API (Railway)

1.  **创建项目**: 在 Railway 上选择 "Deploy from GitHub repo"，并选择你的仓库。
2.  **配置环境变量**:
    *   在项目的 **Variables** 标签页中，添加以下来自Supabase的数据库连接信息：
        *   `DB_NAME`: `postgres`
        *   `DB_USER`: `postgres`
        *   `DB_PASSWORD`: (你的Supabase数据库密码)
        *   `DB_HOST`: (你的Supabase主机地址)
        *   `DB_PORT`: `5432`
3.  **获取API地址**: Railway会自动根据项目根目录的`Procfile`来部署。部署成功后，在 **Settings** 中找到你的公共域名 (e.g., `your-app.up.railway.app`)。

### 2.4. 部署前端 (Netlify)

1.  **更新API地址**:
    *   在代码中，打开 `frontend/scripts/config.js` 文件。
    *   将 `production` 环境的 `API_URL` 修改为你在Railway上获得的后端API地址。
    *   提交并推送这个修改到GitHub。
2.  **连接Netlify**:
    *   在 Netlify 上选择 "Import an existing project"，并选择你的GitHub仓库。
3.  **配置部署设置**:
    *   **Base directory**: `frontend`
    *   **Publish directory**: `frontend`
    *   **Build command**: (留空)
    *   点击 "Deploy site"。

### 2.5. 设置自动化数据更新 (GitHub Actions)

1.  **配置GitHub Secrets**:
    *   在你的GitHub仓库页面，进入 **Settings > Secrets and variables > Actions**。
    *   添加与 Railway 中相同的数据库连接信息 (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)。
2.  **启用工作流**:
    *   进入仓库的 **Actions** 标签页，找到 "自动更新房源数据" 工作流并启用它。
    *   你可以手动触发一次来测试，并检查运行日志。

---

## 3. 给开发者：技术与环境细节

请参考 `memory-bank/techContext.md` 获取详细的技术栈、项目结构和开发环境信息。
