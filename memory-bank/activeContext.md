# 当前工作上下文 (activeContext.md)

**更新日期**: 2025年7月10日

## 🚀 最新进展：项目清理与结构优化完成！

### 当前状态：项目已准备好进行云端部署
项目结构清晰，依赖统一，过时文件已被移除。核心功能稳定，本地一键启动脚本已配置完成。

### ✅ 刚刚完成的关键任务 (2025年7月10日)

#### 1. 依赖管理统一
- **创建根`requirements.txt`**: 将`backend`和`database`的依赖合并到了项目根目录的`requirements.txt`中，作为唯一的Python依赖来源。
- **更新安装脚本**:
  - `start_all_services.bat`: 现在从根`requirements.txt`安装依赖。
  - `.github/workflows/update-data.yml`: GitHub Actions工作流现在也使用根`requirements.txt`。

#### 2. 项目结构清理
- **创建`crawler/`目录**: 为爬虫代码创建了独立的顶级目录，使其与`frontend`, `backend`等模块平行。
- **迁移爬虫**: 将爬虫代码从旧的`rentalAU_mcp/dist`移动到了新的`crawler/dist`。
- **更新脚本路径**: `scripts/automated_data_update.py`已更新，指向爬虫的新位置。
- **删除过时目录**:
  - `rentalAU_mcp/`: 整个旧的、重复的目录已被删除。
  - `prototype/`: 旧的前端原型目录已被删除。
- **归档旧文档**:
  - `MIGRATION_GUIDE.md`: 已移动到`docs/archive/`。
- **清理临时文件**:
  - `quick-demo.md`: 已删除，其内容合并到了`uniapp-miniprogram/demo-instructions.md`。

#### 3. 核心文档更新
- **`README.md`**: 已重写，反映了新的项目结构，并重点突出了一键启动脚本，使其对非技术用户更友好。

### 📊 当前项目结构
```
sydney-rental-platform/
├── frontend/              # 网站前端
├── backend/               # 网站后端
├── crawler/               # 房源数据爬虫
├── database/              # 数据库脚本
├── scripts/               # 管理和启动脚本
├── docs/                  # 项目文档
│   ├── memory-bank/       # AI记忆库
│   └── archive/           # 归档文档
├── uniapp-miniprogram/    # (已过时) 小程序代码
└── mcp-server/            # (开发者用) AI工具服务器
```

## 🎯 下一阶段核心任务：云端部署与测试

项目现在处于一个理想的状态，可以开始进行云端部署。

1.  **本地完整测试**
    - **状态**: ✅ 已完成 (2025年7月10日)
    - **详情**: 成功修复了 `requirements.txt` 中的依赖问题，解决了在 Python 3.13 环境下的编译错误。`test_auto_update.bat` 脚本现在可以完整、成功地执行，确认了本地数据管道的稳定性。

2.  **云端部署**
    - **状态**: ⏳ 未开始
    - **数据库**: 部署到Supabase。
    - **后端**: 部署到Railway或Render。
    - **前端**: 部署到Netlify。
    - **自动化**: 配置并测试GitHub Actions的定时数据更新。

3.  **更新Memory Bank**
    - 在部署完成后，更新`techContext.md`和`systemPatterns.md`以包含生产环境的URL和架构。
