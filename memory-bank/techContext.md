# 技术上下文 (techContext.md)

**最新更新**: 2025年7月10日

## 1. 核心技术栈

- **后端 (backend/)**: Python 3.10+, FastAPI, Strawberry-GraphQL
- **前端 (frontend/)**: HTML5, CSS3, JavaScript (ES6+), Tailwind CSS
- **爬虫 (crawler/)**: Python, aiohttp, pandas
- **数据库 (database/)**: PostgreSQL 17+ with PostGIS 3.x
- **管理脚本 (scripts/)**: Python
- **AI工具 (mcp-server/)**: Node.js, TypeScript

## 2. 开发环境与工具

### 依赖管理
- **Python**: 项目根目录下的 `requirements.txt` 是所有Python依赖的唯一来源。
  - **注意**: 为了解决在 Windows + Python 3.13 环境下的编译问题 (特别是 `pandas` 和 `pydantic-core`)，我们已将依赖项固定到已知兼容且提供预编译二进制文件的版本。
- **Node.js**: `mcp-server/package.json` 用于管理MCP服务器的依赖。

### 本地开发 (Windows)
- **一键启动**: 双击 `start_all_services.bat` 即可启动所有服务。
- **数据更新**: 双击 `test_auto_update.bat` 可手动更新房源数据。

### 开发者启动方式
```bash
# 启动所有服务
python scripts/start_all.py

# 分别启动 (PowerShell 兼容)
python scripts/run_backend.py
cd frontend; python -m http.server 8080
cd mcp-server; npm start
```

### 环境配置
- **环境变量**: 统一由项目根目录的 `.env` 文件管理。
- **代码编辑器**: Visual Studio Code
- **数据库管理**: pgAdmin / psql

## 3. 项目结构

```
sydney-rental-platform/
├── frontend/              # 网站前端
├── backend/               # 网站后端
├── crawler/               # 房源数据爬虫
├── database/              # 数据库脚本
├── scripts/               # 管理和启动脚本
├── docs/                  # 项目文档
│   ├── memory-bank/       # AI记忆库
│   └── archive/           # 归档文档
├── uniapp-miniprogram/    # (已过时) 小程序代码
├── mcp-server/            # (开发者用) AI工具服务器
├── .github/               # GitHub Actions 工作流
├── requirements.txt       # 统一的Python依赖
└── .env                   # 环境变量
```

## 4. 部署架构 (计划)

- **前端**: Netlify 静态托管
- **后端**: Render/Railway 容器化部署
- **数据库**: Supabase / Neon (云端PostgreSQL)
- **自动化**: GitHub Actions 用于CI/CD和定时任务
