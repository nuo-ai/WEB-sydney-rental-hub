#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
集成示例：如何将增强的特征提取器集成到现有的v5_furniture.py中
演示三态逻辑的实际应用和效果对比
"""

import sys
import yaml
from pathlib import Path
from enhanced_feature_extractor import EnhancedFeatureExtractor, create_enhanced_property_features_class

# 假设当前目录结构
CONFIG_DIR = Path('config')

def load_enhanced_configs():
    """加载增强的配置文件"""
    
    # 加载增强的特征配置
    enhanced_features_path = CONFIG_DIR / 'enhanced_features_config.yaml'
    if enhanced_features_path.exists():
        with open(enhanced_features_path, 'r', encoding='utf-8') as f:
            enhanced_config = yaml.safe_load(f)
            features_config = enhanced_config.get('features', [])
    else:
        print(f"⚠️ 增强配置文件不存在: {enhanced_features_path}")
        features_config = []
    
    # 加载家具关键词配置
    furniture_path = CONFIG_DIR / 'furniture_keywords.yaml'
    if furniture_path.exists():
        with open(furniture_path, 'r', encoding='utf-8') as f:
            furniture_keywords = yaml.safe_load(f)
    else:
        print(f"⚠️ 家具关键词配置不存在: {furniture_path}")
        furniture_keywords = {}
    
    # 加载空调关键词配置
    aircon_path = CONFIG_DIR / 'aircon_keywords.yaml'
    if aircon_path.exists():
        with open(aircon_path, 'r', encoding='utf-8') as f:
            aircon_keywords = yaml.safe_load(f)
    else:
        print(f"⚠️ 空调关键词配置不存在: {aircon_path}")
        aircon_keywords = {}
    
    return features_config, furniture_keywords, aircon_keywords

def compare_extractors():
    """对比原始提取器和增强提取器的效果"""
    
    print("📊 特征提取器效果对比测试")
    print("=" * 60)
    
    # 加载配置
    features_config, furniture_keywords, aircon_keywords = load_enhanced_configs()
    
    # 创建增强提取器
    enhanced_extractor = EnhancedFeatureExtractor(
        features_config=features_config,
        furniture_keywords=furniture_keywords,
        aircon_keywords=aircon_keywords
    )
    
    # 测试用例 - 涵盖各种场景
    test_cases = [
        {
            'name': '明确有家具的房源',
            'headline': 'Fully Furnished Modern Apartment',
            'description': 'This beautiful apartment comes fully furnished with modern furniture including sofa, dining table, and all appliances. Move in ready!',
            'features': ['Furnished', 'Air conditioning', 'Gas cooking'],
            'expected_issues': {
                'original': '可能正确检测有家具',
                'enhanced': '准确检测为furnished'
            }
        },
        {
            'name': '明确无家具的房源',
            'headline': 'Spacious Unfurnished Unit',
            'description': 'Property is unfurnished, tenant must provide own furniture. No appliances included except for gas stove and air conditioning.',
            'features': ['Unfurnished', 'Gas stove', 'Split system air con'],
            'expected_issues': {
                'original': '能正确检测无家具',
                'enhanced': '准确检测为unfurnished'
            }
        },
        {
            'name': '信息缺失的房源（最易误判）',
            'headline': 'Beautiful Modern Apartment',
            'description': 'Located in prime area with excellent transport. Close to shops and restaurants. Great natural light.',
            'features': ['Balcony', 'City views', 'Parking available'],
            'expected_issues': {
                'original': '❌ 可能误判为无家具、无空调等',
                'enhanced': '✅ 准确标记为unknown状态'
            }
        },
        {
            'name': '可选家具的房源',
            'headline': 'Flexible Accommodation',
            'description': 'Can be leased furnished or unfurnished depending on tenant preference. Contact us for furniture options.',
            'features': ['Flexible furnishing', 'Modern kitchen', 'Secure parking'],
            'expected_issues': {
                'original': '❌ 无法识别可选状态',
                'enhanced': '✅ 检测为optional状态'
            }
        },
        {
            'name': '否定表述的房源',
            'headline': 'Pet-Free Environment',
            'description': 'No pets allowed in this building. No gym facilities available. Beautiful apartment otherwise.',
            'features': ['No pets', 'No gym', 'Great location'],
            'expected_issues': {
                'original': '❌ 可能无法识别否定表述',
                'enhanced': '✅ 准确识别allows_pets=no, has_gym=no'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 测试用例 {i}: {test_case['name']}")
        print("-" * 40)
        print(f"标题: {test_case['headline']}")
        print(f"描述: {test_case['description'][:100]}...")
        print(f"特征列表: {test_case['features']}")
        
        # 使用增强提取器
        enhanced_result = enhanced_extractor.extract(
            json_data={},
            headline=test_case['headline'],
            description=test_case['description'],
            feature_list=test_case['features']
        )
        
        result_dict = enhanced_result.to_dict()
        
        print(f"\n📈 增强提取器结果:")
        for key, value in result_dict.items():
            if value != 'unknown':  # 只显示有明确结果的特征
                print(f"  • {key}: {value}")
        
        print(f"\n💡 预期改进:")
        print(f"  • 原始版本: {test_case['expected_issues']['original']}")
        print(f"  • 增强版本: {test_case['expected_issues']['enhanced']}")

def demonstrate_integration():
    """演示如何集成到现有代码中"""
    
    print("\n" + "=" * 60)
    print("🔧 集成指南：如何替换现有的FeatureExtractor")
    print("=" * 60)
    
    print("""
