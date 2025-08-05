# 爬虫目录清理计划

## 分析方法
基于对主爬虫 `v5_furniture.py` 的代码分析，追踪其 `import` 语句和配置文件依赖关系。

## 必须保留的文件（生产运行必需）

### 核心程序文件
- `v5_furniture.py` - 主爬虫程序
- `enhanced_feature_extractor.py` - 主爬虫直接导入的特征提取模块

### 配置目录（整个目录保留）
- `config/` - 包含以下必需的配置文件：
  - `crawler_config.yaml` - 主配置文件
  - `furniture_keywords.yaml` - 家具关键词配置
  - `aircon_keywords.yaml` - 空调关键词配置
  - `features_config.yaml` - 特征提取配置
  - `url.txt` / `temp_urls.txt` - URL列表文件
  - 其他 `.yaml` 和 `.txt` 配置文件

### 运行时目录
- `output/` - 爬虫数据输出目录
- `logs/` - 日志目录（在 PROJECT_ROOT 级别）

## 可以安全删除的文件（开发/测试/调试文件）

### Python 脚本文件
- `comprehensive_upgrade_analysis.py` - 升级分析工具
- `enhanced_comparison_script.py` - 比较脚本
- `extract_features.py` - 特征提取开发工具
- `integration_example.py` - 集成示例
- `test_improvements.py` - 测试改进脚本
- `test_v5_upgrades.py` - 版本升级测试

### 分析报告和结果文件
- `test_results_20250805_122639.json` - 测试结果
- `progress.json` - 进度文件
- `ACCURACY_ANALYSIS.md` - 准确性分析文档
- `FINAL_UPGRADE_RESULTS.md` - 升级结果文档
- `UPGRADE_SUMMARY.md` - 升级总结文档

### 输出目录中的临时文件
- `enhanced_comparison_output/` - 比较输出目录
- `upgrade_analysis_output/` - 升级分析输出目录

## 清理后的目录结构
```
crawler/
├── v5_furniture.py              # 主爬虫
├── enhanced_feature_extractor.py # 特征提取器
├── config/                      # 配置目录（完整保留）
│   ├── crawler_config.yaml
│   ├── features_config.yaml
│   ├── furniture_keywords.yaml
│   ├── aircon_keywords.yaml
│   ├── url.txt
│   └── ...
└── output/                      # 输出目录（保留结构，可清空内容）
```

## 预期效果
- 删除 **8-10** 个不必要的文件
- 保留所有生产运行必需的文件
- 大幅简化目录结构
- 确保主爬虫 `v5_furniture.py` 正常运行

## 风险评估
- **零风险**：所有被删除的文件都不是主爬虫运行时的直接依赖
- **可恢复**：如果需要，这些文件可以从 Git 历史中恢复

## 建议执行顺序
1. 备份当前状态（Git commit）
2. 删除标记的文件
3. 测试主爬虫运行
4. 如有问题，从 Git 恢复
