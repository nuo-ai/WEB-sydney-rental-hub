# 自动化ETL工作流指南

本文档详细说明了如何将爬虫生成的最新房源数据自动、高效地加载并更新到Supabase数据库中。

## 核心思想

本工作流的核心是**全自动化**，旨在消除所有手动操作（如重命名文件），以适应定时任务（如Windows计划任务）的真实工作场景。脚本会自动寻找最新的数据文件进行处理。

## 自动化流程图

```mermaid
graph TD
    A[开始: Windows计划任务触发] --> B[执行主脚本<br/>python scripts/run_etl_job.py];
    
    subgraph "主脚本内部流程"
        B --> C{1. 自动寻找最新CSV文件<br/>在 'database/crawler_output/' 目录};
        C --> D[2. 读取并处理最新CSV文件的数据];
        D --> E[3. 连接到Supabase数据库];
        E --> F[4. 智能对比并更新数据库<br/>(新增/更新/下架)];
        F --> G[5. 记录详细日志];
    end

    G --> H[结束: 数据库已是最新状态];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
    style B fill:#9f9,stroke:#333,stroke-width:2px
```

## 新增功能：智能特征提取

🎉 **重大更新 (2025-08-05)**: ETL流程现在包含**智能特征提取系统**，能够从房源描述中自动识别和提取详细的设施特征。

### 自动提取的特征
- **家具状态**: furnished/unfurnished/unknown
- **空调类型**: ducted/reverse_cycle/split_system/general  
- **设施信息**: 游泳池、健身房、停车位、宠物政策等
- **布尔特征**: has_air_conditioning, is_furnished, has_pool, has_gym, has_parking, allows_pets

详细的技术实现请参考：**[爬虫特征提取系统文档](../crawler/crawler_feature_extraction.md)**

## 操作步骤

### 1. (一次性) 配置您的爬虫

**关键约定**: 您需要将您的爬虫程序配置为，将每次抓取到的数据（`.csv` 文件）统一输出到以下目录：
`database/crawler_output/`

文件名可以包含时间戳，例如 `properties_20250804_210000.csv`。ETL脚本会自动根据文件的创建或修改时间来寻找最新的一个。

**新增**: 爬虫数据现在会自动经过特征提取处理，确保您的原始CSV包含`property_description`字段以获得最佳特征提取效果。

### 2. (一次性) 设置Windows计划任务

在Windows的“任务计划程序”中，创建一个新的计划任务。
- **触发器**: 根据您的需求设置，例如每天3次。
- **操作**: 设置为“启动程序”，并配置如下：
  - **程序/脚本**: `python.exe` (建议使用绝对路径，例如 `C:\Python39\python.exe`)
  - **添加参数(可选)**: `D:\WEB-sydney-rental-hub\scripts\run_etl_job.py` (这是我们将要创建的主控脚本)
  - **起始于(可选)**: `D:\WEB-sydney-rental-hub\`

### 3. 运行ETL任务

一旦计划任务被触发，它将执行 `run_etl_job.py` 脚本，该脚本会自动完成以下所有操作：
1.  在 `database/crawler_output/` 目录中找到最新的 `.csv` 文件。
2.  读取该文件的数据。
3.  连接到Supabase数据库。
4.  执行智能数据同步：
    - **新增**: 将新出现的房源插入数据库。
    - **更新**: 如果现有房源信息有变（例如租金），则更新它。
    - **下架**: 将数据库中存在、但最新数据文件中已消失的房源标记为“已下架” (`is_active = FALSE`)。
5.  输出详细的操作日志。

## 数据库结构变更

如果未来您的爬虫增加了**新的数据列**，您需要手动更新数据库的表结构。
1.  在 `database/` 目录下创建一个新的 `.sql` 文件（例如 `add_new_field.sql`）。
2.  在该文件中写入 `ALTER TABLE properties ADD COLUMN ...` 命令。
3.  执行我们创建的迁移脚本来应用更改：
    ```bash
    python database/apply_migration.py --file=your_new_migration_file.sql
    ```
**注意**: 只有在数据**列**发生变化时才需要执行此操作。日常的数据**行**更新是全自动的。