📝 集成步骤：

1️⃣ 备份现有代码
   cp v5_furniture.py v5_furniture_backup.py

2️⃣ 替换导入语句
   # 在v5_furniture.py顶部添加
   from enhanced_feature_extractor import EnhancedFeatureExtractor, create_enhanced_property_features_class

3️⃣ 修改配置加载
   # 替换load_features_config()函数以支持enhanced_features_config.yaml
   
4️⃣ 更新FeatureExtractor初始化
   # 在DomainCrawler.__init__()中替换
   self.feature_extractor = EnhancedFeatureExtractor(FEATURES_CONFIG, FURNITURE_KEYWORDS, AIRCON_KEYWORDS)

5️⃣ 更新PropertyFeatures类创建
   # 替换create_property_features_class调用
   PropertyFeatures = create_enhanced_property_features_class(FEATURES_CONFIG)

6️⃣ 测试运行
   # 使用小批量数据测试新的提取器

⚠️ 重要注意事项：
   • 输出的CSV/Excel文件结构会发生变化（从bool变为str）
   • 下游分析代码可能需要相应调整
   • 建议先在测试环境中验证效果
""")

def show_data_migration_guide():
    """展示数据迁移指南"""
    
    print("\n" + "=" * 60)
    print("📊 数据格式变化和迁移指南")
    print("=" * 60)
    
    print("""
🔄 字段值变化对比：

原始格式 (bool):          增强格式 (str):
─────────────────         ──────────────────
True                  →   'yes'
False                 →   'no' (明确否定) 或 'unknown' (信息缺失)

特殊字段:
has_air_conditioning      →   'yes'/'no'/'unknown'
furnishing_status         →   'furnished'/'unfurnished'/'optional'/'unknown'
air_conditioning_type     →   'ducted'/'split'/'reverse_cycle'/'general'/'unknown'

📈 数据质量提升：
✅ 减少误判：unknown状态避免将"信息缺失"误判为"否定事实"
✅ 增加置信度：明确区分"有"、"没有"和"不确定"
✅ 提高分析价值：为后续统计分析提供更丰富的信息

🔄 下游系统适配：
1. 数据库存储：字段类型从BOOLEAN改为VARCHAR
2. 分析脚本：布尔判断改为字符串匹配
3. 可视化图表：需要处理三态值的显示
4. 筛选逻辑：支持'unknown'作为筛选条件
""")

def create_migration_script():
    """创建数据迁移脚本示例"""
    
    migration_script = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据迁移脚本：将原有的布尔值数据转换为三态字符串值
用于升级现有数据库/CSV文件到新的三态逻辑格式
"""

import pandas as pd
from pathlib import Path

def migrate_boolean_to_ternary(input_file: str, output_file: str):
    """
    将布尔值特征字段迁移为三态字符串值
    """
    
    # 需要迁移的布尔字段列表
    boolean_fields = [
        'is_furnished', 'has_air_conditioning', 'has_wardrobes', 'has_laundry',
        'has_dishwasher', 'has_parking', 'has_gas_cooking', 'has_heating',
        'has_intercom', 'has_lift', 'has_gym', 'has_pool', 'has_garbage_disposal',
        'has_study', 'has_balcony', 'has_city_view', 'has_water_view', 'allows_pets'
    ]
    
    # 读取原始数据
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    
    print(f"📁 读取文件: {input_file}")
    print(f"📊 原始数据行数: {len(df)}")
    
    # 转换布尔字段
    for field in boolean_fields:
        if field in df.columns:
            # True -> 'yes', False -> 'unknown' (因为原来的False可能是误判)
            df[field] = df[field].map({True: 'yes', False: 'unknown'})
            print(f"✅ 转换字段: {field}")
    
    # 特殊处理furnishing_status
    if 'furnishing_status' in df.columns:
        # 如果已经是字符串，保持不变；如果是布尔值，需要转换
        if df['furnishing_status'].dtype == 'bool':
            df['furnishing_status'] = df['furnishing_status'].map({
                True: 'furnished', 
                False: 'unknown'  # 保守处理，避免误判
            })
    
    # 保存迁移后的数据
    output_path = Path(output_file)
    if output_path.suffix == '.csv':
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
    else:
        df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"💾 保存迁移后文件: {output_file}")
    print(f"✅ 迁移完成!")

if __name__ == "__main__":
    # 示例用法
    input_file = "output/old_format_data.xlsx"
    output_file = "output/migrated_ternary_data.xlsx"
    
    migrate_boolean_to_ternary(input_file, output_file)
'''
    
    with open('data_migration_script.py', 'w', encoding='utf-8') as f:
        f.write(migration_script)
    
    print(f"\n📄 已创建数据迁移脚本: data_migration_script.py")

if __name__ == "__main__":
    print("🚀 房产特征提取优化方案演示")
    print("=" * 60)
    
    # 运行效果对比测试
    compare_extractors()
    
    # 展示集成指南
    demonstrate_integration()
    
    # 展示数据迁移指南
    show_data_migration_guide()
    
    # 创建迁移脚本
    create_migration_script()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n📋 下一步建议:")
    print("1. 仔细阅读集成指南和数据迁移说明")
    print("2. 在测试环境中实施增强方案")
    print("3. 对比新旧版本的提取效果")
    print("4. 根据实际效果调整关键词配置")
    print("5. 部署到生产环境")
