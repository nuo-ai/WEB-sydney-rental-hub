# 自动化ETL工作流指南

本文档详细说明了如何将爬虫生成的最新房源数据自动、高效地加载并更新到Supabase数据库中。

## 核心思想

本工作流的核心是**链式自动化**。您只需要启动一个入口脚本（爬虫），后续所有的数据处理、数据库同步和状态通知都将自动依次触发。这极大地简化了手动操作和定时任务的配置。

## 自动化流程图

```mermaid
graph TD
    A[开始: Windows计划任务触发] --> B[1. 执行爬虫脚本<br/>python crawler/v5_furniture.py];
    B --> C[2. 爬虫完成, 自动调用通知脚本<br/>scripts/automated_data_update_with_notifications.py --run-once];
    
    subgraph "通知脚本内部流程"
        C --> D[3. 跳过爬虫, 直接进入ETL];
        D --> E[4. 调用 process_csv.py 处理最新数据];
        E --> F[5. 智能同步数据库<br/>(新增/更新/下架)];
        F --> G[6. 发送包含处理结果的Discord通知];
    end

    G --> H[结束: 数据库与通知均已更新];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
    style B fill:#9f9,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
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
  - **程序/脚本**: `python.exe` (建议使用绝对路径，例如 `C:\Python313\python.exe`)
  - **添加参数(可选)**: `crawler\v5_furniture.py` (这是唯一的入口脚本)
  - **起始于(可选)**: `D:\WEB-sydney-rental-hub\` (确保设置为项目根目录)

### 3. 运行自动化流程

一旦计划任务被触发（或您手动运行 `python crawler/v5_furniture.py`），整个链式流程将自动执行：
1.  **爬虫运行**: `v5_furniture.py` 抓取最新的房源数据并保存为CSV文件。
2.  **触发后续**: 爬虫成功后，它会自动调用 `automated_data_update_with_notifications.py` 脚本。
3.  **ETL与通知**: 通知脚本会：
    - 连接数据库。
    - 调用 `process_csv.py` 处理最新的CSV文件。
    - 将处理结果（新增、更新、下架）同步到数据库。
    - 发送一条包含详细处理结果的Discord通知。
4.  **完成**: 整个流程结束。

## 数据库结构变更

如果未来您的爬虫增加了**新的数据列**，您需要手动更新数据库的表结构。
1.  在 `database/` 目录下创建一个新的 `.sql` 文件（例如 `add_new_field.sql`）。
2.  在该文件中写入 `ALTER TABLE properties ADD COLUMN ...` 命令。
3.  执行我们创建的迁移脚本来应用更改：
    ```bash
    python database/apply_migration.py --file=your_new_migration_file.sql
    ```
**注意**: 只有在数据**列**发生变化时才需要执行此操作。日常的数据**行**更新是全自动的。
