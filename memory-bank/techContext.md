# 技术上下文 (Technical Context)

> **验证日期**: 2025-08-21  
> **更新机制**: 每月初复审。

## 1. 技术栈现状
### 前端
- Vanilla JavaScript (ES6 模块) + HTML5 + CSS3
- TailwindCSS、Font Awesome、noUiSlider
- Google Maps JavaScript API 用于地图和通勤计算

### 后端
- Python FastAPI 与 Strawberry GraphQL
- PostgreSQL/PostGIS（通过 Supabase）
- Celery + Redis 用于异步任务和缓存

### 部署与开发
- 后端启动: `python scripts/run_backend.py`
- 前端启动: `cd frontend && python -m http.server 8080`
- `frontend/netlify.toml` 与 `frontend/scripts/config.js` 包含环境配置

## 2. 当前策略
- 整合旧前端功能，完善核心找房体验。
- MCP 服务器重建计划在 MVP 完成后再评估。
