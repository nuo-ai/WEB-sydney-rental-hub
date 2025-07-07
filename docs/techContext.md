# 技术上下文 (techContext.md)

## 🚀 最新更新：项目重组后的技术架构 (2025年7月7日)

## 1. 核心技术栈

### 后端API服务 (backend/)
- **编程语言**: Python 3.10+
- **Web框架**: FastAPI
- **GraphQL库**: Strawberry-GraphQL
- **数据库ORM**: 直接使用psycopg2 (原生SQL)
- **数据库连接**: psycopg2连接池
- **数据处理**: Pandas (用于ETL)
- **部署**: 云端托管平台 (Render, Railway)

### 前端应用 (frontend/)
- **基础技术**: HTML5, CSS3, JavaScript (ES6+)
- **CSS框架**: Tailwind CSS (CDN版本)
- **状态管理**: localStorage + vanilla JS
- **部署**: Netlify + Python HTTP服务器 (开发)

### MCP服务器 (mcp-server/)
- **编程语言**: TypeScript/Node.js
- **通信协议**: stdio (Model Context Protocol)
- **构建工具**: npm + TypeScript编译器
- **用途**: 为Cline AI助手提供房源搜索工具

### 数据层 (database/)
- **数据库**: PostgreSQL 17+ with PostGIS 3.x
- **地理扩展**: PostGIS (地理空间计算)
- **ETL工具**: Python脚本 (process_csv.py)
- **数据管理**: SQL脚本 + Python管理工具

### 管理工具 (scripts/)
- **启动脚本**: Python多进程管理
- **测试工具**: API测试脚本
- **项目管理**: 一键启动/停止服务

## 2. 开发环境与工具

### 版本控制
- **Git & GitHub**: 项目版本管理
- **分支策略**: 主分支开发，功能分支合并

### 本地开发服务器
```bash
# 一键启动所有服务
python scripts/start_all.py

# 分别启动服务 (PowerShell兼容)
python scripts/run_backend.py                    # 后端API (端口8000)
cd frontend; python -m http.server 8080         # 前端服务 (端口8080)
cd mcp-server; npm start                        # MCP服务器 (stdio)
```

### 开发工具链
- **代码编辑器**: Visual Studio Code
- **Python环境**: venv虚拟环境
- **Node.js管理**: npm包管理器
- **数据库管理**: pgAdmin / psql命令行

### 环境配置
- **环境变量**: 项目根目录 `.env` 文件
- **依赖管理**: `requirements.txt` (Python) + `package.json` (Node.js)
- **配置文件**: 各模块独立配置

## 3. 新的项目结构和路径

### 导入路径修复
```python
# 修复前 (错误) - 旧结构
from server.models.property_models import Property
from server.crud.properties_crud import get_properties

# 修复后 (正确) - 新结构  
from models.property_models import Property
from crud.properties_crud import get_properties
```

### 文件组织
```
项目根目录/
├── frontend/          # 前端应用 (原sydney-rental-hub)
├── backend/           # 后端API (原rentalAU_mcp/server)
├── mcp-server/        # MCP服务器 (原sydney-rental-mcp)
├── database/          # 数据库脚本 (原rentalAU_mcp/etl + SQL)
├── scripts/           # 管理脚本 (新增)
├── docs/              # 项目文档 (原memory-bank)
└── .env              # 环境变量 (统一配置)
```

## 4. PowerShell兼容性

### 命令语法修复
```bash
# 错误语法 (不兼容PowerShell)
cd frontend && python -m http.server 8080

# 正确语法 (PowerShell兼容)
cd frontend; python -m http.server 8080
```

### 脚本执行
- **Python脚本**: 使用 `python script.py` 执行
- **多命令组合**: 使用 `;` 分隔符而不是 `&&`
- **路径处理**: 使用Python的pathlib处理跨平台路径

## 5. 第三方服务集成

### 已集成服务
- **PostgreSQL**: 本地开发 + 云端生产环境
- **PostGIS**: 地理空间计算服务
- **Tailwind CSS**: CDN方式集成

### 计划集成服务
- **支付服务**: Stripe (咨询服务付费)
- **地图服务**: Google Maps API (房源地图显示)
- **交通API**: 悉尼交通数据 (通勤时间计算)

## 6. 部署架构

### 开发环境
- **前端**: Python HTTP服务器 (localhost:8080)
- **后端**: Uvicorn开发服务器 (localhost:8000)
- **数据库**: 本地PostgreSQL实例
- **MCP**: stdio模式运行

### 生产环境 (计划)
- **前端**: Netlify静态托管
- **后端**: Render/Railway容器化部署
- **数据库**: 云端PostgreSQL (如Supabase/Neon)
- **MCP**: 独立服务器部署

## 7. 开发工作流程

### 新的启动流程
1. **环境准备**: 确保 `.env` 文件配置正确
2. **数据库启动**: 启动本地PostgreSQL服务
3. **服务启动**: 运行 `python scripts/start_all.py`
4. **验证**: 访问 http://localhost:8080 测试前端
5. **API测试**: 访问 http://localhost:8000/docs 测试后端

### 开发和调试
- **前端调试**: 浏览器开发者工具
- **后端调试**: FastAPI自动文档 + 日志输出
- **数据库调试**: psql命令行 + pgAdmin
- **MCP调试**: Cline AI助手直接测试

## 8. 性能和监控

### 本地性能指标
- **后端响应时间**: GraphQL查询 < 500ms
- **前端加载时间**: 首屏加载 < 2秒
- **数据库查询**: 地理空间查询 < 100ms
- **内存使用**: 后端 < 200MB

### 监控工具
- **日志记录**: Python logging模块
- **API监控**: FastAPI内置日志
- **数据库监控**: PostgreSQL日志
- **资源监控**: 系统任务管理器

## 9. 质量保证

### 代码质量
- **类型提示**: Python类型注解
- **代码格式**: 统一代码风格
- **错误处理**: 完善的异常处理机制
- **文档**: 详细的代码注释和API文档

### 测试策略
- **单元测试**: 核心业务逻辑测试
- **集成测试**: API端到端测试
- **功能测试**: 前端用户交互测试
- **性能测试**: 数据库查询性能测试

## 10. 扩展性考虑

### 技术扩展
- **微服务化**: 未来可拆分为独立服务
- **缓存层**: Redis缓存热点数据
- **消息队列**: 异步任务处理
- **容器化**: Docker部署支持

### 功能扩展
- **移动应用**: React Native/Flutter
- **实时通信**: WebSocket支持
- **多语言**: 国际化支持
- **AI集成**: 更多AI功能集成
