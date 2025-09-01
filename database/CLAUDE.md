# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述
这是悉尼租房平台的数据库管理系统，负责房源数据的ETL（提取、转换、加载）流程和数据库维护。

## 核心命令

```bash
# 运行ETL数据更新流程
python update_database.py

# 执行数据库初始化
psql -h localhost -U your_user -d your_db -f setup_database.sql

# 应用数据库迁移
psql -h localhost -U your_user -d your_db -f add_last_seen_field.sql

# 优化数据库索引
python auto_optimize_indexes.py
```

## 架构说明

### 数据流程
1. **数据源**: 爬虫生成的CSV文件 (位于 `../dist/output/*_results.csv`)
2. **ETL处理**: `update_database.py` 负责增量更新
   - 识别新增房源并插入
   - 更新已存在房源的信息
   - 标记已下架房源 (is_active = FALSE)
   - 更新 last_seen_at 时间戳
3. **数据存储**: PostgreSQL数据库 (表名: properties)

### 关键数据表结构
- **properties表**: 核心房源数据表
  - listing_id: 主键，房源唯一标识
  - is_active: 标识房源是否在线
  - last_seen_at: 最后一次在数据源中看到的时间
  - bedroom_display: 前端显示用字段 (0房显示为"Studio")
  - geom: PostGIS空间数据字段

### 核心业务逻辑
1. **增量更新机制**: 不删除旧数据，通过is_active字段管理房源状态
2. **下架判断**: 如果房源不在最新CSV中，标记为inactive
3. **数据清洗**: 
   - 布尔值转换 (TRUE/FALSE/YES/NO → bool)
   - 日期处理 (NaT → None)
   - 地理坐标转换为PostGIS格式

## 环境依赖
- PostgreSQL (含PostGIS扩展)
- Python包: pandas, psycopg2, python-dotenv
- 环境变量: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

## 开发注意事项
1. 所有SQL迁移脚本使用IF NOT EXISTS避免重复执行
2. ETL脚本具有容错机制，支持编码自动检测
3. 数据更新使用事务，确保原子性
4. 包含Webhook通知机制用于新房源提醒