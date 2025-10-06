# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 常用开发命令

### 启动后端服务
```bash
# 从项目根目录运行
python scripts/run_backend.py

# 或直接使用 uvicorn (从项目根目录)
uvicorn backend.main:app --reload --port 8000

# Windows 用户推荐方式
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000
```

### 测试 API
```bash
# 健康检查
curl http://localhost:8000/api/health

# GraphQL 接口（在浏览器访问）
http://localhost:8000/graphql
```

### 运行 Celery（如需异步任务）
```bash
# 启动 Celery worker
celery -A backend.celery_worker.celery_app worker --loglevel=info

# 启动 Flower 监控（可选）
celery -A backend.celery_worker.celery_app flower --port=5555
```

## 架构概览

### 分层架构
本项目采用清晰的分层架构设计：

1. **API 层** (`api/`)
   - `graphql_schema.py`: GraphQL 模式定义，主要数据接口
   - `auth_routes.py`: 认证相关的 REST API 路由

2. **CRUD 层** (`crud/`)
   - `properties_crud.py`: 房源数据库操作，包含复杂的地理空间查询
   - `auth_crud.py`: 用户认证相关数据库操作
   - `commute_crud.py`: 通勤计算相关操作

3. **模型层** (`models/`)
   - `property_models.py`: 房源数据模型（Pydantic + Strawberry）
   - `user_models.py`: 用户模型
   - `commute_models.py`: 通勤相关模型

4. **服务层** (`services/`)
   - `email_service.py`: 邮件发送服务

### 核心技术栈
- **Web 框架**: FastAPI (高性能异步框架)
- **GraphQL**: Strawberry GraphQL (类型安全的 GraphQL 实现)
- **数据库**: PostgreSQL + PostGIS (地理空间扩展)
- **连接**: psycopg2 (同步) + asyncpg (异步优化检查)
- **缓存**: Redis + fastapi-cache2
- **异步任务**: Celery + Redis
- **认证**: JWT (python-jose)

### 关键设计模式

1. **数据库连接管理**
   - 使用 `get_db_conn_dependency()` 作为 FastAPI 依赖注入
   - 支持 DATABASE_URL（云数据库）和独立环境变量配置

2. **API 响应标准化**
   - 统一的 `APIResponse` 模型包装所有响应
   - 分页支持：`PaginationInfo` 和游标分页
   - 错误处理：统一的错误码和响应格式

3. **地理空间查询**
   - 使用 PostGIS 的 `ST_DWithin` 进行半径搜索
   - 通勤计算：整合大学位置、交通站点和房源位置

4. **缓存策略**
   - 使用 `@cache` 装饰器缓存频繁查询
   - 支持选择性缓存失效
   - Redis 不可用时降级到内存缓存

## 重要业务逻辑

### 房源查询系统
- 支持多维度筛选：区域、价格、卧室数、设施等
- 智能排序：按价格、距离等排序
- 地理搜索：基于坐标的半径搜索

### 通勤计算核心
- **直接步行**：计算房源到大学的直接步行时间
- **公交连接**：通过轻轨、火车、巴士站点连接的房源
- **步行速度**：1.333 m/s (80m/min)
- **站点半径**：大学到站点 1000m，房源到站点 800m

### AI 聊天系统
- 智能路由到不同 Agent（房源、法律、合同、服务）
- 返回结构化响应：消息、卡片、建议
- 集成房源查询和服务推荐

## 环境配置要求

必需的环境变量（在 .env 文件中）：
```env
# 数据库（优先使用 DATABASE_URL）
DATABASE_URL=postgresql://user:pass@host:port/dbname
# 或独立配置
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# API 安全
API_KEY=your_api_key
SECRET_KEY=your_jwt_secret

# 可选服务
REDIS_URL=redis://localhost:6379/0
GOOGLE_MAPS_API_KEY=your_google_api_key
```

## 数据库索引优化

启动时自动检查并创建的关键索引：
- `idx_properties_main_filter`: 主筛选复合索引
- `idx_properties_available_now`: Available Now 快速查询
- `idx_properties_suburb_lower`: 区域不分大小写搜索

## 调试建议

1. **日志级别**：已设置为 DEBUG，查看详细执行信息
2. **GraphQL 调试**：访问 /graphql 使用 GraphiQL 界面
3. **缓存管理**：使用 `/api/cache/stats` 查看缓存状态
4. **性能监控**：使用 Flower 监控 Celery 任务

## 注意事项

- Windows 开发时使用虚拟环境的完整路径运行 Python
- CORS 已配置为本地开发模式，生产环境需要调整
- 房源列表查询已优化，排除大字段（description, property_features）
- 数据库索引使用 CONCURRENTLY 创建，不锁表