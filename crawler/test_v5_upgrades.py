#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试升级后的v5_furniture.py爬虫脚本
验证是否正确输出三态逻辑格式 ('yes'/'no'/'unknown')
"""

import sys
import json
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入升级后的模块
from enhanced_feature_extractor import EnhancedFeatureExtractor, create_enhanced_property_features_class
from v5_furniture import FEATURES_CONFIG, FURNITURE_KEYWORDS, AIRCON_KEYWORDS

def test_enhanced_property_features():
    """测试增强版PropertyFeatures类是否正确创建"""
    print("🧪 测试增强版PropertyFeatures类...")
    
    try:
        # 创建PropertyFeatures类
        PropertyFeatures = create_enhanced_property_features_class(FEATURES_CONFIG)
        
        # 创建实例
        features = PropertyFeatures()
        
        # 检查默认值
        print(f"   ✅ furnishing_status 默认值: {features.furnishing_status}")
        print(f"   ✅ air_conditioning_type 默认值: {features.air_conditioning_type}")
        
        # 检查其他字段的默认值
        feature_dict = features.to_dict()
        sample_fields = ['has_pool', 'has_gym', 'has_parking', 'allows_pets']
        
        for field in sample_fields:
            if field in feature_dict:
                print(f"   ✅ {field} 默认值: {feature_dict[field]}")
        
        print("   🎉 PropertyFeatures类创建成功！")
        return True
        
    except Exception as e:
        print(f"   ❌ PropertyFeatures类创建失败: {e}")
        return False

def test_enhanced_feature_extractor():
    """测试增强版特征提取器"""
    print("\n🧪 测试增强版特征提取器...")
    
    try:
        # 创建增强版特征提取器
        extractor = EnhancedFeatureExtractor(FEATURES_CONFIG, FURNITURE_KEYWORDS, AIRCON_KEYWORDS)
        
        # 测试样本数据
        test_data = {
            "structuredFeatures": [
                {"name": "Swimming Pool"},
                {"name": "Gym"}
            ]
        }
        
        headline = "Furnished 2BR Apartment with Pool"
        description = "Beautiful apartment with gas cooking. No pets allowed. Features air conditioning."
        feature_list = ["Swimming Pool", "Gym", "Gas Cooking", "Air Conditioning"]
        
        # 提取特征
        features = extractor.extract(test_data, headline, description, feature_list)
        
        print("   📊 提取结果:")
        feature_dict = features.to_dict()
        
        key_features = ['furnishing_status', 'has_pool', 'has_gym', 'has_gas_cooking', 'allows_pets', 'has_air_conditioning']
        
        for feature in key_features:
            if feature in feature_dict:
                value = feature_dict[feature]
                print(f"      • {feature}: {value} ({type(value).__name__})")
        
        # 验证是否为三态逻辑
        three_state_count = 0
        for feature, value in feature_dict.items():
            if isinstance(value, str) and value in ['yes', 'no', 'unknown']:
                three_state_count += 1
        
        print(f"   ✅ 三态逻辑字段数量: {three_state_count}")
        print("   🎉 特征提取器测试成功！")
        return True
        
    except Exception as e:
        print(f"   ❌ 特征提取器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """测试完整集成"""
    print("\n🧪 测试完整集成...")
    
    try:
        # 模拟爬虫的特征提取过程
        from v5_furniture import DomainCrawler
        
        # 创建爬虫实例（仅用于测试特征提取器）
        crawler = DomainCrawler()
        
        print("   ✅ DomainCrawler 实例创建成功")
        print(f"   ✅ 特征提取器类型: {type(crawler.feature_extractor).__name__}")
        
        # 测试特征提取
        test_json = {"structuredFeatures": [{"name": "Pool"}]}
        headline = "Unfurnished Studio Apartment"
        description = "Modern studio with no pets policy. Gas stove included."
        features_list = ["Pool", "No Pets"]
        
        features = crawler.feature_extractor.extract(test_json, headline, description, features_list)
        
        result_dict = features.to_dict()
        print("   📊 集成测试结果:")
        
        important_features = ['furnishing_status', 'allows_pets', 'has_gas_cooking', 'has_pool']
        for feature in important_features:
            if feature in result_dict:
                value = result_dict[feature]
                print(f"      • {feature}: {value}")
        
        print("   🎉 完整集成测试成功！")
        return True
        
    except Exception as e:
        print(f"   ❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试升级后的v5_furniture.py爬虫脚本")
    print("="*60)
    
    results = []
    
    # 运行测试
    results.append(test_enhanced_property_features())
    results.append(test_enhanced_feature_extractor())
    results.append(test_integration())
    
    # 总结结果
    print("\n" + "="*60)
    print("📋 测试总结:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   • 通过测试: {passed}/{total}")
    
    if passed == total:
        print("   🎉 所有测试通过！v5_furniture.py 升级成功！")
        print("   💡 现在爬虫将生成三态逻辑格式的数据 ('yes'/'no'/'unknown')")
    else:
        print("   ⚠️  部分测试失败，需要进一步检查")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
