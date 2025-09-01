# 后端服务 (FastAPI & Celery)

本文档为后端服务提供设置和运行指南，包括 FastAPI 应用、Redis 和 Celery 异步任务队列。

## __0. 项目概述__

这个 `backend` 文件夹是您整个应用的核心后端服务，使用 Python 和 FastAPI 框架构建。它采用了现代、分层的软件架构，结构清晰，功能强大，不仅提供数据查询接口，还集成了异步任务处理能力。

__核心功能与目的__

1. __提供数据 API__：

   - __GraphQL API__: 这是后端的主要数据出口。通过 `api/graphql_schema.py` 文件，它提供了一套强大且灵活的 GraphQL 查询接口。前端和其他服务（比如我们之前分析的 `sydney-rental-mcp`）可以通过这个接口，用非常精确的条件来查询房源数据、大学通勤信息等。
   - __RESTful API__: 同时，它也提供了一些传统的 RESTful API 端点（如 `/api/properties/`），用于简单的数据获取和健康检查。
2. __处理业务逻辑__：

   - __分层架构__：项目代码被清晰地分成了几层：

     - `api/`: 负责处理进来的网络请求和定义 API 结构。
     - `crud/` (Create, Read, Update, Delete): 负责所有与数据库的直接交互，执行 SQL 查询。
     - `models/`: 定义了数据在代码中的结构（例如，一个“房源”应该包含哪些字段）。
   - __通勤计算__：后端包含了复杂的地理空间计算逻辑，用于实现核心的“大学通勤时间”查询功能。
3. __异步任务处理__：

   - 通过集成 __Celery__ (`celery_worker.py`, `tasks.py`)，后端有能力处理耗时的后台任务（例如，批量发送邮件、处理大量数据等），而不会阻塞主服务，提高了应用的响应速度和稳定性。

__技术栈__

- __框架__：FastAPI (一个高性能的 Python web 框架)。
- __API 类型__：主要使用 GraphQL (通过 Strawberry 库实现)，并辅以 RESTful API。
- __数据库交互__：使用 `psycopg2` 库直接与 PostgreSQL 数据库通信。
- __异步任务__：Celery 和 Redis。
- __配置管理__：通过 `.env` 文件和 Pydantic 模型管理环境变量和应用配置。

__工作流程__

1. 前端或 MCP 服务器向后端发送一个 HTTP 请求（比如一个 GraphQL 查询）。
2. `main.py` 接收到请求，FastAPI 根据 URL 将其路由到 `api/` 目录下的相应处理函数。
3. API 层的函数负责解析请求参数，然后调用 `crud/` 目录下的函数来执行数据库查询。
4. CRUD 层的函数构建并执行 SQL 语句，从 PostgreSQL 数据库中获取原始数据。
5. 获取到的数据被转换成 `models/` 中定义的 Pydantic 模型对象。
6. 最终，FastAPI 和 Strawberry 将这些模型对象序列化成 JSON 格式，作为 HTTP 响应返回给客户端。

__总结__

`backend` 文件夹是一个功能完备、架构清晰的现代 Web 后端。它不仅仅是一个简单的数据接口，更是一个集成&#x4E86;__&#x6570;据查询、业务逻辑处理、地理空间计算和异步任&#x52A1;__&#x7B49;多种功能的综合性服务。它是您整个应用的大脑和动力核心，为所有上层应用（包括前端和 MCP 服务器）提供所需的数据和计算能力

---

## 1. 环境准备

- Python 3.8+
- Redis
- PostgreSQL

### 安装 Redis 和 PostgreSQL

对于所有平台（macOS, Windows, Linux）的本地开发，最简单直接的方式是使用 **Docker**。

**使用 Docker:**

```bash
# 启动 PostgreSQL 容器
docker run -d --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=your_password -e POSTGRES_USER=your_user -e POSTGRES_DB=your_db postgres

# 启动 Redis 容器
docker run -d -p 6379:6379 --name some-redis redis
```

**验证服务是否运行:**

