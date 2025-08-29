# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 重要原则

- 当用户提供 Figma 原型图时，请务必 100% 按照原型图的所有内容进行编码，不要自行改动
- 任务结束后，不要去尝试打开前后端服务器，它们一直在本地运行（http://localhost:5173/）
- **代码注释必须严格遵循 `CODE_COMMENT_RULES.md`**：只解释"为什么"，不解释"什么"

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
│   ├── components/        # 可复用组件
│   │   ├── commute/      # 通勤相关组件（TransportModes, LocationCard）
│   │   ├── modals/       # 模态框组件（AuthModal, AddLocationModal, NameLocationModal）
│   │   └── [其他组件]    # PropertyCard, SearchBar, FilterPanel 等
│   ├── views/            # 页面组件
│   │   ├── CommuteTimes.vue  # 通勤查询页面
│   │   └── [其他页面]        # HomeView, PropertyDetail, Favorites 等
│   ├── stores/           # Pinia 状态管理
│   │   ├── auth.js       # 用户认证和地址管理
│   │   ├── commute.js    # 通勤计算和缓存
│   │   └── properties.js # 房源数据管理
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

## 当前状态（2025-01-29 更新）

### 服务运行状态
- Vue 前端: `http://localhost:5173` ✅
- Python 后端: `http://localhost:8000` ✅
- 数据库: Supabase 云数据库 (AWS 悉尼区域) ✅
- Redis 缓存: 15 分钟 TTL ✅
- Google Maps API: 已集成（含有效 API 密钥）✅
- 测试模式: 启用（localStorage 存储）✅

### 最新重大修复（2025-01-29）
- **筛选功能核心问题修复**: 
  - 解决本地数据筛选问题，改用服务端筛选（3456条 vs 300条）
  - 修复筛选计数错误（显示284改为3456）
  - 实现"全选=不筛选"智能逻辑
- **移动端交互修复**:
  - z-index层级系统重构（面板2000 < 下拉10001 < 日期10002）
  - 快速筛选下拉框显示问题解决
  - 日期选择器层级问题修复
- **用户体验优化**:
  - 筛选结果持久化（返回列表保持筛选状态）
  - "入住时间"改为"空出日期"
  - 移动端响应式布局优化

### 之前功能实现（2025-01-28）
- **JWT认证系统**: 完整的注册、登录、邮箱验证流程
- **Google Places API**: 地址自动补全、地理编码、Session Token优化
- **通勤查询功能**: 完整用户流程，支持三种交通方式
- **邮件服务**: 双模式支持（开发/生产）

### 数据统计
- 房源总数: 3456 条（服务端完整数据）
- 覆盖区域: 35 个悉尼地区
- API 响应时间: < 500ms
- 前端加载时间: < 2 秒
- 预设地址: 8 个悉尼常用地点

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

## 核心功能

### 筛选功能
- **三层筛选体系**: 搜索框 + 快速筛选按钮 + 完整筛选面板
- **服务端筛选**: 基于完整数据集（3456条）进行筛选
- **智能逻辑**: "全选=不筛选"自动识别
- **状态持久化**: 筛选结果在页面切换间保持
- **移动端优化**: 底部弹出式面板，响应式布局

### 通勤查询功能
- **入口**: PropertyDetail 页面的 "See travel times" 按钮（Figma 设计实现）
- **流程**: 认证检查 → 通勤页面 → 地址搜索 → 标签分类 → 结果展示
- **测试模式**: 默认启用，地址保存到 localStorage（`juwo-addresses` 键）
- **预设地址**: USYD, UNSW, UTS, Central Station 等澳洲常用地点
- **交通方式**: 支持驾车(DRIVING)、公交(TRANSIT)、步行(WALKING)三种模式
- **缓存策略**: 通勤结果缓存15分钟，存储在 Pinia store 中

### 模态框交互
- **AuthModal**: 注册/登录，支持邮箱验证流程
- **AddLocationModal**: 地址搜索，集成 Google Places API ✅
- **NameLocationModal**: 地址分类（Work/School/Home/Other）

### 测试模式特性
- **自动启用**: `localStorage.setItem('auth-testMode', 'true')`
- **数据存储**: 地址保存到 localStorage，无需后端 API
- **CRUD 操作**: 完整支持添加、加载、删除地址
- **错误处理**: 401 认证错误自动降级到本地存储

## 注意事项

1. **修改代码前必读**：
   - 查看 `memory-bank/INDEX.md` 了解整体架构
   - 检查 `backend/API_ENDPOINTS.md` 确认接口格式
   - 验证相关组件的依赖关系

2. **调试技巧**：
   - 浏览器控制台 -> Network -> XHR 查看 API 调用
   - Vue DevTools -> Pinia 标签查看状态
   - 使用 curl 测试后端 API
   - 模态框问题：检查 `v-model` 和事件触发

3. **性能优化**：
   - 图片使用懒加载
   - 路由组件使用动态导入
   - API 响应启用 Redis 缓存
   - 通勤结果本地缓存避免重复计算
   - Google Places Session Token 优化

4. **安全注意**：
   - 不要提交敏感信息（API keys, tokens）
   - 使用 DOMPurify 处理用户输入
   - JWT 认证已实现，testMode 用于开发
   - Google Maps API key 需要域名限制

5. **开发模式配置**：
   - `testMode = true` 跳过认证，使用 localStorage 存储
   - `EMAIL_DEV_MODE = true` 邮件打印到控制台
   - `VITE_GOOGLE_PLACES_DEV_MODE = true` 使用模拟地址数据
   - 测试模式下地址保存到 `localStorage['juwo-addresses']`
   
6. **相关文档**：
   - `AUTHENTICATION_GUIDE.md` - JWT 认证使用指南
   - `GOOGLE_PLACES_GUIDE.md` - Google Places API 集成指南
   - `FILTER_FIX_SUMMARY.md` - 筛选功能修复详细报告
   - `memory-bank/*.md` - 项目架构和进展文档

## 待优化事项

### 技术债务
- **性能**: 需要虚拟滚动处理3000+房源列表
- **代码质量**: 组件间耦合需要重构
- **测试覆盖**: 缺少单元测试和E2E测试

### 功能待实现
- 房源对比功能
- 收藏夹云同步
- 高级搜索功能
