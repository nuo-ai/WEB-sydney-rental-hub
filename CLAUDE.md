# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 重要原则

- 当用户提供 Figma 原型图时，请务必 100% 按照原型图的所有内容进行编码，不要自行改动
- 任务结束后，不要去尝试打开前后端服务器，它们一直在本地运行（http://localhost:5173/）

## 项目概述

Sydney Rental Hub 是一个房源租赁平台，使用 Vue 3 + Element Plus 前端和 Python FastAPI 后端。项目采用 Memory-Bank-Driven Development 模式，所有产品需求、技术架构、开发计划都统一记录在 `/memory-bank` 目录中。

### 重要文档
- **`memory-bank/projectbrief.md`**: 项目核心问题和目标
- **`memory-bank/productContext.md`**: 用户故事和核心交互流程
- **`memory-bank/systemPatterns.md`**: 系统设计和运作方式
- **`memory-bank/techContext.md`**: 技术栈和开发环境设置
- **`memory-bank/activeContext.md`**: 当前工作焦点和下一步计划
- **`memory-bank/progress.md`**: 开发路线图和当前进展

## 开发命令

### Vue 前端开发
```bash
cd vue-frontend
npm install          # 安装依赖
npm run dev         # 启动开发服务器 (localhost:5173)
npm run build       # 构建生产版本
npm run lint        # 运行 ESLint 检查
npm run format      # 格式化代码
```

### 后端 API 开发
```bash
# 在项目根目录
python scripts/run_backend.py   # 启动 FastAPI 后端 (localhost:8000)

# 或手动启动
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 数据库和缓存
```bash
# Redis 缓存服务
redis-server          # 启动 Redis（用于 API 缓存）
redis-cli FLUSHDB    # 清除缓存

# 数据存储在 Supabase 云数据库（PostgreSQL）
```

## 技术架构

### 前端架构 (Vue 3)
```
vue-frontend/
├── src/
│   ├── components/        # 可复用组件（PropertyCard, SearchBar, FilterPanel 等）
│   ├── views/            # 页面组件（HomeView, PropertyDetail, Favorites 等）
│   ├── stores/           # Pinia 状态管理
│   ├── services/         # API 服务层
│   ├── router/           # Vue Router 配置
│   └── style.css         # 全局样式（JUWO 品牌主题）
```

### 后端架构 (FastAPI)
```
backend/
├── main.py              # FastAPI 应用入口
├── models/              # 数据模型
├── crud/                # 数据库操作
├── api/                 # API 路由和 GraphQL
└── config/              # 配置文件
```

### API 响应格式
所有 API 端点使用统一格式：
```json
{
  "status": "success/error",
  "data": {},
  "pagination": {},
  "error": "错误信息"
}
```

## 设计系统

### JUWO 品牌色系统
```css
:root {
  --juwo-primary: #FF5824;        /* 主品牌色 */
  --juwo-primary-light: #FF7851;  /* 浅色变体 */
  --juwo-primary-dark: #E64100;   /* 深色变体 */
  --juwo-primary-50: #FFF3F0;     /* 背景色 */
}
```

### 统一设计规范
- **圆角**: 6px 统一圆角
- **边框**: 1px 细边框 (#E3E3E3)
- **间距**: 12px 组件间距，24px 卡片间距
- **宽度**: 580px 房源卡片，520px 搜索框，48px 按钮

## 当前状态

### 服务运行状态
- Vue 前端: `http://localhost:5173` ✅
- Python 后端: `http://localhost:8000` ✅
- 数据库: Supabase 云数据库 (AWS 悉尼区域) ✅
- Redis 缓存: 15 分钟 TTL ✅

### 数据统计
- 房源总数: 约 2045 条
- 覆盖区域: 35 个悉尼地区
- API 响应时间: < 500ms
- 前端加载时间: < 2 秒

## 开发规范

### 代码风格
- 使用 Vue 3 Composition API + `<script setup>` 语法
- 遵循 ESLint + Prettier 配置
- 使用 CSS 变量而非硬编码值
- 组件命名使用 PascalCase

### Git 提交
- 使用语义化提交信息
- 主分支: `main`
- 功能分支: `feature/功能名称`

### 测试和验证
```bash
# 检查 Vue 应用
curl -s http://localhost:5173/

# 检查 API 代理
curl -s http://localhost:5173/api/properties

# 测试后端 API
curl -s http://localhost:8000/api/properties?page_size=1
```

## 注意事项

1. **修改代码前必读**：
   - 查看 `memory-bank/INDEX.md` 了解整体架构
   - 检查 `backend/API_ENDPOINTS.md` 确认接口格式
   - 验证相关组件的依赖关系

2. **调试技巧**：
   - 浏览器控制台 -> Network -> XHR 查看 API 调用
   - Vue DevTools -> Pinia 标签查看状态
   - 使用 curl 测试后端 API

3. **性能优化**：
   - 图片使用懒加载
   - 路由组件使用动态导入
   - API 响应启用 Redis 缓存

4. **安全注意**：
   - 不要提交敏感信息（API keys, tokens）
   - 使用 DOMPurify 处理用户输入
   - API 请求需要包含认证头（开发中）
