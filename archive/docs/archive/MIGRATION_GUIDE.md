# 项目重组迁移指南

## 🔄 重组概述

项目已从混乱的文件结构重组为清晰的模块化结构，解决了之前"活跃仓库"混乱导致的路径问题。

## 📁 新旧目录对比

| 旧结构 | 新结构 | 说明 |
|--------|--------|------|
| `sydney-rental-hub/` | `frontend/` | 前端应用文件 |
| `rentalAU_mcp/server/` | `backend/` | 后端API服务 |
| `sydney-rental-mcp/` | `mcp-server/` | MCP服务器 |
| `rentalAU_mcp/etl/` | `database/` | 数据库脚本 |
| `*.py` (根目录) | `scripts/` | 辅助脚本 |
| `memory-bank/` | `docs/` | 项目文档 |

## 🚀 新的启动方式

### 方式1: 一键启动所有服务
```bash
python scripts/start_all.py
```

### 方式2: 分别启动服务
```bash
# 启动后端
python scripts/run_backend.py

# 启动前端
cd frontend; python -m http.server 8080

# 启动MCP服务器
cd mcp-server; npm start
```

## 🔧 需要注意的变更

### 1. 脚本路径更新
- 所有Python脚本移动到 `scripts/` 目录
- 启动脚本已更新路径配置

### 2. 配置文件
- 前端配置文件路径: `frontend/scripts/config.js`
- 后端配置: `backend/` 目录下
- 环境变量文件: 保持在项目根目录

### 3. 数据库脚本
- 数据库初始化: `database/setup_database.sql`
- ETL脚本: `database/process_csv.py`
- 数据更新: `database/update_database.py`

### 4. MCP服务器
- TypeScript源码: `mcp-server/src/`
- 编译输出: `mcp-server/build/`

## ⚠️ 迁移后检查清单

- [ ] 确认所有服务能正常启动
- [ ] 验证前后端连接正常
- [ ] 测试MCP工具功能
- [ ] 检查数据库连接
- [ ] 更新IDE工作目录配置

## 🗂️ 保留的旧目录

以下目录暂时保留，包含一些备份文件：
- `rentalAU_mcp/` - 包含一些配置文件
- `sydney-rental-hub/` - 空目录，可删除
- `src/` - 临时构建目录

## 📋 下一步清理

1. 确认新结构工作正常后
2. 删除空的旧目录
3. 整理剩余的配置文件
4. 更新Git忽略规则

## 🎯 重组带来的好处

1. **清晰的项目结构** - 按功能模块组织
2. **解决路径混乱** - 避免VSCode活跃仓库切换问题
3. **统一的启动方式** - 简化开发流程
4. **更好的可维护性** - 分离关注点
5. **标准化命名** - 使用一致的命名规范
