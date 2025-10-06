# JUWO桔屋找房 - Vue 3版本

🏠 基于Vue 3 + Element Plus构建的现代化房源搜索平台

## 🎯 项目概述

这是JUWO桔屋找房项目的Vue 3重构版本，采用现代化的前端技术栈，为海外留学生提供专业的澳洲租房服务。

### ✨ 核心特性

- 🎨 **JUWO品牌设计** - 采用#FF5824橙色主题的专业UI设计
- 🔍 **智能搜索筛选** - 区域自动补全 + 高级筛选面板
- 📱 **响应式设计** - 完美适配移动端、平板端、桌面端
- 💖 **收藏功能** - 本地收藏管理，后续集成用户系统
- 🏗️ **组件化架构** - 可维护、可扩展的现代前端架构

## 🛠️ 技术栈

### 核心框架
- **Vue 3** - 现代化前端框架
- **Element Plus** - 专业UI组件库
- **Vite** - 快速构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理

### 开发工具
- **ESLint** - 代码质量检查
- **Prettier** - 代码格式化
- **Font Awesome** - 图标库

### API集成
- **Axios** - HTTP客户端
- **FastAPI后端** - 房源数据API (localhost:8000)

## 📋 功能优先级

根据JUWO业务需求，功能按以下优先级开发：

1. 🥇 **房源搜索和筛选** (已完成)
2. 🥈 **用户账户系统** (规划中)
3. 🥉 **收藏功能** (已完成基础版)
4. 4️⃣ **在线咨询/联系** (已完成基础版)
5. 5️⃣ **地图找房功能** (占位页面)
6. 6️⃣ **对比功能** (待开发)

## 🚀 快速开始

### 环境要求
- Node.js 20.x+
- pnpm 8+

### 安装步骤

```bash
# 1. 安装依赖（仓库根目录）
pnpm install

# 2. 启动开发服务器
pnpm --filter @web-sydney/web dev

# 3. 访问应用
open http://localhost:5173
```

### 后端API
确保后端服务正在运行：
```bash
# 在主项目目录
python scripts/run_backend.py
# 后端将运行在 http://localhost:8000
```

## 📁 项目结构

```
apps/web/
├── src/
│   ├── components/          # 可复用组件
│   │   ├── PropertyCard.vue    # 房源卡片
│   │   ├── SearchBar.vue       # 搜索栏
│   │   ├── FilterPanel.vue     # 筛选面板
│   │   └── Navigation.vue      # 导航组件
│   ├── views/               # 页面组件
│   │   ├── Home.vue            # 首页
│   │   ├── Favorites.vue       # 收藏页
│   │   ├── PropertyDetail.vue  # 房源详情
│   │   ├── Map.vue            # 地图页面
│   │   ├── Chat.vue           # AI助手
│   │   └── Profile.vue        # 个人中心
│   ├── stores/              # Pinia状态管理
│   │   └── properties.js       # 房源数据store
│   ├── services/            # API服务
│   │   └── api.js             # API接口封装
│   ├── router/              # 路由配置
│   │   └── index.js           # 路由定义
│   ├── style.css            # 全局样式
│   ├── App.vue             # 根组件
│   └── main.js             # 应用入口
├── public/                  # 静态资源
├── package.json            # 项目配置
└── vite.config.js          # Vite配置
```

## 🎨 设计系统

### JUWO品牌色彩
```css
:root {
  --juwo-primary: #FF5824;        /* 主品牌色 */
  --juwo-primary-light: #FF7851;  /* 浅色变体 */
  --juwo-primary-dark: #E64100;   /* 深色变体 */
  --juwo-primary-50: #FFF3F0;     /* 背景色 */
}
```

### 响应式断点
- **移动端**: < 768px (单列布局)
- **平板端**: 768px - 1199px (双列布局)
- **桌面端**: ≥ 1200px (多列布局)

## 🔧 核心组件

### PropertyCard.vue
房源卡片组件，保持现有的580px设计标准：
- 4:3图片比例轮播
- Font Awesome图标 + 数字显示
- 中英文混合信息展示
- JUWO品牌色收藏按钮

### SearchBar.vue
搜索栏组件，支持：
- 区域/邮编自动补全
- 智能搜索匹配算法
- 多选区域标签
- 键盘导航支持

### FilterPanel.vue
筛选面板组件，包含：
- $0-$5000价格滑块
- 相邻多选房型筛选(1-2, 2-3)
- 入住时间选择
- 区域下拉选择
- 家具选项开关

## 📡 API集成

### 后端接口
```javascript
// 获取房源列表
GET /api/properties?page_size=100

// 获取房源详情  
GET /api/properties/{id}

// 搜索房源
GET /api/properties?search=keyword&filters...
```

### 状态管理
使用Pinia管理应用状态：
- 房源数据缓存
- 筛选条件状态
- 收藏列表管理
- 搜索历史

## 🌟 语言策略

基于成本考虑的中英文混合策略：
- **按钮/菜单**: 中文 (用户友好)
- **房源信息**: 英文 (节省翻译成本)
- **Features**: 中文 (本土化体验)
- **日期时间**: 中文 (用户习惯)

## 🚀 开发命令

```bash
# 开发模式
pnpm --filter @web-sydney/web dev

# 构建生产版本
pnpm --filter @web-sydney/web build

# 预览生产版本
pnpm --filter @web-sydney/web preview

# 代码检查
pnpm --filter @web-sydney/web lint

# 代码格式化
pnpm --filter @web-sydney/web format
```

## 🔮 未来扩展

### 短期计划 (1-3个月)
- [ ] 完善房源详情页
- [ ] 集成用户认证系统
- [ ] 后端收藏API对接
- [ ] Google Maps地图功能

### 中期计划 (3-6个月)
- [ ] uni-app小程序版本
- [ ] 代码复用率90%+
- [ ] 一键多端部署

### 长期计划 (6-12个月)
- [ ] APP版本开发
- [ ] 管理后台系统
- [ ] 高级AI功能

## 🛡️ 开发注意事项

### 样式规范
- 使用CSS变量维护设计一致性
- 遵循JUWO品牌色彩系统
- 保持580px房源卡片标准
- 优先使用Element Plus组件

### 代码规范
- 遵循Vue 3 Composition API
- 使用Pinia进行状态管理
- 组件名称采用PascalCase
- 文件名采用kebab-case

### API集成
- 所有API调用统一通过services/api.js
- 错误处理和加载状态管理
- 数据缓存和性能优化

## 📞 联系支持

如有问题或建议，请联系JUWO开发团队。

---

**JUWO桔屋找房** - 让海外租房更简单 🧡
