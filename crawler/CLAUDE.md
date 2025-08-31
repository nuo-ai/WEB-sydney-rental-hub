# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是悉尼租房平台的爬虫模块，负责从房产网站抓取租房信息并提取关键特征。核心功能包括：
- 批量爬取多个区域的房产数据
- 提取房产特征（家具、空调、停车位等）
- 数据清洗和格式化
- 输出到Excel/CSV文件供后端导入

## 核心命令

```bash
# 运行爬虫（主脚本）
python v5_furniture.py

# 特征提取和分析
python extract_features.py output/data/xxx.csv config/features_config.yaml

# 集成测试示例
python integration_example.py
```

## 架构说明

### 核心组件

1. **v5_furniture.py** - 主爬虫脚本
   - 从 config/url.txt 或 config/temp_urls.txt 读取URL列表
   - 使用多线程并发爬取
   - 自动重试和延迟控制
   - 输出带时间戳的CSV文件到 output/ 目录

2. **enhanced_feature_extractor.py** - 特征提取器V2
   - 基于property_features_keywords.yaml的关键词匹配
   - 实现两级判断逻辑（property_features优先，description备选）
   - 返回三态值：1（确认有）、0（确认无）、-1（未知）

3. **配置文件结构**
   ```
   config/
   ├── crawler_config.yaml          # 爬虫配置（网络、性能、输出设置）
   ├── url.txt                      # 待爬取的URL列表
   ├── property_features_keywords.yaml  # 特征关键词配置
   └── enhanced_features_config.yaml   # 增强特征配置
   ```

### 数据流程

1. URL列表 → 爬虫抓取 → HTML解析
2. 提取基础信息（价格、地址、卧室数等）
3. 提取property_features列表
4. 使用EnhancedFeatureExtractor分析特征
5. 数据清洗和格式化
6. 输出到CSV/Excel文件

## 关键技术细节

### 反爬虫处理
- 随机延迟：delay_min到delay_max之间
- 请求头伪装：模拟Chrome浏览器
- 自动重试：失败后指数退避
- 并发控制：max_workers限制

### 特征提取逻辑
- **is_furnished（家具）**: 两级判断，先查property_features，再查description
- **其他特征**: 仅基于property_features判断
- 使用关键词集合进行模糊匹配
- 返回三态值支持数据质量分析

### 性能优化
- 批量写入：减少I/O操作
- 内存管理：定期垃圾回收
- 并发爬取：多线程提高效率
- 增量保存：避免数据丢失

## 开发注意事项

1. **修改爬虫逻辑时**：
   - 注意保持v5_furniture.py的输出格式兼容性
   - 测试不同区域的URL确保兼容性
   - 检查crawler_config.yaml中的限流设置

2. **添加新特征时**：
   - 更新property_features_keywords.yaml
   - 在enhanced_feature_extractor.py中添加提取逻辑
   - 确保三态值逻辑正确实现

3. **调试技巧**：
   - 查看logs/目录下的日志文件
   - 使用integration_example.py测试特征提取
   - progress.json记录爬取进度

## 依赖管理

爬虫模块特有依赖（需额外安装）：
```bash
pip install lxml pyyaml openpyxl
```

主项目requirements.txt已包含基础依赖。

## 常见问题

1. **爬取失败**：检查网络、增加延迟、更新User-Agent
2. **特征提取不准**：检查关键词配置，分析property_features原始数据
3. **内存溢出**：减小batch_size，增加垃圾回收频率
4. **编码错误**：确保使用UTF-8编码，特别是Windows环境

## 与主项目集成

爬虫输出的CSV文件可直接导入到PostgreSQL数据库：
1. 爬虫生成CSV文件到output/目录
2. 后端使用scripts/import_data.py导入
3. 数据经过清洗后存入Supabase云数据库