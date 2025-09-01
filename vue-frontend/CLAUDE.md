# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Sydney Rental Hub（悉尼租房平台）- 为海外留学生提供高效的悉尼租房解决方案。

技术栈：
- **前端**: Vue 3 + Element Plus + Pinia + Vite
- **后端**: FastAPI + PostgreSQL (Supabase)
- **部署**: 本地开发环境

## 开发命令

### 前端开发
```bash
# 启动开发服务器 (http://localhost:5173)
npm run dev

# 构建生产版本
npm run build

# 代码检查和修复
npm run lint

# 格式化代码
npm run format
```

### 后端开发
```bash
# 启动后端API服务器 (http://localhost:8000)
python ../scripts/run_backend.py

# 或者直接在backend目录运行
cd ../backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 核心架构

### 前端架构
```
src/
├── views/              # 页面组件
│   ├── HomeView.vue    # 房源列表页（虚拟滚动优化）
│   ├── PropertyDetail.vue # 房源详情页（Domain.com.au风格）
│   └── Profile.vue     # 个人中心（待完成）
├── components/         # 可复用组件
│   ├── PropertyCard.vue # 房源卡片（核心展示组件）
│   └── FilterPanel.vue # 筛选面板
├── stores/            # Pinia状态管理
│   └── properties.js  # 房源数据管理（服务端分页）
└── services/          # API服务层
    └── api.js        # 后端API封装
```

### 后端架构
```
backend/
├── main.py           # FastAPI应用入口（JWT认证、分页、缓存）
├── crud/             # 数据库操作层
│   └── properties_crud.py # 房源CRUD操作
├── models/           # 数据模型
└── api/              # API路由
```

### 数据流
1. **列表页加载**: HomeView -> properties.fetchProperties() -> API服务端分页 -> 虚拟滚动展示
2. **详情页加载**: PropertyDetail -> properties.fetchPropertyDetail() -> 优先显示缓存 -> API获取完整数据
3. **筛选流程**: FilterPanel -> applyFilters() -> 服务端筛选 -> 更新列表

## 关键特性

### 性能优化
- **虚拟滚动**: 使用 @tanstack/vue-virtual 处理大量房源列表
- **服务端分页**: 默认每页20条，支持动态调整
- **智能缓存**: 详情页优先展示已有数据，避免白屏
- **API代理**: 开发环境自动代理到后端服务

### 状态管理 (Pinia)
- **filteredProperties**: 当前页房源数据（服务端分页结果）
- **currentProperty**: 当前查看的房源详情
- **favoriteIds**: 收藏列表（localStorage临时存储）
- **分页状态**: currentPage, pageSize, totalCount, hasNext/hasPrev

### API规范
- 统一响应格式: `{ status, data, pagination, error }`
- 分页参数: `page`, `page_size`
- 筛选参数: `suburb`, `min_price`, `max_price`, `bedrooms`, `property_type`

## 开发规范

### 代码风格
- 使用中文注释，解释"为什么"而非"什么"
- 遵循现有代码风格，不做大规模重构
- 保持组件简洁，单一职责

### 提交前检查
```bash
# 运行代码检查
npm run lint

# 格式化代码
npm run format
```

### 调试技巧
- Vue DevTools 已集成，可查看组件状态和Pinia store
- 后端API文档: http://localhost:8000/docs
- 网络请求通过 /api 代理到后端

## 当前重点任务

1. **个人中心页面** - 实现收藏、历史记录、订阅管理
2. **排序功能** - 价格、时间、面积排序
3. **JWT认证系统** - 完善登录注册流程
4. **收藏功能后端化** - 从localStorage迁移到数据库

## 注意事项

- 不要假设库可用性，使用前检查 package.json
- 修改前先理解现有代码结构和约定
- 保持向后兼容，避免破坏现有功能
- 详情页设计参考 Figma: https://www.figma.com/design/rE2gttYDZqtspCs8P6TrmP/