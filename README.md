# Sydney Rental Platform

一个专为中国学生设计的悉尼租房平台，以通勤时间到大学作为主要搜索条件。

## 🏗️ 项目结构

```
sydney-rental-platform/
├── frontend/              # 前端应用 (HTML/CSS/JS)
│   ├── index.html        # 主页
│   ├── details.html      # 房源详情页
│   ├── login.html        # 登录页
│   ├── scripts/          # JavaScript文件
│   └── functions/        # Netlify云函数
├── backend/              # 后端API (FastAPI + GraphQL)
│   ├── main.py          # 主应用入口
│   ├── db.py            # 数据库连接
│   ├── api/             # GraphQL接口
│   ├── models/          # 数据模型
│   └── crud/            # 数据操作
├── mcp-server/          # MCP服务器 (为Cline提供工具)
│   ├── src/             # TypeScript源码
│   ├── build/           # 编译后的JS文件
│   └── package.json     # Node.js依赖
├── database/            # 数据库相关
│   ├── setup_database.sql      # 数据库初始化
│   ├── process_csv.py          # 数据导入脚本
│   ├── update_database.py      # 数据更新脚本
│   └── *.sql                   # 其他SQL脚本
├── scripts/             # 辅助脚本
│   ├── run_backend.py          # 启动后端服务
│   ├── start_all.py            # 启动所有服务
│   └── test_api.py             # API测试脚本
├── docs/               # 项目文档
│   ├── projectBrief.md         # 项目概述
│   ├── systemPatterns.md       # 系统架构
│   └── progress.md             # 开发进度
└── .clinerules/        # Cline AI助手规则
    ├── chinese-communication.md
    ├── windows-powershell.md
    └── default-rules.md
```

## 🚀 快速开始

### 1. 启动后端服务
```bash
python scripts/run_backend.py
```
后端服务将运行在 http://localhost:8000

### 2. 启动前端服务
```bash
cd frontend; python -m http.server 8080
```
前端服务将运行在 http://localhost:8080

### 3. 启动MCP服务器
```bash
cd mcp-server; npm start
```

### 4. 或者一键启动所有服务
```bash
python scripts/start_all.py
```

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+), Tailwind CSS
- **后端**: Python, FastAPI, GraphQL (Strawberry)
- **数据库**: PostgreSQL + PostGIS (地理空间扩展)
- **MCP服务器**: Node.js, TypeScript
- **部署**: Netlify (前端) + Render/Railway (后端)

## 📱 主要功能

- 🎯 **大学通勤搜索** - 以到达大学的通勤时间为主要筛选条件
- 🗺️ **地图展示** - 房源位置和通勤路线可视化
- 💰 **价格筛选** - 按周租金范围筛选
- 🏠 **房型选择** - Studio, 1房, 2房等选项
- 💾 **收藏功能** - 保存感兴趣的房源
- 📱 **移动优先** - 针对手机使用优化

## 🤖 AI工具支持

项目集成了MCP (Model Context Protocol) 服务器，为Cline AI助手提供：
- 房源搜索工具
- 大学比较工具
- 房源详情查询
- 数据库操作接口

## 📄 许可证

MIT License
