# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-08-19

---

## 1. 技术栈现状 (基于代码审计的事实)

经过深度代码审计，我们发现项目**已经拥有一个功能极其完善的技术栈**：

### 1.1. 前端 (基于 Old 版本的优秀实现)
- **框架**: **Vanilla JavaScript (ES6 模块化)** + **HTML5** + **CSS3**
- **样式**: **TailwindCSS** (CDN 版本)
- **地图**: **Google Maps JavaScript API** (完整集成)
- **UI 增强**: 自定义 **UIEnhancer** 系统，支持多种 UI 模式切换
- **滑块控件**: **noUiSlider** (高级价格范围选择)
- **图标**: **Font Awesome** 6.x

### 1.2. 后端 (已验证的企业级架构)
- **框架**: **Python (FastAPI)** + **Strawberry GraphQL**
- **数据库**: **Supabase (PostgreSQL + PostGIS)** 用于地理空间计算
- **异步任务**: **Celery** + **Redis** 完整集成
- **缓存**: **Redis** 缓存系统
- **安全**: API Key + JWT + 限流 完整方案

### 1.3. 部署 (现有配置)
- **前端**: **Netlify** (含 Functions 和代理)
- **后端**: 通过 `scripts/run_backend.py` 在 `localhost:8000`

---

## 2. 本地开发环境设置 (Local Development Setup)

本地开发需要同时启动两个服务：**后端 API** 和 **前端开发服务器**。

### 2.1. 环境准备
- **Python**: 3.8+
- **Node.js**: 18.x+ (用于运行前端开发环境)
- **Git**
- **Docker**: (推荐) 用于快速启动 PostgreSQL 和 Redis 服务。

### 2.2. 首次设置
1.  **克隆仓库**: `git clone <repo-url>`
2.  **配置环境变量**:
    -   在项目根目录，复制 `.env.example` 为 `.env`。
    -   在 `.env` 文件中填入你的数据库连接信息 (`DATABASE_URL`) 和 Google Maps API 密钥 (`GOOGLE_MAPS_API_KEY`)。
3.  **安装后端依赖**: `pip install -r requirements.txt`

### 2.3. 服务检查和启动流程
**重要**: 在启动任何服务前，先检查是否已有服务在运行，避免重复启动。

#### 服务状态检查命令：
```bash
# 检查后端API是否响应
curl -s http://localhost:8000/api/properties?page_size=1

# 检查前端服务器是否运行
curl -s http://localhost:8080/index.html

# 检查进程
netstat -ano | findstr :8000  # Windows
netstat -ano | findstr :8080  # Windows
```

#### 标准检查流程：
1. **检查Environment Details** - 查看"Actively Running Terminals"部分
2. **验证服务响应** - 使用curl测试API
3. **只在必要时启动** - 如果服务未运行或无响应才启动新服务

#### 启动服务（仅在检查确认需要时）：

-   **终端 1 (后端)**:
    ```bash
    # 从项目根目录运行
    python scripts/run_backend.py
    ```
    > 后端将运行在 `http://localhost:8000`。

-   **终端 2 (前端)**:
    ```bash
    # 从项目根目录运行
    cd frontend
    python -m http.server 8080
    ```
    > 前端开发服务器将运行在 `http://localhost:8080`。

#### 当前常用服务状态：
- **后端**: 通常运行在8000端口，命令 `python scripts/run_backend.py`
- **前端**: 通常运行在8080端口，命令 `cd frontend && python -m http.server 8080`

### 2.4. 关键配置文件
- **`frontend/netlify.toml`**: 包含代理规则，将 `/api/*` 请求转发到后端
- **`frontend/scripts/config.js`**: 包含 API 端点和通用配置
- **根目录 `.env`**: 包含数据库连接和 API 密钥

---

## 3. 基于发现的新开发策略 (New Development Strategy)

**核心策略**: 以 `Old/frontend/` 的优秀功能为基础，结合当前版本的 API 集成优势。

### 3.1. 功能迁移计划
- **从 Old 版本恢复**: UIEnhancer 系统、图片轮播、高级筛选面板、价格滑块等
- **从当前版本保留**: 直接 API 调用方式、Netlify Function 集成
- **新增功能**: 自动补全区域搜索、用户认证、后端同步收藏系统

### 3.2. 不需要的工作
- ❌ **React 技术栈迁移**: 现有 Vanilla JS 系统功能已足够强大
- ❌ **从零开发基础功能**: 大多数核心功能已经实现且运行良好
- ❌ **复杂的数据层重构**: 后端 API 已经非常完善

---

## 4. MCP 服务器状态 (MCP Server Status)

### 4.1. 当前状态 (调查时间: 2025-08-19)
- **位置**: `Old/mcp-server/` 目录 (完整的 TypeScript 实现)
- **状态**: **已损坏/不可用**
- **原因**: 依赖主项目后端 `localhost:8000`，但后端未运行导致连接失败

### 4.2. MCP 服务器技术细节
- **框架**: Node.js + TypeScript + MCP SDK
- **功能**: 提供 `search_properties` 和 `get_property_details` 工具
- **连接方式**: 通过 GraphQL 查询后端 API
- **部署历史**: 曾部署到 Vercel，但现已失效

### 4.3. 重建计划 (延后任务)
- **方法**: 从 GitHub 重新克隆和部署
- **优先级**: P2 (在 MVP 完成后)
- **依赖**: 需要先确保主项目后端稳定运行
- **价值**: 为 AI 助手提供租房信息查询能力

---
