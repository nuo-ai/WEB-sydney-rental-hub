# 系统模式 (System Patterns)

> **验证日期**: 2025-08-21  
> **更新机制**: 每月初复审。

## 1. 核心系统架构
本项目采用前后端分离架构：
`前端 (Browser)` ↔️ `后端 API (FastAPI)` ↔️ `数据库 (Supabase/PostgreSQL)`

- 前端负责 UI 渲染与交互。
- 后端提供 REST 与 GraphQL 接口并处理业务逻辑。

## 2. 后端设计模式
- REST 与 GraphQL 双 API。
- 分层结构：`api/`, `crud/`, `models/`, `config/`。
- 使用 PostGIS 进行地理空间查询。
- Celery + Redis 处理异步任务并提供缓存。
- 提供基本的认证与限流机制。

## 3. 前端设计模式
- ES6 模块化 JavaScript 搭配 TailwindCSS 与 Font Awesome。
- 使用本地状态与 `localStorage` 管理数据。
- 提供筛选面板、图片轮播等交互组件。

## 4. 调试与修复经验
- 通过 `curl` 验证 API 行为以定位问题。
- 确保前后端接口契约一致，避免数据不匹配。