- **Redis**: `redis-cli ping` (应返回 `PONG`)
- **PostgreSQL**: 使用任何数据库客户端（如 DBeaver, pgAdmin）尝试连接。

## 2. 环境变量配置

在项目根目录 (`WEB-sydney-rental-hub`) 创建一个名为 `.env` 的文件，并添加以下变量。请根据您的本地设置更新这些值。

```env
# 数据库配置
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Redis 配置
# 如果 Redis 运行在不同的主机或端口，请更新此 URL。
REDIS_URL=redis://localhost:6379/0

# API 安全配置
API_KEY=your_secret_api_key
SECRET_KEY=a_very_secret_key_for_jwt
```

## 3. 启动服务

您需要在**三个不同**的终端中启动三个独立的服务，所有命令都从项目根目录 (`WEB-sydney-rental-hub`) 执行。

### 终端 1: 启动 FastAPI 主服务

此服务处理所有的 API 请求。

**通用/macOS/Linux:**

```bash
uvicorn backend.main:app --reload --port 8000
```

**Windows (推荐的可靠方式):**

```bash
# 确保你已激活虚拟环境 (.venv\Scripts\activate)
```

.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000

```


```

```

```

服务启动后，您可以在 `http://localhost:8000` 访问它。

### 终端 2: 启动 Celery 异步任务工人

此服务在后台处理耗时任务（如发送邮件、数据处理）。

```bash
celery -A backend.celery_worker.celery_app worker --loglevel=info
```

### 终端 3: (可选) 启动 Celery Flower 监控面板

Flower 是一个用于监控和管理 Celery 集群的 Web 工具，在开发过程中强烈推荐使用。

首先，如果尚未安装，请安装它:

```bash
pip install flower
```

然后运行:

```bash
celery -A backend.celery_worker.celery_app flower --port=5555
```

之后您可以在 `http://localhost:5555` 访问 Flower 的监控面板。

## 4. API 端点说明

本后端提供两种主要的 API 接口：

- **RESTful API**:

  - `GET /api/properties/`: 获取房源列表。这是**前端应用**主要使用的数据接口。
  - `GET /api/health`: 健康检查端点。
- **GraphQL API**:

  - `POST /graphql`: 提供复杂的、结构化的数据查询能力。此接口主要供**AI助手或MCP服务器**等高级客户端使用，可以进行精确的通勤时间计算、多条件筛选等。
  - 访问 `http://localhost:8000/graphql` 可以在浏览器中打开 GraphiQL 界面进行交互式查询。

## 5. 故障排查 (Troubleshooting)

### Q1: API 请求返回 `403 Forbidden` 或认证错误？

**原因**: 这通常是由于 API Key 不匹配或未提供。后端服务默认需要一个 `X-API-Key` 请求头进行验证。
**解决方案**:

1. 检查您的客户端（如 Postman, curl 或前端代码）是否在请求头中正确地包含了 `X-API-Key`。
2. 确保请求头中的 key 值与您在 `.env` 文件中设置的 `API_KEY` 完全一致。
3. 在调试期间，您可以临时修改 `backend/main.py` 中的 `get_api_key` 函数来绕过验证，以定位问题。

### Q2: 浏览器控制台报告 `CORS` 错误？

**原因**: 当您在本地同时运行前端和后端服务时（例如，前端在 `localhost:8081`，后端在 `localhost:8000`），浏览器的安全策略会阻止跨域请求。
**解决方案**:

1. 检查 `backend/main.py` 中的 `CORSMiddleware` 配置。
2. 对于本地开发，最简单的解决方法是允许所有来源。确保配置如下：
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"], # 允许所有来源
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
3. 修改后，Uvicorn 的 `--reload` 标志会自动重启服务器，使新配置生效。

### Q3: Uvicorn 启动失败，提示 "无法找到文件" (Windows)？

**原因**: Windows 的命令行启动器可能无法正确解析虚拟环境中的路径。
**解决方案**: 不要直接运行 `uvicorn`，而是明确地使用虚拟环境中的 Python 解释器来运行 `uvicorn` 模块，如下所示：

```bash
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```
